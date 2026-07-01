# 14_DATABASE_USERS.md

# EduTrack Pro — Users Database Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: User

---

# Purpose

The Users table represents every authenticated account within EduTrack Pro.

Authentication is performed exclusively using records stored in this table.

Every authenticated person in the system must have exactly one User record.

Users represent identities.

Student-specific academic information belongs in the Student table.

---

# Responsibilities

The Users table is responsible for

- Authentication
- Authorization
- Identity
- Account Status
- Role Management

The Users table is NOT responsible for

- Academic Records
- Attendance
- Marks
- Assignments
- Analytics
- Dashboard Statistics

---

# Entity Overview

```
User

↓

Authentication

↓

Role

↓

Application Access
```

---

# Database Table

```
users
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

Properties

- Primary Key
- Auto Increment
- Indexed

Purpose

Unique identifier.

---

## full_name

Type

String

Required

Yes

Maximum Length

100

Purpose

Display name of the user.

Validation

- Cannot be empty
- Trim whitespace
- Minimum length 2

---

## email

Type

String

Required

Yes

Unique

Yes

Indexed

Yes

Purpose

Primary login credential.

Validation

- Valid email format
- Lowercase before storage
- Remove leading/trailing spaces
- Unique across entire application

---

## password_hash

Type

String

Required

Yes

Purpose

Stores bcrypt hashed password.

Rules

- Never plaintext
- Never returned by APIs
- Never logged
- Never editable directly

---

## role

Type

Enum

Required

Yes

Values

```
teacher

student
```

Purpose

Determines system permissions.

---

## is_active

Type

Boolean

Default

True

Purpose

Allows administrators or future features to disable accounts without deleting them.

Inactive users cannot log in.

---

## created_at

Type

Datetime

Required

Yes

Default

Current Timestamp

Purpose

Creation timestamp.

---

## updated_at

Type

Datetime

Required

Yes

Automatically updated

Purpose

Tracks latest modification.

---

# Relationships

```
User

1

↓

1

Student
```

Teacher accounts may not have associated Student records.

Student accounts should always reference a corresponding Student profile.

---

# Constraints

Unique

- Email

Required

- full_name
- email
- password_hash
- role

Default Values

- is_active = True

---

# Indexes

Create indexes for

- email
- role
- is_active

These columns are frequently queried.

---

# SQLAlchemy Relationships

Relationship

```
User

↓

Student
```

Bidirectional relationship should be configured where applicable.

---

# CRUD Responsibilities

Create User

Validate

↓

Hash Password

↓

Store User

---

Read User

Retrieve

- By ID
- By Email
- Current User

---

Update User

Allow updating

- Name
- Email
- Password
- Active Status

Role updates should require authorization.

---

Delete User

Delete only when permitted.

Prevent orphaned Student records.

Deletion should preserve database integrity.

---

# Validation Rules

Email

- Required
- Valid format
- Unique
- Lowercase
- No duplicates

Password

- Required
- Hash before storage
- Never expose

Role

Only

```
teacher

student
```

Name

- Required
- Minimum length
- Maximum length
- Trim whitespace

---

# Authentication Rules

Authentication uses

Email

+

Password

Workflow

```
Email

↓

Lookup User

↓

Verify Password

↓

Generate JWT

↓

Return Token
```

Passwords are verified using bcrypt.

---

# Authorization Rules

Teachers

Full academic permissions.

Students

Read-only access to personal information.

Role is determined entirely by this table.

---

# API Operations

Required endpoints

```
POST /login

GET /users/me

GET /users

GET /users/{id}

POST /users

PUT /users/{id}

DELETE /users/{id}
```

Authentication required where applicable.

---

# Business Rules

One email per account.

One account per email.

Passwords always hashed.

Inactive users cannot authenticate.

Role determines access.

Authentication depends entirely upon this table.

---

# Security Rules

Never return

```
password_hash
```

Never expose

JWT secrets.

Never log

Passwords.

Never allow

Password retrieval.

Only password reset/change.

---

# Expected Schemas

Create

```
UserCreate
```

Update

```
UserUpdate
```

Response

```
UserResponse
```

Authentication

```
LoginRequest

LoginResponse
```

Current User

```
CurrentUserResponse
```

---

# Expected Service

```
user_service.py
```

Responsibilities

- Create User
- Update User
- Delete User
- Get User
- Get Current User
- Find By Email
- Activate User
- Deactivate User

---

# Expected Router

```
users.py
```

Responsibilities

Expose all User APIs.

Routers remain lightweight.

Delegate all logic to services.

---

# Expected Tests

Test

- User creation
- Duplicate email rejection
- Password hashing
- Login success
- Login failure
- Role validation
- Active account
- Inactive account
- Delete user
- Update user

Every endpoint should have corresponding tests.

---

# Future Compatibility

Schema should support future additions

- Admin role
- Parent role
- Faculty role
- Multi-factor authentication
- Password reset
- Email verification
- Profile images
- Account recovery

These additions should not require redesigning the current schema.

---

# Definition of Completion

The Users module is complete when

✓ User model exists.

✓ Relationships function.

✓ CRUD operations work.

✓ Password hashing works.

✓ Authentication works.

✓ Authorization works.

✓ JWT generation works.

✓ Validation works.

✓ Duplicate emails prevented.

✓ Swagger documentation complete.

✓ Unit tests pass.

---

# Summary

The Users table is the foundation of authentication and authorization within EduTrack Pro.

Every authenticated interaction begins with a valid User record.

The module should remain secure, reliable, maintainable, and extensible while serving as the identity layer for the entire application.

End of Users Database Specification.