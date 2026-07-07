"""Subject database model."""

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.user import utc_now


class Subject(Base):
    """Academic subject."""

    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=True, index=True)
    subject_code = Column(String(20), unique=True, nullable=False, index=True)
    subject_name = Column(String(100), nullable=False, index=True)
    course = Column(String(100), nullable=False, index=True)
    department = Column(String(100), nullable=False, index=True)
    semester = Column(Integer, nullable=False, index=True)
    credits = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    classroom = relationship("Classroom", back_populates="subjects")
    attendance_records = relationship("Attendance", back_populates="subject")
    marks_records = relationship("Marks", back_populates="subject")
    assignments = relationship("Assignment", back_populates="subject")
