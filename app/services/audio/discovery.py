"""Audio track discovery and validation helpers."""

from __future__ import annotations

from pathlib import Path

from app.core.exceptions import ValidationError

AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"}


def discover_audio_tracks(audio_dir: Path) -> list[Path]:
    """Find supported audio files in a folder and return them in deterministic order."""
    if not audio_dir.exists() or not audio_dir.is_dir():
        raise ValidationError(f"Audio directory not found: {audio_dir}")

    tracks = [
        file_path
        for file_path in audio_dir.iterdir()
        if file_path.is_file() and file_path.suffix.lower() in AUDIO_EXTENSIONS
    ]

    if not tracks:
        raise ValidationError("No supported audio files found.")

    return sorted(tracks, key=lambda item: item.name.lower())
