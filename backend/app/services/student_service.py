"""Student service."""

import secrets
import string
from typing import BinaryIO

from pydantic import ValidationError
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.exceptions import AuthorizationError, ConflictError, NotFoundError
from app.core.security import hash_password
from app.models.student import Student
from app.models.user import User
from app.schemas.student import StudentCreate, StudentImportCommit, StudentImportRow, StudentUpdate
from app.services.classroom_service import ClassroomService
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
        classroom_id: int | None = None,
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
            Student.classroom_id: classroom_id,
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
        """Create a student profile and generate login credentials when needed."""

        data = StudentService._student_payload_data(db, payload)
        StudentService._ensure_unique(db, data)
        credentials: dict[str, str | int] | None = None

        if payload.user_id:
            user = db.query(User).filter(User.id == payload.user_id).first()
            if user is None:
                raise NotFoundError("Linked user not found.")
            if user.role != ROLE_STUDENT:
                raise ConflictError("Student profiles must be linked to student users.")
            if user.student_profile:
                raise ConflictError("User already has a student profile.")
        else:
            existing_user = db.query(User).filter(User.email == data["email"]).first()
            if existing_user:
                raise ConflictError("A user account already exists for this email.")
            generated_password = StudentService.generate_password()
            user = User(
                full_name=f"{data['first_name']} {data['last_name']}",
                email=data["email"],
                password_hash=hash_password(generated_password),
                role=ROLE_STUDENT,
                is_active=True,
            )
            db.add(user)
            db.flush()
            data["user_id"] = user.id
            credentials = {
                "user_id": user.id,
                "email": user.email,
                "password": generated_password,
            }

        data["user_id"] = user.id
        student = Student(**data)
        db.add(student)
        db.commit()
        db.refresh(student)
        student.generated_credentials = credentials
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
        if "classroom_id" in data and data["classroom_id"] is not None:
            ClassroomService.get_classroom(db, data["classroom_id"])
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
    def _ensure_unique(db: Session, data: dict[str, object]) -> None:
        """Validate unique student identifiers."""

        checks = [
            (Student.roll_number == data["roll_number"], "Roll number already exists."),
            (Student.email == normalize_email(str(data["email"])), "Student email already exists."),
        ]
        if data.get("enrollment_number"):
            checks.append(
                (
                    Student.enrollment_number == data["enrollment_number"],
                    "Enrollment number already exists.",
                )
            )
        for condition, message in checks:
            if db.query(Student).filter(condition).first():
                raise ConflictError(message)

    @staticmethod
    def _student_payload_data(db: Session, payload: StudentCreate | StudentImportRow) -> dict[str, object]:
        """Normalize student create/import payload into model data."""

        data = payload.model_dump(exclude={"row_number"} if isinstance(payload, StudentImportRow) else set())
        data["email"] = normalize_email(str(data["email"]))
        data["section"] = data.get("section") or "A"
        data["enrollment_number"] = data.get("enrollment_number") or StudentService.build_enrollment_number(
            str(data["academic_year"]),
            str(data["roll_number"]),
        )
        if data.get("classroom_id") is not None:
            ClassroomService.get_classroom(db, int(data["classroom_id"]))
        else:
            classroom = ClassroomService.find_or_create(
                db,
                str(data["department"]),
                str(data["course"]),
                int(data["semester"]),
                str(data["section"]),
                str(data["academic_year"]),
            )
            data["classroom_id"] = classroom.id
        return data

    @staticmethod
    def build_enrollment_number(academic_year: str, roll_number: str) -> str:
        """Build a deterministic enrollment number when one is not provided."""

        compact_year = "".join(character for character in academic_year if character.isalnum())
        return f"{compact_year}-{roll_number}"[:50]

    @staticmethod
    def generate_password(length: int = 12) -> str:
        """Generate a readable temporary password."""

        alphabet = string.ascii_letters + string.digits
        suffix = "".join(secrets.choice(alphabet) for _ in range(length))
        return f"ETP-{suffix}"

    @staticmethod
    def preview_import(db: Session, filename: str, file: BinaryIO) -> dict[str, object]:
        """Parse and validate a CSV or Excel student import file."""

        rows = StudentService._read_import_rows(filename, file)
        normalized_rows: list[dict[str, object]] = []
        seen_rolls: set[str] = set()
        seen_emails: set[str] = set()
        for index, row in enumerate(rows, start=2):
            data = StudentService._normalize_import_row(row)
            data["row_number"] = index
            errors: list[str] = []
            parsed: StudentImportRow | None = None
            try:
                parsed = StudentImportRow(**data)
            except ValidationError as exc:
                errors.extend(error["msg"] for error in exc.errors())
            if parsed:
                roll_key = parsed.roll_number.lower()
                email_key = str(parsed.email).lower()
                if roll_key in seen_rolls:
                    errors.append("Duplicate roll number in file.")
                if email_key in seen_emails:
                    errors.append("Duplicate email in file.")
                if db.query(Student).filter(Student.roll_number == parsed.roll_number).first():
                    errors.append("Duplicate roll number.")
                if db.query(Student).filter(Student.email == normalize_email(str(parsed.email))).first():
                    errors.append("Duplicate student email.")
                if db.query(User).filter(User.email == normalize_email(str(parsed.email))).first():
                    errors.append("Duplicate user email.")
                if parsed.enrollment_number and db.query(Student).filter(
                    Student.enrollment_number == parsed.enrollment_number
                ).first():
                    errors.append("Duplicate enrollment number.")
                seen_rolls.add(roll_key)
                seen_emails.add(email_key)
                row_data = parsed.model_dump(mode="json")
            else:
                row_data = data
            normalized_rows.append(
                {
                    "row_number": index,
                    "data": row_data,
                    "is_valid": not errors,
                    "errors": errors,
                }
            )
        return {
            "total_rows": len(normalized_rows),
            "valid_rows": sum(1 for row in normalized_rows if row["is_valid"]),
            "invalid_rows": sum(1 for row in normalized_rows if not row["is_valid"]),
            "rows": normalized_rows,
        }

    @staticmethod
    def commit_import(db: Session, payload: StudentImportCommit) -> dict[str, object]:
        """Import valid student rows and return skipped reasons."""

        imported: list[dict[str, object]] = []
        skipped: list[dict[str, object]] = []
        for row in payload.rows:
            try:
                student = StudentService.create_student(db, StudentCreate(**row.model_dump(exclude={"row_number"})))
                imported.append(
                    {
                        "row_number": row.row_number,
                        "student_id": student.id,
                        "roll_number": student.roll_number,
                        "email": student.email,
                        "generated_credentials": getattr(student, "generated_credentials", None),
                    }
                )
            except Exception as exc:  # noqa: BLE001 - import reports should collect row-level failures
                db.rollback()
                if not payload.import_valid_only:
                    skipped.append({"row_number": row.row_number, "reason": str(exc)})
                else:
                    skipped.append({"row_number": row.row_number, "reason": str(exc)})
        return {
            "imported": len(imported),
            "skipped": len(skipped),
            "items": imported,
            "skipped_rows": skipped,
        }

    @staticmethod
    def export_rows(db: Session) -> list[dict[str, object]]:
        """Return student rows ready for CSV export."""

        students = db.query(Student).order_by(Student.roll_number.asc()).all()
        return [
            {
                "Roll No": student.roll_number,
                "First Name": student.first_name,
                "Last Name": student.last_name,
                "Email": student.email,
                "Course": student.course,
                "Department": student.department,
                "Semester": student.semester,
                "Section": student.section or "",
                "Classroom ID": student.classroom_id or "",
            }
            for student in students
        ]

    @staticmethod
    def _read_import_rows(filename: str, file: BinaryIO) -> list[dict[str, object]]:
        """Read student import rows from CSV or Excel."""

        try:
            import pandas as pd
        except ImportError as exc:
            raise ConflictError("Student import requires pandas and openpyxl dependencies.") from exc

        lower_name = filename.lower()
        if lower_name.endswith(".csv"):
            frame = pd.read_csv(file)
        elif lower_name.endswith((".xls", ".xlsx")):
            frame = pd.read_excel(file)
        else:
            raise ConflictError("Only CSV, XLS, and XLSX student imports are supported.")
        frame = frame.where(pd.notnull(frame), None)
        return frame.to_dict(orient="records")

    @staticmethod
    def _normalize_import_row(row: dict[str, object]) -> dict[str, object]:
        """Map spreadsheet column names to API field names."""

        aliases = {
            "roll no": "roll_number",
            "roll number": "roll_number",
            "roll_number": "roll_number",
            "first name": "first_name",
            "first_name": "first_name",
            "last name": "last_name",
            "last_name": "last_name",
            "email": "email",
            "course": "course",
            "department": "department",
            "semester": "semester",
            "section": "section",
            "enrollment number": "enrollment_number",
            "enrollment_number": "enrollment_number",
            "phone": "phone",
            "gender": "gender",
            "date of birth": "date_of_birth",
            "date_of_birth": "date_of_birth",
            "academic year": "academic_year",
            "academic_year": "academic_year",
            "admission date": "admission_date",
            "admission_date": "admission_date",
            "classroom id": "classroom_id",
            "classroom_id": "classroom_id",
        }
        normalized: dict[str, object] = {}
        for key, value in row.items():
            field = aliases.get(str(key).strip().lower())
            if field:
                normalized[field] = value
        return normalized
