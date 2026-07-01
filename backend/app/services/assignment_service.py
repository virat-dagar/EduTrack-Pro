"""Assignment service."""

from datetime import date

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.exceptions import ConflictError, NotFoundError
from app.models.assignment import Assignment
from app.models.subject import Subject
from app.models.user import User
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate
from app.services.student_service import StudentService
from app.utils.constants import ROLE_STUDENT
from app.utils.helpers import apply_sorting, normalize_pagination, paginate_query


class AssignmentService:
    """Business logic for assignments."""

    allowed_sort_fields = {"due_date", "assigned_date", "title", "id"}

    @staticmethod
    def get_assignment(db: Session, assignment_id: int) -> Assignment:
        """Return an assignment."""

        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if assignment is None:
            raise NotFoundError("Assignment not found.")
        return assignment

    @staticmethod
    def list_assignments(
        db: Session,
        current_user: User,
        page: int = 1,
        page_size: int = 20,
        q: str | None = None,
        subject_id: int | None = None,
        teacher_id: int | None = None,
        semester: int | None = None,
        course: str | None = None,
        department: str | None = None,
        is_active: bool | None = None,
        sort: str | None = "due_date",
        order: str = "asc",
    ) -> tuple[list[Assignment], int, int, int]:
        """Return filtered and paginated assignments."""

        safe_page, safe_page_size = normalize_pagination(page, page_size)
        query = db.query(Assignment).join(Subject)
        if current_user.role == ROLE_STUDENT:
            student = StudentService.get_student_by_user(db, current_user.id)
            query = query.filter(
                Assignment.is_active.is_(True),
                Subject.course == student.course,
                Subject.department == student.department,
                Subject.semester == student.semester,
            )
        if q:
            search = f"%{q.strip()}%"
            query = query.filter(or_(Assignment.title.ilike(search), Subject.subject_name.ilike(search)))
        filters = {
            Assignment.subject_id: subject_id,
            Assignment.created_by: teacher_id,
            Subject.semester: semester,
            Subject.course: course,
            Subject.department: department,
        }
        for column, value in filters.items():
            if value not in (None, ""):
                query = query.filter(column == value)
        if is_active is not None:
            query = query.filter(Assignment.is_active == is_active)
        query = apply_sorting(query, Assignment, sort, order, AssignmentService.allowed_sort_fields)
        items, total_items = paginate_query(query, safe_page, safe_page_size)
        return items, total_items, safe_page, safe_page_size

    @staticmethod
    def create_assignment(db: Session, payload: AssignmentCreate, teacher_id: int) -> Assignment:
        """Create an assignment."""

        if db.query(Subject).filter(Subject.id == payload.subject_id).first() is None:
            raise NotFoundError("Subject not found.")
        assignment = Assignment(**payload.model_dump(), created_by=teacher_id)
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        return assignment

    @staticmethod
    def update_assignment(db: Session, assignment_id: int, payload: AssignmentUpdate) -> Assignment:
        """Update an assignment."""

        assignment = AssignmentService.get_assignment(db, assignment_id)
        data = payload.model_dump(exclude_unset=True)
        if "due_date" in data and data["due_date"] < assignment.assigned_date:
            raise ConflictError("Due date must be greater than or equal to assigned date.")
        for field, value in data.items():
            setattr(assignment, field, value)
        db.commit()
        db.refresh(assignment)
        return assignment

    @staticmethod
    def delete_assignment(db: Session, assignment_id: int) -> None:
        """Delete an assignment only when it has no submissions."""

        assignment = AssignmentService.get_assignment(db, assignment_id)
        if assignment.submissions:
            raise ConflictError("Assignment cannot be deleted while submissions exist.")
        db.delete(assignment)
        db.commit()

    @staticmethod
    def upcoming(db: Session, current_user: User) -> list[Assignment]:
        """Return upcoming assignments."""

        query = db.query(Assignment).filter(Assignment.due_date >= date.today())
        if current_user.role == ROLE_STUDENT:
            student = StudentService.get_student_by_user(db, current_user.id)
            query = query.join(Subject).filter(
                Assignment.is_active.is_(True),
                Subject.course == student.course,
                Subject.department == student.department,
                Subject.semester == student.semester,
            )
        return query.order_by(Assignment.due_date.asc()).all()

    @staticmethod
    def overdue(db: Session) -> list[Assignment]:
        """Return overdue active assignments."""

        return (
            db.query(Assignment)
            .filter(Assignment.due_date < date.today(), Assignment.is_active.is_(True))
            .order_by(Assignment.due_date.asc())
            .all()
        )

    @staticmethod
    def enrich(assignment: Assignment) -> dict[str, object]:
        """Return assignment data with subject name."""

        return {
            "id": assignment.id,
            "subject_id": assignment.subject_id,
            "title": assignment.title,
            "description": assignment.description,
            "total_marks": assignment.total_marks,
            "assigned_date": assignment.assigned_date,
            "due_date": assignment.due_date,
            "created_by": assignment.created_by,
            "is_active": assignment.is_active,
            "subject": assignment.subject.subject_name if assignment.subject else None,
            "created_at": assignment.created_at,
            "updated_at": assignment.updated_at,
        }
