# 21_DATABASE_RELATIONSHIPS.md

# EduTrack Pro — Database Relationships Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Database Relationships

---

# Purpose

This document defines every relationship that exists between database entities in EduTrack Pro.

While previous database documents defined individual tables, this document defines how those tables interact.

The objective is to ensure data integrity, proper SQLAlchemy relationship configuration, and consistent navigation between entities.

Every relationship described here should be implemented using SQLAlchemy's `relationship()` and appropriate `ForeignKey` constraints.

---

# Relationship Philosophy

The database should model real-world academic relationships.

Relationships should be

- Explicit
- Bidirectional where useful
- Referentially consistent
- Easy to query
- Easy to maintain

Avoid duplicate information.

Store relationships through foreign keys rather than repeated data.

---

# Complete Entity Diagram

```text
                Users
                  │
        ┌─────────┴─────────┐
        │                   │
     Teacher            Student User
                            │
                            ▼
                        Students
                     ┌─────┼─────┐
                     │     │     │
                     ▼     ▼     ▼
               Attendance Marks Submissions
                     ▲       ▲        ▲
                     │       │        │
                 Subjects────┘        │
                     │                │
                     ▼                │
                Assignments───────────┘
```

---

# Relationship Summary

| Parent | Child | Relationship |
|---------|-------|--------------|
| User | Student | One-to-One |
| Student | Attendance | One-to-Many |
| Student | Marks | One-to-Many |
| Student | Submissions | One-to-Many |
| Subject | Attendance | One-to-Many |
| Subject | Marks | One-to-Many |
| Subject | Assignments | One-to-Many |
| Assignment | Submissions | One-to-Many |
| User (Teacher) | Attendance | One-to-Many |
| User (Teacher) | Marks | One-to-Many |
| User (Teacher) | Assignments | One-to-Many |
| User (Teacher) | Submission Reviews | One-to-Many |

---

# User ↔ Student

Relationship

```
One User

↓

One Student
```

Purpose

Every student account has one authentication record.

Teacher accounts do not require Student records.

Implementation

```
User.id

↓

Student.user_id
```

SQLAlchemy

User

```
student = relationship(
    "Student",
    back_populates="user",
    uselist=False
)
```

Student

```
user = relationship(
    "User",
    back_populates="student"
)
```

---

# Student ↔ Attendance

Relationship

```
One Student

↓

Many Attendance Records
```

Implementation

```
Student.id

↓

Attendance.student_id
```

SQLAlchemy

Student

```
attendance_records = relationship(
    "Attendance",
    back_populates="student"
)
```

Attendance

```
student = relationship(
    "Student",
    back_populates="attendance_records"
)
```

---

# Student ↔ Marks

Relationship

```
One Student

↓

Many Marks Records
```

Implementation

```
Student.id

↓

Marks.student_id
```

Purpose

Store all academic evaluations for one student.

---

# Student ↔ Submissions

Relationship

```
One Student

↓

Many Submissions
```

Implementation

```
Student.id

↓

Submission.student_id
```

Purpose

Track assignment submissions.

---

# Subject ↔ Attendance

Relationship

```
One Subject

↓

Many Attendance Records
```

Implementation

```
Subject.id

↓

Attendance.subject_id
```

Purpose

Attendance is recorded per subject.

---

# Subject ↔ Marks

Relationship

```
One Subject

↓

Many Marks
```

Implementation

```
Subject.id

↓

Marks.subject_id
```

Purpose

Marks belong to academic subjects.

---

# Subject ↔ Assignments

Relationship

```
One Subject

↓

Many Assignments
```

Implementation

```
Subject.id

↓

Assignment.subject_id
```

Purpose

Assignments are always created for a specific subject.

---

# Assignment ↔ Submission

Relationship

```
One Assignment

↓

Many Student Submissions
```

Implementation

```
Assignment.id

↓

Submission.assignment_id
```

Purpose

Multiple students submit one assignment.

---

# Teacher ↔ Attendance

Relationship

```
One Teacher

↓

Many Attendance Records
```

Implementation

