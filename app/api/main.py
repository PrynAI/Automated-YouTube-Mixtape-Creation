"""FastAPI application factory and router registration."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.files import router as files_router
from app.api.routers.health import router as health_router
from app.api.routers.jobs import router as jobs_router
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.infrastructure.repositories.job_store import JobStore


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    setup_logging()
    settings = get_settings()

    app = FastAPI(title=settings.project_name)
    app.state.settings = settings
    app.state.job_store = JobStore()

    allow_origins = settings.cors_allow_origins or ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(jobs_router, prefix=settings.api_v1_prefix)
    app.include_router(files_router, prefix=settings.api_v1_prefix)

    return app


app = create_app()
