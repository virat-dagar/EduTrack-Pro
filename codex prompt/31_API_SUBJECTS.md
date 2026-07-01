# 31_API_SUBJECTS.md

# EduTrack Pro — Subjects API Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Subjects API

---

# Purpose

This document defines every Subject Management API endpoint within EduTrack Pro.

The Subjects API manages the academic subjects offered by the institution.

Subjects act as the academic foundation for

- Attendance
- Marks
- Assignments
- Dashboards
- Reports
- Analytics

Only Teachers are permitted to modify Subject records.

Students may only view subjects applicable to them.

---

# Base Route

```
/api/v1/subjects
```

---

# Resource

```
Subject
```

Represents an academic subject offered by the institution.

Each Subject belongs to

- Course
- Department
- Semester

Each Subject may contain

- Attendance
- Marks
- Assignments

---

# Endpoint Summary

| Method | Endpoint | Purpose |
|---------|----------|----------|
| GET | /subjects | List Subjects |
| GET | /subjects/{id} | Get Subject |
| POST | /subjects | Create Subject |
| PUT | /subjects/{id} | Update Subject |
| DELETE | /subjects/{id} | Delete Subject |
| GET | /subjects/search | Search Subjects |
| GET | /subjects/course/{course} | Subjects by Course |
| GET | /subjects/semester/{semester} | Subjects by Semester |

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

---

# Endpoint

```
GET /api/v1/subjects
```

Purpose

Return paginated list of subjects.

---

# Query Parameters

Pagination

```
?page=1

&page_size=20
```

Search

```
?q=database
```

Filtering

```
?course=B.Tech

&department=Computer Science

&semester=5

&is_active=true
```

Sorting

```
?sort=subject_name

&order=asc
```

---

# Processing Flow

```
Authenticate

↓

Authorize

↓

Apply Search

↓

Apply Filters

↓

Apply Sorting

↓

Apply Pagination

↓

Return Subjects
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
        "id": 12,
        "subject_code": "CS301",
        "subject_name": "Database Management Systems",
        "course": "B.Tech",
        "department": "Computer Science",
        "semester": 5,
        "credits": 4,
        "is_active": true
      }
    ],
    "page": 1,
    "page_size": 20,
    "total_items": 48,
    "total_pages": 3
  }
}
```

---

# Endpoint

```
GET /api/v1/subjects/{id}
```

Purpose

Retrieve one subject.

Teachers and Students may access.

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
    "id": 12,
    "subject_code": "CS301",
    "subject_name": "Database Management Systems",
    "course": "B.Tech",
    "department": "Computer Science",
    "semester": 5,
    "credits": 4,
    "description": "Introduction to relational databases, SQL, normalization, indexing, and transactions.",
    "is_active": true
  }
}
```

---

# Endpoint

```
POST /api/v1/subjects
```

Purpose

Create a new subject.

---

# Authorization

Teacher only.

---

# Request

```json
{
  "subject_code": "CS305",
  "subject_name": "Machine Learning",
  "course": "B.Tech",
  "department": "Computer Science",
  "semester": 6,
  "credits": 4,
  "description": "Introduction to supervised and unsupervised learning."
}
```

---

# Processing Flow

```
Authenticate

↓

Authorize

↓

Validate Request

↓

Check Duplicate Subject Code

↓

Store Subject

↓

Return Subject
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
  "message": "Subject created successfully.",
  "data": {
    "id": 22,
    "subject_code": "CS305",
    "subject_name": "Machine Learning"
  }
}
```

---

# Duplicate Subject Code

Status

```
409 Conflict
```

```json
{
  "success": false,
  "message": "Subject code already exists."
}
```

---

# Endpoint

```
PUT /api/v1/subjects/{id}
```

Purpose

Update subject.

---

# Editable Fields

- Subject Name
- Credits
- Description
- Semester
- Department
- Course
- Active Status

Subject Code should remain immutable once created.

---

# Successful Response

```
200 OK
```

```json
{
  "success": true,
  "message": "Subject updated successfully.",
  "data": {}
}
```

---

# Endpoint

```
DELETE /api/v1/subjects/{id}
```

Purpose

Delete subject.

Authorization

Teacher only.

---

# Processing Flow

```
Authenticate

