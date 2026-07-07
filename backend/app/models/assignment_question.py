"""Assignment question database model."""

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.user import utc_now


class AssignmentQuestion(Base):
    """Question-level marks configuration for an assignment."""

    __tablename__ = "assignment_questions"
    __table_args__ = (
        UniqueConstraint(
            "assignment_id",
            "question_no",
            name="uq_assignment_question_no",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False, index=True)
    question_no = Column(Integer, nullable=False, index=True)
    title = Column(String(150), nullable=True)
    description = Column(Text, nullable=True)
    max_marks = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    assignment = relationship("Assignment", back_populates="questions")
    grades = relationship("SubmissionGrade", back_populates="question")
