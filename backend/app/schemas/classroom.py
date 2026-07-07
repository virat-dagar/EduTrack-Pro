"""Classroom schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.utils.validators import normalize_text


class ClassroomBase(BaseModel):
    """Shared classroom fields."""

    classroom_code: str | None = Field(default=None, max_length=80)
    classroom_name: str | None = Field(default=None, max_length=150)
    department: str = Field(..., min_length=1, max_length=100)
    course: str = Field(..., min_length=1, max_length=100)
    semester: int = Field(..., ge=1)
    section: str = Field(..., min_length=1, max_length=10)
    academic_year: str = Field(..., min_length=4, max_length=20)
    is_active: bool = True

    @field_validator(
        "classroom_code",
        "classroom_name",
        "department",
        "course",
        "section",
        "academic_year",
        mode="before",
    )
    @classmethod
    def clean_text(cls, value: str | None) -> str | None:
        return normalize_text(value) if isinstance(value, str) else value


class ClassroomCreate(ClassroomBase):
    """Create classroom request."""


class ClassroomUpdate(BaseModel):
    """Update classroom request."""

    classroom_code: str | None = Field(default=None, max_length=80)
    classroom_name: str | None = Field(default=None, max_length=150)
    department: str | None = Field(default=None, min_length=1, max_length=100)
    course: str | None = Field(default=None, min_length=1, max_length=100)
    semester: int | None = Field(default=None, ge=1)
    section: str | None = Field(default=None, min_length=1, max_length=10)
    academic_year: str | None = Field(default=None, min_length=4, max_length=20)
    is_active: bool | None = None

    @field_validator(
        "classroom_code",
        "classroom_name",
        "department",
        "course",
        "section",
        "academic_year",
        mode="before",
    )
    @classmethod
    def clean_optional_text(cls, value: str | None) -> str | None:
        return normalize_text(value) if isinstance(value, str) else value


class ClassroomResponse(BaseModel):
    """Classroom response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    classroom_code: str
    classroom_name: str
    department: str
    course: str
    semester: int
    section: str
    academic_year: str
    is_active: bool
    student_count: int | None = None
    subject_count: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ClassroomListResponse(BaseModel):
    """Paginated classroom response."""

    items: list[ClassroomResponse]
    page: int
    page_size: int
    total_items: int
    total_pages: int
