from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.outfit_plan import OutfitPlan


class OutfitPlanRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_plans(self, *, user_id: int, limit: int = 20, offset: int = 0) -> tuple[list[OutfitPlan], int]:
        base = select(OutfitPlan).where(OutfitPlan.user_id == user_id)
        statement = base.order_by(OutfitPlan.planned_for.asc()).limit(limit).offset(offset)
        return list(self.db.scalars(statement).all()), len(self.db.scalars(base).all())

    def get_by_id(self, *, user_id: int, plan_id: int) -> OutfitPlan | None:
        statement = select(OutfitPlan).where(
            OutfitPlan.id == plan_id,
            OutfitPlan.user_id == user_id,
        )
        return self.db.scalar(statement)

    def create(self, plan: OutfitPlan) -> OutfitPlan:
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        return plan

    def update(self, plan: OutfitPlan) -> OutfitPlan:
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        return plan

    def delete(self, plan: OutfitPlan) -> None:
        self.db.delete(plan)
        self.db.commit()

