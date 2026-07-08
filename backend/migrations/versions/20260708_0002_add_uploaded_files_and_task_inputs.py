"""Add uploaded files and task input associations.

Revision ID: 20260708_0002
Revises: 20260706_0001
Create Date: 2026-07-08
"""

from alembic import op
import sqlalchemy as sa


revision = "20260708_0002"
down_revision = "20260706_0001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "uploaded_files",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("original_name", sa.String(length=255), nullable=False),
        sa.Column("stored_name", sa.String(length=255), nullable=False),
        sa.Column("relative_path", sa.String(length=500), nullable=False),
        sa.Column("content_type", sa.String(length=100), nullable=False),
        sa.Column("extension", sa.String(length=20), nullable=False),
        sa.Column("size_bytes", sa.BigInteger(), nullable=False),
        sa.Column("width", sa.Integer(), nullable=False),
        sa.Column("height", sa.Integer(), nullable=False),
        sa.Column("sha256", sa.String(length=64), nullable=False),
        sa.Column("purpose", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "purpose IN ('analysis_input', 'result', 'mask', 'preview')",
            name="ck_uploaded_files_purpose",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("relative_path"),
        sa.UniqueConstraint("stored_name"),
    )
    op.create_index("ix_uploaded_files_created_at", "uploaded_files", ["created_at"], unique=False)
    op.create_index("ix_uploaded_files_deleted_at", "uploaded_files", ["deleted_at"], unique=False)
    op.create_index("ix_uploaded_files_purpose", "uploaded_files", ["purpose"], unique=False)
    op.create_index("ix_uploaded_files_sha256", "uploaded_files", ["sha256"], unique=False)

    op.create_table(
        "task_input_files",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("task_id", sa.String(length=36), nullable=False),
        sa.Column("file_id", sa.String(length=36), nullable=False),
        sa.Column("role", sa.String(length=30), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["file_id"], ["uploaded_files.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["task_id"], ["analysis_tasks.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("task_id", "position", name="uq_task_input_files_task_position"),
    )
    op.create_index("ix_task_input_files_file_id", "task_input_files", ["file_id"], unique=False)
    op.create_index("ix_task_input_files_task_id", "task_input_files", ["task_id"], unique=False)


def downgrade():
    op.drop_index("ix_task_input_files_task_id", table_name="task_input_files")
    op.drop_index("ix_task_input_files_file_id", table_name="task_input_files")
    op.drop_table("task_input_files")

    op.drop_index("ix_uploaded_files_sha256", table_name="uploaded_files")
    op.drop_index("ix_uploaded_files_purpose", table_name="uploaded_files")
    op.drop_index("ix_uploaded_files_deleted_at", table_name="uploaded_files")
    op.drop_index("ix_uploaded_files_created_at", table_name="uploaded_files")
    op.drop_table("uploaded_files")
