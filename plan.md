# Clearance: Plan

*Expanded 2026-11-16 from the original brief (kept in `docs/history/plan-original.md`).*

## What this is

Clearance is a self-hosted company assistant. A company picks any open-source LLM, loads
in its documents, and every employee can ask questions about them. Each person only gets
answers from documents their existing Entra ID (Azure AD) groups allow. The CEO can ask
about anything; HR asking about finance gets a polite "that's outside what you can access".
Access is enforced by the database, not by asking the model to behave.

**It is a portfolio and learning project, not a product to sell.** The market already has
Microsoft 365 Copilot, Glean, Gemini Enterprise and Onyx (see
`docs/research/01-market-and-competitors.md`). The goal is to understand and show the hard
part properly: permission-aware retrieval, identity sync and proof that nothing leaks.

## How we work (this project is different)

The owner must understand every step and every line. So:

1. **Small steps.** One concept per issue and per PR.
2. **Every PR explains every changed file**: what it does, why it's needed, how it fits.
   Every bug fix explains what was wrong and why the fix works.
3. **Every test is explained**: what behaviour it checks, which bug or leak it would catch,
   and why it's written that way. Explanations go in the PR body and in
   `docs/learning/test-guide.md`.
4. **Concepts get a plain-language entry** in `docs/learning/concepts.md` the first time
   they appear, and each milestone ends with a short `docs/learning/mN-*.md` recap.
5. **Design decisions are explained before they're made**: options and trade-offs first,
   then the choice, with the owner asked on the ones that matter.
6. **Clarity over cleverness.** Readable, explicit code you can walk through in an interview.

These rules are in `.claude/CLAUDE.md` and `.claude/rules/learning-mode.md`, so every
development session follows them.

## Scope

**v1 (building now):**
- Local stack in Docker Compose: Postgres + pgvector, Ollama, backend, frontend
- Entra ID login (OIDC) and token verification in the backend
- Entra group sync via Microsoft Graph (full read, then delta queries)
- Ingest a fake company ("Acme Ltd") folder with a permissions file mapping folders to
  Entra group object IDs; chunk, embed and store with ACLs
- Permission-filtered vector search (filter inside SQL) + Postgres row-level security
- Answer generation with citations, through a swappable OpenAI-compatible model client
- Polite out-of-scope reply when nothing the user may see is relevant
- Audit log of every question and which chunks were retrieved
- Leak test suite that gates every merge
- React chat UI with Microsoft login and citations; admin "who can see what" page

**Deferred** (also in `docs/future.md`):
- SharePoint / OneDrive connector with real permission sync
- SCIM push provisioning instead of polling
- Okta / Google Workspace identity
- vLLM production deployment profile and multi-GPU
- Reranker model; hybrid keyword + vector search
- Oversharing report (documents visible to "everyone")
- Per-user answer caching
- Air-gapped install packaging

**Non-goals:**
- Fine-tuning or training models on company data
- Selling it, multi-tenant SaaS hosting, billing
- Fixing over-shared permissions in the source systems (we report them, not fix them)

## Tech stack

Full reasoning and sources: `docs/research/03-stack-choices.md`.

