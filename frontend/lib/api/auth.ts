import { apiRequest } from "@/lib/api/client";
import type {
  AuthResponse,
  CurrentUserResponse,
  LoginPayload,
  RegisterPayload,
} from "@/lib/types";

export function register(payload: RegisterPayload): Promise<AuthResponse> {
  return apiRequest<AuthResponse>("/auth/register", {
    method: "POST",
    body: payload,
    authenticated: false,
  });
}

export function login(payload: LoginPayload): Promise<AuthResponse> {
  return apiRequest<AuthResponse>("/auth/login", {
    method: "POST",
    body: payload,
    authenticated: false,
  });
}

export function fetchCurrentUser(): Promise<CurrentUserResponse> {
  return apiRequest<CurrentUserResponse>("/auth/me");
}

