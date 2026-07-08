from typing import Any

from app.extensions import db
from app.inference import get_adapter
from app.inference.yolo_detector import ModelUnavailableError
from app.models.analysis_task import AnalysisTask
from app.models.task_result import TaskResult
from app.services.storage_service import resolve_stored_path, save_generated_image
from app.services.task_service import transition_task


class InferenceValidationError(ValueError):
    pass


def parse_confidence(parameters: dict[str, Any]) -> float:
    value = parameters.get("confidence", 0.25)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InferenceValidationError("confidence 必须是 0 到 1 之间的数字")
    confidence = float(value)
    if not 0 <= confidence <= 1:
        raise InferenceValidationError("confidence 必须是 0 到 1 之间的数字")
    return confidence


def execute_object_detection(task: AnalysisTask) -> AnalysisTask:
    transition_task(task, "running")
    try:
        if len(task.input_links) != 1:
            raise InferenceValidationError("目标检测任务必须关联一张输入图片")
        confidence = parse_confidence(task.parameters_json)
        model_key = task.model_key or "yolo11n"
        task.model_key = model_key
        adapter = get_adapter(model_key)
        input_file = task.input_links[0].file
        output = adapter.predict(resolve_stored_path(input_file), confidence=confidence)
        result_file = save_generated_image(
            output.annotated_image,
            original_name=f"{task.id}-detection.png",
        )
        result = TaskResult(
            task=task,
            output_file=result_file,
            result_type="object_detection",
            implementation="real_model",
            model_key=output.model_key,
            model_version=output.model_version,
            device=output.device,
            result_json={
                "detection_count": len(output.detections),
                "confidence_threshold": confidence,
                "detections": [item.to_dict() for item in output.detections],
            },
        )
        db.session.add(result)
        db.session.commit()
        transition_task(task, "completed")
    except InferenceValidationError as exc:
        db.session.rollback()
        transition_task(task, "failed", error_code="INVALID_INFERENCE_PARAMETERS", error_message=str(exc))
    except (ModelUnavailableError, LookupError) as exc:
        db.session.rollback()
        transition_task(task, "failed", error_code="MODEL_UNAVAILABLE", error_message=str(exc))
    except Exception:
        db.session.rollback()
        transition_task(
            task,
            "failed",
            error_code="INFERENCE_FAILED",
            error_message="模型推理失败，请检查图片、权重和运行环境",
        )
    return task