| Layer | Choice | Why | Rejected |
|---|---|---|---|
| Vector store + DB | Postgres 17 + pgvector, with row-level security | ACL filter in the same SQL as the vector search; RLS is a second, database-enforced lock | Qdrant (second service, ACLs copied into payloads, no DB-level lock) |
| Backend | Python 3.13, FastAPI, SQLModel, Alembic, uv | Strong RAG ecosystem; matches owner's other projects | Node/TS backend |
| Model server | Ollama (dev); vLLM documented for production | Both OpenAI-compatible, so swapping is config only | Hard-coding one provider SDK |
| Generator model | Start with installed `qwen3.5:9b`; compare Qwen 3 14B / Gemma 3 12B later | Fits 12 GB VRAM at 4-bit | 30B+ models (don't fit) |
| Embeddings | `bge-m3` via Ollama | Small, multilingual, local | Hosted embedding APIs (data leaves the box) |
| Identity | Entra ID: OIDC login + Microsoft Graph group sync | The plan's "use the company's Azure hierarchy" | Keycloak stand-in; own user database |
| Frontend | React + TypeScript + Vite, MSAL React | Demoable; standard Microsoft login library | API-only v1 |
| Tests | pytest (+ real Postgres for integration and leak tests), Vitest | Idiomatic; leak tests need real SQL and RLS | Mocked database for leak tests (would hide RLS bugs) |
| Lint/type | ruff, mypy (strict), oxlint, tsc | Catch mistakes before review; oxlint is what the Vite template now ships | ESLint (slower, more config) |
| CI | GitHub Actions, PR-only, path-filtered | Lean on free minutes | Running on push to main |

## Architecture

```
Browser (React + MSAL) --login--> Entra ID
        | Bearer token (JWT)
        v
FastAPI backend
  auth:       verify JWT (Microsoft JWKS) -> user object ID
  identity:   user -> group IDs (from synced tables)
  retrieval:  embed question -> SQL vector search
              WHERE chunk ACL overlaps user's groups (+ RLS session setting)
  generation: allowed chunks + question -> model client -> answer + citations
              no allowed chunks -> polite "out of scope"
  audit:      log user, question, chunk IDs returned
        |                          |
        v                          v
Postgres + pgvector          Ollama / vLLM (OpenAI-compatible)
  users, groups, memberships     generator model, bge-m3 embeddings
  documents (acl), chunks (vector), audit_log
  RLS policies on documents/chunks
        ^
        |
Background jobs
  group sync: Microsoft Graph (full, then delta) -> users/groups/memberships
  ingest:     Acme folder + permissions file -> documents -> chunks -> embeddings
```

**Request flow for one question:** token checked → user's group IDs loaded → database
session tagged with those IDs (RLS) → question embedded → top-k chunks searched *only among
allowed chunks* → if none are relevant enough, reply out of scope → otherwise prompt the
model with those chunks → return answer + citations → write audit row.

## The hard part

**Guaranteeing that nothing outside a user's access ever reaches the model, and proving it.**

Approach:
1. **Filter inside the search**, never after (one SQL query does both).
2. **Row-level security** as a second lock the app can't forget.
3. **Deny by default:** no ACL = invisible.
4. **Store Entra object IDs**, never names or emails.
5. **Leak test suite** with a fixed fake company: for each persona (CEO, HR, Finance,
   Engineer, new starter with no groups), assert exactly which documents they can retrieve,
   that forbidden content never appears in the prompt sent to the model, and that removing
   someone from a group takes effect after sync.
6. **Audit log** so every answer can be traced to the chunks behind it.

Known limits we document rather than solve: over-shared source permissions, sync delay,
prompt injection inside documents the user is allowed to read.

## External dependencies

| Dependency | Needed for | Cost / limits |
|---|---|---|
| Azure account + free Entra ID tenant | Login, test users and groups | Free tier. Owner creates it (M1). The M365 Developer sandbox is hard to qualify for in 2026, so use a plain free tenant. |
| App registration in Entra | OIDC client + Graph `GroupMember.Read.All`, `User.Read.All` (application permissions, admin consent) | Free |
| Ollama + models | Generation, embeddings | Free, local GPU (RTX 5070 Ti, 12 GB) |
| Docker Desktop | Postgres, local stack | Free for personal use |
| GitHub Actions | CI | Private-repo free minutes are limited, so CI is PR-only and path-filtered |

CI never calls Entra or a real model. Tests use locally signed tokens, a fake Graph
client and a fake model client, so no secrets are needed in CI.

## Testing strategy

- **Unit (pytest):** pure logic: config, chunking, ACL rules, prompt building, token
  claim checks. No network or database.
- **Integration (pytest + real Postgres with pgvector):** repositories, migrations, RLS
  policies, filtered search. CI runs Postgres as a service container.
- **Leak tests (pytest, marked `leak`):** persona-by-persona access matrix over the Acme
  fixture. The heart of the project. Any failure blocks the merge.
- **Frontend (Vitest + Testing Library):** components and the auth-gated routing.
- **Gate:** ruff + mypy + pytest (backend), oxlint + tsc + Vitest + build (frontend), all green in CI.
- **Every test is explained** in its PR and in `docs/learning/test-guide.md`.

## Milestones

Each ends with something runnable. Issues are small, one concept each.

- **M0 Scaffold:** repo, CI, health endpoint, frontend shell, learning docs. *(done by this setup)*
- **M1 Local stack and database:** Docker Compose (Postgres + pgvector, Ollama), DB
  settings, Alembic, the data model (users, groups, memberships, documents, chunks).
  *Runnable: `docker compose up` + migrations create the schema.*
- **M2 Identity:** Entra tenant setup runbook, JWT verification, `/me` endpoint, Graph
  group sync (full then delta), user→groups lookup. *Runnable: a real Entra user calls
  `/me` and sees their groups.*
- **M3 Ingestion:** Acme fixture company, permissions file, loader, chunker, embedding
  client, ingest command. *Runnable: `ingest` fills documents and chunks with ACLs.*
- **M4 Permission-aware retrieval:** filtered vector search, RLS policies, deny-by-default,
  the leak test suite. *Runnable: `/search` returns only allowed chunks, leak tests green.*
- **M5 Answers:** model client (OpenAI-compatible), prompt builder, citations,
  out-of-scope reply, audit log, `/chat` endpoint. *Runnable: ask a question, get a cited
  answer scoped to you.*
- **M6 Frontend:** MSAL login, chat page, citations, admin access page.
  *Runnable: full demo in the browser.*
- **M7 Hardening and demo:** group removal propagation test, model swap demo, threat-model
  doc, README demo script and screenshots, architecture diagram. *Runnable: portfolio-ready.*

## Open questions

- **Which generator model is best on the Acme data?** Decide by a small comparison in M5
  (owner reviews results).
- **How relevant must a chunk be before we answer, versus saying out of scope?** Tune in M5
  with the owner.
- **Owner action in M2:** create the free Azure account / Entra tenant (runbook provided).
