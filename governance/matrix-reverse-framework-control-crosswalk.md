# Reverse Framework Control Crosswalk Matrix

**Document Title:** Reverse Framework Control Crosswalk Matrix 
**Document Type:** Matrix 
**Version:** 0.0.1 
**Date:** 2026-05-28 
**Owner:** Control Framework Maintainer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`governance/matrix-cross-framework-alignment.md`](matrix-cross-framework-alignment.md), [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md), [`compliance/matrix-grc-compliance-alignment.md`](../compliance/matrix-grc-compliance-alignment.md), [`supply-chain/matrix-supply-chain-security-programme-alignment.md`](../supply-chain/matrix-supply-chain-security-programme-alignment.md), [`NOTICE.md`](../NOTICE.md) 
**Classification:** Public 
**Category:** Core Governance 
**Review Frequency:** 6 to 12 months and upon material source-framework or document index change 
**Repository Path:** [`governance/matrix-reverse-framework-control-crosswalk.md`](matrix-reverse-framework-control-crosswalk.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This matrix answers the most common adopter question: "given a control identifier or family from an external framework, which documents in this library address it?". The mapping is structured by external framework so that an adopter can navigate from a regulatory or framework control to the relevant library artefacts.

The forward direction (library document to external framework families) is maintained in [`governance/matrix-cross-framework-alignment.md`](matrix-cross-framework-alignment.md). The two matrices are pair-consistent.

This matrix does not reproduce restricted third-party framework text, does not establish compliance, and does not imply certification or audit conclusion. The alignment type column states the nature of each mapping per the rules in [`NOTICE.md`](../NOTICE.md).

---

## Scope and limitations

1. Coverage is partial. The matrix focuses on the framework control areas most frequently cited across the library: ISO 27001:2022 Annex A, ISO 42001:2023, NIST CSF 2.0, NIST SP 800-53 Rev 5, NIST AI RMF, CSA CCM v4.1, EU AI Act, GDPR, DORA, NIS 2, OWASP LLM Top 10, MITRE ATLAS, CTPAT MSC, BASC v6, and WCO SAFE. It is intended to grow over time as adopter demand reveals gaps.
2. Alignment is architectural unless explicitly stated otherwise. The library artefacts establish baseline control structures; adopting organisations must validate implementation, evidence, and operating effectiveness against their own jurisdiction, sector, processing role, threat model, and risk appetite.
3. External control identifiers and clause numbers are referenced for navigation only. The library does not reproduce control text, questionnaire text, audit guidance, or metrics catalogue text from restrictively-licensed frameworks.
4. Mappings cite the most relevant library artefacts. A document may also be relevant to controls beyond those listed here; the inverse forward matrix and per-document `References and framework alignment` sections remain authoritative.

---

## ISO/IEC 27001:2022 Annex A

| Annex A control area | Library documents | Alignment type |
| --- | --- | --- |
| A.5.1 to A.5.4 Organisational policies, roles, segregation of duties | [`security/policy-information-security.md`](../security/policy-information-security.md), [`governance/register-role-authority.md`](register-role-authority.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md) | Architectural recommendation |
| A.5.7 Threat intelligence | [`operations/procedure-threat-intelligence-and-siem-operations.md`](../operations/procedure-threat-intelligence-and-siem-operations.md) | Architectural recommendation |
| A.5.9 Inventory of assets | [`operations/register-asset-inventory.md`](../operations/register-asset-inventory.md) | Evidence category |
| A.5.10 Acceptable use | [`security/policy-acceptable-use.md`](../security/policy-acceptable-use.md) | Architectural recommendation |
| A.5.12 to A.5.13 Classification and handling of information | [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md) | Architectural recommendation |
| A.5.15 to A.5.18 Access control, identity, authentication, privileged access | [`security/policy-identity-and-access-management.md`](../security/policy-identity-and-access-management.md), [`security/standard-authentication-and-password-management.md`](../security/standard-authentication-and-password-management.md), [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md), [`security/procedure-access-control.md`](../security/procedure-access-control.md), [`security/procedure-identity-management.md`](../security/procedure-identity-management.md) | Architectural recommendation |
| A.5.19 to A.5.22 Supplier relationships | [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`supply-chain/procedure-supplier-due-diligence.md`](../supply-chain/procedure-supplier-due-diligence.md), [`supply-chain/procedure-supplier-ongoing-monitoring.md`](../supply-chain/procedure-supplier-ongoing-monitoring.md), [`supply-chain/procedure-supplier-exit-and-data-return.md`](../supply-chain/procedure-supplier-exit-and-data-return.md) | Architectural recommendation |
| A.5.24 to A.5.28 Incident management lifecycle and evidence | [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`resilience/procedure-cross-domain-incident-coordination.md`](../resilience/procedure-cross-domain-incident-coordination.md), [`resilience/procedure-security-incident-reporting-and-escalation.md`](../resilience/procedure-security-incident-reporting-and-escalation.md), [`security/sop-incident-escalation-matrix.md`](../security/sop-incident-escalation-matrix.md) | Architectural recommendation |
| A.5.30 ICT readiness for business continuity | [`resilience/framework-business-continuity-and-resilience.md`](../resilience/framework-business-continuity-and-resilience.md), [`resilience/standard-business-continuity-and-disaster-recovery.md`](../resilience/standard-business-continuity-and-disaster-recovery.md), [`resilience/plan-it-disaster-recovery.md`](../resilience/plan-it-disaster-recovery.md) | Architectural recommendation |
| A.5.33 Protection of records | [`governance/standard-records-retention-and-destruction.md`](standard-records-retention-and-destruction.md), [`governance/register-data-retention-schedule.md`](register-data-retention-schedule.md) | Architectural recommendation |
| A.6.1 to A.6.5 Personnel security including screening, terms, awareness, disciplinary | [`security/standard-personnel-security-screening.md`](../security/standard-personnel-security-screening.md), [`security/standard-security-awareness-and-training.md`](../security/standard-security-awareness-and-training.md), [`security/procedure-onboarding-and-offboarding.md`](../security/procedure-onboarding-and-offboarding.md), [`security/procedure-security-disciplinary-process.md`](../security/procedure-security-disciplinary-process.md) | Architectural recommendation |
| A.6.2 Remote working and BYOD | [`security/standard-remote-working-security.md`](../security/standard-remote-working-security.md), [`security/policy-byod.md`](../security/policy-byod.md) | Architectural recommendation |
| A.7 Physical and environmental security | [`operations/standard-physical-security-of-it-infrastructure.md`](../operations/standard-physical-security-of-it-infrastructure.md) | Architectural recommendation |
| A.8.5 Secure authentication | [`security/standard-authentication-and-password-management.md`](../security/standard-authentication-and-password-management.md) | Architectural recommendation |
| A.8.6 Capacity management and production controls | [`operations/standard-production-security-requirements.md`](../operations/standard-production-security-requirements.md) | Architectural recommendation |
| A.8.8 Vulnerability management and patching | [`security/procedure-vulnerability-management.md`](../security/procedure-vulnerability-management.md), [`operations/procedure-patch-management.md`](../operations/procedure-patch-management.md) | Architectural recommendation |
| A.8.10 Information deletion and media handling | [`operations/procedure-media-handling-and-transport.md`](../operations/procedure-media-handling-and-transport.md) | Architectural recommendation |
| A.8.11 to A.8.12 Data masking and data leakage prevention | [`security/standard-data-loss-prevention.md`](../security/standard-data-loss-prevention.md) | Architectural recommendation |
| A.8.15 to A.8.16 Logging and monitoring | [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`operations/procedure-security-monitoring-and-alert-management.md`](../operations/procedure-security-monitoring-and-alert-management.md) | Architectural recommendation |
| A.8.20 to A.8.21 Network security and segmentation | [`security/policy-network-communications-security.md`](../security/policy-network-communications-security.md), [`operations/standard-network-security-and-segmentation.md`](../operations/standard-network-security-and-segmentation.md) | Architectural recommendation |
| A.8.24 Use of cryptography | [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md), [`security/framework-cryptographic-key-lifecycle.md`](../security/framework-cryptographic-key-lifecycle.md), [`security/procedure-cryptographic-key-operations.md`](../security/procedure-cryptographic-key-operations.md), [`security/roadmap-post-quantum-cryptography.md`](../security/roadmap-post-quantum-cryptography.md) | Architectural recommendation |
| A.8.25 to A.8.34 Secure development lifecycle and engineering | [`dev-security/policy-secure-development-and-engineering.md`](../dev-security/policy-secure-development-and-engineering.md), [`dev-security/standard-developer-security-requirements.md`](../dev-security/standard-developer-security-requirements.md), [`dev-security/standard-devops-security-requirements.md`](../dev-security/standard-devops-security-requirements.md), [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md), [`dev-security/standard-software-composition-analysis.md`](../dev-security/standard-software-composition-analysis.md), [`dev-security/standard-quality-assurance-and-testing.md`](../dev-security/standard-quality-assurance-and-testing.md) | Architectural recommendation |
| A.8.29 Security testing | [`security/standard-penetration-testing-and-red-team.md`](../security/standard-penetration-testing-and-red-team.md), [`dev-security/standard-quality-assurance-and-testing.md`](../dev-security/standard-quality-assurance-and-testing.md) | Architectural recommendation |

---

## ISO/IEC 42001:2023 (AI management systems)

| ISO 42001 clause area | Library documents | Alignment type |
| --- | --- | --- |
| Clause 5 Leadership and AI governance | [`ai/charter-ai-governance-council.md`](../ai/charter-ai-governance-council.md), [`ai/framework-ai-governance-and-risk.md`](../ai/framework-ai-governance-and-risk.md), [`ai/policy-ai-compliance.md`](../ai/policy-ai-compliance.md) | Architectural recommendation |
| Clause 6 Planning, AI risk and impact | [`ai/procedure-ai-system-impact-assessment.md`](../ai/procedure-ai-system-impact-assessment.md), [`ai/procedure-ai-model-risk-assessment.md`](../ai/procedure-ai-model-risk-assessment.md), [`ai/register-ai-risk.md`](../ai/register-ai-risk.md), [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md) | Architectural recommendation |
| Clause 8 Operation, AI lifecycle | [`ai/framework-ai-model-risk.md`](../ai/framework-ai-model-risk.md), [`ai/procedure-ai-model-lifecycle-management.md`](../ai/procedure-ai-model-lifecycle-management.md), [`ai/matrix-ai-model-risk-control-to-lifecycle-mapping.md`](../ai/matrix-ai-model-risk-control-to-lifecycle-mapping.md), [`ai/standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md) | Architectural recommendation |
| Clause 8.4 Documentation and transparency | [`ai/framework-ai-model-documentation-and-transparency.md`](../ai/framework-ai-model-documentation-and-transparency.md), [`ai/template-model-card.md`](../ai/template-model-card.md), [`ai/template-system-card.md`](../ai/template-system-card.md), [`ai/template-ai-system-register.md`](../ai/template-ai-system-register.md) | Architectural recommendation |
| Clause 9 Performance evaluation, audit, monitoring | [`ai/procedure-ai-audit.md`](../ai/procedure-ai-audit.md), [`ai/procedure-ai-evaluation.md`](../ai/procedure-ai-evaluation.md), [`ai/standard-ai-testing-validation-and-documentation.md`](../ai/standard-ai-testing-validation-and-documentation.md), [`ai/framework-ai-system-audit-certification.md`](../ai/framework-ai-system-audit-certification.md), [`ai/checklist-ai-algorithmic-compliance.md`](../ai/checklist-ai-algorithmic-compliance.md) | Architectural recommendation |
| AI security controls | [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md), [`ai/standard-ai-model-risk.md`](../ai/standard-ai-model-risk.md), [`ai/guide-ai-security-technical-implementation.md`](../ai/guide-ai-security-technical-implementation.md), [`ai/guide-ai-adversarial-test-reference.md`](../ai/guide-ai-adversarial-test-reference.md), [`ai/guideline-adversarial-evaluation-suite-development.md`](../ai/guideline-adversarial-evaluation-suite-development.md) | Architectural recommendation |

---

## NIST CSF 2.0

| CSF function and category | Library documents | Alignment type |
| --- | --- | --- |
| GOVERN GV.OC Organisational context | [`governance/charter-governance-library.md`](charter-governance-library.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md) | Architectural recommendation |
| GOVERN GV.RM Risk management strategy | [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md), [`risk/template-risk-appetite-statement.md`](../risk/template-risk-appetite-statement.md), [`risk/guideline-quantitative-risk-analysis.md`](../risk/guideline-quantitative-risk-analysis.md) | Architectural recommendation |
| GOVERN GV.RR Roles, responsibilities, authorities | [`governance/register-role-authority.md`](register-role-authority.md) | Evidence category |
| GOVERN GV.PO Policy | [`security/policy-information-security.md`](../security/policy-information-security.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md) | Architectural recommendation |
| GOVERN GV.SC Cybersecurity supply chain risk management | [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../supply-chain/framework-supplier-and-cloud-governance.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md) | Architectural recommendation |
| IDENTIFY ID.AM Asset management | [`operations/register-asset-inventory.md`](../operations/register-asset-inventory.md), [`ai/template-ai-system-register.md`](../ai/template-ai-system-register.md) | Evidence category |
| IDENTIFY ID.RA Risk assessment | [`risk/procedure-risk-assessment-methodology.md`](../risk/procedure-risk-assessment-methodology.md), [`risk/procedure-risk-register.md`](../risk/procedure-risk-register.md), [`risk/register-key-risk-indicators.md`](../risk/register-key-risk-indicators.md) | Architectural recommendation |
| PROTECT PR.AA Identity management and authentication | [`security/policy-identity-and-access-management.md`](../security/policy-identity-and-access-management.md), [`security/standard-authentication-and-password-management.md`](../security/standard-authentication-and-password-management.md), [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md) | Architectural recommendation |
| PROTECT PR.DS Data security | [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md), [`security/standard-data-loss-prevention.md`](../security/standard-data-loss-prevention.md), [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md) | Architectural recommendation |
| PROTECT PR.IR Information system integrity and resilience | [`operations/standard-production-security-requirements.md`](../operations/standard-production-security-requirements.md), [`operations/standard-cloud-security-configuration-baseline.md`](../operations/standard-cloud-security-configuration-baseline.md), [`operations/standard-network-security-and-segmentation.md`](../operations/standard-network-security-and-segmentation.md) | Architectural recommendation |
| DETECT DE.CM Continuous monitoring | [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`operations/procedure-security-monitoring-and-alert-management.md`](../operations/procedure-security-monitoring-and-alert-management.md), [`operations/procedure-threat-intelligence-and-siem-operations.md`](../operations/procedure-threat-intelligence-and-siem-operations.md) | Architectural recommendation |
| RESPOND RS.MA Incident management | [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`resilience/procedure-cross-domain-incident-coordination.md`](../resilience/procedure-cross-domain-incident-coordination.md) | Architectural recommendation |
| RESPOND RS.CO Incident communication | [`resilience/plan-crisis-communication.md`](../resilience/plan-crisis-communication.md), [`resilience/procedure-security-incident-reporting-and-escalation.md`](../resilience/procedure-security-incident-reporting-and-escalation.md) | Architectural recommendation |
| RECOVER RC.RP Recovery plan execution | [`resilience/plan-it-disaster-recovery.md`](../resilience/plan-it-disaster-recovery.md), [`resilience/procedure-backup-and-recovery.md`](../resilience/procedure-backup-and-recovery.md), [`resilience/procedure-continuity-and-recovery-testing.md`](../resilience/procedure-continuity-and-recovery-testing.md) | Architectural recommendation |

---

## NIST SP 800-53 Rev 5 (selected families)

| Control family | Library documents | Alignment type |
| --- | --- | --- |
| AC Access Control | [`security/policy-identity-and-access-management.md`](../security/policy-identity-and-access-management.md), [`security/procedure-access-control.md`](../security/procedure-access-control.md), [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md) | Architectural recommendation |
| AT Awareness and Training | [`security/standard-security-awareness-and-training.md`](../security/standard-security-awareness-and-training.md) | Architectural recommendation |
| AU Audit and Accountability | [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md) | Architectural recommendation |
| CA Assessment, Authorization, Monitoring | [`compliance/procedure-control-testing.md`](../compliance/procedure-control-testing.md), [`compliance/standard-internal-audit.md`](../compliance/standard-internal-audit.md), [`security/policy-acceptance-into-service.md`](../security/policy-acceptance-into-service.md) | Architectural recommendation |
| CM Configuration Management | [`operations/procedure-change-management-and-configuration-control.md`](../operations/procedure-change-management-and-configuration-control.md), [`operations/standard-production-security-requirements.md`](../operations/standard-production-security-requirements.md) | Architectural recommendation |
| CP Contingency Planning | [`resilience/framework-business-continuity-and-resilience.md`](../resilience/framework-business-continuity-and-resilience.md), [`resilience/policy-business-continuity-and-disaster-recovery.md`](../resilience/policy-business-continuity-and-disaster-recovery.md), [`resilience/standard-business-continuity-and-disaster-recovery.md`](../resilience/standard-business-continuity-and-disaster-recovery.md) | Architectural recommendation |
| IA Identification and Authentication | [`security/standard-authentication-and-password-management.md`](../security/standard-authentication-and-password-management.md), [`security/procedure-identity-management.md`](../security/procedure-identity-management.md) | Architectural recommendation |
| IR Incident Response | [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`security/sop-incident-escalation-matrix.md`](../security/sop-incident-escalation-matrix.md) | Architectural recommendation |
| MA Maintenance | [`operations/procedure-patch-management.md`](../operations/procedure-patch-management.md) | Architectural recommendation |
| MP Media Protection | [`operations/procedure-media-handling-and-transport.md`](../operations/procedure-media-handling-and-transport.md) | Architectural recommendation |
| PE Physical and Environmental Protection | [`operations/standard-physical-security-of-it-infrastructure.md`](../operations/standard-physical-security-of-it-infrastructure.md) | Architectural recommendation |
| PS Personnel Security | [`security/standard-personnel-security-screening.md`](../security/standard-personnel-security-screening.md), [`security/procedure-onboarding-and-offboarding.md`](../security/procedure-onboarding-and-offboarding.md), [`security/procedure-security-disciplinary-process.md`](../security/procedure-security-disciplinary-process.md) | Architectural recommendation |
| RA Risk Assessment | [`risk/procedure-risk-assessment-methodology.md`](../risk/procedure-risk-assessment-methodology.md), [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md) | Architectural recommendation |
| SA System and Services Acquisition | [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md), [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md), [`security/policy-acceptance-into-service.md`](../security/policy-acceptance-into-service.md) | Architectural recommendation |
| SC System and Communications Protection | [`security/policy-network-communications-security.md`](../security/policy-network-communications-security.md), [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md) | Architectural recommendation |
| SI System and Information Integrity | [`security/procedure-vulnerability-management.md`](../security/procedure-vulnerability-management.md), [`operations/procedure-patch-management.md`](../operations/procedure-patch-management.md), [`security/standard-data-loss-prevention.md`](../security/standard-data-loss-prevention.md) | Architectural recommendation |
| SR Supply Chain Risk Management | [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`dev-security/standard-software-composition-analysis.md`](../dev-security/standard-software-composition-analysis.md) | Architectural recommendation |

---

## NIST AI RMF (Govern, Map, Measure, Manage)

| AI RMF function | Library documents | Alignment type |
| --- | --- | --- |
| GOVERN | [`ai/charter-ai-governance-council.md`](../ai/charter-ai-governance-council.md), [`ai/framework-ai-governance-and-risk.md`](../ai/framework-ai-governance-and-risk.md), [`ai/policy-ai-compliance.md`](../ai/policy-ai-compliance.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md) | Architectural recommendation |
| MAP | [`ai/procedure-ai-system-impact-assessment.md`](../ai/procedure-ai-system-impact-assessment.md), [`ai/template-ai-system-register.md`](../ai/template-ai-system-register.md), [`ai/register-ai-risk.md`](../ai/register-ai-risk.md), [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md) | Architectural recommendation |
| MEASURE | [`ai/procedure-ai-model-risk-assessment.md`](../ai/procedure-ai-model-risk-assessment.md), [`ai/procedure-ai-evaluation.md`](../ai/procedure-ai-evaluation.md), [`ai/standard-ai-testing-validation-and-documentation.md`](../ai/standard-ai-testing-validation-and-documentation.md), [`ai/guideline-adversarial-evaluation-suite-development.md`](../ai/guideline-adversarial-evaluation-suite-development.md), [`ai/guide-ai-adversarial-test-reference.md`](../ai/guide-ai-adversarial-test-reference.md) | Architectural recommendation |
| MANAGE | [`ai/standard-ai-model-risk.md`](../ai/standard-ai-model-risk.md), [`ai/framework-ai-model-risk.md`](../ai/framework-ai-model-risk.md), [`ai/procedure-ai-model-lifecycle-management.md`](../ai/procedure-ai-model-lifecycle-management.md), [`ai/procedure-ai-audit.md`](../ai/procedure-ai-audit.md), [`ai/matrix-ai-model-risk-control-to-lifecycle-mapping.md`](../ai/matrix-ai-model-risk-control-to-lifecycle-mapping.md) | Architectural recommendation |

---

## CSA CCM v4.1 (selected domains)

| CCM domain | Library documents | Alignment type |
| --- | --- | --- |
| AIS Application and Interface Security | [`dev-security/standard-developer-security-requirements.md`](../dev-security/standard-developer-security-requirements.md), [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md), [`security/policy-acceptance-into-service.md`](../security/policy-acceptance-into-service.md) | Architectural recommendation |
| BCR Business Continuity Management and Operational Resilience | [`resilience/framework-business-continuity-and-resilience.md`](../resilience/framework-business-continuity-and-resilience.md), [`resilience/standard-business-continuity-and-disaster-recovery.md`](../resilience/standard-business-continuity-and-disaster-recovery.md), [`resilience/plan-it-disaster-recovery.md`](../resilience/plan-it-disaster-recovery.md) | Architectural recommendation |
| DSP Data Security and Privacy Lifecycle Management | [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md), [`security/standard-data-loss-prevention.md`](../security/standard-data-loss-prevention.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`operations/procedure-media-handling-and-transport.md`](../operations/procedure-media-handling-and-transport.md) | Architectural recommendation |
| EKM Encryption and Key Management | [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md), [`security/framework-cryptographic-key-lifecycle.md`](../security/framework-cryptographic-key-lifecycle.md), [`security/procedure-cryptographic-key-operations.md`](../security/procedure-cryptographic-key-operations.md) | Architectural recommendation |
| GOV Governance, Risk Management, Compliance | [`governance/charter-governance-library.md`](charter-governance-library.md), [`governance/framework-document-architecture-and-interrelationship.md`](framework-document-architecture-and-interrelationship.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md) | Architectural recommendation |
| HRS Human Resources Security | [`security/standard-personnel-security-screening.md`](../security/standard-personnel-security-screening.md), [`security/standard-security-awareness-and-training.md`](../security/standard-security-awareness-and-training.md), [`security/procedure-onboarding-and-offboarding.md`](../security/procedure-onboarding-and-offboarding.md) | Architectural recommendation |
| IAM Identity and Access Management | [`security/policy-identity-and-access-management.md`](../security/policy-identity-and-access-management.md), [`security/standard-privileged-access-management.md`](../security/standard-privileged-access-management.md), [`security/standard-authentication-and-password-management.md`](../security/standard-authentication-and-password-management.md) | Architectural recommendation |
| IPY Interoperability and Portability | [`supply-chain/standard-cloud-exit-and-data-portability.md`](../supply-chain/standard-cloud-exit-and-data-portability.md) | Architectural recommendation |
| IVS Infrastructure and Virtualization Security | [`operations/standard-network-security-and-segmentation.md`](../operations/standard-network-security-and-segmentation.md), [`operations/standard-cloud-security-configuration-baseline.md`](../operations/standard-cloud-security-configuration-baseline.md) | Architectural recommendation |
| LOG Logging and Monitoring | [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`operations/procedure-security-monitoring-and-alert-management.md`](../operations/procedure-security-monitoring-and-alert-management.md) | Architectural recommendation |
| SEF Security Incident Management, Forensics | [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`resilience/procedure-cross-domain-incident-coordination.md`](../resilience/procedure-cross-domain-incident-coordination.md) | Architectural recommendation |
| STA Supply Chain Management, Transparency, Accountability | [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../supply-chain/framework-supplier-and-cloud-governance.md), [`supply-chain/procedure-supplier-due-diligence.md`](../supply-chain/procedure-supplier-due-diligence.md), [`supply-chain/procedure-supplier-ongoing-monitoring.md`](../supply-chain/procedure-supplier-ongoing-monitoring.md), [`supply-chain/procedure-supplier-exit-and-data-return.md`](../supply-chain/procedure-supplier-exit-and-data-return.md) | Architectural recommendation |
| TVM Threat and Vulnerability Management | [`security/procedure-vulnerability-management.md`](../security/procedure-vulnerability-management.md), [`operations/procedure-patch-management.md`](../operations/procedure-patch-management.md), [`operations/procedure-threat-intelligence-and-siem-operations.md`](../operations/procedure-threat-intelligence-and-siem-operations.md) | Architectural recommendation |
| UEM Universal Endpoint Management | [`operations/procedure-endpoint-management-and-device-compliance.md`](../operations/procedure-endpoint-management-and-device-compliance.md), [`security/policy-byod.md`](../security/policy-byod.md) | Architectural recommendation |

---

## EU AI Act

| Article or topic | Library documents | Alignment type |
| --- | --- | --- |
| Article 5 Prohibited AI practices | [`ai/policy-ai-compliance.md`](../ai/policy-ai-compliance.md), [`ai/guideline-ethical-ai-use.md`](../ai/guideline-ethical-ai-use.md) | Regulatory interpretation |
| Article 9 Risk management system for high-risk AI | [`ai/framework-ai-governance-and-risk.md`](../ai/framework-ai-governance-and-risk.md), [`ai/procedure-ai-model-risk-assessment.md`](../ai/procedure-ai-model-risk-assessment.md), [`ai/procedure-ai-system-impact-assessment.md`](../ai/procedure-ai-system-impact-assessment.md), [`ai/register-ai-risk.md`](../ai/register-ai-risk.md), [`risk/annex-ai-risk-methodology.md`](../risk/annex-ai-risk-methodology.md) | Regulatory interpretation |
| Article 10 Data and data governance | [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md), [`ai/template-ai-system-register.md`](../ai/template-ai-system-register.md) | Regulatory interpretation |
| Article 11 Technical documentation; Annex IV | [`ai/framework-ai-model-documentation-and-transparency.md`](../ai/framework-ai-model-documentation-and-transparency.md), [`ai/template-model-card.md`](../ai/template-model-card.md), [`ai/template-system-card.md`](../ai/template-system-card.md), [`ai/standard-ai-testing-validation-and-documentation.md`](../ai/standard-ai-testing-validation-and-documentation.md) | Regulatory interpretation |
| Article 12 Record-keeping | [`ai/template-ai-system-register.md`](../ai/template-ai-system-register.md), [`governance/standard-records-retention-and-destruction.md`](standard-records-retention-and-destruction.md) | Regulatory interpretation |
| Article 14 Human oversight | [`ai/guideline-ethical-ai-use.md`](../ai/guideline-ethical-ai-use.md), [`ai/framework-ai-governance-and-risk.md`](../ai/framework-ai-governance-and-risk.md) | Regulatory interpretation |
| Article 15 Accuracy, robustness, cybersecurity | [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md), [`ai/standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md), [`ai/guide-ai-adversarial-test-reference.md`](../ai/guide-ai-adversarial-test-reference.md), [`ai/guide-ai-security-technical-implementation.md`](../ai/guide-ai-security-technical-implementation.md) | Regulatory interpretation |
| Article 17 Quality management system | [`ai/framework-ai-system-audit-certification.md`](../ai/framework-ai-system-audit-certification.md), [`ai/procedure-ai-audit.md`](../ai/procedure-ai-audit.md) | Regulatory interpretation |
| Article 26 Obligations of deployers | [`supply-chain/procedure-third-party-ai-due-diligence.md`](../supply-chain/procedure-third-party-ai-due-diligence.md), [`ai/policy-ai-compliance.md`](../ai/policy-ai-compliance.md) | Regulatory interpretation |
| Article 43 Conformity assessment | [`ai/framework-ai-system-audit-certification.md`](../ai/framework-ai-system-audit-certification.md), [`ai/checklist-ai-algorithmic-compliance.md`](../ai/checklist-ai-algorithmic-compliance.md) | Regulatory interpretation |
| Article 50 Transparency obligations | [`ai/framework-ai-model-documentation-and-transparency.md`](../ai/framework-ai-model-documentation-and-transparency.md), [`governance/guideline-esg-and-ai-ethics-disclosure.md`](guideline-esg-and-ai-ethics-disclosure.md) | Regulatory interpretation |

---

## GDPR (and UK GDPR by analogue)

| Article | Library documents | Alignment type |
| --- | --- | --- |
| Article 5 Principles of processing | [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`governance/register-data-retention-schedule.md`](register-data-retention-schedule.md) | Legal obligation |
| Article 17 Right to erasure | [`privacy/procedure-data-subject-rights-management.md`](../privacy/procedure-data-subject-rights-management.md), [`governance/standard-records-retention-and-destruction.md`](standard-records-retention-and-destruction.md), [`governance/register-data-retention-schedule.md`](register-data-retention-schedule.md) | Legal obligation |
| Articles 15 to 22 Data subject rights | [`privacy/procedure-data-subject-rights-management.md`](../privacy/procedure-data-subject-rights-management.md) | Legal obligation |
| Article 25 Data protection by design and by default | [`privacy/charter-privacy-management-programme.md`](../privacy/charter-privacy-management-programme.md), [`privacy/policy-privacy-and-data-governance.md`](../privacy/policy-privacy-and-data-governance.md), [`dev-security/policy-secure-development-and-engineering.md`](../dev-security/policy-secure-development-and-engineering.md) | Legal obligation |
| Article 28 Processor obligations | [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md), [`supply-chain/register-subprocessor-template.md`](../supply-chain/register-subprocessor-template.md), [`supply-chain/procedure-supplier-exit-and-data-return.md`](../supply-chain/procedure-supplier-exit-and-data-return.md) | Legal obligation |
| Article 30 Records of processing activities | [`privacy/charter-privacy-management-programme.md`](../privacy/charter-privacy-management-programme.md) | Legal obligation |
| Article 32 Security of processing | [`security/policy-information-security.md`](../security/policy-information-security.md), [`security/standard-data-classification-and-handling.md`](../security/standard-data-classification-and-handling.md), [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md) | Legal obligation |
| Articles 33 to 34 Breach notification | [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md), [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) | Legal obligation |
| Article 35 Data protection impact assessment | [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../privacy/procedure-privacy-impact-and-cross-border-transfer.md) | Legal obligation |
| Chapter V Cross-border transfers | [`privacy/procedure-privacy-impact-and-cross-border-transfer.md`](../privacy/procedure-privacy-impact-and-cross-border-transfer.md), [`privacy/register-cross-border-data-flow.md`](../privacy/register-cross-border-data-flow.md), [`privacy/annex-privacy-jurisdiction-index.md`](../privacy/annex-privacy-jurisdiction-index.md) | Legal obligation |

---

## DORA (Digital Operational Resilience Act)

| Pillar | Library documents | Alignment type |
| --- | --- | --- |
| Pillar 1 ICT risk management | [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`operations/framework-it-service-management.md`](../operations/framework-it-service-management.md), [`security/policy-information-security.md`](../security/policy-information-security.md) | Regulatory interpretation |
| Pillar 2 ICT-related incident reporting | [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`resilience/procedure-security-incident-reporting-and-escalation.md`](../resilience/procedure-security-incident-reporting-and-escalation.md), [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) | Regulatory interpretation |
| Pillar 3 Digital operational resilience testing | [`resilience/procedure-continuity-and-recovery-testing.md`](../resilience/procedure-continuity-and-recovery-testing.md), [`security/standard-penetration-testing-and-red-team.md`](../security/standard-penetration-testing-and-red-team.md), [`resilience/register-resilience-metrics-and-testing-log.md`](../resilience/register-resilience-metrics-and-testing-log.md) | Regulatory interpretation |
| Pillar 4 ICT third-party risk | [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md), [`supply-chain/procedure-supplier-due-diligence.md`](../supply-chain/procedure-supplier-due-diligence.md), [`supply-chain/procedure-supplier-ongoing-monitoring.md`](../supply-chain/procedure-supplier-ongoing-monitoring.md), [`supply-chain/procedure-supplier-exit-and-data-return.md`](../supply-chain/procedure-supplier-exit-and-data-return.md), [`supply-chain/standard-cloud-exit-and-data-portability.md`](../supply-chain/standard-cloud-exit-and-data-portability.md) | Regulatory interpretation |
| Pillar 5 Information and intelligence sharing | [`operations/procedure-threat-intelligence-and-siem-operations.md`](../operations/procedure-threat-intelligence-and-siem-operations.md) | Regulatory interpretation |

---

## NIS 2 Directive

| Article area | Library documents | Alignment type |
| --- | --- | --- |
| Article 21 Cybersecurity risk management measures | [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md), [`security/policy-information-security.md`](../security/policy-information-security.md), [`operations/framework-it-service-management.md`](../operations/framework-it-service-management.md) | Regulatory interpretation |
| Article 21.2(a) Policies on risk analysis and information system security | [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md), [`security/policy-information-security.md`](../security/policy-information-security.md) | Regulatory interpretation |
| Article 21.2(b) Incident handling | [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) | Regulatory interpretation |
| Article 21.2(c) Business continuity, backup, crisis management | [`resilience/framework-business-continuity-and-resilience.md`](../resilience/framework-business-continuity-and-resilience.md), [`resilience/procedure-backup-and-recovery.md`](../resilience/procedure-backup-and-recovery.md), [`resilience/plan-business-continuity-and-crisis-management.md`](../resilience/plan-business-continuity-and-crisis-management.md) | Regulatory interpretation |
| Article 21.2(d) Supply chain security | [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../supply-chain/framework-supplier-and-cloud-governance.md) | Regulatory interpretation |
| Article 21.2(e) Security in network and information systems acquisition, development, maintenance | [`dev-security/policy-secure-development-and-engineering.md`](../dev-security/policy-secure-development-and-engineering.md), [`security/policy-acceptance-into-service.md`](../security/policy-acceptance-into-service.md) | Regulatory interpretation |
| Article 21.2(f) Policies and procedures to assess effectiveness | [`compliance/procedure-control-testing.md`](../compliance/procedure-control-testing.md), [`compliance/standard-internal-audit.md`](../compliance/standard-internal-audit.md) | Regulatory interpretation |
| Article 21.2(g) Basic cyber hygiene practices and training | [`security/standard-security-awareness-and-training.md`](../security/standard-security-awareness-and-training.md) | Regulatory interpretation |
| Article 21.2(h) Cryptography and encryption | [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md), [`security/framework-cryptographic-key-lifecycle.md`](../security/framework-cryptographic-key-lifecycle.md) | Regulatory interpretation |
| Article 21.2(i) Human resources security, access control, asset management | [`security/standard-personnel-security-screening.md`](../security/standard-personnel-security-screening.md), [`security/policy-identity-and-access-management.md`](../security/policy-identity-and-access-management.md), [`operations/register-asset-inventory.md`](../operations/register-asset-inventory.md) | Regulatory interpretation |
| Article 21.2(j) Multi-factor authentication, secured communications | [`security/standard-authentication-and-password-management.md`](../security/standard-authentication-and-password-management.md), [`security/policy-network-communications-security.md`](../security/policy-network-communications-security.md) | Regulatory interpretation |
| Articles 23 to 25 Incident reporting | [`resilience/procedure-security-incident-reporting-and-escalation.md`](../resilience/procedure-security-incident-reporting-and-escalation.md), [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) | Regulatory interpretation |

---

## OWASP LLM Top 10 (2025) and MITRE ATLAS

| Threat area | Library documents | Alignment type |
| --- | --- | --- |
| LLM01 Prompt injection (direct and indirect) | [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md), [`ai/standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md), [`ai/guide-ai-adversarial-test-reference.md`](../ai/guide-ai-adversarial-test-reference.md), [`ai/guide-ai-security-technical-implementation.md`](../ai/guide-ai-security-technical-implementation.md) | Architectural recommendation |
| LLM02 Sensitive information disclosure | [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md), [`privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md), [`security/standard-data-loss-prevention.md`](../security/standard-data-loss-prevention.md) | Architectural recommendation |
| LLM03 Supply chain (model and component provenance) | [`supply-chain/procedure-third-party-ai-due-diligence.md`](../supply-chain/procedure-third-party-ai-due-diligence.md), [`dev-security/standard-software-composition-analysis.md`](../dev-security/standard-software-composition-analysis.md) | Architectural recommendation |
| LLM04 Data and model poisoning | [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md), [`ai/standard-ai-model-risk.md`](../ai/standard-ai-model-risk.md), [`ai/procedure-ai-model-risk-assessment.md`](../ai/procedure-ai-model-risk-assessment.md) | Architectural recommendation |
| LLM05 Improper output handling | [`ai/guide-ai-security-technical-implementation.md`](../ai/guide-ai-security-technical-implementation.md), [`dev-security/standard-developer-security-requirements.md`](../dev-security/standard-developer-security-requirements.md) | Architectural recommendation |
| LLM06 Excessive agency in agentic systems | [`ai/standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md), [`ai/guide-ai-security-technical-implementation.md`](../ai/guide-ai-security-technical-implementation.md) | Architectural recommendation |
| LLM07 System prompt leakage | [`ai/guide-ai-adversarial-test-reference.md`](../ai/guide-ai-adversarial-test-reference.md), [`ai/guide-ai-security-technical-implementation.md`](../ai/guide-ai-security-technical-implementation.md) | Architectural recommendation |
| LLM08 Vector and embedding weaknesses | [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md), [`ai/guide-ai-security-technical-implementation.md`](../ai/guide-ai-security-technical-implementation.md) | Architectural recommendation |
| LLM09 Misinformation and hallucination | [`ai/guideline-ethical-ai-use.md`](../ai/guideline-ethical-ai-use.md), [`ai/procedure-ai-evaluation.md`](../ai/procedure-ai-evaluation.md), [`ai/standard-ai-testing-validation-and-documentation.md`](../ai/standard-ai-testing-validation-and-documentation.md) | Architectural recommendation |
| LLM10 Unbounded consumption | [`ai/standard-ai-and-agentic-development-security.md`](../ai/standard-ai-and-agentic-development-security.md), [`ai/guide-ai-security-technical-implementation.md`](../ai/guide-ai-security-technical-implementation.md) | Architectural recommendation |
| MITRE ATLAS tactics (adversarial ML) | [`ai/standard-ai-security-and-risk.md`](../ai/standard-ai-security-and-risk.md), [`ai/guide-ai-adversarial-test-reference.md`](../ai/guide-ai-adversarial-test-reference.md), [`ai/guideline-adversarial-evaluation-suite-development.md`](../ai/guideline-adversarial-evaluation-suite-development.md) | Architectural recommendation |

---

## CTPAT MSC and BASC v6 (trade and supply-chain security)

| CTPAT MSC domain | Library documents | Alignment type |
| --- | --- | --- |
| Corporate security and security training | [`compliance/logistics/policy-basc-information-security.md`](../compliance/logistics/policy-basc-information-security.md), [`compliance/logistics/register-basc-it-responsibilities.md`](../compliance/logistics/register-basc-it-responsibilities.md), [`security/standard-security-awareness-and-training.md`](../security/standard-security-awareness-and-training.md) | Contractual requirement |
| Personnel security | [`security/standard-personnel-security-screening.md`](../security/standard-personnel-security-screening.md) | Contractual requirement |
| Physical security and physical access controls | [`operations/standard-physical-security-of-it-infrastructure.md`](../operations/standard-physical-security-of-it-infrastructure.md) | Contractual requirement |
| Procedural and cargo security | [`compliance/logistics/register-ctpat-united-states-msc-controls.md`](../compliance/logistics/register-ctpat-united-states-msc-controls.md), [`supply-chain/annex-trade-and-supply-chain-continuity-controls.md`](../supply-chain/annex-trade-and-supply-chain-continuity-controls.md) | Contractual requirement |
| Business partner security | [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md), [`supply-chain/template-supplier-security-questionnaire.md`](../supply-chain/template-supplier-security-questionnaire.md), [`supply-chain/procedure-supplier-due-diligence.md`](../supply-chain/procedure-supplier-due-diligence.md) | Contractual requirement |
| Information technology security | [`compliance/logistics/register-ctpat-united-states-it-controls.md`](../compliance/logistics/register-ctpat-united-states-it-controls.md), [`compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md`](../compliance/logistics/annex-aeo-united-kingdom-cybersecurity.md), [`security/policy-information-security.md`](../security/policy-information-security.md), [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md) | Contractual requirement |
| Compliance with associated programmes (PIP, AEO, AEO-S, NEEC, OEA, WCO SAFE) | [`supply-chain/matrix-supply-chain-security-programme-alignment.md`](../supply-chain/matrix-supply-chain-security-programme-alignment.md), [`compliance/logistics/register-pip-canada-controls.md`](../compliance/logistics/register-pip-canada-controls.md), [`compliance/logistics/procedure-aeo-united-kingdom-self-assessment.md`](../compliance/logistics/procedure-aeo-united-kingdom-self-assessment.md) | Contractual requirement |

---

## How to extend this matrix

1. Add new framework or regulation as a new section heading at the appropriate level of granularity (article, clause, control family, or domain).
2. Cite library documents using markdown links in the canonical form, where the display text is the root-relative path and the target is relative to this file's directory.
3. State alignment type on each row: Legal obligation, Regulatory interpretation, Contractual requirement, Industry practice, Architectural recommendation, or Evidence category.
4. Bump the version of this matrix when a section is added or substantially revised.
5. Regenerate `taxonomy.yml` and ensure that the document index register references this matrix.

---

**End of Document**
