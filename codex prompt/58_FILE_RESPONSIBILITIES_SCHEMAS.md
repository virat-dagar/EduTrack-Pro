# 58_FILE_RESPONSIBILITIES_SCHEMAS.md

# EduTrack Pro — Schema File Responsibilities Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Schema File Responsibilities

---

# Purpose

This document defines the responsibility of every Pydantic schema inside EduTrack Pro.

Schemas act as the communication contract between the API and its clients.

They validate incoming data, serialize outgoing data, and ensure that the API remains secure, predictable, and consistent.

Schemas should never contain database logic or business logic.

---

# Schema Philosophy

Schemas exist to

- Validate Request Data
- Serialize Response Data
- Enforce API Contracts
- Improve Developer Experience
- Prevent Invalid Input

Schemas should NOT

- Query the database
- Perform calculations
- Authenticate users
- Authorize users
- Execute business rules

---

# Folder Structure

```
backend/

app/

schemas/

│

├── __init__.py

├── auth.py

├── user.py

├── student.py

├── subject.py

├── attendance.py

├── marks.py

├── assignment.py

├── submission.py

├── dashboard.py

├── report.py

└── common.py
```

---

# Overall Flow

```
HTTP Request

↓

Pydantic Schema

↓

Router

↓

Service

↓

Database

↓

Service

↓

Response Schema

↓

HTTP Response
```

Schemas validate both directions.

---

# Responsibilities

Every schema should define

✓ Input Validation

✓ Output Serialization

✓ Data Types

✓ Optional Fields

✓ Required Fields

✓ Examples

Nothing else.

---

# Schema Categories

Each entity should have multiple schemas.

Example

```
Create Schema

Update Schema

Response Schema

List Response Schema
```

Avoid using one schema for every operation.

---

# Naming Convention

Use

```
EntityCreate

EntityUpdate

EntityResponse

EntityListResponse
```

Examples

```
StudentCreate

StudentUpdate

StudentResponse

StudentListResponse
```

---

# auth.py

Purpose

Authentication schemas.

Contains

```
LoginRequest

LoginResponse

TokenResponse

CurrentUserResponse
```

---

# LoginRequest

Contains

```
email

password
```

Validation

```
Email Format

Minimum Password Length
```

---

# LoginResponse

Contains

```
access_token

token_type

user
```

Never expose

```
password

password_hash
```

---

# user.py

Contains

```
UserCreate

UserUpdate

UserResponse

UserListResponse
```

Validation

```
Email

Role

Required Fields
```

---

# student.py

Contains

```
StudentCreate

StudentUpdate

StudentResponse

StudentSummary

StudentListResponse
```

Validation

```
Roll Number

Semester

Email

Phone

Course
```

Response should exclude unnecessary internal fields.

---

# subject.py

Contains

```
SubjectCreate

SubjectUpdate

SubjectResponse
```

Validation

```
Subject Code

Credits

Semester
```

---

# attendance.py

Contains

```
AttendanceCreate

AttendanceUpdate

AttendanceResponse

AttendanceSummary
```

Validation

```
Student ID

Subject ID

Attendance Status

Date
```

Allowed Status

```
Present

Absent

Late
```

---

# marks.py

Contains

```
MarksCreate

MarksUpdate

MarksResponse

MarksSummary
```

Validation

```
Marks >= 0

Marks <= Maximum Marks
```

---

# assignment.py

Contains

```
AssignmentCreate

AssignmentUpdate

AssignmentResponse

AssignmentSummary
```

Validation

```
Title

Deadline

Description

Subject
```

---

# submission.py

Contains

```
SubmissionCreate

SubmissionUpdate

SubmissionResponse
```

Validation

```
Assignment ID

Student ID

Submission Status
```

---

# dashboard.py

Contains

```
TeacherDashboardResponse

StudentDashboardResponse

StatisticsCard

ChartResponse

ActivityItem
```

Dashboard schemas are

Read-only.

---

# report.py

Contains

```
StudentReport

AttendanceReport

PerformanceReport

InstitutionReport
```

