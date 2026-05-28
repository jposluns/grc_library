# Supplier Security and Privacy Assurance Procedure

**Document Title:** Supplier Security and Privacy Assurance Procedure 
**Document Type:** Procedure 
**Version:** 1.3.0 
**Date:** 2026-05-27 
**Owner:** Chief Information Security Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`security/policy-information-security.md`](../security/policy-information-security.md), [`governance/standard-records-retention-and-destruction.md`](standard-records-retention-and-destruction.md), [`security/procedure-incident-response.md`](../security/procedure-incident-response.md) 
**Classification:** Public 
**Category:** Governance 
**Review Frequency:** Annual or as required by regulatory or framework changes 
**Repository Path:** [`governance/procedure-supplier-security-and-privacy-assurance.md`](procedure-supplier-security-and-privacy-assurance.md) 
**Confidentiality:** Public 
**Licence:** CC0 1.0 Universal 

This procedure defines the security, privacy, and trade-compliance assurance process for suppliers, vendors, and service providers that handle, process, or transmit organizational, personal, or trade data.

---

## Purpose

To ensure that all third parties meet the organization's technical, privacy, and regulatory standards before engagement and throughout the supplier relationship lifecycle, including ISO/IEC 27001, ISO/IEC 27701, ISO 28000, BASC International Standard v6, and WCO SAFE requirements.

---

## Scope

1. Applies to all third parties providing IT, logistics, customs, data processing, or AI services.
2. Covers all stages of the supplier relationship lifecycle: pre-engagement evaluation, contract negotiation, ongoing monitoring, and termination.
3. Applies to suppliers handling organizational or customer data, personal data subject to privacy laws, trade and customs data regulated under BASC and WCO SAFE, and AI model or dataset services.

---

## Governance and Accountability

| Role | Responsibility |
| --- | --- |
| **CIO** | Provides strategic oversight and approves the supplier assurance framework. |
| **CISO** | Owns the supplier-security assurance programme; validates compliance requirements; approves risk exceptions. |
| **Procurement and Legal** | Ensure that contractual clauses align with security, privacy, and BASC trade-security obligations. |
| **Supplier Relationship Owners (SROs)** | Manage supplier onboarding, evidence collection, and assurance documentation. |
| **Regional BASC Compliance Officers** | Validate trade and customs suppliers for BASC and WCO SAFE compliance. |
| **Privacy Officer / DPO** | Reviews suppliers' data handling and privacy safeguards. |
| **Internal Audit** | Verifies supplier assurance records and evidence of compliance. |

---

## 1. Supplier Risk Tiering

All suppliers are classified by risk tier before onboarding. Tier classification is based on data sensitivity, access scope, and regulatory exposure.

| Tier | Description | Examples | Review Cadence |
| --- | --- | --- | --- |
| **Tier 1: Critical** | Direct access to Restricted or Confidential data; cloud infrastructure providers; AI model or training dataset processors; BASC-regulated logistics and customs platforms. | Cloud platform provider, CSPM vendor, customs broker IT, AI SaaS | Semi-annual |
| **Tier 2: High** | Access to Internal data; SaaS platforms used by all employees; payroll and HR processors. | Payroll processor, collaboration platform provider | Annual |
| **Tier 3: Moderate** | Access to Controlled data; professional services with limited data exposure. | Consulting firms with scoped access | Biennial |
| **Tier 4: Low** | No direct data access; low-risk ancillary services. | Office supplies, facility maintenance | As needed |

---

## 2. Pre-Engagement Due Diligence

Before engaging a new supplier, the Supplier Relationship Owner completes the Supplier Security and Privacy Questionnaire (SSPQ), which captures:

- Security certifications (ISO 27001, SOC 2, or BASC equivalency).
- Privacy compliance statement (GDPR, CPPA, AIDA, or applicable law).
- Trade-security compliance (BASC certification or WCO SAFE AEO equivalency) for logistics suppliers.
- AI data governance policies where the supplier processes training data or model artifacts.
- Subprocessor list and data residency confirmation.
- Breach notification process and response time commitments.

Procurement shall not finalize vendor selection until:

- The SSPQ is completed and reviewed by the CISO.
- All Critical security gaps are remediated or accepted via a documented risk exception approved by the CISO.
- BASC trade suppliers have provided proof of valid certification.

---

## 3. Contractual Security and Privacy Requirements

All supplier contracts must include the following provisions:

