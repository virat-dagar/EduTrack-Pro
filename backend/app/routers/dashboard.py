"""Dashboard router."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import require_student, require_teacher
from app.database.session import get_db
from app.models.user import User
from app.services.dashboard_service import DashboardService
from app.utils.response import success_response

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])


@router.get("/teacher", summary="Teacher dashboard")
def teacher_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Return teacher dashboard."""

    return success_response("", DashboardService.teacher_dashboard(db))


@router.get("/teacher/charts", summary="Teacher dashboard charts")
def teacher_charts(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Return teacher dashboard charts."""

    return success_response("", DashboardService.teacher_charts(db))


@router.get("/teacher/activity", summary="Teacher recent activity")
def teacher_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Return teacher activity."""

    return success_response("", {"items": DashboardService.teacher_activity(db)})


@router.get("/student", summary="Student dashboard")
def student_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
) -> dict:
    """Return student dashboard."""

    return success_response("", DashboardService.student_dashboard(db, current_user))


@router.get("/student/charts", summary="Student dashboard charts")
def student_charts(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
) -> dict:
    """Return student dashboard charts."""

    return success_response("", DashboardService.student_charts(db, current_user))


@router.get("/student/activity", summary="Student recent activity")
def student_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
) -> dict:
    """Return student activity."""

    return success_response("", {"items": DashboardService.student_activity(db, current_user)})
