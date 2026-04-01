import { apiRequest } from "@/lib/api/client";
import type {
  RecommendationRequest,
  RecommendationResponse,
} from "@/lib/types";

export function fetchOutfitRecommendations(
  payload: RecommendationRequest,
): Promise<RecommendationResponse> {
  return apiRequest<RecommendationResponse>("/recommendations/outfits", {
    method: "POST",
    body: payload,
  });
}

