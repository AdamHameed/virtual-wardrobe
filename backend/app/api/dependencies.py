from collections.abc import Generator

from typing import Annotated

from fastapi import Query
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.clothing_item import ClothingItemFilterParams
from app.schemas.common import PaginationParams
from app.core.enums import ClothingStatus, Formality, Season


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_pagination_params(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> PaginationParams:
    return PaginationParams(limit=limit, offset=offset)


def get_clothing_item_filters(
    category: str | None = Query(default=None),
    color: str | None = Query(default=None),
    season: Season | None = Query(default=None),
    formality: Formality | None = Query(default=None),
    status_value: ClothingStatus | None = Query(default=None, alias="status"),
) -> ClothingItemFilterParams:
    return ClothingItemFilterParams(
        category=category,
        color=color,
        season=season,
        formality=formality,
        status=status_value,
    )
