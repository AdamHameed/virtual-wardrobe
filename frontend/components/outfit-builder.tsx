"use client";

import { FormEvent, useDeferredValue, useMemo, useState } from "react";
import { resolveMediaUrl } from "@/lib/api";
import { formatCategoryLabel } from "@/lib/wardrobe";
import type { ClothingItem, FieldErrors, Outfit, OutfitItemRole } from "@/lib/types";

const DEFAULT_VISIBLE_ROLE_ITEMS = 4;

type OutfitBuilderProps = {
  outfits: Outfit[];
  isLoading: boolean;
  isSaving: boolean;
  isDeleting: boolean;
  disabled: boolean;
  error: string | null;
  formErrors: FieldErrors<"name" | "items">;
  outfitName: string;
  outfitNotes: string;
  editingOutfitName: string | null;
  selectedTopIds: number[];
  selectedBottomIds: number[];
  selectedShoesIds: number[];
  selectedOuterwearIds: number[];
  topOptions: ClothingItem[];
  bottomOptions: ClothingItem[];
  shoeOptions: ClothingItem[];
  outerwearOptions: ClothingItem[];
  resolveItem: (clothingItemId: number) => ClothingItem | undefined;
  onOutfitNameChange: (value: string) => void;
  onOutfitNotesChange: (value: string) => void;
  onToggleItem: (role: OutfitItemRole, clothingItemId: number) => void;
  onEditOutfit: (outfit: Outfit) => void;
  onDeleteOutfit: (outfit: Outfit) => Promise<void>;
  onCancelEdit: () => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => Promise<void>;
};

function RolePicker({
  label,
  options,
  selectedIds,
  disabled,
  onToggle,
}: {
  label: string;
  options: ClothingItem[];
  selectedIds: number[];
  disabled: boolean;
  onToggle: (itemId: number) => void;
}) {
  const [query, setQuery] = useState("");
  const [expanded, setExpanded] = useState(false);
  const deferredQuery = useDeferredValue(query);
  const normalizedQuery = deferredQuery.trim().toLowerCase();

  const filteredOptions = useMemo(() => {
    const searched = normalizedQuery
      ? options.filter((item) => {
          const haystack = [item.name, item.category, item.primary_color, item.brand]
            .filter(Boolean)
            .join(" ")
            .toLowerCase();

          return haystack.includes(normalizedQuery);
        })
      : options;

    if (expanded || normalizedQuery) {
      return searched;
    }

    return searched.slice(0, DEFAULT_VISIBLE_ROLE_ITEMS);
  }, [expanded, normalizedQuery, options]);

  const hiddenCount = !expanded && !normalizedQuery
    ? Math.max(0, options.length - DEFAULT_VISIBLE_ROLE_ITEMS)
    : 0;

  return (
    <div className="grid gap-2">
      <div className="flex items-center justify-between gap-3">
        <span className="text-sm font-medium">{label}</span>
        <span className="text-xs text-slate-500">
          {selectedIds.length} selected
        </span>
      </div>
      <input
        className="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm"
        disabled={disabled}
        onChange={(event) => setQuery(event.target.value)}
        placeholder={`Search ${label.toLowerCase()}...`}
        value={query}
      />
      {filteredOptions.length === 0 ? (
        <div className="rounded-2xl border border-dashed border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-500">
          {options.length === 0 ? "No matching items yet." : "No items match this search."}
        </div>
      ) : (
        <div className="grid gap-2">
          {filteredOptions.map((item) => {
            const selected = selectedIds.includes(item.id);

            return (
              <label
                key={item.id}
                className={`flex items-center gap-3 rounded-2xl border px-4 py-3 text-sm transition ${
                  selected
                    ? "border-moss bg-moss/10 text-moss"
                    : "border-slate-200 bg-white text-slate-700"
                }`}
              >
                <input
                  checked={selected}
                  disabled={disabled}
                  onChange={() => onToggle(item.id)}
                  type="checkbox"
                />
                <span className="min-w-0 flex-1 font-medium">{item.name}</span>
                <span className="text-xs text-slate-500">
                  {formatCategoryLabel(item.category)}
                </span>
              </label>
            );
          })}
          {hiddenCount > 0 ? (
            <button
              className="rounded-full border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-100"
              disabled={disabled}
              onClick={() => setExpanded(true)}
              type="button"
            >
              Show {hiddenCount} more
            </button>
          ) : null}
          {expanded && !normalizedQuery && options.length > DEFAULT_VISIBLE_ROLE_ITEMS ? (
            <button
              className="rounded-full border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-100"
              disabled={disabled}
              onClick={() => setExpanded(false)}
              type="button"
            >
              Show fewer
            </button>
          ) : null}
        </div>
      )}
    </div>
  );
}

