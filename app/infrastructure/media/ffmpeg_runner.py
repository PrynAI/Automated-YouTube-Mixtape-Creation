"""Thin wrapper around ffmpeg subprocess execution."""

from __future__ import annotations

import subprocess

from app.core.exceptions import ProcessingError


def run_ffmpeg_command(command: list[str]) -> None:
    """Execute an ffmpeg command and raise a domain error on failure."""
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise ProcessingError(
            "FFmpeg binary not found. Install ffmpeg and ensure it is available in PATH."
        ) from exc
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        raise ProcessingError(f"FFmpeg failed: {stderr or 'unknown error'}") from exc
