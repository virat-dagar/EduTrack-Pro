# 20_DATABASE_SUBMISSIONS.md

# EduTrack Pro — Submissions Database Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Submissions

---

# Purpose

The Submissions table records the submission status of every assignment assigned to students.

A submission represents a student's response to an assignment and forms the bridge between Assignment Management and Academic Evaluation.

The Submission module powers

- Assignment Tracking
- Pending Assignments
- Completed Assignments
- Student Dashboard
- Teacher Dashboard
- Submission Analytics
- Academic Reports

Submissions represent workflow data rather than academic scores.

Marks awarded for submissions should be stored in the Marks module if formal evaluation is required.

---

# Responsibilities

The Submissions table is responsible for

- Assignment Submission Status
- Submission Date
- Submission Tracking
- Student Progress
- Submission Metadata

The Submissions table is NOT responsible for

- Assignment Creation
- Marks
- Authentication
- Analytics Calculations
- Dashboard Rendering

---

# Entity Overview

```
Student

↓

Assignment

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
submissions
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

Unique submission identifier.

---

## assignment_id

Type

Integer

Required

Yes

Foreign Key

```
assignments.id
```

Purpose

References the assignment being submitted.

---

## student_id

Type

Integer

Required

Yes

Foreign Key

```
students.id
```

Purpose

Identifies the student making the submission.

---

## submission_date

Type

Datetime

Required

Yes

Default

Current Timestamp

Purpose

Stores the exact submission time.

---

## status

Type

Enum

Required

Yes

Allowed Values

```
Pending

Submitted

Late

Reviewed
```

Purpose

Tracks submission progress.

---

## submission_notes

Type

Text

Optional

Purpose

Additional comments submitted by the student.

---

## attachment_path

Type

String

Optional

Purpose

Stores uploaded file path or URL.

MVP may support filename storage only.

Future versions may integrate cloud storage.

---

## reviewed_by

Type

Integer

Optional

Foreign Key

```
users.id
```

Purpose

Teacher who reviewed the submission.

Null until reviewed.

---

## reviewed_at

Type

Datetime

Optional

Purpose

Timestamp when review was completed.

---

## feedback

Type

Text

Optional

Purpose

Teacher feedback after review.

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

Submission belongs to

```
Assignment

Student

Teacher(User)
```

Relationship Diagram

```
Assignment

↓

Submission

↑

Student

↑

Teacher(User)
```

---

# Foreign Keys

```
assignment_id

↓

assignments.id
```

```
student_id

↓

students.id
```

```
reviewed_by

↓

users.id
```

Every Submission must reference a valid Assignment and Student.

Reviewer must be a valid Teacher.

---

# Constraints

Required

- assignment_id
- student_id
- submission_date
- status

Optional

- feedback
- attachment_path
- reviewed_by
- reviewed_at

---

# Unique Constraint

One submission per

```
Student

+

Assignment
```

A student cannot submit the same assignment multiple times unless future versioning support is introduced.

---

# Indexes

Create indexes for

- assignment_id
- student_id
- status
- submission_date
- reviewed_by

These fields are queried frequently.

---

# SQLAlchemy Relationships

Submission

↓

Assignment

Submission

↓

Student

Submission

↓

Teacher(User)

Relationships should support efficient navigation from both directions.

---

# CRUD Responsibilities

Create Submission

↓

Validate Student

↓

Validate Assignment

↓

Check Duplicate Submission

↓

Store Submission

---

Read Submission

Support

- By Student
- By Assignment
- Pending Submissions
- Reviewed Submissions
- Submission History

---

Update Submission

Allow updating

- Status
- Notes
- Attachment
- Feedback
- Reviewer

Automatically update

```
updated_at
```

---

Delete Submission

Deletion requires authorization.

Historical integrity should be maintained.

---

# Validation Rules

Assignment

Must exist.

Student

Must exist.

Submission Date

Cannot be null.

Status

Allowed values

```
Pending

Submitted

Late

