"""Unit tests for description text generation service."""

from __future__ import annotations

from pathlib import Path

from app.domain.models import TrackInfo
from app.services.metadata.description import build_youtube_description


def test_build_youtube_description_uses_track_start_timestamps() -> None:
    """Generated description should include overlap-aware timestamp positions."""
    tracks = [
        TrackInfo(filename="A.mp3", path=Path("A.mp3"), duration_ms=120000, start_ms=0),
        TrackInfo(filename="B.mp3", path=Path("B.mp3"), duration_ms=120000, start_ms=114000),
    ]

    description = build_youtube_description(
        tracks=tracks,
        mixtape_name="Test Mix",
        genre="House",
    )

    assert "00:00 - A" in description
    assert "01:54 - B" in description
