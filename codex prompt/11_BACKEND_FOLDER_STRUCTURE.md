# 11_BACKEND_FOLDER_STRUCTURE.md

# EduTrack Pro — Backend Folder Structure

Version: 1.0

Status: Final

Architecture Status: Frozen

---

# Purpose

This document defines the implementation responsibilities of every backend folder.

The backend architecture has already been finalized.

Every backend file created during implementation must belong to exactly one folder and must follow that folder's responsibility.

Do not move files between folders.

Do not create duplicate folders.

Do not create alternate architectures.

---

# Backend Root

```
backend/

│

├── app/

├── tests/

├── requirements.txt

├── alembic.ini

├── README.md

└── main.py
```

Backend contains every server-side responsibility.

No frontend logic belongs here.

---

# Backend Entry Point

```
backend/main.py
```

Purpose

Application entry point.

Responsibilities

- Start FastAPI application
- Register routers
- Register middleware
- Register exception handlers
- Register CORS
- Initialize database
- Launch Swagger documentation

Must NOT contain

- Business logic
- CRUD operations
- Authentication logic
- Database queries

---

# app/

Purpose

Contains the complete FastAPI application.

Every backend implementation belongs somewhere inside this directory.

```
app/

├── core/

├── database/

├── models/

├── schemas/

├── routers/

├── services/

├── utils/

├── exceptions/

└── main.py
```

Each folder owns one responsibility.

---

# app/core/

Purpose

Application-wide configuration.

Contains

- JWT configuration
- Security configuration
- Password hashing
- Environment configuration
- Application settings
- Global constants
- Authentication helpers

Examples

```
core/

config.py

security.py

auth.py

constants.py
```

Responsibilities

- Application configuration
- Secret management
- Password hashing
- JWT creation
- JWT verification
- Environment variables

Must NOT contain

- Database models
- CRUD logic
- API endpoints
- Analytics
- Dashboard logic

---

# app/database/

Purpose

Database initialization.

Contains

```
database/

base.py

session.py

connection.py
```

Responsibilities

- SQLAlchemy engine
- Database session
- Declarative Base
- Connection management

Should expose

Database Session

Engine

Base

Should NOT contain

- Queries
- Business logic
- Validation
- API logic

---

# app/models/

Purpose

Persistent entities.

Contains one SQLAlchemy model per database table.

Expected models

```
models/

user.py

student.py

subject.py

attendance.py

marks.py

assignment.py

submission.py
```

Responsibilities

- Table definitions
- Columns
- Relationships
- Constraints
- Indexes

Every model should

Define

Primary key

Foreign keys

Relationships

Unique constraints

Indexes

Must NOT

Validate requests

Return responses

Perform calculations

Authenticate users

---

# app/schemas/

Purpose

Pydantic schemas.

Expected structure

```
schemas/

user.py

student.py

subject.py

attendance.py

marks.py

assignment.py

submission.py

common.py
```

Each module should define

Create Schema

Update Schema

Response Schema

List Schema

Responsibilities

Validate

Incoming requests

Outgoing responses

Serialization

Must NOT

Query database

Perform calculations

Contain business rules

---

# app/routers/

Purpose

REST API endpoints.

Expected structure

```
routers/

auth.py

users.py

students.py

subjects.py

attendance.py

marks.py

assignments.py

submissions.py

dashboard.py

reports.py
```

Responsibilities

Receive HTTP requests.

Authenticate.

Authorize.

Call services.

Return responses.

Routers remain lightweight.

Should NOT

Query database directly.

Perform calculations.

Implement business logic.

---

# app/services/

Purpose

Business logic.

Expected structure

```
services/

auth_service.py

user_service.py

student_service.py

subject_service.py

attendance_service.py

marks_service.py

assignment_service.py

submission_service.py

dashboard_service.py

analytics_service.py

report_service.py
```

Responsibilities

CRUD

Business Rules

Calculations

Filtering

Searching

Sorting

Validation beyond schemas

Database interaction

Analytics

Prediction

Dashboard aggregation

Services are the heart of the backend.

Most application intelligence belongs here.

---

# app/utils/

Purpose

Reusable helper functions.

Examples

```
utils/

pagination.py

dates.py

helpers.py

responses.py

validators.py

search.py
```

Responsibilities

Reusable utilities.

Formatting.

Pagination.

Date helpers.

Common validation.

Response builders.

Utilities should remain generic.

Avoid module-specific logic.

---

# app/exceptions/

Purpose

Custom exception classes.

Expected files

```
exceptions/

authentication.py

authorization.py

students.py

attendance.py

marks.py

assignments.py

common.py
```

Responsibilities

Meaningful exceptions.

Readable errors.

Reusable error handling.

Avoid generic exceptions whenever practical.

---

# tests/

Purpose

Backend testing.

Suggested organization

```
tests/

test_auth.py

test_users.py

test_students.py

test_subjects.py

test_attendance.py

test_marks.py

test_assignments.py

test_dashboard.py

test_reports.py
```

Responsibilities

API testing.

Authentication testing.

CRUD testing.

Business rule testing.

Validation testing.

Integration testing.

Tests should mirror backend modules.

---

# Folder Dependency Rules

Allowed

```
Router

↓

Service

↓

Model

↓

Database
```

Allowed

```
Schema

↓

Router
```

Allowed

```
Service

↓

Utils
```

Allowed

```
Service

↓

Exceptions
```

Not Allowed

```
Router

↓

Database
```

Not Allowed

```
Model

↓

Router
```

Not Allowed

```
Model

↓

Service
```

Not Allowed

```
Schema

↓

Database
```

Not Allowed

```
Utils

↓

Business Logic
```

Maintain strict dependency direction.

---

# Backend File Organization

Every backend feature should have

```
Model

+

Schema

+

Router

+

Service
```

This structure should remain consistent.

Example

Student Module

```
models/student.py

schemas/student.py

routers/students.py

services/student_service.py
```

Attendance Module

```
models/attendance.py

schemas/attendance.py

routers/attendance.py

services/attendance_service.py
```

Repeat this pattern for every feature.

---

# Import Rules

Imports should always follow

Standard Library

↓

Third-Party Libraries

↓

Internal Project Imports

Avoid circular imports.

Avoid wildcard imports.

Use explicit imports wherever possible.

---

# Backend Coding Rules

Each file should

- Have one responsibility
- Remain modular
- Remain readable
- Be logically organized
- Avoid duplication
- Follow naming conventions
- Include appropriate documentation where necessary

---

# Backend Growth Rules

Future features should integrate naturally.

Examples

Notification Service

Parent Portal

Admin Module

AI Analytics

Docker Support

Cloud Storage

Redis

These additions should fit into the existing folder structure without requiring architectural changes.

---

# Backend Folder Structure Summary

The backend folder structure provides a clear separation between configuration, persistence, validation, business logic, routing, utilities, exceptions, and testing.

Every implementation should respect these boundaries.

No file should perform responsibilities belonging to another folder.

The backend architecture should remain modular, predictable, maintainable, and scalable throughout the lifetime of EduTrack Pro.

End of Backend Folder Structure.