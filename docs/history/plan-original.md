I want to create an system that allows a company or user to select an open source llm and use it.
the twist is that companys want this llm/ or their ai to give to everyone in a company. the issue is that you need to feed it will all the company information. 
this is okay for start up and 1-5 people companies but bigger companies either have to restrict teh data fed in to prevent company information leaking or only allow a given few people to use it as the data itself does not have access controls. 


I want to build an interface that allows me to go to a company. select an open source model for it so that teh open source model is not fixed and can be changed if needed given that training the model might be needed or weights can be transfered. feed in all the company data but create an account system so that each user as access to a relevent subset of data and not everything.

eg CEO has access to all teh data, the finacial sectors llm accounts only has access to the finances, the HR does not have access to the finances so a prompt about it wont return any information about it but kindly decline out of scope. 

for this to sell it has to be reletively easy to setup and 100% accuarte in data leaks so high security.
do intense research if there is anything like this already out there and if this project is worth building. and if yes it is worth building a plan on how to go about it. note down all of this in a docs folder in md files so i can revise over it.  

also take into consideration how companies would need to transfer into our system, for example use the azure heirachy in place to create teh access accounts or whatever service teh company uses. 
ask me questions if needed.

---

## Decisions so far (2026-11-16)

- **This is a portfolio project, not a product to sell.** The market is crowded (Microsoft 365 Copilot, Glean, Amazon Q Business, Gemini Enterprise, and the open-source Onyx). I have no industry connection to target a niche, so the goal is to learn and to show the skill, not to compete.
- **It replaces nova-lite** as my main portfolio project.
- **It runs on the customer's own hardware (self-hosted).** The open-source model is served locally and is swappable, with no retraining.
- **The approach is permission-aware RAG, not fine-tuning.** Company data is never trained into the model weights. Documents are indexed with their access lists, and each query only retrieves what the logged-in user may see. A deterministic filter enforces access, not the LLM.
- **Identity comes from the company's existing directory** (Azure / Entra ID first, via SSO and group sync), so access accounts mirror the hierarchy already in place.
- **The interesting work is outside the RAG core:** connectors that carry permissions, identity sync, enforcement, audit logs and tests that prove nothing leaks.

## How we work on this project (different from my other projects)

I need to understand every step and how the code works in detail. So:

1. **Small steps.** One concept per issue/PR. No large multi-file drops.
2. **Explain every change.** For each file created or changed: what it does, why it is needed, and how it fits the rest of the system. The same goes for every correction or bug fix: what was wrong and why the fix works.
3. **Explain every test.** For each test: what behaviour it checks, why that test is needed (which bug or leak it would catch), and why it is written that way.
4. **Learning notes in `docs/`.** Each milestone gets a short write-up in plain language that I can revise from later, including the concepts (embeddings, vector search, ACL filtering, OIDC/SCIM, etc.).
5. **I stay in the loop.** Pause at key design decisions and explain the options before choosing, rather than deciding silently.
6. **Prefer clarity over cleverness.** Readable code with simple structure beats compact or abstract code, since the point is that I can explain it in an interview.
