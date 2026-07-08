"""Add persisted inference task results.

Revision ID: 20260708_0003
Revises: 20260708_0002
Create Date: 2026-07-08
"""

from alembic import op
import sqlalchemy as sa


revision = "20260708_0003"
down_revision = "20260708_0002"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "task_results",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("task_id", sa.String(length=36), nullable=False),
        sa.Column("output_file_id", sa.String(length=36), nullable=True),
        sa.Column("result_type", sa.String(length=50), nullable=False),
        sa.Column("implementation", sa.String(length=30), nullable=False),
        sa.Column("model_key", sa.String(length=100), nullable=False),
        sa.Column("model_version", sa.String(length=100), nullable=True),
        sa.Column("device", sa.String(length=50), nullable=False),
        sa.Column("result_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["output_file_id"], ["uploaded_files.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["task_id"], ["analysis_tasks.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("task_results") as batch_op:
        batch_op.create_index("ix_task_results_task_id", ["task_id"], unique=False)
        batch_op.create_index("ix_task_results_output_file_id", ["output_file_id"], unique=False)


def downgrade():
    with op.batch_alter_table("task_results") as batch_op:
        batch_op.drop_index("ix_task_results_output_file_id")
        batch_op.drop_index("ix_task_results_task_id")
    op.drop_table("task_results")
