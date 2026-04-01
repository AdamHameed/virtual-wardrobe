from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.clothing_tag import ClothingTag


class ClothingTagRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_tags(self, *, user_id: int, limit: int = 20, offset: int = 0) -> tuple[list[ClothingTag], int]:
        base = select(ClothingTag).where(ClothingTag.user_id == user_id)
        statement = base.order_by(ClothingTag.name.asc()).limit(limit).offset(offset)
        return list(self.db.scalars(statement).all()), len(self.db.scalars(base).all())

    def get_by_id(self, *, user_id: int, tag_id: int) -> ClothingTag | None:
        statement = select(ClothingTag).where(
            ClothingTag.id == tag_id,
            ClothingTag.user_id == user_id,
        )
        return self.db.scalar(statement)

    def create(self, tag: ClothingTag) -> ClothingTag:
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def update(self, tag: ClothingTag) -> ClothingTag:
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def delete(self, tag: ClothingTag) -> None:
        self.db.delete(tag)
        self.db.commit()

