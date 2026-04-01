from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class OutfitPlanBase(BaseModel):
    outfit_id: int
    planned_for: date
    notes: str | None = None
    extra_data: dict[str, Any] | None = None


class OutfitPlanCreate(OutfitPlanBase):
    pass


class OutfitPlanUpdate(BaseModel):
    outfit_id: int | None = None
    planned_for: date | None = None
    notes: str | None = None
    extra_data: dict[str, Any] | None = None


class OutfitPlanRead(OutfitPlanBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
