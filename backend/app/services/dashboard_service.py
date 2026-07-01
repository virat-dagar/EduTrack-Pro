"""Dashboard aggregation service."""

from collections import Counter, defaultdict
from datetime import date

from sqlalchemy.orm import Session

from app.models.assignment import Assignment
from app.models.attendance import Attendance
from app.models.marks import Marks
from app.models.student import Student
from app.models.subject import Subject
from app.models.submission import Submission
from app.models.user import User
from app.services.analytics_service import AnalyticsService
from app.services.assignment_service import AssignmentService
from app.services.student_service import StudentService
from app.utils.constants import ATTENDANCE_PRESENT, SUBMISSION_REVIEWED


class DashboardService:
    """Aggregated dashboard data."""

    @staticmethod
    def teacher_dashboard(db: Session) -> dict[str, object]:
        """Return teacher dashboard summary cards."""

        today_records = db.query(Attendance).filter(Attendance.attendance_date == date.today()).count()
        return {
            "total_students": db.query(Student).filter(Student.is_active.is_(True)).count(),
            "total_subjects": db.query(Subject).filter(Subject.is_active.is_(True)).count(),
            "attendance_today": today_records,
            "attendance_percentage": AnalyticsService.attendance_percentage(db),
            "average_marks": AnalyticsService.average_marks(db),
            "assignments": db.query(Assignment).filter(Assignment.is_active.is_(True)).count(),
            "pending_reviews": db.query(Submission).filter(Submission.reviewed_by.is_(None)).count(),
            "at_risk_students": len(AnalyticsService.at_risk_students(db)),
        }

    @staticmethod
    def teacher_charts(db: Session) -> dict[str, list[dict[str, object]]]:
        """Return teacher chart data."""

        attendance_by_date: defaultdict[str, list[Attendance]] = defaultdict(list)
        for record in db.query(Attendance).order_by(Attendance.attendance_date.asc()).all():
            attendance_by_date[record.attendance_date.isoformat()].append(record)
        attendance_trend = [
            {
                "date": day,
                "percentage": AnalyticsService.percentage(
                    sum(1 for item in records if item.status == ATTENDANCE_PRESENT),
                    len(records),
                ),
            }
            for day, records in attendance_by_date.items()
        ]

        marks_by_date: defaultdict[str, list[Marks]] = defaultdict(list)
        for record in db.query(Marks).order_by(Marks.examination_date.asc()).all():
            marks_by_date[record.examination_date.isoformat()].append(record)
        marks_trend = [
            {
                "date": day,
                "average": AnalyticsService.percentage(
                    sum(item.marks_obtained for item in records),
                    sum(item.maximum_marks for item in records),
                ),
            }
            for day, records in marks_by_date.items()
        ]

        semester_distribution = [
            {"name": str(semester), "value": count}
            for semester, count in Counter(
                student.semester for student in db.query(Student).all()
            ).items()
        ]

        assignment_total = db.query(Submission).count()
        reviewed = db.query(Submission).filter(Submission.status == SUBMISSION_REVIEWED).count()
        assignment_completion = [
            {"name": "Reviewed", "value": reviewed},
            {"name": "Pending", "value": max(assignment_total - reviewed, 0)},
        ]
        at_risk = AnalyticsService.at_risk_students(db)
        risk_distribution = [
            {"name": level, "value": count}
            for level, count in Counter(item["risk_level"] for item in at_risk).items()
        ]
        return {
            "attendance_trend": attendance_trend,
            "marks_trend": marks_trend,
            "semester_distribution": semester_distribution,
            "assignment_completion": assignment_completion,
            "at_risk_distribution": risk_distribution,
        }

    @staticmethod
    def teacher_activity(db: Session, limit: int = 20) -> list[dict[str, object]]:
        """Return recent teacher-facing activity."""

        activities: list[dict[str, object]] = []
        for student in db.query(Student).order_by(Student.created_at.desc()).limit(limit).all():
            activities.append(
                {
                    "type": "Student Added",
                    "message": f"{student.first_name} {student.last_name} was added.",
                    "timestamp": student.created_at,
                }
            )
        for assignment in db.query(Assignment).order_by(Assignment.created_at.desc()).limit(limit).all():
            activities.append(
                {
                    "type": "Assignment Created",
                    "message": assignment.title,
                    "timestamp": assignment.created_at,
                }
            )
        for submission in db.query(Submission).order_by(Submission.updated_at.desc()).limit(limit).all():
            activities.append(
                {
                    "type": "Submission Reviewed" if submission.reviewed_by else "Assignment Submitted",
                    "message": f"Submission #{submission.id}",
                    "timestamp": submission.updated_at,
                }
            )
        return sorted(activities, key=lambda item: item["timestamp"], reverse=True)[:limit]

    @staticmethod
    def student_dashboard(db: Session, current_user: User) -> dict[str, object]:
        """Return student dashboard summary."""

        student = StudentService.get_student_by_user(db, current_user.id)
        attendance = AnalyticsService.attendance_percentage(db, student.id)
        average_marks = AnalyticsService.average_marks(db, student.id)
        score = AnalyticsService.performance_score(average_marks, attendance)
        assignments = AssignmentService.list_assignments(db, current_user, page_size=100)[0]
        submitted_ids = {
            submission.assignment_id
            for submission in db.query(Submission).filter(Submission.student_id == student.id).all()
        }
        pending_assignments = [item for item in assignments if item.id not in submitted_ids]
        has_failed = (
            db.query(Marks)
            .filter(Marks.student_id == student.id)
            .all()
        )
        failed = any(
            AnalyticsService.percentage(record.marks_obtained, record.maximum_marks) < 40
            for record in has_failed
        )
        scholarship = AnalyticsService.scholarship_status(
            attendance,
            average_marks,
            failed,
            len(pending_assignments) == 0,
        )
        return {
            "attendance_percentage": attendance,
            "average_marks": average_marks,
            "grade": AnalyticsService.calculate_grade(average_marks),
            "pending_assignments": len(pending_assignments),
            "submitted_assignments": len(submitted_ids),
            "subjects": db.query(Subject)
            .filter(
                Subject.course == student.course,
                Subject.department == student.department,
                Subject.semester == student.semester,
                Subject.is_active.is_(True),
            )
            .count(),
            "performance_score": score,
            "scholarship_status": scholarship,
        }

    @staticmethod
    def student_charts(db: Session, current_user: User) -> dict[str, list[dict[str, object]]]:
        """Return student chart data."""

        student = StudentService.get_student_by_user(db, current_user.id)
        marks_by_subject: defaultdict[str, list[Marks]] = defaultdict(list)
        for record in db.query(Marks).filter(Marks.student_id == student.id).all():
            subject_name = record.subject.subject_name if record.subject else str(record.subject_id)
            marks_by_subject[subject_name].append(record)
        subject_marks = [
            {
                "subject": subject,
                "average": AnalyticsService.percentage(
                    sum(item.marks_obtained for item in records),
                    sum(item.maximum_marks for item in records),
                ),
            }
            for subject, records in marks_by_subject.items()
        ]
        attendance_trend = [
            {"date": record.attendance_date.isoformat(), "status": record.status}
            for record in db.query(Attendance)
            .filter(Attendance.student_id == student.id)
            .order_by(Attendance.attendance_date.asc())
            .all()
        ]
        submissions = db.query(Submission).filter(Submission.student_id == student.id).all()
        assignment_progress = [
            {"name": "Submitted", "value": len(submissions)},
            {
                "name": "Reviewed",
                "value": sum(1 for submission in submissions if submission.reviewed_by),
            },
        ]
        return {
            "marks_by_subject": subject_marks,
            "attendance_trend": attendance_trend,
            "performance_trend": subject_marks,
            "assignment_progress": assignment_progress,
        }

    @staticmethod
    def student_activity(db: Session, current_user: User, limit: int = 20) -> list[dict[str, object]]:
        """Return recent student activity."""

        student = StudentService.get_student_by_user(db, current_user.id)
        activities: list[dict[str, object]] = []
        for submission in (
            db.query(Submission)
            .filter(Submission.student_id == student.id)
            .order_by(Submission.updated_at.desc())
            .limit(limit)
            .all()
        ):
            activities.append(
                {
                    "type": "Feedback Received" if submission.feedback else "Assignment Submitted",
                    "message": f"Assignment #{submission.assignment_id}",
                    "timestamp": submission.updated_at,
                }
            )
        for record in (
            db.query(Marks)
            .filter(Marks.student_id == student.id)
            .order_by(Marks.created_at.desc())
            .limit(limit)
            .all()
        ):
            activities.append(
                {
                    "type": "Marks Published",
                    "message": record.assessment_type,
                    "timestamp": record.created_at,
                }
            )
        return sorted(activities, key=lambda item: item["timestamp"], reverse=True)[:limit]
