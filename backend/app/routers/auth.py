"""Authentication router."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService
from app.utils.response import success_response

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/login", summary="Login user")
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> dict:
    """Authenticate a user and issue a JWT."""

    user, token, expires_in = AuthService.authenticate_user(db, payload.email, payload.password)
    data = LoginResponse(
        access_token=token,
        expires_in=expires_in,
        user=UserResponse.model_validate(user),
    ).model_dump(mode="json")
    return success_response("Login successful.", data)


@router.get("/me", summary="Current authenticated user")
def get_me(current_user: User = Depends(get_current_user)) -> dict:
    """Return the authenticated user."""

    data = UserResponse.model_validate(current_user).model_dump(mode="json")
    return success_response("", data)
