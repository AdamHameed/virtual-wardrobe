from app.schemas.ai import (
    AIRecommendationLogCreate,
    AIRecommendationLogRead,
    AutoTagSuggestionCreate,
    AutoTagSuggestionGenerateRequest,
    AutoTagSuggestionRead,
    AutoTagSuggestionResult,
    ClothingEmbeddingCreate,
    ClothingEmbeddingRead,
    WardrobeAnalysisRequest,
    WardrobeAnalysisResult,
)
from app.schemas.auth import AuthResponse, CurrentUserResponse, LoginRequest, RegisterRequest
from app.schemas.clothing_item import ClothingItemCreate, ClothingItemRead, ClothingItemUpdate
from app.schemas.clothing_item_tag import (
    ClothingItemTagCreate,
    ClothingItemTagRead,
    ClothingItemTagUpdate,
)
from app.schemas.clothing_tag import ClothingTagCreate, ClothingTagRead, ClothingTagUpdate
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.outfit import OutfitCreate, OutfitRead, OutfitUpdate
from app.schemas.outfit_item import OutfitItemCreate, OutfitItemRead, OutfitItemUpdate
from app.schemas.outfit_plan import OutfitPlanCreate, OutfitPlanRead, OutfitPlanUpdate
from app.schemas.recommendation import (
    OutfitRecommendation,
    OutfitRecommendationRequest,
    OutfitRecommendationResponse,
    RecommendedOutfitItem,
)
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.schemas.wear_log import WearLogCreate, WearLogRead, WearLogUpdate
from app.weather.schemas import WeatherContext, WeatherInput, WindLevel

__all__ = [
    "UserCreate",
    "UserRead",
    "UserUpdate",
    "AutoTagSuggestionCreate",
    "AutoTagSuggestionRead",
    "AutoTagSuggestionGenerateRequest",
    "AutoTagSuggestionResult",
    "AIRecommendationLogCreate",
    "AIRecommendationLogRead",
    "ClothingEmbeddingCreate",
    "ClothingEmbeddingRead",
    "WardrobeAnalysisRequest",
    "WardrobeAnalysisResult",
    "RegisterRequest",
    "LoginRequest",
    "AuthResponse",
    "CurrentUserResponse",
    "ClothingItemCreate",
    "ClothingItemRead",
    "ClothingItemUpdate",
    "ClothingTagCreate",
    "ClothingTagRead",
    "ClothingTagUpdate",
    "PaginationParams",
    "PaginatedResponse",
    "ClothingItemTagCreate",
    "ClothingItemTagRead",
    "ClothingItemTagUpdate",
    "OutfitCreate",
    "OutfitRead",
    "OutfitUpdate",
    "OutfitItemCreate",
    "OutfitItemRead",
    "OutfitItemUpdate",
    "OutfitPlanCreate",
    "OutfitPlanRead",
    "OutfitPlanUpdate",
    "RecommendedOutfitItem",
    "OutfitRecommendation",
    "OutfitRecommendationRequest",
    "OutfitRecommendationResponse",
    "WeatherInput",
    "WeatherContext",
    "WindLevel",
    "WearLogCreate",
    "WearLogRead",
    "WearLogUpdate",
]
