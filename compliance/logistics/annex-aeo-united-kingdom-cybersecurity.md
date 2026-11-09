# UK AEO-S IT and Cybersecurity Requirements

**Document Title:** UK AEO-S IT and Cybersecurity Requirements\
**Document Type:** Annex\
**Version:** 1.0.6\
**Date:** 2026-11-07\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/logistics/README.md`](README.md), [`compliance/logistics/annex-logistics-sector-requirements.md`](annex-logistics-sector-requirements.md), [`compliance/logistics/procedure-aeo-united-kingdom-self-assessment.md`](procedure-aeo-united-kingdom-self-assessment.md), [`compliance/policy-compliance-and-audit-management.md`](../policy-compliance-and-audit-management.md), [`compliance/register-global-regulatory-applicability.md`](../register-global-regulatory-applicability.md), [`compliance/matrix-grc-compliance-alignment.md`](../matrix-grc-compliance-alignment.md), [`security/policy-information-security.md`](../../security/policy-information-security.md), [`security/policy-identity-and-access-management.md`](../../security/policy-identity-and-access-management.md), [`security/standard-privileged-access-management.md`](../../security/standard-privileged-access-management.md), [`security/standard-authentication-and-password-management.md`](../../security/standard-authentication-and-password-management.md), [`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md), [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md), [`operations/standard-network-security-and-segmentation.md`](../../operations/standard-network-security-and-segmentation.md), [`operations/standard-production-security-requirements.md`](../../operations/standard-production-security-requirements.md), [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md), [`operations/procedure-security-monitoring-and-alert-management.md`](../../operations/procedure-security-monitoring-and-alert-management.md), [`operations/procedure-endpoint-management-and-device-compliance.md`](../../operations/procedure-endpoint-management-and-device-compliance.md), [`resilience/procedure-backup-and-recovery.md`](../../resilience/procedure-backup-and-recovery.md), [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md), [`governance/standard-records-retention-and-destruction.md`](../../governance/standard-records-retention-and-destruction.md)\
**Classification:** Public\
**Category:** Compliance: Logistics Sector\
**Review Frequency:** Annual and upon material regulatory or framework change\
**Repository Path:** [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](annex-aeo-united-kingdom-cybersecurity.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

In the UK Authorized Economic Operator (AEO) programme, HMRC tests applicants against the security and safety criteria (UK HMRC AEO security and safety criteria handbook, section 11.1). That Border Force administers the programme is not confirmed by a held source, and the trade facilitation benefits the programme grants are not recorded in the handbook's section 11. The WCO AEO Compendium (2020) United Kingdom entry lists no benefits and names its programme "AEO (European Union Programme)"; the benefits the Compendium's European Union entry lists under the Union Customs Code are not confirmed for the current UK programme. Confirm both with HMRC before relying on them. Under the AEO-S (Authorized Economic Operator Security and Safety) criteria, the applicant's procedures are to be documented and made available for HMRC during the audit of the AEO criteria (section 11.1), its security and safety risk assessment is to address, among other areas, its computer system, accounting records and documents (section 11.2), and it must be able to produce documentation showing the measures and controls it has put in place (section 11.3). The handbook's section 11 does not name cybersecurity or IT security controls; the IT security measures the held handbook names sit under the record keeping criterion, which section 1.4 lists among the AEO-S criteria: appropriate information technology security measures to protect computer systems from unauthorized intrusion and to secure documentation and data (section 8.1), with detail under back-up, recovery, fallback and archiving (section 8.9), protection of computer systems (section 8.10), access rights procedures (section 8.11) and documentation security (section 8.12). The mapping of each control below to those sections is the organization's own; where no held section names a control, as with multi-factor authentication and encryption, this annex treats it as the organization's own scoping of the criteria, to be confirmed with HMRC. This annex defines the organization's IT and cybersecurity controls relevant to AEO-S compliance and maps them to the corresponding GRC library documents.

---

## AEO programme context

HMRC grants AEO status (HMRC Customs Technical Handbook (AEO), section 12.7, under which HMRC can annul an authorization it would not have granted had the application given correct and complete information) and tests AEO-S applicants against the security and safety criteria (UK HMRC AEO security and safety criteria handbook, section 11.1). The HMRC Customs Technical Handbook (AEO) introduction says the UK AEO Programme is based on the World Customs Organization (WCO) SAFE Framework standards (section 1.1), and that AEO-S status is issued to a business established in the UK that fulfils the criteria of customs compliance, appropriate record keeping standards, financial solvency, and appropriate security and safety standards directly related to the activity carried out (section 1.4). The WCO AEO Compendium (2020) lists the United Kingdom among the operational AEO programmes of its Part I, which it describes as AEO programmes based on the WCO SAFE Framework of Standards, and gives the UK programme's title then as "AEO (European Union Programme)". HMRC's AEO-S security and safety criteria (UK HMRC AEO security and safety criteria handbook, section 11) cover, among other areas:

- Physical and access security (sections 11.5, 11.6 and 11.8 to 11.10)
- Personnel security (section 11.7)
- Business partners and external service providers (sections 11.13 and 11.14)
- The computer system, accounting records and documents, as areas the security and safety risk assessment is to address (section 11.2)

This document addresses only the organization's IT and cybersecurity controls for the computer system area (section 11.2) and for the record keeping criterion's IT security measures (section 8.1), mapped by the organization to access rights procedures (section 8.11), protection of computer systems, which names firewalls, anti-virus and other malware protection, back-up routines, user logs and periodic vulnerability management (section 8.10), back-up, recovery, fallback and archiving (section 8.9) and documentation security, which names dealing with incidents which compromise document security and testing systems against unauthorized access (section 8.12); for personnel screening for IT access (section 11.7); and for records retention, which it scopes from the record keeping criterion's procedures to archive and retrieve records and information (sections 8.1 and 8.9), no held section setting a retention period. Section 11 does not name information systems security as a criterion of its own; the held IT security measures sit under the record keeping criterion (section 8), which section 1.4 lists among the AEO-S criteria. All other AEO-S areas are outside IT scope and are governed by the relevant operational and compliance functions.

---

## IT and cybersecurity controls mapping for AEO-S

| Control Objective (the organization's AEO-S scoping, not HMRC text) | IT Control | Governing GRC Document(s) |
| --- | --- | --- |
| Access to IT systems is restricted to authorized personnel | Conditional Access (enterprise identity provider); MFA; PAM; role-based access provisioning | [`security/policy-identity-and-access-management.md`](../../security/policy-identity-and-access-management.md); [`security/standard-privileged-access-management.md`](../../security/standard-privileged-access-management.md); [`security/standard-authentication-and-password-management.md`](../../security/standard-authentication-and-password-management.md) |
| IT systems used for customs and trade operations are protected from unauthorized access and modification | Network segmentation; endpoint protection; change management controls | [`operations/standard-network-security-and-segmentation.md`](../../operations/standard-network-security-and-segmentation.md); [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md); [`operations/standard-production-security-requirements.md`](../../operations/standard-production-security-requirements.md) |
| IT security incidents are detected and responded to promptly | SIEM; endpoint detection and response (EDR) platform; Incident Response Procedure | [`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md); [`operations/procedure-security-monitoring-and-alert-management.md`](../../operations/procedure-security-monitoring-and-alert-management.md); [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md) |
| Personnel with access to sensitive trade IT systems have been security screened | Background screening for Tier 2 and above roles | Personnel Security Screening Standard |
| IT systems are regularly backed up to ensure that continuity is maintained | Cloud-based site recovery service; backup schedule; disaster recovery plan | [`resilience/procedure-backup-and-recovery.md`](../../resilience/procedure-backup-and-recovery.md) |
| IT security risks are formally assessed and managed | Annual risk assessment; risk register | [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md) |
| IT security controls are reviewed and tested | Annual penetration testing; control testing; internal audit | [`compliance/policy-compliance-and-audit-management.md`](../policy-compliance-and-audit-management.md) |
| Trade records are retained for required periods and protected from tampering | Retention policy; collaboration and file storage platform data protection; audit logging | [`governance/standard-records-retention-and-destruction.md`](../../governance/standard-records-retention-and-destruction.md); [`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md) |

---

## Organization's AEO self-assessment

Section 12.2 of the HMRC Customs Technical Handbook (AEO), on monitoring, says HMRC will review an authorized business's AEO status periodically, that regular monitoring is the primary responsibility of the business, and that it is recommended that the business continue to self-assess its compliance with the conditions of the authorization and act on any identified problems as soon as they arise. That is a recommended, continuing self-assessment: no held section names a self-assessment submission to HMRC or an annual cycle. Within section 11, the only self-assessment named is the one in section 11.2, on the security and safety risk assessment, to be carried out by a person with extensive knowledge of the risks and threats applicable to the type of business, and under section 11.3 the documentation of the measures and controls is verified during the AEO audit. The organization's annual AEO self-assessment is its own schedule for the continuing self-assessment section 12.2 recommends, to be confirmed with HMRC. The IT elements of the self-assessment are coordinated by the CISO and completed as part of the annual GRC programme review. The CISO provides documented evidence of IT control effectiveness to the AEO Compliance function, which integrates it into the organization's overall AEO self-assessment and makes it available for HMRC during the audit of the AEO criteria (section 11.1).

---

## References

- UK AEO / AEO-S: HMRC Authorized Economic Operator Guidance
- WCO SAFE Framework of Standards (2025 edition): Annex IV element F (Information Exchange, Access and Confidentiality), the AEO's information security policy and the protection of its electronic systems
- ISO/IEC 27001:2022

---

## Document history

| Version | Date | Change |
| --- | --- | --- |
| 1.0.0 | 2026-05-27 | Initial release |



**End of Document**
