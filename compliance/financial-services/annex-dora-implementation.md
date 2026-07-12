# DORA Implementation Annex

**Document Title:** DORA Implementation Annex\
**Document Type:** Annex\
**Version:** 0.0.7\
**Date:** 2026-07-12\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`compliance/README.md`](README.md), [`compliance/policy-legal-and-regulatory-compliance.md`](../policy-legal-and-regulatory-compliance.md), [`compliance/register-global-regulatory-applicability.md`](../register-global-regulatory-applicability.md), [`compliance/financial-services/annex-financial-services-sector-requirements.md`](annex-financial-services-sector-requirements.md), [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../../risk/standard-third-party-and-supply-chain-risk.md), [`resilience/framework-business-continuity-and-resilience.md`](../../resilience/framework-business-continuity-and-resilience.md), [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../../supply-chain/standard-supplier-security-and-privacy-assurance.md)\
**Classification:** Public\
**Category:** Compliance: Sector-Specific\
**Review Frequency:** Annual and upon material DORA Regulatory Technical Standards (RTS), Implementing Technical Standards (ITS), or supervisory guidance change\
**Repository Path:** [`compliance/financial-services/annex-dora-implementation.md`](annex-dora-implementation.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This annex describes how a financial entity in scope of the EU Digital Operational Resilience Act (Regulation (EU) 2022/2554) can use the core GRC library to implement the five DORA pillars. The annex maps the library to each pillar, identifies the supplementary supervisory artefacts DORA requires, and notes the obligations specific to critical ICT third-party service providers.

This annex does not reproduce DORA articles, RTS, or ITS text. Adopting financial entities consume those from the official EUR-Lex and ESA sources.

---

## Applicability triggers

DORA applies to a broad set of financial entities established in the EU. The library is relevant where the entity is one of the in-scope categories:

1. Credit institution, payment institution, electronic money institution, account information service provider.
2. Investment firm, central securities depository, central counterparty, trading venue.
3. Trade repository, credit rating agency, administrator of critical benchmarks, crowdfunding service provider.
4. Insurance and reinsurance undertaking, insurance intermediary, institution for occupational retirement provision.
5. Manager of alternative investment fund, management company, data reporting service provider.
6. Critical ICT third-party service provider designated by the ESAs.

The micro-enterprise carve-out and the simplified ICT risk management framework apply to a defined subset; consult Article 16 and the related RTS for the exact thresholds.

---

## Relationship to NIS2 (lex specialis)

DORA is a sector-specific Union legal act in relation to the NIS2 Directive (Directive (EU) 2022/2555) for financial entities (NIS2 recital 28). Under NIS2 Article 4, where a sector-specific act's requirements are at least equivalent in effect to the corresponding NIS2 obligations, those NIS2 obligations, including the supervision and enforcement provisions of NIS2 Chapter VII, do not apply to the covered entities. DORA's ICT risk-management, ICT-related-incident-reporting, resilience-testing, information-sharing, and ICT third-party-risk requirements therefore apply to financial entities in place of the equivalent NIS2 obligations; a financial entity in scope of DORA follows this annex for those requirements rather than the NIS2 annex. See the [NIS2 implementation annex](../annex-nis-2-implementation.md) for the NIS2 side of this boundary. This is a scoped lex-specialis displacement of equivalent obligations, not a blanket exemption; a financial entity remains subject to any NIS2 obligation not covered by an at-least-equivalent DORA requirement.

---

## Pillar 1: ICT risk management framework (Articles 5 to 16)

DORA requires a documented ICT risk management framework approved by the management body and subject to a periodic review. The library supports this with:

| DORA element | Library artefact |
| --- | --- |
| Management body responsibility and oversight | [`risk/policy-enterprise-governance-and-risk-management.md`](../../risk/policy-enterprise-governance-and-risk-management.md), [`governance/charter-governance-library.md`](../../governance/charter-governance-library.md) |
| ICT risk management framework | [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md), [`risk/procedure-risk-assessment-methodology.md`](../../risk/procedure-risk-assessment-methodology.md), [`risk/procedure-risk-register.md`](../../risk/procedure-risk-register.md) |
| ICT systems, protocols, and tools | [`operations/framework-it-service-management.md`](../../operations/framework-it-service-management.md), [`operations/register-asset-inventory.md`](../../operations/register-asset-inventory.md) |
| Information security policy | [`security/policy-information-security.md`](../../security/policy-information-security.md), supporting standards across `security/` |
| Identification and classification of ICT-supported business functions | [`operations/register-asset-inventory.md`](../../operations/register-asset-inventory.md), [`risk/procedure-risk-register.md`](../../risk/procedure-risk-register.md) |
| Continuous monitoring of ICT-related risks | [`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md), [`operations/procedure-security-monitoring-and-alert-management.md`](../../operations/procedure-security-monitoring-and-alert-management.md), [`operations/procedure-threat-intelligence-and-siem-operations.md`](../../operations/procedure-threat-intelligence-and-siem-operations.md) |
| Learning and evolving | [`governance/procedure-continuous-improvement-register.md`](../../governance/procedure-continuous-improvement-register.md), [`compliance/procedure-capa.md`](../procedure-capa.md) |

Gap: DORA-specific RTS templates for the simplified ICT risk management framework (for in-scope smaller entities) require their own evidence outside the library.

---

## Pillar 2: ICT-related incident reporting (Articles 17 to 23)

DORA requires classification, management, and reporting of major ICT-related incidents and significant cyber threats.

| DORA element | Library artefact |
| --- | --- |
| Incident management process | [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md), [`resilience/procedure-cross-domain-incident-coordination.md`](../../resilience/procedure-cross-domain-incident-coordination.md) |
| Incident classification (Article 18 criteria) | The library provides severity criteria; entities must extend to DORA classification thresholds (clients affected, services affected, data losses, reputational impact, duration, geographical spread, economic impact) |
| Reporting to competent authority | Library does not provide the regulator-specific reporting template; entities use the ITS-defined forms (initial, intermediate, final notification) within DORA-defined windows |
| Major cyber threat voluntary reporting | Supported by [`operations/procedure-threat-intelligence-and-siem-operations.md`](../../operations/procedure-threat-intelligence-and-siem-operations.md) |
| Information about clients and counterparts | [`resilience/plan-crisis-communication.md`](../../resilience/plan-crisis-communication.md) |

DORA-mandated reporting windows (the reporting obligation is Article 19; the content and time limits are set by the RTS in Commission Delegated Regulation (EU) 2025/301 and the standard forms by the ITS in Commission Implementing Regulation (EU) 2025/302, both adopted under Article 20): the initial notification is due as early as possible and in any case within 4 hours of the incident's classification as major AND no later than 24 hours from the moment the entity became aware of the incident; the intermediate report at the latest within 72 hours of the initial notification; and the final report no later than one month after the intermediate report. Classification as a major incident applies the criteria and materiality thresholds in the RTS in Commission Delegated Regulation (EU) 2024/1772 (under Article 18). Adopting entities encode these in their per-incident severity playbooks.

---

## Pillar 3: Digital operational resilience testing (Articles 24 to 27)

DORA requires a comprehensive digital operational resilience testing programme. The library supports this with:

| DORA element | Library artefact |
| --- | --- |
| ICT testing programme | [`resilience/procedure-continuity-and-recovery-testing.md`](../../resilience/procedure-continuity-and-recovery-testing.md), [`resilience/register-resilience-metrics-and-testing-log.md`](../../resilience/register-resilience-metrics-and-testing-log.md) |
| Vulnerability assessments, scans, source code reviews | [`security/procedure-vulnerability-management.md`](../../security/procedure-vulnerability-management.md), [`dev-security/standard-software-composition-analysis.md`](../../dev-security/standard-software-composition-analysis.md), [`dev-security/procedure-secure-code-review.md`](../../dev-security/procedure-secure-code-review.md) (if adopted) |
| Network security assessments, gap analyses, performance testing | [`operations/standard-network-security-and-segmentation.md`](../../operations/standard-network-security-and-segmentation.md), [`security/standard-penetration-testing-and-red-team.md`](../../security/standard-penetration-testing-and-red-team.md) |
| End-to-end testing | [`resilience/procedure-continuity-and-recovery-testing.md`](../../resilience/procedure-continuity-and-recovery-testing.md) |
| Threat-led penetration testing (TLPT) | [`security/standard-penetration-testing-and-red-team.md`](../../security/standard-penetration-testing-and-red-team.md) provides the baseline; TLPT must additionally follow the TIBER-EU framework or equivalent as set by the ESAs |

TLPT-scope entities are those identified by competent authorities based on their importance to the financial sector (Article 26(8), applying the Article 4(2) criteria). Each test covers several or all of the entity's critical or important functions and is performed on live production systems, with the precise scope validated by the competent authority (Article 26(2)). Frequency: at minimum every three years, which the competent authority may reduce or increase for a given entity based on its risk profile (Article 26(1)).

---

## Pillar 4: Managing ICT third-party risk (Articles 28 to 44)

This pillar materially extends standard third-party risk management. The library supports this with:

| DORA element | Library artefact |
| --- | --- |
| Third-party risk strategy | [`risk/standard-third-party-and-supply-chain-risk.md`](../../risk/standard-third-party-and-supply-chain-risk.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../../supply-chain/framework-supplier-and-cloud-governance.md) |
| ICT third-party register | [`supply-chain/register-supplier-risk-template.md`](../../supply-chain/register-supplier-risk-template.md), [`supply-chain/register-subprocessor-template.md`](../../supply-chain/register-subprocessor-template.md) |
| Pre-contractual analysis | [`supply-chain/procedure-supplier-due-diligence.md`](../../supply-chain/procedure-supplier-due-diligence.md), [`supply-chain/procedure-supplier-onboarding-security-review.md`](../../supply-chain/procedure-supplier-onboarding-security-review.md) |
| Mandatory contract clauses (Article 30) | [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../../supply-chain/standard-supplier-security-and-privacy-assurance.md) provides the structure; entities must verify all Article 30 minimum clauses are present including audit rights, exit strategy, subcontracting conditions, service-level descriptions, and incident notification commitments |
| Concentration risk assessment | [`supply-chain/register-concentration-risk.md`](../../supply-chain/register-concentration-risk.md) |
| Exit strategies | [`supply-chain/procedure-supplier-exit-and-data-return.md`](../../supply-chain/procedure-supplier-exit-and-data-return.md), [`supply-chain/standard-cloud-exit-and-data-portability.md`](../../supply-chain/standard-cloud-exit-and-data-portability.md) |
| Ongoing monitoring | [`supply-chain/procedure-supplier-ongoing-monitoring.md`](../../supply-chain/procedure-supplier-ongoing-monitoring.md) |

**Register of information (Article 28(3)).** In-scope financial entities maintain and update a register of all contractual arrangements for the use of ICT services, at entity, sub-consolidated, and consolidated levels, documented so as to distinguish arrangements that support critical or important functions from those that do not, and report at least yearly to the competent authority on new arrangements, the categories of ICT third-party service providers, the types of contractual arrangement, and the ICT services and functions provided. The library's supplier and concentration registers ([`supply-chain/register-supplier-risk-template.md`](../../supply-chain/register-supplier-risk-template.md), [`supply-chain/register-concentration-risk.md`](../../supply-chain/register-concentration-risk.md)) are the operational inputs; the DORA register itself is a supervisory artefact the entity maintains at the regulation's granularity and produces to the competent authority on request.

### Critical ICT third-party service providers

Designated providers are designated by the ESAs, through the Joint Committee and on a recommendation from the Oversight Forum, following an assessment against the Article 31(2) criteria: the systemic impact of a large-scale operational failure of the provider, the systemic character or importance of the financial entities relying on it, the reliance on the provider for critical or important functions, and the degree of substitutability. For each designated provider the ESAs appoint a Lead Overseer (the ESA responsible for the financial entities holding the largest share of total assets among those using the provider, Article 31(1)(b)), which has powers to request information and documentation and to conduct general investigations and inspections (Article 35, exercised through Articles 37 to 39). A designated provider established in a third country may be used by a financial entity only if the provider establishes a subsidiary in the Union within the 12 months following its designation (Article 31(12)). The consequence for an adopter: a financial entity relying on a designated critical provider verifies the Union-subsidiary condition, maintains the Article 30 contractual arrangements and an exit strategy for the provider ([`supply-chain/procedure-supplier-exit-and-data-return.md`](../../supply-chain/procedure-supplier-exit-and-data-return.md)), and carries the provider in its Article 28 register.

---

## Pillar 5: Information and intelligence sharing (Article 45)

Voluntary; DORA encourages financial entities to share cyber threat information and intelligence including indicators of compromise, tactics, techniques, and procedures. The library supports this through:

| DORA element | Library artefact |
| --- | --- |
| Threat intelligence operations | [`operations/procedure-threat-intelligence-and-siem-operations.md`](../../operations/procedure-threat-intelligence-and-siem-operations.md) |
| Confidentiality, protection of personal data, antitrust safeguards | Library privacy and compliance artefacts |

---

## Library gaps requiring additional documentation

1. **Register of all contractual arrangements** in the format and granularity DORA requires (Article 28(3) and the related RTS). Entities maintain this in a regulatory-compliant register beyond the library's supplier risk template.
2. **Concentration risk register** specific to critical ICT third-party providers and intra-group concentrations.
3. **Incident reporting templates** matching the EBA/EIOPA/ESMA-published forms.
4. **TLPT scoping documentation** under TIBER-EU.
5. **Management body annual review evidence** of the ICT risk management framework.
6. **ICT business continuity strategy and policy** at the level of detail Article 11 requires beyond the library baseline.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| DORA | Regulation (EU) 2022/2554 | Primary regulation |
| DORA RTS and ITS | Multiple, adopted by the Commission on ESA drafts; the incident-reporting set is Delegated Reg (EU) 2024/1772 (classification and materiality thresholds), Delegated Reg (EU) 2025/301 (report content and time limits), and Implementing Reg (EU) 2025/302 (report forms and templates) | Implementing detail |
| TIBER-EU | ECB framework | Threat-led penetration testing |
| EBA Guidelines on outsourcing arrangements | EBA/GL/2019/02 | Predecessor framework, partially superseded by DORA but retained where in force |
| EIOPA Guidelines on ICT security and governance | EIOPA-BoS-20-600 | Insurance sector |
| ISO/IEC 27001:2022 | Annex A | Underlying control catalogue |
| NIST CSF 2.0 | All functions | Cross-walk |

---

## Limitations

This annex is a CC BY-SA 4.0 navigation aid. DORA compliance requires regulator-specific reporting, contractual language verified against Article 30, evidence at the granularity required by RTS and ITS, and supervisory engagement. Adopting financial entities consult the regulation, the published RTS and ITS, and the ESA and competent-authority guidance applicable to their entity type. This annex is not legal advice and does not establish compliance.

---

**End of Document**
