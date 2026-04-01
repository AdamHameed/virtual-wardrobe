from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.core.enums import OutfitItemRole


class OutfitItemBase(BaseModel):
    clothing_item_id: int
    role: OutfitItemRole
    position: int = 0
    extra_data: dict[str, Any] | None = None


class OutfitItemCreate(OutfitItemBase):
    pass


class OutfitItemUpdate(BaseModel):
    role: OutfitItemRole | None = None
    position: int | None = None
    extra_data: dict[str, Any] | None = None


class OutfitItemRead(OutfitItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    outfit_id: int
    created_at: datetime
    updated_at: datetime
