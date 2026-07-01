# 56_FILE_RESPONSIBILITIES_DATABASE.md

# EduTrack Pro — Database File Responsibilities Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Database File Responsibilities

---

# Purpose

This document defines the responsibility of every file inside the database layer of EduTrack Pro.

The database layer is responsible only for

- Database Connection
- ORM Base
- Session Management
- Database Initialization
- Migrations Support

It must NEVER contain business logic.

---

# Database Philosophy

The database layer exists to provide a reliable interface between the application and SQLite.

Business rules belong inside

```
services/
```

API handling belongs inside

```
routers/
```

Validation belongs inside

```
schemas/
```

---

# Database Folder Structure

```
backend/

app/

database/

│

├── database.py

├── base.py

├── session.py

├── init_db.py

├── seed.py

└── __init__.py
```

Future

```
migrations/

alembic.ini
```

---

# Overall Architecture

```
Router

↓

Service

↓

Database Session

↓

SQLAlchemy ORM

↓

SQLite
```

The database layer never knows about routers or frontend.

---

# database.py

Purpose

Primary database configuration.

Responsibilities

```
Create Engine

Create SessionLocal

Expose Base

Database Dependency

Connection Management
```

Should contain

```
create_engine()

sessionmaker()

Declarative Base
```

Should NEVER contain

Business Logic

Queries

Authentication

Analytics

---

# Example Responsibilities

```
Engine Creation

↓

Session Factory

↓

Dependency Injection
```

Nothing else.

---

# base.py

Purpose

Expose the shared SQLAlchemy Base class.

Responsibilities

```
DeclarativeBase

Model Registration
```

Every model inherits from

```
Base
```

Only.

---

# session.py

Purpose

Database session handling.

Responsibilities

```
Open Session

Yield Session

Close Session
```

Used by

```
FastAPI Depends()
```

No queries.

---

# init_db.py

Purpose

Initialize database.

Responsibilities

```
Create Tables

Verify Tables

Initialize Metadata
```

Executed

```
First Run

Development

Testing
```

Should not seed data.

---

# seed.py

Purpose

Populate development database.

Examples

```
Admin User

Demo Teacher

Demo Student

Subjects

Sample Attendance

Sample Marks

Assignments
```

Never execute automatically in production.

---

# __init__.py

Purpose

Package initialization.

May expose

```
Base

Session

Engine
```

Contains no logic.

---

# Database Dependency Flow

```
FastAPI Route

↓

Depends(get_db)

↓

Database Session

↓

Service Layer

↓

ORM Query
```

---

# Connection Lifecycle

```
Request Starts

↓

Open Session

↓

Execute Queries

↓

Commit / Rollback

↓

Close Session
```

Always close sessions.

---

# Transactions

Every transaction should follow

```
Begin

↓

Execute

↓

Commit

↓

Rollback on Error
```

Never leave transactions open.

---

# Commit Rules

Commit only after

Successful validation.

Successful service execution.

Successful database operation.

Rollback immediately on exception.

---

# Session Ownership

Only the request should own the session.

Do not create global sessions.

Do not share sessions across requests.

---

# Database Configuration

Read from

```
.env
```

Example

```
DATABASE_URL

DEBUG

ECHO_SQL
```

Never hardcode database paths.

---

# SQLite Support

MVP

```
SQLite
```

Future compatibility

```
PostgreSQL

MySQL

MariaDB
```

No code changes outside configuration.

---

# Engine Configuration

Recommended

```
Future=True

Pool Pre Ping

Echo=False

Connect Args
```

SQLite should support

```
check_same_thread=False
```

---

# Metadata

Managed automatically.

Models register themselves through inheritance.

No manual table registration.

---

# ORM Usage

Always use

```
SQLAlchemy ORM
```

Avoid raw SQL unless absolutely necessary.

---

# Query Responsibility

Database layer

Does NOT

know

Students

Marks

Attendance

Assignments

Only

Tables

Sessions

Connections

---

# Migration Support

Future

```
Alembic
```

Migration scripts belong

Outside

```
database/
```

---

# Performance Guidelines

Reuse

Engine.

Create

Session Per Request.

Avoid reconnecting repeatedly.

---

# Error Handling

Database layer handles

```
Connection Failure

Transaction Failure

Commit Failure
```

Business exceptions handled elsewhere.

---

# Logging

Log

```
Connection Established

Connection Closed

Migration

Critical Database Errors
```

Do not log

Passwords.

Secrets.

JWT.

---

# Testing

Unit tests should verify

✓ Engine Creation

✓ Session Creation

✓ Session Cleanup

✓ Rollback

✓ Commit

✓ Initialization

✓ Seed Script

---

# File Dependency Rules

Allowed

```
database.py

↓

session.py

↓

service.py
```

Not Allowed

```
database.py

↓

router.py
```

Not Allowed

```
database.py

↓

frontend
```

---

# Future Compatibility

Database layer should support

```
Connection Pooling

Read Replicas

Redis Cache

Cloud SQL

Docker

Kubernetes

Database Monitoring
```

without redesign.

---

# Database File Checklist

Every database file should

✓ Have one responsibility.

✓ Avoid business logic.

✓ Be reusable.

✓ Be independently testable.

✓ Support dependency injection.

✓ Remain database-agnostic where possible.

---

# Definition of Completion

Database File Responsibilities are complete when

✓ Connection management isolated.

✓ Sessions isolated.

✓ Initialization isolated.

✓ Seed scripts isolated.

✓ Migration compatibility maintained.

✓ Clean separation enforced.

---

# Summary

The Database File Responsibilities specification defines a clean and modular persistence layer for EduTrack Pro.

By separating engine creation, session management, initialization, and development seeding into dedicated files, the application maintains a robust, scalable, and maintainable database architecture that supports future database upgrades with minimal effort.

End of Database File Responsibilities Specification.