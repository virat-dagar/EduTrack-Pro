# 43_ROUTING.md

# EduTrack Pro — Routing Architecture Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Routing

---

# Purpose

This document defines the routing architecture for the EduTrack Pro frontend.

Routing controls

- Navigation
- Authentication
- Authorization
- Layout selection
- Route protection
- URL structure

The routing system should be scalable, maintainable, and role-aware.

---

# Routing Philosophy

The routing layer should

- Be centralized
- Support protected routes
- Support public routes
- Support role-based routing
- Prevent unauthorized access
- Keep URLs predictable
- Separate layouts from pages

---

# Routing Technology

Library

```
React Router DOM v6+
```

Main Router

```
BrowserRouter
```

Navigation

```
useNavigate()

Link

NavLink
```

---

# Router Architecture

```
BrowserRouter

↓

AppRoutes

↓

Public Routes

↓

Protected Routes

↓

Dashboard Layout

↓

Pages
```

---

# Routing Folder

```
src/

routes/

│

├── AppRoutes.jsx

├── ProtectedRoute.jsx

└── PublicRoute.jsx
```

---

# Route Categories

Application routes are divided into

```
Public

Protected

Role-Based

Fallback
```

---

# Public Routes

No authentication required.

Examples

```
/

Login

404

403
```

---

# Protected Routes

Authentication required.

Requires

```
Valid JWT
```

Unauthenticated users

↓

Redirect

```
/login
```

---

# Role-Based Routes

Teacher

May access

```
Dashboard

Students

Attendance

Marks

Subjects

Assignments

Reports

Users

Analytics
```

Student

May access

```
Dashboard

My Attendance

My Marks

Assignments

Profile

Reports
```

Students should never access teacher pages.

---

# URL Structure

```
/

↓

login

↓

dashboard

↓

students

↓

attendance

↓

marks

↓

subjects

↓

assignments

↓

reports

↓

profile

↓

settings
```

---

# Complete Route Tree

```
/

│

├── login

│

├── dashboard

│   ├── teacher

│   └── student

│

├── students

│   ├── list

│   ├── create

│   ├── :id

│   └── edit/:id

│

├── subjects

│   ├── list

│   ├── create

│   ├── :id

│   └── edit/:id

│

├── attendance

│   ├── list

│   ├── mark

│   ├── summary

│   └── history

│

├── marks

│   ├── list

│   ├── create

│   ├── performance

│   └── edit/:id

│

├── assignments

│   ├── list

│   ├── create

│   ├── :id

│   └── edit/:id

│

├── reports

│   ├── students

│   ├── attendance

│   ├── marks

│   └── institution

│

├── profile

│

├── settings

│

├── forbidden

│

└── *
```

---

# Application Entry

```
main.jsx

↓

BrowserRouter

↓

App

↓

AppRoutes
```

---

# AppRoutes Responsibilities

Responsible for

- Registering routes
- Layout selection
- Nested routes
- Redirects

AppRoutes should not contain business logic.

---

# PublicRoute Component

Responsibilities

```
Prevent authenticated users

from visiting Login page.
```

Example

Authenticated User

↓

Visits

```
/login
```

↓

Redirect

```
/dashboard
```

---

# ProtectedRoute Component

Responsibilities

Verify

```
JWT

↓

Authenticated

↓

Authorized

↓

Render Page
```

Otherwise

```
Redirect Login
```

---

# Protected Route Flow

```
User

↓

Protected Route

↓

Check Token

↓

Check Current User

↓

Role Validation

↓

Render Page

OR

Redirect
```

---

# Authentication Check

ProtectedRoute should verify

```
JWT Exists

↓

JWT Valid

↓

Current User Loaded
```

No API page should render before authentication completes.

---

# Authorization Check

Teacher Routes

```
Role == teacher
```

Student Routes

```
Role == student
```

Failure

↓

Redirect

```
/403
```

---

# Nested Layouts

Dashboard pages should share

```
Sidebar

Navbar

Content Area
```

Implemented through

