from flask import Blueprint, request

from app.services.task_service import (
    TaskNotFoundError,
    TaskValidationError,
    create_task,
    get_task,
    list_tasks,
    soft_delete_task,
)
from app.services.inference_service import execute_object_detection
from app.utils.responses import error_response, success_response


tasks_blueprint = Blueprint("tasks", __name__)


def parse_positive_integer(value: str | None, default: int, field_name: str) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise TaskValidationError(f"{field_name} 必须是整数") from exc


@tasks_blueprint.post("/tasks")
def create_analysis_task():
    try:
        task = create_task(request.get_json(silent=True))
    except TaskValidationError as exc:
        return error_response(code="VALIDATION_ERROR", message=str(exc), status_code=400)

    if task.task_type == "object_detection":
        task = execute_object_detection(task)
    message = "目标检测已完成" if task.status == "completed" else "任务已创建"
    return success_response(data=task.to_dict(), message=message, status_code=201)


@tasks_blueprint.get("/tasks")
def get_analysis_tasks():
    try:
        pagination = list_tasks(
            page=parse_positive_integer(request.args.get("page"), 1, "page"),
            page_size=parse_positive_integer(request.args.get("page_size"), 10, "page_size"),
            status=request.args.get("status") or None,
            task_type=request.args.get("task_type") or None,
        )
    except TaskValidationError as exc:
        return error_response(code="VALIDATION_ERROR", message=str(exc), status_code=400)

    return success_response(
        data={
            "items": [task.to_dict() for task in pagination.items],
            "page": pagination.page,
            "page_size": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
        }
    )


@tasks_blueprint.get("/tasks/<task_id>")
def get_analysis_task(task_id: str):
    try:
        task = get_task(task_id)
    except TaskNotFoundError as exc:
        return error_response(code="TASK_NOT_FOUND", message=str(exc), status_code=404)
    return success_response(data=task.to_dict())


@tasks_blueprint.delete("/tasks/<task_id>")
def delete_analysis_task(task_id: str):
    try:
        task = soft_delete_task(task_id)
    except TaskNotFoundError as exc:
        return error_response(code="TASK_NOT_FOUND", message=str(exc), status_code=404)
    return success_response(data={"id": task.id}, message="任务已删除")
