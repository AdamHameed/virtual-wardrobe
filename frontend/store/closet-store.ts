"use client";

import { create } from "zustand";
import { createClothingItem, fetchClothingItems } from "@/lib/api";
import { ClothingItem, CreateClothingItemPayload } from "@/lib/types";

type ClosetStore = {
  items: ClothingItem[];
  isLoading: boolean;
  error: string | null;
  loadItems: () => Promise<void>;
  addItem: (payload: CreateClothingItemPayload) => Promise<void>;
};

export const useClosetStore = create<ClosetStore>((set) => ({
  items: [],
  isLoading: false,
  error: null,
  loadItems: async () => {
    set({ isLoading: true, error: null });

    try {
      const items = await fetchClothingItems();
      set({ items, isLoading: false });
    } catch (error) {
      set({
        error:
          error instanceof Error ? error.message : "Unable to load wardrobe.",
        isLoading: false,
      });
    }
  },
  addItem: async (payload) => {
    set({ isLoading: true, error: null });

    try {
      const item = await createClothingItem(payload);
      set((state) => ({
        items: [item, ...state.items],
        isLoading: false,
      }));
    } catch (error) {
      set({
        error:
          error instanceof Error ? error.message : "Unable to save clothing item.",
        isLoading: false,
      });
    }
  },
}));

