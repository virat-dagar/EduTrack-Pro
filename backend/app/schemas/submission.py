"""Submission schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.utils.constants import SUBMISSION_REVIEWED, SUBMISSION_STATUSES


class SubmissionCreate(BaseModel):
    """Create submission request."""

    assignment_id: int
    submission_notes: str | None = None
    attachment_path: str | None = Field(default=None, max_length=255)


class SubmissionUpdate(BaseModel):
    """Update submission request."""

    submission_notes: str | None = None
    attachment_path: str | None = Field(default=None, max_length=255)


class SubmissionReview(BaseModel):
    """Review submission request."""

    status: str = SUBMISSION_REVIEWED
    feedback: str | None = None

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
    reviewed_by: int | None = None
    reviewed_at: datetime | None = None
    feedback: str | None = None
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
