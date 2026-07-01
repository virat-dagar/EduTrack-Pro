"""User database model."""

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


def utc_now() -> datetime:
    """Return the current UTC timestamp."""

    return datetime.now(timezone.utc)


class User(Base):
    """Authenticated user account."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, index=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    student_profile = relationship("Student", back_populates="user", uselist=False)
    attendance_marked = relationship(
        "Attendance",
        back_populates="teacher",
        foreign_keys="Attendance.marked_by",
    )
    marks_entered = relationship(
        "Marks",
        back_populates="teacher",
        foreign_keys="Marks.entered_by",
    )
    assignments_created = relationship(
        "Assignment",
        back_populates="teacher",
        foreign_keys="Assignment.created_by",
    )
    submissions_reviewed = relationship(
        "Submission",
        back_populates="reviewer",
        foreign_keys="Submission.reviewed_by",
    )
