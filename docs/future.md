# Backlog (unscheduled)

Ideas not yet in a milestone. When one is scheduled it becomes a GitHub issue and is
removed from here.

## Connectors
- 2026-11-16: SharePoint / OneDrive connector with real per-file permission sync via Microsoft Graph.
- 2026-11-16: Confluence or Google Drive connector.

## Identity
- 2026-11-16: SCIM push provisioning instead of Graph delta polling.
- 2026-11-16: Okta and Google Workspace as identity sources.
- 2026-11-16: Graph change notifications (webhooks) to cut sync delay.

## Retrieval quality
- 2026-11-16: Reranker model (e.g. bge-reranker-v2-m3) after the filtered search.
- 2026-11-16: Hybrid keyword + vector search.

## Security and governance
- 2026-11-16: Oversharing report: documents visible to very broad groups.
- 2026-11-16: Per-user answer cache keyed by permissions.

## Deployment
- 2026-11-16: vLLM production profile, multi-GPU.
- 2026-11-16: Air-gapped install packaging (offline images and model weights).

## Models
- 2026-11-25: Evaluate Thinking Machines **Inkling 2 Mini** (`thinkingmachines/Inkling-2-Mini`,
  Apache-2.0, released 2026-11-17) as a generator candidate in the M5 model comparison.
  26.4B total / 3.4B active looped MoE (about 5.4B effective active), 1M-token context,
  vLLM/SGLang/llama.cpp/Ollama support. **Blocked on hardware for dev:** the checkpoint is
  about 20 GB and the Ollama tags are 18–20 GB, and the model card recommends 32 GB+ of VRAM
  (the newsletter's "runs in 16 GB" claim did not hold up). The dev GPU has 12 GB, so it would
  spill to CPU RAM and run slowly. The card also lists Ollama "on Apple Silicon" only. Its
  card warns of weaker factual recall, reasoning loops and weaker instruction-following than
  larger models. Test it on the Acme set for: answers grounded only in the supplied chunks,
  "I don't know" when the allowed chunks lack the answer, and citation accuracy. A refusal
  is a UX check, not a security control, because forbidden chunks never reach the model.
  Better fit for the vLLM production profile than for the 12 GB dev box.
