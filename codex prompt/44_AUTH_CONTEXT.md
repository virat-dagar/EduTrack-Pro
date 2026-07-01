# 44_AUTH_CONTEXT.md

# EduTrack Pro — Authentication Context Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Authentication Context

---

# Purpose

This document defines the Authentication Context architecture for EduTrack Pro.

The Authentication Context is responsible for managing the authenticated user throughout the React application.

It serves as the single source of truth for

- Login Status
- Current User
- JWT Token
- User Role
- Session State
- Authentication Loading
- Logout

No component should manage authentication independently.

---

# Authentication Philosophy

Authentication state should exist only once.

Instead of every page checking

```
Local Storage
```

every page should consume

```
AuthContext
```

This guarantees

- Consistency
- Simplicity
- Better performance
- Easier maintenance

---

# Location

```
src/

context/

AuthContext.jsx
```

---

# Related Files

```
useAuth.js

api.js

ProtectedRoute.jsx

PublicRoute.jsx

authService.js
```

---

# Responsibilities

AuthContext manages

✓ JWT Token

✓ Logged-in User

✓ Authentication Status

✓ Login

✓ Logout

✓ Session Persistence

✓ Initial Authentication

✓ Loading State

It should NOT

- Render UI
- Call routers directly
- Perform business calculations

---

# Overall Authentication Flow

```
Application Starts

↓

AuthContext Initializes

↓

Read Local Storage

↓

JWT Found?

↓

YES

↓

GET /auth/me

↓

User Loaded

↓

Authenticated

↓

Render App

↓

NO

↓

Guest User

↓

Login Page
```

---

# Authentication Lifecycle

```
Login

↓

Store JWT

↓

Load User

↓

Authenticated

↓

Protected Routes

↓

Logout

↓

Clear Storage

↓

Guest User
```

---

# Context State

Recommended State

```javascript
{
    user: null,
    token: null,
    role: null,
    isAuthenticated: false,
    loading: true
}
```

Everything should be derived from this state.

---

# Context Values

Expose

```
user

token

role

loading

isAuthenticated

login()

logout()

refreshUser()

setUser()
```

These values should be available globally.

---

# Login Flow

```
Login Form

↓

POST /auth/login

↓

Receive JWT

↓

Store JWT

↓

Load Current User

↓

Update Context

↓

Redirect Dashboard
```

---

# Login Function

Responsibilities

```
Authenticate

↓

Save JWT

↓

Load User

↓

Update State

↓

Return Success
```

Login should never directly redirect.

The page handles navigation.

---

# Logout Flow

```
Logout Button

↓

Clear Context

↓

Remove JWT

↓

Remove Cached User

↓

Redirect Login
```

---

# Logout Responsibilities

```
Remove Token

↓

Remove User

↓

Reset Context

↓

Navigate Login
```

---

# Initial Application Load

When the application starts

```
Read JWT

↓

Token Exists?

↓

YES

↓

Validate Token

↓

Load User

↓

Update Context

↓

Render

↓

NO

↓

Guest
```

---

# Session Persistence

Authentication should survive

Browser Refresh

Tab Refresh

Soft Reload

JWT remains inside

```
Local Storage
```

until logout.

---

# Local Storage Keys

Recommended

```
access_token

current_user (optional)

theme
```

Avoid storing unnecessary information.

---

# Current User

After login

Call

```
GET /auth/me
```

Never trust cached user data forever.

Backend is the source of truth.

---

# Auto Login

If

```
JWT Exists

AND

JWT Valid
```

Automatically authenticate user.

User should not login repeatedly.

---

# Invalid Token

Flow

```
Application Starts

↓

JWT Exists

↓

GET /auth/me

↓

401 Unauthorized

↓

Remove Token

↓

Logout

↓

Redirect Login
```

---

# Expired Token

Flow

```
API Request

↓

401

↓

Logout

↓

Login Screen
```

Future versions may support

Refresh Tokens.

---

# Authentication Loading

During startup

```
Loading

↓

Verify JWT

↓

Load User

↓

Render Application
```

Never render protected pages before authentication completes.

---

# Loading State

Context should expose

```
loading
```

Pages should display

Loading Screen

until authentication completes.

---

# Role Management

Store

```
Teacher

Student
```

Role should be available globally.

Used by

```
Sidebar

Navigation

Protected Routes

Dashboard
```

---

# Authorization

Frontend authorization improves UX.

Backend authorization provides security.

Never rely on frontend role checks alone.

---

# Protected Route Integration

ProtectedRoute checks

```
loading

↓

Authenticated

↓

Role

↓

Render
```

Otherwise

Redirect.

---

# Public Route Integration

If authenticated

```
Login

↓

Redirect Dashboard
```

Guests remain on public pages.

---

# Axios Integration

Axios should automatically

```
Read JWT

↓

Attach Header

↓

Authorization

Bearer TOKEN
```

No component manually attaches tokens.

---

# 401 Response

Axios Interceptor

```
401

↓

Logout

↓

Navigate Login

↓

Show Toast
```

Centralize this behavior.

---

# Authentication Errors

Examples

```
Invalid Credentials

Expired Session

Unauthorized

Network Error
```

Display user-friendly messages.

---

# Security

Never store

```
Password

Password Hash

Secret Keys
```

Only

```
JWT

User

Theme
```

---

# Authentication Hook

```
useAuth()
```

Returns

```
user

role

loading

login

logout

isAuthenticated
```

Components should consume

```
useAuth()
```

instead of

```
useContext()
```

directly.

---

# Navbar Integration

Navbar displays

```
User Name

Role

Avatar

Logout
```

using AuthContext.

---

# Sidebar Integration

Sidebar should render

Teacher Menu

or

Student Menu

based on

```
role
```

---

# Dashboard Integration

Dashboard loads only after

```
loading == false

AND

Authenticated
```

---

# Route Refresh

Refreshing

```
/students

/dashboard

/reports
```

should preserve login state.

---

# Authentication Events

Context should react to

```
Login

Logout

401

Token Expiration

Profile Refresh
```

---

# Performance

Avoid repeated calls to

```
GET /auth/me
```

Call only

- Startup
- Manual Refresh
- Login

---

# Future Compatibility

Architecture should support

```
Refresh Tokens

Google Login

Microsoft Login

GitHub Login

Multi-Factor Authentication

Remember Me

Multiple Sessions

Session Management
```

without redesign.

---

# Testing

Verify

✓ Login

✓ Logout

✓ Refresh

✓ Auto Login

✓ Invalid Token

✓ Expired Token

✓ Protected Routes

✓ Public Routes

✓ Loading State

✓ Role Updates

✓ Navbar Updates

✓ Sidebar Updates

---

# AuthContext Checklist

Every implementation should

✓ Store JWT.

✓ Store Current User.

✓ Expose Authentication State.

✓ Handle Login.

✓ Handle Logout.

✓ Handle Startup Authentication.

✓ Handle Token Expiration.

✓ Integrate with Axios.

✓ Support Protected Routes.

---

# Definition of Completion

Authentication Context implementation is complete when

✓ Login works.

✓ Logout works.

✓ Startup authentication works.

✓ Protected routes work.

✓ Role state works.

✓ Session persists.

✓ Loading handled.

✓ Axios integration complete.

✓ Tests pass.

---

# Summary

The Authentication Context is the central authentication manager of EduTrack Pro.

It maintains the authenticated user, session state, JWT lifecycle, and global authentication logic while providing a clean, reusable API for every React component in the application.

By centralizing authentication, the frontend remains consistent, secure, maintainable, and ready for future authentication enhancements.

End of Authentication Context Specification.