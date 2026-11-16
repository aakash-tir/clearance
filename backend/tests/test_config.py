"""Tests for clearance.config.Settings."""

import pytest
from pydantic import ValidationError

from clearance.config import Environment, Settings


def test_defaults_work_with_no_configuration(monkeypatch: pytest.MonkeyPatch) -> None:
    """A fresh checkout must start without any env vars set (dev defaults)."""
    for name in ("CLEARANCE_ENVIRONMENT", "CLEARANCE_MODEL_BASE_URL", "CLEARANCE_CHAT_MODEL"):
        monkeypatch.delenv(name, raising=False)

    settings = Settings(_env_file=None)

    assert settings.environment is Environment.DEV
    assert str(settings.model_base_url) == "http://localhost:11434/v1"


def test_environment_variables_override_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    """Swapping the model must be a config change only (the plan's 'model is not fixed')."""
    monkeypatch.setenv("CLEARANCE_MODEL_BASE_URL", "http://gpu-server:8000/v1")
    monkeypatch.setenv("CLEARANCE_CHAT_MODEL", "gemma3:12b")

    settings = Settings(_env_file=None)

    assert str(settings.model_base_url) == "http://gpu-server:8000/v1"
    assert settings.chat_model == "gemma3:12b"


def test_unknown_environment_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    """A typo like 'prodd' must fail at startup, not silently run with dev settings."""
    monkeypatch.setenv("CLEARANCE_ENVIRONMENT", "prodd")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_model_url_must_be_a_url(monkeypatch: pytest.MonkeyPatch) -> None:
    """A malformed model server address must fail at startup with a clear error."""
    monkeypatch.setenv("CLEARANCE_MODEL_BASE_URL", "not a url")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)
