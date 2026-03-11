"""Integration tests for basic API reachability and routing behavior."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.api.main import create_app


def test_health_check() -> None:
    """Health endpoint should return a successful status payload."""
    app = create_app()
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_unknown_job_returns_404() -> None:
    """Unknown job ids should return an HTTP 404."""
    app = create_app()
    client = TestClient(app)

    response = client.get("/api/v1/jobs/not-found")

    assert response.status_code == 404
