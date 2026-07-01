# 35_API_SUBMISSIONS.md

# EduTrack Pro — Submissions API Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Submissions API

---

# Purpose

This document defines every Assignment Submission API endpoint within EduTrack Pro.

The Submissions API manages the complete lifecycle of assignment submissions.

Submission data powers

- Student Dashboard
- Teacher Dashboard
- Assignment Tracking
- Submission Tracking
- Pending Reviews
- Performance Reports
- Assignment Analytics

Submissions are created by students and reviewed by teachers.

---

# Base Route

```
/api/v1/submissions
```

---

# Resource

```
Submission
```

Represents one student's submission for one assignment.

Each Submission belongs to

- One Assignment
- One Student

Each Submission may be reviewed by

- One Teacher

---

# Endpoint Summary

| Method | Endpoint | Purpose |
|---------|----------|----------|
| GET | /submissions | List Submissions |
| GET | /submissions/{id} | Get Submission |
| POST | /submissions | Submit Assignment |
| PUT | /submissions/{id} | Update Submission |
| DELETE | /submissions/{id} | Delete Submission |
| GET | /submissions/student/{student_id} | Student Submissions |
| GET | /submissions/assignment/{assignment_id} | Assignment Submissions |
| GET | /submissions/pending | Pending Reviews |
| PUT | /submissions/{id}/review | Review Submission |

---

# Authentication

Required

Yes

---

# Authorization

Teachers

✓ View all submissions

✓ Review submissions

✓ Delete submissions

Students

✓ Submit assignments

✓ View only their own submissions

✓ Update own submission before deadline

Students may never review submissions.

---

# Endpoint

```
GET /api/v1/submissions
```

Purpose

Return paginated submissions.

---

# Query Parameters

Pagination

```
?page=1

&page_size=20
```

Filtering

```
assignment_id

student_id

status

reviewed

start_date

end_date
```

Sorting

```
?sort=submission_date

&order=desc
```

Search

```
?q=
```

---

# Processing Flow

```
Authenticate

↓

Authorize

↓

Apply Filters

↓

Apply Search

↓

Apply Sorting

↓

Apply Pagination

↓

Return Submissions
```

---

# Successful Response

Status

```
200 OK
```

Example

```json
{
    "success": true,
    "message": "",
    "data": {
        "items": [
            {
                "id": 85,
                "assignment_id": 12,
                "student_id": 8,
                "submission_date": "2026-07-18T14:35:00Z",
                "status": "Submitted",
                "reviewed": false
            }
        ],
        "page": 1,
        "page_size": 20,
        "total_items": 145,
        "total_pages": 8
    }
}
```

---

# Endpoint

```
GET /api/v1/submissions/{id}
```

Purpose

Retrieve one submission.

Teachers

May access any submission.

Students

May access only their own submission.

---

# Successful Response

```
200 OK
```

```json
{
    "success": true,
    "message": "",
    "data": {
        "id": 85,
        "assignment_id": 12,
        "student_id": 8,
        "submission_date": "2026-07-18T14:35:00Z",
        "status": "Submitted",
        "attachment_path": "uploads/assignment12.pdf",
        "feedback": null
    }
}
```

---

# Endpoint

```
POST /api/v1/submissions
```

Purpose

Submit an assignment.

---

# Authorization

Student only.

---

# Request

```json
{
    "assignment_id": 12,
    "submission_notes": "Completed all questions.",
    "attachment_path": "uploads/assignment12.pdf"
}
```

---

# Processing Flow

```
Authenticate

↓

Authorize

↓

Validate Assignment

↓

Verify Deadline

↓

Check Duplicate Submission

↓

Store Submission

↓

Return Success
```

---

# Successful Response

Status

```
201 Created
```

```json
{
    "success": true,
    "message": "Assignment submitted successfully.",
    "data": {
        "id": 85
    }
}
```

---

# Duplicate Submission

Status

```
409 Conflict
```

```json
{
    "success": false,
    "message": "Assignment has already been submitted."
}
```

---

# Endpoint

```
PUT /api/v1/submissions/{id}
```

Purpose

Update submission.

---

# Authorization

Student only.

---

# Editable Fields

```
Submission Notes

Attachment
```

Students may update submissions only before

```
Assignment Due Date
```

After the deadline,

submission becomes read-only unless future resubmission functionality is enabled.

---

# Successful Response

```
200 OK
```

```json
{
    "success": true,
    "message": "Submission updated successfully."
}
```

---

# Endpoint

```
DELETE /api/v1/submissions/{id}
```

Purpose

Delete submission.

Authorization

Teacher only.

Deletion should normally be avoided to preserve academic history.

---

# Successful Response

