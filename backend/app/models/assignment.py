"""Assignment database model."""

from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.user import utc_now


class Assignment(Base):
    """Teacher-created academic assignment."""

    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    title = Column(String(150), nullable=False, index=True)
    description = Column(Text, nullable=False)
    total_marks = Column(Float, nullable=False)
    assigned_date = Column(Date, nullable=False, index=True)
    due_date = Column(Date, nullable=False, index=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    subject = relationship("Subject", back_populates="assignments")
    teacher = relationship("User", back_populates="assignments_created", foreign_keys=[created_by])
    submissions = relationship("Submission", back_populates="assignment")