Future

```
PDF Metadata

Export Response
```

---

# common.py

Contains reusable schemas.

Examples

```
Pagination

APIResponse

ErrorResponse

SuccessResponse

MessageResponse
```

Avoid duplicating common response models.

---

# __init__.py

Exports

```
Authentication Schemas

Student Schemas

Attendance Schemas

Marks Schemas

Assignment Schemas

Dashboard Schemas
```

Simplifies imports.

---

# Request Schemas

Purpose

Validate incoming requests.

Example

```
POST

PUT

PATCH
```

Should reject invalid input before reaching services.

---

# Response Schemas

Purpose

Control API output.

Prevent accidental exposure of

```
Password Hash

Internal IDs

Sensitive Metadata
```

---

# Validation Rules

Use Pydantic validation for

```
Email

String Length

Integer Range

Date

Enum Values

Lists
```

Prefer schema validation over manual validation.

---

# Optional Fields

Use

```
Optional[]
```

only when data is genuinely optional.

Avoid making everything optional.

---

# Default Values

Allowed

```
is_active=True

status="Pending"

created_at=None
```

Avoid business-related defaults.

---

# Enums

Prefer enums for

```
Role

Attendance Status

Assignment Status

Submission Status

Risk Level
```

Avoid raw strings.

---

# Nested Schemas

Allowed.

Example

```
StudentResponse

↓

AttendanceSummary

↓

MarksSummary
```

Avoid deeply nested objects.

---

# ORM Compatibility

Enable

```
from_attributes = True
```

(Pydantic v2)

or

```
orm_mode = True
```

(Pydantic v1)

Allows automatic serialization from SQLAlchemy models.

---

# Serialization Rules

Never expose

```
password_hash

JWT Secret

Database Internals
```

Only expose API-safe fields.

---

# Error Schema

Standard

```
success

message

errors

timestamp
```

Used consistently across APIs.

---

# Pagination Schema

Contains

```
items

page

page_size

total

total_pages
```

Reusable across every module.

---

# Business Logic

Never implement

```
calculate_grade()

calculate_attendance()

calculate_performance()
```

Schemas validate only.

---

# Import Rules

Allowed

```
schemas

↓

models (for ORM compatibility)

or

typing
```

Not Allowed

```
schemas

↓

routers
```

Not Allowed

```
schemas

↓

services
```

Not Allowed

```
schemas

↓

database
```

---

# Security

Never expose

```
password_hash

internal_notes

audit_logs

JWT Secret
```

Use dedicated response schemas.

---

# Performance

Keep schemas lightweight.

Avoid extremely deep nesting.

Reuse common schemas whenever possible.

---

# Documentation

Every schema should include

```
Field Descriptions

Examples

Validation Rules
```

Improves automatic Swagger/OpenAPI documentation.

---

# Future Compatibility

Schema architecture should support

```
API Versioning

GraphQL

WebSockets

Mobile API

AI Endpoints

Bulk Operations
```

without redesign.

---

# Testing

Verify

✓ Validation

✓ Serialization

✓ Required Fields

✓ Optional Fields

✓ Enum Validation

✓ Nested Models

✓ Error Responses

✓ Pagination Responses

---

# Schema Checklist

Every schema should

✓ Validate input.

✓ Serialize output.

✓ Be reusable.

✓ Avoid business logic.

✓ Support OpenAPI.

✓ Protect sensitive data.

✓ Follow naming conventions.

---

# Definition of Completion

Schema File Responsibilities are complete when

✓ Every API endpoint has request and response schemas.

✓ Validation rules enforced.

✓ Sensitive fields protected.

✓ Pagination standardized.

✓ Documentation generated correctly.

---

# Summary

The Schema File Responsibilities specification establishes the validation and serialization layer of EduTrack Pro.

By separating request validation, response formatting, and API contracts from business logic and database models, the application maintains a secure, predictable, well-documented, and scalable API architecture that follows modern FastAPI and Pydantic best practices.

End of Schema File Responsibilities Specification.