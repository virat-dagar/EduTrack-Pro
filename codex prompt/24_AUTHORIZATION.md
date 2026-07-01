# 24_AUTHORIZATION.md

# EduTrack Pro — Authorization Module Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Authorization

---

# Purpose

The Authorization module determines **what an authenticated user is allowed to do** within EduTrack Pro.

Authentication answers

> **Who is the user?**

Authorization answers

> **What is the user allowed to access?**

These responsibilities must remain completely separate.

Authentication should always occur before authorization.

---

# Authorization Responsibilities

The Authorization module is responsible for

- Role-Based Access Control (RBAC)
- Permission Validation
- Resource Ownership Validation
- Protected Endpoint Access
- Feature Restrictions
- Role Enforcement

The Authorization module is NOT responsible for

- Login
- Password Verification
- JWT Generation
- Password Hashing
- Business Calculations
- Database CRUD

---

# Authorization Philosophy

Every request should pass through two checks.

```
Authentication

↓

Authorization

↓

Business Logic
```

A request should never reach the Service Layer unless both checks succeed.

---

# Supported Roles

The MVP supports two roles.

```
teacher

student
```

Future versions may introduce

```
admin

parent

faculty

hod

principal
```

The architecture should remain extensible.

---

# Role Hierarchy

```
Teacher

↓

Student
```

Teachers possess administrative academic privileges.

Students possess read-only personal privileges.

---

# Teacher Permissions

Teachers may

✓ View all students

✓ Create students

✓ Update students

✓ Delete students

✓ View all attendance

✓ Mark attendance

✓ Update attendance

✓ Delete attendance

✓ View all marks

✓ Add marks

✓ Update marks

✓ Delete marks

✓ Create assignments

✓ Update assignments

✓ Delete assignments

✓ View all submissions

✓ Review submissions

✓ Generate reports

✓ Access analytics

✓ View dashboards

---

# Student Permissions

Students may

✓ View own profile

✓ View own attendance

✓ View own marks

✓ View own assignments

✓ View own submissions

✓ Submit assignments

✓ View dashboard

✓ View reports

Students may NOT

✗ View other students

✗ Create attendance

✗ Modify attendance

✗ Enter marks

✗ Modify marks

✗ Delete academic records

✗ Create assignments

✗ Access teacher analytics

✗ Access teacher dashboard

---

# Permission Matrix

| Feature | Teacher | Student |
|----------|:-------:|:-------:|
| Login | ✓ | ✓ |
| View Own Profile | ✓ | ✓ |
| View All Students | ✓ | ✗ |
| Create Student | ✓ | ✗ |
| Edit Student | ✓ | ✗ |
| Delete Student | ✓ | ✗ |
| View Attendance | ✓ | Own Only |
| Mark Attendance | ✓ | ✗ |
| Edit Attendance | ✓ | ✗ |
| View Marks | ✓ | Own Only |
| Enter Marks | ✓ | ✗ |
| Edit Marks | ✓ | ✗ |
| Create Assignment | ✓ | ✗ |
| Edit Assignment | ✓ | ✗ |
| Delete Assignment | ✓ | ✗ |
| Submit Assignment | ✗ | ✓ |
| Review Submission | ✓ | ✗ |
| Dashboard | Teacher | Student |
| Analytics | ✓ | Limited |
| Reports | ✓ | Own Only |

---

# Authorization Workflow

```
Authenticated User

↓

Extract Role

↓

Check Permission

↓

Authorized

↓

Execute Service

OR

↓

403 Forbidden
```

---

# Protected Endpoint Workflow

Every protected endpoint should perform

```
JWT Validation

↓

Current User

↓

Role Verification

↓

Ownership Verification

↓

Business Logic
```

No endpoint should skip authorization.

---

# Ownership Rules

Some resources require ownership validation.

Examples

Student Dashboard

Only the logged-in student may access it.

```
Current User

↓

Student ID

↓

Requested Student ID

↓

Match

↓

Allow
```

If IDs do not match

```
403 Forbidden
```

---

# Teacher Override

Teachers may access all academic records.

Examples

All Students

All Attendance

All Marks

