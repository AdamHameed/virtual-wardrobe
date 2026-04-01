from sqlalchemy import Enum, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import OutfitItemRole
from app.db.base import Base
from app.db.enum_utils import enum_values
from app.models.mixins import ExtraDataMixin, TimestampMixin


class OutfitItem(TimestampMixin, ExtraDataMixin, Base):
    __tablename__ = "outfit_items"
    __table_args__ = (
        UniqueConstraint("outfit_id", "clothing_item_id", name="uq_outfit_items_outfit_item"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    outfit_id: Mapped[int] = mapped_column(ForeignKey("outfits.id", ondelete="CASCADE"), index=True)
    clothing_item_id: Mapped[int] = mapped_column(
        ForeignKey("clothing_items.id", ondelete="RESTRICT"),
        index=True,
    )
    role: Mapped[OutfitItemRole] = mapped_column(
        Enum(OutfitItemRole, name="outfit_item_role_enum", values_callable=enum_values),
        nullable=False,
    )
    position: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    outfit: Mapped["Outfit"] = relationship(back_populates="items")
    clothing_item: Mapped["ClothingItem"] = relationship(back_populates="outfit_items")
