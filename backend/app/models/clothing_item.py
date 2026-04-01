from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import ClothingStatus, Formality, Season
from app.db.base import Base
from app.models.mixins import ExtraDataMixin, TimestampMixin
from app.utils.media import build_media_url


class ClothingItem(TimestampMixin, ExtraDataMixin, Base):
    __tablename__ = "clothing_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    subcategory: Mapped[str | None] = mapped_column(String(100), nullable=True)
    primary_color: Mapped[str | None] = mapped_column(String(100), nullable=True)
    secondary_color: Mapped[str | None] = mapped_column(String(100), nullable=True)
    season: Mapped[Season | None] = mapped_column(
        Enum(Season, name="season_enum"),
        nullable=True,
    )
    formality: Mapped[Formality | None] = mapped_column(
        Enum(Formality, name="formality_enum"),
        nullable=True,
    )
    material: Mapped[str | None] = mapped_column(String(100), nullable=True)
    brand: Mapped[str | None] = mapped_column(String(100), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[ClothingStatus] = mapped_column(
        Enum(ClothingStatus, name="clothing_status_enum"),
        default=ClothingStatus.CLEAN,
        nullable=False,
    )
    wear_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_worn_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(back_populates="clothing_items")
    tag_links: Mapped[list["ClothingItemTag"]] = relationship(
        back_populates="clothing_item",
        cascade="all, delete-orphan",
    )
    outfit_items: Mapped[list["OutfitItem"]] = relationship(back_populates="clothing_item")

    @property
    def image_url(self) -> str | None:
        return build_media_url(self.image_path)

