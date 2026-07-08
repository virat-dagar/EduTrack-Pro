"""Local development seed data."""

from datetime import date

from app.core.security import hash_password
from app.database.init_db import create_database
from app.database.database import SessionLocal
from app.models.assignment import Assignment
from app.models.assignment_question import AssignmentQuestion
from app.models.classroom import Classroom
from app.models.student import Student
from app.models.subject import Subject
from app.models.user import User
from app.schemas.classroom import ClassroomCreate
from app.services.classroom_service import ClassroomService


def seed_demo_data() -> None:
    """Create deterministic local demo accounts and academic records."""

    create_database()
    db = SessionLocal()
    try:
        teacher = db.query(User).filter(User.email == "teacher@example.com").first()
        if teacher is None:
            teacher = User(
                full_name="Demo Teacher",
                email="teacher@example.com",
                password_hash=hash_password("Password123"),
                role="teacher",
                is_active=True,
            )
            db.add(teacher)
            db.commit()
            db.refresh(teacher)
        else:
            # Force-reset credentials in case a stale db has a different
            # password from an earlier run (e.g. an old committed db file).
            teacher.password_hash = hash_password("Password123")
            teacher.role = "teacher"
            teacher.is_active = True
            db.commit()

        student_user = db.query(User).filter(User.email == "student@example.com").first()
        if student_user is None:
            student_user = User(
                full_name="Demo Student",
                email="student@example.com",
                password_hash=hash_password("Password123"),
                role="student",
                is_active=True,
            )
            db.add(student_user)
            db.commit()
            db.refresh(student_user)
        else:
            student_user.password_hash = hash_password("Password123")
            student_user.role = "student"
            student_user.is_active = True
            db.commit()

        student = db.query(Student).filter(Student.user_id == student_user.id).first()
        classroom = (
            db.query(Classroom)
            .filter(
                Classroom.department == "Computer Science",
                Classroom.course == "B.Tech",
                Classroom.semester == 5,
                Classroom.section == "A",
                Classroom.academic_year == "2026-27",
            )
            .first()
        )
        if classroom is None:
            classroom = ClassroomService.create_classroom(
                db,
                ClassroomCreate(
                    department="Computer Science",
                    course="B.Tech",
                    semester=5,
                    section="A",
                    academic_year="2026-27",
                ),
            )

        if student is None:
            student = Student(
                user_id=student_user.id,
                classroom_id=classroom.id,
                roll_number="CSE23001",
                enrollment_number="2026CSE001",
                first_name="Demo",
                last_name="Student",
                date_of_birth=date(2005, 5, 15),
                gender="Other",
                email="student@example.com",
                phone="9876543210",
                course="B.Tech",
                department="Computer Science",
                semester=5,
                section="A",
                academic_year="2026-27",
                admission_date=date(2026, 7, 1),
                is_active=True,
            )
            db.add(student)
        elif student.classroom_id is None:
            student.classroom_id = classroom.id

        subject = db.query(Subject).filter(Subject.subject_code == "CS301").first()
        if subject is None:
            subject = Subject(
                classroom_id=classroom.id,
                subject_code="CS301",
                subject_name="Database Management Systems",
                course="B.Tech",
                department="Computer Science",
                semester=5,
                credits=4,
                description="Relational databases, SQL, normalization, indexing, and transactions.",
                is_active=True,
            )
            db.add(subject)
            db.commit()
            db.refresh(subject)
        elif subject.classroom_id is None:
            subject.classroom_id = classroom.id

        assignment = db.query(Assignment).filter(Assignment.title == "Normalization Assignment").first()
        if assignment is None:
            assignment = Assignment(
                classroom_id=classroom.id,
                subject_id=subject.id,
                title="Normalization Assignment",
                description="Solve normalization exercises for the database design module.",
                pdf_file="/demo/normalization-assignment.pdf",
                total_marks=20,
                assigned_date=date.today(),
                due_date=date(date.today().year, 12, 31),
                created_by=teacher.id,
                is_published=True,
                is_active=True,
            )
            assignment.questions = [
                AssignmentQuestion(question_no=1, title="Normal Forms", max_marks=5),
                AssignmentQuestion(question_no=2, title="Dependency Analysis", max_marks=5),
                AssignmentQuestion(question_no=3, title="Schema Decomposition", max_marks=10),
            ]
            db.add(assignment)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()
    print("Demo data ready: teacher@example.com / Password123 and student@example.com / Password123")