export function OutfitBuilder({
  outfits,
  isLoading,
  isSaving,
  isDeleting,
  disabled,
  error,
  formErrors,
  outfitName,
  outfitNotes,
  editingOutfitName,
  selectedTopIds,
  selectedBottomIds,
  selectedShoesIds,
  selectedOuterwearIds,
  topOptions,
  bottomOptions,
  shoeOptions,
  outerwearOptions,
  resolveItem,
  onOutfitNameChange,
  onOutfitNotesChange,
  onToggleItem,
  onEditOutfit,
  onDeleteOutfit,
  onCancelEdit,
  onSubmit,
}: OutfitBuilderProps) {
  return (
    <section className="grid items-start gap-8 lg:grid-cols-[0.95fr_1.05fr]">
      <form
        className="rounded-[2rem] border border-white/70 bg-white/90 p-6 shadow-panel lg:sticky lg:top-6"
        onSubmit={onSubmit}
      >
        <div className="space-y-4">
          <div>
            <p className="text-sm uppercase tracking-[0.25em] text-clay">
              Outfit Studio
            </p>
            <h2 className="mt-2 text-2xl font-semibold">
              {editingOutfitName ? "Edit outfit" : "Create an outfit"}
            </h2>
            <p className="mt-1 text-sm text-slate-600">
              Build looks without flooding the screen with every possible item at once.
            </p>
          </div>

          <label className="grid gap-2">
            <span className="text-sm font-medium">Outfit name</span>
            <input
              className="rounded-2xl border border-slate-200 bg-white px-4 py-3"
              disabled={disabled}
              value={outfitName}
              onChange={(event) => onOutfitNameChange(event.target.value)}
              placeholder="Weekend Coffee Run"
            />
            {formErrors.name ? (
              <span className="text-sm text-red-600">{formErrors.name}</span>
            ) : null}
          </label>

          <label className="grid gap-2">
            <span className="text-sm font-medium">Notes</span>
            <textarea
              className="min-h-24 rounded-2xl border border-slate-200 bg-white px-4 py-3"
              disabled={disabled}
              value={outfitNotes}
              onChange={(event) => onOutfitNotesChange(event.target.value)}
              placeholder="Easy transitional outfit for cool mornings."
            />
          </label>

          <div className="grid gap-4 lg:grid-cols-2">
            <RolePicker
              label="Tops"
              options={topOptions}
              selectedIds={selectedTopIds}
              disabled={disabled}
              onToggle={(itemId) => onToggleItem("top", itemId)}
            />
            <RolePicker
              label="Bottoms"
              options={bottomOptions}
              selectedIds={selectedBottomIds}
              disabled={disabled}
              onToggle={(itemId) => onToggleItem("bottom", itemId)}
            />
            <RolePicker
              label="Shoes"
              options={shoeOptions}
              selectedIds={selectedShoesIds}
              disabled={disabled}
              onToggle={(itemId) => onToggleItem("shoes", itemId)}
            />
            <RolePicker
              label="Outerwear"
              options={outerwearOptions}
              selectedIds={selectedOuterwearIds}
              disabled={disabled}
              onToggle={(itemId) => onToggleItem("outerwear", itemId)}
            />
          </div>

          {formErrors.items ? (
            <p className="text-sm text-red-600">{formErrors.items}</p>
          ) : null}

          <div className="flex flex-wrap gap-3">
            <button
              className="rounded-full bg-ink px-5 py-3 text-sm font-medium text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
              disabled={disabled || isLoading || isSaving}
              type="submit"
            >
              {isSaving ? "Saving..." : editingOutfitName ? "Save outfit" : "Create outfit"}
            </button>
            {editingOutfitName ? (
              <button
                className="rounded-full border border-slate-300 px-5 py-3 text-sm font-medium text-slate-700 transition hover:bg-slate-100"
                onClick={onCancelEdit}
                type="button"
              >
                Cancel edit
              </button>
            ) : null}
          </div>

          {disabled ? (
            <p className="text-sm text-slate-500">
              Sign in and add a few wardrobe items before saving outfits.
            </p>
          ) : null}

          {error ? <p className="text-sm text-red-600">{error}</p> : null}
        </div>
      </form>

      <div className="rounded-[2rem] border border-white/70 bg-white/90 p-6 shadow-panel">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-semibold">Saved outfits</h2>
            <p className="text-sm text-slate-600">
              Keep the library editable as your closet changes.
            </p>
          </div>
          <span className="rounded-full bg-slate-100 px-4 py-2 text-sm font-medium">
            {outfits.length}
          </span>
        </div>

        <div className="mt-5 grid gap-4">
          {isLoading ? (
            <div className="rounded-[1.5rem] border border-dashed border-slate-300 bg-slate-50 p-6 text-sm text-slate-500">
              Loading saved outfits...
            </div>
          ) : null}

          {outfits.map((outfit) => (
            <article
              key={outfit.id}
              className="rounded-[1.5rem] border border-slate-200 bg-white p-5"
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h3 className="text-lg font-semibold">{outfit.name}</h3>
                  {outfit.notes ? (
                    <p className="mt-1 text-sm text-slate-600">{outfit.notes}</p>
                  ) : null}
                </div>
                <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">
                  {outfit.items.length} piece{outfit.items.length === 1 ? "" : "s"}
                </span>
              </div>

              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                {outfit.items.map((outfitItem) => {
                  const item = resolveItem(outfitItem.clothing_item_id);

                  return (
                    <div
                      key={outfitItem.id}
                      className="flex items-center gap-3 rounded-2xl border border-slate-200 bg-slate-50 p-3"
                    >
                      <div className="h-16 w-16 overflow-hidden rounded-2xl bg-slate-200">
                        {item?.image_url ? (
                          <img
                            alt={item.name}
                            className="h-full w-full object-cover"
                            src={resolveMediaUrl(item.image_url) ?? ""}
                          />
                        ) : (
                          <div className="flex h-full items-center justify-center text-[10px] uppercase tracking-[0.2em] text-slate-400">
                            No Image
                          </div>
                        )}
                      </div>
                      <div className="min-w-0">
                        <p className="text-xs font-medium uppercase tracking-[0.2em] text-moss">
                          {outfitItem.role}
                        </p>
                        <p className="truncate text-sm font-medium text-slate-800">
                          {item?.name ?? `Item #${outfitItem.clothing_item_id}`}
                        </p>
                        {item ? (
                          <p className="truncate text-xs text-slate-500">
                            {formatCategoryLabel(item.category)}
                          </p>
                        ) : null}
                      </div>
                    </div>
                  );
                })}
              </div>

              <div className="mt-4 flex flex-wrap gap-3">
                <button
                  className="rounded-full bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-200"
                  onClick={() => onEditOutfit(outfit)}
                  type="button"
                >
                  Edit
                </button>
                <button
                  className="rounded-full bg-red-50 px-4 py-2 text-sm font-medium text-red-700 transition hover:bg-red-100 disabled:cursor-not-allowed disabled:opacity-60"
                  disabled={isDeleting}
                  onClick={() => void onDeleteOutfit(outfit)}
                  type="button"
                >
                  {isDeleting ? "Deleting..." : "Delete"}
                </button>
              </div>
            </article>
          ))}

          {!isLoading && outfits.length === 0 ? (
            <div className="rounded-[1.5rem] border border-dashed border-slate-300 bg-slate-50 p-6 text-sm text-slate-500">
              No outfits yet. Create your first look from the items in your closet.
            </div>
          ) : null}
        </div>
      </div>
    </section>
  );
}
