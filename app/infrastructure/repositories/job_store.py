"""Thread-safe in-memory repository for job records."""

from __future__ import annotations

from dataclasses import replace
from threading import Lock

from app.domain.models import JobRecord, JobStatus


class JobStore:
    """Store and update job records safely across worker threads."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._jobs: dict[str, JobRecord] = {}

    def create(self, job_id: str) -> JobRecord:
        """Create and register a new queued job record."""
        record = JobRecord(job_id=job_id, status=JobStatus.QUEUED, message="Job queued")
        with self._lock:
            self._jobs[job_id] = record
        return record

    def get(self, job_id: str) -> JobRecord | None:
        """Fetch a job record by id, if present."""
        with self._lock:
            return self._jobs.get(job_id)

    def update(self, job_id: str, **changes: object) -> JobRecord:
        """Apply field updates to an existing job record and return it."""
        with self._lock:
            current = self._jobs[job_id]
            updated = replace(current, **changes)
            self._jobs[job_id] = updated
        return updated
