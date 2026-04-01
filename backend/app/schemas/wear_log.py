from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class WearLogBase(BaseModel):
    outfit_id: int
    worn_at: datetime
    notes: str | None = None
    extra_data: dict[str, Any] | None = None


class WearLogCreate(WearLogBase):
    pass


class WearLogUpdate(BaseModel):
    outfit_id: int | None = None
    worn_at: datetime | None = None
    notes: str | None = None
    extra_data: dict[str, Any] | None = None


class WearLogRead(WearLogBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
