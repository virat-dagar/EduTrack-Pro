"""Subjects router."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_teacher
from app.database.session import get_db
from app.models.user import User
from app.schemas.subject import SubjectCreate, SubjectResponse, SubjectUpdate
from app.services.subject_service import SubjectService
from app.utils.response import pagination_response, success_response

router = APIRouter(prefix="/api/v1/subjects", tags=["Subjects"])


@router.get("", summary="List subjects")
def list_subjects(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = None,
    course: str | None = None,
    department: str | None = None,
    classroom_id: int | None = None,
    semester: int | None = None,
    credits: int | None = None,
    is_active: bool | None = None,
    sort: str | None = "subject_name",
    order: str = "asc",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return subjects."""

    items, total_items, safe_page, safe_page_size = SubjectService.list_subjects(
        db,
        page,
        page_size,
        q,
        course,
        department,
        classroom_id,
        semester,
        credits,
        is_active,
        sort,
        order,
    )
    data = pagination_response(
        [SubjectResponse.model_validate(item).model_dump(mode="json") for item in items],
        safe_page,
        safe_page_size,
        total_items,
    )
    return success_response("", data)


@router.get("/search", summary="Search subjects")
def search_subjects(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = None,
    course: str | None = None,
    department: str | None = None,
    classroom_id: int | None = None,
    semester: int | None = None,
    credits: int | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Advanced subject search."""

    items, total_items, safe_page, safe_page_size = SubjectService.list_subjects(
        db,
        page,
        page_size,
        q,
        course,
        department,
        classroom_id,
        semester,
        credits,
        is_active,
    )
    data = pagination_response(
        [SubjectResponse.model_validate(item).model_dump(mode="json") for item in items],
        safe_page,
        safe_page_size,
        total_items,
    )
    return success_response("", data)


@router.get("/course/{course}", summary="Subjects by course")
def subjects_by_course(
    course: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return subjects for a course."""

    items, total_items, page, page_size = SubjectService.list_subjects(db, course=course, page_size=100)
    data = pagination_response(
        [SubjectResponse.model_validate(item).model_dump(mode="json") for item in items],
        page,
        page_size,
        total_items,
    )
    return success_response("", data)


@router.get("/semester/{semester}", summary="Subjects by semester")
def subjects_by_semester(
    semester: int,
    course: str | None = None,
    department: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return subjects for a semester."""

    items, total_items, page, page_size = SubjectService.list_subjects(
        db,
        semester=semester,
        course=course,
        department=department,
        page_size=100,
    )
    data = pagination_response(
        [SubjectResponse.model_validate(item).model_dump(mode="json") for item in items],
        page,
        page_size,
        total_items,
    )
    return success_response("", data)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Create subject")
def create_subject(
    payload: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Create a subject."""

    subject = SubjectService.create_subject(db, payload)
    return success_response(
        "Subject created successfully.",
        SubjectResponse.model_validate(subject).model_dump(mode="json"),
    )


@router.get("/{subject_id}", summary="Get subject")
def get_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return one subject."""

    subject = SubjectService.get_subject(db, subject_id)
    return success_response("", SubjectResponse.model_validate(subject).model_dump(mode="json"))


@router.put("/{subject_id}", summary="Update subject")
def update_subject(
    subject_id: int,
    payload: SubjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Update a subject."""

    subject = SubjectService.update_subject(db, subject_id, payload)
    return success_response(
        "Subject updated successfully.",
        SubjectResponse.model_validate(subject).model_dump(mode="json"),
    )


@router.delete("/{subject_id}", summary="Delete subject")
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Delete a subject."""

    SubjectService.delete_subject(db, subject_id)
    return success_response("Subject deleted successfully.", None)
