"""Common Pydantic schemas."""

from typing import Any

from pydantic import BaseModel, Field


class APIResponse(BaseModel):
    """Standard API response envelope."""

    success: bool
    message: str = ""
    data: Any = None


class ErrorDetail(BaseModel):
    """Field-level error detail."""

    field: str
    message: str


class ErrorResponse(BaseModel):
    """Standard error response envelope."""

    success: bool = False
    message: str
    errors: list[ErrorDetail] = Field(default_factory=list)


class PaginationData(BaseModel):
    """Paginated data payload."""

    items: list[Any]
    page: int
    page_size: int
    total_items: int
    total_pages: int


class MessageResponse(BaseModel):
    """Simple message response."""

    success: bool = True
    message: str
    data: Any = None
