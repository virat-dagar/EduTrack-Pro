"""Report service."""

from sqlalchemy.orm import Session

from app.exceptions import AuthorizationError
from app.models.assignment import Assignment
from app.models.attendance import Attendance
from app.models.marks import Marks
from app.models.student import Student
from app.models.submission import Submission
from app.models.subject import Subject
from app.models.user import User
from app.services.analytics_service import AnalyticsService
from app.services.assignment_service import AssignmentService
from app.services.student_service import StudentService
from app.utils.constants import ATTENDANCE_ABSENT, ATTENDANCE_LATE, ATTENDANCE_PRESENT, ROLE_STUDENT, SUBMISSION_LATE


class ReportService:
    """Read-only academic report generation."""

    @staticmethod
    def student_report(db: Session, student_id: int, current_user: User) -> dict[str, object]:
        """Generate a student academic report."""

        student = StudentService.get_student(db, student_id)
        if current_user.role == ROLE_STUDENT and student.user_id != current_user.id:
            raise AuthorizationError("Students may only generate their own report.")
        attendance = AnalyticsService.attendance_percentage(db, student.id)
        average_marks = AnalyticsService.average_marks(db, student.id)
        score = AnalyticsService.performance_score(average_marks, attendance)
        assignments = AssignmentService.list_assignments(db, current_user, page_size=100)[0]
        submitted_ids = {
            submission.assignment_id
            for submission in db.query(Submission).filter(Submission.student_id == student.id).all()
        }
        pending_assignments = len([assignment for assignment in assignments if assignment.id not in submitted_ids])
        failed = any(
            AnalyticsService.percentage(record.marks_obtained, record.maximum_marks) < 40
            for record in db.query(Marks).filter(Marks.student_id == student.id).all()
        )
        return {
            "student": {
                "id": student.id,
                "name": f"{student.first_name} {student.last_name}",
                "roll_number": student.roll_number,
            },
            "attendance_percentage": attendance,
            "average_marks": average_marks,
            "grade": AnalyticsService.calculate_grade(average_marks),
            "pending_assignments": pending_assignments,
            "performance_score": score,
            "scholarship_status": AnalyticsService.scholarship_status(
                attendance,
                average_marks,
                failed,
                pending_assignments == 0,
            ),
        }

    @staticmethod
    def attendance_report(db: Session) -> dict[str, object]:
        """Generate attendance report."""

        total_records = db.query(Attendance).count()
        present = db.query(Attendance).filter(Attendance.status == ATTENDANCE_PRESENT).count()
        absent = db.query(Attendance).filter(Attendance.status == ATTENDANCE_ABSENT).count()
        late = db.query(Attendance).filter(Attendance.status == ATTENDANCE_LATE).count()
        return {
            "total_students": db.query(Student).filter(Student.is_active.is_(True)).count(),
            "average_attendance": AnalyticsService.percentage(present, total_records),
            "present": present,
            "absent": absent,
            "late": late,
        }

    @staticmethod
    def marks_report(db: Session) -> dict[str, object]:
        """Generate marks report."""

        records = db.query(Marks).all()
        if not records:
            return {
                "average_marks": 0.0,
                "highest_marks": 0.0,
                "lowest_marks": 0.0,
                "pass_percentage": 0.0,
            }
        percentages = [
            AnalyticsService.percentage(record.marks_obtained, record.maximum_marks)
            for record in records
        ]
        return {
            "average_marks": round(sum(percentages) / len(percentages), 2),
            "highest_marks": max(record.marks_obtained for record in records),
            "lowest_marks": min(record.marks_obtained for record in records),
            "pass_percentage": AnalyticsService.percentage(
                sum(1 for percentage in percentages if percentage >= 40),
                len(percentages),
            ),
        }

    @staticmethod
    def assignment_report(db: Session) -> dict[str, object]:
        """Generate assignment completion report."""

        total_assignments = db.query(Assignment).count()
        submitted = db.query(Submission).count()
        late_submissions = db.query(Submission).filter(Submission.status == SUBMISSION_LATE).count()
        expected = total_assignments * max(db.query(Student).filter(Student.is_active.is_(True)).count(), 1)
        return {
            "total_assignments": total_assignments,
            "submitted": submitted,
            "pending": max(expected - submitted, 0),
            "late_submissions": late_submissions,
        }

    @staticmethod
    def performance_report(db: Session) -> dict[str, object]:
        """Generate performance report."""

        students = db.query(Student).filter(Student.is_active.is_(True)).all()
        scores = [
            {
                "student_id": student.id,
                "name": f"{student.first_name} {student.last_name}",
                "performance_score": AnalyticsService.performance_score(
                    AnalyticsService.average_marks(db, student.id),
                    AnalyticsService.attendance_percentage(db, student.id),
                ),
            }
            for student in students
        ]
        average = round(
            sum(item["performance_score"] for item in scores) / len(scores),
            2,
        ) if scores else 0.0
        return {
            "average_performance": average,
            "top_performers": sorted(scores, key=lambda item: item["performance_score"], reverse=True)[:5],
            "at_risk_students": AnalyticsService.at_risk_students(db),
            "performance_distribution": AnalyticsService.performance_distribution(db),
        }

    @staticmethod
    def institution_report(db: Session) -> dict[str, object]:
        """Generate institution-wide summary."""

        return {
            "students": db.query(Student).filter(Student.is_active.is_(True)).count(),
            "subjects": db.query(Subject).filter(Subject.is_active.is_(True)).count(),
            "attendance_percentage": AnalyticsService.attendance_percentage(db),
            "average_marks": AnalyticsService.average_marks(db),
            "assignment_completion": AnalyticsService.assignment_completion_percentage(db),
        }
