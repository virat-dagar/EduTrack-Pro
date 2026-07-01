"""Academic analytics service."""

from collections import Counter

from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.models.marks import Marks
from app.models.student import Student
from app.models.submission import Submission
from app.utils.constants import ATTENDANCE_PRESENT, SUBMISSION_LATE, SUBMISSION_REVIEWED


class AnalyticsService:
    """Read-only academic calculations."""

    @staticmethod
    def percentage(numerator: float, denominator: float) -> float:
        """Return a rounded percentage."""

        if denominator <= 0:
            return 0.0
        return round((numerator / denominator) * 100, 2)

    @staticmethod
    def calculate_grade(percentage: float) -> str:
        """Calculate grade from percentage."""

        if percentage >= 90:
            return "A+"
        if percentage >= 80:
            return "A"
        if percentage >= 70:
            return "B+"
        if percentage >= 60:
            return "B"
        if percentage >= 50:
            return "C"
        if percentage >= 40:
            return "D"
        return "F"

    @staticmethod
    def performance_score(average_marks: float, attendance_percentage: float) -> float:
        """Calculate unified performance score."""

        return round((average_marks * 0.7) + (attendance_percentage * 0.3), 2)

    @staticmethod
    def attendance_percentage(db: Session, student_id: int | None = None) -> float:
        """Calculate attendance percentage."""

        query = db.query(Attendance)
        if student_id is not None:
            query = query.filter(Attendance.student_id == student_id)
        total = query.count()
        present = query.filter(Attendance.status == ATTENDANCE_PRESENT).count()
        return AnalyticsService.percentage(present, total)

    @staticmethod
    def average_marks(db: Session, student_id: int | None = None) -> float:
        """Calculate average marks percentage."""

        query = db.query(Marks)
        if student_id is not None:
            query = query.filter(Marks.student_id == student_id)
        records = query.all()
        total_obtained = sum(record.marks_obtained for record in records)
        total_maximum = sum(record.maximum_marks for record in records)
        return AnalyticsService.percentage(total_obtained, total_maximum)

    @staticmethod
    def risk_level(attendance_percentage: float, performance_score: float) -> str | None:
        """Return the academic risk level for a student."""

        if attendance_percentage < 70 and performance_score < 50:
            return "High"
        if attendance_percentage < 75 and performance_score < 65:
            return "Medium"
        if attendance_percentage < 80 or performance_score < 70:
            return "Low"
        return None

    @staticmethod
    def scholarship_status(
        attendance_percentage: float,
        average_marks: float,
        has_failed_subjects: bool,
        assignments_completed: bool,
    ) -> str:
        """Determine scholarship eligibility."""

        if (
            attendance_percentage >= 85
            and average_marks >= 80
            and not has_failed_subjects
            and assignments_completed
        ):
            return "Eligible"
        return "Not Eligible"

    @staticmethod
    def at_risk_students(db: Session) -> list[dict[str, object]]:
        """Return students with low, medium, or high risk."""

        results: list[dict[str, object]] = []
        for student in db.query(Student).filter(Student.is_active.is_(True)).all():
            attendance = AnalyticsService.attendance_percentage(db, student.id)
            marks = AnalyticsService.average_marks(db, student.id)
            score = AnalyticsService.performance_score(marks, attendance)
            level = AnalyticsService.risk_level(attendance, score)
            if level:
                results.append(
                    {
                        "student_id": student.id,
                        "name": f"{student.first_name} {student.last_name}",
                        "attendance_percentage": attendance,
                        "performance_score": score,
                        "risk_level": level,
                    }
                )
        return results

    @staticmethod
    def performance_distribution(db: Session) -> list[dict[str, object]]:
        """Return count of students by performance category."""

        buckets: Counter[str] = Counter()
        for student in db.query(Student).filter(Student.is_active.is_(True)).all():
            score = AnalyticsService.performance_score(
                AnalyticsService.average_marks(db, student.id),
                AnalyticsService.attendance_percentage(db, student.id),
            )
            if score >= 90:
                buckets["Excellent"] += 1
            elif score >= 80:
                buckets["Very Good"] += 1
            elif score >= 70:
                buckets["Good"] += 1
            elif score >= 60:
                buckets["Average"] += 1
            else:
                buckets["Needs Improvement"] += 1
        return [{"name": key, "value": value} for key, value in buckets.items()]

    @staticmethod
    def assignment_completion_percentage(db: Session) -> float:
        """Calculate reviewed/submitted assignment completion percentage."""

        total = db.query(Submission).count()
        completed = db.query(Submission).filter(Submission.status == SUBMISSION_REVIEWED).count()
        if completed == 0:
            completed = db.query(Submission).filter(Submission.status != SUBMISSION_LATE).count()
        return AnalyticsService.percentage(completed, total)
