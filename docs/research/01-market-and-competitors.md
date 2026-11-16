# Market and competitors

*Researched 2026-11-16. Prices and feature lists change often, so re-check before quoting them.*

## The question

Is there already a product that lets a company pick an open-source LLM, feed it all of
its data, and still have each employee see only the data they are allowed to see?

**Short answer: yes, several.** That is why this is a portfolio project, not a startup.
The market splits into three groups.

## 1. Big cloud assistants (closed models, hosted by the vendor)

| Product | What it does | Price (approx.) | Why it doesn't fit our idea |
|---|---|---|---|
| **Microsoft 365 Copilot** | Chat over everything in M365 (SharePoint, OneDrive, Teams, mail). Respects the user's existing M365 permissions. | Per-seat add-on to M365 licences | Closed model, Microsoft's cloud. Customer can't pick or self-host the model. |
| **Glean** | Enterprise search + assistant over 100+ connectors, permission-aware. | Not published. Reported ~$50–75/user/month, ~100-seat minimum ([GoSearch](https://www.gosearch.ai/blog/glean-pricing-explained), [coworker.ai](https://coworker.ai/blog/glean-pricing)) | Expensive, cloud-hosted, closed models. |
| **Amazon Q Business** | Permission-aware Q&A over company data on AWS. | Was $3 (Lite) / $20 (Pro) per user/month. Reported closed to new customers on 2026-07-31 in favour of "Amazon Quick" ([coworker.ai comparison](https://coworker.ai/blog/enterprise-ai-pricing-comparison-2026)) | AWS cloud only. Shows even a giant's product line shifts. |
| **Gemini Enterprise** | Google's equivalent over Workspace and other sources. | Reported $21 (Business) / $30 (Standard) per seat/month ([Monetizely](https://www.getmonetizely.com/articles/how-do-gemini-enterprise-microsoft-365-copilot-and-amazon-q-business-stack-up-comparing-pricing-models-and-value)) | Google cloud, closed model. |

**Lesson from Copilot:** these products don't leak through the AI. They leak because the
*source* permissions were already too broad. Microsoft's own guidance says most
"oversharing" comes from configuration problems such as broken inheritance and "Anyone"
links ([Microsoft Tech Community](https://techcommunity.microsoft.com/blog/microsoft365copilotblog/mitigate-oversharing-to-govern-microsoft-365-copilot-and-agents/4448744),
[Petri: "Copilot didn't overshare your data. Your permissions did"](https://petri.com/copilot-didnt-overshare-your-data-your-permissions-did/)).
Our system inherits the same problem, so an **access report** ("who can see what") is a
useful feature, not an extra.

## 2. Open-source, self-hostable, permission-aware

| Product | Notes |
|---|---|
| **Onyx** (formerly Danswer) | Closest to our idea. Self-hostable, any model, 40+ connectors. **But** the permission-sync feature is under the paid *Enterprise* licence, not the MIT open-source core ([Onyx connectors docs](https://docs.onyx.app/admins/connectors/overview.md), [Onyx permissioning](https://docs.onyx.app/enterprise_edition/permissioning)). Even Onyx's docs list fewer permission-syncing connectors than its marketing page. |

So the one open-source tool that does exactly this keeps the hard part behind a paywall.
That confirms the hard part is real, and that building it is a good thing to show.

## 3. Open-source "chat with your documents" tools (any model, coarse access)

| Product | Access control |
|---|---|
| **Open WebUI** | Group-based access *per knowledge base* (read/write grants to groups or users). Not per document. Its own docs note that uploads don't carry the source system's ACL ([Open WebUI groups](https://docs.openwebui.com/features/authentication-access/rbac/groups), [Nextcloud + Open WebUI write-up](https://wz-it.com/en/knowledge/ki/rag-nextcloud-open-webui/)). |
| **AnythingLLM** | Multi-user, isolated *workspaces*. Isolation is by workspace, not by document or synced group ([Open WebUI vs AnythingLLM](https://docs.openwebui.com/alternatives/anythingllm.md)). |
| **Dify** | App/workflow builder with knowledge bases. Search found no per-document ACL support. |

These let you pick any model, but someone has to manually split data into separate
buckets. Nothing comes from the company's existing directory or file permissions.

## Where this project sits

What we build = **Group 3's freedom of model + Group 1's permission awareness, self-hosted,
with the permission sync that Onyx keeps behind its paywall.**

As a business, it would compete with Onyx Enterprise and consultancies, and the buyers
(regulated, air-gapped companies) are slow and few. As a **portfolio project** it is strong:
permission-aware RAG, identity integration and leak testing are exactly the parts real
companies struggle with.

## Sources

- [Onyx connectors overview](https://docs.onyx.app/admins/connectors/overview.md)
- [Onyx enterprise permissioning](https://docs.onyx.app/enterprise_edition/permissioning)
- [Open WebUI groups / RBAC](https://docs.openwebui.com/features/authentication-access/rbac/groups)
- [Open WebUI vs AnythingLLM](https://docs.openwebui.com/alternatives/anythingllm.md)
- [RAG + Nextcloud + Open WebUI, ACL caveat](https://wz-it.com/en/knowledge/ki/rag-nextcloud-open-webui/)
- [Microsoft: mitigate oversharing for Copilot](https://techcommunity.microsoft.com/blog/microsoft365copilotblog/mitigate-oversharing-to-govern-microsoft-365-copilot-and-agents/4448744)
- [Microsoft Learn: get ready for Copilot with SharePoint Advanced Management](https://learn.microsoft.com/sharepoint/get-ready-copilot-sharepoint-advanced-management)
- [Petri: Copilot didn't overshare your data](https://petri.com/copilot-didnt-overshare-your-data-your-permissions-did/)
- [Glean pricing explained (GoSearch)](https://www.gosearch.ai/blog/glean-pricing-explained)
- [Enterprise AI pricing comparison 2026 (coworker.ai)](https://coworker.ai/blog/enterprise-ai-pricing-comparison-2026)
- [Gemini Enterprise vs Copilot vs Amazon Q (Monetizely)](https://www.getmonetizely.com/articles/how-do-gemini-enterprise-microsoft-365-copilot-and-amazon-q-business-stack-up-comparing-pricing-models-and-value)
- [Glean alternatives: price the permission sync (beri.net)](https://www.beri.net/article/glean-alternatives-permission-sync-copilot-rovo-onyx-quick-2026)

Most pricing sources are vendor or comparison blogs, not official price lists.
