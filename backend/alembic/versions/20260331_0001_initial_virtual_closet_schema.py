"""initial virtual closet schema

Revision ID: 20260331_0001
Revises:
Create Date: 2026-03-31 00:00:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260331_0001"
down_revision = None
branch_labels = None
depends_on = None


clothing_status_enum = sa.Enum(
    "clean",
    "dirty",
    "unavailable",
    name="clothing_status_enum",
)
season_enum = sa.Enum(
    "spring",
    "summer",
    "fall",
    "winter",
    "all_season",
    name="season_enum",
)
formality_enum = sa.Enum(
    "casual",
    "smart_casual",
    "business",
    "formal",
    "athletic",
    "lounge",
    name="formality_enum",
)
outfit_item_role_enum = sa.Enum(
    "top",
    "bottom",
    "shoes",
    "outerwear",
    "accessory",
    "one_piece",
    name="outfit_item_role_enum",
)
clothing_tag_source_enum = sa.Enum(
    "manual",
    "generated",
    "system",
    name="clothing_tag_source_enum",
)


def upgrade() -> None:
    bind = op.get_bind()
    clothing_status_enum.create(bind, checkfirst=True)
    season_enum.create(bind, checkfirst=True)
    formality_enum.create(bind, checkfirst=True)
    outfit_item_role_enum.create(bind, checkfirst=True)
    clothing_tag_source_enum.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("extra_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    op.create_table(
        "clothing_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("subcategory", sa.String(length=100), nullable=True),
        sa.Column("primary_color", sa.String(length=100), nullable=True),
        sa.Column("secondary_color", sa.String(length=100), nullable=True),
        sa.Column("season", season_enum, nullable=True),
        sa.Column("formality", formality_enum, nullable=True),
        sa.Column("material", sa.String(length=100), nullable=True),
        sa.Column("brand", sa.String(length=100), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("image_path", sa.String(length=500), nullable=True),
        sa.Column("status", clothing_status_enum, nullable=False, server_default="clean"),
        sa.Column("wear_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_worn_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("extra_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_clothing_items_category"), "clothing_items", ["category"], unique=False)
    op.create_index(op.f("ix_clothing_items_id"), "clothing_items", ["id"], unique=False)
    op.create_index(op.f("ix_clothing_items_user_id"), "clothing_items", ["user_id"], unique=False)

    op.create_table(
        "clothing_tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("source", clothing_tag_source_enum, nullable=False, server_default="manual"),
        sa.Column("extra_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "name", name="uq_clothing_tags_user_name"),
    )
    op.create_index(op.f("ix_clothing_tags_id"), "clothing_tags", ["id"], unique=False)
    op.create_index(op.f("ix_clothing_tags_user_id"), "clothing_tags", ["user_id"], unique=False)

    op.create_table(
        "outfits",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("extra_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_outfits_id"), "outfits", ["id"], unique=False)
    op.create_index(op.f("ix_outfits_user_id"), "outfits", ["user_id"], unique=False)

    op.create_table(
        "clothing_item_tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("clothing_item_id", sa.Integer(), nullable=False),
        sa.Column("clothing_tag_id", sa.Integer(), nullable=False),
        sa.Column("extra_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["clothing_item_id"], ["clothing_items.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["clothing_tag_id"], ["clothing_tags.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("clothing_item_id", "clothing_tag_id", name="uq_clothing_item_tags_item_tag"),
    )
    op.create_index(op.f("ix_clothing_item_tags_clothing_item_id"), "clothing_item_tags", ["clothing_item_id"], unique=False)
    op.create_index(op.f("ix_clothing_item_tags_clothing_tag_id"), "clothing_item_tags", ["clothing_tag_id"], unique=False)
    op.create_index(op.f("ix_clothing_item_tags_id"), "clothing_item_tags", ["id"], unique=False)

    op.create_table(
        "outfit_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("outfit_id", sa.Integer(), nullable=False),
        sa.Column("clothing_item_id", sa.Integer(), nullable=False),
        sa.Column("role", outfit_item_role_enum, nullable=False),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("extra_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["clothing_item_id"], ["clothing_items.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["outfit_id"], ["outfits.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("outfit_id", "clothing_item_id", name="uq_outfit_items_outfit_item"),
    )
    op.create_index(op.f("ix_outfit_items_clothing_item_id"), "outfit_items", ["clothing_item_id"], unique=False)
    op.create_index(op.f("ix_outfit_items_id"), "outfit_items", ["id"], unique=False)
    op.create_index(op.f("ix_outfit_items_outfit_id"), "outfit_items", ["outfit_id"], unique=False)

    op.create_table(
        "outfit_plans",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("outfit_id", sa.Integer(), nullable=False),
        sa.Column("planned_for", sa.Date(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("extra_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["outfit_id"], ["outfits.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "outfit_id", "planned_for", name="uq_outfit_plans_user_outfit_day"),
    )
    op.create_index(op.f("ix_outfit_plans_id"), "outfit_plans", ["id"], unique=False)
    op.create_index(op.f("ix_outfit_plans_outfit_id"), "outfit_plans", ["outfit_id"], unique=False)
    op.create_index(op.f("ix_outfit_plans_planned_for"), "outfit_plans", ["planned_for"], unique=False)
    op.create_index(op.f("ix_outfit_plans_user_id"), "outfit_plans", ["user_id"], unique=False)

    op.create_table(
        "wear_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("outfit_id", sa.Integer(), nullable=False),
        sa.Column("worn_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("extra_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["outfit_id"], ["outfits.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_wear_logs_id"), "wear_logs", ["id"], unique=False)
    op.create_index(op.f("ix_wear_logs_outfit_id"), "wear_logs", ["outfit_id"], unique=False)
    op.create_index(op.f("ix_wear_logs_user_id"), "wear_logs", ["user_id"], unique=False)
    op.create_index(op.f("ix_wear_logs_worn_at"), "wear_logs", ["worn_at"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_wear_logs_worn_at"), table_name="wear_logs")
    op.drop_index(op.f("ix_wear_logs_user_id"), table_name="wear_logs")
    op.drop_index(op.f("ix_wear_logs_outfit_id"), table_name="wear_logs")
    op.drop_index(op.f("ix_wear_logs_id"), table_name="wear_logs")
    op.drop_table("wear_logs")

    op.drop_index(op.f("ix_outfit_plans_user_id"), table_name="outfit_plans")
    op.drop_index(op.f("ix_outfit_plans_planned_for"), table_name="outfit_plans")
    op.drop_index(op.f("ix_outfit_plans_outfit_id"), table_name="outfit_plans")
    op.drop_index(op.f("ix_outfit_plans_id"), table_name="outfit_plans")
    op.drop_table("outfit_plans")

    op.drop_index(op.f("ix_outfit_items_outfit_id"), table_name="outfit_items")
    op.drop_index(op.f("ix_outfit_items_id"), table_name="outfit_items")
    op.drop_index(op.f("ix_outfit_items_clothing_item_id"), table_name="outfit_items")
    op.drop_table("outfit_items")

    op.drop_index(op.f("ix_clothing_item_tags_id"), table_name="clothing_item_tags")
    op.drop_index(op.f("ix_clothing_item_tags_clothing_tag_id"), table_name="clothing_item_tags")
    op.drop_index(op.f("ix_clothing_item_tags_clothing_item_id"), table_name="clothing_item_tags")
    op.drop_table("clothing_item_tags")

    op.drop_index(op.f("ix_outfits_user_id"), table_name="outfits")
    op.drop_index(op.f("ix_outfits_id"), table_name="outfits")
    op.drop_table("outfits")

    op.drop_index(op.f("ix_clothing_tags_user_id"), table_name="clothing_tags")
    op.drop_index(op.f("ix_clothing_tags_id"), table_name="clothing_tags")
    op.drop_table("clothing_tags")

    op.drop_index(op.f("ix_clothing_items_user_id"), table_name="clothing_items")
    op.drop_index(op.f("ix_clothing_items_id"), table_name="clothing_items")
    op.drop_index(op.f("ix_clothing_items_category"), table_name="clothing_items")
    op.drop_table("clothing_items")

    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

    bind = op.get_bind()
    clothing_tag_source_enum.drop(bind, checkfirst=True)
    outfit_item_role_enum.drop(bind, checkfirst=True)
    formality_enum.drop(bind, checkfirst=True)
    season_enum.drop(bind, checkfirst=True)
    clothing_status_enum.drop(bind, checkfirst=True)
