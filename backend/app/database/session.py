"""Database session dependency."""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Yield a request-scoped database session."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
