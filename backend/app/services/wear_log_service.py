from sqlalchemy.orm import Session

from app.models.clothing_item import ClothingItem
from app.models.user import User
from app.models.wear_log import WearLog
from app.repositories.clothing_item_repository import ClothingItemRepository
from app.repositories.outfit_repository import OutfitRepository
from app.repositories.wear_log_repository import WearLogRepository
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.wear_log import WearLogCreate, WearLogUpdate
from app.services.exceptions import bad_request, not_found


class WearLogService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = WearLogRepository(db)
        self.outfit_repository = OutfitRepository(db)
        self.clothing_item_repository = ClothingItemRepository(db)

    def list_logs(self, *, current_user: User, pagination: PaginationParams) -> PaginatedResponse[WearLog]:
        items, total = self.repository.list_logs(
            user_id=current_user.id,
            limit=pagination.limit,
            offset=pagination.offset,
        )
        return PaginatedResponse[WearLog](
            items=items,
            total=total,
            limit=pagination.limit,
            offset=pagination.offset,
        )

    def get_log(self, *, current_user: User, wear_log_id: int) -> WearLog:
        wear_log = self.repository.get_by_id(user_id=current_user.id, wear_log_id=wear_log_id)
        if wear_log is None:
            raise not_found("Wear log not found.")
        return wear_log

    def create_log(self, *, current_user: User, payload: WearLogCreate) -> WearLog:
        outfit = self.outfit_repository.get_by_id(user_id=current_user.id, outfit_id=payload.outfit_id)
        if outfit is None:
            raise bad_request("Outfit does not belong to the authenticated user.")

        wear_log = WearLog(
            user_id=current_user.id,
            outfit_id=payload.outfit_id,
            worn_at=payload.worn_at,
            notes=payload.notes,
            extra_data=payload.extra_data,
        )
        created_log = self.repository.create(wear_log)
        self._increment_wear_stats(outfit.items, payload.worn_at)
        return created_log

    def update_log(self, *, current_user: User, wear_log_id: int, payload: WearLogUpdate) -> WearLog:
        wear_log = self.get_log(current_user=current_user, wear_log_id=wear_log_id)
        updates = payload.model_dump(exclude_unset=True)
        if "outfit_id" in updates:
            outfit = self.outfit_repository.get_by_id(user_id=current_user.id, outfit_id=updates["outfit_id"])
            if outfit is None:
                raise bad_request("Outfit does not belong to the authenticated user.")
        for field, value in updates.items():
            setattr(wear_log, field, value)
        return self.repository.update(wear_log)

    def delete_log(self, *, current_user: User, wear_log_id: int) -> None:
        wear_log = self.get_log(current_user=current_user, wear_log_id=wear_log_id)
        self.repository.delete(wear_log)

    def _increment_wear_stats(self, items: list, worn_at) -> None:
        for outfit_item in items:
            clothing_item: ClothingItem = outfit_item.clothing_item
            clothing_item.wear_count += 1
            clothing_item.last_worn_at = worn_at
            self.clothing_item_repository.update(clothing_item)

