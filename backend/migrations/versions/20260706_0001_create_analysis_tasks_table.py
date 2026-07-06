"""Create the analysis_tasks table.

Revision ID: 20260706_0001
Revises:
Create Date: 2026-07-06
"""

from alembic import op
import sqlalchemy as sa


revision = "20260706_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "analysis_tasks",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("task_type", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("model_key", sa.String(length=100), nullable=True),
        sa.Column("parameters_json", sa.JSON(), nullable=False),
        sa.Column("error_code", sa.String(length=100), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("duration_ms", sa.BigInteger(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "status IN ('pending', 'running', 'completed', 'failed')",
            name="ck_analysis_tasks_status",
        ),
        sa.CheckConstraint(
            "task_type IN ('object_detection', 'land_cover_classification', 'road_segmentation', 'change_detection')",
            name="ck_analysis_tasks_task_type",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_analysis_tasks_created_at", "analysis_tasks", ["created_at"], unique=False)
    op.create_index("ix_analysis_tasks_deleted_at", "analysis_tasks", ["deleted_at"], unique=False)
    op.create_index("ix_analysis_tasks_status", "analysis_tasks", ["status"], unique=False)
    op.create_index("ix_analysis_tasks_task_type", "analysis_tasks", ["task_type"], unique=False)


def downgrade():
    op.drop_index("ix_analysis_tasks_task_type", table_name="analysis_tasks")
    op.drop_index("ix_analysis_tasks_status", table_name="analysis_tasks")
    op.drop_index("ix_analysis_tasks_deleted_at", table_name="analysis_tasks")
    op.drop_index("ix_analysis_tasks_created_at", table_name="analysis_tasks")
    op.drop_table("analysis_tasks")
