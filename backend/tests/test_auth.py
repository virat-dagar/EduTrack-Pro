"""Authentication tests."""

from tests.conftest import auth_headers, create_user


def test_login_and_current_user(client, db_session):
    """Users can login and fetch their current profile."""

    create_user(db_session, "teacher@example.com", "teacher", "Teacher User")

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "teacher@example.com", "password": "Password123"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["data"]["user"]["role"] == "teacher"

    me = client.get("/api/v1/auth/me", headers=auth_headers(client, "teacher@example.com"))
    assert me.status_code == 200
    assert me.json()["data"]["email"] == "teacher@example.com"


def test_login_rejects_invalid_credentials(client, db_session):
    """Invalid credentials return a standardized 401 error."""

    create_user(db_session, "teacher@example.com", "teacher")

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "teacher@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["success"] is False
