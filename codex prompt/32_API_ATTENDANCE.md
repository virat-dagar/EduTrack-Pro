# 32_API_ATTENDANCE.md

# EduTrack Pro — Attendance API Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Attendance API

---

# Purpose

This document defines every Attendance Management API endpoint within EduTrack Pro.

The Attendance API is responsible for recording, retrieving, updating, and analyzing student attendance.

Attendance data powers

- Student Dashboard
- Teacher Dashboard
- Attendance Analytics
- Attendance Percentage
- At-Risk Student Detection
- Scholarship Eligibility
- Reports

Attendance is considered an academic record and must be protected by strict validation and authorization.

---

# Base Route

```
/api/v1/attendance
```

---

# Resource

```
Attendance
```

Represents one student's attendance for one subject on one academic day.

---

# Endpoint Summary

| Method | Endpoint | Purpose |
|---------|----------|----------|
| GET | /attendance | List Attendance |
| GET | /attendance/{id} | Get Attendance Record |
| POST | /attendance | Mark Attendance |
| PUT | /attendance/{id} | Update Attendance |
| DELETE | /attendance/{id} | Delete Attendance |
| GET | /attendance/student/{student_id} | Student Attendance |
| GET | /attendance/subject/{subject_id} | Subject Attendance |
| GET | /attendance/summary | Attendance Summary |
| GET | /attendance/percentage/{student_id} | Attendance Percentage |

---

# Authentication

Required

Yes

---

# Authorization

Teachers

✓ Full CRUD

✓ View all attendance

Students

✓ View only their own attendance

Students may never modify attendance.

---

# Endpoint

```
GET /api/v1/attendance
```

Purpose

Return paginated attendance records.

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

semester

status

attendance_date

start_date

end_date
```

Sorting

```
?sort=attendance_date

&order=desc
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

Apply Sorting

↓

Apply Pagination

↓

Return Attendance Records
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
        "id": 101,
        "student_id": 12,
        "subject_id": 4,
        "attendance_date": "2026-07-15",
        "status": "Present",
        "marked_by": 2
      }
    ],
    "page": 1,
    "page_size": 20,
    "total_items": 480,
    "total_pages": 24
  }
}
```

---

# Endpoint

```
GET /api/v1/attendance/{id}
```

Purpose

Retrieve one attendance record.

Teachers

May access all records.

Students

May access only their own record.

---

# Endpoint

```
POST /api/v1/attendance
```

Purpose

Mark attendance.

---

# Authorization

Teacher only.

---

# Request

```json
{
  "student_id": 12,
  "subject_id": 4,
  "attendance_date": "2026-07-15",
  "status": "Present",
  "remarks": "Present throughout the lecture."
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

Check Duplicate Record

↓

Store Attendance

↓

Return Attendance Record
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
  "message": "Attendance marked successfully.",
  "data": {
    "id": 101
  }
}
```

---

# Duplicate Attendance

Status

```
409 Conflict
```

```json
{
  "success": false,
  "message": "Attendance already marked for this student, subject, and date."
}
```

---

# Endpoint

```
PUT /api/v1/attendance/{id}
```

Purpose

Update attendance.

---

# Editable Fields

```
Status

Remarks
```

---

# Successful Response

```
200 OK
```

```json
{
  "success": true,
  "message": "Attendance updated successfully."
}
```

---

# Endpoint

```
DELETE /api/v1/attendance/{id}
```

Purpose

Delete attendance record.

Authorization

Teacher only.

Deletion should be restricted to authorized academic corrections.

---

# Successful Response

```
200 OK
```

```json
{
  "success": true,
  "message": "Attendance deleted successfully."
}
```

---

# Endpoint

```
GET /api/v1/attendance/student/{student_id}
```

Purpose

Retrieve complete attendance history for one student.

Teachers

May access any student.

Students

May access only their own history.

---

# Query Parameters

Optional

```
subject_id

semester

start_date

end_date
```

---

# Endpoint

```
GET /api/v1/attendance/subject/{subject_id}
```

Purpose

Retrieve attendance records for one subject.

Teachers only.

---

# Query Parameters

Optional

```
attendance_date

semester

status
```

---

# Endpoint

```
GET /api/v1/attendance/summary
```

Purpose

Return attendance statistics.

Supports

- Daily Summary
- Weekly Summary
- Monthly Summary
- Semester Summary

---

# Example Response

```json
{
  "success": true,
  "message": "",
  "data": {
    "total_records": 1200,
    "present": 1040,
    "absent": 130,
    "late": 30
  }
}
```

---

# Endpoint

```
GET /api/v1/attendance/percentage/{student_id}
```

Purpose

Calculate attendance percentage.

Formula

```
Present Classes

/

Total Classes

×

100
```

Calculation must occur inside

```
attendance_service.py
```

---

# Example Response

```json
{
  "success": true,
  "message": "",
  "data": {
    "student_id": 12,
    "attendance_percentage": 91.67
  }
}
```

---

# Validation Rules

Attendance Date

- Required
- Cannot be future date

Student

Must exist.

Subject

Must exist.

Duplicate records prohibited.

Status

Allowed values

```
Present

Absent

Late
```

---

# Expected Schemas

```
AttendanceCreate

AttendanceUpdate

AttendanceResponse

AttendanceListResponse

AttendanceSummaryResponse

AttendancePercentageResponse
```

---

# Expected Router

```
routers/attendance.py
```

Responsibilities

- Attendance CRUD
- Student Attendance
- Subject Attendance
- Attendance Summary
- Attendance Percentage

No business logic.

---

# Expected Service

```
services/attendance_service.py
```

Responsibilities

- Mark Attendance
- Update Attendance
- Delete Attendance
- Student History
- Subject History
- Attendance Percentage
- Attendance Summary
- Duplicate Validation
- Filtering
- Searching

---

# Business Rules

Only Teachers may mark attendance.

Students cannot modify attendance.

One attendance record per

```
Student

+

Subject

+

Date
```

Attendance percentages must always be calculated dynamically.

Attendance statistics should power dashboards, reports, scholarship eligibility, and risk detection.

---

# Search

Support

```
Student

Subject

Date

Teacher
```

Search should ignore case where applicable.

---

# Filters

Support

```
Student

Subject

Semester

Status

Date Range
```

Multiple filters should be combinable.

---

# Sorting

Support

```
Attendance Date

Student

Subject

Status
```

Ascending and descending.

---

# Security

Teachers

Full CRUD.

Students

Read-only access to their own attendance.

Ownership validation must occur on every student-specific endpoint.

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

✓ Mark Attendance

✓ Duplicate Attendance Prevention

✓ Update Attendance

✓ Delete Attendance

✓ Student History

✓ Subject History

✓ Attendance Summary

✓ Attendance Percentage

✓ Pagination

✓ Filtering

✓ Sorting

✓ Authentication

✓ Authorization

✓ Ownership Validation

---

# Future Compatibility

Architecture should support

- Bulk Attendance Upload
- CSV Import
- Excel Import
- QR Code Attendance
- RFID Attendance
- Biometric Attendance
- Holiday Calendar
- Leave Management
- Attendance Corrections Workflow

without redesigning the Attendance API.

---

# Definition of Completion

The Attendance API is complete when

✓ CRUD works.

✓ Attendance percentage works.

✓ Attendance summary works.

✓ Duplicate attendance prevented.

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

The Attendance API provides secure and reliable management of academic attendance records while maintaining institutional integrity, role-based access control, and standardized REST behavior.

It serves as a critical data source for dashboards, reports, analytics, scholarship evaluation, and at-risk student identification throughout EduTrack Pro.

End of Attendance API Specification.