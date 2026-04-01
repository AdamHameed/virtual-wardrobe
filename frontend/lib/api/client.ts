import { API_URL } from "@/lib/config";
import { clearAccessToken, getAccessToken } from "@/lib/auth/token-storage";

type RequestOptions = Omit<RequestInit, "body" | "headers"> & {
  body?: BodyInit | object | null;
  headers?: HeadersInit;
  authenticated?: boolean;
};

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

function formatValidationErrors(
  detail: Array<{ loc?: Array<string | number>; msg?: string }>,
): string {
  const messages = detail
    .map((issue) => {
      if (!issue.msg) {
        return null;
      }

      const path = issue.loc?.slice(1).join(".") ?? "";
      return path ? `${path}: ${issue.msg}` : issue.msg;
    })
    .filter((message): message is string => Boolean(message));

  return messages.join(" ");
}

async function parseError(response: Response): Promise<never> {
  let message = "Request failed";

  try {
    const contentType = response.headers.get("content-type") ?? "";
    if (contentType.includes("application/json")) {
      const json = (await response.json()) as {
        detail?: string | Array<{ loc?: Array<string | number>; msg?: string }>;
      };
      if (typeof json.detail === "string") {
        message = json.detail;
      } else if (Array.isArray(json.detail)) {
        message = formatValidationErrors(json.detail) || message;
      }
    } else {
      const text = await response.text();
      message = text || message;
    }
  } catch {
    message = response.statusText || message;
  }

  throw new ApiError(message, response.status);
}

async function parseResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    if (response.status === 401) {
      clearAccessToken();
    }
    return parseError(response);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export async function apiRequest<T>(
  path: string,
  options: RequestOptions = {},
): Promise<T> {
  const { body, headers, authenticated = true, ...init } = options;
  const requestHeaders = new Headers(headers);

  let requestBody: BodyInit | null | undefined = body as BodyInit | null | undefined;
  const isFormData = typeof FormData !== "undefined" && body instanceof FormData;

  if (body && !isFormData && typeof body === "object") {
    requestHeaders.set("Content-Type", "application/json");
    requestBody = JSON.stringify(body);
  }

  if (authenticated) {
    const token = getAccessToken();
    if (token) {
      requestHeaders.set("Authorization", `Bearer ${token}`);
    }
  }

  let response: Response;

  try {
    response = await fetch(`${API_URL}${path}`, {
      ...init,
      headers: requestHeaders,
      body: requestBody,
    });
  } catch {
    throw new ApiError(
      "Unable to reach the backend. Confirm the Docker services are running.",
      0,
    );
  }

  return parseResponse<T>(response);
}
