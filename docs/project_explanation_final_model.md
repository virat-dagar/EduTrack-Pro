# EduTrack Pro Project Explanation — Final Model

This document is the current, file-by-file explanation of the EduTrack Pro repository. It follows the style of `docs/Project_explanation.md`, but it is based on the files that currently exist in the project rather than on an older project snapshot.

The guide explains the complete source-controlled implementation: the root scripts, FastAPI backend, SQLAlchemy database layer, Alembic migrations, React frontend, tests, documentation, configuration, and static assets. The repository also creates local runtime files such as `backend/edutrack_pro.db`, virtual environments, `node_modules`, uploads, and Python cache files; those are generated artifacts and are not treated as application source files.

## 1. Project Summary

EduTrack Pro is a full-stack academic management system. It supports:

- teacher and student authentication;
- student, classroom, subject, attendance, and marks management;
- assignment creation, publishing, file upload, submissions, and grading;
- dashboards, analytics, reports, CSV/Excel student import, and student export;
- responsive React pages with role-aware navigation, dark mode, reusable components, and API-backed state.

The project is divided into two applications:

- `backend/`: a FastAPI application using SQLAlchemy, SQLite, Alembic, Pydantic, JWT authentication, and pytest;
- `frontend/`: a React 19 single-page application built and served by Vite.

The principal runtime path is:

```text
Browser
  -> React routes and pages
  -> frontend service modules
  -> Axios client
  -> FastAPI routers
  -> backend service classes
  -> SQLAlchemy models and database session
  -> SQLite database
```

## 2. Current Repository Structure

```text
EduTrack_Pro/
  backend/                    FastAPI API and tests
  frontend/                   React + Vite application
  docs/                       Project-level documentation
  setup/                      Cross-platform setup helpers
  demo.sh / demo.bat          Local demo runners
  setup.sh / setup.bat        Interactive setup entry points
  Makefile                    Common development commands
  README.md                   Repository quick start
  LICENSE                     Project license text
```

The current repository contains 209 existing tracked files before this guide is added. The complete inventory is described later in this document.

### Root File Responsibilities

- `.gitignore` — Excludes local environments, databases, caches, build output, dependency directories, and secrets from version control.
- `LICENSE` — States the legal terms under which the project can be used and distributed.
- `Makefile` — Provides short developer commands for setup, backend/frontend startup, tests, and linting.
- `README.md` — Gives the top-level quick start, demo credentials, setup choices, and common commands.
- `demo.sh` — Unix demo orchestrator that prepares dependencies, seeds data, selects free ports, starts both servers, waits for health, and cleans up on exit.
- `demo.bat` — Windows demo orchestrator with the same setup, port selection, health polling, startup, and stop behavior using Windows commands.
- `setup.sh` — Unix interactive menu that delegates backend, frontend, or complete setup to the scripts in `setup/`.
- `setup.bat` — Windows interactive setup menu that delegates to the Windows scripts in `setup/`.
- `setup/backend.sh` — Unix root-level backend setup helper that creates the Python environment and installs backend packages.
- `setup/backend.bat` — Windows root-level backend setup helper.
- `setup/frontend.sh` — Unix root-level frontend setup helper that installs npm packages and optionally starts Vite.
- `setup/frontend.bat` — Windows root-level frontend setup helper.

## 3. Running The Project

### First-Time Setup

On macOS or Linux:

```bash
chmod +x setup.sh
./setup.sh
```

Choose backend, frontend, or complete project setup. On Windows, run:

```bat
setup.bat
```

The backend setup creates a Python virtual environment and installs `backend/requirements.txt`. The frontend setup installs the packages in `frontend/package.json` using the committed lock file when possible.

### Start The Backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

The Windows equivalent uses `venv\\Scripts\\activate`. The API is normally available at `http://127.0.0.1:8000`, with interactive documentation at `/docs`.

### Start The Frontend

```bash
cd frontend
npm install
npm run dev
```

The Vite development server normally uses `http://localhost:5173`.

### Run The Demo

```bash
./demo.sh
```

`demo.sh` finds an available backend and frontend port, prepares dependencies, creates `.env` from `.env.example` when needed, seeds demo data, starts both processes, waits for backend health, and stops child processes on exit. `demo.bat` provides the equivalent Windows flow in separate command windows.

Demo credentials created by the seed script are:

```text
teacher@example.com / Password123
student@example.com / Password123
```

### Common Commands

```bash
make backend       # backend setup
make frontend      # frontend setup
make run-backend   # run FastAPI with reload
make run-frontend  # run Vite
make test          # backend tests and frontend lint
make lint          # backend Ruff and frontend ESLint
```

## 4. Environment And Configuration

### Backend Variables

`backend/.env.example` documents the settings consumed by `backend/app/core/config.py`:

| Variable | Purpose |
| --- | --- |
| `DATABASE_URL` | SQLAlchemy database URL; local default is SQLite |
| `SECRET_KEY` | Secret used to sign JWT access tokens |
| `JWT_ALGORITHM` / `ALGORITHM` | JWT signing algorithm, normally `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime |
| `CORS_ORIGINS` / `BACKEND_CORS_ORIGINS` | Comma-separated allowed browser origins |
| `UPLOAD_DIR` | Optional directory for assignment and submission files |

The default API database is `sqlite:///./edutrack_pro.db`. Production deployments should provide a strong secret and an explicit database URL.

### Frontend Variables

`VITE_API_BASE_URL` controls the Axios base URL. Its default is:

```text
http://localhost:8000/api/v1
```

The demo runners override this value when they select a different backend port.

## 5. Backend Architecture

The backend is intentionally layered:

```text
app.main
  -> routers
  -> service classes
  -> models and SQLAlchemy session
  -> SQLite or configured relational database
```

- Routers define HTTP paths, request dependencies, status codes, and response wrappers.
- Schemas validate input and describe serialized output.
- Services contain query logic, business rules, analytics, imports, file handling, and aggregation.
- Models define tables, columns, constraints, and relationships.
- Core modules provide settings, authentication, logging, and reusable dependencies.
- Database modules create engines, sessions, metadata, tables, and seed data.
- Exceptions and utilities keep error handling, pagination, validation, and response formats consistent.

