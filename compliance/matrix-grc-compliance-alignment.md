# GRC Library Compliance Alignment Matrix

**Document Title:** GRC Library Compliance Alignment Matrix\
**Document Type:** Matrix\
**Version:** 1.6.0\
**Date:** 2026-06-26\
**Owner:** Chief Information Security Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/policy-compliance-and-audit-management.md`](policy-compliance-and-audit-management.md), [`compliance/register-global-regulatory-applicability.md`](register-global-regulatory-applicability.md), [`compliance/logistics/register-basc-it-responsibilities.md`](../compliance/logistics/register-basc-it-responsibilities.md), [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](logistics/annex-aeo-united-kingdom-cybersecurity.md), [`governance/charter-governance-library.md`](../governance/charter-governance-library.md), [`governance/matrix-cross-framework-alignment.md`](../governance/matrix-cross-framework-alignment.md)\
**Classification:** Public\
**Category:** Compliance Management\
**Review Frequency:** Annual and upon material regulatory or framework change\
**Repository Path:** [`compliance/matrix-grc-compliance-alignment.md`](matrix-grc-compliance-alignment.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

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

Read across a row to identify which frameworks a given document supports. Read down a column to identify which GRC library documents collectively satisfy a framework's requirements. A cell containing "N/A" indicates no direct mapping; the document may still provide contextual support. "N/A" is used in particular for the customs and trade-security columns (CTPAT, PIP, BASC, WCO SAFE, AEO/AEO-S) on documents whose subject is not customs or trade security.

---

## Notes

This matrix is indicative only. It reflects the best available assessment of control mappings at the time of publication based on the content of each GRC library document and publicly available framework documentation. Specific control mapping for a formal certification assessment, audit submission, or regulatory response requires an engagement-specific review by qualified practitioners with access to the full framework specifications and the organisation's operational evidence. No entry in this matrix constitutes a certification, attestation, or legal opinion.

---

## Governance domain

| Domain | Document Title | Path | CSA CCM v4.1 | ISO 27001:2022 | NIST CSF 2.0 | CTPAT | PIP | BASC v6 | WCO SAFE | AEO/AEO-S |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Governance | Governance Library Charter | [`governance/charter-governance-library.md`](../governance/charter-governance-library.md) | GRC-01, GRC-02 | §5.1, §5.2, §6.1 | GV.OC, GV.RM | N/A | Programme governance | §5.1, §7.5 | Pillar II (Customs-to-Business Partnership) | Management commitment |
| Governance | Policy: Exception and Risk Acceptance Management | [`governance/policy-exception-and-risk-acceptance-management.md`](../governance/policy-exception-and-risk-acceptance-management.md) | GRC-04, GRC-05 | §6.1.3, §8.2 | GV.RM, ID.RA | N/A | N/A | §6.1, §10 | N/A | Risk management |
| Governance | Standard: Records Retention and Destruction | [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md) | DSP-07, DSP-08 | A.5.33, A.8.10 | PR.DS | Documentation and record-keeping | Record retention | §7.5 | Pillar II (Customs-to-Business) | Documentation security; Trade records retention |
| Governance | Register: Document Index and Classification | [`governance/register-document-index-and-classification.md`](../governance/register-document-index-and-classification.md) | GRC-01 | §7.5 | GV.OC | N/A | N/A | §7.5 | N/A | Documentation security |

---

## Risk domain

| Domain | Document Title | Path | CSA CCM v4.1 | ISO 27001:2022 | NIST CSF 2.0 | CTPAT | PIP | BASC v6 | WCO SAFE | AEO/AEO-S |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Risk | Policy: Enterprise Governance and Risk Management | [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md) | GRC-01, GRC-02, GRC-03 | §5.1, §5.3, §6.1, §6.2 | GV.RM, GV.OC, ID.RA | N/A | Programme governance | §5.1, §6.1 | N/A | Management commitment; Risk management |
| Risk | Standard: Enterprise Risk Management | [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md) | GRC-01, GRC-02 | §6.1.1, §6.1.2, §6.1.3, §8.2, §8.3 | ID.RA, GV.RM | N/A | Risk assessment | §6.1 | N/A | IT security risk management; Risk management |
| Risk | Standard: Third-Party and Supply Chain Risk | [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md) | STA-01, STA-02, STA-03 | A.5.19, A.5.20, A.5.21, A.5.22 | GV.SC | Business partner requirements | Third-party security | §6.1, §8.6 | Pillar II (Customs-to-Business; Standard 6) | Business partners; IT security risk management |
| Risk | Procedure: Risk Assessment Methodology | [`risk/procedure-risk-assessment-methodology.md`](../risk/procedure-risk-assessment-methodology.md) | GRC-01, GRC-02 | §6.1.1, §6.1.2, §6.1.3, §8.2, §8.3 | ID.RA, GV.RM | N/A | Risk assessment | §6.1 | N/A | IT security risk management |
| Risk | Procedure: Risk Register | [`risk/procedure-risk-register.md`](../risk/procedure-risk-register.md) | GRC-02 | §6.1.2, §6.1.3, §8.2, §8.3, §9.1 | ID.RA, GV.RM | N/A | Risk assessment | §6.1, §9.1 | N/A | IT security risk management |
| Risk | Procedure: Risk Acceptance | [`risk/procedure-risk-acceptance.md`](../risk/procedure-risk-acceptance.md) | GRC-02, GRC-04 | §6.1.3, §8.3 | GV.RM, ID.RA | N/A | N/A | §6.1, §10 | N/A | Risk management |
| Risk | Register: Assurance Map | [`risk/register-assurance-map.md`](../risk/register-assurance-map.md) | A&A-02, A&A-03, GRC-02 | §9.1, §9.2, A.5.35 | GV.OV, GV.RM, ID.IM | N/A | N/A | §9.1, §9.2 | N/A | IT controls review and testing |
| Risk | Register: Key Risk Indicators | [`risk/register-key-risk-indicators.md`](../risk/register-key-risk-indicators.md) | GRC-02, A&A-03 | §6.1, §9.1 | GV.RM, ID.RA, ID.IM | N/A | N/A | §6.1, §9.1 | N/A | IT controls review and testing |
| Risk | Register: Scenario Risk Catalogue | [`risk/register-scenario-risk-catalogue.md`](../risk/register-scenario-risk-catalogue.md) | GRC-02, BCR-02, A&A-03 | §6.1, §8.2 | ID.RA, GV.RM, RC.RP | N/A | N/A | §6.1 | N/A | IT security risk management |
| Risk | Guideline: Quantitative Risk Analysis | [`risk/guideline-quantitative-risk-analysis.md`](../risk/guideline-quantitative-risk-analysis.md) | GRC-02, A&A-03 | §6.1.2, §8.2 | ID.RA, GV.RM | N/A | N/A | N/A | N/A | IT security risk management |
| Risk | Template: Enterprise Risk Register | [`risk/template-enterprise-risk-register.md`](../risk/template-enterprise-risk-register.md) | GRC-02, GRC-04 | §6.1.2, §6.1.3, §9.1 | ID.RA, GV.RM | N/A | N/A | §6.1 | N/A | IT security risk management |
| Risk | Template: Operational Risk Register | [`risk/template-operational-risk-register.md`](../risk/template-operational-risk-register.md) | GRC-02, GRC-04 | §6.1.2, §6.1.3, §9.1 | ID.RA, GV.RM | N/A | N/A | §6.1 | N/A | IT security risk management |
| Risk | Template: Risk Appetite Statement | [`risk/template-risk-appetite-statement.md`](../risk/template-risk-appetite-statement.md) | GRC-02 | §5.1, §6.1.1, §6.1.3 | GV.RM, GV.OV | N/A | N/A | N/A | N/A | Management commitment; Risk management |
| Risk | Template: Board Risk Report | [`risk/template-board-risk-report.md`](../risk/template-board-risk-report.md) | GRC-02, GRC-06 | §5.1, §9.1, §9.3 | GV.RM, GV.OV | N/A | N/A | N/A | N/A | Management commitment |
| Risk | Annex: AI-Specific Risk Methodology | [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md) | GRC-02, AIS-01, A&A-03 | §6.1.2, §6.1.3, §8.2 | ID.RA, GV.RM, GV.OC | N/A | N/A | N/A | N/A | IT security risk management |

---

## Compliance domain

| Domain | Document Title | Path | CSA CCM v4.1 | ISO 27001:2022 | NIST CSF 2.0 | CTPAT | PIP | BASC v6 | WCO SAFE | AEO/AEO-S |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Compliance | Policy: Compliance, Audit, and CAPA Management | [`compliance/policy-compliance-and-audit-management.md`](policy-compliance-and-audit-management.md) | GRC-06, GRC-07, GRC-08 | §9.2, §9.3, §10.1, §10.2 | GV.OC, ID.IM | N/A | Programme governance | §9.2, §10 | N/A | IT controls review and testing |
| Compliance | Register: Global Regulatory Applicability | [`compliance/register-global-regulatory-applicability.md`](register-global-regulatory-applicability.md) | GRC-01, GRC-06 | §4.1, §4.2, §6.1 | GV.OC, GV.RM | N/A | Programme governance | §4.1, §6.1 | N/A | Management commitment |
| Compliance | Register: BASC IT and Information Security Responsibilities | [`compliance/logistics/register-basc-it-responsibilities.md`](../compliance/logistics/register-basc-it-responsibilities.md) | GRC-01, GRC-02 | §5.3, §6.1, §9.1 | GV.OC, GV.RM | N/A | N/A | §5.1, §6.1, §7.2, §7.5, §8.1, §8.3, §8.4, §8.5, §9.1, §9.2, §10 | Pillar II (Customs-to-Business; Standard 6) | All AEO-S IT requirement areas |
| Compliance | Register: BASC IT Compliance Monitoring and KPIs | [`compliance/logistics/register-basc-it-compliance-kpis.md`](../compliance/logistics/register-basc-it-compliance-kpis.md) | GRC-04, GRC-08 | §9.1 | GV.OC, ID.IM | N/A | N/A | §9.1 | N/A | IT controls review and testing |
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
| Security | Standard: Data Classification and Handling | [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md) | DSP-01, DSP-02, DSP-03 | A.5.12, A.5.13, A.8.10 | PR.DS | N/A | Data protection | §7.5, §8.4 | Pillar II (ICT security) | Documentation security |
| Security | Standard: Privileged Access Management | [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md) | IAM-05, IAM-06, IAM-07 | A.5.18, A.8.2 | PR.AA, PR.IR | IT access controls | Access controls | §8.5 | Pillar II (Standard 6, access) | Access to IT systems |
| Security | Standard: Authentication and Password Management | [`security/standard-authentication-and-password-management.md`](../security/standard-authentication-and-password-management.md) | IAM-02, IAM-03, IAM-08 | A.5.17, A.8.5 | PR.AA | IT access controls | Access controls | §8.3, §8.5 | Pillar II (Standard 6, access) | Access to IT systems; Personnel security screening |
| Security | Procedure: Incident Response | [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) | SEF-01, SEF-02, SEF-03, SEF-04, SEF-05 | A.5.24, A.5.25, A.5.26, A.5.27, A.5.28 | RS.MA, RS.AN, RS.CO, RS.MI, RC.RP | IT security incidents | Incident response | §8.4, §10 | Pillar II (ICT security) | IT security incident detection and response |
| Security | Procedure: Vulnerability Management | [`security/procedure-vulnerability-management.md`](../security/procedure-vulnerability-management.md) | TVM-01, TVM-02, TVM-03 | A.8.8 | ID.RA, PR.PS, DE.CM | IT security controls | IT security | §8.4, §9.1 | Pillar II (ICT security) | IT security controls review and testing |

---

## Operations domain

| Domain | Document Title | Path | CSA CCM v4.1 | ISO 27001:2022 | NIST CSF 2.0 | CTPAT | PIP | BASC v6 | WCO SAFE | AEO/AEO-S |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Operations | Standard: Production Security Requirements | [`operations/standard-production-security-requirements.md`](../operations/standard-production-security-requirements.md) | CCC-01, CCC-02, TVM-01 | A.8.8, A.8.9, A.8.31 | PR.PS, DE.CM | IT security controls | IT security | §8.1, §8.4 | Pillar II (ICT security) | IT systems protection |
| Operations | Standard: Network Security and Segmentation | [`operations/standard-network-security-and-segmentation.md`](../operations/standard-network-security-and-segmentation.md) | I&S-03, I&S-06, I&S-08, I&S-09 | A.8.20, A.8.21, A.8.22 | PR.IR, DE.CM | IT security controls | Network security | §8.4 | Pillar II (ICT security) | IT systems protection |
| Operations | Standard: Cloud Security Configuration Baseline | [`operations/standard-cloud-security-configuration-baseline.md`](../operations/standard-cloud-security-configuration-baseline.md) | CCC-01, CCC-02, CEK-01, IAM-01 | A.8.9, A.8.23, A.8.24 | PR.PS, PR.IR | IT security controls | IT security | §8.4 | Pillar II (ICT security) | Information systems security |
| Operations | Standard: Physical Security of IT Infrastructure | [`operations/standard-physical-security-of-it-infrastructure.md`](../operations/standard-physical-security-of-it-infrastructure.md) | DCS-01, DCS-02, DCS-03, DCS-04, DCS-05 | A.7.1, A.7.2, A.7.3, A.7.4, A.7.5, A.7.6, A.7.7, A.7.8 | PR.IR | Physical access controls | Physical security | §8.4 | Pillar II (Customs-to-Business; physical security) | Physical and access security |
| Operations | Standard: Certificate Authority Management | [`operations/standard-certificate-authority-management.md`](../operations/standard-certificate-authority-management.md) | CEK-03, CEK-04, IAM-08 | A.8.24 | PR.DS | IT security controls | IT security | §8.4 | Pillar II (ICT security) | Information systems security |
| Operations | Procedure: Change Management and Configuration Control | [`operations/procedure-change-management-and-configuration-control.md`](../operations/procedure-change-management-and-configuration-control.md) | CCC-01, CCC-02, CCC-03, CCC-04, CCC-05 | A.8.9, A.8.32 | PR.PS, ID.IM | IT security controls | IT security | §8.1 | Pillar II (ICT security) | IT systems protection |
| Operations | Procedure: Endpoint Management and Device Compliance | [`operations/procedure-endpoint-management-and-device-compliance.md`](../operations/procedure-endpoint-management-and-device-compliance.md) | UEM-01, UEM-02, UEM-03 | A.8.1, A.8.7 | PR.IR, DE.CM | IT security controls | IT security | §8.4 | Pillar II (ICT security) | IT security incident detection and response |
| Operations | Procedure: Media Handling and Transport | [`operations/procedure-media-handling-and-transport.md`](../operations/procedure-media-handling-and-transport.md) | DSP-04, DSP-05 | A.7.10, A.8.10 | PR.DS | N/A | Data protection | §7.5, §8.4 | N/A | Documentation security |
| Operations | Procedure: Security Monitoring and Alert Management | [`operations/procedure-security-monitoring-and-alert-management.md`](../operations/procedure-security-monitoring-and-alert-management.md) | LOG-02, LOG-03, SEF-01 | A.8.15, A.8.16 | DE.CM, DE.AE, RS.MA | IT security monitoring | IT security | §9.1 | Pillar II (ICT security) | IT security incident detection and response |
| Operations | Procedure: Threat Intelligence and SIEM Operations | [`operations/procedure-threat-intelligence-and-siem-operations.md`](../operations/procedure-threat-intelligence-and-siem-operations.md) | TVM-02, LOG-03, SEF-01 | A.5.7, A.8.16 | DE.CM, DE.AE, ID.RA | IT security monitoring | IT security | §8.4, §9.1 | Pillar II (ICT security) | IT security incident detection and response |
| Operations | Framework: IT Service Management | [`operations/framework-it-service-management.md`](../operations/framework-it-service-management.md) | SEF-02, SEF-01, CCC-01 | A.5.24, A.5.26, A.8.32 | RS.MA, ID.IM, PR.PS | N/A | N/A | N/A | N/A | N/A |
| Operations | Standard: Service Level Management | [`operations/standard-service-level-management.md`](../operations/standard-service-level-management.md) | SEF-02, STA-11 | §9.1, A.5.22 | ID.IM, GV.OV, ID.RA | N/A | N/A | N/A | N/A | N/A |
| Operations | Standard: Site Reliability Engineering | [`operations/standard-site-reliability-engineering.md`](../operations/standard-site-reliability-engineering.md) | SEF-03, CCC-01 | A.5.29, A.5.26, A.8.32 | DE.CM, RS.MA, RC.RP | N/A | N/A | N/A | N/A | N/A |
| Operations | Procedure: Patch Management | [`operations/procedure-patch-management.md`](../operations/procedure-patch-management.md) | TVM-08, TVM-01, CCC-01 | A.8.8, A.8.32, A.5.20 | PR.PS, ID.RA, DE.CM | IT security controls | IT security | §8.1, §8.4 | Pillar II (ICT security) | IT systems protection |
| Operations | Procedure: Release Management | [`operations/procedure-release-management.md`](../operations/procedure-release-management.md) | CCC-01, CCC-02, CCC-09 | A.8.32 | PR.PS, ID.IM | IT security controls | IT security | §8.1 | Pillar II (ICT security) | IT systems protection |
| Operations | Standard: Capacity and Performance Management | [`operations/standard-capacity-and-performance-management.md`](../operations/standard-capacity-and-performance-management.md) | I&S-02, BCR-03 | A.8.6 | ID.AM, PR.IR | N/A | N/A | N/A | N/A | N/A |
| Operations | Standard: Observability and Telemetry | [`operations/standard-observability-and-telemetry.md`](../operations/standard-observability-and-telemetry.md) | LOG-01, LOG-03, LOG-07 | A.8.15, A.8.16 | DE.CM, DE.AE | N/A | N/A | N/A | N/A | N/A |
| Operations | Standard: IT Financial Management | [`operations/standard-it-financial-management.md`](../operations/standard-it-financial-management.md) | GRC-01, GRC-02 | §5.1, A.5.13, A.5.14 | GV.OC, GV.RM | N/A | N/A | N/A | N/A | N/A |
| Operations | Register: Asset Inventory | [`operations/register-asset-inventory.md`](../operations/register-asset-inventory.md) | DCS-06, DCS-07, UEM-04 | A.5.9, A.5.10, A.8.1 | ID.AM | N/A | N/A | §8.1 | N/A | IT systems protection |
| Operations | Register: IT Operations KPIs | [`operations/register-it-operations-kpis.md`](../operations/register-it-operations-kpis.md) | GRC-02, A&A-03, SEF-05 | §6.1, §9.1 | GV.OV, ID.IM | N/A | N/A | §9.1 | N/A | IT controls review and testing |
| Operations | Register: IT Security Operations | [`operations/register-it-security-operations.md`](../operations/register-it-security-operations.md) | SEF-01, LOG-03, A&A-03 | §9.1, A.8.8 | DE.CM, ID.IM | N/A | N/A | §8.4, §9.1 | N/A | IT security incident detection and response |

---

## Supply chain domain

| Domain | Document Title | Path | CSA CCM v4.1 | ISO 27001:2022 | NIST CSF 2.0 | CTPAT | PIP | BASC v6 | WCO SAFE | AEO/AEO-S |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Supply Chain | Framework: Supplier and Cloud Governance | [`supply-chain/framework-supplier-and-cloud-governance.md`](../supply-chain/framework-supplier-and-cloud-governance.md) | STA-01, STA-02, STA-03, STA-04, STA-05 | A.5.19, A.5.20, A.5.21, A.5.22, A.5.23 | GV.SC | Business partner requirements; Cargo security | Third-party and supply chain security | §8.6 | Pillar II (Standard 6, business partners); Pillar II (Standard 5, supply chain) | Business partners |
| Supply Chain | Standard: Supplier Security and Privacy Assurance | [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md) | STA-01, STA-02, STA-03 | A.5.19, A.5.20, A.5.21, A.5.22 | GV.SC | Business partner requirements | Third-party security | §8.6 | Pillar II (Customs-to-Business; Standard 6) | Business partners |
| Supply Chain | Standard: Supplier Resilience Monitoring | [`supply-chain/standard-supplier-resilience-monitoring.md`](../supply-chain/standard-supplier-resilience-monitoring.md) | STA-10, STA-13, BCR-01 | A.5.19, A.5.22, A.5.30 | GV.SC, RC.RP | Business partner requirements; ongoing monitoring | Third-party and supply chain security | §8.6 | Pillar II (Customs-to-Business; Standard 6) | Business partners |
| Supply Chain | Standard: Cloud Exit and Data Portability | [`supply-chain/standard-cloud-exit-and-data-portability.md`](../supply-chain/standard-cloud-exit-and-data-portability.md) | IPY-01, IPY-02, IPY-03, IPY-04, STA-13 | A.5.20, A.5.23 | ID.AM, GV.SC | N/A | N/A | N/A | N/A | N/A |
| Supply Chain | Procedure: Supplier Due Diligence | [`supply-chain/procedure-supplier-due-diligence.md`](../supply-chain/procedure-supplier-due-diligence.md) | STA-02, STA-04 | A.5.19, A.5.20 | GV.SC | Business partner vetting | Third-party vetting | §8.6 | Pillar II (Customs-to-Business; Standard 6) | Business partners |
| Supply Chain | Procedure: Supplier Onboarding Security Review | [`supply-chain/procedure-supplier-onboarding-security-review.md`](../supply-chain/procedure-supplier-onboarding-security-review.md) | STA-01, STA-02, STA-04, STA-12, IAM-06 | A.5.19, A.5.20, A.5.21 | GV.SC, ID.RA | Business partner vetting | Third-party vetting | §8.6 | Pillar II (Customs-to-Business; Standard 6) | Business partners |
| Supply Chain | Procedure: Supplier Ongoing Monitoring | [`supply-chain/procedure-supplier-ongoing-monitoring.md`](../supply-chain/procedure-supplier-ongoing-monitoring.md) | STA-13, STA-14, GRC-07 | A.5.19, A.5.22, §9.1 | GV.SC, DE.CM, ID.RA | Business partner requirements | Third-party security | §8.6 | Pillar II (Customs-to-Business; Standard 6) | Business partners |
| Supply Chain | Procedure: Supplier Audit | [`supply-chain/procedure-supplier-audit.md`](../supply-chain/procedure-supplier-audit.md) | STA-04, STA-05, GRC-07 | A.5.20, A.5.22, §9.2 | GV.SC | Business partner requirements | Third-party audit | §8.6, §9.2 | Pillar II (Customs-to-Business; Standard 6) | Business partners; IT controls review and testing |
| Supply Chain | Procedure: Supplier Exit and Data Return | [`supply-chain/procedure-supplier-exit-and-data-return.md`](../supply-chain/procedure-supplier-exit-and-data-return.md) | STA-14, DSP-16, IAM-07 | A.5.18, A.5.20, A.8.10 | GV.SC, PR.DS, PR.AA | Business partner requirements; change of approved service providers | Third-party security | §8.6 | Pillar II (Customs-to-Business; Standard 6) | Business partners |
| Supply Chain | Procedure: Fourth-Party and Nth-Party Risk | [`supply-chain/procedure-fourth-party-and-nth-party-risk.md`](../supply-chain/procedure-fourth-party-and-nth-party-risk.md) | STA-01, STA-08, STA-09 | A.5.19, A.5.21, A.5.22 | GV.SC, ID.RA | Business partner requirements | Third-party security | §6.1, §8.6 | Pillar II (Customs-to-Business; Standard 6) | Business partners; IT security risk management |
| Supply Chain | Procedure: Third-Party AI Due Diligence | [`supply-chain/procedure-third-party-ai-due-diligence.md`](../supply-chain/procedure-third-party-ai-due-diligence.md) | STA-01, STA-02, STA-04, STA-13 | A.5.19, A.5.20, A.5.21, A.5.22 | GV.SC, ID.RA | N/A | N/A | N/A | N/A | N/A |
| Supply Chain | Register: Concentration Risk | [`supply-chain/register-concentration-risk.md`](../supply-chain/register-concentration-risk.md) | STA-10, BCR-02, GRC-02 | A.5.19, A.5.21, A.5.30, §6.1 | GV.SC, ID.RA | N/A | N/A | N/A | N/A | N/A |
| Supply Chain | Register: Software Bill of Materials | [`supply-chain/register-sbom.md`](../supply-chain/register-sbom.md) | STA-09, TVM-06, TVM-08, TVM-03 | A.5.21, A.8.30, A.8.31 | ID.AM, GV.SC, ID.RA | N/A | N/A | N/A | N/A | N/A |
| Supply Chain | Register: Subprocessor Register Template | [`supply-chain/register-subprocessor-template.md`](../supply-chain/register-subprocessor-template.md) | STA-03, STA-13, DSP-10, DSP-19 | A.5.19, A.5.20, A.5.21, A.5.34 | GV.SC, PR.DS | N/A | N/A | N/A | N/A | N/A |
| Supply Chain | Register: Supplier Risk Register Template | [`supply-chain/register-supplier-risk-template.md`](../supply-chain/register-supplier-risk-template.md) | STA-01, STA-02, STA-04, STA-14, GRC-02 | A.5.19, A.5.20, A.5.21, A.5.22 | GV.SC, ID.RA | Business partner requirements | Third-party security | §8.6 | Pillar II (Customs-to-Business; Standard 6) | Business partners |
| Supply Chain | Template: Supplier Offboarding Evidence | [`supply-chain/template-supplier-offboarding-evidence.md`](../supply-chain/template-supplier-offboarding-evidence.md) | IPY-04, DSP-02, STA-12 | A.5.11, A.5.22, A.8.10 | GV.SC, PR.DS | Business partner requirements | Third-party security | §8.6 | Pillar II (Customs-to-Business; Standard 6) | Business partners |
| Supply Chain | Template: Supplier Security Questionnaire | [`supply-chain/template-supplier-security-questionnaire.md`](../supply-chain/template-supplier-security-questionnaire.md) | A&A-04, STA-13, STA-16 | A.5.19, A.5.21, A.5.22 | GV.SC, ID.RA | Business partner vetting; security questionnaire | Third-party vetting | §8.6 | Pillar II (Customs-to-Business; Standard 6) | Business partners |
| Supply Chain | Annex: Trade and Supply-Chain Continuity Controls | [`supply-chain/annex-trade-and-supply-chain-continuity-controls.md`](../supply-chain/annex-trade-and-supply-chain-continuity-controls.md) | STA-01, STA-08, BCR-02, BCR-04 | A.5.19, A.5.29, A.5.30 | GV.SC, RC.RP | Business partner requirements; Cargo security | Third-party security; Business continuity | §8.1, §8.6 | Pillar II (Customs-to-Business; Standard 6) | Business partners; IT systems backup and continuity |

---

## Resilience domain

| Domain | Document Title | Path | CSA CCM v4.1 | ISO 27001:2022 | NIST CSF 2.0 | CTPAT | PIP | BASC v6 | WCO SAFE | AEO/AEO-S |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Resilience | Policy: Business Continuity and Disaster Recovery | [`resilience/policy-business-continuity-and-disaster-recovery.md`](../resilience/policy-business-continuity-and-disaster-recovery.md) | BCR-01, BCR-02 | A.5.29, A.5.30 | RC.RP, RC.CO | N/A | Business continuity | §8.1 | N/A | IT systems backup and continuity |
| Resilience | Standard: Business Continuity and Disaster Recovery | [`resilience/standard-business-continuity-and-disaster-recovery.md`](../resilience/standard-business-continuity-and-disaster-recovery.md) | BCR-01, BCR-02, BCR-03, BCR-04, BCR-05 | A.5.29, A.5.30, A.8.14 | RC.RP, RC.CO, GV.OC | N/A | Business continuity | §8.1 | N/A | IT systems backup and continuity |
| Resilience | Procedure: Backup and Recovery | [`resilience/procedure-backup-and-recovery.md`](../resilience/procedure-backup-and-recovery.md) | BCR-08, BCR-09, BCR-10 | A.8.13 | RC.RP | N/A | Business continuity | §8.1 | N/A | IT systems backup and continuity |
| Resilience | Framework: Business Continuity and Resilience | [`resilience/framework-business-continuity-and-resilience.md`](../resilience/framework-business-continuity-and-resilience.md) | BCR-01, BCR-02, BCR-03, BCR-04, BCR-06, BCR-07 | A.5.29, A.5.30, A.8.13, A.8.14 | RC.RP, RC.CO, GV.OC, ID.RA | N/A | Business continuity | §8.1 | N/A | IT systems backup and continuity |
| Resilience | Plan: Business Continuity and Crisis Management | [`resilience/plan-business-continuity-and-crisis-management.md`](../resilience/plan-business-continuity-and-crisis-management.md) | BCR-04, BCR-07, BCR-09, SEF-03 | A.5.24, A.5.29, A.5.30 | RC.RP, RC.CO, RS.MA | N/A | Business continuity | §8.1 | N/A | Business continuity |
| Resilience | Plan: IT Disaster Recovery | [`resilience/plan-it-disaster-recovery.md`](../resilience/plan-it-disaster-recovery.md) | BCR-08, BCR-09, BCR-11 | A.5.29, A.5.30, A.8.13, A.8.14 | RC.RP, RC.CO, ID.IM | N/A | Business continuity | §8.1 | N/A | IT systems backup and continuity |
| Resilience | Plan: Pandemic Continuity | [`resilience/plan-pandemic-continuity.md`](../resilience/plan-pandemic-continuity.md) | BCR-01, BCR-02, BCR-04 | A.5.29, A.5.30 | RC.RP, RC.CO, GV.OC | N/A | Business continuity | §8.1 | N/A | Business continuity |
| Resilience | Plan: Physical Site Continuity | [`resilience/plan-physical-site-continuity.md`](../resilience/plan-physical-site-continuity.md) | BCR-01, BCR-04, BCR-09 | A.5.29, A.5.30 | RC.RP, RC.CO, PR.IR | N/A | Business continuity | §8.1 | N/A | Business continuity |
| Resilience | Plan: Crisis Communication | [`resilience/plan-crisis-communication.md`](../resilience/plan-crisis-communication.md) | BCR-07, SEF-08 | A.5.24, A.5.26 | RC.CO, RS.CO | N/A | N/A | N/A | N/A | N/A |
| Resilience | Procedure: Business Impact Analysis | [`resilience/procedure-business-impact-analysis.md`](../resilience/procedure-business-impact-analysis.md) | BCR-02, BCR-03 | A.5.29, A.5.30 | ID.RA, GV.OC, RC.RP | N/A | Business continuity | §8.1 | N/A | Business continuity |
| Resilience | Procedure: Continuity and Recovery Testing | [`resilience/procedure-continuity-and-recovery-testing.md`](../resilience/procedure-continuity-and-recovery-testing.md) | BCR-06, BCR-10 | A.5.30, A.8.13 | RC.RP, ID.IM | N/A | Business continuity | §8.1 | N/A | IT systems backup and continuity |
| Resilience | Procedure: Crisis Management and Emergency Operations Activation | [`resilience/procedure-crisis-management-eoc-activation.md`](../resilience/procedure-crisis-management-eoc-activation.md) | BCR-07, BCR-09 | A.5.29, A.5.30 | RC.RP, RC.CO | N/A | Business continuity | §8.1 | N/A | Business continuity |
| Resilience | Procedure: Cross-Domain Incident Coordination | [`resilience/procedure-cross-domain-incident-coordination.md`](../resilience/procedure-cross-domain-incident-coordination.md) | SEF-07, SEF-08, SEF-09 | A.5.24, A.5.26, A.5.28 | RS.MA, RS.CO, RC.CO | N/A | Incident response | §8.4, §10 | N/A | IT security incident detection and response |
| Resilience | Procedure: Security Incident Reporting and Escalation | [`resilience/procedure-security-incident-reporting-and-escalation.md`](../resilience/procedure-security-incident-reporting-and-escalation.md) | SEF-01, SEF-06, SEF-08 | A.5.24, A.5.25, A.5.26 | DE.AE, RS.MA, RS.CO | N/A | Incident response | §8.4, §10 | N/A | IT security incident detection and response |
| Resilience | Guideline: Emergency Response and Protective Actions | [`resilience/guideline-emergency-response-and-protective-actions.md`](../resilience/guideline-emergency-response-and-protective-actions.md) | BCR-09, SEF-01 | A.5.24, A.5.29 | RS.MA, GV.RR | N/A | N/A | N/A | N/A | N/A |
| Resilience | Register: Emergency Operations Contact Directory | [`resilience/register-eoc-contact-directory.md`](../resilience/register-eoc-contact-directory.md) | BCR-07, SEF-10 | A.5.24, A.5.29 | RC.CO, RS.CO | N/A | Business continuity | §8.1 | N/A | Business continuity |
| Resilience | Register: Resilience Metrics and Testing Log | [`resilience/register-resilience-metrics-and-testing-log.md`](../resilience/register-resilience-metrics-and-testing-log.md) | A&A-03, BCR-06, BCR-10 | A.5.29, A.5.30, §9.1 | RC.RP, ID.IM | N/A | Business continuity | §8.1 | N/A | IT controls review and testing |
| Resilience | Template: Departmental Continuity Plan | [`resilience/template-departmental-continuity-plan.md`](../resilience/template-departmental-continuity-plan.md) | BCR-02, BCR-03, BCR-04 | A.5.29, A.5.30 | RC.RP, RC.CO | N/A | Business continuity | §8.1 | N/A | Business continuity |
| Resilience | Template: Lessons Learned | [`resilience/template-lessons-learned.md`](../resilience/template-lessons-learned.md) | BCR-06 | A.5.27 | ID.IM | N/A | N/A | N/A | N/A | N/A |
| Resilience | Template: Recovery Runbook | [`resilience/template-recovery-runbook.md`](../resilience/template-recovery-runbook.md) | BCR-09, BCR-10 | A.5.30, A.8.13 | RC.RP, RC.CO | N/A | Business continuity | §8.1 | N/A | IT systems backup and continuity |
| Resilience | Template: Tabletop Exercise | [`resilience/template-tabletop-exercise.md`](../resilience/template-tabletop-exercise.md) | BCR-06, BCR-10 | A.5.30 | ID.IM, RC.RP | N/A | N/A | N/A | N/A | N/A |

---

## Privacy domain

| Domain | Document Title | Path | CSA CCM v4.1 | ISO 27001:2022 | NIST CSF 2.0 | CTPAT | PIP | BASC v6 | WCO SAFE | AEO/AEO-S |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Privacy | Policy: Privacy and Data Governance | [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md) | DSP-01, DSP-02, DSP-03, DSP-04 | A.5.34, A.8.11, A.8.12 | GV.PO, PR.DS | N/A | Data protection | §8.4 | N/A | Documentation security |
| Privacy | Procedure: Privacy Impact and Cross-Border Transfer | [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../privacy/procedure-privacy-impact-and-cross-border-transfer.md) | DSP-03, DSP-04, DSP-06 | A.5.34 | GV.PO, PR.DS, ID.RA | N/A | Data protection | §8.4 | N/A | Documentation security |

---

## Architecture domain

| Domain | Document Title | Path | CSA CCM v4.1 | ISO 27001:2022 | NIST CSF 2.0 | CTPAT | PIP | BASC v6 | WCO SAFE | AEO/AEO-S |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Architecture | Enterprise Architecture Framework | [`architecture/framework-enterprise-architecture.md`](../architecture/framework-enterprise-architecture.md) | GRC-01, GRC-02 | §6.1, A.5.8, A.8.27 | GV.OC, GV.RM, ID.AM, PR.PS | N/A | N/A | N/A | N/A | N/A |
| Architecture | Architecture Review Procedure | [`architecture/procedure-architecture-review.md`](../architecture/procedure-architecture-review.md) | GRC-01, CCC-01, CCC-02 | A.5.8, A.8.27, §8.1 | GV.OC, GV.RM, PR.PS, ID.IM | N/A | N/A | N/A | N/A | N/A |
| Architecture | API Design Standard | [`architecture/standard-api-design.md`](../architecture/standard-api-design.md) | AIS-01, AIS-02, AIS-04, IPY-01 | A.5.14, A.8.26, A.8.27 | ID.AM, PR.DS, PR.PS | N/A | N/A | N/A | N/A | N/A |
| Architecture | Architecture Decision Records Standard | [`architecture/standard-architecture-decision-records.md`](../architecture/standard-architecture-decision-records.md) | GRC-01, CCC-02, CCC-03 | §7.5, A.8.27 | GV.OC, PR.PS, ID.IM | N/A | N/A | N/A | N/A | N/A |
| Architecture | Data Architecture Standard | [`architecture/standard-data-architecture.md`](../architecture/standard-data-architecture.md) | DSP-01, DSP-02, DSP-03, DSP-05, DSP-07 | A.5.12, A.5.13, A.5.34, A.8.10 | GV.OC, ID.AM, PR.DS | N/A | N/A | N/A | N/A | N/A |
| Architecture | Integration Architecture Standard | [`architecture/standard-integration-architecture.md`](../architecture/standard-integration-architecture.md) | AIS-04, IPY-01, I&S-03, DSP-04 | A.5.14, A.8.20, A.8.21, A.8.26 | ID.AM, PR.DS, PR.IR, DE.CM | N/A | N/A | N/A | N/A | N/A |
| Architecture | Reference Architecture Standard | [`architecture/standard-reference-architecture.md`](../architecture/standard-reference-architecture.md) | GRC-01, AIS-01 | A.8.27, A.8.32 | GV.OC, ID.AM, PR.PS | N/A | N/A | N/A | N/A | N/A |
| Architecture | Technology Radar Standard | [`architecture/standard-technology-radar.md`](../architecture/standard-technology-radar.md) | GRC-01, STA-01 | §6.1, A.5.20, A.8.30 | GV.OC, GV.SC, ID.AM | N/A | N/A | N/A | N/A | N/A |

---

## Dev-security domain

| Domain | Document Title | Path | CSA CCM v4.1 | ISO 27001:2022 | NIST CSF 2.0 | CTPAT | PIP | BASC v6 | WCO SAFE | AEO/AEO-S |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Dev-security | AI Coding Assistant Security Guideline | [`dev-security/guideline-ai-coding-assistant-security.md`](../dev-security/guideline-ai-coding-assistant-security.md) | AIS-04, AIS-05, AIS-07, TVM-06 | A.8.27, A.8.29, A.5.36 | GV.SC, PR.PS, ID.RA | N/A | N/A | N/A | N/A | N/A |
| Dev-security | Secure Development and Engineering Policy | [`dev-security/policy-secure-development-and-engineering.md`](../dev-security/policy-secure-development-and-engineering.md) | AIS-04, AIS-05, AIS-06, CCC-01, TVM-06 | A.8.25, A.8.28, A.8.29, A.8.30, A.8.31 | PR.PS, ID.RA, GV.RR | N/A | N/A | N/A | N/A | N/A |
| Dev-security | Secure Code Review Procedure | [`dev-security/procedure-secure-code-review.md`](../dev-security/procedure-secure-code-review.md) | AIS-04, AIS-05, CCC-01, CCC-02, TVM-06 | A.8.28, A.8.29, A.8.30, A.8.4 | PR.PS, ID.RA, DE.CM | N/A | N/A | N/A | N/A | N/A |
| Dev-security | Compliance Controls and Gap Register Template | [`dev-security/register-compliance-controls-and-gap-register.md`](../dev-security/register-compliance-controls-and-gap-register.md) | A&A-04, GRC-07, A&A-05, A&A-06, GRC-01 | A.5.36, A.5.35, §9.1 | GV.OC, ID.IM, GV.RM | N/A | N/A | N/A | N/A | N/A |
| Dev-security | API Security Standard | [`dev-security/standard-api-security.md`](../dev-security/standard-api-security.md) | AIS-08, AIS-05, IAM-15, IAM-13, LOG-03 | A.8.26, A.8.28, A.8.25, A.5.14 | PR.AA, PR.DS, DE.CM | N/A | N/A | N/A | N/A | N/A |
| Dev-security | AWS Cloud Hardening Baseline Standard | [`dev-security/standard-cloud-hardening-baseline-aws.md`](../dev-security/standard-cloud-hardening-baseline-aws.md) | I&S-04, I&S-03, IAM-01, LOG-01, CEK-01 | A.8.9, A.8.20, A.8.24, A.8.15, A.5.15 | PR.AA, PR.DS, DE.CM, PR.PS | N/A | N/A | N/A | N/A | N/A |
| Dev-security | Azure Cloud Hardening Baseline Standard | [`dev-security/standard-cloud-hardening-baseline-azure.md`](../dev-security/standard-cloud-hardening-baseline-azure.md) | I&S-04, I&S-03, IAM-01, LOG-01, CEK-01 | A.8.9, A.8.20, A.8.24, A.8.15, A.5.15 | PR.AA, PR.DS, DE.CM, PR.PS | N/A | N/A | N/A | N/A | N/A |
| Dev-security | Google Cloud Platform Hardening Baseline Standard | [`dev-security/standard-cloud-hardening-baseline-gcp.md`](../dev-security/standard-cloud-hardening-baseline-gcp.md) | I&S-04, I&S-03, IAM-01, LOG-01, CEK-01 | A.8.9, A.8.20, A.8.24, A.8.15, A.5.15 | PR.AA, PR.DS, DE.CM, PR.PS | N/A | N/A | N/A | N/A | N/A |
| Dev-security | Container and Image Security Standard | [`dev-security/standard-container-and-image-security.md`](../dev-security/standard-container-and-image-security.md) | I&S-04, AIS-06, TVM-03, STA-09, I&S-06 | A.8.25, A.8.8, A.8.7, A.8.28 | PR.PS, ID.RA, PR.AA | N/A | N/A | N/A | N/A | N/A |
| Dev-security | Developer Security Requirements | [`dev-security/standard-developer-security-requirements.md`](../dev-security/standard-developer-security-requirements.md) | AIS-02, AIS-05, CEK-01, IAM-13, TVM-04 | A.8.28, A.8.25, A.5.17, A.8.24, A.8.8 | PR.PS, PR.AA, ID.RA | N/A | N/A | N/A | N/A | N/A |
| Dev-security | DevOps Security Requirements | [`dev-security/standard-devops-security-requirements.md`](../dev-security/standard-devops-security-requirements.md) | CCC-01, CCC-04, CCC-05, I&S-05, I&S-04 | A.8.25, A.8.27, A.8.31, A.8.32 | PR.PS, PR.AA, ID.RA | N/A | N/A | N/A | N/A | N/A |
| Dev-security | Mobile Application Security Standard | [`dev-security/standard-mobile-application-security.md`](../dev-security/standard-mobile-application-security.md) | UEM-01, AIS-05, CEK-03, IAM-13, AIS-04 | A.8.26, A.8.25, A.8.28, A.8.24 | PR.DS, PR.AA, PR.PS | N/A | N/A | N/A | N/A | N/A |
| Dev-security | Quality Assurance and Testing Standard | [`dev-security/standard-quality-assurance-and-testing.md`](../dev-security/standard-quality-assurance-and-testing.md) | CCC-02, AIS-05, CCC-01, TVM-07, AIS-07 | A.8.29, A.8.31, A.8.32 | PR.PS, ID.RA | N/A | N/A | N/A | N/A | N/A |
| Dev-security | Security Baseline and Standards Reference | [`dev-security/standard-security-baseline-and-standards-reference.md`](../dev-security/standard-security-baseline-and-standards-reference.md) | GRC-01, GRC-05, IAM-01, DSP-01, CEK-01, LOG-01 | A.5.1, A.5.12, A.5.15, A.8.15, A.8.24 | GV.OC, PR.AA, DE.CM, PR.DS | N/A | N/A | N/A | N/A | N/A |
| Dev-security | Security Quick Reference | [`dev-security/standard-security-quick-reference.md`](../dev-security/standard-security-quick-reference.md) | IAM-01, CEK-03, DSP-01, TVM-01, CCC-01, AIS-05 | A.5.15, A.5.12, A.8.24, A.8.8, A.8.32 | PR.AA, PR.DS, PR.PS | N/A | N/A | N/A | N/A | N/A |
| Dev-security | Software Composition Analysis Standard | [`dev-security/standard-software-composition-analysis.md`](../dev-security/standard-software-composition-analysis.md) | STA-09, TVM-06, TVM-08, TVM-03 | A.8.30, A.8.31, A.5.21 | ID.AM, GV.SC, ID.RA | N/A | N/A | N/A | N/A | N/A |
| Dev-security | Software Evaluation, Acceptance and Lifecycle Management Standard | [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md) | STA-01, AIS-06, CCC-05, TVM-08, STA-13 | A.8.30, A.8.29, A.8.31, A.8.32 | GV.SC, PR.PS, ID.AM | N/A | N/A | N/A | N/A | N/A |

---

## Framework coverage summary

This matrix is being expanded toward comprehensive coverage of the library's substantive documents (policies, standards, procedures, guidelines, frameworks, plans, charters, templates, annexes, and substantive registers across every domain). Library-infrastructure and meta artefacts (the framework matrices and crosswalks themselves, worklists, root meta-specifications, the document index, and generated portals or scorecards) are out of scope. Coverage is added domain by domain, so the matrix is a living document rather than a fixed-size snapshot; the table below therefore describes where each framework's coverage concentrates rather than a per-framework document count, which would drift as the expansion proceeds.

| Framework | Coverage emphasis |
| --- | --- |
| CSA CCM v4.1 | Broad applicability across the IT and security documents, spanning the GRC, IAM, DSP, LOG, I&S, CEK, TVM, SEF, BCR, STA, DCS, UEM, HRS, CCC, AIS, and IPY families |
| ISO/IEC 27001:2022 | Broad applicability across Annex A controls and management-system clauses §4 to §10 |
| NIST CSF 2.0 | Broad applicability across the GV, ID, PR, DE, RS, RC functions |
| CTPAT | Focused on security, operations, supply-chain, and resilience documents; not applicable to most non-logistics IT-governance content |
| PIP (Canada) | Focused on the programme requirements for IT security, access, data protection, and continuity |
| BASC v6 | Broad within the logistics and IT-security scope; operational cargo-security domains are out of this matrix's IT scope |
| WCO SAFE | Focused on Pillar II (Customs-to-Business partnership: AEO and ICT-security requirements); Pillar I (Customs-to-Customs) is largely outside this matrix's IT scope |
| AEO/AEO-S | Focused on the information-systems-security requirement area; physical and personnel security supported by operations and governance documents |



**End of Document**
