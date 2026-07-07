"""Submission question-wise grade database model."""

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.user import utc_now


class SubmissionGrade(Base):
    """Marks awarded for one question in one submission."""

    __tablename__ = "submission_grades"
    __table_args__ = (
        UniqueConstraint(
            "submission_id",
            "question_id",
            name="uq_submission_grade_question",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("assignment_questions.id"), nullable=False, index=True)
    obtained_marks = Column(Float, nullable=False)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    submission = relationship("Submission", back_populates="question_grades")
    question = relationship("AssignmentQuestion", back_populates="grades")
