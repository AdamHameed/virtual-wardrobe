import { apiRequest } from "@/lib/api/client";
import type {
  Outfit,
  OutfitCreatePayload,
  OutfitUpdatePayload,
  PaginatedResponse,
  PaginationParams,
} from "@/lib/types";

function buildPaginationQuery(pagination?: PaginationParams): string {
  const params = new URLSearchParams();

  if (pagination?.limit !== undefined) {
    params.set("limit", String(pagination.limit));
  }
  if (pagination?.offset !== undefined) {
    params.set("offset", String(pagination.offset));
  }

  const query = params.toString();
  return query ? `?${query}` : "";
}

export function listOutfits(
  pagination?: PaginationParams,
): Promise<PaginatedResponse<Outfit>> {
  return apiRequest<PaginatedResponse<Outfit>>(
    `/outfits${buildPaginationQuery(pagination)}`,
  );
}

export function getOutfit(outfitId: number): Promise<Outfit> {
  return apiRequest<Outfit>(`/outfits/${outfitId}`);
}

export function createOutfit(payload: OutfitCreatePayload): Promise<Outfit> {
  return apiRequest<Outfit>("/outfits", {
    method: "POST",
    body: payload,
  });
}

export function updateOutfit(
  outfitId: number,
  payload: OutfitUpdatePayload,
): Promise<Outfit> {
  return apiRequest<Outfit>(`/outfits/${outfitId}`, {
    method: "PATCH",
    body: payload,
  });
}

export function deleteOutfit(outfitId: number): Promise<void> {
  return apiRequest<void>(`/outfits/${outfitId}`, {
    method: "DELETE",
  });
}
