from sqlalchemy import Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import ProvenanceSource
from app.db.base import Base
from app.models.mixins import ExtraDataMixin, TimestampMixin


class AIRecommendationLog(TimestampMixin, ExtraDataMixin, Base):
    __tablename__ = "ai_recommendation_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    request_type: Mapped[str] = mapped_column(String(100), nullable=False)
    source: Mapped[ProvenanceSource] = mapped_column(
        Enum(ProvenanceSource, name="provenance_source_enum"),
        default=ProvenanceSource.RULE_BASED,
        nullable=False,
    )
    score: Mapped[float | None] = mapped_column(Numeric(6, 3), nullable=True)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship()
