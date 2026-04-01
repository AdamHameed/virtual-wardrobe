from abc import ABC, abstractmethod

from app.models.user import User
from app.schemas.recommendation import (
    OutfitRecommendationRequest,
    OutfitRecommendationResponse,
)
from app.weather.schemas import WeatherContext


class RecommendationEngine(ABC):
    @abstractmethod
    def recommend_outfits(
        self,
        *,
        current_user: User,
        request: OutfitRecommendationRequest,
        weather: WeatherContext | None,
    ) -> OutfitRecommendationResponse:
        raise NotImplementedError
