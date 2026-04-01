from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Float

from app.core.enums import ProvenanceSource
from app.db.base import Base
from app.db.enum_utils import enum_values
from app.models.mixins import ExtraDataMixin, TimestampMixin


class ClothingEmbedding(TimestampMixin, ExtraDataMixin, Base):
    __tablename__ = "clothing_embeddings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    clothing_item_id: Mapped[int] = mapped_column(
        ForeignKey("clothing_items.id", ondelete="CASCADE"),
        index=True,
    )
    model_key: Mapped[str] = mapped_column(String(255), nullable=False)
    dimensions: Mapped[int] = mapped_column(Integer, nullable=False)
    vector: Mapped[list[float] | None] = mapped_column(ARRAY(Float), nullable=True)
    source: Mapped[ProvenanceSource] = mapped_column(
        Enum(ProvenanceSource, name="provenance_source_enum", values_callable=enum_values),
        default=ProvenanceSource.AI_GENERATED,
        nullable=False,
    )

    user: Mapped["User"] = relationship()
    clothing_item: Mapped["ClothingItem"] = relationship()
