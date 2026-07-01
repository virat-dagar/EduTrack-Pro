"""Assignment schemas."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class AssignmentCreate(BaseModel):
    """Create assignment request."""

    subject_id: int
    title: str = Field(..., min_length=1, max_length=150)
    description: str = Field(..., min_length=1)
    total_marks: float = Field(..., gt=0)
    assigned_date: date
    due_date: date

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: str) -> str:
        return value.strip()

    @model_validator(mode="after")
    def validate_dates(self) -> "AssignmentCreate":
        if self.due_date < self.assigned_date:
            raise ValueError("Due date must be greater than or equal to assigned date.")
        return self


class AssignmentUpdate(BaseModel):
    """Update assignment request."""

    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, min_length=1)
    total_marks: float | None = Field(default=None, gt=0)
    due_date: date | None = None
    is_active: bool | None = None


class AssignmentResponse(BaseModel):
    """Assignment response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    subject_id: int
    title: str
    description: str
    total_marks: float
    assigned_date: date
    due_date: date
    created_by: int
    is_active: bool
    subject: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AssignmentListResponse(BaseModel):
    """Paginated assignment response."""

    items: list[AssignmentResponse]
    page: int
    page_size: int
    total_items: int
    total_pages: int
