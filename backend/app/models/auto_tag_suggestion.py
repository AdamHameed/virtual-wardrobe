from sqlalchemy import Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import ProvenanceSource, SuggestionStatus
from app.db.base import Base
from app.db.enum_utils import enum_values
from app.models.mixins import ExtraDataMixin, TimestampMixin


class AutoTagSuggestion(TimestampMixin, ExtraDataMixin, Base):
    __tablename__ = "auto_tag_suggestions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    clothing_item_id: Mapped[int] = mapped_column(
        ForeignKey("clothing_items.id", ondelete="CASCADE"),
        index=True,
    )
    suggested_tag: Mapped[str] = mapped_column(String(100), nullable=False)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Numeric(4, 3), nullable=True)
    source: Mapped[ProvenanceSource] = mapped_column(
        Enum(ProvenanceSource, name="provenance_source_enum", values_callable=enum_values),
        default=ProvenanceSource.AI_GENERATED,
        nullable=False,
    )
    status: Mapped[SuggestionStatus] = mapped_column(
        Enum(SuggestionStatus, name="suggestion_status_enum", values_callable=enum_values),
        default=SuggestionStatus.PENDING,
        nullable=False,
    )

    user: Mapped["User"] = relationship()
    clothing_item: Mapped["ClothingItem"] = relationship()
