from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_pagination_params
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.outfit import OutfitCreate, OutfitRead, OutfitUpdate
from app.services.outfit_service import OutfitService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[OutfitRead])
def list_outfits(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    pagination: Annotated[PaginationParams, Depends(get_pagination_params)],
) -> PaginatedResponse[OutfitRead]:
    return OutfitService(db).list_outfits(current_user=current_user, pagination=pagination)


@router.post("", response_model=OutfitRead, status_code=status.HTTP_201_CREATED)
def create_outfit(
    payload: OutfitCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> OutfitRead:
    return OutfitService(db).create_outfit(current_user=current_user, payload=payload)


@router.get("/{outfit_id}", response_model=OutfitRead)
def get_outfit(
    outfit_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> OutfitRead:
    return OutfitService(db).get_outfit(current_user=current_user, outfit_id=outfit_id)


@router.patch("/{outfit_id}", response_model=OutfitRead)
def update_outfit(
    outfit_id: int,
    payload: OutfitUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> OutfitRead:
    return OutfitService(db).update_outfit(current_user=current_user, outfit_id=outfit_id, payload=payload)


@router.delete("/{outfit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_outfit(
    outfit_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Response:
    OutfitService(db).delete_outfit(current_user=current_user, outfit_id=outfit_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
