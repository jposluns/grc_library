# FedRAMP Sector Requirements Annex

**Document Title:** FedRAMP Sector Requirements Annex\
**Document Type:** Annex\
**Version:** 0.0.16\
**Date:** 2026-09-18\
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

This annex does not reproduce FedRAMP control text or the FedRAMP-specified certification-package requirements. Adopting organizations consume those from the official FedRAMP source (which, under the 2026 rules, specifies required information rather than providing fixed templates).

---

## Applicability triggers

The library is relevant to FedRAMP where the organization:

1. Sells or intends to sell a cloud service offering to a US federal agency.
2. Operates as a cloud service provider for a federal contractor whose contract requires FedRAMP authorization flow-down.
3. Operates as an independent assessment service (an independent assessor, formerly a third-party assessment organization or 3PAO) supporting certification packages.
4. Operates as a state, local, or tribal government provider whose buyer requires StateRAMP, TX-RAMP, or equivalent and relies on FedRAMP-equivalent controls.

The library is not relevant where the organization has no federal customer in pipeline and no contractual flow-down requirement.

---

## Authorization route selection

Under the 2026 Consolidated Rules the pre-2026 routes are superseded: the Joint Authorization Board Provisional ATO is retired, and FedRAMP Ready went legacy in July 2026 (no new submissions, with existing Ready status retained through the transition). A cloud service offering's authorization is now described by a **certification profile**: the combination of a certification type, a certification path, and a certification class.

| Dimension | Options | Basis for choosing |
| --- | --- | --- |
| Certification type | **20x** (modern; assurance based primarily on measured outcomes, evidenced through Key Security Indicators) or **Rev5** (legacy; assurance based primarily on documented plans and Rev5 Controls) | 20x for offerings following the measured-outcomes model; Rev5 for offerings continuing under the legacy documented-plans model during the transition |
| Certification path | **Program** (provided directly by FedRAMP) or **Agency** (agency-sponsored; a legacy path available only for Rev5 and still requiring review and approval from FedRAMP) | Program for a direct FedRAMP certification with no agency sponsor; Agency only where an agency sponsor exists and the offering is Rev5 |
| Certification class | **Class A** through **Class D**, increasing from minimal assurance at Class A to significant assurance at Class D | Chosen so the class matches the assurance the offering must supply to its federal customers |

The transition timeline in the held July 2026 rules places optional adoption from 4 July 2026, mandatory adoption from 1 January 2027, and the end of new Rev5 certifications on 11 June 2027; these dates are from the held July 2026 snapshot, so verify the live FedRAMP rules before relying on them.

---

## Certification class selection

Under the 2026 Consolidated Rules a cloud service offering is described by a certification profile (type, path, and class; see Authorization route selection above). The certification class describes the depth and assurance of the certification data a provider supplies, chosen against the assurance an agency customer needs. Certification classes are not a one-for-one replacement for FIPS 199 impact levels: an agency categorizes its own information system under FIPS 199 and FIPS 200, then reviews a service's certification package to judge whether the protections suit the intended use.

| Certification class | Assurance and use-case guidance | 20x availability (held July 2026 snapshot) | Rev5 availability and applicable baseline |
| --- | --- | --- | --- |
| Class A (minimal assurance) | Pilots, configuration and testing, or extremely low or negligible-risk use cases such as processing public information or getting started with very few users | Program required; Agency unavailable | Unavailable under both paths |
| Class B | Most Low-impact agency systems, and some Moderate or High-impact systems with appropriate compensating controls | Program required; Agency unavailable | Agency generally required, Program limited (Ready Conversion or Lost Sponsor, with FedRAMP confirming eligibility); the applicable NIST SP 800-53 Rev. 5 controls are recorded in the Security Decision Record |
| Class C | Most Low or Moderate-impact agency systems, and some High-impact systems with appropriate compensating controls | Program required; Agency unavailable | Agency generally required, Program limited; the applicable Rev5 controls are recorded in the Security Decision Record |
| Class D (significant assurance) | Most agency systems regardless of impact level with appropriate compensating controls; excludes systems that process classified information | Program coming in 2027; Agency unavailable | Agency required; Program unavailable; the applicable Rev5 controls are recorded in the Security Decision Record |

