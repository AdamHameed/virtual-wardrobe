from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.outfit_item import OutfitItem
from app.models.outfit import Outfit


class OutfitRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_outfits(self, *, user_id: int, limit: int = 20, offset: int = 0) -> tuple[list[Outfit], int]:
        base = (
            select(Outfit)
            .where(Outfit.user_id == user_id)
            .options(selectinload(Outfit.items).selectinload(OutfitItem.clothing_item))
        )
        statement = base.order_by(Outfit.created_at.desc()).limit(limit).offset(offset)
        return list(self.db.scalars(statement).all()), len(self.db.scalars(base).all())

    def get_by_id(self, *, user_id: int, outfit_id: int) -> Outfit | None:
        statement = (
            select(Outfit)
            .where(Outfit.id == outfit_id, Outfit.user_id == user_id)
            .options(selectinload(Outfit.items).selectinload(OutfitItem.clothing_item))
        )
        return self.db.scalar(statement)

    def create(self, outfit: Outfit) -> Outfit:
        self.db.add(outfit)
        self.db.commit()
        self.db.refresh(outfit)
        return outfit

    def update(self, outfit: Outfit) -> Outfit:
        self.db.add(outfit)
        self.db.commit()
        self.db.refresh(outfit)
        return outfit

    def delete(self, outfit: Outfit) -> None:
        self.db.delete(outfit)
        self.db.commit()
