from io import BytesIO

from PIL import Image


def make_image_bytes(image_format="PNG", size=(16, 12)):
    buffer = BytesIO()
    Image.new("RGB", size, color=(45, 110, 85)).save(buffer, format=image_format)
    return buffer.getvalue()


def upload_png(client, filename="demo.png"):
    return client.post(
        "/api/v1/files",
        data={
            "file": (BytesIO(make_image_bytes()), filename, "image/png"),
            "purpose": "analysis_input",
        },
        content_type="multipart/form-data",
    )


def test_upload_and_read_image(client):
    upload_response = upload_png(client, filename="../../遥感样例.png")

    assert upload_response.status_code == 201
    uploaded = upload_response.get_json()["data"]
    assert uploaded["original_name"] == "遥感样例.png"
    assert uploaded["width"] == 16
    assert uploaded["height"] == 12
    assert uploaded["size_bytes"] > 0
    assert len(uploaded["sha256"]) == 64

    content_response = client.get(uploaded["content_url"])
    assert content_response.status_code == 200
    assert content_response.content_type == "image/png"
    assert content_response.data == make_image_bytes()


def test_rejects_unsupported_extension(client):
    response = client.post(
        "/api/v1/files",
        data={"file": (BytesIO(b"not an image"), "payload.txt", "text/plain")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.get_json()["code"] == "UNSUPPORTED_FILE_TYPE"


def test_rejects_mime_mismatch(client):
    response = client.post(
        "/api/v1/files",
        data={"file": (BytesIO(make_image_bytes()), "demo.png", "image/jpeg")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.get_json()["code"] == "MIME_TYPE_MISMATCH"


def test_rejects_invalid_image_content(client):
    response = client.post(
        "/api/v1/files",
        data={"file": (BytesIO(b"pretend png"), "demo.png", "image/png")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.get_json()["code"] == "INVALID_IMAGE"


def test_rejects_request_over_size_limit(client):
    response = client.post(
        "/api/v1/files",
        data={"file": (BytesIO(b"x" * (1024 * 1024 + 1)), "large.png", "image/png")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 413
    assert response.get_json()["code"] == "FILE_TOO_LARGE"
