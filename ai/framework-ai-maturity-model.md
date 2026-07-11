# AI Maturity Model Framework

**Document Title:** AI Maturity Model Framework\
**Document Type:** Framework\
**Version:** 0.0.1\
**Date:** 2026-07-11\
**Owner:** AI Governance Approver\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/charter-ai-governance-council.md`](charter-ai-governance-council.md), [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`governance/standard-maturity-assessment-methodology.md`](../governance/standard-maturity-assessment-methodology.md), [`governance/framework-governance-performance-and-improvement.md`](../governance/framework-governance-performance-and-improvement.md), [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material AI risk, framework, or regulatory change\
**Repository Path:** [`ai/framework-ai-maturity-model.md`](framework-ai-maturity-model.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This framework defines a domain-specific maturity instrument for an organization's AI governance and security. It gives the AI Governance Council the backing instrument for the "AI maturity KPI" recorded in its charter, and it provides the AI-domain view of programme maturity that feeds the organization's governance performance reporting.

It is the AI-domain deepening of the [Maturity Assessment Methodology Standard](../governance/standard-maturity-assessment-methodology.md): it reuses that standard's maturity ladder, its median-of-medians aggregation, and its compensating floor-check, and applies them to a set of AI-specific assessment domains. It does not define a second maturity ladder or a competing aggregation method; where this framework and that standard could differ, the standard governs the ladder and the aggregation, and this framework governs the AI-domain content assessed against them.

The assessment domains are adapted from the OWASP AI Maturity Assessment (AIMA) v1.0 (CC BY-SA 4.0) and cross-referenced to the CMU SEI AI Adoption Maturity Model.

## 2. Scope

This framework applies to the organization's AI programme: the governance structures, the AI systems, and the practices that develop, deploy, and operate them. It assesses AI-programme maturity, not the document-maturity classification that the generated adopter scorecard reports (the two are distinct maturity surfaces, per the Maturity Assessment Methodology Standard Section 8); this framework does not feed or edit that generated artefact.

The assessment is proportionate to the organization's AI footprint: an organization with a small number of low-impact AI systems assesses the same domains at lower resolution than one operating high-impact systems at scale.

## 3. Governance and accountability

| Role | Responsibility |
| --- | --- |
| **AI Governance Council (AIGC)** | Owns the AI maturity assessment; reviews the scored result; sets improvement targets; reports the AI maturity KPI to the Executive Risk Committee. |
| **AI Governance Lead** | Conducts the assessment, gathers evidence per domain, and computes the per-domain and overall maturity levels. |
| **Domain contributors** | Supply the evidence for the domains they own (data, privacy, security, operations). |

## 4. The maturity ladder

This framework uses the five-tier CMMI ladder defined in the [Maturity Assessment Methodology Standard](../governance/standard-maturity-assessment-methodology.md) Section 4, unchanged: Level 1 Initial, Level 2 Managed, Level 3 Defined, Level 4 Quantitatively Managed, Level 5 Optimized. Each assessment domain (Section 5) is rated against this ladder, and the results aggregate per Section 6.

The OWASP AIMA source expresses its criteria as three practice-maturity levels per stream; those three source levels are mapped onto the corpus ladder rather than imported as a separate scale, so the organization carries one maturity ladder across all domains.

## 5. Assessment domains

The assessment covers eight domains, each with three practices, adapted from the OWASP AI Maturity Assessment v1.0. Each practice is evaluated along two complementary streams: **Create and Promote** (stream A: establishing and driving the practice) and **Measure and Improve** (stream B: measuring the practice and improving it on evidence).

| Domain | Practices |
| --- | --- |
| Responsible AI | Ethical values and societal impact; Transparency and explainability; Fairness and bias |
| Governance | Strategy and metrics; Policy and compliance; Education and guidance |
| Data Management | Data quality and integrity; Data governance and accountability; Data used in training |
| Privacy | Data minimization and purpose limitation; Privacy by design and default; User control and transparency |
| Design | Threat assessment; Security architecture; Security requirements |
| Implementation | Secure build; Secure deployment; Defect management |
| Verification | Security testing; Requirement-based testing; Architecture assessment |
| Operations | Incident management; Event management; Operational management |

Each practice is rated at the maturity level (Section 4) that the organization's evidence supports for each stream. An organization selects the domains and practices material to its AI footprint and records why any are out of scope, rather than asserting all of them.

## 6. Scoring and aggregation

The per-domain and overall maturity levels are computed with the median-of-medians aggregation of the [Maturity Assessment Methodology Standard](../governance/standard-maturity-assessment-methodology.md) Section 5, treating each per-practice, per-stream rating as a scored item: the domain level is the median of all its per-practice, per-stream ratings (the three practices assessed across the two streams), and the overall level is the median of the domain levels. The compensating floor-check of that standard's Section 7 applies: any domain or practice assessed at Level 1 (Initial) is surfaced explicitly rather than masked by a higher median, because the median can hide a small number of low outliers.

The AI maturity KPI reported to the AIGC is the overall level together with the floor-check exceptions, not the overall level alone.

## 7. The maturity scorecard

The assessment is recorded in a scorecard that lists, per domain and practice, the assessed level for each stream, the evidence relied on, the target level, and any improvement action. The scorecard is the durable record behind the AI maturity KPI and the input to the improvement targets the AIGC sets.

| Domain | Practice | Stream A level | Stream B level | Evidence | Target | Improvement action |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

## 8. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| Maturity Assessment Methodology Standard | Sections 4, 5, 7 | The maturity ladder, aggregation, and floor-check this framework applies to the AI domain |
| OWASP AI Maturity Assessment (AIMA) v1.0 | Eight domains, three practices, two streams (CC BY-SA 4.0) | The assessment structure, adapted with attribution and share-alike |
| CMU SEI AI Adoption Maturity Model v1.0 | Five-level adoption ladder; eight dimensions | Cross-referenced adoption-maturity view (cited by reference) |
| ISO/IEC 42001:2023 | Clause 9: Performance evaluation | Management-system performance evaluation and improvement |
| NIST AI RMF (2023) | GOVERN and MEASURE functions | Governance maturity and measurement of AI risk |

## 9. Limitations

This framework is original CC BY-SA 4.0 content; its assessment domains are adapted from the OWASP AI Maturity Assessment v1.0 (CC BY-SA 4.0) with attribution and share-alike, and it cross-references the CMU SEI AI Adoption Maturity Model by reference only (that model is copyright-restricted and is not reproduced). A self-assessed maturity level reflects the assessor's evidence and judgement and is subject to optimism bias; the floor-check (Section 6) mitigates but does not remove this. The maturity level is a process-maturity indicator, not a measure of an AI system's capability or safety, and a high maturity level does not by itself establish that any given AI system is low-risk.

---

**End of Document**
