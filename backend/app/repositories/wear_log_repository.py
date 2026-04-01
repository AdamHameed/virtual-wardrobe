from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.wear_log import WearLog


class WearLogRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_logs(self, *, user_id: int, limit: int = 20, offset: int = 0) -> tuple[list[WearLog], int]:
        base = select(WearLog).where(WearLog.user_id == user_id)
        statement = base.order_by(WearLog.worn_at.desc()).limit(limit).offset(offset)
        return list(self.db.scalars(statement).all()), len(self.db.scalars(base).all())

    def get_by_id(self, *, user_id: int, wear_log_id: int) -> WearLog | None:
        statement = select(WearLog).where(
            WearLog.id == wear_log_id,
            WearLog.user_id == user_id,
        )
        return self.db.scalar(statement)

    def create(self, wear_log: WearLog) -> WearLog:
        self.db.add(wear_log)
        self.db.commit()
        self.db.refresh(wear_log)
        return wear_log

    def update(self, wear_log: WearLog) -> WearLog:
        self.db.add(wear_log)
        self.db.commit()
        self.db.refresh(wear_log)
        return wear_log

    def delete(self, wear_log: WearLog) -> None:
        self.db.delete(wear_log)
        self.db.commit()

