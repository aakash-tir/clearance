"""FastAPI application entry point.

Run locally with:  uv run uvicorn clearance.main:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel

from clearance import __version__
from clearance.config import Settings, get_settings


class HealthResponse(BaseModel):
    """What /health returns. A typed model so the API docs show the exact shape."""

    status: str
    version: str
    environment: str


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the app. Tests pass their own settings; production reads the environment."""
    settings = settings or get_settings()
    app = FastAPI(title="Clearance", version=__version__)

    @app.get("/health")
    def health() -> HealthResponse:
        """Liveness check: the process is up. Says nothing about the database yet."""
        return HealthResponse(
            status="ok", version=__version__, environment=settings.environment.value
        )

    return app


app = create_app()
