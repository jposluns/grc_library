# Assurance Map Register

**Document Title:** Assurance Map Register\
**Document Type:** Register\
**Version:** 1.1.2\
**Date:** 2026-07-02\
**Owner:** Chief Risk Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`risk/policy-enterprise-governance-and-risk-management.md`](policy-enterprise-governance-and-risk-management.md), [`risk/standard-enterprise-risk-management.md`](standard-enterprise-risk-management.md), [`risk/template-enterprise-risk-register.md`](template-enterprise-risk-register.md), [`risk/template-operational-risk-register.md`](template-operational-risk-register.md), [`risk/template-board-risk-report.md`](template-board-risk-report.md), [`governance/framework-continuous-assurance-and-improvement.md`](../governance/framework-continuous-assurance-and-improvement.md), [`governance/register-role-authority.md`](../governance/register-role-authority.md), [`compliance/policy-compliance-and-audit-management.md`](../compliance/policy-compliance-and-audit-management.md)\
**Classification:** Public\
**Category:** Risk Management\
**Review Frequency:** Annual and upon material change to lines of defence, assurance providers, or risk methodology\
**Repository Path:** [`risk/register-assurance-map.md`](register-assurance-map.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register records, for each material risk, what assurance is in place and where the gaps are. It applies the three-lines model (and where adopted, the IIA's Three Lines Model 2020 update) by mapping risks against the activities of the first, second, and third lines of defence and against external assurance.

The board, the audit committee, and the risk committee use the map to confirm that material risks are subject to proportionate, independent, and effective assurance, and that significant gaps are deliberate and time-bound.

---

## Scope

The assurance map covers:

1. Top enterprise risks per the enterprise risk register.
2. Material operational risks per the operational risk register.
3. Compliance obligations per the compliance and audit management policy.
4. Critical controls per the control register.
5. Customer-impact services per the resilience programme.

It does not cover every individual control; it operates at the risk-area level and is supported by the control register.

---

## Section 1: lines of defence

| Line | Description |
| --- | --- |
| First line | Business and operations functions that own and execute controls |
| Second line | Specialist oversight functions: risk, compliance, information security, privacy, AI governance, legal |
| Third line | Internal audit; independent assurance |
| External | External audit, regulatory examination, supplier-attestation programmes, certification bodies |
| Customer-driven | Customer audits, customer security reviews |

Each line provides assurance through different mechanisms: control operation (first line), monitoring and challenge (second line), independent testing and opinion (third line), and external attestation (external).

---

## Section 2: register structure

Each entry in the assurance map has:

| Field | Description |
| --- | --- |
| Risk area identifier | Pointer to the enterprise or operational risk |
| Risk area title | Short descriptive title |
| Risk owner | Per the linked risk register |
| Linked controls | Control identifiers from the **adopter's own control register**. The library does not ship a control register because the control identifier scheme is necessarily adopter-defined (each organization's controls catalogue reflects its specific systems, vendors, and regulatory environment). The worked example below uses placeholder IDs in the form `CTL-IAM-001` to illustrate the field shape; adopters substitute their own scheme. A typical control register has columns: control ID, control statement, owner, frequency, evidence class, framework cross-reference. Adopters who do not yet have a control register can begin by extracting controls from their normative policies and standards into a flat register before populating the Linked-controls field here. |
| Linked obligations | Compliance obligations from the obligations register |
| First-line activity | What the first line does to manage the risk; cadence; evidence |
| Second-line activity | What the second line does; cadence; evidence |
| Third-line activity | Internal audit coverage; last audit; next audit |
| External activity | External attestations, regulator examinations, certifications |
| Customer-driven activity | Customer audits or reviews that exercise this area |
| Assurance level | Per the rating scale (see Section 5) |
| Coverage commentary | Brief narrative summarizing how the area is covered |
| Identified gaps | Where the rating is less than green, the gap |
| Gap treatment | Action and owner |
| Last assurance event | The most recent assurance activity touching this area |
| Next assurance event | The next scheduled activity |
| Linked KRIs | Indicators monitoring this area |
| Material change since last review | Significant changes affecting assurance |

---

## Section 3: domains the map covers

The map is structured around the following domains; each domain may contain multiple risk-area entries.

| Domain | Examples |
| --- | --- |
| Information security | Identity and access; vulnerability management; logging; incident response; encryption |
| Privacy | Personal-data handling; cross-border transfer; consent; data-subject rights |
| AI and machine learning | AI governance; foundation-model lifecycle; AI access; AI evaluation |
| Resilience and continuity | Business continuity; disaster recovery; supplier resilience; severe-but-plausible scenarios |
| Supplier and third-party | Onboarding; ongoing monitoring; offboarding; concentration |
| Financial control | Internal financial control; SOX ITGC where applicable |
| Compliance | Regulatory obligations; sector requirements |
| Conduct and ethics | Code of conduct; conflict of interest; whistleblower |
| Health and safety | Where applicable |
| Operational | Service delivery; capacity; release; change; incident |
| Strategic | Strategy execution; transformation programmes |
| Climate and sustainability | Where applicable |

---

## Section 4: activity-type taxonomy

To support consistency, the activities captured in each entry use the following taxonomy.

| Activity type | Description |
| --- | --- |
| Control operation | The control runs and produces evidence |
| Self-attestation | First-line owner attests to control operation |
| Management review | First-line management reviews evidence |
| Second-line monitoring | Second-line monitors and challenges |
| Second-line testing | Second-line tests control effectiveness |
| Independent assurance | Third-line independent testing |
| External audit | External auditor opinion |
| Certification | Independent certification (e.g. ISO 27001, ISO 42001, SOC 2 Type II) |
| Regulator examination | Regulator-led examination |
| Customer audit | Customer-led audit of the organization |
| Supplier attestation | Supplier-provided attestation of their controls |
| Threat-led testing | TIBER-EU, CBEST, or equivalent |
| Penetration testing | Per the penetration testing standard |
| Internal review | Cross-functional internal review |

---

## Section 5: assurance rating scale

| Rating | Description |
| --- | --- |
| Green | Adequate, current, independent, and proportionate assurance is in place |
| Amber-1 | Assurance exists but is not yet current; refresh required within an agreed window |
| Amber-2 | Assurance exists but coverage is partial; gap closure planned |
| Red | Material gap; no or insufficient assurance; remediation required and time-bound |
| Not applicable | The risk area does not require independent assurance at this time; rationale documented |
| Out of cycle | Recent material change has invalidated prior assurance; re-assurance scheduled |

Ratings are reviewed at least annually and on material change.

---

## Section 6: governance

| Element | Description |
| --- | --- |
| Owner of the map | Chief Risk Officer (or equivalent) |
| Contributors | Heads of internal audit, compliance, information security, privacy, AI governance, supplier risk, business continuity |
| Approval | Audit and risk committee approves the map and its annual refresh |
| Reporting | Material gaps are reported to the board risk committee in the board risk report |
| Refresh cadence | Annual full refresh; quarterly update for material changes |
| Trigger refresh | New material risk, new regulatory expectation, significant control change, significant supplier change, material incident |

---

## Section 7: integration with the assurance plan

| Element | Description |
| --- | --- |
| Internal audit plan | Built from the map; the audit plan is risk-based |
| Compliance monitoring plan | Built from the map; compliance plan covers high-risk obligation areas |
| Information-security testing plan | Built from the map; penetration testing prioritized by risk area |
| AI assurance plan | Built from the map; AI-specific reviews prioritized by risk classification |
| Supplier assurance plan | Built from the map; supplier audits and attestations prioritized by criticality |
| Resilience exercise plan | Built from the map; severe-but-plausible scenarios prioritized by risk |
| External-assurance commitments | Tracked centrally; aligned with regulatory expectations |
| Customer-audit calendar | Tracked centrally |

The assurance plan is the prospective view; the map is the current state.

---

## Section 8: gap management

| Step | Description |
| --- | --- |
| Identification | Gap identified during the refresh, the audit committee review, or an external event |
| Classification | Material (warrants formal treatment) or minor (managed through routine activity) |
| Treatment | Specific actions, owner, and target date |
| Tracking | Tracked in the assurance map until closed |
| Closure | The accountable first-line risk or control owner proposes closure with evidence; the relevant second-line function (risk, compliance, information security, privacy, or AI governance, per the gap's domain) confirms and signs off the closure. Where the gap was raised by the third line (internal audit), internal audit confirms the closure evidence resolves the finding. |
| Reporting | Material gaps reported to the board until closed |
| Persistent gaps | Repeated or persistent gaps escalate as a finding of the second line |

---

## Worked example (illustrative; not a real entry)

| Field | Example value |
| --- | --- |
| Risk area identifier | ERR-INF-002 |
| Risk area title | Identity-provider compromise causing widespread access |
| Risk owner | Chief Information Security Officer |
| Linked controls | CTL-IAM-001, CTL-IAM-002, CTL-IAM-007 |
| Linked obligations | Sector regulator authentication-strength expectations |
| First-line activity | IAM operations team operates the IdP and runs joiner-mover-leaver process daily |
| Second-line activity | Information security reviews IAM telemetry monthly; quarterly access review oversight |
| Third-line activity | Internal audit assessed IAM controls last cycle; next audit Q4 |
| External activity | ISO 27001 certification covers IAM; SOC 2 Type II from the IdP supplier received quarterly |
| Customer-driven activity | Annual customer-driven audit covers IAM as part of broader assessment |
| Assurance level | Amber-1 |
| Coverage commentary | Strong first- and second-line activity; third-line refresh due in the current cycle |
| Identified gaps | Internal-audit refresh scheduled but not yet complete |
| Gap treatment | Complete Q4 audit on schedule |
| Last assurance event | Internal-audit cycle previous year |
| Next assurance event | Internal-audit cycle Q4 current year |
| Linked KRIs | KRI-IAM-001 (privileged-account count), KRI-IAM-003 (MFA coverage) |

---

## Operating expectations

1. The map is the single source of truth for board-visible assurance.
2. The map is reviewed at least annually with the audit and risk committee.
3. The internal-audit plan, the compliance-monitoring plan, the information-security testing plan, the AI assurance plan, the supplier assurance plan, and the resilience exercise plan are reconciled with the map.
4. Material gaps have a documented owner, treatment, and target date; persistent gaps are escalated.
5. The risk register and the assurance map are kept consistent; the same risk identifier is used in both.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| IIA Three Lines Model 2020 | Three lines model | Lines of defence |
| ISO 31000:2018 | Risk management principles | Risk management baseline |
| COSO ERM 2017 | Enterprise risk management | Enterprise risk integration |
| COBIT 2019 | MEA02 Managed assurance | Governance of enterprise IT |
| ISO/IEC 27001:2022 | A.5.35 Independent review of information security | Independent review |
| ISO/IEC 42001:2023 | Management system assurance | AI management system |
| Basel Committee Operational Risk Principles | Three lines | Operational risk governance |
| FRC UK Corporate Governance Code | Audit, risk and internal control | UK governance |
| OECD G20 Principles of Corporate Governance | Board oversight | Governance baseline |

---

## Limitations

This register is a CC BY-SA 4.0 baseline. Adopting organizations populate it with their own risk areas, controls, and assurance activities and align it to the regulatory and sector environment in which they operate.

---

**End of Document**
