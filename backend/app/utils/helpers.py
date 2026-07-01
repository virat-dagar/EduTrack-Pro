"""General helper functions."""

from math import ceil
from typing import Any

from sqlalchemy.orm import Query

from app.utils.constants import DEFAULT_PAGE, DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE


def normalize_pagination(page: int, page_size: int) -> tuple[int, int]:
    """Clamp pagination values to the supported range."""

    safe_page = max(page or DEFAULT_PAGE, 1)
    safe_page_size = min(max(page_size or DEFAULT_PAGE_SIZE, 1), MAX_PAGE_SIZE)
    return safe_page, safe_page_size


def paginate_query(query: Query, page: int, page_size: int) -> tuple[list[Any], int]:
    """Return paginated query items and total item count."""

    safe_page, safe_page_size = normalize_pagination(page, page_size)
    total_items = query.count()
    items = (
        query.offset((safe_page - 1) * safe_page_size)
        .limit(safe_page_size)
        .all()
    )
    return items, total_items


def total_pages(total_items: int, page_size: int) -> int:
    """Calculate total pages."""

    return ceil(total_items / page_size) if total_items else 0


def apply_sorting(query: Query, model: Any, sort: str | None, order: str, allowed: set[str]) -> Query:
    """Apply safe sorting to a SQLAlchemy query."""

    sort_field = sort if sort in allowed else next(iter(allowed))
    column = getattr(model, sort_field)
    if order.lower() == "desc":
        return query.order_by(column.desc())
    return query.order_by(column.asc())
