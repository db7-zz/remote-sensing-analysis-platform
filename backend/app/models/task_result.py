from uuid import uuid4

from app.extensions import db
from app.models.analysis_task import isoformat_utc, utc_now


class TaskResult(db.Model):
    __tablename__ = "task_results"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    task_id = db.Column(
        db.String(36),
        db.ForeignKey("analysis_tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    output_file_id = db.Column(
        db.String(36),
        db.ForeignKey("uploaded_files.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    result_type = db.Column(db.String(50), nullable=False, default="object_detection")
    implementation = db.Column(db.String(30), nullable=False, default="real_model")
    model_key = db.Column(db.String(100), nullable=False)
    model_version = db.Column(db.String(100), nullable=True)
    device = db.Column(db.String(50), nullable=False)
    result_json = db.Column(db.JSON, nullable=False, default=dict)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)

    task = db.relationship("AnalysisTask", back_populates="results")
    output_file = db.relationship("UploadedFile", lazy="joined")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "result_type": self.result_type,
            "implementation": self.implementation,
            "model_key": self.model_key,
            "model_version": self.model_version,
            "device": self.device,
            "data": self.result_json,
            "output_file": self.output_file.to_dict() if self.output_file else None,
            "created_at": isoformat_utc(self.created_at),
        }
