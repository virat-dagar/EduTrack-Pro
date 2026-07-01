"""Authentication schemas."""

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.schemas.user import UserResponse
from app.utils.validators import normalize_email


class LoginRequest(BaseModel):
    """Login request body."""

    email: EmailStr
    password: str = Field(..., min_length=1)

    @field_validator("email")
    @classmethod
    def clean_email(cls, value: EmailStr) -> str:
        return normalize_email(str(value))


class LoginResponse(BaseModel):
    """Login response data."""

    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    user: UserResponse


class CurrentUserResponse(UserResponse):
    """Current user response."""
