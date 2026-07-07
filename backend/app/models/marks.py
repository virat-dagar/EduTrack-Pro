"""Marks database model."""

from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.user import utc_now


class Marks(Base):
    """Academic marks record."""

    __tablename__ = "marks"
    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "subject_id",
            "assessment_type",
            "examination_date",
            name="uq_marks_student_subject_assessment_date",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    assessment_type = Column(String(50), nullable=False, index=True)
    marks_obtained = Column(Float, nullable=False)
    maximum_marks = Column(Float, nullable=False)
    examination_date = Column(Date, nullable=False, index=True)
    remarks = Column(Text, nullable=True)
    entered_by = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    classroom = relationship("Classroom", back_populates="marks_records")
    student = relationship("Student", back_populates="marks_records")
    subject = relationship("Subject", back_populates="marks_records")
    teacher = relationship("User", back_populates="marks_entered", foreign_keys=[entered_by])
