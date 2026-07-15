"""Assignments router."""

from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_teacher
from app.database.session import get_db
from app.models.user import User
from app.schemas.assignment import (
    AssignmentCreate,
    AssignmentResponse,
    AssignmentUpdate,
)
from app.services.assignment_service import AssignmentService
from app.utils.response import pagination_response, success_response

router = APIRouter(prefix="/api/v1/assignments", tags=["Assignments"])


@router.post(
    "/upload", status_code=status.HTTP_201_CREATED, summary="Upload assignment file"
)
def upload_assignment_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Upload a PDF/attachment for an assignment, teacher-only."""

    return success_response(
        "Assignment file uploaded successfully.",
        AssignmentService.save_uploaded_file(db, file, current_user),
    )


@router.get("", summary="List assignments")
def list_assignments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return assignments."""

    items, total_items, safe_page, safe_page_size = AssignmentService.list_assignments(
        db,
        current_user,
        page,
        page_size,
        q,
        subject_id,
        classroom_id,
        teacher_id,
        semester,
        course,
        department,
        is_active,
        sort,
        order,
    )
    data = pagination_response(
        [
            AssignmentResponse.model_validate(
                AssignmentService.enrich_for_user(db, item, current_user)
            ).model_dump(mode="json")
            for item in items
        ],
        safe_page,
        safe_page_size,
        total_items,
    )
    return success_response("", data)


@router.get("/upcoming", summary="Upcoming assignments")
def upcoming_assignments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return upcoming assignments."""

    items = AssignmentService.upcoming(db, current_user)
    return success_response(
        "",
        [
            AssignmentResponse.model_validate(
                AssignmentService.enrich_for_user(db, item, current_user)
            ).model_dump(mode="json")
            for item in items
        ],
    )


@router.get("/overdue", summary="Overdue assignments")
def overdue_assignments(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Return overdue assignments."""

    items = AssignmentService.overdue(db)
    return success_response(
        "",
        [
            AssignmentResponse.model_validate(
                AssignmentService.enrich(item)
            ).model_dump(mode="json")
            for item in items
        ],
    )


@router.get("/subject/{subject_id}", summary="Subject assignments")
def subject_assignments(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return assignments for one subject."""

    items, total_items, page, page_size = AssignmentService.list_assignments(
        db,
        current_user,
        subject_id=subject_id,
        page_size=100,
    )
    data = pagination_response(
        [
            AssignmentResponse.model_validate(
                AssignmentService.enrich_for_user(db, item, current_user)
            ).model_dump(mode="json")
            for item in items
        ],
        page,
        page_size,
        total_items,
    )
    return success_response("", data)


@router.get("/teacher/{teacher_id}", summary="Teacher assignments")
def teacher_assignments(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Return assignments created by a teacher."""

    items, total_items, page, page_size = AssignmentService.list_assignments(
        db,
        current_user,
        teacher_id=teacher_id,
        page_size=100,
    )
    data = pagination_response(
        [
            AssignmentResponse.model_validate(
                AssignmentService.enrich(item)
            ).model_dump(mode="json")
            for item in items
        ],
        page,
        page_size,
        total_items,
    )
    return success_response("", data)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Create assignment")
def create_assignment(
    payload: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Create assignment."""

    assignment = AssignmentService.create_assignment(db, payload, current_user.id)
    return success_response(
        "Assignment created successfully.",
        AssignmentResponse.model_validate(
            AssignmentService.enrich(assignment)
        ).model_dump(mode="json"),
    )


@router.get("/{assignment_id}", summary="Get assignment")
def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return one assignment."""

    assignment = AssignmentService.get_assignment(db, assignment_id)
    return success_response(
        "",
        AssignmentResponse.model_validate(
            AssignmentService.enrich_for_user(db, assignment, current_user)
        ).model_dump(mode="json"),
    )


@router.put("/{assignment_id}/publish", summary="Publish assignment")
def publish_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Publish assignment to its target classroom."""

    assignment = AssignmentService.publish(db, assignment_id)
    return success_response(
        "Assignment published successfully.",
        AssignmentResponse.model_validate(
            AssignmentService.enrich(assignment)
        ).model_dump(mode="json"),
    )


@router.get(
    "/{assignment_id}/submissions/summary", summary="Assignment submission summary"
)
def assignment_submission_summary(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Return assignment submission totals."""

    return success_response("", AssignmentService.submission_summary(db, assignment_id))


@router.put("/{assignment_id}", summary="Update assignment")
def update_assignment(
    assignment_id: int,
    payload: AssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Update assignment."""

    assignment = AssignmentService.update_assignment(db, assignment_id, payload)
    return success_response(
        "Assignment updated successfully.",
        AssignmentResponse.model_validate(
            AssignmentService.enrich(assignment)
        ).model_dump(mode="json"),
    )


@router.delete("/{assignment_id}", summary="Delete assignment")
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Delete assignment."""

    AssignmentService.delete_assignment(db, assignment_id)
    return success_response("Assignment deleted successfully.", None)