The pre-2026 impact-level baselines (Low, Moderate, High) are superseded as the selection model by the certification classes above; the FedRAMP Tailored LI-SaaS baseline is not separately enumerated in the 2026 certification-profile model. Both persist in the historical Rev5 baseline records.

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

1. **Certification package documentation.** Under the 2026 Consolidated Rules the historically required System Security Plan is superseded: for FedRAMP Rev5 the Certification Package Overview replaces the base System Security Plan (not including its appendices), and the Security Decision Record replaces the traditional System Security Plan as a persistently maintained, verified, and validated record of the provider's security decisions; the rules' crosswalk maps the former System Security Plan and its appendices onto the Certification Package Overview and Security Decision Record together. The security practices are expressed as measured Key Security Indicators under 20x and as Rev5 Controls under Rev5. The library provides architectural inputs; the certification-package documents are per-system artefacts built outside the library.
2. **Ongoing Certification reporting.** The 2026 Consolidated Rules replace continuous monitoring with Ongoing Certification: providers supply an Ongoing Certification Report every three months in a human-readable format, and make historical vulnerability detection and response activity available in JSON for automated retrieval, updated at least monthly (Class A may, Class B should), at least every 14 days (Class C should), and at least every 7 days (Class D should). For Rev5 certifications, the system component inventory is reviewed and updated at an organization-defined frequency.
3. **Accepted Weaknesses list.** The 2026 Consolidated Rules eliminate provider Plans of Action and Milestones and replace them with a list of Accepted Weaknesses; the library risk register remains the conceptual basis for tracking and accepting weaknesses. Agencies may still maintain their own Plans of Action and Milestones from the provider's reported vulnerability information.
4. **Independent assessment.** The 2026 rules do not require a separate Security Assessment Plan or Security Assessment Report for either 20x or Rev5 certifications; the assessment information is captured in the Security Decision Record. Under the legacy Agency path an agency authorizing official may still request the traditional Security Assessment Plan and Report in addition to FedRAMP's materials.
5. **Incident Response Reporting per FedRAMP's Incident Evaluation and Communication rules.** Library incident procedures cover the lifecycle; the 2026 Consolidated Rules layer FedRAMP-specific reporting on top. A FedRAMP Reportable Incident (one affecting, or likely to affect, the confidentiality or integrity of federal customer data) is filed on class-graded Initial Incident Report clocks keyed to a Potential Agency Impact N-rating (PAIN): for example Class B within 6 hours for PAIN-5 to PAIN-3 and 1 business day for PAIN-2 to PAIN-1, with class-specific clocks for Classes C and D, plus ongoing and final reports and any agency-specific procedures.
6. **FIPS-validated cryptography.** Library cryptographic key lifecycle framework establishes the practice; under the 2026 Consolidated Rules a provider documents its use of cryptographic modules, and the expectation to use cryptographic modules (or update streams of such modules) with an active NIST Cryptographic Module Validation Program validation is class-dependent (Classes A and B may, Class C should, Class D must).
7. **Personnel screening (NIST SP 800-53 PS-3).** The Rev5 PS-3 personnel-screening control applies to Classes B to D; the 2026 rules assign no FedRAMP-specific parameter values, screening is required before access is authorized, and the provider defines its own rescreening conditions and frequency, beyond the library's screening standard.
8. **CUI handling, where applicable.** Where the service handles Controlled Unclassified Information, CUI-protection obligations (for example NIST SP 800-171 / 800-172) arise from the CUI program and contract terms under their own authority; the 2026 FedRAMP rules do not themselves impose them.

---

## Operating expectations

