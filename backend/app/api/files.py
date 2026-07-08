from flask import Blueprint, request, send_file

from app.services.storage_service import (
    FileValidationError,
    StoredFileNotFoundError,
    get_uploaded_file,
    resolve_stored_path,
    save_uploaded_image,
)
from app.utils.responses import error_response, success_response


files_blueprint = Blueprint("files", __name__)


@files_blueprint.post("/files")
def upload_file():
    try:
        uploaded_file = save_uploaded_image(
            request.files.get("file"),
            request.form.get("purpose", "analysis_input"),
        )
    except FileValidationError as exc:
        return error_response(code=exc.code, message=str(exc), status_code=400)

    return success_response(data=uploaded_file.to_dict(), message="图片上传成功", status_code=201)


@files_blueprint.get("/files/<file_id>/content")
def get_file_content(file_id: str):
    try:
        uploaded_file = get_uploaded_file(file_id)
        path = resolve_stored_path(uploaded_file)
    except StoredFileNotFoundError as exc:
        return error_response(code="FILE_NOT_FOUND", message=str(exc), status_code=404)

    return send_file(
        path,
        mimetype=uploaded_file.content_type,
        download_name=uploaded_file.original_name,
        as_attachment=False,
        conditional=True,
    )
