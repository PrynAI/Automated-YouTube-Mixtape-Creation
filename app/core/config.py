"""Application configuration and filesystem path setup."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Container for runtime configuration values used across the app."""

    project_name: str
    api_v1_prefix: str
    cors_allow_origins: list[str]
    data_dir: Path
    upload_audio_dir: Path
    upload_image_dir: Path
    output_audio_dir: Path
    output_description_dir: Path
    output_video_dir: Path
    temp_dir: Path
    ffmpeg_binary: str


@lru_cache
def get_settings() -> Settings:
    """Build and cache settings from environment variables.

    The first call also ensures all required runtime directories exist.
    """

    base_data_dir = Path(os.getenv("MIXTAPE_DATA_DIR", "data"))

    settings = Settings(
        project_name=os.getenv("MIXTAPE_PROJECT_NAME", "Automated YouTube Mixtape Creation API"),
        api_v1_prefix=os.getenv("MIXTAPE_API_V1_PREFIX", "/api/v1"),
        cors_allow_origins=[
            origin.strip()
            for origin in os.getenv("MIXTAPE_CORS_ALLOW_ORIGINS", "*").split(",")
            if origin.strip()
        ],
        data_dir=base_data_dir,
        upload_audio_dir=base_data_dir / "uploads" / "audio",
        upload_image_dir=base_data_dir / "uploads" / "images",
        output_audio_dir=base_data_dir / "outputs" / "audio",
        output_description_dir=base_data_dir / "outputs" / "descriptions",
        output_video_dir=base_data_dir / "outputs" / "video",
        temp_dir=base_data_dir / "temp",
        ffmpeg_binary=os.getenv("FFMPEG_BINARY", "ffmpeg"),
    )

    for directory in [
        settings.data_dir,
        settings.upload_audio_dir,
        settings.upload_image_dir,
        settings.output_audio_dir,
        settings.output_description_dir,
        settings.output_video_dir,
        settings.temp_dir,
    ]:
        directory.mkdir(parents=True, exist_ok=True)

    return settings
