"""Classroom database model."""

from sqlalchemy import Boolean, Column, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.user import utc_now


class Classroom(Base):
    """Academic class grouping for ERP/LMS workflows."""

    __tablename__ = "classrooms"
    __table_args__ = (
        UniqueConstraint(
            "department",
            "course",
            "semester",
            "section",
            "academic_year",
            name="uq_classroom_academic_group",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    classroom_code = Column(String(80), unique=True, nullable=False, index=True)
    classroom_name = Column(String(150), nullable=False)
    department = Column(String(100), nullable=False, index=True)
    course = Column(String(100), nullable=False, index=True)
    semester = Column(Integer, nullable=False, index=True)
    section = Column(String(10), nullable=False, index=True)
    academic_year = Column(String(20), nullable=False, index=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    students = relationship("Student", back_populates="classroom")
    subjects = relationship("Subject", back_populates="classroom")
    assignments = relationship("Assignment", back_populates="classroom")
    attendance_records = relationship("Attendance", back_populates="classroom")
    marks_records = relationship("Marks", back_populates="classroom")
