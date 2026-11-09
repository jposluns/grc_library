# Canada PIP IT and Cybersecurity Compliance Controls Register

**Document Title:** Canada PIP IT and Cybersecurity Compliance Controls Register\
**Document Type:** Register\
**Version:** 1.0.8\
**Date:** 2026-11-07\
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
**UK parallel programme:** Authorized Economic Operator Security and Safety (AEO-S), administered by HMRC\
**US parallel programme:** Customs-Trade Partnership Against Terrorism (CTPAT), administered by CBP\
**Mutual recognition:** The CBSA maintains Authorized Economic Operator mutual recognition arrangements with partner customs administrations; the held reference material documents the Canada-Mexico AEO mutual recognition arrangement, signed in Cancun, Mexico, on 11 May 2016. Organizations holding a partner-programme certification (for example CTPAT, or an AEO or AEO-S scheme) should confirm the current scope of any applicable arrangement against the CBSA's published mutual recognition arrangements before relying on it for evidence reuse. That UK AEO-S certification is comparable to PIP is not confirmed by a held source; the WCO AEO Compendium (2020) lists both programmes (the UK's then reported as the European Union programme) among operational AEO programmes, and a Canada-UK mutual recognition arrangement is not recorded in it.

---

## Programme overview

PIP is a voluntary partnership programme in which businesses commit to enhancing border security in exchange for expedited cargo processing at Canadian ports of entry. The programme is administered by CBSA; the WCO AEO Compendium (2020) lists Partners in Protection (PIP) among the operational AEO programmes of its Part I, which it describes as AEO programmes based on the WCO SAFE Framework of Standards. The PIP security profile is organized into four security areas: corporate security, cargo and conveyance security, physical security, and supply chain partner security. Cybersecurity is addressed within the corporate security area; PIP does not publish a separate, numbered information-technology requirement set. The control references below are the organization's own, mapped to those PIP cybersecurity expectations.

PIP membership process: an applicant completes the security-profile questionnaire in the CBSA Trusted Trader Portal and submits supporting evidence (documents and photographs). Members review and update their security profile in the Trusted Trader Portal at least annually. The CBSA does not publish a tiered-membership ladder for PIP.

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

## PIP-AEO-S alignment

The WCO AEO Compendium (2020) lists PIP and the UK programme (then reported as the European Union programme) among AEO programmes based on the WCO SAFE Framework of Standards. Overlap between their security requirements is not confirmed by a held source, so the table below is the organization's own candidate mapping, each row subject to CBSA acceptance requirement by requirement. A Canada-UK mutual recognition arrangement is not recorded in the Compendium: evidence gathered for AEO-S may be offered in a PIP application, but an AEO-S certification is not a formal shortcut to CBSA acceptance.

| Control (org) | UK AEO-S Equivalent | Evidence Sharing |
|---|---|---|
| CYB-1 Access Control | AEO-S: Appropriate access controls for trade systems | Candidate overlap, subject to CBSA acceptance |
| CYB-2 Password Management | AEO-S: Password and authentication management | Candidate overlap, subject to CBSA acceptance |
| CYB-3 Data Integrity | AEO-S: IT data integrity and confidentiality requirements | Candidate overlap, subject to CBSA acceptance |
| CYB-4 Network Security | AEO-S: Network and infrastructure security | Candidate overlap, subject to CBSA acceptance |
| CYB-5 Vulnerability Management | AEO-S: Regular security reviews | Candidate overlap, subject to CBSA acceptance |
| CYB-6 Incident Response | AEO-S: security procedures reviewed and amended after an incident (handbook §11.4), how security incidents are reported and dealt with, with no recipient named (§11.8, building and boundary security) and, for cargo units, incident reporting and recording and the action to be taken, including reporting to law enforcement or senior management (§11.12, cargo security); notification to HMRC of all changes that may affect AEO status, including disclosure of security incidents, to the AEO Central Site as soon as the change is known or, at the latest, within 14 calendar days of the change, using form C122 (§12.4, notification of changes); CBSA supplement needed | Partial candidate overlap, subject to CBSA acceptance |
| CYB-7 Training | AEO-S: Security awareness training | Candidate overlap, subject to CBSA acceptance |
| CYB-8 Asset Management | AEO-S: IT asset inventory | Candidate overlap, subject to CBSA acceptance |
| CYB-9 Third-Party Controls | AEO-S: Third-party IT security provisions | Candidate overlap, subject to CBSA acceptance |
| CYB-10 Business Continuity | AEO-S: IT continuity provisions | Candidate overlap, subject to CBSA acceptance |

See [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](annex-aeo-united-kingdom-cybersecurity.md) for the organization's AEO-S IT controls and its self-assessment.

---

## PIP-CTPAT cross-reference

The CBSA and US Customs and Border Protection operate trusted-trader programmes (PIP and CTPAT) that participate in mutual recognition (the WCO AEO Compendium (2020) records a concluded Canada-US MRA, June 2008). Organizations should confirm the current scope of the CBSA-CBP arrangement against the CBSA's published mutual recognition arrangements before reusing evidence. Where an arrangement applies, evidence collected for CTPAT IT criteria may support the corresponding PIP cybersecurity expectations, subject to jurisdiction-specific supplements. See [`compliance/logistics/register-ctpat-united-states-it-controls.md`](register-ctpat-united-states-it-controls.md) for the CTPAT mapping.

| Control (org) | CTPAT Equivalent | Shared Evidence |
|---|---|---|
| CYB-1 to CYB-10 | CTPAT IT-1 to IT-10 (the organization's candidate counterparts) | Candidate overlap, subject to CBSA acceptance: with jurisdiction-specific supplements for CBSA notification obligations |

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
