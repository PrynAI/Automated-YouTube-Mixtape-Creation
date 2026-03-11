"""Quick manual smoke test for the full media pipeline using sample assets."""

from __future__ import annotations

from pathlib import Path

from app.core.config import get_settings
from app.domain.models import PipelineInput, PipelineOptions
from app.services.pipeline.mixtape_orchestrator import run_mixtape_pipeline


def main() -> None:
    """Run one pipeline execution against sample files and print artifact paths."""
    settings = get_settings()
    job_id = "smoke_test"

    input_audio_dir = Path("experiment_notebooks/input_mp3files")
    image_path = Path("experiment_notebooks/images/image.png")

    pipeline_input = PipelineInput(
        job_id=job_id,
        audio_dir=input_audio_dir,
        output_audio_path=settings.output_audio_dir / f"{job_id}_mixtape.mp3",
        output_description_path=settings.output_description_dir / f"{job_id}_description.txt",
        output_video_path=settings.output_video_dir / f"{job_id}_mixtape.mp4",
        image_path=image_path,
        options=PipelineOptions(transition_ms=6000, mixtape_name="Smoke Test", genre="House"),
    )

    result = run_mixtape_pipeline(pipeline_input, settings)
    print(f"Audio: {result.output_audio_path}")
    print(f"Description: {result.output_description_path}")
    print(f"Video: {result.output_video_path}")


if __name__ == "__main__":
    main()
