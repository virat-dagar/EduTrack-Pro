"""Subject API tests."""

from tests.conftest import auth_headers, create_user


def test_subject_crud(client, db_session):
    """Teachers can create, update, list, and delete subjects."""

    create_user(db_session, "teacher@example.com", "teacher")
    headers = auth_headers(client, "teacher@example.com")

    create_response = client.post(
        "/api/v1/subjects",
        headers=headers,
        json={
            "subject_code": "CS301",
            "subject_name": "Database Management Systems",
            "course": "B.Tech",
            "department": "Computer Science",
            "semester": 5,
            "credits": 4,
            "description": "Databases.",
            "is_active": True,
        },
    )
    assert create_response.status_code == 201
    subject_id = create_response.json()["data"]["id"]

    update_response = client.put(
        f"/api/v1/subjects/{subject_id}",
        headers=headers,
        json={"credits": 5},
    )
    assert update_response.status_code == 200
    assert update_response.json()["data"]["credits"] == 5

    list_response = client.get("/api/v1/subjects", headers=headers)
    assert list_response.status_code == 200
    assert list_response.json()["data"]["total_items"] == 1

    delete_response = client.delete(f"/api/v1/subjects/{subject_id}", headers=headers)
    assert delete_response.status_code == 200
