"""Attendance router."""

from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_teacher
from app.database.session import get_db
from app.models.user import User
from app.schemas.attendance import AttendanceBulkCreate, AttendanceCreate, AttendanceResponse, AttendanceUpdate
from app.services.attendance_service import AttendanceService
from app.services.student_service import StudentService
from app.utils.response import pagination_response, success_response

router = APIRouter(prefix="/api/v1/attendance", tags=["Attendance"])


@router.get("", summary="List attendance")
def list_attendance(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    student_id: int | None = None,
    subject_id: int | None = None,
    classroom_id: int | None = None,
    semester: int | None = None,
    status: str | None = None,
    attendance_date: date | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    sort: str | None = "attendance_date",
    order: str = "desc",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return attendance records."""

    items, total_items, safe_page, safe_page_size = AttendanceService.list_records(
        db,
        current_user,
        page,
        page_size,
        student_id,
        subject_id,
        classroom_id,
        semester,
        status,
        attendance_date,
        start_date,
        end_date,
        sort,
        order,
    )
    data = pagination_response(
        [AttendanceResponse.model_validate(item).model_dump(mode="json") for item in items],
        safe_page,
        safe_page_size,
        total_items,
    )
    return success_response("", data)


@router.get("/summary", summary="Attendance summary")
def attendance_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Return attendance statistics."""

    return success_response("", AttendanceService.summary(db))


@router.get("/analytics", summary="Attendance analytics")
def attendance_analytics(
    classroom_id: int | None = None,
    subject_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Return attendance analytics."""

    return success_response("", AttendanceService.analytics(db, classroom_id, subject_id))


@router.get("/at-risk", summary="At-risk attendance students")
def at_risk_students(
    threshold: float = Query(75.0, ge=0, le=100),
    classroom_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Return students below attendance threshold."""

    return success_response("", AttendanceService.at_risk_students(db, threshold, classroom_id))


@router.get("/classroom/{classroom_id}/sheet", summary="Classroom attendance sheet")
def classroom_attendance_sheet(
    classroom_id: int,
    subject_id: int,
    attendance_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Load classroom students for bulk attendance marking."""

    return success_response("", AttendanceService.classroom_sheet(db, classroom_id, subject_id, attendance_date))


@router.post("/bulk", status_code=status.HTTP_201_CREATED, summary="Bulk mark attendance")
def bulk_mark_attendance(
    payload: AttendanceBulkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Create or update attendance for a classroom."""

    return success_response("Bulk attendance saved successfully.", AttendanceService.mark_bulk(db, payload, current_user.id))


@router.get("/percentage/{student_id}", summary="Attendance percentage")
def attendance_percentage(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return attendance percentage for a student."""

    StudentService.ensure_access(db, student_id, current_user)
    return success_response(
        "",
        {
            "student_id": student_id,
            "attendance_percentage": AttendanceService.percentage(db, student_id),
        },
    )


@router.get("/student/{student_id}", summary="Student attendance")
def student_attendance(
    student_id: int,
    subject_id: int | None = None,
    semester: int | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return attendance history for one student."""

    StudentService.ensure_access(db, student_id, current_user)
    items, total_items, page, page_size = AttendanceService.list_records(
        db,
        current_user,
        1,
        100,
        student_id,
        subject_id,
        None,
        semester,
        None,
        None,
        start_date,
        end_date,
    )
    data = pagination_response(
        [AttendanceResponse.model_validate(item).model_dump(mode="json") for item in items],
        page,
        page_size,
        total_items,
    )
    return success_response("", data)


@router.get("/subject/{subject_id}", summary="Subject attendance")
def subject_attendance(
    subject_id: int,
    attendance_date: date | None = None,
    semester: int | None = None,
    status_filter: str | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Return attendance for one subject."""

    items, total_items, page, page_size = AttendanceService.list_records(
        db,
        current_user,
        1,
        100,
        None,
        subject_id,
        None,
        semester,
        status_filter,
        attendance_date,
    )
    data = pagination_response(
        [AttendanceResponse.model_validate(item).model_dump(mode="json") for item in items],
        page,
        page_size,
        total_items,
    )
    return success_response("", data)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Mark attendance")
def mark_attendance(
    payload: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Mark attendance."""

    record = AttendanceService.mark_attendance(db, payload, current_user.id)
    return success_response(
        "Attendance marked successfully.",
        AttendanceResponse.model_validate(record).model_dump(mode="json"),
    )


@router.get("/{attendance_id}", summary="Get attendance")
def get_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return one attendance record."""

    record = AttendanceService.get_record(db, attendance_id)
    StudentService.ensure_access(db, record.student_id, current_user)
    return success_response("", AttendanceResponse.model_validate(record).model_dump(mode="json"))


@router.put("/{attendance_id}", summary="Update attendance")
def update_attendance(
    attendance_id: int,
    payload: AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Update attendance."""

    record = AttendanceService.update_attendance(db, attendance_id, payload)
    return success_response(
        "Attendance updated successfully.",
        AttendanceResponse.model_validate(record).model_dump(mode="json"),
    )


@router.delete("/{attendance_id}", summary="Delete attendance")
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Delete attendance."""

    AttendanceService.delete_attendance(db, attendance_id)
    return success_response("Attendance deleted successfully.", None)
