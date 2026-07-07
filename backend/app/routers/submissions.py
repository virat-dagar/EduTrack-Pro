"""Submissions router."""

from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_student, require_teacher
from app.database.session import get_db
from app.models.user import User
from app.schemas.submission import SubmissionCreate, SubmissionResponse, SubmissionReview, SubmissionUpdate
from app.services.student_service import StudentService
from app.services.submission_service import SubmissionService
from app.utils.response import pagination_response, success_response

router = APIRouter(prefix="/api/v1/submissions", tags=["Submissions"])


@router.get("", summary="List submissions")
def list_submissions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    assignment_id: int | None = None,
    student_id: int | None = None,
    status_filter: str | None = Query(default=None, alias="status"),
    reviewed: bool | None = None,
    sort: str | None = "submission_date",
    order: str = "desc",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return submissions."""

    items, total_items, safe_page, safe_page_size = SubmissionService.list_submissions(
        db,
        current_user,
        page,
        page_size,
        assignment_id,
        student_id,
        status_filter,
        reviewed,
        sort,
        order,
    )
    data = pagination_response(
        [SubmissionResponse.model_validate(SubmissionService.enrich(item)).model_dump(mode="json") for item in items],
        safe_page,
        safe_page_size,
        total_items,
    )
    return success_response("", data)


@router.get("/pending", summary="Pending reviews")
def pending_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Return submissions awaiting review."""

    return success_response("", SubmissionService.pending_reviews(db))


@router.post("/upload", status_code=status.HTTP_201_CREATED, summary="Upload submission file")
def upload_submission_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
) -> dict:
    """Upload a solution file for a student submission."""

    return success_response(
        "Submission file uploaded successfully.",
        SubmissionService.save_uploaded_file(db, file, current_user),
    )


@router.get("/student/{student_id}", summary="Student submissions")
def student_submissions(
    student_id: int,
    status_filter: str | None = Query(default=None, alias="status"),
    assignment_id: int | None = None,
    reviewed: bool | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return submissions for a student."""

    StudentService.ensure_access(db, student_id, current_user)
    items, total_items, page, page_size = SubmissionService.list_submissions(
        db,
        current_user,
        1,
        100,
        assignment_id,
        student_id,
        status_filter,
        reviewed,
    )
    data = pagination_response(
        [SubmissionResponse.model_validate(SubmissionService.enrich(item)).model_dump(mode="json") for item in items],
        page,
        page_size,
        total_items,
    )
    return success_response("", data)


@router.get("/assignment/{assignment_id}", summary="Assignment submissions")
def assignment_submissions(
    assignment_id: int,
    status_filter: str | None = Query(default=None, alias="status"),
    reviewed: bool | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Return submissions for an assignment."""

    items, total_items, page, page_size = SubmissionService.list_submissions(
        db,
        current_user,
        1,
        100,
        assignment_id,
        None,
        status_filter,
        reviewed,
    )
    data = pagination_response(
        [SubmissionResponse.model_validate(SubmissionService.enrich(item)).model_dump(mode="json") for item in items],
        page,
        page_size,
        total_items,
    )
    return success_response("", data)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Submit assignment")
def submit_assignment(
    payload: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
) -> dict:
    """Submit assignment."""

    submission = SubmissionService.submit_assignment(db, payload, current_user)
    return success_response(
        "Assignment submitted successfully.",
        SubmissionResponse.model_validate(SubmissionService.enrich(submission)).model_dump(mode="json"),
    )


@router.get("/{submission_id}", summary="Get submission")
def get_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return one submission."""

    submission = SubmissionService.ensure_access(db, submission_id, current_user)
    return success_response(
        "",
        SubmissionResponse.model_validate(SubmissionService.enrich(submission)).model_dump(mode="json"),
    )


@router.put("/{submission_id}", summary="Update submission")
def update_submission(
    submission_id: int,
    payload: SubmissionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
) -> dict:
    """Update submission."""

    submission = SubmissionService.update_submission(db, submission_id, payload, current_user)
    return success_response(
        "Submission updated successfully.",
        SubmissionResponse.model_validate(SubmissionService.enrich(submission)).model_dump(mode="json"),
    )


@router.delete("/{submission_id}", summary="Delete submission")
def delete_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Delete submission."""

    SubmissionService.delete_submission(db, submission_id)
    return success_response("Submission deleted successfully.", None)


@router.put("/{submission_id}/review", summary="Review submission")
def review_submission(
    submission_id: int,
    payload: SubmissionReview,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Review submission."""

    submission = SubmissionService.review_submission(db, submission_id, payload, current_user.id)
    return success_response(
        "Submission reviewed successfully.",
        SubmissionResponse.model_validate(SubmissionService.enrich(submission)).model_dump(mode="json"),
    )
