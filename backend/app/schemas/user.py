"""User schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.utils.constants import USER_ROLES
from app.utils.validators import normalize_email, normalize_text


class UserBase(BaseModel):
    """Shared user fields."""

    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    role: str
    is_active: bool = True

    @field_validator("full_name")
    @classmethod
    def clean_full_name(cls, value: str) -> str:
        return normalize_text(value)

    @field_validator("email")
    @classmethod
    def clean_email(cls, value: str) -> str:
        return normalize_email(str(value))

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        if value not in USER_ROLES:
            raise ValueError("Role must be either teacher or student.")
        return value


class UserCreate(UserBase):
    """Create user request."""

    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseModel):
    """Update user request."""

    full_name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    role: str | None = None
    is_active: bool | None = None

    @field_validator("full_name")
    @classmethod
    def clean_optional_full_name(cls, value: str | None) -> str | None:
        return normalize_text(value) if value is not None else value

    @field_validator("email")
    @classmethod
    def clean_optional_email(cls, value: EmailStr | None) -> str | None:
        return normalize_email(str(value)) if value is not None else value

    @field_validator("role")
    @classmethod
    def validate_optional_role(cls, value: str | None) -> str | None:
        if value is not None and value not in USER_ROLES:
            raise ValueError("Role must be either teacher or student.")
        return value


class UserResponse(BaseModel):
    """User response without sensitive fields."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserListResponse(BaseModel):
    """Paginated user response."""

    items: list[UserResponse]
    page: int
    page_size: int
    total_items: int
    total_pages: int


class UserActivationResponse(BaseModel):
    """User activation response."""

    id: int
    is_active: bool