## 6. Backend Startup And Request Flow

When `app.main:app` is imported:

1. Settings are loaded from environment variables.
2. Logging is configured.
3. A FastAPI application is created with metadata and API documentation settings.
4. CORS middleware is installed.
5. Global exception handlers are registered.
6. Every API router is included.
7. The lifespan startup creates or updates the local database tables.
8. `/health` and `/api/v1/health` expose health responses.

For a protected request, FastAPI resolves `get_db`, decodes the bearer token through `get_current_user`, optionally checks the teacher or student role, calls the service, and wraps the result in the common response format.

## 7. Authentication And Authorization

The login flow is:

1. The frontend posts credentials to `/api/v1/auth/login`.
2. `AuthService` finds the user and verifies the password hash.
3. The backend returns a JWT and safe user information.
4. `AuthContext` stores the token and user in browser storage.
5. Axios adds `Authorization: Bearer <token>` to later calls.
6. Backend dependencies decode the token and load the current user.
7. Router dependencies enforce role-specific access.

The supported roles are `teacher` and `student`. Teachers manage institutional data. Students see their own profile, attendance, marks, assignments, submissions, and student dashboard. Sensitive `password_hash` data is never included in response schemas.

## 8. Database Model

The database contains these core entities:

| Entity | Purpose | Main relationships |
| --- | --- | --- |
| `users` | Login identity and role | Optional one-to-one student profile; teacher audit relationships |
| `students` | Academic student profile | Classroom, attendance, marks, submissions |
| `classrooms` | Department/course/semester/section grouping | Students, subjects, assignments, attendance, marks |
| `subjects` | Academic subject catalog | Attendance, marks, assignments |
| `attendance` | Daily student-subject presence | Student, subject, classroom, marking teacher |
| `marks` | Assessment result | Student, subject, classroom, entering teacher |
| `assignments` | Teacher-created work | Classroom, subject, questions, submissions |
| `assignment_questions` | Per-question maximum marks | Assignment and question grades |
| `submissions` | Student work and review state | Assignment, student, reviewer, grades |
| `submission_grades` | Per-question obtained marks | Submission and assignment question |

Important uniqueness rules include user email, student roll number, enrollment number, student email, subject code, one attendance record per student/subject/date, one marks record per student/subject/assessment/date, one question number per assignment, and one submission per student/assignment.

## 9. Backend File-by-File Explanation

### 9.1 Backend Root, Migration, And Documentation Files

- `backend/.env.example` — Safe development template for database, JWT, CORS, upload, and runtime settings. It is copied to `.env` by setup/demo flows; the real `.env` is ignored.
- `backend/.gitignore` — Keeps the backend virtual environments, local database, `.env`, uploads, caches, and generated files out of version control.
- `backend/README.md` — Backend-specific quick start with virtual-environment, server, seed, migration, and test commands.
- `backend/requirements.txt` — Runtime Python dependencies, including FastAPI, Uvicorn, SQLAlchemy, Alembic, Pydantic settings, JWT/password libraries, pandas, and spreadsheet/file support.
- `backend/requirements-dev.txt` — Development additions such as pytest and Ruff.
- `backend/setup.sh` — Unix setup script that creates the backend virtual environment and installs runtime/development packages.
- `backend/setup.bat` — Windows counterpart to `backend/setup.sh`.
- `backend/alembic.ini` — Alembic configuration, including the migration script location and database URL fallback.
- `backend/alembic/README` — Alembic's local migration-directory note and usage reminder.
- `backend/alembic/env.py` — Connects Alembic to application settings and SQLAlchemy metadata so migrations can run against the configured database.
- `backend/alembic/script.py.mako` — Template used by Alembic when generating a new revision file.
- `backend/alembic/versions/20260701_1200_initial_schema.py` — Creates the original users, students, subjects, attendance, marks, assignments, and submissions schema, including indexes and constraints.
- `backend/alembic/versions/20260707_0900_erp_lms_expansion.py` — Adds classrooms, question-wise assignment grading, classroom foreign keys, assignment publication/file fields, submission grading fields, and related tables.
- `backend/docs/api.md` — Backend API usage reference, including authentication, resources, pagination, and common response conventions.
- `backend/docs/architecture.md` — Short explanation of the FastAPI/router/service/model layering and frontend-to-backend flow.
- `backend/docs/database.md` — Database tables and uniqueness constraints, plus the `alembic upgrade head` command.
- `backend/docs/deployment.md` — Deployment commands for installing dependencies, applying migrations, starting Uvicorn, building the frontend, and setting production variables.

### 9.2 Backend Core

- `backend/app/core/__init__.py` — Marks `core` as a Python package; it intentionally has no application logic.
- `backend/app/core/config.py` — Defines the settings object, environment-backed defaults, CORS parsing, and `resolve_upload_dir`, which turns the upload setting into a usable filesystem path.
- `backend/app/core/dependencies.py` — Provides `get_current_user`, `require_teacher`, `require_student`, and `ensure_teacher_or_owner`. These functions centralize JWT identity loading and role/ownership checks.
- `backend/app/core/logging.py` — Configures application logging and exposes `get_logger` so modules use consistent log formatting and levels.
- `backend/app/core/security.py` — Hashes and verifies passwords with the configured password library, creates signed access tokens, and decodes/validates JWT payloads.

### 9.3 Backend Database Package

- `backend/app/database/__init__.py` — Marks the database directory as a package.
- `backend/app/database/base.py` — Defines the declarative SQLAlchemy `Base` and imports all model modules through `import_models`, ensuring metadata contains every table before creation or migration inspection.
- `backend/app/database/database.py` — Creates the SQLAlchemy engine and `SessionLocal`. SQLite receives `check_same_thread=False` and a foreign-key pragma listener.
- `backend/app/database/init_db.py` — Calls metadata creation and contains compatibility logic for adding expected SQLite columns when a local database predates the latest migration.
- `backend/app/database/session.py` — Implements the FastAPI `get_db` generator. It opens one session per request, yields it, and closes it reliably.
- `backend/app/database/seed.py` — Idempotently creates demo teacher/student accounts and representative classrooms, subjects, students, attendance, marks, assignments, questions, submissions, and grades. It is executable as `python -m app.database.seed`.

