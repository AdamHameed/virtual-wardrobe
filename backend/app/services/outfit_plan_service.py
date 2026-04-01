from sqlalchemy.orm import Session

from app.models.outfit_plan import OutfitPlan
from app.models.user import User
from app.repositories.outfit_plan_repository import OutfitPlanRepository
from app.repositories.outfit_repository import OutfitRepository
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.outfit_plan import OutfitPlanCreate, OutfitPlanUpdate
from app.services.exceptions import bad_request, not_found


class OutfitPlanService:
    def __init__(self, db: Session) -> None:
        self.repository = OutfitPlanRepository(db)
        self.outfit_repository = OutfitRepository(db)

    def list_plans(self, *, current_user: User, pagination: PaginationParams) -> PaginatedResponse:
        items, total = self.repository.list_plans(
            user_id=current_user.id,
            limit=pagination.limit,
            offset=pagination.offset,
        )
        return PaginatedResponse(
            items=items,
            total=total,
            limit=pagination.limit,
            offset=pagination.offset,
        )

    def get_plan(self, *, current_user: User, plan_id: int) -> OutfitPlan:
        plan = self.repository.get_by_id(user_id=current_user.id, plan_id=plan_id)
        if plan is None:
            raise not_found("Outfit plan not found.")
        return plan

    def create_plan(self, *, current_user: User, payload: OutfitPlanCreate) -> OutfitPlan:
        self._ensure_outfit_owned(current_user=current_user, outfit_id=payload.outfit_id)
        plan = OutfitPlan(
            user_id=current_user.id,
            outfit_id=payload.outfit_id,
            planned_for=payload.planned_for,
            notes=payload.notes,
            extra_data=payload.extra_data,
        )
        return self.repository.create(plan)

    def update_plan(self, *, current_user: User, plan_id: int, payload: OutfitPlanUpdate) -> OutfitPlan:
        plan = self.get_plan(current_user=current_user, plan_id=plan_id)
        updates = payload.model_dump(exclude_unset=True)
        if "outfit_id" in updates:
            self._ensure_outfit_owned(current_user=current_user, outfit_id=updates["outfit_id"])
        for field, value in updates.items():
            setattr(plan, field, value)
        return self.repository.update(plan)

    def delete_plan(self, *, current_user: User, plan_id: int) -> None:
        plan = self.get_plan(current_user=current_user, plan_id=plan_id)
        self.repository.delete(plan)

    def _ensure_outfit_owned(self, *, current_user: User, outfit_id: int) -> None:
        if self.outfit_repository.get_by_id(user_id=current_user.id, outfit_id=outfit_id) is None:
            raise bad_request("Outfit does not belong to the authenticated user.")
