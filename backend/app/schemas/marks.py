"""Marks schemas."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.utils.constants import ASSESSMENT_TYPES
from app.utils.validators import ensure_not_future


class MarksCreate(BaseModel):
    """Create marks request."""

    student_id: int
    subject_id: int
    assessment_type: str
    marks_obtained: float = Field(..., ge=0)
    maximum_marks: float = Field(..., gt=0)
    examination_date: date
    remarks: str | None = None

    @field_validator("assessment_type")
    @classmethod
    def validate_assessment_type(cls, value: str) -> str:
        if value not in ASSESSMENT_TYPES:
            raise ValueError("Assessment type is not supported.")
        return value

    @field_validator("examination_date")
    @classmethod
    def validate_examination_date(cls, value: date) -> date:
        ensure_not_future(value, "Examination date")
        return value

    @model_validator(mode="after")
    def validate_marks_range(self) -> "MarksCreate":
        if self.marks_obtained > self.maximum_marks:
            raise ValueError("Marks obtained cannot exceed maximum marks.")
        return self


class MarksUpdate(BaseModel):
    """Update marks request."""

    marks_obtained: float | None = Field(default=None, ge=0)
    maximum_marks: float | None = Field(default=None, gt=0)
    remarks: str | None = None

    @model_validator(mode="after")
    def validate_optional_marks_range(self) -> "MarksUpdate":
        if (
            self.marks_obtained is not None
            and self.maximum_marks is not None
            and self.marks_obtained > self.maximum_marks
        ):
            raise ValueError("Marks obtained cannot exceed maximum marks.")
        return self


class MarksResponse(BaseModel):
    """Marks response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    subject_id: int
    assessment_type: str
    marks_obtained: float
    maximum_marks: float
    examination_date: date
    remarks: str | None = None
    entered_by: int
    percentage: float | None = None
    grade: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class MarksSummaryResponse(BaseModel):
    """Marks summary response."""

    average_percentage: float
    highest_marks: float
    lowest_marks: float
    total_records: int


class MarksAverageResponse(BaseModel):
    """Student average marks response."""

    student_id: int
    average_percentage: float
    grade: str
    subjects_completed: int


class MarksListResponse(BaseModel):
    """Paginated marks response."""

    items: list[MarksResponse]
    page: int
    page_size: int
    total_items: int
    total_pages: int
