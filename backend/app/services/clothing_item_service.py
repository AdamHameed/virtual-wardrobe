from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.clothing_item import ClothingItem
from app.models.user import User
from app.repositories.clothing_item_repository import ClothingItemRepository
from app.schemas.clothing_item import (
    ClothingItemCreate,
    ClothingItemFilterParams,
    ClothingItemUpdate,
)
from app.schemas.common import PaginatedResponse, PaginationParams
from app.services.exceptions import not_found
from app.utils.media import save_upload


class ClothingItemService:
    def __init__(self, db: Session) -> None:
        self.repository = ClothingItemRepository(db)

    def list_items(
        self,
        *,
        current_user: User,
        filters: ClothingItemFilterParams,
        pagination: PaginationParams,
    ) -> PaginatedResponse:
        items, total = self.repository.list_items(
            user_id=current_user.id,
            query=filters.query,
            category=filters.category,
            color=filters.color,
            season=filters.season.value if filters.season else None,
            formality=filters.formality.value if filters.formality else None,
            status=filters.status.value if filters.status else None,
            limit=pagination.limit,
            offset=pagination.offset,
        )
        return PaginatedResponse(
            items=items,
            total=total,
            limit=pagination.limit,
            offset=pagination.offset,
        )

    def get_item(self, *, current_user: User, item_id: int) -> ClothingItem:
        item = self.repository.get_by_id(user_id=current_user.id, item_id=item_id)
        if item is None:
            raise not_found("Clothing item not found.")
        return item

    async def create_item(
        self,
        *,
        current_user: User,
        payload: ClothingItemCreate,
        image: UploadFile | None,
    ) -> ClothingItem:
        image_path = await save_upload(image) if image else None
        item = ClothingItem(
            user_id=current_user.id,
            name=payload.name,
            category=payload.category,
            subcategory=payload.subcategory,
            primary_color=payload.primary_color,
            secondary_color=payload.secondary_color,
            season=payload.season,
            formality=payload.formality,
            material=payload.material,
            brand=payload.brand,
            notes=payload.notes,
            image_path=image_path,
            status=payload.status,
            wear_count=payload.wear_count,
            last_worn_at=payload.last_worn_at,
            extra_data=payload.extra_data,
        )
        return self.repository.create(item)

    async def update_item(
        self,
        *,
        current_user: User,
        item_id: int,
        payload: ClothingItemUpdate,
        image: UploadFile | None,
    ) -> ClothingItem:
        item = self.get_item(current_user=current_user, item_id=item_id)
        updates = payload.model_dump(exclude_unset=True)

        if image is not None:
            updates["image_path"] = await save_upload(image)

        for field, value in updates.items():
            setattr(item, field, value)

        return self.repository.update(item)

    def delete_item(self, *, current_user: User, item_id: int) -> None:
        item = self.get_item(current_user=current_user, item_id=item_id)
        self.repository.delete(item)
