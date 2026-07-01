# 37_API_REPORTS.md

# EduTrack Pro — Reports API Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Reports API

---

# Purpose

This document defines every Report Generation API endpoint within EduTrack Pro.

The Reports API is responsible for generating academic reports from aggregated institutional data.

Unlike CRUD APIs, Reports APIs generate read-only documents and summaries.

Reports consume data from

- Students
- Subjects
- Attendance
- Marks
- Assignments
- Submissions

The Reports API never modifies database records.

---

# Report Philosophy

Reports should

- Aggregate data
- Generate summaries
- Produce printable output
- Support PDF export
- Be reusable
- Be fast

All calculations belong in the Service Layer.

---

# Base Route

```
/api/v1/reports
```

---

# Authentication

Required

Yes

---

# Authorization

Teachers

✓ Institution Reports

✓ Student Reports

✓ Attendance Reports

✓ Marks Reports

✓ Assignment Reports

Students

✓ Personal Reports Only

Students may never access reports belonging to other students.

---

# Report Types

EduTrack Pro supports

```
Student Academic Report

Attendance Report

Marks Report

Assignment Report

Performance Report

Institution Summary
```

Future versions may introduce additional report types.

---

# Endpoint Summary

| Method | Endpoint | Purpose |
|---------|----------|----------|
| GET | /reports/student/{student_id} | Student Academic Report |
| GET | /reports/attendance | Attendance Report |
| GET | /reports/marks | Marks Report |
| GET | /reports/assignments | Assignment Report |
| GET | /reports/performance | Performance Report |
| GET | /reports/institution | Institution Summary |
| GET | /reports/student/{student_id}/pdf | Student PDF Report *(Future)* |

---

# Endpoint

```
GET /api/v1/reports/student/{student_id}
```

Purpose

Generate complete academic report for one student.

---

# Authorization

Teachers

May generate reports for any student.

Students

May generate only their own report.

Ownership validation required.

---

# Processing Flow

```
Authenticate

↓

Authorize

↓

Verify Ownership

↓

Collect Attendance

↓

Collect Marks

↓

Collect Assignments

↓

Calculate Performance

↓

Generate Report

↓

Return JSON
```

---

# Example Response

```json
{
    "success": true,
    "message": "",
    "data": {
        "student": {
            "id": 12,
            "name": "Virat Sharma",
            "roll_number": "CSE23012"
        },
        "attendance_percentage": 91.8,
        "average_marks": 84.5,
        "grade": "A",
        "pending_assignments": 2,
        "performance_score": 87.4
    }
}
```

---

# Endpoint

```
GET /api/v1/reports/attendance
```

Purpose

Generate attendance report.

---

# Authorization

Teacher only.

---

# Filters

Support

```
Student

Subject

Department

Course

Semester

Date Range
```

---

# Example Response

```json
{
    "success": true,
    "message": "",
    "data": {
        "total_students": 420,
        "average_attendance": 89.7,
        "present": 382,
        "absent": 38
    }
}
```

---

# Endpoint

```
GET /api/v1/reports/marks
```

Purpose

Generate academic marks report.

---

# Filters

Support

```
Subject

Semester

Department

Assessment Type

Date Range
```

---

# Example Response

```json
{
    "success": true,
    "message": "",
    "data": {
        "average_marks": 78.3,
        "highest_marks": 99,
        "lowest_marks": 28,
        "pass_percentage": 94.6
    }
}
```

---

# Endpoint

```
GET /api/v1/reports/assignments
```

Purpose

Generate assignment completion report.

---

# Example Response

```json
{
    "success": true,
    "message": "",
    "data": {
        "total_assignments": 28,
        "submitted": 512,
        "pending": 38,
        "late_submissions": 12
    }
}
```

---

# Endpoint

```
GET /api/v1/reports/performance
```

Purpose

Generate academic performance report.

---

# Report Includes

