# EduTrack Pro Backend

FastAPI backend for EduTrack Pro.

## Setup

From the backend folder:

```bash
chmod +x setup.sh
./setup.sh
```

On Windows:

```bat
setup.bat
```

The setup script checks Python 3.11+, creates `venv`, installs dependencies, and creates `.env` from `.env.example` only if `.env` does not already exist.

## Run

```bash
uvicorn app.main:app --reload
```

## Demo Data

```bash
.venv/bin/python -m app.database.seed
```

Demo credentials:

```text
teacher@example.com / Password123
student@example.com / Password123
```
