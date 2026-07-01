# 00_README_FIRST.md

# EduTrack Pro — Codex Input Package

**Version:** 1.0  
**Status:** Final (Architecture Frozen)  
**Project:** EduTrack Pro  
**Authors:** Virat & Harmeet  
**Primary Implementation Target:** OpenAI Codex  
**Purpose:** Complete implementation package for generating the EduTrack Pro codebase.

---

# Read This First

This directory contains the complete implementation specification for **EduTrack Pro**.

These documents are **not documentation for developers**.

They are implementation instructions intended for an AI software engineering model (Codex) to build the project exactly as specified.

The Software Design Document (SDD) has already finalized the architecture. The purpose of this package is to eliminate ambiguity during implementation.

This package acts as the **single source of implementation truth**.

---

# Primary Goal

Implement a production-quality Academic Performance Analytics Platform called **EduTrack Pro**.

The application should feel like a real SaaS product rather than a college assignment.

Every feature described throughout this package must be implemented completely.

The final application should be suitable for:

- Portfolio
- Resume
- Final Year Project
- Live Demonstration
- GitHub Repository

---

# Attached Files

The Codex session will receive:

- This implementation package
- EduTrack Pro Software Design Document (SDD)
- Existing project ZIP containing the folder structure

The existing folder structure must be respected.

The architecture has already been finalized.

---

# Architecture Freeze

The architecture is frozen.

Do NOT:

- Rename folders
- Rename files
- Introduce new architectural layers
- Replace libraries
- Move responsibilities between modules
- Restructure the project

Only implement the existing architecture.

If additional helper functions are required, place them inside the appropriate existing folders.

---

# Existing Folder Structure

The supplied ZIP already contains the project structure.

Implementation should happen inside the existing files and folders.

Do not redesign the repository.

---

# Source of Truth Priority

If multiple files appear to describe similar functionality, follow this priority order.

Priority 1

This implementation package.

Priority 2

Software Design Document (SDD).

Priority 3

Existing project structure.

Never invent functionality that conflicts with these documents.

---

# Implementation Philosophy

The project should prioritize:

- Readability
- Maintainability
- Scalability
- Modularity
- Separation of Concerns
- Clean Architecture
- Production-quality code

Avoid shortcuts.

Avoid placeholder implementations.

Avoid unfinished modules.

---

# Expected Quality

Every implemented feature should be complete.

Every endpoint should function.

Every frontend page should communicate with the backend.

Every CRUD operation should work.

Authentication should be fully functional.

Dashboard statistics should be calculated correctly.

Analytics should produce deterministic results.

Reports should work.

Forms should validate correctly.

Errors should be handled gracefully.

---

# No Placeholder Code

Avoid:

```python
pass

# TODO

raise NotImplementedError
```

Avoid incomplete implementations.

Every function should perform its intended responsibility.

---

# Backend Expectations

Backend implementation must include:

- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication
- bcrypt password hashing
- Alembic migrations
- SQLite database
- RESTful APIs
- Role-Based Access Control
- Business logic
- Validation
- Exception handling
- Documentation
- Logging

---

# Frontend Expectations

Frontend implementation must include:

- React
- Vite
- React Router
- Axios
- CSS
- Recharts
- Responsive Design

Every page should connect to live backend APIs.

Avoid hardcoded demo data except where explicitly required.

---

# Database Expectations

Database must include all entities described within the Software Design Document.

Relationships must be properly implemented.

Foreign keys must be enforced.

Constraints must be respected.

Indexes should be added where appropriate.

---

# Coding Standards

The project should look like it was written by experienced software engineers.

Requirements include:

- Clean naming
- Small reusable functions
- Modular architecture
- Minimal duplication
- Consistent formatting
- Proper comments
- Type hints where appropriate
- Meaningful variable names

---

# Error Handling

Handle expected failures gracefully.

Examples include:

- Invalid credentials
- Missing resources
- Duplicate records
- Invalid input
- Unauthorized access
- Forbidden actions
- Database failures

Never expose internal stack traces to users.

---

# Security

Authentication must follow JWT.

Passwords must always be hashed.

Never store plaintext passwords.

Protect every required endpoint.

Students must never access another student's data.

Teachers should only perform authorized actions.

---

# Performance

Avoid unnecessary database queries.

Avoid duplicated API calls.

Reuse frontend components.

Reuse backend services.

Maintain responsive performance.

---

# UI Quality

The interface should feel modern.

Use the provided light and dark theme references.

Maintain visual consistency across all pages.

Use reusable layouts and reusable components.

Responsive behaviour is mandatory.

---

# Documentation

Code should remain understandable.

Public functions should include concise docstrings where appropriate.

Complex business rules should be documented with comments explaining *why*, not *what*.

---

# Testing

Every implemented module should be testable.

Backend APIs should work correctly through Swagger UI.

Frontend should integrate successfully with backend APIs.

Critical functionality should not remain untested.

---

# Definition of Completion

The project is complete only when:

- Backend is fully implemented.
- Frontend is fully implemented.
- APIs are connected.
- Authentication works.
- CRUD operations work.
- Dashboards work.
- Analytics work.
- Reports work.
- Validation works.
- Error handling works.
- Responsive layouts work.
- Documentation is consistent.
- Application can be demonstrated without missing functionality.

---

# Reading Order

Codex should process these implementation files in numerical order.

Example:

00_README_FIRST.md

↓

01_CODEX_MASTER_PROMPT.md

↓

02_MASTER_ENGINEERING_SPEC.md

↓

...

↓

Final Checklist

Do not skip files.

Every subsequent document expands upon this introduction.

---

# Final Instruction

Implement EduTrack Pro exactly as described throughout this implementation package.

The objective is not merely to generate code.

The objective is to produce a complete, professional, production-quality Academic Performance Analytics Platform while preserving the frozen architecture and maintaining consistency across the entire codebase.