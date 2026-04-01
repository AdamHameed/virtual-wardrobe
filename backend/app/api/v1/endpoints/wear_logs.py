from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_pagination_params
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.wear_log import WearLogCreate, WearLogRead, WearLogUpdate
from app.services.wear_log_service import WearLogService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[WearLogRead])
def list_wear_logs(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    pagination: Annotated[PaginationParams, Depends(get_pagination_params)],
) -> PaginatedResponse[WearLogRead]:
    return WearLogService(db).list_logs(current_user=current_user, pagination=pagination)


@router.post("", response_model=WearLogRead, status_code=status.HTTP_201_CREATED)
def create_wear_log(
    payload: WearLogCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> WearLogRead:
    return WearLogService(db).create_log(current_user=current_user, payload=payload)


@router.get("/{wear_log_id}", response_model=WearLogRead)
def get_wear_log(
    wear_log_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> WearLogRead:
    return WearLogService(db).get_log(current_user=current_user, wear_log_id=wear_log_id)


@router.patch("/{wear_log_id}", response_model=WearLogRead)
def update_wear_log(
    wear_log_id: int,
    payload: WearLogUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> WearLogRead:
    return WearLogService(db).update_log(current_user=current_user, wear_log_id=wear_log_id, payload=payload)


@router.delete("/{wear_log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wear_log(
    wear_log_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Response:
    WearLogService(db).delete_log(current_user=current_user, wear_log_id=wear_log_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
