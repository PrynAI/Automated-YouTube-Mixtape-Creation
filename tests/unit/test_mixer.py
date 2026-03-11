"""Unit tests for overlap-based audio mixer behavior."""

from __future__ import annotations

from pathlib import Path

from pydub import AudioSegment

from app.services.audio.mixer import create_smooth_fade_mixtape


def test_create_smooth_fade_mixtape_generates_track_starts(tmp_path: Path) -> None:
    """Mixer should emit an output file and correct start offsets for tracks."""
    track1 = tmp_path / "01_first.wav"
    track2 = tmp_path / "02_second.wav"

    AudioSegment.silent(duration=5000).export(track1, format="wav")
    AudioSegment.silent(duration=4000).export(track2, format="wav")

    output = tmp_path / "mix.wav"
    tracks = create_smooth_fade_mixtape([track1, track2], output_path=output, transition_ms=1000)

    assert output.exists()
    assert len(tracks) == 2
    assert tracks[0].start_ms == 0
    assert tracks[1].start_ms == 4000
