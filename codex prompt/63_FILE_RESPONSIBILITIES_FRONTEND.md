# 63_FILE_RESPONSIBILITIES_FRONTEND.md

# EduTrack Pro — Frontend File Responsibilities Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Frontend File Responsibilities

---

# Purpose

This document defines the responsibility of every major frontend folder and file inside EduTrack Pro.

The frontend is responsible for

- Rendering the User Interface
- Managing Client-side State
- Handling User Interaction
- Communicating with Backend APIs
- Presenting Data
- Navigating Between Pages

The frontend must never contain business logic.

---

# Frontend Philosophy

The frontend should answer only one question:

> "How should the information be presented to the user?"

Business logic belongs in

```
Backend Services
```

The frontend should only

- Collect Input
- Display Data
- Send Requests
- Render Responses

---

# Technology Stack

```
React

Vite

React Router

Axios

Tailwind CSS

Recharts

Lucide React
```

---

# Frontend Folder Structure

```
frontend/

src/

│

├── assets/

├── components/

├── contexts/

├── hooks/

├── layouts/

├── pages/

├── routes/

├── services/

├── styles/

├── utils/

├── App.jsx

├── main.jsx

└── index.css
```

---

# Overall Flow

```
User

↓

React Component

↓

API Service

↓

Backend

↓

API Response

↓

Component Render
```

---

# main.jsx

Purpose

Application entry point.

Responsibilities

```
Render React App

Mount Root Component

Load Global Styles

Initialize Providers
```

Should NOT contain

Application logic.

---

# App.jsx

Purpose

Application root.

Responsibilities

```
Routes

Global Providers

Theme Provider

Authentication Provider

Layout Selection
```

Should remain lightweight.

---

# assets/

Purpose

Stores static assets.

Contains

```
Images

Icons

SVG

Logos

Illustrations

Fonts
```

Never contains React components.

---

# components/

Purpose

Reusable UI components.

Contains

```
Buttons

Cards

Tables

Charts

Inputs

Badges

Navbar

Sidebar

Modal

Toast
```

Rules

✓ Reusable

✓ Configurable

✓ Stateless whenever possible

---

# Component Structure

```
Component.jsx

Component.module.css (if required)

index.js (optional)
```

One component per file.

---

# contexts/

Purpose

Global React Context.

Contains

```
AuthContext

ThemeContext
```

Future

```
NotificationContext

SettingsContext
```

Context should only store

Global state.

---

# AuthContext

Responsibilities

```
Current User

JWT

Login

Logout

Authentication Status
```

Should never fetch unrelated data.

---

# ThemeContext

Responsibilities

```
Current Theme

Toggle Theme

Persist Theme
```

Only UI state.

---

# hooks/

Purpose

Reusable custom React hooks.

Examples

```
useAuth()

useTheme()

useDebounce()

usePagination()

useLocalStorage()

useApi()
```

Hooks should encapsulate reusable logic.

---

# layouts/

Purpose

Application layouts.

Contains

```
DashboardLayout

AuthLayout

BlankLayout
```

Layout handles

```
Navbar

Sidebar

Content Wrapper
```

---

# DashboardLayout

Responsibilities

```
Navbar

Sidebar

Content Area

Responsive Layout
```

Used by

Teacher Dashboard

Student Dashboard

---

# AuthLayout

Responsibilities

```
Centered Login Card

Background

Minimal Layout
```

Used only for

Authentication pages.

---

# pages/

Purpose

Application screens.

Contains

```
Login

Teacher Dashboard

Student Dashboard

Students

Subjects

Attendance

Marks

Assignments

Reports

Settings

Profile

404
```

Pages should

Compose components.

Avoid heavy logic.

---

# Route Philosophy

One page

↓

One route

↓

One responsibility.

---

# routes/

Purpose

Application routing.

Contains

```
Public Routes

Protected Routes

Role Routes
```

Examples

```
ProtectedRoute

TeacherRoute

StudentRoute
```

---

# ProtectedRoute

Responsibilities

```
Verify Authentication

Redirect Login

Render Protected Page
```

---

# TeacherRoute

Responsibilities

```
Verify Teacher Role

403 if Unauthorized
```

---

# StudentRoute

Responsibilities

