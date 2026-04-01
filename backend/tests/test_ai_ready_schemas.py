from app.core.enums import ProvenanceSource, SuggestionStatus
from app.schemas.ai import (
    AIRecommendationLogCreate,
    AutoTagSuggestionCreate,
    ClothingEmbeddingCreate,
    WardrobeAnalysisResult,
)


def test_ai_placeholder_schemas_preserve_provenance_fields() -> None:
    suggestion = AutoTagSuggestionCreate(
        clothing_item_id=1,
        suggested_tag="minimalist",
        source=ProvenanceSource.AI_GENERATED,
        status=SuggestionStatus.PENDING,
    )
    log = AIRecommendationLogCreate(
        request_type="outfit_recommendation",
        source=ProvenanceSource.RULE_BASED,
    )
    embedding = ClothingEmbeddingCreate(
        clothing_item_id=1,
        model_key="placeholder-embedding-model",
        dimensions=3,
        vector=[0.1, 0.2, 0.3],
    )
    analysis = WardrobeAnalysisResult(
        source=ProvenanceSource.MANUAL,
        summary="No analysis configured.",
    )

    assert suggestion.source == ProvenanceSource.AI_GENERATED
    assert suggestion.status == SuggestionStatus.PENDING
    assert log.source == ProvenanceSource.RULE_BASED
    assert embedding.dimensions == 3
    assert analysis.source == ProvenanceSource.MANUAL
