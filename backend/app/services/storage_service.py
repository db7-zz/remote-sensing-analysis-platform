from hashlib import sha256
from io import BytesIO
from pathlib import Path, PurePath
from uuid import uuid4
import warnings

from flask import current_app
from PIL import Image, UnidentifiedImageError
from sqlalchemy import select
from werkzeug.datastructures import FileStorage

from app.extensions import db
from app.models.uploaded_file import FILE_PURPOSES, UploadedFile


ALLOWED_EXTENSIONS = {
    ".jpg": ("image/jpeg", "JPEG"),
    ".jpeg": ("image/jpeg", "JPEG"),
    ".png": ("image/png", "PNG"),
}


class FileValidationError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


class StoredFileNotFoundError(LookupError):
    pass


def get_upload_root() -> Path:
    return Path(current_app.config["UPLOAD_ROOT"]).resolve()


def clean_original_name(filename: str) -> str:
    normalized = filename.replace("\\", "/")
    return PurePath(normalized).name[:255]


def inspect_image(data: bytes, expected_format: str) -> tuple[int, int]:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            Image.MAX_IMAGE_PIXELS = current_app.config["MAX_IMAGE_PIXELS"]
            with Image.open(BytesIO(data)) as image:
                image.verify()
            with Image.open(BytesIO(data)) as image:
                if image.format != expected_format:
                    raise FileValidationError("IMAGE_FORMAT_MISMATCH", "图片内容与文件扩展名不一致")
                width, height = image.size
    except FileValidationError:
        raise
    except (Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise FileValidationError("IMAGE_TOO_LARGE", "图片像素数量超过允许上限") from None
    except (UnidentifiedImageError, OSError, SyntaxError):
        raise FileValidationError("INVALID_IMAGE", "文件无法被识别为有效图片") from None

    if width < 1 or height < 1:
        raise FileValidationError("INVALID_IMAGE", "图片尺寸无效")
    return width, height


def save_uploaded_image(file: FileStorage | None, purpose: str) -> UploadedFile:
    if file is None or not file.filename:
        raise FileValidationError("FILE_REQUIRED", "请选择要上传的图片")
    if purpose not in FILE_PURPOSES:
        raise FileValidationError("INVALID_FILE_PURPOSE", "文件用途不受支持")

    original_name = clean_original_name(file.filename)
    extension = Path(original_name).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise FileValidationError("UNSUPPORTED_FILE_TYPE", "只支持 JPEG 和 PNG 图片")

    expected_mime, expected_format = ALLOWED_EXTENSIONS[extension]
    if file.mimetype != expected_mime:
        raise FileValidationError("MIME_TYPE_MISMATCH", "图片 MIME 类型与扩展名不一致")

    max_bytes = current_app.config["MAX_CONTENT_LENGTH"]
    content = file.stream.read(max_bytes + 1)
    if not content:
        raise FileValidationError("EMPTY_FILE", "上传文件不能为空")
    if len(content) > max_bytes:
        raise FileValidationError("FILE_TOO_LARGE", "上传文件超过大小限制")

    width, height = inspect_image(content, expected_format)
    stored_name = f"{uuid4()}{extension}"
    upload_root = get_upload_root()
    destination_directory = upload_root / "original"
    destination_directory.mkdir(parents=True, exist_ok=True)
    destination = destination_directory / stored_name
    destination.write_bytes(content)

    uploaded_file = UploadedFile(
        original_name=original_name,
        stored_name=stored_name,
        relative_path=destination.relative_to(upload_root).as_posix(),
        content_type=expected_mime,
        extension=extension,
        size_bytes=len(content),
        width=width,
        height=height,
        sha256=sha256(content).hexdigest(),
        purpose=purpose,
    )
    try:
        db.session.add(uploaded_file)
        db.session.commit()
    except Exception:
        db.session.rollback()
        destination.unlink(missing_ok=True)
        raise
    return uploaded_file


def get_uploaded_file(file_id: str) -> UploadedFile:
    uploaded_file = db.session.scalar(
        select(UploadedFile).where(
            UploadedFile.id == file_id,
            UploadedFile.deleted_at.is_(None),
        )
    )
    if uploaded_file is None:
        raise StoredFileNotFoundError("文件不存在")
    return uploaded_file


def resolve_stored_path(uploaded_file: UploadedFile) -> Path:
    upload_root = get_upload_root()
    candidate = (upload_root / uploaded_file.relative_path).resolve()
    if candidate != upload_root and upload_root not in candidate.parents:
        raise StoredFileNotFoundError("文件存储路径无效")
    if not candidate.is_file():
        raise StoredFileNotFoundError("文件内容不存在")
    return candidate
