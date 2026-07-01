"""Subject schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.utils.validators import normalize_text


class SubjectBase(BaseModel):
    """Shared subject fields."""

    subject_code: str = Field(..., min_length=1, max_length=20)
    subject_name: str = Field(..., min_length=1, max_length=100)
    course: str = Field(..., min_length=1, max_length=100)
    department: str = Field(..., min_length=1, max_length=100)
    semester: int = Field(..., ge=1)
    credits: int = Field(..., ge=1)
    description: str | None = None
    is_active: bool = True

    @field_validator("subject_code")
    @classmethod
    def clean_subject_code(cls, value: str) -> str:
        return normalize_text(value).upper()

    @field_validator("subject_name", "course", "department", mode="before")
    @classmethod
    def clean_text(cls, value: str) -> str:
        return normalize_text(value)


class SubjectCreate(SubjectBase):
    """Create subject request."""


class SubjectUpdate(BaseModel):
    """Update subject request."""

    subject_name: str | None = Field(default=None, min_length=1, max_length=100)
    course: str | None = Field(default=None, min_length=1, max_length=100)
    department: str | None = Field(default=None, min_length=1, max_length=100)
    semester: int | None = Field(default=None, ge=1)
    credits: int | None = Field(default=None, ge=1)
    description: str | None = None
    is_active: bool | None = None


class SubjectResponse(BaseModel):
    """Subject response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    subject_code: str
    subject_name: str
    course: str
    department: str
    semester: int
    credits: int
    description: str | None = None
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None


class SubjectListResponse(BaseModel):
    """Paginated subject response."""

    items: list[SubjectResponse]
    page: int
    page_size: int
    total_items: int
    total_pages: int
