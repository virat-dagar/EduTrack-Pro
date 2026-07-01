# 28_API_AUTH.md

# EduTrack Pro — Authentication API Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Authentication API

---

# Purpose

This document defines every Authentication API endpoint exposed by the EduTrack Pro backend.

Authentication APIs are responsible only for verifying identity.

Authorization is handled separately.

Every endpoint defined here should follow the standards defined in

- 23_AUTHENTICATION.md
- 24_AUTHORIZATION.md
- 25_SECURITY.md
- 26_JWT_FLOW.md
- 27_API_STANDARDS.md

---

# Base Route

```
/api/v1/auth
```

All authentication endpoints belong under this route.

---

# Authentication Endpoints

| Method | Endpoint | Purpose |
|---------|----------|----------|
| POST | /login | Login user |
| GET | /me | Current authenticated user |
| POST | /logout *(Future)* | Logout |
| POST | /refresh *(Future)* | Refresh JWT |
| POST | /change-password *(Future)* | Change Password |
| POST | /forgot-password *(Future)* | Password Reset |
| POST | /reset-password *(Future)* | Reset Password |

Only Login and Current User are required for MVP.

---

# Endpoint

```
POST /api/v1/auth/login
```

Purpose

Authenticate user and issue JWT.

Authentication Required

No

Authorization Required

No

---

# Request Body

```json
{
    "email": "teacher@example.com",
    "password": "Password123"
}
```

---

# Validation Rules

Email

- Required
- Valid email format

Password

- Required
- Minimum length validation

---

# Processing Flow

```
Receive Request

↓

Validate Input

↓

Find User

↓

Verify Password

↓

Check Active Status

↓

Generate JWT

↓

Return Token
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
    "message": "Login successful.",
    "data": {
        "access_token": "JWT_TOKEN",
        "token_type": "Bearer",
        "expires_in": 86400,
        "user": {
            "id": 1,
            "full_name": "Virat",
            "email": "teacher@example.com",
            "role": "teacher"
        }
    }
}
```

---

# Failure Response

Invalid Credentials

Status

```
401 Unauthorized
```

```json
{
    "success": false,
    "message": "Invalid email or password."
}
```

---

# Inactive Account

Status

```
403 Forbidden
```

```json
{
    "success": false,
    "message": "Your account has been disabled."
}
```

---

# Endpoint

```
GET /api/v1/auth/me
```

Purpose

Return information about the currently authenticated user.

Authentication Required

Yes

Authorization Required

Any authenticated user.

---

# Request Header

```
Authorization

Bearer <JWT_TOKEN>
```

---

# Processing Flow

```
Receive Request

↓

Extract JWT

↓

Validate JWT

↓

Find User

↓

Return User
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
        "id": 1,
        "full_name": "Virat",
        "email": "teacher@example.com",
        "role": "teacher",
        "is_active": true
    }
}
```

---

# Missing Token

Status

```
401 Unauthorized
```

Example

```json
{
    "success": false,
    "message": "Authentication token is missing."
}
```

---

# Invalid Token

Status

```
401 Unauthorized
```

Example

```json
{
    "success": false,
    "message": "Invalid authentication token."
}
```

---

# Expired Token

Status

```
401 Unauthorized
```

Example

```json
{
    "success": false,
    "message": "Authentication token has expired."
}
```

---

# JWT Header Format

Every protected request should include

```
Authorization: Bearer <JWT_TOKEN>
```

No other authentication mechanism should be used.

---

# Authentication Dependencies

Every protected endpoint should use

```
get_current_user()
```

Responsibilities

- Read Authorization Header
- Decode JWT
- Verify Signature
- Verify Expiration
- Verify Active User
- Return Current User

---

# API Schemas

Required Request Schemas

```
LoginRequest
```

Required Response Schemas

```
LoginResponse

CurrentUserResponse

TokenResponse

ErrorResponse
```

---

# Authentication Router

Expected File

```
routers/auth.py
```

Responsibilities

- Login Endpoint
- Current User Endpoint

No business logic should exist inside the router.

---

# Authentication Service

Expected File

```
services/auth_service.py
```

Responsibilities

- Verify Password
- Generate JWT
- Decode JWT
- Authenticate User
- Retrieve Current User

---

# Authentication Security

Passwords

- Never returned
- Never logged
- Always hashed

JWT

- Signed using HS256
- Secret loaded from environment variables
- Expiration enforced

---

# Swagger Documentation

Swagger should include

- Request examples
- Response examples
- Authentication requirements
- Error responses
- Status codes

Both endpoints should appear under the **Authentication** tag.

---

# API Testing

Test

✓ Login Success

✓ Wrong Password

✓ Unknown Email

✓ Missing Email

✓ Missing Password

✓ Current User

✓ Invalid JWT

✓ Expired JWT

✓ Missing JWT

✓ Disabled User

---

# Future Endpoints

Architecture should support

```
POST /logout

POST /refresh

POST /change-password

POST /forgot-password

POST /reset-password
```

These endpoints should integrate without modifying the existing authentication API.

---

# Authentication API Checklist

Verify

✓ Login works.

✓ Current User works.

✓ JWT generated.

✓ JWT validated.

✓ Password verified.

✓ Active user enforced.

✓ Error responses standardized.

✓ Swagger documentation complete.

✓ Tests pass.

---

# Summary

The Authentication API provides secure identity verification for EduTrack Pro through JWT-based authentication.

It exposes a minimal, standardized set of endpoints that establish authenticated sessions while maintaining strong security, predictable responses, and compatibility with future authentication enhancements.

End of Authentication API Specification.