# 60_FILE_RESPONSIBILITIES_SERVICES.md

# EduTrack Pro — Service File Responsibilities Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Service File Responsibilities

---

# Purpose

This document defines the responsibility of every Service Layer file inside EduTrack Pro.

The Service Layer is the heart of the backend.

It contains all business logic, calculations, workflows, validations, and interactions between the API and the database.

Every operation performed by the application should pass through the Service Layer.

---

# Service Philosophy

The Service Layer is responsible for answering one question:

> "How should the application behave?"

Routers expose APIs.

Models represent data.

Schemas validate data.

Database manages persistence.

Services decide what actually happens.

---

# Architecture Position

```
Frontend

↓

Router

↓

Service

↓

Database

↓

Models
```

Every backend request should flow through services.

---

# Folder Structure

```
backend/

app/

services/

│

├── __init__.py

├── auth_service.py

├── user_service.py

├── student_service.py

├── subject_service.py

├── attendance_service.py

├── marks_service.py

├── assignment_service.py

├── submission_service.py

├── dashboard_service.py

├── analytics_service.py

├── report_service.py
```

---

# Overall Workflow

```
HTTP Request

↓

Router

↓

Schema Validation

↓

Service

↓

Database

↓

Response
```

Services coordinate the application.

---

# Responsibilities

Every service may

✓ Query database

✓ Validate business rules

✓ Calculate analytics

✓ Call other services

✓ Handle transactions

✓ Raise exceptions

✓ Return structured data

Services should NOT

✗ Define API routes

✗ Render frontend

✗ Define database tables

✗ Store global state

---

# auth_service.py

Purpose

Authentication logic.

Responsibilities

```
Authenticate User

Verify Password

Generate JWT

Validate JWT

Load Current User
```

Future

```
Refresh Tokens

Forgot Password

Reset Password

Multi-Factor Authentication
```

---

# user_service.py

Purpose

User management.

Responsibilities

```
Create User

Update User

Delete User

List Users

Get User

Activate User

Deactivate User
```

Should validate

```
Unique Email

Role

Permissions
```

---

# student_service.py

Purpose

Student management.

Responsibilities

```
Create Student

Update Student

Delete Student

Search Student

Get Student

List Students
```

Business validation

```
Roll Number

Email

Semester

Course
```

---

# subject_service.py

Purpose

Subject management.

Responsibilities

```
Create Subject

Update Subject

Delete Subject

Assign Teacher

List Subjects
```

---

# attendance_service.py

Purpose

Attendance management.

Responsibilities

```
Mark Attendance

Update Attendance

Delete Attendance

Attendance Summary

Attendance Percentage

Attendance History
```

Business rules

```
No duplicate attendance

Valid attendance status

Date validation
```

---

# marks_service.py

Purpose

Marks management.

Responsibilities

```
Add Marks

Update Marks

Delete Marks

Calculate Average

Calculate Grade

Subject Statistics
```

Business validation

```
Marks Range

Maximum Marks

Duplicate Entry
```

---

# assignment_service.py

Purpose

Assignment management.

Responsibilities

```
Create Assignment

Update Assignment

Delete Assignment

Upcoming Assignments

Overdue Assignments
```

Business rules

```
Deadline Validation

Teacher Ownership
```

---

# submission_service.py

Purpose

Submission management.

Responsibilities

```
Submit Assignment

Update Submission

Delete Submission

Review Submission

Assign Marks

Feedback
```

Business validation

```
Submission Deadline

Duplicate Submission

Assignment Exists
```

---

# dashboard_service.py

Purpose

Dashboard aggregation.

Responsibilities

Teacher Dashboard

Student Dashboard

Statistics

Recent Activity

Charts

Quick Actions

No business calculations.

Dashboard consumes

```
Analytics Service
```

---

# analytics_service.py

Purpose

Academic analytics.

Responsibilities

```
Attendance %

Average Marks

Performance Score

Risk Level

Scholarship Eligibility

Top Performers

Performance Trends
```

