# EduTrack Pro Project Explanation

This document explains the current EduTrack Pro implementation as a full-stack project. It covers how the backend, frontend, database, authentication, services, routing, setup scripts, and development workflow fit together.

The project is expected to change over time, so treat this file as a current snapshot of the working implementation rather than a permanent product specification.

## 1. Project Summary

EduTrack Pro is an academic management application for tracking students, subjects, attendance, marks, assignments, submissions, dashboards, and reports.

The application has two main parts:

- `backend/`: FastAPI API server with SQLAlchemy models, service-layer business logic, SQLite persistence, Alembic migrations, JWT authentication, and tests.
- `frontend/`: React + Vite single page app with protected routes, dashboards, CRUD pages, API services, reusable UI components, and responsive styling.

The main runtime flow is:

```text
Browser
  -> React routes and pages
  -> Frontend service modules
  -> Axios API client
  -> FastAPI routers
  -> Backend services
  -> SQLAlchemy models
  -> SQLite database
```

## 2. Root-Level Structure

```text
EduTrack_Pro/
  backend/                 FastAPI backend application
  frontend/                React frontend application
  docs/                    Project-level documentation
  setup/                   Shared setup scripts
  codex prompt/            Original engineering specification files
  setup.sh                 Root setup menu
  run_demo.sh              One-command local demo runner
  README.md                Short project setup overview
```

Important root-level scripts:

- `./run_demo.sh`: prepares demo data and starts both backend and frontend.
- `./setup.sh`: opens a setup menu for backend, frontend, or complete project setup.

## 3. How To Run The Project

### Recommended Demo Run

From the project root:

```bash
./run_demo.sh
```

The script:

- Finds the project root automatically.
- Uses the backend virtual environment from `backend/.venv` or `backend/venv`.
- Installs missing backend or frontend dependencies when needed.
- Creates `backend/.env` from `backend/.env.example` if needed.
- Seeds demo data through `backend/app/database/seed.py`.
- Starts the backend on `http://127.0.0.1:8000`.
- Starts the frontend on `http://127.0.0.1:5173`.
- Stops both servers when you press `Ctrl+C`.

Demo accounts:

```text
teacher@example.com / Password123
student@example.com / Password123
```

Useful URLs:

```text
Frontend:     http://127.0.0.1:5173
Backend docs: http://127.0.0.1:8000/docs
Health:       http://127.0.0.1:8000/health
```

### Manual Backend Run

```bash
cd backend
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Seed demo data:

```bash
cd backend
.venv/bin/python -m app.database.seed
```

### Manual Frontend Run

```bash
cd frontend
npm run dev
```

## 4. Environment Configuration

### Backend Environment

Backend settings are loaded in `backend/app/core/config.py`.

Supported variables:

| Variable | Purpose | Default |
| --- | --- | --- |
| `DATABASE_URL` | SQLAlchemy database URL | `sqlite:///./edutrack_pro.db` |
| `SECRET_KEY` | JWT signing secret | Local development secret |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `ALGORITHM` | Fallback JWT algorithm name | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT lifetime | `1440` |
| `CORS_ORIGINS` | Allowed frontend origins | `http://localhost:5173,http://127.0.0.1:5173` |
| `BACKEND_CORS_ORIGINS` | Alternate CORS variable | Same as above |

### Frontend Environment

The frontend API client reads:

| Variable | Purpose | Default |
| --- | --- | --- |
| `VITE_API_BASE_URL` | Backend API base URL | `http://localhost:8000/api/v1` |

The demo runner sets `VITE_API_BASE_URL` automatically to match the backend host and port.

### Demo Runner Environment

`run_demo.sh` supports these optional variables:

| Variable | Purpose | Default |
| --- | --- | --- |
| `BACKEND_HOST` | Backend bind host | `127.0.0.1` |
| `BACKEND_PORT` | Backend port | `8000` |
| `FRONTEND_HOST` | Frontend bind host | `127.0.0.1` |
| `FRONTEND_PORT` | Frontend port | `5173` |
| `SKIP_SETUP` | Skip dependency setup checks | `0` |

Example:

```bash
BACKEND_PORT=8010 FRONTEND_PORT=5174 ./run_demo.sh
```

## 5. Backend Architecture

The backend follows a layered FastAPI architecture:

```text
FastAPI app
  -> Routers
  -> Services
  -> SQLAlchemy models
  -> Database session
  -> SQLite database
```

Layer responsibilities:

- `main.py`: creates the FastAPI app, configures CORS, registers exception handlers, includes routers, and initializes the database on startup.
- `routers/`: owns HTTP paths, dependency injection, status codes, request schemas, and response wrapping.
- `services/`: owns business rules, database queries, cross-entity validation, analytics, reports, and dashboard aggregation.
- `schemas/`: owns Pydantic request and response schemas.
- `models/`: owns SQLAlchemy table definitions and relationships.
- `database/`: owns engine, sessions, metadata import, initialization, and demo seed data.
- `core/`: owns runtime settings, authentication helpers, password hashing, JWT helpers, logging, and dependencies.
- `exceptions/`: owns custom exceptions and global exception handlers.
- `utils/`: owns constants, validators, response helpers, and small shared helpers.

## 6. Backend Folder Details

