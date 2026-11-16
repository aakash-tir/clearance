# Scaffold file guide (M0)

Every file created by the initial setup: what it is, why it exists, and how it fits.
Later PRs explain their own files in the PR body; this page covers the starting point.

## Repo root

| File | What it is | Why it exists |
|---|---|---|
| `plan.md` | The project plan: scope, stack, architecture, milestones. | Single source of truth for *what* we're building and in what order. The original brief is in `docs/history/plan-original.md`. |
| `README.md` | How to run the project and where things are. | First thing anyone (or an interviewer) reads. |
| `CLAUDE.md` | One line `@.claude/CLAUDE.md` plus graphify's section. | Claude Code loads the root `CLAUDE.md` automatically; the `@` import pulls in the real instructions so they live inside `.claude/`. |
| `.gitignore` | Files git must never track. | Keeps secrets (`.env`, keys), virtualenvs, `node_modules` and build output out of the repo. Written *before* the first commit so no secret can slip in. |

## `.claude/`: instructions for Claude Code

| File | What it is | Why it exists |
|---|---|---|
| `CLAUDE.md` | Project rules: stack, conventions, security rules, git/CI rules, learning mode. | Every development session starts by reading this, so the rules are followed without being repeated. |
| `project-context.md` | Architecture, auth model, data model, security invariants, known gaps. | The long reference; `CLAUDE.md` stays short and points here. |
| `progress.md` | Where the project is right now. | Lets a new session pick up without re-reading history. |
| `rules/learning-mode.md` | How every change must be explained (files, tests, fixes). | Your requirement to understand every step, written as a rule so it can't be skipped. |
| `rules/issue-workflow.md` | The issue → branch → PR → green CI → merge loop. | Makes every change small, reviewable and tested. |
| `rules/frontend/react.md` | Empty placeholder. | Will hold React-specific conventions from M6. |
| `settings.json` | Hook wiring for Claude Code. | Runs `protect-main.sh` before git commands, plus graphify's hooks that point Claude at the knowledge graph. |
| `hooks/protect-main.sh` | A script that blocks `git commit/merge/push` on `main`. | GitHub's server-side protection may need a paid plan on private repos; this enforces "PRs only" locally. |
| `skills/architecture-diagram/` | Copy of the diagram skill. | So the diagram workflow travels with the repo. |
| `settings.local.json`, `CLAUDE.local.json`, `.mcp.json`, `agents/` | Empty placeholders. | Standard layout; local files are gitignored. |

## `.github/`: GitHub configuration

| File | What it is | Why it exists |
|---|---|---|
| `workflows/backend.yml` | CI: install with uv, then ruff (lint), ruff format check, mypy (types), pytest. | Proves every backend PR is clean and tested before merge. Runs only when `backend/` changes, only on PRs, to save Actions minutes. |
| `workflows/frontend.yml` | CI: `npm ci`, oxlint, `tsc -b`, Vitest, Vite build. | Same, for `frontend/`. |
| `pull_request_template.md` | The PR body skeleton. | Forces the per-file and per-test explanation tables (learning mode) and the merge checklist. |
| `ISSUE_TEMPLATE/feature.yml` | Issue form with Context, **What you will learn**, Scope, Acceptance criteria. | Every issue states its learning goal up front. |
| `ISSUE_TEMPLATE/bug.yml` | Bug issue form. | Requires a test that fails before the fix. |

## `backend/`: Python service

| File | What it is | Why it exists |
|---|---|---|
| `pyproject.toml` | Package metadata, dependencies, and tool config (pytest, ruff, mypy). | One file defines the whole Python project. `[dependency-groups] dev` holds test/lint tools that production doesn't need. pytest markers `integration` and `leak` are declared here so a typo in a marker name fails (`--strict-markers`). |
| `uv.lock` | Exact versions of every installed package. | Everyone (and CI, via `uv sync --locked`) gets identical versions, so "works on my machine" can't happen. |
| `README.md` | Backend run commands. | Quick reference. |
| `src/clearance/__init__.py` | Marks `clearance` as a package; holds `__version__`. | One place for the version, shown by `/health`. The `src/` layout means tests import the *installed* package, catching packaging mistakes. |
| `src/clearance/config.py` | `Settings`: typed configuration from `CLEARANCE_*` env vars. | Fails fast on bad config (e.g. `prodd`). Holds the model server URL and model names, which is how the model stays swappable. |
| `src/clearance/main.py` | `create_app()` builds the FastAPI app; `/health` endpoint. | A factory function (not just a global) lets tests build an app with their own settings. `/health` is how Docker and you check the server is up. |
| `tests/test_config.py` | Tests for settings. | See `test-guide.md`. |
| `tests/test_health.py` | Tests for `/health`. | See `test-guide.md`. |

## `frontend/`: React app

| File | What it is | Why it exists |
|---|---|---|
| `package.json` / `package-lock.json` | Dependencies and scripts (`dev`, `build`, `lint`, `typecheck`, `test`). | Lockfile pins exact versions; CI uses `npm ci` to install exactly those. |
| `index.html` | The page Vite serves; loads `src/main.tsx`. | Entry point of the web app. |
| `vite.config.ts` | Vite build config + Vitest config (jsdom, setup file). | One config for building and testing. |
| `tsconfig*.json` | TypeScript settings for app code and for config files. | Strict type checking catches mistakes before runtime. |
| `src/main.tsx` | Mounts `<App />` into the page. | React's starting point. |
| `src/App.tsx` | The app shell (title + one sentence). | Placeholder until M6 adds login and chat. |
| `src/index.css` | Minimal styles. | Readable layout, light and dark. |
| `src/test-setup.ts` | Runs before tests: adds DOM matchers, cleans up after each test. | Keeps tests independent of each other. |
| `src/App.test.tsx` | Tests for the shell. | See `test-guide.md`. |
| `public/favicon.svg` | Browser tab icon from the template. | Cosmetic. |

## `docs/`: for people

| Path | What's there |
|---|---|
| `research/` | Market and competitors, why permission-aware RAG, stack choices: each with sources. |
| `learning/` | `concepts.md` (glossary), this file, `test-guide.md`, and milestone recaps later. |
| `history/plan-original.md` | Your original brief. |
| `future.md` | Backlog of unscheduled ideas. |
| `architecture/` | The architecture diagram (created when there's real architecture, M1+). |

## Other

| Path | What it is |
|---|---|
| `logs/YYYY-MM-DD.md` | One file per working day: what was done, why, how. |
| `graphify-out/` | The knowledge graph of the code (refreshed in each PR with `graphify update .`). |
