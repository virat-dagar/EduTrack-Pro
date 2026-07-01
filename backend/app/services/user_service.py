"""User service."""

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.exceptions import ConflictError, NotFoundError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.helpers import apply_sorting, normalize_pagination, paginate_query
from app.utils.validators import normalize_email


class UserService:
    """Business logic for user accounts."""

    allowed_sort_fields = {"full_name", "email", "created_at", "role", "id"}

    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        """Return a user by ID."""

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise NotFoundError("User not found.")
        return user

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        """Return a user by email."""

        return db.query(User).filter(User.email == normalize_email(email)).first()

    @staticmethod
    def list_users(
        db: Session,
        page: int = 1,
        page_size: int = 20,
        q: str | None = None,
        role: str | None = None,
        is_active: bool | None = None,
        sort: str | None = "full_name",
        order: str = "asc",
    ) -> tuple[list[User], int, int, int]:
        """Return filtered and paginated users."""

        safe_page, safe_page_size = normalize_pagination(page, page_size)
        query = db.query(User)
        if q:
            search = f"%{q.strip()}%"
            query = query.filter(or_(User.full_name.ilike(search), User.email.ilike(search)))
        if role:
            query = query.filter(User.role == role)
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        query = apply_sorting(query, User, sort, order, UserService.allowed_sort_fields)
        items, total_items = paginate_query(query, safe_page, safe_page_size)
        return items, total_items, safe_page, safe_page_size

    @staticmethod
    def create_user(db: Session, payload: UserCreate) -> User:
        """Create a user with a hashed password."""

        email = normalize_email(str(payload.email))
        if UserService.get_by_email(db, email):
            raise ConflictError("Email already exists.")
        user = User(
            full_name=payload.full_name.strip(),
            email=email,
            password_hash=hash_password(payload.password),
            role=payload.role,
            is_active=payload.is_active,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_user(db: Session, user_id: int, payload: UserUpdate) -> User:
        """Update user profile fields."""

        user = UserService.get_user(db, user_id)
        data = payload.model_dump(exclude_unset=True)
        if "email" in data and data["email"] is not None:
            email = normalize_email(str(data["email"]))
            existing = UserService.get_by_email(db, email)
            if existing and existing.id != user.id:
                raise ConflictError("Email already exists.")
            data["email"] = email
        for field, value in data.items():
            setattr(user, field, value)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> None:
        """Delete a user when no dependent academic data would be orphaned."""

        user = UserService.get_user(db, user_id)
        if (
            user.student_profile
            or user.attendance_marked
            or user.marks_entered
            or user.assignments_created
            or user.submissions_reviewed
        ):
            raise ConflictError("User cannot be deleted while related records exist.")
        db.delete(user)
        db.commit()

    @staticmethod
    def set_active(db: Session, user_id: int, is_active: bool) -> User:
        """Activate or deactivate a user."""

        user = UserService.get_user(db, user_id)
        user.is_active = is_active
        db.commit()
        db.refresh(user)
        return user