```
Average Marks

Average Attendance

Top Performers

At-Risk Students

Performance Distribution
```

---

# Example Response

```json
{
    "success": true,
    "message": "",
    "data": {
        "average_performance": 81.6,
        "top_performers": [],
        "at_risk_students": [],
        "performance_distribution": []
    }
}
```

---

# Endpoint

```
GET /api/v1/reports/institution
```

Purpose

Generate institution-wide academic summary.

Teacher only.

---

# Report Includes

```
Total Students

Total Subjects

Attendance Statistics

Marks Statistics

Assignments

Submissions

Performance Summary
```

---

# Expected Response

```json
{
    "success": true,
    "message": "",
    "data": {
        "students": 480,
        "subjects": 28,
        "attendance_percentage": 90.7,
        "average_marks": 79.1,
        "assignment_completion": 93.4
    }
}
```

---

# PDF Export

Future Endpoint

```
GET

/api/v1/reports/student/{student_id}/pdf
```

Purpose

Generate downloadable PDF.

Implementation

```
reportlab
```

The JSON endpoint should remain the source of truth.

---

# Report Service

Expected File

```
services/report_service.py
```

Responsibilities

- Student Reports
- Attendance Reports
- Marks Reports
- Assignment Reports
- Performance Reports
- Institution Summary
- PDF Generation
- Report Aggregation

---

# Report Router

Expected File

```
routers/reports.py
```

Responsibilities

Expose report endpoints.

No calculations.

No business logic.

---

# Expected Schemas

```
StudentReportResponse

AttendanceReportResponse

MarksReportResponse

AssignmentReportResponse

PerformanceReportResponse

InstitutionReportResponse
```

---

# Business Rules

Reports are read-only.

Reports never modify data.

Attendance percentage should be calculated dynamically.

Average marks should be calculated dynamically.

Performance scores should be calculated dynamically.

Every report should reflect the current database state.

---

# Filters

Support

```
Department

Course

Semester

Student

Subject

Teacher

Date Range
```

Filters should be combinable.

---

# Performance Requirements

Reports should

Load quickly.

Use aggregation queries.

Avoid repeated database calls.

Avoid N+1 query problems.

---

# Security

Teachers

Institution-wide access.

Students

Personal reports only.

Ownership validation required.

No report should expose another student's academic information.

---

# Swagger Documentation

Document

- Report endpoints
- Parameters
- Filters
- Authentication
- Authorization
- Response Models
- Examples

---

# API Testing

Verify

✓ Student Report

✓ Attendance Report

✓ Marks Report

✓ Assignment Report

✓ Performance Report

✓ Institution Report

✓ Authorization

✓ Ownership Validation

✓ Filtering

✓ Authentication

✓ Performance

---

# Future Compatibility

Architecture should support

- PDF Reports

- Excel Reports

- CSV Export

- Scheduled Reports

- Email Reports

- Automated Weekly Reports

- Comparative Reports

- AI Generated Insights

without redesigning the Reports API.

---

# Report Generation Workflow

```
Request

↓

Authentication

↓

Authorization

↓

Collect Required Data

↓

Aggregate

↓

Calculate Statistics

↓

Generate Report

↓

Return JSON

↓

(Optional PDF Export)
```

---

# Definition of Completion

Reports API is complete when

✓ Student reports work.

✓ Attendance reports work.

✓ Marks reports work.

✓ Assignment reports work.

✓ Performance reports work.

✓ Institution reports work.

✓ Filtering works.

✓ Authentication enforced.

✓ Authorization enforced.

✓ Ownership validation works.

✓ Swagger complete.

✓ Tests pass.

---

# Summary

The Reports API provides a centralized reporting layer for EduTrack Pro, transforming raw academic data into structured summaries for students, teachers, and institutional administrators.

It serves as the foundation for academic reporting, analytics, future PDF generation, and export capabilities while maintaining strict security, standardized REST behavior, and efficient aggregation.

End of Reports API Specification.