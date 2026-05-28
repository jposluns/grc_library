# US CTPAT IT and Cybersecurity Compliance Controls Register

**Document Title:** US CTPAT IT and Cybersecurity Compliance Controls Register 
**Document Type:** Register 
**Version:** 1.0.2 
**Date:** 2026-05-28 
**Owner:** Chief Compliance Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`compliance/logistics/README.md`](README.md), [`compliance/logistics/annex-logistics-sector-requirements.md`](annex-logistics-sector-requirements.md), [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](annex-aeo-united-kingdom-cybersecurity.md), [`compliance/logistics/register-ctpat-united-states-msc-controls.md`](register-ctpat-united-states-msc-controls.md), [`compliance/logistics/register-basc-it-responsibilities.md`](register-basc-it-responsibilities.md), [`compliance/policy-compliance-and-audit-management.md`](../policy-compliance-and-audit-management.md), [`compliance/policy-legal-and-regulatory-compliance.md`](../policy-legal-and-regulatory-compliance.md), [`compliance/matrix-grc-compliance-alignment.md`](../matrix-grc-compliance-alignment.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../../supply-chain/framework-supplier-and-cloud-governance.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../../risk/standard-third-party-and-supply-chain-risk.md) 
**Classification:** Public 
**Category:** Compliance: Logistics Sector 
**Review Frequency:** Annual and upon material CTPAT criteria update, audit finding, or certification renewal 
**Repository Path:** [`compliance/logistics/register-ctpat-united-states-it-controls.md`](register-ctpat-united-states-it-controls.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This register documents the organisation's implementation status against the IT and cybersecurity-related minimum security criteria of the U.S. Customs-Trade Partnership Against Terrorism (CTPAT) programme. It supports CTPAT membership compliance, annual trade partner profile updates, and pre-certification readiness assessments.

**Programme authority:** U.S. Customs and Border Protection (CBP) 
**UK parallel programme:** Authorized Economic Operator to Security and Safety (AEO-S), administered by HMRC 
**Mutual recognition:** CTPAT and UK AEO-S maintain a mutual recognition arrangement under the UK-US Trade and Investment Working Group, providing reciprocal facilitation benefits for qualifying members at points of entry in both countries. See [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](annex-aeo-united-kingdom-cybersecurity.md) for AEO-S IT controls detail.

---

## Programme overview

CTPAT is a voluntary government-business partnership programme administered by U.S. Customs and Border Protection. Members who meet the minimum security criteria receive expedited cargo processing and reduced examination rates at US ports of entry. Since the 2020 criteria revision, IT and cybersecurity form a dedicated minimum security criteria category alongside physical, personnel, procedural, and cargo security.

Membership tiers:
- **Tier 1: Certified:** Minimum criteria met; CTPAT membership active
- **Tier 2: Validated:** CBP Supply Chain Security Specialist (SCSS) has conducted on-site validation
- **Tier 3: Status member:** Consistently exceeds minimum criteria; enhanced facilitation benefits

---

## IT and cybersecurity minimum security criteria

The following table maps each CTPAT IT and cybersecurity minimum security criterion (2020 revision) to the organisation's control framework and implementation status.

| Criterion ID | CTPAT Requirement | Control Reference | Implementation Evidence | Status | Last Reviewed |
|---|---|---|---|---|---|
| IT-1 | **Access Control**: Implement documented access control procedures limiting system access to authorized personnel. Enforce principle of least privilege. Disable or remove dormant accounts promptly. | [`security/procedure-access-control.md`](../../security/procedure-access-control.md), [`security/procedure-identity-management.md`](../../security/procedure-identity-management.md) | Access provisioning records; quarterly access reviews; account deactivation logs | Implemented | |
| IT-2 | **Password and Authentication Management**: Enforce password complexity, minimum length, and rotation requirements. Prohibit sharing of credentials. Implement multi-factor authentication for remote access and privileged accounts. | [`security/procedure-identity-management.md`](../../security/procedure-identity-management.md), [`security/policy-information-security.md`](../../security/policy-information-security.md) | MFA configuration records; password policy enforcement evidence; privileged account MFA attestation | Implemented | |
| IT-3 | **Vulnerability and Security Management**: Conduct periodic vulnerability assessments or penetration tests. Apply security patches in a timely manner. Maintain current antivirus and endpoint protection. | [`dev-security/standard-developer-security-requirements.md`](../../dev-security/standard-developer-security-requirements.md), [`operations/register-it-security-operations.md`](../../operations/register-it-security-operations.md) | Vulnerability scan reports; patch management records; endpoint protection dashboard | Implemented | |
| IT-4 | **IT Infrastructure and Network Management**: Deploy firewalls and intrusion detection or prevention systems. Segment networks carrying cargo and logistics data from general corporate traffic. Encrypt data in transit and at rest where operationally feasible. | [`security/framework-cryptographic-key-lifecycle.md`](../../security/framework-cryptographic-key-lifecycle.md), [`dev-security/standard-devops-security-requirements.md`](../../dev-security/standard-devops-security-requirements.md) | Firewall configuration review; network segmentation diagram; encryption-at-rest attestation | Implemented | |
| IT-5 | **Incident Management and Response**: Maintain a documented cybersecurity incident response plan. Define escalation and notification procedures including notification to CBP when incidents affect supply chain integrity. | [`resilience/procedure-cross-domain-incident-coordination.md`](../../resilience/procedure-cross-domain-incident-coordination.md), [`security/sop-incident-escalation-matrix.md`](../../security/sop-incident-escalation-matrix.md) | Incident response plan; CBP notification runbook; incident logs (current year) | Implemented | |
| IT-6 | **Cyber Threat Awareness Training**: Provide annual cybersecurity awareness training to all personnel with system access. Include phishing recognition, social engineering, and cargo diversion techniques. | [`governance/framework-human-capital-and-ethical-conduct.md`](../../governance/framework-human-capital-and-ethical-conduct.md) | Training completion reports; annual security awareness attestations | Implemented | |
| IT-7 | **Hardware and Software Asset Management**: Maintain an inventory of IT hardware and software used in supply chain operations. Implement procedures for secure disposal of storage media containing trade or cargo data. | [`operations/register-asset-inventory.md`](../../operations/register-asset-inventory.md) | Asset inventory register; media disposal records; decommissioning certificates | Implemented | |
| IT-8 | **Third-Party IT Access Controls**: Assess and manage IT security risks posed by third-party vendors and service providers with access to supply chain systems. Include cybersecurity requirements in vendor contracts. | [`risk/standard-third-party-and-supply-chain-risk.md`](../../risk/standard-third-party-and-supply-chain-risk.md), [`supply-chain/procedure-supplier-due-diligence.md`](../../supply-chain/procedure-supplier-due-diligence.md) | Vendor security assessment records; contract security clauses; third-party access logs | Implemented | |
| IT-9 | **Business Continuity and Recovery**: Maintain documented procedures for recovering critical supply chain IT systems following a cyber incident or outage. Test recovery capability periodically. | [`resilience/plan-it-disaster-recovery.md`](../../resilience/plan-it-disaster-recovery.md), [`resilience/procedure-continuity-and-recovery-testing.md`](../../resilience/procedure-continuity-and-recovery-testing.md) | Recovery test reports; RTO/RPO records; backup validation logs | Implemented | |
| IT-10 | **Logging and Monitoring**: Enable and retain audit logs for systems processing cargo, manifests, or trade data. Review logs for anomalous access or activity. | [`operations/register-it-security-operations.md`](../../operations/register-it-security-operations.md) | Log retention configuration; SIEM monitoring evidence; log review records | Implemented | |

---

## CTPAT-AEO-s control alignment

Both CTPAT and UK AEO-S require substantively equivalent IT security controls. The table below cross-references CTPAT IT criteria with their AEO-S counterparts to support joint compliance and reduce duplication of evidence.

| CTPAT Criterion | AEO-S Equivalent Requirement | Shared Evidence Possible |
|---|---|---|
| IT-1 Access Control | AEO-S: Appropriate access controls for trade systems | Yes |
| IT-2 Authentication | AEO-S: Password policy and privileged access management | Yes |
| IT-3 Vulnerability Management | AEO-S: Regular security reviews and patch management | Yes |
| IT-4 Network Security | AEO-S: IT infrastructure security including network controls | Yes |
| IT-5 Incident Response | AEO-S: Incident reporting to HMRC; documented response procedures | Yes: with HMRC-specific notification supplement |
| IT-6 Awareness Training | AEO-S: Security awareness training for relevant staff | Yes |
| IT-7 Asset Management | AEO-S: Documented IT asset inventory | Yes |
| IT-8 Third-Party Controls | AEO-S: IT security provisions in third-party contracts | Yes |
| IT-9 Business Continuity | AEO-S: IT continuity provisions | Yes |
| IT-10 Logging | AEO-S: Audit trail maintenance for trade records | Yes: retention periods may differ |

See [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](annex-aeo-united-kingdom-cybersecurity.md) for the full AEO-S mapping and HMRC submission requirements.

---

## CTPAT-BASC control alignment

BASC (Business Alliance for Secure Commerce) requires comparable IT security controls for Latin American trade routes. See [`compliance/logistics/register-basc-it-responsibilities.md`](register-basc-it-responsibilities.md) for the detailed BASC IT mapping. Key overlapping criteria:

| CTPAT Criterion | BASC Equivalent |
|---|---|
| IT-1 to IT-3 | BASC IT Security: access control, password management, vulnerability management |
| IT-5 | BASC: Incident management and reporting obligations |
| IT-6 | BASC: Information security awareness training requirements |
| IT-8 | BASC: Third-party supplier IT security requirements |

---

## Programme-wide alignment

For a consolidated view of how CTPAT IT controls map to other applicable trade programmes (BASC, PIP, AEO, AEO-S, NEEC, OEA) and to ISO 28000, see [`supply-chain/matrix-supply-chain-security-programme-alignment.md`](../../supply-chain/matrix-supply-chain-security-programme-alignment.md).

---

## Review and maintenance

| Activity | Frequency | Responsibility |
|---|---|---|
| Control status update | Quarterly | Trade Compliance Manager |
| Evidence refresh for annual CBP profile update | Annually (before profile submission deadline) | Chief Compliance Officer |
| Full register review after CTPAT criteria revision | Within 60 days of CBP publication | Chief Compliance Officer |
| Readiness check prior to CBP SCSS validation visit | On notice of scheduled visit | Trade Compliance Manager |

---

**End of Document**
