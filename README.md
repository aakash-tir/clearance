# Clearance

A self-hosted company assistant. A company picks any open-source LLM and loads its
documents, and each employee only gets answers from documents their Entra ID groups allow.
The CEO can ask about anything; HR asking about finance gets "that's outside what you can
access". Access is enforced by the database (a filter inside the vector search plus
Postgres row-level security), not by asking the model to behave.

A portfolio and learning project. See `plan.md` for scope and milestones and
`docs/learning/` for explanations of every concept, file and test.

## Status

M0 scaffold: health endpoint, React shell, CI. Building M1 next.

## Run it

**Backend** (Python 3.13, [uv](https://docs.astral.sh/uv/)):
```bash
cd backend
uv sync
uv run uvicorn clearance.main:app --reload     # http://127.0.0.1:8000/health
```

**Frontend** (Node 20.19+):
```bash
cd frontend
npm ci
npm run dev                                    # http://localhost:5173
```

## Test it (the same checks CI runs)

```bash
cd backend  && uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest
cd frontend && npm run lint && npm run typecheck && npm test && npm run build
```

## Layout

| Path | What's there |
|---|---|
| `backend/` | FastAPI service (`src/clearance/`) and its tests |
| `frontend/` | React + TypeScript + Vite app |
| `docs/research/` | Competitors, why permission-aware RAG, stack choices |
| `docs/learning/` | Concepts, file guide, test guide, milestone recaps |
| `logs/` | Day-by-day record of what changed and why |
| `.claude/` | Rules for Claude Code sessions working on this repo |
