# 06_PROJECT_ARCHITECTURE.md

# EduTrack Pro — Project Architecture

Version: 1.0

Status: Final

Architecture Status: Frozen

---

# Purpose

This document defines the complete software architecture of EduTrack Pro.

The architecture has already been finalized during the design phase and **must not be modified during implementation**.

Every module, file, API, database model, frontend page, and service must follow this architecture exactly.

If implementation decisions are required, they should preserve the existing architecture instead of introducing new patterns.

---

# Architectural Philosophy

EduTrack Pro follows a modular layered architecture.

Each layer has one responsibility.

Each layer communicates only with adjacent layers.

Responsibilities are never mixed.

The architecture prioritizes

- Readability
- Maintainability
- Scalability
- Testability
- Separation of Concerns

---

# High-Level System Architecture

```text
                        User
                         │
                         ▼
               React Frontend (Vite)
                         │
                         ▼
                  Axios API Services
                         │
                         ▼
                FastAPI REST Endpoints
                         │
                         ▼
                 Business Service Layer
                         │
                         ▼
             SQLAlchemy Database Models
                         │
                         ▼
                    SQLite Database
```

Every request should follow this path.

No layer should bypass another.

---

# Backend Architecture

The backend follows a layered architecture.

```text
Client Request
      │
      ▼
 FastAPI Router
      │
      ▼
 Business Service
      │
      ▼
 SQLAlchemy Model
      │
      ▼
 SQLite Database
      │
      ▼
 Service
      │
      ▼
 Router
      │
      ▼
 JSON Response
```

---

## Backend Layer Responsibilities

### Router Layer

Responsible for

- Receiving requests
- Dependency injection
- Authentication dependencies
- Authorization dependencies
- Calling services
- Returning HTTP responses

Routers must **not**

- Calculate grades
- Query database directly
- Perform analytics
- Contain business rules

---

### Service Layer

Responsible for

- Business logic
- Validation beyond schema validation
- Database operations
- Calculations
- Analytics
- Rule enforcement

Everything intelligent belongs here.

Examples

Attendance %

CGPA

Scholarship

Prediction

Risk Detection

Filtering

Searching

Sorting

---

### Model Layer

Responsible only for database representation.

Models define

- Tables
- Columns
- Relationships
- Constraints
- Indexes

Models do not

- Validate requests
- Calculate business rules
- Return HTTP responses

---

### Schema Layer

Responsible for

- Input validation
- Output serialization

Schemas define

- Request Models

- Response Models

- Update Models

- Create Models

Schemas never access databases.

Schemas never contain business logic.

---

### Database Layer

Responsible only for persistent storage.

Database responsibilities

- Store information
- Maintain relationships
- Enforce constraints

Database should never contain application logic.

---

# Frontend Architecture

Frontend follows component-driven architecture.

```text
React App

│

├── Layouts

├── Pages

├── Components

├── Hooks

├── Context

├── Services

└── Assets
```

Every folder has one responsibility.

---

# Frontend Layer Responsibilities

## Layouts

Provide page structure.

Examples

Dashboard Layout

Authentication Layout

Layouts contain

Sidebar

Navbar

Content Area

Footer

Layouts should never fetch business data.

---

## Pages

Pages coordinate functionality.

Responsibilities

- Fetch data
- Manage page state
- Connect components
- Handle page events

Pages should remain lightweight.

Business calculations belong in backend.

---

## Components

Components display information.

Examples

Cards

Tables

Forms

Charts

Buttons

Inputs

Dialogs

Components should be reusable.

---

## Hooks

Hooks manage reusable logic.

Examples

Authentication

API Requests

Pagination

Search

Theme

Avoid duplicated React logic.

---

## Context

Context stores application-wide state.

Examples

Authentication

Current User

Theme

Application Settings

Do not place page-specific state inside Context.

---

## Services

Services communicate with backend APIs.

Every HTTP request should pass through services.

Pages should never call Axios directly.