All Assignments

All Reports

All Analytics

Teachers are institutional managers.

---

# Student Restrictions

Students are limited to their own academic information.

Examples

Allowed

```
GET /students/me

GET /attendance/me

GET /marks/me

GET /assignments

GET /submissions/me
```

Not Allowed

```
GET /students

DELETE /students/2

POST /attendance

POST /marks

DELETE /assignments
```

---

# Authorization Dependencies

Expected reusable dependencies

```
get_current_user()

require_teacher()

require_student()

require_owner()
```

These dependencies should be reusable across routers.

---

# Endpoint Protection

Teacher-only endpoints

```
POST

PUT

DELETE
```

Academic management APIs

Student endpoints

```
GET

Own Resources

POST Submission
```

Never duplicate permission logic.

---

# Authorization Service

Expected file

```
services/auth_service.py
```

or

```
services/authorization_service.py
```

Responsibilities

- Verify Roles
- Verify Ownership
- Permission Helpers
- Resource Validation

Business permission logic belongs here.

---

# Router Responsibilities

Routers should

Authenticate

↓

Authorize

↓

Call Service

Authorization should occur before any business logic executes.

---

# Error Responses

Unauthorized

```
401 Unauthorized
```

Authenticated but insufficient permissions

```
403 Forbidden
```

Missing Resource

```
404 Not Found
```

Validation Failure

```
422 Unprocessable Entity
```

Unexpected Failure

```
500 Internal Server Error
```

---

# Authorization Response Example

```json
{
    "success": false,
    "message": "You do not have permission to perform this action."
}
```

Avoid exposing internal authorization details.

---

# Dashboard Authorization

Teacher Dashboard

Teacher only.

Student Dashboard

Student only.

Users attempting to access the wrong dashboard should receive

```
403 Forbidden
```

---

# Report Authorization

Teachers

May generate

- Institution Reports
- Student Reports
- Attendance Reports
- Marks Reports

Students

May generate only

- Personal Report
- Personal Attendance
- Personal Marks

---

# Analytics Authorization

Teachers

May access

- At-Risk Students
- Overall Performance
- Institution Statistics
- Department Statistics

Students

May access only

- Personal Analytics
- Personal Trends
- Personal Prediction

---

# Future Role Expansion

Architecture should support

```
Administrator

↓

Principal

↓

Head of Department

↓

Faculty

↓

Teacher

↓

Parent

↓

Student
```

Permission definitions should remain centralized.

---

# Security Principles

Never trust

Frontend role.

Frontend route.

Frontend hidden buttons.

Every request must be validated on the backend.

Frontend restrictions improve usability.

Backend restrictions provide security.

---

# Logging

Log

Permission denied events.

Suspicious access attempts.

Repeated authorization failures.

Do not log

Passwords.

JWT secrets.

Sensitive academic data.

---

# Swagger Documentation

Every protected endpoint should clearly indicate

Authentication Required

Required Role

Expected Responses

Permission Errors

Swagger should accurately reflect authorization requirements.

---

# Testing Requirements

Test

✓ Teacher access

✓ Student access

✓ Forbidden endpoints

✓ Ownership validation

✓ Teacher override

✓ Dashboard authorization

✓ Report authorization

✓ Analytics authorization

✓ Unauthorized requests

✓ Permission denied responses

---

# Best Practices

Always

Authenticate first.

Authorize second.

Execute business logic third.

Never combine authentication and authorization logic.

Never duplicate permission checks.

Keep authorization reusable.

---

# Definition of Completion

Authorization is complete when

✓ Role validation works.

✓ Ownership validation works.

✓ Teacher permissions enforced.

✓ Student restrictions enforced.

✓ Protected endpoints secure.

✓ Dashboard access controlled.

✓ Report access controlled.

✓ Analytics access controlled.

✓ Swagger documentation complete.

✓ Tests pass.

---

# Summary

The Authorization module protects every academic resource within EduTrack Pro through centralized Role-Based Access Control.

By separating identity verification from permission enforcement, the application remains secure, maintainable, and extensible for future roles and institutional requirements.

End of Authorization Module Specification.