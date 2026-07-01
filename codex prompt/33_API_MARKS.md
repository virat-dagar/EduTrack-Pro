# 33_API_MARKS.md

# EduTrack Pro — Marks API Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Marks API

---

# Purpose

This document defines every Marks Management API endpoint within EduTrack Pro.

The Marks API is responsible for managing all academic marks recorded for students.

Marks data powers

- Student Dashboard
- Teacher Dashboard
- Academic Performance
- Performance Analytics
- Grade Calculation
- Performance Prediction
- Scholarship Eligibility
- Reports

Marks are permanent academic records and therefore require strict validation and authorization.

---

# Base Route

```
/api/v1/marks
```

---

# Resource

```
Marks
```

Represents one assessment record for one student in one subject.

---

# Endpoint Summary

| Method | Endpoint | Purpose |
|---------|----------|----------|
| GET | /marks | List Marks |
| GET | /marks/{id} | Get Marks Record |
| POST | /marks | Add Marks |
| PUT | /marks/{id} | Update Marks |
| DELETE | /marks/{id} | Delete Marks |
| GET | /marks/student/{student_id} | Student Marks |
| GET | /marks/subject/{subject_id} | Subject Marks |
| GET | /marks/summary | Marks Summary |
| GET | /marks/average/{student_id} | Student Average |

---

# Authentication

Required

Yes

---

# Authorization

Teachers

✓ Full CRUD

✓ View all marks

Students

✓ View only their own marks

Students may never modify academic marks.

---

# Endpoint

```
GET /api/v1/marks
```

Purpose

Return paginated marks records.

---

# Query Parameters

Pagination

```
?page=1

&page_size=20
```

Filtering

```
student_id

subject_id

assessment_type

semester

start_date

end_date
```

Sorting

```
?sort=examination_date

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

Return Marks
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
        "id": 55,
        "student_id": 12,
        "subject_id": 5,
        "assessment_type": "Mid Semester",
        "marks_obtained": 41,
        "maximum_marks": 50,
        "percentage": 82.0
      }
    ],
    "page": 1,
    "page_size": 20,
    "total_items": 320,
    "total_pages": 16
  }
}
```

---

# Endpoint

```
GET /api/v1/marks/{id}
```

Purpose

Retrieve one marks record.

Teachers

May access all records.

Students

May access only their own record.

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
    "id": 55,
    "student_id": 12,
    "subject_id": 5,
    "assessment_type": "Mid Semester",
    "marks_obtained": 41,
    "maximum_marks": 50,
    "percentage": 82.0,
    "grade": "A"
  }
}
```

---

# Endpoint

```
POST /api/v1/marks
```

Purpose

Add a new marks record.

---

# Authorization

Teacher only.

---

# Request

```json
{
  "student_id": 12,
  "subject_id": 5,
  "assessment_type": "Mid Semester",
  "marks_obtained": 41,
  "maximum_marks": 50,
  "examination_date": "2026-07-20",
  "remarks": "Good performance."
}
```

---

# Processing Flow

```
Authenticate

↓

Authorize

↓

Validate Student

↓

Validate Subject

↓

Validate Marks

↓

Check Duplicate Entry

↓

Store Marks

↓

Return Response
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
  "message": "Marks added successfully.",
  "data": {
    "id": 55
  }
}
```

---

# Duplicate Record

Status

```
409 Conflict
```

```json
{
  "success": false,
  "message": "Marks already exist for this assessment."
}
```

---

# Endpoint

```
PUT /api/v1/marks/{id}
```

Purpose

Update marks.

---

# Editable Fields

```
Marks Obtained

Maximum Marks

Remarks
```

Assessment type should remain unchanged after creation.

---

# Successful Response

```
200 OK
```

```json
{
  "success": true,
  "message": "Marks updated successfully."
}
```

---

# Endpoint

```
DELETE /api/v1/marks/{id}
```

Purpose

Delete marks.

Authorization

Teacher only.

Deletion should be limited to academic corrections.

---

# Successful Response

```
200 OK
```

```json
{
  "success": true,
  "message": "Marks deleted successfully."
}
```

---

# Endpoint

```
GET /api/v1/marks/student/{student_id}
```

Purpose

Retrieve complete marks history for one student.

Teachers

May access any student.

Students

May access only their own marks.

---

# Query Parameters

Optional

```
subject_id

