"""Centralized logging setup for API and background processing."""

from __future__ import annotations

import logging
import os


LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def setup_logging() -> None:
    """Configure global logging level and format from environment."""
    level_name = os.getenv("MIXTAPE_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    logging.basicConfig(level=level, format=LOG_FORMAT)