```
DashboardLayout
```

---

# Dashboard Layout Flow

```
DashboardLayout

↓

Sidebar

↓

Navbar

↓

Outlet()

↓

Current Page
```

React Router

```
Outlet
```

renders child routes.

---

# Dynamic Routes

Supported

```
students/:id

subjects/:id

assignments/:id

marks/:id
```

Dynamic IDs should always be validated.

---

# Navigation

Use

```
Link

NavLink
```

Avoid

```
window.location
```

---

# Redirect Rules

Unauthenticated

↓

```
/login
```

Authenticated

↓

Role Dashboard

Teacher

↓

```
/dashboard/teacher
```

Student

↓

```
/dashboard/student
```

Unknown Routes

↓

```
404
```

Forbidden

↓

```
403
```

---

# Dashboard Routing

Teacher

```
/dashboard/teacher
```

Student

```
/dashboard/student
```

Dashboard components remain separate.

---

# Student Routes

Teacher

```
Students List

Student Details

Create Student

Edit Student
```

Student

```
Own Profile Only
```

---

# Attendance Routes

Teacher

```
Attendance List

Attendance Summary

Mark Attendance
```

Student

```
Attendance History
```

---

# Marks Routes

Teacher

```
Marks List

Add Marks

Performance
```

Student

```
My Marks
```

---

# Assignment Routes

Teacher

```
Assignments

Create Assignment

Edit Assignment
```

Student

```
Assignments

Submission
```

---

# Reports Routes

Teacher

Institution Reports

Attendance Reports

Marks Reports

Student Reports

Student

Own Academic Report

---

# Lazy Loading

Pages should use

```
React.lazy()

+

Suspense
```

Example

```
Dashboard

Students

Reports
```

Improve startup performance.

---

# Loading Screen

While lazy loading

Display

```
Loading Spinner

or

Skeleton
```

---

# Scroll Behavior

Every navigation

↓

Scroll to

Top

Automatically.

---

# Breadcrumb Support

Architecture should support

```
Dashboard

>

Students

>

Student Details
```

Future implementation.

---

# Route Constants

Recommended

```
utils/constants.js
```

Store

```
ROUTES.LOGIN

ROUTES.DASHBOARD

ROUTES.STUDENTS

ROUTES.ATTENDANCE

ROUTES.MARKS
```

Avoid hardcoded strings.

---

# Error Pages

Dedicated pages

```
403

404

500
```

Friendly UI.

Navigation back to dashboard.

---

# Security

Routes alone

DO NOT

provide security.

Backend authorization remains mandatory.

Frontend routing improves UX only.

---

# Performance

Routing should

Support lazy loading.

Avoid unnecessary rerenders.

Keep layouts persistent.

Only page content changes.

---

# Future Compatibility

Routing architecture should support

```
Admin

Parent

Notifications

Calendar

Messaging

Examinations

AI Assistant

Plugin Pages
```

without restructuring.

---

# Testing

Verify

✓ Public Routes

✓ Protected Routes

✓ Login Redirect

✓ Logout Redirect

✓ Role Validation

✓ Dynamic Routes

✓ Unknown Routes

✓ Nested Layouts

✓ Lazy Loading

✓ Navigation

---

# Routing Checklist

Every route should

✓ Have one page.

✓ Use correct layout.

✓ Be protected if necessary.

✓ Validate role.

✓ Handle loading.

✓ Handle errors.

✓ Support navigation.

---

# Definition of Completion

Routing implementation is complete when

✓ Public routes work.

✓ Protected routes work.

✓ Teacher routing works.

✓ Student routing works.

✓ Nested layouts work.

✓ Dynamic routes work.

✓ Redirects work.

✓ Error pages work.

✓ Tests pass.

---

# Summary

The EduTrack Pro routing architecture provides a centralized, scalable, and role-aware navigation system built on React Router.

By separating public, protected, and role-based routes while leveraging reusable layouts and lazy loading, the application remains secure, maintainable, and optimized for future expansion.

End of Routing Architecture Specification.