```text
backend/
  app/
    core/
      config.py            Environment-backed settings
      dependencies.py      Auth and role dependencies
      logging.py           Logging setup
      security.py          Password hashing and JWT helpers
    database/
      base.py              Base metadata and model import helper
      database.py          SQLAlchemy engine and session factory
      init_db.py           Database table creation
      seed.py              Demo accounts and demo academic records
      session.py           FastAPI database session dependency
    exceptions/
      custom_exceptions.py Domain exception classes
      handlers.py          FastAPI exception handler registration
    models/
      user.py
      student.py
      subject.py
      attendance.py
      marks.py
      assignment.py
      submission.py
    routers/
      auth.py
      users.py
      students.py
      subjects.py
      attendance.py
      marks.py
      assignments.py
      submissions.py
      dashboard.py
      reports.py
    schemas/
      auth.py
      user.py
      student.py
      subject.py
      attendance.py
      marks.py
      assignment.py
      submission.py
      dashboard.py
      report.py
      common.py
    services/
      auth_service.py
      user_service.py
      student_service.py
      subject_service.py
      attendance_service.py
      marks_service.py
      assignment_service.py
      submission_service.py
      analytics_service.py
      dashboard_service.py
      report_service.py
    utils/
      constants.py
      helpers.py
      response.py
      validators.py
    main.py
  alembic/
    env.py
    versions/
  docs/
    api.md
    architecture.md
    database.md
    deployment.md
  tests/
  requirements.txt
  requirements-dev.txt
  alembic.ini
```

## 7. Backend Startup Flow

When `app.main:app` is loaded:

1. Settings are loaded from environment variables.
2. Logging is configured.
3. FastAPI app metadata is created.
4. CORS middleware is registered.
5. Global exception handlers are registered.
6. All API routers are included.
7. The lifespan startup calls `create_database()`.
8. Health endpoints are available at `/health` and `/api/v1/health`.

## 8. Authentication And Authorization

Authentication is JWT-based.

Main files:

- `backend/app/core/security.py`
- `backend/app/core/dependencies.py`
- `backend/app/services/auth_service.py`
- `backend/app/routers/auth.py`

Login flow:

1. Frontend submits email and password to `POST /api/v1/auth/login`.
2. `auth_service.py` validates the user and password.
3. Backend returns a JWT access token and user information.
4. Frontend stores the token in local storage.
5. Axios attaches `Authorization: Bearer <token>` to protected requests.
6. Backend dependencies decode the token and load the current user.

Roles:

- `teacher`: can manage institutional data such as students, subjects, attendance, marks, assignments, submissions, reports, and teacher dashboards.
- `student`: can access student-facing dashboards and their own academic records.

Important auth dependencies:

- `get_current_user`
- `require_teacher`
- `require_student`
- `ensure_teacher_or_owner`

## 9. API Response And Error Shape

Successful backend responses use a consistent wrapper:

```json
{
  "success": true,
  "message": "Readable message",
  "data": {}
}
```

Errors are normalized by global exception handlers. Custom domain exceptions include:

- `AuthenticationError`
- `AuthorizationError`
- `NotFoundError`
- `ConflictError`
- `BusinessRuleError`

Validation, SQLAlchemy, and unexpected exceptions are also handled centrally.

## 10. Database And Data Model

The current local database is SQLite. SQLAlchemy is used for ORM models and sessions. Alembic is configured for migrations.

Database URL default:

```text
sqlite:///./edutrack_pro.db
```

### Tables

#### users

Stores application accounts.

Important fields:

- `id`
- `full_name`
- `email`
- `password_hash`
- `role`
- `is_active`
- `created_at`
- `updated_at`

Relationships:

- One user can have one student profile.
- Teacher users can mark attendance, enter marks, create assignments, and review submissions.

#### students

Stores academic student profiles.

Important fields:

- `id`
- `user_id`
- `roll_number`
- `enrollment_number`
- `first_name`
- `last_name`
- `date_of_birth`
- `gender`
- `email`
- `phone`
- `course`
- `department`
- `semester`
- `section`
- `academic_year`
- `admission_date`
- `profile_photo`
- `is_active`
- `created_at`
- `updated_at`

Relationships:

- Belongs to one user.
- Has attendance records.
- Has marks records.
- Has assignment submissions.

#### subjects

Stores subjects offered by the institution.

Important fields:

- `id`
- `subject_code`
- `subject_name`
- `course`
- `department`
- `semester`
- `credits`
- `description`
- `is_active`
- `created_at`
- `updated_at`

Relationships:

- Has attendance records.
- Has marks records.
- Has assignments.

#### attendance

Stores attendance entries per student, subject, and date.

Important fields:

- `id`
- `student_id`
- `subject_id`
- `attendance_date`
- `status`
- `remarks`
- `marked_by`
- `created_at`
- `updated_at`

Relationships:

- Belongs to a student.
- Belongs to a subject.
- Is marked by a teacher user.

#### marks

Stores assessment marks.

Important fields:

- `id`
- `student_id`
- `subject_id`
- `assessment_type`
- `marks_obtained`
- `maximum_marks`
- `examination_date`
- `remarks`
- `entered_by`
- `created_at`
- `updated_at`

Relationships:

- Belongs to a student.
- Belongs to a subject.
- Is entered by a teacher user.

#### assignments

Stores assignment definitions.

Important fields:

- `id`
- `subject_id`
- `title`
- `description`
- `total_marks`
- `assigned_date`
- `due_date`
- `created_by`
- `is_active`
- `created_at`
- `updated_at`

Relationships:

- Belongs to a subject.
- Is created by a teacher user.
- Has submissions.

#### submissions

Stores student assignment submissions and review metadata.

Important fields:

- `id`
- `assignment_id`
- `student_id`
- `submission_date`
- `status`
- `submission_notes`
- `attachment_path`
- `reviewed_by`
- `reviewed_at`
- `feedback`
- `created_at`
- `updated_at`

Relationships:

- Belongs to an assignment.
- Belongs to a student.
- May be reviewed by a teacher user.

## 11. Backend API Map

Base URL:

```text
http://127.0.0.1:8000/api/v1
```

