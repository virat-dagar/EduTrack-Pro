"""Submission database model."""

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.user import utc_now


class Submission(Base):
    """Student assignment submission."""

    __tablename__ = "submissions"
    __table_args__ = (
        UniqueConstraint(
            "assignment_id",
            "student_id",
            name="uq_submission_assignment_student",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    submission_date = Column(DateTime(timezone=True), nullable=False, default=utc_now, index=True)
    status = Column(String(20), nullable=False, index=True)
    submission_notes = Column(Text, nullable=True)
    attachment_path = Column(String(255), nullable=True)
    submitted_file = Column(String(255), nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    feedback = Column(Text, nullable=True)
    total_marks = Column(Float, nullable=True)
    percentage = Column(Float, nullable=True)
    grade = Column(String(5), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("Student", back_populates="submissions")
    reviewer = relationship("User", back_populates="submissions_reviewed", foreign_keys=[reviewed_by])
    question_grades = relationship(
        "SubmissionGrade",
        back_populates="submission",
        cascade="all, delete-orphan",
    )
