from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.core.enums import ClothingStatus, Formality, Season


class ClothingItemBase(BaseModel):
    name: str
    category: str
    subcategory: str | None = None
    primary_color: str | None = None
    secondary_color: str | None = None
    season: Season | None = None
    formality: Formality | None = None
    material: str | None = None
    brand: str | None = None
    notes: str | None = None
    status: ClothingStatus = ClothingStatus.CLEAN
    wear_count: int = 0
    last_worn_at: datetime | None = None
    extra_data: dict[str, Any] | None = None


class ClothingItemCreate(ClothingItemBase):
    pass


class ClothingItemUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    subcategory: str | None = None
    primary_color: str | None = None
    secondary_color: str | None = None
    season: Season | None = None
    formality: Formality | None = None
    material: str | None = None
    brand: str | None = None
    notes: str | None = None
    image_path: str | None = None
    status: ClothingStatus | None = None
    wear_count: int | None = None
    last_worn_at: datetime | None = None
    extra_data: dict[str, Any] | None = None


class ClothingItemFilterParams(BaseModel):
    category: str | None = None
    color: str | None = None
    season: Season | None = None
    formality: Formality | None = None
    status: ClothingStatus | None = None


class ClothingItemRead(ClothingItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    image_path: str | None = None
    image_url: str | None = None
    created_at: datetime
    updated_at: datetime
