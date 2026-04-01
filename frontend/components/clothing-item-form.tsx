"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import type { FieldErrors, Season } from "@/lib/types";

type ClothingItemFormProps = {
  title?: string;
  description?: string;
  submitLabel?: string;
  secondaryActionLabel?: string;
  categories: readonly string[];
  seasons: readonly Season[];
  name: string;
  category: string;
  primaryColor: string;
  season: Season;
  notes: string;
  disabled: boolean;
  isSubmitting: boolean;
  errors: FieldErrors<"name" | "category" | "primary_color">;
  onNameChange: (value: string) => void;
  onCategoryChange: (value: string) => void;
  onPrimaryColorChange: (value: string) => void;
  onSeasonChange: (value: Season) => void;
  onNotesChange: (value: string) => void;
  onImageChange: (file: File | null) => void;
  onSecondaryAction?: () => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => Promise<void>;
};

function stopStream(stream: MediaStream | null) {
  stream?.getTracks().forEach((track) => track.stop());
}

export function ClothingItemForm({
  title = "Add a clothing item",
  description = "Capture the essentials and keep your wardrobe inventory tidy.",
  submitLabel = "Add to closet",
  secondaryActionLabel,
  categories,
  seasons,
  name,
  category,
  primaryColor,
  season,
  notes,
  disabled,
  isSubmitting,
  errors,
  onNameChange,
  onCategoryChange,
  onPrimaryColorChange,
  onSeasonChange,
  onNotesChange,
  onImageChange,
  onSecondaryAction,
  onSubmit,
}: ClothingItemFormProps) {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [cameraOpen, setCameraOpen] = useState(false);
  const [cameraError, setCameraError] = useState<string | null>(null);
  const [cameraStream, setCameraStream] = useState<MediaStream | null>(null);
  const [selectedImageName, setSelectedImageName] = useState<string | null>(null);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.srcObject = cameraStream;
    }
  }, [cameraStream]);

  useEffect(() => {
    return () => {
      stopStream(cameraStream);
    };
  }, [cameraStream]);

  async function openCamera() {
    setCameraError(null);

    if (!navigator.mediaDevices?.getUserMedia) {
      setCameraError("Camera access is not supported in this browser.");
      return;
    }

    try {
      stopStream(cameraStream);
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment" },
        audio: false,
      });
      setCameraStream(stream);
      setCameraOpen(true);
    } catch {
      setCameraError("Unable to access the camera. Check browser permissions.");
    }
  }

  function closeCamera() {
    stopStream(cameraStream);
    setCameraStream(null);
    setCameraOpen(false);
  }

  function capturePhoto() {
    if (!videoRef.current || !canvasRef.current) {
      return;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const width = video.videoWidth;
    const height = video.videoHeight;

    if (!width || !height) {
      setCameraError("Camera preview is not ready yet. Try again in a moment.");
      return;
    }

    canvas.width = width;
    canvas.height = height;

    const context = canvas.getContext("2d");
    if (!context) {
      setCameraError("Unable to capture a photo from this browser.");
      return;
    }

    context.drawImage(video, 0, 0, width, height);
    canvas.toBlob((blob) => {
      if (!blob) {
        setCameraError("Unable to capture a photo.");
        return;
      }

      const file = new File([blob], `camera-capture-${Date.now()}.jpg`, {
        type: "image/jpeg",
      });
      onImageChange(file);
      setSelectedImageName(file.name);
      closeCamera();
    }, "image/jpeg", 0.92);
  }

  return (
    <form
      className="rounded-[2rem] border border-white/70 bg-white/90 p-6 shadow-panel backdrop-blur lg:sticky lg:top-6"
      onSubmit={onSubmit}
    >
      <div className="grid gap-4">
        <div className="space-y-1">
          <h2 className="text-2xl font-semibold">{title}</h2>
          <p className="text-sm text-slate-600">{description}</p>
        </div>

        <label className="grid gap-2">
          <span className="text-sm font-medium">Item name</span>
          <input
            className="rounded-2xl border border-slate-200 bg-white px-4 py-3"
            disabled={disabled || isSubmitting}
            placeholder="Cream wool cardigan"
            value={name}
            onChange={(event) => onNameChange(event.target.value)}
          />
          {errors.name ? <span className="text-sm text-red-600">{errors.name}</span> : null}
        </label>

        <div className="grid gap-4 sm:grid-cols-2">
          <label className="grid gap-2">
            <span className="text-sm font-medium">Category</span>
            <select
              className="rounded-2xl border border-slate-200 bg-white px-4 py-3"
              disabled={disabled || isSubmitting}
              value={category}
              onChange={(event) => onCategoryChange(event.target.value)}
            >
              {categories.map((option) => (
                <option key={option}>{option}</option>
              ))}
            </select>
            {errors.category ? (
              <span className="text-sm text-red-600">{errors.category}</span>
            ) : null}
          </label>

          <label className="grid gap-2">
            <span className="text-sm font-medium">Season</span>
            <select
              className="rounded-2xl border border-slate-200 bg-white px-4 py-3"
              disabled={disabled || isSubmitting}
              value={season}
              onChange={(event) => onSeasonChange(event.target.value as Season)}
            >
              {seasons.map((option) => (
                <option key={option} value={option}>
                  {option.replace("_", " ")}
                </option>
              ))}
            </select>
          </label>
        </div>

        <label className="grid gap-2">
          <span className="text-sm font-medium">Primary color</span>
          <input
            className="rounded-2xl border border-slate-200 bg-white px-4 py-3"
            disabled={disabled || isSubmitting}
            placeholder="Oatmeal"
            value={primaryColor}
            onChange={(event) => onPrimaryColorChange(event.target.value)}
          />
          {errors.primary_color ? (
            <span className="text-sm text-red-600">{errors.primary_color}</span>
          ) : null}
        </label>

        <label className="grid gap-2">
          <span className="text-sm font-medium">Notes</span>
          <textarea
            className="min-h-28 rounded-2xl border border-slate-200 bg-white px-4 py-3"
            disabled={disabled || isSubmitting}
            placeholder="Soft knit, oversized fit, everyday staple."
            value={notes}
            onChange={(event) => onNotesChange(event.target.value)}
          />
        </label>

        <div className="grid gap-3">
          <label className="grid gap-2">
            <span className="text-sm font-medium">Image</span>
            <input
              className="block w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 file:mr-4 file:rounded-full file:border-0 file:bg-ink file:px-4 file:py-2 file:text-sm file:font-medium file:text-white"
              type="file"
              accept="image/*"
              disabled={disabled || isSubmitting}
              onChange={(event) => {
                const file = event.target.files?.[0] ?? null;
                onImageChange(file);
                setSelectedImageName(file?.name ?? null);
              }}
            />
          </label>

          <div className="flex flex-wrap gap-3">
            <button
              className="rounded-full border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-60"
              disabled={disabled || isSubmitting}
              onClick={() => void openCamera()}
              type="button"
            >
              Use camera
            </button>
            {selectedImageName ? (
              <span className="rounded-full bg-slate-100 px-4 py-2 text-sm text-slate-600">
                {selectedImageName}
              </span>
            ) : null}
          </div>

          {cameraError ? (
            <p className="text-sm text-red-600">{cameraError}</p>
          ) : null}

          {cameraOpen ? (
            <div className="grid gap-3 rounded-[1.5rem] border border-slate-200 bg-slate-50 p-4">
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="aspect-[4/3] w-full rounded-[1.25rem] bg-slate-900 object-cover"
              />
              <canvas ref={canvasRef} className="hidden" />
              <div className="flex flex-wrap gap-3">
                <button
                  className="rounded-full bg-ink px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-800"
                  onClick={capturePhoto}
                  type="button"
                >
                  Capture photo
                </button>
                <button
                  className="rounded-full border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-100"
                  onClick={closeCamera}
                  type="button"
                >
                  Close camera
                </button>
              </div>
            </div>
          ) : null}
        </div>

        <div className="flex flex-wrap gap-3">
          <button
            className="rounded-full bg-ink px-5 py-3 text-sm font-medium text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
            disabled={disabled || isSubmitting}
            type="submit"
          >
            {isSubmitting ? "Saving..." : submitLabel}
          </button>
          {secondaryActionLabel && onSecondaryAction ? (
            <button
              className="rounded-full border border-slate-300 px-5 py-3 text-sm font-medium text-slate-700 transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-60"
              disabled={isSubmitting}
              onClick={onSecondaryAction}
              type="button"
            >
              {secondaryActionLabel}
            </button>
          ) : null}
        </div>
      </div>
    </form>
  );
}