Reviewed
```

Duplicate Submission

Must be rejected.

Attachment

Optional.

Validate filename/path.

---

# Submission Lifecycle

Teacher creates assignment

↓

Student views assignment

↓

Student submits assignment

↓

Submission stored

↓

Teacher reviews submission

↓

Teacher provides feedback

↓

Submission marked reviewed

↓

Dashboard updated

---

# Late Submission Rules

If

```
submission_date

>

assignment.due_date
```

Status should automatically become

```
Late
```

unless overridden by authorized institutional rules.

Business logic belongs inside

```
submission_service.py
```

---

# Search Requirements

Support searching by

- Student
- Assignment
- Status

---

# Filtering Requirements

Allow filtering by

- Student
- Assignment
- Status
- Date Range
- Reviewed
- Pending

Filters should be combinable.

---

# Sorting Requirements

Support sorting by

- Submission Date
- Assignment
- Student
- Status

Ascending and descending.

---

# API Operations

Required endpoints

```
GET /submissions

GET /submissions/{id}

POST /submissions

PUT /submissions/{id}

DELETE /submissions/{id}

GET /submissions/student/{student_id}

GET /submissions/assignment/{assignment_id}

GET /submissions/pending

GET /submissions/reviewed
```

---

# Expected Schemas

Create

```
SubmissionCreate
```

Update

```
SubmissionUpdate
```

Response

```
SubmissionResponse
```

List

```
SubmissionListResponse
```

Review

```
SubmissionReviewResponse
```

---

# Expected Service

```
submission_service.py
```

Responsibilities

- Create Submission
- Update Submission
- Delete Submission
- Review Submission
- Pending Submissions
- Late Submission Detection
- Submission History
- Duplicate Validation

---

# Expected Router

```
submissions.py
```

Responsibilities

Expose REST endpoints.

Students may

- Submit assignments
- View their own submissions

Teachers may

- View all submissions
- Review submissions
- Update review status
- Provide feedback

---

# Business Rules

Every Assignment may have many Submissions.

Every Student may submit an Assignment only once.

Only Teachers may review submissions.

Students cannot modify reviewed submissions unless future resubmission functionality is implemented.

Late submissions should be detected automatically.

Dashboard statistics should include

- Pending Reviews
- Total Submissions
- Late Submissions
- Reviewed Submissions

---

# Dashboard Integration

Teacher Dashboard

Display

- Pending Reviews
- Recent Submissions
- Late Submissions
- Submission Statistics

Student Dashboard

Display

- Submitted Assignments
- Pending Assignments
- Late Submissions
- Teacher Feedback

---

# Reports Integration

Submissions contribute to

- Assignment Reports
- Student Reports
- Semester Reports
- Teacher Activity Reports

---

# Expected Tests

Test

- Submission creation
- Duplicate submission prevention
- Late submission detection
- Review workflow
- Feedback update
- Delete submission
- Validation
- Authentication
- Authorization

Every endpoint should have corresponding tests.

---

# Future Compatibility

The schema should support future additions

- Multiple File Uploads
- Cloud Storage Integration
- Versioned Resubmissions
- Plagiarism Detection
- Automatic Grading
- Rubric Evaluation
- Peer Assessment
- Submission History
- Offline Upload Synchronization

These additions should integrate without redesigning the existing schema.

---

# Definition of Completion

The Submission module is complete when

✓ Submission model exists.

✓ Relationships function.

✓ CRUD operations work.

✓ Duplicate submissions prevented.

✓ Review workflow works.

✓ Late submission detection works.

✓ Filtering works.

✓ Validation works.

✓ Authentication enforced.

✓ Authorization enforced.

✓ Swagger documentation complete.

✓ Tests pass.

---

# Summary

The Submissions table completes the academic workflow by connecting Students with Assignments and enabling structured submission tracking.

It provides the foundation for assignment management, teacher review workflows, dashboards, analytics, and reports while maintaining clean separation from academic grading logic.

End of Submissions Database Specification.