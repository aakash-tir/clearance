# Project context: Clearance

Deep context for development sessions. `plan.md` has scope and milestones;
`docs/research/` has the reasoning behind every choice.

## Architecture (target, v1)

```
Browser (React + MSAL) --OIDC login--> Entra ID
   | Bearer JWT
   v
FastAPI (backend/src/clearance)
   auth        verify JWT against Microsoft JWKS (issuer, audience, expiry, signature)
   identity    user object ID -> group object IDs (from synced tables)
   retrieval   embed question -> pgvector search WHERE chunk ACL && user groups
               (+ RLS: session variable carries the user's group IDs)
   generation  allowed chunks + question -> model client -> answer + citations
               nothing relevant & allowed -> polite out-of-scope reply
   audit       user, question, returned chunk IDs, timestamp
   |                         |
Postgres 17 + pgvector    Ollama (dev) / vLLM (prod), OpenAI-compatible
   ^
Background jobs: group sync (Graph full + delta), ingest (Acme folder + permissions file)
```

## Auth model
- **Authentication:** Entra ID OIDC. Backend trusts only tokens whose signature verifies
  against Microsoft's published keys and whose `iss`, `aud`, `exp`, `tid` match config.
  User identity = `oid` claim (object ID).
- **Authorisation:** group membership from our synced tables (not from the token's
  `groups` claim, which overflows past ~200 groups and goes stale until re-login).
- **Admins:** a configured Entra group ID; admins see everything and the access report.
- **Tests:** a local RSA key signs fake tokens; a fake Graph client feeds group sync.

## Data model (planned in M1)
- `users(id = Entra oid, display_name, email, synced_at)`
- `groups(id = Entra group oid, display_name, synced_at)`
- `memberships(user_id, group_id)`
- `documents(id, source, path, title, acl_group_ids uuid[], acl_user_ids uuid[], content_hash, ingested_at)`
- `chunks(id, document_id, ordinal, text, embedding vector(1024), embedding_model)`
  (chunks inherit the document ACL via join, or a copied column, decided in M4 with the owner)
- `audit_log(id, user_id, question, chunk_ids, answered, created_at)`
- `sync_state(source, delta_link, last_synced_at)`

## Security invariants
1. Permission filter is **inside** the search SQL. No post-filtering.
2. RLS on `documents` and `chunks` as an independent second lock.
3. Deny by default: empty ACL = invisible (except admins).
4. ACLs contain object IDs only.
5. Leak tests cover every query path; they are the merge gate and are never weakened.

## Known gaps / accepted limits
- Over-shared source permissions are inherited faithfully (report them, M7+).
- Group changes take effect only after the next sync.
- Prompt injection inside documents the user can read can distort answers (can't leak
  forbidden data, since the model never sees it).
- No SharePoint connector in v1 (fake company folder only).

## Current state
M0 scaffold only: `/health` endpoint, typed settings, React shell, CI. See
`.claude/progress.md`.