### Authentication

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/auth/login` | Login and receive JWT token |
| `GET` | `/auth/me` | Get current authenticated user |

### Users

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/users` | List users |
| `POST` | `/users` | Create user |
| `GET` | `/users/{user_id}` | Get user |
| `PUT` | `/users/{user_id}` | Update user |
| `DELETE` | `/users/{user_id}` | Delete user |
| `PUT` | `/users/{user_id}/activate` | Activate user |
| `PUT` | `/users/{user_id}/deactivate` | Deactivate user |

### Students

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/students` | List students |
| `GET` | `/students/me` | Current student's profile |
| `GET` | `/students/search` | Search students |
| `POST` | `/students` | Create student |
| `GET` | `/students/{student_id}` | Get student |
| `PUT` | `/students/{student_id}` | Update student |
| `DELETE` | `/students/{student_id}` | Delete student |

### Subjects

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/subjects` | List subjects |
| `GET` | `/subjects/search` | Search subjects |
| `GET` | `/subjects/course/{course}` | Subjects by course |
| `GET` | `/subjects/semester/{semester}` | Subjects by semester |
| `POST` | `/subjects` | Create subject |
| `GET` | `/subjects/{subject_id}` | Get subject |
| `PUT` | `/subjects/{subject_id}` | Update subject |
| `DELETE` | `/subjects/{subject_id}` | Delete subject |

### Attendance

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/attendance` | List attendance |
| `GET` | `/attendance/summary` | Attendance summary |
| `GET` | `/attendance/percentage/{student_id}` | Student attendance percentage |
| `GET` | `/attendance/student/{student_id}` | Student attendance records |
| `GET` | `/attendance/subject/{subject_id}` | Subject attendance records |
| `POST` | `/attendance` | Mark attendance |
| `GET` | `/attendance/{attendance_id}` | Get attendance record |
| `PUT` | `/attendance/{attendance_id}` | Update attendance record |
| `DELETE` | `/attendance/{attendance_id}` | Delete attendance record |

### Marks

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/marks` | List marks |
| `GET` | `/marks/summary` | Marks summary |
| `GET` | `/marks/average/{student_id}` | Student marks average |
| `GET` | `/marks/student/{student_id}` | Student marks records |
| `GET` | `/marks/subject/{subject_id}` | Subject marks records |
| `POST` | `/marks` | Add marks |
| `GET` | `/marks/{marks_id}` | Get marks record |
| `PUT` | `/marks/{marks_id}` | Update marks record |
| `DELETE` | `/marks/{marks_id}` | Delete marks record |

### Assignments

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/assignments` | List assignments |
| `GET` | `/assignments/upcoming` | Upcoming assignments |
| `GET` | `/assignments/overdue` | Overdue assignments |
| `GET` | `/assignments/subject/{subject_id}` | Subject assignments |
| `GET` | `/assignments/teacher/{teacher_id}` | Teacher assignments |
| `POST` | `/assignments` | Create assignment |
| `GET` | `/assignments/{assignment_id}` | Get assignment |
| `PUT` | `/assignments/{assignment_id}` | Update assignment |
| `DELETE` | `/assignments/{assignment_id}` | Delete assignment |

### Submissions

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/submissions` | List submissions |
| `GET` | `/submissions/pending` | Pending reviews |
| `GET` | `/submissions/student/{student_id}` | Student submissions |
| `GET` | `/submissions/assignment/{assignment_id}` | Assignment submissions |
| `POST` | `/submissions` | Submit assignment |
| `GET` | `/submissions/{submission_id}` | Get submission |
| `PUT` | `/submissions/{submission_id}` | Update submission |
| `DELETE` | `/submissions/{submission_id}` | Delete submission |
| `PUT` | `/submissions/{submission_id}/review` | Review submission |

### Dashboard

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/dashboard/teacher` | Teacher dashboard summary |
| `GET` | `/dashboard/teacher/charts` | Teacher dashboard chart data |
| `GET` | `/dashboard/teacher/activity` | Teacher recent activity |
| `GET` | `/dashboard/student` | Student dashboard summary |
| `GET` | `/dashboard/student/charts` | Student dashboard chart data |
| `GET` | `/dashboard/student/activity` | Student recent activity |

### Reports

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/reports/student/{student_id}` | Student academic report |
| `GET` | `/reports/attendance` | Attendance report |
| `GET` | `/reports/marks` | Marks report |
| `GET` | `/reports/assignments` | Assignment report |
| `GET` | `/reports/performance` | Performance report |
| `GET` | `/reports/institution` | Institution summary |

## 12. Backend Services

The service layer contains most backend behavior.

| Service | Responsibility |
| --- | --- |
| `auth_service.py` | Login validation, password verification, token generation, current user handling |
| `user_service.py` | User CRUD, active/inactive state management, user lookup |
| `student_service.py` | Student CRUD, search, profile lookup, uniqueness validation |
| `subject_service.py` | Subject CRUD, search, course/semester filters |
| `attendance_service.py` | Attendance CRUD, student/subject filters, summaries, percentages |
| `marks_service.py` | Marks CRUD, student/subject filters, summaries, averages |
| `assignment_service.py` | Assignment CRUD, upcoming/overdue filters, teacher/subject filters |
| `submission_service.py` | Submission CRUD, pending reviews, assignment review workflow |
| `analytics_service.py` | Aggregated calculations used by dashboards and reports |
| `dashboard_service.py` | Teacher and student dashboard summaries, charts, activity |
| `report_service.py` | Student, attendance, marks, assignment, performance, and institution reports |

## 13. Frontend Architecture

The frontend is a React + Vite single page app.

Core frontend flow:

