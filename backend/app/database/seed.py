"""Local development seed data."""

from datetime import date

from app.core.security import hash_password
from app.database.init_db import create_database
from app.database.database import SessionLocal
from app.models.assignment import Assignment
from app.models.student import Student
from app.models.subject import Subject
from app.models.user import User


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

        student = db.query(Student).filter(Student.user_id == student_user.id).first()
        if student is None:
            student = Student(
                user_id=student_user.id,
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

        subject = db.query(Subject).filter(Subject.subject_code == "CS301").first()
        if subject is None:
            subject = Subject(
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

        assignment = db.query(Assignment).filter(Assignment.title == "Normalization Assignment").first()
        if assignment is None:
            db.add(
                Assignment(
                    subject_id=subject.id,
                    title="Normalization Assignment",
                    description="Solve normalization exercises for the database design module.",
                    total_marks=20,
                    assigned_date=date.today(),
                    due_date=date(date.today().year, 12, 31),
                    created_by=teacher.id,
                    is_active=True,
                )
            )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()
    print("Demo data ready: teacher@example.com / Password123 and student@example.com / Password123")