```
Verify Student Role

Redirect if Invalid
```

---

# services/

Purpose

API communication.

Contains

```
api.js

authService.js

studentService.js

subjectService.js

attendanceService.js

marksService.js

assignmentService.js

submissionService.js

dashboardService.js

reportService.js
```

Services

Call backend APIs only.

---

# api.js

Purpose

Axios configuration.

Contains

```
Base URL

JWT Interceptor

Response Interceptor

Timeout

Headers
```

Shared across application.

---

# Authentication Service

Responsibilities

```
Login

Logout

Current User

Token Refresh (Future)
```

---

# Student Service

Responsibilities

```
CRUD Requests

Search

Pagination
```

No UI code.

---

# Dashboard Service

Responsibilities

```
Teacher Dashboard API

Student Dashboard API

Charts

Activity
```

---

# Report Service

Responsibilities

```
Generate Reports

Download Reports

Export
```

Future

```
PDF

CSV

Excel
```

---

# styles/

Purpose

Global styles.

Contains

```
Tailwind

Theme Variables

Global CSS

Animations
```

Avoid component-specific styling.

---

# index.css

Responsibilities

```
Tailwind Imports

CSS Variables

Typography

Theme Variables

Global Reset
```

---

# utils/

Purpose

Reusable helper functions.

Examples

```
Date Formatting

Validators

Storage

Formatters

Helpers
```

No React components.

---

# State Management

Global

```
Context API
```

Local

```
useState
```

Derived

```
useMemo
```

Async

```
useEffect
```

Future

```
TanStack Query
```

compatible.

---

# API Communication

Components

↓

Services

↓

Axios

↓

Backend

Never

```
Component

↓

Axios
```

directly.

---

# Error Handling

Pages should

Display

```
Loading

Error

Empty State

Retry
```

Components should never crash silently.

---

# Theme Support

Every page

Every component

Every layout

Supports

```
Light Theme

Dark Theme
```

---

# Responsive Support

Every page supports

```
Desktop

Tablet

Mobile
```

No desktop-only screens.

---

# Component Communication

Preferred

```
Props
```

Shared

```
Context
```

Avoid deeply nested prop drilling.

---

# Import Rules

Allowed

```
Pages

↓

Components

↓

Hooks

↓

Services

↓

Utils
```

Not Allowed

```
Components

↓

Pages
```

Not Allowed

```
Services

↓

Components
```

Not Allowed

```
Utils

↓

React Components
```

---

# Performance

Use

```
React.memo()

useMemo()

useCallback()

Lazy Loading
```

where beneficial.

Avoid unnecessary re-renders.

---

# Code Splitting

Pages should be

```
Lazy Loaded
```

using

```
React.lazy()

Suspense
```

---

# Accessibility

Support

```
Keyboard Navigation

ARIA Labels

Focus Indicators

Semantic HTML
```

Every page.

---

# Testing

Frontend tests should verify

✓ Rendering

✓ Routing

✓ API Calls

✓ Theme

✓ Authentication

✓ Forms

✓ Tables

✓ Charts

✓ Responsive Layout

---

# Future Compatibility

Frontend architecture should support

```
PWA

Offline Mode

Notifications

AI Assistant

Calendar

Messaging

Command Palette

Multi-language

White-label Themes
```

without restructuring.

---

# Frontend Checklist

Every frontend file should

✓ Have one responsibility.

✓ Be reusable.

✓ Avoid business logic.

✓ Support responsiveness.

✓ Support accessibility.

✓ Support themes.

✓ Be independently testable.

---

# Definition of Completion

Frontend File Responsibilities are complete when

✓ Folder structure implemented.

✓ Pages isolated.

✓ Components reusable.

✓ Services centralized.

✓ Context minimal.

✓ Routing secured.

✓ Theme supported.

✓ Responsive behavior complete.

---

# Summary

The Frontend File Responsibilities specification establishes a modular, scalable, and maintainable React architecture for EduTrack Pro.

By separating pages, components, layouts, services, contexts, hooks, utilities, and routing into clearly defined layers, the frontend remains easy to extend, highly reusable, and aligned with modern React engineering practices while maintaining a clean separation between presentation and business logic.

End of Frontend File Responsibilities Specification.