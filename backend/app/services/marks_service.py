"""Marks service."""

from datetime import date

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.exceptions import ConflictError, NotFoundError
from app.models.marks import Marks
from app.models.student import Student
from app.models.subject import Subject
from app.models.user import User
from app.schemas.marks import MarksCreate, MarksUpdate
from app.services.analytics_service import AnalyticsService
from app.services.student_service import StudentService
from app.utils.constants import ROLE_STUDENT
from app.utils.helpers import apply_sorting, normalize_pagination, paginate_query


class MarksService:
    """Business logic for marks records."""

    allowed_sort_fields = {"examination_date", "student_id", "subject_id", "assessment_type", "id"}

    @staticmethod
    def get_record(db: Session, marks_id: int) -> Marks:
        """Return one marks record."""

        record = db.query(Marks).filter(Marks.id == marks_id).first()
        if record is None:
            raise NotFoundError("Marks record not found.")
        return record

    @staticmethod
    def list_records(
        db: Session,
        current_user: User,
        page: int = 1,
        page_size: int = 20,
        q: str | None = None,
        student_id: int | None = None,
        subject_id: int | None = None,
        assessment_type: str | None = None,
        semester: int | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        sort: str | None = "examination_date",
        order: str = "desc",
    ) -> tuple[list[Marks], int, int, int]:
        """Return filtered and paginated marks records."""

        safe_page, safe_page_size = normalize_pagination(page, page_size)
        query = db.query(Marks).join(Student).join(Subject)
        if current_user.role == ROLE_STUDENT:
            student = StudentService.get_student_by_user(db, current_user.id)
            query = query.filter(Marks.student_id == student.id)
        if q:
            search = f"%{q.strip()}%"
            query = query.filter(
                or_(
                    Student.first_name.ilike(search),
                    Student.last_name.ilike(search),
                    Subject.subject_name.ilike(search),
                    Subject.subject_code.ilike(search),
                )
            )
        if student_id:
            query = query.filter(Marks.student_id == student_id)
        if subject_id:
            query = query.filter(Marks.subject_id == subject_id)
        if assessment_type:
            query = query.filter(Marks.assessment_type == assessment_type)
        if semester:
            query = query.filter(Student.semester == semester)
        if start_date:
            query = query.filter(Marks.examination_date >= start_date)
        if end_date:
            query = query.filter(Marks.examination_date <= end_date)
        query = apply_sorting(query, Marks, sort, order, MarksService.allowed_sort_fields)
        items, total_items = paginate_query(query, safe_page, safe_page_size)
        return items, total_items, safe_page, safe_page_size

    @staticmethod
    def add_marks(db: Session, payload: MarksCreate, teacher_id: int) -> Marks:
        """Create a marks record."""

        MarksService._validate_student_subject(db, payload.student_id, payload.subject_id)
        duplicate = (
            db.query(Marks)
            .filter(
                Marks.student_id == payload.student_id,
                Marks.subject_id == payload.subject_id,
                Marks.assessment_type == payload.assessment_type,
                Marks.examination_date == payload.examination_date,
            )
            .first()
        )
        if duplicate:
            raise ConflictError("Marks already exist for this assessment.")
        record = Marks(**payload.model_dump(), entered_by=teacher_id)
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def update_marks(db: Session, marks_id: int, payload: MarksUpdate) -> Marks:
        """Update marks values."""

        record = MarksService.get_record(db, marks_id)
        data = payload.model_dump(exclude_unset=True)
        new_obtained = data.get("marks_obtained", record.marks_obtained)
        new_maximum = data.get("maximum_marks", record.maximum_marks)
        if new_obtained > new_maximum:
            raise ConflictError("Marks obtained cannot exceed maximum marks.")
        for field, value in data.items():
            setattr(record, field, value)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def delete_marks(db: Session, marks_id: int) -> None:
        """Delete marks."""

        record = MarksService.get_record(db, marks_id)
        db.delete(record)
        db.commit()

    @staticmethod
    def average(db: Session, student_id: int) -> dict[str, object]:
        """Return average marks for a student."""

        records = db.query(Marks).filter(Marks.student_id == student_id).all()
        total_obtained = sum(record.marks_obtained for record in records)
        total_maximum = sum(record.maximum_marks for record in records)
        average_percentage = AnalyticsService.percentage(total_obtained, total_maximum)
        return {
            "student_id": student_id,
            "average_percentage": average_percentage,
            "grade": AnalyticsService.calculate_grade(average_percentage),
            "subjects_completed": len({record.subject_id for record in records}),
        }

    @staticmethod
    def summary(db: Session) -> dict[str, float | int]:
        """Return marks statistics."""

        records = db.query(Marks).all()
        if not records:
            return {
                "average_percentage": 0.0,
                "highest_marks": 0.0,
                "lowest_marks": 0.0,
                "total_records": 0,
            }
        percentages = [
            AnalyticsService.percentage(record.marks_obtained, record.maximum_marks)
            for record in records
        ]
        return {
            "average_percentage": round(sum(percentages) / len(percentages), 2),
            "highest_marks": max(record.marks_obtained for record in records),
            "lowest_marks": min(record.marks_obtained for record in records),
            "total_records": len(records),
        }

    @staticmethod
    def enrich(record: Marks) -> dict[str, object]:
        """Return marks data with calculated percentage and grade."""

        percentage = AnalyticsService.percentage(record.marks_obtained, record.maximum_marks)
        return {
            "id": record.id,
            "student_id": record.student_id,
            "subject_id": record.subject_id,
            "assessment_type": record.assessment_type,
            "marks_obtained": record.marks_obtained,
            "maximum_marks": record.maximum_marks,
            "examination_date": record.examination_date,
            "remarks": record.remarks,
            "entered_by": record.entered_by,
            "percentage": percentage,
            "grade": AnalyticsService.calculate_grade(percentage),
            "created_at": record.created_at,
            "updated_at": record.updated_at,
        }

    @staticmethod
    def _validate_student_subject(db: Session, student_id: int, subject_id: int) -> None:
        """Validate marks relationships."""

        if db.query(Student).filter(Student.id == student_id).first() is None:
            raise NotFoundError("Student not found.")
        if db.query(Subject).filter(Subject.id == subject_id).first() is None:
            raise NotFoundError("Subject not found.")