```text
main.jsx
  -> BrowserRouter
  -> ThemeProvider
  -> AuthProvider
  -> SidebarProvider
  -> App
  -> AppRoutes
  -> Layouts
  -> Pages
  -> Service modules
  -> Axios client
```

Frontend responsibilities:

- Routes decide which screen to show.
- Route guards protect authenticated and role-specific pages.
- Context providers store shared UI and auth state.
- Service modules hide raw API calls from pages.
- Reusable components keep forms, cards, tables, layout, feedback, and charts consistent.
- Utility modules handle storage, date formatting, formatting, validation, constants, and helper functions.

## 14. Frontend Folder Details

```text
frontend/
  src/
    assets/
      hero.png
    components/
      charts/
      common/
      dashboard/
      feedback/
      layout/
      tables/
      ui/
    context/
      AuthContext.jsx
      SidebarContext.jsx
      ThemeContext.jsx
      authContext.js
      sidebarContext.js
      themeContext.js
    hooks/
      useApi.js
      useAuth.js
      useDebounce.js
      usePagination.js
      useSidebar.js
      useTheme.js
    layouts/
      AuthLayout.jsx
      BlankLayout.jsx
      DashboardLayout.jsx
    pages/
      assignments/
      attendance/
      auth/
      dashboard/
      errors/
      marks/
      profile/
      reports/
      settings/
      students/
      subjects/
    routes/
      AppRoutes.jsx
      ProtectedRoute.jsx
      PublicRoute.jsx
    services/
      api.js
      assignmentService.js
      attendanceService.js
      authService.js
      dashboardService.js
      marksService.js
      reportService.js
      studentService.js
      subjectService.js
      submissionService.js
      userService.js
    styles/
      animations.css
      globals.css
      theme.css
      variables.css
    utils/
      constants.js
      dateUtils.js
      formatters.js
      helpers.js
      storage.js
      validators.js
    App.jsx
    main.jsx
    index.css
  package.json
  vite.config.js
```

## 15. Frontend Routing

Routing is defined in `frontend/src/routes/AppRoutes.jsx`.

Public routes:

| Path | Page |
| --- | --- |
| `/login` | Login page |
| `/forbidden` | Forbidden page |
| `*` | Not found page |

Protected dashboard routes:

| Path | Access |
| --- | --- |
| `/dashboard/teacher` | Teacher only |
| `/dashboard/student` | Student only |

Student routes:

| Path | Access |
| --- | --- |
| `/students/list` | Teacher only |
| `/students/create` | Teacher only |
| `/students/:id` | Authenticated |
| `/students/edit/:id` | Teacher only |

Subject routes:

| Path | Access |
| --- | --- |
| `/subjects/list` | Authenticated |
| `/subjects/create` | Teacher only |
| `/subjects/:id` | Authenticated |
| `/subjects/edit/:id` | Teacher only |

Attendance routes:

| Path | Access |
| --- | --- |
| `/attendance/list` | Authenticated |
| `/attendance/mark` | Teacher only |
| `/attendance/summary` | Teacher only |
| `/attendance/history` | Authenticated |

Marks routes:

| Path | Access |
| --- | --- |
| `/marks/list` | Authenticated |
| `/marks/create` | Teacher only |
| `/marks/performance` | Authenticated |
| `/marks/edit/:id` | Teacher only |

Assignment routes:

| Path | Access |
| --- | --- |
| `/assignments/list` | Authenticated |
| `/assignments/create` | Teacher only |
| `/assignments/:id` | Authenticated |
| `/assignments/edit/:id` | Teacher only |

Report routes:

| Path | Access |
| --- | --- |
| `/reports/students` | Authenticated |
| `/reports/attendance` | Teacher only |
| `/reports/marks` | Teacher only |
| `/reports/institution` | Teacher only |

Other protected routes:

| Path | Access |
| --- | --- |
| `/profile` | Authenticated |
| `/settings` | Authenticated |

## 16. Frontend State And Context

### Auth Context

Files:

- `frontend/src/context/AuthContext.jsx`
- `frontend/src/context/authContext.js`
- `frontend/src/hooks/useAuth.js`

Responsibilities:

- Stores current user.
- Stores authentication status.
- Logs users in and out.
- Loads the current user from `/auth/me`.
- Redirects unauthorized users.
- Exposes auth actions to pages and route guards.

### Theme Context

Files:

- `frontend/src/context/ThemeContext.jsx`
- `frontend/src/context/themeContext.js`
- `frontend/src/hooks/useTheme.js`

Responsibilities:

- Stores selected theme.
- Allows theme switching.
- Persists theme preference.

### Sidebar Context

Files:

- `frontend/src/context/SidebarContext.jsx`
- `frontend/src/context/sidebarContext.js`
- `frontend/src/hooks/useSidebar.js`

Responsibilities:

- Stores sidebar open/collapsed state.
- Supports dashboard layout behavior on desktop and mobile.

## 17. Frontend API Layer

The Axios instance lives in `frontend/src/services/api.js`.

Responsibilities:

- Reads `VITE_API_BASE_URL`.
- Sets JSON headers.
- Adds `Authorization: Bearer <token>` when a token exists.
- Normalizes successful responses by returning response data.
- Dispatches an app-wide unauthorized event when the backend returns `401`.

Service modules map frontend calls to backend endpoints:

| Service | Backend area |
| --- | --- |
| `authService.js` | `/auth` |
| `userService.js` | `/users` |
| `studentService.js` | `/students` |
| `subjectService.js` | `/subjects` |
| `attendanceService.js` | `/attendance` |
| `marksService.js` | `/marks` |
| `assignmentService.js` | `/assignments` |
| `submissionService.js` | `/submissions` |
| `dashboardService.js` | `/dashboard` |
| `reportService.js` | `/reports` |

