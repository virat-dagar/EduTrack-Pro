"""Marks router."""

from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_teacher
from app.database.session import get_db
from app.models.user import User
from app.schemas.marks import MarksCreate, MarksResponse, MarksUpdate
from app.services.marks_service import MarksService
from app.services.student_service import StudentService
from app.utils.response import pagination_response, success_response

router = APIRouter(prefix="/api/v1/marks", tags=["Marks"])


@router.get("", summary="List marks")
def list_marks(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = None,
    student_id: int | None = None,
    subject_id: int | None = None,
    assessment_type: str | None = None,
    semester: int | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    sort: str | None = "examination_date",
    order: str = "desc",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return marks records."""

    items, total_items, safe_page, safe_page_size = MarksService.list_records(
        db,
        current_user,
        page,
        page_size,
        q,
        student_id,
        subject_id,
        assessment_type,
        semester,
        start_date,
        end_date,
        sort,
        order,
    )
    data = pagination_response(
        [MarksResponse.model_validate(MarksService.enrich(item)).model_dump(mode="json") for item in items],
        safe_page,
        safe_page_size,
        total_items,
    )
    return success_response("", data)


@router.get("/summary", summary="Marks summary")
def marks_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Return marks statistics."""

    return success_response("", MarksService.summary(db))


@router.get("/average/{student_id}", summary="Student marks average")
def marks_average(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return student average marks."""

    StudentService.ensure_access(db, student_id, current_user)
    return success_response("", MarksService.average(db, student_id))


@router.get("/student/{student_id}", summary="Student marks")
def student_marks(
    student_id: int,
    subject_id: int | None = None,
    semester: int | None = None,
    assessment_type: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return marks for one student."""

    StudentService.ensure_access(db, student_id, current_user)
    items, total_items, page, page_size = MarksService.list_records(
        db,
        current_user,
        1,
        100,
        None,
        student_id,
        subject_id,
        assessment_type,
        semester,
    )
    data = pagination_response(
        [MarksResponse.model_validate(MarksService.enrich(item)).model_dump(mode="json") for item in items],
        page,
        page_size,
        total_items,
    )
    return success_response("", data)


@router.get("/subject/{subject_id}", summary="Subject marks")
def subject_marks(
    subject_id: int,
    assessment_type: str | None = None,
    semester: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Return marks for one subject."""

    items, total_items, page, page_size = MarksService.list_records(
        db,
        current_user,
        1,
        100,
        None,
        None,
        subject_id,
        assessment_type,
        semester,
    )
    data = pagination_response(
        [MarksResponse.model_validate(MarksService.enrich(item)).model_dump(mode="json") for item in items],
        page,
        page_size,
        total_items,
    )
    return success_response("", data)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Add marks")
def add_marks(
    payload: MarksCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Add marks."""

    record = MarksService.add_marks(db, payload, current_user.id)
    return success_response(
        "Marks added successfully.",
        MarksResponse.model_validate(MarksService.enrich(record)).model_dump(mode="json"),
    )


@router.get("/{marks_id}", summary="Get marks")
def get_marks(
    marks_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return one marks record."""

    record = MarksService.get_record(db, marks_id)
    StudentService.ensure_access(db, record.student_id, current_user)
    return success_response(
        "",
        MarksResponse.model_validate(MarksService.enrich(record)).model_dump(mode="json"),
    )


@router.put("/{marks_id}", summary="Update marks")
def update_marks(
    marks_id: int,
    payload: MarksUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Update marks."""

    record = MarksService.update_marks(db, marks_id, payload)
    return success_response(
        "Marks updated successfully.",
        MarksResponse.model_validate(MarksService.enrich(record)).model_dump(mode="json"),
    )


@router.delete("/{marks_id}", summary="Delete marks")
def delete_marks(
    marks_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Delete marks."""

    MarksService.delete_marks(db, marks_id)
    return success_response("Marks deleted successfully.", None)
