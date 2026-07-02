# UK AEO-S IT and Cybersecurity Requirements

**Document Title:** UK AEO-S IT and Cybersecurity Requirements\
**Document Type:** Annex\
**Version:** 1.0.3\
**Date:** 2026-07-02\
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

The UK Authorised Economic Operator (AEO) programme, administered by HMRC and Border Force, grants recognized trade facilitation benefits to businesses that meet defined security and safety standards. AEO-S (Security and Safety) specifically requires documented security controls covering IT systems, access controls, personnel security, and cybersecurity. This annex defines the organization's IT and cybersecurity controls relevant to AEO-S compliance and maps them to the corresponding GRC library documents.

---

## AEO programme context

AEO status is granted by HMRC under the UK's implementation of the World Customs Organization (WCO) SAFE Framework of Standards. AEO-S requires that an applicant demonstrates adequate security standards across:

- Physical and access security
- Personnel security
- Business partners
- Information systems security
- Documentation security

This document addresses information systems security only. All other AEO-S domains are outside IT scope and are governed by the relevant operational and compliance functions.

---

## IT and cybersecurity controls mapping for AEO-s

| AEO-S Requirement | IT Control | Governing GRC Document(s) |
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

## Self-assessment obligation

AEO-S requires periodic self-assessment against HMRC AEO criteria. The IT elements of the self-assessment are coordinated by the CISO and completed as part of the annual GRC programme review. The CISO provides documented evidence of IT control effectiveness to the AEO Compliance function for inclusion in the overall AEO self-assessment submission.

---

## References

- UK AEO / AEO-S: HMRC Authorized Economic Operator Guidance
- WCO SAFE Framework of Standards: Information and Communications Technology Security
- ISO/IEC 27001:2022

---

## Document history

| Version | Date | Change |
| --- | --- | --- |
| 1.0.0 | 2026-05-27 | Initial release |



**End of Document**
