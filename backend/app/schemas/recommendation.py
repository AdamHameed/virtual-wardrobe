from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import ProvenanceSource
from app.core.enums import Formality, OutfitItemRole, Season
from app.schemas.clothing_item import ClothingItemRead
from app.weather.schemas import WeatherContext, WeatherInput


class OutfitRecommendationRequest(BaseModel):
    weather: WeatherInput | None = None
    season: Season | None = None
    occasion: str | None = None
    limit: int = Field(default=5, ge=1, le=20)


class RecommendedOutfitItem(BaseModel):
    role: OutfitItemRole
    item: ClothingItemRead


class OutfitRecommendation(BaseModel):
    source: ProvenanceSource
    score: float
    explanation: list[str] = Field(default_factory=list)
    selected_items: list[RecommendedOutfitItem] = Field(default_factory=list)


class OutfitRecommendationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    recommendations: list[OutfitRecommendation] = Field(default_factory=list)


class RecommendationContext(BaseModel):
    target_season: Season | None = None
    target_formality: Formality | None = None
    weather: WeatherContext | None = None
    require_outerwear: bool = False
