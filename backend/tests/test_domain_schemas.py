from datetime import date, datetime, timezone

from app.core.enums import ClothingStatus, OutfitItemRole
from app.schemas.clothing_item import ClothingItemCreate
from app.schemas.outfit import OutfitCreate
from app.schemas.outfit_plan import OutfitPlanCreate
from app.schemas.outfit_item import OutfitItemCreate
from app.schemas.user import UserCreate
from app.schemas.wear_log import WearLogCreate


def test_clothing_item_schema_accepts_extended_fields() -> None:
    payload = ClothingItemCreate(
        name="Oxford Shirt",
        category="tops",
        subcategory="shirt",
        primary_color="blue",
        secondary_color="white",
        status=ClothingStatus.CLEAN,
        wear_count=3,
    )

    assert payload.category == "tops"
    assert payload.status == ClothingStatus.CLEAN


def test_outfit_plans_and_wear_logs_support_calendar_and_timestamp_fields() -> None:
    plan = OutfitPlanCreate(outfit_id=2, planned_for=date(2026, 4, 1))
    wear_log = WearLogCreate(
        outfit_id=2,
        worn_at=datetime(2026, 4, 1, 14, 30, tzinfo=timezone.utc),
    )

    assert plan.planned_for.isoformat() == "2026-04-01"
    assert wear_log.worn_at.tzinfo is not None
    assert OutfitItemRole.TOP.value == "top"


def test_outfit_schema_supports_embedded_item_roles() -> None:
    payload = OutfitCreate(
        name="Rainy Day",
        items=[
            OutfitItemCreate(clothing_item_id=10, role=OutfitItemRole.TOP),
            OutfitItemCreate(clothing_item_id=11, role=OutfitItemRole.OUTERWEAR),
        ],
    )

    assert len(payload.items) == 2
    assert payload.items[1].role == OutfitItemRole.OUTERWEAR


def test_user_schema_validates_email_payloads() -> None:
    user = UserCreate(
        email="closet@example.com",
        display_name="Closet Owner",
        password="super-secret",
    )

    assert user.email == "closet@example.com"
