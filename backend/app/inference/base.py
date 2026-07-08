from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass(frozen=True)
class Detection:
    class_id: int
    class_name: str
    confidence: float
    bbox: tuple[float, float, float, float]

    def to_dict(self) -> dict:
        x1, y1, x2, y2 = self.bbox
        return {
            "class_id": self.class_id,
            "class_name": self.class_name,
            "confidence": round(self.confidence, 6),
            "bbox": {"x1": round(x1, 2), "y1": round(y1, 2), "x2": round(x2, 2), "y2": round(y2, 2)},
        }


@dataclass
class DetectionOutput:
    detections: list[Detection]
    annotated_image: Image.Image
    model_key: str
    model_version: str
    device: str


class DetectorAdapter(ABC):
    @abstractmethod
    def predict(self, image_path: Path, *, confidence: float) -> DetectionOutput:
        raise NotImplementedError