### 9.4 Backend Application Entry Point

- `backend/app/main.py` — Creates the FastAPI app, configures CORS, creates the upload directory, mounts `/uploads`, registers exception handlers, includes every API router, initializes the database during lifespan startup, and exposes both health endpoints.

### 9.5 Backend Exceptions

- `backend/app/exceptions/__init__.py` — Re-exports the application exception types for convenient imports.
- `backend/app/exceptions/custom_exceptions.py` — Defines `AppException` and domain subclasses: `AuthenticationError`, `AuthorizationError`, `NotFoundError`, `ConflictError`, and `BusinessRuleError`. Each carries a status code, message, and optional details.
- `backend/app/exceptions/handlers.py` — Registers FastAPI handlers that normalize domain errors, request validation failures, database errors, and unexpected exceptions into predictable JSON error responses.

### 9.6 Backend Models

- `backend/app/models/__init__.py` — Imports and exports every ORM model so the database metadata and application imports use one central model list.
- `backend/app/models/user.py` — Defines the `users` table, `utc_now` timestamp helper, email uniqueness, role, active state, password hash, and teacher-side relationships to created assignments, marked attendance, entered marks, and reviewed submissions.
- `backend/app/models/student.py` — Defines student identity/profile fields, its one-to-one user relationship, optional classroom membership, and relationships to attendance, marks, and submissions.
- `backend/app/models/classroom.py` — Defines classroom code/name, department, course, semester, section, academic year, active state, and the composite uniqueness rule preventing duplicate academic groups.
- `backend/app/models/subject.py` — Defines subject code/name, course, department, semester, credits, optional classroom, active state, and relationships to attendance, marks, and assignments.
- `backend/app/models/attendance.py` — Stores one dated status per student and subject, optional classroom, remarks, marking teacher, timestamps, and a unique student/subject/date constraint.
- `backend/app/models/marks.py` — Stores assessment type, obtained/maximum marks, examination date, optional classroom, remarks, entering teacher, and a unique assessment identity per student/subject/date.
- `backend/app/models/assignment.py` — Stores subject/classroom, title, description, optional PDF, total marks, assigned/due dates, creator, publication state, timestamps, and relationships to questions and submissions.
- `backend/app/models/assignment_question.py` — Stores ordered question number, optional title/description, maximum marks, and a unique question number inside each assignment. It owns related `SubmissionGrade` rows.
- `backend/app/models/submission.py` — Stores assignment/student ownership, submission date, status, notes, legacy/new file references, review metadata, total marks, percentage, grade, and question-grade relationships.
- `backend/app/models/submission_grade.py` — Stores one obtained score and optional feedback for a submission question, with foreign keys to the submission, assignment question, and reviewing teacher where applicable.

### 9.7 Backend Schemas

- `backend/app/schemas/__init__.py` — Marks the schemas directory as a package.
- `backend/app/schemas/common.py` — Defines reusable `APIResponse`, error detail/error response, pagination data, and message response shapes.
- `backend/app/schemas/auth.py` — Defines login input, login output containing token/user data, and current-user output.
- `backend/app/schemas/user.py` — Defines user create/update/response schemas, validates role/email/name, and excludes password hashes from output.
- `backend/app/schemas/student.py` — Defines student create/update/output schemas plus normalized import rows and import commit payloads. Validators normalize email/phone/text and reject future birth dates.
- `backend/app/schemas/classroom.py` — Defines classroom create/update/response/list schemas with normalized academic-group fields and semester validation.
- `backend/app/schemas/subject.py` — Defines subject create/update/response/list schemas and normalizes subject code, name, course, and department.
- `backend/app/schemas/attendance.py` — Defines single attendance input/update/output, summary/percentage responses, and bulk attendance items/request payloads.
- `backend/app/schemas/marks.py` — Defines marks input/update/output, summary, average, and paginated list responses with range and date validation.
- `backend/app/schemas/assignment.py` — Defines assignment question input/output and assignment create/update/output/list payloads, including publication, classroom, PDF, and question data.
- `backend/app/schemas/submission.py` — Defines submission create/update, question score, review, output, and paginated list payloads. A create request must include either `submitted_file` or `attachment_path`.
- `backend/app/schemas/dashboard.py` — Defines teacher/student dashboard summaries plus generic chart and activity response objects.
- `backend/app/schemas/report.py` — Defines typed response shapes for student, attendance, marks, assignment, performance, and institution reports.

### 9.8 Backend Services

- `backend/app/services/__init__.py` — Marks the service directory as a package.
- `backend/app/services/auth_service.py` — Looks up users, verifies credentials, creates JWT login responses, and returns the current safe user representation.
- `backend/app/services/user_service.py` — Implements user listing, creation, retrieval, updates, deletion, activation, deactivation, duplicate checks, and pagination.
- `backend/app/services/student_service.py` — Implements student CRUD, user-account creation, temporary credential generation, current-student lookup, search, export, import preview/commit, classroom validation, and duplicate detection.
- `backend/app/services/classroom_service.py` — Implements classroom CRUD, academic-group uniqueness checks, active-state handling, and classroom list/detail operations.
- `backend/app/services/subject_service.py` — Implements subject CRUD, subject code checks, search, course filtering, semester filtering, classroom checks, and pagination.
- `backend/app/services/attendance_service.py` — Implements single and bulk attendance marking, duplicate/date validation, student/subject/classroom filters, summary and percentage calculations, history, analytics, and at-risk student detection.
- `backend/app/services/marks_service.py` — Implements marks CRUD, assessment validation, uniqueness checks, student/subject filtering, averages, summaries, and classroom-aware queries.
- `backend/app/services/assignment_service.py` — Implements assignment CRUD, question synchronization, classroom/subject checks, publication, upcoming/overdue queries, file storage, teacher filtering, and assignment submission summaries.
- `backend/app/services/submission_service.py` — Implements submission file storage, student submission creation/update, ownership checks, due-date status, duplicate prevention, teacher review, question-wise score validation, total/percentage/grade calculation, and enriched responses.
- `backend/app/services/analytics_service.py` — Aggregates attendance and marks metrics, trends, distributions, at-risk students, and dashboard chart data.
- `backend/app/services/dashboard_service.py` — Builds teacher and student dashboard cards, charts, activity feeds, assignment counts, attendance metrics, and performance summaries.
- `backend/app/services/report_service.py` — Builds student academic reports, attendance/marks/assignment reports, performance reports, and institution-level summaries.

