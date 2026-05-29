# GRC Library Compliance Alignment Matrix

**Document Title:** GRC Library Compliance Alignment Matrix\
**Document Type:** Matrix\
**Version:** 1.0.0\
**Date:** 2026-05-27\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/policy-compliance-and-audit-management.md`](policy-compliance-and-audit-management.md), [`compliance/register-global-regulatory-applicability.md`](register-global-regulatory-applicability.md), [`compliance/logistics/register-basc-it-responsibilities.md`](../compliance/logistics/register-basc-it-responsibilities.md), [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](logistics/annex-aeo-united-kingdom-cybersecurity.md), [`governance/charter-governance-library.md`](../governance/charter-governance-library.md), [`governance/matrix-cross-framework-alignment.md`](../governance/matrix-cross-framework-alignment.md)\
**Classification:** Public\
**Category:** Compliance Management\
**Review Frequency:** Annual and upon material regulatory or framework change\
**Repository Path:** [`compliance/matrix-grc-compliance-alignment.md`](matrix-grc-compliance-alignment.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

---

## How to use this matrix

This matrix maps GRC library documents to the control domains and section references of eight compliance and security frameworks. Each row represents one GRC library document. Each framework column lists the control identifiers, domains, or section references that the document materially supports.

**Framework column keys:**

| Column | Framework | Reference Basis |
| --- | --- | --- |
| CSA CCM v4.1 | Cloud Security Alliance Cloud Controls Matrix v4 | Control domain identifiers (e.g., IAM, SEF, DSP) |
| ISO 27001:2022 | ISO/IEC 27001:2022 Annex A | Annex A control numbers and §6 to §10 clauses |
| NIST CSF 2.0 | NIST Cybersecurity Framework 2.0 | Core Functions (GV, ID, PR, DE, RS, RC) |
| CTPAT | C-TPAT Minimum Security Criteria | Section headings |
| PIP | Partners in Protection (Canada Border Services Agency) | Programme requirement areas |
| BASC v6 | BASC International Standard v6 | Chapter references |
| WCO SAFE | WCO SAFE Framework of Standards | Pillar and standard references |
| AEO/AEO-S | UK HMRC Authorized Economic Operator (Security and Safety) | Requirement area headings |

Read across a row to identify which frameworks a given document supports. Read down a column to identify which GRC library documents collectively satisfy a framework's requirements. A cell containing ": " indicates no direct mapping; the document may still provide contextual support.

---

## Notes

This matrix is indicative only. It reflects the best available assessment of control mappings at the time of publication based on the content of each GRC library document and publicly available framework documentation. Specific control mapping for a formal certification assessment, audit submission, or regulatory response requires an engagement-specific review by qualified practitioners with access to the full framework specifications and the organisation's operational evidence. No entry in this matrix constitutes a certification, attestation, or legal opinion.

---

## Governance domain

| Domain | Document Title | Path | CSA CCM v4.1 | ISO 27001:2022 | NIST CSF 2.0 | CTPAT | PIP | BASC v6 | WCO SAFE | AEO/AEO-S |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Governance | Governance Library Charter | [`governance/charter-governance-library.md`](../governance/charter-governance-library.md) | GRC-01, GRC-02 | §5.1, §5.2, §6.1 | GV.OC, GV.RM | N/A | Programme governance | §5.1, §7.5 | Pillar I (Customs-Business Partnership) | Management commitment |
| Governance | Policy: Governance and Risk Management | [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md) | GRC-01, GRC-02, GRC-03 | §5.2, §6.1, §6.2 | GV.RM, GV.OC | N/A | Programme governance | §5.1, §6.1 | N/A | Management commitment |
| Governance | Policy: Exception and Risk Acceptance Management | [`governance/policy-exception-and-risk-acceptance-management.md`](../governance/policy-exception-and-risk-acceptance-management.md) | GRC-04, GRC-05 | §6.1.3, §8.2 | GV.RM, ID.RA | N/A |: | §6.1, §10 | N/A | Risk management |
| Governance | Standard: Records Retention and Destruction | [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md) | DSP-07, DSP-08 | A.5.33, A.8.10 | PR.DS, PR.IP | Documentation and record-keeping | Record retention | §7.5 | Pillar II (Customs-to-Customs) | Documentation security; Trade records retention |
| Supply Chain | Standard: Supplier Security and Privacy Assurance | [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md) | STA-01, STA-02, STA-03 | A.5.19, A.5.20, A.5.21, A.5.22 | GV.SC, ID.SC | Business partner requirements | Third-party security | §8.6 | Pillar I (Standard 6) | Business partners |
| Governance | Register: Document Index and Classification | [`governance/register-document-index-and-classification.md`](../governance/register-document-index-and-classification.md) | GRC-01 | §7.5 | GV.OC | N/A |: | §7.5 | N/A | Documentation security |

---

## Risk domain

| Domain | Document Title | Path | CSA CCM v4.1 | ISO 27001:2022 | NIST CSF 2.0 | CTPAT | PIP | BASC v6 | WCO SAFE | AEO/AEO-S |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Risk | Policy: Enterprise Governance and Risk Management | [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md) | GRC-01, GRC-02, GRC-03 | §5.3, §6.1, §6.2 | GV.RM, ID.RA | N/A | Programme governance | §5.1, §6.1 | N/A | Management commitment; Risk management |
| Risk | Standard: Enterprise Risk Management | [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md) | GRC-03, GRC-04, GRC-05 | §6.1.2, §6.1.3 | ID.RA, GV.RM | N/A | Risk assessment | §6.1 | N/A | IT security risk management |
| Risk | Procedure: Risk Register | [`risk/procedure-risk-register.md`](../risk/procedure-risk-register.md) | GRC-04, GRC-05 | §6.1.2, §6.1.3, §9.1 | ID.RA, GV.RM | N/A | Risk assessment | §6.1, §9.1 | N/A | IT security risk management |

---

## Compliance domain

| Domain | Document Title | Path | CSA CCM v4.1 | ISO 27001:2022 | NIST CSF 2.0 | CTPAT | PIP | BASC v6 | WCO SAFE | AEO/AEO-S |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Compliance | Policy: Compliance, Audit, and CAPA Management | [`compliance/policy-compliance-and-audit-management.md`](policy-compliance-and-audit-management.md) | GRC-06, GRC-07, GRC-08 | §9.2, §9.3, §10.1, §10.2 | GV.OC, ID.IM | N/A | Programme governance | §9.2, §10 | N/A | IT controls review and testing |
| Compliance | Register: Global Regulatory Applicability | [`compliance/register-global-regulatory-applicability.md`](register-global-regulatory-applicability.md) | GRC-01, GRC-06 | §4.1, §4.2, §6.1 | GV.OC, GV.RM | N/A | Programme governance | §4.1, §6.1 | N/A | Management commitment |
| Compliance | Register: BASC IT and Information Security Responsibilities | [`compliance/logistics/register-basc-it-responsibilities.md`](../compliance/logistics/register-basc-it-responsibilities.md) | GRC-01, GRC-02 | §5.3, §6.1, §9.1 | GV.OC, GV.RM | N/A |: | §5.1, §6.1, §7.2, §7.5, §8.1, §8.3, §8.4, §8.5, §9.1, §9.2, §10 | Pillar I (Standard 6) | All AEO-S IT requirement areas |
| Compliance | Register: BASC IT Compliance Monitoring and KPIs | [`compliance/logistics/register-basc-it-compliance-kpis.md`](../compliance/logistics/register-basc-it-compliance-kpis.md) | GRC-04, GRC-08 | §9.1 | GV.OC, ID.IM | N/A |: | §9.1 | N/A | IT controls review and testing |
| Compliance | Annex: AEO-S IT and Cybersecurity Requirements | [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](logistics/annex-aeo-united-kingdom-cybersecurity.md) | IAM-01, SEF-01, DSP-01 | §5.3, §8.1, §9.1 | GV.OC, PR.AA, DE.CM | IT security requirements | IT security | §8.4, §8.5 | Pillar II (ICT security) | Access to IT systems; Information systems security; IT security incidents; Trade records retention |

---

## Security domain

| Domain | Document Title | Path | CSA CCM v4.1 | ISO 27001:2022 | NIST CSF 2.0 | CTPAT | PIP | BASC v6 | WCO SAFE | AEO/AEO-S |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Security | Policy: Information Security | [`security/policy-information-security.md`](../security/policy-information-security.md) | GRC-01, IAM-01, SEF-01 | §5.2, A.5.1, A.5.2 | GV.OC, GV.PO | IT security policy | IT security | §8.4 | Pillar II (ICT security) | Information systems security |
| Security | Policy: Identity and Access Management | [`security/policy-identity-and-access-management.md`](../security/policy-identity-and-access-management.md) | IAM-01, IAM-02, IAM-03, IAM-04 | A.5.15, A.5.16, A.5.17, A.5.18 | PR.AA, PR.IR | IT access controls | Access controls | §8.5 | Pillar II (Standard 6, access) | Access to IT systems |
| Security | Policy: Acceptable Use | [`security/policy-acceptable-use.md`](../security/policy-acceptable-use.md) | HRS-01, HRS-02 | A.5.10, A.6.2, A.8.1 | GV.PO, PR.AT | N/A | Employee security | §7.2 | N/A | Personnel security |
| Security | Policy: Encryption and Key Management | [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md) | CEK-01, CEK-02, CEK-03, CEK-04 | A.8.24 | PR.DS | IT security controls | Data protection | §8.4 | Pillar II (ICT security) | Information systems security |
| Security | Standard: Logging and Monitoring | [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md) | LOG-01, LOG-02, LOG-03, LOG-04 | A.8.15, A.8.16, A.8.17 | DE.CM, DE.AE | IT security monitoring | IT security | §9.1 | Pillar II (ICT security) | IT security incidents; Trade records retention |
| Security | Standard: Data Classification and Handling | [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md) | DSP-01, DSP-02, DSP-03 | A.5.12, A.5.13, A.8.10 | PR.DS, PR.IP | N/A | Data protection | §7.5, §8.4 | Pillar II (ICT security) | Documentation security |
| Security | Standard: Privileged Access Management | [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md) | IAM-05, IAM-06, IAM-07 | A.5.18, A.8.2 | PR.AA, PR.IR | IT access controls | Access controls | §8.5 | Pillar II (Standard 6, access) | Access to IT systems |
| Security | Standard: Authentication and Password Management | [`security/standard-authentication-and-password-management.md`](../security/standard-authentication-and-password-management.md) | IAM-02, IAM-03, IAM-08 | A.5.17, A.8.5 | PR.AA | IT access controls | Access controls | §8.3, §8.5 | Pillar II (Standard 6, access) | Access to IT systems; Personnel security screening |
| Security | Procedure: Incident Response | [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) | SEF-01, SEF-02, SEF-03, SEF-04, SEF-05 | A.5.24, A.5.25, A.5.26, A.5.27, A.5.28 | RS.MA, RS.AN, RS.CO, RS.MI, RC.RP | IT security incidents | Incident response | §8.4, §10 | Pillar II (ICT security) | IT security incident detection and response |
| Security | Procedure: Vulnerability Management | [`security/procedure-vulnerability-management.md`](../security/procedure-vulnerability-management.md) | TVM-01, TVM-02, TVM-03 | A.8.8 | ID.RA, PR.IP, DE.CM | IT security controls | IT security | §8.4, §9.1 | Pillar II (ICT security) | IT security controls review and testing |

---

## Operations domain

| Domain | Document Title | Path | CSA CCM v4.1 | ISO 27001:2022 | NIST CSF 2.0 | CTPAT | PIP | BASC v6 | WCO SAFE | AEO/AEO-S |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Operations | Standard: Production Security Requirements | [`operations/standard-production-security-requirements.md`](../operations/standard-production-security-requirements.md) | CCC-01, CCC-02, TVM-01 | A.8.8, A.8.9, A.8.31 | PR.IP, DE.CM | IT security controls | IT security | §8.1, §8.4 | Pillar II (ICT security) | IT systems protection |
| Operations | Standard: Network Security and Segmentation | [`operations/standard-network-security-and-segmentation.md`](../operations/standard-network-security-and-segmentation.md) | NET-01, NET-02, NET-03, NET-04, NET-05, NET-06 | A.8.20, A.8.21, A.8.22 | PR.IR, DE.CM | IT security controls | Network security | §8.4 | Pillar II (ICT security) | IT systems protection |
| Operations | Standard: Cloud Security Configuration Baseline | [`operations/standard-cloud-security-configuration-baseline.md`](../operations/standard-cloud-security-configuration-baseline.md) | CCC-01, CCC-02, CEK-01, IAM-01 | A.8.9, A.8.23, A.8.24 | PR.IP, PR.IR | IT security controls | IT security | §8.4 | Pillar II (ICT security) | Information systems security |
| Operations | Standard: Physical Security of IT Infrastructure | [`operations/standard-physical-security-of-it-infrastructure.md`](../operations/standard-physical-security-of-it-infrastructure.md) | DCS-01, DCS-02, DCS-03, DCS-04, DCS-05 | A.7.1, A.7.2, A.7.3, A.7.4, A.7.5, A.7.6, A.7.7, A.7.8 | PR.IR | Physical access controls | Physical security | §8.4 | Pillar I (Standard 3, physical security) | Physical and access security |
| Operations | Standard: Certificate Authority Management | [`operations/standard-certificate-authority-management.md`](../operations/standard-certificate-authority-management.md) | CEK-03, CEK-04, IAM-08 | A.8.24 | PR.DS | IT security controls | IT security | §8.4 | Pillar II (ICT security) | Information systems security |
| Operations | Procedure: Change Management and Configuration Control | [`operations/procedure-change-management-and-configuration-control.md`](../operations/procedure-change-management-and-configuration-control.md) | CCC-01, CCC-02, CCC-03, CCC-04, CCC-05 | A.8.9, A.8.32 | PR.IP, ID.IM | IT security controls | IT security | §8.1 | Pillar II (ICT security) | IT systems protection |
| Operations | Procedure: Endpoint Management and Device Compliance | [`operations/procedure-endpoint-management-and-device-compliance.md`](../operations/procedure-endpoint-management-and-device-compliance.md) | UEM-01, UEM-02, UEM-03 | A.8.1, A.8.7 | PR.IR, DE.CM | IT security controls | IT security | §8.4 | Pillar II (ICT security) | IT security incident detection and response |
| Operations | Procedure: Media Handling and Transport | [`operations/procedure-media-handling-and-transport.md`](../operations/procedure-media-handling-and-transport.md) | DSP-04, DSP-05 | A.7.10, A.8.10 | PR.DS | N/A | Data protection | §7.5, §8.4 | N/A | Documentation security |
| Operations | Procedure: Security Monitoring and Alert Management | [`operations/procedure-security-monitoring-and-alert-management.md`](../operations/procedure-security-monitoring-and-alert-management.md) | LOG-02, LOG-03, SEF-01 | A.8.15, A.8.16 | DE.CM, DE.AE, RS.MA | IT security monitoring | IT security | §9.1 | Pillar II (ICT security) | IT security incident detection and response |
| Operations | Procedure: Threat Intelligence and SIEM Operations | [`operations/procedure-threat-intelligence-and-siem-operations.md`](../operations/procedure-threat-intelligence-and-siem-operations.md) | TVM-02, LOG-03, SEF-01 | A.5.7, A.8.16 | DE.CM, DE.AE, ID.RA | IT security monitoring | IT security | §8.4, §9.1 | Pillar II (ICT security) | IT security incident detection and response |

---

## Supply chain domain

| Domain | Document Title | Path | CSA CCM v4.1 | ISO 27001:2022 | NIST CSF 2.0 | CTPAT | PIP | BASC v6 | WCO SAFE | AEO/AEO-S |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Supply Chain | Framework: Supplier and Cloud Governance | [`supply-chain/framework-supplier-and-cloud-governance.md`](../supply-chain/framework-supplier-and-cloud-governance.md) | STA-01, STA-02, STA-03, STA-04, STA-05 | A.5.19, A.5.20, A.5.21, A.5.22, A.5.23 | GV.SC, ID.SC | Business partner requirements; Cargo security | Third-party and supply chain security | §8.6 | Pillar I (Standard 6, business partners); Pillar I (Standard 5, supply chain) | Business partners |
| Supply Chain | Standard: Third-Party Risk | [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md) | STA-01, STA-03, STA-04 | A.5.19, A.5.21, A.5.22 | GV.SC, ID.SC | Business partner requirements | Third-party security | §8.6 | Pillar I (Standard 6) | Business partners |
| Supply Chain | Procedure: Supplier Due Diligence | [`supply-chain/procedure-supplier-due-diligence.md`](../supply-chain/procedure-supplier-due-diligence.md) | STA-02, STA-04 | A.5.19, A.5.20 | GV.SC, ID.SC | Business partner vetting | Third-party vetting | §8.6 | Pillar I (Standard 6) | Business partners |
| Supply Chain | Procedure: Supplier Audit | [`supply-chain/procedure-supplier-audit.md`](../supply-chain/procedure-supplier-audit.md) | STA-04, STA-05, GRC-07 | A.5.20, A.5.22, §9.2 | GV.SC, ID.SC | Business partner requirements | Third-party audit | §8.6, §9.2 | Pillar I (Standard 6) | Business partners; IT controls review and testing |

---

## Resilience domain

| Domain | Document Title | Path | CSA CCM v4.1 | ISO 27001:2022 | NIST CSF 2.0 | CTPAT | PIP | BASC v6 | WCO SAFE | AEO/AEO-S |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Resilience | Policy: Business Continuity and Disaster Recovery | [`resilience/policy-business-continuity-and-disaster-recovery.md`](../resilience/policy-business-continuity-and-disaster-recovery.md) | BCR-01, BCR-02 | A.5.29, A.5.30 | RC.RP, RC.CO | N/A | Business continuity | §8.1 | N/A | IT systems backup and continuity |
| Resilience | Standard: Business Continuity and Disaster Recovery | [`resilience/standard-business-continuity-and-disaster-recovery.md`](../resilience/standard-business-continuity-and-disaster-recovery.md) | BCR-01, BCR-02, BCR-03, BCR-04, BCR-05 | A.5.29, A.5.30, A.8.14 | RC.RP, RC.CO, ID.BE | N/A | Business continuity | §8.1 | N/A | IT systems backup and continuity |
| Resilience | Procedure: Backup and Recovery | [`resilience/procedure-backup-and-recovery.md`](../resilience/procedure-backup-and-recovery.md) | BCR-06, BCR-07, BCR-08, BCR-09, BCR-10, BCR-11 | A.8.13 | RC.RP | N/A | Business continuity | §8.1 | N/A | IT systems backup and continuity |

---

## Privacy domain

| Domain | Document Title | Path | CSA CCM v4.1 | ISO 27001:2022 | NIST CSF 2.0 | CTPAT | PIP | BASC v6 | WCO SAFE | AEO/AEO-S |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Privacy | Policy: Privacy and Data Governance | [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md) | DSP-01, DSP-02, DSP-03, DSP-04 | A.5.34, A.8.11, A.8.12 | GV.PO, PR.DS | N/A | Data protection | §8.4 | N/A | Documentation security |
| Privacy | Procedure: Privacy Impact and Cross-Border Transfer | [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../privacy/procedure-privacy-impact-and-cross-border-transfer.md) | DSP-03, DSP-04, DSP-06 | A.5.34 | GV.PO, PR.DS, ID.RA | N/A | Data protection | §8.4 | N/A | Documentation security |

---

## Framework coverage summary

The following table summarizes how many GRC library documents provide primary coverage per framework, to assist in identifying gaps.

| Framework | Primary Documents in This Matrix | Notes |
| --- | --- | --- |
| CSA CCM v4.1 | All 42 documents | Coverage across IAM, DSP, LOG, NET, CEK, TVM, SEF, BCR, GRC, STA, DCS, UEM, HRS, CCC families |
| ISO/IEC 27001:2022 | All 42 documents | Coverage across Annex A clauses and management system clauses §4 to §10 |
| NIST CSF 2.0 | All 42 documents | Coverage across GV, ID, PR, DE, RS, RC functions |
| CTPAT | 18 documents | Primary coverage in security, operations, supply chain, and resilience domains |
| PIP (Canada) | 24 documents | Coverage across programme requirements for IT security, access, data protection, continuity |
| BASC v6 | 38 documents | Strong coverage; operational cargo security domains out of IT scope |
| WCO SAFE | 22 documents | Coverage in Pillar I (customs-business partnership) and Pillar II (customs-to-customs) |
| AEO/AEO-S | 20 documents | Coverage of information systems security requirement area; physical and personnel security supported by operations and governance documents |



**End of Document**
