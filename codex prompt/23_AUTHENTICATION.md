# 23_AUTHENTICATION.md

# EduTrack Pro — Authentication Module Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Authentication

---

# Purpose

The Authentication module is responsible for verifying user identity and establishing secure sessions within EduTrack Pro.

Authentication answers one question:

> **Who is the user?**

It does **not** determine permissions.

Authorization is handled separately in `24_AUTHORIZATION.md`.

Authentication must remain centralized, secure, reusable, and independent of business logic.

---

# Authentication Responsibilities

The Authentication module is responsible for

- User Login
- User Logout
- Password Verification
- Password Hashing
- JWT Token Generation
- JWT Validation
- Current User Retrieval
- Session Authentication
- Protected Route Authentication

Authentication is NOT responsible for

- Permission Checking
- Business Logic
- Student Management
- Academic Records
- Dashboards
- Analytics

---

# Authentication Flow

```
User

↓

Login Form

↓

Email + Password

↓

Backend Validation

↓

Find User

↓

Verify Password

↓

Generate JWT

↓

Return Token

↓

Frontend Stores Token

↓

Protected APIs

↓

JWT Verification

↓

Current User

↓

Authorized Request
```

---

# Login Workflow

Step 1

User enters

- Email
- Password

↓

Step 2

Frontend validates

- Empty fields
- Email format

↓

Step 3

POST

```
/auth/login
```

↓

Step 4

Backend

Find user by email

↓

Step 5

Verify

```
bcrypt.checkpw()
```

↓

Step 6

Generate JWT

↓

Step 7

Return

```
Access Token

User Information

Role
```

↓

Step 8

Frontend stores JWT

↓

Dashboard

---

# Failed Login Workflow

```
Invalid Email

OR

Invalid Password

↓

Authentication Failure

↓

401 Unauthorized

↓

Display Error

↓

Remain On Login Page
```

No JWT should be generated.

---

# Password Storage

Passwords must NEVER be stored in plaintext.

Storage workflow

```
Password

↓

bcrypt.hashpw()

↓

Password Hash

↓

Database
```

Only the hash should be stored.

---

# Password Verification

Verification workflow

```
Entered Password

↓

bcrypt.checkpw()

↓

Stored Hash

↓

True

OR

False
```

Passwords should never be decrypted.

---

# JWT Authentication

Authentication uses

```
JSON Web Tokens
```

JWT contains

- User ID
- Email
- Role
- Expiration Time

Sensitive information should never be embedded inside the token.

---

# JWT Payload

Recommended payload

```json
{
    "sub": "user_id",
    "email": "user@example.com",
    "role": "teacher",
    "exp": "<expiration_timestamp>"
}
```

Do not include

- Password
- Password Hash
- Phone
- Student Information

---

# JWT Lifetime

Recommended

```
Access Token

24 Hours
```

Future support may introduce Refresh Tokens.

The MVP requires only Access Tokens.

---

# Authentication Headers

Protected requests should include

```
Authorization

Bearer <JWT_TOKEN>
```

Every protected endpoint should verify this header.

---

# Current User Workflow

Protected endpoint

↓

JWT

↓

Decode

↓

Validate

↓

Retrieve User

↓

Return Current User

Current User should be available through a reusable dependency.

---

# Authentication Dependency

Every protected endpoint should use

```
get_current_user()
```

Responsibilities

- Decode JWT
- Verify signature
- Check expiration
- Retrieve database user
- Reject invalid tokens

Do not duplicate this logic.

---

# Logout Workflow

Logout occurs primarily on the frontend.

Workflow

```
Logout Button

↓

Delete JWT

↓

Delete Cached User

↓

Redirect Login

↓

Protected Routes Locked
```

No server-side session storage exists.

---

# Authentication Errors

Handle

Invalid Email

Invalid Password

Expired Token

Malformed Token

Inactive User

Missing Token

Invalid Signature

Every failure should return meaningful responses.

---

# Authentication Status Codes

Successful Login

```
200
```

Invalid Credentials

```
401
```

Missing Token

```
401
```

Expired Token

```
401
```

Inactive User

```
403
```

Unexpected Error

```
500
```

---

# Login Request

```json
{
    "email": "teacher@example.com",
    "password": "********"
}
```

---

# Login Response

```json
{
    "success": true,
    "message": "Login successful.",
    "data": {
        "access_token": "...",
        "token_type": "bearer",
        "user": {}
    }
}
```

---

# Authentication Schemas

Required schemas

```
LoginRequest

LoginResponse

CurrentUserResponse

TokenResponse
```

---

# Authentication Service

Expected file

```
services/auth_service.py
```

Responsibilities

- Authenticate User
- Verify Password
- Generate JWT
- Decode JWT
- Get Current User
- Validate Token

Business logic belongs here.

---

# Authentication Router

Expected file

```
routers/auth.py
```

Endpoints

```
POST /auth/login

GET /auth/me
```

Future

```
POST /auth/logout

POST /auth/refresh

POST /auth/change-password
```

---

# Password Change Workflow

Future compatible

```
Old Password

↓

Verify

↓

New Password

↓

Hash

↓

Store

↓

Success
```

Passwords should always be rehashed.

---

# Account Status Rules

Only active users

```
is_active == True
```

may authenticate.

Inactive accounts should receive

```
403 Forbidden
```

---

# Security Rules

Never

Store plaintext passwords.

Return password hashes.

Log passwords.

Log JWT secrets.

Accept expired JWTs.

Trust frontend authentication.

Authentication should always be verified by the backend.

---

# Swagger Documentation

Document

Login

Current User

Authentication Header

JWT Format

Response Models

Status Codes

Swagger should clearly indicate which endpoints require authentication.

---

# Testing Requirements

Test

✓ Login Success

✓ Login Failure

✓ Invalid Email

✓ Invalid Password

✓ Password Hashing

✓ JWT Generation

✓ JWT Verification

✓ Expired Token

✓ Missing Token

✓ Current User

✓ Inactive Account

✓ Protected Endpoint Authentication

---

# Future Compatibility

Authentication architecture should support

- Refresh Tokens
- Password Reset
- Email Verification
- Multi-Factor Authentication (MFA)
- OAuth (Google/GitHub)
- Single Sign-On (SSO)
- Session Revocation
- Device Management

These features should integrate without redesigning the current authentication flow.

---

# Definition of Completion

Authentication is complete when

✓ Login works.

✓ Password hashing works.

✓ Password verification works.

✓ JWT generation works.

✓ JWT validation works.

✓ Current user retrieval works.

✓ Protected endpoints authenticate correctly.

✓ Inactive users are blocked.

✓ Swagger documentation complete.

✓ Tests pass.

---

# Summary

The Authentication module establishes secure user identity across EduTrack Pro.

It provides a centralized, JWT-based authentication system built on bcrypt password hashing and reusable FastAPI dependencies.

All protected backend functionality depends on this module functioning correctly.

End of Authentication Module Specification.