from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.db.base import Base
from app.models.mixins import ExtraDataMixin, TimestampMixin


class User(TimestampMixin, ExtraDataMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    clothing_items: Mapped[list["ClothingItem"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    clothing_tags: Mapped[list["ClothingTag"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    outfits: Mapped[list["Outfit"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    outfit_plans: Mapped[list["OutfitPlan"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    wear_logs: Mapped[list["WearLog"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

