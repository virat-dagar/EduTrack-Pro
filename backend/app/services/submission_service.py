"""Submission service."""

from datetime import date

from sqlalchemy.orm import Session

from app.exceptions import AuthorizationError, ConflictError, NotFoundError
from app.models.assignment import Assignment
from app.models.submission import Submission
from app.models.user import User
from app.schemas.submission import SubmissionCreate, SubmissionReview, SubmissionUpdate
from app.services.student_service import StudentService
from app.utils.constants import ROLE_STUDENT, SUBMISSION_LATE, SUBMISSION_REVIEWED, SUBMISSION_SUBMITTED
from app.utils.helpers import apply_sorting, normalize_pagination, paginate_query


class SubmissionService:
    """Business logic for assignment submissions."""

    allowed_sort_fields = {"submission_date", "status", "assignment_id", "student_id", "id"}

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
            attachment_path=payload.attachment_path,
        )
        db.add(submission)
        db.commit()
        db.refresh(submission)
        return submission

    @staticmethod
    def update_submission(
        db: Session,
        submission_id: int,
        payload: SubmissionUpdate,
        current_user: User,
    ) -> Submission:
        """Update a submission before the assignment due date."""

        submission = SubmissionService.ensure_access(db, submission_id, current_user)
        if date.today() > submission.assignment.due_date:
            raise ConflictError("Submission cannot be updated after the due date.")
        for field, value in payload.model_dump(exclude_unset=True).items():
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
            "reviewed_by": submission.reviewed_by,
            "reviewed_at": submission.reviewed_at,
            "feedback": submission.feedback,
            "reviewed": submission.reviewed_by is not None,
            "created_at": submission.created_at,
            "updated_at": submission.updated_at,
        }
