"""Student API tests."""

from tests.conftest import auth_headers, create_student_profile, create_user


def test_teacher_can_create_student(client, db_session):
    """Teachers can create student profiles."""

    create_user(db_session, "teacher@example.com", "teacher")
    student_user = create_user(db_session, "student@example.com", "student", "Student User")
    headers = auth_headers(client, "teacher@example.com")

    response = client.post(
        "/api/v1/students",
        headers=headers,
        json={
            "user_id": student_user.id,
            "roll_number": "CSE23001",
            "enrollment_number": "2026CSE001",
            "first_name": "Test",
            "last_name": "Student",
            "date_of_birth": "2005-01-01",
            "gender": "Other",
            "email": "student@example.com",
            "phone": "9876543210",
            "course": "B.Tech",
            "department": "Computer Science",
            "semester": 5,
            "section": "A",
            "academic_year": "2026-27",
            "admission_date": "2026-07-01",
            "is_active": True,
        },
    )

    assert response.status_code == 201
    assert response.json()["data"]["roll_number"] == "CSE23001"


def test_student_can_only_access_own_profile(client, db_session):
    """Students cannot list all student profiles."""

    create_user(db_session, "teacher@example.com", "teacher")
    student_user = create_user(db_session, "student@example.com", "student", "Student User")
    create_student_profile(db_session, student_user)
    headers = auth_headers(client, "student@example.com")

    list_response = client.get("/api/v1/students", headers=headers)
    assert list_response.status_code == 403

    me_response = client.get("/api/v1/students/me", headers=headers)
    assert me_response.status_code == 200
    assert me_response.json()["data"]["email"] == "student@example.com"
