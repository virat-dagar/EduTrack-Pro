"""Assignment service."""

import re
from datetime import date
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.config import get_settings, resolve_upload_dir
from app.exceptions import ConflictError, NotFoundError
from app.models.assignment import Assignment
from app.models.assignment_question import AssignmentQuestion
from app.models.classroom import Classroom
from app.models.student import Student
from app.models.submission import Submission
from app.models.subject import Subject
from app.models.user import User, utc_now
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate
from app.services.student_service import StudentService
from app.utils.constants import ROLE_STUDENT
from app.utils.helpers import apply_sorting, normalize_pagination, paginate_query


class AssignmentService:
    """Business logic for assignments."""

    allowed_sort_fields = {"due_date", "assigned_date", "title", "id"}
    allowed_upload_extensions = {
        ".pdf",
        ".doc",
        ".docx",
        ".png",
        ".jpg",
        ".jpeg",
        ".zip",
    }

    @staticmethod
    def save_uploaded_file(
        db: Session, upload: UploadFile, current_user: User
    ) -> dict[str, object]:
        """Store a teacher-uploaded assignment file and return its public URL."""

        original_name = upload.filename or "assignment"
        extension = Path(original_name).suffix.lower()
        if extension not in AssignmentService.allowed_upload_extensions:
            raise ConflictError(
                "Unsupported file type. Upload PDF, DOC, DOCX, image, or ZIP files."
            )

        settings = get_settings()
        safe_stem = (
            re.sub(r"[^A-Za-z0-9_-]+", "-", Path(original_name).stem).strip("-")
            or "assignment"
        )
        file_name = f"{safe_stem}-{uuid4().hex[:12]}{extension}"
        relative_dir = Path("assignments") / f"teacher_{current_user.id}"
        target_dir = resolve_upload_dir(settings.upload_dir) / relative_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / file_name

        total_bytes = 0
        with target_path.open("wb") as output:
            while True:
                chunk = upload.file.read(1024 * 1024)
                if not chunk:
                    break
                total_bytes += len(chunk)
                if total_bytes > settings.max_upload_bytes:
                    output.close()
                    target_path.unlink(missing_ok=True)
                    raise ConflictError(
                        "Uploaded file exceeds the configured size limit."
                    )
                output.write(chunk)

        return {
            "file_name": original_name,
            "stored_file": file_name,
            "file_url": f"/uploads/{relative_dir.as_posix()}/{file_name}",
            "size_bytes": total_bytes,
        }

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
        classroom_id: int | None = None,
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
                Assignment.is_active.is_(True), Assignment.is_published.is_(True)
            )
            query = query.filter(
                or_(
                    Assignment.classroom_id == student.classroom_id,
                    (
                        (Assignment.classroom_id.is_(None))
                        & (Subject.course == student.course)
                        & (Subject.department == student.department)
                        & (Subject.semester == student.semester)
                    ),
                )
            )
        if q:
            search = f"%{q.strip()}%"
            query = query.filter(
                or_(Assignment.title.ilike(search), Subject.subject_name.ilike(search))
            )
        filters = {
            Assignment.subject_id: subject_id,
            Assignment.classroom_id: classroom_id,
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
        query = apply_sorting(
            query, Assignment, sort, order, AssignmentService.allowed_sort_fields
        )
        items, total_items = paginate_query(query, safe_page, safe_page_size)
        return items, total_items, safe_page, safe_page_size

    @staticmethod
    def create_assignment(
        db: Session, payload: AssignmentCreate, teacher_id: int
    ) -> Assignment:
        """Create an assignment."""

        subject = db.query(Subject).filter(Subject.id == payload.subject_id).first()
        if subject is None:
            raise NotFoundError("Subject not found.")
        if (
            payload.classroom_id
            and db.query(Classroom).filter(Classroom.id == payload.classroom_id).first()
            is None
        ):
            raise NotFoundError("Classroom not found.")
        data = payload.model_dump(exclude={"questions"})
        data["classroom_id"] = data.get("classroom_id") or subject.classroom_id
        data["total_marks"] = AssignmentService._total_marks(
            payload.total_marks, payload.questions
        )
        data["published_at"] = utc_now() if payload.is_published else None
        assignment = Assignment(**data, created_by=teacher_id)
        assignment.questions = [
            AssignmentQuestion(**question.model_dump())
            for question in sorted(payload.questions, key=lambda item: item.question_no)
        ]
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        return assignment

    @staticmethod
    def update_assignment(
        db: Session, assignment_id: int, payload: AssignmentUpdate
    ) -> Assignment:
        """Update an assignment."""

        assignment = AssignmentService.get_assignment(db, assignment_id)
        questions = (
            payload.questions if "questions" in payload.model_fields_set else None
        )
        data = payload.model_dump(exclude_unset=True, exclude={"questions"})
        if "due_date" in data and data["due_date"] < assignment.assigned_date:
            raise ConflictError(
                "Due date must be greater than or equal to assigned date."
            )
        if data.get("classroom_id") is not None:
            if (
                db.query(Classroom).filter(Classroom.id == data["classroom_id"]).first()
                is None
            ):
                raise NotFoundError("Classroom not found.")
        if "is_published" in data:
            if data["is_published"] and assignment.published_at is None:
                assignment.published_at = utc_now()
            if not data["is_published"]:
                assignment.published_at = None
        for field, value in data.items():
            setattr(assignment, field, value)
        if questions is not None:
            assignment.questions = [
                AssignmentQuestion(**question.model_dump())
                for question in sorted(questions, key=lambda item: item.question_no)
            ]
            assignment.total_marks = AssignmentService._total_marks(
                assignment.total_marks, questions
            )
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
                Assignment.is_published.is_(True),
            )
            query = query.filter(
                or_(
                    Assignment.classroom_id == student.classroom_id,
                    (
                        (Assignment.classroom_id.is_(None))
                        & (Subject.course == student.course)
                        & (Subject.department == student.department)
                        & (Subject.semester == student.semester)
                    ),
                )
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
    def publish(db: Session, assignment_id: int) -> Assignment:
        """Publish an assignment."""

        assignment = AssignmentService.get_assignment(db, assignment_id)
        assignment.is_published = True
        assignment.published_at = assignment.published_at or utc_now()
        db.commit()
        db.refresh(assignment)
        return assignment

    @staticmethod
    def submission_summary(db: Session, assignment_id: int) -> dict[str, object]:
        """Return submission counts for an assignment."""

        assignment = AssignmentService.get_assignment(db, assignment_id)
        if assignment.classroom_id:
            assigned_count = (
                db.query(Student)
                .filter(
                    Student.classroom_id == assignment.classroom_id,
                    Student.is_active.is_(True),
                )
                .count()
            )
        else:
            assigned_count = 0
        submitted = len(assignment.submissions or [])
        return {
            "assignment_id": assignment.id,
            "assigned_students": assigned_count,
            "submitted": submitted,
            "pending": max(assigned_count - submitted, 0) if assigned_count else 0,
            "reviewed": len(
                [
                    item
                    for item in assignment.submissions
                    if item.reviewed_by is not None
                ]
            ),
        }

    @staticmethod
    def enrich(assignment: Assignment) -> dict[str, object]:
        """Return assignment data with subject name."""

        return {
            "id": assignment.id,
            "classroom_id": assignment.classroom_id,
            "subject_id": assignment.subject_id,
            "title": assignment.title,
            "description": assignment.description,
            "pdf_file": assignment.pdf_file,
            "total_marks": assignment.total_marks,
            "assigned_date": assignment.assigned_date,
            "due_date": assignment.due_date,
            "created_by": assignment.created_by,
            "is_published": assignment.is_published,
            "published_at": assignment.published_at,
            "is_active": assignment.is_active,
            "subject": assignment.subject.subject_name if assignment.subject else None,
            "classroom": (
                assignment.classroom.classroom_name if assignment.classroom else None
            ),
            "questions": [
                {
                    "id": question.id,
                    "assignment_id": question.assignment_id,
                    "question_no": question.question_no,
                    "title": question.title,
                    "description": question.description,
                    "max_marks": question.max_marks,
                }
                for question in assignment.questions
            ],
            "created_at": assignment.created_at,
            "updated_at": assignment.updated_at,
        }

    @staticmethod
    def enrich_for_user(
        db: Session, assignment: Assignment, current_user: User
    ) -> dict[str, object]:
        """Return assignment data with current student's submission state."""

        data = AssignmentService.enrich(assignment)
        if current_user.role != ROLE_STUDENT:
            return data
        student = StudentService.get_student_by_user(db, current_user.id)
        submission = (
            db.query(Submission)
            .filter(
                Submission.assignment_id == assignment.id,
                Submission.student_id == student.id,
            )
            .first()
        )
        if submission is None:
            data.update(
                {
                    "my_submission_id": None,
                    "submission_status": "Pending",
                    "submission_file": None,
                    "submission_grade": None,
                    "submission_percentage": None,
                    "submission_feedback": None,
                }
            )
            return data
        data.update(
            {
                "my_submission_id": submission.id,
                "submission_status": submission.status,
                "submission_file": submission.submitted_file
                or submission.attachment_path,
                "submission_grade": submission.grade,
                "submission_percentage": submission.percentage,
                "submission_feedback": submission.feedback,
            }
        )
        return data

    @staticmethod
    def _total_marks(total_marks: float | None, questions: list[object]) -> float:
        """Calculate total marks from questions or explicit total."""

        if questions:
            return float(
                sum(
                    (
                        question["max_marks"]
                        if isinstance(question, dict)
                        else question.max_marks
                    )
                    for question in questions
                )
            )
        if total_marks is None:
            raise ConflictError("Total marks or questions are required.")
        return float(total_marks)
