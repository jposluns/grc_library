# Identity and Access Management Policy

**Document Title:** Identity and Access Management Policy
**Document Type:** Policy
**Version:** 0.0.1
**Date:** 2026 05 26
**Owner:** Chief Information Security Officer
**Approving Authority:** Executive Management
**Related Documents:** `security/policy-information-security.md`, `security/procedure-access-control.md`, `security/procedure-identity-management.md`, `ai/standard-ai-security-and-risk.md`
**Classification:** Public
**Category:** Information Security
**Review Frequency:** Annual and upon material identity, access, architecture, or regulatory change
**Repository Path:** `security/policy-identity-and-access-management.md`
**Confidentiality:** Public
**Licence:** CC0 1.0 Universal

---

## Purpose

This policy defines reusable requirements for governing digital identities, authentication, authorization, privileged access, service accounts, access reviews, access removal, and identity-related evidence.

---

## Policy Statements

1. Every identity must be uniquely attributable to a person, system, workload, service, device, or approved automation.
2. Access must be approved before use and must be limited to the minimum access required for the approved purpose.
3. Privileged access must be restricted, time-bound where feasible, logged, periodically reviewed, and removed when no longer required.
4. Shared accounts must be prohibited unless explicitly approved, monitored, and justified by technical necessity.
5. Service accounts, workload identities, API keys, tokens, secrets, and automation credentials must have assigned owners, defined purpose, rotation expectations, and expiry or review dates.
6. Authentication strength must be proportionate to risk, data sensitivity, privilege level, exposure, and regulatory context.
7. Access to personal data, sensitive data, production systems, administrative interfaces, AI systems, retrieval stores, model endpoints, logs, and supplier portals must be reviewed periodically.
8. Joiner, mover, and leaver processes must update access promptly when role, employment, contract, supplier relationship, or system purpose changes.
9. AI agents, plugins, tools, and model integrations must be treated as identities or delegated access paths where they can retrieve data, invoke tools, execute actions, or access systems.
10. Exceptions must be documented, approved, time-bound, and monitored.

---

## Evidence Expectations

Evidence may include identity inventory, access approval, privileged access review, service account review, authentication configuration record, leaver access removal record, exception record, and access recertification result.

---

**End of Document**
