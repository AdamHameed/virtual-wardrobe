from sqlalchemy import Enum, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import ClothingTagSource
from app.db.base import Base
from app.models.mixins import ExtraDataMixin, TimestampMixin


class ClothingTag(TimestampMixin, ExtraDataMixin, Base):
    __tablename__ = "clothing_tags"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_clothing_tags_user_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    source: Mapped[ClothingTagSource] = mapped_column(
        Enum(ClothingTagSource, name="clothing_tag_source_enum"),
        default=ClothingTagSource.MANUAL,
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="clothing_tags")
    item_links: Mapped[list["ClothingItemTag"]] = relationship(
        back_populates="tag",
        cascade="all, delete-orphan",
    )

