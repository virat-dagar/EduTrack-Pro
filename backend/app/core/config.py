"""Application configuration for EduTrack Pro."""

from functools import lru_cache
import os


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