## 18. Main User Workflows

### Teacher Login And Dashboard

1. Teacher logs in through `/login`.
2. Frontend stores JWT and user details.
3. Teacher is routed to `/dashboard/teacher`.
4. Dashboard requests summary, chart, and activity data.
5. Teacher can manage students, subjects, attendance, marks, assignments, submissions, and reports.

### Student Login And Dashboard

1. Student logs in through `/login`.
2. Frontend stores JWT and user details.
3. Student is routed to `/dashboard/student`.
4. Student dashboard loads academic summary, chart data, and activity.
5. Student can view permitted records and assignment information.

### Student Management

1. Teacher opens student list.
2. Frontend calls `/students`.
3. Teacher can create, edit, view, search, or delete student profiles.
4. Backend validates uniqueness for account and student identifiers.

### Attendance Management

1. Teacher opens mark attendance page.
2. Frontend loads student and subject options.
3. Teacher submits attendance status and remarks.
4. Backend stores the attendance record with teacher ownership.
5. Summary and percentage endpoints aggregate attendance data.

### Marks Management

1. Teacher creates marks for a student and subject.
2. Backend validates marks against maximum marks.
3. Marks pages and performance screens read summaries and averages.
4. Reports reuse marks aggregations for broader academic reporting.

### Assignment And Submission Management

1. Teacher creates an assignment for a subject.
2. Assignment appears in assignment lists and upcoming/overdue views.
3. Student submits work through the submissions API.
4. Teacher reviews pending submissions and records feedback.

### Reports

Reports use backend aggregation services to expose:

- Student academic report.
- Attendance report.
- Marks report.
- Assignment report.
- Performance report.
- Institution report.

## 19. UI Component System

Common components:

- `Button`
- `Input`
- `Card`
- `Modal`

Layout components:

- `Navbar`
- `Sidebar`
- `PageHeader`

Feedback components:

- `LoadingState`
- `EmptyState`
- `ErrorState`

Data and dashboard components:

- `DataTable`
- `StatCard`
- `ChartCard`
- `Badge`

The styling system is split across:

- `variables.css`: design tokens and CSS variables.
- `theme.css`: theme-specific styles.
- `globals.css`: base layout, typography, form, table, page, and utility styling.
- `animations.css`: transitions and animation helpers.

## 20. Validation And Shared Constants

Backend shared constants live in:

```text
backend/app/utils/constants.py
```

They define supported roles, attendance statuses, assessment types, submission statuses, gender values, and pagination defaults.

Frontend shared constants live in:

```text
frontend/src/utils/constants.js
```

Frontend validators and helpers live in:

```text
frontend/src/utils/validators.js
frontend/src/utils/helpers.js
frontend/src/utils/dateUtils.js
frontend/src/utils/formatters.js
frontend/src/utils/storage.js
```

## 21. Tests And Quality Checks

Backend tests live in `backend/tests/`.

Current backend test areas:

- Authentication
- Users
- Students
- Subjects
- Attendance
- Marks
- Assignments
- Submissions

Useful commands:

```bash
backend/.venv/bin/python -m pytest
```

```bash
cd backend
.venv/bin/python -m ruff check app tests
```

Frontend checks:

```bash
cd frontend
npm run lint
npm run build
```

The project has been verified with:

- Backend tests passing.
- Backend Ruff checks passing.
- Frontend ESLint passing.
- Frontend production build passing.

## 22. Migrations

Alembic is configured in:

```text
backend/alembic.ini
backend/alembic/env.py
backend/alembic/versions/
```

The current project also creates tables on startup through `create_database()`, which is convenient for local development. For stricter production workflows, migrations should be treated as the source of schema changes and run before application startup.

Useful command:

```bash
cd backend
.venv/bin/alembic upgrade head
```

## 23. Demo Data

Demo data is created by:

```text
backend/app/database/seed.py
```

The seed script is idempotent. It creates:

- A demo teacher account.
- A demo student account.
- A student profile.
- A sample subject.
- A sample assignment.

Demo credentials:

```text
teacher@example.com / Password123
student@example.com / Password123
```

## 24. Current Local Development Notes

- The app currently uses SQLite by default.
- The backend API prefix is `/api/v1`.
- The frontend defaults to `http://localhost:8000/api/v1`, while `run_demo.sh` uses `http://127.0.0.1:8000/api/v1`.
- `run_demo.sh` starts Uvicorn without reload so local demo startup does not depend on filesystem watch permissions.
- `backend/.env` is local configuration and should not contain production secrets in source control.
- The frontend `dist/` folder is build output.
- Python cache folders and frontend dependency folders are generated artifacts.

## 25. How To Add A New Feature

For a new backend feature:

1. Add or update SQLAlchemy models if the data model changes.
2. Add or update Alembic migrations.
3. Add or update Pydantic schemas.
4. Add service-layer functions for business behavior.
5. Add router endpoints.
6. Register new routers in `app/main.py` if needed.
7. Add tests in `backend/tests/`.
8. Update frontend services if the feature is exposed to the UI.

For a new frontend feature:

1. Add service functions in `frontend/src/services/`.
2. Add pages under `frontend/src/pages/`.
3. Add routes in `frontend/src/routes/AppRoutes.jsx`.
4. Use existing layouts and shared components.
5. Keep role protection consistent with backend authorization.
6. Add validation helpers only when shared across pages.
7. Run lint and build.

## 26. Important Consistency Rules

When making future changes:

- Keep backend route paths and frontend service paths synchronized.
- Keep backend role checks and frontend route guards aligned.
- Keep schema names, model names, service names, and page names predictable.
- Do not put business logic into routers when it belongs in services.
- Do not call Axios directly from pages when a service module should own that API call.
- Update this document when a major route, table, service, page, or workflow changes.

