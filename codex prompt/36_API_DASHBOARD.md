# 36_API_DASHBOARD.md

# EduTrack Pro — Dashboard API Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Dashboard API

---

# Purpose

This document defines every Dashboard API endpoint within EduTrack Pro.

Unlike CRUD APIs, the Dashboard API is an aggregation layer.

It combines data from multiple modules to generate dashboard cards, charts, statistics, analytics, and summaries.

The Dashboard API should never directly modify database records.

Its responsibility is to efficiently collect and present data.

---

# Dashboard Philosophy

Dashboard endpoints should

- Read data only
- Aggregate information
- Perform calculations
- Return visualization-ready responses

Dashboard APIs should never perform CRUD operations.

---

# Base Route

```
/api/v1/dashboard
```

---

# Dashboard Types

EduTrack Pro provides two dashboards.

```
Teacher Dashboard

Student Dashboard
```

Each dashboard has different permissions and data.

---

# Authentication

Required

Yes

---

# Authorization

Teacher Dashboard

Teacher only.

Student Dashboard

Student only.

Users attempting to access another dashboard should receive

```
403 Forbidden
```

---

# Endpoint Summary

| Method | Endpoint | Purpose |
|---------|----------|----------|
| GET | /dashboard/teacher | Teacher Dashboard |
| GET | /dashboard/student | Student Dashboard |
| GET | /dashboard/teacher/charts | Teacher Charts |
| GET | /dashboard/student/charts | Student Charts |
| GET | /dashboard/teacher/activity | Recent Activity |
| GET | /dashboard/student/activity | Student Activity |

---

# Teacher Dashboard

Endpoint

```
GET /api/v1/dashboard/teacher
```

Purpose

Return complete teacher dashboard summary.

---

# Dashboard Cards

Return

```
Total Students

Total Subjects

Attendance Today

Average Attendance

Average Marks

Assignments

Pending Reviews

At-Risk Students
```

---

# Example Response

```json
{
    "success": true,
    "message": "",
    "data": {
        "total_students": 480,
        "total_subjects": 28,
        "attendance_today": 441,
        "attendance_percentage": 91.87,
        "average_marks": 78.42,
        "assignments": 15,
        "pending_reviews": 9,
        "at_risk_students": 17
    }
}
```

---

# Teacher Charts

Endpoint

```
GET /api/v1/dashboard/teacher/charts
```

Purpose

Return chart data.

Charts include

- Attendance Trend
- Marks Trend
- Department Distribution
- Semester Distribution
- Assignment Completion
- At-Risk Distribution

---

# Example Response

```json
{
    "attendance_trend": [],
    "marks_trend": [],
    "semester_distribution": [],
    "assignment_completion": []
}
```

---

# Teacher Recent Activity

Endpoint

```
GET /api/v1/dashboard/teacher/activity
```

Purpose

Return recent institutional activity.

Examples

- Attendance Marked
- Marks Added
- Assignment Created
- Submission Reviewed
- Student Added

Limit

Default

```
20 Records
```

---

# Student Dashboard

Endpoint

```
GET /api/v1/dashboard/student
```

Purpose

Return student dashboard.

---

# Dashboard Cards

Return

```
Attendance %

Average Marks

Current Grade

Assignments Pending

Assignments Submitted

Subjects

Performance Score
```

---

# Example Response

```json
{
    "success": true,
    "message": "",
    "data": {
        "attendance_percentage": 92.6,
        "average_marks": 84.3,
        "grade": "A",
        "pending_assignments": 2,
        "submitted_assignments": 9,
        "subjects": 6,
        "performance_score": 87.2
    }
}
```

---

# Student Charts

Endpoint

```
GET /api/v1/dashboard/student/charts
```

Purpose

Return visualization data.

Charts

- Subject-wise Marks
- Attendance Trend
- Performance Trend
- Assignment Progress

---

# Example Response

```json
{
    "marks_by_subject": [],
    "attendance_trend": [],
    "performance_trend": [],
    "assignment_progress": []
}
```

---

# Student Activity

Endpoint

```
GET /api/v1/dashboard/student/activity
```

Purpose

Return recent student activity.

Examples

- Assignment Submitted
- Attendance Updated
- Marks Published
- Feedback Received

---

# Data Sources

Teacher Dashboard consumes

```
Users

Students

Subjects

Attendance

Marks

Assignments

Submissions
```

Student Dashboard consumes

```
Attendance

Marks

Assignments

Submissions
```

No dashboard should directly manipulate these tables.

---

# Aggregation Rules

Dashboard calculations should occur inside

```
dashboard_service.py
```

Never inside routers.

---

# Dashboard Service

Expected File

```
services/dashboard_service.py
```

Responsibilities

- Teacher Dashboard
- Student Dashboard
- Dashboard Cards
- Charts
- Activity Feed
- Summary Statistics
- Dashboard Aggregations

---

# Dashboard Router

Expected File

```
routers/dashboard.py
```

Responsibilities

Expose dashboard endpoints.

No calculations.

No business logic.

---

# Performance Requirements

Dashboard should load

```
< 1 Second
```

Recommended

Perform aggregation queries.

Avoid

Multiple nested database calls.

Avoid

N+1 queries.

---

# Caching

Not required for MVP.

Future support

```
Redis
```

may cache

- Dashboard Statistics
- Charts
- Analytics

Architecture should remain compatible.

---

# Dashboard Refresh

Dashboard data should always reflect

Current database state.

No manual refresh logic required.

Frontend refreshes by calling APIs.

---

# Expected Schemas

```
TeacherDashboardResponse

StudentDashboardResponse

TeacherChartsResponse

StudentChartsResponse

ActivityResponse
```

---

# Business Rules

Teacher Dashboard

Institution-wide data.

Student Dashboard

Personal academic data only.

Attendance

Calculated dynamically.

Average Marks

Calculated dynamically.

Performance Score

Calculated dynamically.

Pending Reviews

Calculated dynamically.

---

# Dashboard Widgets

Teacher

```
Total Students

Attendance

Average Marks

Subjects

Assignments

Pending Reviews

At-Risk Students
```

Student

```
Attendance %

Average Marks

Grade

Assignments

Performance

Subjects
```

---

# Security

Teacher Dashboard

Teacher only.

Student Dashboard

Student only.

Students must never access institutional statistics.

---

# Swagger Documentation

Document

- Dashboard Summary
- Charts
- Activity
- Authentication
- Authorization
- Response Models

---

# API Testing

Verify

✓ Teacher Dashboard

✓ Student Dashboard

✓ Dashboard Authorization

✓ Charts

✓ Activity Feed

✓ Statistics

✓ Authentication

✓ Performance

---

# Future Compatibility

Dashboard architecture should support

- Live Notifications

- AI Insights

- Predictive Analytics

- Custom Widgets

- Widget Rearrangement

- Export Dashboard

- Real-time Charts

without redesigning existing endpoints.

---

# Definition of Completion

Dashboard API is complete when

✓ Teacher Dashboard works.

✓ Student Dashboard works.

✓ Charts work.

✓ Activity feed works.

✓ Dashboard statistics correct.

✓ Authentication enforced.

✓ Authorization enforced.

✓ Swagger complete.

✓ Tests pass.

---

# Summary

The Dashboard API provides aggregated, visualization-ready academic insights for both teachers and students.

It serves as the presentation layer for institutional analytics by combining data from Attendance, Marks, Assignments, Submissions, Students, and Subjects into fast, secure, and standardized REST endpoints.

End of Dashboard API Specification.