↓

Authorize

↓

Verify Subject Exists

↓

Verify No Dependent Records

↓

Delete Subject

↓

Return Success
```

Subjects referenced by Attendance, Marks, or Assignments should not be deleted unless business rules explicitly allow it.

---

# Successful Response

```
200 OK
```

```json
{
  "success": true,
  "message": "Subject deleted successfully."
}
```

---

# Endpoint

```
GET /api/v1/subjects/search
```

Purpose

Advanced subject search.

---

# Supported Parameters

```
?q=

course

department

semester

credits

is_active
```

Search should ignore case.

---

# Endpoint

```
GET /api/v1/subjects/course/{course}
```

Purpose

Return all subjects belonging to a course.

---

# Endpoint

```
GET /api/v1/subjects/semester/{semester}
```

Purpose

Return all subjects offered during a semester.

Optional filters

```
course

department
```

---

# Expected Schemas

```
SubjectCreate

SubjectUpdate

SubjectResponse

SubjectListResponse

SubjectSearchResponse
```

---

# Expected Router

```
routers/subjects.py
```

Responsibilities

- Subject CRUD
- Subject Search
- Subject Filtering
- Course-wise Listing
- Semester-wise Listing

Router should contain no business logic.

---

# Expected Service

```
services/subject_service.py
```

Responsibilities

- Create Subject
- Update Subject
- Delete Subject
- Get Subject
- List Subjects
- Search Subjects
- Filter Subjects
- Validate Subject Data
- Check Duplicate Subject Code

---

# Business Rules

Every Subject must have a unique Subject Code.

Attendance records require valid Subjects.

Marks require valid Subjects.

Assignments require valid Subjects.

Inactive Subjects should remain available for historical reports but should not appear in default active listings.

Teachers manage Subjects.

Students only view Subjects.

---

# Search

Supported Fields

- Subject Name
- Subject Code
- Department
- Course

Search should be case insensitive.

---

# Filters

Support

```
Course

Department

Semester

Credits

Active Status
```

Multiple filters should be combinable.

---

# Sorting

Support

```
Subject Name

Subject Code

Semester

Credits

Created Date
```

Ascending and descending.

---

# Security

Teachers

Full CRUD.

Students

Read-only access.

Deletion should preserve database integrity.

Subject Codes must remain immutable after creation.

---

# Swagger Documentation

Every endpoint should include

- Summary
- Description
- Authentication
- Authorization
- Request Schema
- Response Schema
- Status Codes
- Examples

---

# API Testing

Verify

✓ Subject Creation

✓ Subject Update

✓ Subject Delete

✓ Duplicate Subject Code

✓ Subject Search

✓ Subject Filtering

✓ Pagination

✓ Sorting

✓ Authentication

✓ Authorization

✓ Validation

---

# Future Compatibility

Architecture should support

- Faculty Assignment
- Subject Prerequisites
- Elective Subjects
- Core Subjects
- Laboratory Subjects
- Credit Categories
- Semester Cloning
- Bulk Subject Import

without redesigning the Subjects API.

---

# Definition of Completion

The Subjects API is complete when

✓ CRUD works.

✓ Search works.

✓ Filtering works.

✓ Pagination works.

✓ Sorting works.

✓ Authentication enforced.

✓ Authorization enforced.

✓ Duplicate Subject Codes prevented.

✓ Swagger documentation complete.

✓ Tests pass.

---

# Summary

The Subjects API provides secure management of institutional academic subjects and serves as the foundation for Attendance, Marks, Assignments, Dashboards, Reports, and Analytics.

It follows consistent REST standards while maintaining data integrity, role-based access control, and future scalability.

End of Subjects API Specification.