"""Core domain entities for jobs and media pipeline execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional


class JobStatus(str, Enum):
    """Lifecycle states for a processing job."""

    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True)
class TrackInfo:
    """Computed timing metadata for one track in the final mixtape."""

    filename: str
    path: Path
    duration_ms: int
    start_ms: int


@dataclass(frozen=True)
class PipelineOptions:
    """User-configurable options for mixtape generation."""

    transition_ms: int = 6000
    mixtape_name: str = "Pryn House Mixtape"
    genre: str = "Pryn House"


@dataclass(frozen=True)
class PipelineInput:
    """All required inputs and output targets for a pipeline run."""

    job_id: str
    audio_dir: Path
    output_audio_path: Path
    output_description_path: Path
    output_video_path: Optional[Path]
    image_path: Optional[Path]
    options: PipelineOptions


@dataclass(frozen=True)
class PipelineResult:
    """Artifacts produced by a completed pipeline run."""

    track_infos: list[TrackInfo]
    output_audio_path: Path
    output_description_path: Path
    output_video_path: Optional[Path]


@dataclass
class JobRecord:
    """Mutable in-memory representation of a job and its artifacts."""

    job_id: str
    status: JobStatus
    message: str = ""
    error: Optional[str] = None
    audio_output_relpath: Optional[str] = None
    description_output_relpath: Optional[str] = None
    video_output_relpath: Optional[str] = None
    tracks: list[dict[str, int | str]] = field(default_factory=list)
