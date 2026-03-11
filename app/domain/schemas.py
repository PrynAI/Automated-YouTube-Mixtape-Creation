"""Typed dictionary contracts used for lightweight structured payloads."""

from __future__ import annotations

from typing import TypedDict


class TrackDict(TypedDict):
    """Serialized track timing payload used in API responses."""

    filename: str
    start_ms: int
    duration_ms: int
