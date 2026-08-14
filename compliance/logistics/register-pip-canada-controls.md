# Canada PIP IT and Cybersecurity Compliance Controls Register

**Document Title:** Canada PIP IT and Cybersecurity Compliance Controls Register\
**Document Type:** Register\
**Version:** 1.0.5\
**Date:** 2026-08-14\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/logistics/README.md`](README.md), [`compliance/logistics/annex-logistics-sector-requirements.md`](annex-logistics-sector-requirements.md), [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](annex-aeo-united-kingdom-cybersecurity.md), [`compliance/logistics/register-ctpat-united-states-it-controls.md`](register-ctpat-united-states-it-controls.md), [`compliance/logistics/register-basc-it-responsibilities.md`](register-basc-it-responsibilities.md), [`compliance/policy-compliance-and-audit-management.md`](../policy-compliance-and-audit-management.md), [`compliance/policy-legal-and-regulatory-compliance.md`](../policy-legal-and-regulatory-compliance.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../../supply-chain/framework-supplier-and-cloud-governance.md), [`supply-chain/matrix-supply-chain-security-programme-alignment.md`](../../supply-chain/matrix-supply-chain-security-programme-alignment.md)\
**Classification:** Public\
**Category:** Compliance: Logistics Sector\
**Review Frequency:** Annual and upon material CBSA criteria update, audit finding, or certification renewal\
**Repository Path:** [`compliance/logistics/register-pip-canada-controls.md`](register-pip-canada-controls.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register documents the organization's IT and cybersecurity controls and maps them to the cybersecurity expectations of Canada's Partners in Protection (PIP) programme administered by the Canada Border Services Agency (CBSA). It supports PIP membership, the annual security-profile update in the CBSA Trusted Trader Portal, and application readiness.

**Programme authority:** Canada Border Services Agency (CBSA)\
**UK parallel programme:** Authorized Economic Operator to Security and Safety (AEO-S), administered by HMRC\
**US parallel programme:** Customs-Trade Partnership Against Terrorism (CTPAT), administered by CBP\
**Mutual recognition:** The CBSA maintains Authorized Economic Operator mutual recognition arrangements with partner customs administrations; the held reference material documents the Canada-Mexico AEO mutual recognition arrangement, signed in Cancun, Mexico, on 11 May 2016. Organizations holding a partner-programme certification (for example CTPAT, or an AEO or AEO-S scheme) should confirm the current scope of any applicable arrangement against the CBSA's published mutual recognition arrangements before relying on it for evidence reuse. The UK AEO-S programme derives from the WCO SAFE Framework and provides functionally comparable security and safety certification.

---

## Programme overview

PIP is a voluntary partnership programme in which businesses commit to enhancing border security in exchange for expedited cargo processing at Canadian ports of entry. The programme is administered by CBSA and aligns with the World Customs Organization (WCO) SAFE Framework of Standards. The PIP security profile is organized into four security areas: corporate security, cargo and conveyance security, physical security, and supply chain partner security. Cybersecurity is addressed within the corporate security area; PIP does not publish a separate, numbered information-technology requirement set. The control references below are the organization's own, mapped to those PIP cybersecurity expectations.

PIP membership process: an applicant completes the security-profile questionnaire in the CBSA Trusted Trader Portal and submits supporting evidence (documents and photographs). The CBSA reviews the profile and may conduct an on-site validation. Members review and update their security profile in the Trusted Trader Portal at least annually. The CBSA does not publish a tiered-membership ladder for PIP.

---

## Organization IT and cybersecurity controls (mapped to PIP corporate-security expectations)

PIP does not publish a numbered IT requirement set; the control references (CYB-n) below are the organization's own, mapping its IT and cybersecurity controls to the cybersecurity expectations within the PIP corporate security area.

| Control ID | Control | Reference Document | Implementation Evidence | Status | Last Reviewed |
|---|---|---|---|---|---|
| CYB-1 | **Access Control and Authentication**: Implement documented procedures for granting, modifying, and revoking access to IT systems used in trade and supply chain operations. Enforce principle of least privilege. Apply multi-factor authentication for remote access. | [`security/procedure-access-control.md`](../../security/procedure-access-control.md), [`security/procedure-identity-management.md`](../../security/procedure-identity-management.md) | Access provisioning records; access review logs; MFA configuration attestation | Implemented | |
| CYB-2 | **Password Management**: Enforce minimum password complexity, length, and rotation standards. Prohibit shared credentials. Implement account lockout policies. | [`security/procedure-identity-management.md`](../../security/procedure-identity-management.md), [`security/policy-information-security.md`](../../security/policy-information-security.md) | Password policy documentation; lockout configuration records | Implemented | |
| CYB-3 | **Data Integrity and Protection**: Implement controls to protect the integrity and confidentiality of electronic trade data including manifests, customs declarations, and cargo documentation. Encrypt sensitive trade data in transit. | [`security/framework-cryptographic-key-lifecycle.md`](../../security/framework-cryptographic-key-lifecycle.md), [`security/policy-information-security.md`](../../security/policy-information-security.md) | Encryption configuration records; data classification policy; integrity monitoring evidence | Implemented | |
| CYB-4 | **Network Security**: Deploy firewalls, intrusion detection systems, and network access controls. Restrict external access to trade systems. Monitor network traffic for anomalies. | [`dev-security/standard-devops-security-requirements.md`](../../dev-security/standard-devops-security-requirements.md), [`operations/register-it-security-operations.md`](../../operations/register-it-security-operations.md) | Firewall configuration review; IDS/IPS deployment evidence; network access control records | Implemented | |
| CYB-5 | **Vulnerability and Patch Management**: Conduct periodic vulnerability assessments of systems used in supply chain operations. Apply security patches in a timely manner aligned with risk severity. | [`dev-security/standard-developer-security-requirements.md`](../../dev-security/standard-developer-security-requirements.md), [`operations/register-it-security-operations.md`](../../operations/register-it-security-operations.md) | Vulnerability scan reports; patch management records; remediation tracking log | Implemented | |
| CYB-6 | **Incident Reporting and Response**: Maintain documented cyber incident response procedures. Report security incidents that affect supply chain integrity or border data to CBSA in accordance with the PIP partnership agreement. | [`resilience/procedure-cross-domain-incident-coordination.md`](../../resilience/procedure-cross-domain-incident-coordination.md), [`security/sop-incident-escalation-matrix.md`](../../security/sop-incident-escalation-matrix.md) | Incident response plan; CBSA notification runbook; incident log | Implemented | |
| CYB-7 | **Security Awareness Training**: Provide security awareness training to personnel with access to trade and logistics systems. Training must cover cyber threats relevant to supply chain operations. | [`governance/framework-human-capital-and-ethical-conduct.md`](../../governance/framework-human-capital-and-ethical-conduct.md) | Training completion records; annual awareness attestations | Implemented | |
| CYB-8 | **Hardware and Software Asset Management**: Maintain an inventory of hardware and software assets used in customs and trade operations. Implement secure disposal procedures for storage media. | [`operations/register-asset-inventory.md`](../../operations/register-asset-inventory.md) | Asset inventory register; media disposal records | Implemented | |
| CYB-9 | **Third-Party and Service Provider Controls**: Assess IT security risks posed by third-party suppliers and service providers with access to trade systems. Include appropriate IT security obligations in contracts. | [`risk/standard-third-party-and-supply-chain-risk.md`](../../risk/standard-third-party-and-supply-chain-risk.md), [`supply-chain/procedure-supplier-due-diligence.md`](../../supply-chain/procedure-supplier-due-diligence.md) | Vendor risk assessment records; contract security clauses; third-party access logs | Implemented | |
| CYB-10 | **Business Continuity**: Maintain procedures for restoring critical trade and customs IT systems following an incident or outage. Test continuity capability periodically. | [`resilience/plan-it-disaster-recovery.md`](../../resilience/plan-it-disaster-recovery.md), [`resilience/procedure-continuity-and-recovery-testing.md`](../../resilience/procedure-continuity-and-recovery-testing.md) | Recovery test reports; RTO records; backup validation logs | Implemented | |

---

## PIP-AEO-s alignment

Canada's PIP and the UK's AEO-S both derive from the WCO SAFE Framework, resulting in significant overlap in security requirements. Organizations certified under AEO-S can reference this certification when applying for PIP or demonstrating equivalent security standards to CBSA.

| PIP Requirement | UK AEO-S Equivalent | Evidence Sharing |
|---|---|---|
| CYB-1 Access Control | AEO-S: Appropriate access controls for trade systems | Yes |
| CYB-2 Password Management | AEO-S: Password and authentication management | Yes |
| CYB-3 Data Integrity | AEO-S: IT data integrity and confidentiality requirements | Yes |
| CYB-4 Network Security | AEO-S: Network and infrastructure security | Yes |
| CYB-5 Vulnerability Management | AEO-S: Regular security reviews | Yes |
| CYB-6 Incident Response | AEO-S: Incident reporting to HMRC: CBSA supplement needed | Partial |
| CYB-7 Training | AEO-S: Security awareness training | Yes |
| CYB-8 Asset Management | AEO-S: IT asset inventory | Yes |
| CYB-9 Third-Party Controls | AEO-S: Third-party IT security provisions | Yes |
| CYB-10 Business Continuity | AEO-S: IT continuity provisions | Yes |

See [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](annex-aeo-united-kingdom-cybersecurity.md) for AEO-S controls and HMRC submission guidance.

---

## PIP-CTPAT cross-reference

The CBSA and US Customs and Border Protection operate trusted-trader programmes (PIP and CTPAT) that participate in mutual recognition. Organizations should confirm the current scope of the CBSA-CBP arrangement against the CBSA's published mutual recognition arrangements before reusing evidence. Where an arrangement applies, evidence collected for CTPAT IT criteria may support the corresponding PIP cybersecurity expectations, subject to jurisdiction-specific supplements. See [`compliance/logistics/register-ctpat-united-states-it-controls.md`](register-ctpat-united-states-it-controls.md) for the CTPAT mapping.

| PIP Requirement | CTPAT Equivalent | Shared Evidence |
|---|---|---|
| CYB-1 to CYB-10 | CTPAT IT-1 to IT-10 (broadly equivalent) | Yes: with jurisdiction-specific supplements for CBSA notification obligations |

---

## Programme-wide alignment

For a consolidated view across CTPAT, PIP, BASC, AEO, AEO-S, NEEC, and OEA, see [`supply-chain/matrix-supply-chain-security-programme-alignment.md`](../../supply-chain/matrix-supply-chain-security-programme-alignment.md).

---

## Review and maintenance

| Activity | Frequency | Responsibility |
|---|---|---|
| Control status update | Quarterly | Trade Compliance Manager |
| Evidence refresh for annual CBSA profile update | Annually | Chief Compliance Officer |
| Full register review after CBSA criteria revision | Within 60 days of CBSA publication | Chief Compliance Officer |
| Readiness check prior to CBSA validation visit | On notice of scheduled visit | Trade Compliance Manager |

---

**End of Document**
