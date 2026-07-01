"""Model package exports."""

from app.models.assignment import Assignment
from app.models.attendance import Attendance
from app.models.marks import Marks
from app.models.student import Student
from app.models.subject import Subject
from app.models.submission import Submission
from app.models.user import User

__all__ = [
    "Assignment",
    "Attendance",
    "Marks",
    "Student",
    "Subject",
    "Submission",
    "User",
]
