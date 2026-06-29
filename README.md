# EduTrack Pro

EduTrack Pro is a React + Python project for student, attendance, marks, assignment, and reporting workflows.

## Quick Setup

Run the project setup menu from the repository root:

```bash
chmod +x setup.sh
./setup.sh
```

On Windows:

```bat
setup.bat
```

Choose:

```text
1. Backend
2. Frontend
3. Complete Project
```

## Backend

```bash
cd backend
chmod +x setup.sh
./setup.sh
uvicorn app.main:app --reload
```

Windows:

```bat
cd backend
setup.bat
uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend
chmod +x setup.sh
./setup.sh
```

Windows:

```bat
cd frontend
setup.bat
```

## Common Commands

```bash
make backend
make frontend
make run-backend
make run-frontend
make test
```