### 9.9 Backend Routers And API Endpoints

Every router returns service results through the common response convention and uses database/auth dependencies.

- `backend/app/routers/__init__.py` — Marks the router directory as a package.
- `backend/app/routers/auth.py` — Exposes `POST /api/v1/auth/login` and `GET /api/v1/auth/me`.
- `backend/app/routers/users.py` — Exposes user list/create/detail/update/delete and activate/deactivate endpoints for teacher administration.
- `backend/app/routers/students.py` — Exposes student list/detail/create/update/delete, `/me`, search, export, import preview, and import commit endpoints.
- `backend/app/routers/classrooms.py` — Exposes classroom list/create/detail/update/delete endpoints.
- `backend/app/routers/subjects.py` — Exposes subject list/search/course/semester filters and CRUD endpoints.
- `backend/app/routers/attendance.py` — Exposes attendance list, summary, analytics, at-risk, classroom sheet, bulk mark, percentage, student/subject history, and single-record CRUD endpoints.
- `backend/app/routers/marks.py` — Exposes marks list, summary, average, student/subject filters, and CRUD endpoints.
- `backend/app/routers/assignments.py` — Exposes assignment-file upload, list, upcoming, overdue, subject/teacher filters, create/detail/update/delete, publish, and submission-summary endpoints.
- `backend/app/routers/submissions.py` — Exposes submission list, pending reviews, upload, student/assignment filters, create/detail/update/delete, and teacher review endpoints.
- `backend/app/routers/dashboard.py` — Exposes teacher and student dashboard summary, charts, and activity endpoints.
- `backend/app/routers/reports.py` — Exposes student, attendance, marks, assignment, performance, and institution report endpoints.

The most important endpoint map is:

| Area | Representative endpoints |
| --- | --- |
| Auth | `POST /auth/login`, `GET /auth/me` |
| Students | `GET/POST /students`, `GET/PUT/DELETE /students/{id}`, `/students/import/*`, `/students/export` |
| Classrooms | `GET/POST /classrooms`, `GET/PUT/DELETE /classrooms/{id}` |
| Subjects | `GET/POST /subjects`, filter/search endpoints, CRUD by ID |
| Attendance | `/attendance`, `/attendance/bulk`, `/attendance/analytics`, `/attendance/at-risk`, summary/history routes |
| Marks | `/marks`, summary/average/history routes, CRUD by ID |
| Assignments | `/assignments`, upload/publish/upcoming/overdue routes, CRUD by ID |
| Submissions | `/submissions`, upload/pending/review routes, student/assignment filters |
| Dashboards | `/dashboard/teacher/*`, `/dashboard/student/*` |
| Reports | `/reports/student/{id}`, `/reports/attendance`, `/reports/marks`, `/reports/assignments`, `/reports/performance`, `/reports/institution` |

### 9.10 Backend Utilities

- `backend/app/utils/__init__.py` — Marks the utilities directory as a package.
- `backend/app/utils/constants.py` — Centralizes role names, attendance statuses, assessment types, assignment/submission statuses, grade thresholds, and related allowed values.
- `backend/app/utils/helpers.py` — Normalizes pagination, slices SQLAlchemy queries, computes total pages, and applies allow-listed sorting.
- `backend/app/utils/response.py` — Builds success, error, and pagination response dictionaries with consistent keys.
- `backend/app/utils/validators.py` — Normalizes emails/text, rejects future dates, and validates phone-number shape.

### 9.11 Backend Tests

- `backend/tests/__init__.py` — Empty package marker for the test suite.
- `backend/tests/conftest.py` — Creates isolated test database/session fixtures, configures the FastAPI test client, and supplies authenticated teacher/student helpers.
- `backend/tests/test_auth.py` — Tests login success/failure, token use, and current-user behavior.
- `backend/tests/test_users.py` — Tests user administration and activation/deactivation behavior.
- `backend/tests/test_students.py` — Tests student CRUD, student-user credentials, permissions, and student-specific access.
- `backend/tests/test_subjects.py` — Tests subject CRUD, validation, search, and filtering.
- `backend/tests/test_attendance.py` — Tests single attendance, duplicate protection, summaries, and role permissions.
- `backend/tests/test_marks.py` — Tests marks creation, updates, summaries, averages, and authorization.
- `backend/tests/test_assignments.py` — Tests assignment CRUD, publication, date filters, and teacher/student rules.
- `backend/tests/test_submissions.py` — Tests submission creation, duplicate/due-date rules, file references, and review behavior.
- `backend/tests/test_erp_lms_workflows.py` — Integration-style coverage for classroom membership, bulk student import, bulk attendance, assignment questions, submission review, and question-wise grading.

## 10. Frontend Architecture

The frontend is a Vite application with a single `App` component, React Router route definitions, lazy-loaded pages, three global contexts, reusable UI primitives, and one service module per backend domain.

The browser flow is:

```text
main.jsx
  -> providers
  -> App
  -> AppRoutes
  -> public/protected layout
  -> lazy page
  -> domain service
  -> Axios API client
```

`AuthContext` manages the session, `ThemeContext` manages light/dark mode, and `SidebarContext` manages desktop/mobile sidebar state. `ProtectedRoute` prevents unauthenticated or incorrectly authorized access.

## 11. Frontend File-by-File Explanation

### 11.1 Frontend Root And Build Files

