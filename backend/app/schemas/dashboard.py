"""Dashboard response schemas."""

from typing import Any

from pydantic import BaseModel


class TeacherDashboardResponse(BaseModel):
    """Teacher dashboard summary."""

    total_students: int
    total_subjects: int
    attendance_today: int
    attendance_percentage: float
    average_marks: float
    assignments: int
    pending_reviews: int
    at_risk_students: int


class StudentDashboardResponse(BaseModel):
    """Student dashboard summary."""

    attendance_percentage: float
    average_marks: float
    grade: str
    pending_assignments: int
    submitted_assignments: int
    subjects: int
    performance_score: float
    scholarship_status: str | None = None


class ChartResponse(BaseModel):
    """Chart response payload."""

    data: dict[str, list[dict[str, Any]]]


class ActivityResponse(BaseModel):
    """Activity feed response."""

    items: list[dict[str, Any]]
