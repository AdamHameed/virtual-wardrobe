"use client";

import { FormEvent, useDeferredValue, useEffect, useState } from "react";
import { clothingItemsApi, outfitsApi, resolveMediaUrl } from "@/lib/api";
import { AuthPanel } from "@/components/auth-panel";
import { ClothingItemForm } from "@/components/clothing-item-form";
import { OutfitBuilder } from "@/components/outfit-builder";
import { WardrobeList } from "@/components/wardrobe-list";
import { getItemsForRole } from "@/lib/wardrobe";
import {
  validateAuthPayload,
  validateClothingItemPayload,
  validateOutfitPayload,
} from "@/lib/validation";
import type {
  ClothingItem,
  ClothingItemCreatePayload,
  FieldErrors,
  LoginPayload,
  Outfit,
  OutfitCreatePayload,
  OutfitItemRole,
  RegisterPayload,
  Season,
} from "@/lib/types";
import { useAuthStore } from "@/store/auth-store";

const categories = ["Tops", "Bottoms", "Outerwear", "Shoes", "Accessories"] as const;
const seasons = ["spring", "summer", "fall", "winter", "all_season"] as const;

function getErrorMessage(error: unknown, fallback: string): string {
  return error instanceof Error ? error.message : fallback;
}

function toggleSelection(current: number[], itemId: number): number[] {
  return current.includes(itemId)
    ? current.filter((id) => id !== itemId)
    : [...current, itemId];
}

function buildOutfitItems(
  selectedTopIds: number[],
  selectedBottomIds: number[],
  selectedShoesIds: number[],
  selectedOuterwearIds: number[],
) {
  return [
    ...selectedTopIds.map((clothing_item_id, index) => ({
      clothing_item_id,
      role: "top" as const,
      position: index,
    })),
    ...selectedBottomIds.map((clothing_item_id, index) => ({
      clothing_item_id,
      role: "bottom" as const,
      position: selectedTopIds.length + index,
    })),
    ...selectedShoesIds.map((clothing_item_id, index) => ({
      clothing_item_id,
      role: "shoes" as const,
      position: selectedTopIds.length + selectedBottomIds.length + index,
    })),
    ...selectedOuterwearIds.map((clothing_item_id, index) => ({
      clothing_item_id,
      role: "outerwear" as const,
      position:
        selectedTopIds.length + selectedBottomIds.length + selectedShoesIds.length + index,
    })),
  ];
}

