"""Attendance API tests."""

from tests.conftest import auth_headers, create_student_profile, create_subject, create_user


def test_attendance_marking_and_duplicate_rejection(client, db_session):
    """Attendance can be marked once per student, subject, and date."""

    create_user(db_session, "teacher@example.com", "teacher")
    student_user = create_user(db_session, "student@example.com", "student", "Student User")
    student = create_student_profile(db_session, student_user)
    subject = create_subject(db_session)
    headers = auth_headers(client, "teacher@example.com")
    payload = {
        "student_id": student.id,
        "subject_id": subject.id,
        "attendance_date": "2026-07-01",
        "status": "Present",
        "remarks": "On time",
    }

    response = client.post("/api/v1/attendance", headers=headers, json=payload)
    assert response.status_code == 201

    duplicate = client.post("/api/v1/attendance", headers=headers, json=payload)
    assert duplicate.status_code == 409

    percentage = client.get(f"/api/v1/attendance/percentage/{student.id}", headers=headers)
    assert percentage.status_code == 200
    assert percentage.json()["data"]["attendance_percentage"] == 100.0
