from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import CheckConstraint

from app.extensions import db


TASK_TYPES = (
    "object_detection",
    "land_cover_classification",
    "road_segmentation",
    "change_detection",
)
TASK_STATUSES = ("pending", "running", "completed", "failed")


def utc_now() -> datetime:
    return datetime.now(UTC)


def isoformat_utc(value: datetime | None) -> str | None:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).isoformat()


class AnalysisTask(db.Model):
    __tablename__ = "analysis_tasks"
    __table_args__ = (
        CheckConstraint(f"task_type IN {TASK_TYPES}", name="ck_analysis_tasks_task_type"),
        CheckConstraint(f"status IN {TASK_STATUSES}", name="ck_analysis_tasks_status"),
    )

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(120), nullable=False)
    task_type = db.Column(db.String(50), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default="pending", index=True)
    model_key = db.Column(db.String(100), nullable=True)
    parameters_json = db.Column(db.JSON, nullable=False, default=dict)
    error_code = db.Column(db.String(100), nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now)
    started_at = db.Column(db.DateTime(timezone=True), nullable=True)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    duration_ms = db.Column(db.BigInteger, nullable=True)
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True, index=True)

    input_links = db.relationship(
        "TaskInputFile",
        back_populates="task",
        cascade="all, delete-orphan",
        order_by="TaskInputFile.position",
        lazy="selectin",
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "task_type": self.task_type,
            "status": self.status,
            "model_key": self.model_key,
            "parameters": self.parameters_json,
            "error_code": self.error_code,
            "error_message": self.error_message,
            "created_at": isoformat_utc(self.created_at),
            "updated_at": isoformat_utc(self.updated_at),
            "started_at": isoformat_utc(self.started_at),
            "completed_at": isoformat_utc(self.completed_at),
            "duration_ms": self.duration_ms,
            "input_files": [link.to_dict() for link in self.input_links],
        }
