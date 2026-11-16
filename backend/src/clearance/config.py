"""Application settings, read from environment variables.

Every setting has a safe local-development default, so the app starts with no
configuration. In other environments the values come from `CLEARANCE_*` environment
variables (or a local `.env` file, which is gitignored).
"""

from enum import StrEnum

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    """Where the app is running. Anything else is rejected at startup."""

    DEV = "dev"
    TEST = "test"
    PROD = "prod"


class Settings(BaseSettings):
    """All configuration in one typed object.

    Pydantic checks types when the object is created, so a typo such as
    CLEARANCE_ENVIRONMENT=prodd fails at startup instead of somewhere later.
    """

    model_config = SettingsConfigDict(env_prefix="CLEARANCE_", env_file=".env", extra="ignore")

    environment: Environment = Environment.DEV

    # The model server (Ollama in dev, vLLM in production). Both speak the
    # OpenAI-compatible API, so swapping the model is only a change to these values.
    model_base_url: AnyHttpUrl = AnyHttpUrl("http://localhost:11434/v1")
    chat_model: str = "qwen3.5:9b"
    embedding_model: str = "bge-m3"


def get_settings() -> Settings:
    """Build settings from the current environment.

    A function (not a module-level constant) so tests can change environment
    variables and get fresh settings.
    """
    return Settings()
