# Third-Party and Supply Chain Risk Standard

**Document Title:** Third-Party and Supply Chain Risk Standard 
**Document Type:** Standard 
**Version:** 1.0.0 
**Date:** 2026-05-27 
**Owner:** Chief Risk Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`risk/README.md`](README.md), [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md), [`risk/template-enterprise-risk-register.md`](template-enterprise-risk-register.md), [`risk/procedure-risk-assessment-methodology.md`](procedure-risk-assessment-methodology.md), [`supply-chain/standard-third-party-risk.md`](../supply-chain/standard-third-party-risk.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../supply-chain/framework-supplier-and-cloud-governance.md), [`supply-chain/procedure-supplier-due-diligence.md`](../supply-chain/procedure-supplier-due-diligence.md), [`supply-chain/procedure-supplier-audit.md`](../supply-chain/procedure-supplier-audit.md), [`compliance/policy-compliance-and-audit-management.md`](../compliance/policy-compliance-and-audit-management.md), [`governance/policy-governance-and-risk-management.md`](../governance/policy-governance-and-risk-management.md) 
**Classification:** Public 
**Category:** Risk Management: Third-Party and Supply Chain 
**Review Frequency:** Annual and upon material supply chain change, significant third-party incident, or regulatory update 
**Repository Path:** [`risk/standard-third-party-and-supply-chain-risk.md`](standard-third-party-and-supply-chain-risk.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This standard defines the enterprise risk management requirements for identifying, assessing, treating, and monitoring risks arising from third-party relationships and supply chain dependencies. It complements the operational supplier governance procedures in the supply-chain domain by establishing the risk management lens through which all third-party and supply chain risks are evaluated, escalated, and reported.

---

## Scope

This standard applies to all third-party relationships including:

- Logistics and freight service providers
- Technology and software vendors
- Cloud service providers
- Managed service providers
- Professional services and consultants
- Data processors and subprocessors
- Critical infrastructure and utilities
- Trade compliance and customs agents
- Subcontractors and second-tier suppliers with material operational impact

---

## Risk classification

All third-party relationships must be classified into one of the following tiers at onboarding and reassessed at least annually.

| Tier | Classification | Criteria | Review Frequency |
|---|---|---|---|
| **Tier 1: Critical** | Single point of failure; direct access to sensitive data or critical systems; regulatory or trade compliance dependency; revenue impact if unavailable | Processes personal data at scale; sole-source provider; no contractual substitute; CTPAT / AEO-S / BASC dependency | Quarterly |
| **Tier 2: High** | Significant operational dependency; access to systems or data; material revenue or compliance impact if unavailable | Provides important but substitutable services; processes limited personal data; available alternatives exist | Semi-annually |
| **Tier 3: Moderate** | Indirect operational dependency; limited data access; manageable impact if unavailable | Commercial relationships without system integration; standard commoditized services | Annually |
| **Tier 4: Low** | Minimal operational dependency; no data access; low impact if relationship ends | Transactional suppliers; easily substituted; no integration | At renewal or every 2 years |

---

## Risk assessment requirements

### 1. Due diligence assessment

All Tier 1 and Tier 2 third parties must complete a due diligence assessment before onboarding. Due diligence must evaluate the following risk domains:

| Risk Domain | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---|---|---|---|
| Financial solvency and business viability | Full assessment | Full assessment | Abbreviated | Not required |
| Information security posture | Full assessment with evidence | Full assessment | Self-attestation | Not required |
| Privacy and data protection compliance | Full assessment | Full assessment | If applicable | Not required |
| Business continuity and resilience capability | Full assessment | Full assessment | Abbreviated | Not required |
| Trade compliance programme membership (CTPAT / AEO-S / PIP / BASC where applicable) | Mandatory where in-scope | Mandatory where in-scope | Where applicable | Not required |
| AI systems in service delivery | Full AI due diligence | Assessment if AI-enabled | Not required | Not required |
| Sub-contractor and fourth-party dependencies | Required | Required | Where material | Not required |
| Legal, regulatory, and sanctions compliance | Mandatory | Mandatory | Abbreviated | Not required |

Operational procedures: [`supply-chain/procedure-supplier-due-diligence.md`](../supply-chain/procedure-supplier-due-diligence.md), [`supply-chain/procedure-third-party-ai-due-diligence.md`](../supply-chain/procedure-third-party-ai-due-diligence.md)

### 2. Risk scoring

Third-party risks are scored using the same 5×5 likelihood × impact matrix as enterprise risks. See [`risk/procedure-risk-assessment-methodology.md`](procedure-risk-assessment-methodology.md).

In addition to inherent and residual scores, third-party risk assessments must capture:
- **Concentration risk:** Degree to which multiple critical dependencies converge on a single supplier or geographic region
- **Fourth-party risk:** Key sub-dependencies of the third party that could cascade to the organization
- **Substitutability:** Estimated time and cost to replace the supplier if the relationship fails

### 3. Risk register integration

All Tier 1 third-party risks rated High or Critical must be entered into the enterprise risk register ([`risk/template-enterprise-risk-register.md`](template-enterprise-risk-register.md)) under the Supplier risk category. Tier 2 risks rated High should be entered. Lower-rated risks may be tracked in the operational supplier risk register ([`supply-chain/register-supplier-risk-template.md`](../supply-chain/register-supplier-risk-template.md)).

---

## Contract requirements

All contracts with third parties must include risk-aligned provisions. Minimum contract clauses by tier:

| Clause Type | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---|---|---|---|
| Security and privacy obligations | Full clause set | Full clause set | Abbreviated | Standard T&Cs |
| Audit and inspection rights | Right to audit and request audit reports | Right to audit reports | Where applicable | Not required |
| Incident notification requirements | 24-hour notification of material incidents | 24-hour notification | 72-hour notification | Standard |
| Business continuity requirements | Documented BCP; tested annually | Documented BCP | Where applicable | Not required |
| Sub-contractor approval | Written consent required | Written consent required | Notification | Not required |
| Data return and deletion on exit | Mandatory; timelines defined | Mandatory | Mandatory if data shared | Not required |
| Trade compliance programme membership | Mandatory for in-scope logistics | Mandatory where applicable | Where applicable | Not required |
| Right to terminate for cause | Mandatory | Mandatory | Mandatory | Standard |
| Liability and indemnification | Negotiated; minimum defined | Negotiated; minimum defined | Standard | Standard |

---

## Ongoing monitoring

### Tier 1 and tier 2 monitoring requirements

Continuous or periodic monitoring activities for critical and high-tier third parties:

| Activity | Tier 1 Frequency | Tier 2 Frequency | Method |
|---|---|---|---|
| Financial health check | Quarterly | Semi-annually | Credit reports; financial statements |
| Security posture review | Quarterly | Semi-annually | Updated questionnaire; security ratings service |
| Incident and breach notification review | Ongoing, trigger-based | Ongoing, trigger-based | Incident reports; threat intelligence |
| Trade compliance status verification | Annually; on renewal | Annually | CBP/HMRC/CBSA verification portals |
| Contractual obligation compliance | Quarterly | Semi-annually | SLA reporting; invoice review |
| Fourth-party (sub-contractor) monitoring | Semi-annually | Annually | Sub-contractor disclosure; spot checks |
| Business continuity test participation | Annually | Where applicable | Joint continuity exercises |

Procedures: [`supply-chain/procedure-supplier-ongoing-monitoring.md`](../supply-chain/procedure-supplier-ongoing-monitoring.md)

### Concentration risk monitoring

The Chief Risk Officer must maintain visibility of concentration risk across the supplier portfolio:

- No single Tier 1 supplier should represent more than the Board-approved concentration threshold for any single service category
- Geographic concentration in critical freight lanes must be assessed annually
- Technology concentration (e.g., single cloud provider hosting multiple critical systems) must be documented and managed

---

## Supply chain continuity risk

For all Tier 1 suppliers and critical trade lanes, a supply chain continuity risk assessment must be completed as part of the business impact analysis process:

| Assessment Element | Requirement |
|---|---|
| Single-source dependency identification | Document all sole-source Tier 1 suppliers; escalate to Board where no alternative exists |
| Substitute and alternate source identification | Identify pre-qualified alternates for all Tier 1 and Tier 2 suppliers |
| Geographic diversification | Assess exposure to single-country or single-region supply chain disruption |
| Critical freight lane resilience | Assess alternative routing for all critical freight lanes |
| Supplier financial distress early warning | Define indicators that trigger contingency planning activation |

Reference: [`supply-chain/annex-trade-and-supply-chain-continuity-controls.md`](../supply-chain/annex-trade-and-supply-chain-continuity-controls.md)

---

## Incident and breach management

### Supplier security incident response

When a Tier 1 or Tier 2 supplier experiences a security incident or data breach that may affect the organization:

1. Require the supplier to notify the organization within the contractually defined notification window
2. Initiate the supplier incident assessment within 4 hours of notification
3. Evaluate whether the incident triggers the organization's own incident response obligations (regulatory notification, customer notification)
4. Escalate to the enterprise incident response team if the incident affects the organization's systems or data: follow [`resilience/procedure-incident-response.md`](../resilience/procedure-incident-response.md)
5. Document the incident in the supplier's risk record; reassess residual risk rating
6. Initiate a CAPA if the incident reveals systemic control gaps: [`compliance/procedure-capa.md`](../compliance/procedure-capa.md)

### Supplier exit triggered by incident or performance failure

Where an incident or performance failure necessitates terminating a supplier relationship, initiate the supplier exit procedure: [`supply-chain/procedure-supplier-exit-and-data-return.md`](../supply-chain/procedure-supplier-exit-and-data-return.md).

---

## Reporting

| Report | Frequency | Audience |
|---|---|---|
| Tier 1 supplier risk summary | Quarterly | Chief Risk Officer; executive leadership |
| Supply chain concentration risk report | Annually | Board / Risk Committee |
| Third-party incident report | As triggered | Executive leadership; Board (if material) |
| Trade compliance programme status | Annually | Chief Compliance Officer |
| Enterprise risk register update (Supplier category) | Quarterly | Chief Risk Officer |

---

## Framework alignment

| Framework | Relevant Section |
|---|---|
| ISO 27001:2022 | A.5.19 to A.5.22 Information security in supplier relationships |
| ISO 28000 | Supply chain security management; risk and threat assessment |
| NIST SP 800-53 Rev 5 | SA-9 External System Services; SR Supply Chain Risk Management |
| NIST CSF 2.0 | GV.SC Supply Chain Risk Management; ID.SC Supply Chain Cybersecurity |
| WCO SAFE Framework | Pillar 2: Customs-to-Business partnerships; supply chain security standards |
| CTPAT | Business Partner Requirements; IT security requirements for partners |
| AEO-S (UK) | Criterion 1(e): Practical standards of competence including partner management |

---

**End of Document**
