from abc import ABC, abstractmethod

from app.models.user import User
from app.schemas.ai import AutoTagSuggestionGenerateRequest, AutoTagSuggestionResult


class AutoTaggingEngine(ABC):
    @abstractmethod
    def suggest_tags(
        self,
        *,
        current_user: User,
        request: AutoTagSuggestionGenerateRequest,
    ) -> list[AutoTagSuggestionResult]:
        raise NotImplementedError


class NoOpAutoTaggingEngine(AutoTaggingEngine):
    def suggest_tags(
        self,
        *,
        current_user: User,
        request: AutoTagSuggestionGenerateRequest,
    ) -> list[AutoTagSuggestionResult]:
        return []
