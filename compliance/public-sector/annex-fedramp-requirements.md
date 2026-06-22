# FedRAMP Sector Requirements Annex

**Document Title:** FedRAMP Sector Requirements Annex\
**Document Type:** Annex\
**Version:** 0.0.5\
**Date:** 2026-06-22\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/README.md`](README.md), [`compliance/policy-legal-and-regulatory-compliance.md`](../policy-legal-and-regulatory-compliance.md), [`compliance/register-global-regulatory-applicability.md`](../register-global-regulatory-applicability.md), [`compliance/matrix-grc-compliance-alignment.md`](../matrix-grc-compliance-alignment.md), [`security/policy-information-security.md`](../../security/policy-information-security.md), [`operations/standard-cloud-security-configuration-baseline.md`](../../operations/standard-cloud-security-configuration-baseline.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../../supply-chain/standard-supplier-security-and-privacy-assurance.md)\
**Classification:** Public\
**Category:** Compliance: Sector-Specific\
**Review Frequency:** Annual and upon material FedRAMP baseline, OMB guidance, or authorisation status change\
**Repository Path:** [`compliance/public-sector/annex-fedramp-requirements.md`](annex-fedramp-requirements.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex describes how a cloud service provider seeking US Federal Risk and Authorization Management Program (FedRAMP) authorisation can use the core GRC library to demonstrate the control set, evidence, and operating expectations FedRAMP requires. The annex maps the library to FedRAMP baselines, identifies applicability triggers, describes the authorisation routes, and lists the supplementary documentation FedRAMP requires beyond the library's baseline.

This annex does not reproduce FedRAMP control text, the FedRAMP Tailored guidance, or the assessment documentation templates. Adopting organisations consume those from the official FedRAMP source.

---

## Applicability triggers

The library is relevant to FedRAMP where the organisation:

1. Sells or intends to sell a cloud service offering to a US federal agency.
2. Operates as a cloud service provider for a federal contractor whose contract requires FedRAMP authorisation flow-down.
3. Operates as a third-party assessment organisation (3PAO) supporting authorisation packages.
4. Operates as a state, local, or tribal government provider whose buyer requires StateRAMP, TX-RAMP, or equivalent and relies on FedRAMP-equivalent controls.

The library is not relevant where the organisation has no federal customer in pipeline and no contractual flow-down requirement.

---

## Authorisation route selection

| Route | When to choose | Effort |
| --- | --- | --- |
| Joint Authorization Board (JAB) Provisional ATO (P-ATO) | High-impact services with broad agency demand; CSP can sustain continuous JAB engagement | Highest; finite annual slots |
| Agency Authorization (A-ATO) | Specific agency sponsor identified; faster than JAB; package later submitted for agency-to-agency reuse | High |
| FedRAMP Tailored | SaaS with limited impact and well-defined data scope (Low or Moderate); reduced control set | Lower |
| FedRAMP Ready | Pre-authorisation marketplace listing; demonstrates a 3PAO-assessed control posture without an agency sponsor | Medium |

---

## Baseline selection

FedRAMP baselines map to FIPS 199 system categorisation. Adopting organisations confirm the categorisation with their agency sponsor before selecting a baseline.

| Baseline | Use case | Control count (approximate) |
| --- | --- | --- |
| FedRAMP Low | Public-facing services with no confidentiality, integrity, or availability impact above Low | About 125 controls |
| FedRAMP Moderate | Most federal use cases involving controlled unclassified information (CUI) | About 325 controls |
| FedRAMP High | Mission-critical federal use cases including law enforcement, emergency services, financial systems | About 425 controls |
| FedRAMP Tailored Low (LI-SaaS) | SaaS only, limited data scope | About 40 controls plus the FedRAMP Tailored Authorization Process |

---

## Library coverage and gaps

The library provides architectural baselines that align with FedRAMP control families. Adopting organisations must implement and evidence the controls per the selected baseline; the library is not a substitute for the authorisation package.

| FedRAMP control family | Library coverage |
| --- | --- |
| AC Access Control | [`security/policy-identity-and-access-management.md`](../../security/policy-identity-and-access-management.md), [`security/procedure-access-control.md`](../../security/procedure-access-control.md), [`security/standard-privileged-access-management.md`](../../security/standard-privileged-access-management.md) |
| AT Awareness and Training | [`security/standard-security-awareness-and-training.md`](../../security/standard-security-awareness-and-training.md) |
| AU Audit and Accountability | [`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md), [`operations/procedure-security-monitoring-and-alert-management.md`](../../operations/procedure-security-monitoring-and-alert-management.md) |
| CA Assessment, Authorization, and Monitoring | [`compliance/procedure-control-testing.md`](../procedure-control-testing.md), [`compliance/standard-internal-audit.md`](../standard-internal-audit.md), [`security/policy-acceptance-into-service.md`](../../security/policy-acceptance-into-service.md) |
| CM Configuration Management | [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md), [`operations/standard-production-security-requirements.md`](../../operations/standard-production-security-requirements.md) |
| CP Contingency Planning | [`resilience/framework-business-continuity-and-resilience.md`](../../resilience/framework-business-continuity-and-resilience.md), [`resilience/standard-business-continuity-and-disaster-recovery.md`](../../resilience/standard-business-continuity-and-disaster-recovery.md), [`resilience/plan-it-disaster-recovery.md`](../../resilience/plan-it-disaster-recovery.md) |
| IA Identification and Authentication | [`security/standard-authentication-and-password-management.md`](../../security/standard-authentication-and-password-management.md), [`security/procedure-identity-management.md`](../../security/procedure-identity-management.md) |
| IR Incident Response | [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md), [`resilience/procedure-cross-domain-incident-coordination.md`](../../resilience/procedure-cross-domain-incident-coordination.md) |
| MA Maintenance | [`operations/procedure-patch-management.md`](../../operations/procedure-patch-management.md) |
| MP Media Protection | [`operations/procedure-media-handling-and-transport.md`](../../operations/procedure-media-handling-and-transport.md) |
| PE Physical and Environmental Protection | [`operations/standard-physical-security-of-it-infrastructure.md`](../../operations/standard-physical-security-of-it-infrastructure.md) |
| PS Personnel Security | [`security/standard-personnel-security-screening.md`](../../security/standard-personnel-security-screening.md), [`security/procedure-onboarding-and-offboarding.md`](../../security/procedure-onboarding-and-offboarding.md) |
| RA Risk Assessment | [`risk/procedure-risk-assessment-methodology.md`](../../risk/procedure-risk-assessment-methodology.md), [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md) |
| SA System and Services Acquisition | [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../../supply-chain/standard-supplier-security-and-privacy-assurance.md), [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](../../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md), [`security/policy-acceptance-into-service.md`](../../security/policy-acceptance-into-service.md) |
| SC System and Communications Protection | [`security/policy-network-communications-security.md`](../../security/policy-network-communications-security.md), [`security/policy-encryption-and-key-management.md`](../../security/policy-encryption-and-key-management.md) |
| SI System and Information Integrity | [`security/procedure-vulnerability-management.md`](../../security/procedure-vulnerability-management.md), [`operations/procedure-patch-management.md`](../../operations/procedure-patch-management.md), [`security/standard-data-loss-prevention.md`](../../security/standard-data-loss-prevention.md) |
| SR Supply Chain Risk Management | [`risk/standard-third-party-and-supply-chain-risk.md`](../../risk/standard-third-party-and-supply-chain-risk.md), [`dev-security/standard-software-composition-analysis.md`](../../dev-security/standard-software-composition-analysis.md) |

