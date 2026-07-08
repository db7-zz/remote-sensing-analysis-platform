from io import BytesIO

from PIL import Image

from app.inference.base import Detection, DetectionOutput
from app.inference.yolo_detector import ModelUnavailableError
from app.services.task_service import TaskTransitionError, transition_task


def create_task(client, **overrides):
    payload = {
        "name": "任务管理测试",
        "task_type": "land_cover_classification",
        "model_key": None,
        "parameters": {"confidence": 0.35},
    }
    payload.update(overrides)
    return client.post("/api/v1/tasks", json=payload)


def test_create_list_and_get_task(client):
    create_response = create_task(client)

    assert create_response.status_code == 201
    created = create_response.get_json()["data"]
    assert created["status"] == "pending"
    assert created["parameters"] == {"confidence": 0.35}

    list_response = client.get("/api/v1/tasks?page=1&page_size=10&task_type=land_cover_classification")
    listing = list_response.get_json()["data"]
    assert list_response.status_code == 200
    assert listing["total"] == 1
    assert listing["items"][0]["id"] == created["id"]

    detail_response = client.get(f"/api/v1/tasks/{created['id']}")
    assert detail_response.status_code == 200
    assert detail_response.get_json()["data"]["name"] == "任务管理测试"


def test_invalid_task_type_returns_validation_error(client):
    response = create_task(client, task_type="not-a-real-task")

    assert response.status_code == 400
    assert response.get_json()["code"] == "VALIDATION_ERROR"


def test_soft_deleted_task_is_hidden(client):
    created = create_task(client).get_json()["data"]

    delete_response = client.delete(f"/api/v1/tasks/{created['id']}")
    assert delete_response.status_code == 200

    detail_response = client.get(f"/api/v1/tasks/{created['id']}")
    assert detail_response.status_code == 404
    assert detail_response.get_json()["code"] == "TASK_NOT_FOUND"

    assert client.get("/api/v1/tasks").get_json()["data"]["total"] == 0


def test_task_status_transition_rules(app, client):
    task_id = create_task(client).get_json()["data"]["id"]

    with app.app_context():
        from app.services.task_service import get_task

        task = get_task(task_id)
        transition_task(task, "running")
        transition_task(task, "completed")

        assert task.status == "completed"
        assert task.started_at is not None
        assert task.completed_at is not None
        assert task.duration_ms is not None

        try:
            transition_task(task, "running")
        except TaskTransitionError:
            pass
        else:
            raise AssertionError("完成态任务不应允许重新进入 running")


def test_create_task_with_uploaded_input(client):
    image_buffer = BytesIO()
    Image.new("RGB", (10, 8), color=(20, 80, 120)).save(image_buffer, format="PNG")
    upload_response = client.post(
        "/api/v1/files",
        data={"file": (BytesIO(image_buffer.getvalue()), "input.png", "image/png")},
        content_type="multipart/form-data",
    )
    file_id = upload_response.get_json()["data"]["id"]

    task_response = create_task(client, input_file_ids=[file_id])

    assert task_response.status_code == 201
    input_files = task_response.get_json()["data"]["input_files"]
    assert len(input_files) == 1
    assert input_files[0]["role"] == "primary"
    assert input_files[0]["file"]["id"] == file_id


class FakeDetector:
    def predict(self, image_path, *, confidence):
        image = Image.open(image_path).convert("RGB")
        return DetectionOutput(
            detections=[Detection(2, "car", 0.91, (1.0, 2.0, 8.0, 7.0))],
            annotated_image=image,
            model_key="yolo11n",
            model_version="test-weight.pt",
            device="cpu",
        )


class EmptyDetector:
    def predict(self, image_path, *, confidence):
        return DetectionOutput(
            detections=[],
            annotated_image=Image.open(image_path).convert("RGB"),
            model_key="yolo11n",
            model_version="test-weight.pt",
            device="cpu",
        )


def upload_task_image(client):
    image_buffer = BytesIO()
    Image.new("RGB", (10, 8), color=(20, 80, 120)).save(image_buffer, format="PNG")
    response = client.post(
        "/api/v1/files",
        data={"file": (BytesIO(image_buffer.getvalue()), "input.png", "image/png")},
        content_type="multipart/form-data",
    )
    return response.get_json()["data"]["id"]


def test_object_detection_runs_and_persists_real_result(app, client, monkeypatch):
    monkeypatch.setattr("app.services.inference_service.get_adapter", lambda model_key: FakeDetector())
    image_buffer = BytesIO()
    Image.new("RGB", (10, 8), color=(20, 80, 120)).save(image_buffer, format="PNG")
    upload_response = client.post(
        "/api/v1/files",
        data={"file": (BytesIO(image_buffer.getvalue()), "input.png", "image/png")},
        content_type="multipart/form-data",
    )
    file_id = upload_response.get_json()["data"]["id"]

    response = create_task(
        client,
        name="真实目标检测测试",
        task_type="object_detection",
        model_key="yolo11n",
        parameters={"confidence": 0.3},
        input_file_ids=[file_id],
    )

    assert response.status_code == 201
    task = response.get_json()["data"]
    assert task["status"] == "completed"
    assert task["duration_ms"] is not None
    assert task["results"][0]["implementation"] == "real_model"
    assert task["results"][0]["data"]["detection_count"] == 1
    assert task["results"][0]["data"]["detections"][0]["class_name"] == "car"
    result_url = task["results"][0]["output_file"]["content_url"]
    assert client.get(result_url).status_code == 200


def test_object_detection_requires_one_image(client):
    response = create_task(client, task_type="object_detection", model_key="yolo11n")

    assert response.status_code == 400
    assert "一张输入图片" in response.get_json()["message"]


def test_object_detection_with_no_targets_completes(client, monkeypatch):
    monkeypatch.setattr("app.services.inference_service.get_adapter", lambda model_key: EmptyDetector())
    response = create_task(
        client,
        task_type="object_detection",
        model_key="yolo11n",
        input_file_ids=[upload_task_image(client)],
    )

    task = response.get_json()["data"]
    assert task["status"] == "completed"
    assert task["results"][0]["data"]["detection_count"] == 0
    assert task["results"][0]["data"]["detections"] == []


def test_missing_model_marks_task_failed(client, monkeypatch):
    def unavailable(model_key):
        raise ModelUnavailableError("YOLO 权重不存在：yolo11n.pt")

    monkeypatch.setattr("app.services.inference_service.get_adapter", unavailable)
    response = create_task(
        client,
        task_type="object_detection",
        model_key="yolo11n",
        input_file_ids=[upload_task_image(client)],
    )

    task = response.get_json()["data"]
    assert task["status"] == "failed"
    assert task["error_code"] == "MODEL_UNAVAILABLE"
    assert "权重不存在" in task["error_message"]


def test_inference_exception_marks_task_failed(client, monkeypatch):
    class BrokenDetector:
        def predict(self, image_path, *, confidence):
            raise RuntimeError("internal details must not leak")

    monkeypatch.setattr("app.services.inference_service.get_adapter", lambda model_key: BrokenDetector())
    response = create_task(
        client,
        task_type="object_detection",
        model_key="yolo11n",
        input_file_ids=[upload_task_image(client)],
    )

    task = response.get_json()["data"]
    assert task["status"] == "failed"
    assert task["error_code"] == "INFERENCE_FAILED"
    assert "internal details" not in task["error_message"]
