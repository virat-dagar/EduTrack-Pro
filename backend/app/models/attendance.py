"""Attendance database model."""

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.user import utc_now


class Attendance(Base):
    """Daily attendance record for one student and subject."""

    __tablename__ = "attendance"
    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "subject_id",
            "attendance_date",
            name="uq_attendance_student_subject_date",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    attendance_date = Column(Date, nullable=False, index=True)
    status = Column(String(20), nullable=False, index=True)
    remarks = Column(Text, nullable=True)
    marked_by = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    classroom = relationship("Classroom", back_populates="attendance_records")
    student = relationship("Student", back_populates="attendance_records")
    subject = relationship("Subject", back_populates="attendance_records")
    teacher = relationship("User", back_populates="attendance_marked", foreign_keys=[marked_by])
