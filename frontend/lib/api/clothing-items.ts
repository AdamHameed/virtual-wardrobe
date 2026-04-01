import { apiRequest } from "@/lib/api/client";
import type {
  ClothingItem,
  ClothingItemCreatePayload,
  ClothingItemFilters,
  ClothingItemUpdatePayload,
  PaginatedResponse,
  PaginationParams,
} from "@/lib/types";

function buildQuery(
  pagination?: PaginationParams,
  filters?: ClothingItemFilters,
): string {
  const params = new URLSearchParams();

  if (pagination?.limit !== undefined) {
    params.set("limit", String(pagination.limit));
  }
  if (pagination?.offset !== undefined) {
    params.set("offset", String(pagination.offset));
  }

  if (filters?.query) {
    params.set("q", filters.query);
  }
  if (filters?.category) {
    params.set("category", filters.category);
  }
  if (filters?.color) {
    params.set("color", filters.color);
  }
  if (filters?.season) {
    params.set("season", filters.season);
  }
  if (filters?.formality) {
    params.set("formality", filters.formality);
  }
  if (filters?.status) {
    params.set("status", filters.status);
  }

  const query = params.toString();
  return query ? `?${query}` : "";
}

function buildClothingItemFormData(
  payload: ClothingItemCreatePayload | ClothingItemUpdatePayload,
): FormData {
  const formData = new FormData();

  Object.entries(payload).forEach(([key, value]) => {
    if (value === undefined || value === null) {
      return;
    }

    if (key === "image" && value instanceof File) {
      formData.append("image", value);
      return;
    }

    formData.append(key, String(value));
  });

  return formData;
}

export function listClothingItems(
  pagination?: PaginationParams,
  filters?: ClothingItemFilters,
): Promise<PaginatedResponse<ClothingItem>> {
  return apiRequest<PaginatedResponse<ClothingItem>>(
    `/clothing-items${buildQuery(pagination, filters)}`,
  );
}

export function getClothingItem(itemId: number): Promise<ClothingItem> {
  return apiRequest<ClothingItem>(`/clothing-items/${itemId}`);
}

export function createClothingItem(
  payload: ClothingItemCreatePayload,
): Promise<ClothingItem> {
  return apiRequest<ClothingItem>("/clothing-items", {
    method: "POST",
    body: buildClothingItemFormData(payload),
  });
}

export function updateClothingItem(
  itemId: number,
  payload: ClothingItemUpdatePayload,
): Promise<ClothingItem> {
  return apiRequest<ClothingItem>(`/clothing-items/${itemId}`, {
    method: "PATCH",
    body: buildClothingItemFormData(payload),
  });
}

export function deleteClothingItem(itemId: number): Promise<void> {
  return apiRequest<void>(`/clothing-items/${itemId}`, {
    method: "DELETE",
  });
}
