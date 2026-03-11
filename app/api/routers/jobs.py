"""Job creation and status endpoints for mixtape processing."""

from __future__ import annotations

import logging
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, Request, UploadFile
from pydantic import ValidationError

from app.api.deps import get_app_settings, get_job_store
from app.api.dto.requests import JobCreateOptions
from app.api.dto.responses import JobCreateResponse, JobStatusResponse, TrackResponse
from app.core.config import Settings
from app.domain.models import JobRecord, JobStatus, PipelineInput, PipelineOptions
from app.infrastructure.repositories.job_store import JobStore
from app.infrastructure.storage.local_store import save_upload_file
from app.infrastructure.storage.path_manager import get_job_paths
from app.services.pipeline.mixtape_orchestrator import run_mixtape_pipeline

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs", tags=["jobs"])


def _relpath_from_data_root(settings: Settings, file_path: Path | None) -> str | None:
    """Convert an absolute artifact path into a path relative to the data root."""
    if file_path is None:
        return None
    return file_path.relative_to(settings.data_dir).as_posix()


def _build_job_status_response(request: Request, job_record: JobRecord) -> JobStatusResponse:
    """Build an API response model from an internal job record."""
    record = job_record

    audio_url = (
        str(request.url_for("download_audio", job_id=record.job_id))
        if record.audio_output_relpath
        else None
    )
    description_url = (
        str(request.url_for("download_description", job_id=record.job_id))
        if record.description_output_relpath
        else None
    )
    video_url = (
        str(request.url_for("download_video", job_id=record.job_id))
        if record.video_output_relpath
        else None
    )

    track_items = [TrackResponse(**track) for track in record.tracks]

    return JobStatusResponse(
        job_id=record.job_id,
        status=record.status,
        message=record.message,
        error=record.error,
        audio_download_url=audio_url,
        description_download_url=description_url,
        video_download_url=video_url,
        tracks=track_items,
    )


def _process_job(
    *,
    job_id: str,
    settings: Settings,
    job_store: JobStore,
    transition_ms: int,
    mixtape_name: str,
    genre: str,
    audio_dir: Path,
    image_path: Path | None,
    output_audio_path: Path,
    output_description_path: Path,
    output_video_path: Path,
) -> None:
    """Execute job pipeline in the background and update job status accordingly."""
    try:
        job_store.update(job_id, status=JobStatus.PROCESSING, message="Processing job")

        pipeline_input = PipelineInput(
            job_id=job_id,
            audio_dir=audio_dir,
            output_audio_path=output_audio_path,
            output_description_path=output_description_path,
            output_video_path=output_video_path if image_path else None,
            image_path=image_path,
            options=PipelineOptions(
                transition_ms=transition_ms,
                mixtape_name=mixtape_name,
                genre=genre,
            ),
        )

        result = run_mixtape_pipeline(pipeline_input, settings)

        job_store.update(
            job_id,
            status=JobStatus.COMPLETED,
            message="Job completed",
            audio_output_relpath=_relpath_from_data_root(settings, result.output_audio_path),
            description_output_relpath=_relpath_from_data_root(settings, result.output_description_path),
            video_output_relpath=_relpath_from_data_root(settings, result.output_video_path),
            tracks=[
                {
                    "filename": track.filename,
                    "start_ms": track.start_ms,
                    "duration_ms": track.duration_ms,
                }
                for track in result.track_infos
            ],
        )
    except Exception as exc:
        logger.exception("Job %s failed", job_id)
        job_store.update(
            job_id,
            status=JobStatus.FAILED,
            message="Job failed",
            error=str(exc),
        )


@router.post("", response_model=JobCreateResponse, summary="Create a mixtape generation job")
async def create_job(
    background_tasks: BackgroundTasks,
    audio_files: list[UploadFile] = File(...),
    image_file: UploadFile | None = File(default=None),
    transition_ms: int = Form(default=6000),
    mixtape_name: str = Form(default="Pryn House Mixtape"),
    genre: str = Form(default="Pryn House"),
    settings: Settings = Depends(get_app_settings),
    job_store: JobStore = Depends(get_job_store),
) -> JobCreateResponse:
    """Queue a new job by persisting uploads and scheduling background processing."""
    if not audio_files:
        raise HTTPException(status_code=400, detail="At least one audio file is required.")

    try:
        options = JobCreateOptions(
            transition_ms=transition_ms,
            mixtape_name=mixtape_name,
            genre=genre,
        )
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    job_id = uuid4().hex
    job_store.create(job_id)

    job_paths = get_job_paths(settings, job_id)

    for audio_file in audio_files:
        await save_upload_file(audio_file, job_paths.upload_audio_dir)

    saved_image_path: Path | None = None
    if image_file and image_file.filename:
        saved_image_path = await save_upload_file(image_file, job_paths.upload_image_dir)

    background_tasks.add_task(
        _process_job,
        job_id=job_id,
        settings=settings,
        job_store=job_store,
        transition_ms=options.transition_ms,
        mixtape_name=options.mixtape_name,
        genre=options.genre,
        audio_dir=job_paths.upload_audio_dir,
        image_path=saved_image_path,
        output_audio_path=job_paths.output_audio_path,
        output_description_path=job_paths.output_description_path,
        output_video_path=job_paths.output_video_path,
    )

    return JobCreateResponse(job_id=job_id, status=JobStatus.QUEUED, message="Job queued")


@router.get("/{job_id}", response_model=JobStatusResponse, summary="Get job status")
def get_job_status(
    job_id: str,
    request: Request,
    job_store: JobStore = Depends(get_job_store),
) -> JobStatusResponse:
    """Return current status and artifact URLs for the given job id."""
    job_record = job_store.get(job_id)
    if not job_record:
        raise HTTPException(status_code=404, detail="Job not found")

    return _build_job_status_response(request, job_record)
