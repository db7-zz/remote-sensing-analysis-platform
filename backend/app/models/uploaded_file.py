from uuid import uuid4

from sqlalchemy import CheckConstraint, UniqueConstraint

from app.extensions import db
from app.models.analysis_task import isoformat_utc, utc_now


FILE_PURPOSES = ("analysis_input", "result", "mask", "preview")


class UploadedFile(db.Model):
    __tablename__ = "uploaded_files"
    __table_args__ = (
        CheckConstraint(f"purpose IN {FILE_PURPOSES}", name="ck_uploaded_files_purpose"),
    )

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    original_name = db.Column(db.String(255), nullable=False)
    stored_name = db.Column(db.String(255), nullable=False, unique=True)
    relative_path = db.Column(db.String(500), nullable=False, unique=True)
    content_type = db.Column(db.String(100), nullable=False)
    extension = db.Column(db.String(20), nullable=False)
    size_bytes = db.Column(db.BigInteger, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    sha256 = db.Column(db.String(64), nullable=False, index=True)
    purpose = db.Column(db.String(50), nullable=False, default="analysis_input", index=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now, index=True)
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True, index=True)

    task_links = db.relationship("TaskInputFile", back_populates="file", lazy="selectin")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "original_name": self.original_name,
            "content_type": self.content_type,
            "extension": self.extension,
            "size_bytes": self.size_bytes,
            "width": self.width,
            "height": self.height,
            "sha256": self.sha256,
            "purpose": self.purpose,
            "content_url": f"/api/v1/files/{self.id}/content",
            "created_at": isoformat_utc(self.created_at),
        }


class TaskInputFile(db.Model):
    __tablename__ = "task_input_files"
    __table_args__ = (
        UniqueConstraint("task_id", "position", name="uq_task_input_files_task_position"),
    )

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    task_id = db.Column(
        db.String(36),
        db.ForeignKey("analysis_tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    file_id = db.Column(
        db.String(36),
        db.ForeignKey("uploaded_files.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    role = db.Column(db.String(30), nullable=False, default="primary")
    position = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)

    task = db.relationship("AnalysisTask", back_populates="input_links")
    file = db.relationship("UploadedFile", back_populates="task_links", lazy="joined")

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "position": self.position,
            "file": self.file.to_dict(),
        }
