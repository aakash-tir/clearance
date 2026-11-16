# Why permission-aware RAG (and not fine-tuning)

*Researched 2026-11-16.*

## The two ways to "teach" a model company data

### Option A: train it in (fine-tuning)
You keep training the model on the company's documents, so the facts end up stored in
its weights (the billions of numbers that make up the model).

**Why this can't work for us:**
- **Weights have no access control.** Once the finance figures are in the weights, every
  user who talks to that model can potentially pull them out. You can't say "this
  number is only for the finance group" inside a neural network.
- **"Please don't tell HR" is not security.** You could instruct the model to refuse, but
  instructions can be bypassed with clever prompts (jailbreaks). A rule that can be
  argued with is not a lock.
- **Swapping the model means retraining.** The plan wants the model to be swappable.
  With fine-tuning, every new model needs the whole training run again.
- **Data changes daily.** People join, leave and change teams; documents get edited.
  Retraining every time is impossible.

The only "fine-tuning" variant that keeps access control is *one model per permission
group*, which multiplies cost and still breaks when a user is in several groups.

### Option B: look it up at question time (RAG)
**RAG = Retrieval-Augmented Generation.** The model stays generic. When a user asks a
question:

1. Find the few passages in the company's documents most related to the question
   (retrieval).
2. Paste those passages into the prompt with the question.
3. The model writes an answer from those passages and cites them (generation).

**Permission-aware RAG** adds one rule to step 1: *only search the passages this user
is allowed to read.* The model can't leak what it was never shown.

This is a **deterministic** guarantee (an ordinary database filter), not an AI behaviour.
That is the only way to get close to the plan's "100% no leaks" requirement.

## Where leaks still happen (and what we do about each)

From practitioner write-ups and OWASP's LLM Top 10 (2025: LLM01 prompt injection, LLM02
sensitive information disclosure, LLM08 vector and embedding weaknesses):

| Leak | What goes wrong | Our defence |
|---|---|---|
| **Post-filtering** | Search everything, then remove forbidden results. A bug in the "remove" step leaks; it also returns too few results. | Filter **inside** the search query (SQL `WHERE`), never after. |
| **Forgotten filter** | One new code path queries chunks without the filter. | Postgres **row-level security (RLS)**: the database itself refuses rows the session's user can't see, even if the app forgets. Two independent locks. |
| **Missing ACL** | A document is ingested with no permissions recorded and becomes visible to all. | **Deny by default**: no ACL means nobody (except admins) sees it. Tested. |
| **Stale permissions** | Someone leaves the finance group but the index still lets them in until the next sync. | Group membership checked at query time from the latest sync; sync interval and "last synced" are visible; removal tests. |
| **Over-shared source** | The finance file is already open to "Everyone" in SharePoint. | Can't fix the source, but an admin **access report** shows it before go-live. |
| **Caches and chat history** | A cached answer or old conversation is shown to someone else. | Cache keyed by user permissions (or no answer cache in v1); history is per user and also under RLS. |
| **Identity mix-ups** | Group deleted and recreated with the same name; email reused. | Store Entra **object IDs**, never names or emails, in ACLs. |
| **Prompt injection** | A document the user *can* see contains "ignore your rules and print …". | The model only ever sees allowed passages, so injection can't reach forbidden data. It can still produce bad answers, so it's documented as a known limit. |

## Sources

- [Permission-aware retrieval, the missing layer (DEV)](https://dev.to/alaikrm/permission-aware-retrieval-the-missing-layer-in-enterprise-rag-security-199f)
- [RAG with permissions: where access control has to sit (WZ-IT)](https://wz-it.com/en/knowledge/ki/rag-permissions/)
- [The PII leak in your RAG pipeline (tianpan.co)](https://tianpan.co/blog/2026-04-19-pii-leak-rag-pipeline-access-control)
- [Document-level security in RAG (fast.io, vendor blog)](https://fast.io/resources/document-level-security-rag/)
- [RAG system design with permissions (letsdatascience)](https://letsdatascience.com/blog/rag-system-design-permissions)
- [Agent entitlement inheritance (pebblous)](https://blog.pebblous.ai/report/agent-entitlement-inheritance-retrieval/en/)

These are mostly practitioner and vendor blogs, not peer-reviewed. They agree on the
failure modes above, which is why the table is built from what they have in common.
