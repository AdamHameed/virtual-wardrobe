from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_pagination_params
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.clothing_tag import ClothingTagCreate, ClothingTagRead, ClothingTagUpdate
from app.schemas.common import PaginatedResponse, PaginationParams
from app.services.clothing_tag_service import ClothingTagService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[ClothingTagRead])
def list_tags(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    pagination: Annotated[PaginationParams, Depends(get_pagination_params)],
) -> PaginatedResponse[ClothingTagRead]:
    return ClothingTagService(db).list_tags(current_user=current_user, pagination=pagination)


@router.post("", response_model=ClothingTagRead, status_code=status.HTTP_201_CREATED)
def create_tag(
    payload: ClothingTagCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ClothingTagRead:
    return ClothingTagService(db).create_tag(current_user=current_user, payload=payload)


@router.get("/{tag_id}", response_model=ClothingTagRead)
def get_tag(
    tag_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ClothingTagRead:
    return ClothingTagService(db).get_tag(current_user=current_user, tag_id=tag_id)


@router.patch("/{tag_id}", response_model=ClothingTagRead)
def update_tag(
    tag_id: int,
    payload: ClothingTagUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ClothingTagRead:
    return ClothingTagService(db).update_tag(current_user=current_user, tag_id=tag_id, payload=payload)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Response:
    ClothingTagService(db).delete_tag(current_user=current_user, tag_id=tag_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
