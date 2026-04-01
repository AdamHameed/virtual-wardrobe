from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from itertools import product

from app.core.enums import Formality, OutfitItemRole, ProvenanceSource, Season
from app.models.clothing_item import ClothingItem
from app.models.user import User
from app.repositories.clothing_item_repository import ClothingItemRepository
from app.recommendations.engine import RecommendationEngine
from app.schemas.clothing_item import ClothingItemRead
from app.schemas.recommendation import (
    OutfitRecommendation,
    OutfitRecommendationRequest,
    OutfitRecommendationResponse,
    RecommendedOutfitItem,
    RecommendationContext,
)
from app.weather.schemas import WeatherContext, WindLevel

TOP_CATEGORIES = {"tops", "top", "shirt", "shirts", "sweater", "hoodie", "blouse", "t-shirt"}
BOTTOM_CATEGORIES = {"bottoms", "bottom", "pants", "trousers", "jeans", "skirt", "shorts"}
SHOE_CATEGORIES = {"shoes", "shoe", "sneakers", "boots", "loafers", "heels", "sandals"}
OUTERWEAR_CATEGORIES = {"outerwear", "jacket", "coat", "blazer", "cardigan"}
NEUTRAL_COLORS = {"black", "white", "gray", "grey", "navy", "beige", "brown", "cream", "tan", "olive"}
COLOR_FAMILIES: dict[str, set[str]] = {
    "blue": {"blue", "navy", "denim"},
    "red": {"red", "burgundy", "maroon"},
    "green": {"green", "olive", "sage"},
    "brown": {"brown", "beige", "tan", "camel", "cream"},
    "black": {"black", "gray", "grey", "white"},
}
OCCASION_TO_FORMALITY = {
    "casual": Formality.CASUAL,
    "smart casual": Formality.SMART_CASUAL,
    "smart_casual": Formality.SMART_CASUAL,
    "business": Formality.BUSINESS,
    "office": Formality.BUSINESS,
    "formal": Formality.FORMAL,
    "wedding": Formality.FORMAL,
    "athletic": Formality.ATHLETIC,
    "gym": Formality.ATHLETIC,
    "lounge": Formality.LOUNGE,
}


@dataclass
class CandidateOutfit:
    top: ClothingItem
    bottom: ClothingItem
    shoes: ClothingItem
    outerwear: ClothingItem | None = None

    def items_with_roles(self) -> list[tuple[OutfitItemRole, ClothingItem]]:
        items = [
            (OutfitItemRole.TOP, self.top),
            (OutfitItemRole.BOTTOM, self.bottom),
            (OutfitItemRole.SHOES, self.shoes),
        ]
        if self.outerwear is not None:
            items.append((OutfitItemRole.OUTERWEAR, self.outerwear))
        return items


