# Adopter Maturity Self-Assessment Template

**Document Title:** Adopter Maturity Self-Assessment Template\
**Document Type:** Template\
**Version:** 1.0.0\
**Date:** 2026-06-20\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`docs/adopter-guide.md`](adopter-guide.md), [`docs/template-quickstart-by-profile.md`](template-quickstart-by-profile.md), [`docs/maturity-scorecard.md`](maturity-scorecard.md), [`docs/decision-tree.md`](decision-tree.md), [`README.md`](../README.md)\
**Classification:** Public\
**Category:** Adopter Experience\
**Review Frequency:** Annual, and on material change to the library's domain structure\
**Repository Path:** [`docs/template-maturity-self-assessment.md`](template-maturity-self-assessment.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template is a guided self-assessment that lets an adopting organisation score its own programme maturity per library domain and overall. The result is a programme-shaped picture of where the adoption is mature and where it is shallow, with concrete next-step guidance per tier.

The existing [`docs/maturity-scorecard.md`](maturity-scorecard.md) rates each library document's stability (Mature, Baseline, Draft). This template rates the adopter's own **adoption maturity** across five tiers, modelled on the standard process-maturity ladder (Initial, Developing, Defined, Managed, Optimising). The two scorecards are complementary: the library scorecard tells the adopter which artefacts are stable enough to copy; the adopter assessment tells the adopter how mature their own use of those artefacts is.

Self-assessment is honest by design. Adopters are encouraged to score conservatively. A Tier-3 programme that knows it is Tier 3 is more useful than a Tier-3 programme that believes it is Tier 4 because the latter will be surprised by an external audit and the former will not.

---

## Scope

This template applies to:

- An adopting organisation conducting its first programme-maturity self-assessment after copying library artefacts.
- An adopting organisation tracking maturity progression year-over-year.
- An external assessor or internal auditor conducting a programme-level review using the library as a reference framework.

It does not replace a formal audit; it produces a directional picture of where a programme stands so the adopter can prioritise where to invest next.

---

## Maturity tiers

The five tiers, modelled on the process-maturity ladder used in NIST CSF Tiers, CMMI, and similar frameworks:

| Tier | Name | Definition |
| --- | --- | --- |
| 1 | Initial | Ad-hoc, reactive. Artefacts copied from the library exist but have not been customised. No assigned owner. Activity is incident-driven. |
| 2 | Developing | Some artefacts customised. Ownership assigned for the core artefacts (policy, register). Activity is mostly reactive but a basic cadence exists. |
| 3 | Defined | Artefacts customised to the organisation's operating model. Ownership assigned for all in-scope artefacts. Documented review cadence applied. Activity is repeatable and broadly applied. |
| 4 | Managed | Quantitative metrics on programme health (review completion rate, control-test pass rate, finding-closure time, etc.). Programme adjustments driven by data, not by opinion. |
| 5 | Optimising | Continuous improvement loop in place. Metrics drive targeted improvements; lessons learned feed back into artefact updates. The library-derived programme is itself a contributor to upstream improvement (issues filed against the library where the adopter has found gaps). |

A programme can be at different tiers per domain. A multi-national might be Tier 4 in `compliance/financial-services/` (heavy external scrutiny drives maturity) and Tier 2 in `architecture/` (less external pressure).

---

## How to use this template

1. **Copy this file into your own corpus** as `adopter-maturity-self-assessment.md` (or a project-specific name). Replace the placeholder header values with the assessment date and the assessor name.
2. **Work through each domain section below** in order. The domains follow the library's 11-domain structure. For each domain, answer the 5 to 8 questions by placing your tier in the response column.
3. **Score the domain** by taking the median of the per-question tiers. Median, not mean, so a single low score does not drag the median; conversely a single high score does not inflate it.
4. **Score the overall programme** by taking the median of the per-domain scores.
5. **Record the assessment date** and the assessor's name in the header. Keep prior assessments alongside the current one so progression is visible year over year.
6. **Use the per-tier next-step guidance** at the end of the document to prioritise the next investment.

A complete self-assessment for a single-domain or single-jurisdiction programme typically takes 1 to 2 hours. A full 11-domain assessment for a multi-national programme typically takes 1 to 2 days, often split across owners by domain.

