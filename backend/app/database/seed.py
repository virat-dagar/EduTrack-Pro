"""Local development seed data.

Creates a named demo roster (not real credentials) so the UI has enough
realistic-looking data to work on layout/design with:
  - Teacher: Feroz            feroz@edutrack.com     / Feroz@123
  - Student: Virat Dagar      virat@edutrack.com      / Virat@123
  - Student: Harmeet Bhati    harmeet@edutrack.com    / Harmeet@123
  - Student: Jaaleen Khanna   jaaleen@edutrack.com    / Jaaleen@123
  - Student: Bhavesh Yadav    bhavesh@edutrack.com    / Bhavesh@123
  - Student: Aprajita Mishra  aprajita@edutrack.com   / Aprajita@123
"""

import random
from datetime import date, timedelta

from app.core.security import hash_password
from app.database.init_db import create_database
from app.database.database import SessionLocal
from app.models.assignment import Assignment
from app.models.assignment_question import AssignmentQuestion
from app.models.attendance import Attendance
from app.models.classroom import Classroom
from app.models.marks import Marks
from app.models.student import Student
from app.models.subject import Subject
from app.models.user import User
from app.schemas.classroom import ClassroomCreate
from app.services.classroom_service import ClassroomService

TEACHER = {"full_name": "Feroz", "email": "feroz@edutrack.com", "password": "Feroz@123"}

STUDENTS = [
    {
        "first_name": "Virat",
        "last_name": "Dagar",
        "email": "virat@edutrack.com",
        "password": "Virat@123",
        "roll_number": "CSE23001",
        "enrollment_number": "2026CSE001",
        "dob": date(2005, 3, 12),
        "gender": "Male",
        "phone": "9876543201",
    },
    {
        "first_name": "Harmeet",
        "last_name": "Bhati",
        "email": "harmeet@edutrack.com",
        "password": "Harmeet@123",
        "roll_number": "CSE23002",
        "enrollment_number": "2026CSE002",
        "dob": date(2005, 6, 24),
        "gender": "Male",
        "phone": "9876543202",
    },
    {
        "first_name": "Jaaleen",
        "last_name": "Khanna",
        "email": "jaaleen@edutrack.com",
        "password": "Jaaleen@123",
        "roll_number": "CSE23003",
        "enrollment_number": "2026CSE003",
        "dob": date(2005, 1, 30),
        "gender": "Female",
        "phone": "9876543203",
    },
    {
        "first_name": "Bhavesh",
        "last_name": "Yadav",
        "email": "bhavesh@edutrack.com",
        "password": "Bhavesh@123",
        "roll_number": "CSE23004",
        "enrollment_number": "2026CSE004",
        "dob": date(2005, 9, 8),
        "gender": "Male",
        "phone": "9876543204",
    },
    {
        "first_name": "Aprajita",
        "last_name": "Mishra",
        "email": "aprajita@edutrack.com",
        "password": "Aprajita@123",
        "roll_number": "CSE23005",
        "enrollment_number": "2026CSE005",
        "dob": date(2005, 11, 17),
        "gender": "Female",
        "phone": "9876543205",
    },
]

SUBJECTS = [
    {
        "subject_code": "CS301",
        "subject_name": "Database Management Systems",
        "credits": 4,
        "description": "Relational databases, SQL, normalization, indexing, and transactions.",
    },
    {
        "subject_code": "CS302",
        "subject_name": "Operating Systems",
        "credits": 4,
        "description": "Processes, scheduling, memory management, and concurrency.",
    },
]

# Rough per-student attendance rate, used only to generate believable demo
# data (not randomized per run — fixed seed keeps re-seeds deterministic).
ATTENDANCE_RATE = [0.95, 0.88, 0.7, 0.6, 0.92]
MARKS_PROFILE = [88, 76, 55, 48, 91]  # out of 100, scaled per assessment


def _get_or_create_user(db, *, full_name, email, password, role):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        user = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            role=role,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Force-reset credentials in case a stale db has a different
        # password from an earlier run (e.g. an old committed db file).
        user.full_name = full_name
        user.password_hash = hash_password(password)
        user.role = role
        user.is_active = True
        db.commit()
    return user