class RuleBasedRecommendationEngine(RecommendationEngine):
    source = "rule_based"

    def __init__(self, clothing_item_repository: ClothingItemRepository) -> None:
        self.clothing_item_repository = clothing_item_repository

    def recommend_outfits(
        self,
        *,
        current_user: User,
        request: OutfitRecommendationRequest,
        weather: WeatherContext | None,
    ) -> OutfitRecommendationResponse:
        items = self.clothing_item_repository.list_available_items_for_user(user_id=current_user.id)
        context = self._build_context(request, weather)
        filtered_items = self._filter_items(items=items, context=context)
        recommendations = self._generate_recommendations(filtered_items, context, request.limit)
        return OutfitRecommendationResponse(recommendations=recommendations)

    def _build_context(
        self,
        request: OutfitRecommendationRequest,
        weather: WeatherContext | None,
    ) -> RecommendationContext:
        target_formality = None
        if request.occasion:
            target_formality = OCCASION_TO_FORMALITY.get(request.occasion.strip().lower())

        require_outerwear = False
        if weather is not None:
            temperature = weather.temperature_c
            if temperature is not None and temperature <= 12:
                require_outerwear = True
            if weather.precipitation:
                require_outerwear = True
            if weather.wind_level == WindLevel.WINDY:
                require_outerwear = True

        return RecommendationContext(
            target_season=request.season,
            target_formality=target_formality,
            weather=weather,
            require_outerwear=require_outerwear,
        )

    def _filter_items(
        self,
        *,
        items: list[ClothingItem],
        context: RecommendationContext,
    ) -> list[ClothingItem]:
        filtered = items

        if context.target_season is not None:
            filtered = [
                item
                for item in filtered
                if item.season in {None, Season.ALL_SEASON, context.target_season}
            ]

        if context.target_formality is not None:
            filtered = [
                item
                for item in filtered
                if item.formality in {None, context.target_formality}
            ]

        return filtered

    def _generate_recommendations(
        self,
        items: list[ClothingItem],
        context: RecommendationContext,
        limit: int,
    ) -> list[OutfitRecommendation]:
        tops = self._limit_pool(self._items_for_role(items, OutfitItemRole.TOP))
        bottoms = self._limit_pool(self._items_for_role(items, OutfitItemRole.BOTTOM))
        shoes = self._limit_pool(self._items_for_role(items, OutfitItemRole.SHOES))
        outerwear_options = self._limit_pool(self._items_for_role(items, OutfitItemRole.OUTERWEAR))

        if not tops or not bottoms or not shoes:
            return []

        candidates: list[tuple[float, OutfitRecommendation]] = []
        for top, bottom, shoe in product(tops, bottoms, shoes):
            if len({top.id, bottom.id, shoe.id}) < 3:
                continue

            candidate = CandidateOutfit(top=top, bottom=bottom, shoes=shoe)
            if context.require_outerwear:
                if not outerwear_options:
                    continue
                best_outerwear = max(
                    outerwear_options,
                    key=lambda item: self._score_candidate(
                        CandidateOutfit(top=top, bottom=bottom, shoes=shoe, outerwear=item),
                        context,
                    )[0],
                )
                candidate.outerwear = best_outerwear

            score, explanation = self._score_candidate(candidate, context)
            recommendation = OutfitRecommendation(
                source=ProvenanceSource.RULE_BASED,
                score=round(score, 3),
                explanation=explanation,
                selected_items=[
                    RecommendedOutfitItem(
                        role=role,
                        item=ClothingItemRead.model_validate(item),
                    )
                    for role, item in candidate.items_with_roles()
                ],
            )
            candidates.append((score, recommendation))

        candidates.sort(key=lambda pair: pair[0], reverse=True)
        return [recommendation for _, recommendation in candidates[:limit]]

    def _items_for_role(self, items: list[ClothingItem], role: OutfitItemRole) -> list[ClothingItem]:
        return [item for item in items if self._infer_role(item) == role]

    def _infer_role(self, item: ClothingItem) -> OutfitItemRole | None:
        normalized = {item.category.strip().lower()}
        if item.subcategory:
            normalized.add(item.subcategory.strip().lower())

        if normalized & TOP_CATEGORIES:
            return OutfitItemRole.TOP
        if normalized & BOTTOM_CATEGORIES:
            return OutfitItemRole.BOTTOM
        if normalized & SHOE_CATEGORIES:
            return OutfitItemRole.SHOES
        if normalized & OUTERWEAR_CATEGORIES:
            return OutfitItemRole.OUTERWEAR
        return None

    def _limit_pool(self, items: list[ClothingItem], size: int = 8) -> list[ClothingItem]:
        return sorted(items, key=self._freshness_rank, reverse=True)[:size]

    def _score_candidate(
        self,
        candidate: CandidateOutfit,
        context: RecommendationContext,
    ) -> tuple[float, list[str]]:
        items = [item for _, item in candidate.items_with_roles()]
        completeness = 1.0 if all([candidate.top, candidate.bottom, candidate.shoes]) else 0.0
        season_score = self._season_score(items, context)
        weather_score = self._weather_score(items, context)
        formality_score = self._formality_score(items, context)
        color_score = self._color_score(items)
        diversity_score = self._diversity_score(items)

        score = (
            completeness * 0.25
            + season_score * 0.15
            + weather_score * 0.15
            + formality_score * 0.15
            + color_score * 0.15
            + diversity_score * 0.15
        )

        explanation = [
            "Includes the essential top, bottom, and shoes combination.",
            self._season_explanation(season_score, context),
            self._weather_explanation(weather_score, context),
            self._formality_explanation(formality_score, context),
            self._color_explanation(color_score),
            self._diversity_explanation(diversity_score),
        ]
        if candidate.outerwear is not None:
            explanation.append("Added outerwear based on the supplied weather conditions.")

        return score, explanation

    def _season_score(self, items: list[ClothingItem], context: RecommendationContext) -> float:
        if context.target_season is None:
            return 0.8
        matches = 0
        for item in items:
            if item.season in {None, Season.ALL_SEASON, context.target_season}:
                matches += 1
        return matches / len(items)

    def _weather_score(self, items: list[ClothingItem], context: RecommendationContext) -> float:
        if context.weather is None or context.weather.temperature_c is None:
            return 0.8

        temperature = context.weather.temperature_c
        return sum(self._item_weather_score(item, temperature) for item in items) / len(items)

    def _item_weather_score(self, item: ClothingItem, temperature_c: float) -> float:
        category_name = item.category.strip().lower()
        if temperature_c <= 12:
            if item.season == Season.SUMMER:
                return 0.35
            if item.season in {Season.WINTER, Season.FALL}:
                return 0.95
            if category_name in OUTERWEAR_CATEGORIES:
                return 1.0
            return 0.75

        if temperature_c >= 24:
            if item.season == Season.WINTER:
                return 0.35
            if item.season == Season.SUMMER:
                return 0.95
            if category_name in OUTERWEAR_CATEGORIES:
                return 0.4
            return 0.8

        return 0.85 if item.season in {None, Season.ALL_SEASON, Season.SPRING, Season.FALL} else 0.75

    def _formality_score(self, items: list[ClothingItem], context: RecommendationContext) -> float:
        if context.target_formality is not None:
            matches = 0
            for item in items:
                if item.formality in {None, context.target_formality}:
                    matches += 1
            return matches / len(items)

        explicit = [item.formality for item in items if item.formality is not None]
        if not explicit:
            return 0.75
        most_common = max(set(explicit), key=explicit.count)
        return explicit.count(most_common) / len(explicit)

    def _color_score(self, items: list[ClothingItem]) -> float:
        colors = [self._primary_color_name(item) for item in items if self._primary_color_name(item)]
        if len(colors) <= 1:
            return 0.8

        pair_scores: list[float] = []
        for index, color in enumerate(colors):
            for other in colors[index + 1 :]:
                pair_scores.append(self._pair_color_score(color, other))

        return sum(pair_scores) / len(pair_scores) if pair_scores else 0.75

    def _pair_color_score(self, left: str, right: str) -> float:
        if left == right:
            return 0.9
        if left in NEUTRAL_COLORS or right in NEUTRAL_COLORS:
            return 0.85
        for family in COLOR_FAMILIES.values():
            if left in family and right in family:
                return 0.8
        return 0.55

    def _diversity_score(self, items: list[ClothingItem]) -> float:
        freshness = [self._freshness_rank(item) for item in items]
        if not freshness:
            return 0.0
        return min(sum(freshness) / len(freshness), 1.0)

    def _freshness_rank(self, item: ClothingItem) -> float:
        wear_penalty = min(item.wear_count / 20, 0.45)
        if item.last_worn_at is None:
            recency_bonus = 1.0
        else:
            delta_days = max(
                (datetime.now(timezone.utc) - item.last_worn_at.astimezone(timezone.utc)).days,
                0,
            )
            recency_bonus = min(delta_days / 30, 1.0)
        return max(recency_bonus - wear_penalty, 0.1)

    def _primary_color_name(self, item: ClothingItem) -> str | None:
        return item.primary_color.strip().lower() if item.primary_color else None

    def _season_explanation(self, score: float, context: RecommendationContext) -> str:
        if context.target_season is None:
            return "Used season-flexible pieces because no target season was provided."
        if score >= 0.99:
            return "Every selected piece aligns with the requested season."
        if score >= 0.7:
            return "Most pieces match the requested season or work year-round."
        return "Season alignment is partial, but the outfit still remains wearable."

    def _weather_explanation(self, score: float, context: RecommendationContext) -> str:
        if context.weather is None or context.weather.temperature_c is None:
            return "Weather was not provided, so the outfit stays weather-flexible."
        if score >= 0.85:
            return "The outfit is well aligned with the supplied temperature and conditions."
        if context.weather.temperature_c <= 12:
            return "Penalized warm-season pieces and favored colder-weather layers."
        if context.weather.temperature_c >= 24:
            return "Penalized heavy cold-weather pieces to keep the outfit lighter."
        return "Weather fit is reasonable, with a few flexible all-season pieces."

    def _formality_explanation(self, score: float, context: RecommendationContext) -> str:
        if context.target_formality is not None and score >= 0.99:
            return f"Formality matches the requested {context.target_formality.value} occasion."
        if context.target_formality is not None:
            return "Formality mostly aligns with the requested occasion."
        if score >= 0.8:
            return "The selected pieces keep a consistent dress level."
        return "The outfit mixes dress levels slightly to preserve flexibility."

    def _color_explanation(self, score: float) -> str:
        if score >= 0.85:
            return "Colors are coordinated through neutrals or closely related tones."
        if score >= 0.7:
            return "Colors are reasonably compatible and balanced."
        return "Colors provide a more contrast-forward combination."

    def _diversity_explanation(self, score: float) -> str:
        if score >= 0.85:
            return "Prioritized pieces that have not been worn recently."
        if score >= 0.65:
            return "Balances familiar staples with some wear diversity."
        return "Uses more frequently worn staples because the pool is limited."
