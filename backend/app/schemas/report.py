"""Report response schemas."""

from typing import Any

from pydantic import BaseModel


class StudentReportResponse(BaseModel):
    """Student academic report."""

    student: dict[str, Any]
    attendance_percentage: float
    average_marks: float
    grade: str
    pending_assignments: int
    performance_score: float
    scholarship_status: str


class AttendanceReportResponse(BaseModel):
    """Attendance report."""

    total_students: int
    average_attendance: float
    present: int
    absent: int
    late: int = 0


class MarksReportResponse(BaseModel):
    """Marks report."""

    average_marks: float
    highest_marks: float
    lowest_marks: float
    pass_percentage: float


class AssignmentReportResponse(BaseModel):
    """Assignment report."""

    total_assignments: int
    submitted: int
    pending: int
    late_submissions: int


class PerformanceReportResponse(BaseModel):
    """Performance report."""

    average_performance: float
    top_performers: list[dict[str, Any]]
    at_risk_students: list[dict[str, Any]]
    performance_distribution: list[dict[str, Any]]


class InstitutionReportResponse(BaseModel):
    """Institution report."""

    students: int
    subjects: int
    attendance_percentage: float
    average_marks: float
    assignment_completion: float