- `frontend/.gitignore` — Ignores `node_modules`, Vite output, local environment files, and editor/runtime artifacts.
- `frontend/README.md` — Documents `npm install`, development, lint, build, and `VITE_API_BASE_URL` usage.
- `frontend/package.json` — Defines the React/Vite package, runtime dependencies (`axios`, `lucide-react`, `react-router-dom`, `react-toastify`, `recharts`), dev dependencies, and `dev`, `build`, `lint`, and `preview` scripts.
- `frontend/package-lock.json` — Locks the complete npm dependency graph for reproducible installs.
- `frontend/index.html` — Vite HTML entry document. It provides the favicon, viewport metadata, title, root element, and module script for `src/main.jsx`.
- `frontend/vite.config.js` — Enables the React plugin in Vite.
- `frontend/eslint.config.js` — Configures ESLint recommended rules, browser globals, React hooks rules, refresh rules, JSX parsing, and `dist` exclusion.
- `frontend/setup.sh` — Unix frontend setup script that checks Node/npm, installs packages, and optionally starts the dev server.
- `frontend/setup.bat` — Windows counterpart to the frontend setup script.
- `frontend/public/favicon.png` — Browser tab/favicon image.
- `frontend/src/assets/hero-dark.png` — Dark-theme hero artwork used by the authentication layout.
- `frontend/src/assets/hero-light.png` — Light-theme hero artwork used by the authentication layout.

### 11.2 Frontend Bootstrap, Layouts, Contexts, And Hooks

- `frontend/src/main.jsx` — Creates the React root, wraps the app in `StrictMode`, `BrowserRouter`, `AuthProvider`, `SidebarProvider`, and `ThemeProvider`, then loads global CSS.
- `frontend/src/App.jsx` — Renders the route tree and global colored `ToastContainer`.
- `frontend/src/layouts/AuthLayout.jsx` — Provides the split login/authentication presentation and switches hero art according to the theme.
- `frontend/src/layouts/DashboardLayout.jsx` — Provides the authenticated shell containing `Navbar`, `Sidebar`, and the routed `Outlet` content.
- `frontend/src/layouts/BlankLayout.jsx` — Minimal wrapper used for forbidden and not-found pages.
- `frontend/src/context/authContext.js` — Creates the shared `AuthContext` object.
- `frontend/src/context/AuthContext.jsx` — Loads persisted auth state, logs in/out, calls `/auth/me` when needed, stores token/user data, exposes loading/authenticated state, and displays login errors through toasts.
- `frontend/src/context/sidebarContext.js` — Creates the shared `SidebarContext` object.
- `frontend/src/context/SidebarContext.jsx` — Manages sidebar open/collapsed state, responsive behavior, and persisted preference.
- `frontend/src/context/themeContext.js` — Creates the shared `ThemeContext` object.
- `frontend/src/context/ThemeContext.jsx` — Manages light/dark theme, applies the theme class/attribute, and persists the selected mode.
- `frontend/src/hooks/useApi.js` — Generic request hook with loading, error, refresh, dependency-based loading, and optional toast handling.
- `frontend/src/hooks/useAuth.js` — Reads and validates `AuthContext` for components that need the current user or auth actions.
- `frontend/src/hooks/useDebounce.js` — Delays a value update for search inputs and other rapidly changing controls.
- `frontend/src/hooks/usePagination.js` — Provides page/page-size state and helpers for paginated list pages.
- `frontend/src/hooks/useSidebar.js` — Reads `SidebarContext`.
- `frontend/src/hooks/useTheme.js` — Reads `ThemeContext`.

### 11.3 Frontend Reusable Components

- `frontend/src/components/common/Button.jsx` — Shared button with variants, loading/disabled state, icon support, and consistent styling.
- `frontend/src/components/common/Card.jsx` — Small surface/container primitive used throughout pages and dashboards.
- `frontend/src/components/common/CountUp.jsx` — Animates numeric values for dashboard statistics.
- `frontend/src/components/common/Input.jsx` — Labeled form input with icon, hint, and validation-error display.
- `frontend/src/components/common/Modal.jsx` — Controlled modal shell with title, close action, and shared button styling.
- `frontend/src/components/charts/ChartCard.jsx` — Wraps Recharts bar, line, or area visualizations in a card and falls back to `EmptyState` when data is empty.
- `frontend/src/components/dashboard/StatCard.jsx` — Displays a titled metric, optional icon/detail, tone, and animated value.
- `frontend/src/components/feedback/EmptyState.jsx` — Standard no-data message.
- `frontend/src/components/feedback/ErrorState.jsx` — Standard error message with alert icon.
- `frontend/src/components/feedback/LoadingState.jsx` — Standard loading indicator and label.
- `frontend/src/components/layout/Navbar.jsx` — Shows product identity, current user, theme toggle, sidebar control, and logout action.
- `frontend/src/components/layout/PageHeader.jsx` — Consistent title/description/action row for pages.
- `frontend/src/components/layout/Sidebar.jsx` — Role-aware navigation links, grouped modules, active-link styling, and responsive close behavior.
- `frontend/src/components/tables/DataTable.jsx` — Generic column/row table with row keys and empty-state handling.
- `frontend/src/components/ui/Badge.jsx` — Small status badge with semantic tones.

### 11.4 Frontend Pages

