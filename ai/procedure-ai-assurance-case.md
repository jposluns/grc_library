# AI Assurance Case Procedure

**Document Title:** AI Assurance Case Procedure\
**Document Type:** Procedure\
**Version:** 1.0.6\
**Date:** 2026-10-27\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/framework-ai-assurance-evidence.md`](framework-ai-assurance-evidence.md), [`ai/template-ai-assurance-case.md`](template-ai-assurance-case.md), [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md), [`ai/procedure-ai-audit.md`](procedure-ai-audit.md), [`ai/procedure-ai-evaluation.md`](procedure-ai-evaluation.md), [`ai/charter-ai-governance-council.md`](charter-ai-governance-council.md), [`compliance/template-audit-evidence-package.md`](../compliance/template-audit-evidence-package.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material AI governance or regulatory change\
**Repository Path:** [`ai/procedure-ai-assurance-case.md`](procedure-ai-assurance-case.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure defines how an assurance case for an AI system is established, argued, evidenced, reviewed, reported, maintained, and closed. [`ai/framework-ai-assurance-evidence.md`](framework-ai-assurance-evidence.md) owns the evidence model that the assurance case organizes: the claim taxonomy, the evidence classes, the attestation tiers, and the sufficiency criteria. That framework deliberately defines no assurance activity; this procedure supplies the activity. It adapts the assurance case structure of ISO/IEC/IEEE 15026-2:2022 (Clause 5) to the corpus's existing evidence model, by paraphrase and clause reference only: the 15026 series is a licensed proprietary reference and is not reproduced here.

---

## Scope

Applies to every AI system recorded in the AI System Register. The depth of the assurance case is proportionate to risk: ISO/IEC/IEEE 15026-2:2022 (Clause 4.1) ties how much validity and confidence an assurance case needs to supply to the risk reduction the system is expected to deliver. This procedure graduates depth by the audit tier assigned under [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md) Section 3:

- **Audit Tier 1 (high-risk)**: the full structured argument layer of Section 3 is mandatory.
- **Audit Tiers 2 to 4**: the structured argument layer is optional; the claims-by-evidence record defined in [`ai/framework-ai-assurance-evidence.md`](framework-ai-assurance-evidence.md) Section 3.5, completed per Sections 2 and 4 of this procedure (including the claim list of Section 2.3), is the minimum.

---

## Roles and responsibilities

| Role | Responsibility |
| --- | --- |
| **AI System Owner** | Custodian of the assurance case ([`ai/framework-ai-assurance-evidence.md`](framework-ai-assurance-evidence.md) Section 2.1): establishes it, keeps it current, and marshals it for each gate. |
| **Chief Information Security Officer (CISO)** | Owns this procedure; adjudicates disputed independence, tier, and sufficiency determinations. |
| **Assurance case reviewer** | Performs the Section 5 review at the independence level the system's audit tier requires. |
| **AI Governance Council (AIGC)** | Consumes the assurance case report at deployment-approval and periodic-review gates. |
| **Internal Audit** | Consumes the marshalled case through [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md) Section 4 and [`ai/procedure-ai-audit.md`](procedure-ai-audit.md) Section 3. |

---

## 1. Triggers

1.1 The assurance case must be initiated at the Intake stage of the lifecycle model in [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md) and maintained through to the Retirement stage. ISO/IEC/IEEE 15026-2:2022 (Clause 4.1) advises opening the assurance case as early in the system's life cycle as possible and keeping it maintained until the system's final stage.

1.2 The assurance case must be brought current, and its report produced, before each deployment-approval gate and each audit gate (the marshalling obligation of [`ai/framework-ai-assurance-evidence.md`](framework-ai-assurance-evidence.md) Section 5, requirement 5).

1.3 A material change, per the material change thresholds table in [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md), triggers reassessment of the affected claims, arguments, and evidence.

---

## 2. Establish the case

2.1 The AI System Owner must open an assurance case record using [`ai/template-ai-assurance-case.md`](template-ai-assurance-case.md) and complete its Part A:

- a description of the system, the service it delivers, and its AI System Register reference;
- a description of the environment of use;
- a description of the system's life cycle and its current stage;
- the top-level claim and a discussion of the uncertainty attached to it;
- the degree of confidence required in achieving the top-level claim, and why that claim was selected. ISO/IEC/IEEE 15026-4:2021 (Clause 5.2) lists the claim, the degree of confidence required, the justification of claim selection, the evidence, and the argument as the body of assurance information for a system; a revision of ISO/IEC/IEEE 15026-4:2021 is pending.

2.2 The AI System Owner must record the context the case relies on in Part B of the template: definitions of terms and identifiers, the assumptions the argument depends on, and references to documents concerning the system (the context elements of ISO/IEC/IEEE 15026-2:2022, Clause 5.3.1).

2.3 At every audit tier, the AI System Owner must record each claim the case makes in the claim list of Part C of the template, with a Claim ID unique within the case: the Part A top-level claim, which Part A cites by its Claim ID; the nine assurance claims of [`ai/framework-ai-assurance-evidence.md`](framework-ai-assurance-evidence.md) Section 3.1, by reference; and any system-specific claims. The evidence index, the gap register, and, where completed, the argument table reference claims by these Claim IDs.

---

## 3. Develop the argument

This section is mandatory for Audit Tier 1 systems and optional for Audit Tiers 2 to 4 (see Scope).

3.1 Decompose the top-level claim into the nine assurance claims of [`ai/framework-ai-assurance-evidence.md`](framework-ai-assurance-evidence.md) Section 3.1, by reference and without restating them, and add any system-specific sub-claims the top-level claim needs, entering each sub-claim in the claim list (step 2.3).

3.2 Record each step of reasoning by which a claim is derived from supporting claims or from evidence, following the supported-claim structure of ISO/IEC/IEEE 15026-2:2022 (Clause 5.3.5): a claim, the argument that supports it, and the contexts that apply. Each inference must carry a stated justification of why its method of reasoning is valid or has merit (ISO/IEC/IEEE 15026-1:2025, Clause 6.2).

3.3 Where a part of the argument is not yet developed, it must be recorded explicitly as an undeveloped argument in the sense of ISO/IEC/IEEE 15026-2:2022 (Clause 3.1.7): a marked stand-in for the concrete reasoning that will later take its place. A recorded undeveloped argument is a documented gap: it must carry a closure plan in Part E of the template, and it does not of itself block an approval or audit gate. What blocks a gate is an undocumented gap on a material claim, per [`ai/framework-ai-assurance-evidence.md`](framework-ai-assurance-evidence.md) Section 5, requirement 2.

---

## 4. Link evidence

4.1 Each evidence item in the case must point at an evidence record carrying the minimum fields of [`ai/framework-ai-assurance-evidence.md`](framework-ai-assurance-evidence.md) Section 5, requirement 1. This procedure adds no fields to that record.

4.2 For each evidence item, the case must additionally record its scope of applicability, its uncertainty (covering how credible the source is and how accurate the measurement is), and the assumptions it rests on (the evidence-item fields of ISO/IEC/IEEE 15026-2:2022, Clause 5.3.2).

4.3 Evidence weight and sufficiency are judged by the attestation tiers and sufficiency criteria of [`ai/framework-ai-assurance-evidence.md`](framework-ai-assurance-evidence.md) Sections 3.3 and 3.4, applied by reference. A claim that lacks sufficient evidence must carry a documented gap per that framework's Section 5, requirement 2.

4.4 Each evidence item must reference, by Claim ID, the claims it supports (Part D of the template), and each documented gap must reference, by Claim ID, the claim it affects (Part E of the template).

---

## 5. Review

5.1 Before each gate submission, the assurance case must be reviewed by a reviewer whose independence is graduated by the system's audit tier under [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md) Section 3. The graduation is informed by NIST AI RMF 1.0 (NIST AI 100-1) MEASURE 1.3, under which internal experts who did not serve as front-line developers for the system and/or independent assessors are involved in regular assessments and updates, and domain experts, users, AI actors external to the team that developed or deployed the AI system, and affected communities are consulted in support of assessments as necessary per organizational risk tolerance:

| Audit tier | Minimum reviewer independence |
| --- | --- |
| Audit Tier 1 (high-risk) | A reviewer from a function independent of the development team |
| Audit Tier 2 (general-purpose) | A peer outside the project |
| Audit Tier 3 (standard) | Documented self-review by the AI System Owner |
| Audit Tier 4 (low-risk) | Documented self-review by the AI System Owner |

5.2 The review must weigh whether the claims are true in a balanced manner: ISO/IEC/IEEE 15026-2:2022 (Clause 4.1) advises assessing each claim so that unconscious bias is removed, for example by presenting the full extent of uncertainty that can be considered. The reviewer must look for counter-evidence, not only confirmation, and record the outcome in Part F of the template.

---

## 6. Report and gate submission

6.1 For each gate, the AI System Owner must produce an assurance case report: an introduction to the case with a full index of its claim, argument, and evidence, sufficient for the case to be reassembled from the index (the report concept of ISO/IEC/IEEE 15026-2:2022, Clause 3.1.2, whose notes observe that such reports serve decision gates when a life cycle stage is exited or entered). Part A of the template is the report; its case index field carries the index.

6.2 The report and the marshalled evidence pack are submitted to the AIGC gate, and serve the audit evidence catalogue of [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md) Section 4 and the evidence-collection step of [`ai/procedure-ai-audit.md`](procedure-ai-audit.md) Section 3. Using a structured, evidence-supported argument as the basis for deployment decisions is consistent with the safety-case practice for AI systems described in the International AI Safety Report 2026.

6.3 Boundary. The assurance case is claim-centred and lifecycle-long. It is not the control-centred, audit-time package of [`compliance/template-audit-evidence-package.md`](../compliance/template-audit-evidence-package.md), and it is not the EU AI Act technical documentation: Article 11 of Regulation (EU) 2024/1689, as amended by Regulation (EU) 2026/1744, requires that technical documentation for a high-risk AI system be drawn up before the system is placed on the market or put into service, be kept up to date, and contain, at a minimum, the elements set out in Annex IV; under Article 72(3) as amended, the post-market monitoring plan is part of that technical documentation, and SMEs, including start-ups, and SMCs may provide the Annex IV elements in a simplified manner. The assurance case may index artefacts that also serve those obligations, but it does not discharge them.

---

## 7. Maintenance and change

7.1 The assurance case must be updated by a recorded change whenever the system is substantively modified, its environment changes, or the case's top-level claim changes (ISO/IEC/IEEE 15026-1:2025, Clause 6.1). Materiality is judged against the material change thresholds in [`ai/framework-ai-governance-and-risk.md`](framework-ai-governance-and-risk.md).

7.2 Maintenance planning for the system must keep the assurance claim continuously achieved, evaluate how changes to the system or its environment affect the case, and update and release the case's artefacts under change control (ISO/IEC/IEEE 15026-4:2021, Clause 6.5.25; a revision of ISO/IEC/IEEE 15026-4:2021 is pending). Changes are logged in Part G of the template.

---

## 8. Retirement

8.1 At the Retirement stage of the lifecycle model, the AI System Owner must close the assurance case: record the disposition of the system, mark the case closed, and retain it with its evidence index per the applicable retention schedule.

---

## 9. Records

9.1 The assurance case and its evidence are records under configuration management: each evidence item must be uniquely identified, verifiable, and auditable (evidence-management guidance that ISO/IEC/IEEE 15026-1:2025, Clause 6.3 relays from a guidebook rather than issues as its own direction). ISO/IEC/IEEE 15026-4:2021 (Clause 5.2) treats the assurance information as an element of the system's managed configuration, kept current across the whole life cycle; a revision of ISO/IEC/IEEE 15026-4:2021 is pending.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC/IEEE 15026-1:2025 | Clause 6 | The five assurance case components (claims, arguments, evidence, justifications, assumptions); justification of reasoning; evidence management |
| ISO/IEC/IEEE 15026-2:2022 | Clauses 4 and 5; Annex C | Use, structure, and content of the assurance case; terminology comparison with GSN, SACM, and CAE |
| ISO/IEC/IEEE 15026-4:2021 | Clauses 5.2 and 6.5.25 | Assurance information in the life cycle; maintenance of the assurance claim. A revision is pending (an FDIS replacement is under development); this document cites the current 2021 edition |
| NIST AI 100-1 (AI RMF 1.0) | MEASURE 1.1, 1.3, 2.3 | Documentation of unmeasured characteristics; reviewer independence; deployment-representative demonstration |
| EU AI Act (Regulation (EU) 2024/1689 as amended by Regulation (EU) 2026/1744) | Article 11; Annex IV; Article 72(3) | Boundary only: the technical documentation obligation the assurance case indexes but does not discharge |
| International AI Safety Report 2026 | Safety cases | Structured, evidence-supported arguments as a basis for AI deployment decisions |

---

## Limitations

An assurance case is an argument over evidence, not a substitute for the activities that produce the evidence: a well-structured case over weak evidence is a weak case. This procedure does not define the evidence model (owned by [`ai/framework-ai-assurance-evidence.md`](framework-ai-assurance-evidence.md)), does not perform any testing, evaluation, or audit activity, and does not create legal or regulatory compliance by itself. The ISO/IEC/IEEE 15026 series is paraphrased, not reproduced; adopters needing the normative text obtain the licensed standards. Adopters validate the tier graduation in Section 5 against their own risk tolerance and regulatory context.

---

**End of Document**
