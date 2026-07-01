# 18_DATABASE_MARKS.md

# EduTrack Pro — Marks Database Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Marks

---

# Purpose

The Marks table stores every academic assessment recorded for students throughout their academic journey.

Marks represent the primary indicator of academic performance and serve as one of the most important datasets within EduTrack Pro.

Marks power

- Academic Performance
- Subject Performance
- Student Dashboard
- Teacher Dashboard
- Analytics
- Grade Calculation
- Scholarship Eligibility
- Performance Prediction
- Academic Reports

The Marks table should remain accurate, consistent, and immutable except through authorized updates.

---

# Responsibilities

The Marks table is responsible for

- Student Marks
- Subject Marks
- Internal Assessments
- Examination Scores
- Academic Performance Data

The Marks table is NOT responsible for

- Authentication
- Student Information
- Subject Information
- Grade Calculation Logic
- Dashboard Rendering
- Analytics Processing

All calculations should occur within the Service Layer.

---

# Entity Overview

```
Student

↓

Marks

↓

Performance Analytics

↓

Dashboard

↓

Prediction

↓

Reports

↓

Scholarship Eligibility
```

---

# Database Table

```
marks
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

Unique identifier for every marks record.

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

Identifies the student.

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

Identifies the subject.

---

## assessment_type

Type

Enum

Required

Yes

Allowed Values

```
Assignment

Quiz

Internal

Mid Semester

Practical

End Semester
```

Purpose

Defines the academic assessment category.

---

## marks_obtained

Type

Float

Required

Yes

Purpose

Marks earned by the student.

Validation

- Greater than or equal to 0
- Less than or equal to maximum_marks

---

## maximum_marks

Type

Float

Required

Yes

Purpose

Maximum possible score.

Validation

- Positive number
- Greater than zero

---

## examination_date

Type

Date

Required

Yes

Purpose

Date of examination or assessment.

Validation

- Cannot be a future date

---

## remarks

Type

Text

Optional

Purpose

Teacher comments regarding performance.

---

## entered_by

Type

Integer

Required

Yes

Foreign Key

```
users.id
```

Purpose

Stores the teacher who entered the marks.

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

Marks belongs to

```
Student

Subject

Teacher(User)
```

Relationship Diagram

```
Student

↓

Marks

↑

Subject

↑

Teacher(User)
```

---

# Foreign Keys

```
student_id

↓

students.id
```

```
subject_id

↓

subjects.id
```

```
entered_by

↓

users.id
```

Every Marks record must reference valid Student, Subject, and Teacher records.

---

# Constraints

Required

- student_id
- subject_id
- assessment_type
- marks_obtained
- maximum_marks
- examination_date
- entered_by

---

# Unique Constraint

One marks entry per

```
Student

+

Subject

+

Assessment Type

+

Examination Date
```

Duplicate entries for the same assessment should not be permitted.

---

# Indexes

Create indexes for

- student_id
- subject_id
- assessment_type
- examination_date
- entered_by

These fields are frequently queried.

---

# SQLAlchemy Relationships

Marks

↓

Student

Marks

↓

Subject

Marks

↓

Teacher(User)

Relationships should support efficient querying in both directions.

---

# CRUD Responsibilities

Create Marks

↓

Validate Student

↓

Validate Subject

↓

Validate Teacher

↓

Validate Score

↓

Check Duplicate

↓

Store Record

---

Read Marks

Support

- Student Marks
- Subject Marks
- Assessment History
- Semester Marks
- Academic Summary

---

Update Marks

Allow updating

- Marks Obtained
- Maximum Marks
- Remarks

Update timestamp automatically.

---

Delete Marks

Deletion should require authorization.

Maintain academic consistency.

---

# Validation Rules

Marks Obtained

- Required
- Numeric
- Greater than or equal to zero
- Cannot exceed maximum marks

Maximum Marks

- Required
- Positive number

Assessment Type

Allowed Values

```
Assignment

