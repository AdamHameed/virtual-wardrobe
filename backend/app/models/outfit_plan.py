from datetime import date

from sqlalchemy import Date, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import ExtraDataMixin, TimestampMixin


class OutfitPlan(TimestampMixin, ExtraDataMixin, Base):
    __tablename__ = "outfit_plans"
    __table_args__ = (
        UniqueConstraint("user_id", "outfit_id", "planned_for", name="uq_outfit_plans_user_outfit_day"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    outfit_id: Mapped[int] = mapped_column(ForeignKey("outfits.id", ondelete="CASCADE"), index=True)
    planned_for: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(back_populates="outfit_plans")
    outfit: Mapped["Outfit"] = relationship(back_populates="plans")

