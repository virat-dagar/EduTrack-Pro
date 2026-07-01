"""Subject service."""

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.exceptions import ConflictError, NotFoundError
from app.models.subject import Subject
from app.schemas.subject import SubjectCreate, SubjectUpdate
from app.utils.helpers import apply_sorting, normalize_pagination, paginate_query


class SubjectService:
    """Business logic for academic subjects."""

    allowed_sort_fields = {"subject_name", "subject_code", "semester", "credits", "created_at", "id"}

    @staticmethod
    def get_subject(db: Session, subject_id: int) -> Subject:
        """Return a subject by ID."""

        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if subject is None:
            raise NotFoundError("Subject not found.")
        return subject

    @staticmethod
    def list_subjects(
        db: Session,
        page: int = 1,
        page_size: int = 20,
        q: str | None = None,
        course: str | None = None,
        department: str | None = None,
        semester: int | None = None,
        credits: int | None = None,
        is_active: bool | None = None,
        sort: str | None = "subject_name",
        order: str = "asc",
    ) -> tuple[list[Subject], int, int, int]:
        """Return filtered and paginated subjects."""

        safe_page, safe_page_size = normalize_pagination(page, page_size)
        query = db.query(Subject)
        if q:
            search = f"%{q.strip()}%"
            query = query.filter(
                or_(
                    Subject.subject_name.ilike(search),
                    Subject.subject_code.ilike(search),
                    Subject.department.ilike(search),
                    Subject.course.ilike(search),
                )
            )
        filters = {
            Subject.course: course,
            Subject.department: department,
            Subject.semester: semester,
            Subject.credits: credits,
        }
        for column, value in filters.items():
            if value not in (None, ""):
                query = query.filter(column == value)
        if is_active is not None:
            query = query.filter(Subject.is_active == is_active)
        query = apply_sorting(query, Subject, sort, order, SubjectService.allowed_sort_fields)
        items, total_items = paginate_query(query, safe_page, safe_page_size)
        return items, total_items, safe_page, safe_page_size

    @staticmethod
    def create_subject(db: Session, payload: SubjectCreate) -> Subject:
        """Create a subject."""

        if db.query(Subject).filter(Subject.subject_code == payload.subject_code).first():
            raise ConflictError("Subject code already exists.")
        subject = Subject(**payload.model_dump())
        db.add(subject)
        db.commit()
        db.refresh(subject)
        return subject

    @staticmethod
    def update_subject(db: Session, subject_id: int, payload: SubjectUpdate) -> Subject:
        """Update a subject."""

        subject = SubjectService.get_subject(db, subject_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(subject, field, value)
        db.commit()
        db.refresh(subject)
        return subject

    @staticmethod
    def delete_subject(db: Session, subject_id: int) -> None:
        """Delete a subject only when no dependent records exist."""

        subject = SubjectService.get_subject(db, subject_id)
        if subject.attendance_records or subject.marks_records or subject.assignments:
            raise ConflictError("Subject cannot be deleted while academic records exist.")
        db.delete(subject)
        db.commit()
