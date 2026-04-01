from sqlalchemy.orm import Session

from app.models.outfit import Outfit
from app.models.outfit_item import OutfitItem
from app.models.user import User
from app.repositories.clothing_item_repository import ClothingItemRepository
from app.repositories.outfit_repository import OutfitRepository
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.outfit import OutfitCreate, OutfitUpdate
from app.schemas.outfit_item import OutfitItemCreate
from app.services.exceptions import bad_request, not_found


class OutfitService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = OutfitRepository(db)
        self.clothing_item_repository = ClothingItemRepository(db)

    def list_outfits(self, *, current_user: User, pagination: PaginationParams) -> PaginatedResponse[Outfit]:
        items, total = self.repository.list_outfits(
            user_id=current_user.id,
            limit=pagination.limit,
            offset=pagination.offset,
        )
        return PaginatedResponse[Outfit](
            items=items,
            total=total,
            limit=pagination.limit,
            offset=pagination.offset,
        )

    def get_outfit(self, *, current_user: User, outfit_id: int) -> Outfit:
        outfit = self.repository.get_by_id(user_id=current_user.id, outfit_id=outfit_id)
        if outfit is None:
            raise not_found("Outfit not found.")
        return outfit

    def create_outfit(self, *, current_user: User, payload: OutfitCreate) -> Outfit:
        outfit = Outfit(
            user_id=current_user.id,
            name=payload.name,
            notes=payload.notes,
            extra_data=payload.extra_data,
        )
        outfit.items = self._build_outfit_items(
            current_user=current_user,
            items=payload.items,
        )
        return self.repository.create(outfit)

    def update_outfit(self, *, current_user: User, outfit_id: int, payload: OutfitUpdate) -> Outfit:
        outfit = self.get_outfit(current_user=current_user, outfit_id=outfit_id)
        updates = payload.model_dump(exclude_unset=True, exclude={"items"})
        for field, value in updates.items():
            setattr(outfit, field, value)

        if payload.items is not None:
            outfit.items = self._build_outfit_items(current_user=current_user, items=payload.items)

        return self.repository.update(outfit)

    def delete_outfit(self, *, current_user: User, outfit_id: int) -> None:
        outfit = self.get_outfit(current_user=current_user, outfit_id=outfit_id)
        self.repository.delete(outfit)

    def _build_outfit_items(
        self,
        *,
        current_user: User,
        items: list[OutfitItemCreate],
    ) -> list[OutfitItem]:
        clothing_item_ids = [item.clothing_item_id for item in items]
        owned_items = self.clothing_item_repository.get_many_by_ids(
            user_id=current_user.id,
            item_ids=clothing_item_ids,
        )
        owned_item_ids = {item.id for item in owned_items}

        missing = [item_id for item_id in clothing_item_ids if item_id not in owned_item_ids]
        if missing:
            raise bad_request("One or more clothing items do not belong to the authenticated user.")

        if len(clothing_item_ids) != len(set(clothing_item_ids)):
            raise bad_request("Duplicate clothing items are not allowed in a single outfit.")

        return [
            OutfitItem(
                clothing_item_id=item.clothing_item_id,
                role=item.role,
                position=item.position,
                extra_data=item.extra_data,
            )
            for item in items
        ]