semester

assessment_type
```

---

# Endpoint

```
GET /api/v1/marks/subject/{subject_id}
```

Purpose

Retrieve marks for one subject.

Teacher only.

---

# Query Parameters

Optional

```
assessment_type

semester
```

---

# Endpoint

```
GET /api/v1/marks/summary
```

Purpose

Return institutional marks statistics.

Example

```json
{
  "success": true,
  "message": "",
  "data": {
    "average_percentage": 78.4,
    "highest_marks": 98,
    "lowest_marks": 21,
    "total_records": 950
  }
}
```

---

# Endpoint

```
GET /api/v1/marks/average/{student_id}
```

Purpose

Return overall academic performance.

Calculation performed inside

```
marks_service.py
```

---

# Example Response

```json
{
  "success": true,
  "message": "",
  "data": {
    "student_id": 12,
    "average_percentage": 84.75,
    "grade": "A",
    "subjects_completed": 6
  }
}
```

---

# Validation Rules

Student

Must exist.

Subject

Must exist.

Marks

Must be

```
0

≤

marks_obtained

≤

maximum_marks
```

Maximum Marks

Must be positive.

Assessment Type

Allowed

```
Assignment

Quiz

Internal

Mid Semester

Practical

End Semester
```

Duplicate assessments prohibited.

---

# Expected Schemas

```
MarksCreate

MarksUpdate

MarksResponse

MarksListResponse

MarksSummaryResponse

MarksAverageResponse
```

---

# Expected Router

```
routers/marks.py
```

Responsibilities

- Marks CRUD
- Student Marks
- Subject Marks
- Marks Summary
- Average Calculation

No business logic.

---

# Expected Service

```
services/marks_service.py
```

Responsibilities

- Add Marks
- Update Marks
- Delete Marks
- Student Marks
- Subject Marks
- Average Calculation
- Grade Calculation
- Performance Summary
- Duplicate Validation
- Filtering
- Searching

---

# Grade Calculation

Grades are calculated dynamically.

Recommended mapping

```
90–100 → A+

80–89 → A

70–79 → B+

60–69 → B

50–59 → C

40–49 → D

Below 40 → F
```

The database stores only raw marks.

Grades are computed inside the Service Layer.

---

# Business Rules

Only Teachers may enter marks.

Students cannot modify marks.

Each assessment should have only one marks record.

Marks should automatically contribute to

- Dashboard
- Reports
- Analytics
- Performance Prediction
- Scholarship Eligibility

---

# Search

Support

```
Student

Subject

Assessment Type
```

Case insensitive.

---

# Filters

Support

```
Student

Subject

Assessment Type

Semester

Date Range
```

Filters should be combinable.

---

# Sorting

Support

```
Examination Date

Marks

Percentage

Student

Subject
```

Ascending and descending.

---

# Security

Teachers

Full CRUD.

Students

Read-only access to their own academic records.

Ownership validation required for all student-specific endpoints.

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

✓ Add Marks

✓ Update Marks

✓ Delete Marks

✓ Duplicate Prevention

✓ Average Calculation

✓ Grade Calculation

✓ Student Marks

✓ Subject Marks

✓ Marks Summary

✓ Pagination

✓ Filtering

✓ Sorting

✓ Authentication

✓ Authorization

✓ Ownership Validation

---

# Future Compatibility

Architecture should support

- Weighted Assessments
- GPA
- CGPA
- Relative Grading
- Bulk Marks Upload
- CSV Import
- Excel Import
- Grade Moderation
- Re-evaluation Workflow

without redesigning the Marks API.

---

# Definition of Completion

The Marks API is complete when

✓ CRUD works.

✓ Average calculation works.

✓ Grade calculation works.

✓ Summary works.

✓ Duplicate entries prevented.

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

The Marks API provides secure management of academic assessment records while maintaining institutional integrity, centralized grade calculation, standardized REST behavior, and role-based access control.

It serves as the primary source of academic performance data for dashboards, reports, analytics, scholarship evaluation, and future performance prediction within EduTrack Pro.

End of Marks API Specification.