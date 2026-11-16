"""Tests for the /health endpoint."""

from fastapi.testclient import TestClient

from clearance import __version__
from clearance.config import Environment, Settings
from clearance.main import create_app


def test_health_reports_ok_version_and_environment() -> None:
    """The endpoint answers 200 with the running version and environment."""
    client = TestClient(create_app(Settings(environment=Environment.TEST)))

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": __version__, "environment": "test"}


def test_unknown_route_returns_404() -> None:
    """Routes that don't exist must not accidentally answer (guards against catch-all routes)."""
    client = TestClient(create_app(Settings(environment=Environment.TEST)))

    assert client.get("/does-not-exist").status_code == 404
