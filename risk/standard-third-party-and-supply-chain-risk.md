# Third-Party and Supply Chain Risk Standard

**Document Title:** Third-Party and Supply Chain Risk Standard 
**Document Type:** Standard 
**Version:** 1.1.0 
**Date:** 2026-05-28 
**Owner:** Chief Risk Officer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`risk/README.md`](README.md), [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md), [`risk/template-enterprise-risk-register.md`](template-enterprise-risk-register.md), [`risk/procedure-risk-assessment-methodology.md`](procedure-risk-assessment-methodology.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../supply-chain/framework-supplier-and-cloud-governance.md), [`supply-chain/procedure-supplier-due-diligence.md`](../supply-chain/procedure-supplier-due-diligence.md), [`supply-chain/procedure-supplier-audit.md`](../supply-chain/procedure-supplier-audit.md), [`supply-chain/procedure-supplier-ongoing-monitoring.md`](../supply-chain/procedure-supplier-ongoing-monitoring.md), [`supply-chain/procedure-supplier-exit-and-data-return.md`](../supply-chain/procedure-supplier-exit-and-data-return.md), [`supply-chain/procedure-third-party-ai-due-diligence.md`](../supply-chain/procedure-third-party-ai-due-diligence.md), [`compliance/policy-compliance-and-audit-management.md`](../compliance/policy-compliance-and-audit-management.md), [`risk/policy-enterprise-governance-and-risk-management.md`](../risk/policy-enterprise-governance-and-risk-management.md) 
**Classification:** Public 
**Category:** Risk Management: Third-Party and Supply Chain 
**Review Frequency:** Annual and upon material supply chain change, significant third-party incident, or regulatory update 
**Repository Path:** [`risk/standard-third-party-and-supply-chain-risk.md`](standard-third-party-and-supply-chain-risk.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This standard defines the framework, methodology, and control requirements for identifying, assessing, treating, and monitoring risks arising from third-party relationships and supply chain dependencies. It is the master third-party and supply-chain risk standard for the library: the enterprise risk-management lens, the lifecycle expectations, and the contracting controls are all defined here. Operational procedures in the supply-chain domain implement the lifecycle steps; this standard governs them.

This standard supersedes the prior `supply-chain/standard-third-party-risk.md` (removed in the same change). All cross-references previously pointing at that document point here.

---

## Scope

This standard applies to all third-party relationships involving access to the organisation's data, systems, networks, facilities, or operational continuity, including:

- Logistics and freight service providers
- Technology and software vendors
- Cloud service providers
- Managed service providers
- Professional services and consultants
- Data processors and subprocessors
- AI model, data, and inference-service suppliers
- Critical infrastructure and utilities
- Trade compliance and customs agents
- Subcontractors and second-tier suppliers with material operational impact

The standard applies globally across all business units and regional operations and covers the full supplier lifecycle from onboarding to contract termination, including subcontractors engaged by third parties.

---

## Risk classification

All third-party relationships must be classified into one of the following tiers at onboarding and reassessed at least annually.

| Tier | Classification | Criteria | Review Frequency |
|---|---|---|---|
| **Tier 1: Critical** | Single point of failure; direct access to sensitive data or critical systems; regulatory or trade-compliance dependency; revenue impact if unavailable; AI model or training-data supply for high-risk AI systems | Processes personal data at scale; sole-source provider; no contractual substitute; CTPAT / AEO-S / BASC dependency where the organisation participates | Quarterly |
| **Tier 2: High** | Significant operational dependency; access to systems or data; material revenue or compliance impact if unavailable; cloud or key service dependencies | Provides important but substitutable services; processes limited personal data; available alternatives exist | Semi-annually |
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
- **Fourth-party risk:** Key sub-dependencies of the third party that could cascade to the organisation
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
| Trade compliance programme membership | Mandatory for in-scope logistics where the organisation participates | Mandatory where applicable | Where applicable | Not required |
| Right to terminate for cause | Mandatory | Mandatory | Mandatory | Standard |
| Liability and indemnification | Negotiated; minimum defined | Negotiated; minimum defined | Standard | Standard |

### AI service-provider contract requirements

For third parties providing AI models, inference services, training data, or other AI capabilities, contracts must additionally require:

- Dataset lineage documentation demonstrating data provenance.
- Model validation and explainability evidence per ISO/IEC 42001 §9.
- Assurance of ethical data sourcing and absence of prohibited training data.
- No-training-on-customer-data commitment unless explicit opt-in is documented, per the AI vendor security questionnaire.
- Notice period for material model behaviour changes; the provider's deprecation policy.
- Cross-border data-transfer mechanism per the privacy framework.

See [`ai/template-ai-vendor-security-questionnaire.md`](../ai/template-ai-vendor-security-questionnaire.md) and [`ai/procedure-foundation-model-lifecycle.md`](../ai/procedure-foundation-model-lifecycle.md) for the operational vehicle.

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

Monitoring is supported by:

- A Third-Party Risk Assessment Questionnaire (TPRAQ) re-issued per the cadence above.
- Security-rating and threat-intelligence services where the cost-benefit profile justifies.
- SLA compliance tracking and incident-reporting metrics.
- Vulnerability scanning results and audit attestation reviews.

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

When a Tier 1 or Tier 2 supplier experiences a security incident or data breach that may affect the organisation:

1. Require the supplier to notify the organisation within the contractually defined notification window
2. Initiate the supplier incident assessment within 4 hours of notification
3. Evaluate whether the incident triggers the organisation's own incident response obligations (regulatory notification, customer notification)
4. Escalate to the enterprise incident response team if the incident affects the organisation's systems or data: follow [`resilience/procedure-cross-domain-incident-coordination.md`](../resilience/procedure-cross-domain-incident-coordination.md)
5. Document the incident in the supplier's risk record; reassess residual risk rating
6. Initiate a CAPA if the incident reveals systemic control gaps: [`compliance/procedure-capa.md`](../compliance/procedure-capa.md)

### Supplier exit triggered by incident or performance failure

Where an incident or performance failure necessitates terminating a supplier relationship, initiate the supplier exit procedure: [`supply-chain/procedure-supplier-exit-and-data-return.md`](../supply-chain/procedure-supplier-exit-and-data-return.md).

---

## Offboarding and contract termination

Upon contract termination or expiry, the third party must:

1. Return or securely delete all organisational data in accordance with the contracted retention schedule.
2. Revoke all system access credentials within 24 hours of termination.
3. Provide written confirmation of data destruction or return.
4. Transfer or destroy any model artefacts, embeddings, fine-tuned weights, or evaluation data derived from the organisation's data, where the contract is AI-related.

Residual risks identified during offboarding must be reviewed, documented, and logged in the appropriate risk register for closure validation. The supplier offboarding evidence template ([`supply-chain/template-supplier-offboarding-evidence.md`](../supply-chain/template-supplier-offboarding-evidence.md)) records the evidence collected.

The full offboarding workflow is described in [`supply-chain/procedure-supplier-exit-and-data-return.md`](../supply-chain/procedure-supplier-exit-and-data-return.md).

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
| ISO/IEC 27036-3:2013 | Information security for supplier relationships: ICT supply chain security |
| ISO 28000 | Supply chain security management; risk and threat assessment |
| NIST SP 800-53 Rev 5 | SA-9 External System Services; SR Supply Chain Risk Management |
| NIST SP 800-161r2 | Cybersecurity Supply Chain Risk Management Practices for Systems and Organisations |
| NIST CSF 2.0 | GV.SC Supply Chain Risk Management; ID.SC Supply Chain Cybersecurity |
| COBIT 2019 | APO10 Managed Vendors |
| CSA CCM v4.1 | STA-02 Supply Chain Management, Transparency, and Accountability |
| WCO SAFE Framework | Pillar 2: Customs-to-Business partnerships; supply chain security standards |
| CTPAT | Business Partner Requirements; IT security requirements for partners |
| AEO-S (UK) | Criterion 1(e): Practical standards of competence including partner management |

---

**End of Document**
