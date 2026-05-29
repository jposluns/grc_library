# NIS 2 Implementation Annex

**Document Title:** NIS 2 Implementation Annex\
**Document Type:** Annex\
**Version:** 0.0.1\
**Date:** 2026-05-28\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/README.md`](README.md), [`compliance/policy-legal-and-regulatory-compliance.md`](policy-legal-and-regulatory-compliance.md), [`compliance/register-global-regulatory-applicability.md`](register-global-regulatory-applicability.md), [`compliance/matrix-grc-compliance-alignment.md`](matrix-grc-compliance-alignment.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../risk/standard-third-party-and-supply-chain-risk.md), [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md), [`resilience/framework-business-continuity-and-resilience.md`](../resilience/framework-business-continuity-and-resilience.md)\
**Classification:** Public\
**Category:** Compliance: Sector-Specific\
**Review Frequency:** Annual and upon material national NIS 2 transposition, supervisory guidance, or sector designation change\
**Repository Path:** [`compliance/annex-nis-2-implementation.md`](annex-nis-2-implementation.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

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

## Article 21 cybersecurity risk-management measures

Article 21 sets ten categories of cybersecurity risk-management measures. The library covers each as follows.

| NIS 2 Article 21.2 sub-measure | Library artefact |
| --- | --- |
| (a) Policies on risk analysis and information system security | `risk/policy-enterprise-governance-and-risk-management.md`, `security/policy-information-security.md` |
| (b) Incident handling | `security/procedure-security-incident-response.md`, `resilience/procedure-cross-domain-incident-coordination.md`, `security/sop-incident-escalation-matrix.md` |
| (c) Business continuity, including backup management and disaster recovery, and crisis management | `resilience/framework-business-continuity-and-resilience.md`, `resilience/standard-business-continuity-and-disaster-recovery.md`, `resilience/procedure-backup-and-recovery.md`, `resilience/plan-business-continuity-and-crisis-management.md`, `resilience/plan-crisis-communication.md` |
| (d) Supply chain security including security-related aspects concerning relationships between each entity and its direct suppliers or service providers | `risk/standard-third-party-and-supply-chain-risk.md`, `supply-chain/framework-supplier-and-cloud-governance.md`, `supply-chain/standard-supplier-security-and-privacy-assurance.md`, `supply-chain/procedure-supplier-due-diligence.md` |
| (e) Security in network and information systems acquisition, development, and maintenance, including vulnerability handling and disclosure | `dev-security/policy-secure-development-and-engineering.md`, `dev-security/standard-developer-security-requirements.md`, `dev-security/standard-software-composition-analysis.md`, `security/procedure-vulnerability-management.md`, `security/policy-acceptance-into-service.md` |
| (f) Policies and procedures to assess the effectiveness of cybersecurity risk-management measures | `compliance/procedure-control-testing.md`, `compliance/standard-internal-audit.md`, `governance/procedure-grc-programme-management-and-annual-review.md` |
| (g) Basic cyber hygiene practices and cybersecurity training | `security/standard-security-awareness-and-training.md` |
| (h) Policies and procedures regarding the use of cryptography and, where appropriate, encryption | `security/policy-encryption-and-key-management.md`, `security/framework-cryptographic-key-lifecycle.md`, `security/procedure-cryptographic-key-operations.md` |
| (i) Human resources security, access control policies, and asset management | `security/standard-personnel-security-screening.md`, `security/policy-identity-and-access-management.md`, `operations/register-asset-inventory.md`, `security/procedure-onboarding-and-offboarding.md` |
| (j) The use of multi-factor or continuous authentication solutions, secured voice, video and text communications and secured emergency communication systems within the entity, where appropriate | `security/standard-authentication-and-password-management.md`, `security/policy-network-communications-security.md` |

---

## Article 20 management body responsibilities

NIS 2 places direct accountability on the management body. Members can be held personally liable for non-compliance with Article 21 measures and Article 23 reporting. The management body must:

1. Approve the cybersecurity risk-management measures.
2. Oversee implementation.
3. Receive training to identify cybersecurity risks and management practices and assess them.
4. Offer similar training to staff on a regular basis.

Library support: `governance/framework-human-capital-and-ethical-conduct.md`, `governance/register-role-authority.md`, `security/standard-security-awareness-and-training.md`. Each adopting entity additionally maintains a record of management-body training and approval evidence.

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

Library coverage: `security/procedure-security-incident-response.md` provides the lifecycle; `resilience/procedure-security-incident-reporting-and-escalation.md` provides the internal escalation. Adopting entities encode the NIS 2 windows in their severity playbooks and ensure that the early-warning and final-report templates are pre-prepared per national-CSIRT requirements.

---

## Library gaps requiring additional documentation

1. **Management body training register** with specific NIS 2 content and frequency.
2. **CSIRT contact register** with the national CSIRT and the cross-border CSIRTs of jurisdictions where the entity operates.
3. **Incident reporting templates** in the format the national CSIRT publishes.
4. **Sectoral cybersecurity certification scheme** evidence where applicable under future delegated acts.
5. **Information exchange arrangements** with peer entities under Article 29 where the entity participates.
6. **National transposition specifics** including the supervisory regime, fines, and the registration requirement with the competent authority.

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

This annex is a public-domain navigation aid. NIS 2 compliance requires conformance with the national transposition law of every Member State in which the entity is established or provides services, registration with the competent authority, sector-specific certification where required by delegated acts, and supervisory engagement. Adopting entities consult the national transposition law, the competent authority's guidance, and ENISA's practical guidelines. This annex is not legal advice and does not establish compliance.

---

**End of Document**
