import type {
  ClothingItemCreatePayload,
  FieldErrors,
  LoginPayload,
  OutfitCreatePayload,
  RegisterPayload,
} from "@/lib/types";

export function validateAuthPayload(
  payload: RegisterPayload | LoginPayload,
  mode: "login" | "register",
): FieldErrors<"email" | "password" | "display_name"> {
  const errors: FieldErrors<"email" | "password" | "display_name"> = {};

  if (!payload.email.trim()) {
    errors.email = "Email is required.";
  }

  if (!payload.password.trim()) {
    errors.password = "Password is required.";
  } else if (payload.password.length < 8) {
    errors.password = "Password must be at least 8 characters.";
  }

  if (mode === "register" && "display_name" in payload) {
    if (!payload.display_name?.trim()) {
      errors.display_name = "Display name is required for demo-friendly accounts.";
    }
  }

  return errors;
}

export function validateClothingItemPayload(
  payload: ClothingItemCreatePayload,
): FieldErrors<"name" | "category" | "primary_color"> {
  const errors: FieldErrors<"name" | "category" | "primary_color"> = {};

  if (!payload.name.trim()) {
    errors.name = "Item name is required.";
  }

  if (!payload.category.trim()) {
    errors.category = "Category is required.";
  }

  if (payload.primary_color && payload.primary_color.trim().length > 100) {
    errors.primary_color = "Color should stay under 100 characters.";
  }

  return errors;
}

export function validateOutfitPayload(
  payload: OutfitCreatePayload,
): FieldErrors<"name" | "items"> {
  const errors: FieldErrors<"name" | "items"> = {};

  if (!payload.name.trim()) {
    errors.name = "Outfit name is required.";
  }

  if (!payload.items || payload.items.length < 3) {
    errors.items = "Pick at least a top, bottom, and shoes.";
  } else {
    const itemIds = payload.items.map((item) => item.clothing_item_id);
    const roles = new Set(payload.items.map((item) => item.role));

    if (!roles.has("top") || !roles.has("bottom") || !roles.has("shoes")) {
      errors.items = "Include at least one top, one bottom, and one pair of shoes.";
      return errors;
    }

    if (new Set(itemIds).size !== itemIds.length) {
      errors.items = "Choose different clothing items for each outfit role.";
    }
  }

  return errors;
}
