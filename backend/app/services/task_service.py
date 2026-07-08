from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select

from app.extensions import db
from app.models.analysis_task import AnalysisTask, TASK_STATUSES, TASK_TYPES, utc_now
from app.models.uploaded_file import TaskInputFile, UploadedFile


ALLOWED_TRANSITIONS = {
    "pending": {"running", "failed"},
    "running": {"completed", "failed"},
    "completed": set(),
    "failed": set(),
}


class TaskValidationError(ValueError):
    pass


class TaskNotFoundError(LookupError):
    pass


class TaskTransitionError(ValueError):
    pass


def create_task(payload: Any) -> AnalysisTask:
    if not isinstance(payload, dict):
        raise TaskValidationError("请求体必须是 JSON 对象")

    task_type = payload.get("task_type")
    if task_type not in TASK_TYPES:
        raise TaskValidationError(f"task_type 必须是以下值之一：{', '.join(TASK_TYPES)}")

    name = payload.get("name") or f"{task_type} task"
    if not isinstance(name, str) or not name.strip() or len(name.strip()) > 120:
        raise TaskValidationError("name 必须是 1 到 120 个字符的字符串")

    model_key = payload.get("model_key")
    if model_key is not None and (not isinstance(model_key, str) or len(model_key) > 100):
        raise TaskValidationError("model_key 必须是长度不超过 100 的字符串")

    parameters = payload.get("parameters", {})
    if not isinstance(parameters, dict):
        raise TaskValidationError("parameters 必须是 JSON 对象")

    input_file_ids = payload.get("input_file_ids", [])
    if not isinstance(input_file_ids, list) or not all(isinstance(item, str) for item in input_file_ids):
        raise TaskValidationError("input_file_ids 必须是文件 ID 字符串数组")
    if len(input_file_ids) > 2:
        raise TaskValidationError("一个任务最多关联两个输入文件")
    if len(input_file_ids) != len(set(input_file_ids)):
        raise TaskValidationError("input_file_ids 不能包含重复文件")

    files_by_id: dict[str, UploadedFile] = {}
    if input_file_ids:
        uploaded_files = db.session.scalars(
            select(UploadedFile).where(
                UploadedFile.id.in_(input_file_ids),
                UploadedFile.deleted_at.is_(None),
            )
        ).all()
        files_by_id = {uploaded_file.id: uploaded_file for uploaded_file in uploaded_files}
        if len(files_by_id) != len(input_file_ids):
            raise TaskValidationError("一个或多个输入文件不存在")

    task = AnalysisTask(
        name=name.strip(),
        task_type=task_type,
        model_key=model_key,
        parameters_json=parameters,
    )
    for position, file_id in enumerate(input_file_ids):
        if task_type == "change_detection" and len(input_file_ids) == 2:
            role = "before" if position == 0 else "after"
        else:
            role = "primary" if position == 0 else "secondary"
        task.input_links.append(
            TaskInputFile(
                file=files_by_id[file_id],
                role=role,
                position=position,
            )
        )
    db.session.add(task)
    db.session.commit()
    return task


def list_tasks(*, page: int, page_size: int, status: str | None, task_type: str | None):
    if page < 1:
        raise TaskValidationError("page 必须大于等于 1")
    if page_size < 1 or page_size > 100:
        raise TaskValidationError("page_size 必须在 1 到 100 之间")
    if status is not None and status not in TASK_STATUSES:
        raise TaskValidationError(f"status 必须是以下值之一：{', '.join(TASK_STATUSES)}")
    if task_type is not None and task_type not in TASK_TYPES:
        raise TaskValidationError(f"task_type 必须是以下值之一：{', '.join(TASK_TYPES)}")

    statement = select(AnalysisTask).where(AnalysisTask.deleted_at.is_(None))
    if status:
        statement = statement.where(AnalysisTask.status == status)
    if task_type:
        statement = statement.where(AnalysisTask.task_type == task_type)
    statement = statement.order_by(AnalysisTask.created_at.desc())

    return db.paginate(statement, page=page, per_page=page_size, error_out=False)


def get_task(task_id: str) -> AnalysisTask:
    task = db.session.scalar(
        select(AnalysisTask).where(
            AnalysisTask.id == task_id,
            AnalysisTask.deleted_at.is_(None),
        )
    )
    if task is None:
        raise TaskNotFoundError("任务不存在")
    return task


def soft_delete_task(task_id: str) -> AnalysisTask:
    task = get_task(task_id)
    task.deleted_at = utc_now()
    db.session.commit()
    return task


def transition_task(
    task: AnalysisTask,
    new_status: str,
    *,
    error_code: str | None = None,
    error_message: str | None = None,
) -> AnalysisTask:
    if new_status not in ALLOWED_TRANSITIONS.get(task.status, set()):
        raise TaskTransitionError(f"不允许从 {task.status} 转换为 {new_status}")

    now = utc_now()
    if new_status == "running":
        task.started_at = now
    if new_status in {"completed", "failed"}:
        task.completed_at = now
        if task.started_at:
            started_at = task.started_at
            if started_at.tzinfo is None:
                started_at = started_at.replace(tzinfo=UTC)
            task.duration_ms = int((now - started_at).total_seconds() * 1000)
    if new_status == "failed":
        task.error_code = error_code or "TASK_FAILED"
        task.error_message = error_message or "任务执行失败"

    task.status = new_status
    db.session.commit()
    return task
