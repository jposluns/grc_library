# AI Assurance Case Template

**Document Title:** AI Assurance Case Template\
**Document Type:** Template\
**Version:** 1.0.2\
**Date:** 2026-10-25\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/procedure-ai-assurance-case.md`](procedure-ai-assurance-case.md), [`ai/framework-ai-assurance-evidence.md`](framework-ai-assurance-evidence.md), [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md), [`ai/template-ai-system-register.md`](template-ai-system-register.md), [`compliance/template-audit-evidence-package.md`](../compliance/template-audit-evidence-package.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material AI governance or regulatory change\
**Repository Path:** [`ai/template-ai-assurance-case.md`](template-ai-assurance-case.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template is the record format for the assurance case of an AI system. It is completed and maintained by the AI System Owner under [`ai/procedure-ai-assurance-case.md`](procedure-ai-assurance-case.md), over the evidence model of [`ai/framework-ai-assurance-evidence.md`](framework-ai-assurance-evidence.md). Its structure adapts, by paraphrase and clause reference, the assurance case structure of ISO/IEC/IEEE 15026-2:2022 (Clause 5): a licensed proprietary standard that is not reproduced here.

A populated assurance case identifies real systems, their weaknesses, and their residual risks, and is sensitive operational material. This CC BY-SA 4.0 template contains no example values.

---

## Scope

One assurance case is maintained per AI system in the AI System Register. Parts A, B, D, E, F, and G are completed for every system. Part C (the structured argument) is mandatory for systems at Audit Tier 1 of [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md) Section 3 and optional for Audit Tiers 2 to 4.

---

## Part A: Assurance case report

Part A is the assurance case report: the introduction to and index of the case, usable at decision gates (per the report concept of ISO/IEC/IEEE 15026-2:2022, Clause 3.1.2).

| Field | Required content |
| --- | --- |
| System and service | Description of the AI system and the service it delivers |
| AI System Register reference | Identifier in the AI System Register |
| Audit tier and risk classification | Per [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md) Section 3 and [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md) |
| Environment of use | The operating environment the claims depend on |
| Life cycle | The system life cycle, the current stage, and transition and disposal arrangements |
| Top-level claim | The top-level claim and a discussion of its uncertainty |
| Required degree of confidence | The confidence required in achieving the top-level claim, and why that claim was selected |
| Changes | Changes relevant to the claim made since the previous version, and changes planned for the next |
| Structure mapping | Mapping of this case's elements to the structure of ISO/IEC/IEEE 15026-2:2022 Clause 5, or a documented justification for partial coverage |
| Executive summary | Findings, conclusions, and overall case status for the gate audience |

---

## Part B: Context register

Each context element the argument relies on (ISO/IEC/IEEE 15026-2:2022, Clause 5.3.1):

| Field | Required content |
| --- | --- |
| Context ID | Unique within the case |
| Type | Definition, assumption, or document reference |
| Content | The definition text, the assumption text, or the document reference |
| Applies to | The claim or argument IDs this context governs |

---

## Part C: Argument table

The structured argument layer (mandatory for Audit Tier 1; optional below). Each row is a supported claim per ISO/IEC/IEEE 15026-2:2022, Clause 5.3.5. The nine claims of [`ai/framework-ai-assurance-evidence.md`](framework-ai-assurance-evidence.md) Section 3.1 are entered by reference as the first decomposition level.

| Field | Required content |
| --- | --- |
| Claim ID | Unique within the case |
| Claim | The bounded assertion (for the first level, a reference to the framework Section 3.1 claim) |
| Parent claim | The claim this one supports |
| Argument | The inference deriving the claim from its sub-claims, or the reference to the evidence item that supports it, or the marker "undeveloped" |
| Justification | Why the method of reasoning is valid or has merit (ISO/IEC/IEEE 15026-1:2025, Clause 6.2) |
| Context IDs | Part B entries that apply |
| Status | Developed or undeveloped; an undeveloped argument must have a Part E entry |
| Evidence IDs | Part D entries that support the claim |

---

## Part D: Evidence index

One row per evidence item. The underlying evidence record carries the minimum fields of [`ai/framework-ai-assurance-evidence.md`](framework-ai-assurance-evidence.md) Section 5, requirement 1; this index adds only the case-specific fields of ISO/IEC/IEEE 15026-2:2022, Clause 5.3.2.

| Field | Required content |
| --- | --- |
| Evidence ID | Unique within the case |
| Evidence record reference | Pointer to the framework-conformant evidence record (artefact, class, tier, currency, producer; for quantitative test and evaluation evidence, the precision reporting of [`ai/standard-ai-testing-validation-and-documentation.md`](standard-ai-testing-validation-and-documentation.md) Section 5.6 required for the system's risk tier) |
| Scope of applicability | What the evidence does and does not cover |
| Uncertainty | Credibility of the source and measurement accuracy |
| Assumptions | Assumptions the evidence rests on |

---

## Part E: Gap and undeveloped-argument register

Per [`ai/framework-ai-assurance-evidence.md`](framework-ai-assurance-evidence.md) Section 5, requirement 2: every insufficiency is documented here. A recorded entry does not of itself block a gate; an undocumented gap on a material claim does.

| Field | Required content |
| --- | --- |
| Gap ID | Unique within the case |
| Affected claim | Claim ID |
| Nature | Missing evidence, insufficient evidence, or undeveloped argument |
| What is missing | Statement of the shortfall |
| Closure plan | Actions, owner, and target date |

---

## Part F: Review record and sign-off

| Field | Required content |
| --- | --- |
| Review date | Date of the Section 5 review under the procedure |
| Reviewer and independence | Reviewer role and the independence level met, against the audit-tier minimum |
| Counter-evidence considered | What disconfirming evidence was sought and what was found |
| Outcome | Accepted, accepted with conditions, or returned |
| Sign-off | AI System Owner and reviewer |

---

## Part G: Change log

| Field | Required content |
| --- | --- |
| Change date | Date |
| Trigger | Substantive system modification, environment change, top-level claim change, or material change threshold crossed |
| Parts affected | Which parts of the case changed |
| Summary | What changed and why |

---

## Notation note

This template is notation-neutral: it prescribes record content, not a drawing notation. Adopters using goal structuring notation (GSN), the structured assurance case metamodel (SACM), or claims-arguments-evidence (CAE) tooling can map this structure through the terminology comparison in ISO/IEC/IEEE 15026-2:2022, Annex C.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC/IEEE 15026-2:2022 | Clause 5; Annex C | Assurance case structure (Parts A to D); notation mapping |
| ISO/IEC/IEEE 15026-1:2025 | Clause 6 | Component vocabulary; justification of reasoning; evidence management |
| ISO/IEC/IEEE 15026-4:2021 | Clause 5.2 | The assurance information set Part A records. A revision is pending (an FDIS replacement is under development); this document cites the current 2021 edition |
| NIST AI 100-1 (AI RMF 1.0) | MEASURE 1.1, 1.3 | Documented unmeasured characteristics (Part E); reviewer independence (Part F) |

---

## Limitations

This template records an argument; it does not produce evidence or perform assurance activities. It restates neither the evidence model of [`ai/framework-ai-assurance-evidence.md`](framework-ai-assurance-evidence.md) nor the normative text of the ISO/IEC/IEEE 15026 series, which adopters obtain under licence where they need it. The completed case is not the EU AI Act technical documentation (Article 11 and Annex IV of Regulation (EU) 2024/1689, as amended by Regulation (EU) 2026/1744) and is distinct from the control-centred [`compliance/template-audit-evidence-package.md`](../compliance/template-audit-evidence-package.md). Adopters adapt the part structure, the tier cut-off for Part C, and the review fields to their own governance context.

---

**End of Document**
