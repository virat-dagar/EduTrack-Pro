# 30_API_STUDENTS.md

# EduTrack Pro — Students API Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Students API

---

# Purpose

This document defines every Student Management API endpoint within EduTrack Pro.

The Students API manages all academic student records.

It is responsible for

- Student CRUD
- Student Search
- Student Filtering
- Student Profiles
- Student Listings

Authentication and authorization must be enforced for every endpoint.

---

# Base Route

```
/api/v1/students
```

---

# Resource

```
Student
```

Represents an enrolled academic student.

Each Student is associated with one User account.

---

# Endpoint Summary

| Method | Endpoint | Purpose |
|---------|----------|----------|
| GET | /students | List Students |
| GET | /students/{id} | Get Student |
| POST | /students | Create Student |
| PUT | /students/{id} | Update Student |
| DELETE | /students/{id} | Delete Student |
| GET | /students/me | Current Student Profile |
| GET | /students/search | Search Students |

---

# Authentication

Required

Yes

---

# Authorization

Teacher

- Full Access

Student

- May only access

```
GET /students/me

GET /students/{own_id}
```

Students may never access another student's profile.

---

# Endpoint

```
GET /api/v1/students
```

Purpose

Return paginated student list.

---

# Query Parameters

Pagination

```
?page=1

&page_size=20
```

Search

```
?q=virat
```

Filtering

```
?semester=5

&department=CSE

&course=BTech

&section=A

&academic_year=2026-27

&is_active=true
```

Sorting

```
?sort=first_name

&order=asc
```

---

# Processing Flow

```
Authenticate

↓

Authorize

↓

Validate Query Parameters

↓

Apply Search

↓

Apply Filters

↓

Apply Sorting

↓

Apply Pagination

↓

Return Students
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
        "id": 1,
        "roll_number": "CSE23001",
        "enrollment_number": "2026CSE001",
        "first_name": "Virat",
        "last_name": "Sharma",
        "department": "Computer Science",
        "course": "B.Tech",
        "semester": 5,
        "section": "A"
      }
    ],
    "page": 1,
    "page_size": 20,
    "total_items": 250,
    "total_pages": 13
  }
}
```

---

# Endpoint

```
GET /api/v1/students/{id}
```

Purpose

Retrieve one student profile.

Teachers

May access any student.

Students

May access only their own profile.

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
    "id": 1,
    "roll_number": "CSE23001",
    "enrollment_number": "2026CSE001",
    "first_name": "Virat",
    "last_name": "Sharma",
    "email": "virat@example.com",
    "phone": "9876543210",
    "department": "Computer Science",
    "course": "B.Tech",
    "semester": 5,
    "section": "A",
    "academic_year": "2026-27"
  }
}
```

---

# Endpoint

```
GET /api/v1/students/me
```

Purpose

Return the currently authenticated student's profile.

Authentication

Required

Authorization

Student only.

---

# Processing Flow

```
JWT

↓

Current User

↓

Student Profile

↓

Return Profile
```

---

# Successful Response

```
200 OK
```

Returns the authenticated student's complete academic profile.

---

# Endpoint

```
POST /api/v1/students
```

Purpose

Create a new student record.

---

# Authorization

Teacher only.

---

# Request

```json
{
  "user_id": 12,
  "roll_number": "CSE23025",
  "enrollment_number": "2026CSE025",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "9876543210",
  "course": "B.Tech",
  "department": "Computer Science",
  "semester": 5,
  "section": "A",
  "academic_year": "2026-27",
  "admission_date": "2026-07-01"
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

Verify User Exists

↓

Check Duplicate Roll Number

↓

Check Duplicate Enrollment Number

↓

Store Student

↓

Return Student
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
  "message": "Student created successfully.",
  "data": {
    "id": 25,
    "roll_number": "CSE23025",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

---

# Duplicate Validation

Duplicate Roll Number

```
409 Conflict
```

Duplicate Enrollment Number

```
409 Conflict
```

Duplicate Email

```
409 Conflict
```

---

# Endpoint

```
PUT /api/v1/students/{id}
```

Purpose

Update student information.

---

# Editable Fields

- First Name
- Last Name
- Phone
- Department
- Course
- Semester
- Section
- Academic Year
- Active Status

Roll Number and Enrollment Number should remain immutable unless explicitly permitted by institutional policy.

---

# Successful Response

```
200 OK
```

```json
{
  "success": true,
  "message": "Student updated successfully.",
  "data": {}
}
```

---

# Endpoint

```
DELETE /api/v1/students/{id}
```

Purpose

Delete student.

Authorization

Teacher only.

---

# Processing Flow

```
Authenticate

↓

Authorize

↓

Verify Student

↓

Verify Relationships

↓

Delete Student

↓

Return Success
```

Deletion should preserve referential integrity.

---

# Successful Response

```
200 OK
```

```json
{
  "success": true,
  "message": "Student deleted successfully."
}
```

---

# Endpoint

```
GET /api/v1/students/search
```

Purpose

Advanced student search.

---

# Supported Parameters

```
?q=

department

course

semester

section

academic_year
```

Search should be

Case insensitive.

Pagination supported.

---

# Expected Schemas

```
StudentCreate

StudentUpdate

StudentResponse

StudentListResponse

StudentSearchResponse
```

---

# Expected Router

```
routers/students.py
```

Responsibilities

- Student CRUD
- Student Search
- Student Filters
- Current Student Profile

No business logic.

---

# Expected Service

```
services/student_service.py
```

Responsibilities

- Create Student
- Update Student
- Delete Student
- Get Student
- Get Current Student
- Search Students
- Filter Students
- Validate Student Data

---

# Business Rules

Every Student must reference an existing User.

Roll Number must be unique.

Enrollment Number must be unique.

Teachers manage student records.

Students may only access their own profile.

Deleting a student must preserve database integrity.

---

# Search

Supported fields

- First Name
- Last Name
- Roll Number
- Enrollment Number

Search should ignore case.

---

# Filters

Support

```
Course

Department

Semester

Section

Academic Year

Active Status
```

Filters should be combinable.

---

# Sorting

Support

```
First Name

Last Name

Roll Number

Semester

Admission Date
```

Ascending and descending.

---

# Security

Teachers

Full CRUD.

Students

Read-only access to their own academic profile.

Ownership validation must always occur on the backend.

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

✓ Student Creation

✓ Student Update

✓ Student Delete

✓ Student Search

✓ Student Filtering

✓ Pagination

✓ Sorting

✓ Duplicate Roll Number

✓ Duplicate Enrollment Number

✓ Authentication

✓ Authorization

✓ Ownership Validation

---

# Future Compatibility

Architecture should support

- Bulk Student Import
- CSV Import
- Excel Import
- Student Promotion
- Semester Advancement
- Student Archive
- Alumni Records
- Department Transfer

without redesigning the Students API.

---

# Definition of Completion

The Students API is complete when

✓ CRUD works.

✓ Search works.

✓ Filtering works.

✓ Pagination works.

✓ Sorting works.

✓ Authentication enforced.

✓ Authorization enforced.

✓ Ownership validation works.

✓ Duplicate validation works.

✓ Swagger documentation complete.

✓ Tests pass.

---

# Summary

The Students API provides secure, role-based management of academic student records while enforcing ownership validation, institutional data integrity, and consistent REST API standards.

It serves as the primary academic resource API upon which Attendance, Marks, Assignments, Reports, Dashboards, and Analytics depend.

End of Students API Specification.