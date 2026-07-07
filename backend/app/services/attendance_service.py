"""Attendance service."""

from datetime import date

from sqlalchemy.orm import Session

from app.exceptions import ConflictError, NotFoundError
from app.models.attendance import Attendance
from app.models.classroom import Classroom
from app.models.student import Student
from app.models.subject import Subject
from app.models.user import User
from app.schemas.attendance import AttendanceBulkCreate, AttendanceCreate, AttendanceUpdate
from app.services.student_service import StudentService
from app.utils.constants import ATTENDANCE_ABSENT, ATTENDANCE_LATE, ATTENDANCE_PRESENT, ROLE_STUDENT
from app.utils.helpers import apply_sorting, normalize_pagination, paginate_query


class AttendanceService:
    """Business logic for attendance records."""

    allowed_sort_fields = {"attendance_date", "student_id", "subject_id", "status", "id"}

    @staticmethod
    def get_record(db: Session, attendance_id: int) -> Attendance:
        """Return one attendance record."""

        record = db.query(Attendance).filter(Attendance.id == attendance_id).first()
        if record is None:
            raise NotFoundError("Attendance record not found.")
        return record

    @staticmethod
    def list_records(
        db: Session,
        current_user: User,
        page: int = 1,
        page_size: int = 20,
        student_id: int | None = None,
        subject_id: int | None = None,
        classroom_id: int | None = None,
        semester: int | None = None,
        status: str | None = None,
        attendance_date: date | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        sort: str | None = "attendance_date",
        order: str = "desc",
    ) -> tuple[list[Attendance], int, int, int]:
        """Return filtered and paginated attendance records."""

        safe_page, safe_page_size = normalize_pagination(page, page_size)
        query = db.query(Attendance).join(Student)
        if current_user.role == ROLE_STUDENT:
            student = StudentService.get_student_by_user(db, current_user.id)
            query = query.filter(Attendance.student_id == student.id)
        if student_id:
            query = query.filter(Attendance.student_id == student_id)
        if subject_id:
            query = query.filter(Attendance.subject_id == subject_id)
        if classroom_id:
            query = query.filter(Attendance.classroom_id == classroom_id)
        if semester:
            query = query.filter(Student.semester == semester)
        if status:
            query = query.filter(Attendance.status == status)
        if attendance_date:
            query = query.filter(Attendance.attendance_date == attendance_date)
        if start_date:
            query = query.filter(Attendance.attendance_date >= start_date)
        if end_date:
            query = query.filter(Attendance.attendance_date <= end_date)
        query = apply_sorting(query, Attendance, sort, order, AttendanceService.allowed_sort_fields)
        items, total_items = paginate_query(query, safe_page, safe_page_size)
        return items, total_items, safe_page, safe_page_size

    @staticmethod
    def mark_attendance(db: Session, payload: AttendanceCreate, teacher_id: int) -> Attendance:
        """Create an attendance record."""

        student = AttendanceService._validate_student_subject(db, payload.student_id, payload.subject_id)
        duplicate = (
            db.query(Attendance)
            .filter(
                Attendance.student_id == payload.student_id,
                Attendance.subject_id == payload.subject_id,
                Attendance.attendance_date == payload.attendance_date,
            )
            .first()
        )
        if duplicate:
            raise ConflictError("Attendance already marked for this student, subject, and date.")
        data = payload.model_dump()
        data["classroom_id"] = data.get("classroom_id") or student.classroom_id
        record = Attendance(**data, marked_by=teacher_id)
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def update_attendance(db: Session, attendance_id: int, payload: AttendanceUpdate) -> Attendance:
        """Update attendance status and remarks."""

        record = AttendanceService.get_record(db, attendance_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(record, field, value)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def delete_attendance(db: Session, attendance_id: int) -> None:
        """Delete an attendance record."""

        record = AttendanceService.get_record(db, attendance_id)
        db.delete(record)
        db.commit()

    @staticmethod
    def percentage(db: Session, student_id: int) -> float:
        """Calculate attendance percentage for a student."""

        total = db.query(Attendance).filter(Attendance.student_id == student_id).count()
        present = (
            db.query(Attendance)
            .filter(Attendance.student_id == student_id, Attendance.status == ATTENDANCE_PRESENT)
            .count()
        )
        return round((present / total) * 100, 2) if total else 0.0

    @staticmethod
    def classroom_sheet(
        db: Session,
        classroom_id: int,
        subject_id: int,
        attendance_date: date,
    ) -> dict[str, object]:
        """Return students and existing attendance for a classroom/date."""

        classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
        if classroom is None:
            raise NotFoundError("Classroom not found.")
        if db.query(Subject).filter(Subject.id == subject_id).first() is None:
            raise NotFoundError("Subject not found.")
        students = (
            db.query(Student)
            .filter(Student.classroom_id == classroom_id, Student.is_active.is_(True))
            .order_by(Student.roll_number.asc())
            .all()
        )
        existing = {
            record.student_id: record
            for record in db.query(Attendance)
            .filter(
                Attendance.classroom_id == classroom_id,
                Attendance.subject_id == subject_id,
                Attendance.attendance_date == attendance_date,
            )
            .all()
        }
        return {
            "classroom": {
                "id": classroom.id,
                "classroom_code": classroom.classroom_code,
                "classroom_name": classroom.classroom_name,
                "department": classroom.department,
                "course": classroom.course,
                "semester": classroom.semester,
                "section": classroom.section,
            },
            "subject_id": subject_id,
            "attendance_date": attendance_date,
            "students": [
                {
                    "student_id": student.id,
                    "roll_number": student.roll_number,
                    "name": f"{student.first_name} {student.last_name}",
                    "status": existing.get(student.id).status if student.id in existing else ATTENDANCE_PRESENT,
                    "remarks": existing.get(student.id).remarks if student.id in existing else None,
                    "attendance_id": existing.get(student.id).id if student.id in existing else None,
                }
                for student in students
            ],
        }

    @staticmethod
    def mark_bulk(db: Session, payload: AttendanceBulkCreate, teacher_id: int) -> dict[str, object]:
        """Create or update attendance records for a classroom sheet."""

        if db.query(Classroom).filter(Classroom.id == payload.classroom_id).first() is None:
            raise NotFoundError("Classroom not found.")
        if db.query(Subject).filter(Subject.id == payload.subject_id).first() is None:
            raise NotFoundError("Subject not found.")

        saved = 0
        updated = 0
        skipped: list[dict[str, object]] = []
        valid_student_ids = {
            student.id
            for student in db.query(Student)
            .filter(Student.classroom_id == payload.classroom_id, Student.is_active.is_(True))
            .all()
        }
        for item in payload.records:
            if item.student_id not in valid_student_ids:
                skipped.append({"student_id": item.student_id, "reason": "Student is not in this classroom."})
                continue
            existing = (
                db.query(Attendance)
                .filter(
                    Attendance.student_id == item.student_id,
                    Attendance.subject_id == payload.subject_id,
                    Attendance.attendance_date == payload.attendance_date,
                )
                .first()
            )
            if existing:
                existing.status = item.status
                existing.remarks = item.remarks
                existing.classroom_id = payload.classroom_id
                existing.marked_by = teacher_id
                updated += 1
            else:
                db.add(
                    Attendance(
                        classroom_id=payload.classroom_id,
                        student_id=item.student_id,
                        subject_id=payload.subject_id,
                        attendance_date=payload.attendance_date,
                        status=item.status,
                        remarks=item.remarks,
                        marked_by=teacher_id,
                    )
                )
                saved += 1
        db.commit()
        return {
            "saved": saved,
            "updated": updated,
            "skipped": len(skipped),
            "skipped_rows": skipped,
        }

    @staticmethod
    def summary(db: Session) -> dict[str, int]:
        """Return attendance summary counts."""

        return {
            "total_records": db.query(Attendance).count(),
            "present": db.query(Attendance).filter(Attendance.status == ATTENDANCE_PRESENT).count(),
            "absent": db.query(Attendance).filter(Attendance.status == ATTENDANCE_ABSENT).count(),
            "late": db.query(Attendance).filter(Attendance.status == ATTENDANCE_LATE).count(),
        }

    @staticmethod
    def analytics(
        db: Session,
        classroom_id: int | None = None,
        subject_id: int | None = None,
    ) -> dict[str, object]:
        """Return attendance analytics for dashboards."""

        query = db.query(Attendance)
        if classroom_id:
            query = query.filter(Attendance.classroom_id == classroom_id)
        if subject_id:
            query = query.filter(Attendance.subject_id == subject_id)
        records = query.all()
        total = len(records)
        present = len([record for record in records if record.status == ATTENDANCE_PRESENT])
        absent = len([record for record in records if record.status == ATTENDANCE_ABSENT])
        late = len([record for record in records if record.status == ATTENDANCE_LATE])
        percentage = round((present / total) * 100, 2) if total else 0.0
        subject_rows = []
        subject_ids = sorted({record.subject_id for record in records})
        for current_subject_id in subject_ids:
            subject_records = [record for record in records if record.subject_id == current_subject_id]
            subject_present = len([record for record in subject_records if record.status == ATTENDANCE_PRESENT])
            subject_total = len(subject_records)
            subject = db.query(Subject).filter(Subject.id == current_subject_id).first()
            subject_rows.append(
                {
                    "subject_id": current_subject_id,
                    "subject": subject.subject_name if subject else None,
                    "attendance_percentage": round((subject_present / subject_total) * 100, 2)
                    if subject_total
                    else 0.0,
                    "total_records": subject_total,
                }
            )
        return {
            "total_records": total,
            "present": present,
            "absent": absent,
            "late": late,
            "attendance_percentage": percentage,
            "subject_wise": subject_rows,
        }

    @staticmethod
    def at_risk_students(db: Session, threshold: float = 75.0, classroom_id: int | None = None) -> dict[str, object]:
        """Return students whose attendance is below the threshold."""

        student_query = db.query(Student).filter(Student.is_active.is_(True))
        if classroom_id:
            student_query = student_query.filter(Student.classroom_id == classroom_id)
        items = []
        for student in student_query.order_by(Student.roll_number.asc()).all():
            percentage = AttendanceService.percentage(db, student.id)
            if percentage < threshold:
                items.append(
                    {
                        "student_id": student.id,
                        "roll_number": student.roll_number,
                        "name": f"{student.first_name} {student.last_name}",
                        "classroom_id": student.classroom_id,
                        "attendance_percentage": percentage,
                    }
                )
        return {
            "threshold": threshold,
            "count": len(items),
            "items": items,
        }

    @staticmethod
    def _validate_student_subject(db: Session, student_id: int, subject_id: int) -> Student:
        """Validate attendance relationships."""

        student = db.query(Student).filter(Student.id == student_id).first()
        if student is None:
            raise NotFoundError("Student not found.")
        if db.query(Subject).filter(Subject.id == subject_id).first() is None:
            raise NotFoundError("Subject not found.")
        return student
