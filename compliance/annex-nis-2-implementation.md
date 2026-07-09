# NIS 2 Implementation Annex

**Document Title:** NIS 2 Implementation Annex\
**Document Type:** Annex\
**Version:** 1.2.0\
**Date:** 2026-07-09\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/README.md`](README.md), [`compliance/policy-legal-and-regulatory-compliance.md`](policy-legal-and-regulatory-compliance.md), [`compliance/register-global-regulatory-applicability.md`](register-global-regulatory-applicability.md), [`compliance/matrix-grc-compliance-alignment.md`](matrix-grc-compliance-alignment.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`resilience/framework-business-continuity-and-resilience.md`](../resilience/framework-business-continuity-and-resilience.md)\
**Classification:** Public\
**Category:** Compliance: Sector-Specific\
**Review Frequency:** Annual and upon material national NIS 2 transposition, supervisory guidance, or sector designation change\
**Repository Path:** [`compliance/annex-nis-2-implementation.md`](annex-nis-2-implementation.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex describes how an entity in scope of EU Directive (EU) 2022/2555 (NIS 2) can use the core GRC library to implement the cybersecurity risk-management measures and the incident reporting obligations the directive imposes. It identifies the entity classification, the article-by-article mapping to library artefacts, the management body responsibilities, and the supplementary documentation that NIS 2 transposing laws require beyond the library baseline.

This annex does not reproduce NIS 2 article text or national transposition law. Adopting entities consume those from EUR-Lex and the national supervisor.

---

## Entity classification (Articles 2 to 3 and Annexes I to II)

NIS 2 introduces a size-cap rule and two categories of in-scope entity: Essential and Important. Adopting entities first confirm whether they fall in scope; the library is relevant where the entity is classified Essential or Important.

| Category | Examples (illustrative) |
| --- | --- |
| Essential | Energy, transport, banking, financial market infrastructures, health (hospitals, laboratories, manufacturers of medicinal products), drinking water, waste water, digital infrastructure (DNS service providers, TLD name registries, cloud computing service providers, data centre service providers, content delivery network providers, trust service providers, providers of public electronic communications networks or services), ICT service management (managed service providers, managed security service providers), public administration entities, space |
| Important | Postal and courier services, waste management, manufacture, production and distribution of chemicals, food, manufacturing (medical devices, computers and electronics, machinery, motor vehicles, transport equipment), digital providers (online marketplaces, online search engines, social networking services platforms), research |

Article 3 size cap: large (250+ employees or 50M euros turnover) and medium (50+ employees or 10M euros turnover) entities are in scope by default; specific subsectors are in scope below the cap by virtue of their function.

---

## DORA and sector-specific lex specialis (Article 4)

Where a sector-specific Union legal act requires essential or important entities to adopt cybersecurity risk-management measures or to notify significant incidents, and those requirements are at least equivalent in effect to the obligations of this Directive, the corresponding NIS2 provisions, including the supervision and enforcement provisions of Chapter VII, do not apply to those entities (Article 4(1)). Equivalence means that the sector-specific risk-management measures are at least equivalent in effect to those in Article 21(1) and (2), or that the incident-notification requirements are at least equivalent in effect to those in Article 23(1) to (6) with the appropriate access for the CSIRTs, competent authorities, or single points of contact (Article 4(2)).

For financial entities, the EU Digital Operational Resilience Act (Regulation (EU) 2022/2554, DORA) is the sector-specific act (NIS2 recital 28). A financial entity in scope of DORA therefore follows DORA for the equivalent ICT risk-management and incident-reporting requirements, and NIS2 Articles 21 and 23 and the Chapter VII supervision and enforcement provisions do not apply to it to that extent. The [DORA implementation annex](financial-services/annex-dora-implementation.md) carries the DORA-side treatment and the reciprocal statement of this boundary.

This is a scoped lex-specialis displacement of the equivalent obligations, not a blanket exemption: NIS2 continues to apply to entities in a NIS2 sector that the sector-specific act does not cover (Article 4(1), second sentence), and to any NIS2 obligation not met by an at-least-equivalent sector-specific requirement.

---

## Article 21 cybersecurity risk-management measures

Article 21 sets ten categories of cybersecurity risk-management measures. The library covers each as follows.

| NIS 2 Article 21.2 sub-measure | Library artefact | Evidence class |
| --- | --- | --- |
| (a) Policies on risk analysis and information system security | [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md), [`security/policy-information-security.md`](../security/policy-information-security.md) | Approved policy with version; risk register; risk assessment outputs; management-body sign-off record |
| (b) Incident handling | [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`resilience/procedure-cross-domain-incident-coordination.md`](../resilience/procedure-cross-domain-incident-coordination.md), [`security/sop-incident-escalation-matrix.md`](../security/sop-incident-escalation-matrix.md) | Incident register; post-incident reviews; escalation logs; Article 23 reporting evidence |
| (c) Business continuity, including backup management and disaster recovery, and crisis management | [`resilience/framework-business-continuity-and-resilience.md`](../resilience/framework-business-continuity-and-resilience.md), [`resilience/standard-business-continuity-and-disaster-recovery.md`](../resilience/standard-business-continuity-and-disaster-recovery.md), [`resilience/procedure-backup-and-recovery.md`](../resilience/procedure-backup-and-recovery.md), [`resilience/plan-business-continuity-and-crisis-management.md`](../resilience/plan-business-continuity-and-crisis-management.md), [`resilience/plan-crisis-communication.md`](../resilience/plan-crisis-communication.md) | BCP and DR plans; backup test results; tabletop exercise records; recovery time and recovery point measurements |
| (d) Supply chain security including security-related aspects concerning relationships between each entity and its direct suppliers or service providers | [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../supply-chain/framework-supplier-and-cloud-governance.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../supply-chain/standard-supplier-security-and-privacy-assurance.md), [`supply-chain/procedure-supplier-due-diligence.md`](../supply-chain/procedure-supplier-due-diligence.md) | Supplier risk register; due-diligence assessments; supplier contract security clauses; ongoing monitoring evidence |
| (e) Security in network and information systems acquisition, development, and maintenance, including vulnerability handling and disclosure | [`dev-security/policy-secure-development-and-engineering.md`](../dev-security/policy-secure-development-and-engineering.md), [`dev-security/standard-developer-security-requirements.md`](../dev-security/standard-developer-security-requirements.md), [`dev-security/standard-software-composition-analysis.md`](../dev-security/standard-software-composition-analysis.md), [`security/procedure-vulnerability-management.md`](../security/procedure-vulnerability-management.md), [`security/policy-acceptance-into-service.md`](../security/policy-acceptance-into-service.md) | SDLC artefacts (SAST, SCA, DAST results); vulnerability register; patch-management records; coordinated-disclosure log |
| (f) Policies and procedures to assess the effectiveness of cybersecurity risk-management measures | [`compliance/procedure-control-testing.md`](procedure-control-testing.md), [`compliance/standard-internal-audit.md`](standard-internal-audit.md), [`governance/procedure-grc-programme-management-and-annual-review.md`](../governance/procedure-grc-programme-management-and-annual-review.md) | Control-testing reports; internal audit reports; annual programme review records; remediation tracking |
| (g) Basic cyber hygiene practices and cybersecurity training | [`security/standard-security-awareness-and-training.md`](../security/standard-security-awareness-and-training.md) | Training completion records; phishing-simulation results; awareness campaign artefacts; management-body training evidence |
| (h) Policies and procedures regarding the use of cryptography and, where appropriate, encryption | [`security/policy-encryption-and-key-management.md`](../security/policy-encryption-and-key-management.md), [`security/framework-cryptographic-key-lifecycle.md`](../security/framework-cryptographic-key-lifecycle.md), [`security/procedure-cryptographic-key-operations.md`](../security/procedure-cryptographic-key-operations.md) | Cryptographic-controls inventory; key-management procedure records; HSM logs; algorithm-compliance attestations |
| (i) Human resources security, access control policies, and asset management | [`security/standard-personnel-security-screening.md`](../security/standard-personnel-security-screening.md), [`security/policy-identity-and-access-management.md`](../security/policy-identity-and-access-management.md), [`operations/register-asset-inventory.md`](../operations/register-asset-inventory.md), [`security/procedure-onboarding-and-offboarding.md`](../security/procedure-onboarding-and-offboarding.md) | Personnel screening records; access-review reports; asset inventory; onboarding/offboarding ticket records |
| (j) The use of multi-factor or continuous authentication solutions, secured voice, video and text communications and secured emergency communication systems within the entity, where appropriate | [`security/standard-authentication-and-password-management.md`](../security/standard-authentication-and-password-management.md), [`security/policy-network-communications-security.md`](../security/policy-network-communications-security.md) | MFA enrollment records; authentication logs; secure-communications configuration evidence; emergency-communication system test records |

---

## Article 20 management body responsibilities

NIS 2 places direct accountability on the management body. Members can be held personally liable for non-compliance with Article 21 measures and Article 23 reporting. The management body must:

1. Approve the cybersecurity risk-management measures.
2. Oversee implementation.
3. Receive training to identify cybersecurity risks and management practices and assess them.
4. Offer similar training to staff on a regular basis.

Library support: [`governance/framework-human-capital-and-ethical-conduct.md`](../governance/framework-human-capital-and-ethical-conduct.md), [`governance/register-role-authority.md`](../governance/register-role-authority.md), [`security/standard-security-awareness-and-training.md`](../security/standard-security-awareness-and-training.md). Each adopting entity additionally maintains a record of management-body training and approval evidence.

---

## Articles 23 to 25 incident reporting

NIS 2 mandates a tiered incident-notification regime to the competent authority or CSIRT.

| Phase | Window | Content |
| --- | --- | --- |
| Early warning | Within 24 hours of awareness of a significant incident | Indication of whether the incident is suspected to be caused by unlawful or malicious acts and whether it could have cross-border impact |
| Incident notification | Within 72 hours of awareness | Initial assessment of severity, impact, indicators of compromise where available |
| Intermediate report | Upon request of the competent authority or CSIRT | Update on the situation |
| Final report | Within one month of submitting the incident notification | Detailed description, type of threat or root cause, applied and ongoing mitigation, where applicable cross-border impact |

Significance threshold (Article 23(3)): the incident has caused or is capable of causing severe operational disruption of the services or financial loss for the entity concerned; the incident has affected or is capable of affecting other natural or legal persons by causing considerable material or non-material damage.

Library coverage: [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md) provides the lifecycle; [`resilience/procedure-security-incident-reporting-and-escalation.md`](../resilience/procedure-security-incident-reporting-and-escalation.md) provides the internal escalation. Adopting entities encode the NIS 2 windows in their severity playbooks and ensure that the early-warning and final-report templates are pre-prepared per national-CSIRT requirements.

---

## Supervision and penalties (Articles 32 to 34)

NIS2 supervision differs by entity class. Essential entities are subject to a comprehensive regime combining proactive and reactive measures: competent authorities may conduct on-site inspections, off-site supervision, and regular targeted security audits without a triggering precondition (Article 32). Important entities are subject to a lighter, reactive regime: competent authorities act only when provided with evidence, indication, or information that the entity does not comply, in particular with Articles 21 and 23, through ex-post supervisory measures (Article 33). The directive frames this comprehensive-ex-ante-and-ex-post versus light-ex-post-only distinction in recital 122.

Administrative fines (Article 34) are set at directive-level floors that each Member State's transposition must at least meet (the directive states "a maximum of at least"). For an infringement of Article 21 or 23, an essential entity is subject to a maximum of at least EUR 10 000 000 or at least 2 % of the total worldwide annual turnover in the preceding financial year of the undertaking to which it belongs, whichever is higher (Article 34(4)); an important entity to a maximum of at least EUR 7 000 000 or at least 1,4 % of that turnover, whichever is higher (Article 34(5)). The applied maxima, the procedural regime, and the registration requirement with the competent authority are set by national transposition law (transposition deadline 17 October 2024; national measures applied from 18 October 2024).

---

## Library gaps requiring additional documentation

1. **Management body training register** with specific NIS 2 content and frequency.
2. **CSIRT contact register** with the national CSIRT and the cross-border CSIRTs of jurisdictions where the entity operates.
3. **Incident reporting templates** in the format the national CSIRT publishes.
4. **Sectoral cybersecurity certification scheme** evidence where applicable under future delegated acts.
5. **Information exchange arrangements** with peer entities under Article 29 where the entity participates.
6. **National transposition specifics**: the applied supervisory procedures, the transposed fine maxima (the directive-level Article 34 floors are stated in the Supervision and penalties section above), and the registration requirement with the competent authority.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| NIS 2 Directive | (EU) 2022/2555 | Primary directive |
| NIS 2 Implementing Acts | Multiple per Article 21(5) and 27 | Technical and methodological specifications |
| ENISA guidelines | Multiple | Practical guidance |
| EU Cyber Resilience Act | Where products are placed on the EU market | Complementary obligation |
| EU Cybersecurity Act | (EU) 2019/881 | Certification framework |
| ISO/IEC 27001:2022 | Annex A | Underlying control catalogue |
| NIST CSF 2.0 | All functions | Cross-walk |

---

## Limitations

This annex is a CC BY-SA 4.0 navigation aid. NIS 2 compliance requires conformance with the national transposition law of every Member State in which the entity is established or provides services, registration with the competent authority, sector-specific certification where required by delegated acts, and supervisory engagement. Adopting entities consult the national transposition law, the competent authority's guidance, and ENISA's practical guidelines. This annex is not legal advice and does not establish compliance.

---

**End of Document**