---

## Assessment

### Section 1: Governance domain

For each statement, place your tier (1 to 5) in the response column. Per-statement guidance follows the table.

| # | Statement | Your tier | Notes |
| --- | --- | --- | --- |
| G1 | A governance charter is in place, customised to our organisation's structure. | _ | |
| G2 | The document inventory (which artefacts we have adopted, where they live, who owns them) is current. | _ | |
| G3 | Each artefact has a named owner and an approving authority defined in the metadata block. | _ | |
| G4 | A documented review cadence is applied: artefacts that are due for review are reviewed on schedule. | _ | |
| G5 | Document and policy approval records are kept (who approved, when, against which version). | _ | |
| G6 | Programme-level performance and improvement reviews happen at least annually. | _ | |
| G7 | Findings from reviews drive concrete artefact updates within a defined timeframe. | _ | |

Per-statement scoring (apply to each statement above):

- Tier 1: No, or the activity happens reactively after an incident.
- Tier 2: Partially. Some artefacts have the property; others do not.
- Tier 3: Yes, applied consistently across the in-scope artefacts.
- Tier 4: Yes, plus we measure the activity (e.g., review completion rate, time to close finding).
- Tier 5: Yes plus measured, and the measurement drives improvements that close back into the library / upstream issues.

**Domain G score (median of G1 to G7):** _

### Section 2: Risk domain

| # | Statement | Your tier | Notes |
| --- | --- | --- | --- |
| R1 | A risk register exists, populated with the organisation's actual top risks (not placeholder content). | _ | |
| R2 | Each risk has an owner, a likelihood and impact rating, and a treatment status. | _ | |
| R3 | A documented risk-assessment methodology is followed when adding or updating risks. | _ | |
| R4 | Risks are reviewed at least annually; high-rated risks at least quarterly. | _ | |
| R5 | Risk-acceptance decisions are recorded with rationale and approving authority. | _ | |
| R6 | Quantitative risk metrics are tracked (e.g., open-risk count by tier, average time to remediation). | _ | |

**Domain R score (median):** _

### Section 3: Compliance domain

| # | Statement | Your tier | Notes |
| --- | --- | --- | --- |
| C1 | A compliance-and-audit-management policy is in place. | _ | |
| C2 | Compliance obligations for our jurisdictions and sectors are registered, with mapping to internal controls. | _ | |
| C3 | An internal audit programme exists; audits run on a defined cadence. | _ | |
| C4 | Audit findings are tracked to closure with a CAPA process. | _ | |
| C5 | Control-testing evidence is centrally captured and refreshed at the defined cadence. | _ | |
| C6 | Cross-framework alignment (ISO 27001, SOC 2, NIST CSF, etc.) is documented where multiple frameworks apply. | _ | |

**Domain C score (median):** _

### Section 4: Privacy domain

| # | Statement | Your tier | Notes |
| --- | --- | --- | --- |
| P1 | A privacy policy is in place and aligned to the home-jurisdiction privacy law. | _ | |
| P2 | A record of processing activities is current. | _ | |
| P3 | Data subject rights requests have a documented handling procedure and tracked turnaround time. | _ | |
| P4 | Breach response procedure is documented and tested at desk-check or tabletop level annually. | _ | |
| P5 | Cross-border transfer mechanisms are documented for each cross-border data flow. | _ | |
| P6 | Children's data, automated decision-making, and special-category processing have dedicated handling where applicable. | _ | |

**Domain P score (median):** _

### Section 5: Security domain

| # | Statement | Your tier | Notes |
| --- | --- | --- | --- |
| S1 | A security policy and an acceptable-use policy are published and acknowledged by staff. | _ | |
| S2 | Access controls are documented and enforced; access reviews happen at least annually. | _ | |
| S3 | Incident-response procedures are documented and tested annually. | _ | |
| S4 | Vulnerability management has a documented cadence (scanning, prioritisation, remediation). | _ | |
| S5 | Cryptography standards (TLS versions, hashing algorithms, key management) are documented and enforced. | _ | |
| S6 | Logging and monitoring requirements are documented; SIEM or equivalent receives feeds. | _ | |
| S7 | A security-awareness training programme runs at least annually. | _ | |

