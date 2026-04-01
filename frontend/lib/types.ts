export type ClothingItem = {
  id: number;
  name: string;
  category: string;
  color?: string | null;
  season?: string | null;
  notes?: string | null;
  image_url?: string | null;
  created_at: string;
  updated_at: string;
};

export type CreateClothingItemPayload = {
  name: string;
  category: string;
  color?: string;
  season?: string;
  notes?: string;
  image?: File | null;
};

