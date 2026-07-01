# 38_SERVICE_LAYER.md

# EduTrack Pro — Service Layer Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Service Layer

---

# Purpose

The Service Layer contains all business logic for EduTrack Pro.

It acts as the bridge between

```
Routers

↓

Services

↓

Database Models
```

Routers should never directly interact with database models.

Every database operation must pass through the Service Layer.

---

# Service Layer Philosophy

The Service Layer is responsible for

- Business Rules
- Data Validation
- Database Operations
- Calculations
- Aggregations
- Error Handling
- Transaction Management

The Service Layer is NOT responsible for

- HTTP Requests
- API Routing
- HTML Rendering
- UI Logic
- Authentication Middleware

---

# Overall Architecture

```
Frontend

↓

FastAPI Router

↓

Authentication

↓

Authorization

↓

Service Layer

↓

SQLAlchemy Models

↓

Database
```

Every API request must flow through this architecture.

---

# Service Layer Directory

```
backend/

app/

services/

│

├── auth_service.py

├── user_service.py

├── student_service.py

├── subject_service.py

├── attendance_service.py

├── marks_service.py

├── assignment_service.py

├── submission_service.py

├── dashboard_service.py

├── report_service.py

├── analytics_service.py
```

Every business operation belongs inside one of these services.

---

# Responsibilities

Every service should

- Receive validated input
- Apply business rules
- Query database
- Validate relationships
- Handle exceptions
- Return structured results

Services should NEVER return HTTP responses.

They return Python objects.

Routers convert those into API responses.

---

# Standard Service Flow

```
Router

↓

Service Function

↓

Validation

↓

Business Logic

↓

Database Query

↓

Calculation

↓

Return Result

↓

Router Response
```

---

# Authentication Service

File

```
auth_service.py
```

Responsibilities

- Login
- Password Verification
- Password Hashing
- JWT Generation
- JWT Validation
- Current User
- Authentication Helpers

---

# User Service

File

```
user_service.py
```

Responsibilities

- Create User
- Update User
- Delete User
- List Users
- Search Users
- Activate User
- Deactivate User

---

# Student Service

File

```
student_service.py
```

Responsibilities

- Create Student
- Update Student
- Delete Student
- Student Search
- Student Filters
- Student Validation
- Student Profile

---

# Subject Service

File

```
subject_service.py
```

Responsibilities

- CRUD
- Search
- Filters
- Duplicate Validation
- Semester Queries

---

# Attendance Service

File

```
attendance_service.py
```

Responsibilities

- Mark Attendance
- Update Attendance
- Delete Attendance
- Attendance Percentage
- Attendance Summary
- Attendance History
- Duplicate Prevention

Attendance calculations belong only here.

---

# Marks Service

File

```
marks_service.py
```

Responsibilities

- Add Marks
- Update Marks
- Delete Marks
- Average Marks
- Grade Calculation
- Performance Score
- Academic Summary

Marks calculations should never occur inside routers.

---

# Assignment Service

File

```
assignment_service.py
```

Responsibilities

- Create Assignment
- Update Assignment
- Delete Assignment
- Upcoming Assignments
- Overdue Assignments
- Assignment Validation

---

# Submission Service

File

```
submission_service.py
```

Responsibilities

- Submit Assignment
- Review Submission
- Late Submission Detection
- Pending Reviews
- Submission History
- Duplicate Validation

---

# Dashboard Service

File

```
dashboard_service.py
```

Responsibilities

- Dashboard Cards
- Dashboard Charts
- Dashboard Statistics
- Recent Activity
- Aggregated Data

This service combines data from multiple modules.

---

# Report Service

File

```
report_service.py
```

Responsibilities

- Student Reports
- Attendance Reports
- Marks Reports
- Assignment Reports
- Institution Reports
- PDF Generation (Future)

---

# Analytics Service

File

```
analytics_service.py
```

Responsibilities

- At-Risk Students
- Performance Trends
- Attendance Trends
- Academic Insights
- Prediction Logic
- Scholarship Eligibility

Analytics should remain independent of CRUD services.

---

# Database Session Handling

Services receive

```
Database Session

(db: Session)
```

through dependency injection.

Services should never create database sessions manually.

---

# Validation Flow

```
Router

↓

Pydantic Validation

↓

Service Validation

↓

Database Constraints
```

Every important business rule belongs inside the Service Layer.

---

# Business Rule Examples

Attendance

```
Only one attendance record per

Student

+

Subject

+

Date
```

Marks

```
Marks

≤

Maximum Marks
```

Assignments

```
Due Date

≥

Assigned Date
```

Submissions

```
One submission

Per student

Per assignment
```

Services enforce these rules.

---

# Transactions

Every write operation should follow

```
Create

↓

Commit

↓

Refresh

↓

Return Object
```

On failure

```
Rollback

↓

Raise Exception
```

Never leave incomplete transactions.

---

# Error Handling

Services should raise

Custom Exceptions

Examples

```
DuplicateStudentException

SubjectNotFoundException

AttendanceAlreadyExists

UnauthorizedAccess

InvalidMarksException
```

Routers convert exceptions into HTTP responses.

---

# Logging

Services should log

- Critical Failures
- Unexpected Errors
- Business Violations

Never log

- Passwords
- JWT Tokens
- Secrets

---

# Dependency Rules

Services may call

Utility Functions

Analytics Service

Helper Functions

Services should avoid circular dependencies.

---

# Reusability

Business logic should exist only once.

Bad

```
Attendance %

Calculated

Router

Dashboard

Reports
```

Good

```
Attendance Service

↓

Dashboard

Reports

Analytics
```

Everything calls one implementation.

---

# Performance

Services should

Use indexes.

Use efficient queries.

Avoid duplicate database calls.

Avoid N+1 queries.

Batch queries when possible.

---

# Unit Testing

Each service should have dedicated tests.

Verify

✓ CRUD

✓ Validation

✓ Business Rules

✓ Transactions

✓ Error Handling

✓ Edge Cases

Services should be independently testable.

---

# Future Compatibility

Architecture should support

- Machine Learning

- AI Insights

- Email Service

- Notification Service

- SMS Service

- Audit Logs

- Redis Cache

- Celery Workers

without redesigning the Service Layer.

---

# Service Checklist

Every service should

✓ Perform validation.

✓ Apply business rules.

✓ Query database.

✓ Handle transactions.

✓ Raise meaningful exceptions.

✓ Return structured objects.

✓ Avoid HTTP logic.

✓ Remain reusable.

---

# Definition of Completion

Service Layer implementation is complete when

✓ Every router calls a service.

✓ Business logic centralized.

✓ Database operations isolated.

✓ Validation implemented.

✓ Transactions safe.

✓ Exceptions handled.

✓ Tests pass.

---

# Summary

The Service Layer is the core business engine of EduTrack Pro.

It separates business logic from API routing, centralizes validation and calculations, ensures reusable and maintainable code, and provides the foundation for dashboards, analytics, reports, and future system expansion.

End of Service Layer Specification.