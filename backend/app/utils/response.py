"""Standard API response builders."""

from typing import Any


def success_response(message: str = "", data: Any = None) -> dict[str, Any]:
    """Build a standard successful API response."""

    return {"success": True, "message": message, "data": data}


def error_response(
    message: str,
    errors: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Build a standard error API response."""

    return {"success": False, "message": message, "errors": errors or []}


def pagination_response(
    items: list[Any],
    page: int,
    page_size: int,
    total_items: int,
) -> dict[str, Any]:
    """Build a paginated response payload."""

    total_pages = (total_items + page_size - 1) // page_size if total_items else 0
    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages,
    }