```
200 OK
```

```json
{
    "success": true,
    "message": "Submission deleted successfully."
}
```

---

# Endpoint

```
GET /api/v1/submissions/student/{student_id}
```

Purpose

Return all submissions made by a student.

Teachers

May access all students.

Students

May access only their own submissions.

---

# Query Parameters

Optional

```
status

assignment_id

reviewed
```

---

# Endpoint

```
GET /api/v1/submissions/assignment/{assignment_id}
```

Purpose

Return all submissions for one assignment.

Teacher only.

---

# Query Parameters

Optional

```
status

reviewed
```

---

# Endpoint

```
GET /api/v1/submissions/pending
```

Purpose

Return submissions awaiting review.

Teacher only.

Used by

Teacher Dashboard

Assignment Analytics

---

# Example Response

```json
{
    "success": true,
    "message": "",
    "data": {
        "pending_reviews": 18,
        "items": []
    }
}
```

---

# Endpoint

```
PUT /api/v1/submissions/{id}/review
```

Purpose

Review submission.

Authorization

Teacher only.

---

# Request

```json
{
    "status": "Reviewed",
    "feedback": "Excellent work. Well documented."
}
```

---

# Processing Flow

```
Authenticate

↓

Authorize

↓

Verify Submission

↓

Update Review

↓

Store Feedback

↓

Return Success
```

---

# Successful Response

```
200 OK
```

```json
{
    "success": true,
    "message": "Submission reviewed successfully."
}
```

---

# Validation Rules

Assignment

Must exist.

Student

Must exist.

Duplicate submissions prohibited.

Submission date

Automatically generated.

Late submissions

Automatically detected.

Status

Allowed values

```
Pending

Submitted

Late

Reviewed
```

---

# Expected Schemas

```
SubmissionCreate

SubmissionUpdate

SubmissionReview

SubmissionResponse

SubmissionListResponse

PendingSubmissionResponse
```

---

# Expected Router

```
routers/submissions.py
```

Responsibilities

- Submission CRUD
- Student Submissions
- Assignment Submissions
- Pending Reviews
- Review Submission

Router contains no business logic.

---

# Expected Service

```
services/submission_service.py
```

Responsibilities

- Submit Assignment
- Update Submission
- Delete Submission
- Review Submission
- Student Submission History
- Assignment Submission History
- Pending Reviews
- Late Submission Detection
- Duplicate Validation

---

# Business Rules

Each Student may submit

One Submission

Per Assignment.

Teachers review submissions.

Students cannot review submissions.

Late submissions should be detected automatically.

Teacher feedback should appear on the Student Dashboard.

Submission statistics should automatically update dashboards.

---

# Search

Support

```
Student

Assignment

Status
```

Case insensitive.

---

# Filters

Support

```
Assignment

Student

Status

Reviewed

Date Range
```

Multiple filters should be combinable.

---

# Sorting

Support

```
Submission Date

Student

Assignment

Status
```

Ascending and descending.

---

# Security

Teachers

Full access.

Students

Access only their own submissions.

Ownership validation must occur on every student endpoint.

Submission review restricted to Teachers.

---

# Swagger Documentation

Every endpoint should include

- Summary
- Description
- Authentication
- Authorization
- Request Schema
- Response Schema
- Error Responses
- Examples

---

# API Testing

Verify

✓ Submit Assignment

✓ Duplicate Submission Prevention

✓ Update Submission

✓ Delete Submission

✓ Student Submission History

✓ Assignment Submission History

✓ Pending Reviews

✓ Review Submission

✓ Late Submission Detection

✓ Pagination

✓ Filtering

✓ Sorting

✓ Authentication

✓ Authorization

✓ Ownership Validation

---

# Future Compatibility

Architecture should support

- Multiple File Uploads

- Cloud Storage

- Resubmissions

- Version History

- Rubric Evaluation

- Plagiarism Detection

- Automatic Grading

- Peer Review

without redesigning the API.

---

# Definition of Completion

The Submissions API is complete when

✓ CRUD works.

✓ Review workflow works.

✓ Pending review listing works.

✓ Duplicate submissions prevented.

✓ Late submission detection works.

✓ Filtering works.

✓ Pagination works.

✓ Sorting works.

✓ Authentication enforced.

✓ Authorization enforced.

✓ Ownership validation works.

✓ Swagger documentation complete.

✓ Tests pass.

---

# Summary

The Submissions API manages the complete assignment submission workflow within EduTrack Pro.

It enables students to submit coursework and teachers to review submissions while maintaining secure ownership validation, standardized REST behavior, academic integrity, and seamless integration with dashboards, reports, analytics, and future grading systems.

End of Submissions API Specification.