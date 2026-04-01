from typing import Annotated
from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Virtual Closet API"
    app_env: str = "production"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/virtual_closet"
    cors_origins: Annotated[list[str], NoDecode] = ["http://localhost:3000"]
    media_root: str = "media"
    media_url: str = "/media"
    max_upload_size_mb: int = 10
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 60
    jwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="VC_",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if value.startswith("postgresql+psycopg://"):
            return value
        if value.startswith("postgres://"):
            return value.replace("postgres://", "postgresql+psycopg://", 1)
        if value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+psycopg://", 1)
        return value

    @field_validator("media_root")
    @classmethod
    def ensure_media_root_exists(cls, value: str) -> str:
        Path(value).mkdir(parents=True, exist_ok=True)
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
