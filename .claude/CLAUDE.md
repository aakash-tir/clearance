# Clearance

A self-hosted company assistant: a company picks any open-source LLM, loads its documents,
and each employee only gets answers from documents their Entra ID groups allow. Access is
enforced by the database (filter inside the vector search + Postgres row-level security),
never by asking the model to behave. **A portfolio and learning project:** the owner must
understand every line, so the learning-mode rules below override the usual pace.

See `@.claude/project-context.md` for the architecture, auth model, data model and known
gaps. The full plan is `plan.md`; research is in `docs/research/`.

## Learning mode (required, overrides speed)
The owner is learning from this project. Follow `.claude/rules/learning-mode.md` in every
session. In short:
- **One concept per issue and per PR.** Small diffs.
- **Explain every changed file** (what / why / how it fits) and **every test** (what it
  checks / which bug or leak it catches / why it's written that way), in the PR body
  (template sections are required) and in your reply.
- **Explain every correction:** what was wrong, the evidence, why the fix works.
- **Options before decisions:** for any real design choice, lay out options and trade-offs
  and ask the owner before choosing.
- Keep `docs/learning/concepts.md` and `docs/learning/test-guide.md` current in the same PR.
- **Clarity over cleverness.** Explicit, readable code with docstrings that say why.

## Tech stack
- **Backend** (`backend/`): Python 3.13, FastAPI, SQLModel, Alembic, pydantic-settings;
  managed with **uv**. HTTP client and test transport: **httpx2**.
- **Database:** Postgres 17 + pgvector, with row-level security on document and chunk tables.
- **Models:** any OpenAI-compatible server. Ollama in dev (`qwen3.5:9b` chat, `bge-m3`
  embeddings), vLLM for production. All model calls go through one client module.
- **Identity:** Entra ID (OIDC login; Microsoft Graph group sync with delta queries).
  ACLs store Entra **object IDs only**, never names or emails.
- **Frontend** (`frontend/`): React 19 + TypeScript + Vite 8, MSAL React (from M6), oxlint,
  Vitest 4 + Testing Library.
- **CI:** GitHub Actions, `backend.yml` and `frontend.yml`, PR-only and path-filtered.

## Conventions
- `backend/src/clearance/` is the package; tests in `backend/tests/` mirror its layout.
- Settings only via `clearance.config.Settings` (`CLEARANCE_*` env vars). No secrets in code.
- **Security rules that must never be broken:**
  - Filter by permission **inside** the search query, never after retrieval.
  - **Deny by default:** a document with no ACL is visible to nobody but admins.
  - Every new query path over documents/chunks gets a leak test (`@pytest.mark.leak`).
  - Tests never call Entra or a real model: use locally signed tokens and fake clients.
- pytest markers: `integration` (needs Postgres), `leak` (no-leak proof, merge gate).
- **Testing / local gate:**
  - Backend: `cd backend && uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest`
  - Frontend: `cd frontend && npm run lint && npm run typecheck && npm test && npm run build`
- Frontend: Vitest 5 failed to install under npm 10.8 on the dev machine (arborist
  "edgesOut" error), so Vitest is pinned to `^4.1`.

## Git workflow (required)
This repo has a GitHub remote, so `main` is protected:
- **Never commit directly to `main`** and never merge into it locally. All changes
  land on a branch and reach `main` only through a GitHub pull request.
- Enforced locally by `.claude/hooks/protect-main.sh` (wired as a PreToolUse hook in
  `.claude/settings.json`), which denies `git commit`/`git merge`/`git push` against
  `main`.
- Workflow: branch → commit → push the branch → open a PR → merge the PR → pull `main`.

## Issues, PRs and CI (required)
- **One issue = one thing:** a single base, one PR in size. Milestones mirror the plan's
  phases (`M0`…`M7`) and hold several issues.
- **One PR per issue.** Branch `<type>/<issue#>-<slug>`; PR body starts with `Closes #n`.
- **Never merge unless every CI check is green**, verified with `gh pr checks --watch`.
  Merge with `gh pr merge --squash --delete-branch`.
- Out-of-scope bugs found mid-branch become **new issues**, not scope creep.
- The work loop is in `.claude/rules/issue-workflow.md` and is followed in every dev session.
- `docs/future.md` holds only *unscheduled* ideas. Once scheduled into a milestone, an
  item becomes an issue and leaves `future.md`.

## CI (required)
CI is lean on GitHub Actions minutes: workflows run on pull requests only (nothing on
the merge to `main`), each only when its own files change, and docs-only PRs (`docs/`,
`logs/`, `graphify-out/`, `*.md`) run none. Never merge a PR with a red or pending
check; a docs-only PR with no checks may merge. Don't add a `push: main` trigger or a
separate follow-up PR for docs or the graph: each costs a CI run.

## Before every PR merge (required)
Two artifacts must be kept current, together, **in the same PR**:
1. **Knowledge graph:** once the code is final, run `graphify update .` and commit
   the refreshed `graphify-out/` to the PR. This is the only refresh: there are no
   graphify git hooks.
2. **Architecture diagram:** update `docs/architecture/architecture-diagram.html`
   whenever the merged PR changed the architecture: components, stages,
   data stores/collections, external services, flows, schedules, or
   retention rules. Use the `architecture-diagram` skill's MANUAL
   workflow (hand-placed layout per its design system) and verify the
   render with a headless-browser screenshot before committing.
   Auto-generated output is a draft scaffold only. Docs-only or purely
   cosmetic merges don't need a diagram update, but say so in the
   changelog entry.

Both artifacts may be empty or absent on a brand-new project. The first merge that
introduces real structure is the one that creates them.

## Backlog (required)
All future work (bugs, known gaps, feature ideas, scaling items) is recorded in
`docs/future.md` (dated bullet under the matching section). When you find or defer an
issue, add it there; when one is COMPLETE, remove it. `logs/` and the PR history are
the record of finished work (no Done section).

## Where things belong (required)
- `.claude/`: everything Claude reads: `CLAUDE.md`, `project-context.md`,
  `progress.md`, `rules/`, project agents and skills, settings and hooks.
- `docs/`: everything a person reads: `architecture/`, `future.md`, `plans/`,
  `research/`, `runbooks/`, `history/`, and `learning/` (concepts, test guide, file guide,
  milestone recaps).
- `logs/`: the dated record (below).
- The repo root stays clean: only `CLAUDE.md`, `README.md`, `plan.md`, and the
  language's required root files.

If Claude must load it to work correctly it goes in `.claude/`; if a person reads it to
understand or operate the project it goes in `docs/`. When both are true, the full
version lives in `docs/` and `.claude/CLAUDE.md` points at it.

## Change log (required)
Every day that content is added, there is exactly **one** log file: `logs/YYYY-MM-DD.md`.
Check whether today's file exists; create it if missing, append to it otherwise. Never a
file per change, never one growing log. A day with no changes has no file.

Each entry is a `##` heading naming what was done, followed by:
**What we did** · **The reason** (root cause, for fixes) · **How it was solved**.

Write the reasoning, not the diff (git already has the code). For a fix, include the
evidence that identified the root cause (traceback, version pin, timeline). Say
explicitly when a change was docs-only or cosmetic and needed no diagram update.

## Don't commit secrets
Keep `.env`, credentials, and tokens gitignored. Never hardcode API keys in source.
Entra client secrets and tenant IDs live in `.env` only (see `.env.example` once added).
