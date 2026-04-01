"use client";

import { useMemo, useState } from "react";
import { resolveMediaUrl } from "@/lib/api";
import { formatCategoryLabel, formatSeasonLabel } from "@/lib/wardrobe";
import type { ClothingItem, Season } from "@/lib/types";

const DEFAULT_VISIBLE_ITEMS = 6;

type WardrobeListProps = {
  items: ClothingItem[];
  isLoading: boolean;
  isDeletingItem: boolean;
  error: string | null;
  searchQuery: string;
  seasonFilter: Season | "all";
  onSearchQueryChange: (value: string) => void;
  onSeasonFilterChange: (value: Season | "all") => void;
  onViewItem: (item: ClothingItem) => void;
  onEditItem: (item: ClothingItem) => void;
  onDeleteItem: (item: ClothingItem) => Promise<void>;
};

export function WardrobeList({
  items,
  isLoading,
  isDeletingItem,
  error,
  searchQuery,
  seasonFilter,
  onSearchQueryChange,
  onSeasonFilterChange,
  onViewItem,
  onEditItem,
  onDeleteItem,
}: WardrobeListProps) {
  const [showAll, setShowAll] = useState(false);

  const visibleItems = useMemo(
    () => (showAll ? items : items.slice(0, DEFAULT_VISIBLE_ITEMS)),
    [items, showAll],
  );

  const hasOverflow = items.length > DEFAULT_VISIBLE_ITEMS;

  return (
    <section className="space-y-5">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h2 className="text-2xl font-semibold">Closet Inventory</h2>
          <p className="text-sm text-slate-600">
            Search across item names, categories, brands, colors, and notes.
          </p>
        </div>
        <div className="grid w-full max-w-xl gap-4 sm:grid-cols-2">
          <label className="grid gap-2">
            <span className="text-sm font-medium">Search wardrobe</span>
            <input
              className="rounded-2xl border border-slate-200 bg-white px-4 py-3"
              placeholder="Search items..."
              value={searchQuery}
              onChange={(event) => {
                setShowAll(false);
                onSearchQueryChange(event.target.value);
              }}
            />
          </label>
          <label className="grid gap-2">
            <span className="text-sm font-medium">Season</span>
            <select
              className="rounded-2xl border border-slate-200 bg-white px-4 py-3"
              value={seasonFilter}
              onChange={(event) => {
                setShowAll(false);
                onSeasonFilterChange(event.target.value as Season | "all");
              }}
            >
              <option value="all">All seasons</option>
              <option value="spring">Spring</option>
              <option value="summer">Summer</option>
              <option value="fall">Fall</option>
              <option value="winter">Winter</option>
              <option value="all_season">All season</option>
            </select>
          </label>
        </div>
      </div>

      {isLoading ? (
        <div className="rounded-[1.75rem] border border-dashed border-slate-300 bg-white/60 p-8 text-sm text-slate-500">
          Loading your wardrobe...
        </div>
      ) : null}

      {!isLoading && error ? (
        <div className="rounded-[1.75rem] border border-red-200 bg-red-50 p-8 text-sm text-red-700">
          {error}
        </div>
      ) : null}

      {!isLoading && !error ? (
        <>
          <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
            {visibleItems.map((item) => (
              <article
                key={item.id}
                className="overflow-hidden rounded-[1.75rem] border border-white/70 bg-white/90 shadow-panel"
              >
                <button
                  className="block aspect-[4/3] w-full bg-slate-100 text-left transition hover:opacity-90"
                  onClick={() => onViewItem(item)}
                  type="button"
                >
                  {item.image_url ? (
                    <img
                      alt={item.name}
                      className="h-full w-full object-cover"
                      src={resolveMediaUrl(item.image_url) ?? ""}
                    />
                  ) : (
                    <div className="flex h-full items-center justify-center text-sm uppercase tracking-[0.25em] text-slate-400">
                      No Image
                    </div>
                  )}
                </button>

                <div className="space-y-3 p-5">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <h3 className="text-lg font-semibold">{item.name}</h3>
                      <p className="text-sm text-slate-500">
                        {formatCategoryLabel(item.category)}
                      </p>
                    </div>
                    <span className="rounded-full bg-moss/10 px-3 py-1 text-xs font-medium text-moss">
                      {formatSeasonLabel(item.season)}
                    </span>
                  </div>

                  <div className="flex flex-wrap gap-2 text-xs text-slate-600">
                    {item.primary_color ? (
                      <span className="rounded-full bg-slate-100 px-3 py-1">
                        {item.primary_color}
                      </span>
                    ) : null}
                    {item.brand ? (
                      <span className="rounded-full bg-slate-100 px-3 py-1">
                        {item.brand}
                      </span>
                    ) : null}
                  </div>

                  {item.notes ? (
                    <p className="text-sm leading-6 text-slate-600">{item.notes}</p>
                  ) : null}

                  <div className="flex flex-wrap gap-3">
                    <button
                      className="rounded-full bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-200"
                      onClick={() => onViewItem(item)}
                      type="button"
                    >
                      View
                    </button>
                    <button
                      className="rounded-full bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-200"
                      onClick={() => onEditItem(item)}
                      type="button"
                    >
                      Edit
                    </button>
                    <button
                      className="rounded-full bg-red-50 px-4 py-2 text-sm font-medium text-red-700 transition hover:bg-red-100 disabled:cursor-not-allowed disabled:opacity-60"
                      disabled={isDeletingItem}
                      onClick={() => void onDeleteItem(item)}
                      type="button"
                    >
                      {isDeletingItem ? "Deleting..." : "Delete"}
                    </button>
                  </div>
                </div>
              </article>
            ))}

            {items.length === 0 ? (
              <div className="rounded-[1.75rem] border border-dashed border-slate-300 bg-white/60 p-8 text-sm text-slate-500">
                No items match this search yet.
              </div>
            ) : null}
          </div>

          {hasOverflow ? (
            <div className="flex justify-center">
              <button
                className="rounded-full border border-slate-300 bg-white px-5 py-3 text-sm font-medium text-slate-700 transition hover:bg-slate-100"
                onClick={() => setShowAll((current) => !current)}
                type="button"
              >
                {showAll
                  ? "Show fewer items"
                  : `Show all ${items.length} items`}
              </button>
            </div>
          ) : null}
        </>
      ) : null}
    </section>
  );
}
