export const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export function getBackendOrigin(): string {
  return API_URL.replace(/\/api\/v1\/?$/, "");
}

export function resolveMediaUrl(path: string | null | undefined): string | null {
  if (!path) {
    return null;
  }

  if (path.startsWith("http://") || path.startsWith("https://")) {
    return path;
  }

  return `${getBackendOrigin()}${path}`;
}

