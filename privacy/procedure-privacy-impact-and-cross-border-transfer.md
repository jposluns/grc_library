# Privacy Impact and Cross-Border Transfer Procedure

**Document Title:** Privacy Impact and Cross-Border Transfer Procedure\
**Document Type:** Procedure\
**Version:** 1.4.0\
**Date:** 2026-06-22\
**Owner:** Chief Information Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`privacy/template-dpia.md`](template-dpia.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md), [`security/policy-information-security.md`](../security/policy-information-security.md), [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change\
**Repository Path:** [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](procedure-privacy-impact-and-cross-border-transfer.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organisation uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customisation guidance.

---

## Purpose

This procedure defines the process for conducting Privacy Impact Assessments (PIAs), AI Impact Assessments (AI-IAs), and Cross-Border Data Transfer Assessments to identify, evaluate, and mitigate privacy and data protection risks associated with data processing activities, including AI training and inference operations.

---

## Scope

1. Applies to all projects, systems, products, and services that process personal data, sensitive data, or AI-related datasets.
2. Covers new or modified processing activities; AI model development, training, or inference affecting individuals' rights; and any transfer of data across national or regional boundaries.
3. Includes data from all regions where the organisation operates (EU, Canada, US, China, Brazil, and APAC).

---

## Governance

| Role | Responsibility |
|---|---|
| CIO (acting DPO) | Accountable for ensuring PIAs and cross-border transfer reviews are completed in compliance with global privacy laws. |
| CISO | Ensures that technical and organisational measures are implemented to mitigate identified risks. |
| AIGC | Reviews AI-related impact assessments for ethical, transparency, and accountability alignment. |
| Executive Risk Committee (ERC) | Approves high-risk processing activities requiring escalation beyond the CIO. |

High-risk processing activities require CIO approval and ERC escalation.

---

## Procedure

### Step 1: Initiation

**Trigger events:**

- New system or product launch.
- Major changes to processing, purpose, or data categories.
- Introduction of AI or ML components.
- Expansion of processing to new jurisdictions.

The Project Owner must notify the Privacy Office or CIO (acting DPO) before data collection or processing begins. Where the processing is subject to GDPR (or an equivalent regime), the Project Owner must work through the Article 35(1) trigger checklist and the EDPB WP248 nine-criteria framework set out in Section 1 and Section 2 of [`privacy/template-dpia.md`](template-dpia.md) before concluding whether a DPIA is required.

---

### Step 2: Scoping and data mapping

Identify and document:

- Types of personal or sensitive data processed.
- Data sources, collection methods, and intended uses.
- Storage locations and data flows including cross-border transfers.
- Stakeholders, processors, and sub-processors.

---

### Step 3: Risk identification and evaluation

Evaluate risks to data subjects:

- Unauthorized access, disclosure, modification, loss, or misuse.
- Assess likelihood and impact using ISO/IEC 31000 criteria.

For AI systems, identify risks related to:

- Bias and model opacity.
- Data poisoning.
- Cross-border AI model export or data residency violations.

Assign risk level: **Low**, **Medium**, **High**, or **Critical**.

---

### Step 4: Control selection and mitigation

Define and implement:

- Data minimization, pseudonymization, encryption, RBAC, and privacy-by-design features.

For cross-border transfers:

- Use Standard Contractual Clauses (SCCs), APEC CBPR 2.0, or approved adequacy frameworks.

For transfers from China:

- Apply PIPL Articles 38 to 40.

For EU transfers involving AI systems:

- Document compliance with EU Data Act (Regulation (EU) 2023/2854) data-sharing and access obligations (the Act governs obligations on data holders for fair access and use; it does not impose general "export requirements").

---

### Step 5: Consultation and approval

This step has **two distinct pathways**: an internal governance pathway and a regulatory pathway. The pathways may apply independently or in combination; the regulatory pathway is mandatory when its trigger criteria are met and is NOT substituted by the internal pathway.

#### Step 5.1: Internal escalation pathway (organisation governance)

- The CIO (acting DPO) reviews all completed PIAs and transfer assessments.
- For AI systems or high-risk processing, the AIGC conducts additional review per ISO/IEC 42005:2025 and EU AI Act Annex IV.
- If residual risk remains **high**, executive sign-off by the ERC and Legal Counsel is required before go-live.

This is the organisation's internal governance check. It is necessary but not sufficient where the Article 36 regulatory pathway in Step 5.2 also applies.

#### Step 5.2: GDPR Article 36 prior consultation with the supervisory authority (regulatory)

**Trigger.** Article 36(1) requires the controller to consult the supervisory authority prior to processing where a DPIA conducted under Article 35 indicates that the processing would result in a **high risk to the rights and freedoms of natural persons in the absence of measures taken by the controller to mitigate the risk**. In operational terms, if the DPIA's *residual* risk after the controller's planned mitigations remains **high**, Article 36 prior consultation is mandatory before processing begins.

The Article 36 trigger is distinct from the internal Step 5.1 trigger. The internal trigger is the organisation's risk-appetite threshold for executive escalation; the Article 36 trigger is the regulatory threshold for supervisory-authority consultation. A processing activity may trigger one, the other, or both.

**Consultation content (Article 36(3)).** The consultation packet provided to the supervisory authority must include:

| Item | Article 36(3) reference |
|---|---|
| Responsibilities of the controller, joint controllers, and processors (in particular within a group of undertakings) | (a) |
| The purposes and means of the intended processing | (b) |
| The measures and safeguards provided to protect the rights and freedoms of data subjects | (c) |
| Where applicable, the contact details of the DPO | (d) |
| The DPIA report itself | (e) |
| Any other information requested by the supervisory authority | (f) |

**Timeline (Article 36(2)).** The supervisory authority must provide written advice within **8 weeks** of receipt of the consultation request. The period may be extended by a **further 6 weeks** depending on the complexity of the intended processing; the supervisory authority must inform the controller of any extension within **1 month** of receipt of the request. **During the consultation period, the controller must not commence the processing.**

**Supervisory authority powers.** The supervisory authority may (a) issue written advice (the default); or (b) exercise the corrective powers in Article 58 (warnings, orders, processing bans, fines) where the supervisory authority is of the opinion that the intended processing would infringe the GDPR.

**Interaction with the internal escalation pathway (Step 5.1).** The order of operations for a processing activity that triggers both pathways:

1. DPIA complete with residual-risk assessment.
2. Where residual risk is high, the CIO (acting DPO) initiates Article 36 prior consultation with the lead supervisory authority (per the one-stop-shop mechanism for cross-border processing, or with each affected supervisory authority for processing not subject to the one-stop-shop).
3. Supervisory authority responds with written advice or corrective measures within the Article 36(2) timeline.
4. Controller adjusts the processing per the supervisory authority's response, or decides to abandon the processing.
5. Internal ERC sign-off on the adjusted processing for go-live (Step 5.1).

The Article 36 pathway is regulatory and external; the ERC pathway is governance and internal. Both must be cleared before high-residual-risk processing begins.

**Non-EU equivalents.** Other jurisdictions have analogous prior-consultation regimes; consult the per-jurisdiction triggers and timelines in [`privacy/annex-privacy-jurisdiction-index.md`](annex-privacy-jurisdiction-index.md). Notable examples: LGPD Article 38 (Brazil, ANPD prior consultation); PIPL Articles 55-56 (China, CAC security assessment for high-risk transfers); UK GDPR Article 36 (post-Brexit retained equivalent). The trigger thresholds, content requirements, and timelines vary by regime.

#### Step 5.3: Documentation requirements

Both pathways must be evidenced. Records retained per Step 6:

| Pathway | Required records |
|---|---|
| Step 5.1 (internal escalation) | ERC meeting minutes recording the high-residual-risk processing; Legal Counsel sign-off memo; residual-risk acceptance signature by the CIO (acting DPO) |
| Step 5.2 (Article 36 prior consultation) | Article 36(3) consultation packet as sent to the supervisory authority; supervisory authority's written response (advice or corrective measures); the controller's response to the supervisory authority (adjustments made or decision to abandon); evidence of adjustment to processing prior to go-live |

---

### Step 6: Record keeping and documentation

Maintain in the compliance repository:

- Completed PIA/AI-IA report. Where the assessment is a GDPR Article 35 DPIA, use [`privacy/template-dpia.md`](template-dpia.md) for the structural shape, including the Article 35(7) content checklist.
- Data flow diagrams and jurisdiction maps.
- Cross-border transfer assessment logs.
- Mitigation plan and residual risk summary.
- Approvals and sign-off documentation.

All records retained for a minimum of **7 years**.

---

### Step 7: Review and update

PIAs and cross-border transfer records are reviewed:

- Annually.
- Upon significant change to processing or system configuration.
- Upon introduction of new jurisdictions or AI models.

---

## Children's data protection

Processing of children's personal data requires enhanced safeguards including verifiable parental consent and restricted access controls. AI models trained on data from minors must be clearly segregated and subject to periodic bias and risk reviews. Marketing and profiling using children's data is prohibited unless expressly authorized by applicable law.

---

## Framework alignment

| Requirement | Reference |
|---|---|
| Privacy Impact Assessment Requirements | ISO/IEC 27701 §7.5 |
| Data Protection Impact Assessments | GDPR Article 35 |
| Conformity Assessment Information Requirements | EU AI Act Annex IV |
| AI Impact Assessment Obligations (Canada) | AIDA §29 |
| Privacy Impact and Risk Assessment Control | CSA CCM v4.1 PRI-05 |
| AI Impact Assessment | ISO/IEC 42005:2025 |

---

**End of Document**
