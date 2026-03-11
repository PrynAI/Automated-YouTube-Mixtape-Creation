"""HTTP client helpers used by Streamlit pages to talk to the FastAPI backend."""

from __future__ import annotations

import os
from typing import Any

import requests

API_BASE_URL = os.getenv("MIXTAPE_API_URL", "http://localhost:8000")


class ApiClientError(Exception):
    """Raised when API calls fail and the UI needs a readable error."""


def _raise_for_status(response: requests.Response) -> None:
    """Translate HTTP errors into `ApiClientError` for UI-friendly handling."""
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        detail = response.text
        raise ApiClientError(detail) from exc


def create_job(
    audio_payloads: list[dict[str, Any]],
    image_payload: dict[str, Any] | None,
    transition_ms: int,
    mixtape_name: str,
    genre: str,
) -> dict[str, Any]:
    """Submit a multipart job request with uploaded media and job options."""
    files: list[tuple[str, tuple[str, bytes, str]]] = []

    for audio in audio_payloads:
        files.append(
            (
                "audio_files",
                (
                    str(audio["name"]),
                    audio["bytes"],
                    str(audio.get("type") or "audio/mpeg"),
                ),
            )
        )

    if image_payload:
        files.append(
            (
                "image_file",
                (
                    str(image_payload["name"]),
                    image_payload["bytes"],
                    str(image_payload.get("type") or "image/png"),
                ),
            )
        )

    data = {
        "transition_ms": str(transition_ms),
        "mixtape_name": mixtape_name,
        "genre": genre,
    }

    response = requests.post(
        f"{API_BASE_URL}/api/v1/jobs",
        files=files,
        data=data,
        timeout=300,
    )
    _raise_for_status(response)
    return response.json()


def get_job_status(job_id: str) -> dict[str, Any]:
    """Fetch current status details for a job id."""
    response = requests.get(f"{API_BASE_URL}/api/v1/jobs/{job_id}", timeout=30)
    _raise_for_status(response)
    return response.json()


def fetch_text_file(file_url: str) -> str:
    """Download a text artifact (description file) from the backend."""
    response = requests.get(file_url, timeout=30)
    _raise_for_status(response)
    return response.text
