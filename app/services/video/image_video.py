"""Video rendering service that combines one image with one audio track."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from app.core.exceptions import ProcessingError
from app.infrastructure.media.ffmpeg_runner import run_ffmpeg_command


def create_video_from_static_image(
    image_path: Path,
    audio_path: Path,
    output_path: Path,
    ffmpeg_binary: str,
    video_resolution: tuple[int, int] = (1280, 720),
    preset: str = "ultrafast",
    fps: int = 1,
) -> None:
    """Render an MP4 whose visuals are a looped static image for audio duration."""
    if not image_path.exists():
        raise ProcessingError(f"Image not found: {image_path}")
    if not audio_path.exists():
        raise ProcessingError(f"Audio not found: {audio_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    resized_image_path = output_path.parent / f"{output_path.stem}_resized_temp.jpg"

    try:
        image = Image.open(image_path)
        image = image.resize(video_resolution)
        image.save(resized_image_path)

        command = [
            ffmpeg_binary,
            "-y",
            "-loop",
            "1",
            "-i",
            str(resized_image_path),
            "-i",
            str(audio_path),
            "-c:v",
            "libx264",
            "-preset",
            preset,
            "-tune",
            "stillimage",
            "-r",
            str(fps),
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(output_path),
        ]
        run_ffmpeg_command(command)
    except OSError as exc:
        raise ProcessingError(f"Failed to process image/video: {exc}") from exc
    finally:
        if resized_image_path.exists():
            resized_image_path.unlink()