**Domain S score (median):** _

### Section 6: Operations domain

| # | Statement | Your tier | Notes |
| --- | --- | --- | --- |
| O1 | An operations-management policy or framework is in place. | _ | |
| O2 | Change management is documented and applied to operational changes. | _ | |
| O3 | Capacity, performance, and availability are monitored. | _ | |
| O4 | Operational runbooks exist for the recurring procedures the team executes. | _ | |
| O5 | On-call rotation, escalation paths, and out-of-hours coverage are documented. | _ | |

**Domain O score (median):** _

### Section 7: Resilience domain

| # | Statement | Your tier | Notes |
| --- | --- | --- | --- |
| Re1 | A business-continuity policy is in place. | _ | |
| Re2 | A business-impact analysis identifies critical processes and their RTO and RPO. | _ | |
| Re3 | A disaster-recovery plan exists for the critical IT services. | _ | |
| Re4 | Resilience tests run at least annually (tabletop minimum; full failover where the tier warrants). | _ | |
| Re5 | Test results drive updates to the BIA, DR plan, and runbooks. | _ | |

**Domain Re score (median):** _

### Section 8: Supply chain domain

| # | Statement | Your tier | Notes |
| --- | --- | --- | --- |
| Su1 | A supply-chain-and-third-party security policy is in place. | _ | |
| Su2 | The vendor inventory is current; each vendor has a risk rating. | _ | |
| Su3 | Vendor due-diligence procedures are followed before onboarding. | _ | |
| Su4 | Vendor contracts include security and (where applicable) privacy terms. | _ | |
| Su5 | Vendor-incident-response paths and contact lists are current. | _ | |
| Su6 | SBOM or equivalent provenance is required for in-scope software vendors. | _ | |

**Domain Su score (median):** _

### Section 9: Architecture domain

| # | Statement | Your tier | Notes |
| --- | --- | --- | --- |
| A1 | An architecture policy or framework is in place. | _ | |
| A2 | Reference architectures exist for the recurring patterns the organisation builds. | _ | |
| A3 | An architecture-review process applies to material changes. | _ | |
| A4 | Architecture decisions are recorded (ADRs or equivalent). | _ | |
| A5 | Architecture posture (cloud, identity, network) is reviewed at least annually. | _ | |

**Domain A score (median):** _

### Section 10: Developer-security and DevSecOps domain

| # | Statement | Your tier | Notes |
| --- | --- | --- | --- |
| D1 | Developer security requirements are documented and known to the engineering teams. | _ | |
| D2 | CI/CD pipelines include security gates (SAST, SCA, secret scanning, IaC scanning). | _ | |
| D3 | Code reviews include a security checkpoint for changes to security-sensitive code paths. | _ | |
| D4 | Branch-protection rules enforce review and gate-passing on protected branches. | _ | |
| D5 | Developer awareness training covers the language stacks the organisation ships in. | _ | |
| D6 | AI coding assistant usage is governed by documented rules. | _ | |

**Domain D score (median):** _

### Section 11: AI domain

(Skip this section if AI systems are not operationally relevant to the organisation. Otherwise complete it.)

| # | Statement | Your tier | Notes |
| --- | --- | --- | --- |
| AI1 | An AI policy and governance framework are in place. | _ | |
| AI2 | An AI system register is current, classifying systems by risk tier. | _ | |
| AI3 | Each high-risk AI system has a system card; model cards exist for in-scope models. | _ | |
| AI4 | Dataset datasheets exist for training and evaluation datasets in scope. | _ | |
| AI5 | AI-specific risks (bias, hallucination, prompt injection, agent over-permission) are reflected in the risk register. | _ | |
| AI6 | An AI red-team or adversarial-test programme runs on the highest-tier systems. | _ | |
| AI7 | AI vendor due diligence is governed by a dedicated procedure. | _ | |

**Domain AI score (median):** _

---

## Overall programme tier

**Overall programme tier (median of all completed domain scores):** _

---

## Per-tier next-step guidance

### If your programme tier is 1 (Initial)

