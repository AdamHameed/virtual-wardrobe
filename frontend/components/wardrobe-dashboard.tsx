"use client";

import { FormEvent, useEffect, useState } from "react";
import { resolveMediaUrl } from "@/lib/api";
import { useClosetStore } from "@/store/closet-store";

const categories = ["Tops", "Bottoms", "Outerwear", "Shoes", "Accessories"];
const seasons = ["Spring", "Summer", "Fall", "Winter", "All Season"];

export function WardrobeDashboard() {
  const { items, isLoading, error, loadItems, addItem } = useClosetStore();
  const [name, setName] = useState("");
  const [category, setCategory] = useState(categories[0]);
  const [color, setColor] = useState("");
  const [season, setSeason] = useState(seasons[0]);
  const [notes, setNotes] = useState("");
  const [image, setImage] = useState<File | null>(null);

  useEffect(() => {
    void loadItems();
  }, [loadItems]);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!name.trim()) {
      return;
    }

    await addItem({
      name,
      category,
      color,
      season,
      notes,
      image,
    });

    setName("");
    setCategory(categories[0]);
    setColor("");
    setSeason(seasons[0]);
    setNotes("");
    setImage(null);
    event.currentTarget.reset();
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-7xl flex-col gap-10 px-6 py-10 lg:px-10">
      <section className="grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
        <div className="space-y-4">
          <p className="text-sm uppercase tracking-[0.3em] text-clay">
            Virtual Closet
          </p>
          <h1 className="max-w-3xl text-4xl font-semibold tracking-tight sm:text-5xl">
            Organize your wardrobe with a Docker-ready full-stack starter.
          </h1>
          <p className="max-w-2xl text-base leading-7 text-slate-600">
            Capture clothing items, upload photos locally, and build from a
            clean monorepo foundation designed for future growth.
          </p>
        </div>

        <form
          className="rounded-[2rem] border border-white/70 bg-white/90 p-6 shadow-panel backdrop-blur"
          onSubmit={onSubmit}
        >
          <div className="grid gap-4">
            <label className="grid gap-2">
              <span className="text-sm font-medium">Item name</span>
              <input
                className="rounded-2xl border border-slate-200 bg-white px-4 py-3"
                placeholder="Cream wool cardigan"
                value={name}
                onChange={(event) => setName(event.target.value)}
              />
            </label>

            <div className="grid gap-4 sm:grid-cols-2">
              <label className="grid gap-2">
                <span className="text-sm font-medium">Category</span>
                <select
                  className="rounded-2xl border border-slate-200 bg-white px-4 py-3"
                  value={category}
                  onChange={(event) => setCategory(event.target.value)}
                >
                  {categories.map((option) => (
                    <option key={option}>{option}</option>
                  ))}
                </select>
              </label>

              <label className="grid gap-2">
                <span className="text-sm font-medium">Season</span>
                <select
                  className="rounded-2xl border border-slate-200 bg-white px-4 py-3"
                  value={season}
                  onChange={(event) => setSeason(event.target.value)}
                >
                  {seasons.map((option) => (
                    <option key={option}>{option}</option>
                  ))}
                </select>
              </label>
            </div>

            <label className="grid gap-2">
              <span className="text-sm font-medium">Color</span>
              <input
                className="rounded-2xl border border-slate-200 bg-white px-4 py-3"
                placeholder="Oatmeal"
                value={color}
                onChange={(event) => setColor(event.target.value)}
              />
            </label>

            <label className="grid gap-2">
              <span className="text-sm font-medium">Notes</span>
              <textarea
                className="min-h-28 rounded-2xl border border-slate-200 bg-white px-4 py-3"
                placeholder="Soft knit, oversized fit, everyday staple."
                value={notes}
                onChange={(event) => setNotes(event.target.value)}
              />
            </label>

            <label className="grid gap-2">
              <span className="text-sm font-medium">Image</span>
              <input
                className="block w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 file:mr-4 file:rounded-full file:border-0 file:bg-ink file:px-4 file:py-2 file:text-sm file:font-medium file:text-white"
                type="file"
                accept="image/*"
                onChange={(event) => setImage(event.target.files?.[0] ?? null)}
              />
            </label>

            <button
              className="rounded-full bg-ink px-5 py-3 text-sm font-medium text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
              disabled={isLoading}
              type="submit"
            >
              {isLoading ? "Saving..." : "Add to closet"}
            </button>

            {error ? <p className="text-sm text-red-600">{error}</p> : null}
          </div>
        </form>
      </section>

      <section className="space-y-5">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-semibold">Closet Inventory</h2>
            <p className="text-sm text-slate-600">
              Items are stored in PostgreSQL and images live in the backend media volume.
            </p>
          </div>
          <span className="rounded-full bg-white/80 px-4 py-2 text-sm font-medium shadow-panel">
            {items.length} item{items.length === 1 ? "" : "s"}
          </span>
        </div>

        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
          {items.map((item) => (
            <article
              key={item.id}
              className="overflow-hidden rounded-[1.75rem] border border-white/70 bg-white/90 shadow-panel"
            >
              <div className="aspect-[4/3] bg-slate-100">
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
              </div>
              <div className="space-y-3 p-5">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h3 className="text-lg font-semibold">{item.name}</h3>
                    <p className="text-sm text-slate-500">{item.category}</p>
                  </div>
                  <span className="rounded-full bg-moss/10 px-3 py-1 text-xs font-medium text-moss">
                    {item.season ?? "Seasonless"}
                  </span>
                </div>

                <div className="flex flex-wrap gap-2 text-xs text-slate-600">
                  {item.color ? (
                    <span className="rounded-full bg-slate-100 px-3 py-1">
                      {item.color}
                    </span>
                  ) : null}
                </div>

                {item.notes ? (
                  <p className="text-sm leading-6 text-slate-600">{item.notes}</p>
                ) : null}
              </div>
            </article>
          ))}

          {!isLoading && items.length === 0 ? (
            <div className="rounded-[1.75rem] border border-dashed border-slate-300 bg-white/60 p-8 text-sm text-slate-500">
              No clothing items yet. Add your first piece using the form above.
            </div>
          ) : null}
        </div>
      </section>
    </main>
  );
}
