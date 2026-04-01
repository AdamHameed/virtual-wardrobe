from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.outfit_item import OutfitItemCreate, OutfitItemRead


class OutfitBase(BaseModel):
    name: str
    notes: str | None = None
    extra_data: dict[str, Any] | None = None


class OutfitCreate(OutfitBase):
    items: list[OutfitItemCreate] = Field(default_factory=list)


class OutfitUpdate(BaseModel):
    name: str | None = None
    notes: str | None = None
    extra_data: dict[str, Any] | None = None
    items: list[OutfitItemCreate] | None = None


class OutfitRead(OutfitBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    items: list[OutfitItemRead] = Field(default_factory=list)
