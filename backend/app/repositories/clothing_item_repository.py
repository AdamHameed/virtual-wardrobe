from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.enums import ClothingStatus
from app.models.clothing_item import ClothingItem


class ClothingItemRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_items(
        self,
        *,
        user_id: int,
        category: str | None = None,
        color: str | None = None,
        season: str | None = None,
        formality: str | None = None,
        status: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[ClothingItem], int]:
        statement = select(ClothingItem).where(ClothingItem.user_id == user_id)
        count_statement = select(ClothingItem).where(ClothingItem.user_id == user_id)

        if category:
            statement = statement.where(ClothingItem.category == category)
            count_statement = count_statement.where(ClothingItem.category == category)
        if color:
            color_clause = or_(
                ClothingItem.primary_color == color,
                ClothingItem.secondary_color == color,
            )
            statement = statement.where(color_clause)
            count_statement = count_statement.where(color_clause)
        if season:
            statement = statement.where(ClothingItem.season == season)
            count_statement = count_statement.where(ClothingItem.season == season)
        if formality:
            statement = statement.where(ClothingItem.formality == formality)
            count_statement = count_statement.where(ClothingItem.formality == formality)
        if status:
            statement = statement.where(ClothingItem.status == status)
            count_statement = count_statement.where(ClothingItem.status == status)

        statement = statement.order_by(ClothingItem.created_at.desc()).limit(limit).offset(offset)
        items = list(self.db.scalars(statement).all())
        total = len(self.db.scalars(count_statement).all())
        return items, total

    def get_by_id(self, *, user_id: int, item_id: int) -> ClothingItem | None:
        statement = select(ClothingItem).where(
            ClothingItem.id == item_id,
            ClothingItem.user_id == user_id,
        )
        return self.db.scalar(statement)

    def get_many_by_ids(self, *, user_id: int, item_ids: list[int]) -> list[ClothingItem]:
        if not item_ids:
            return []
        statement = select(ClothingItem).where(
            ClothingItem.user_id == user_id,
            ClothingItem.id.in_(item_ids),
        )
        return list(self.db.scalars(statement).all())

    def create(self, item: ClothingItem) -> ClothingItem:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: ClothingItem) -> ClothingItem:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: ClothingItem) -> None:
        self.db.delete(item)
        self.db.commit()

    def list_available_items_for_user(self, *, user_id: int) -> list[ClothingItem]:
        statement = (
            select(ClothingItem)
            .where(
                ClothingItem.user_id == user_id,
                ClothingItem.status.notin_(
                    [ClothingStatus.DIRTY, ClothingStatus.UNAVAILABLE],
                ),
            )
            .order_by(ClothingItem.created_at.desc())
        )
        return list(self.db.scalars(statement).all())
