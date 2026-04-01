from sqlalchemy.orm import Session

from app.models.clothing_tag import ClothingTag
from app.models.user import User
from app.repositories.clothing_tag_repository import ClothingTagRepository
from app.schemas.clothing_tag import ClothingTagCreate, ClothingTagUpdate
from app.schemas.common import PaginatedResponse, PaginationParams
from app.services.exceptions import not_found


class ClothingTagService:
    def __init__(self, db: Session) -> None:
        self.repository = ClothingTagRepository(db)

    def list_tags(self, *, current_user: User, pagination: PaginationParams) -> PaginatedResponse[ClothingTag]:
        items, total = self.repository.list_tags(
            user_id=current_user.id,
            limit=pagination.limit,
            offset=pagination.offset,
        )
        return PaginatedResponse[ClothingTag](
            items=items,
            total=total,
            limit=pagination.limit,
            offset=pagination.offset,
        )

    def get_tag(self, *, current_user: User, tag_id: int) -> ClothingTag:
        tag = self.repository.get_by_id(user_id=current_user.id, tag_id=tag_id)
        if tag is None:
            raise not_found("Tag not found.")
        return tag

    def create_tag(self, *, current_user: User, payload: ClothingTagCreate) -> ClothingTag:
        tag = ClothingTag(
            user_id=current_user.id,
            name=payload.name,
            description=payload.description,
            source=payload.source,
            extra_data=payload.extra_data,
        )
        return self.repository.create(tag)

    def update_tag(self, *, current_user: User, tag_id: int, payload: ClothingTagUpdate) -> ClothingTag:
        tag = self.get_tag(current_user=current_user, tag_id=tag_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(tag, field, value)
        return self.repository.update(tag)

    def delete_tag(self, *, current_user: User, tag_id: int) -> None:
        tag = self.get_tag(current_user=current_user, tag_id=tag_id)
        self.repository.delete(tag)

