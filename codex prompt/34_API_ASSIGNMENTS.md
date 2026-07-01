# 34_API_ASSIGNMENTS.md

# EduTrack Pro — Assignments API Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Assignments API

---

# Purpose

This document defines every Assignment Management API endpoint within EduTrack Pro.

The Assignments API manages the complete lifecycle of academic assignments.

Assignments power

- Student Dashboard
- Teacher Dashboard
- Assignment Tracking
- Pending Work
- Submission Management
- Academic Reports
- Performance Analytics

Assignments are created by teachers and completed by students.

---

# Base Route

```
/api/v1/assignments
```

---

# Resource

```
Assignment
```

Represents one academic assignment belonging to a subject.

Each Assignment belongs to

- One Subject
- One Teacher

Each Assignment may have

- Multiple Student Submissions

---

# Endpoint Summary

| Method | Endpoint | Purpose |
|---------|----------|----------|
| GET | /assignments | List Assignments |
| GET | /assignments/{id} | Get Assignment |
| POST | /assignments | Create Assignment |
| PUT | /assignments/{id} | Update Assignment |
| DELETE | /assignments/{id} | Delete Assignment |
| GET | /assignments/subject/{subject_id} | Subject Assignments |
| GET | /assignments/teacher/{teacher_id} | Teacher Assignments |
| GET | /assignments/upcoming | Upcoming Assignments |
| GET | /assignments/overdue | Overdue Assignments |

---

# Authentication

Required

Yes

---

# Authorization

Teachers

✓ Full CRUD

Students

✓ Read Only

Students may never create, modify, or delete assignments.

---

# Endpoint

```
GET /api/v1/assignments
```

Purpose

Return paginated assignment list.

---

# Query Parameters

Pagination

```
?page=1

&page_size=20
```

Search

```
?q=
```

Filtering

```
subject_id

teacher_id

semester

course

department

is_active
```

Sorting

```
?sort=due_date

&order=asc
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

Return Assignments
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
                "id": 15,
                "title": "Normalization Assignment",
                "subject": "Database Management Systems",
                "total_marks": 20,
                "assigned_date": "2026-07-01",
                "due_date": "2026-07-10",
                "is_active": true
            }
        ],
        "page": 1,
        "page_size": 20,
        "total_items": 45,
        "total_pages": 3
    }
}
```

---

# Endpoint

```
GET /api/v1/assignments/{id}
```

Purpose

Retrieve one assignment.

Accessible by

Teachers

Students

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
        "id": 15,
        "subject_id": 5,
        "title": "Normalization Assignment",
        "description": "Solve all normalization questions.",
        "total_marks": 20,
        "assigned_date": "2026-07-01",
        "due_date": "2026-07-10",
        "created_by": 2
    }
}
```

---

# Endpoint

```
POST /api/v1/assignments
```

Purpose

Create assignment.

---

# Authorization

Teacher only.

---

# Request

```json
{
    "subject_id": 5,
    "title": "SQL Assignment",
    "description": "Write SQL queries for all questions.",
    "total_marks": 25,
    "assigned_date": "2026-07-12",
    "due_date": "2026-07-20"
}
```

---

# Processing Flow

```
Authenticate

↓

Authorize

↓

Validate Subject

↓

Validate Dates

↓

Store Assignment

↓

Return Assignment
```

---

# Successful Response

```
201 Created
```

```json
{
    "success": true,
    "message": "Assignment created successfully.",
    "data": {
        "id": 22
    }
}
```

---

# Validation Rules

Due Date

Must be

```
>=

Assigned Date
```

Subject

Must exist.

Teacher

Must exist.

---

# Endpoint

```
PUT /api/v1/assignments/{id}
```

Purpose

Update assignment.

---

# Editable Fields

```
Title

Description

Total Marks

Due Date

Active Status
```

Subject should not change after creation.

---

# Successful Response

```
200 OK
```

```json
{
    "success": true,
    "message": "Assignment updated successfully."
}
```

---

# Endpoint

```
DELETE /api/v1/assignments/{id}
```

Purpose

Delete assignment.

Authorization

Teacher only.

Deletion should preserve submission integrity.

Assignments with submissions should normally not be deleted.

Prefer archival through

```
is_active = false
```

---

# Successful Response

```
200 OK
```

```json
{
    "success": true,
    "message": "Assignment deleted successfully."
}
```

---

# Endpoint

```
GET /api/v1/assignments/subject/{subject_id}
```

Purpose

Return all assignments for a subject.

Students see only active assignments.

Teachers see all assignments.

---

# Endpoint

```
GET /api/v1/assignments/teacher/{teacher_id}
```

Purpose

Return assignments created by one teacher.

Teacher only.

---

# Endpoint

```
GET /api/v1/assignments/upcoming
```

Purpose

Return assignments whose due date has not passed.

Supports

```
course

department

semester

subject
```

---

# Endpoint

```
GET /api/v1/assignments/overdue
```

Purpose

Return overdue assignments.

Teacher only.

Used for dashboard analytics.

---

# Expected Schemas

```
AssignmentCreate

AssignmentUpdate

AssignmentResponse

AssignmentListResponse

UpcomingAssignmentResponse
```

---

# Expected Router

```
routers/assignments.py
```

Responsibilities

- Assignment CRUD
- Subject Assignments
- Teacher Assignments
- Upcoming Assignments
- Overdue Assignments

No business logic.

---

# Expected Service

```
services/assignment_service.py
```

Responsibilities

- Create Assignment
- Update Assignment
- Delete Assignment
- Assignment Listing
- Subject Assignments
- Teacher Assignments
- Upcoming Assignments
- Overdue Assignments
- Validation

---

# Business Rules

Assignments belong to one subject.

Assignments are created only by teachers.

Students cannot edit assignments.

Assignments should automatically appear on

- Student Dashboard
- Teacher Dashboard

Assignment deadlines should update dashboard statistics automatically.

---

# Search

Support

```
Title

Subject

Teacher
```

Case insensitive.

---

# Filters

Support

```
Subject

Department

Course

Semester

Teacher

Active Status
```

---

# Sorting

Support

```
Due Date

Assigned Date

Title

Subject
```

Ascending and descending.

---

# Security

Teachers

Full CRUD.

Students

Read-only access.

Assignment ownership should be tracked.

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

✓ Assignment Creation

✓ Assignment Update

✓ Assignment Delete

✓ Upcoming Assignments

✓ Overdue Assignments

✓ Subject Assignments

✓ Teacher Assignments

✓ Pagination

✓ Filtering

✓ Sorting

✓ Authentication

✓ Authorization

---

# Future Compatibility

Architecture should support

- Scheduled Publishing
- Draft Assignments
- File Attachments
- Multiple Attachments
- Rubrics
- Group Assignments
- Assignment Templates
- Automatic Reminder Notifications

without redesigning the API.

---

# Definition of Completion

The Assignments API is complete when

✓ CRUD works.

✓ Upcoming assignments work.

✓ Overdue assignments work.

✓ Filtering works.

✓ Pagination works.

✓ Sorting works.

✓ Authentication enforced.

✓ Authorization enforced.

✓ Validation works.

✓ Swagger documentation complete.

✓ Tests pass.

---

# Summary

The Assignments API provides complete management of academic assignments within EduTrack Pro.

It enables teachers to organize coursework while allowing students to access assignment information through a secure, consistent, and scalable REST API that integrates seamlessly with submissions, dashboards, reports, and analytics.

End of Assignments API Specification.