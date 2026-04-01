from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import ExtraDataMixin, TimestampMixin


class ClothingItemTag(TimestampMixin, ExtraDataMixin, Base):
    __tablename__ = "clothing_item_tags"
    __table_args__ = (
        UniqueConstraint(
            "clothing_item_id",
            "clothing_tag_id",
            name="uq_clothing_item_tags_item_tag",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    clothing_item_id: Mapped[int] = mapped_column(
        ForeignKey("clothing_items.id", ondelete="CASCADE"),
        index=True,
    )
    clothing_tag_id: Mapped[int] = mapped_column(
        ForeignKey("clothing_tags.id", ondelete="CASCADE"),
        index=True,
    )

    clothing_item: Mapped["ClothingItem"] = relationship(back_populates="tag_links")
    tag: Mapped["ClothingTag"] = relationship(back_populates="item_links")

