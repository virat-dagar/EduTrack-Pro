# 16_DATABASE_SUBJECTS.md

# EduTrack Pro — Subjects Database Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Subject

---

# Purpose

The Subjects table stores all academic subjects offered by the institution.

Subjects form the academic foundation for Attendance, Marks, Assignments, Analytics, Dashboards, and Reports.

Every attendance record, marks entry, and assignment must belong to an existing subject.

Subjects are managed only by Teachers.

Students can only view subjects associated with their course and semester.

---

# Responsibilities

The Subjects table is responsible for

- Subject Information
- Subject Code
- Subject Name
- Course Mapping
- Semester Mapping
- Credit Information
- Academic Organization

The Subjects table is NOT responsible for

- Attendance
- Marks
- Student Information
- Authentication
- Reports
- Analytics

---

# Entity Overview

```
Subject

↓

Attendance

↓

Marks

↓

Assignments

↓

Dashboard

↓

Analytics

↓

Reports
```

---

# Database Table

```
subjects
```

---

# Primary Key

```
id
```

Properties

- Integer
- Primary Key
- Auto Increment
- Indexed
- Not Null

---

# Columns

## id

Type

Integer

Purpose

Unique database identifier.

---

## subject_code

Type

String

Required

Yes

Unique

Yes

Indexed

Yes

Purpose

Official subject identifier.

Examples

```
CS301

CS205

MA101
```

Validation

- Required
- Uppercase
- No duplicates
- Maximum length 20

---

## subject_name

Type

String

Required

Yes

Maximum Length

100

Purpose

Official subject name.

Examples

```
Database Management Systems

Operating Systems

Computer Networks
```

Validation

- Required
- Trim whitespace
- Unique within course and semester where applicable

---

## course

Type

String

Required

Yes

Purpose

Academic course.

Examples

```
B.Tech

BCA

BBA
```

---

## department

Type

String

Required

Yes

Purpose

Academic department.

Examples

```
Computer Science

Information Technology

Mechanical Engineering
```

---

## semester

Type

Integer

Required

Yes

Purpose

Semester in which the subject is taught.

Validation

Positive integer.

---

## credits

Type

Integer

Required

Yes

Purpose

Academic credit value.

Validation

Positive integer.

---

## description

Type

Text

Optional

Purpose

Brief description of the subject.

---

## is_active

Type

Boolean

Default

True

Purpose

Determines whether the subject is currently offered.

Inactive subjects remain in historical records but are hidden from default listings.

---

## created_at

Type

Datetime

Default

Current Timestamp

---

## updated_at

Type

Datetime

Automatically Updated

---

# Relationships

A Subject may have

```
Many Attendance Records

Many Marks Records

Many Assignments
```

Relationship Diagram

```
Subject

├── Attendance

├── Marks

└── Assignments
```

---

# Foreign Key Relationships

Attendance

```
subject_id

↓

subjects.id
```

Marks

```
subject_id

↓

subjects.id
```

Assignments

```
subject_id

↓

subjects.id
```

---

# Constraints

Unique

- subject_code

Required

- subject_code
- subject_name
- course
- department
- semester
- credits

---

# Indexes

Create indexes for

- subject_code
- subject_name
- semester
- department
- course
- is_active

These fields are frequently queried.

---

# SQLAlchemy Relationships

Subject

↓

Attendance

Subject

↓

Marks

Subject

↓

Assignments

Relationships should support efficient querying from both directions.

---

# CRUD Responsibilities

Create Subject

↓

Validate

↓

Check duplicate subject code

↓

Store subject

---

Read Subject

Support

- By ID
- By Subject Code
- By Semester
- By Course
- By Department
- List All

---

Update Subject

Allow updating

- Name
- Credits
- Description
- Active Status

Do not allow duplicate subject codes.

---

Delete Subject

Deletion must verify dependencies.

A subject with existing attendance, marks, or assignments should not be deleted unless explicitly handled according to business rules.

---

# Validation Rules

Subject Code

- Required
- Uppercase
- Unique
- Maximum length 20

Subject Name

- Required
- Maximum length 100

Credits

- Positive integer

Semester

- Positive integer

Course

- Required

Department

- Required

---

# Search Requirements

Support searching by

- Subject Name
- Subject Code
- Course
- Department

Search should be case insensitive.

---

# Filtering Requirements

Allow filtering by

- Course
- Department
- Semester
- Active Status

Filters should be combinable.

---

# Sorting Requirements

Support sorting by

- Subject Name
- Subject Code
- Semester
- Credits

Ascending and descending.

---

# API Operations

Required endpoints

```
GET /subjects

GET /subjects/{id}

POST /subjects

PUT /subjects/{id}

DELETE /subjects/{id}

GET /subjects/search

GET /subjects/filter
```

---

# Expected Schemas

Create

```
SubjectCreate
```

Update

```
SubjectUpdate
```

Response

```
SubjectResponse
```

List

```
SubjectListResponse
```

---

# Expected Service

```
subject_service.py
```

Responsibilities

- Create Subject
- Update Subject
- Delete Subject
- Search Subjects
- Filter Subjects
- Validate Subject Data

---

# Expected Router

```
subjects.py
```

Responsibilities

Expose REST endpoints for Subject operations.

Teachers may

- Create
- Update
- Delete

Students may

- View

---

# Business Rules

Every Attendance record must reference an existing Subject.

Every Marks record must reference an existing Subject.

Every Assignment must reference an existing Subject.

Inactive subjects should remain available for historical reports but should not appear in default active subject lists.

Subject codes must remain unique across the institution.

---

# Expected Tests

Test

- Subject creation
- Duplicate subject code
- Update subject
- Delete subject
- Search
- Filter
- Validation
- Authorization
- Authentication

Every endpoint should have corresponding tests.

---

# Future Compatibility

The schema should support future additions

- Subject Prerequisites
- Subject Outcomes
- Laboratory Flag
- Elective/Core Classification
- Faculty Assignment
- Timetable Integration
- Credit Categories

These additions should integrate without redesigning the existing table.

---

# Definition of Completion

The Subject module is complete when

✓ Subject model exists.

✓ Relationships function.

✓ CRUD operations work.

✓ Search works.

✓ Filtering works.

✓ Validation works.

✓ Duplicate subject codes prevented.

✓ Authentication enforced.

✓ Authorization enforced.

✓ Swagger documentation complete.

✓ Tests pass.

---

# Summary

The Subjects table organizes the academic structure of EduTrack Pro.

Attendance, Marks, Assignments, Dashboards, Analytics, and Reports all depend on valid Subject records.

The implementation should prioritize data integrity, maintainability, efficient querying, and future extensibility.

End of Subjects Database Specification.