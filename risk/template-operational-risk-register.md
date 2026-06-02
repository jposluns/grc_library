# Operational Risk Register Template

**Document Title:** Operational Risk Register Template\
**Document Type:** Template\
**Version:** 1.0.1\
**Date:** 2026-06-02\
**Owner:** Chief Risk Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md), [`risk/template-enterprise-risk-register.md`](template-enterprise-risk-register.md), [`risk/procedure-risk-register.md`](procedure-risk-register.md), [`risk/procedure-risk-assessment-methodology.md`](procedure-risk-assessment-methodology.md), [`risk/guideline-quantitative-risk-analysis.md`](guideline-quantitative-risk-analysis.md), [`risk/register-key-risk-indicators.md`](register-key-risk-indicators.md), [`risk/policy-enterprise-governance-and-risk-management.md`](policy-enterprise-governance-and-risk-management.md), [`operations/framework-it-service-management.md`](../operations/framework-it-service-management.md), [`resilience/framework-business-continuity-and-resilience.md`](../resilience/framework-business-continuity-and-resilience.md)\
**Classification:** Public\
**Category:** Risk Management\
**Review Frequency:** Annual and upon material change to risk methodology or business operations\
**Repository Path:** [`risk/template-operational-risk-register.md`](template-operational-risk-register.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template structures the operational risk register that an organisation maintains at the business-process and business-unit level. The operational risk register complements the enterprise risk register (which captures top-of-the-house risk) by capturing the risk-and-control state inside operational processes.

Operational risk is the risk of loss from inadequate or failed internal processes, people, and systems, or from external events. This template applies the Basel definition without limiting scope to financial services.

---

## Scope

The operational risk register applies to:

1. Business processes that produce, deliver, or support customer or operational outcomes.
2. Internal control activities that depend on those processes.
3. Operational events whose realisation would affect service delivery, regulatory standing, or financial result.

It does not duplicate the enterprise risk register; it feeds into it via aggregation and escalation.

---

## Template structure

### Section A: register identification

| Field | Description |
| --- | --- |
| Register name | The name of this register instance |
| Business unit or process scope | The unit, process, or product the register covers |
| Register owner | The person accountable for the register's accuracy and currency |
| Register administrator | The person who maintains the register day-to-day |
| Review cadence | At least quarterly for active operations; more frequently for high-volatility units |
| Last review date | Most recent material review |
| Next review due | The date the next review is required |
| Version | Register version |
| Approval | Senior accountable owner sign-off |

### Section B: scope and assumptions

| Field | Description |
| --- | --- |
| Process map reference | Pointer to the process map(s) the register covers |
| Inclusion criteria | What is included in this register |
| Exclusion criteria | What is intentionally out of scope |
| Assumptions | Material assumptions underpinning the risk assessment |
| Risk appetite reference | The risk appetite statement applicable to this scope |
| Tolerance reference | Operational tolerances applicable to this scope |

### Section C: risk entries

Each operational risk entry has the following fields:

| Field | Description |
| --- | --- |
| Risk identifier | Unique identifier within the register |
| Risk title | Short descriptive title |
| Risk description | The risk expressed as cause-event-effect |
| Risk taxonomy | Per the organisation's operational risk taxonomy (see Section D) |
| Risk owner | The person accountable for managing the risk |
| Process or activity affected | The process or activity in scope |
| Inherent likelihood | Per the assessment scale |
| Inherent impact | Per the assessment scale |
| Inherent rating | Likelihood and impact combined |
| Existing controls | Controls operating today |
| Control effectiveness | Effective, partially effective, or ineffective; rationale recorded |
| Residual likelihood | After existing controls |
| Residual impact | After existing controls |
| Residual rating | Combined residual rating |
| Treatment decision | Accept, mitigate, transfer, avoid |
| Treatment plan | Where mitigation is selected, the action plan |
| Treatment owner | The person accountable for treatment delivery |
| Treatment target date | When the treatment is expected to be effective |
| Linked enterprise risk | Where this risk aggregates upward, the linked enterprise risk identifier |
| Linked controls | Control identifiers from the control register |
| Linked KRIs | Key risk indicators that monitor this risk |
| Status | Open, monitoring, closed |
| Last updated | Date of last material update |
| Comments | Free-text context |

### Section D: operational risk taxonomy

The taxonomy below is consistent with the Basel operational risk event categorisation, expressed in vendor-neutral terms.

| Top-level category | Examples |
| --- | --- |
| Internal fraud | Misappropriation; abuse of authority; tax non-compliance |
| External fraud | Theft; system intrusion; fraudulent customer activity |
| Employment practices and workplace safety | Health and safety; discrimination; harassment |
| Clients, products, and business practices | Mis-selling; fiduciary breach; product defects |
| Damage to physical assets | Natural disaster; vandalism; terrorism |
| Business disruption and system failures | Application outage; infrastructure failure; supplier failure; cyber incident |
| Execution, delivery, and process management | Transaction error; missed deadline; reporting error; data quality |
| Compliance and regulatory | Regulatory breach; reporting failure; sanctions breach |
| Information and cyber | Per the security framework |
| Third party and supplier | Per the third-party risk standard |
| AI-specific operational risk | Per the AI risk methodology annex |
| Conduct | Per the conduct or ethics framework |
| Climate-related operational | Acute and chronic climate-related events; per the climate risk framework where applicable |

### Section E: assessment scales

The likelihood and impact scales use the organisation's risk methodology. For consistency, this template proposes the following ordinal scales; adopting organisations may calibrate or replace them.

| Likelihood | Description |
| --- | --- |
| Very low | Event not expected within the planning horizon |
| Low | Could occur but unlikely; would be unusual |
| Moderate | Could occur occasionally |
| High | Likely to occur within the planning horizon |
| Very high | Expected to occur, possibly more than once |

| Impact | Description |
| --- | --- |
| Negligible | No measurable effect on service or financial result |
| Minor | Localised effect; short-duration |
| Moderate | Material effect on a business unit or function |
| Major | Material effect across business units; regulatory attention possible |
| Severe | Existential impact; significant regulatory or reputational consequence |

For quantitative assessments, the FAIR-aligned guideline supplies a quantitative model.

### Section F: control linkage

Each risk entry references controls in the control register. Controls are characterised by:

| Field | Description |
| --- | --- |
| Control identifier | Unique identifier in the control register |
| Control type | Preventive, detective, corrective, directive |
| Control nature | Manual, semi-automated, automated |
| Control owner | The person accountable for the control's operation |
| Control frequency | How often the control operates |
| Test cadence | How often the control is tested |
| Last test result | Pass, partial, fail; with date |
| Linked assurance | Internal audit, external audit, second-line review reference |

### Section G: scenario and emerging risk linkage

| Field | Description |
| --- | --- |
| Linked scenario | Identifier in the scenario risk catalogue |
| Emerging-risk signals | Signals being tracked that may materialise the risk |
| Horizon-scanning source | Where signals are sourced |

### Section H: loss events and near-misses

| Field | Description |
| --- | --- |
| Event identifier | Unique identifier for the event |
| Event date | Date the event occurred or was identified |
| Event description | What happened |
| Linked risk identifier | The risk this event materialises |
| Direct loss | Financial impact realised |
| Indirect loss | Other realised impact (regulatory, reputational, customer) |
| Near-miss indicator | Whether this was a near-miss rather than a realised event |
| Root cause | Per the post-incident review |
| Corrective actions | Actions taken |
| Linked incident or post-incident review | Reference to the incident response procedure record |

### Section I: aggregation, reporting, and escalation

| Activity | Description |
| --- | --- |
| Aggregation rules | How operational risk entries roll up to enterprise risk entries |
| Reporting cadence | Quarterly to operational management; selected items reported to the risk committee |
| Escalation triggers | Conditions that prompt escalation (e.g. rating change, control failure, KRI breach) |
| Heatmap | Aggregated heatmap by category produced for management |
| Trend analysis | Rating trend and event-frequency trend reviewed quarterly |
| Customer-facing impact summary | Where operational risk materialises in customer impact, recorded for the resilience programme |

### Section J: integration

| Programme | Integration point |
| --- | --- |
| Enterprise risk management | Aggregation upward via linked enterprise risk identifier |
| Internal control framework | Risks linked to controls; control effectiveness informs residual rating |
| Internal audit | Audit findings inform risk re-assessment |
| Resilience programme | Severity 1 and 2 risks coordinated with the business continuity programme |
| Incident management | Incidents linked back to the risk(s) they materialise |
| KRI register | KRIs that monitor this risk |
| Assurance map | Coverage of risks by lines of defence |
| Board reporting | Top operational risks summarised in the board risk report |

---

## Worked example (illustrative; not a real entry)

The example below illustrates a single risk entry. Adopting organisations replace it with their own entries.

| Field | Example value |
| --- | --- |
| Risk identifier | OPRR-PMT-014 |
| Risk title | Payment-processor outage degrading checkout availability |
| Risk description | Cause: critical-path payment processor failure. Event: checkout traffic cannot complete. Effect: lost revenue and customer dissatisfaction |
| Risk taxonomy | Business disruption and system failures; third party |
| Risk owner | Head of Payments Engineering |
| Process or activity affected | Customer checkout |
| Inherent likelihood | Moderate |
| Inherent impact | Major |
| Inherent rating | High |
| Existing controls | Multi-processor routing; processor-failover automation; runbook; provider monitoring |
| Control effectiveness | Partially effective; multi-processor tested at quarter-end |
| Residual likelihood | Low |
| Residual impact | Moderate |
| Residual rating | Moderate |
| Treatment decision | Mitigate |
| Treatment plan | Add second-line failover provider; complete by Q3 |
| Linked enterprise risk | ERR-OPS-003 (revenue continuity) |
| Linked controls | CTL-PMT-014a, CTL-PMT-014b |
| Linked KRIs | KRI-PMT-002 (provider availability); KRI-PMT-004 (failover test pass rate) |
| Status | Open |

---

## Operating expectations

1. The register is reviewed at least quarterly with the risk owner; high-risk entries reviewed more frequently.
2. All material loss events are captured even when the inherent risk was not previously recorded; the register is updated accordingly.
3. The register is the source of operational-risk reporting; ad-hoc reports reconcile to the register.
4. Updates flow into the enterprise risk register, the KRI register, the assurance map, and board reporting.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO 31000:2018 | Risk management principles and guidelines | Risk management baseline |
| ISO/IEC 27005:2022 | Information security risk management | Cross-walk to information risk |
| COSO ERM 2017 | Enterprise risk management | Enterprise risk integration |
| Basel Committee Operational Risk Principles | Operational risk taxonomy | Operational risk framework |
| ORX Reference Taxonomy | Operational risk event types | Industry taxonomy |
| FAIR | Factor analysis of information risk | Quantitative method |
| COBIT 2019 | EDM03 risk optimization objective | Governance of enterprise IT |
| NIST CSF 2.0 | Govern function | Risk integration |

---

## Limitations

This template is a CC BY-SA 4.0 baseline. Adopting organisations calibrate the scales, taxonomy depth, and reporting cadence to their size and regulatory profile. The template does not replace specialist risk-domain methodologies (information risk, supplier risk, AI risk) that have their own registers and methodologies cross-referenced here.

---

**End of Document**
