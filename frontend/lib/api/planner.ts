import { apiRequest } from "@/lib/api/client";
import type {
  OutfitPlan,
  OutfitPlanCreatePayload,
  OutfitPlanUpdatePayload,
  PaginatedResponse,
  PaginationParams,
} from "@/lib/types";

function buildPaginationQuery(pagination?: PaginationParams): string {
  const params = new URLSearchParams();

  if (pagination?.limit) {
    params.set("limit", String(pagination.limit));
  }
  if (pagination?.offset) {
    params.set("offset", String(pagination.offset));
  }

  const query = params.toString();
  return query ? `?${query}` : "";
}

export function listPlannerEntries(
  pagination?: PaginationParams,
): Promise<PaginatedResponse<OutfitPlan>> {
  return apiRequest<PaginatedResponse<OutfitPlan>>(
    `/outfit-plans${buildPaginationQuery(pagination)}`,
  );
}

export function getPlannerEntry(planId: number): Promise<OutfitPlan> {
  return apiRequest<OutfitPlan>(`/outfit-plans/${planId}`);
}

export function createPlannerEntry(
  payload: OutfitPlanCreatePayload,
): Promise<OutfitPlan> {
  return apiRequest<OutfitPlan>("/outfit-plans", {
    method: "POST",
    body: payload,
  });
}

export function updatePlannerEntry(
  planId: number,
  payload: OutfitPlanUpdatePayload,
): Promise<OutfitPlan> {
  return apiRequest<OutfitPlan>(`/outfit-plans/${planId}`, {
    method: "PATCH",
    body: payload,
  });
}

export function deletePlannerEntry(planId: number): Promise<void> {
  return apiRequest<void>(`/outfit-plans/${planId}`, {
    method: "DELETE",
  });
}

