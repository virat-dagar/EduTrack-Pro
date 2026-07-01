# 19_DATABASE_ASSIGNMENTS.md

# EduTrack Pro — Assignments Database Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Assignments

---

# Purpose

The Assignments table stores every academic assignment created by teachers.

Assignments help students track coursework while allowing teachers to manage deadlines, monitor progress, and evaluate academic engagement.

Assignments contribute to

- Student Dashboard
- Teacher Dashboard
- Assignment Tracking
- Academic Progress
- Performance Analytics
- Reports

Assignments are academic entities and therefore require proper validation and authorization.

---

# Responsibilities

The Assignments table is responsible for

- Assignment Information
- Assignment Deadlines
- Subject Association
- Assignment Instructions
- Assignment Availability

The Assignments table is NOT responsible for

- Student Submission Files
- Marks
- Authentication
- Dashboard Rendering
- Analytics Calculations

Submission tracking belongs to the Submissions module.

---

# Entity Overview

```
Teacher

↓

Assignment

↓

Student

↓

Submission

↓

Dashboard

↓

Reports

↓

Analytics
```

---

# Database Table

```
assignments
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

Unique assignment identifier.

---

## subject_id

Type

Integer

Required

Yes

Foreign Key

```
subjects.id
```

Purpose

Associates the assignment with a subject.

---

## title

Type

String

Required

Yes

Maximum Length

150

Purpose

Assignment title.

Validation

- Required
- Trim whitespace
- Maximum length 150

---

## description

Type

Text

Required

Yes

Purpose

Detailed assignment instructions.

---

## total_marks

Type

Float

Required

Yes

Purpose

Maximum marks obtainable.

Validation

- Positive number

---

## assigned_date

Type

Date

Required

Yes

Purpose

Assignment release date.

---

## due_date

Type

Date

Required

Yes

Purpose

Submission deadline.

Validation

- Must be greater than or equal to assigned_date

---

## created_by

Type

Integer

Required

Yes

Foreign Key

```
users.id
```

Purpose

Teacher who created the assignment.

---

## is_active

Type

Boolean

Default

True

Purpose

Controls assignment visibility.

Inactive assignments remain in historical records.

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

Assignment belongs to

```
Subject

Teacher(User)
```

Assignment has

```
Many Submissions
```

Relationship Diagram

```
Teacher(User)

↓

Assignment

↑

Subject

↓

Submission
```

---

# Foreign Keys

```
subject_id

↓

subjects.id
```

```
created_by

↓

users.id
```

Every assignment must reference an existing Subject and Teacher.

---

# Constraints

Required

- subject_id
- title
- description
- total_marks
- assigned_date
- due_date
- created_by

---

# Indexes

Create indexes for

- subject_id
- due_date
- assigned_date
- created_by
- is_active

These columns are frequently queried.

---

# SQLAlchemy Relationships

Assignment

↓

Subject

Assignment

↓

Teacher(User)

Assignment

↓

Submissions

Relationships should be bidirectional wherever appropriate.

---

# CRUD Responsibilities

Create Assignment

↓

Validate Teacher

↓

Validate Subject

↓

Validate Dates

↓

Store Assignment

---

Read Assignment

Support

- By ID
- By Subject
- By Teacher
- Active Assignments
- Assignment History

---

Update Assignment

Allow updating

- Title
- Description
- Total Marks
- Due Date
- Active Status

Modification updates

```
updated_at
```

---

Delete Assignment

Deletion requires authorization.

Prevent deletion when business rules prohibit it.

Maintain database integrity.

---

# Validation Rules

Title

- Required
- Maximum length 150

Description

- Required

Total Marks

- Positive number

Assigned Date

- Required

Due Date

- Required
- Must not precede assigned date

Teacher

Must exist.

Subject

Must exist.

---

# Assignment Lifecycle

Teacher creates assignment

↓

Assignment becomes active

↓

Students view assignment

↓

Students submit work

↓

Deadline reached

↓

Teacher reviews submissions

↓

Assignment archived

---

# Search Requirements

Support searching by

- Title
- Subject
- Teacher

Search should be case insensitive.

---

# Filtering Requirements

Allow filtering by

- Subject
- Teacher
- Active Status
- Due Date
- Date Range

Filters should be combinable.

---

# Sorting Requirements

Support sorting by

- Due Date
- Assigned Date
- Title
- Subject

Ascending and descending.

---

# API Operations

Required endpoints

```
GET /assignments

GET /assignments/{id}

POST /assignments

PUT /assignments/{id}

DELETE /assignments/{id}

GET /assignments/subject/{subject_id}

GET /assignments/teacher/{teacher_id}

GET /assignments/active

GET /assignments/upcoming
```

---

# Expected Schemas

Create

```
AssignmentCreate
```

Update

```
AssignmentUpdate
```

Response

```
AssignmentResponse
```

List

```
AssignmentListResponse
```

---

# Expected Service

```
assignment_service.py
```

Responsibilities

- Create Assignment
- Update Assignment
- Delete Assignment
- Assignment Listing
- Active Assignments
- Upcoming Deadlines
- Assignment Validation

---

# Expected Router

```
assignments.py
```

Responsibilities

Expose REST endpoints.

Teachers may

- Create
- Update
- Delete

Students may

- View available assignments.

---

# Business Rules

Only Teachers may create assignments.

Every Assignment belongs to one Subject.

Students cannot modify assignments.

Inactive assignments should remain available for historical reports.

Dashboard statistics should include

- Active Assignments
- Upcoming Deadlines
- Overdue Assignments

Assignment completion tracking is handled by the Submission module.

---

# Dashboard Integration

Teacher Dashboard

Display

- Active Assignments
- Upcoming Deadlines
- Submission Counts
- Overdue Assignments

Student Dashboard

Display

- Assigned Work
- Upcoming Deadlines
- Pending Assignments

---

# Reports Integration

Assignments contribute to

- Student Reports
- Teacher Reports
- Assignment Reports
- Semester Reports

---

# Expected Tests

Test

- Assignment creation
- Update assignment
- Delete assignment
- Due date validation
- Subject validation
- Teacher validation
- Active assignment listing
- Upcoming assignment listing
- Authentication
- Authorization

Every endpoint should have corresponding tests.

---

# Future Compatibility

The schema should support future additions

- File Attachments
- Multiple Attachments
- Rubrics
- Assignment Categories
- Peer Review
- Group Assignments
- Scheduled Publishing
- Assignment Templates
- Automatic Deadline Reminders

These additions should integrate without redesigning the current schema.

---

# Definition of Completion

The Assignment module is complete when

✓ Assignment model exists.

✓ Relationships function.

✓ CRUD operations work.

✓ Active assignment listing works.

✓ Upcoming deadlines work.

✓ Validation works.

✓ Authentication enforced.

✓ Authorization enforced.

✓ Swagger documentation complete.

✓ Tests pass.

---

# Summary

The Assignments table manages coursework across EduTrack Pro.

It connects Teachers, Subjects, and Students while supporting dashboards, reports, and future academic workflows.

The implementation should prioritize maintainability, validation, authorization, and seamless integration with the Submission module.

End of Assignments Database Specification.