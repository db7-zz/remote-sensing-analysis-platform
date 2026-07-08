from pathlib import Path

from flask import current_app
from PIL import Image, ImageDraw, ImageFont

from app.inference.base import Detection, DetectionOutput, DetectorAdapter


class ModelUnavailableError(RuntimeError):
    pass


class YoloDetector(DetectorAdapter):
    model_key = "yolo11n"

    def __init__(self):
        self._model = None
        self._loaded_path: Path | None = None

    def _load_model(self):
        model_path = Path(current_app.config["YOLO_MODEL_PATH"])
        if not model_path.is_file():
            raise ModelUnavailableError(f"YOLO 权重不存在：{model_path.name}")
        if self._model is None or self._loaded_path != model_path:
            try:
                from ultralytics import YOLO
            except ImportError as exc:
                raise ModelUnavailableError("Ultralytics 尚未安装") from exc
            self._model = YOLO(str(model_path))
            self._loaded_path = model_path
        return self._model, model_path

    def predict(self, image_path: Path, *, confidence: float) -> DetectionOutput:
        model, model_path = self._load_model()
        device = current_app.config["YOLO_DEVICE"]
        results = model.predict(
            source=str(image_path),
            conf=confidence,
            imgsz=current_app.config["YOLO_IMAGE_SIZE"],
            device=device,
            verbose=False,
        )
        result = results[0]
        names = result.names
        detections: list[Detection] = []
        for box in result.boxes:
            class_id = int(box.cls.item())
            coordinates = tuple(float(value) for value in box.xyxy[0].tolist())
            detections.append(
                Detection(
                    class_id=class_id,
                    class_name=str(names[class_id]),
                    confidence=float(box.conf.item()),
                    bbox=coordinates,
                )
            )

        annotated = self._draw_detections(image_path, detections)
        return DetectionOutput(
            detections=detections,
            annotated_image=annotated,
            model_key=self.model_key,
            model_version=model_path.name,
            device=str(device),
        )

    @staticmethod
    def _draw_detections(image_path: Path, detections: list[Detection]) -> Image.Image:
        image = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        for detection in detections:
            x1, y1, x2, y2 = detection.bbox
            color = (26, 145, 110)
            draw.rectangle((x1, y1, x2, y2), outline=color, width=3)
            label = f"{detection.class_name} {detection.confidence:.2f}"
            left, top, right, bottom = draw.textbbox((x1, y1), label, font=font)
            draw.rectangle((left, top, right + 4, bottom + 4), fill=color)
            draw.text((x1 + 2, y1 + 2), label, fill="white", font=font)
        return image
