# 64_CODING_STANDARDS.md

# EduTrack Pro — Coding Standards Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Coding Standards

---

# Purpose

This document establishes the official coding standards for the EduTrack Pro project.

Its objective is to ensure that every line of code written throughout the project remains

- Consistent
- Readable
- Maintainable
- Testable
- Scalable
- Professional

Every contributor must follow these standards.

---

# Engineering Philosophy

Code is read far more often than it is written.

Prioritize

- Readability
- Simplicity
- Consistency
- Explicitness

Avoid writing code that is merely clever.

Write code that another developer can understand in six months.

---

# General Principles

Every piece of code should satisfy

✓ Readability

✓ Maintainability

✓ Predictability

✓ Reusability

✓ Simplicity

✓ Performance

---

# SOLID Principles

The project should follow SOLID principles.

---

## Single Responsibility Principle

Every

```
Function

Class

Component

Service

Module
```

should have one responsibility.

---

## Open / Closed Principle

Code should be

```
Open for Extension

Closed for Modification
```

Prefer extension over rewriting.

---

## Liskov Substitution Principle

Derived classes should behave correctly when substituted for base classes.

---

## Interface Segregation Principle

Avoid creating overly large interfaces.

Keep APIs focused.

---

## Dependency Inversion Principle

Depend on abstractions.

Avoid tight coupling.

---

# DRY Principle

```
Don't Repeat Yourself
```

Avoid duplicated

- Logic
- Queries
- Components
- Validation
- Styles

If code is repeated more than twice,

extract it.

---

# KISS Principle

```
Keep It Simple
```

Always choose the simpler solution when both satisfy requirements.

---

# YAGNI Principle

```
You Aren't Gonna Need It
```

Do not implement speculative features.

Build only what is required for the current version.

---

# Naming Conventions

Names should clearly communicate intent.

Good names eliminate the need for comments.

---

# Variable Naming

Use

```
camelCase
```

Examples

```
studentName

averageMarks

attendancePercentage

currentUser
```

Avoid

```
x

temp

abc

data1

obj
```

---

# Python Variables

Use

```
snake_case
```

Examples

```
student_name

average_marks

attendance_percentage

current_user
```

---

# Constants

Use

```
UPPER_SNAKE_CASE
```

Examples

```
MAX_MARKS

DEFAULT_PAGE_SIZE

JWT_EXPIRATION

API_VERSION
```

---

# Class Naming

Use

```
PascalCase
```

Examples

```
StudentService

AttendanceRouter

DashboardLayout

UserResponse
```

---

# Function Naming

Python

```
snake_case
```

Example

```
calculate_average()

create_student()

mark_attendance()
```

JavaScript

```
camelCase
```

Example

```
calculateAverage()

createStudent()

markAttendance()
```

Functions should describe actions.

---

# Boolean Naming

Boolean variables should answer a question.

Examples

```
isActive

hasPermission

canEdit

isAuthenticated

hasAttendance
```

Avoid

```
status

flag

check
```

---

# File Naming

Python

```
snake_case.py
```

React Components

```
PascalCase.jsx
```

JavaScript Utilities

```
camelCase.js
```

---

# Folder Naming

Use

```
lowercase
```

Examples

```
components

services

utils

models

routers
```

Avoid spaces.

---

# Function Length

Target

```
20–40 Lines
```

Maximum

```
60 Lines
```

If longer,

split into smaller functions.

---

# Class Length

Target

```
<300 Lines
```

If larger,

consider splitting responsibilities.

---

# Component Length

Preferred

```
<200 Lines
```

Maximum

```
300 Lines
```

Large components should be decomposed.

---

# File Length

Preferred

```
<400 Lines
```

Absolute Maximum

```
600 Lines
```

Large files should be split.

---

# Nesting

Maximum nesting depth

```
3 Levels
```

Avoid deeply nested

```
if

for

while

try
```

Prefer early returns.

---

# Comments

Write comments to explain

```
Why
```

not

```
What
```

Good code should explain itself.

---

# TODO Comments

Allowed format

```
TODO:

FIXME:

NOTE:
```

Avoid vague TODOs.

---

# Docstrings

Every public function should include

```
Purpose

Parameters

Returns

Raises
```

Python format

```
Google Style
```

preferred.

---

