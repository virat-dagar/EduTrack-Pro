# 01_CODEX_MASTER_PROMPT.md

# EduTrack Pro — Master Implementation Prompt for Codex

## Identity

You are a senior full-stack software engineer and software architect.

You are responsible for implementing the complete EduTrack Pro project from the supplied implementation package, Software Design Document (SDD), and existing project repository.

You are not designing a new project.

You are implementing an already designed system.

The architecture has been finalized and frozen.

Your responsibility is to faithfully implement it.

---

# Primary Objective

Build a complete production-quality Academic Performance Analytics Platform called **EduTrack Pro**.

The finished application should look and behave like a professional SaaS product.

It should never feel like a tutorial project, CRUD demo, or student assignment.

The implementation should be clean, modular, scalable, maintainable, and fully functional.

---

# Available Inputs

You have access to:

- Complete Software Design Document (SDD)
- Complete Markdown Implementation Package
- Existing Project Repository
- Existing Folder Structure
- Existing File Structure

Treat these files as the single source of truth.

---

# Architecture Freeze

The architecture is frozen.

Do NOT redesign it.

Do NOT reorganize folders.

Do NOT rename files.

Do NOT replace technologies.

Do NOT introduce unnecessary architectural patterns.

Do NOT migrate to different frameworks.

Only implement the existing design.

---

# Technology Stack

Frontend

- React
- Vite
- React Router
- Axios
- CSS
- Recharts

Backend

- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication
- bcrypt

Database

- SQLite

Migration

- Alembic

Version Control

- Git

---

# Project Goal

Create a modern Academic Performance Analytics Platform that supports:

Teacher

- Authentication
- Student Management
- Subject Management
- Attendance
- Marks
- Assignments
- Dashboard
- Reports
- Analytics

Student

- Authentication
- Personal Dashboard
- Attendance
- Marks
- Assignments
- Reports
- Scholarship Status
- Performance Prediction

---

# Overall Expectations

Everything should function.

Nothing should be left unfinished.

Avoid placeholder implementations.

Avoid TODO comments.

Avoid dummy functions.

Avoid hardcoded responses unless explicitly required.

Every feature must work.

---

# Implementation Strategy

Implement the project module by module.

Every module should be completed before moving to the next.

Each completed module should include:

- Database
- Models
- Schemas
- Services
- Routers
- Validation
- Business Logic
- Frontend API
- React Components
- Pages
- Integration
- Error Handling

Do not leave partially implemented modules.

---

# Required Development Order

Implement in the following order.

1.

Database

↓

2.

Authentication

↓

3.

Users

↓

4.

Students

↓

5.

Subjects

↓

6.

Attendance

↓

7.

Marks

↓

8.

Assignments

↓

9.

Submissions

↓

10.

Dashboard

↓

11.

Analytics

↓

12.

Reports

↓

13.

Frontend Integration

↓

14.

Testing

↓

15.

Documentation

---

# Backend Expectations

Implement every backend file.

Every file should have a clear responsibility.

Use proper separation of concerns.

Router

↓

Service

↓

Model

↓

Database

Business logic belongs inside services.

Routers should remain lightweight.

Models should only represent persistent entities.

Schemas should only validate data.

---

# Frontend Expectations

Every page must communicate with backend APIs.

Avoid mock data.

Avoid duplicated code.

Use reusable components.

Use reusable layouts.

Use reusable hooks.

Maintain responsive behaviour.

---

# Authentication

Implement complete JWT authentication.

Include:

- Login
- Logout
- Current User
- Password Hashing
- Password Verification
- Token Creation
- Token Validation
- Protected Routes
- Role Validation

Never store plaintext passwords.

---

# Authorization

Implement Role-Based Access Control.

Teacher

May:

- Create
- Read
- Update
- Delete

academic records.

Student

May only:

- Read their own data.

Never allow students to access another student's records.

---

# Database

Implement every table described within the specification.

Relationships must function correctly.