1. Each security decision recorded in the certification package's Security Decision Record (which carries the applicable Rev5-control information for Rev5 and the Key Security Indicator information for 20x) references the relevant library artefact and any organization-specific extension.
2. Ongoing Certification reporting follows the cadence the 2026 Consolidated Rules set (the three-monthly Ongoing Certification Report, and JSON vulnerability-activity reporting for automated retrieval, updated at least monthly (Class A may, Class B should), at least every 14 days (Class C should), and at least every 7 days (Class D should)); the library's metrics and audit registers feed but do not replace that reporting.
3. Significant change requests follow the FedRAMP significant change process; the library's change management procedure is the operational input.
4. For Classes B to D an independent verification and validation assessment of all applicable FedRAMP rules by a FedRAMP Recognized independent assessment service (or FedRAMP) is completed at least annually; a Class A certification may complete one and follows its underlying alternative security framework's assessment expectations. The assessment-evidence repository is organized around the FedRAMP assessment, not library structure.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| FedRAMP Rev5 | NIST SP 800-53 Rev. 5 controls (class-specific, per FedRAMP Rev5 Controls Guidance) | Legacy documented-plans certification type; applicable controls recorded in the Security Decision Record |
| FedRAMP 20x | 2026 Consolidated Rules + Key Security Indicators (KSIs) | Modern measured-outcomes certification type; certification Classes A to D |
| Certification Package Overview (CPO) | 2026 Consolidated Rules certification package | For Rev5, replaces the historically required System Security Plan (not including appendices); supplied in human-readable and JSON formats |
| Security Decision Record (SDR) | 2026 Consolidated Rules certification package | Persistently maintained record of a provider's security decisions; replaces the traditional System Security Plan for both types |
| Key Security Indicators (KSIs) | Finalized 2026 KSI content, folded into the Consolidated Rules | 20x measured-outcome evidence (supersedes the RFC-0006 draft) |
| NIST SP 800-53 Rev. 5 | Security and Privacy Controls | Underlying Rev5 control catalogue |
| NIST SP 800-37 Rev. 2 | Risk Management Framework | Authorization lifecycle |
| NIST SP 800-171 / 800-172 | Protecting CUI | External CUI-protection standards, where applicable; not imposed by the 2026 FedRAMP rules |
| OMB M-22-09 | Federal Zero Trust Strategy | External federal architectural direction; not imposed by the 2026 FedRAMP rules |
| FIPS 199 | Standards for Security Categorization | Categorization prerequisite |
| FIPS 200 | Minimum Security Requirements | Baseline prerequisite |
| FIPS 140 (NIST CMVP) | Cryptographic module validation | Cryptographic module use documented per the 2026 rules; using CMVP-validated modules or update streams is class-dependent (Classes A and B may, Class C should, Class D must) |

The 2026 Consolidated Rules distinguish applicability by certification type (Rev5 or 20x) and by certification class (A to D). Their held timeline places the rules in optional adoption from 4 July 2026, schedules mandatory adoption for 1 January 2027, and ends new Rev5 certifications on 11 June 2027; these dates are from the held July 2026 snapshot, so verify the live FedRAMP rules before relying on the transition timeline. RFC-0006 is a superseded historical draft; the finalized Key Security Indicators are the current 20x specification. The Authorization route selection and Certification class selection sections, the certification-package documentation, and the Framework alignment table now reflect the 2026 certification-profile structure (type, path, and class), the Certification Classes A to D, and the Certification Package Overview / Security Decision Record documentation model. JAB Provisional ATO is retired and FedRAMP Ready went legacy in July 2026 (no new submissions; existing Ready status persists through the transition).

---

## Limitations

This annex is a CC BY-SA 4.0 navigation aid. FedRAMP authorization requires the FedRAMP-mandated certification-package materials and, depending on the certification path and class, a federal agency sponsor and independent verification and validation by a FedRAMP Recognized assessor; this library does not produce authorization by itself. Adopting organizations consult the official FedRAMP programme documentation before commencing authorization work. This annex is not a substitute for FedRAMP programme guidance.

---

**End of Document**
