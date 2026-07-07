"""FastAPI application entry point."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings, resolve_upload_dir
from app.core.logging import configure_logging
from app.database.init_db import create_database
from app.exceptions.handlers import register_exception_handlers
from app.routers import (
    assignments,
    attendance,
    auth,
    classrooms,
    dashboard,
    marks,
    reports,
    students,
    subjects,
    submissions,
    users,
)
from app.utils.response import success_response

settings = get_settings()
configure_logging()
upload_root = resolve_upload_dir(settings.upload_dir)
upload_root.mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app_instance: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize application resources."""

    upload_root.mkdir(parents=True, exist_ok=True)
    create_database()
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Academic tracking API for EduTrack Pro.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.mount("/uploads", StaticFiles(directory=upload_root), name="uploads")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(classrooms.router)
app.include_router(students.router)
app.include_router(subjects.router)
app.include_router(attendance.router)
app.include_router(marks.router)
app.include_router(assignments.router)
app.include_router(submissions.router)
app.include_router(dashboard.router)
app.include_router(reports.router)


@app.get("/health", tags=["Health"], summary="Health check")
@app.get("/api/v1/health", tags=["Health"], summary="Versioned health check")
def health_check() -> dict:
    """Return application health."""

    return success_response("EduTrack Pro API is healthy.", {"status": "ok"})