export function WardrobeDashboard() {
  const {
    user,
    status,
    error: authError,
    initialized,
    initialize,
    register,
    login,
    logout,
    clearError,
  } = useAuthStore();

  const [items, setItems] = useState<ClothingItem[]>([]);
  const [allItems, setAllItems] = useState<ClothingItem[]>([]);
  const [itemsTotal, setItemsTotal] = useState(0);
  const [outfits, setOutfits] = useState<Outfit[]>([]);

  const [isLoadingItems, setIsLoadingItems] = useState(false);
  const [isSavingItem, setIsSavingItem] = useState(false);
  const [isDeletingItem, setIsDeletingItem] = useState(false);
  const [isLoadingOutfits, setIsLoadingOutfits] = useState(false);
  const [isSavingOutfit, setIsSavingOutfit] = useState(false);
  const [isDeletingOutfit, setIsDeletingOutfit] = useState(false);

  const [itemsError, setItemsError] = useState<string | null>(null);
  const [outfitsError, setOutfitsError] = useState<string | null>(null);

  const [authMode, setAuthMode] = useState<"login" | "register">("register");
  const [authFormErrors, setAuthFormErrors] = useState<
    FieldErrors<"email" | "password" | "display_name">
  >({});
  const [itemFormErrors, setItemFormErrors] = useState<
    FieldErrors<"name" | "category" | "primary_color">
  >({});
  const [outfitFormErrors, setOutfitFormErrors] = useState<
    FieldErrors<"name" | "items">
  >({});

  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [activeTab, setActiveTab] = useState<"clothes" | "outfits">("clothes");

  const [editingItem, setEditingItem] = useState<ClothingItem | null>(null);
  const [editingOutfit, setEditingOutfit] = useState<Outfit | null>(null);
  const [viewingItem, setViewingItem] = useState<ClothingItem | null>(null);

  const [name, setName] = useState("");
  const [category, setCategory] = useState<(typeof categories)[number]>(categories[0]);
  const [primaryColor, setPrimaryColor] = useState("");
  const [season, setSeason] = useState<Season>(seasons[0]);
  const [notes, setNotes] = useState("");
  const [image, setImage] = useState<File | null>(null);

  const [searchQuery, setSearchQuery] = useState("");
  const [seasonFilter, setSeasonFilter] = useState<Season | "all">("all");
  const deferredSearchQuery = useDeferredValue(searchQuery);

  const [outfitName, setOutfitName] = useState("");
  const [outfitNotes, setOutfitNotes] = useState("");
  const [selectedTopIds, setSelectedTopIds] = useState<number[]>([]);
  const [selectedBottomIds, setSelectedBottomIds] = useState<number[]>([]);
  const [selectedShoesIds, setSelectedShoesIds] = useState<number[]>([]);
  const [selectedOuterwearIds, setSelectedOuterwearIds] = useState<number[]>([]);

  const topOptions = getItemsForRole(allItems, "top");
  const bottomOptions = getItemsForRole(allItems, "bottom");
  const shoeOptions = getItemsForRole(allItems, "shoes");
  const outerwearOptions = getItemsForRole(allItems, "outerwear");

  useEffect(() => {
    void initialize();
  }, [initialize]);

  useEffect(() => {
    if (!initialized || status !== "authenticated") {
      setItems([]);
      setAllItems([]);
      setItemsTotal(0);
      setOutfits([]);
      return;
    }

    async function loadItemsWithFallback() {
      setIsLoadingItems(true);
      setItemsError(null);

      try {
        const filteredResponse = await clothingItemsApi.listClothingItems(
          { limit: 48, offset: 0 },
          {
            ...(deferredSearchQuery.trim() ? { query: deferredSearchQuery.trim() } : {}),
            ...(seasonFilter !== "all" ? { season: seasonFilter } : {}),
          },
        );
        setItems(filteredResponse.items);
        setItemsTotal(filteredResponse.total);

        try {
          const allResponse = await clothingItemsApi.listClothingItems({
            limit: 100,
            offset: 0,
          });
          setAllItems(allResponse.items);
        } catch {
          setAllItems(filteredResponse.items);
        }
      } catch (error) {
        setItemsError(getErrorMessage(error, "Unable to load wardrobe."));
      } finally {
        setIsLoadingItems(false);
      }
    }

    void loadItemsWithFallback();
  }, [deferredSearchQuery, initialized, seasonFilter, status]);

  useEffect(() => {
    if (!initialized || status !== "authenticated") {
      setOutfits([]);
      return;
    }

    async function loadOutfits() {
      setIsLoadingOutfits(true);
      setOutfitsError(null);

      try {
        const response = await outfitsApi.listOutfits({ limit: 24, offset: 0 });
        setOutfits(response.items);
      } catch (error) {
        setOutfitsError(getErrorMessage(error, "Unable to load saved outfits."));
      } finally {
        setIsLoadingOutfits(false);
      }
    }

    void loadOutfits();
  }, [initialized, status]);

  function resetItemForm() {
    setEditingItem(null);
    setName("");
    setCategory(categories[0]);
    setPrimaryColor("");
    setSeason(seasons[0]);
    setNotes("");
    setImage(null);
    setItemFormErrors({});
  }

  function resetOutfitForm() {
    setEditingOutfit(null);
    setOutfitName("");
    setOutfitNotes("");
    setSelectedTopIds([]);
    setSelectedBottomIds([]);
    setSelectedShoesIds([]);
    setSelectedOuterwearIds([]);
    setOutfitFormErrors({});
  }

  function startEditingItem(item: ClothingItem) {
    setEditingItem(item);
    setName(item.name);
    setCategory((categories.find((option) => option.toLowerCase() === item.category) ??
      categories[0]) as (typeof categories)[number]);
    setPrimaryColor(item.primary_color ?? "");
    setSeason(item.season ?? seasons[0]);
    setNotes(item.notes ?? "");
    setImage(null);
    setItemFormErrors({});
  }

  async function onAuthSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    clearError();

    const payload: RegisterPayload | LoginPayload =
      authMode === "register"
        ? {
            email,
            password,
            display_name: displayName || null,
          }
        : {
            email,
            password,
          };

    const errors = validateAuthPayload(payload, authMode);
    setAuthFormErrors(errors);

    if (Object.keys(errors).length > 0) {
      return;
    }

    if (authMode === "register") {
      await register(payload as RegisterPayload);
      return;
    }

    await login(payload as LoginPayload);
  }

  async function onSaveItem(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const payload: ClothingItemCreatePayload = {
      name,
      category: category.toLowerCase(),
      primary_color: primaryColor,
      season,
      notes,
      image,
    };

    const errors = validateClothingItemPayload(payload);
    setItemFormErrors(errors);

    if (Object.keys(errors).length > 0) {
      return;
    }

    setIsSavingItem(true);
    setItemsError(null);

    try {
      if (editingItem) {
        const updatedItem = await clothingItemsApi.updateClothingItem(editingItem.id, payload);
        setItems((currentItems) =>
          currentItems.map((item) => (item.id === updatedItem.id ? updatedItem : item)),
        );
        setAllItems((currentItems) =>
          currentItems.map((item) => (item.id === updatedItem.id ? updatedItem : item)),
        );
        setViewingItem((current) => (current?.id === updatedItem.id ? updatedItem : current));
      } else {
        const newItem = await clothingItemsApi.createClothingItem(payload);
        setItems((currentItems) => [newItem, ...currentItems]);
        setAllItems((currentItems) => [newItem, ...currentItems]);
        setItemsTotal((currentTotal) => currentTotal + 1);
      }

      resetItemForm();
    } catch (error) {
      setItemsError(getErrorMessage(error, "Unable to save clothing item."));
    } finally {
      setIsSavingItem(false);
    }
  }

  async function onDeleteItem(item: ClothingItem) {
    const confirmed = window.confirm(`Delete "${item.name}" from your wardrobe?`);
    if (!confirmed) {
      return;
    }

    setIsDeletingItem(true);
    setItemsError(null);

    try {
      await clothingItemsApi.deleteClothingItem(item.id);
      setItems((currentItems) => currentItems.filter((currentItem) => currentItem.id !== item.id));
      setAllItems((currentItems) => currentItems.filter((currentItem) => currentItem.id !== item.id));
      setItemsTotal((currentTotal) => Math.max(0, currentTotal - 1));
      setViewingItem((current) => (current?.id === item.id ? null : current));
      if (editingItem?.id === item.id) {
        resetItemForm();
      }
      setOutfits((currentOutfits) =>
        currentOutfits
          .map((outfit) => ({
            ...outfit,
            items: outfit.items.filter((outfitItem) => outfitItem.clothing_item_id !== item.id),
          }))
          .filter((outfit) => outfit.items.length > 0),
      );
    } catch (error) {
      setItemsError(getErrorMessage(error, "Unable to delete clothing item."));
    } finally {
      setIsDeletingItem(false);
    }
  }

  async function onCreateOutfit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const payload: OutfitCreatePayload = {
      name: outfitName,
      notes: outfitNotes || null,
      items: buildOutfitItems(
        selectedTopIds,
        selectedBottomIds,
        selectedShoesIds,
        selectedOuterwearIds,
      ),
    };

    const errors = validateOutfitPayload(payload);
    setOutfitFormErrors(errors);

    if (Object.keys(errors).length > 0) {
      return;
    }

    setIsSavingOutfit(true);
    setOutfitsError(null);

    try {
      if (editingOutfit) {
        const outfit = await outfitsApi.updateOutfit(editingOutfit.id, payload);
        setOutfits((currentOutfits) =>
          currentOutfits.map((currentOutfit) =>
            currentOutfit.id === outfit.id ? outfit : currentOutfit,
          ),
        );
      } else {
        const outfit = await outfitsApi.createOutfit(payload);
        setOutfits((currentOutfits) => [outfit, ...currentOutfits]);
      }

      resetOutfitForm();
    } catch (error) {
      setOutfitsError(getErrorMessage(error, "Unable to save outfit."));
    } finally {
      setIsSavingOutfit(false);
    }
  }

  function onEditOutfit(outfit: Outfit) {
    setEditingOutfit(outfit);
    setOutfitName(outfit.name);
    setOutfitNotes(outfit.notes ?? "");
    setSelectedTopIds(
      outfit.items.filter((item) => item.role === "top").map((item) => item.clothing_item_id),
    );
    setSelectedBottomIds(
      outfit.items.filter((item) => item.role === "bottom").map((item) => item.clothing_item_id),
    );
    setSelectedShoesIds(
      outfit.items.filter((item) => item.role === "shoes").map((item) => item.clothing_item_id),
    );
    setSelectedOuterwearIds(
      outfit.items
        .filter((item) => item.role === "outerwear")
        .map((item) => item.clothing_item_id),
    );
    setOutfitFormErrors({});
  }

  async function onDeleteOutfit(outfit: Outfit) {
    const confirmed = window.confirm(`Delete the outfit "${outfit.name}"?`);
    if (!confirmed) {
      return;
    }

    setIsDeletingOutfit(true);
    setOutfitsError(null);

    try {
      await outfitsApi.deleteOutfit(outfit.id);
      setOutfits((currentOutfits) =>
        currentOutfits.filter((currentOutfit) => currentOutfit.id !== outfit.id),
      );
      if (editingOutfit?.id === outfit.id) {
        resetOutfitForm();
      }
    } catch (error) {
      setOutfitsError(getErrorMessage(error, "Unable to delete outfit."));
    } finally {
      setIsDeletingOutfit(false);
    }
  }

  function resolveItem(clothingItemId: number): ClothingItem | undefined {
    return allItems.find((item) => item.id === clothingItemId);
  }

  function onToggleOutfitItem(role: OutfitItemRole, clothingItemId: number) {
    setOutfitFormErrors({});

    if (role === "top") {
      setSelectedTopIds((current) => toggleSelection(current, clothingItemId));
      return;
    }
    if (role === "bottom") {
      setSelectedBottomIds((current) => toggleSelection(current, clothingItemId));
      return;
    }
    if (role === "shoes") {
      setSelectedShoesIds((current) => toggleSelection(current, clothingItemId));
      return;
    }
    if (role === "outerwear") {
      setSelectedOuterwearIds((current) => toggleSelection(current, clothingItemId));
    }
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-7xl flex-col gap-10 px-6 py-10 lg:px-10">
      <section className="grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
        <div className="space-y-4">
          <p className="text-sm uppercase tracking-[0.3em] text-clay">
            Virtual Closet
          </p>
          <h1 className="max-w-3xl text-4xl font-semibold tracking-tight sm:text-5xl">
            Build outfits from a wardrobe that stays easy to browse and maintain.
          </h1>
          <p className="max-w-2xl text-base leading-7 text-slate-600">
            Manage your closet, open full item photos, and compose layered outfits from
            the same streamlined dashboard.
          </p>
        </div>

        <div className="rounded-[2rem] border border-white/70 bg-white/90 p-6 shadow-panel backdrop-blur">
          {status === "authenticated" && user ? (
            <div className="space-y-3">
              <p className="text-sm uppercase tracking-[0.25em] text-moss">
                Signed In
              </p>
              <h2 className="text-2xl font-semibold">
                {user.display_name ?? user.email}
              </h2>
              <p className="text-sm text-slate-600">
                Search your wardrobe, edit saved pieces, and build looks with multiple layers.
              </p>
              <button
                className="rounded-full border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-100"
                onClick={logout}
                type="button"
              >
                Sign out
              </button>
            </div>
          ) : (
            <AuthPanel
              authMode={authMode}
              displayName={displayName}
              email={email}
              password={password}
              status={status}
              authError={authError}
              errors={authFormErrors}
              onModeChange={(mode) => {
                setAuthMode(mode);
                setAuthFormErrors({});
                clearError();
              }}
              onDisplayNameChange={setDisplayName}
              onEmailChange={setEmail}
              onPasswordChange={setPassword}
              onSubmit={onAuthSubmit}
            />
          )}
        </div>
      </section>

      <section className="space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex gap-2 rounded-full bg-white/90 p-1 shadow-panel">
            <button
              className={`rounded-full px-5 py-2 text-sm font-medium transition ${
                activeTab === "clothes"
                  ? "bg-ink text-white"
                  : "text-slate-600 hover:bg-slate-100"
              }`}
              onClick={() => setActiveTab("clothes")}
              type="button"
            >
              Clothes
            </button>
            <button
              className={`rounded-full px-5 py-2 text-sm font-medium transition ${
                activeTab === "outfits"
                  ? "bg-ink text-white"
                  : "text-slate-600 hover:bg-slate-100"
              }`}
              onClick={() => setActiveTab("outfits")}
              type="button"
            >
              Outfits
            </button>
          </div>

          {status === "authenticated" ? (
            <span className="rounded-full bg-white/80 px-4 py-2 text-sm font-medium shadow-panel">
              {activeTab === "clothes"
                ? `${itemsTotal} total item${itemsTotal === 1 ? "" : "s"}`
                : `${outfits.length} saved outfit${outfits.length === 1 ? "" : "s"}`}
            </span>
          ) : null}
        </div>

        {activeTab === "clothes" ? (
          <>
            <section className="grid items-start gap-8 lg:grid-cols-[0.95fr_1.05fr]">
              <ClothingItemForm
                title={editingItem ? "Edit clothing item" : "Add a clothing item"}
                description={
                  editingItem
                    ? "Update the details for this piece, or replace its image if you want a better reference."
                    : "Capture the essentials and keep your wardrobe inventory tidy."
                }
                submitLabel={editingItem ? "Save changes" : "Add to closet"}
                secondaryActionLabel={editingItem ? "Cancel edit" : undefined}
                categories={categories}
                seasons={seasons}
                name={name}
                category={category}
                primaryColor={primaryColor}
                season={season}
                notes={notes}
                disabled={status !== "authenticated"}
                isSubmitting={isSavingItem}
                errors={itemFormErrors}
                onNameChange={setName}
                onCategoryChange={(value) => setCategory(value as (typeof categories)[number])}
                onPrimaryColorChange={setPrimaryColor}
                onSeasonChange={setSeason}
                onNotesChange={setNotes}
                onImageChange={setImage}
                onSecondaryAction={resetItemForm}
                onSubmit={onSaveItem}
              />

              <WardrobeList
                items={items}
                isLoading={isLoadingItems}
                isDeletingItem={isDeletingItem}
                error={
                  status === "authenticated"
                    ? itemsError
                    : initialized
                      ? "Sign in to load your closet and start saving items."
                      : null
                }
                searchQuery={searchQuery}
                seasonFilter={seasonFilter}
                onSearchQueryChange={setSearchQuery}
                onSeasonFilterChange={setSeasonFilter}
                onViewItem={setViewingItem}
                onEditItem={startEditingItem}
                onDeleteItem={onDeleteItem}
              />
            </section>

            <section className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-semibold">Wardrobe at a glance</h2>
                <p className="text-sm text-slate-600">
                  {status === "authenticated"
                    ? `Showing ${items.length} of ${itemsTotal} wardrobe items.`
                    : "Authenticate to explore your closet and save outfit combinations."}
                </p>
              </div>
            </section>
          </>
        ) : (
          <OutfitBuilder
            outfits={outfits}
            isLoading={isLoadingOutfits}
            isSaving={isSavingOutfit}
            isDeleting={isDeletingOutfit}
            disabled={status !== "authenticated"}
            error={
              status === "authenticated"
                ? outfitsError
                : initialized
                  ? "Sign in to create and save outfits."
                  : null
            }
            formErrors={outfitFormErrors}
            outfitName={outfitName}
            outfitNotes={outfitNotes}
            editingOutfitName={editingOutfit?.name ?? null}
            selectedTopIds={selectedTopIds}
            selectedBottomIds={selectedBottomIds}
            selectedShoesIds={selectedShoesIds}
            selectedOuterwearIds={selectedOuterwearIds}
            topOptions={topOptions}
            bottomOptions={bottomOptions}
            shoeOptions={shoeOptions}
            outerwearOptions={outerwearOptions}
            resolveItem={resolveItem}
            onOutfitNameChange={setOutfitName}
            onOutfitNotesChange={setOutfitNotes}
            onToggleItem={onToggleOutfitItem}
            onEditOutfit={onEditOutfit}
            onDeleteOutfit={onDeleteOutfit}
            onCancelEdit={resetOutfitForm}
            onSubmit={onCreateOutfit}
          />
        )}
      </section>

      {viewingItem ? (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/70 p-6">
          <div className="w-full max-w-4xl overflow-hidden rounded-[2rem] bg-white shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-200 px-6 py-4">
              <div>
                <h3 className="text-xl font-semibold">{viewingItem.name}</h3>
                <p className="text-sm text-slate-500">
                  {viewingItem.primary_color ?? "No color noted"} · {viewingItem.category}
                </p>
              </div>
              <button
                className="rounded-full border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-100"
                onClick={() => setViewingItem(null)}
                type="button"
              >
                Close
              </button>
            </div>
            <div className="grid gap-6 p-6 lg:grid-cols-[1.25fr_0.75fr]">
              <div className="overflow-hidden rounded-[1.5rem] bg-slate-100">
                {viewingItem.image_url ? (
                  <img
                    alt={viewingItem.name}
                    className="h-full w-full object-contain bg-slate-100"
                    src={resolveMediaUrl(viewingItem.image_url) ?? ""}
                  />
                ) : (
                  <div className="flex min-h-[24rem] items-center justify-center text-sm uppercase tracking-[0.25em] text-slate-400">
                    No Image
                  </div>
                )}
              </div>
              <div className="space-y-4">
                <div className="flex flex-wrap gap-2 text-xs text-slate-600">
                  <span className="rounded-full bg-slate-100 px-3 py-1 capitalize">
                    {viewingItem.category}
                  </span>
                  {viewingItem.season ? (
                    <span className="rounded-full bg-slate-100 px-3 py-1 capitalize">
                      {viewingItem.season.replace("_", " ")}
                    </span>
                  ) : null}
                </div>
                {viewingItem.notes ? (
                  <p className="text-sm leading-7 text-slate-600">{viewingItem.notes}</p>
                ) : (
                  <p className="text-sm text-slate-500">No notes for this item yet.</p>
                )}
                <div className="flex flex-wrap gap-3">
                  <button
                    className="rounded-full bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-200"
                    onClick={() => {
                      startEditingItem(viewingItem);
                      setViewingItem(null);
                    }}
                    type="button"
                  >
                    Edit item
                  </button>
                  <button
                    className="rounded-full bg-red-50 px-4 py-2 text-sm font-medium text-red-700 transition hover:bg-red-100"
                    onClick={() => void onDeleteItem(viewingItem)}
                    type="button"
                  >
                    Delete item
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </main>
  );
}
