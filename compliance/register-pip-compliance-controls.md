# PIP IT and Cybersecurity Compliance Controls Register

**Document Title:** PIP IT and Cybersecurity Compliance Controls Register 
**Document Type:** Register 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Compliance Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`compliance/README.md`](README.md), [`compliance/policy-compliance-and-audit-management.md`](policy-compliance-and-audit-management.md), [`compliance/policy-legal-and-regulatory-compliance.md`](policy-legal-and-regulatory-compliance.md), [`compliance/annex-aeo-s-it-cybersecurity-requirements.md`](annex-aeo-s-it-cybersecurity-requirements.md), [`sectors/basc/register-basc-it-responsibilities.md`](../sectors/basc/register-basc-it-responsibilities.md), [`compliance/register-ctpat-it-controls.md`](register-ctpat-it-controls.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../supply-chain/framework-supplier-and-cloud-governance.md), [`supply-chain/matrix-supply-chain-security-programme-alignment.md`](../supply-chain/matrix-supply-chain-security-programme-alignment.md) 
**Classification:** Public 
**Category:** Trade Compliance: IT and Cybersecurity Controls 
**Review Frequency:** Annual and upon material CBSA criteria update, audit finding, or certification renewal 
**Repository Path:** [`compliance/register-pip-compliance-controls.md`](register-pip-compliance-controls.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This register documents the organization's implementation status against the IT and cybersecurity-related security requirements of Canada's Partners in Protection (PIP) programme administered by the Canada Border Services Agency (CBSA). It supports PIP membership compliance, annual partnership profile updates, and pre-certification readiness assessments.

**Programme authority:** Canada Border Services Agency (CBSA) 
**UK parallel programme:** Authorized Economic Operator to Security and Safety (AEO-S), administered by HMRC 
**US parallel programme:** Customs-Trade Partnership Against Terrorism (CTPAT), administered by CBP 
**Mutual recognition:** PIP maintains mutual recognition arrangements with CTPAT (US) and the EU AEO programme. The UK AEO-S programme, as the successor to the EU AEO scheme for UK operators, provides functionally equivalent security and safety certification. Organizations holding AEO-S or CTPAT certification can reference those programmes when demonstrating equivalent security standards to CBSA.

---

## Programme overview

PIP is a voluntary partnership programme in which businesses commit to enhancing border security in exchange for expedited cargo processing at Canadian ports of entry. The programme is administered by CBSA and aligns with the World Customs Organization (WCO) SAFE Framework of Standards. IT and cybersecurity requirements are embedded in the Information Technology security section of the PIP security profile.

PIP membership tiers:
- **Approved:** Partnership agreement signed; security profile accepted by CBSA
- **Validated:** CBSA officer has conducted on-site validation assessment
- **Gold Member:** Validated member consistently meeting enhanced criteria

---

## IT and cybersecurity security requirements

| Requirement ID | PIP Requirement | Control Reference | Implementation Evidence | Status | Last Reviewed |
|---|---|---|---|---|---|
| PIP-IT-1 | **Access Control and Authentication**: Implement documented procedures for granting, modifying, and revoking access to IT systems used in trade and supply chain operations. Enforce principle of least privilege. Apply multi-factor authentication for remote access. | [`security/procedure-access-control.md`](../security/procedure-access-control.md), [`security/procedure-identity-management.md`](../security/procedure-identity-management.md) | Access provisioning records; access review logs; MFA configuration attestation | Implemented | |
| PIP-IT-2 | **Password Management**: Enforce minimum password complexity, length, and rotation standards. Prohibit shared credentials. Implement account lockout policies. | [`security/procedure-identity-management.md`](../security/procedure-identity-management.md), [`security/policy-information-security.md`](../security/policy-information-security.md) | Password policy documentation; lockout configuration records | Implemented | |
| PIP-IT-3 | **Data Integrity and Protection**: Implement controls to protect the integrity and confidentiality of electronic trade data including manifests, customs declarations, and cargo documentation. Encrypt sensitive trade data in transit. | [`security/framework-cryptographic-key-lifecycle.md`](../security/framework-cryptographic-key-lifecycle.md), [`security/policy-information-security.md`](../security/policy-information-security.md) | Encryption configuration records; data classification policy; integrity monitoring evidence | Implemented | |
| PIP-IT-4 | **Network Security**: Deploy firewalls, intrusion detection systems, and network access controls. Restrict external access to trade systems. Monitor network traffic for anomalies. | [`dev-security/standard-devops-security-requirements.md`](../dev-security/standard-devops-security-requirements.md), [`operations/register-it-security-operations.md`](../operations/register-it-security-operations.md) | Firewall configuration review; IDS/IPS deployment evidence; network access control records | Implemented | |
| PIP-IT-5 | **Vulnerability and Patch Management**: Conduct periodic vulnerability assessments of systems used in supply chain operations. Apply security patches in a timely manner aligned with risk severity. | [`dev-security/standard-developer-security-requirements.md`](../dev-security/standard-developer-security-requirements.md), [`operations/register-it-security-operations.md`](../operations/register-it-security-operations.md) | Vulnerability scan reports; patch management records; remediation tracking log | Implemented | |
| PIP-IT-6 | **Incident Reporting and Response**: Maintain documented cyber incident response procedures. Report security incidents that affect supply chain integrity or border data to CBSA in accordance with the PIP partnership agreement. | [`resilience/procedure-cross-domain-incident-coordination.md`](../resilience/procedure-cross-domain-incident-coordination.md), [`security/sop-incident-escalation-matrix.md`](../security/sop-incident-escalation-matrix.md) | Incident response plan; CBSA notification runbook; incident log | Implemented | |
| PIP-IT-7 | **Security Awareness Training**: Provide security awareness training to personnel with access to trade and logistics systems. Training must cover cyber threats relevant to supply chain operations. | [`governance/framework-human-capital-and-ethical-conduct.md`](../governance/framework-human-capital-and-ethical-conduct.md) | Training completion records; annual awareness attestations | Implemented | |
| PIP-IT-8 | **Hardware and Software Asset Management**: Maintain an inventory of hardware and software assets used in customs and trade operations. Implement secure disposal procedures for storage media. | [`operations/register-asset-inventory.md`](../operations/register-asset-inventory.md) | Asset inventory register; media disposal records | Implemented | |
| PIP-IT-9 | **Third-Party and Service Provider Controls**: Assess IT security risks posed by third-party suppliers and service providers with access to trade systems. Include appropriate IT security obligations in contracts. | [`supply-chain/standard-third-party-risk.md`](../supply-chain/standard-third-party-risk.md), [`supply-chain/procedure-supplier-due-diligence.md`](../supply-chain/procedure-supplier-due-diligence.md) | Vendor risk assessment records; contract security clauses; third-party access logs | Implemented | |
| PIP-IT-10 | **Business Continuity**: Maintain procedures for restoring critical trade and customs IT systems following an incident or outage. Test continuity capability periodically. | [`resilience/plan-it-disaster-recovery.md`](../resilience/plan-it-disaster-recovery.md), [`resilience/procedure-continuity-and-recovery-testing.md`](../resilience/procedure-continuity-and-recovery-testing.md) | Recovery test reports; RTO records; backup validation logs | Implemented | |

---

## PIP-AEO-s alignment

Canada's PIP and the UK's AEO-S both derive from the WCO SAFE Framework, resulting in significant overlap in security requirements. Organizations certified under AEO-S can reference this certification when applying for PIP or demonstrating equivalent security standards to CBSA.

| PIP Requirement | UK AEO-S Equivalent | Evidence Sharing |
|---|---|---|
| PIP-IT-1 Access Control | AEO-S: Appropriate access controls for trade systems | Yes |
| PIP-IT-2 Password Management | AEO-S: Password and authentication management | Yes |
| PIP-IT-3 Data Integrity | AEO-S: IT data integrity and confidentiality requirements | Yes |
| PIP-IT-4 Network Security | AEO-S: Network and infrastructure security | Yes |
| PIP-IT-5 Vulnerability Management | AEO-S: Regular security reviews | Yes |
| PIP-IT-6 Incident Response | AEO-S: Incident reporting to HMRC: CBSA supplement needed | Partial |
| PIP-IT-7 Training | AEO-S: Security awareness training | Yes |
| PIP-IT-8 Asset Management | AEO-S: IT asset inventory | Yes |
| PIP-IT-9 Third-Party Controls | AEO-S: Third-party IT security provisions | Yes |
| PIP-IT-10 Business Continuity | AEO-S: IT continuity provisions | Yes |

See [`compliance/annex-aeo-s-it-cybersecurity-requirements.md`](annex-aeo-s-it-cybersecurity-requirements.md) for AEO-S controls and HMRC submission guidance.

---

## PIP-CTPAT cross-reference

CTPAT (US) and PIP (Canada) maintain a mutual recognition arrangement. Evidence collected for CTPAT IT criteria may be reused for PIP with minimal supplementation. See [`compliance/register-ctpat-it-controls.md`](register-ctpat-it-controls.md) for the CTPAT mapping.

| PIP Requirement | CTPAT Equivalent | Shared Evidence |
|---|---|---|
| PIP-IT-1 to PIP-IT-10 | CTPAT IT-1 to IT-10 (broadly equivalent) | Yes: with jurisdiction-specific supplements for CBSA notification obligations |

---

## Programme-wide alignment

For a consolidated view across CTPAT, PIP, BASC, AEO, AEO-S, NEEC, and OEA, see [`supply-chain/matrix-supply-chain-security-programme-alignment.md`](../supply-chain/matrix-supply-chain-security-programme-alignment.md).

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
