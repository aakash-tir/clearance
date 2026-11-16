# Clearance backend

FastAPI service. See the root `README.md` for setup and `docs/learning/` for explanations.

```bash
uv sync                 # install
uv run uvicorn clearance.main:app --reload   # run on http://127.0.0.1:8000
uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest   # the gate
```
