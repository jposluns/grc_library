# Trade Compliance Programme Gap Assessment Template

**Document Title:** Trade Compliance Programme Gap Assessment Template\
**Document Type:** Template\
**Version:** 1.0.9\
**Date:** 2026-11-07\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/logistics/README.md`](README.md), [`compliance/logistics/annex-logistics-sector-requirements.md`](annex-logistics-sector-requirements.md), [`compliance/logistics/register-ctpat-united-states-it-controls.md`](register-ctpat-united-states-it-controls.md), [`compliance/logistics/register-pip-canada-controls.md`](register-pip-canada-controls.md), [`compliance/logistics/register-basc-it-responsibilities.md`](register-basc-it-responsibilities.md), [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](annex-aeo-united-kingdom-cybersecurity.md), [`compliance/logistics/procedure-aeo-united-kingdom-self-assessment.md`](procedure-aeo-united-kingdom-self-assessment.md), [`compliance/policy-compliance-and-audit-management.md`](../policy-compliance-and-audit-management.md), [`compliance/procedure-capa.md`](../procedure-capa.md), [`supply-chain/matrix-supply-chain-security-programme-alignment.md`](../../supply-chain/matrix-supply-chain-security-programme-alignment.md)\
**Classification:** Public\
**Category:** Compliance: Logistics Sector\
**Review Frequency:** Annual and upon programme criteria revision, new programme application, or material change to supply chain operations\
**Repository Path:** [`compliance/logistics/template-trade-compliance-gap-assessment.md`](template-trade-compliance-gap-assessment.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template provides a structured approach for assessing the organization's current security controls against the requirements of one or more internationally recognized trade compliance and trusted-trader programmes. It is used for:

- Initial gap assessment prior to applying for a new programme certification
- Annual readiness reviews for existing programme memberships
- Pre-audit preparation before regulatory body validation visits
- Identifying controls that can serve multiple programmes simultaneously (shared evidence)

The Programme Source column names the programmes whose requirements the organization maps each row to. For AEO-S, those attributions are the organization's own scoping, not HMRC text, except where a held section holds them: the held HMRC security and safety criteria (UK HMRC AEO security and safety criteria handbook, section 11) set out no IT control, and no held section names an annual cycle. Section 11 names the computer system as an area the security and safety risk assessment is to address (section 11.2), and lists software providers among the external service providers and expects the business's requirements to be stated in contracts (section 11.14), the held provision nearest to the third-party IT security controls row. The record keeping criterion, which section 1.4 of the HMRC Customs Technical Handbook (AEO) lists among the AEO-S criteria, asks for appropriate information technology security measures to protect computer systems from unauthorized intrusion and to secure documentation and data (section 8.1), with detail under back-up, recovery, fallback and archiving (section 8.9), protection of computer systems, naming firewalls, anti-virus and other malware protection, a business continuity or disaster recovery plan, back-up routines, logs of each user and their actions and periodic vulnerability management (section 8.10), access rights procedures, including the format for setting passwords (section 8.11), and documentation security (section 8.12); those sections are the held provisions nearest to the access control, vulnerability management, network and firewall, business continuity and IT recovery, and audit logging rows, and no held section names multi-factor authentication. Section 12.2 recommends that the business continue to self-assess its compliance with the conditions of the authorization, the held provision nearest to the internal security audit or self-assessment row. Section 12.4 of the HMRC Customs Technical Handbook (AEO) says businesses must notify HMRC of all changes that may affect their AEO status, including disclosure of security incidents, and should notify the AEO Central Site as soon as the change is known or, at the latest, within 14 calendar days of the change, using form C122; the security incident reporting row cites it. Where a row names a section of the HMRC Customs Technical Handbook (AEO) beside AEO-S, that attribution rests on the held section named, to the extent the row states. Confirm each other AEO-S attribution with HMRC before relying on it.

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
| | ☐ ISO 28000:2022 Supply Chain Security Management. ISO 28000:2022 is not held in the reference base; confirm its requirements against the standard before treating this attribution as verified. <!-- ref-absence: ISO 28000:2022 --> |
| **Assessment Scope** | *(describe the supply chain segments, facilities, and operations included)* |
| **Assessor(s)** | *(role titles)* |
| **Review Date** | |
| **Approved By** | Chief Compliance Officer |

---

## Section 1: corporate security and governance

| Requirement Area | Programme Source | Current Control or Evidence | Gap Description | Gap Severity | Remediation Action | Target Date | Owner |
|---|---|---|---|---|---|---|---|
| Written security policy covering supply chain operations | CTPAT; PIP; AEO-S; BASC | [`compliance/policy-compliance-and-audit-management.md`](../policy-compliance-and-audit-management.md) | | | | | |
| Designated security management responsibility | CTPAT; PIP; AEO-S | Role defined in security policy | | | | | |
| Internal security audit or self-assessment | AEO-S; CTPAT | [`compliance/logistics/procedure-aeo-united-kingdom-self-assessment.md`](procedure-aeo-united-kingdom-self-assessment.md) | | | | | |
| Security governance committee or forum | AEO-S; BASC | | | | | | |
| Annual management review of security programme | ISO 28000:2022; AEO-S. ISO 28000:2022 is not held in the reference base; confirm its requirements against the standard before treating this attribution as verified. <!-- ref-absence: ISO 28000:2022 --> | | | | | | |

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
| Security awareness and training at hire | CTPAT; PIP; AEO-S; BASC | [`governance/framework-human-capital-and-ethical-conduct.md`](../../governance/framework-human-capital-and-ethical-conduct.md) | | | | | |
| Annual security refresher training | CTPAT; AEO-S; BASC | | | | | | |
| Procedures for termination and access revocation | CTPAT; PIP; AEO-S | [`security/procedure-access-control.md`](../../security/procedure-access-control.md) | | | | | |
| Employee reporting mechanism for suspicious activity | CTPAT; PIP; AEO-S; BASC | | | | | | |

---

## Section 4: cargo and conveyance security

| Requirement Area | Programme Source | Current Control or Evidence | Gap Description | Gap Severity | Remediation Action | Target Date | Owner |
|---|---|---|---|---|---|---|---|
| Cargo receiving and verification procedures | CTPAT; PIP; AEO-S; BASC | | | | | | |
| Documentation accuracy: manifests, declarations, bills of lading | CTPAT; PIP; AEO-S (customs declarations only: HMRC Customs Technical Handbook (AEO), sections 8.1 and 8.7, which name neither manifests nor bills of lading; section 2.4 names a bill of lading only in describing a carrier); NEEC | | | | | | |
| Outbound cargo inspection before loading | CTPAT; PIP; AEO-S | | | | | | |
| Chain of custody documentation across handoffs | CTPAT; AEO-S; ISO 28000:2022. ISO 28000:2022 is not held in the reference base; confirm its requirements against the standard before treating this attribution as verified. <!-- ref-absence: ISO 28000:2022 --> | | | | | | |
| Procedures for detecting and reporting anomalies | CTPAT; PIP; BASC | | | | | | |

---

## Section 5: business partner and supplier security

| Requirement Area | Programme Source | Current Control or Evidence | Gap Description | Gap Severity | Remediation Action | Target Date | Owner |
|---|---|---|---|---|---|---|---|
| Security vetting of trading partners | CTPAT; PIP; AEO-S; BASC | [`supply-chain/procedure-supplier-due-diligence.md`](../../supply-chain/procedure-supplier-due-diligence.md) | | | | | |
| Written security requirements in partner contracts | CTPAT; AEO-S | [`risk/standard-third-party-and-supply-chain-risk.md`](../../risk/standard-third-party-and-supply-chain-risk.md) | | | | | |
| Process for verifying partner AEO/CTPAT/PIP status | CTPAT; AEO-S | | | | | | |
| Periodic reassessment of existing partners | CTPAT; AEO-S; BASC | [`supply-chain/procedure-supplier-audit.md`](../../supply-chain/procedure-supplier-audit.md) | | | | | |

---

## Section 6: IT and cybersecurity

| Requirement Area | Programme Source | Current Control or Evidence | Gap Description | Gap Severity | Remediation Action | Target Date | Owner |
|---|---|---|---|---|---|---|---|
| Access control: least privilege, account management | CTPAT IT-1; PIP; AEO-S | [`security/procedure-access-control.md`](../../security/procedure-access-control.md) | | | | | |
| Multi-factor authentication for remote and privileged access | CTPAT IT-2; AEO-S | [`security/procedure-identity-management.md`](../../security/procedure-identity-management.md) | | | | | |
| Vulnerability management and patch cycle | CTPAT IT-3; AEO-S | [`operations/register-it-security-operations.md`](../../operations/register-it-security-operations.md) | | | | | |
| Network segmentation and firewall controls | CTPAT IT-4; AEO-S | | | | | | |
| Cyber incident response procedures | CTPAT IT-5; PIP; AEO-S | [`resilience/procedure-cross-domain-incident-coordination.md`](../../resilience/procedure-cross-domain-incident-coordination.md) | | | | | |
| Cybersecurity awareness training | CTPAT IT-6; PIP; AEO-S | [`governance/framework-human-capital-and-ethical-conduct.md`](../../governance/framework-human-capital-and-ethical-conduct.md) | | | | | |
| IT asset inventory | CTPAT IT-7; PIP; AEO-S | [`operations/register-asset-inventory.md`](../../operations/register-asset-inventory.md) | | | | | |
| Third-party IT security controls | CTPAT IT-8; PIP; AEO-S | [`risk/standard-third-party-and-supply-chain-risk.md`](../../risk/standard-third-party-and-supply-chain-risk.md) | | | | | |
| Business continuity and IT recovery | CTPAT IT-9; PIP; AEO-S | [`resilience/plan-it-disaster-recovery.md`](../../resilience/plan-it-disaster-recovery.md) | | | | | |
| Audit logging and monitoring | CTPAT IT-10; AEO-S | [`operations/register-it-security-operations.md`](../../operations/register-it-security-operations.md) | | | | | |

**Detailed IT controls mapping:** See [`compliance/logistics/register-ctpat-united-states-it-controls.md`](register-ctpat-united-states-it-controls.md), [`compliance/logistics/register-pip-canada-controls.md`](register-pip-canada-controls.md), and [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](annex-aeo-united-kingdom-cybersecurity.md).

---

## Section 7: incident response and reporting

| Requirement Area | Programme Source | Current Control or Evidence | Gap Description | Gap Severity | Remediation Action | Target Date | Owner |
|---|---|---|---|---|---|---|---|
| Documented procedure for reporting security incidents to programme authority | CTPAT; PIP; AEO-S (HMRC Customs Technical Handbook (AEO) section 12.4: disclosure of security incidents to HMRC, as a change that may affect AEO status, notified to the AEO Central Site on form C122 within 14 calendar days at the latest); BASC | [`security/sop-incident-escalation-matrix.md`](../../security/sop-incident-escalation-matrix.md) | | | | | |
| Communication with customs authorities during supply chain disruption | CTPAT; PIP; AEO-S | | | | | | |
| Post-incident review and corrective action | All programmes | [`compliance/procedure-capa.md`](../procedure-capa.md) | | | | | |

---

## Section 8: regulatory and customs compliance record

| Requirement Area | Programme Source | Current Control or Evidence | Gap Description | Gap Severity | Remediation Action | Target Date | Owner |
|---|---|---|---|---|---|---|---|
| History of customs compliance: declarations, duty payments | AEO-S (required criterion: under the HMRC Customs Technical Handbook (AEO), section 1.4, AEO-S status is issued to a business that fulfils the criterion of customs compliance and the other criteria that section lists, and section 7.1 sets the conditions applicants must adhere to and says HMRC examines their record of compliance with customs and tax requirements over the 3 years before the application); AEO (mandatory); CTPAT | | | | | | |
| No serious or repeated infringements of customs rules | AEO-S (HMRC Customs Technical Handbook (AEO), section 7.1); AEO; NEEC; OEA | | | | | | |
| Adequate record-keeping systems with audit trail | AEO-S (HMRC Customs Technical Handbook (AEO), section 8.1); AEO; CTPAT | | | | | | |
| Financial solvency evidence | AEO-S (HMRC Customs Technical Handbook (AEO), sections 9.1 and 9.2); AEO; CTPAT | | | | | | |

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

For each gap rated Critical or High, document a formal remediation plan below. Link each item to a CAPA record using [`compliance/procedure-capa.md`](../procedure-capa.md).

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
