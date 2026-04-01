from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import ProvenanceSource, SuggestionStatus


class AutoTagSuggestionBase(BaseModel):
    clothing_item_id: int
    suggested_tag: str
    rationale: str | None = None
    confidence: float | None = None
    source: ProvenanceSource = ProvenanceSource.AI_GENERATED
    status: SuggestionStatus = SuggestionStatus.PENDING
    extra_data: dict[str, Any] | None = None


class AutoTagSuggestionCreate(AutoTagSuggestionBase):
    pass


class AutoTagSuggestionRead(AutoTagSuggestionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class AutoTagSuggestionGenerateRequest(BaseModel):
    clothing_item_id: int


class AutoTagSuggestionResult(BaseModel):
    source: ProvenanceSource = ProvenanceSource.MANUAL
    suggested_tag: str
    confidence: float | None = None
    rationale: str | None = None


class AIRecommendationLogBase(BaseModel):
    request_type: str
    source: ProvenanceSource = ProvenanceSource.RULE_BASED
    score: float | None = None
    rationale: str | None = None
    extra_data: dict[str, Any] | None = None


class AIRecommendationLogCreate(AIRecommendationLogBase):
    pass


class AIRecommendationLogRead(AIRecommendationLogBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class ClothingEmbeddingBase(BaseModel):
    clothing_item_id: int
    model_key: str
    dimensions: int
    vector: list[float] | None = None
    source: ProvenanceSource = ProvenanceSource.AI_GENERATED
    extra_data: dict[str, Any] | None = None


class ClothingEmbeddingCreate(ClothingEmbeddingBase):
    pass


class ClothingEmbeddingRead(ClothingEmbeddingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class WardrobeAnalysisRequest(BaseModel):
    include_outfit_history: bool = True
    include_unused_items: bool = True


class WardrobeAnalysisResult(BaseModel):
    source: ProvenanceSource
    summary: str
    insights: list[str] = Field(default_factory=list)