- `frontend/src/pages/auth/LoginPage.jsx` — Login form, client-side validation, error toast, and role-based redirect after authentication.
- `frontend/src/pages/dashboard/TeacherDashboard.jsx` — Teacher metrics, charts, attendance risk, assignment activity, and quick academic overview.
- `frontend/src/pages/dashboard/StudentDashboard.jsx` — Student attendance, marks, assignment, performance, charts, and recent activity overview.
- `frontend/src/pages/students/StudentsList.jsx` — Teacher student table with search, pagination, create/import navigation, and export action.
- `frontend/src/pages/students/StudentForm.jsx` — Student create/edit form. New records receive backend-generated login credentials that can be shown once to the teacher.
- `frontend/src/pages/students/StudentDetail.jsx` — Student profile/detail view with teacher edit navigation and student-safe access behavior.
- `frontend/src/pages/students/StudentImportPage.jsx` — Uploads CSV/Excel data, previews normalized rows/errors, and commits valid import rows.
- `frontend/src/pages/classrooms/ClassroomsList.jsx` — Lists classrooms and provides a teacher form for creating academic groups.
- `frontend/src/pages/subjects/SubjectsList.jsx` — Subject list with filters, table rows, and teacher create navigation.
- `frontend/src/pages/subjects/SubjectForm.jsx` — Subject create/edit form with code, course, department, semester, credits, classroom, and active-state fields.
- `frontend/src/pages/subjects/SubjectDetail.jsx` — Subject detail view with teacher edit action.
- `frontend/src/pages/attendance/AttendanceList.jsx` — Attendance history table with filters and role-aware mark action.
- `frontend/src/pages/attendance/AttendanceHistory.jsx` — Thin page wrapper that reuses `AttendanceList` for the history route.
- `frontend/src/pages/attendance/MarkAttendance.jsx` — Teacher bulk attendance screen. It loads classrooms/subjects, renders a student grid, supports present/absent controls, and submits one bulk request.
- `frontend/src/pages/attendance/AttendanceSummary.jsx` — Teacher attendance summary cards and aggregate view.
- `frontend/src/pages/marks/MarksList.jsx` — Marks table with filtering, percentage formatting, and teacher create/edit actions.
- `frontend/src/pages/marks/MarksForm.jsx` — Teacher marks create/edit form with assessment type, student, subject, dates, obtained/max marks, and remarks.
- `frontend/src/pages/marks/PerformancePage.jsx` — Performance/average view for the current student or selected student context.
- `frontend/src/pages/assignments/AssignmentsList.jsx` — Assignment list with status badges, upcoming/overdue information, teacher create action, and detail links.
- `frontend/src/pages/assignments/AssignmentForm.jsx` — Teacher assignment form with classroom/subject, dates, PDF/file reference, publication state, and dynamic question rows.
- `frontend/src/pages/assignments/AssignmentDetail.jsx` — Assignment description, download/submit controls, student submission state, teacher submission table, and question-wise grading form.
- `frontend/src/pages/reports/ReportsPage.jsx` — Role-aware report selector and renderer for student, attendance, marks, institution, and performance reports.
- `frontend/src/pages/profile/ProfilePage.jsx` — Displays the authenticated user's profile and, for students, the linked academic profile.
- `frontend/src/pages/settings/SettingsPage.jsx` — Theme preference screen with light/dark mode controls.
- `frontend/src/pages/errors/ForbiddenPage.jsx` — Friendly 403 page with navigation back into the application.
- `frontend/src/pages/errors/NotFoundPage.jsx` — Friendly 404 page for unknown routes.

### 11.5 Frontend Routing

- `frontend/src/routes/AppRoutes.jsx` — Defines lazy imports, the public `/login` route, the protected dashboard shell, teacher/student role routes, CRUD routes, report routes, and fallback error routes. Suspense uses `LoadingState`.
- `frontend/src/routes/ProtectedRoute.jsx` — Redirects unauthenticated users to login, checks allowed roles, preserves the attempted location, and redirects unauthorized users to `/forbidden`.
- `frontend/src/routes/PublicRoute.jsx` — Prevents authenticated users from reopening login and sends them to the dashboard appropriate for their role.

Main route groups:

```text
/login
/dashboard/teacher       /dashboard/student
/students/list           /students/create       /students/import       /students/:id
/classrooms/list
/subjects/list           /subjects/create       /subjects/:id
/attendance/list         /attendance/mark       /attendance/summary    /attendance/history
/marks/list              /marks/create          /marks/performance
/assignments/list        /assignments/create    /assignments/:id
/reports/students        /reports/attendance    /reports/marks         /reports/institution
/profile                 /settings
/forbidden               /*
```

### 11.6 Frontend API Services

- `frontend/src/services/api.js` — Creates the Axios instance, reads `VITE_API_BASE_URL`, attaches the stored JWT to requests, and handles common unauthorized behavior.
- `frontend/src/services/authService.js` — Calls login and current-user endpoints.
- `frontend/src/services/userService.js` — Wraps teacher user administration endpoints.
- `frontend/src/services/studentService.js` — Wraps student CRUD, search, export, import preview, and import commit endpoints.
- `frontend/src/services/classroomService.js` — Wraps classroom list, create, update, and delete endpoints.
- `frontend/src/services/subjectService.js` — Wraps subject CRUD, search, course, and semester endpoints.
- `frontend/src/services/attendanceService.js` — Wraps attendance list, summary, analytics, at-risk, classroom sheet, bulk, percentage, and history endpoints.
- `frontend/src/services/marksService.js` — Wraps marks list, summary, average, student/subject filters, and CRUD endpoints.
- `frontend/src/services/assignmentService.js` — Wraps assignment list/detail/create/update/delete, file upload, publish, date filters, teacher/subject filters, and submission summary.
- `frontend/src/services/submissionService.js` — Wraps submission list, upload, create/update/delete, student/assignment filters, pending reviews, and review endpoints.
- `frontend/src/services/dashboardService.js` — Wraps teacher/student dashboard summary, charts, and activity endpoints.
- `frontend/src/services/reportService.js` — Wraps all report endpoint variants.

The services use `compactParams` to avoid sending empty query values and return the Axios response for the page/hook layer to unwrap.

### 11.7 Frontend Utilities And Styling

- `frontend/src/utils/constants.js` — Defines roles, route paths, storage keys, attendance statuses, assessment types, and UI option values shared by routes/forms.
- `frontend/src/utils/dateUtils.js` — Formats API dates for display and returns today's date in ISO form for forms.
- `frontend/src/utils/formatters.js` — Formats percentages/numbers and converts machine values to readable labels.
- `frontend/src/utils/helpers.js` — Chooses a dashboard path from a user role, unwraps API response data, and compacts query parameters.
- `frontend/src/utils/storage.js` — Provides namespaced localStorage read/write/remove helpers.
- `frontend/src/utils/validators.js` — Contains email, required-field, and login-form validation helpers.
- `frontend/src/App.css` — App-level visual rules and compatibility styles.
- `frontend/src/index.css` — Global reset, body/root defaults, font and base application styles.
- `frontend/src/styles/variables.css` — Shared CSS variables for colors, spacing, radii, shadows, and typography.
- `frontend/src/styles/theme.css` — Base theme tokens and light-theme surface rules.
- `frontend/src/styles/dark-theme.css` — Dark-theme overrides for backgrounds, surfaces, text, borders, and controls.
- `frontend/src/styles/globals.css` — Shared layout, form, button, table, and page-level global styling.
- `frontend/src/styles/animations.css` — Reusable transitions, entrance effects, loading effects, and count-up presentation.

## 12. Important User Workflows

### Teacher Login And Administration

