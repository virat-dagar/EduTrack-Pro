"""Classrooms router."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_teacher
from app.database.session import get_db
from app.models.user import User
from app.schemas.classroom import ClassroomCreate, ClassroomResponse, ClassroomUpdate
from app.services.classroom_service import ClassroomService
from app.utils.response import pagination_response, success_response

router = APIRouter(prefix="/api/v1/classrooms", tags=["Classrooms"])


@router.get("", summary="List classrooms")
def list_classrooms(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = None,
    department: str | None = None,
    course: str | None = None,
    semester: int | None = None,
    section: str | None = None,
    academic_year: str | None = None,
    is_active: bool | None = None,
    sort: str | None = "department",
    order: str = "asc",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return classrooms."""

    items, total_items, safe_page, safe_page_size = ClassroomService.list_classrooms(
        db,
        page,
        page_size,
        q,
        department,
        course,
        semester,
        section,
        academic_year,
        is_active,
        sort,
        order,
    )
    data = pagination_response(
        [ClassroomResponse.model_validate(ClassroomService.enrich(item)).model_dump(mode="json") for item in items],
        safe_page,
        safe_page_size,
        total_items,
    )
    return success_response("", data)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Create classroom")
def create_classroom(
    payload: ClassroomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Create classroom."""

    classroom = ClassroomService.create_classroom(db, payload)
    return success_response(
        "Classroom created successfully.",
        ClassroomResponse.model_validate(ClassroomService.enrich(classroom)).model_dump(mode="json"),
    )


@router.get("/{classroom_id}", summary="Get classroom")
def get_classroom(
    classroom_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return one classroom."""

    classroom = ClassroomService.get_classroom(db, classroom_id)
    return success_response(
        "",
        ClassroomResponse.model_validate(ClassroomService.enrich(classroom)).model_dump(mode="json"),
    )


@router.put("/{classroom_id}", summary="Update classroom")
def update_classroom(
    classroom_id: int,
    payload: ClassroomUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Update classroom."""

    classroom = ClassroomService.update_classroom(db, classroom_id, payload)
    return success_response(
        "Classroom updated successfully.",
        ClassroomResponse.model_validate(ClassroomService.enrich(classroom)).model_dump(mode="json"),
    )


@router.delete("/{classroom_id}", summary="Delete classroom")
def delete_classroom(
    classroom_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Delete classroom."""

    ClassroomService.delete_classroom(db, classroom_id)
    return success_response("Classroom deleted successfully.", None)
