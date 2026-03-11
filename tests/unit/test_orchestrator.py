"""Unit tests for end-to-end pipeline orchestration (without video output)."""

from __future__ import annotations

from pathlib import Path

from pydub import AudioSegment

from app.core.config import get_settings
from app.domain.models import PipelineInput, PipelineOptions
from app.services.pipeline.mixtape_orchestrator import run_mixtape_pipeline


def test_run_mixtape_pipeline_without_image(tmp_path: Path) -> None:
    """Pipeline should generate audio+description successfully when no image is provided."""
    audio_dir = tmp_path / "audio"
    audio_dir.mkdir(parents=True)

    AudioSegment.silent(duration=3000).export(audio_dir / "01.wav", format="wav")
    AudioSegment.silent(duration=3000).export(audio_dir / "02.wav", format="wav")

    output_audio = tmp_path / "out.wav"
    output_description = tmp_path / "description.txt"
    output_video = tmp_path / "out.mp4"

    pipeline_input = PipelineInput(
        job_id="test",
        audio_dir=audio_dir,
        output_audio_path=output_audio,
        output_description_path=output_description,
        output_video_path=output_video,
        image_path=None,
        options=PipelineOptions(transition_ms=1000, mixtape_name="Unit Mix", genre="House"),
    )

    result = run_mixtape_pipeline(pipeline_input, get_settings())

    assert result.output_audio_path.exists()
    assert result.output_description_path.exists()
    assert result.output_video_path is None
    assert len(result.track_infos) == 2
