"""ERP/LMS workflow tests."""

from tests.conftest import auth_headers, create_subject, create_user


def _create_student(client, headers, email="student@example.com", roll_number="CSE23002"):
    response = client.post(
        "/api/v1/students",
        headers=headers,
        json={
            "roll_number": roll_number,
            "first_name": "Auto",
            "last_name": "Student",
            "email": email,
            "course": "B.Tech",
            "department": "Computer Science",
            "semester": 5,
            "section": "A",
            "academic_year": "2026-27",
        },
    )
    assert response.status_code == 201
    return response.json()["data"]


def test_student_creation_generates_login_credentials(client, db_session):
    """Teacher-created students automatically receive linked login accounts."""

    create_user(db_session, "teacher@example.com", "teacher")
    headers = auth_headers(client, "teacher@example.com")

    data = _create_student(client, headers)

    credentials = data["generated_credentials"]
    assert data["user_id"] == credentials["user_id"]
    assert data["classroom_id"] is not None

    login = client.post(
        "/api/v1/auth/login",
        json={"email": credentials["email"], "password": credentials["password"]},
    )
    assert login.status_code == 200
    assert login.json()["data"]["user"]["role"] == "student"


def test_student_import_preview_reports_valid_and_invalid_rows(client, db_session):
    """CSV import preview validates rows before commit."""

    create_user(db_session, "teacher@example.com", "teacher")
    headers = auth_headers(client, "teacher@example.com")
    csv_content = (
        "Roll No,First Name,Last Name,Email,Course,Department,Semester,Section\n"
        "CSE23003,Valid,Student,valid@example.com,B.Tech,Computer Science,5,A\n"
        "CSE23004,Invalid,Student,not-an-email,B.Tech,Computer Science,5,A\n"
    )

    response = client.post(
        "/api/v1/students/import/preview",
        headers=headers,
        files={"file": ("students.csv", csv_content, "text/csv")},
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total_rows"] == 2
    assert data["valid_rows"] == 1
    assert data["invalid_rows"] == 1


def test_bulk_attendance_marks_classroom_sheet(client, db_session):
    """Teachers can save attendance for an entire classroom."""

    create_user(db_session, "teacher@example.com", "teacher")
    subject = create_subject(db_session)
    headers = auth_headers(client, "teacher@example.com")
    student = _create_student(client, headers)

    sheet = client.get(
        f"/api/v1/attendance/classroom/{student['classroom_id']}/sheet",
        headers=headers,
        params={"subject_id": subject.id, "attendance_date": "2026-07-01"},
    )
    assert sheet.status_code == 200
    assert len(sheet.json()["data"]["students"]) == 1

    response = client.post(
        "/api/v1/attendance/bulk",
        headers=headers,
        json={
            "classroom_id": student["classroom_id"],
            "subject_id": subject.id,
            "attendance_date": "2026-07-01",
            "records": [{"student_id": student["id"], "status": "Present"}],
        },
    )

    assert response.status_code == 201
    assert response.json()["data"]["saved"] == 1


def test_assignment_question_grading_calculates_totals(client, db_session):
    """Teacher grading question-wise marks calculates total, percentage, and grade."""

    create_user(db_session, "teacher@example.com", "teacher")
    subject = create_subject(db_session)
    teacher_headers = auth_headers(client, "teacher@example.com")
    student = _create_student(client, teacher_headers)
    credentials = student["generated_credentials"]

    assignment_response = client.post(
        "/api/v1/assignments",
        headers=teacher_headers,
        json={
            "classroom_id": student["classroom_id"],
            "subject_id": subject.id,
            "title": "Question-wise Assignment",
            "description": "Solve both questions.",
            "assigned_date": "2026-07-01",
            "due_date": "2026-07-20",
            "questions": [
                {"question_no": 1, "title": "Q1", "max_marks": 5},
                {"question_no": 2, "title": "Q2", "max_marks": 10},
            ],
        },
    )
    assert assignment_response.status_code == 201
    assignment = assignment_response.json()["data"]

    student_login = client.post(
        "/api/v1/auth/login",
        json={"email": credentials["email"], "password": credentials["password"]},
    )
    student_headers = {"Authorization": f"Bearer {student_login.json()['data']['access_token']}"}
    submission_response = client.post(
        "/api/v1/submissions",
        headers=student_headers,
        json={"assignment_id": assignment["id"], "submitted_file": "/uploads/solution.pdf"},
    )
    assert submission_response.status_code == 201
    submission_id = submission_response.json()["data"]["id"]

    review = client.put(
        f"/api/v1/submissions/{submission_id}/review",
        headers=teacher_headers,
        json={
            "status": "Reviewed",
            "feedback": "Strong work.",
            "question_scores": [
                {"question_id": assignment["questions"][0]["id"], "obtained_marks": 4},
                {"question_id": assignment["questions"][1]["id"], "obtained_marks": 8},
            ],
        },
    )

    assert review.status_code == 200
    data = review.json()["data"]
    assert data["total_marks"] == 12.0
    assert data["percentage"] == 80.0
    assert data["grade"] == "A"


def test_student_uploads_solution_and_assignment_status_updates(client, db_session):
    """Student portal uploads a file and reflects the submission status."""

    create_user(db_session, "teacher@example.com", "teacher")
    subject = create_subject(db_session)
    teacher_headers = auth_headers(client, "teacher@example.com")
    student = _create_student(client, teacher_headers, "portal-student@example.com", "CSE23009")
    credentials = student["generated_credentials"]

    assignment_response = client.post(
        "/api/v1/assignments",
        headers=teacher_headers,
        json={
            "classroom_id": student["classroom_id"],
            "subject_id": subject.id,
            "title": "Portal Upload Assignment",
            "description": "Upload the solved file.",
            "assigned_date": "2026-07-01",
            "due_date": "2026-07-20",
            "total_marks": 20,
        },
    )
    assert assignment_response.status_code == 201
    assignment = assignment_response.json()["data"]

    student_login = client.post(
        "/api/v1/auth/login",
        json={"email": credentials["email"], "password": credentials["password"]},
    )
    student_headers = {"Authorization": f"Bearer {student_login.json()['data']['access_token']}"}

    upload = client.post(
        "/api/v1/submissions/upload",
        headers=student_headers,
        files={"file": ("solution.pdf", b"%PDF-1.4\nstudent solution", "application/pdf")},
    )
    assert upload.status_code == 201
    uploaded_file = upload.json()["data"]["file_url"]
    assert uploaded_file.startswith("/uploads/submissions/student_")

    submission_response = client.post(
        "/api/v1/submissions",
        headers=student_headers,
        json={
            "assignment_id": assignment["id"],
            "submitted_file": uploaded_file,
            "submission_notes": "Please review the uploaded answer sheet.",
        },
    )
    assert submission_response.status_code == 201
    submission = submission_response.json()["data"]
    assert submission["submitted_file"] == uploaded_file

    detail = client.get(f"/api/v1/assignments/{assignment['id']}", headers=student_headers)
    assert detail.status_code == 200
    data = detail.json()["data"]
    assert data["my_submission_id"] == submission["id"]
    assert data["submission_status"] == "Submitted"
    assert data["submission_file"] == uploaded_file
