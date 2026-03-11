"""Local filesystem persistence helpers for uploaded files."""

from __future__ import annotations

from pathlib import Path

import aiofiles
from fastapi import UploadFile

from app.core.exceptions import ValidationError


def sanitize_filename(filename: str) -> str:
    """Normalize a user-provided filename and prevent empty values."""
    safe_name = Path(filename).name.strip()
    if not safe_name:
        raise ValidationError("Filename is empty.")
    return safe_name


async def save_upload_file(upload_file: UploadFile, destination_dir: Path) -> Path:
    """Persist one uploaded file to disk and return its final path."""
    safe_name = sanitize_filename(upload_file.filename or "")
    destination_dir.mkdir(parents=True, exist_ok=True)

    destination = destination_dir / safe_name
    async with aiofiles.open(destination, "wb") as file_handle:
        content = await upload_file.read()
        await file_handle.write(content)

    await upload_file.close()
    return destination
