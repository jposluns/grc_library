# Privacy Impact and Cross-Border Transfer Procedure

**Document Title:** Privacy Impact and Cross-Border Transfer Procedure\
**Document Type:** Procedure\
**Version:** 1.3.2\
**Date:** 2026-05-28\
**Owner:** Chief Information Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md), [`security/policy-information-security.md`](../security/policy-information-security.md), [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change\
**Repository Path:** [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](procedure-privacy-impact-and-cross-border-transfer.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

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

The Project Owner must notify the Privacy Office or CIO (acting DPO) before data collection or processing begins.

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

- Document compliance with EU Data Act export requirements.

---

### Step 5: Consultation and approval

- The CIO (acting DPO) reviews all completed PIAs and transfer assessments.
- For AI systems or high-risk processing, the AIGC conducts additional review per ISO/IEC 42005:2025 and EU AI Act Annex IV.
- If residual risk remains high, executive sign-off by the ERC and Legal Counsel is required before go-live.

---

### Step 6: Record keeping and documentation

Maintain in the compliance repository:

- Completed PIA/AI-IA report.
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
