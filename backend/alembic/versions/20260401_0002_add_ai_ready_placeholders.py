"""add ai ready placeholder tables

Revision ID: 20260401_0002
Revises: 20260331_0001
Create Date: 2026-04-01 00:00:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260401_0002"
down_revision = "20260331_0001"
branch_labels = None
depends_on = None


provenance_source_enum = postgresql.ENUM(
    "manual",
    "rule_based",
    "ai_generated",
    name="provenance_source_enum",
    create_type=False,
)
suggestion_status_enum = postgresql.ENUM(
    "pending",
    "accepted",
    "rejected",
    name="suggestion_status_enum",
    create_type=False,
)


def upgrade() -> None:
    bind = op.get_bind()
    provenance_source_enum.create(bind, checkfirst=True)
    suggestion_status_enum.create(bind, checkfirst=True)

    op.create_table(
        "auto_tag_suggestions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("clothing_item_id", sa.Integer(), nullable=False),
        sa.Column("suggested_tag", sa.String(length=100), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=True),
        sa.Column("confidence", sa.Numeric(4, 3), nullable=True),
        sa.Column("source", provenance_source_enum, nullable=False, server_default="ai_generated"),
        sa.Column("status", suggestion_status_enum, nullable=False, server_default="pending"),
        sa.Column("extra_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["clothing_item_id"], ["clothing_items.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_auto_tag_suggestions_id"), "auto_tag_suggestions", ["id"], unique=False)
    op.create_index(op.f("ix_auto_tag_suggestions_user_id"), "auto_tag_suggestions", ["user_id"], unique=False)
    op.create_index(op.f("ix_auto_tag_suggestions_clothing_item_id"), "auto_tag_suggestions", ["clothing_item_id"], unique=False)

    op.create_table(
        "ai_recommendation_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("request_type", sa.String(length=100), nullable=False),
        sa.Column("source", provenance_source_enum, nullable=False, server_default="rule_based"),
        sa.Column("score", sa.Numeric(6, 3), nullable=True),
        sa.Column("rationale", sa.Text(), nullable=True),
        sa.Column("extra_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ai_recommendation_logs_id"), "ai_recommendation_logs", ["id"], unique=False)
    op.create_index(op.f("ix_ai_recommendation_logs_user_id"), "ai_recommendation_logs", ["user_id"], unique=False)

    op.create_table(
        "clothing_embeddings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("clothing_item_id", sa.Integer(), nullable=False),
        sa.Column("model_key", sa.String(length=255), nullable=False),
        sa.Column("dimensions", sa.Integer(), nullable=False),
        sa.Column("vector", postgresql.ARRAY(sa.Float()), nullable=True),
        sa.Column("source", provenance_source_enum, nullable=False, server_default="ai_generated"),
        sa.Column("extra_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["clothing_item_id"], ["clothing_items.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_clothing_embeddings_id"), "clothing_embeddings", ["id"], unique=False)
    op.create_index(op.f("ix_clothing_embeddings_user_id"), "clothing_embeddings", ["user_id"], unique=False)
    op.create_index(op.f("ix_clothing_embeddings_clothing_item_id"), "clothing_embeddings", ["clothing_item_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_clothing_embeddings_clothing_item_id"), table_name="clothing_embeddings")
    op.drop_index(op.f("ix_clothing_embeddings_user_id"), table_name="clothing_embeddings")
    op.drop_index(op.f("ix_clothing_embeddings_id"), table_name="clothing_embeddings")
    op.drop_table("clothing_embeddings")

    op.drop_index(op.f("ix_ai_recommendation_logs_user_id"), table_name="ai_recommendation_logs")
    op.drop_index(op.f("ix_ai_recommendation_logs_id"), table_name="ai_recommendation_logs")
    op.drop_table("ai_recommendation_logs")

    op.drop_index(op.f("ix_auto_tag_suggestions_clothing_item_id"), table_name="auto_tag_suggestions")
    op.drop_index(op.f("ix_auto_tag_suggestions_user_id"), table_name="auto_tag_suggestions")
    op.drop_index(op.f("ix_auto_tag_suggestions_id"), table_name="auto_tag_suggestions")
    op.drop_table("auto_tag_suggestions")

    bind = op.get_bind()
    suggestion_status_enum.drop(bind, checkfirst=True)
    provenance_source_enum.drop(bind, checkfirst=True)