This service contains

Most application calculations.

---

# report_service.py

Purpose

Report generation.

Responsibilities

```
Student Report

Attendance Report

Marks Report

Institution Report

Performance Report

PDF Preparation
```

Reports consume

Analytics Service.

---

# __init__.py

Purpose

Export services.

Simplifies imports.

---

# Business Logic

Only services should implement

```
Attendance Percentage

Average Marks

Performance Score

Grade Calculation

Scholarship Eligibility

Risk Detection
```

Never implement these inside

```
Routers

Models

Schemas
```

---

# Cross-Service Communication

Allowed

```
Dashboard Service

↓

Analytics Service
```

Allowed

```
Report Service

↓

Analytics Service
```

Allowed

```
Submission Service

↓

Assignment Service
```

Avoid circular service dependencies.

---

# Validation

Services perform

Business validation.

Examples

```
Student Exists

Assignment Open

Attendance Not Duplicate

Teacher Authorized
```

Input validation remains in schemas.

---

# Database Access

Services are the only layer that should interact directly with ORM models.

Example

```
Service

↓

SQLAlchemy Session

↓

Query

↓

Commit
```

---

# Transactions

Every write operation

```
Begin

↓

Validate

↓

Execute

↓

Commit

↓

Rollback if Failure
```

---

# Exception Handling

Services raise

```
StudentNotFound

SubjectNotFound

DuplicateAttendance

DuplicateSubmission

UnauthorizedAction

ValidationException
```

Routers return responses.

---

# Logging

Services should log

```
Student Created

Attendance Marked

Assignment Submitted

Report Generated

Authentication Success

Authentication Failure
```

Never log

```
Passwords

JWT

Sensitive Personal Information
```

---

# Performance

Services should

Batch queries.

Avoid N+1 queries.

Reuse analytics.

Avoid duplicated calculations.

---

# Return Values

Services return

```
Models

DTO-like Objects

Structured Dictionaries
```

Routers serialize them using schemas.

---

# Import Rules

Allowed

```
Models

Database

Utils

Exceptions

Other Services (when appropriate)
```

Not Allowed

```
Services

↓

Routers
```

Not Allowed

```
Services

↓

Frontend
```

---

# Dependency Rules

Preferred

```
Router

↓

Service

↓

Model
```

Avoid

```
Service

↓

Router
```

Avoid

```
Service

↓

Service

↓

Service

↓

Service
```

Keep dependencies shallow.

---

# Caching

Not required for MVP.

Future

```
Redis

Memory Cache

Analytics Cache
```

should integrate here.

---

# Testing

Every service should test

✓ Successful execution

✓ Invalid input

✓ Missing records

✓ Authorization

✓ Transactions

✓ Rollback

✓ Database failures

✓ Business rules

---

# Future Compatibility

Service architecture should support

```
Background Jobs

Task Queue

Email Notifications

SMS

AI Recommendations

Machine Learning

Microservices

Event Bus
```

without redesign.

---

# Service Checklist

Every service should

✓ Own business logic.

✓ Query database.

✓ Validate business rules.

✓ Handle transactions.

✓ Raise meaningful exceptions.

✓ Remain independently testable.

✓ Avoid presentation logic.

---

# Definition of Completion

Service File Responsibilities are complete when

✓ Every module has its own service.

✓ Business logic centralized.

✓ Transactions handled.

✓ Validation implemented.

✓ Analytics separated.

✓ Reports separated.

✓ Tests pass.

---

# Summary

The Service Layer is the operational core of EduTrack Pro.

It orchestrates every business workflow by coordinating validation, database operations, analytics, reporting, and transaction management while keeping routers lightweight and models focused solely on persistence.

By centralizing application behavior inside dedicated service modules, EduTrack Pro achieves a clean, scalable, maintainable, and enterprise-grade backend architecture that is easy to extend and test.

End of Service File Responsibilities Specification.