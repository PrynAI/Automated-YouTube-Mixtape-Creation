"""Audio mixing service for overlap-based fade transitions."""

from __future__ import annotations

from pathlib import Path

from pydub import AudioSegment

from app.core.exceptions import ProcessingError
from app.domain.models import TrackInfo


def create_smooth_fade_mixtape(
    tracks: list[Path],
    output_path: Path,
    transition_ms: int,
) -> list[TrackInfo]:
    """Mix tracks into one audio file and return overlap-aware track timing metadata."""
    if transition_ms < 0:
        raise ProcessingError("Transition must be non-negative.")
    if not tracks:
        raise ProcessingError("At least one track is required to create a mixtape.")

    mixed_audio: AudioSegment | None = None
    track_infos: list[TrackInfo] = []
    current_start_ms = 0

    for track_path in tracks:
        song = AudioSegment.from_file(track_path)
        song = song.set_channels(2).set_frame_rate(44100)
        duration_ms = len(song)

        track_infos.append(
            TrackInfo(
                filename=track_path.name,
                path=track_path,
                duration_ms=duration_ms,
                start_ms=current_start_ms,
            )
        )

        if mixed_audio is None:
            mixed_audio = song
            current_start_ms += duration_ms
            continue

        overlap = min(transition_ms, duration_ms, len(mixed_audio))

        # Build one transition segment where outgoing and incoming tracks overlap.
        outgoing = mixed_audio[-overlap:].fade_out(overlap).low_pass_filter(4000)
        incoming = song[:overlap].fade_in(overlap).low_pass_filter(4000)
        transition = outgoing.overlay(incoming)

        mixed_audio = mixed_audio[:-overlap] + transition + song[overlap:]
        current_start_ms += duration_ms - overlap

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if mixed_audio is None:
        raise ProcessingError("Failed to create mixed audio.")

    export_format = output_path.suffix.lstrip(".") or "mp3"
    mixed_audio.export(output_path, format=export_format)
    return track_infos
