export type ProvenanceSource = "manual" | "rule_based" | "ai_generated";

export type ClothingStatus = "clean" | "dirty" | "unavailable";
export type Season = "spring" | "summer" | "fall" | "winter" | "all_season";
export type Formality =
  | "casual"
  | "smart_casual"
  | "business"
  | "formal"
  | "athletic"
  | "lounge";
export type OutfitItemRole =
  | "top"
  | "bottom"
  | "shoes"
  | "outerwear"
  | "accessory"
  | "one_piece";
export type WindLevel = "calm" | "breezy" | "windy";

export type PaginationParams = {
  limit?: number;
  offset?: number;
};

export type PaginatedResponse<T> = {
  items: T[];
  total: number;
  limit: number;
  offset: number;
};

export type User = {
  id: number;
  email: string;
  display_name: string | null;
  is_active: boolean;
  extra_data: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
};

export type RegisterPayload = {
  email: string;
  password: string;
  display_name?: string | null;
  extra_data?: Record<string, unknown> | null;
};

export type LoginPayload = {
  email: string;
  password: string;
};

export type AuthResponse = {
  access_token: string;
  token_type: "bearer";
  user: User;
};

export type CurrentUserResponse = {
  user: User;
};

export type ClothingItem = {
  id: number;
  user_id: number;
  name: string;
  category: string;
  subcategory: string | null;
  primary_color: string | null;
  secondary_color: string | null;
  season: Season | null;
  formality: Formality | null;
  material: string | null;
  brand: string | null;
  notes: string | null;
  status: ClothingStatus;
  wear_count: number;
  last_worn_at: string | null;
  extra_data: Record<string, unknown> | null;
  image_path: string | null;
  image_url: string | null;
  created_at: string;
  updated_at: string;
};

export type ClothingItemFilters = {
  query?: string;
  category?: string;
  color?: string;
  season?: Season;
  formality?: Formality;
  status?: ClothingStatus;
};

export type ClothingItemCreatePayload = {
  name: string;
  category: string;
  subcategory?: string;
  primary_color?: string;
  secondary_color?: string;
  season?: Season;
  formality?: Formality;
  material?: string;
  brand?: string;
  notes?: string;
  status?: ClothingStatus;
  image?: File | null;
};

export type ClothingItemUpdatePayload = Partial<ClothingItemCreatePayload>;

export type OutfitItem = {
  id: number;
  outfit_id: number;
  clothing_item_id: number;
  role: OutfitItemRole;
  position: number;
  extra_data: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
};

export type OutfitItemCreatePayload = {
  clothing_item_id: number;
  role: OutfitItemRole;
  position?: number;
  extra_data?: Record<string, unknown> | null;
};

export type Outfit = {
  id: number;
  user_id: number;
  name: string;
  notes: string | null;
  extra_data: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
  items: OutfitItem[];
};

export type OutfitCreatePayload = {
  name: string;
  notes?: string | null;
  extra_data?: Record<string, unknown> | null;
  items?: OutfitItemCreatePayload[];
};

export type OutfitUpdatePayload = Partial<OutfitCreatePayload>;

export type OutfitPlan = {
  id: number;
  user_id: number;
  outfit_id: number;
  planned_for: string;
  notes: string | null;
  extra_data: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
};

export type OutfitPlanCreatePayload = {
  outfit_id: number;
  planned_for: string;
  notes?: string | null;
  extra_data?: Record<string, unknown> | null;
};

export type OutfitPlanUpdatePayload = Partial<OutfitPlanCreatePayload>;

export type WeatherInput = {
  temperature_c?: number | null;
  condition?: string | null;
  precipitation?: boolean;
  wind_level?: WindLevel | null;
};

export type RecommendationRequest = {
  weather?: WeatherInput | null;
  season?: Season | null;
  occasion?: string | null;
  limit?: number;
};

export type RecommendationItem = {
  role: OutfitItemRole;
  item: ClothingItem;
};

export type Recommendation = {
  source: ProvenanceSource;
  score: number;
  explanation: string[];
  selected_items: RecommendationItem[];
};

export type RecommendationResponse = {
  recommendations: Recommendation[];
};

export type FieldErrors<T extends string = string> = Partial<Record<T, string>>;
