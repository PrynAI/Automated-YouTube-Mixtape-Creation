"""Path factory for job-scoped upload and artifact locations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.core.config import Settings


@dataclass(frozen=True)
class JobPaths:
    """Concrete filesystem locations used while processing one job."""

    job_id: str
    upload_audio_dir: Path
    upload_image_dir: Path
    output_audio_path: Path
    output_description_path: Path
    output_video_path: Path


def get_job_paths(settings: Settings, job_id: str) -> JobPaths:
    """Create and return all upload/output paths for a job id."""
    upload_audio_dir = settings.upload_audio_dir / job_id
    upload_image_dir = settings.upload_image_dir / job_id

    output_audio_path = settings.output_audio_dir / f"{job_id}_mixtape.mp3"
    output_description_path = settings.output_description_dir / f"{job_id}_description.txt"
    output_video_path = settings.output_video_dir / f"{job_id}_mixtape.mp4"

    upload_audio_dir.mkdir(parents=True, exist_ok=True)
    upload_image_dir.mkdir(parents=True, exist_ok=True)

    return JobPaths(
        job_id=job_id,
        upload_audio_dir=upload_audio_dir,
        upload_image_dir=upload_image_dir,
        output_audio_path=output_audio_path,
        output_description_path=output_description_path,
        output_video_path=output_video_path,
    )
