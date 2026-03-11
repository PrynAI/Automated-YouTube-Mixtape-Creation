"""Response-side DTO definitions returned by API endpoints."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.domain.models import JobStatus


class JobCreateResponse(BaseModel):
    """Response returned after a new job is queued."""

    job_id: str
    status: JobStatus
    message: str


class TrackResponse(BaseModel):
    """Track timing details shown in job status responses."""

    filename: str
    start_ms: int
    duration_ms: int


class JobStatusResponse(BaseModel):
    """Full job status payload returned to the UI polling endpoint."""

    job_id: str
    status: JobStatus
    message: str
    error: str | None = None
    audio_download_url: str | None = None
    description_download_url: str | None = None
    video_download_url: str | None = None
    tracks: list[TrackResponse] = Field(default_factory=list)