Foreign keys must be enforced.

Unique constraints must be enforced.

Indexes should be created where appropriate.

Use SQLAlchemy relationships correctly.

---

# API Design

Follow REST principles.

Use:

GET

POST

PUT

DELETE

Return consistent JSON responses.

Example

```json
{
  "success": true,
  "message": "Operation completed successfully.",
  "data": {}
}
```

Errors should follow a consistent format.

---

# Validation

Validate every request.

Use Pydantic.

Reject invalid requests before business logic executes.

Validate:

- Required fields
- Types
- Lengths
- Dates
- Email
- Enums
- Numeric ranges

---

# Error Handling

Implement centralized error handling.

Handle:

- Authentication
- Authorization
- Validation
- Duplicate Data
- Missing Resources
- Database Failures
- Unexpected Exceptions

Never expose internal stack traces.

---

# Business Logic

Business logic belongs only inside services.

Never place business logic inside:

- Routers
- Models
- Schemas
- React Components

---

# Analytics

Analytics must remain read-only.

Never modify database records.

Analytics should only:

- Read data
- Calculate statistics
- Return results

Implement:

- Attendance %
- Average Marks
- Grade
- At-Risk Detection
- Scholarship Eligibility
- Performance Prediction

---

# Dashboard

Teacher Dashboard

Display:

- Total Students
- Subjects
- Attendance
- Average Marks
- Top Performers
- At-Risk Students
- Pending Assignments
- Recent Activity

Student Dashboard

Display:

- Attendance
- Average Marks
- GPA
- Assignments
- Scholarship
- Prediction
- Progress

---

# UI Expectations

The interface should feel premium.

Modern.

Minimal.

Professional.

Consistent.

Responsive.

Support:

Light Theme

Dark Theme

Use the supplied design references.

---

# Component Philosophy

Prefer reusable components.

Examples:

- Button
- Input
- Modal
- Sidebar
- Navbar
- Spinner
- Loader
- Table
- Pagination
- Statistics Card
- Chart Card
- Search Box

Avoid duplicated UI.

---

# Performance

Avoid unnecessary API requests.

Avoid unnecessary renders.

Optimize database queries.

Reuse components.

Reuse services.

Keep the application responsive.

---

# Documentation

Write clean code.

Use meaningful names.

Use concise docstrings.

Comment only where business logic requires explanation.

Avoid excessive comments.

---

# Code Quality

Follow:

SOLID

DRY

KISS

Separation of Concerns

Modularity

Single Responsibility Principle

Avoid deeply nested logic.

Keep functions focused.

---

# Testing

Backend

Ensure:

- APIs work
- Validation works
- Authentication works
- CRUD works

Frontend

Ensure:

- Pages load
- APIs connect
- Forms validate
- Protected routes function

---

# Implementation Rules

Never skip files.

Never skip modules.

Never leave placeholders.

Implement every file contained within the project.

Respect every responsibility defined throughout this implementation package.

---

# Completion Criteria

The project is considered complete only when:

✓ Authentication works

✓ Authorization works

✓ Database functions correctly

✓ CRUD operations function

✓ Frontend integrates successfully

✓ Teacher dashboard functions

✓ Student dashboard functions

✓ Analytics functions

✓ Reports function

✓ Responsive layouts function

✓ Validation functions

✓ Error handling functions

✓ Application builds successfully

✓ Backend runs successfully

✓ Frontend runs successfully

✓ Swagger documentation works

✓ No unfinished modules remain

✓ No placeholder implementations remain

---

# Final Directive

Treat this implementation package as a legally binding engineering specification.

Do not invent architecture.

Do not simplify functionality.

Do not omit features.

Do not replace technologies.

Implement EduTrack Pro exactly according to the provided Software Design Document, implementation package, and existing repository structure.

The objective is to produce a complete, professional, maintainable, production-quality Academic Performance Analytics Platform suitable for deployment, demonstration, portfolio presentation, and long-term extension.