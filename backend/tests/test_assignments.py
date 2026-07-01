"""Assignment API tests."""

from tests.conftest import auth_headers, create_subject, create_user


def test_assignment_crud(client, db_session):
    """Teachers can create and update assignments."""

    create_user(db_session, "teacher@example.com", "teacher")
    subject = create_subject(db_session)
    headers = auth_headers(client, "teacher@example.com")

    response = client.post(
        "/api/v1/assignments",
        headers=headers,
        json={
            "subject_id": subject.id,
            "title": "SQL Assignment",
            "description": "Write SQL queries.",
            "total_marks": 25,
            "assigned_date": "2026-07-01",
            "due_date": "2026-07-20",
        },
    )
    assert response.status_code == 201
    assignment_id = response.json()["data"]["id"]

    update = client.put(
        f"/api/v1/assignments/{assignment_id}",
        headers=headers,
        json={"title": "Advanced SQL Assignment"},
    )
    assert update.status_code == 200
    assert update.json()["data"]["title"] == "Advanced SQL Assignment"
