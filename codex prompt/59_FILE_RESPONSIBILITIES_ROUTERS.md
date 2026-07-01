# 59_FILE_RESPONSIBILITIES_ROUTERS.md

# EduTrack Pro — Router File Responsibilities Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Router File Responsibilities

---

# Purpose

This document defines the responsibility of every FastAPI router inside EduTrack Pro.

Routers expose the REST API to frontend clients.

Their responsibility is to receive requests, validate input, call the appropriate service layer, and return standardized responses.

Routers should remain extremely lightweight.

---

# Router Philosophy

Routers act as the

```
HTTP Interface
```

between the frontend and backend.

Routers should only

- Receive Requests
- Validate Requests
- Authenticate Users
- Authorize Users
- Call Services
- Return Responses

Routers should NEVER

- Query the database
- Calculate analytics
- Implement business logic
- Perform complex validation
- Generate reports directly

---

# Folder Structure

```
backend/

app/

routers/

│

├── __init__.py

├── auth.py

├── users.py

├── students.py

├── subjects.py

├── attendance.py

├── marks.py

├── assignments.py

├── submissions.py

├── dashboard.py

├── reports.py

└── health.py
```

---

# Overall Request Flow

```
HTTP Request

↓

Router

↓

Schema Validation

↓

Authentication

↓

Authorization

↓

Service Layer

↓

Response Schema

↓

HTTP Response
```

Routers should never skip the service layer.

---

# Common Responsibilities

Every router should

✓ Register endpoints

✓ Validate request schema

✓ Inject dependencies

✓ Authenticate user

✓ Authorize user

✓ Call service

✓ Return response

---

# Router Naming

File Names

```
students.py

marks.py

attendance.py
```

Router Variable

```
router = APIRouter(...)
```

Avoid inconsistent naming.

---

# __init__.py

Purpose

Exports all routers.

Simplifies registration inside

```
main.py
```

---

# auth.py

Purpose

Authentication endpoints.

Endpoints

```
POST /login

GET /me
```

Future

```
POST /refresh

POST /logout

POST /forgot-password

POST /reset-password
```

Responsibilities

```
Authenticate User

Return JWT

Return Current User
```

---

# users.py

Purpose

User management.

Endpoints

```
GET /users

GET /users/{id}

POST /users

PUT /users/{id}

DELETE /users/{id}
```

Teacher only.

---

# students.py

Purpose

Student CRUD.

Endpoints

```
GET /students

GET /students/{id}

POST /students

PUT /students/{id}

DELETE /students/{id}
```

Responsibilities

```
Validate Request

Call Student Service

Return Response
```

---

# subjects.py

Purpose

Subject CRUD.

Endpoints

```
GET /subjects

GET /subjects/{id}

POST /subjects

PUT /subjects/{id}

DELETE /subjects/{id}
```

---

# attendance.py

Purpose

Attendance management.

Endpoints

```
GET /attendance

POST /attendance

PUT /attendance/{id}

DELETE /attendance/{id}

GET /attendance/student/{id}

GET /attendance/summary
```

---

# marks.py

Purpose

Marks management.

Endpoints

```
GET /marks

POST /marks

PUT /marks/{id}

DELETE /marks/{id}

GET /marks/student/{id}
```

---

# assignments.py

Purpose

Assignment management.

Endpoints

```
GET /assignments

GET /assignments/{id}

POST /assignments

PUT /assignments/{id}

DELETE /assignments/{id}
```

---

# submissions.py

Purpose

Assignment submissions.

Endpoints

```
GET /submissions

POST /submissions

PUT /submissions/{id}

DELETE /submissions/{id}

POST /submissions/{id}/review
```

---

# dashboard.py

Purpose

Dashboard APIs.

Endpoints

Teacher

```
GET /dashboard/teacher
```

Student

```
GET /dashboard/student
```

Charts

```
GET /dashboard/teacher/charts

GET /dashboard/student/charts
```

Recent Activity

```
GET /dashboard/teacher/activity

GET /dashboard/student/activity
```

Read-only.

---

# reports.py

Purpose

Report generation.

Endpoints

```
GET /reports/student

GET /reports/attendance

GET /reports/marks

GET /reports/performance

GET /reports/institution
```

Future

```
GET /reports/pdf

GET /reports/csv

GET /reports/excel
```

---

# health.py

Purpose

Health monitoring.

Endpoint

```
GET /health
```

Returns

```
Application Status

Database Status

Version
```

---

# Dependency Injection

Routers should use

```
Depends()
```

Examples

```
Database Session

Current User

Current Teacher

Current Student
```

Never instantiate dependencies manually.

---

# Authentication

Protected routers require

```
Valid JWT
```

Authentication should occur before calling services.

---

# Authorization

Teacher-only routes

Validate

```
Role == Teacher
```

Student routes

Validate

```
Ownership

OR

Student Role
```

Never trust frontend authorization.

---

# Request Validation

Handled automatically through

```
Pydantic Schemas
```

Reject invalid requests before reaching services.

---

# Response Serialization

Always return

```
Response Schemas
```

Never return raw ORM models.

---

# Error Handling

Routers should catch

```
Validation Errors

Authentication Errors

Authorization Errors
```

Business exceptions should bubble from services.

Return standardized responses.

---

# Status Codes

Use appropriate HTTP codes.

```
200 OK

201 Created

204 No Content

400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

422 Validation Error

500 Internal Server Error
```

---

# Pagination

List endpoints should support

```
page

page_size

search

sort

filter
```

Do not return unlimited records.

---

# Query Parameters

Use query parameters for

```
Search

Sorting

Filtering

Pagination
```

Avoid request bodies for GET endpoints.

---

# Logging

Routers may log

```
Endpoint Access

Authentication Failure

Unexpected Errors
```

Do not log

Passwords.

JWT Tokens.

Sensitive student data.

---

# Performance

Routers should

Remain lightweight.

Perform minimal processing.

Delegate everything to services.

---

# Import Rules

Allowed

```
schemas

services

dependencies

FastAPI
```

Not Allowed

```
routers

↓

database queries
```

Not Allowed

```
routers

↓

analytics calculations
```

---

# API Documentation

Every endpoint should include

```
Summary

Description

Response Model

Status Codes

Tags
```

FastAPI should generate complete OpenAPI documentation.

---

# Future Compatibility

Router architecture should support

```
API Versioning

Admin APIs

Parent Portal

Mobile APIs

Bulk Operations

WebSockets

GraphQL Gateway
```

without restructuring existing routers.

---

# Testing

Verify

✓ CRUD endpoints

✓ Authentication

✓ Authorization

✓ Validation

✓ Status codes

✓ Pagination

✓ Error handling

✓ Response schemas

---

# Router Checklist

Every router should

✓ Expose REST endpoints.

✓ Validate requests.

✓ Authenticate users.

✓ Authorize users.

✓ Call services.

✓ Return standardized responses.

✓ Avoid business logic.

---

# Definition of Completion

Router File Responsibilities are complete when

✓ Every module has its own router.

✓ Authentication enforced.

✓ Authorization enforced.

✓ CRUD endpoints complete.

✓ Documentation generated.

✓ Tests pass.

---

# Summary

The Router File Responsibilities specification defines the HTTP layer of EduTrack Pro.

By keeping routers lightweight and delegating business logic to the service layer, the backend remains modular, maintainable, testable, and aligned with Clean Architecture principles while providing a consistent REST API for the frontend.

End of Router File Responsibilities Specification.