## 27. Quick Mental Model

If you are trying to understand where something belongs:

- HTTP request handling belongs in `backend/app/routers/`.
- Business logic belongs in `backend/app/services/`.
- Data shape validation belongs in `backend/app/schemas/`.
- Database structure belongs in `backend/app/models/`.
- Shared backend setup belongs in `backend/app/core/`, `backend/app/database/`, `backend/app/utils/`, or `backend/app/exceptions/`.
- Frontend API calls belong in `frontend/src/services/`.
- Frontend screens belong in `frontend/src/pages/`.
- Shared UI belongs in `frontend/src/components/`.
- Shared frontend state belongs in `frontend/src/context/`.
- App navigation belongs in `frontend/src/routes/`.

That is the core shape of EduTrack Pro as it currently stands.

## 28. ERP/LMS Expansion Snapshot

The project has now moved beyond a CRUD-only academic tracker. The current expansion introduces the first ERP/LMS layer:

- Classroom-centered academic organization.
- Automatic student account creation.
- Generated student credentials.
- CSV/Excel student import preview and commit.
- Student export.
- Bulk classroom attendance.
- Attendance analytics and at-risk students.
- Classroom-targeted assignments.
- Assignment file/PDF references.
- Student assignment submissions.
- Teacher submission review.
- Question-wise grading with automatic total, percentage, and grade.

The new model is:

```text
Institution
  -> Department
  -> Course
  -> Semester
  -> Section
  -> Classroom
  -> Students
```

Everything that needs class context can now reference `classroom_id`.

## 29. Classroom Module

Classrooms represent one academic group, such as:

```text
Computer Science / B.Tech / Semester 5 / Section A / 2026-27
```

Backend model:

```text
Classroom
id
classroom_code
classroom_name
department
course
semester
section
academic_year
is_active
created_at
updated_at
```

Create classroom:

```http
POST /api/v1/classrooms
```

Request:

```json
{
  "department": "Computer Science",
  "course": "B.Tech",
  "semester": 5,
  "section": "A",
  "academic_year": "2026-27",
  "classroom_code": "optional",
  "classroom_name": "optional",
  "is_active": true
}
```

If `classroom_code` is not provided, the backend generates one from the academic group.

List classrooms:

```http
GET /api/v1/classrooms
```

Query parameters:

```text
page
page_size
q
department
course
semester
section
academic_year
is_active
sort
order
```

Frontend page:

```text
/classrooms/list
```

## 30. Student Creation And Login Credentials

Student creation no longer requires the teacher to manually create a user first.

Preferred flow:

```text
Teacher enters student academic details
  -> Backend creates User
  -> Backend creates Student
  -> Backend links Student.user_id to User.id
  -> Backend assigns/creates Classroom
  -> Backend returns one-time generated credentials
```

Create student:

```http
POST /api/v1/students
```

Required request fields:

```json
{
  "roll_number": "CSE23001",
  "first_name": "Rahul",
  "last_name": "Sharma",
  "email": "rahul@example.com",
  "course": "B.Tech",
  "department": "Computer Science",
  "semester": 5
}
```

Optional request fields:

```json
{
  "user_id": 12,
  "classroom_id": 4,
  "enrollment_number": "2026CSE001",
  "date_of_birth": "2005-01-01",
  "gender": "Other",
  "phone": "9876543210",
  "section": "A",
  "academic_year": "2026-27",
  "admission_date": "2026-07-01",
  "profile_photo": "/uploads/student.png",
  "is_active": true
}
```

ID behavior:

- `student.id` is generated by the database.
- `user_id` is optional.
- If `user_id` is provided, it must belong to an existing user with role `student`.
- If `user_id` is not provided, the backend creates a new `User` automatically.
- `classroom_id` is optional.
- If `classroom_id` is provided, the student is assigned to that classroom.
- If `classroom_id` is not provided, the backend finds or creates a classroom from `department`, `course`, `semester`, `section`, and `academic_year`.
- `enrollment_number` is optional.
- If `enrollment_number` is missing, the backend generates one from `academic_year` and `roll_number`.

Credential behavior:

- The backend generates a temporary password like `ETP-xxxxxxxxxxxx`.
- The password is stored only as a bcrypt hash in `users.password_hash`.
- The plain password is returned only in the create/import response.
- Teachers must share that temporary password with the student.
- The student logs in with their email and generated password.

Create response includes:

```json
{
  "id": 1,
  "user_id": 2,
  "classroom_id": 4,
  "roll_number": "CSE23001",
  "email": "rahul@example.com",
  "generated_credentials": {
    "user_id": 2,
    "email": "rahul@example.com",
    "password": "ETP-GeneratedPassword"
  }
}
```

Frontend page:

```text
/students/create
```

## 31. Student Bulk Import

Bulk import supports CSV, XLS, and XLSX files.

Expected spreadsheet columns:

```text
Roll No
First Name
Last Name
Email
Course
Department
Semester
Section
```

Optional columns:

```text
Enrollment Number
Phone
Gender
Date of Birth
Academic Year
Admission Date
Classroom ID
```

Preview import:

```http
POST /api/v1/students/import/preview
Content-Type: multipart/form-data
```

Form field:

```text
file = students.csv | students.xlsx
```

Preview response:

```json
{
  "total_rows": 116,
  "valid_rows": 112,
  "invalid_rows": 4,
  "rows": [
    {
      "row_number": 2,
      "data": {},
      "is_valid": true,
      "errors": []
    }
  ]
}
```

Validation catches:

- Duplicate roll number.
- Duplicate email.
- Duplicate enrollment number.
- Invalid email.
- Missing required fields.
- Invalid semester.
- Invalid phone.

