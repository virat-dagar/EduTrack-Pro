"""Students router."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_student, require_teacher
from app.database.session import get_db
from app.models.user import User
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate
from app.services.student_service import StudentService
from app.utils.response import pagination_response, success_response

router = APIRouter(prefix="/api/v1/students", tags=["Students"])


@router.get("", summary="List students")
def list_students(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = None,
    course: str | None = None,
    department: str | None = None,
    semester: int | None = None,
    section: str | None = None,
    academic_year: str | None = None,
    is_active: bool | None = None,
    sort: str | None = "first_name",
    order: str = "asc",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Return paginated students."""

    items, total_items, safe_page, safe_page_size = StudentService.list_students(
        db,
        page,
        page_size,
        q,
        course,
        department,
        semester,
        section,
        academic_year,
        is_active,
        sort,
        order,
    )
    data = pagination_response(
        [StudentResponse.model_validate(item).model_dump(mode="json") for item in items],
        safe_page,
        safe_page_size,
        total_items,
    )
    return success_response("", data)


@router.get("/me", summary="Current student profile")
def get_current_student_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
) -> dict:
    """Return the current student's profile."""

    student = StudentService.get_student_by_user(db, current_user.id)
    return success_response("", StudentResponse.model_validate(student).model_dump(mode="json"))


@router.get("/search", summary="Search students")
def search_students(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = None,
    department: str | None = None,
    course: str | None = None,
    semester: int | None = None,
    section: str | None = None,
    academic_year: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Advanced student search."""

    items, total_items, safe_page, safe_page_size = StudentService.list_students(
        db,
        page,
        page_size,
        q,
        course,
        department,
        semester,
        section,
        academic_year,
        None,
        "first_name",
        "asc",
    )
    data = pagination_response(
        [StudentResponse.model_validate(item).model_dump(mode="json") for item in items],
        safe_page,
        safe_page_size,
        total_items,
    )
    return success_response("", data)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Create student")
def create_student(
    payload: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Create a student profile."""

    student = StudentService.create_student(db, payload)
    return success_response(
        "Student created successfully.",
        StudentResponse.model_validate(student).model_dump(mode="json"),
    )


@router.get("/{student_id}", summary="Get student")
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return a student profile."""

    student = StudentService.ensure_access(db, student_id, current_user)
    return success_response("", StudentResponse.model_validate(student).model_dump(mode="json"))


@router.put("/{student_id}", summary="Update student")
def update_student(
    student_id: int,
    payload: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Update a student profile."""

    student = StudentService.update_student(db, student_id, payload)
    return success_response(
        "Student updated successfully.",
        StudentResponse.model_validate(student).model_dump(mode="json"),
    )


@router.delete("/{student_id}", summary="Delete student")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Delete a student profile."""

    StudentService.delete_student(db, student_id)
    return success_response("Student deleted successfully.", None)
