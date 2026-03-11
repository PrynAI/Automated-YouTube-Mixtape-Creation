"""Artifact download endpoints for completed jobs."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from app.api.deps import get_app_settings, get_job_store
from app.core.config import Settings
from app.infrastructure.repositories.job_store import JobStore

router = APIRouter(prefix="/jobs/{job_id}/download", tags=["files"])


def _resolve_artifact_path(settings: Settings, relpath: str | None) -> Path:
    """Resolve an artifact relative path to an absolute file path and validate it."""
    if not relpath:
        raise HTTPException(status_code=404, detail="Artifact not available")

    artifact_path = settings.data_dir / relpath
    if not artifact_path.exists() or not artifact_path.is_file():
        raise HTTPException(status_code=404, detail="Artifact file not found")
    return artifact_path


@router.get("/audio", name="download_audio", summary="Download mixed audio")
def download_audio(
    job_id: str,
    settings: Settings = Depends(get_app_settings),
    job_store: JobStore = Depends(get_job_store),
) -> FileResponse:
    """Download the generated mixtape audio file for a completed job."""
    job_record = job_store.get(job_id)
    if not job_record:
        raise HTTPException(status_code=404, detail="Job not found")

    audio_path = _resolve_artifact_path(settings, job_record.audio_output_relpath)
    return FileResponse(
        path=audio_path,
        media_type="audio/mpeg",
        filename=audio_path.name,
    )


@router.get("/description", name="download_description", summary="Download description text")
def download_description(
    job_id: str,
    settings: Settings = Depends(get_app_settings),
    job_store: JobStore = Depends(get_job_store),
) -> FileResponse:
    """Download the generated description text file for a completed job."""
    job_record = job_store.get(job_id)
    if not job_record:
        raise HTTPException(status_code=404, detail="Job not found")

    description_path = _resolve_artifact_path(settings, job_record.description_output_relpath)
    return FileResponse(
        path=description_path,
        media_type="text/plain",
        filename=description_path.name,
    )


@router.get("/video", name="download_video", summary="Download rendered video")
def download_video(
    job_id: str,
    settings: Settings = Depends(get_app_settings),
    job_store: JobStore = Depends(get_job_store),
) -> FileResponse:
    """Download the rendered video file for a completed job."""
    job_record = job_store.get(job_id)
    if not job_record:
        raise HTTPException(status_code=404, detail="Job not found")

    video_path = _resolve_artifact_path(settings, job_record.video_output_relpath)
    return FileResponse(
        path=video_path,
        media_type="video/mp4",
        filename=video_path.name,
    )
