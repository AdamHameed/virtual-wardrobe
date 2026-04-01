from sqlalchemy.orm import Session

from app.ai.auto_tagging import AutoTaggingEngine, NoOpAutoTaggingEngine
from app.ai.wardrobe_analysis import NoOpWardrobeAnalysisEngine, WardrobeAnalysisEngine
from app.models.user import User
from app.recommendations.engine import RecommendationEngine
from app.recommendations.rule_based import RuleBasedRecommendationEngine
from app.repositories.clothing_item_repository import ClothingItemRepository
from app.schemas.recommendation import (
    OutfitRecommendationRequest,
    OutfitRecommendationResponse,
)
from app.weather.manual import ManualWeatherService
from app.weather.service import WeatherService


class RecommendationService:
    def __init__(
        self,
        db: Session,
        engine: RecommendationEngine | None = None,
        weather_service: WeatherService | None = None,
        auto_tagging_engine: AutoTaggingEngine | None = None,
        wardrobe_analysis_engine: WardrobeAnalysisEngine | None = None,
    ) -> None:
        self.engine = engine or RuleBasedRecommendationEngine(
            ClothingItemRepository(db),
        )
        self.weather_service = weather_service or ManualWeatherService()
        self.auto_tagging_engine = auto_tagging_engine or NoOpAutoTaggingEngine()
        self.wardrobe_analysis_engine = wardrobe_analysis_engine or NoOpWardrobeAnalysisEngine()

    def recommend_outfits(
        self,
        *,
        current_user: User,
        request: OutfitRecommendationRequest,
    ) -> OutfitRecommendationResponse:
        weather = self.weather_service.resolve_weather(request.weather)
        return self.engine.recommend_outfits(
            current_user=current_user,
            request=request,
            weather=weather,
        )
