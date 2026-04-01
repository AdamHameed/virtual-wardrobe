# AI-Ready Extension Points

The backend is prepared for future AI components without requiring frontend API rewrites.

## Current interfaces

- `app/recommendations/engine.py`
  Recommendation contract used by the existing recommendation endpoint.
- `app/ai/auto_tagging.py`
  `AutoTaggingEngine` interface plus a no-op default implementation.
- `app/ai/wardrobe_analysis.py`
  `WardrobeAnalysisEngine` interface plus a no-op default implementation.
- `app/weather/service.py`
  Weather abstraction already used by recommendations and ready for a real provider.

## Current implementations

- `app/recommendations/rule_based.py`
  Active recommendation engine used in production today.
- `app/ai/auto_tagging.py`
  `NoOpAutoTaggingEngine` placeholder.
- `app/ai/wardrobe_analysis.py`
  `NoOpWardrobeAnalysisEngine` placeholder.

## Where future AI code plugs in

1. Recommendation generation
   Replace `RuleBasedRecommendationEngine` with a new class implementing `RecommendationEngine`.
   `RecommendationService` can accept that engine without changing `/api/v1/recommendations/outfits`.

2. Auto-tagging
   Implement `AutoTaggingEngine` in a new module such as `app/ai/auto_tagging_openai.py`.
   Persist suggestions into `auto_tag_suggestions` using the placeholder model.

3. Wardrobe analysis
   Implement `WardrobeAnalysisEngine` in a new module such as `app/ai/wardrobe_analysis_openai.py`.
   Reuse `clothing_embeddings` and `ai_recommendation_logs` if analysis results need traceability.

4. Embeddings
   `clothing_embeddings` is reserved for vector-like features without forcing a provider or extension today.

## Provenance conventions

Use `ProvenanceSource` values consistently:

- `manual`
- `rule_based`
- `ai_generated`

These values are already safe for API responses because they serialize as stable strings.
