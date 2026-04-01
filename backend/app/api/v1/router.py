from fastapi import APIRouter

from app.api.v1.endpoints import auth, clothing_items, health, outfit_plans, outfits, recommendations, tags, wear_logs

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(clothing_items.router, prefix="/clothing-items", tags=["clothing-items"])
api_router.include_router(tags.router, prefix="/tags", tags=["tags"])
api_router.include_router(outfits.router, prefix="/outfits", tags=["outfits"])
api_router.include_router(outfit_plans.router, prefix="/outfit-plans", tags=["outfit-plans"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(wear_logs.router, prefix="/wear-logs", tags=["wear-logs"])
