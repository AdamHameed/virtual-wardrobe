"use client";

import { FormEvent } from "react";
import type { FieldErrors } from "@/lib/types";

type AuthPanelProps = {
  authMode: "login" | "register";
  displayName: string;
  email: string;
  password: string;
  status: "idle" | "loading" | "authenticated" | "anonymous";
  authError: string | null;
  errors: FieldErrors<"email" | "password" | "display_name">;
  onModeChange: (mode: "login" | "register") => void;
  onDisplayNameChange: (value: string) => void;
  onEmailChange: (value: string) => void;
  onPasswordChange: (value: string) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => Promise<void>;
};

export function AuthPanel({
  authMode,
  displayName,
  email,
  password,
  status,
  authError,
  errors,
  onModeChange,
  onDisplayNameChange,
  onEmailChange,
  onPasswordChange,
  onSubmit,
}: AuthPanelProps) {
  return (
    <form className="grid gap-4" onSubmit={onSubmit}>
      <div className="flex gap-2 rounded-full bg-slate-100 p-1">
        <button
          className={`flex-1 rounded-full px-4 py-2 text-sm font-medium ${authMode === "register" ? "bg-ink text-white" : "text-slate-600"}`}
          onClick={() => onModeChange("register")}
          type="button"
        >
          Register
        </button>
        <button
          className={`flex-1 rounded-full px-4 py-2 text-sm font-medium ${authMode === "login" ? "bg-ink text-white" : "text-slate-600"}`}
          onClick={() => onModeChange("login")}
          type="button"
        >
          Login
        </button>
      </div>

      {authMode === "register" ? (
        <label className="grid gap-2">
          <span className="text-sm font-medium">Display name</span>
          <input
            className="rounded-2xl border border-slate-200 bg-white px-4 py-3"
            value={displayName}
            onChange={(event) => onDisplayNameChange(event.target.value)}
            placeholder="Closet Owner"
          />
          {errors.display_name ? (
            <span className="text-sm text-red-600">{errors.display_name}</span>
          ) : null}
        </label>
      ) : null}

      <label className="grid gap-2">
        <span className="text-sm font-medium">Email</span>
        <input
          className="rounded-2xl border border-slate-200 bg-white px-4 py-3"
          type="email"
          value={email}
          onChange={(event) => onEmailChange(event.target.value)}
          placeholder="closet@example.com"
        />
        {errors.email ? (
          <span className="text-sm text-red-600">{errors.email}</span>
        ) : null}
      </label>

      <label className="grid gap-2">
        <span className="text-sm font-medium">Password</span>
        <input
          className="rounded-2xl border border-slate-200 bg-white px-4 py-3"
          type="password"
          value={password}
          onChange={(event) => onPasswordChange(event.target.value)}
          placeholder="At least 8 characters"
        />
        {errors.password ? (
          <span className="text-sm text-red-600">{errors.password}</span>
        ) : null}
      </label>

      <button
        className="rounded-full bg-ink px-5 py-3 text-sm font-medium text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
        disabled={status === "loading"}
        type="submit"
      >
        {status === "loading"
          ? "Working..."
          : authMode === "register"
            ? "Create account"
            : "Sign in"}
      </button>


      {authError ? <p className="text-sm text-red-600">{authError}</p> : null}
    </form>
  );
}
