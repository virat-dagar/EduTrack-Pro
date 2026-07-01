"""Attendance service."""

from datetime import date

from sqlalchemy.orm import Session

from app.exceptions import ConflictError, NotFoundError
from app.models.attendance import Attendance
from app.models.student import Student
from app.models.subject import Subject
from app.models.user import User
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate
from app.services.student_service import StudentService
from app.utils.constants import ATTENDANCE_ABSENT, ATTENDANCE_LATE, ATTENDANCE_PRESENT, ROLE_STUDENT
from app.utils.helpers import apply_sorting, normalize_pagination, paginate_query


class AttendanceService:
    """Business logic for attendance records."""

    allowed_sort_fields = {"attendance_date", "student_id", "subject_id", "status", "id"}

    @staticmethod
    def get_record(db: Session, attendance_id: int) -> Attendance:
        """Return one attendance record."""

        record = db.query(Attendance).filter(Attendance.id == attendance_id).first()
        if record is None:
            raise NotFoundError("Attendance record not found.")
        return record

    @staticmethod
    def list_records(
        db: Session,
        current_user: User,
        page: int = 1,
        page_size: int = 20,
        student_id: int | None = None,
        subject_id: int | None = None,
        semester: int | None = None,
        status: str | None = None,
        attendance_date: date | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        sort: str | None = "attendance_date",
        order: str = "desc",
    ) -> tuple[list[Attendance], int, int, int]:
        """Return filtered and paginated attendance records."""

        safe_page, safe_page_size = normalize_pagination(page, page_size)
        query = db.query(Attendance).join(Student)
        if current_user.role == ROLE_STUDENT:
            student = StudentService.get_student_by_user(db, current_user.id)
            query = query.filter(Attendance.student_id == student.id)
        if student_id:
            query = query.filter(Attendance.student_id == student_id)
        if subject_id:
            query = query.filter(Attendance.subject_id == subject_id)
        if semester:
            query = query.filter(Student.semester == semester)
        if status:
            query = query.filter(Attendance.status == status)
        if attendance_date:
            query = query.filter(Attendance.attendance_date == attendance_date)
        if start_date:
            query = query.filter(Attendance.attendance_date >= start_date)
        if end_date:
            query = query.filter(Attendance.attendance_date <= end_date)
        query = apply_sorting(query, Attendance, sort, order, AttendanceService.allowed_sort_fields)
        items, total_items = paginate_query(query, safe_page, safe_page_size)
        return items, total_items, safe_page, safe_page_size

    @staticmethod
    def mark_attendance(db: Session, payload: AttendanceCreate, teacher_id: int) -> Attendance:
        """Create an attendance record."""

        AttendanceService._validate_student_subject(db, payload.student_id, payload.subject_id)
        duplicate = (
            db.query(Attendance)
            .filter(
                Attendance.student_id == payload.student_id,
                Attendance.subject_id == payload.subject_id,
                Attendance.attendance_date == payload.attendance_date,
            )
            .first()
        )
        if duplicate:
            raise ConflictError("Attendance already marked for this student, subject, and date.")
        record = Attendance(**payload.model_dump(), marked_by=teacher_id)
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def update_attendance(db: Session, attendance_id: int, payload: AttendanceUpdate) -> Attendance:
        """Update attendance status and remarks."""

        record = AttendanceService.get_record(db, attendance_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(record, field, value)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def delete_attendance(db: Session, attendance_id: int) -> None:
        """Delete an attendance record."""

        record = AttendanceService.get_record(db, attendance_id)
        db.delete(record)
        db.commit()

    @staticmethod
    def percentage(db: Session, student_id: int) -> float:
        """Calculate attendance percentage for a student."""

        total = db.query(Attendance).filter(Attendance.student_id == student_id).count()
        present = (
            db.query(Attendance)
            .filter(Attendance.student_id == student_id, Attendance.status == ATTENDANCE_PRESENT)
            .count()
        )
        return round((present / total) * 100, 2) if total else 0.0

    @staticmethod
    def summary(db: Session) -> dict[str, int]:
        """Return attendance summary counts."""

        return {
            "total_records": db.query(Attendance).count(),
            "present": db.query(Attendance).filter(Attendance.status == ATTENDANCE_PRESENT).count(),
            "absent": db.query(Attendance).filter(Attendance.status == ATTENDANCE_ABSENT).count(),
            "late": db.query(Attendance).filter(Attendance.status == ATTENDANCE_LATE).count(),
        }

    @staticmethod
    def _validate_student_subject(db: Session, student_id: int, subject_id: int) -> None:
        """Validate attendance relationships."""

        if db.query(Student).filter(Student.id == student_id).first() is None:
            raise NotFoundError("Student not found.")
        if db.query(Subject).filter(Subject.id == subject_id).first() is None:
            raise NotFoundError("Subject not found.")
