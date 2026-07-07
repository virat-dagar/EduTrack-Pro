"""Student schemas."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.utils.constants import GENDERS
from app.utils.validators import ensure_not_future, normalize_email, normalize_text, validate_phone


class StudentBase(BaseModel):
    """Shared student fields."""

    user_id: int | None = None
    classroom_id: int | None = None
    roll_number: str = Field(..., min_length=1, max_length=30)
    enrollment_number: str | None = Field(default=None, min_length=1, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    date_of_birth: date = Field(default_factory=lambda: date(2000, 1, 1))
    gender: str = "Other"
    email: EmailStr
    phone: str = "0000000000"
    course: str = Field(..., min_length=1, max_length=100)
    department: str = Field(..., min_length=1, max_length=100)
    semester: int = Field(..., ge=1)
    section: str | None = Field(default=None, max_length=10)
    academic_year: str = Field(default="2026-27", min_length=4, max_length=20)
    admission_date: date = Field(default_factory=date.today)
    profile_photo: str | None = Field(default=None, max_length=255)
    is_active: bool = True

    @field_validator(
        "roll_number",
        "enrollment_number",
        "first_name",
        "last_name",
        "course",
        "department",
        "academic_year",
        "section",
        mode="before",
    )
    @classmethod
    def clean_text(cls, value: str | None) -> str | None:
        return normalize_text(value) if isinstance(value, str) else value

    @field_validator("email")
    @classmethod
    def clean_email(cls, value: EmailStr) -> str:
        return normalize_email(str(value))

    @field_validator("phone")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        return validate_phone(value)

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, value: str) -> str:
        if value not in GENDERS:
            raise ValueError("Gender must be Male, Female, or Other.")
        return value

    @field_validator("date_of_birth")
    @classmethod
    def validate_birth_date(cls, value: date) -> date:
        ensure_not_future(value, "Date of birth")
        return value


class StudentCreate(StudentBase):
    """Create student request."""


class StudentUpdate(BaseModel):
    """Update student request."""

    first_name: str | None = Field(default=None, min_length=1, max_length=50)
    last_name: str | None = Field(default=None, min_length=1, max_length=50)
    date_of_birth: date | None = None
    gender: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    course: str | None = Field(default=None, min_length=1, max_length=100)
    classroom_id: int | None = None
    department: str | None = Field(default=None, min_length=1, max_length=100)
    semester: int | None = Field(default=None, ge=1)
    section: str | None = Field(default=None, max_length=10)
    academic_year: str | None = Field(default=None, min_length=4, max_length=20)
    profile_photo: str | None = Field(default=None, max_length=255)
    is_active: bool | None = None

    @field_validator("email")
    @classmethod
    def clean_optional_email(cls, value: EmailStr | None) -> str | None:
        return normalize_email(str(value)) if value is not None else value

    @field_validator("phone")
    @classmethod
    def validate_optional_phone(cls, value: str | None) -> str | None:
        return validate_phone(value) if value is not None else value

    @field_validator("gender")
    @classmethod
    def validate_optional_gender(cls, value: str | None) -> str | None:
        if value is not None and value not in GENDERS:
            raise ValueError("Gender must be Male, Female, or Other.")
        return value

    @field_validator("date_of_birth")
    @classmethod
    def validate_optional_birth_date(cls, value: date | None) -> date | None:
        if value is not None:
            ensure_not_future(value, "Date of birth")
        return value


class StudentResponse(BaseModel):
    """Student response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    classroom_id: int | None = None
    roll_number: str
    enrollment_number: str
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    email: EmailStr
    phone: str
    course: str
    department: str
    semester: int
    section: str | None = None
    academic_year: str
    admission_date: date
    profile_photo: str | None = None
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None
    generated_credentials: dict[str, str | int] | None = None


class StudentListResponse(BaseModel):
    """Paginated student response."""

    items: list[StudentResponse]
    page: int
    page_size: int
    total_items: int
    total_pages: int


class StudentImportRow(BaseModel):
    """Normalized student import row."""

    row_number: int | None = None
    roll_number: str = Field(..., min_length=1, max_length=30)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    course: str = Field(..., min_length=1, max_length=100)
    department: str = Field(..., min_length=1, max_length=100)
    semester: int = Field(..., ge=1)
    section: str | None = Field(default="A", max_length=10)
    enrollment_number: str | None = Field(default=None, max_length=50)
    phone: str = "0000000000"
    gender: str = "Other"
    date_of_birth: date = Field(default_factory=lambda: date(2000, 1, 1))
    academic_year: str = Field(default="2026-27", min_length=4, max_length=20)
    admission_date: date = Field(default_factory=date.today)
    classroom_id: int | None = None

    @field_validator("email")
    @classmethod
    def clean_import_email(cls, value: EmailStr) -> str:
        return normalize_email(str(value))

    @field_validator("phone")
    @classmethod
    def validate_import_phone(cls, value: str) -> str:
        return validate_phone(value)


class StudentImportCommit(BaseModel):
    """Commit validated student import rows."""

    rows: list[StudentImportRow]
    import_valid_only: bool = True
