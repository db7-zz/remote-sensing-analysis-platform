from app.inference.base import DetectorAdapter
from app.inference.yolo_detector import YoloDetector


_ADAPTERS: dict[str, DetectorAdapter] = {"yolo11n": YoloDetector()}


def get_adapter(model_key: str) -> DetectorAdapter:
    try:
        return _ADAPTERS[model_key]
    except KeyError as exc:
        raise LookupError(f"不支持的模型：{model_key}") from exc
