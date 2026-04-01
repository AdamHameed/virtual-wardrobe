from __future__ import annotations

import socket
import time
from urllib.parse import urlparse

from app.core.config import settings


def get_target() -> tuple[str, int]:
    parsed = urlparse(settings.database_url.replace("+psycopg", ""))
    host = parsed.hostname or "db"
    port = parsed.port or 5432
    return host, port


def wait_for_db(timeout_seconds: int = 60) -> None:
    host, port = get_target()
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
      try:
          with socket.create_connection((host, port), timeout=2):
              print(f"Database is reachable at {host}:{port}.")
              return
      except OSError:
          print(f"Waiting for database at {host}:{port}...")
          time.sleep(2)

    raise TimeoutError(f"Timed out waiting for database at {host}:{port}.")


if __name__ == "__main__":
    wait_for_db()
