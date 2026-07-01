# 55_FILE_RESPONSIBILITIES_CORE.md

# EduTrack Pro — Core File Responsibilities Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Core File Responsibilities

---

# Purpose

This document defines the responsibility of every core file inside the EduTrack Pro project.

Every file must have one clearly defined responsibility.

No file should become a "God File" containing unrelated logic.

This follows the

```
Single Responsibility Principle (SRP)
```

---

# Core Philosophy

Every file should answer one question:

> "Why does this file exist?"

If multiple unrelated answers exist,

the file should be split.

---

# Project Root

```
edutrack-pro/

│

├── frontend/

├── backend/

├── docs/

├── README.md

├── .gitignore

└── docker-compose.yml (Future)
```

---

# README.md

Purpose

Project documentation.

Contains

```
Project Overview

Features

Installation

Setup

Tech Stack

Folder Structure

Screenshots

Contributors

License
```

Should never contain

Implementation code.

---

# .gitignore

Purpose

Ignore unnecessary files.

Should ignore

```
node_modules/

venv/

.env

__pycache__/

.pytest_cache/

dist/

build/

coverage/

.idea/

.vscode/
```

---

# docs/

Purpose

Project documentation only.

Contains

```
Architecture

API Documentation

ER Diagrams

Deployment

Reports

Screenshots

Presentation
```

Never contains source code.

---

# Frontend Root

```
frontend/
```

Purpose

Contains the complete React application.

Nothing backend-related belongs here.

---

# Backend Root

```
backend/
```

Purpose

Contains the complete FastAPI application.

Nothing frontend-related belongs here.

---

# frontend/src/

Purpose

Contains all frontend source code.

Only production source code.

No build artifacts.

---

# backend/app/

Purpose

Contains all backend application code.

No scripts.

No temporary files.

---

# main.py

Location

```
backend/app/main.py
```

Purpose

Application entry point.

Responsibilities

```
Create FastAPI App

Register Routers

Register Middleware

Register Exception Handlers

Register CORS

Startup Events

Shutdown Events
```

Must NOT contain

Business Logic.

Database Queries.

Authentication Logic.

Analytics.

---

# config.py

Location

```
backend/app/config.py
```

Purpose

Application configuration.

Stores

```
Environment Variables

JWT Settings

Database URL

Secret Keys

Application Settings
```

Never hardcode values.

---

# database.py

Location

```
backend/app/database/database.py
```

Purpose

Create database engine.

Create session factory.

Provide database dependency.

Responsibilities

```
Engine

SessionLocal

Base

Database Dependency
```

Should never contain models.

---

# dependencies.py

Purpose

Shared FastAPI dependencies.

Examples

```
Current User

Current Teacher

Current Student

Database Session
```

Avoid duplicate dependency functions.

---

# constants.py

Purpose

Application-wide constants.

Examples

```
User Roles

Attendance Status

Assignment Status

Default Pagination

API Version
```

Avoid hardcoded values.

---

# settings.py

Purpose

Central configuration object.

Responsible for

```
Loading .env

Validation

Default Values
```

Should use

```
Pydantic Settings
```

---

# logger.py

Purpose

Central logging configuration.

Responsible for

```
Console Logging

File Logging

Log Formatting

Log Levels
```

Never print directly in production code.

---

# security.py

Purpose

Security helper functions.

Examples

```
Password Hashing

Password Verification

JWT Generation

JWT Verification

Token Utilities
```

No routing logic.

---

# exceptions.py

Purpose

Custom exception classes.

Examples

```
StudentNotFound

Unauthorized

Forbidden

AssignmentNotFound

ValidationError
```

Avoid generic exceptions.

---

# responses.py

Purpose

Reusable API response builders.

Examples

```
Success Response

Error Response

Pagination Response
```

Keeps response format consistent.

---

# middleware.py

Purpose

Application middleware.

Examples

```
Request Logging

CORS

Performance Metrics

Future Rate Limiting
```

Business logic should never exist here.

---

# startup.py

Purpose

Application startup tasks.

Examples

```
Database Check

Seed Admin User

Load Config

Health Check
```

---

# shutdown.py

Purpose

Cleanup tasks.

Examples

```
Close Connections

Cleanup Resources

Flush Logs
```

---

# health.py

