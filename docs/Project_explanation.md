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
