from datetime import datetime, timedelta, timezone

from app.core.enums import ClothingStatus, Formality, Season
from app.models.clothing_item import ClothingItem
from app.models.user import User
from app.recommendations.rule_based import RuleBasedRecommendationEngine
from app.schemas.recommendation import OutfitRecommendationRequest
from app.weather.manual import ManualWeatherService
from app.weather.schemas import WeatherInput, WindLevel


class FakeClothingItemRepository:
    def __init__(self, items: list[ClothingItem]) -> None:
        self.items = items

    def list_available_items_for_user(self, *, user_id: int) -> list[ClothingItem]:
        return [
            item
            for item in self.items
            if item.user_id == user_id
            and item.status not in {ClothingStatus.DIRTY, ClothingStatus.UNAVAILABLE}
        ]


def make_item(
    *,
    item_id: int,
    user_id: int,
    name: str,
    category: str,
    subcategory: str | None = None,
    primary_color: str | None = None,
    season: Season | None = None,
    formality: Formality | None = None,
    status: ClothingStatus = ClothingStatus.CLEAN,
    wear_count: int = 0,
    last_worn_at: datetime | None = None,
) -> ClothingItem:
    now = datetime.now(timezone.utc)
    return ClothingItem(
        id=item_id,
        user_id=user_id,
        name=name,
        category=category,
        subcategory=subcategory,
        primary_color=primary_color,
        season=season,
        formality=formality,
        status=status,
        wear_count=wear_count,
        last_worn_at=last_worn_at,
        created_at=now,
        updated_at=now,
    )


def test_rule_based_engine_returns_ranked_outfits() -> None:
    user = User(id=1, email="user@example.com", hashed_password="hashed", is_active=True)
    items = [
        make_item(item_id=1, user_id=1, name="Oxford", category="tops", primary_color="blue", season=Season.SPRING, formality=Formality.SMART_CASUAL, wear_count=1, last_worn_at=datetime.now(timezone.utc) - timedelta(days=20)),
        make_item(item_id=2, user_id=1, name="Chinos", category="bottoms", primary_color="beige", season=Season.SPRING, formality=Formality.SMART_CASUAL, wear_count=2, last_worn_at=datetime.now(timezone.utc) - timedelta(days=15)),
        make_item(item_id=3, user_id=1, name="Loafers", category="shoes", primary_color="brown", season=Season.SPRING, formality=Formality.SMART_CASUAL, wear_count=0, last_worn_at=None),
        make_item(item_id=4, user_id=1, name="Rain Jacket", category="outerwear", primary_color="navy", season=Season.SPRING, formality=Formality.SMART_CASUAL, wear_count=0, last_worn_at=None),
        make_item(item_id=5, user_id=1, name="Dirty Tee", category="tops", status=ClothingStatus.DIRTY),
    ]
    engine = RuleBasedRecommendationEngine(FakeClothingItemRepository(items))
    weather = ManualWeatherService().resolve_weather(
        WeatherInput(
            temperature_c=9,
            condition="rain",
            precipitation=True,
            wind_level=WindLevel.WINDY,
        )
    )

    response = engine.recommend_outfits(
        current_user=user,
        request=OutfitRecommendationRequest(
            season=Season.SPRING,
            occasion="smart casual",
            weather=WeatherInput(
                temperature_c=9,
                condition="rain",
                precipitation=True,
                wind_level=WindLevel.WINDY,
            ),
            limit=3,
        ),
        weather=weather,
    )

    assert response.recommendations
    first = response.recommendations[0]
    assert first.source == "rule_based"
    assert first.score > 0
    assert {selected.role.value for selected in first.selected_items} >= {"top", "bottom", "shoes", "outerwear"}
    assert all(selected.item.name != "Dirty Tee" for selected in first.selected_items)
