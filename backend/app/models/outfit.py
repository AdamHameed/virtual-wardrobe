from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import ExtraDataMixin, TimestampMixin


class Outfit(TimestampMixin, ExtraDataMixin, Base):
    __tablename__ = "outfits"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(back_populates="outfits")
    items: Mapped[list["OutfitItem"]] = relationship(
        back_populates="outfit",
        cascade="all, delete-orphan",
    )
    plans: Mapped[list["OutfitPlan"]] = relationship(
        back_populates="outfit",
        cascade="all, delete-orphan",
    )
    wear_logs: Mapped[list["WearLog"]] = relationship(
        back_populates="outfit",
        cascade="all, delete-orphan",
    )