```text
LoginPage
  -> authService.login
  -> AuthContext stores JWT/user
  -> ProtectedRoute verifies teacher role
  -> DashboardLayout renders teacher navigation
  -> page service calls API
  -> service class validates and persists data
```

### Student Creation And Credentials

1. A teacher submits the student form or commits an import.
2. `StudentService` creates a student user with role `student`.
3. A temporary password is generated and only its hash is stored.
4. The plain generated credential is returned once in `generated_credentials`.
5. The teacher shares it with the student.
6. The student logs in through the normal login page.

Permanent plain-text password storage is intentionally avoided.

### Bulk Attendance

The teacher selects a classroom, subject, and date. The frontend loads the classroom sheet, assigns statuses in a grid, and sends a bulk payload. The backend verifies that every student belongs to the selected classroom and prevents duplicate student/subject/date records.

### Assignment And Submission

Teachers create an assignment with questions, maximum marks, optional file, classroom, dates, and publication state. Students see active assignments for their classroom, upload or reference a submission file, and may update an unreviewed submission before the due date. Teachers see submissions and review them question by question.

### Question-Wise Grading

For each question, the teacher enters obtained marks and optional feedback. The backend verifies that the question belongs to the assignment and that the score is not greater than `max_marks`, then calculates:

```text
total_marks = sum(question obtained marks)
percentage = total_marks / total assignment marks * 100
grade = A+ (>=90), A (>=80), B (>=70), C (>=60), D (>=50), F otherwise
```

The resulting totals are stored on `submissions`, while per-question details are stored in `submission_grades`.

## 13. Response And Error Conventions

Successful responses generally follow:

```json
{
  "success": true,
  "message": "Readable message",
  "data": {}
}
```

Paginated responses add `items`, `page`, `page_size`, `total_items`, and `total_pages`. Errors are normalized into an error response containing a message and optional details. This allows frontend hooks and pages to display consistent loading, empty, error, and success states.

## 14. Migrations, Seed Data, And Local Database Notes

Alembic is the durable schema history. Use:

```bash
cd backend
alembic upgrade head
```

The application startup also creates missing tables for local development. `seed.py` is designed to be repeatable and can populate an existing local SQLite database without duplicating the demo records.

The checked-out repository may contain a local `backend/edutrack_pro.db`, a `backend/venv`, or Python cache files in a developer workspace. Those files are environment artifacts, not tracked source files, and should not be manually documented as application modules.

## 15. Quality Checks

Backend tests:

```bash
cd backend
python -m pytest
```

Backend lint:

```bash
python -m ruff check app tests
```

Frontend checks:

```bash
cd frontend
npm run lint
npm run build
```

The most valuable end-to-end checks are the ERP/LMS workflow tests because they cover relationships across classrooms, students, attendance, assignments, submissions, and grading rather than only isolated CRUD functions.

## 16. Consistency Rules For Future Changes

When adding a feature:

1. Add or update a model and migration if the database shape changes.
2. Add a schema for input/output validation.
3. Put business rules in the relevant service rather than directly in the router.
4. Add a router endpoint with the correct dependency and response wrapper.
5. Add a frontend service method and page/component state.
6. Add role-aware routes and navigation when necessary.
7. Add backend tests for both successful and forbidden paths.
8. Update the relevant documentation and this inventory if a new file is introduced.

Keep these boundaries intact:

- routers handle HTTP concerns;
- services handle business rules and data access;
- schemas handle validation and serialization;
- models handle persistence relationships;
- frontend pages handle presentation and user interaction;
- frontend services handle HTTP calls;
- shared constants prevent frontend/backend value drift.

## 17. Complete File Coverage Checklist

The following paths are all of the source-controlled files present in the project snapshot used for this document. Each one is explained above or is explicitly identified as a package marker/configuration/asset.

### Root

```text
.gitignore
LICENSE
Makefile
README.md
demo.bat
demo.sh
setup.bat
setup.sh
setup/backend.bat
setup/backend.sh
setup/frontend.bat
setup/frontend.sh
```

### Backend

```text
backend/.env.example
backend/.gitignore
backend/README.md
backend/alembic.ini
backend/alembic/README
backend/alembic/env.py
backend/alembic/script.py.mako
backend/alembic/versions/20260701_1200_initial_schema.py
backend/alembic/versions/20260707_0900_erp_lms_expansion.py
backend/app/core/__init__.py
backend/app/core/config.py
backend/app/core/dependencies.py
backend/app/core/logging.py
backend/app/core/security.py
backend/app/database/__init__.py
backend/app/database/base.py
backend/app/database/database.py
backend/app/database/init_db.py
backend/app/database/seed.py
backend/app/database/session.py
backend/app/exceptions/__init__.py
backend/app/exceptions/custom_exceptions.py
backend/app/exceptions/handlers.py
backend/app/main.py
backend/app/models/__init__.py
backend/app/models/assignment.py
backend/app/models/assignment_question.py
backend/app/models/attendance.py
backend/app/models/classroom.py
backend/app/models/marks.py
backend/app/models/student.py
backend/app/models/subject.py
backend/app/models/submission.py
backend/app/models/submission_grade.py
backend/app/models/user.py
backend/app/routers/__init__.py
backend/app/routers/assignments.py
backend/app/routers/attendance.py
backend/app/routers/auth.py
backend/app/routers/classrooms.py
backend/app/routers/dashboard.py
backend/app/routers/marks.py
backend/app/routers/reports.py
backend/app/routers/students.py
backend/app/routers/subjects.py
backend/app/routers/submissions.py
backend/app/routers/users.py
backend/app/schemas/__init__.py
backend/app/schemas/assignment.py
backend/app/schemas/attendance.py
backend/app/schemas/auth.py
backend/app/schemas/classroom.py
backend/app/schemas/common.py
backend/app/schemas/dashboard.py
backend/app/schemas/marks.py
backend/app/schemas/report.py
backend/app/schemas/student.py
backend/app/schemas/subject.py
backend/app/schemas/submission.py
backend/app/schemas/user.py
backend/app/services/__init__.py
backend/app/services/analytics_service.py
backend/app/services/assignment_service.py
backend/app/services/attendance_service.py
backend/app/services/auth_service.py
backend/app/services/classroom_service.py
backend/app/services/dashboard_service.py
backend/app/services/marks_service.py
backend/app/services/report_service.py
backend/app/services/student_service.py
backend/app/services/subject_service.py
backend/app/services/submission_service.py
backend/app/services/user_service.py
backend/app/utils/__init__.py
backend/app/utils/constants.py
backend/app/utils/helpers.py
backend/app/utils/response.py
backend/app/utils/validators.py
backend/docs/api.md
backend/docs/architecture.md
backend/docs/database.md
backend/docs/deployment.md
backend/requirements-dev.txt
backend/requirements.txt
backend/setup.bat
backend/setup.sh
backend/tests/__init__.py
backend/tests/conftest.py
backend/tests/test_assignments.py
backend/tests/test_attendance.py
backend/tests/test_auth.py
backend/tests/test_erp_lms_workflows.py
backend/tests/test_marks.py
backend/tests/test_students.py
backend/tests/test_subjects.py
backend/tests/test_submissions.py
backend/tests/test_users.py
```

