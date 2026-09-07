# FedRAMP Sector Requirements Annex

**Document Title:** FedRAMP Sector Requirements Annex\
**Document Type:** Annex\
**Version:** 0.0.10\
**Date:** 2026-09-07\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/README.md`](../README.md), [`compliance/policy-legal-and-regulatory-compliance.md`](../policy-legal-and-regulatory-compliance.md), [`compliance/register-global-regulatory-applicability.md`](../register-global-regulatory-applicability.md), [`compliance/matrix-grc-compliance-alignment.md`](../matrix-grc-compliance-alignment.md), [`security/policy-information-security.md`](../../security/policy-information-security.md), [`operations/standard-cloud-security-configuration-baseline.md`](../../operations/standard-cloud-security-configuration-baseline.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../../supply-chain/standard-supplier-security-and-privacy-assurance.md)\
**Classification:** Public\
**Category:** Compliance: Sector-Specific\
**Review Frequency:** Annual and upon material FedRAMP baseline, OMB guidance, or authorization status change\
**Repository Path:** [`compliance/public-sector/annex-fedramp-requirements.md`](annex-fedramp-requirements.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex describes how a cloud service provider seeking US Federal Risk and Authorization Management Program (FedRAMP) authorization can use the core GRC library to demonstrate the control set, evidence, and operating expectations FedRAMP requires. The annex maps the library to FedRAMP baselines, identifies applicability triggers, describes the authorization routes, and lists the supplementary documentation FedRAMP requires beyond the library's baseline.

This annex does not reproduce FedRAMP control text, the FedRAMP Tailored guidance, or the assessment documentation templates. Adopting organizations consume those from the official FedRAMP source.

---

## Applicability triggers

The library is relevant to FedRAMP where the organization:

1. Sells or intends to sell a cloud service offering to a US federal agency.
2. Operates as a cloud service provider for a federal contractor whose contract requires FedRAMP authorization flow-down.
3. Operates as a third-party assessment organization (3PAO) supporting authorization packages.
4. Operates as a state, local, or tribal government provider whose buyer requires StateRAMP, TX-RAMP, or equivalent and relies on FedRAMP-equivalent controls.

The library is not relevant where the organization has no federal customer in pipeline and no contractual flow-down requirement.

---

## Authorization route selection

Under the 2026 Consolidated Rules the pre-2026 routes (Joint Authorization Board Provisional ATO and FedRAMP Ready) are discontinued. A cloud service offering's authorization is now described by a **certification profile**: the combination of a certification type, a certification path, and a certification class.

| Dimension | Options | Basis for choosing |
| --- | --- | --- |
| Certification type | **20x** (modern; assurance based primarily on measured outcomes, evidenced through Key Security Indicators) or **Rev5** (legacy; assurance based primarily on documented plans and Rev5 Controls) | 20x for offerings following the measured-outcomes model; Rev5 for offerings continuing under the legacy documented-plans model during the transition |
| Certification path | **Program** (provided directly by FedRAMP) or **Agency** (agency-sponsored; a legacy path available only for Rev5 and still requiring review and approval from FedRAMP) | Program for a direct FedRAMP certification with no agency sponsor; Agency only where an agency sponsor exists and the offering is Rev5 |
| Certification class | **Class A** through **Class D**, increasing from minimal assurance at Class A to significant assurance at Class D | Chosen so the class matches the assurance the offering must supply to its federal customers |

The transition timeline in the held July 2026 rules places optional adoption from 4 July 2026, mandatory adoption from 1 January 2027, and the end of new Rev5 certifications on 11 June 2027; these dates are from the held July 2026 snapshot, so verify the live FedRAMP rules before relying on them.

---

> **Pre-2026 sections below.** The baseline-selection, library-coverage-and-gaps, operating-expectations, and framework-alignment sections that follow still reflect the pre-2026 FedRAMP structure (impact-level baselines, monthly continuous monitoring and POA&Ms, FedRAMP templates, and 3PAO terminology). The 2026 Consolidated Rules supersede much of this (Certification Classes A to D, Ongoing Certification, Accepted Weaknesses, no FedRAMP-provided templates, independent assessors); a fuller refresh is tracked separately (P-1.79).

## Baseline selection

FedRAMP baselines map to FIPS 199 system categorization. Adopting organizations confirm the categorization with their agency sponsor before selecting a baseline.

| Baseline | Use case | Rev. 5 baseline entries (controls and control enhancements) |
| --- | --- | --- |
| FedRAMP Low | Public-facing services with no confidentiality, integrity, or availability impact above Low | 156 |
| FedRAMP Moderate | Most federal use cases involving controlled unclassified information (CUI) | 323 |
| FedRAMP High | Mission-critical federal use cases including law enforcement, emergency services, financial systems | 410 |
| FedRAMP Tailored Low (LI-SaaS) | SaaS only, limited data scope | 156 tailored entries (all Low-baseline controls, assigned tailoring actions) |

---

## Library coverage and gaps

The library provides architectural baselines that align with FedRAMP control families. Adopting organizations must implement and evidence the controls per the selected baseline; the library is not a substitute for the authorization package.

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

Library gaps requiring additional documentation for a FedRAMP authorization package:

1. **Certification package documentation.** Under the 2026 Consolidated Rules the historically required System Security Plan and appendices are replaced, for both certification types, by the Certification Package Overview and the Security Decision Record (SDR); the security practices are expressed as measured Key Security Indicators under 20x and as Rev5 Controls under Rev5. The library provides architectural inputs; the certification-package documents are per-system artefacts built outside the library.
2. **Continuous Monitoring (ConMon) plan and monthly reporting.** FedRAMP requires monthly POA&M, vulnerability scan submission, and inventory updates.
3. **Plan of Action and Milestones (POA&M) register.** Tracked per FedRAMP cadence; library risk register is the conceptual basis but FedRAMP format is mandated.
4. **Independent assessment.** The 2026 rules do not require a separate Security Assessment Plan or Security Assessment Report for either 20x or Rev5 certifications; the assessment information is captured in the Security Decision Record. Under the legacy Agency path an agency authorizing official may still request the traditional Security Assessment Plan and Report in addition to FedRAMP's materials.
5. **Incident Response Reporting per OMB M-22-09 and US-CERT timelines.** Library incident procedures cover lifecycle; FedRAMP-specific reporting timelines are layered on top.
6. **FIPS-validated cryptography.** Library cryptographic key lifecycle framework establishes the practice; FedRAMP additionally requires FIPS 140-3 (or 140-2 in transition) validated modules.
7. **Personnel investigations under federal standards.** US federal background investigation standards beyond the library's screening standard.
8. **CUI handling under NIST SP 800-171 and 800-172.** Where the service handles CUI.

---

## Operating expectations

1. Each control implementation in the SSP references the relevant library artefact and any organization-specific extension.
2. ConMon submissions follow the FedRAMP-published cadence and template; the library's metrics and audit registers feed but do not replace the ConMon submission.
3. Significant change requests follow the FedRAMP significant change process; the library's change management procedure is the operational input.
4. Annual assessment by a 3PAO is scheduled; the assessment-evidence repository is structured around FedRAMP test cases, not library structure.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| FedRAMP Rev5 Baselines (Low, Moderate, High) | NIST SP 800-53 Rev. 5 + FedRAMP parameters | Legacy controls-based certification type |
| FedRAMP 20x | 2026 Consolidated Rules + Key Security Indicators (KSIs) | Modern measured-outcomes certification type; certification Classes A to D |
| FedRAMP Rev5 Tailored | LI-SaaS Authorization Process | Legacy tailored route |
| NIST SP 800-53 Rev. 5 | Security and Privacy Controls | Underlying control catalogue |
| NIST SP 800-37 Rev. 2 | Risk Management Framework | Authorization lifecycle |
| NIST SP 800-171 / 800-172 | Protecting CUI | Where applicable |
| OMB M-22-09 | Federal Zero Trust Strategy | Architectural direction |
| FIPS 199 | Standards for Security Categorization | Categorization prerequisite |
| FIPS 200 | Minimum Security Requirements | Baseline prerequisite |
| FIPS 140-3 / 140-2 | Cryptographic Module Validation | FIPS-validated cryptography |

The 2026 Consolidated Rules distinguish applicability by certification type (Rev5 or 20x) and by certification class (A to D). Their held timeline places the rules in optional adoption from 4 July 2026, schedules mandatory adoption for 1 January 2027, and ends new Rev5 certifications on 11 June 2027; these dates are from the held July 2026 snapshot, so verify the live FedRAMP rules before relying on the transition timeline. RFC-0006 is a superseded historical draft; the finalized Key Security Indicators are the current 20x specification. The Authorization route selection section above and the certification-package documentation items now reflect the 2026 certification-profile structure (type, path, and class) and the Certification Package Overview / Security Decision Record documentation model. JAB Provisional ATO is retired and FedRAMP Ready went legacy in July 2026 (no new submissions; existing Ready status persists through the transition). Several other sections of this annex still reflect the pre-2026 FedRAMP structure and are NOT yet updated: the baseline-selection table (Low/Moderate/High and Tailored, superseded by Certification Classes A to D), the continuous-monitoring and POA&M model (the 2026 rules replace continuous monitoring with Ongoing Certification and POA&Ms with a list of Accepted Weaknesses), the documentation templates (FedRAMP no longer provides templates), the assessor terminology (3PAO, now independent assessor), and the framework-alignment table. A fuller refresh of those sections to the 2026 model is tracked separately (P-1.79).

---

## Limitations

This annex is a CC BY-SA 4.0 navigation aid. FedRAMP authorization requires the FedRAMP-mandated artefacts, a federal sponsor or marketplace listing, and engagement with a 3PAO; this library does not produce authorization by itself. Adopting organizations consult the official FedRAMP programme documentation and engage a 3PAO before commencing authorization work. This annex is not a substitute for FedRAMP programme guidance.

---

**End of Document**
