"""Classroom service."""

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.exceptions import ConflictError, NotFoundError
from app.models.classroom import Classroom
from app.schemas.classroom import ClassroomCreate, ClassroomUpdate
from app.utils.helpers import apply_sorting, normalize_pagination, paginate_query
from app.utils.validators import normalize_text


class ClassroomService:
    """Business logic for academic classroom groups."""

    allowed_sort_fields = {"department", "course", "semester", "section", "academic_year", "id"}

    @staticmethod
    def get_classroom(db: Session, classroom_id: int) -> Classroom:
        """Return a classroom by ID."""

        classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
        if classroom is None:
            raise NotFoundError("Classroom not found.")
        return classroom

    @staticmethod
    def list_classrooms(
        db: Session,
        page: int = 1,
        page_size: int = 20,
        q: str | None = None,
        department: str | None = None,
        course: str | None = None,
        semester: int | None = None,
        section: str | None = None,
        academic_year: str | None = None,
        is_active: bool | None = None,
        sort: str | None = "department",
        order: str = "asc",
    ) -> tuple[list[Classroom], int, int, int]:
        """Return filtered and paginated classrooms."""

        safe_page, safe_page_size = normalize_pagination(page, page_size)
        query = db.query(Classroom)
        if q:
            search = f"%{q.strip()}%"
            query = query.filter(
                or_(
                    Classroom.classroom_code.ilike(search),
                    Classroom.classroom_name.ilike(search),
                    Classroom.department.ilike(search),
                    Classroom.course.ilike(search),
                    Classroom.section.ilike(search),
                )
            )
        filters = {
            Classroom.department: department,
            Classroom.course: course,
            Classroom.semester: semester,
            Classroom.section: section,
            Classroom.academic_year: academic_year,
        }
        for column, value in filters.items():
            if value not in (None, ""):
                query = query.filter(column == value)
        if is_active is not None:
            query = query.filter(Classroom.is_active == is_active)
        query = apply_sorting(query, Classroom, sort, order, ClassroomService.allowed_sort_fields)
        items, total_items = paginate_query(query, safe_page, safe_page_size)
        return items, total_items, safe_page, safe_page_size

    @staticmethod
    def create_classroom(db: Session, payload: ClassroomCreate) -> Classroom:
        """Create a classroom."""

        data = payload.model_dump()
        data["classroom_code"] = data["classroom_code"] or ClassroomService.build_code(
            data["department"],
            data["course"],
            data["semester"],
            data["section"],
            data["academic_year"],
        )
        data["classroom_name"] = data["classroom_name"] or ClassroomService.build_name(
            data["department"],
            data["course"],
            data["semester"],
            data["section"],
        )
        ClassroomService._ensure_unique(db, data)
        classroom = Classroom(**data)
        db.add(classroom)
        db.commit()
        db.refresh(classroom)
        return classroom

    @staticmethod
    def update_classroom(db: Session, classroom_id: int, payload: ClassroomUpdate) -> Classroom:
        """Update a classroom."""

        classroom = ClassroomService.get_classroom(db, classroom_id)
        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(classroom, field, value)
        if not classroom.classroom_code:
            classroom.classroom_code = ClassroomService.build_code(
                classroom.department,
                classroom.course,
                classroom.semester,
                classroom.section,
                classroom.academic_year,
            )
        if not classroom.classroom_name:
            classroom.classroom_name = ClassroomService.build_name(
                classroom.department,
                classroom.course,
                classroom.semester,
                classroom.section,
            )
        duplicate = (
            db.query(Classroom)
            .filter(Classroom.classroom_code == classroom.classroom_code, Classroom.id != classroom.id)
            .first()
        )
        if duplicate:
            raise ConflictError("Classroom code already exists.")
        db.commit()
        db.refresh(classroom)
        return classroom

    @staticmethod
    def delete_classroom(db: Session, classroom_id: int) -> None:
        """Delete an unused classroom."""

        classroom = ClassroomService.get_classroom(db, classroom_id)
        if classroom.students or classroom.subjects or classroom.assignments:
            raise ConflictError("Classroom cannot be deleted while academic records are linked.")
        db.delete(classroom)
        db.commit()

    @staticmethod
    def find_or_create(
        db: Session,
        department: str,
        course: str,
        semester: int,
        section: str | None,
        academic_year: str,
    ) -> Classroom:
        """Find or create a classroom for an academic group."""

        clean_department = normalize_text(department) or department
        clean_course = normalize_text(course) or course
        clean_section = normalize_text(section or "A") or "A"
        clean_year = normalize_text(academic_year) or academic_year
        classroom = (
            db.query(Classroom)
            .filter(
                func.lower(Classroom.department) == clean_department.lower(),
                func.lower(Classroom.course) == clean_course.lower(),
                Classroom.semester == semester,
                func.lower(Classroom.section) == clean_section.lower(),
                func.lower(Classroom.academic_year) == clean_year.lower(),
            )
            .first()
        )
        if classroom:
            return classroom
        payload = ClassroomCreate(
            department=clean_department,
            course=clean_course,
            semester=semester,
            section=clean_section,
            academic_year=clean_year,
        )
        return ClassroomService.create_classroom(db, payload)

    @staticmethod
    def enrich(classroom: Classroom) -> dict[str, object]:
        """Return classroom data with derived counts."""

        return {
            "id": classroom.id,
            "classroom_code": classroom.classroom_code,
            "classroom_name": classroom.classroom_name,
            "department": classroom.department,
            "course": classroom.course,
            "semester": classroom.semester,
            "section": classroom.section,
            "academic_year": classroom.academic_year,
            "is_active": classroom.is_active,
            "student_count": len(classroom.students or []),
            "subject_count": len(classroom.subjects or []),
            "created_at": classroom.created_at,
            "updated_at": classroom.updated_at,
        }

    @staticmethod
    def build_code(
        department: str,
        course: str,
        semester: int,
        section: str,
        academic_year: str,
    ) -> str:
        """Build a stable classroom code."""

        pieces = [department, course, f"S{semester}", section, academic_year]
        return "-".join(ClassroomService._slug(piece) for piece in pieces if piece).upper()

    @staticmethod
    def build_name(department: str, course: str, semester: int, section: str) -> str:
        """Build a readable classroom name."""

        return f"{department} - {course} Semester {semester} Section {section}"

    @staticmethod
    def _slug(value: object) -> str:
        """Return a compact code-safe string."""

        text = normalize_text(str(value)) or str(value)
        return "".join(character for character in text if character.isalnum())

    @staticmethod
    def _ensure_unique(db: Session, data: dict[str, object]) -> None:
        """Validate unique classroom identifiers."""

        existing_code = db.query(Classroom).filter(Classroom.classroom_code == data["classroom_code"]).first()
        if existing_code:
            raise ConflictError("Classroom code already exists.")
        existing_group = (
            db.query(Classroom)
            .filter(
                Classroom.department == data["department"],
                Classroom.course == data["course"],
                Classroom.semester == data["semester"],
                Classroom.section == data["section"],
                Classroom.academic_year == data["academic_year"],
            )
            .first()
        )
        if existing_group:
            raise ConflictError("Classroom already exists for this academic group.")
