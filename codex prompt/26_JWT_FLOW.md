# 26_JWT_FLOW.md

# EduTrack Pro — JWT Authentication Flow Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: JWT Flow

---

# Purpose

This document defines the complete JSON Web Token (JWT) lifecycle within EduTrack Pro.

JWT serves as the authentication mechanism between the frontend and backend.

Every protected API request relies on JWT validation.

This document explains how tokens are

- Created
- Signed
- Returned
- Stored
- Sent
- Verified
- Expired
- Rejected

The JWT implementation should remain centralized and reusable.

---

# JWT Overview

Authentication Method

```
JSON Web Token (JWT)
```

Algorithm

```
HS256
```

Authentication Type

```
Stateless Authentication
```

Token Transport

```
Authorization Header

Bearer <JWT>
```

---

# Complete Authentication Lifecycle

```
User

↓

Login Page

↓

Email + Password

↓

POST /auth/login

↓

Backend Authentication

↓

Password Verification

↓

Generate JWT

↓

Return Token

↓

Frontend Stores Token

↓

Protected API Request

↓

Authorization Header

↓

Backend JWT Verification

↓

Current User

↓

Authorization

↓

Business Logic

↓

JSON Response
```

---

# Login Flow

Step 1

User enters

```
Email

Password
```

↓

Step 2

Frontend validates

- Empty fields
- Email format

↓

Step 3

Backend receives

```
POST /auth/login
```

↓

Step 4

Lookup User

↓

Step 5

Verify Password

↓

Step 6

Generate JWT

↓

Step 7

Return

```
JWT

Role

User Information
```

↓

Step 8

Redirect Dashboard

---

# JWT Generation Flow

```
User

↓

Verify Password

↓

Generate Payload

↓

Add Expiration

↓

Sign Token

↓

Return JWT
```

Only authenticated users receive JWTs.

---

# JWT Payload

Recommended payload

```json
{
  "sub": "1",
  "email": "teacher@example.com",
  "role": "teacher",
  "exp": 1782919200
}
```

Payload should remain minimal.

---

# JWT Payload Rules

Include

- User ID
- Email
- Role
- Expiration

Never include

- Password
- Password Hash
- Phone
- Student Information
- Attendance
- Marks
- Personal Data

JWT is an identity token.

It is not a database.

---

# Token Signing

JWT should be signed using

```
SECRET_KEY
```

Stored inside

```
.env
```

Algorithm

```
HS256
```

Secret key must never be hardcoded.

---

# JWT Expiration

Recommended

```
24 Hours
```

Configuration

```
ACCESS_TOKEN_EXPIRE_MINUTES
```

stored inside environment variables.

Expired tokens become invalid immediately.

---

# Frontend Storage

After login

```
JWT

↓

Local Storage
```

Recommended key

```
access_token
```

User information may also be cached separately.

---

# Frontend Request Flow

Every protected request

```
Retrieve Token

↓

Authorization Header

↓

HTTP Request
```

Header

```
Authorization

Bearer eyJhbGc...
```

Axios should automatically attach the token using an interceptor.

---

# Backend Verification Flow

```
Receive Request

↓

Read Authorization Header

↓

Extract Token

↓

Decode JWT

↓

Verify Signature

↓

Verify Expiration

↓

Retrieve User

↓

Current User Dependency

↓

Authorization

↓

Execute Endpoint
```

---

# Invalid Token Flow

```
JWT

↓

Decode

↓

Failure

↓

401 Unauthorized

↓

Return Error
```

No endpoint should continue processing after JWT failure.

---

# Missing Token Flow

```
Protected Request

↓

No Authorization Header

↓

401 Unauthorized
```

---

# Expired Token Flow

```
JWT

↓

Expiration Check

↓

Expired

↓

401 Unauthorized
```

Frontend should redirect users back to Login.

---

# Invalid Signature Flow

```
JWT

↓

Signature Validation

↓

Failure

↓

401 Unauthorized
```

Possible causes

- Tampering
- Wrong Secret
- Corrupted Token

---

# Current User Dependency

Reusable dependency

```
get_current_user()
```

Responsibilities

- Read Authorization header
- Decode JWT
- Verify Signature
- Verify Expiration
- Retrieve User
- Verify User Exists
- Verify Active Status
- Return Current User

Every protected endpoint should use this dependency.

---

# Protected Route Flow

```
Incoming Request

↓

JWT Verification

↓

Current User

↓

Authorization

↓

Business Logic

↓

Database

↓

JSON Response
```

Authentication always occurs before authorization.

---

# Logout Flow

Logout is handled on the frontend.

Workflow

```
Logout

↓

Remove JWT

↓

Remove Cached User

↓

Redirect Login
```

No server-side session invalidation is required for the MVP.

---

# Token Refresh

Not implemented in MVP.

Future flow

```
Access Token Expired

↓

Refresh Token

↓

Generate New Access Token

↓

Continue Session
```

Architecture should remain compatible.

---

# Token Revocation

Not implemented for MVP.

Future enhancements may include

- Blacklisting
- Session Revocation
- Device Logout
- Forced Logout

Current implementation remains stateless.

---

# Axios Integration

Axios interceptor should

Before every request

```
Read JWT

↓

Add Authorization Header

↓

Send Request
```

Centralize this behavior.

Do not manually attach tokens in every API call.

---

# FastAPI Security Dependency

Recommended implementation

```
OAuth2PasswordBearer
```

Combined with

```
get_current_user()
```

This provides consistent JWT handling across all routers.

---

# Error Responses

Missing Token

```json
{
  "success": false,
  "message": "Authentication token is missing."
}
```

Expired Token

```json
{
  "success": false,
  "message": "Authentication token has expired."
}
```

Invalid Token

```json
{
  "success": false,
  "message": "Invalid authentication token."
}
```

---

# Security Considerations

Always

Verify expiration.

Verify signature.

Verify user exists.

Verify account active.

Never trust token contents without validation.

Never accept unsigned JWTs.

---

# Environment Variables

Required

```
SECRET_KEY

ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES
```

Should be loaded through application configuration.

Never expose these values.

---

# JWT Testing

Verify

✓ Login generates token.

✓ Token decodes correctly.

✓ Signature verification works.

✓ Expired token rejected.

✓ Invalid token rejected.

✓ Missing token rejected.

✓ Authorization header parsed.

✓ Current user retrieved.

✓ Active user verified.

✓ Inactive user rejected.

---

# Future Compatibility

JWT implementation should support

- Refresh Tokens
- Token Rotation
- OAuth Providers
- Multi-Factor Authentication
- Device Sessions
- Session Revocation
- Single Sign-On

These additions should not require redesigning the authentication architecture.

---

# JWT Lifecycle Diagram

```
Login

↓

Password Verification

↓

JWT Generation

↓

Frontend Storage

↓

Protected Request

↓

JWT Verification

↓

Current User

↓

Authorization

↓

Business Logic

↓

Response

↓

Logout

↓

Delete Token
```

---

# Definition of Completion

JWT implementation is complete when

✓ Tokens are generated.

✓ Tokens are signed securely.

✓ Tokens contain minimal payload.

✓ Protected endpoints validate tokens.

✓ Expired tokens rejected.

✓ Invalid tokens rejected.

✓ Current user dependency reusable.

✓ Frontend automatically sends JWT.

✓ Swagger authentication works.

✓ Tests pass.

---

# Summary

JWT provides secure, stateless authentication throughout EduTrack Pro.

Every protected request depends on a properly generated, transmitted, verified, and validated token before business logic executes.

The implementation should remain centralized, secure, maintainable, and easily extensible for future authentication enhancements.

End of JWT Flow Specification.