# 61_FILE_RESPONSIBILITIES_UTILS.md

# EduTrack Pro — Utility File Responsibilities Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Utility File Responsibilities

---

# Purpose

This document defines the responsibility of every utility file inside EduTrack Pro.

Utilities are reusable helper functions that simplify common programming tasks throughout the application.

Utilities should remain completely independent of business logic.

They exist to eliminate duplicated code.

---

# Utility Philosophy

Utilities answer one question:

> "Can this piece of code be reused anywhere without knowing anything about the business domain?"

If the answer is yes,

it belongs inside

```
utils/
```

Otherwise,

it belongs elsewhere.

---

# Folder Structure

Backend

```
backend/

app/

utils/

│

├── __init__.py

├── constants.py

├── date_utils.py

├── validators.py

├── pagination.py

├── formatters.py

├── response.py

├── helpers.py

├── file_utils.py

└── logger.py
```

Frontend

```
frontend/

src/

utils/

│

├── constants.js

├── formatters.js

├── validators.js

├── storage.js

├── helpers.js

├── dateUtils.js

└── apiHelpers.js
```

Utilities remain framework-independent whenever possible.

---

# Responsibilities

Utilities may

✓ Format values

✓ Convert data

✓ Validate generic input

✓ Generate reusable helpers

✓ Build reusable responses

✓ Handle pagination

✓ Manipulate dates

Utilities should NEVER

✗ Query the database

✗ Call APIs directly

✗ Implement business rules

✗ Authenticate users

✗ Access React State

✗ Access FastAPI Request objects

---

# constants.py

Purpose

Application-wide constants.

Contains

```
Roles

Attendance Status

Assignment Status

Submission Status

Risk Levels

Pagination Defaults

Date Formats

API Version

Default Limits
```

Never hardcode these values elsewhere.

---

# date_utils.py

Purpose

Date helper functions.

Examples

```
Current Date

Current Time

Parse Date

Format Date

Days Between

Weeks Between

Months Between

Start of Semester

End of Semester
```

Should never know about students or attendance.

---

# validators.py

Purpose

Reusable validation helpers.

Examples

```
Email Validation

Phone Validation

Password Strength

Roll Number Format

String Length

Positive Numbers
```

Business validation belongs in services.

---

# pagination.py

Purpose

Reusable pagination utilities.

Functions

```
paginate()

calculate_offset()

calculate_total_pages()

build_pagination_response()
```

Shared across every list endpoint.

---

# formatters.py

Purpose

Formatting helpers.

Examples

```
Currency

Percentage

Grade Display

Date Formatting

Time Formatting

Name Formatting

Title Case

Initials
```

No database access.

---

# response.py

Purpose

Standardized API responses.

Examples

```
Success Response

Error Response

Created Response

Deleted Response

Pagination Response
```

Ensures every endpoint follows one response format.

---

# helpers.py

Purpose

General-purpose helper functions.

Examples

```
Generate UUID

Random String

Slug Generator

Safe Dictionary Access

Deep Copy Helpers

Boolean Conversion
```

Avoid placing unrelated helpers here.

Split into dedicated files if they grow.

---

# file_utils.py

Purpose

File-related helpers.

Future responsibilities

```
PDF Helpers

CSV Export

Excel Export

File Validation

Temporary File Cleanup
```

Not required for MVP but reserved.

---

# logger.py

Purpose

Reusable logging helpers.

Functions

```
info()

warning()

error()

debug()

critical()
```

Should wrap the configured logging system.

---

# storage.js

Frontend utility.

Purpose

Browser storage helpers.

Functions

```
Save Token

Load Token

Remove Token

Save Theme

Load Theme

Clear Storage
```

Should hide direct

```
localStorage
```

usage.

---

# apiHelpers.js

Frontend utility.

Purpose

Generic API helpers.

Examples

```
Build Query Parameters

Handle Pagination

Normalize Errors

Extract Messages
```

