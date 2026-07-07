"""Assignment schemas."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class AssignmentQuestionCreate(BaseModel):
    """Create assignment question request."""

    question_no: int = Field(..., ge=1)
    title: str | None = Field(default=None, max_length=150)
    description: str | None = None
    max_marks: float = Field(..., gt=0)


class AssignmentQuestionResponse(BaseModel):
    """Assignment question response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    assignment_id: int
    question_no: int
    title: str | None = None
    description: str | None = None
    max_marks: float


class AssignmentCreate(BaseModel):
    """Create assignment request."""

    subject_id: int
    classroom_id: int | None = None
    title: str = Field(..., min_length=1, max_length=150)
    description: str = Field(..., min_length=1)
    pdf_file: str | None = Field(default=None, max_length=255)
    total_marks: float | None = Field(default=None, gt=0)
    assigned_date: date
    due_date: date
    is_published: bool = True
    questions: list[AssignmentQuestionCreate] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: str) -> str:
        return value.strip()

    @model_validator(mode="after")
    def validate_dates(self) -> "AssignmentCreate":
        if self.due_date < self.assigned_date:
            raise ValueError("Due date must be greater than or equal to assigned date.")
        if self.total_marks is None and not self.questions:
            raise ValueError("Total marks or at least one question is required.")
        return self


class AssignmentUpdate(BaseModel):
    """Update assignment request."""

    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, min_length=1)
    classroom_id: int | None = None
    pdf_file: str | None = Field(default=None, max_length=255)
    total_marks: float | None = Field(default=None, gt=0)
    due_date: date | None = None
    is_published: bool | None = None
    is_active: bool | None = None
    questions: list[AssignmentQuestionCreate] | None = None


class AssignmentResponse(BaseModel):
    """Assignment response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    classroom_id: int | None = None
    subject_id: int
    title: str
    description: str
    pdf_file: str | None = None
    total_marks: float
    assigned_date: date
    due_date: date
    created_by: int
    is_published: bool
    published_at: datetime | None = None
    is_active: bool
    subject: str | None = None
    classroom: str | None = None
    questions: list[AssignmentQuestionResponse] = Field(default_factory=list)
    my_submission_id: int | None = None
    submission_status: str | None = None
    submission_file: str | None = None
    submission_grade: str | None = None
    submission_percentage: float | None = None
    submission_feedback: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AssignmentListResponse(BaseModel):
    """Paginated assignment response."""

    items: list[AssignmentResponse]
    page: int
    page_size: int
    total_items: int
    total_pages: int
