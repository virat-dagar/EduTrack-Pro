"""FastAPI dependencies for authentication and authorization."""

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database.session import get_db
from app.exceptions import AuthenticationError, AuthorizationError
from app.models.user import User
from app.utils.constants import ROLE_STUDENT, ROLE_TEACHER

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Validate JWT credentials and return the active current user."""

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AuthenticationError("Authentication token is missing.")
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload.get("sub", 0))
    except (TypeError, ValueError):
        raise AuthenticationError("Invalid authentication token.") from None

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise AuthenticationError("Invalid authentication token.")
    if not user.is_active:
        raise AuthenticationError("User account is inactive.")
    return user


def require_teacher(current_user: User = Depends(get_current_user)) -> User:
    """Require the current user to be a teacher."""

    if current_user.role != ROLE_TEACHER:
        raise AuthorizationError("Teacher access is required.")
    return current_user


def require_student(current_user: User = Depends(get_current_user)) -> User:
    """Require the current user to be a student."""

    if current_user.role != ROLE_STUDENT:
        raise AuthorizationError("Student access is required.")
    return current_user


def ensure_teacher_or_owner(current_user: User, owner_user_id: int) -> None:
    """Allow teachers or the owning student user."""

    if current_user.role == ROLE_TEACHER:
        return
    if current_user.id != owner_user_id:
        raise AuthorizationError("You may only access your own academic records.")