def seed_demo_data() -> None:
    """Create the named demo roster and supporting academic records."""

    create_database()
    db = SessionLocal()
    try:
        teacher = _get_or_create_user(
            db,
            full_name=TEACHER["full_name"],
            email=TEACHER["email"],
            password=TEACHER["password"],
            role="teacher",
        )

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

        subjects = []
        for subject_data in SUBJECTS:
            subject = (
                db.query(Subject)
                .filter(Subject.subject_code == subject_data["subject_code"])
                .first()
            )
            if subject is None:
                subject = Subject(
                    classroom_id=classroom.id,
                    subject_code=subject_data["subject_code"],
                    subject_name=subject_data["subject_name"],
                    course="B.Tech",
                    department="Computer Science",
                    semester=5,
                    credits=subject_data["credits"],
                    description=subject_data["description"],
                    is_active=True,
                )
                db.add(subject)
                db.commit()
                db.refresh(subject)
            elif subject.classroom_id is None:
                subject.classroom_id = classroom.id
                db.commit()
            subjects.append(subject)

        students = []
        for index, student_data in enumerate(STUDENTS):
            student_user = _get_or_create_user(
                db,
                full_name=f"{student_data['first_name']} {student_data['last_name']}",
                email=student_data["email"],
                password=student_data["password"],
                role="student",
            )

            student = (
                db.query(Student).filter(Student.user_id == student_user.id).first()
            )
            if student is None:
                student = Student(
                    user_id=student_user.id,
                    classroom_id=classroom.id,
                    roll_number=student_data["roll_number"],
                    enrollment_number=student_data["enrollment_number"],
                    first_name=student_data["first_name"],
                    last_name=student_data["last_name"],
                    date_of_birth=student_data["dob"],
                    gender=student_data["gender"],
                    email=student_data["email"],
                    phone=student_data["phone"],
                    course="B.Tech",
                    department="Computer Science",
                    semester=5,
                    section="A",
                    academic_year="2026-27",
                    admission_date=date(2026, 7, 1),
                    is_active=True,
                )
                db.add(student)
                db.commit()
                db.refresh(student)
            elif student.classroom_id is None:
                student.classroom_id = classroom.id
                db.commit()

            students.append((student, ATTENDANCE_RATE[index], MARKS_PROFILE[index]))

        # Attendance: last 14 weekdays, per student, per subject.
        rng = random.Random(42)
        today = date.today()
        weekdays = []
        cursor = today
        while len(weekdays) < 14:
            cursor -= timedelta(days=1)
            if cursor.weekday() < 5:
                weekdays.append(cursor)

        for student, rate, _ in students:
            for subject in subjects:
                already_seeded = (
                    db.query(Attendance)
                    .filter(
                        Attendance.student_id == student.id,
                        Attendance.subject_id == subject.id,
                    )
                    .first()
                )
                if already_seeded:
                    continue
                for day in weekdays:
                    status = "Present" if rng.random() < rate else "Absent"
                    db.add(
                        Attendance(
                            classroom_id=classroom.id,
                            student_id=student.id,
                            subject_id=subject.id,
                            attendance_date=day,
                            status=status,
                            marked_by=teacher.id,
                        )
                    )
        db.commit()

        # Marks: two assessments per subject, per student.
        assessments = [
            ("Midterm", 50, date(today.year, max(today.month - 2, 1), 15)),
            ("Final", 50, date(today.year, today.month, 1)),
        ]
        for student, _, profile in students:
            for subject in subjects:
                already_seeded = (
                    db.query(Marks)
                    .filter(
                        Marks.student_id == student.id, Marks.subject_id == subject.id
                    )
                    .first()
                )
                if already_seeded:
                    continue
                for assessment_type, max_marks, exam_date in assessments:
                    scored = round(max_marks * (profile / 100) + rng.uniform(-3, 3), 1)
                    scored = max(0, min(max_marks, scored))
                    db.add(
                        Marks(
                            classroom_id=classroom.id,
                            student_id=student.id,
                            subject_id=subject.id,
                            assessment_type=assessment_type,
                            marks_obtained=scored,
                            maximum_marks=max_marks,
                            examination_date=exam_date,
                            entered_by=teacher.id,
                        )
                    )
        db.commit()

        assignment = (
            db.query(Assignment)
            .filter(Assignment.title == "Normalization Assignment")
            .first()
        )
        if assignment is None:
            assignment = Assignment(
                classroom_id=classroom.id,
                subject_id=subjects[0].id,
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
                AssignmentQuestion(
                    question_no=2, title="Dependency Analysis", max_marks=5
                ),
                AssignmentQuestion(
                    question_no=3, title="Schema Decomposition", max_marks=10
                ),
            ]
            db.add(assignment)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()
    print("Demo data ready:")
    print(f"  Teacher: {TEACHER['email']} / {TEACHER['password']}")
    for student_data in STUDENTS:
        print(f"  Student: {student_data['email']} / {student_data['password']}")
