"""Dependency provider functions used by FastAPI routers."""

from __future__ import annotations

from fastapi import Request

from app.core.config import Settings
from app.infrastructure.repositories.job_store import JobStore


def get_app_settings(request: Request) -> Settings:
    """Return application settings stored on FastAPI app state."""
    return request.app.state.settings


def get_job_store(request: Request) -> JobStore:
    """Return the in-memory job repository from app state."""
    return request.app.state.job_store
