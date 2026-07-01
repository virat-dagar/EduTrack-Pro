# 22_DATABASE_MIGRATIONS.md

# EduTrack Pro — Database Migration Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Database Migrations

---

# Purpose

This document defines the database migration strategy for EduTrack Pro.

Database migrations ensure that every change made to the database schema is version-controlled, reproducible, reversible, and consistent across development environments.

All database schema changes must be managed through Alembic.

Direct manual modification of production database schemas is prohibited.

---

# Migration Philosophy

Database schemas evolve over time.

Instead of manually modifying database tables, every structural change should be recorded as a migration.

Migration goals

- Version Control
- Repeatability
- Rollback Support
- Team Collaboration
- Safe Deployment
- Database Consistency

---

# Migration Tool

Official migration tool

```
Alembic
```

ORM

```
SQLAlchemy
```

Database

```
SQLite
```

Future compatibility

- PostgreSQL
- MySQL
- MariaDB

---

# Directory Structure

```
backend/

alembic/

│

├── versions/

├── env.py

├── script.py.mako

└── README
```

Migration configuration

```
backend/

alembic.ini
```

---

# Migration Responsibilities

Alembic manages

- Table Creation
- Column Creation
- Foreign Keys
- Constraints
- Indexes
- Schema Updates
- Schema Rollbacks

Alembic should not manage

- Business Logic
- Data Validation
- Authentication
- Application Configuration

---

# Initial Migration

The first migration should create

```
users

students

subjects

attendance

marks

assignments

submissions
```

including

- Primary Keys
- Foreign Keys
- Constraints
- Indexes

The initial migration represents Version 1 of the database.

---

# Migration Order

Create tables in dependency order.

Recommended sequence

```
Users

↓

Students

↓

Subjects

↓

Assignments

↓

Attendance

↓

Marks

↓

Submissions
```

Dependencies should always exist before child tables.

---

# Foreign Key Migration Order

Users

↓

Students

Students

↓

Attendance

Students

↓

Marks

Students

↓

Submissions

Subjects

↓

Attendance

Subjects

↓

Marks

Subjects

↓

Assignments

Assignments

↓

Submissions

The migration order should prevent foreign key failures.

---

# Naming Convention

Migration files should follow

```
YYYYMMDD_HHMM_description.py
```

Examples

```
20260701_1200_initial_schema.py

20260702_1430_add_indexes.py

20260704_0900_add_profile_photo.py
```

Migration names should describe the schema change.

---

# Migration Contents

Each migration should contain

Upgrade

↓

Downgrade

Both functions are mandatory.

---

# Upgrade Function

Responsible for

- Creating tables
- Adding columns
- Creating indexes
- Creating constraints
- Adding foreign keys

Upgrade should never remove data.

---

# Downgrade Function

Responsible for

Reversing the upgrade.

Examples

- Drop indexes
- Drop constraints
- Drop columns
- Drop tables

Downgrades should safely restore the previous schema version.

---

# Migration Rules

Every migration should

- Be atomic
- Be reversible
- Be tested
- Be documented

Never combine unrelated schema changes into a single migration.

---

# Schema Versioning

Every migration represents one schema version.

Example

```
Version 1

↓

Initial Schema

↓

Version 2

↓

Indexes

↓

Version 3

↓

Additional Columns

↓

Version 4

↓

New Constraints
```

Migration history should remain linear.

---

# Index Migration

Indexes should be created during migrations.

Required indexes

Users

- email
- role

Students

- roll_number
- enrollment_number
- semester

Subjects

- subject_code
- semester

Attendance

- student_id
- subject_id
- attendance_date

Marks

- student_id
- subject_id

Assignments

- subject_id
- due_date

Submissions

- assignment_id
- student_id

---

# Constraint Migration

Create constraints for

Primary Keys

Foreign Keys

Unique Keys

Check Constraints

Examples

Unique Email

Unique Roll Number

Unique Subject Code

Duplicate Attendance Prevention

Duplicate Submission Prevention

---

# Relationship Migration

Foreign key constraints should be created during migrations.

Never create relationships manually after deployment.

Relationship creation belongs inside migration scripts.

---

# Data Migration Policy

Schema migrations

Change database structure.

Data migrations

Modify stored records.

Keep these responsibilities separate.

Avoid combining structural changes with data transformation.

---

# Rollback Strategy

Every migration must support rollback.

Rollback should

Restore previous schema.

Maintain database consistency.

Avoid partial rollback.

Rollback should be tested before release.

---

# Development Workflow

Recommended workflow

```
Modify Model

↓

Generate Migration

↓

Review Migration

↓

Run Migration

↓

Verify Schema

↓

Commit Code
```

Never skip migration review.

Automatically generated migrations should always be inspected.

---

# Migration Testing

Each migration should be tested on

Empty database.

Existing populated database.

Rollback scenario.

Repeated execution prevention.

---

# Production Migration Rules

Before production deployment

Backup database.

Run migration.

Verify schema.

Verify API.

Verify application startup.

Only then release.

---

# Migration Safety

Never

Delete production tables without migration.

Rename columns manually.

Modify constraints manually.

Alter foreign keys manually.

Every structural change belongs inside Alembic.

---

# Future Migration Examples

Possible future migrations

- Add Parent Accounts
- Add Notifications
- Add Departments
- Add Courses
- Add Profile Photos
- Add GPA
- Add Semester History
- Add Timetable
- Add AI Predictions

Each feature should receive its own migration.

---

# Alembic Configuration

Configuration should include

Database URL

Target Metadata

Migration Script Location

Environment Configuration

Offline Mode

Online Mode

Configuration should remain centralized.

---

# Migration Best Practices

Keep migrations

Small

Focused

Reversible

Documented

Reviewable

Readable

Avoid large migrations containing multiple unrelated changes.

---

# Common Migration Workflow

```
Update SQLAlchemy Model

↓

Generate Alembic Revision

↓

Review Generated Code

↓

Run Upgrade

↓

Verify Database

↓

Run Application

↓

Commit Changes
```

---

# Migration Validation Checklist

Before accepting a migration verify

✓ Upgrade executes successfully.

✓ Downgrade executes successfully.

✓ Tables created correctly.

✓ Constraints created.

✓ Indexes created.

✓ Relationships work.

✓ Application starts.

✓ CRUD operations succeed.

✓ Existing data preserved.

---

# Definition of Completion

Migration support is complete when

✓ Alembic configured.

✓ Initial migration exists.

✓ Upgrade works.

✓ Downgrade works.

✓ Tables created correctly.

✓ Constraints enforced.

✓ Foreign keys created.

✓ Indexes created.

✓ Version history maintained.

✓ Migration documentation complete.

---

# Summary

Database migrations provide the foundation for safe and maintainable schema evolution throughout the lifetime of EduTrack Pro.

Every database modification should be tracked, version-controlled, reversible, and thoroughly tested using Alembic.

Following this strategy ensures consistent database structure across development, testing, deployment, and future project expansion.

End of Database Migration Specification.