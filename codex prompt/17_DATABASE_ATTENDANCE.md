# 17_DATABASE_ATTENDANCE.md

# EduTrack Pro — Attendance Database Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Attendance

---

# Purpose

The Attendance table records the attendance status of every student for every subject on every academic day.

Attendance forms one of the most important datasets in EduTrack Pro.

It powers

- Attendance History
- Attendance Percentage
- Dashboard Statistics
- At-Risk Detection
- Performance Analytics
- Scholarship Eligibility
- Student Reports

Attendance records are permanent academic records and therefore require strict validation.

---

# Responsibilities

The Attendance table is responsible for

- Daily Attendance
- Student Attendance History
- Subject Attendance
- Attendance Statistics
- Attendance Percentage Calculations (through services)
- Attendance Reporting

The Attendance table is NOT responsible for

- Authentication
- Student Information
- Subject Information
- Marks
- Assignments
- Analytics Calculations
- Dashboard Rendering

---

# Entity Overview

```
Student

↓

Attendance

↓

Attendance Analytics

↓

Dashboard

↓

Reports

↓

Scholarship

↓

Risk Detection
```

Attendance is one of the primary data sources of EduTrack Pro.

---

# Database Table

```
attendance
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

Unique attendance record identifier.

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

Identifies the student whose attendance is being recorded.

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

## attendance_date

Type

Date

Required

Yes

Purpose

Date on which attendance is recorded.

Validation

- Required
- Cannot be future date

---

## status

Type

Enum

Required

Yes

Values

```
Present

Absent

Late
```

Purpose

Attendance status.

---

## remarks

Type

Text

Optional

Purpose

Teacher remarks for unusual attendance situations.

---

## marked_by

Type

Integer

Required

Yes

Foreign Key

```
users.id
```

Purpose

Stores which teacher marked attendance.

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

Attendance belongs to

```
Student

Subject

Teacher(User)
```

Relationship Diagram

```
Student

↓

Attendance

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
marked_by

↓

users.id
```

Every attendance record must reference valid Student, Subject, and Teacher records.

---

# Constraints

Required

- student_id
- subject_id
- attendance_date
- status
- marked_by

---

# Unique Constraint

One attendance record per

```
Student

+

Subject

+

Attendance Date
```

Duplicate attendance records for the same student, subject, and date must never be allowed.

---

# Indexes

Create indexes for

- student_id
- subject_id
- attendance_date
- status
- marked_by

These fields are frequently queried.

---

# SQLAlchemy Relationships

Attendance

↓

Student

Attendance

↓

Subject

Attendance

↓

Teacher(User)

Relationships should support efficient querying from both directions.

---

# CRUD Responsibilities

Create Attendance

↓

Validate Student

↓

Validate Subject

↓

Validate Teacher

↓

Check Duplicate Record

↓

Store Attendance

---

Read Attendance

Support

- By Student
- By Subject
- By Date
- By Semester
- Attendance History
- Attendance Summary

---

Update Attendance

Allow

- Status
- Remarks

Every modification should update

```
updated_at
```

---

Delete Attendance

Delete only according to authorization rules.

Deletion should preserve academic integrity.

---

# Validation Rules

Attendance Date

- Required
- Valid date
- Cannot be future date

Status

Allowed values

```
Present

Absent

Late
```

Student

Must exist.

Subject

Must exist.

Teacher

Must exist.

Duplicate Record

Must be rejected.

---

# Attendance Business Rules

Attendance may only be marked by Teachers.

Students cannot create attendance records.

Attendance should only be recorded once per student per subject per day.

Attendance history must remain immutable except through authorized updates.

---

# Attendance Percentage Rules

Attendance percentage is calculated in

```
attendance_service.py
```

Formula

```
Attendance %

=

(Number of Present Classes)

/

(Total Classes Conducted)

×

100
```

Late attendance may be treated according to institutional policy.

Business rules should remain centralized.

---

# Attendance Summary Requirements

The service layer should support

- Daily Summary
- Weekly Summary
- Monthly Summary
- Semester Summary
- Subject Summary
- Student Summary

These summaries should be generated dynamically.

---

# Search Requirements

Support searching by

- Student
- Subject
- Date
- Teacher

---

# Filtering Requirements

Allow filtering by

- Student
- Subject
- Semester
- Date Range
- Attendance Status

Filters should be combinable.

---

# Sorting Requirements

Support sorting by

- Date
- Student
- Subject
- Status

Ascending and descending.

---

# API Operations

Required endpoints

```
GET /attendance

GET /attendance/{id}

POST /attendance

PUT /attendance/{id}

DELETE /attendance/{id}

GET /attendance/student/{student_id}

GET /attendance/subject/{subject_id}

GET /attendance/summary

GET /attendance/percentage
```

---

# Expected Schemas

Create

```
AttendanceCreate
```

Update

```
AttendanceUpdate
```

Response

```
AttendanceResponse
```

Summary

```
AttendanceSummaryResponse
```

Percentage

```
AttendancePercentageResponse
```

---

# Expected Service

```
attendance_service.py
```

Responsibilities

- Mark Attendance
- Update Attendance
- Delete Attendance
- Attendance History
- Attendance Percentage
- Attendance Summary
- Duplicate Validation
- Attendance Statistics

---

# Expected Router

```
attendance.py
```

Responsibilities

Expose REST endpoints for attendance operations.

Teachers may

- Create
- Update
- Delete

Students may

- View their own attendance.

---

# Business Rules

Attendance records are permanent academic records.

Attendance percentages must always reflect current data.

Dashboard statistics must use attendance data.

Scholarship eligibility depends on attendance.

Risk detection depends on attendance.

Reports consume attendance history.

Attendance calculations should never be duplicated outside the Attendance Service.

---

# Expected Tests

Test

- Attendance creation
- Duplicate attendance prevention
- Attendance update
- Attendance deletion
- Attendance percentage
- Student history
- Subject history
- Date validation
- Authentication
- Authorization

Every endpoint should have corresponding tests.

---

# Future Compatibility

The schema should support future additions

- Biometric Attendance
- QR Attendance
- RFID Attendance
- Excused Leave
- Medical Leave
- Holiday Calendar
- Attendance Import
- Bulk Attendance Upload

These additions should integrate without redesigning the current schema.

---

# Definition of Completion

The Attendance module is complete when

✓ Attendance model exists.

✓ Relationships function.

✓ CRUD operations work.

✓ Duplicate attendance prevented.

✓ Attendance percentage works.

✓ Attendance history works.

✓ Filtering works.

✓ Validation works.

✓ Authentication enforced.

✓ Authorization enforced.

✓ Swagger documentation complete.

✓ Tests pass.

---

# Summary

The Attendance table records every student's academic attendance and serves as one of the primary data sources for EduTrack Pro.

Dashboards, Analytics, Scholarship Eligibility, Risk Detection, and Reports all depend on accurate attendance data.

The implementation should prioritize integrity, efficient querying, reliable calculations, and long-term maintainability.

End of Attendance Database Specification.