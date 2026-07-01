# 62_FILE_RESPONSIBILITIES_EXCEPTIONS.md

# EduTrack Pro — Exception File Responsibilities Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Exception File Responsibilities

---

# Purpose

This document defines the exception architecture of EduTrack Pro.

The Exception Layer standardizes how errors are created, raised, propagated, and returned throughout the application.

A predictable exception system makes the application

- Easier to debug
- Easier to maintain
- Easier to test
- Easier to extend
- More professional

Every exception should have one clear meaning.

---

# Exception Philosophy

Errors are not failures.

Errors are expected outcomes that must be handled gracefully.

Every exception should answer

> "What exactly went wrong?"

Avoid generic exceptions whenever possible.

---

# Exception Architecture

```
Frontend

↓

HTTP Request

↓

Router

↓

Service

↓

Exception Raised

↓

Exception Handler

↓

Standard API Response

↓

Frontend Error UI
```

Exceptions should never bypass the handler.

---

# Folder Structure

```
backend/

app/

exceptions/

│

├── __init__.py

├── base.py

├── auth.py

├── users.py

├── students.py

├── subjects.py

├── attendance.py

├── marks.py

├── assignments.py

├── submissions.py

├── reports.py

├── analytics.py

└── handlers.py
```

---

# Responsibilities

The Exception Layer is responsible for

✓ Defining custom exceptions

✓ Grouping related exceptions

✓ Standardizing responses

✓ Centralizing error handling

✓ Improving debugging

The Exception Layer should NOT

✗ Query the database

✗ Perform authentication

✗ Implement business logic

✗ Generate reports

---

# Exception Flow

```
Request

↓

Router

↓

Service

↓

Raise Exception

↓

Global Handler

↓

JSON Response

↓

Frontend
```

---

# Base Exception

File

```
base.py
```

Purpose

Defines the application's base exception.

Every custom exception should inherit from

```
EduTrackException
```

Contains

```
Message

Status Code

Error Code

Details

Timestamp
```

---

# Authentication Exceptions

File

```
auth.py
```

Contains

```
InvalidCredentials

InvalidToken

ExpiredToken

Unauthorized

Forbidden

InactiveAccount
```

HTTP Codes

```
401

403
```

---

# User Exceptions

File

```
users.py
```

Contains

```
UserNotFound

DuplicateEmail

InvalidRole

UserAlreadyExists

CannotDeleteSelf
```

---

# Student Exceptions

File

```
students.py
```

Contains

```
StudentNotFound

DuplicateRollNumber

DuplicateStudentEmail

InvalidSemester

InvalidCourse
```

---

# Subject Exceptions

File

```
subjects.py
```

Contains

```
SubjectNotFound

DuplicateSubjectCode

InvalidCredits

TeacherNotAssigned
```

---

# Attendance Exceptions

File

```
attendance.py
```

Contains

```
AttendanceNotFound

AttendanceAlreadyMarked

InvalidAttendanceStatus

AttendanceLocked

AttendanceDateInvalid
```

---

# Marks Exceptions

File

```
marks.py
```

Contains

```
MarksNotFound

InvalidMarks

MaximumMarksExceeded

DuplicateMarksEntry

ExamTypeInvalid
```

---

# Assignment Exceptions

File

```
assignments.py
```

Contains

```
AssignmentNotFound

DeadlinePassed

AssignmentClosed

DuplicateAssignment

InvalidDeadline
```

---

# Submission Exceptions

File

```
submissions.py
```

Contains

```
SubmissionNotFound

AlreadySubmitted

SubmissionClosed

ReviewAlreadyCompleted

SubmissionDeadlinePassed
```

---

# Analytics Exceptions

File

```
analytics.py
```

Contains

```
AnalyticsUnavailable

InsufficientData

InvalidAnalyticsRange
```

---

# Report Exceptions

File

```
reports.py
```

Contains

```
ReportGenerationFailed

ReportNotFound

InvalidReportType

ExportFailed
```

---

# handlers.py

Purpose

Global exception handlers.

Responsibilities

```
Catch Exceptions

Convert to JSON

Assign Status Codes

Log Errors

Return Standard Response
```

Should register handlers inside

```
main.py
```

---

# __init__.py

Purpose

Expose all exception classes.

