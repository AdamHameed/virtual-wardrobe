"use client";

import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";
import { authApi, ApiError } from "@/lib/api";
import {
  clearAccessToken,
  getAccessToken,
  setAccessToken,
} from "@/lib/auth/token-storage";
import type {
  LoginPayload,
  RegisterPayload,
  User,
} from "@/lib/types";

type AuthStore = {
  token: string | null;
  user: User | null;
  status: "idle" | "loading" | "authenticated" | "anonymous";
  error: string | null;
  initialized: boolean;
  initialize: () => Promise<void>;
  register: (payload: RegisterPayload) => Promise<void>;
  login: (payload: LoginPayload) => Promise<void>;
  logout: () => void;
  clearError: () => void;
};

function getErrorMessage(error: unknown): string {
  if (error instanceof ApiError || error instanceof Error) {
    return error.message;
  }

  return "Something went wrong.";
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      status: "idle",
      error: null,
      initialized: false,
      initialize: async () => {
        const token = getAccessToken();
        if (!token) {
          set({
            token: null,
            user: null,
            status: "anonymous",
            initialized: true,
          });
          return;
        }

        set({ status: "loading", error: null });

        try {
          const response = await authApi.fetchCurrentUser();
          set({
            token,
            user: response.user,
            status: "authenticated",
            initialized: true,
          });
        } catch {
          clearAccessToken();
          set({
            token: null,
            user: null,
            status: "anonymous",
            initialized: true,
          });
        }
      },
      register: async (payload) => {
        set({ status: "loading", error: null });

        try {
          const response = await authApi.register(payload);
          setAccessToken(response.access_token);
          set({
            token: response.access_token,
            user: response.user,
            status: "authenticated",
            initialized: true,
          });
        } catch (error) {
          set({
            error: getErrorMessage(error),
            status: "anonymous",
            initialized: true,
          });
        }
      },
      login: async (payload) => {
        set({ status: "loading", error: null });

        try {
          const response = await authApi.login(payload);
          setAccessToken(response.access_token);
          set({
            token: response.access_token,
            user: response.user,
            status: "authenticated",
            initialized: true,
          });
        } catch (error) {
          set({
            error: getErrorMessage(error),
            status: "anonymous",
            initialized: true,
          });
        }
      },
      logout: () => {
        clearAccessToken();
        set({
          token: null,
          user: null,
          status: "anonymous",
          error: null,
          initialized: true,
        });
      },
      clearError: () => set({ error: null }),
    }),
    {
      name: "virtual-closet-auth",
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        token: state.token,
        user: state.user,
      }),
    },
  ),
);

