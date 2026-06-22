# Privacy and Data Governance Policy

**Document Title:** Privacy and Data Governance Policy\
**Document Type:** Policy\
**Version:** 1.4.2\
**Date:** 2026-06-22\
**Owner:** Chief Information Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-information-security.md`](../security/policy-information-security.md), [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md), [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md), [`compliance/register-global-regulatory-applicability.md`](../compliance/register-global-regulatory-applicability.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, regulatory, or AI governance change\
**Repository Path:** [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organisation uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customisation guidance.

---

## Purpose

This policy defines principles, governance structure, and control framework for managing personal data and organisational information assets across all jurisdictions. It consolidates Privacy Policy, Data Governance Policy, Data Quality Policy, and Records Management Policy into a unified global standard. It supports the organisation's compliance with applicable data protection laws, upholds data accuracy and integrity, and governs ethical use of information including AI training datasets.

**Applicable Frameworks:** ISO/IEC 27701:2025 PIMS (standalone), ISO 8000-8 Data Quality Principles, EU GDPR, EU Data Act (Regulation (EU) 2023/2854; applicable from 12 September 2025), Canada CPPA (Bill C-27 lapsed January 2025), APEC CBPR 2.0, China PIPL, CSA CCM v4.1 domains PRI and DSP.

---

## Scope

1. Applies to all employees, contractors, subsidiaries, and third parties that collect, process, share, or store organisational or personal data.
2. Covers all forms of data, including structured, unstructured, derived, anonymized, synthetic, and AI training datasets.
3. Applies to all geographies where the organisation operates, including cross-border data transfers and multinational data processing arrangements.
4. Encompasses the entire data lifecycle from collection through storage, use, disclosure, retention, and destruction.

---

## Governance and accountability

### Accountable roles

1. The **Chief Information Officer (CIO)** serves as the accountable executive for global data governance and assumes all responsibilities normally assigned to the Data Protection Officer (DPO) until that role is appointed.
2. The **Chief Information Security Officer (CISO)** ensures that security controls protect data confidentiality, integrity, and availability.
3. The CIO, in the capacity of acting DPO, represents the organisation before regulatory authorities and oversees the organisation's compliance with applicable privacy laws.
4. **Regional Data Stewards and Privacy Leads** ensure that compliance with local data protection laws (EU GDPR, CPPA, PIPL, LGPD, etc.).

### Governance committees

- **Data Governance Council (DGC):** Sets strategic data management objectives.
- **AI Governance Council (AIGC):** Ensures that responsible use of data for AI training and operation.

### Roles and responsibilities

| Role | Responsibilities |
|---|---|
| CIO (acting DPO) | Accountable for compliance with privacy and data protection laws, overseeing PIMS implementation, regulatory reporting, and response to data subject requests until a DPO is appointed. |
| CISO | Implements and monitors technical security measures to ensure that data protection and integrity. |
| Data Owners | Accountable for accuracy, quality, and lawful use of data within their domain. |
| Data Stewards | Maintain data dictionaries, classification schemes, and quality validation rules. |
| System Owners | Implement data protection controls, retention schedules, and access management. |
| Employees and Contractors | Handle data in compliance with this policy and complete annual privacy training. |
| Third Parties | Adhere to contractually defined data protection obligations and submit to audits. |
| AI Engineers and Data Scientists | Ensure that AI training datasets comply with privacy, consent, and data minimization requirements. |
| Internal Audit | Reviews data governance effectiveness and verifies compliance. |

---

## Policy requirements

### 1. Lawful and fair processing

- Personal data shall be collected and processed only for legitimate business purposes in compliance with applicable laws.
- Individuals shall be informed about data collection, use, retention, and transfer through transparent notices.
- Consent, where required, must be specific, informed, and revocable.

### 2. Data classification and handling

- All data assets must be classified based on sensitivity: Public, Controlled, Internal, Confidential, and Restricted, per the [Data Classification and Handling Standard](../security/standard-data-classification-and-handling.md).
- Handling procedures for each classification level shall be documented and enforced through technical and organisational controls.
- Sensitive personal data and AI datasets shall be encrypted at rest and in transit.

### 3. Data quality and accuracy

- Data must be accurate, complete, and kept up to date in accordance with ISO 8000-8.
- Periodic validation processes shall verify data integrity, detect anomalies, and prevent unauthorized modification.

### 4. Records and retention management

- Records shall be maintained according to approved retention schedules and applicable legal or regulatory timeframes.
- Destruction or anonymization of records shall be conducted securely and verifiably.
- Retention schedules shall cover both structured data and AI training artifacts.

### 5. Privacy by design and default

- Systems and processes shall embed privacy principles from inception, including data minimization and pseudonymization.
- Privacy Impact Assessments (PIAs) shall be conducted for new systems, major changes, and AI model training activities.
- PIAs shall assess lawful basis, consent management, cross-border data transfer, and model explainability impacts.

### 6. Cross-border data transfers

- All data transfers between jurisdictions must comply with applicable legal mechanisms, such as EU SCCs, APEC CBPR 2.0 certifications, or recognized adequacy decisions.
- The organisation shall maintain a register of all cross-border data flows, reviewed quarterly.
- Transfers to jurisdictions lacking adequate protection must include additional safeguards and executive approval.

### 7. AI training data governance

- AI models shall only be trained on datasets that comply with privacy, consent, and licensing obligations.
- Datasets must include provenance metadata detailing source, collection date, consent type, and processing purpose.
- Disclosure of training dataset categories shall be documented for transparency and compliance with the EU Data Act (Regulation (EU) 2023/2854).
- Synthetic and anonymized data used for AI training shall undergo reidentification risk assessments.

### 8. Data subject rights

- Individuals shall have the right to access, correct, delete, or port their personal data as required under GDPR, CPPA, and PIPL.
- Requests must be processed within legal timeframes (typically 30 days).
- Denials must be justified in writing and reviewed by the CIO (acting DPO).

### 9. Third-party and supplier governance

- All vendors processing personal or regulated data must be assessed for privacy and security compliance before engagement.
- Data processing agreements shall include breach notification, audit rights, and cross-border data protection clauses.
- Supplier performance shall be monitored and reviewed annually.

### 10. Incident response and breach management

- Data breaches shall be reported immediately to the CISO and CIO (acting DPO).
- Regulatory notifications shall be issued within 72 hours (GDPR standard) or as required by local laws.
- Post-incident reviews shall determine root cause, impact, and mitigation actions.

### 11. Monitoring and continual improvement

- Compliance shall be monitored through audits, metrics, and incident trends.
- Lessons learned from data breaches or privacy complaints shall be integrated into training and control design.
- This policy is reviewed annually and upon major regulatory change.

---

## Framework alignment

| Policy Area | ISO/IEC 27701 | COBIT 2019 | CSA CCM v4.1 | Regulatory References |
|---|---|---|---|---|
| Governance and accountability | Clauses 5 to 7 | APO13.01 | PRI-01 | GDPR Art 5, CPPA |
| Lawful processing and consent | Clause 8.2 | DSS05 | PRI-02 | GDPR, PIPL, LGPD |
| Data classification and handling | Clause 8.5 | DSS01 | DSP-01 | ISO 8000-8 §5, SOX, SOC 2 |
| Cross-border data transfers | Clause 8.6 | APO10 | PRI-03 | GDPR Ch V, CBPR 2.0 |
| AI training data governance | N/A | DSS05.06 | DSP-04 | ISO 8000-8 §6, EU Data Act (Regulation (EU) 2023/2854) |
| Data subject rights | Clause 8.7 | MEA01 | PRI-04 | GDPR Arts 15 to 22, CPPA |
| Records management | Clause 8.8 | DSS01 | DSP-02 | ISO 8000-8 §7, Retention laws |
| Breach management | Clause 8.9 | DSS02 | PRI-05 | GDPR Art 33, PIPL Art 57 |

---

**End of Document**
