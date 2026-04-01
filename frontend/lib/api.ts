import { ClothingItem, CreateClothingItemPayload } from "@/lib/types";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export function resolveMediaUrl(path: string | null | undefined): string | null {
  if (!path) {
    return null;
  }

  if (path.startsWith("http://") || path.startsWith("https://")) {
    return path;
  }

  const backendOrigin = API_URL.replace(/\/api\/v1\/?$/, "");
  return `${backendOrigin}${path}`;
}

async function parseResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Request failed");
  }

  return response.json() as Promise<T>;
}

export async function fetchClothingItems(): Promise<ClothingItem[]> {
  const response = await fetch(`${API_URL}/clothing-items`, {
    cache: "no-store",
  });

  return parseResponse<ClothingItem[]>(response);
}

export async function createClothingItem(
  payload: CreateClothingItemPayload,
): Promise<ClothingItem> {
  const formData = new FormData();
  formData.append("name", payload.name);
  formData.append("category", payload.category);

  if (payload.color) {
    formData.append("color", payload.color);
  }

  if (payload.season) {
    formData.append("season", payload.season);
  }

  if (payload.notes) {
    formData.append("notes", payload.notes);
  }

  if (payload.image) {
    formData.append("image", payload.image);
  }

  const response = await fetch(`${API_URL}/clothing-items`, {
    method: "POST",
    body: formData,
  });

  return parseResponse<ClothingItem>(response);
}
