"""Orchestrates the full mixtape generation pipeline."""

from __future__ import annotations

from app.core.config import Settings
from app.domain.models import PipelineInput, PipelineResult
from app.services.audio.discovery import discover_audio_tracks
from app.services.audio.mixer import create_smooth_fade_mixtape
from app.services.metadata.description import build_youtube_description, save_description
from app.services.video.image_video import create_video_from_static_image


def run_mixtape_pipeline(pipeline_input: PipelineInput, settings: Settings) -> PipelineResult:
    """Run discover -> mix -> describe -> optional video render and return artifacts."""
    tracks = discover_audio_tracks(pipeline_input.audio_dir)

    track_infos = create_smooth_fade_mixtape(
        tracks=tracks,
        output_path=pipeline_input.output_audio_path,
        transition_ms=pipeline_input.options.transition_ms,
    )

    description = build_youtube_description(
        tracks=track_infos,
        mixtape_name=pipeline_input.options.mixtape_name,
        genre=pipeline_input.options.genre,
    )
    save_description(description, pipeline_input.output_description_path)

    output_video_path = None
    if pipeline_input.image_path:
        create_video_from_static_image(
            image_path=pipeline_input.image_path,
            audio_path=pipeline_input.output_audio_path,
            output_path=pipeline_input.output_video_path,
            ffmpeg_binary=settings.ffmpeg_binary,
        )
        output_video_path = pipeline_input.output_video_path

    return PipelineResult(
        track_infos=track_infos,
        output_audio_path=pipeline_input.output_audio_path,
        output_description_path=pipeline_input.output_description_path,
        output_video_path=output_video_path,
    )
