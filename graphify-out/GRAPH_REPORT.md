# Graph Report - custom-llms  (2026-11-16)

## Corpus Check
- 42 files · ~18,487 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 334 nodes · 333 edges · 36 communities (26 shown, 10 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 10 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Settings
- The AI side
- compilerOptions
- devDependencies
- compilerOptions
- generate_diagram.py
- package.json
- Design System
- plugins
- Clearance
- Clearance: Plan
- Tech stack choices
- Scaffold file guide (M0)
- pull_request_template.md
- Project context: Clearance
- The security side
- Market and competitors
- Learning mode (required for all development)
- Backlog (unscheduled)
- Backend
- Why permission-aware RAG (and not fine-tuning)
- Clearance
- Issue → PR → CI workflow (required for all development)
- protect-main.sh
- plan-original.md
- tsconfig.json
- README.md
- __init__.py
- CLAUDE.md
- progress.md
- README.md
- README.md
- clearance

## God Nodes (most connected - your core abstractions)
1. `compilerOptions` - 18 edges
2. `compilerOptions` - 15 edges
3. `Settings` - 12 edges
4. `Clearance` - 12 edges
5. `Clearance: Plan` - 11 edges
6. `Design System` - 10 edges
7. `The AI side` - 10 edges
8. `Tech stack choices` - 9 edges
9. `The security side` - 8 edges
10. `The identity side` - 8 edges

## Surprising Connections (you probably didn't know these)
- `HealthResponse` --uses--> `Settings`  [INFERRED]
  backend/src/clearance/main.py → backend/src/clearance/config.py
- `test_defaults_work_with_no_configuration()` --calls--> `Settings`  [INFERRED]
  backend/tests/test_config.py → backend/src/clearance/config.py
- `test_environment_variables_override_defaults()` --calls--> `Settings`  [INFERRED]
  backend/tests/test_config.py → backend/src/clearance/config.py
- `test_model_url_must_be_a_url()` --calls--> `Settings`  [INFERRED]
  backend/tests/test_config.py → backend/src/clearance/config.py
- `test_unknown_environment_is_rejected()` --calls--> `Settings`  [INFERRED]
  backend/tests/test_config.py → backend/src/clearance/config.py

## Import Cycles
- None detected.

## Communities (36 total, 10 thin omitted)

### Community 0 - "Settings"
Cohesion: 0.09
Nodes (31): Environment, get_settings(), Application settings, read from environment variables.  Every setting has a safe, Where the app is running. Anything else is rejected at startup., All configuration in one typed object.      Pydantic checks types when the objec, Build settings from the current environment.      A function (not a module-level, Settings, create_app() (+23 more)

### Community 1 - "The AI side"
Cohesion: 0.08
Nodes (24): Chunking, CI (continuous integration), Concepts, in plain language, Embedding, Entra ID (formerly Azure Active Directory), Fakes and fixtures, JWT (JSON Web Token), LLM (large language model) (+16 more)

### Community 2 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 3 - "devDependencies"
Cohesion: 0.09
Nodes (23): devDependencies, jsdom, oxlint, @testing-library/jest-dom, @testing-library/react, @types/node, @types/react, @types/react-dom (+15 more)

### Community 4 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 5 - "generate_diagram.py"
Cohesion: 0.18
Nodes (14): assign_columns(), endpoint(), esc(), group_chain(), layout(), main(), Node, (cx, cy, left, right, top, bottom, column) for a node OR group id. (+6 more)

### Community 6 - "package.json"
Cohesion: 0.12
Nodes (16): dependencies, react, react-dom, name, private, scripts, build, dev (+8 more)

### Community 7 - "Design System"
Cohesion: 0.12
Nodes (15): Architecture Diagram Skill, Auto-layout scaffold (local extension v1.2), Color Palette, Component Box Pattern, Design System, Export Toolbar (built-in), Info Card Pattern, Layout Structure (+7 more)

### Community 8 - "plugins"
Cohesion: 0.16
Nodes (10): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, App(), oxc, react (+2 more)

### Community 9 - "Clearance"
Cohesion: 0.15
Nodes (12): Backlog (required), Before every PR merge (required), Change log (required), CI (required), Clearance, Conventions, Don't commit secrets, Git workflow (required) (+4 more)

### Community 10 - "Clearance: Plan"
Cohesion: 0.17
Nodes (11): Architecture, Clearance: Plan, External dependencies, How we work (this project is different), Milestones, Open questions, Scope, Tech stack (+3 more)

### Community 11 - "Tech stack choices"
Cohesion: 0.20
Nodes (9): Backend (decided, not asked), First data source (asked), Frontend (asked), Identity (asked), Model server (decided, not asked), Models (decided, not asked), Sources, Tech stack choices (+1 more)

### Community 12 - "Scaffold file guide (M0)"
Cohesion: 0.22
Nodes (8): `backend/`: Python service, `.claude/`: instructions for Claude Code, `docs/`: for people, `frontend/`: React app, `.github/`: GitHub configuration, Other, Repo root, Scaffold file guide (M0)

### Community 13 - "pull_request_template.md"
Cohesion: 0.22
Nodes (8): Before merge, Every changed file, explained (learning mode, required), Every test, explained (required), Fixes and corrections (if any), Follow-up issues filed, How it was tested, New concepts, What changed

### Community 14 - "Project context: Clearance"
Cohesion: 0.25
Nodes (7): Architecture (target, v1), Auth model, Current state, Data model (planned in M1), Known gaps / accepted limits, Project context: Clearance, Security invariants

### Community 15 - "The security side"
Cohesion: 0.25
Nodes (8): ACL (access control list), Authentication vs authorisation, Defence in depth, Deny by default, Pre-filtering vs post-filtering, RBAC (role-based access control), Row-level security (RLS), The security side

### Community 16 - "Market and competitors"
Cohesion: 0.25
Nodes (7): 1. Big cloud assistants (closed models, hosted by the vendor), 2. Open-source, self-hostable, permission-aware, 3. Open-source "chat with your documents" tools (any model, coarse access), Market and competitors, Sources, The question, Where this project sits

### Community 17 - "Learning mode (required for all development)"
Cohesion: 0.29
Nodes (6): After writing code: the explanation (required), Before writing code, End of each milestone, Learning mode (required for all development), Tests (security project, so extra care), While writing code

### Community 18 - "Backlog (unscheduled)"
Cohesion: 0.29
Nodes (6): Backlog (unscheduled), Connectors, Deployment, Identity, Retrieval quality, Security and governance

### Community 19 - "Backend"
Cohesion: 0.29
Nodes (6): Backend, Frontend, `src/App.test.tsx`, Test guide, `tests/test_config.py`, `tests/test_health.py`

### Community 20 - "Why permission-aware RAG (and not fine-tuning)"
Cohesion: 0.29
Nodes (6): Option A: train it in (fine-tuning), Option B: look it up at question time (RAG), Sources, The two ways to "teach" a model company data, Where leaks still happen (and what we do about each), Why permission-aware RAG (and not fine-tuning)

### Community 21 - "Clearance"
Cohesion: 0.33
Nodes (5): Clearance, Layout, Run it, Status, Test it (the same checks CI runs)

### Community 22 - "Issue → PR → CI workflow (required for all development)"
Cohesion: 0.40
Nodes (4): Invariants, Issue → PR → CI workflow (required for all development), The loop, Writing issues

## Knowledge Gaps
- **192 isolated node(s):** `clearance`, `$schema`, `typescript`, `oxc`, `react/rules-of-hooks` (+187 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `devDependencies` connect `devDependencies` to `package.json`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Why does `Concepts, in plain language` connect `The AI side` to `The security side`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Settings` (e.g. with `HealthResponse` and `test_defaults_work_with_no_configuration()`) actually correct?**
  _`Settings` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `clearance`, `$schema`, `typescript` to the rest of the system?**
  _192 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Settings` be split into smaller, more focused modules?**
  _Cohesion score 0.08571428571428572 - nodes in this community are weakly interconnected._
- **Should `The AI side` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `compilerOptions` be split into smaller, more focused modules?**
  _Cohesion score 0.08333333333333333 - nodes in this community are weakly interconnected._