### Frontend

```text
frontend/.gitignore
frontend/README.md
frontend/eslint.config.js
frontend/index.html
frontend/package-lock.json
frontend/package.json
frontend/public/favicon.png
frontend/setup.bat
frontend/setup.sh
frontend/src/App.css
frontend/src/App.jsx
frontend/src/assets/hero-dark.png
frontend/src/assets/hero-light.png
frontend/src/components/charts/ChartCard.jsx
frontend/src/components/common/Button.jsx
frontend/src/components/common/Card.jsx
frontend/src/components/common/CountUp.jsx
frontend/src/components/common/Input.jsx
frontend/src/components/common/Modal.jsx
frontend/src/components/dashboard/StatCard.jsx
frontend/src/components/feedback/EmptyState.jsx
frontend/src/components/feedback/ErrorState.jsx
frontend/src/components/feedback/LoadingState.jsx
frontend/src/components/layout/Navbar.jsx
frontend/src/components/layout/PageHeader.jsx
frontend/src/components/layout/Sidebar.jsx
frontend/src/components/tables/DataTable.jsx
frontend/src/components/ui/Badge.jsx
frontend/src/context/AuthContext.jsx
frontend/src/context/SidebarContext.jsx
frontend/src/context/ThemeContext.jsx
frontend/src/context/authContext.js
frontend/src/context/sidebarContext.js
frontend/src/context/themeContext.js
frontend/src/hooks/useApi.js
frontend/src/hooks/useAuth.js
frontend/src/hooks/useDebounce.js
frontend/src/hooks/usePagination.js
frontend/src/hooks/useSidebar.js
frontend/src/hooks/useTheme.js
frontend/src/index.css
frontend/src/layouts/AuthLayout.jsx
frontend/src/layouts/BlankLayout.jsx
frontend/src/layouts/DashboardLayout.jsx
frontend/src/main.jsx
frontend/src/pages/assignments/AssignmentDetail.jsx
frontend/src/pages/assignments/AssignmentForm.jsx
frontend/src/pages/assignments/AssignmentsList.jsx
frontend/src/pages/attendance/AttendanceHistory.jsx
frontend/src/pages/attendance/AttendanceList.jsx
frontend/src/pages/attendance/AttendanceSummary.jsx
frontend/src/pages/attendance/MarkAttendance.jsx
frontend/src/pages/auth/LoginPage.jsx
frontend/src/pages/classrooms/ClassroomsList.jsx
frontend/src/pages/dashboard/StudentDashboard.jsx
frontend/src/pages/dashboard/TeacherDashboard.jsx
frontend/src/pages/errors/ForbiddenPage.jsx
frontend/src/pages/errors/NotFoundPage.jsx
frontend/src/pages/marks/MarksForm.jsx
frontend/src/pages/marks/MarksList.jsx
frontend/src/pages/marks/PerformancePage.jsx
frontend/src/pages/profile/ProfilePage.jsx
frontend/src/pages/reports/ReportsPage.jsx
frontend/src/pages/settings/SettingsPage.jsx
frontend/src/pages/students/StudentDetail.jsx
frontend/src/pages/students/StudentForm.jsx
frontend/src/pages/students/StudentImportPage.jsx
frontend/src/pages/students/StudentsList.jsx
frontend/src/pages/subjects/SubjectDetail.jsx
frontend/src/pages/subjects/SubjectForm.jsx
frontend/src/pages/subjects/SubjectsList.jsx
frontend/src/routes/AppRoutes.jsx
frontend/src/routes/ProtectedRoute.jsx
frontend/src/routes/PublicRoute.jsx
frontend/src/services/api.js
frontend/src/services/assignmentService.js
frontend/src/services/attendanceService.js
frontend/src/services/authService.js
frontend/src/services/classroomService.js
frontend/src/services/dashboardService.js
frontend/src/services/marksService.js
frontend/src/services/reportService.js
frontend/src/services/studentService.js
frontend/src/services/subjectService.js
frontend/src/services/submissionService.js
frontend/src/services/userService.js
frontend/src/styles/animations.css
frontend/src/styles/dark-theme.css
frontend/src/styles/globals.css
frontend/src/styles/theme.css
frontend/src/styles/variables.css
frontend/src/utils/constants.js
frontend/src/utils/dateUtils.js
frontend/src/utils/formatters.js
frontend/src/utils/helpers.js
frontend/src/utils/storage.js
frontend/src/utils/validators.js
frontend/vite.config.js
```

### Project Documentation

- `docs/EduTrack-Pro-Study-Guide.md` — Existing learning-oriented guide for understanding the project and its workflows.
- `docs/Project_explanation.md` — Original broad project explanation that this final model follows in tone and organization.
- `docs/project_explanation_final_model.md` — This current, expanded file-by-file explanation and repository inventory.

## 18. Quick Mental Model

If one sentence is needed to understand the whole project, use this:

```text
React pages use domain services to call protected FastAPI routers; routers delegate to service classes; services validate and aggregate SQLAlchemy models; migrations and seed data establish the academic domain; contexts and shared components keep the browser experience consistent for teachers and students.
```

Treat this document as a snapshot. Whenever a new file, endpoint, model, migration, page, or workflow is added, update the relevant section and the complete file coverage checklist.
