"""Request-side DTO definitions for API endpoints."""

from __future__ import annotations

from pydantic import BaseModel, Field


class JobCreateOptions(BaseModel):
    """Validated user options sent when creating a new processing job."""

    transition_ms: int = Field(default=6000, ge=0, le=60000)
    mixtape_name: str = Field(default="Pryn House Mixtape", min_length=1, max_length=120)
    genre: str = Field(default="Pryn House", min_length=1, max_length=80)
