import type { ClothingItem, OutfitItemRole } from "@/lib/types";

const roleMatchers: Record<OutfitItemRole, string[]> = {
  top: ["tops", "top", "shirt", "sweater", "hoodie", "blouse"],
  bottom: ["bottoms", "bottom", "pants", "trousers", "jeans", "skirt", "shorts"],
  shoes: ["shoes", "shoe", "sneakers", "boots", "loafers", "heels", "sandals"],
  outerwear: ["outerwear", "jacket", "coat", "blazer", "cardigan"],
  accessory: ["accessories", "accessory", "bag", "belt", "hat", "scarf"],
  one_piece: ["dress", "jumpsuit", "one_piece"],
};

export function getItemsForRole(
  items: ClothingItem[],
  role: OutfitItemRole,
): ClothingItem[] {
  const matchers = roleMatchers[role];

  return items.filter((item) => {
    const normalized = [item.category, item.subcategory]
      .filter(Boolean)
      .map((value) => value!.toLowerCase());

    return normalized.some((value) => matchers.includes(value));
  });
}

export function formatSeasonLabel(value: string | null | undefined): string {
  if (!value) {
    return "Seasonless";
  }

  return value
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export function formatCategoryLabel(value: string): string {
  return value
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}