Library gaps requiring additional documentation for a FedRAMP authorisation package:

1. **System Security Plan (SSP).** FedRAMP requires an SSP using the FedRAMP template. The library provides architectural inputs; the SSP itself is a per-system artefact built outside the library.
2. **Continuous Monitoring (ConMon) plan and monthly reporting.** FedRAMP requires monthly POA&M, vulnerability scan submission, and inventory updates.
3. **Plan of Action and Milestones (POA&M) register.** Tracked per FedRAMP cadence; library risk register is the conceptual basis but FedRAMP format is mandated.
4. **3PAO Security Assessment Report (SAR) and Security Assessment Plan (SAP).** Produced by the assessor using FedRAMP templates.
5. **Incident Response Reporting per OMB M-22-09 and US-CERT timelines.** Library incident procedures cover lifecycle; FedRAMP-specific reporting timelines are layered on top.
6. **FIPS-validated cryptography.** Library cryptographic key lifecycle framework establishes the practice; FedRAMP additionally requires FIPS 140-3 (or 140-2 in transition) validated modules.
7. **Personnel investigations under federal standards.** US federal background investigation standards beyond the library's screening standard.
8. **CUI handling under NIST SP 800-171 and 800-172.** Where the service handles CUI.

---

## Operating expectations

1. Each control implementation in the SSP references the relevant library artefact and any organisation-specific extension.
2. ConMon submissions follow the FedRAMP-published cadence and template; the library's metrics and audit registers feed but do not replace the ConMon submission.
3. Significant change requests follow the FedRAMP significant change process; the library's change management procedure is the operational input.
4. Annual assessment by a 3PAO is scheduled; the assessment-evidence repository is structured around FedRAMP test cases, not library structure.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| FedRAMP Baseline (Low, Moderate, High) | NIST SP 800-53 Rev. 5 + FedRAMP parameters | Primary control set |
| FedRAMP Tailored | LI-SaaS Authorization Process | Tailored route |
| NIST SP 800-53 Rev. 5 | Security and Privacy Controls | Underlying control catalogue |
| NIST SP 800-37 Rev. 2 | Risk Management Framework | Authorisation lifecycle |
| NIST SP 800-171 / 800-172 | Protecting CUI | Where applicable |
| OMB M-22-09 | Federal Zero Trust Strategy | Architectural direction |
| FIPS 199 | Standards for Security Categorization | Categorisation prerequisite |
| FIPS 200 | Minimum Security Requirements | Baseline prerequisite |
| FIPS 140-3 / 140-2 | Cryptographic Module Validation | FIPS-validated cryptography |

---

## Limitations

This annex is a CC BY-SA 4.0 navigation aid. FedRAMP authorisation requires the FedRAMP-mandated artefacts, a federal sponsor or marketplace listing, and engagement with a 3PAO; this library does not produce authorisation by itself. Adopting organisations consult the official FedRAMP programme documentation and engage a 3PAO before commencing authorisation work. This annex is not a substitute for FedRAMP programme guidance.

---

**End of Document**
