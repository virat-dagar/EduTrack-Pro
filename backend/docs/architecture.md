# EduTrack Pro Architecture

EduTrack Pro follows the frozen specification architecture:

```text
React Frontend
Axios API Services
FastAPI Routers
Service Layer
SQLAlchemy Models
SQLite Database
```

Routers handle HTTP concerns only. Services contain business logic, validation beyond schemas, database operations, analytics, dashboard aggregation, and report generation. Models define tables and relationships. Schemas validate requests and serialize responses.

The frontend uses React Router protected routes, centralized API services, auth/theme/sidebar context, reusable components, and responsive dashboard layouts.