Purpose

Health check endpoints.

Example

```
GET /health
```

Returns

```
Application Status

Database Status

Version
```

---

# utils/

Purpose

Reusable helper functions.

Examples

```
Date Formatting

Pagination

Validation Helpers

String Helpers

General Utilities
```

Utilities should remain pure functions.

---

# assets/

Frontend only.

Stores

```
Images

Icons

Logos

Illustrations

SVG Files
```

No JavaScript.

---

# public/

Purpose

Static frontend files.

Examples

```
favicon

manifest

robots.txt
```

---

# package.json

Purpose

Frontend dependency management.

Contains

```
Dependencies

Scripts

Project Metadata
```

Should not contain secrets.

---

# requirements.txt

Purpose

Backend dependency management.

Contains

```
FastAPI

SQLAlchemy

Pydantic

JWT

Passlib

Uvicorn

Alembic
```

Only production dependencies.

---

# .env

Purpose

Environment configuration.

Contains

```
Database URL

JWT Secret

API URL

Debug Mode
```

Must NEVER be committed.

---

# .env.example

Purpose

Template for developers.

Contains

Placeholder values only.

Safe to commit.

---

# vite.config.js

Purpose

Frontend build configuration.

Responsibilities

```
Aliases

Plugins

Development Server

Environment Loading
```

---

# tailwind.config.js

Purpose

Tailwind customization.

Contains

```
Colors

Fonts

Spacing

Animations

Theme Tokens
```

No application logic.

---

# postcss.config.js

Purpose

PostCSS plugins.

Normally

```
Tailwind

Autoprefixer
```

---

# eslint.config.js

Purpose

Code quality rules.

Ensures

```
Consistent Style

Best Practices

No Unused Variables

Import Rules
```

---

# prettier.config.js (Future)

Purpose

Automatic code formatting.

Ensures

Consistent formatting.

---

# Root Responsibilities Summary

| File | Responsibility |
|------|----------------|
| README.md | Project documentation |
| .gitignore | Ignore unnecessary files |
| .env | Environment variables |
| .env.example | Environment template |
| main.py | FastAPI entry point |
| config.py | Configuration |
| settings.py | Environment loader |
| database.py | Database connection |
| dependencies.py | Shared dependencies |
| constants.py | Global constants |
| logger.py | Logging |
| security.py | Security helpers |
| middleware.py | Middleware |
| exceptions.py | Custom exceptions |
| responses.py | API responses |
| startup.py | Startup tasks |
| shutdown.py | Cleanup tasks |
| health.py | Health endpoint |

---

# File Dependency Rules

Allowed

```
Router

↓

Service

↓

Database
```

Allowed

```
Component

↓

Service

↓

API
```

Not Allowed

```
Router

↓

Router
```

Not Allowed

```
Service

↓

Router
```

Not Allowed

```
Component

↓

Database
```

---

# Import Rules

Imports should always flow downward.

```
Configuration

↓

Utilities

↓

Database

↓

Services

↓

Routers

↓

Application
```

Avoid circular imports.

---

# Future Compatibility

Core architecture should support

```
Docker

Redis

Celery

Microservices

WebSockets

Cloud Storage

CI/CD

Monitoring
```

without restructuring the project.

---

# Testing

Verify

✓ Every file has one responsibility.

✓ No circular imports.

✓ No duplicated utilities.

✓ No duplicated configuration.

✓ Clear separation of concerns.

✓ Minimal coupling.

---

# Core File Responsibility Checklist

Every core file should

✓ Have one purpose.

✓ Be easy to locate.

✓ Be independently testable.

✓ Avoid business logic unless intended.

✓ Follow clean architecture.

✓ Remain reusable.

---

# Definition of Completion

Core File Responsibilities are complete when

✓ Every root/core file has a clearly defined responsibility.

✓ Project entry points are separated.

✓ Configuration is centralized.

✓ Utilities are reusable.

✓ Architecture remains scalable.

---

# Summary

The Core File Responsibilities specification establishes the foundational responsibilities of the project's infrastructure files.

By clearly defining the purpose of every core file and enforcing strict separation of concerns, EduTrack Pro maintains a clean, maintainable, and production-ready architecture that can scale without accumulating technical debt.

End of Core File Responsibilities Specification.