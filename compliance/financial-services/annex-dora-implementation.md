# DORA Implementation Annex

**Document Title:** DORA Implementation Annex 
**Document Type:** Annex 
**Version:** 0.0.2 
**Date:** 2026-05-28 
**Owner:** Chief Compliance Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`compliance/README.md`](README.md), [`compliance/policy-legal-and-regulatory-compliance.md`](../policy-legal-and-regulatory-compliance.md), [`compliance/register-global-regulatory-applicability.md`](../register-global-regulatory-applicability.md), [`compliance/financial-services/annex-financial-services-sector-requirements.md`](annex-financial-services-sector-requirements.md), [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md), [`risk/standard-third-party-and-supply-chain-risk.md`](../../risk/standard-third-party-and-supply-chain-risk.md), [`resilience/framework-business-continuity-and-resilience.md`](../../resilience/framework-business-continuity-and-resilience.md), [`security/procedure-security-incident-response.md`](../../security/procedure-security-incident-response.md), [`supply-chain/standard-supplier-security-and-privacy-assurance.md`](../../supply-chain/standard-supplier-security-and-privacy-assurance.md) 
**Classification:** Public 
**Category:** Compliance: Sector-Specific 
**Review Frequency:** Annual and upon material DORA Regulatory Technical Standards (RTS), Implementing Technical Standards (ITS), or supervisory guidance change 
**Repository Path:** [`compliance/financial-services/annex-dora-implementation.md`](annex-dora-implementation.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

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

## Pillar 1: ICT risk management framework (Articles 5 to 16)

DORA requires a documented ICT risk management framework approved by the management body and subject to a periodic review. The library supports this with:

| DORA element | Library artefact |
| --- | --- |
| Management body responsibility and oversight | `risk/policy-enterprise-governance-and-risk-management.md`, `governance/charter-governance-library.md` |
| ICT risk management framework | `risk/standard-enterprise-risk-management.md`, `risk/procedure-risk-assessment-methodology.md`, `risk/procedure-risk-register.md` |
| ICT systems, protocols, and tools | `operations/framework-it-service-management.md`, `operations/register-asset-inventory.md` |
| Information security policy | `security/policy-information-security.md`, supporting standards across `security/` |
| Identification and classification of ICT-supported business functions | `operations/register-asset-inventory.md`, `risk/procedure-risk-register.md` |
| Continuous monitoring of ICT-related risks | `security/standard-logging-and-monitoring.md`, `operations/procedure-security-monitoring-and-alert-management.md`, `operations/procedure-threat-intelligence-and-siem-operations.md` |
| Learning and evolving | `governance/procedure-continuous-improvement-register.md`, `compliance/procedure-capa.md` |

Gap: DORA-specific RTS templates for the simplified ICT risk management framework (for in-scope smaller entities) require their own evidence outside the library.

---

## Pillar 2: ICT-related incident reporting (Articles 17 to 23)

DORA requires classification, management, and reporting of major ICT-related incidents and significant cyber threats.

| DORA element | Library artefact |
| --- | --- |
| Incident management process | `security/procedure-security-incident-response.md`, `resilience/procedure-cross-domain-incident-coordination.md` |
| Incident classification (Article 18 criteria) | The library provides severity criteria; entities must extend to DORA classification thresholds (clients affected, services affected, data losses, reputational impact, duration, geographical spread, economic impact) |
| Reporting to competent authority | Library does not provide the regulator-specific reporting template; entities use the ITS-defined forms (initial, intermediate, final notification) within DORA-defined windows |
| Major cyber threat voluntary reporting | Supported by `operations/procedure-threat-intelligence-and-siem-operations.md` |
| Information about clients and counterparts | `resilience/plan-crisis-communication.md` |

DORA-mandated reporting windows (subject to RTS / ITS): initial notification "no later than 4 hours from classification as major"; intermediate report within 72 hours; final report within one month. Adopting entities encode these in their per-incident severity playbooks.

---

## Pillar 3: Digital operational resilience testing (Articles 24 to 27)

DORA requires a comprehensive digital operational resilience testing programme. The library supports this with:

| DORA element | Library artefact |
| --- | --- |
| ICT testing programme | `resilience/procedure-continuity-and-recovery-testing.md`, `resilience/register-resilience-metrics-and-testing-log.md` |
| Vulnerability assessments, scans, source code reviews | `security/procedure-vulnerability-management.md`, `dev-security/standard-software-composition-analysis.md`, `dev-security/procedure-secure-code-review.md` (if adopted) |
| Network security assessments, gap analyses, performance testing | `operations/standard-network-security-and-segmentation.md`, `security/standard-penetration-testing-and-red-team.md` |
| End-to-end testing | `resilience/procedure-continuity-and-recovery-testing.md` |
| Threat-led penetration testing (TLPT) | `security/standard-penetration-testing-and-red-team.md` provides the baseline; TLPT must additionally follow the TIBER-EU framework or equivalent as set by the ESAs |

TLPT-scope entities are those identified by competent authorities based on their importance to the financial sector. Frequency: at minimum every three years.

---

## Pillar 4: Managing ICT third-party risk (Articles 28 to 44)

This pillar materially extends standard third-party risk management. The library supports this with:

| DORA element | Library artefact |
| --- | --- |
| Third-party risk strategy | `risk/standard-third-party-and-supply-chain-risk.md`, `supply-chain/framework-supplier-and-cloud-governance.md` |
| ICT third-party register | `supply-chain/register-supplier-risk-template.md`, `supply-chain/register-subprocessor-template.md` |
| Pre-contractual analysis | `supply-chain/procedure-supplier-due-diligence.md`, `supply-chain/procedure-supplier-onboarding-security-review.md` |
| Mandatory contract clauses (Article 30) | `supply-chain/standard-supplier-security-and-privacy-assurance.md` provides the structure; entities must verify all Article 30 minimum clauses are present including audit rights, exit strategy, subcontracting conditions, service-level descriptions, and incident notification commitments |
| Concentration risk assessment | Library gap: planned `supply-chain/register-concentration-risk.md` (Phase 9.4); entities must implement before DORA enforcement |
| Exit strategies | `supply-chain/procedure-supplier-exit-and-data-return.md`, `supply-chain/standard-cloud-exit-and-data-portability.md` |
| Ongoing monitoring | `supply-chain/procedure-supplier-ongoing-monitoring.md` |

### Critical ICT third-party service providers

Designation criteria are set in Article 31 (criticality, substitutability, market impact). Designated providers are subject to Oversight Framework supervision by a Lead Overseer (ECB, EBA, EIOPA, or ESMA depending on designation).

---

## Pillar 5: Information and intelligence sharing (Article 45)

Voluntary; DORA encourages financial entities to share cyber threat information and intelligence including indicators of compromise, tactics, techniques, and procedures. The library supports this through:

| DORA element | Library artefact |
| --- | --- |
| Threat intelligence operations | `operations/procedure-threat-intelligence-and-siem-operations.md` |
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
| DORA RTS and ITS | Multiple; published by ESAs | Implementing detail |
| TIBER-EU | ECB framework | Threat-led penetration testing |
| EBA Guidelines on outsourcing arrangements | EBA/GL/2019/02 | Predecessor framework, partially superseded by DORA but retained where in force |
| EIOPA Guidelines on ICT security and governance | EIOPA-BoS-20-600 | Insurance sector |
| ISO/IEC 27001:2022 | Annex A | Underlying control catalogue |
| NIST CSF 2.0 | All functions | Cross-walk |

---

## Limitations

This annex is a public-domain navigation aid. DORA compliance requires regulator-specific reporting, contractual language verified against Article 30, evidence at the granularity required by RTS and ITS, and supervisory engagement. Adopting financial entities consult the regulation, the published RTS and ITS, and the ESA and competent-authority guidance applicable to their entity type. This annex is not legal advice and does not establish compliance.

---

**End of Document**
