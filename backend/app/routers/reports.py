"""Reports router."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_teacher
from app.database.session import get_db
from app.models.user import User
from app.services.report_service import ReportService
from app.utils.response import success_response

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])


@router.get("/student/{student_id}", summary="Student academic report")
def student_report(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Generate student report."""

    return success_response("", ReportService.student_report(db, student_id, current_user))


@router.get("/attendance", summary="Attendance report")
def attendance_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Generate attendance report."""

    return success_response("", ReportService.attendance_report(db))


@router.get("/marks", summary="Marks report")
def marks_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Generate marks report."""

    return success_response("", ReportService.marks_report(db))


@router.get("/assignments", summary="Assignment report")
def assignment_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Generate assignment report."""

    return success_response("", ReportService.assignment_report(db))


@router.get("/performance", summary="Performance report")
def performance_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Generate performance report."""

    return success_response("", ReportService.performance_report(db))


@router.get("/institution", summary="Institution summary")
def institution_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Generate institution report."""

    return success_response("", ReportService.institution_report(db))