Simplifies imports.

---

# Exception Categories

System

```
500 Internal Errors
```

Validation

```
400

422
```

Authentication

```
401
```

Authorization

```
403
```

Missing Resources

```
404
```

Conflict

```
409
```

---

# Standard Response Format

Every error should return

```json
{
  "success": false,
  "message": "Student not found.",
  "error_code": "STUDENT_NOT_FOUND",
  "details": {},
  "timestamp": "2026-07-01T12:00:00Z"
}
```

Every endpoint should use the same format.

---

# Error Codes

Use descriptive error codes.

Examples

```
INVALID_TOKEN

USER_NOT_FOUND

STUDENT_NOT_FOUND

DUPLICATE_EMAIL

INVALID_MARKS

ATTENDANCE_ALREADY_MARKED

SUBMISSION_CLOSED
```

Never expose stack traces.

---

# Raising Exceptions

Only the

```
Service Layer
```

should raise business exceptions.

Routers should

Catch

↓

Return Response

---

# Validation Errors

Handled automatically by

```
Pydantic
```

Global handler should format them consistently.

---

# Logging

Log

```
Timestamp

Exception Type

Request Path

HTTP Method

User ID (if available)

Message
```

Never log

```
Passwords

JWT

Secrets

Sensitive Student Records
```

---

# HTTP Status Mapping

| Exception | Status |
|------------|--------|
| InvalidCredentials | 401 |
| InvalidToken | 401 |
| Unauthorized | 401 |
| Forbidden | 403 |
| StudentNotFound | 404 |
| SubjectNotFound | 404 |
| AssignmentNotFound | 404 |
| DuplicateEmail | 409 |
| DuplicateRollNumber | 409 |
| AttendanceAlreadyMarked | 409 |
| InvalidMarks | 400 |
| ValidationError | 422 |
| InternalServerError | 500 |

---

# Unexpected Exceptions

Any unexpected exception should

```
Log Error

↓

Return

500

↓

Generic Message
```

Never expose

```
Python Traceback
```

to clients.

---

# Frontend Compatibility

Frontend should receive

```
Message

↓

Display Toast

↓

Optional Retry
```

No frontend parsing of stack traces.

---

# Exception Hierarchy

```
EduTrackException

│

├── AuthenticationException

├── ValidationException

├── NotFoundException

├── ConflictException

├── ReportException

├── AnalyticsException

└── DatabaseException
```

Inheritance reduces duplication.

---

# Dependency Rules

Allowed

```
Services

↓

Exceptions
```

Allowed

```
Handlers

↓

Exceptions
```

Not Allowed

```
Exceptions

↓

Services
```

Not Allowed

```
Exceptions

↓

Database
```

---

# Performance

Exception creation should be lightweight.

Avoid expensive formatting.

Only capture stack traces when necessary.

---

# Testing

Verify

✓ Custom exceptions

✓ Status codes

✓ Global handler

✓ Validation formatting

✓ Authentication errors

✓ Authorization errors

✓ Conflict responses

✓ Unexpected exceptions

✓ Logging

---

# Documentation

Every exception should define

```
Purpose

Status Code

Message

Error Code
```

Keep names descriptive.

---

# Future Compatibility

Exception architecture should support

```
API Versioning

Localization

Internationalized Messages

Distributed Logging

Sentry

Cloud Monitoring

Audit Trails
```

without restructuring.

---

# Exception Checklist

Every exception should

✓ Have one purpose.

✓ Use descriptive names.

✓ Map to proper HTTP status.

✓ Return standardized JSON.

✓ Avoid leaking internal details.

✓ Be independently testable.

---

# Definition of Completion

Exception File Responsibilities are complete when

✓ Custom exceptions defined.

✓ Global handler implemented.

✓ Standard response format enforced.

✓ Logging integrated.

✓ HTTP status mapping complete.

✓ Tests pass.

---

# Summary

The Exception File Responsibilities specification establishes a centralized and standardized error-handling architecture for EduTrack Pro.

By organizing exceptions into domain-specific modules, enforcing consistent response formats, and separating business errors from infrastructure concerns, the application achieves predictable behavior, improved debugging, stronger security, and a professional API experience suitable for production-grade software.

End of Exception File Responsibilities Specification.