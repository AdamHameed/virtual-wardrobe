from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    display_name: str | None = None
    is_active: bool = True
    extra_data: dict[str, Any] | None = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    display_name: str | None = None
    is_active: bool | None = None
    password: str | None = None
    extra_data: dict[str, Any] | None = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

