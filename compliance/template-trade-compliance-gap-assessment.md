# Trade Compliance Programme Gap Assessment Template

**Document Title:** Trade Compliance Programme Gap Assessment Template 
**Document Type:** Template 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Compliance Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`compliance/README.md`](README.md), [`compliance/policy-compliance-and-audit-management.md`](policy-compliance-and-audit-management.md), [`compliance/register-ctpat-it-controls.md`](register-ctpat-it-controls.md), [`compliance/register-pip-compliance-controls.md`](register-pip-compliance-controls.md), [`compliance/register-basc-it-responsibilities.md`](register-basc-it-responsibilities.md), [`compliance/annex-aeo-s-it-cybersecurity-requirements.md`](annex-aeo-s-it-cybersecurity-requirements.md), [`compliance/procedure-aeo-it-self-assessment.md`](procedure-aeo-it-self-assessment.md), [`supply-chain/matrix-supply-chain-security-programme-alignment.md`](../supply-chain/matrix-supply-chain-security-programme-alignment.md), [`compliance/procedure-capa.md`](procedure-capa.md) 
**Classification:** Public 
**Category:** Trade Compliance: Gap Assessment 
**Review Frequency:** Annual and upon programme criteria revision, new programme application, or material change to supply chain operations 
**Repository Path:** [`compliance/template-trade-compliance-gap-assessment.md`](template-trade-compliance-gap-assessment.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This template provides a structured approach for assessing the organization's current security controls against the requirements of one or more internationally recognized trade compliance and trusted-trader programmes. It is used for:

- Initial gap assessment prior to applying for a new programme certification
- Annual readiness reviews for existing programme memberships
- Pre-audit preparation before regulatory body validation visits
- Identifying controls that can serve multiple programmes simultaneously (shared evidence)

---

## Assessment header

Complete the following fields for each gap assessment.

| Field | Value |
|---|---|
| **Assessment ID** | `TCGA-[YYYY]-[NNN]` |
| **Assessment Date** | |
| **Programme(s) in Scope** | *(check all that apply)* |
| | ☐ CTPAT (US to CBP) |
| | ☐ PIP (Canada to CBSA) |
| | ☐ AEO-S (UK to HMRC) |
| | ☐ AEO (EU) |
| | ☐ BASC (Latin America) |
| | ☐ NEEC (Mexico to SAT) |
| | ☐ OEA (Brazil to RFB) |
| | ☐ ISO 28000 Supply Chain Security Management |
| **Assessment Scope** | *(describe the supply chain segments, facilities, and operations included)* |
| **Assessor(s)** | *(role titles)* |
| **Review Date** | |
| **Approved By** | Chief Compliance Officer |

---

## Section 1: corporate security and governance

| Requirement Area | Programme Source | Current Control or Evidence | Gap Description | Gap Severity | Remediation Action | Target Date | Owner |
|---|---|---|---|---|---|---|---|
| Written security policy covering supply chain operations | CTPAT; PIP; AEO-S; BASC | [`compliance/policy-compliance-and-audit-management.md`](policy-compliance-and-audit-management.md) | | | | | |
| Designated security management responsibility | CTPAT; PIP; AEO-S | Role defined in security policy | | | | | |
| Internal security audit or self-assessment | AEO-S; CTPAT | [`compliance/procedure-aeo-it-self-assessment.md`](procedure-aeo-it-self-assessment.md) | | | | | |
| Security governance committee or forum | AEO-S; BASC | | | | | | |
| Annual management review of security programme | ISO 28000; AEO-S | | | | | | |

---

## Section 2: physical security

| Requirement Area | Programme Source | Current Control or Evidence | Gap Description | Gap Severity | Remediation Action | Target Date | Owner |
|---|---|---|---|---|---|---|---|
| Perimeter security: fencing, barriers, lighting | CTPAT; PIP; AEO-S; BASC | | | | | | |
| Access controls to cargo storage and handling areas | CTPAT; PIP; AEO-S; BASC; NEEC | | | | | | |
| CCTV or equivalent monitoring of cargo areas | CTPAT; AEO-S; BASC | | | | | | |
| Inspection of incoming and outgoing conveyances | CTPAT; PIP; AEO-S | | | | | | |
| Seals and tamper-evidence on cargo units | CTPAT; PIP; AEO-S; BASC | | | | | | |
| Visitor management and access records | CTPAT; AEO-S; BASC | | | | | | |

---

## Section 3: personnel security

| Requirement Area | Programme Source | Current Control or Evidence | Gap Description | Gap Severity | Remediation Action | Target Date | Owner |
|---|---|---|---|---|---|---|---|
| Pre-employment background screening | CTPAT; PIP; AEO-S; BASC | | | | | | |
| Security awareness and training at hire | CTPAT; PIP; AEO-S; BASC | [`governance/framework-human-capital-and-ethical-conduct.md`](../governance/framework-human-capital-and-ethical-conduct.md) | | | | | |
| Annual security refresher training | CTPAT; AEO-S; BASC | | | | | | |
| Procedures for termination and access revocation | CTPAT; PIP; AEO-S | [`security/procedure-access-control.md`](../security/procedure-access-control.md) | | | | | |
| Employee reporting mechanism for suspicious activity | CTPAT; PIP; AEO-S; BASC | | | | | | |

---

## Section 4: cargo and conveyance security

| Requirement Area | Programme Source | Current Control or Evidence | Gap Description | Gap Severity | Remediation Action | Target Date | Owner |
|---|---|---|---|---|---|---|---|
| Cargo receiving and verification procedures | CTPAT; PIP; AEO-S; BASC | | | | | | |
| Documentation accuracy: manifests, declarations, bills of lading | CTPAT; PIP; AEO-S; NEEC | | | | | | |
| Outbound cargo inspection before loading | CTPAT; PIP; AEO-S | | | | | | |
| Chain of custody documentation across handoffs | CTPAT; AEO-S; ISO 28000 | | | | | | |
| Procedures for detecting and reporting anomalies | CTPAT; PIP; BASC | | | | | | |

---

## Section 5: business partner and supplier security

| Requirement Area | Programme Source | Current Control or Evidence | Gap Description | Gap Severity | Remediation Action | Target Date | Owner |
|---|---|---|---|---|---|---|---|
| Security vetting of trading partners | CTPAT; PIP; AEO-S; BASC | [`supply-chain/procedure-supplier-due-diligence.md`](../supply-chain/procedure-supplier-due-diligence.md) | | | | | |
| Written security requirements in partner contracts | CTPAT; AEO-S | [`supply-chain/standard-third-party-risk.md`](../supply-chain/standard-third-party-risk.md) | | | | | |
| Process for verifying partner AEO/CTPAT/PIP status | CTPAT; AEO-S | | | | | | |
| Periodic reassessment of existing partners | CTPAT; AEO-S; BASC | [`supply-chain/procedure-supplier-audit.md`](../supply-chain/procedure-supplier-audit.md) | | | | | |

---

## Section 6: IT and cybersecurity

| Requirement Area | Programme Source | Current Control or Evidence | Gap Description | Gap Severity | Remediation Action | Target Date | Owner |
|---|---|---|---|---|---|---|---|
| Access control: least privilege, account management | CTPAT IT-1; PIP-IT-1; AEO-S | [`security/procedure-access-control.md`](../security/procedure-access-control.md) | | | | | |
| Multi-factor authentication for remote and privileged access | CTPAT IT-2; PIP-IT-1; AEO-S | [`security/procedure-identity-management.md`](../security/procedure-identity-management.md) | | | | | |
| Vulnerability management and patch cycle | CTPAT IT-3; PIP-IT-5; AEO-S | [`operations/register-it-security-operations.md`](../operations/register-it-security-operations.md) | | | | | |
| Network segmentation and firewall controls | CTPAT IT-4; PIP-IT-4; AEO-S | | | | | | |
| Cyber incident response procedures | CTPAT IT-5; PIP-IT-6; AEO-S | [`resilience/procedure-incident-response.md`](../resilience/procedure-incident-response.md) | | | | | |
| Cybersecurity awareness training | CTPAT IT-6; PIP-IT-7; AEO-S | [`governance/framework-human-capital-and-ethical-conduct.md`](../governance/framework-human-capital-and-ethical-conduct.md) | | | | | |
| IT asset inventory | CTPAT IT-7; PIP-IT-8; AEO-S | [`operations/register-asset-inventory.md`](../operations/register-asset-inventory.md) | | | | | |
| Third-party IT security controls | CTPAT IT-8; PIP-IT-9; AEO-S | [`supply-chain/standard-third-party-risk.md`](../supply-chain/standard-third-party-risk.md) | | | | | |
| Business continuity and IT recovery | CTPAT IT-9; PIP-IT-10; AEO-S | [`resilience/plan-it-disaster-recovery.md`](../resilience/plan-it-disaster-recovery.md) | | | | | |
| Audit logging and monitoring | CTPAT IT-10; AEO-S | [`operations/register-it-security-operations.md`](../operations/register-it-security-operations.md) | | | | | |

**Detailed IT controls mapping:** See [`compliance/register-ctpat-it-controls.md`](register-ctpat-it-controls.md), [`compliance/register-pip-compliance-controls.md`](register-pip-compliance-controls.md), and [`compliance/annex-aeo-s-it-cybersecurity-requirements.md`](annex-aeo-s-it-cybersecurity-requirements.md).

---

## Section 7: incident response and reporting

| Requirement Area | Programme Source | Current Control or Evidence | Gap Description | Gap Severity | Remediation Action | Target Date | Owner |
|---|---|---|---|---|---|---|---|
| Documented procedure for reporting security incidents to programme authority | CTPAT; PIP; AEO-S; BASC | [`security/sop-incident-escalation-matrix.md`](../security/sop-incident-escalation-matrix.md) | | | | | |
| Communication with customs authorities during supply chain disruption | CTPAT; PIP; AEO-S | | | | | | |
| Post-incident review and corrective action | All programmes | [`compliance/procedure-capa.md`](procedure-capa.md) | | | | | |

---

## Section 8: regulatory and customs compliance record

| Requirement Area | Programme Source | Current Control or Evidence | Gap Description | Gap Severity | Remediation Action | Target Date | Owner |
|---|---|---|---|---|---|---|---|
| History of customs compliance: declarations, duty payments | AEO-S (mandatory); AEO (mandatory); CTPAT | | | | | | |
| No serious or repeated infringements of customs rules | AEO-S; AEO; NEEC; OEA | | | | | | |
| Adequate record-keeping systems with audit trail | AEO-S; AEO; CTPAT | | | | | | |
| Financial solvency evidence | AEO-S; AEO; CTPAT | | | | | | |

---

## Gap severity definitions

| Severity | Definition | Response Timeline |
|---|---|---|
| **Critical** | Gap would result in programme disqualification or enforcement action; no compensating control exists | Immediate: resolve before certification submission or renewal |
| **High** | Gap significantly undermines programme requirement; compensating control partially addresses it | 30 days |
| **Medium** | Partial implementation; programme requirement substantially met but evidence gaps exist | 90 days |
| **Low** | Minor documentation or administrative gap; control is implemented but not formally evidenced | 180 days |

---

## Gap summary dashboard

Complete after all sections are assessed.

| Section | Total Requirements | Compliant | Partially Compliant | Non-Compliant | Not Applicable |
|---|---|---|---|---|---|
| 1. Corporate Security and Governance | | | | | |
| 2. Physical Security | | | | | |
| 3. Personnel Security | | | | | |
| 4. Cargo and Conveyance Security | | | | | |
| 5. Business Partner Security | | | | | |
| 6. IT and Cybersecurity | | | | | |
| 7. Incident Response and Reporting | | | | | |
| 8. Regulatory and Customs Compliance | | | | | |
| **Total** | | | | | |

**Overall Readiness Assessment:**
- ☐ Ready for programme application or renewal: no Critical or High gaps
- ☐ Conditional readiness: remediation plan required for High gaps before submission
- ☐ Not ready: Critical gaps require resolution; do not proceed with application

---

## Remediation plan

For each gap rated Critical or High, document a formal remediation plan below. Link each item to a CAPA record using [`compliance/procedure-capa.md`](procedure-capa.md).

| Gap Ref | Gap Description | Programme | Severity | Remediation Steps | CAPA ID | Target Date | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

---

## Sign-off

| Role | Name (role title) | Date | Signature |
|---|---|---|---|
| Assessor | | | |
| Trade Compliance Manager | | | |
| Chief Compliance Officer | | | |

---

**End of Document**
