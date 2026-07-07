"""Model package exports."""

from app.models.assignment import Assignment
from app.models.assignment_question import AssignmentQuestion
from app.models.attendance import Attendance
from app.models.classroom import Classroom
from app.models.marks import Marks
from app.models.student import Student
from app.models.subject import Subject
from app.models.submission import Submission
from app.models.submission_grade import SubmissionGrade
from app.models.user import User

__all__ = [
    "Assignment",
    "AssignmentQuestion",
    "Attendance",
    "Classroom",
    "Marks",
    "Student",
    "Subject",
    "Submission",
    "SubmissionGrade",
    "User",
]
