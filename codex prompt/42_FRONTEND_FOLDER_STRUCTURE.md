# 42_FRONTEND_FOLDER_STRUCTURE.md

# EduTrack Pro — Frontend Folder Structure Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Frontend Folder Structure

---

# Purpose

This document defines the complete frontend directory structure for EduTrack Pro.

The objective is to maintain a scalable, modular, and production-ready React application.

Every file has one clear responsibility.

No folder should contain unrelated functionality.

---

# Design Principles

The frontend structure follows

- Separation of Concerns
- Feature Independence
- Component Reusability
- Maintainability
- Scalability
- Predictable Navigation
- Clean Architecture

---

# Complete Folder Structure

```
frontend/

│

├── public/

│   ├── favicon.ico

│   ├── logo.png

│   └── manifest.json

│

├── src/

│

│   ├── assets/

│   │

│   │   ├── images/

│   │   ├── icons/

│   │   ├── logos/

│   │   └── illustrations/

│   │

│   ├── components/

│   │

│   │   ├── common/

│   │   ├── layout/

│   │   ├── dashboard/

│   │   ├── students/

│   │   ├── attendance/

│   │   ├── marks/

│   │   ├── assignments/

│   │   ├── reports/

│   │   ├── charts/

│   │   ├── forms/

│   │   ├── tables/

│   │   ├── ui/

│   │   └── feedback/

│   │

│   ├── pages/

│   │

│   │   ├── auth/

│   │   ├── dashboard/

│   │   ├── students/

│   │   ├── attendance/

│   │   ├── marks/

│   │   ├── assignments/

│   │   ├── reports/

│   │   ├── profile/

│   │   ├── settings/

│   │   └── errors/

│   │

│   ├── layouts/

│   │

│   │   ├── DashboardLayout.jsx
│   │   ├── AuthLayout.jsx
│   │   └── BlankLayout.jsx
│   │

│   ├── services/

│   │

│   │   ├── api.js
│   │   ├── authService.js
│   │   ├── userService.js
│   │   ├── studentService.js
│   │   ├── subjectService.js
│   │   ├── attendanceService.js
│   │   ├── marksService.js
│   │   ├── assignmentService.js
│   │   ├── submissionService.js
│   │   ├── dashboardService.js
│   │   └── reportService.js
│   │

│   ├── context/

│   │

│   │   ├── AuthContext.jsx
│   │   ├── ThemeContext.jsx
│   │   └── SidebarContext.jsx
│   │

│   ├── hooks/

│   │

│   │   ├── useAuth.js
│   │   ├── useTheme.js
│   │   ├── usePagination.js
│   │   ├── useDebounce.js
│   │   └── useApi.js
│   │

│   ├── routes/

│   │

│   │   ├── AppRoutes.jsx
│   │   ├── ProtectedRoute.jsx
│   │   └── PublicRoute.jsx
│   │

│   ├── utils/

│   │

│   │   ├── constants.js
│   │   ├── validators.js
│   │   ├── helpers.js
│   │   ├── dateUtils.js
│   │   ├── formatters.js
│   │   └── storage.js
│   │

│   ├── styles/

│   │

│   │   ├── globals.css
│   │   ├── variables.css
│   │   ├── animations.css
│   │   └── theme.css
│   │

│   ├── App.jsx
│   ├── main.jsx
│   └── vite-env.d.ts
│

├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── .env
```

---

# Folder Responsibilities

Each folder has exactly one responsibility.

---

# assets/

Stores

```
Images

SVG

Icons

Logos

Illustrations

Brand Assets
```

Never store JavaScript files here.

---

# components/

Contains reusable UI components.

These components should be

Reusable

Independent

Small

Composable

Components should never perform API requests directly.

---

# common/

Contains reusable application-wide components.

Examples

```
Button

Input

Card

Modal

Loader

Avatar

Badge

Tooltip

Breadcrumb
```

---

# layout/

Contains layout components.

Examples

```
Sidebar

Navbar

Header

Footer

Page Container

Content Wrapper
```

---

# dashboard/

Contains dashboard-specific components.

Examples

```
Dashboard Cards

Statistics Cards

Quick Actions

Recent Activity

Summary Panels
```

---

# students/

Contains student-related UI.

Examples

```
Student Card

Student Form

Student Table

Student Profile

Student Filters
```

---

# attendance/

Contains attendance UI.

Examples

```
Attendance Table

Attendance Calendar

Attendance Form

Attendance Card

Attendance Percentage
```

---

# marks/

Contains marks-related components.

Examples

```
Marks Table

Grade Badge

Marks Form

Performance Card
```

---

# assignments/

Contains

```
Assignment Card

Assignment Form

Assignment Table

Assignment Status
```

---

# reports/

Contains report-specific UI.

Examples

```
Report Card

Report Filters

Export Button

Summary Panel
```

---

# charts/

