# Concepts, in plain language

A revision sheet for every idea this project uses. Each entry says what it is, gives an
everyday analogy, and says where it shows up in this project. New concepts get added
here in the PR that first uses them.

---

## The AI side

### LLM (large language model)
A program that predicts the next word, trained on huge amounts of text. It "knows"
general things but nothing about Acme Ltd.
**Here:** the open-source model (e.g. Qwen) that writes the final answer.

### Tokens and context window
Models read text as *tokens* (word pieces, roughly ¾ of a word each). The *context
window* is how many tokens fit in one request: question + retrieved passages + answer.
**Here:** limits how many passages we can paste into the prompt.

### Weights
The billions of numbers inside a model that store what it learned. Training changes
them; asking questions doesn't.
**Here:** why we *don't* train company data in. Weights can't be access-controlled
(see `docs/research/02-why-permission-aware-rag.md`).

### Embedding
A list of numbers (e.g. 1024 of them) that represents the *meaning* of a piece of text.
Texts with similar meaning get similar numbers. Analogy: GPS coordinates for meaning.
"Q3 revenue" and "third-quarter sales" end up close together.
**Here:** every chunk gets an embedding when ingested; every question gets one when asked.

### Vector search (similarity search)
Finding the stored embeddings closest to the question's embedding, usually by *cosine
distance* (the angle between the two lists of numbers). An **index** (pgvector's HNSW)
makes this fast without comparing against every row.
**Here:** step 1 of answering a question, *with the permission filter inside it*.

### Chunking
Splitting a document into passages of a few hundred tokens, because a whole document is
too big to paste in and too vague to embed well.
**Here:** each chunk keeps a link to its document, so it inherits the document's ACL.

### RAG (retrieval-augmented generation)
Look up relevant passages first, then have the model answer *from those passages*.
Analogy: an open-book exam where you can only bring the pages you're cleared to read.
**Here:** the whole question-answering pipeline.

### Prompt injection
Text inside a document that tries to give the model orders ("ignore previous
instructions…"). The model can't reliably tell data from instructions.
**Here:** a known limit. It can't expose forbidden data because the model never sees
any, but it can still make an answer wrong.

### OpenAI-compatible API
A de facto standard request format for "send messages, get a reply" that Ollama, vLLM
and many others accept.
**Here:** why swapping the model is just a config change.

---

## The security side

### Authentication vs authorisation
*Authentication* = proving who you are (logging in). *Authorisation* = what you're
allowed to do once in. Analogy: showing your badge at the door vs which rooms it opens.
**Here:** Entra ID does authentication; our database filter does authorisation.

### ACL (access control list)
The list attached to a thing saying who may access it. Ours lists Entra **group IDs**
(and sometimes user IDs).
**Here:** every document has one; chunks inherit it.

### RBAC (role-based access control)
Permissions given to roles or groups instead of individuals. "Finance team can read
finance docs", not "Alice, Bob and Carol can".
**Here:** Entra groups are the roles.

### Deny by default
If there is no rule saying yes, the answer is no. A document with an empty ACL is
visible to nobody (except admins).
**Here:** the single most important rule, with its own tests.

### Pre-filtering vs post-filtering
*Post*: search everything, then throw away what the user can't see (one bug = leak).
*Pre*: only ever search what the user can see.
**Here:** always pre-filter, inside the SQL query.

### Row-level security (RLS)
A Postgres feature: a policy on a table so that each database session only sees the
rows it's allowed to, *no matter what query the app sends*.
Analogy: even if a librarian fetches the wrong shelf, the locked shelf won't open.
**Here:** our second, independent lock behind the app's own filter.

### Defence in depth
Several independent safeguards, so one mistake isn't a breach.
**Here:** app filter + RLS + deny-by-default + leak tests.

---

## The identity side

### Entra ID (formerly Azure Active Directory)
Microsoft's company directory: users, groups, and login for Microsoft 365 and apps.
**Here:** where we get users and groups, so the company doesn't recreate them.

### Tenant
One organisation's private copy of Entra ID, with its own users and groups.
**Here:** you create a free test tenant with fake users (ceo@, hr@, finance@).

### Object ID
The permanent unique ID (a GUID) of a user or group. Names and emails can change or
be reused; object IDs can't.
**Here:** ACLs store object IDs only.

### OIDC (OpenID Connect) and OAuth 2.0
The standard "Sign in with Microsoft" flow. The user logs in at Microsoft; our app gets
back a signed token saying who they are.
**Here:** the React app logs in with MSAL; the backend checks the token.

### JWT (JSON Web Token)
A signed, base64-encoded JSON blob: header, claims (user ID, expiry, audience…), and a
signature. Anyone can read it; only Microsoft can sign it.
**Here:** the backend verifies the signature against Microsoft's public keys (JWKS)
and checks issuer, audience and expiry before trusting any claim.

### Microsoft Graph and delta queries
Graph is Microsoft's API for directory data. A *delta query* returns only what changed
since your last call (new members, removed members as "@removed").
**Here:** how group sync keeps our copy of "who is in which group" current.

### SCIM
A standard protocol where the identity provider *pushes* user and group changes to an
app, instead of the app polling.
**Here:** deferred. Graph delta polling first; SCIM is in `docs/future.md`.

---

## The engineering side

### Migration (Alembic)
A versioned script that changes the database schema (add a table, a column, a policy).
Running them in order rebuilds the schema anywhere.

### Test levels
- *Unit*: one function, no database or network. Fast.
- *Integration*: real Postgres (in Docker / CI service), real SQL, fake model.
- *Leak tests*: our name for integration tests that assert a user can't retrieve or be
  answered from content outside their ACL. They gate every merge.

### Fakes and fixtures
A *fake* stands in for an external service (Entra, the LLM) so tests are fast,
offline and repeatable. A *fixture* is pytest's way of setting up data a test needs.

### CI (continuous integration)
GitHub Actions runs lint, type check and tests on every pull request. A PR merges only
when all of them are green.