Commit import:

```http
POST /api/v1/students/import/commit
```

Request:

```json
{
  "rows": [
    {
      "roll_number": "CSE23001",
      "first_name": "Rahul",
      "last_name": "Sharma",
      "email": "rahul@example.com",
      "course": "B.Tech",
      "department": "Computer Science",
      "semester": 5,
      "section": "A"
    }
  ],
  "import_valid_only": true
}
```

Commit response:

```json
{
  "imported": 112,
  "skipped": 4,
  "items": [
    {
      "student_id": 1,
      "roll_number": "CSE23001",
      "email": "rahul@example.com",
      "generated_credentials": {
        "user_id": 2,
        "email": "rahul@example.com",
        "password": "ETP-GeneratedPassword"
      }
    }
  ],
  "skipped_rows": [
    {
      "row_number": 8,
      "reason": "Duplicate roll number."
    }
  ]
}
```

Export students:

```http
GET /api/v1/students/export
```

Frontend page:

```text
/students/import
```

## 32. Bulk Attendance Workflow

Teachers no longer need to mark one student at a time.

Workflow:

```text
Select Classroom
Select Subject
Select Date
Load Students
Mark Present/Absent/Late in grid
Save Attendance
```

Load classroom sheet:

```http
GET /api/v1/attendance/classroom/{classroom_id}/sheet
```

Query parameters:

```text
subject_id
attendance_date
```

Example:

```http
GET /api/v1/attendance/classroom/4/sheet?subject_id=2&attendance_date=2026-07-01
```

Response:

```json
{
  "classroom": {
    "id": 4,
    "classroom_name": "Computer Science - B.Tech Semester 5 Section A"
  },
  "subject_id": 2,
  "attendance_date": "2026-07-01",
  "students": [
    {
      "student_id": 1,
      "roll_number": "CSE23001",
      "name": "Rahul Sharma",
      "status": "Present",
      "remarks": null,
      "attendance_id": null
    }
  ]
}
```

Save bulk attendance:

```http
POST /api/v1/attendance/bulk
```

Request:

```json
{
  "classroom_id": 4,
  "subject_id": 2,
  "attendance_date": "2026-07-01",
  "records": [
    {
      "student_id": 1,
      "status": "Present",
      "remarks": "On time"
    },
    {
      "student_id": 2,
      "status": "Absent"
    }
  ]
}
```

Response:

```json
{
  "saved": 52,
  "updated": 0,
  "skipped": 0,
  "skipped_rows": []
}
```

Frontend page:

```text
/attendance/mark
```

UI controls:

- Mark All Present.
- Mark All Absent.
- Invert Selection.
- Save Attendance.

## 33. Attendance Analytics

Attendance analytics endpoint:

```http
GET /api/v1/attendance/analytics
```

Query parameters:

```text
classroom_id
subject_id
```

Response:

```json
{
  "total_records": 120,
  "present": 104,
  "absent": 12,
  "late": 4,
  "attendance_percentage": 86.67,
  "subject_wise": [
    {
      "subject_id": 2,
      "subject": "Database Management Systems",
      "attendance_percentage": 82.0,
      "total_records": 50
    }
  ]
}
```

At-risk students:

```http
GET /api/v1/attendance/at-risk
```

Query parameters:

```text
threshold = 75
classroom_id
```

Response:

```json
{
  "threshold": 75,
  "count": 3,
  "items": [
    {
      "student_id": 1,
      "roll_number": "CSE23001",
      "name": "Rahul Sharma",
      "classroom_id": 4,
      "attendance_percentage": 72.5
    }
  ]
}
```

## 34. Assignment LMS Workflow

Assignments now support a publish-submit-grade workflow.

Teacher workflow:

```text
Create Assignment
Select Subject
Select Classroom
Add PDF/File Path
Add Questions and Max Marks
Publish
View Submissions
Grade Question-wise
```

Create assignment:

```http
POST /api/v1/assignments
```

Request:

```json
{
  "classroom_id": 4,
  "subject_id": 2,
  "title": "Math Assignment",
  "description": "Solve all questions.",
  "pdf_file": "/uploads/math-assignment.pdf",
  "assigned_date": "2026-07-01",
  "due_date": "2026-07-20",
  "is_published": true,
  "questions": [
    {
      "question_no": 1,
      "title": "Q1",
      "max_marks": 5
    },
    {
      "question_no": 2,
      "title": "Q2",
      "max_marks": 10
    }
  ]
}
```

Rules:

- `subject_id` is required.
- `classroom_id` is optional but recommended.
- `pdf_file` stores a file path or URL reference.
- `total_marks` may be provided directly.
- If `questions` are provided, the backend calculates `total_marks` from question `max_marks`.
- If neither `total_marks` nor `questions` are provided, the request is rejected.
- `is_published=true` makes it visible to assigned students.

Publish assignment:

```http
PUT /api/v1/assignments/{assignment_id}/publish
```

Submission summary:

```http
GET /api/v1/assignments/{assignment_id}/submissions/summary
```

Response:

```json
{
  "assignment_id": 1,
  "assigned_students": 52,
  "submitted": 45,
  "pending": 7,
  "reviewed": 30
}
```

Frontend pages:

```text
/assignments/create
/assignments/{id}
```

## 35. Student Submission Portal

Student workflow:

```text
Open Assignment
Download/View Assignment File
Choose Solution File
Add Notes
Upload File
Submit Assignment
Track Submission Status
View Grade And Feedback
```

Frontend pages:

```text
/assignments/list
/assignments/{id}
```

Student assignment list behavior:

- Students only see active, published assignments assigned to their classroom.
- Each row shows title, subject, classroom, total marks, due date, personal submission status, and grade when available.
- The action button opens the full LMS assignment page.

