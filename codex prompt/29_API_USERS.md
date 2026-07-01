# 29_API_USERS.md

# EduTrack Pro — Users API Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Users API

---

# Purpose

This document defines every User Management API endpoint in EduTrack Pro.

Unlike the Authentication API, which is responsible for verifying identity and issuing JWTs, the Users API manages user accounts.

User Management includes

- Creating users
- Viewing users
- Updating users
- Deleting users
- Listing users
- Activating users
- Deactivating users

All user management endpoints are protected.

---

# Base Route

```
/api/v1/users
```

---

# Resource

```
User
```

Represents

- Teacher Accounts
- Student Accounts

Future versions may include

- Administrator
- Parent
- Principal
- Head of Department

---

# Endpoint Summary

| Method | Endpoint | Purpose |
|---------|----------|----------|
| GET | /users | List Users |
| GET | /users/{id} | Get User |
| POST | /users | Create User |
| PUT | /users/{id} | Update User |
| DELETE | /users/{id} | Delete User |
| PUT | /users/{id}/activate | Activate User |
| PUT | /users/{id}/deactivate | Deactivate User |

---

# Authentication

Required

Yes

---

# Authorization

Teachers only.

Students may never manage users.

---

# Endpoint

```
GET /api/v1/users
```

Purpose

Return paginated list of users.

---

# Query Parameters

Pagination

```
?page=1

&page_size=20
```

Search

```
?q=virat
```

Filtering

```
?role=teacher

?is_active=true
```

Sorting

```
?sort=full_name

&order=asc
```

---

# Processing Flow

```
Authenticate

↓

Authorize

↓

Read Query Parameters

↓

Fetch Users

↓

Apply Search

↓

Apply Filters

↓

Apply Sorting

↓

Apply Pagination

↓

Return Response
```

---

# Successful Response

Status

```
200 OK
```

Example

```json
{
  "success": true,
  "message": "",
  "data": {
    "items": [
      {
        "id": 1,
        "full_name": "Virat",
        "email": "teacher@example.com",
        "role": "teacher",
        "is_active": true
      }
    ],
    "page": 1,
    "page_size": 20,
    "total_items": 12,
    "total_pages": 1
  }
}
```

---

# Endpoint

```
GET /api/v1/users/{id}
```

Purpose

Retrieve one user.

---

# Authorization

Teachers only.

---

# Successful Response

```
200 OK
```

```json
{
  "success": true,
  "message": "",
  "data": {
    "id": 1,
    "full_name": "Virat",
    "email": "teacher@example.com",
    "role": "teacher",
    "is_active": true,
    "created_at": "2026-07-01T10:30:00Z"
  }
}
```

---

# Not Found

```
404 Not Found
```

```json
{
  "success": false,
  "message": "User not found."
}
```

---

# Endpoint

```
POST /api/v1/users
```

Purpose

Create a new user account.

---

# Authorization

Teachers only.

---

# Request

```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "password": "Password123",
  "role": "student"
}
```

---

# Processing Flow

```
Authenticate

↓

Authorize

↓

Validate Request

↓

Check Duplicate Email

↓

Hash Password

↓

Store User

↓

Return User
```

---

# Successful Response

```
201 Created
```

```json
{
  "success": true,
  "message": "User created successfully.",
  "data": {
    "id": 15,
    "full_name": "John Doe",
    "email": "john@example.com",
    "role": "student",
    "is_active": true
  }
}
```

---

# Validation Errors

Duplicate Email

```
409 Conflict
```

```json
{
  "success": false,
  "message": "Email already exists."
}
```

---

# Endpoint

```
PUT /api/v1/users/{id}
```

Purpose

Update user information.

---

# Editable Fields

```
Full Name

Email

Role

Active Status
```

Password updates should use a dedicated endpoint in future versions.

---

# Processing Flow

```
Authenticate

↓

Authorize

↓

Validate

↓

Check User Exists

↓

Check Duplicate Email

↓

Update User

↓

Return Updated User
```

---

# Successful Response

```
200 OK
```

```json
{
  "success": true,
  "message": "User updated successfully.",
  "data": {
    "id": 5,
    "full_name": "Updated Name",
    "email": "updated@example.com",
    "role": "teacher"
  }
}
```

---

# Endpoint

```
DELETE /api/v1/users/{id}
```

Purpose

Delete a user.

---

# Authorization

Teachers only.

---

# Business Rules

Before deletion

Verify

- User exists
- No orphaned Student records
- No orphaned Attendance
- No orphaned Marks
- No orphaned Assignments

Deletion should preserve referential integrity.

---

# Successful Response

```
200 OK
```

```json
{
  "success": true,
  "message": "User deleted successfully."
}
```

---

# Endpoint

```
PUT /api/v1/users/{id}/activate
```

Purpose

Activate a disabled account.

---

# Processing Flow

```
Authenticate

↓

Authorize

↓

Verify User

↓

Set is_active=True

↓

Return Success
```

---

# Successful Response

```
200 OK
```

```json
{
  "success": true,
  "message": "User activated successfully."
}
```

---

# Endpoint

```
PUT /api/v1/users/{id}/deactivate
```

Purpose

Disable a user account.

Inactive users cannot authenticate.

---

# Successful Response

```
200 OK
```

```json
{
  "success": true,
  "message": "User deactivated successfully."
}
```

---

# Expected Schemas

```
UserCreate

UserUpdate

UserResponse

UserListResponse

UserActivationResponse
```

---

# Expected Router

```
routers/users.py
```

Responsibilities

- User CRUD
- User Search
- User Filtering
- Activation
- Deactivation

No business logic.

---

# Expected Service

```
services/user_service.py
```

Responsibilities

- Create User
- Update User
- Delete User
- Find User
- List Users
- Search Users
- Activate User
- Deactivate User
- Duplicate Email Validation

---

# Business Rules

Every email must be unique.

Passwords must always be hashed.

Inactive users cannot log in.

Teachers manage user accounts.

Students cannot access user management APIs.

---

# Search

Supported

```
?q=

Searches

- Name

- Email
```

Case insensitive.

---

# Filters

Support

```
role

is_active
```

Multiple filters may be combined.

---

# Sorting

Support

```
full_name

email

created_at

role
```

Ascending and descending.

---

# Security

Never return

```
password_hash
```

Never expose

- JWT Secrets
- Internal Security Fields

---

# Swagger Documentation

Every endpoint should include

- Summary
- Description
- Authentication
- Request Model
- Response Model
- Error Responses
- Examples

---

# API Testing

Verify

✓ List Users

✓ Get User

✓ Create User

✓ Update User

✓ Delete User

✓ Activate User

✓ Deactivate User

✓ Duplicate Email

✓ Authentication

✓ Authorization

✓ Pagination

✓ Filtering

✓ Searching

✓ Sorting

---

# Future Compatibility

Support future endpoints

```
PUT /users/{id}/change-role

PUT /users/{id}/reset-password

GET /users/statistics

GET /users/activity
```

Architecture should support these without redesign.

---

# Definition of Completion

The Users API is complete when

✓ CRUD endpoints work.

✓ Authentication enforced.

✓ Authorization enforced.

✓ Pagination works.

✓ Filtering works.

✓ Searching works.

✓ Sorting works.

✓ Duplicate emails prevented.

✓ Swagger complete.

✓ Tests pass.

---

# Summary

The Users API provides secure, role-based management of application accounts.

It enables teachers to manage institutional users while maintaining consistent REST standards, secure password handling, proper validation, and predictable API behavior.

End of Users API Specification.