"""Backend test fixtures."""

from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import hash_password
from app.database.base import Base, import_models
from app.database.session import get_db
from app.main import app
from app.models.student import Student
from app.models.subject import Subject
from app.models.user import User

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import_models()


def override_get_db():
    """Yield a test database session."""

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_database():
    """Reset test tables before each test."""

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """FastAPI test client."""

    return TestClient(app)


@pytest.fixture
def db_session():
    """Direct database session for arranging test data."""

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_user(db, email: str, role: str = "teacher", full_name: str = "Test User") -> User:
    """Create a test user."""

    user = User(
        full_name=full_name,
        email=email,
        password_hash=hash_password("Password123"),
        role=role,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def auth_headers(client: TestClient, email: str) -> dict[str, str]:
    """Login and return authorization headers."""

    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "Password123"},
    )
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_student_profile(db, user: User) -> Student:
    """Create a test student profile."""

    student = Student(
        user_id=user.id,
        roll_number="CSE23001",
        enrollment_number="2026CSE001",
        first_name="Test",
        last_name="Student",
        date_of_birth=date(2005, 1, 1),
        gender="Other",
        email=user.email,
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
    db.commit()
    db.refresh(student)
    return student


def create_subject(db) -> Subject:
    """Create a test subject."""

    subject = Subject(
        subject_code="CS301",
        subject_name="Database Management Systems",
        course="B.Tech",
        department="Computer Science",
        semester=5,
        credits=4,
        description="Databases and SQL.",
        is_active=True,
    )
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject
