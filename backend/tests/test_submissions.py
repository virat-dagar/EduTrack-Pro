"""Submission API tests."""

from datetime import date

from app.models.assignment import Assignment
from tests.conftest import auth_headers, create_student_profile, create_subject, create_user


def test_student_submission_and_teacher_review(client, db_session):
    """Students submit assignments and teachers review them."""

    teacher = create_user(db_session, "teacher@example.com", "teacher")
    student_user = create_user(db_session, "student@example.com", "student", "Student User")
    create_student_profile(db_session, student_user)
    subject = create_subject(db_session)
    assignment = Assignment(
        subject_id=subject.id,
        title="SQL Assignment",
        description="Write SQL queries.",
        total_marks=25,
        assigned_date=date(2026, 7, 1),
        due_date=date(2026, 7, 20),
        created_by=teacher.id,
        is_active=True,
    )
    db_session.add(assignment)
    db_session.commit()
    db_session.refresh(assignment)

    student_headers = auth_headers(client, "student@example.com")
    response = client.post(
        "/api/v1/submissions",
        headers=student_headers,
        json={
            "assignment_id": assignment.id,
            "submitted_file": "/uploads/submissions/student_1/sql-assignment.pdf",
            "submission_notes": "Done",
        },
    )
    assert response.status_code == 201
    submission_id = response.json()["data"]["id"]

    teacher_headers = auth_headers(client, "teacher@example.com")
    review = client.put(
        f"/api/v1/submissions/{submission_id}/review",
        headers=teacher_headers,
        json={"status": "Reviewed", "feedback": "Good work."},
    )
    assert review.status_code == 200
    assert review.json()["data"]["feedback"] == "Good work."
