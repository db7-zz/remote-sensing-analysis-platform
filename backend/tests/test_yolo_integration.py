from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image

from app.config import Config


@pytest.mark.skipif(not Path(Config.YOLO_MODEL_PATH).is_file(), reason="本地 YOLO 权重未准备")
def test_real_yolo_cpu_inference_pipeline(client):
    image_buffer = BytesIO()
    Image.new("RGB", (320, 240), color=(190, 205, 195)).save(image_buffer, format="JPEG")
    upload_response = client.post(
        "/api/v1/files",
        data={"file": (BytesIO(image_buffer.getvalue()), "real-yolo-input.jpg", "image/jpeg")},
        content_type="multipart/form-data",
    )
    file_id = upload_response.get_json()["data"]["id"]

    response = client.post(
        "/api/v1/tasks",
        json={
            "name": "真实 YOLO CPU 集成测试",
            "task_type": "object_detection",
            "model_key": "yolo11n",
            "parameters": {"confidence": 0.25},
            "input_file_ids": [file_id],
        },
    )

    assert response.status_code == 201
    task = response.get_json()["data"]
    assert task["status"] == "completed"
    assert task["error_code"] is None
    assert task["results"][0]["implementation"] == "real_model"
    assert task["results"][0]["model_key"] == "yolo11n"
    assert task["results"][0]["device"] == "cpu"
    assert task["results"][0]["data"]["detection_count"] >= 0
    assert client.get(task["results"][0]["output_file"]["content_url"]).status_code == 200
