from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ClothingItemTagBase(BaseModel):
    clothing_item_id: int
    clothing_tag_id: int
    extra_data: dict[str, Any] | None = None


class ClothingItemTagCreate(ClothingItemTagBase):
    pass


class ClothingItemTagUpdate(BaseModel):
    extra_data: dict[str, Any] | None = None


class ClothingItemTagRead(ClothingItemTagBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

