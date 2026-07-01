# 09_PROJECT_FOLDER_STRUCTURE.md

# EduTrack Pro — Project Folder Structure

Version: 1.0

Status: Final

Architecture Status: Frozen

---

# Purpose

This document defines the official folder structure of EduTrack Pro.

The folder structure has already been finalized.

Codex must **respect the existing repository structure** and implement code inside the appropriate files and folders.

Do not rename folders.

Do not move files.

Do not introduce parallel architectures.

The implementation must follow the existing repository layout.

---

# Repository Overview

The project consists of two independent applications.

```
EduTrack-Pro/

├── backend/
├── frontend/
├── docs/
├── README.md
├── .gitignore
└── other project configuration files
```

The backend and frontend communicate exclusively through REST APIs.

---

# Backend Folder Structure

```
backend/

├── app/
│
├── tests/
│
├── requirements.txt
│
├── alembic.ini
│
└── main.py
```

Backend contains all server-side code.

No frontend code should exist here.

---

# app/

The `app` folder contains the complete FastAPI application.

Every backend feature belongs somewhere inside this directory.

```
app/

├── core/
├── database/
├── models/
├── schemas/
├── routers/
├── services/
├── utils/
├── exceptions/
└── main.py
```

---

# core/

Purpose

Application-wide configuration.

Contains

- JWT configuration
- Security configuration
- Settings
- Environment configuration
- Password hashing
- Authentication helpers

Responsibilities

- Global configuration
- Security helpers
- Application constants

Must NOT contain

- Business logic
- CRUD operations
- Database models

---

# database/

Purpose

Database initialization.

Responsibilities

- Database engine
- Session creation
- Base model
- Connection configuration

Only database configuration belongs here.

---

# models/

Purpose

SQLAlchemy ORM models.

Every database table must have exactly one model.

Responsibilities

- Table definitions
- Relationships
- Constraints
- Indexes

Must NOT contain

- API logic
- Validation
- Business calculations

---

# schemas/

Purpose

Pydantic schemas.

Responsibilities

- Request validation
- Response serialization
- Update schemas
- Create schemas

Each model should have corresponding schemas.

---

# routers/

Purpose

REST API endpoints.

Responsibilities

- API routes
- Dependency injection
- Authentication dependencies
- Authorization dependencies
- HTTP responses

Routers remain thin.

Business logic belongs inside services.

---

# services/

Purpose

Business logic.

Responsibilities

- CRUD operations
- Validation
- Analytics
- Calculations
- Database interaction
- Rule enforcement

Every major module should have its own service.

Examples

StudentService

AttendanceService

MarksService

AssignmentService

DashboardService

AnalyticsService

---

# utils/

Purpose

Reusable helper functions.

Examples

- Date utilities
- Formatting
- Pagination
- Search helpers
- Common validators

Utilities should remain generic.

---

# exceptions/

Purpose

Custom exception classes.

Responsibilities

Provide meaningful exceptions.

Examples

StudentNotFound

DuplicateEnrollment

InvalidAttendance

UnauthorizedAccess

Avoid generic exceptions.

---

# tests/

Purpose

Backend testing.

Contains

- API tests
- Service tests
- Authentication tests
- Integration tests

Tests should mirror backend modules.

---

# Frontend Folder Structure

```
frontend/

├── src/
├── public/
├── package.json
├── vite.config.js
└── other configuration files
```

Frontend contains the complete React application.

---

# src/

Purpose

Main React application.

Contains

```
src/

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
└── main.jsx
```

---

# assets/

Purpose

Static resources.

Contains

- Images
- Icons
- Logos
- Fonts

No business logic.

---

# components/

Purpose

Reusable UI components.

Examples

Button

Card

Modal

Table

Chart

Sidebar

Navbar

Loader

Pagination

Components should be generic whenever practical.

---

# contexts/

Purpose

Global React Contexts.

Examples

AuthContext

ThemeContext

SettingsContext

Do not place page-specific state here.

---

# hooks/

Purpose

Reusable React hooks.

Examples

useAuth

useStudents

useAttendance

usePagination

useTheme

Hooks should encapsulate reusable logic.

---

# layouts/

Purpose

Application layouts.

Examples

DashboardLayout

AuthLayout

Layouts define page structure.

Layouts should not implement business logic.

---

# pages/

Purpose

Route-level components.

Examples

Login

Dashboard

Students

Attendance

Marks

Assignments

Reports

Pages coordinate API calls and compose reusable components.

---

# routes/

Purpose

Application routing.

Responsibilities

- Public routes
- Protected routes
- Role-based routes

Navigation should remain centralized.

---

# services/

Purpose

Frontend API communication.

Responsibilities

- Axios instance
- API requests
- Authentication headers
- Error interception

All backend communication passes through this folder.

---

# styles/

Purpose

Global styling.

Contains

- Theme styles
- Variables
- Layout styles
- Global CSS

Maintain a consistent design language.

---

# utils/

Purpose

Reusable frontend helper functions.

Examples

Date formatting

Input formatting

Local storage helpers

General utility functions

---

# App.jsx

Purpose

Application root.

Responsibilities

- Route rendering
- Global providers
- Layout initialization

Business logic should remain elsewhere.

---

# main.jsx

Purpose

Application entry point.

Responsibilities

- React initialization
- Context providers
- Router initialization

---

# Documentation Folder

```
docs/
```

Purpose

Project documentation.

Contains

- Architecture documentation
- API documentation
- Reports
- Development notes

Documentation should remain separate from source code.

---

# Configuration Files

Repository-level configuration files should remain lightweight.

Examples

README.md

Purpose

Project overview.

Installation instructions.

Usage guide.

Architecture summary.

---

.gitignore

Purpose

Ignore

- Dependencies
- Build artifacts
- Virtual environments
- Cache
- Secrets
- Local configuration

---

# Folder Responsibility Rules

Each folder owns one responsibility.

Examples

Models

↓

Database representation

Schemas

↓

Validation

Routers

↓

HTTP

Services

↓

Business Logic

Components

↓

UI

Pages

↓

Application Screens

Layouts

↓

Structure

Contexts

↓

Global State

Hooks

↓

Reusable Logic

Services

↓

API Communication

Never mix these responsibilities.

---

# Folder Interaction Rules

Allowed

Pages

↓

Components

↓

API Services

↓

Backend

Backend

Routers

↓

Services

↓

Models

↓

Database

Not Allowed

Components

↓

Database

Models

↓

Routers

Pages

↓

Database

Services

↓

React Components

Maintain strict architectural boundaries.

---

# Folder Structure Summary

The repository structure has been intentionally designed to separate concerns across the application.

Every folder has a clearly defined responsibility.

The implementation should preserve this structure exactly while placing every new class, function, and module into its appropriate location.

No architectural restructuring should occur during implementation.

End of Project Folder Structure.