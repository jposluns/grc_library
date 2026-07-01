# FR-48 deferred worklist (entangled docs)

**Date:** 2026-07-01\
**License:** CC BY-SA 4.0

The 38 policy/standard documents that FR-48's safe-subset pass (PR #520) deferred because their section numbers are cited, self-referenced, or coupled to inline prose clause numbers, so a renumber to the canonical fully-numbered model (`## N.` H2 + hierarchical `### N.M` H3) needs a **lockstep citation/clause remap** rather than the purely-additive change the 28 safe docs received. This file is the starting worklist for the dedicated effort TODO §1.1 describes; it is maintainer working state, exempt from corpus audit gates.

**Split note.** The corpus's 66 non-fully-numbered policy/standard docs divide: 28 safe (normalized in PR #520) + 38 deferred (below). The last 5 of the deferred set were initially applied in PR #520 and then **reverted** when the pre-push skeptical verifier caught the inline-clause-numbering coupling (DEFECT 2) plus one missed bare-parenthetical inbound citation (DEFECT 1); they are restored to their pre-FR-48 state and listed here.

**Entanglement forms** (why each doc is deferred):
- **inbound `§N`** / **inbound "Section N"**: another live document cites this doc's section by number (a renumber shifts the target; the citer must be updated in the same PR). Both markdown-link (`[..](doc) §N`) and bare-parenthetical (`(doc §N)`) forms count. "Section N" citers include the [`dev-security/claude-rules/languages/`](../dev-security/claude-rules/languages/) pack files for the mobile-app standard.
- **intra `§N`** / **intra "Section N"**: the doc references its own sections by number in body prose (the reference must be remapped when the headings renumber).
- **inline clause numbering**: the doc's body carries numbered prose clauses (`3.1 Internal Audit must...`, `4.3 CAPA effectiveness must be validated...`) keyed to the OLD local H3 numbering; renumbering the headings without realigning these inline clauses (and any external citation of them, e.g. `procedure-capa.md` -> `policy-compliance-and-audit-management.md §4.3`) breaks the heading<->clause correspondence. The remap must renumber the inline clauses in lockstep with the headings.
- **uses "## Section N:" labels**: the doc's H2s are `## Section N: title`; the strip-and-renumber changes the section number the "Section N" scheme exposes, so it is unsafe wherever that doc is also cited or self-references.

**Build-time discipline.** Recompute the inbound citers at build time (they drift as the corpus changes); for each doc, produce the old-section-number to new-`§N` map and apply it to every citer (corpus-wide grep, not the doc's own input set) in the same PR, then re-parse. Recommended shape: one domain-batch per PR, deterministic apply + citation remap + re-parse. The numbering itself is gate-blind (gate 38 strips numbering when matching), so this is editorial consistency, not error-prevention.

## Deferred documents (recompute reasons at build time)

- [ ] `ai/standard-ai-access-and-agent-permissions.md` -- intra §N, uses "## Section N:" labels
- [ ] `ai/standard-ai-and-agentic-development-security.md` -- inbound §N, intra §N
- [ ] `ai/standard-ai-inference-cost-governance.md` -- intra "Section N", intra §N, uses "## Section N:" labels
- [ ] `ai/standard-ai-model-risk.md` -- inbound §N
- [ ] `ai/standard-ai-security-and-risk.md` -- intra §N
- [ ] `ai/standard-ai-testing-validation-and-documentation.md` -- intra §N
- [ ] `architecture/standard-integration-architecture.md` -- intra "Section N", uses "## Section N:" labels
- [ ] `architecture/standard-technology-radar.md` -- intra "Section N", uses "## Section N:" labels
- [ ] `compliance/standard-internal-audit.md` -- inbound §N, intra "Section N", intra §N
- [ ] `dev-security/standard-api-security.md` -- intra §N, uses "## Section N:" labels
- [ ] `dev-security/standard-developer-security-requirements.md` -- inbound §N, intra §N
- [ ] `dev-security/standard-devops-security-requirements.md` -- intra §N
- [ ] `dev-security/standard-mobile-application-security.md` -- inbound "Section N", intra "Section N", uses "## Section N:" labels
- [ ] `dev-security/standard-quality-assurance-and-testing.md` -- intra §N
- [ ] `dev-security/standard-software-composition-analysis.md` -- inbound §N
- [ ] `governance/policy-digital-twin-and-simulation-governance.md` -- intra §N
- [ ] `governance/policy-exception-and-risk-acceptance-management.md` -- inbound §N, intra §N
- [ ] `governance/standard-records-retention-and-destruction.md` -- intra §N, uses "## Section N:" labels
- [ ] `operations/standard-capacity-and-performance-management.md` -- intra §N, uses "## Section N:" labels
- [ ] `operations/standard-observability-and-telemetry.md` -- intra §N, uses "## Section N:" labels
- [ ] `operations/standard-production-security-requirements.md` -- inbound §N, intra §N
- [ ] `operations/standard-service-level-management.md` -- intra §N
- [ ] `privacy/policy-privacy-and-data-governance.md` -- inbound §N, intra §N
- [ ] `risk/standard-third-party-and-supply-chain-risk.md` -- intra §N
- [ ] `security/policy-acceptance-into-service.md` -- intra §N
- [ ] `security/policy-encryption-and-key-management.md` -- inbound §N, intra §N
- [ ] `security/policy-identity-and-access-management.md` -- intra §N
- [ ] `security/standard-authentication-and-password-management.md` -- intra §N
- [ ] `security/standard-data-classification-and-handling.md` -- intra §N
- [ ] `security/standard-logging-and-monitoring.md` -- inbound §N, intra §N
- [ ] `security/standard-personnel-security-screening.md` -- intra §N
- [ ] `security/standard-security-awareness-and-training.md` -- intra §N
- [ ] `supply-chain/standard-supplier-resilience-monitoring.md` -- intra §N
- [ ] `compliance/policy-compliance-and-audit-management.md` -- inbound §N (bare-parenthetical, `procedure-capa.md` §4.3), inline clause numbering (reverted from PR #520)
- [ ] `compliance/policy-legal-and-regulatory-compliance.md` -- inline clause numbering (reverted from PR #520)
- [ ] `dev-security/policy-secure-development-and-engineering.md` -- inline clause numbering (reverted from PR #520)
- [ ] `security/policy-network-communications-security.md` -- inline clause numbering (reverted from PR #520)
- [ ] `security/policy-information-security.md` -- inline clause numbering (reverted from PR #520)
