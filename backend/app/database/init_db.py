"""Database initialization helpers."""

from sqlalchemy import inspect, text

from app.database.base import Base, import_models
from app.database.database import engine


def create_database() -> None:
    """Create database tables for local development and tests."""

    import_models()
    Base.metadata.create_all(bind=engine)
    _ensure_sqlite_columns()


def _ensure_sqlite_columns() -> None:
    """Add nullable development columns to existing SQLite databases."""

    if engine.dialect.name != "sqlite":
        return

    column_map = {
        "students": {
            "classroom_id": "INTEGER",
        },
        "subjects": {
            "classroom_id": "INTEGER",
        },
        "attendance": {
            "classroom_id": "INTEGER",
        },
        "marks": {
            "classroom_id": "INTEGER",
        },
        "assignments": {
            "classroom_id": "INTEGER",
            "pdf_file": "VARCHAR(255)",
            "is_published": "BOOLEAN DEFAULT 1 NOT NULL",
            "published_at": "DATETIME",
        },
        "submissions": {
            "submitted_file": "VARCHAR(255)",
            "total_marks": "FLOAT",
            "percentage": "FLOAT",
            "grade": "VARCHAR(5)",
        },
    }
    with engine.begin() as connection:
        inspector = inspect(connection)
        table_names = set(inspector.get_table_names())
        for table_name, columns in column_map.items():
            if table_name not in table_names:
                continue
            existing = {column["name"] for column in inspector.get_columns(table_name)}
            for column_name, column_type in columns.items():
                if column_name not in existing:
                    connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"))
