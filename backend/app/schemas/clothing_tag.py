from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.core.enums import ClothingTagSource


class ClothingTagBase(BaseModel):
    name: str
    description: str | None = None
    source: ClothingTagSource = ClothingTagSource.MANUAL
    extra_data: dict[str, Any] | None = None


class ClothingTagCreate(ClothingTagBase):
    pass


class ClothingTagUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    source: ClothingTagSource | None = None
    extra_data: dict[str, Any] | None = None


class ClothingTagRead(ClothingTagBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
