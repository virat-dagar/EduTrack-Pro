"""Users router."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_teacher
from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService
from app.utils.response import pagination_response, success_response

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("", summary="List users")
def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = None,
    role: str | None = None,
    is_active: bool | None = None,
    sort: str | None = "full_name",
    order: str = "asc",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Return paginated users."""

    items, total_items, safe_page, safe_page_size = UserService.list_users(
        db,
        page,
        page_size,
        q,
        role,
        is_active,
        sort,
        order,
    )
    data = pagination_response(
        [UserResponse.model_validate(item).model_dump(mode="json") for item in items],
        safe_page,
        safe_page_size,
        total_items,
    )
    return success_response("", data)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Create user")
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Create a user account."""

    user = UserService.create_user(db, payload)
    return success_response(
        "User created successfully.",
        UserResponse.model_validate(user).model_dump(mode="json"),
    )


@router.get("/{user_id}", summary="Get user")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Return one user."""

    user = UserService.get_user(db, user_id)
    return success_response("", UserResponse.model_validate(user).model_dump(mode="json"))


@router.put("/{user_id}", summary="Update user")
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Update user fields."""

    user = UserService.update_user(db, user_id, payload)
    return success_response(
        "User updated successfully.",
        UserResponse.model_validate(user).model_dump(mode="json"),
    )


@router.delete("/{user_id}", summary="Delete user")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Delete a user."""

    UserService.delete_user(db, user_id)
    return success_response("User deleted successfully.", None)


@router.put("/{user_id}/activate", summary="Activate user")
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Activate a user."""

    user = UserService.set_active(db, user_id, True)
    return success_response(
        "User activated successfully.",
        UserResponse.model_validate(user).model_dump(mode="json"),
    )


@router.put("/{user_id}/deactivate", summary="Deactivate user")
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
) -> dict:
    """Deactivate a user."""

    user = UserService.set_active(db, user_id, False)
    return success_response(
        "User deactivated successfully.",
        UserResponse.model_validate(user).model_dump(mode="json"),
    )
