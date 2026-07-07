"""Application configuration for EduTrack Pro."""

from functools import lru_cache
import os
from pathlib import Path


class Settings:
    """Runtime settings loaded from environment variables."""

    app_name: str = "EduTrack Pro"
    api_v1_prefix: str = "/api/v1"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./edutrack_pro.db")
    secret_key: str = os.getenv(
        "SECRET_KEY",
        "edutrack-pro-local-development-secret-change-before-production",
    )
    algorithm: str = os.getenv("JWT_ALGORITHM", os.getenv("ALGORITHM", "HS256"))
    access_token_expire_minutes: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440")
    )
    upload_dir: str = os.getenv("UPLOAD_DIR", "uploads")
    max_upload_bytes: int = int(os.getenv("MAX_UPLOAD_BYTES", "10485760"))
    cors_origins: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            os.getenv(
                "BACKEND_CORS_ORIGINS",
                "http://localhost:5173,http://127.0.0.1:5173",
            ),
        ).split(",")
        if origin.strip()
    ]


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()


def resolve_upload_dir(upload_dir: str | None = None) -> Path:
    """Return an absolute path for runtime uploads."""

    configured_dir = upload_dir or get_settings().upload_dir
    path = Path(configured_dir)
    if path.is_absolute():
        return path
    return Path(__file__).resolve().parents[2] / path
