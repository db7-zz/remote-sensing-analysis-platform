from io import BytesIO

from PIL import Image

from app.services.task_service import TaskTransitionError, transition_task


def create_task(client, **overrides):
    payload = {
        "name": "港口目标检测",
        "task_type": "object_detection",
        "model_key": "yolo_default",
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

    list_response = client.get("/api/v1/tasks?page=1&page_size=10&task_type=object_detection")
    listing = list_response.get_json()["data"]
    assert list_response.status_code == 200
    assert listing["total"] == 1
    assert listing["items"][0]["id"] == created["id"]

    detail_response = client.get(f"/api/v1/tasks/{created['id']}")
    assert detail_response.status_code == 200
    assert detail_response.get_json()["data"]["name"] == "港口目标检测"


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
