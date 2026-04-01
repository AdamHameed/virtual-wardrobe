from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_pagination_params
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.outfit_plan import OutfitPlanCreate, OutfitPlanRead, OutfitPlanUpdate
from app.services.outfit_plan_service import OutfitPlanService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[OutfitPlanRead])
def list_outfit_plans(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    pagination: Annotated[PaginationParams, Depends(get_pagination_params)],
) -> PaginatedResponse[OutfitPlanRead]:
    return OutfitPlanService(db).list_plans(current_user=current_user, pagination=pagination)


@router.post("", response_model=OutfitPlanRead, status_code=status.HTTP_201_CREATED)
def create_outfit_plan(
    payload: OutfitPlanCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> OutfitPlanRead:
    return OutfitPlanService(db).create_plan(current_user=current_user, payload=payload)


@router.get("/{plan_id}", response_model=OutfitPlanRead)
def get_outfit_plan(
    plan_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> OutfitPlanRead:
    return OutfitPlanService(db).get_plan(current_user=current_user, plan_id=plan_id)


@router.patch("/{plan_id}", response_model=OutfitPlanRead)
def update_outfit_plan(
    plan_id: int,
    payload: OutfitPlanUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> OutfitPlanRead:
    return OutfitPlanService(db).update_plan(current_user=current_user, plan_id=plan_id, payload=payload)


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_outfit_plan(
    plan_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Response:
    OutfitPlanService(db).delete_plan(current_user=current_user, plan_id=plan_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
