"""Unit tests for static-image video rendering service."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.core.exceptions import ProcessingError
from app.services.video.image_video import create_video_from_static_image


def test_create_video_from_static_image_raises_for_missing_image(tmp_path: Path) -> None:
    """Renderer should fail fast when the image path does not exist."""
    audio_path = tmp_path / "audio.mp3"
    audio_path.write_bytes(b"dummy")

    with pytest.raises(ProcessingError):
        create_video_from_static_image(
            image_path=tmp_path / "missing.png",
            audio_path=audio_path,
            output_path=tmp_path / "out.mp4",
            ffmpeg_binary="ffmpeg",
        )
