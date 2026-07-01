"""Marks API tests."""

from tests.conftest import auth_headers, create_student_profile, create_subject, create_user


def test_marks_average_and_grade(client, db_session):
    """Marks are stored and average/grade are calculated."""

    create_user(db_session, "teacher@example.com", "teacher")
    student_user = create_user(db_session, "student@example.com", "student", "Student User")
    student = create_student_profile(db_session, student_user)
    subject = create_subject(db_session)
    headers = auth_headers(client, "teacher@example.com")

    response = client.post(
        "/api/v1/marks",
        headers=headers,
        json={
            "student_id": student.id,
            "subject_id": subject.id,
            "assessment_type": "Mid Semester",
            "marks_obtained": 45,
            "maximum_marks": 50,
            "examination_date": "2026-07-01",
            "remarks": "Strong work",
        },
    )
    assert response.status_code == 201
    assert response.json()["data"]["grade"] == "A+"

    average = client.get(f"/api/v1/marks/average/{student.id}", headers=headers)
    assert average.status_code == 200
    assert average.json()["data"]["average_percentage"] == 90.0
    assert average.json()["data"]["grade"] == "A+"