# React Components

Each component should

- Receive props
- Render UI
- Avoid business logic
- Be reusable
- Be testable

---

# Hooks

Custom hooks should begin with

```
use
```

Examples

```
useAuth()

useTheme()

useApi()
```

---

# Imports

Order imports as follows.

Python

```
Standard Library

↓

Third-party Libraries

↓

Internal Modules
```

JavaScript

```
React

↓

Libraries

↓

Components

↓

Hooks

↓

Services

↓

Utilities

↓

Styles
```

One blank line between groups.

---

# Magic Numbers

Avoid

```
75

100

42
```

Use constants instead.

Example

```
MINIMUM_ATTENDANCE_PERCENTAGE
```

---

# Error Handling

Never ignore exceptions.

Never write

```
except:
    pass
```

Always handle or re-raise exceptions.

---

# Logging

Log

- Important events
- Errors
- Warnings

Do not log

- Passwords
- Tokens
- Sensitive information

---

# Code Duplication

Avoid duplicate

- Queries
- Components
- Validation
- Styles
- Utilities

Extract common functionality.

---

# State Management

Keep state

- Minimal
- Local when possible
- Global only when necessary

Avoid unnecessary Context values.

---

# API Calls

All API requests must go through

```
services/
```

Never call Axios directly inside components.

---

# Styling

Use

```
Tailwind CSS
```

Avoid inline styles unless absolutely necessary.

Avoid duplicated utility classes.

---

# Responsiveness

Every page must support

- Desktop
- Tablet
- Mobile

No fixed-width layouts.

---

# Accessibility

Every interactive element must support

- Keyboard navigation
- Focus state
- Screen readers

Use semantic HTML.

---

# Performance

Avoid

- Unnecessary renders
- Large components
- Expensive calculations during rendering

Memoize only when beneficial.

---

# Git Standards

Every commit should represent one logical change.

Avoid giant commits.

Commit messages should be meaningful.

Examples

```
feat: add attendance dashboard

fix: resolve login validation

refactor: simplify student service
```

---

# Formatting

Python

```
Black
```

JavaScript

```
Prettier
```

Linting

```
ESLint
```

Never manually fight formatting tools.

---

# Testing Expectations

Every new feature should include

✓ Unit tests (where applicable)

✓ Manual verification

✓ No lint errors

✓ No console errors

---

# Security Standards

Never

- Hardcode secrets
- Commit `.env`
- Expose passwords
- Trust frontend validation

Always validate on the backend.

---

# Pull Request Checklist

Every PR should

✓ Compile successfully

✓ Pass linting

✓ Pass tests

✓ Follow naming conventions

✓ Remove debug code

✓ Remove unused imports

✓ Update documentation if needed

---

# Code Review Guidelines

Reviewers should check

✓ Readability

✓ Correctness

✓ Architecture

✓ Security

✓ Performance

✓ Testing

✓ Naming

✓ Documentation

Do not approve code that violates these standards.

---

# Anti-Patterns

Avoid

```
God Classes

God Components

Long Functions

Circular Imports

Deep Nesting

Hardcoded Values

Business Logic in UI

Business Logic in Routers

Duplicated Code

Silent Exceptions

Unused Variables
```

---

# Future Compatibility

Coding standards should remain valid as the project grows to support

- PostgreSQL
- Docker
- Redis
- Background Workers
- AI Features
- Mobile Applications
- Multi-Tenant Deployments

without requiring major rewrites.

---

# Coding Standards Checklist

Every contribution should

✓ Follow naming conventions.

✓ Be readable.

✓ Be modular.

✓ Be testable.

✓ Avoid duplication.

✓ Respect architecture.

✓ Pass linting.

✓ Follow formatting rules.

---

# Definition of Completion

Coding Standards are successfully adopted when

✓ All contributors follow them.

✓ Codebase remains consistent.

✓ Reviews become easier.

✓ Technical debt remains low.

✓ New developers can onboard quickly.

---

# Summary

The EduTrack Pro Coding Standards establish a consistent engineering culture across the entire project.

By enforcing clear naming conventions, clean architecture, modular design, proper formatting, security practices, and maintainability principles, the codebase remains professional, scalable, and easy to understand, providing a strong foundation for long-term development and collaboration.

End of Coding Standards Specification.