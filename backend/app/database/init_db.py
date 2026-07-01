"""Database initialization helpers."""

from app.database.base import Base, import_models
from app.database.database import engine


def create_database() -> None:
    """Create database tables for local development and tests."""

    import_models()
    Base.metadata.create_all(bind=engine)
