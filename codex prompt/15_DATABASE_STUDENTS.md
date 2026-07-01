# 15_DATABASE_STUDENTS.md

# EduTrack Pro — Students Database Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Student

---

# Purpose

The Students table stores the complete academic profile of every student enrolled in the institution.

Unlike the Users table, which manages authentication and authorization, the Students table manages academic identity.

Every student in EduTrack Pro must have exactly one Student record.

All academic modules reference students through this table.

---

# Responsibilities

The Students table is responsible for

- Student Identity
- Academic Information
- Enrollment Details
- Course Information
- Semester Information

The Students table is NOT responsible for

- Authentication
- Authorization
- Attendance
- Marks
- Assignments
- Reports
- Analytics

---

# Entity Overview

```
Student

↓

Attendance

↓

Marks

↓

Assignments

↓

Submissions

↓

Dashboard

↓

Reports

↓

Analytics
```

The Student entity is the core academic entity of EduTrack Pro.

---

# Database Table

```
students
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

## user_id

Type

Integer

Required

Yes

Foreign Key

```
users.id
```

Purpose

Connects the student profile to the authenticated user account.

Rules

- One Student belongs to one User.
- One User may have one Student profile.
- Teacher accounts do not require Student records.

---

## roll_number

Type

String

Required

Yes

Unique

Yes

Indexed

Yes

Purpose

Official institutional roll number.

Validation

- Required
- Unique
- Trim whitespace
- Maximum length 30

---

## enrollment_number

Type

String

Required

Yes

Unique

Yes

Indexed

Yes

Purpose

Official enrollment identifier.

Validation

- Required
- Unique
- Maximum length 50

---

## first_name

Type

String

Required

Yes

Maximum Length

50

Validation

- Required
- Trim whitespace
- Alphabetic characters only where appropriate

---

## last_name

Type

String

Required

Yes

Maximum Length

50

Validation

- Required
- Trim whitespace

---

## date_of_birth

Type

Date

Required

Yes

Purpose

Student birth date.

Validation

- Valid date
- Cannot be future date

---

## gender

Type

Enum

Values

```
Male

Female

Other
```

Required

Yes

---

## email

Type

String

Required

Yes

Unique

Yes

Purpose

Primary student email.

Validation

- Valid email
- Lowercase
- Unique

This may match the User email depending on implementation.

---

## phone

Type

String

Required

Yes

Purpose

Student contact number.

Validation

- Digits only
- Valid length

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

Electronics

Mechanical
```

---

## semester

Type

Integer

Required

Yes

Validation

Positive integer.

Purpose

Current semester.

---

## section

Type

String

Optional

Purpose

Academic section.

Example

```
A

B

C
```

---

## academic_year

Type

String

Required

Yes

Example

```
2025-26
```

---

## admission_date

Type

Date

Required

Yes

Purpose

Official admission date.

---

## profile_photo

Type

String

Optional

Purpose

Stores image path or URL.

Not required for MVP.

---

## is_active

Type

Boolean

Default

True

Purpose

Indicates whether the student is currently active.

Inactive students should not appear in default searches.

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

Student has

```
One User

Many Attendance Records

Many Marks

Many Assignment Submissions
```

Relationship Diagram

```
User

1

↓

1

Student

↓

Attendance

↓

Marks

↓

Submissions
```

---

# Foreign Keys

```
user_id

↓

users.id
```

Every Student must reference a valid User account.

---

# Constraints

Unique

- roll_number
- enrollment_number
- email

Required

- user_id
- roll_number
- enrollment_number
- first_name
- last_name
- email
- course
- semester

---

# Indexes

Create indexes for

- roll_number
- enrollment_number
- email
- semester
- department
- course
- academic_year

These columns are frequently searched.

---

# SQLAlchemy Relationships

Student

↓

User

Student

↓

Attendance

Student

↓

Marks

Student

↓

Submissions

Relationships should be bidirectional where appropriate.

---

# CRUD Responsibilities

Create Student

↓

Validate

↓

Verify User exists

↓

Check duplicate roll number

↓

Check duplicate enrollment number

↓

Store student

---

Read Student

Support

- By ID
- By Roll Number
- By Enrollment Number
- By Semester
- By Department
- List All

---

Update Student

Allow updating

- Name
- Semester
- Section
- Course
- Contact Details

Do not allow duplicate identifiers.

---

Delete Student

Validate dependencies before deletion.

Prevent orphaned records.

Delete only according to business rules.

---

# Validation Rules

Roll Number

- Required
- Unique
- Trim whitespace

Enrollment Number

- Required
- Unique

Semester

- Positive integer

Admission Date

- Cannot be future date

Email

- Valid format
- Unique

Names

- Required
- Maximum length
- Trim whitespace

---

# Search Requirements

Support searching by

- Name
- Roll Number
- Enrollment Number
- Department
- Course
- Semester

Searching should be case insensitive where practical.

---

# Filtering Requirements

Allow filtering by

- Course
- Department
- Semester
- Section
- Academic Year
- Active Status

Filtering should be combinable.

---

# Sorting Requirements

Support sorting by

- Name
- Roll Number
- Admission Date
- Semester

Ascending and descending.

---

# API Operations

Required endpoints

```
GET /students

GET /students/{id}

POST /students

PUT /students/{id}

DELETE /students/{id}

GET /students/search

GET /students/filter
```

---

# Expected Schemas

Create

```
StudentCreate
```

Update

```
StudentUpdate
```

Response

```
StudentResponse
```

List

```
StudentListResponse
```

Search

```
StudentSearchResponse
```

---

# Expected Service

```
student_service.py
```

Responsibilities

- Create Student
- Update Student
- Delete Student
- Get Student
- List Students
- Search Students
- Filter Students
- Validate Student Data

---

# Expected Router

```
students.py
```

Responsibilities

Expose REST endpoints for Student operations.

Authentication required.

Teacher-only modification endpoints.

Students may only access their own profile.

---

# Business Rules

Every Student must have one User account.

Roll Number must remain unique.

Enrollment Number must remain unique.

Deleting a Student must preserve database integrity.

Attendance, Marks, and Submissions depend on Student records.

---

# Expected Tests

Test

- Student creation
- Duplicate roll number
- Duplicate enrollment number
- Update student
- Delete student
- Search student
- Filter student
- Authentication
- Authorization
- Validation

Every endpoint should have corresponding tests.

---

# Future Compatibility

The schema should support future additions

- Guardian Information
- Address
- Blood Group
- Emergency Contact
- Academic Advisor
- Hostel Details
- Scholarships
- Achievements
- Profile Documents

These additions should integrate without redesigning the existing table.

---

# Definition of Completion

The Student module is complete when

✓ Student model exists.

✓ Relationships function.

✓ CRUD operations work.

✓ Search works.

✓ Filtering works.

✓ Validation works.

✓ Duplicate identifiers prevented.

✓ Authentication enforced.

✓ Authorization enforced.

✓ Swagger documentation complete.

✓ Tests pass.

---

# Summary

The Students table is the central academic entity of EduTrack Pro.

Every academic feature—including Attendance, Marks, Assignments, Reports, Dashboards, and Analytics—depends upon accurate Student records.

The implementation should prioritize data integrity, maintainability, efficient querying, and future scalability.

End of Students Database Specification.