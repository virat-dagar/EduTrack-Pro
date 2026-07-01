# 57_FILE_RESPONSIBILITIES_MODELS.md

# EduTrack Pro — Model File Responsibilities Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Model File Responsibilities

---

# Purpose

This document defines the responsibility of every SQLAlchemy model inside EduTrack Pro.

Models represent the application's database tables.

A model should describe

- Table Name
- Columns
- Relationships
- Constraints
- Indexes

A model should NEVER contain business logic.

---

# Model Philosophy

Models are responsible for representing data.

They are **not responsible** for

- API Logic
- Validation
- Authentication
- Authorization
- Business Rules
- Analytics
- Report Generation

Those belong to other layers.

---

# Folder Structure

```
backend/

app/

models/

│

├── __init__.py

├── user.py

├── student.py

├── subject.py

├── attendance.py

├── marks.py

├── assignment.py

├── submission.py
```

Future

```
notification.py

audit_log.py

department.py

semester.py
```

---

# Overall Architecture

```
Database

↓

Models

↓

Services

↓

Routers
```

Models should never import routers.

---

# Common Responsibilities

Every model should define

✓ Table Name

✓ Columns

✓ Primary Key

✓ Foreign Keys

✓ Relationships

✓ Constraints

✓ Indexes

Nothing more.

---

# Common Model Structure

Every model should contain

```
Class Definition

↓

__tablename__

↓

Columns

↓

Relationships

↓

__repr__()
```

Avoid helper methods unless absolutely necessary.

---

# user.py

Purpose

Represents application users.

Responsibilities

```
User Table

Authentication Data

Role Information

Account Status
```

Contains

```
id

name

email

password_hash

role

is_active

created_at

updated_at
```

Relationships

```
Student (Optional)

Assignments (Future)
```

---

# student.py

Purpose

Represents student records.

Contains

```
id

roll_number

full_name

course

semester

email

phone

date_of_birth

created_at

updated_at
```

Relationships

```
Attendance

Marks

Submissions
```

Should not store

Performance Score.

Attendance Percentage.

Grades.

These are calculated dynamically.

---

# subject.py

Purpose

Represents academic subjects.

Contains

```
id

subject_code

subject_name

semester

credits

teacher_id

created_at
```

Relationships

```
Marks

Assignments

Attendance
```

---

# attendance.py

Purpose

Stores attendance records.

Contains

```
id

student_id

subject_id

date

status

created_at
```

Relationships

```
Student

Subject
```

Status

```
Present

Absent

Late
```

---

# marks.py

Purpose

Stores examination marks.

Contains

```
id

student_id

subject_id

marks

maximum_marks

exam_type

created_at
```

Relationships

```
Student

Subject
```

Grades are NOT stored.

Grades are calculated.

---

# assignment.py

Purpose

Stores assignment metadata.

Contains

```
id

title

description

subject_id

deadline

created_by

created_at
```

Relationships

```
Subject

Submissions
```

---

# submission.py

Purpose

Stores assignment submissions.

Contains

```
id

assignment_id

student_id

submitted_at

status

marks

feedback
```

Relationships

```
Assignment

Student
```

---

# __init__.py

Purpose

Expose models.

Example

```
User

Student

Subject

Attendance

Marks

Assignment

Submission
```

Simplifies imports.

---

# Naming Convention

Classes

```
PascalCase
```

Example

```
Student

Attendance

Assignment
```

Table Names

```
snake_case
```

Example

```
students

attendance

assignments
```

---

# Column Naming

Use

```
snake_case
```

Examples

```
created_at

updated_at

student_id

subject_id
```

Avoid camelCase.

---

# Primary Keys

Every table should have

```
id
```

Type

```
Integer

Auto Increment
```

---

# Foreign Keys

Use explicit references.

Example

```
student_id

↓

students.id
```

Never use implicit relationships.

---

# Relationships

Use

```
relationship()
```

Back-populates where appropriate.

Example

```
Student

↓

Attendance

↓

Student
```

Bidirectional relationships only where useful.

---

# Constraints

Use database constraints for

```
Unique Email

Unique Roll Number

Required Fields

Foreign Keys
```

Avoid relying solely on frontend validation.

---

# Indexes

Create indexes for

```
email

roll_number

student_id

subject_id

date
```

Optimize frequent queries.

---

# Default Values

Allowed

```
created_at

updated_at

is_active
```

Avoid calculated defaults.

---

# Timestamps

Every major model should include

```
created_at

updated_at
```

Managed automatically.

---

# Soft Delete

Not required for MVP.

Future support

```
deleted_at

is_deleted
```

---

# Business Logic

Never implement

```
calculate_attendance()

calculate_grade()

calculate_performance()

is_scholarship_eligible()
```

inside models.

Business logic belongs in

```
services/
```

---

# Validation

Models should rely on

Database constraints.

Input validation belongs to

```
schemas/
```

---

# Serialization

Models should not serialize themselves.

Use

```
Pydantic Schemas
```

instead.

---

# Security

Never expose

```
password_hash
```

through API responses.

Sensitive fields should remain internal.

---

# Logging

Models should not perform logging.

Logging belongs to

```
services

or

middleware
```

---

# Performance

Avoid eager loading unless required.

Use relationship loading strategies appropriately.

Prevent unnecessary joins.

---

# Import Rules

Allowed

```
models

↓

database
```

Not Allowed

```
models

↓

routers
```

Not Allowed

```
models

↓

frontend
```

Not Allowed

```
models

↓

services
```

---

# Future Compatibility

Model architecture should support

```
Audit Logs

Departments

Timetable

Calendar

Notifications

AI Insights

Multi-Campus

Multi-Tenant
```

without restructuring existing models.

---

# Testing

Verify

✓ Table Creation

✓ Relationships

✓ Constraints

✓ Indexes

✓ Foreign Keys

✓ Default Values

✓ Cascade Rules

---

# Model Checklist

Every model should

✓ Represent one table.

✓ Define relationships.

✓ Avoid business logic.

✓ Include timestamps.

✓ Follow naming conventions.

✓ Be independently testable.

---

# Definition of Completion

Model File Responsibilities are complete when

✓ Every entity has its own model.

✓ Relationships are defined.

✓ Constraints enforced.

✓ Business logic excluded.

✓ Naming conventions followed.

---

# Summary

The Model File Responsibilities specification establishes a clean ORM layer for EduTrack Pro by ensuring each SQLAlchemy model represents only database structure and relationships.

By separating persistence from business logic and validation, the application maintains a scalable, maintainable, and production-ready architecture that aligns with modern backend engineering practices.

End of Model File Responsibilities Specification.