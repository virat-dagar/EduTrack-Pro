"""Attendance schemas."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.utils.constants import ATTENDANCE_STATUSES
from app.utils.validators import ensure_not_future


class AttendanceCreate(BaseModel):
    """Create attendance request."""

    student_id: int
    subject_id: int
    attendance_date: date
    status: str
    remarks: str | None = None

    @field_validator("attendance_date")
    @classmethod
    def validate_attendance_date(cls, value: date) -> date:
        ensure_not_future(value, "Attendance date")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in ATTENDANCE_STATUSES:
            raise ValueError("Attendance status must be Present, Absent, or Late.")
        return value


class AttendanceUpdate(BaseModel):
    """Update attendance request."""

    status: str | None = None
    remarks: str | None = None

    @field_validator("status")
    @classmethod
    def validate_optional_status(cls, value: str | None) -> str | None:
        if value is not None and value not in ATTENDANCE_STATUSES:
            raise ValueError("Attendance status must be Present, Absent, or Late.")
        return value


class AttendanceResponse(BaseModel):
    """Attendance response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    subject_id: int
    attendance_date: date
    status: str
    remarks: str | None = None
    marked_by: int
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AttendanceSummaryResponse(BaseModel):
    """Attendance summary response."""

    total_records: int
    present: int
    absent: int
    late: int


class AttendancePercentageResponse(BaseModel):
    """Attendance percentage response."""

    student_id: int
    attendance_percentage: float


class AttendanceListResponse(BaseModel):
    """Paginated attendance response."""

    items: list[AttendanceResponse]
    page: int
    page_size: int
    total_items: int
    total_pages: int
