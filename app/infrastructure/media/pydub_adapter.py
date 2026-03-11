"""Helpers that isolate direct pydub interactions."""

from __future__ import annotations

from pathlib import Path

from pydub import AudioSegment


def read_audio_duration_ms(audio_path: Path) -> int:
    """Read and return audio duration in milliseconds."""
    segment = AudioSegment.from_file(audio_path)
    return len(segment)
