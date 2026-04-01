from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Response, UploadFile, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_clothing_item_filters, get_db, get_pagination_params
from app.auth.dependencies import get_current_user
from app.core.enums import ClothingStatus, Formality, Season
from app.models.user import User
from app.schemas.clothing_item import (
    ClothingItemCreate,
    ClothingItemFilterParams,
    ClothingItemRead,
    ClothingItemUpdate,
)
from app.schemas.common import PaginatedResponse, PaginationParams
from app.services.clothing_item_service import ClothingItemService

router = APIRouter()


def build_clothing_item_create(
    name: Annotated[str, Form(...)],
    category: Annotated[str, Form(...)],
    subcategory: Annotated[str | None, Form()] = None,
    primary_color: Annotated[str | None, Form()] = None,
    secondary_color: Annotated[str | None, Form()] = None,
    season: Annotated[Season | None, Form()] = None,
    formality: Annotated[Formality | None, Form()] = None,
    material: Annotated[str | None, Form()] = None,
    brand: Annotated[str | None, Form()] = None,
    notes: Annotated[str | None, Form()] = None,
    status_value: Annotated[ClothingStatus, Form(alias="status")] = ClothingStatus.CLEAN,
) -> ClothingItemCreate:
    return ClothingItemCreate(
        name=name,
        category=category,
        subcategory=subcategory,
        primary_color=primary_color,
        secondary_color=secondary_color,
        season=season,
        formality=formality,
        material=material,
        brand=brand,
        notes=notes,
        status=status_value,
    )


def build_clothing_item_update(
    name: Annotated[str | None, Form()] = None,
    category: Annotated[str | None, Form()] = None,
    subcategory: Annotated[str | None, Form()] = None,
    primary_color: Annotated[str | None, Form()] = None,
    secondary_color: Annotated[str | None, Form()] = None,
    season: Annotated[Season | None, Form()] = None,
    formality: Annotated[Formality | None, Form()] = None,
    material: Annotated[str | None, Form()] = None,
    brand: Annotated[str | None, Form()] = None,
    notes: Annotated[str | None, Form()] = None,
    status_value: Annotated[ClothingStatus | None, Form(alias="status")] = None,
) -> ClothingItemUpdate:
    payload: dict[str, object] = {}
    if name is not None:
        payload["name"] = name
    if category is not None:
        payload["category"] = category
    if subcategory is not None:
        payload["subcategory"] = subcategory
    if primary_color is not None:
        payload["primary_color"] = primary_color
    if secondary_color is not None:
        payload["secondary_color"] = secondary_color
    if season is not None:
        payload["season"] = season
    if formality is not None:
        payload["formality"] = formality
    if material is not None:
        payload["material"] = material
    if brand is not None:
        payload["brand"] = brand
    if notes is not None:
        payload["notes"] = notes
    if status_value is not None:
        payload["status"] = status_value
    return ClothingItemUpdate(**payload)


@router.get("", response_model=PaginatedResponse[ClothingItemRead])
def list_clothing_items(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    filters: Annotated[ClothingItemFilterParams, Depends(get_clothing_item_filters)],
    pagination: Annotated[PaginationParams, Depends(get_pagination_params)],
) -> PaginatedResponse[ClothingItemRead]:
    return ClothingItemService(db).list_items(
        current_user=current_user,
        filters=filters,
        pagination=pagination,
    )


@router.post("", response_model=ClothingItemRead, status_code=status.HTTP_201_CREATED)
async def create_clothing_item(
    payload: Annotated[ClothingItemCreate, Depends(build_clothing_item_create)],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    image: UploadFile | None = File(default=None),
) -> ClothingItemRead:
    return await ClothingItemService(db).create_item(
        current_user=current_user,
        payload=payload,
        image=image,
    )


@router.get("/{item_id}", response_model=ClothingItemRead)
def get_clothing_item(
    item_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ClothingItemRead:
    return ClothingItemService(db).get_item(current_user=current_user, item_id=item_id)


@router.patch("/{item_id}", response_model=ClothingItemRead)
async def update_clothing_item(
    item_id: int,
    payload: Annotated[ClothingItemUpdate, Depends(build_clothing_item_update)],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    image: UploadFile | None = File(default=None),
) -> ClothingItemRead:
    return await ClothingItemService(db).update_item(
        current_user=current_user,
        item_id=item_id,
        payload=payload,
        image=image,
    )


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clothing_item(
    item_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Response:
    ClothingItemService(db).delete_item(current_user=current_user, item_id=item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
