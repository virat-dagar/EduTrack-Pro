"""User API tests."""

from tests.conftest import auth_headers, create_user


def test_teacher_can_create_and_list_users(client, db_session):
    """Teachers can manage users."""

    create_user(db_session, "teacher@example.com", "teacher")
    headers = auth_headers(client, "teacher@example.com")

    response = client.post(
        "/api/v1/users",
        headers=headers,
        json={
            "full_name": "Student User",
            "email": "student@example.com",
            "password": "Password123",
            "role": "student",
            "is_active": True,
        },
    )

    assert response.status_code == 201
    assert response.json()["data"]["email"] == "student@example.com"

    list_response = client.get("/api/v1/users", headers=headers)
    assert list_response.status_code == 200
    assert list_response.json()["data"]["total_items"] == 2


def test_duplicate_email_is_rejected(client, db_session):
    """Duplicate emails return conflict."""

    create_user(db_session, "teacher@example.com", "teacher")
    headers = auth_headers(client, "teacher@example.com")

    payload = {
        "full_name": "Duplicate",
        "email": "duplicate@example.com",
        "password": "Password123",
        "role": "student",
        "is_active": True,
    }
    assert client.post("/api/v1/users", headers=headers, json=payload).status_code == 201
    response = client.post("/api/v1/users", headers=headers, json=payload)
    assert response.status_code == 409
