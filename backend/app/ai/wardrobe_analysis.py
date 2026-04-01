from abc import ABC, abstractmethod

from app.models.user import User
from app.schemas.ai import WardrobeAnalysisRequest, WardrobeAnalysisResult


class WardrobeAnalysisEngine(ABC):
    @abstractmethod
    def analyze(
        self,
        *,
        current_user: User,
        request: WardrobeAnalysisRequest,
    ) -> WardrobeAnalysisResult:
        raise NotImplementedError


class NoOpWardrobeAnalysisEngine(WardrobeAnalysisEngine):
    def analyze(
        self,
        *,
        current_user: User,
        request: WardrobeAnalysisRequest,
    ) -> WardrobeAnalysisResult:
        return WardrobeAnalysisResult(
            source="manual",
            summary="Wardrobe analysis engine is not configured yet.",
            insights=[],
        )
