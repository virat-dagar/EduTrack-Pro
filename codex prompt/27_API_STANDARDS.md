# 27_API_STANDARDS.md

# EduTrack Pro — API Standards Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: API Standards

---

# Purpose

This document defines the global REST API standards for EduTrack Pro.

Every API endpoint in the backend must follow these standards to ensure consistency, maintainability, predictability, and ease of frontend integration.

These rules apply to every router, endpoint, request, and response in the project.

No module should define its own API conventions.

---

# API Philosophy

EduTrack Pro follows a

```
RESTful API Architecture
```

Every endpoint should be

- Predictable
- Stateless
- Resource-oriented
- Consistent
- Version-ready
- Easy to document
- Easy to consume

---

# API Base URL

Development

```
http://localhost:8000/api/v1
```

Future Production

```
https://domain.com/api/v1
```

Every API should be versioned.

---

# URL Naming Rules

Use

- lowercase
- plural resource names
- hyphens only when required
- nouns instead of verbs

Good

```
/students

/subjects

/attendance

/marks

/assignments

/submissions
```

Avoid

```
/getStudents

/createStudent

/deleteAttendance

/updateMarks
```

---

# HTTP Methods

GET

Retrieve resources.

POST

Create resources.

PUT

Replace existing resource.

PATCH

Partial update (optional future support).

DELETE

Remove resource.

Use HTTP methods according to REST principles.

---

# CRUD Mapping

| Operation | HTTP Method |
|------------|-------------|
| Create | POST |
| Read | GET |
| Update | PUT |
| Delete | DELETE |

---

# Resource Naming

Collections

```
/students
```

Single Resource

```
/students/{id}
```

Nested Resources

```
/students/{id}/attendance

/students/{id}/marks

/subjects/{id}/assignments
```

---

# API Versioning

Every endpoint should begin with

```
/api/v1/
```

Example

```
GET /api/v1/students

POST /api/v1/auth/login
```

Future versions

```
/api/v2/
```

Versioning should not require restructuring routers.

---

# Request Format

Requests should use

```
JSON
```

Example

```json
{
    "name": "Virat",
    "semester": 5
}
```

Never use XML.

---

# Response Format

Every successful response must follow

```json
{
    "success": true,
    "message": "Student created successfully.",
    "data": {}
}
```

Every response should include

- success
- message
- data

---

# Error Response Format

All errors must follow

```json
{
    "success": false,
    "message": "Validation failed.",
    "errors": [
        {
            "field": "email",
            "message": "Email already exists."
        }
    ]
}
```

Never return inconsistent error structures.

---

# HTTP Status Codes

200

Successful GET

201

Successful Create

204

Successful Delete (optional)

400

Bad Request

401

Unauthorized

403

Forbidden

404

Not Found

409

Conflict

422

Validation Error

500

Internal Server Error

Use status codes consistently.

---

# Pagination

Endpoints returning collections should support

```
?page=1

&page_size=20
```

Example

```
GET /students?page=2&page_size=25
```

Default page size

```
20
```

Maximum page size

```
100
```

---

# Pagination Response

Example

```json
{
    "success": true,
    "message": "",
    "data": {
        "items": [],
        "page": 1,
        "page_size": 20,
        "total_items": 150,
        "total_pages": 8
    }
}
```

---

# Sorting

Support

```
?sort=name

?order=asc
```

Example

```
GET /students?sort=semester&order=desc
```

Allowed

Ascending

Descending

---

# Filtering

Support

```
?semester=5

?department=CSE

?course=BTech
```

Multiple filters should be combinable.

---

# Searching

Support

```
?q=virat
```

Example

```
GET /students?q=john
```

Searching should be

Case insensitive.

Backend-driven.

---

# Date Filtering

Example

```
GET /attendance

?start_date=2026-01-01

&end_date=2026-01-31
```

Dates should use

```
YYYY-MM-DD
```

---

# Request Validation

Every request should pass

Frontend Validation

↓

Pydantic Validation

↓

Business Validation

↓

Database Constraints

Reject invalid requests before reaching the database.

---

# Response Data

Only include fields required by the client.

Avoid exposing

- Password Hash
- JWT Secret
- Internal IDs unnecessarily
- Stack Traces

---

# Endpoint Consistency

Every CRUD module should expose

```
GET

POST

PUT

DELETE
```

where applicable.

Endpoints should follow identical patterns.

---

# Authentication Header

Protected endpoints require

```
Authorization

Bearer <JWT>
```

Missing header

↓

401 Unauthorized

---

# Idempotency

GET

Safe

PUT

Idempotent

DELETE

Idempotent

POST

Not necessarily idempotent

Design endpoints accordingly.

---

# API Documentation

Swagger should include

- Summary
- Description
- Request Schema
- Response Schema
- Authentication
- Status Codes
- Examples

Every endpoint must be documented.

---

# Naming Conventions

Routes

Plural nouns

Variables

snake_case

JSON

camelCase is optional, but project should consistently use one style.

Recommended

snake_case throughout backend.

---

# Time Format

Dates

```
YYYY-MM-DD
```

DateTime

ISO-8601

Example

```
2026-07-01T14:30:00Z
```

---

# Boolean Values

Use

```
true

false
```

Never

```
1

0

Yes

No
```

---

# Numeric Fields

Use proper numeric types.

Examples

```
marks

credits

semester

attendance_percentage
```

Avoid returning numbers as strings.

---

# Null Handling

Optional fields may return

```
null
```

Avoid

```
""

"N/A"
```

Maintain consistent typing.

---

# Bulk Operations

Future compatible

Examples

```
POST /attendance/bulk

POST /marks/bulk

POST /students/import
```

Bulk operations should remain separate from normal CRUD endpoints.

---

# API Performance

Prefer

- Pagination
- Filtering
- Indexed queries
- Aggregated responses

Avoid returning unnecessary data.

---

# Security Standards

Every protected endpoint

Authenticate

↓

Authorize

↓

Validate

↓

Execute

↓

Respond

Never expose sensitive information.

---

# Logging

Log

- Requests
- Authentication failures
- Authorization failures
- Unexpected exceptions

Do not log

- Passwords
- Tokens
- Secrets

---

# API Testing

Every endpoint should be tested for

✓ Success

✓ Validation

✓ Authentication

✓ Authorization

✓ Invalid Input

✓ Missing Resource

✓ Edge Cases

✓ Unexpected Errors

---

# Future Compatibility

API architecture should support

- GraphQL
- WebSockets
- Mobile Clients
- Third-party Integrations
- Public APIs
- Rate Limiting
- API Keys

without redesigning the current REST architecture.

---

# API Checklist

Every endpoint should satisfy

✓ RESTful

✓ Versioned

✓ Documented

✓ Authenticated (if required)

✓ Authorized (if required)

✓ Validated

✓ Predictable

✓ Consistent Response

✓ Proper Status Codes

✓ Tested

---

# Definition of Completion

API standards are complete when

✓ Every router follows REST conventions.

✓ Every response follows a common structure.

✓ Every error is standardized.

✓ Pagination implemented.

✓ Filtering implemented.

✓ Searching implemented.

✓ Swagger documentation complete.

✓ Authentication consistent.

✓ Authorization consistent.

✓ All endpoints follow identical conventions.

---

# Summary

The EduTrack Pro API follows a standardized REST architecture with consistent routing, request validation, response formatting, authentication, authorization, pagination, filtering, and documentation.

Following these standards ensures seamless frontend integration, maintainable backend development, and a professional, production-ready API.

End of API Standards Specification.