Contains chart wrappers.

Examples

```
Line Chart

Bar Chart

Pie Chart

Radar Chart

Area Chart
```

Charts receive processed data from backend.

---

# forms/

Contains reusable form components.

Examples

```
Text Input

Password Input

Dropdown

Checkbox

Date Picker

Search Box
```

---

# tables/

Contains reusable data tables.

Features

```
Pagination

Sorting

Filtering

Search

Row Actions
```

---

# ui/

Contains design-system primitives.

Examples

```
Typography

Divider

Chip

Spinner

Skeleton

Toast
```

---

# feedback/

Contains user feedback components.

Examples

```
Loading Screen

Error Screen

Success Message

Empty State

Confirmation Dialog
```

---

# pages/

Contains route-level pages.

Each page represents one URL.

Pages coordinate components.

Pages should never contain large reusable UI.

---

# auth/

Contains

```
Login

Forgot Password (Future)

Reset Password (Future)
```

---

# dashboard/

Contains

```
Teacher Dashboard

Student Dashboard
```

---

# students/

Contains

```
Student List

Student Details

Add Student

Edit Student
```

---

# attendance/

Contains

```
Attendance Page

Attendance History

Attendance Summary
```

---

# marks/

Contains

```
Marks List

Add Marks

Performance Page
```

---

# assignments/

Contains

```
Assignment List

Assignment Details

Create Assignment
```

---

# reports/

Contains

```
Report Dashboard

Student Reports

Institution Reports
```

---

# profile/

Contains

```
User Profile

Account Settings
```

---

# settings/

Contains

```
Theme

Preferences

Application Settings
```

---

# errors/

Contains

```
404

403

500
```

---

# layouts/

Defines page layouts.

Dashboard pages should use

```
DashboardLayout
```

Authentication pages should use

```
AuthLayout
```

Landing pages may use

```
BlankLayout
```

---

# services/

Responsible only for

API communication.

Every backend module should have exactly one service.

Services should use

```
Axios Instance
```

No React code inside services.

---

# context/

Stores global application state.

Includes

```
Authentication

Theme

Sidebar
```

Avoid storing page-specific data globally.

---

# hooks/

Contains reusable custom React hooks.

Examples

```
Authentication

Pagination

Theme

API

Debounce
```

Hooks should remain framework-independent.

---

# routes/

Controls routing.

Contains

```
Application Routes

Protected Routes

Public Routes
```

No page logic.

---

# utils/

Contains utility functions.

Examples

```
Formatting

Date Utilities

Validation

Storage

Constants
```

Utilities should remain pure functions.

---

# styles/

Contains global styling.

Includes

```
Global CSS

Variables

Animations

Themes
```

Avoid page-specific CSS.

Use Tailwind utilities whenever possible.

---

# Root Files

main.jsx

Application entry point.

---

App.jsx

Loads routing and global providers.

---

vite.config.js

Vite configuration.

---

tailwind.config.js

Tailwind configuration.

---

.env

Contains

```
API URL

Environment Variables
```

Never commit

```
.env
```

---

# Import Rules

Good

```
Page

↓

Component

↓

Hook

↓

Service
```

Avoid

```
Component

↓

Component

↓

Component

↓

API
```

API calls belong inside pages or hooks.

---

# Component Hierarchy

```
Page

↓

Layout

↓

Feature Components

↓

UI Components

↓

HTML
```

---

# Naming Convention

Components

```
PascalCase
```

Example

```
StudentTable.jsx
```

Hooks

```
camelCase

with

use
```

Example

```
useAuth.js
```

Utilities

```
camelCase
```

Example

```
dateUtils.js
```

Folders

```
lowercase
```

---

# Performance

Organizing components by responsibility allows

✓ Better lazy loading

✓ Easier testing

✓ Better scalability

✓ Faster development

✓ Smaller components

---

# Future Compatibility

Structure should support

```
Notifications

AI Assistant

Live Chat

Messaging

Calendar

Examinations

Timetable

Mobile App
```

without major restructuring.

---

# Folder Structure Checklist

Every folder should

✓ Have one responsibility.

✓ Avoid duplicate functionality.

✓ Avoid circular dependencies.

✓ Remain scalable.

✓ Be easy to navigate.

---

# Definition of Completion

Frontend Folder Structure is complete when

✓ Every folder has one purpose.

✓ API communication isolated.

✓ Routing isolated.

✓ State isolated.

✓ Components reusable.

✓ Pages modular.

✓ Utilities centralized.

✓ Architecture scalable.

---

# Summary

The EduTrack Pro frontend follows a feature-based, component-driven architecture designed for long-term maintainability and scalability.

By separating pages, components, services, contexts, hooks, utilities, layouts, and styles into clearly defined modules, the project remains clean, professional, and ready for future expansion without architectural changes.

End of Frontend Folder Structure Specification.