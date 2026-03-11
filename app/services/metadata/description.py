"""Description text generation service for YouTube tracklists."""

from __future__ import annotations

from pathlib import Path

from app.domain.models import TrackInfo

DEFAULT_HASHTAGS = [
    "#AfroHouse",
    "#HouseMusic",
    "#EDM",
    "#DanceMusic",
    "#Mixtape",
    "#ElectronicMusic",
    "#DJMix",
    "#PartyMusic",
    "#DeepHouse",
    "#AfroHouseVibes",
]


def _format_timestamp(milliseconds: int) -> str:
    """Convert millisecond offsets into `mm:ss` format."""
    total_seconds = max(0, milliseconds // 1000)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


def build_youtube_description(
    tracks: list[TrackInfo],
    mixtape_name: str,
    genre: str,
    hashtags: list[str] | None = None,
) -> str:
    """Generate a formatted description string with timestamps and hashtags."""
    tag_values = hashtags if hashtags else DEFAULT_HASHTAGS

    lines: list[str] = [
        f"🔥 {mixtape_name} 🔥",
        f"Genre: {genre}",
        "",
        "🎵 Tracklist:",
    ]

    for track in tracks:
        timestamp = _format_timestamp(track.start_ms)
        track_name = Path(track.filename).stem
        lines.append(f"{timestamp} - {track_name}")

    lines.extend(
        [
            "",
            "💽 Download/Listen links:",
            "Find the original tracks on your preferred platforms.",
            "",
            "🎧 Follow for more mixes!",
            "",
            " ".join(tag_values),
        ]
    )

    return "\n".join(lines)


def save_description(description: str, output_path: Path) -> None:
    """Persist generated description text to disk."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(description, encoding="utf-8")
