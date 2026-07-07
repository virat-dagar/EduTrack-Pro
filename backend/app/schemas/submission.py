"""Submission schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.utils.constants import SUBMISSION_REVIEWED, SUBMISSION_STATUSES


class SubmissionCreate(BaseModel):
    """Create submission request."""

    assignment_id: int
    submission_notes: str | None = None
    attachment_path: str | None = Field(default=None, max_length=255)
    submitted_file: str | None = Field(default=None, max_length=255)

    @model_validator(mode="after")
    def require_submission_file(self) -> "SubmissionCreate":
        """Require a file reference for assignment submissions."""

        if not self.attachment_path and not self.submitted_file:
            raise ValueError("submitted_file or attachment_path is required.")
        return self


class SubmissionUpdate(BaseModel):
    """Update submission request."""

    submission_notes: str | None = None
    attachment_path: str | None = Field(default=None, max_length=255)
    submitted_file: str | None = Field(default=None, max_length=255)


class SubmissionQuestionScore(BaseModel):
    """Question-wise score for submission review."""

    question_id: int
    obtained_marks: float = Field(..., ge=0)
    feedback: str | None = None


class SubmissionReview(BaseModel):
    """Review submission request."""

    status: str = SUBMISSION_REVIEWED
    feedback: str | None = None
    question_scores: list[SubmissionQuestionScore] = Field(default_factory=list)

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in SUBMISSION_STATUSES:
            raise ValueError("Submission status is not supported.")
        return value


class SubmissionResponse(BaseModel):
    """Submission response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    assignment_id: int
    student_id: int
    submission_date: datetime
    status: str
    submission_notes: str | None = None
    attachment_path: str | None = None
    submitted_file: str | None = None
    reviewed_by: int | None = None
    reviewed_at: datetime | None = None
    feedback: str | None = None
    total_marks: float | None = None
    percentage: float | None = None
    grade: str | None = None
    question_grades: list[dict[str, object]] = Field(default_factory=list)
    reviewed: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class SubmissionListResponse(BaseModel):
    """Paginated submission response."""

    items: list[SubmissionResponse]
    page: int
    page_size: int
    total_items: int
    total_pages: int
