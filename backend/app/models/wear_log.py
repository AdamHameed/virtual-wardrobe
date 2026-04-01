from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import ExtraDataMixin, TimestampMixin


class WearLog(TimestampMixin, ExtraDataMixin, Base):
    __tablename__ = "wear_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    outfit_id: Mapped[int] = mapped_column(ForeignKey("outfits.id", ondelete="CASCADE"), index=True)
    worn_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(back_populates="wear_logs")
    outfit: Mapped["Outfit"] = relationship(back_populates="wear_logs")