Avoid Axios calls here.

---

# constants.js

Frontend constants.

Contains

```
Routes

Roles

Theme Names

Chart Colors

Page Sizes

Toast Durations
```

---

# dateUtils.js

Frontend date helpers.

Examples

```
Display Date

Relative Time

Academic Year

Time Ago

Deadline Countdown
```

Should match backend formatting where possible.

---

# formatters.js

Frontend formatting.

Examples

```
Attendance %

Grade

Performance Score

Names

Numbers

Phone Numbers
```

Display only.

No calculations.

---

# validators.js

Frontend validation.

Examples

```
Required Fields

Email

Phone

Password

Length

Regular Expressions
```

Frontend validation improves UX.

Backend validation remains authoritative.

---

# helpers.js

Frontend generic helpers.

Examples

```
Class Name Merge

Debounce

Throttle

Array Helpers

Object Helpers

Search Utilities
```

---

# Utility Design Rules

Utilities should

Be

```
Pure Functions
```

Meaning

```
Same Input

↓

Same Output
```

Avoid hidden side effects.

---

# Reusability

Every utility should be reusable across multiple modules.

If a function is used only once,

it probably does not belong in

```
utils/
```

---

# Dependency Rules

Utilities may depend on

```
Standard Library

Small Helper Libraries
```

Utilities should never depend on

```
Database

Routers

Services

React Components
```

---

# Naming Convention

Functions

```
camelCase
```

Examples

```
formatDate()

validateEmail()

paginate()

saveToken()
```

Files

```
snake_case (Python)

camelCase (JavaScript)
```

---

# Error Handling

Utilities should raise

Meaningful exceptions.

Never silently fail.

Example

```
Invalid Date

Invalid Email

Invalid UUID
```

---

# Logging

Utilities generally should not perform logging.

Logging belongs in

```
Services

Middleware
```

except

```
logger.py
```

---

# Performance

Utility functions should

Be lightweight.

Avoid unnecessary allocations.

Avoid repeated conversions.

Remain deterministic.

---

# Testing

Every utility should have unit tests.

Examples

✓ Date formatting

✓ Pagination

✓ Validators

✓ Response builders

✓ Storage helpers

✓ Number formatting

✓ Error formatting

---

# Documentation

Every exported function should include

```
Purpose

Parameters

Return Type

Examples
```

Keep documentation concise.

---

# Import Rules

Allowed

```
Services

Routers

Frontend Components

Hooks
```

↓

Import

```
Utilities
```

Not Allowed

```
Utilities

↓

Services
```

Not Allowed

```
Utilities

↓

Database
```

Not Allowed

```
Utilities

↓

Frontend Components
```

Utilities remain at the bottom of the dependency graph.

---

# Future Compatibility

Utility architecture should support

```
Internationalization

Localization

Timezone Conversion

Currency Formatting

File Compression

Encryption Helpers

AI Formatting Utilities
```

without restructuring existing files.

---

# Utility Checklist

Every utility should

✓ Be reusable.

✓ Be pure.

✓ Be independently testable.

✓ Avoid business logic.

✓ Avoid framework dependencies.

✓ Have descriptive names.

✓ Have documentation.

---

# Definition of Completion

Utility File Responsibilities are complete when

✓ Reusable helpers centralized.

✓ Constants centralized.

✓ Formatting isolated.

✓ Validation isolated.

✓ Pagination standardized.

✓ Utilities remain framework-independent.

✓ Tests pass.

---

# Summary

The Utility File Responsibilities specification defines the reusable helper layer of EduTrack Pro.

By centralizing formatting, validation, pagination, constants, storage, and general-purpose helper functions into dedicated utility modules, the application minimizes code duplication, improves maintainability, and establishes a clean foundation that supports long-term scalability while keeping business logic isolated within the Service Layer.

End of Utility File Responsibilities Specification.