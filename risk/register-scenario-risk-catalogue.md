# Scenario Risk Catalogue

**Document Title:** Scenario Risk Catalogue\
**Document Type:** Register\
**Version:** 0.0.1\
**Date:** 2026-05-28\
**Owner:** Chief Risk Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md), [`risk/template-enterprise-risk-register.md`](template-enterprise-risk-register.md), [`risk/template-operational-risk-register.md`](template-operational-risk-register.md), [`risk/guideline-quantitative-risk-analysis.md`](guideline-quantitative-risk-analysis.md), [`resilience/template-tabletop-exercise.md`](../resilience/template-tabletop-exercise.md), [`resilience/framework-business-continuity-and-resilience.md`](../resilience/framework-business-continuity-and-resilience.md), [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md)\
**Classification:** Public\
**Category:** Risk Management\
**Review Frequency:** Annual and upon material change to the threat or business environment\
**Repository Path:** [`risk/register-scenario-risk-catalogue.md`](register-scenario-risk-catalogue.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This catalogue lists scenarios used for scenario-based risk analysis, stress testing, tabletop exercises, business-continuity testing, and resilience assurance. Each scenario is a plausible adverse event that exercises the organisation's controls, response, and recovery posture.

The catalogue is the source from which scenario tests are scheduled. It complements the enterprise and operational risk registers (which list risks) and the tabletop exercise template (which structures a single exercise).

---

## Scope

The catalogue covers scenarios that:

1. Could materially affect customer service delivery.
2. Could materially affect financial performance.
3. Could materially affect regulatory standing.
4. Stress controls in ways that frequency-based loss data does not capture.
5. Stress organisational coordination across teams, suppliers, and regulators.

It does not catalogue every conceivable incident; it catalogues a curated set chosen to exercise different control areas across a rolling window.

---

## Catalogue structure

Each scenario in the catalogue has:

| Field | Description |
| --- | --- |
| Scenario identifier | Unique identifier in the catalogue |
| Scenario title | Short descriptive title |
| Scenario class | Per the classification below |
| Scenario narrative | Plausible narrative; cause-event-effect with timeline |
| Plausibility rating | Tail, plausible, frequent |
| Severity assumption | Range of severity values used for testing |
| Affected functions | The business and operational functions exercised |
| Affected systems | The systems exercised |
| Affected suppliers | The suppliers exercised |
| Linked risks | Identifiers from the enterprise and operational risk registers |
| Controls exercised | The controls the scenario stresses |
| Recovery objectives exercised | The RTO, RPO, RTA targets stressed |
| Regulatory expectation | Where a regulator requires the scenario (e.g. financial-services severe-but-plausible) |
| Last used | Date last exercised |
| Next due | When the next exercise is scheduled |
| Owner | Person accountable for keeping the scenario current |
| Notes | Free-text context |

---

## Scenario classes

| Class | Description |
| --- | --- |
| Cyber attack | Ransomware, destructive intrusion, data exfiltration, supply-chain compromise, account takeover, insider misuse |
| AI-specific | Model-driven decision failure, prompt-injection cascade, agentic-tool misuse, training-data poisoning, model-provider failure, deepfake-driven fraud |
| Technology failure | Infrastructure failure, cloud-provider regional impairment, database corruption, deployment failure, certificate expiry, identity-provider outage |
| Supplier failure | Critical supplier insolvency, critical supplier exit, critical supplier security incident, fourth-party cascade |
| People and conduct | Senior departure, key-person incapacitation, mass departure, insider fraud, harassment incident, whistleblower disclosure |
| External event | Natural disaster, pandemic, civil disturbance, geopolitical sanction, power outage, telecommunications failure |
| Financial market | Liquidity squeeze, currency shock, counterparty failure, capital-markets disruption |
| Regulatory | New regulation, regulatory enforcement, cross-border data-flow restriction, ex parte injunction |
| Reputational | Adverse media campaign, customer-data breach disclosure, executive misconduct disclosure |
| Climate-related | Acute climate event, chronic climate transition disruption |
| Concurrent | Combination of two or more of the above (e.g. cyber incident during regional outage) |

---

## Reference scenario set

This reference set is illustrative; adopting organisations replace entries with their own.

### Cyber attack

| Identifier | Scenario |
| --- | --- |
| SCN-CYB-001 | Ransomware encrypts critical production systems; backups partially compromised |
| SCN-CYB-002 | Destructive wiper executed via a software-supply-chain compromise |
| SCN-CYB-003 | Multi-tenant cloud provider control-plane intrusion exposing organisational tenants |
| SCN-CYB-004 | Identity-provider compromise enabling lateral movement across SaaS estate |
| SCN-CYB-005 | Insider exfiltrates customer dataset via legitimate access path |
| SCN-CYB-006 | Adversary-in-the-middle bypasses MFA via phishing for high-privilege account |
| SCN-CYB-007 | Critical zero-day vulnerability in an internet-facing product with no patch available |
| SCN-CYB-008 | Long-running, low-and-slow intrusion discovered after months of presence |
| SCN-CYB-009 | DDoS coincident with a planned product launch |
| SCN-CYB-010 | Supply-chain compromise of a code-signing key used by a vendor |

### AI-specific

| Identifier | Scenario |
| --- | --- |
| SCN-AI-001 | Foundation-model provider deprecates model with insufficient notice; downstream services disrupted |
| SCN-AI-002 | Provider-side safety classifier change materially changes customer-facing model behaviour |
| SCN-AI-003 | Prompt-injection cascade enables an agent to leak sensitive data to an attacker |
| SCN-AI-004 | Agentic tool invocation initiates a downstream financial action without proper authorisation |
| SCN-AI-005 | Training-data leak exposes customer-confidential content to a public model |
| SCN-AI-006 | Adversarial dataset poisoning degrades model quality in production |
| SCN-AI-007 | Cost-runaway event exhausts AI inference budget and rate limits |
| SCN-AI-008 | Deepfake-based fraud targets a senior executive |
| SCN-AI-009 | Regulatory finding requires a foundation model to be withdrawn from a jurisdiction |
| SCN-AI-010 | Model provider becomes subject to a restricted-list designation |

### Technology failure

| Identifier | Scenario |
| --- | --- |
| SCN-TEC-001 | Cloud-provider regional outage exceeding the recovery objective |
| SCN-TEC-002 | Database corruption silent for several days; backups partly affected |
| SCN-TEC-003 | Mass certificate expiry due to lapsed renewal automation |
| SCN-TEC-004 | Identity-provider outage prevents authentication across the SaaS estate |
| SCN-TEC-005 | Critical platform service silently degraded; impact detected via customer complaints |
| SCN-TEC-006 | Network-segmentation failure exposes internal services |
| SCN-TEC-007 | Production deployment introduces a data-loss defect |
| SCN-TEC-008 | DNS or registrar compromise misroutes traffic |

### Supplier failure

| Identifier | Scenario |
| --- | --- |
| SCN-SUP-001 | Critical SaaS supplier becomes insolvent with limited notice |
| SCN-SUP-002 | Critical supplier suffers a destructive cyber incident |
| SCN-SUP-003 | Critical supplier is acquired by a restricted-list buyer |
| SCN-SUP-004 | Critical supplier's fourth party suffers a regional outage that cascades |
| SCN-SUP-005 | Provider data-residency change forces unplanned migration |

### People and conduct

| Identifier | Scenario |
| --- | --- |
| SCN-PPL-001 | Sudden incapacitation of a key person controlling a critical system |
| SCN-PPL-002 | Coordinated departure of a critical engineering team |
| SCN-PPL-003 | Insider fraud discovered via a whistleblower disclosure |
| SCN-PPL-004 | High-profile harassment or misconduct allegation against a senior executive |
| SCN-PPL-005 | Strike or industrial action affecting an operational team |

### External event

| Identifier | Scenario |
| --- | --- |
| SCN-EXT-001 | Natural disaster causing extended primary-site unavailability |
| SCN-EXT-002 | Pandemic causing extended workforce-distribution change |
| SCN-EXT-003 | National or regional telecommunications outage |
| SCN-EXT-004 | Long-duration power outage at a primary site |
| SCN-EXT-005 | Civil disturbance restricting site access |

### Financial market

| Identifier | Scenario |
| --- | --- |
| SCN-FIN-001 | Counterparty default disrupting receivables |
| SCN-FIN-002 | Currency shock affecting cost base or revenue |
| SCN-FIN-003 | Liquidity squeeze affecting short-term operations |

### Regulatory

| Identifier | Scenario |
| --- | --- |
| SCN-REG-001 | New regulation triggers a short-window compliance project |
| SCN-REG-002 | Cross-border data-flow restriction requires rapid architectural change |
| SCN-REG-003 | Regulatory enforcement action with a public component |
| SCN-REG-004 | Mandatory incident reporting deadline tested under load |
| SCN-REG-005 | Sectoral resilience exercise mandated by a regulator |

### Reputational

| Identifier | Scenario |
| --- | --- |
| SCN-REP-001 | Adverse media campaign about product quality or safety |
| SCN-REP-002 | Customer-data breach disclosure with high media attention |
| SCN-REP-003 | Executive misconduct disclosure |
| SCN-REP-004 | Coordinated social-media campaign against the organisation |

### Climate-related

| Identifier | Scenario |
| --- | --- |
| SCN-CLM-001 | Acute climate event affecting a primary operating region |
| SCN-CLM-002 | Chronic climate-driven supplier disruption |
| SCN-CLM-003 | Regulatory disclosure failure on climate-related risk |

### Concurrent

| Identifier | Scenario |
| --- | --- |
| SCN-CON-001 | Cyber incident during a regional cloud outage |
| SCN-CON-002 | Pandemic plus a supplier failure plus a regulatory deadline |
| SCN-CON-003 | Identity-provider outage during a peak-traffic event |
| SCN-CON-004 | Critical-key-person incapacitation during a cyber incident |

---

## Severity calibration

Each scenario is exercised at one or more severity levels. The severity calibration is:

| Severity | Description |
| --- | --- |
| Moderate | Plausible bad day; exercises routine response |
| Severe-but-plausible | A bad outcome that the organisation should still be able to manage |
| Extreme | A tail scenario that exercises the limits of the organisation's response |

For regulated organisations, the severe-but-plausible level aligns with operational resilience regulatory expectations.

---

## Use of the catalogue

| Use | Description |
| --- | --- |
| Risk assessment | Scenarios inform impact assumptions in the enterprise and operational risk registers |
| Stress testing | Used in scenario stress testing per the risk methodology |
| Tabletop exercises | Selected scenarios scheduled per the resilience programme |
| Business-continuity testing | Selected scenarios drive continuity-plan tests per the resilience programme |
| Cyber exercises | Selected scenarios drive red-team and purple-team engagements per the penetration testing standard |
| Crisis-management exercises | Selected scenarios drive crisis-management exercises with leadership |
| Regulatory exercises | Selected scenarios used in TIBER-EU, CBEST, sector-specific tests where applicable |

---

## Catalogue maintenance

| Activity | Description |
| --- | --- |
| Annual review | Catalogue reviewed at least annually against threat-intelligence inputs and emerging-risk signals |
| Lessons feedback | Lessons learned from incidents and exercises update existing scenarios and add new ones |
| Horizon scanning | New scenarios proposed via the emerging-risk process |
| Retirement | Scenarios no longer plausible are retired with documented rationale |
| Coverage check | Annual coverage check confirms each control domain has at least one scenario stressing it |

---

## Operating expectations

1. The catalogue is exercised across a rolling window such that each scenario class is touched at least annually.
2. Each scenario has a named owner who keeps it current.
3. Scenario selection for any given exercise is documented; high-impact scenarios are prioritized.
4. The catalogue is reconciled against threat intelligence and incident history quarterly.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO 31000:2018 | Risk management principles | Risk management baseline |
| ISO 22301:2019 | Business continuity management | Continuity testing |
| ISO/IEC 27005:2022 | Information security risk management | Information-risk integration |
| Basel Committee Operational Resilience Principles | Severe-but-plausible scenarios | Operational resilience |
| Bank of England / PRA SS1/21 | Operational resilience for financial services | Severe-but-plausible expectations |
| DORA | Articles 24 to 27 (digital operational resilience testing) | EU financial services |
| TIBER-EU | Threat intelligence-based ethical red teaming | Cyber resilience testing |
| NIST CSF 2.0 | Govern, Identify, Detect, Respond, Recover | Risk function alignment |
| ENISA Guidelines | Cyber incident scenarios | EU baseline |

---

## Limitations

This catalogue is a CC BY-SA 4.0 baseline. Adopting organisations curate scenarios to their threat environment, regulatory expectations, sector profile, and customer base. The scenarios listed are illustrative and not exhaustive; new scenarios are added as the threat and business environment evolves.

---

**End of Document**
