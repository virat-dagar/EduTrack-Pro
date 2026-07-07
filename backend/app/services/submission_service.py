"""Submission service."""

from datetime import date
from pathlib import Path
import re
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import get_settings, resolve_upload_dir
from app.exceptions import AuthorizationError, ConflictError, NotFoundError
from app.models.assignment import Assignment
from app.models.assignment_question import AssignmentQuestion
from app.models.submission import Submission
from app.models.submission_grade import SubmissionGrade
from app.models.user import User
from app.schemas.submission import SubmissionCreate, SubmissionQuestionScore, SubmissionReview, SubmissionUpdate
from app.services.student_service import StudentService
from app.utils.constants import ROLE_STUDENT, SUBMISSION_LATE, SUBMISSION_REVIEWED, SUBMISSION_SUBMITTED
from app.utils.helpers import apply_sorting, normalize_pagination, paginate_query


class SubmissionService:
    """Business logic for assignment submissions."""

    allowed_sort_fields = {"submission_date", "status", "assignment_id", "student_id", "id"}
    allowed_upload_extensions = {".pdf", ".doc", ".docx", ".png", ".jpg", ".jpeg", ".zip"}

    @staticmethod
    def get_submission(db: Session, submission_id: int) -> Submission:
        """Return a submission."""

        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if submission is None:
            raise NotFoundError("Submission not found.")
        return submission

    @staticmethod
    def ensure_access(db: Session, submission_id: int, current_user: User) -> Submission:
        """Return a submission if the user may view it."""

        submission = SubmissionService.get_submission(db, submission_id)
        if current_user.role != ROLE_STUDENT:
            return submission
        student = StudentService.get_student_by_user(db, current_user.id)
        if submission.student_id != student.id:
            raise AuthorizationError("You may only access your own submissions.")
        return submission

    @staticmethod
    def list_submissions(
        db: Session,
        current_user: User,
        page: int = 1,
        page_size: int = 20,
        assignment_id: int | None = None,
        student_id: int | None = None,
        status: str | None = None,
        reviewed: bool | None = None,
        sort: str | None = "submission_date",
        order: str = "desc",
    ) -> tuple[list[Submission], int, int, int]:
        """Return filtered and paginated submissions."""

        safe_page, safe_page_size = normalize_pagination(page, page_size)
        query = db.query(Submission)
        if current_user.role == ROLE_STUDENT:
            student = StudentService.get_student_by_user(db, current_user.id)
            query = query.filter(Submission.student_id == student.id)
        if assignment_id:
            query = query.filter(Submission.assignment_id == assignment_id)
        if student_id:
            query = query.filter(Submission.student_id == student_id)
        if status:
            query = query.filter(Submission.status == status)
        if reviewed is not None:
            query = query.filter(Submission.reviewed_by.isnot(None) if reviewed else Submission.reviewed_by.is_(None))
        query = apply_sorting(query, Submission, sort, order, SubmissionService.allowed_sort_fields)
        items, total_items = paginate_query(query, safe_page, safe_page_size)
        return items, total_items, safe_page, safe_page_size

    @staticmethod
    def submit_assignment(db: Session, payload: SubmissionCreate, current_user: User) -> Submission:
        """Submit an assignment as the current student."""

        student = StudentService.get_student_by_user(db, current_user.id)
        assignment = db.query(Assignment).filter(Assignment.id == payload.assignment_id).first()
        if assignment is None:
            raise NotFoundError("Assignment not found.")
        if not assignment.is_published or not assignment.is_active:
            raise ConflictError("Assignment is not open for submissions.")
        if assignment.classroom_id and assignment.classroom_id != student.classroom_id:
            raise AuthorizationError("This assignment is not assigned to your classroom.")
        duplicate = (
            db.query(Submission)
            .filter(
                Submission.assignment_id == payload.assignment_id,
                Submission.student_id == student.id,
            )
            .first()
        )
        if duplicate:
            raise ConflictError("Assignment has already been submitted.")
        status = SUBMISSION_LATE if date.today() > assignment.due_date else SUBMISSION_SUBMITTED
        submission = Submission(
            assignment_id=payload.assignment_id,
            student_id=student.id,
            status=status,
            submission_notes=payload.submission_notes,
            attachment_path=payload.attachment_path or payload.submitted_file,
            submitted_file=payload.submitted_file or payload.attachment_path,
        )
        db.add(submission)
        db.commit()
        db.refresh(submission)
        return submission

    @staticmethod
    def save_uploaded_file(db: Session, upload: UploadFile, current_user: User) -> dict[str, object]:
        """Store a student submission file and return its public URL."""

        student = StudentService.get_student_by_user(db, current_user.id)
        original_name = upload.filename or "submission"
        extension = Path(original_name).suffix.lower()
        if extension not in SubmissionService.allowed_upload_extensions:
            raise ConflictError("Unsupported file type. Upload PDF, DOC, DOCX, image, or ZIP files.")

        settings = get_settings()
        safe_stem = re.sub(r"[^A-Za-z0-9_-]+", "-", Path(original_name).stem).strip("-") or "submission"
        file_name = f"{safe_stem}-{uuid4().hex[:12]}{extension}"
        relative_dir = Path("submissions") / f"student_{student.id}"
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
                    raise ConflictError("Uploaded file exceeds the configured size limit.")
                output.write(chunk)

        return {
            "file_name": original_name,
            "stored_file": file_name,
            "file_url": f"/uploads/{relative_dir.as_posix()}/{file_name}",
            "size_bytes": total_bytes,
        }

    @staticmethod
    def update_submission(
        db: Session,
        submission_id: int,
        payload: SubmissionUpdate,
        current_user: User,
    ) -> Submission:
        """Update a submission before the assignment due date."""

        submission = SubmissionService.ensure_access(db, submission_id, current_user)
        if submission.reviewed_by is not None:
            raise ConflictError("Reviewed submissions cannot be updated.")
        if date.today() > submission.assignment.due_date:
            raise ConflictError("Submission cannot be updated after the due date.")
        data = payload.model_dump(exclude_unset=True)
        if "submitted_file" in data and data.get("attachment_path") is None:
            data["attachment_path"] = data["submitted_file"]
        if "attachment_path" in data and data.get("submitted_file") is None:
            data["submitted_file"] = data["attachment_path"]
        for field, value in data.items():
            setattr(submission, field, value)
        db.commit()
        db.refresh(submission)
        return submission

    @staticmethod
    def delete_submission(db: Session, submission_id: int) -> None:
        """Delete a submission."""

        submission = SubmissionService.get_submission(db, submission_id)
        db.delete(submission)
        db.commit()

    @staticmethod
    def review_submission(
        db: Session,
        submission_id: int,
        payload: SubmissionReview,
        teacher_id: int,
    ) -> Submission:
        """Review a submission."""

        submission = SubmissionService.get_submission(db, submission_id)
        if payload.question_scores:
            SubmissionService._apply_question_scores(db, submission, payload.question_scores)
        submission.status = payload.status or SUBMISSION_REVIEWED
        submission.feedback = payload.feedback
        submission.reviewed_by = teacher_id
        from app.models.user import utc_now

        submission.reviewed_at = utc_now()
        db.commit()
        db.refresh(submission)
        return submission

    @staticmethod
    def pending_reviews(db: Session) -> dict[str, object]:
        """Return submissions awaiting review."""

        items = (
            db.query(Submission)
            .filter(Submission.reviewed_by.is_(None))
            .order_by(Submission.submission_date.desc())
            .all()
        )
        return {
            "pending_reviews": len(items),
            "items": [SubmissionService.enrich(item) for item in items],
        }

    @staticmethod
    def enrich(submission: Submission) -> dict[str, object]:
        """Return submission data with reviewed flag."""

        return {
            "id": submission.id,
            "assignment_id": submission.assignment_id,
            "student_id": submission.student_id,
            "submission_date": submission.submission_date,
            "status": submission.status,
            "submission_notes": submission.submission_notes,
            "attachment_path": submission.attachment_path,
            "submitted_file": submission.submitted_file,
            "reviewed_by": submission.reviewed_by,
            "reviewed_at": submission.reviewed_at,
            "feedback": submission.feedback,
            "total_marks": submission.total_marks,
            "percentage": submission.percentage,
            "grade": submission.grade,
            "question_grades": [
                {
                    "id": grade.id,
                    "question_id": grade.question_id,
                    "question_no": grade.question.question_no if grade.question else None,
                    "max_marks": grade.question.max_marks if grade.question else None,
                    "obtained_marks": grade.obtained_marks,
                    "feedback": grade.feedback,
                }
                for grade in submission.question_grades
            ],
            "reviewed": submission.reviewed_by is not None,
            "created_at": submission.created_at,
            "updated_at": submission.updated_at,
        }

    @staticmethod
    def _apply_question_scores(
        db: Session,
        submission: Submission,
        question_scores: list[SubmissionQuestionScore],
    ) -> None:
        """Replace question-wise grades and calculate submission totals."""

        questions = {
            question.id: question
            for question in db.query(AssignmentQuestion)
            .filter(AssignmentQuestion.assignment_id == submission.assignment_id)
            .all()
        }
        if not questions:
            raise ConflictError("Assignment does not have question-wise grading configured.")
        for existing in list(submission.question_grades):
            db.delete(existing)
        db.flush()

        obtained_total = 0.0
        max_total = sum(question.max_marks for question in questions.values())
        seen_questions: set[int] = set()
        for score in question_scores:
            question = questions.get(score.question_id)
            if question is None:
                raise ConflictError("Question does not belong to this assignment.")
            if score.question_id in seen_questions:
                raise ConflictError("Duplicate question score submitted.")
            if score.obtained_marks > question.max_marks:
                raise ConflictError(f"Question {question.question_no} exceeds maximum marks.")
            seen_questions.add(score.question_id)
            obtained_total += score.obtained_marks
            db.add(
                SubmissionGrade(
                    submission_id=submission.id,
                    question_id=score.question_id,
                    obtained_marks=score.obtained_marks,
                    feedback=score.feedback,
                )
            )
        submission.total_marks = round(obtained_total, 2)
        submission.percentage = round((obtained_total / max_total) * 100, 2) if max_total else 0.0
        submission.grade = SubmissionService._grade_for_percentage(submission.percentage)

    @staticmethod
    def _grade_for_percentage(percentage: float | None) -> str:
        """Return a simple academic grade from percentage."""

        value = percentage or 0.0
        if value >= 90:
            return "A+"
        if value >= 80:
            return "A"
        if value >= 70:
            return "B"
        if value >= 60:
            return "C"
        if value >= 50:
            return "D"
        return "F"