Student assignment detail behavior:

- Shows assignment description, subject, classroom, due date, total marks, and questions.
- Shows a download link when `pdf_file` is available.
- Shows the student's current submission status: `Pending`, `Submitted`, `Late`, or `Reviewed`.
- Lets the student upload a solution file directly from the browser.
- Lets the student update their solution before the due date while the submission is not reviewed.
- Shows uploaded file link, grade, percentage, teacher feedback, and question-wise marks after review.

Upload solution file:

```http
POST /api/v1/submissions/upload
Content-Type: multipart/form-data
```

Form field:

```text
file = solution.pdf | solution.docx | solution.png | solution.zip
```

Allowed file extensions:

```text
.pdf
.doc
.docx
.png
.jpg
.jpeg
.zip
```

Default maximum upload size:

```text
10 MB
```

Environment setting:

```text
MAX_UPLOAD_BYTES=10485760
UPLOAD_DIR=uploads
```

Upload response:

```json
{
  "file_name": "solution.pdf",
  "stored_file": "solution-a1b2c3d4e5f6.pdf",
  "file_url": "/uploads/submissions/student_1/solution-a1b2c3d4e5f6.pdf",
  "size_bytes": 2048
}
```

Submit assignment:

```http
POST /api/v1/submissions
```

Request:

```json
{
  "assignment_id": 1,
  "submitted_file": "/uploads/submissions/student_1/solution-a1b2c3d4e5f6.pdf",
  "submission_notes": "Completed all questions."
}
```

Update an existing submission:

```http
PUT /api/v1/submissions/{submission_id}
```

Request:

```json
{
  "submitted_file": "/uploads/submissions/student_1/revised-solution-a1b2c3d4e5f6.pdf",
  "submission_notes": "Uploaded revised answer sheet."
}
```

Get the student's enriched assignment detail:

```http
GET /api/v1/assignments/{assignment_id}
```

Student-specific response fields:

```json
{
  "my_submission_id": 5,
  "submission_status": "Submitted",
  "submission_file": "/uploads/submissions/student_1/solution-a1b2c3d4e5f6.pdf",
  "submission_grade": null,
  "submission_percentage": null,
  "submission_feedback": null
}
```

Get full submission detail:

```http
GET /api/v1/submissions/{submission_id}
```

After review, response includes:

```json
{
  "status": "Reviewed",
  "total_marks": 12,
  "percentage": 80,
  "grade": "A",
  "feedback": "Strong work.",
  "question_grades": []
}
```

Rules:

- Only students can submit.
- Only students can upload submission files through `/submissions/upload`.
- The assignment must be active and published.
- If the assignment has a `classroom_id`, the student must belong to that classroom.
- A student can submit an assignment only once.
- A submitted assignment can be updated before the due date while it is not reviewed.
- Reviewed submissions cannot be updated by students.
- Submission status is `Submitted` or `Late` depending on the due date.
- Uploaded files are stored under the configured upload directory and served from `/uploads/...`.

## 36. Question-Wise Grading

Teacher grading workflow:

```text
Open Assignment
Open Student Submission
Enter obtained marks per question
Save Grade
Backend calculates total, percentage, and grade
```

Review submission:

```http
PUT /api/v1/submissions/{submission_id}/review
```

Request:

```json
{
  "status": "Reviewed",
  "feedback": "Good work.",
  "question_scores": [
    {
      "question_id": 10,
      "obtained_marks": 4,
      "feedback": "Correct method."
    },
    {
      "question_id": 11,
      "obtained_marks": 8
    }
  ]
}
```

Backend calculation:

```text
total_marks = sum(obtained_marks)
percentage = total_marks / sum(question.max_marks) * 100
grade =
  A+ when percentage >= 90
  A  when percentage >= 80
  B  when percentage >= 70
  C  when percentage >= 60
  D  when percentage >= 50
  F  otherwise
```

Response includes:

```json
{
  "id": 5,
  "status": "Reviewed",
  "total_marks": 12,
  "percentage": 80,
  "grade": "A",
  "question_grades": [
    {
      "question_id": 10,
      "question_no": 1,
      "max_marks": 5,
      "obtained_marks": 4
    }
  ]
}
```

## 37. New Backend Tables

New tables:

```text
classrooms
assignment_questions
submission_grades
```

Expanded tables:

```text
students.classroom_id
subjects.classroom_id
attendance.classroom_id
marks.classroom_id
assignments.classroom_id
assignments.pdf_file
assignments.is_published
assignments.published_at
submissions.submitted_file
submissions.total_marks
submissions.percentage
submissions.grade
```

Migration:

```text
backend/alembic/versions/20260707_0900_erp_lms_expansion.py
```

## 38. New Frontend Screens

Added or upgraded screens:

```text
/classrooms/list       Create/list classrooms
/students/create       Auto-generates student user credentials
/students/import       CSV/Excel preview and import
/attendance/mark       Bulk classroom attendance grid
/assignments/create    Classroom assignment with questions
/assignments/:id       Submit, view submissions, and grade question-wise
```

## 39. Credential Storage Answer

When a new student is created, they need credentials. EduTrack Pro now handles this automatically.

The expected behavior is:

1. Teacher creates or imports the student.
2. Backend creates a `User` with role `student`.
3. Backend generates a temporary password.
4. Backend stores only `password_hash`.
5. Backend returns the plain password once in `generated_credentials`.
6. Teacher gives the email/password to the student.
7. Student logs in normally through `/login`.

Plain passwords should not be permanently stored. For a future production version, the next step would be:

- Add a forced password reset on first login.
- Add password reset email flow.
- Add credential export/download for import batches.
- Add audit logs for credential generation.
