# AI Algorithmic Compliance Checklist

**Document Title:** AI Algorithmic Compliance Checklist\
**Document Type:** Checklist\
**Version:** 1.0.1\
**Date:** 2026-06-22\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/policy-ai-compliance.md`](policy-ai-compliance.md), [`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md), [`ai/procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md), [`ai/template-ai-system-register.md`](template-ai-system-register.md), [`ai/template-model-card.md`](template-model-card.md), [`ai/template-system-card.md`](template-system-card.md), [`ai/standard-ai-security-and-risk.md`](standard-ai-security-and-risk.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md)\
**Classification:** Public\
**Category:** AI Governance\
**Review Frequency:** 6 to 12 months and upon material AI governance or regulatory change\
**Repository Path:** [`ai/checklist-ai-algorithmic-compliance.md`](checklist-ai-algorithmic-compliance.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose and usage

This checklist provides a structured assessment tool for evaluating AI system compliance before deployment and at periodic review intervals. It is used by the AIGC and CISO as part of the AI System Impact Assessment Procedure ([`ai/procedure-ai-system-impact-assessment.md`](procedure-ai-system-impact-assessment.md)) and the AI System Audit and Certification Framework ([`ai/framework-ai-system-audit-certification.md`](framework-ai-system-audit-certification.md)).

The checklist is completed by the AI System Owner in the first instance, reviewed by the CISO, and reviewed by the Chief Privacy Officer for items in Section B. For high-risk AI systems (Tier 1), the completed checklist is submitted to the AIGC for approval before deployment.

### Completion instructions

- For each item, select the status: **Yes**, **No**, **Partial**, or **N/A**.
- **Evidence:** Record the document, record, test result, or system reference that substantiates the status selected.
- **Owner:** Record the role responsible for the control.
- **Notes:** Record any relevant context, caveats, or links to associated CAPA records.
- **N/A** may only be used where the item genuinely does not apply to the system. The reason must be recorded in the Notes field.

---

## Checklist header

| Field | Entry |
|---|---|
| AI System Name | |
| AI System Register ID | |
| Risk Tier (EU AI Act) | |
| Risk Tier (NIST AI RMF) | |
| Assessment Type | Pre-deployment / Annual review / Post-incident review / Post-modification review |
| Assessment Date | |
| Assessed By | |
| CISO Review Date | |
| Chief Privacy Officer Review Date | |
| AIGC Approval Date (Tier 1 only) | |

---

## Section a: governance and documentation

*Synthesized from: EU AI Act Art. 11, 13; ISO/IEC 42001:2023 §8.4; NIST AI RMF Govern function*

| # | Control Item | Status (Yes / No / Partial / N/A) | Evidence | Owner | Notes |
|---|---|---|---|---|---|
| A1 | AI system registered in the AI System Register with complete metadata, including system name, version, deployment context, risk tier, intended use, and data categories | | | | |
| A2 | Risk tier classification documented for both the EU AI Act tier and NIST AI RMF risk category; classification reviewed and approved by the AIGC | | | | |
| A3 | Model card completed and current, reflecting the model version in production ([`ai/template-model-card.md`](template-model-card.md)) | | | | |
| A4 | System card completed and current, reflecting the current deployment context, human oversight design, and known limitations ([`ai/template-system-card.md`](template-system-card.md)) | | | | |
| A5 | AI system owner (technical accountability) and operational owner (business accountability) designated and documented in the AI System Register | | | | |
| A6 | Training data provenance documented and validated, including data sources, data quality measures, data exclusions, and governance agreements | | | | |
| A7 | Data quality and bias assessment completed before deployment and at the most recent periodic audit; methodology and results documented | | | | |
| A8 | Explainability approach documented, including the method used, its limitations, and how outputs are communicated to users and overseers | | | | |
| A9 | Intended use, prohibited use cases, and operational limitations clearly defined in the system card and communicated to users and business unit owners | | | | |
| A10 | Human oversight mechanism documented in the system card and tested: designated overseers identified; override capability verified; training completed | | | | |

---

## Section b: data and privacy compliance

*Synthesized from: GDPR Art. 5, 9, 22, 25, 35; EU AI Act Art. 10, 13; ISO/IEC 42001:2023 §8.4; ISO/IEC 27701*

| # | Control Item | Status (Yes / No / Partial / N/A) | Evidence | Owner | Notes |
|---|---|---|---|---|---|
| B1 | Personal data processing performed by the AI system has been mapped; lawful basis for each processing activity is documented | | | | |
| B2 | Data minimization principle applied to training and inference data: only data necessary for the stated purpose is collected and processed | | | | |
| B3 | Privacy Impact Assessment (PIA) or AI-specific impact assessment (AI-IA / FRIA) completed where required by privacy regulation or the AI System Impact Assessment Procedure | | | | |
| B4 | Where the AI system may process data relating to children, specific safeguards are implemented and documented | | | | |
| B5 | Cross-border data transfer controls are in place and documented for any training or inference data transferred across jurisdictions | | | | |
| B6 | Data retention and deletion obligations for training data, inference logs, and output data are documented and implemented | | | | |
| B7 | Training data has been subject to a re-identification risk assessment; residual re-identification risk is documented and accepted by the Chief Privacy Officer | | | | |
| B8 | Where consent is the lawful basis for using training data, consent validity has been verified and records are maintained | | | | |

---

## Section c: security controls

*Synthesized from: OWASP LLM Top 10 (2025); MITRE ATLAS adversarial ML evaluation; EU AI Act Art. 15; NIST AI RMF Measure 2.6; ISO/IEC 42001:2023 §8.4*

| # | Control Item | Status (Yes / No / Partial / N/A) | Evidence | Owner | Notes |
|---|---|---|---|---|---|
| C1 | Prompt injection attack resistance tested (OWASP LLM01): system has been assessed for direct and indirect prompt injection; findings documented and remediated | | | | |
| C2 | Training data poisoning controls in place (OWASP LLM04 Data and Model Poisoning in the 2025 edition): data provenance validated; integrity controls applied; adversarial data injection tested | | | | |
| C3 | Model inversion and membership inference risks assessed (NIST AI RMF MAP 2.3; not a distinct OWASP LLM Top 10:2025 category but related to LLM02 Sensitive Information Disclosure): risk assessment documented; mitigations implemented where risk is material | | | | |
| C4 | Output validation implemented before AI outputs are used in downstream decisions or communicated to users: validation logic documented and tested | | | | |
| C5 | AI system access controls verified: principle of least privilege applied; service accounts are isolated; privileged access is logged and reviewed | | | | |
| C6 | AI system logs (inputs, outputs, decisions, anomalies) forwarded to the SIEM platform and retained for a minimum of 12 months per [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md) | | | | |
| C7 | Adversarial robustness testing completed per MITRE ATLAS evaluation: test scenarios documented; results recorded; findings remediated or risk-accepted | | | | |
| C8 | Third-party model and API dependencies assessed for supply chain risk: provider security posture reviewed; dependency inventory maintained; fallback arrangements documented | | | | |

---

## Section d: operational controls

*Synthesized from: EU AI Act Art. 14, 26; NIST AI RMF Manage function; IEEE 7000-2021 §7.3*

| # | Control Item | Status (Yes / No / Partial / N/A) | Evidence | Owner | Notes |
|---|---|---|---|---|---|
| D1 | Human oversight assigned and documented for all automated or AI-assisted decisions that directly affect individuals: oversight responsibilities are role-specific and not delegated entirely to the AI system | | | | |
| D2 | Automated decision-making with significant impact on individuals is subject to a human review pathway: individuals can request human review; the pathway is tested and documented | | | | |
| D3 | Model performance monitoring is active: accuracy, data drift, and bias drift metrics are captured; alerting thresholds are set; monitoring results are reviewed regularly | | | | |
| D4 | Incident response plan includes AI-specific scenarios: prompt injection, model compromise, adversarial attack, biased output at scale, and GPAI model outage are included | | | | |
| D5 | AI system user notification and transparency disclosures are in place: users are informed they are interacting with an AI system before or at the point of first interaction | | | | |
| D6 | AI-generated content labelling implemented where required: text, images, audio, and video substantially generated by AI and published externally or shared with third parties are labelled (EU AI Act Art. 50) | | | | |

---

## Section e: regulatory compliance

*Synthesized from: EU AI Act 2024 Title I-VIII; Canada AIDA 2024; UK AI Safety Institute guidance 2024; ISO/IEC 42001:2023; NIST AI RMF Govern function*

| # | Control Item | Status (Yes / No / Partial / N/A) | Evidence | Owner | Notes |
|---|---|---|---|---|---|
| E1 | EU AI Act compliance obligations identified and documented for this specific system: risk tier confirmed; applicable Articles listed; deployer obligations addressed | | | | |
| E2 | Canada AIDA obligations assessed and documented: determination made as to whether AIDA high-impact AI system obligations apply; obligations documented and tracked | | | | |
| E3 | UK AI safety priorities reviewed: ICO AI and data protection guidance considered; AI Safety Institute evaluation criteria reviewed for applicable system types | | | | |
| E4 | ISO/IEC 42001:2023 alignment gaps for this system identified and tracked: gaps are recorded in the CAPA system and assigned to owners | | | | |
| E5 | Post-market monitoring plan in place for high-risk systems: plan documents metrics, thresholds, frequency, responsible party, and escalation path | | | | |
| E6 | Serious incident reporting pathway to competent authority established: reporting contacts documented; internal escalation path tested; 15 business day reporting deadline acknowledged | | | | |

---

## Scoring and disposition guidance

### Scoring

1. Count the total number of applicable items (excluding N/A).
2. Count the number of items with a status of **Yes**.
3. Calculate the compliance score as: (Yes count / Applicable item count) × 100.

| Score | Disposition |
|---|---|
| 95% or above | Compliant: proceed to deployment or confirm continued deployment |
| 80% to 94% | Conditional: CAPA records must be raised for all No and Partial items before deployment is approved for Tier 1 systems; for systems in production, remediation plan required within 60 days |
| Below 80% | **High finding**: system must not be deployed until score reaches at least 80%; systems already in production require a formal remediation plan approved by the AIGC within 60 days; CISO reports to AIGC at next scheduled meeting |

### Mandatory CAPA requirements for high-risk (tier 1) systems

For any AI system classified as Tier 1 (High-Risk):

- Any item in **Section A** with a status of **No** or **Partial** must generate a CAPA record before deployment is approved.
- Any item in **Section C** with a status of **No** or **Partial** must generate a CAPA record before deployment is approved.
- CAPAs raised as a condition of deployment must be completed and verified by the CISO before the AI system goes live.

CAPA records are managed per [`compliance/policy-compliance-and-audit-management.md`](../compliance/policy-compliance-and-audit-management.md).

### Re-assessment triggers

This checklist must be re-completed when:

- The AI system undergoes a substantial modification.
- The AI system is deployed in a new context or to a new user population.
- A serious AI incident involving the system is resolved and the system is returned to production.
- Applicable regulations or standards are materially updated.
- The AIGC or CISO determines a re-assessment is warranted based on post-market monitoring signals.

---

**End of Document**
