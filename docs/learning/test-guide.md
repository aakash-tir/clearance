# Test guide

Every test in the project: what it checks, which bug or leak it would catch, and why it's
written that way. Each PR that adds or changes a test updates this file.

**How to run everything:**
```bash
cd backend  && uv run pytest          # backend tests
cd frontend && npm test               # frontend tests
```

**Test levels used here** (see `concepts.md` → Test levels): unit, integration (real
Postgres), leak (`@pytest.mark.leak`, the merge gate).

All M0 tests were checked to fail when the code is broken: renaming the heading to
"Clearence" failed a frontend test, and changing `/health`'s status to "up" failed a
backend test.

---

## Backend

### `tests/test_config.py`

| Test | What it checks | Bug it would catch | Why written this way |
|---|---|---|---|
| `test_defaults_work_with_no_configuration` | With no `CLEARANCE_*` env vars, settings load with dev defaults (environment `dev`, Ollama URL). | Someone adds a required setting with no default, so a fresh clone can't start. | `monkeypatch.delenv` removes any env vars on your machine, and `_env_file=None` ignores a local `.env`, so the test sees a truly empty config. |
| `test_environment_variables_override_defaults` | `CLEARANCE_MODEL_BASE_URL` and `CLEARANCE_CHAT_MODEL` change the model server and model. | Model choice gets hard-coded, breaking the plan's "the model is swappable" promise. | Uses a vLLM-style URL and a different model name, the exact swap the plan describes. |
| `test_unknown_environment_is_rejected` | `CLEARANCE_ENVIRONMENT=prodd` raises `ValidationError`. | A typo silently runs production with dev behaviour. | `Environment` is an enum, so only `dev`/`test`/`prod` are valid; the test proves the enum is enforced. |
| `test_model_url_must_be_a_url` | A malformed model URL raises `ValidationError`. | A bad URL is only discovered when the first question fails, far from the cause. | `AnyHttpUrl` validates at startup: fail fast, close to the mistake. |

### `tests/test_health.py`

| Test | What it checks | Bug it would catch | Why written this way |
|---|---|---|---|
| `test_health_reports_ok_version_and_environment` | `GET /health` returns 200 and exactly `{status, version, environment}`. | The endpoint breaks, changes shape, or reports the wrong environment. Docker health checks and monitoring rely on it. | `TestClient` calls the app in-process (no real server). Comparing the whole JSON (not one field) catches extra or missing fields. Builds the app with explicit `Settings(environment=TEST)` so the result doesn't depend on your machine. |
| `test_unknown_route_returns_404` | A non-existent path returns 404. | A catch-all route that answers everything, which could expose data on unexpected URLs. | Simple guard; becomes more meaningful once real routes exist. |

---

## Frontend

### `src/App.test.tsx`

| Test | What it checks | Bug it would catch | Why written this way |
|---|---|---|---|
| `shows the product name as the main heading` | An `<h1>` named "Clearance" is rendered. | App crashes on render, or the heading is lost or misnamed. | `getByRole('heading', { level: 1 })` queries like a screen reader, so it also checks the heading is semantically correct, not just styled text. |
| `tells the user that answers are limited to what they can access` | The explanation sentence is shown. | The key product promise disappears from the UI. | Case-insensitive regex so small wording changes elsewhere don't break it, but removing the promise does. |
