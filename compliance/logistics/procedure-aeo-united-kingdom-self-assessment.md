# UK AEO IT Self-Assessment Procedure

**Document Title:** UK AEO IT Self-Assessment Procedure\
**Document Type:** Procedure\
**Version:** 1.0.2\
**Date:** 2026-07-02\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/logistics/README.md`](README.md), [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](annex-aeo-united-kingdom-cybersecurity.md), [`compliance/policy-compliance-and-audit-management.md`](../policy-compliance-and-audit-management.md), [`compliance/register-global-regulatory-applicability.md`](../register-global-regulatory-applicability.md), [`security/policy-identity-and-access-management.md`](../../security/policy-identity-and-access-management.md), [`security/standard-privileged-access-management.md`](../../security/standard-privileged-access-management.md), [`security/standard-authentication-and-password-management.md`](../../security/standard-authentication-and-password-management.md), [`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md), [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md), [`operations/standard-network-security-and-segmentation.md`](../../operations/standard-network-security-and-segmentation.md), [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md), [`operations/procedure-security-monitoring-and-alert-management.md`](../../operations/procedure-security-monitoring-and-alert-management.md), [`operations/procedure-endpoint-management-and-device-compliance.md`](../../operations/procedure-endpoint-management-and-device-compliance.md), [`resilience/procedure-backup-and-recovery.md`](../../resilience/procedure-backup-and-recovery.md), [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md), [`governance/standard-records-retention-and-destruction.md`](../../governance/standard-records-retention-and-destruction.md)\
**Classification:** Public\
**Category:** Compliance: Logistics Sector\
**Review Frequency:** Annual and upon material regulatory or framework change\
**Repository Path:** [`compliance/logistics/procedure-aeo-united-kingdom-self-assessment.md`](procedure-aeo-united-kingdom-self-assessment.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose and scope

### 1.1 Purpose

This procedure defines the process for completing the IT and cybersecurity elements of the annual Authorized Economic Operator (AEO) and AEO-S (Security and Safety) self-assessment submission to HMRC.

The AEO-S programme, administered by HMRC and Border Force under the UK's implementation of the World Customs Organization (WCO) SAFE Framework of Standards, requires the organization to demonstrate that adequate IT and cybersecurity controls are in place to protect trade systems, trade data, and the integrity of customs documentation.

### 1.2 Scope

This procedure covers only the IT and cybersecurity elements of the AEO-S self-assessment. It does not cover:

- Customs process compliance and trade record-keeping requirements.
- Financial solvency criteria.
- Physical security and site access controls.
- Personnel security outside of IT-relevant background screening.
- Business partner security management.

Those domains are outside IT scope and are governed by the AEO Compliance function (Legal / Finance / Compliance). The CISO's role is to provide the IT evidence package described in this procedure to the AEO Compliance function for inclusion in the overall submission.

The IT control areas covered by this procedure are drawn from the eight AEO-S IT controls mapped in [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](annex-aeo-united-kingdom-cybersecurity.md).

---

## 2. Governance

### 2.1 CISO: IT element lead

The CISO is the lead responsible party for all IT elements of the AEO-S self-assessment. The CISO:

- Initiates IT evidence collection 90 days before the HMRC submission deadline.
- Assigns evidence collection tasks to appropriate technical teams.
- Reviews all IT evidence items before they are included in the IT evidence package.
- Signs off on the IT evidence package before handoff to the AEO Compliance function.
- Coordinates the response to any HMRC follow-up queries on IT elements.

### 2.2 AEO compliance function

The AEO Compliance function (Legal / Finance / Compliance) owns the overall AEO-S self-assessment submission. It provides the CISO with the submission timeline and any HMRC guidance updates. It integrates the IT evidence package into the overall submission and manages the HMRC submission process.

### 2.3 Legal review

Legal reviews the IT evidence package before submission to confirm that:

- No personally identifiable information about individual employees is included.
- No incident detail that could create legal exposure is included in the submission.
- The package accurately represents the organization's compliance position.

### 2.4 CIO sign-off

The CIO provides sign-off on the completed IT evidence package, confirming that the evidence accurately represents the state of IT controls as of the assessment date.

---

## 3. Self-assessment trigger and timeline

### 3.1 Annual trigger

The AEO IT self-assessment is conducted annually. The HMRC submission window is typically in Q4 of the calendar year, subject to annual confirmation from the AEO Compliance function.

### 3.2 Timeline

| Milestone | Target Timing (relative to HMRC submission deadline) | Responsible Party |
|---|---|---|
| AEO Compliance function confirms submission deadline and any updated HMRC guidance | By T-100 days | AEO Compliance function |
| CISO initiates IT evidence collection; assigns tasks to technical teams | T-90 days | CISO |
| Technical teams complete evidence collection for all eight IT control areas | T-60 days | Technical teams (assigned by CISO) |
| CISO reviews all collected evidence; requests remediation of gaps | T-50 days | CISO |
| Legal review of IT evidence package for data protection and legal exposure | T-30 days | Legal |
| CIO sign-off on IT evidence package | T-20 days | CIO |
| IT evidence package delivered to AEO Compliance function | T-10 business days | CISO |
| HMRC submission deadline | T-0 | AEO Compliance function |

---

## 4. IT control evidence collection

Evidence is collected across the eight IT control areas defined in [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](annex-aeo-united-kingdom-cybersecurity.md). Evidence must be:

- Current as of the assessment date (generated within the preceding 12 months unless a longer period is specified).
- Anonymized or aggregated where it would otherwise contain personally identifiable information.
- Summarized where the full document contains commercially sensitive or legally sensitive information not relevant to the HMRC assessment.
- Clearly labelled with the IT control area and the date of the evidence.

### 4.1 Access controls

| Evidence Item | Description | Source |
|---|---|---|
| IAM review report | Output of the most recent identity and access management review, confirming that access to trade-relevant IT systems is restricted to authorized personnel; includes confirmation of role-based access provisioning; aggregated statistics only: no individual names | Identity and Access Management team |
| MFA coverage metric | Percentage of users with multi-factor authentication enabled for access to trade-relevant IT systems; confirmation that MFA is enforced for all Tier 2 and above roles | Identity and Access Management team |
| PAM audit log summary | Summary of privileged access management controls for trade-relevant systems; confirmation that privileged sessions are logged; no individual session detail | Security Operations team |

Governing documents: [`security/policy-identity-and-access-management.md`](../../security/policy-identity-and-access-management.md); [`security/standard-privileged-access-management.md`](../../security/standard-privileged-access-management.md); [`security/standard-authentication-and-password-management.md`](../../security/standard-authentication-and-password-management.md)

### 4.2 System protection

| Evidence Item | Description | Source |
|---|---|---|
| Change management log excerpt | Summary of the change management process applied to trade-relevant IT systems during the preceding 12 months; confirmation that changes are authorized, tested, and documented; no individual change detail | Change Management function |
| Network segmentation evidence | Documentation confirming that trade-relevant IT systems operate within segmented network zones; architecture summary without IP address detail or topology diagrams | Infrastructure / Network team |
| Endpoint protection coverage report | Percentage of endpoints running current endpoint protection software; confirmation of coverage across trade-relevant systems | IT Operations team |

Governing documents: [`operations/standard-network-security-and-segmentation.md`](../../operations/standard-network-security-and-segmentation.md); [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md); [`operations/standard-production-security-requirements.md`](../../operations/standard-production-security-requirements.md); [`operations/procedure-endpoint-management-and-device-compliance.md`](../../operations/procedure-endpoint-management-and-device-compliance.md)

### 4.3 Incident detection and response

| Evidence Item | Description | Source |
|---|---|---|
| SIEM alert coverage report | Confirmation that trade-relevant IT systems are monitored by the SIEM platform; alert coverage metrics; no individual alert or incident detail | Security Operations team |
| Incident register summary | Aggregated summary of security incidents detected and responded to during the preceding 12 months; total count by severity; average response time; confirmation that an incident response process is in place. No individual incident names, descriptions, or affected parties | CISO |

Governing documents: [`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md); [`operations/procedure-security-monitoring-and-alert-management.md`](../../operations/procedure-security-monitoring-and-alert-management.md); [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md)

### 4.4 Personnel screening

| Evidence Item | Description | Source |
|---|---|---|
| Screening completion records | Aggregated count of personnel in Tier 2 and above roles who have completed required background screening; confirmation of screening policy; no individual names or screening results | Human Resources / People function |

Governing documents: Personnel Security Screening Standard

### 4.5 Backup and recovery

| Evidence Item | Description | Source |
|---|---|---|
| Backup job completion report | Summary of backup job completion rates for trade-relevant systems over the preceding 12 months; percentage of successful backups; confirmation of backup scope | Infrastructure / IT Operations team |
| Last successful restore test date | Date of the most recent successful restore test for trade-relevant systems; confirmation that the restore was validated; no detail on system contents restored | Infrastructure / IT Operations team |

Governing documents: [`resilience/procedure-backup-and-recovery.md`](../../resilience/procedure-backup-and-recovery.md)

### 4.6 Risk assessment

| Evidence Item | Description | Source |
|---|---|---|
| Risk register summary | Summary of current information security risk register entries rated High; confirmation that a formal risk assessment process is in place and was conducted within the preceding 12 months. High-risk items listed by risk category only: no detail on specific systems, vulnerabilities, or control gaps | CISO |

Governing documents: [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md)

### 4.7 Control testing

| Evidence Item | Description | Source |
|---|---|---|
| Internal audit report summary | Summary of the most recent internal IT security audit: audit date; scope (trade-relevant systems confirmed as in scope); overall findings count by severity; confirmation that findings are tracked to remediation. No individual finding detail | CISO / Internal Audit |
| Penetration test summary | Date of most recent penetration test; scope confirmation (trade-relevant systems included); overall result (pass / conditional pass / fail); confirmation that critical and high findings were remediated. No individual finding detail, vulnerability names, or test methodology detail | CISO / External Penetration Test provider |

Governing documents: [`compliance/policy-compliance-and-audit-management.md`](../policy-compliance-and-audit-management.md)

### 4.8 Records retention

| Evidence Item | Description | Source |
|---|---|---|
| Retention policy evidence | Reference to the organization's records retention policy confirming that trade records are retained for required periods and that the policy is current | Legal / Compliance / CISO |
| Audit log retention confirmation | Confirmation that audit logs for trade-relevant IT systems are retained for the required minimum period and are protected from tampering | CISO |

Governing documents: [`governance/standard-records-retention-and-destruction.md`](../../governance/standard-records-retention-and-destruction.md); [`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md)

---

## 5. IT evidence package assembly

### 5.1 Package format

The CISO assembles all collected evidence items into the IT evidence package. The package must:

- Use a consistent format with a cover sheet identifying the organization, assessment date, CISO name (role only in the submission version), and submission date.
- Include a table of contents listing each IT control area and the evidence items included.
- Clearly label each evidence item with the control area it supports and the date of the evidence.
- Include a CISO attestation statement confirming that the evidence accurately represents the state of IT controls as of the assessment date.

### 5.2 Anonymization and summarization requirements

The IT evidence package submitted to HMRC must not contain:

- Individual employee names, usernames, or identifiers.
- Individual incident descriptions, affected system names, or vulnerability detail.
- IP addresses, network topology detail, or system architecture diagrams.
- Proprietary tool names or configuration detail that could provide an adversary with exploitable information.

Where source evidence contains such information, the CISO prepares a sanitized summary or extract for inclusion in the package.

---

## 6. Internal review

The IT evidence package is subject to the following sequential review and sign-off before handoff:

1. **CISO review:** Confirms completeness, accuracy, and appropriate anonymization of all evidence items. Requests remediation from technical teams where gaps are identified.
2. **Legal review:** Reviews the package for data protection considerations (ensures that no personal data is included that would require a legal basis for disclosure to HMRC) and for any legal exposure arising from the content of incident summaries or risk register entries.
3. **CIO sign-off:** Provides written sign-off confirming that the IT evidence package accurately represents the state of IT controls as of the assessment date.

---

## 7. Handoff to AEO compliance function

The CISO delivers the completed, reviewed, and CIO-signed IT evidence package to the AEO Compliance function at least 10 business days before the HMRC submission deadline.

Delivery is accompanied by a short briefing note summarizing:

- Any control areas where evidence indicates a gap or weakness.
- Any material changes to IT controls since the previous AEO submission.
- Any recommendations for how the AEO Compliance function should present the IT evidence in the context of the overall submission.

The AEO Compliance function is responsible for integrating the IT evidence package into the overall AEO-S self-assessment submission and for managing the submission to HMRC.

---

## 8. Post-submission: retention of IT evidence package

The CISO retains a complete copy of the IT evidence package as submitted (the version integrated into the HMRC submission) for a minimum of 7 years from the date of submission. Retention is managed in accordance with [`governance/standard-records-retention-and-destruction.md`](../../governance/standard-records-retention-and-destruction.md).

The retained package must include:

- All evidence items as submitted.
- The CISO attestation statement.
- The CIO sign-off record.
- The Legal review confirmation.
- The date of submission to the AEO Compliance function.

---

## 9. HMRC audit response

If HMRC requests follow-up information or conducts an audit of the IT elements of the AEO-S submission, the CISO coordinates the response.

### 9.1 Response process

1. The AEO Compliance function notifies the CISO of the HMRC follow-up request, including the specific IT elements queried and the deadline for response.
2. The CISO reviews the query and determines whether the response can be provided from the retained evidence package or whether additional evidence must be gathered.
3. The CISO prepares the IT response, applies the same anonymization and summarization rules as for the original submission, and submits the response to the AEO Compliance function for transmission to HMRC within the agreed timeline.
4. Legal reviews the response before submission if it addresses incidents, vulnerabilities, or control gaps in more detail than the original submission.

### 9.2 Timeline

The CISO aims to provide the IT response to the AEO Compliance function within 10 business days of receiving the request, or within the HMRC-specified deadline if shorter. Where the HMRC deadline cannot be met due to the complexity of the request, the AEO Compliance function must notify HMRC and request an extension.

---

## 10. Related documents and framework alignment

### 10.1 GRC library documents

| Document | Relevance |
|---|---|
| [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](annex-aeo-united-kingdom-cybersecurity.md) | Defines the eight IT control areas and their mapping to AEO-S requirements; primary reference for evidence collection |
| [`compliance/policy-compliance-and-audit-management.md`](../policy-compliance-and-audit-management.md) | Governs the overall compliance and audit programme; CAPA management |
| [`compliance/register-global-regulatory-applicability.md`](../register-global-regulatory-applicability.md) | Confirms AEO-S as an applicable regulatory obligation |
| [`security/policy-identity-and-access-management.md`](../../security/policy-identity-and-access-management.md) | Access control evidence source |
| [`security/standard-privileged-access-management.md`](../../security/standard-privileged-access-management.md) | PAM evidence source |
| [`security/standard-authentication-and-password-management.md`](../../security/standard-authentication-and-password-management.md) | MFA coverage evidence source |
| [`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md) | SIEM and audit log retention evidence source |
| [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md) | Incident detection and response evidence source |
| [`operations/standard-network-security-and-segmentation.md`](../../operations/standard-network-security-and-segmentation.md) | Network segmentation evidence source |
| [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md) | Change management evidence source |
| [`operations/procedure-security-monitoring-and-alert-management.md`](../../operations/procedure-security-monitoring-and-alert-management.md) | SIEM alert coverage evidence source |
| [`operations/procedure-endpoint-management-and-device-compliance.md`](../../operations/procedure-endpoint-management-and-device-compliance.md) | Endpoint protection coverage evidence source |
| [`resilience/procedure-backup-and-recovery.md`](../../resilience/procedure-backup-and-recovery.md) | Backup and recovery evidence source |
| [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md) | Risk register evidence source |
| [`governance/standard-records-retention-and-destruction.md`](../../governance/standard-records-retention-and-destruction.md) | Records retention evidence source |

### 10.2 External framework alignment

| Framework / Authority | Relevance |
|---|---|
| UK HMRC AEO / AEO-S guidance | Defines AEO-S criteria and self-assessment obligations; primary regulatory driver for this procedure |
| WCO SAFE Framework of Standards: ICT security pillar | Defines international standards for customs IT security that underpin the HMRC AEO-S requirements |
| ISO/IEC 27001:2022 §9.1 | Monitoring and measurement of information security controls; provides the methodology for assessing and evidencing control effectiveness used in Sections 4 and 5 |

---

**End of Document**