```
User.id

↓

Attendance.marked_by
```

Purpose

Track which teacher marked attendance.

---

# Teacher ↔ Marks

Relationship

```
One Teacher

↓

Many Marks Records
```

Implementation

```
User.id

↓

Marks.entered_by
```

Purpose

Maintain audit history.

---

# Teacher ↔ Assignments

Relationship

```
One Teacher

↓

Many Assignments
```

Implementation

```
User.id

↓

Assignment.created_by
```

Purpose

Track assignment ownership.

---

# Teacher ↔ Submission Reviews

Relationship

```
One Teacher

↓

Many Reviewed Submissions
```

Implementation

```
User.id

↓

Submission.reviewed_by
```

Purpose

Track review ownership.

---

# Cardinality Summary

| Relationship | Cardinality |
|--------------|-------------|
| User → Student | 1 : 1 |
| Student → Attendance | 1 : N |
| Student → Marks | 1 : N |
| Student → Submission | 1 : N |
| Subject → Attendance | 1 : N |
| Subject → Marks | 1 : N |
| Subject → Assignment | 1 : N |
| Assignment → Submission | 1 : N |
| Teacher → Attendance | 1 : N |
| Teacher → Marks | 1 : N |
| Teacher → Assignment | 1 : N |
| Teacher → Review | 1 : N |

---

# Cascade Rules

Relationships should avoid accidental data loss.

Recommended behavior

User

↓

Student

Cascade only when explicitly deleting the user.

Student

↓

Attendance

Cascade delete.

Student

↓

Marks

Cascade delete.

Student

↓

Submission

Cascade delete.

Subject

↓

Attendance

Restrict deletion if attendance exists.

Subject

↓

Marks

Restrict deletion.

Subject

↓

Assignments

Restrict deletion.

Assignment

↓

Submission

Cascade delete.

These rules preserve historical academic integrity.

---

# Lazy Loading Strategy

Use SQLAlchemy relationship loading appropriately.

Default

```
selectin
```

Use joined loading only where it significantly improves performance.

Avoid unnecessary eager loading.

---

# Bidirectional Relationships

Whenever beneficial, configure

```
back_populates
```

instead of duplicated relationship definitions.

Benefits

- Easier navigation
- Cleaner ORM
- Simpler queries

---

# Referential Integrity

Every foreign key must reference an existing record.

Invalid references must never be inserted.

Validation occurs at

- Pydantic
- Service Layer
- Database

---

# Orphan Prevention

The system should never allow orphan records.

Examples

Attendance without Student

Marks without Subject

Submission without Assignment

These situations should always be rejected.

---

# Relationship Validation

Before inserting related records

Verify

✓ Parent exists

✓ Parent active (where required)

✓ Foreign key valid

Reject invalid references before database insertion.

---

# Query Examples

Typical relationship queries

Student

↓

Attendance History

Student

↓

Marks

Subject

↓

Assignments

Assignment

↓

Submissions

Teacher

↓

Created Assignments

Teacher

↓

Marked Attendance

The ORM should make these queries straightforward.

---

# Performance Considerations

Relationships should support

- Efficient joins
- Aggregations
- Dashboard queries
- Analytics calculations

Avoid N+1 query problems.

Prefer relationship loading strategies where appropriate.

---

# Future Relationships

The schema should accommodate future entities such as

- Departments
- Courses
- Semesters
- Parent Accounts
- Faculty Profiles
- Timetables
- Notifications

without redesigning existing relationships.

---

# Definition of Completion

Database relationships are complete when

✓ Every foreign key exists.

✓ Every relationship is configured.

✓ Bidirectional navigation works.

✓ Referential integrity enforced.

✓ Cascade rules implemented.

✓ No orphan records possible.

✓ Queries execute efficiently.

✓ Relationships support analytics and dashboards.

---

# Summary

Database relationships form the backbone of EduTrack Pro.

Correct relationship design ensures data integrity, efficient querying, reliable analytics, and maintainable business logic.

Every module in the application depends on these relationships functioning correctly.

End of Database Relationships Specification.