---

# Authentication Flow

```text
User Login

↓

React Login Page

↓

Axios

↓

POST /login

↓

Authentication Service

↓

Password Verification

↓

JWT Token

↓

Frontend Storage

↓

Protected Routes

↓

Authenticated Requests
```

Authentication should remain centralized.

---

# Authorization Flow

```text
JWT Token

↓

Authentication Dependency

↓

Current User

↓

Role Verification

↓

Endpoint Access
```

Every protected endpoint must verify user permissions.

---

# Data Flow

Standard request flow

```text
User

↓

React Component

↓

React Page

↓

API Service

↓

Axios

↓

FastAPI Router

↓

Business Service

↓

SQLAlchemy

↓

SQLite

↓

Business Service

↓

Router

↓

JSON

↓

Frontend

↓

UI Update
```

Maintain this flow consistently.

---

# Module Architecture

Each feature follows identical structure.

```text
Feature

│

├── Model

├── Schema

├── Service

├── Router

├── Frontend Service

├── Components

└── Page
```

Every module should be self-contained.

---

# Core Modules

Authentication

User Management

Student Management

Subject Management

Attendance

Marks

Assignments

Submissions

Dashboard

Analytics

Reports

Each module communicates through services.

Avoid hidden coupling.

---

# Dependency Rules

Allowed

Router

↓

Service

↓

Model

Allowed

Page

↓

API Service

↓

Backend

Not Allowed

Router

↓

Router

Model

↓

Router

Component

↓

Database

Service

↓

React Component

Backend

↓

Frontend

Maintain strict dependency direction.

---

# Communication Principles

Modules should interact through clearly defined interfaces.

Examples

Attendance uses Student information.

Marks use Subject information.

Dashboard consumes Attendance.

Reports consume Analytics.

Modules should never directly manipulate another module's internal implementation.

---

# Folder Ownership

Every folder has one purpose.

Backend

core

Application configuration.

database

Database connection.

models

SQLAlchemy models.

schemas

Pydantic schemas.

routers

REST endpoints.

services

Business logic.

utils

Reusable utilities.

exceptions

Custom exceptions.

Frontend

layouts

Application layouts.

pages

Route pages.

components

Reusable UI.

hooks

Reusable React logic.

services

Axios communication.

contexts

Global state.

assets

Images and icons.

styles

Global styling.

---

# Error Handling Flow

```text
Exception

↓

Service

↓

Custom Exception

↓

Global Exception Handler

↓

JSON Response

↓

Frontend

↓

Toast / UI Feedback
```

Every error should follow this flow.

---

# Analytics Architecture

Analytics remain read-only.

```text
Attendance

Marks

Assignments

↓

Analytics Service

↓

Calculated Results

↓

Dashboard

↓

Reports
```

Analytics never modify stored records.

---

# Dashboard Architecture

Teacher Dashboard

Consumes

Students

Attendance

Marks

Assignments

Analytics

Reports

Student Dashboard

Consumes

Personal Attendance

Personal Marks

Assignments

Scholarship

Prediction

Both dashboards are consumers of data.

They should never implement business calculations.

---

# Future Scalability

The architecture should support future expansion without restructuring.

Potential additions

- PostgreSQL
- Redis
- Docker
- Notifications
- Email
- AI Analytics
- Mobile App
- Parent Portal
- Admin Portal

Future features should integrate naturally into the existing architecture.

---

# Architectural Constraints

Do not

- Change folder structure
- Rename files
- Merge modules
- Duplicate business logic
- Bypass service layer
- Place business logic inside React
- Place calculations inside routers

Every implementation must respect the frozen architecture.

---

# Architecture Summary

EduTrack Pro follows a modular, layered architecture that separates presentation, communication, business logic, and persistence into distinct layers.

This architecture ensures

- Maintainability
- Scalability
- Testability
- Security
- Consistency

Every subsequent implementation document assumes this architecture as the foundation.

End of Project Architecture.