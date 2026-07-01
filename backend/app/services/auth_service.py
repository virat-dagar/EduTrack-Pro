"""Authentication service."""

from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.exceptions import AuthenticationError
from app.models.user import User


class AuthService:
    """Authentication workflows."""

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> tuple[User, str, int]:
        """Authenticate a user and issue a JWT."""

        user = db.query(User).filter(User.email == email).first()
        if user is None or not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid email or password.")
        if not user.is_active:
            raise AuthenticationError("User account is inactive.")
        token, expires_in = create_access_token(
            subject=str(user.id),
            email=user.email,
            role=user.role,
        )
        return user, token, expires_in