Focus: get to Tier 2 in the highest-exposure domain first. Pick one domain (typically Privacy if no other regulator is dominant, or the sector overlay if a sector regulator is in scope) and bring it to Tier 2 before broadening. Tier-2 progression is best achieved by:

- Customising the highest-impact artefacts in the chosen domain (policy + one register).
- Assigning a named owner per artefact.
- Adding the artefacts to a basic review schedule.

Investing in a second domain at Tier 1 is less valuable than getting the first domain to Tier 2.

### If your programme tier is 2 (Developing)

Focus: get to Tier 3 across the in-scope domains. The differentiator between Tier 2 and Tier 3 is **consistency**. Tier-3 progression is best achieved by:

- Applying ownership and review cadence to all in-scope artefacts, not just the core few.
- Documenting the review schedule centrally (e.g., as a copy of [`governance/register-document-review-schedule.md`](../governance/register-document-review-schedule.md)).
- Ensuring approval records are kept (consider copying [`governance/template-document-review-record.md`](../governance/template-document-review-record.md)).

Resist the urge to start measuring (Tier-4 behaviour) before Tier 3 is consistent.

### If your programme tier is 3 (Defined)

Focus: introduce metrics. The differentiator between Tier 3 and Tier 4 is **quantitative management**. Tier-4 progression is best achieved by:

- Tracking review completion rate by domain.
- Tracking finding-closure time and open-finding count by severity.
- Reporting a small set of metrics to the governance forum or board.

Metric inflation is a Tier-4 trap; pick fewer than 10 metrics total and keep them stable for at least four cycles before adjusting.

### If your programme tier is 4 (Managed)

Focus: close the improvement loop. The differentiator between Tier 4 and Tier 5 is **learning**. Tier-5 progression is best achieved by:

- Running annual programme-improvement reviews that explicitly trace metric trends to artefact updates.
- Filing issues against the library where the organisation has found gaps the library does not yet cover.
- Sharing lessons-learned externally where appropriate (industry forums, sector groups, regulator-led councils).

A programme stays at Tier 4 if the metrics inform conversations but do not change artefacts.

### If your programme tier is 5 (Optimising)

The programme has reached the top of the standard ladder. Maintenance at this tier requires:

- Continuing to file upstream issues against the library.
- Continuing the improvement loop with the existing cadence; do not let it lapse.
- Mentoring or assisting other adopters where the organisation has capacity (sector forums, internal-audit communities, etc.).

---

## Recording the assessment

Below is a template for recording the assessment. Replace the placeholders.

```
Assessment date: <YYYY-MM-DD>
Assessor: <name and role>
Programme scope: <organisation, business unit, or programme>

Domain scores:
- Governance: <tier>
- Risk: <tier>
- Compliance: <tier>
- Privacy: <tier>
- Security: <tier>
- Operations: <tier>
- Resilience: <tier>
- Supply chain: <tier>
- Architecture: <tier>
- DevSecOps: <tier>
- AI (if in scope): <tier>

Overall tier: <median>

Top three investment priorities for the next year:
1. <domain and specific action>
2. <domain and specific action>
3. <domain and specific action>

Notes / context:
<free text>
```

Keep prior assessments alongside the current one so progression is visible year over year. The prior assessment's "top three investment priorities" plus the current scores should tell a coherent story; if they do not, the gap is itself a finding.

---

## Review questions for the assessor

Before finalising:

1. Did we use the median (not the mean) for per-domain and overall scoring?
2. Did we score conservatively where the organisation has a programme but cannot prove it operates consistently?
3. Did we record per-statement notes for any low scores so the next assessor sees the reasoning?
4. Did we identify the top three investment priorities based on a combination of current tier and exposure (a Tier-1 score in a high-exposure domain is more urgent than a Tier-2 score in a low-exposure domain)?
5. Did we file the assessment in the same location as prior years so progression is auditable?

---

## Maintenance

This template is updated when:

- The library adds or removes a domain that changes the assessment scope.
- A material change to the maturity-tier definitions is warranted (e.g., adoption of a different reference ladder).
- Adopter feedback identifies statements that consistently produce false positives or negatives.

---

## Licence

CC BY-SA 4.0. Adapt and share, including for commercial use; preserve the licence on derivative works.
