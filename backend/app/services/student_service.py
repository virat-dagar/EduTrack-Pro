"""Student service."""

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.exceptions import AuthorizationError, ConflictError, NotFoundError
from app.models.student import Student
from app.models.user import User
from app.schemas.student import StudentCreate, StudentUpdate
from app.utils.constants import ROLE_STUDENT, ROLE_TEACHER
from app.utils.helpers import apply_sorting, normalize_pagination, paginate_query
from app.utils.validators import normalize_email


class StudentService:
    """Business logic for student profiles."""

    allowed_sort_fields = {"first_name", "roll_number", "admission_date", "semester", "id"}

    @staticmethod
    def get_student(db: Session, student_id: int) -> Student:
        """Return a student by ID."""

        student = db.query(Student).filter(Student.id == student_id).first()
        if student is None:
            raise NotFoundError("Student not found.")
        return student

    @staticmethod
    def get_student_by_user(db: Session, user_id: int) -> Student:
        """Return a student profile by user ID."""

        student = db.query(Student).filter(Student.user_id == user_id).first()
        if student is None:
            raise NotFoundError("Student profile not found.")
        return student

    @staticmethod
    def ensure_access(db: Session, student_id: int, current_user: User) -> Student:
        """Return a student if the current user may access it."""

        student = StudentService.get_student(db, student_id)
        if current_user.role == ROLE_TEACHER or student.user_id == current_user.id:
            return student
        raise AuthorizationError("You may only access your own student profile.")

    @staticmethod
    def list_students(
        db: Session,
        page: int = 1,
        page_size: int = 20,
        q: str | None = None,
        course: str | None = None,
        department: str | None = None,
        semester: int | None = None,
        section: str | None = None,
        academic_year: str | None = None,
        is_active: bool | None = None,
        sort: str | None = "first_name",
        order: str = "asc",
    ) -> tuple[list[Student], int, int, int]:
        """Return filtered and paginated students."""

        safe_page, safe_page_size = normalize_pagination(page, page_size)
        query = db.query(Student)
        if q:
            search = f"%{q.strip()}%"
            query = query.filter(
                or_(
                    Student.first_name.ilike(search),
                    Student.last_name.ilike(search),
                    Student.roll_number.ilike(search),
                    Student.enrollment_number.ilike(search),
                    Student.department.ilike(search),
                    Student.course.ilike(search),
                )
            )
        filters = {
            Student.course: course,
            Student.department: department,
            Student.semester: semester,
            Student.section: section,
            Student.academic_year: academic_year,
        }
        for column, value in filters.items():
            if value not in (None, ""):
                query = query.filter(column == value)
        if is_active is not None:
            query = query.filter(Student.is_active == is_active)
        query = apply_sorting(query, Student, sort, order, StudentService.allowed_sort_fields)
        items, total_items = paginate_query(query, safe_page, safe_page_size)
        return items, total_items, safe_page, safe_page_size

    @staticmethod
    def create_student(db: Session, payload: StudentCreate) -> Student:
        """Create a student profile."""

        user = db.query(User).filter(User.id == payload.user_id).first()
        if user is None:
            raise NotFoundError("Linked user not found.")
        if user.role != ROLE_STUDENT:
            raise ConflictError("Student profiles must be linked to student users.")
        if user.student_profile:
            raise ConflictError("User already has a student profile.")
        StudentService._ensure_unique(db, payload)
        student = Student(**payload.model_dump())
        student.email = normalize_email(str(payload.email))
        db.add(student)
        db.commit()
        db.refresh(student)
        return student

    @staticmethod
    def update_student(db: Session, student_id: int, payload: StudentUpdate) -> Student:
        """Update a student profile."""

        student = StudentService.get_student(db, student_id)
        data = payload.model_dump(exclude_unset=True)
        if "email" in data and data["email"] is not None:
            email = normalize_email(str(data["email"]))
            existing = db.query(Student).filter(Student.email == email, Student.id != student.id).first()
            if existing:
                raise ConflictError("Student email already exists.")
            data["email"] = email
        for field, value in data.items():
            setattr(student, field, value)
        db.commit()
        db.refresh(student)
        return student

    @staticmethod
    def delete_student(db: Session, student_id: int) -> None:
        """Delete a student only when dependent academic records do not exist."""

        student = StudentService.get_student(db, student_id)
        if student.attendance_records or student.marks_records or student.submissions:
            raise ConflictError("Student cannot be deleted while academic records exist.")
        db.delete(student)
        db.commit()

    @staticmethod
    def _ensure_unique(db: Session, payload: StudentCreate) -> None:
        """Validate unique student identifiers."""

        checks = [
            (Student.roll_number == payload.roll_number, "Roll number already exists."),
            (
                Student.enrollment_number == payload.enrollment_number,
                "Enrollment number already exists.",
            ),
            (Student.email == normalize_email(str(payload.email)), "Student email already exists."),
        ]
        for condition, message in checks:
            if db.query(Student).filter(condition).first():
                raise ConflictError(message)
