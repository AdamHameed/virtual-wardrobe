from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.recommendation import (
    OutfitRecommendationRequest,
    OutfitRecommendationResponse,
)
from app.services.recommendation_service import RecommendationService

router = APIRouter()


@router.post("/outfits", response_model=OutfitRecommendationResponse)
def recommend_outfits(
    payload: OutfitRecommendationRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> OutfitRecommendationResponse:
    return RecommendationService(db).recommend_outfits(
        current_user=current_user,
        request=payload,
    )