Quiz

Internal

Mid Semester

Practical

End Semester
```

Examination Date

- Required
- Cannot be future date

Student

Must exist.

Subject

Must exist.

Teacher

Must exist.

Duplicate assessments must be rejected.

---

# Academic Performance Rules

Average marks

Grade

CGPA (future)

Performance prediction

Subject performance

Semester performance

must all be calculated inside

```
marks_service.py
```

The Marks table stores raw data only.

---

# Grade Calculation Rules

Grades are derived from percentages.

Example default grading policy

```
90–100  → A+

80–89   → A

70–79   → B+

60–69   → B

50–59   → C

40–49   → D

Below 40 → F
```

These rules should remain configurable inside the Service Layer.

The database should never store calculated grades unless explicitly required in future versions.

---

# Average Calculation

Formula

```
Average

=

Total Marks Obtained

/

Total Maximum Marks

×

100
```

Calculation belongs exclusively inside the Marks Service.

---

# Search Requirements

Support searching by

- Student
- Subject
- Assessment Type
- Examination Date

---

# Filtering Requirements

Allow filtering by

- Student
- Subject
- Semester
- Assessment Type
- Date Range

Filters should be combinable.

---

# Sorting Requirements

Support sorting by

- Examination Date
- Marks
- Student
- Subject

Ascending and descending.

---

# API Operations

Required endpoints

```
GET /marks

GET /marks/{id}

POST /marks

PUT /marks/{id}

DELETE /marks/{id}

GET /marks/student/{student_id}

GET /marks/subject/{subject_id}

GET /marks/summary

GET /marks/average
```

---

# Expected Schemas

Create

```
MarksCreate
```

Update

```
MarksUpdate
```

Response

```
MarksResponse
```

Summary

```
MarksSummaryResponse
```

Average

```
MarksAverageResponse
```

---

# Expected Service

```
marks_service.py
```

Responsibilities

- Create Marks
- Update Marks
- Delete Marks
- Student Marks
- Subject Marks
- Academic Average
- Grade Calculation
- Performance Summary
- Duplicate Validation

---

# Expected Router

```
marks.py
```

Responsibilities

Expose REST endpoints for marks operations.

Teachers may

- Create
- Update
- Delete

Students may

- View only their own marks.

---

# Business Rules

Marks may only be entered by Teachers.

Students cannot modify academic records.

Performance calculations depend on Marks.

Dashboard statistics depend on Marks.

Reports depend on Marks.

Scholarship eligibility depends on Marks.

Performance prediction depends on Marks.

Business calculations must never be duplicated outside the Marks Service.

---

# Expected Tests

Test

- Marks creation
- Duplicate assessment prevention
- Update marks
- Delete marks
- Average calculation
- Grade calculation
- Student history
- Subject history
- Validation
- Authentication
- Authorization

Every endpoint should have corresponding tests.

---

# Future Compatibility

The schema should support future additions

- Grade Moderation
- Relative Grading
- Weighted Assessments
- GPA
- CGPA
- Grade History
- Re-evaluation
- Result Publication
- Bulk Marks Upload

These additions should integrate without redesigning the current schema.

---

# Definition of Completion

The Marks module is complete when

✓ Marks model exists.

✓ Relationships function.

✓ CRUD operations work.

✓ Duplicate assessments prevented.

✓ Average calculation works.

✓ Grade calculation works.

✓ Filtering works.

✓ Validation works.

✓ Authentication enforced.

✓ Authorization enforced.

✓ Swagger documentation complete.

✓ Tests pass.

---

# Summary

The Marks table stores every academic assessment completed by students and serves as one of the primary data sources of EduTrack Pro.

Dashboards, Analytics, Scholarship Eligibility, Performance Prediction, and Academic Reports all depend on accurate Marks records.

The implementation should prioritize integrity, efficient querying, centralized calculations, and long-term maintainability.

End of Marks Database Specification.