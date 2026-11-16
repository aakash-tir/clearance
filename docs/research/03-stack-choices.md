# Tech stack choices

*Researched and decided 2026-11-16. The user chose the starred option on each question asked.*

Each section: the options, what actually separates them **for this project**, and the decision.

## Vector store (asked)

The vector store holds each chunk of text, its embedding (a list of numbers that
represents its meaning) and its access list. It is where "HR never sees finance" is
enforced, so it's the most important choice.

| Option | For | Against |
|---|---|---|
| ★ **Postgres + pgvector** | One database for users, groups, documents, chunks and vectors. The ACL filter is a SQL `WHERE` inside the same query as the vector search. **Row-level security** gives a second, database-enforced lock. Fine up to millions of chunks ([encore.dev](https://encore.dev/articles/pgvector-vs-qdrant)). | Heavy filtering can push a query off the vector index into a slower scan, so we need to watch query plans ([techsy.io](https://techsy.io/en/blog/qdrant-vs-chroma-vs-pgvector)). Irrelevant at our scale. |
| Qdrant + Postgres | Faster filtered search at large scale ([elest.io](https://blog.elest.io/pgvector-vs-qdrant-vs-weaviate-which-vector-database-holds-up-at-100m-vectors/)). | Two services; ACLs copied into Qdrant payloads must stay in sync with Postgres; no database-level second lock. |

**Decision: Postgres 17 + pgvector, with row-level security.**

## Model server (decided, not asked)

| Option | For | Against |
|---|---|---|
| ★ **Ollama for development** | Already installed; one command to pull a model; runs on a laptop GPU. | Built for one user, not many at once. |
| **vLLM for "production"** | Built for many users at once; Prometheus metrics; Apache-2.0 ([Red Hat](https://developers.redhat.com/articles/2025/07/08/ollama-or-vllm-how-choose-right-llm-serving-tool-your-use-case)). | NVIDIA/CUDA only; heavier to run. |

Both expose an **OpenAI-compatible API**. Switching is a base URL and model name change
([morphllm](https://www.morphllm.com/comparisons/vllm-vs-ollama)). So the app talks to "an
OpenAI-compatible endpoint" through one small client module, and **swapping the model or
server is a config change**. That is how the plan's "the model is not fixed" requirement
is met.

**Decision: Ollama in dev, vLLM documented as the production option, both behind one client.**

## Models (decided, not asked)

The dev machine has an RTX 5070 Ti Laptop GPU with 12 GB VRAM.

- **Generator:** a ~9–14B model at 4-bit fits 12 GB with room for context. Candidates:
  Qwen 3 14B, Gemma 3 12B QAT ([bestllmfor.com](https://bestllmfor.com/best/vram-12gb/)),
  or the already-installed `qwen3.5:9b`. Start with what's installed; compare in a later
  issue.
- **Embeddings:** `bge-m3` (multilingual, runs in Ollama, small). Changing the embedding
  model means re-embedding every chunk, so the model name is stored with each chunk.

Most "best model for 12 GB" pages are SEO content. Treat rankings as weak evidence and
test on our own data.

## Identity (asked)

| Option | For | Against |
|---|---|---|
| ★ **Entra ID from day one** | Real OIDC login + Microsoft Graph group sync. Matches the plan ("use the Azure hierarchy"). | Needs a free Azure account to create a tenant. The M365 Developer Program sandbox is hard to qualify for in 2026 ([Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/5884678/stuck-on-you-don-t-currently-qualify-for-a-sandbox)). |
| Keycloak locally | Offline, no account. | Not the real thing; Entra becomes a later rewrite. |

**Decision: Entra ID.** Tests never call Entra: they use locally signed fake tokens and a
fake Graph client, so CI needs no secrets.

Group sync uses **Microsoft Graph delta queries**, which return only what changed since
last time; removed members come back as "@removed" entries. Large groups can return
incomplete results on the first sync, so do a full baseline read first
([office365itpros](https://office365itpros.com/2026/06/25/graph-delta-queries-entra-id-groups/),
[alflokken](https://alflokken.github.io/posts/graph-delta-queries)).

## First data source (asked)

**Decision: a fake company folder ("Acme Ltd")** with finance, HR, engineering and
all-staff documents, plus a permissions file mapping folders to Entra group object IDs.
Known content means we can write no-leak tests with exact expected answers.
SharePoint/OneDrive with real permission sync comes in a later milestone.

## Backend (decided, not asked)

**Python 3.13 + FastAPI + SQLModel + Alembic, managed with uv; pytest, ruff, mypy.**
Rejected: Node/TypeScript backend (the Python ML/RAG ecosystem is stronger and it matches
the owner's other projects).

## Frontend (asked)

**Decision: a small React + TypeScript + Vite app**, with Microsoft login (MSAL), a chat
page with citations, and an admin "who can see what" page. Vitest for tests.
Rejected: API-only v1 (not demoable).

## Sources

- [pgvector vs Qdrant (encore.dev)](https://encore.dev/articles/pgvector-vs-qdrant)
- [pgvector vs Qdrant vs Weaviate at 100M vectors (elest.io)](https://blog.elest.io/pgvector-vs-qdrant-vs-weaviate-which-vector-database-holds-up-at-100m-vectors/)
- [Qdrant vs Chroma vs pgvector (techsy.io)](https://techsy.io/en/blog/qdrant-vs-chroma-vs-pgvector)
- [Ollama or vLLM? (Red Hat Developer)](https://developers.redhat.com/articles/2025/07/08/ollama-or-vllm-how-choose-right-llm-serving-tool-your-use-case)
- [vLLM vs Ollama 2026 (morphllm)](https://www.morphllm.com/comparisons/vllm-vs-ollama)
- [Best local LLM for 12 GB VRAM (bestllmfor.com)](https://bestllmfor.com/best/vram-12gb/)
- [Graph delta queries with Entra ID groups (office365itpros)](https://office365itpros.com/2026/06/25/graph-delta-queries-entra-id-groups/)
- [Graph delta queries (alflokken)](https://alflokken.github.io/posts/graph-delta-queries)
- [Microsoft Learn: delta query overview](https://learn.microsoft.com/graph/delta-query-overview)
- [M365 dev sandbox qualification issues (Microsoft Q&A)](https://learn.microsoft.com/en-us/answers/questions/5884678/stuck-on-you-don-t-currently-qualify-for-a-sandbox)