| Clause | Requirement |
| --- | --- |
| **Data protection** | Confidentiality obligations; AES-256 encryption at rest and TLS 1.3 in transit; access controls per least-privilege. |
| **Privacy compliance** | Compliance with GDPR, CPPA, AIDA, and applicable jurisdictional laws; data processing agreement (DPA) where required. |
| **Trade compliance** | BASC and WCO SAFE obligations for logistics suppliers; customs data handling per BASC Section 6. |
| **Incident notification** | Notification to the organization within 24 hours of any breach or suspected compromise affecting organizational data. |
| **Audit rights** | Right to audit or request evidence of compliance; penetration test results upon request. |
| **Subprocessing** | Approval required for new subprocessors; equivalent obligations flow down contractually. |
| **Data return / destruction** | Data returned or destroyed upon contract termination; certificate of destruction provided. |

BASC trade suppliers must provide proof of valid BASC certification or WCO SAFE AEO equivalency as a contract condition.

---

## 4. Supplier Evidence and Monitoring

### 4.1 Evidence Collection

The SRO collects and maintains evidence in the Supplier Assurance Repository:

- Certifications and attestations (ISO 27001, ISO 27701, BASC, SOC 2 Type II).
- Applicable policy documents and security questionnaire responses.
- Penetration test results (Tier 1 and Tier 2 suppliers).
- Data-flow diagrams and jurisdiction mapping.
- AI model governance records where applicable.

Evidence is retained in the Supplier Assurance Repository for 7 years per the Records Retention and Destruction Standard.

### 4.2 Ongoing Monitoring

| Activity | Tier 1 | Tier 2 | Tier 3 |
| --- | --- | --- | --- |
| Certification renewal check | Semi-annual | Annual | Biennial |
| SSPQ re-attestation | Semi-annual | Annual | Biennial |
| Penetration test result review | Annual | Biennial | On request |
| Subprocessor list review | Quarterly | Annual | On change |

Continuous threat intelligence monitoring for Tier 1 suppliers is performed by Security Operations where technically feasible.

---

## 5. Breach and Incident Response Coordination

Upon receiving a supplier breach notification:

1. The SRO immediately notifies the CISO and Privacy Officer.
2. Security Operations initiates the Incident Response Procedure.
3. Legal Counsel assesses regulatory notification obligations by jurisdiction.
4. The CISO and Privacy Officer coordinate response activities with the supplier.
5. Regulatory notifications (GDPR 72-hour, CPPA, applicable laws) are assessed and issued.

Failure by a supplier to notify within the contractually required 24-hour window constitutes a material contract breach and triggers a supplier risk escalation review.

---

## 6. Termination and Offboarding

Upon contract termination, the SRO coordinates the following within 30 days:

| Obligation | SLA |
| --- | --- |
| Revoke all system and network access | 24 hours of termination |
| Return or securely destroy all organizational data | 30 days |
| Provide data-destruction certificate | 30 days |
| Archive all assurance evidence | Upon offboarding completion |

Offboarding evidence is retained for 7 years. Where a supplier holds BASC-regulated trade data, the Regional BASC Compliance Officer must confirm destruction compliance.

---

## 7. Metrics

Supplier assurance metrics are reported to the CISO quarterly:

| Metric | Target |
| --- | --- |
| Tier 1 suppliers with current SSPQ | 100% |
| Tier 1 suppliers with valid ISO 27001 / SOC 2 certification | ≥ 90% |
| Supplier breach notifications received and processed within SLA | 100% |
| Offboarding completed with destruction certificate | 100% |
| Risk exceptions open > 90 days | Zero critical exceptions |

---

## Framework Alignment

| Control Area | ISO/IEC 27001 | ISO/IEC 27701 | COBIT 2025 | CSA CCM v5 | Other |
| --- | --- | --- | --- | --- | --- |
| Supplier due diligence | A.5.19, A.5.20 | §7.3 | APO10 | STA-01, STA-02 | ISO 28000 |
| Contractual requirements | A.5.20 | §7.3.5 | APO10.03 | STA-03, STA-04 | BASC v6 §6 |
| Monitoring and review | A.5.22 | §7.3.6 | APO10.04 | STA-05 | WCO SAFE |
| Termination and offboarding | A.5.20 | §7.3.7 | APO10.05 | STA-06 | N/A |
| Breach coordination | A.5.24 to 5.28 | §8.9 | DSS02 | SEF-02 | GDPR Art. 33 |



**End of Document**
