# Control Testing Procedure

**Document Title:** Control Testing Procedure\
**Document Type:** Procedure\
**Version:** 1.1.0\
**Date:** 2026-07-06\
**Owner:** Chief Compliance Officer\
**Approving Authority:** Chief Information Officer\
**Related Documents:** [`compliance/standard-internal-audit.md`](standard-internal-audit.md), [`compliance/procedure-audit-planning.md`](procedure-audit-planning.md), [`compliance/procedure-capa.md`](procedure-capa.md), [`governance/framework-continuous-assurance-and-improvement.md`](../governance/framework-continuous-assurance-and-improvement.md), [`governance/framework-governance-performance-and-improvement.md`](../governance/framework-governance-performance-and-improvement.md)\
**Classification:** Public\
**Category:** Compliance Management\
**Review Frequency:** Annual and upon material control framework change\
**Repository Path:** [`compliance/procedure-control-testing.md`](procedure-control-testing.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure defines the processes for testing the design and operating effectiveness of internal controls across the organization's governance, risk, compliance, security, and operational domains. Control testing provides objective evidence that controls are functioning as intended and supports certification, audit readiness, and continuous assurance activities.

---

## Scope

Applies to all controls defined in the organization's control frameworks including ISO/IEC 27001 Annex A, COBIT 2019, CSA CCM v4.1, NIST SP 800-53, and any applicable regulatory control requirements. Encompasses preventive, detective, and corrective controls across all domains.

---

## Roles and responsibilities

| Role | Responsibility |
| --- | --- |
| **Chief Compliance Officer** | Owns the control testing programme; approves the annual testing calendar; receives the quarterly results summary; authorizes any deviation from the planned testing scope. |
| **GRC Programme Manager** | Schedules and coordinates control testing activities; maintains the Control Testing Register; tracks remediation to closure; escalates overdue remediation per section 6. |
| **Internal Audit** | Executes independent control testing; determines test methods and sample sizes; issues findings; performs the independent re-test that validates remediation before closure. |
| **Control Owners** | Provide control evidence within the requested window; respond to findings; author and execute remediation plans; do not self-assess the effectiveness of controls they own. |
| **CISO** | Reviews security control testing results; approves remediation plans for security-domain deficiencies; receives the quarterly results summary. |
| **Independent reviewer** | A reviewer not involved in executing a given test (a second GRC or Internal Audit team member) confirms the test conclusion, the adequacy of the evidence, and the result classification before the result is entered in the Control Testing Register. This separation of execution from review applies to all Deficiency and Material Weakness results. |

The tester of a control is never the owner or operator of that control: control testing is performed by Internal Audit or the GRC function independently of the control owner, so that the conclusion does not rest on a self-assessment.

---

## 1. Control testing planning

1.1 The annual Control Testing Calendar is prepared by the GRC Programme Manager in alignment with the Audit Planning Procedure.

1.2 Controls are prioritized for testing based on:
- Risk rating (the current residual risk score of the risk the control mitigates, not the inherent risk).
- Certification scope (ISO/IEC 27001, SOC 2, BASC, etc.).
- Prior year findings and remediation outcomes (a control with a prior deficiency is re-tested in the next cycle regardless of its risk rating).
- Material changes to the control environment (a new, modified, or migrated control is tested in the cycle following the change).

1.3 Testing frequency is set by the control's residual-risk rating, subject to the certification-scope minimums:

| Residual risk | Minimum operating-effectiveness testing frequency |
| --- | --- |
| **High** | Annually, at minimum; semi-annually where a prior-year deficiency is open or recently closed |
| **Medium** | At least once every two years |
| **Low** | At least once every three years |

No control within a certification scope is tested less often than the certification's own cycle requires (for example, controls in the ISO/IEC 27001 and SOC 2 scopes are tested at least annually irrespective of risk rating), and no in-scope control remains untested for more than three consecutive years.

1.4 The Control Testing Calendar records, per planned test: the control identifier and framework reference, the control owner, the test type (design or operating effectiveness), the planned test period, the assigned tester, the residual-risk rating driving the frequency, and the certification scopes the control supports.

1.5 The calendar distinguishes design effectiveness testing (is the control properly designed?) from operating effectiveness testing (is the control working as designed over the test period?). The GRC Programme Manager reviews the calendar at mid-year and re-sequences remaining tests to reflect new risks, incidents, or control changes that have emerged since the calendar was set.

---

## 2. Control testing methodology

### 2.1 Design effectiveness testing

Design testing verifies that a control, if operating as designed, would prevent or detect the associated risk.

Design testing methods:
- Policy and procedure review.
- Control design interview with control owner.
- Control flowchart and process mapping review.
- Comparison against control framework requirement.

Outcome: Design adequate / Design gap identified.

### 2.2 Operating effectiveness testing

Operating testing verifies that a control has operated consistently during the test period.

Operating testing methods:

| Testing Method | Applicability |
| --- | --- |
| **Inquiry** | Interviews with control operators; supports but does not stand alone |
| **Observation** | Direct observation of control execution |
| **Inspection** | Review of documents, logs, and evidence samples |
| **Re-performance** | Independent re-execution of the control to verify outcome |
| **Automated testing** | Continuous monitoring outputs; automated evidence collection |

Sample sizes for inspection-based tests follow a risk-based sampling methodology:
- High-risk controls: 25 to 40 samples or 100% population if feasible.
- Medium-risk controls: 15 to 25 samples.
- Low-risk controls: 5 to 15 samples.

The chosen sample size and selection method are recorded in the test's "Sampling justification" field in the audit-evidence package (see [`compliance/template-audit-evidence-package.md`](template-audit-evidence-package.md) §"Operating evidence" per-test field set). Auditors reviewing the package see the statistical or judgemental basis for the chosen sample size without having to reconstruct it from this procedure.

### 2.3 Sampling methodology

Before selecting a sample, the tester defines the population: the complete set of control occurrences in the test period (for example, every privileged-access grant in the quarter, or every change record raised against the in-scope system). The population definition, its size, and the source from which it was drawn are recorded in the evidence package.

The selection method is chosen by the control's residual-risk rating and the nature of the population:

| Selection method | When to use |
| --- | --- |
| **Full population (100%)** | Low-volume populations (broadly, 25 or fewer occurrences), and any population for a control whose failure is individually consequential (for example, quarterly access recertification) |
| **Random selection** | Large, homogeneous populations where every occurrence carries comparable risk; supports a statistically defensible conclusion across the population |
| **Risk-based (targeted) selection** | Populations where specific occurrences carry elevated risk (for example, changes to production financial systems, or access grants to privileged roles); the sample is weighted toward the higher-risk occurrences |
| **Haphazard selection** | Permitted only as a supplement for Low-risk controls; it is not used as the primary method for High-risk controls, because it supports no statistical inference about the population |

The tester records, in the evidence package, the population definition, the sample size, the selection method, the selection rationale, and any limitation on the conclusion the sample supports (for example, that a judgemental sample does not support a statistical projection across the population). A sample that surfaces one or more exceptions is not silently expanded to seek a clean result: the exception is evaluated on its merits under section 4, and any extension of the sample is documented with its rationale.

---

## 3. Evidence collection

3.1 All testing is supported by documented evidence retained in the compliance repository.

3.2 Evidence must be relevant (it bears on the control objective tested), sufficient (enough to support the conclusion), reliable (the more independent of the control owner the source, the more reliable), and traceable to the specific control occurrence and period tested.

3.3 Working papers record, for each test, the control tested, the test objective, the population and sample, the procedures performed, the evidence examined (with identifiers sufficient for a reviewer to retrieve it), the exceptions noted, and the conclusion reached. Working papers are completed contemporaneously during fieldwork, not reconstructed afterward, so that a reviewer can re-trace the test from the working paper alone.

3.4 Where a control test relies solely on inquiry (interview) evidence, the tester corroborates it with at least one other evidence type (observation, inspection, or re-performance) before concluding that the control is effective. Inquiry alone does not support an Effective result for a Deficiency-or-higher-risk control.

3.5 Evidence is retained for a minimum of 7 years per [`governance/standard-records-retention-and-destruction.md`](../governance/standard-records-retention-and-destruction.md), or longer where regulatory requirements specify. The 7-year floor aligns with Sarbanes-Oxley §103 audit-evidence retention and the records-retention standard's Corporate Governance, Financial, and Legal-and-Compliance domain default (each carrying a 7-year retention).

---

## 4. Testing results and findings

4.1 Control testing results are classified as:

| Result | Definition |
| --- | --- |
| **Effective** | Control designed and operating effectively; no exceptions noted |
| **Observation** | Minor weakness; no material risk; improvement recommended |
| **Deficiency** | Control gap that, individually or in combination, could lead to failure to prevent or detect a material misstatement or breach |
| **Material Weakness** | Significant deficiency with high likelihood of material impact if not remediated |

4.2 Each result carries a defined response requirement:

| Result | Notification | CAPA required? | Response timeline |
| --- | --- | --- | --- |
| **Effective** | Recorded in the Control Testing Register; no individual notification | No | None |
| **Observation** | Control owner notified | Optional (owner discretion, recorded) | Improvement, if undertaken, tracked to the next test cycle |
| **Deficiency** | Control owner and the relevant domain executive (CCO, or CISO for security controls) notified within 5 business days | Yes: a CAPA record is opened | Remediation plan within 10 business days (section 6) |
| **Material Weakness** | Control owner, the domain executive, and the Enterprise Risk Committee notified within 2 business days | Yes: a CAPA record is opened and flagged for executive oversight | Executive review and remediation within 30 days (section 6) |

4.3 Deficiencies and material weaknesses are logged in the CAPA Register and managed to closure under [`compliance/procedure-capa.md`](procedure-capa.md). The control-testing result and the CAPA record cross-reference each other so that a reader of either can trace the full lifecycle from detection to validated closure.

4.4 Control owners receive testing results within 5 business days of testing completion. A Deficiency or Material Weakness result is confirmed by the independent reviewer (see Roles and responsibilities) before it is finalized and notified.

> **Classification-scheme note.** This procedure's result categories (Effective / Observation / Deficiency / Material Weakness) carry a Sarbanes-Oxley framing (the "material weakness" concept of SOX §404, the internal-control-over-financial-reporting provision). The organization's canonical finding-classification scheme, used by the Internal Audit Standard ([`compliance/standard-internal-audit.md`](standard-internal-audit.md) §7) and the CAPA Procedure ([`compliance/procedure-capa.md`](procedure-capa.md) §5), is Critical / High / Moderate / Low / Observation. When a control-testing Deficiency or Material Weakness is routed into the CAPA Register, it is assigned the CAPA scheme's severity (broadly, a Material Weakness maps to Critical, and a Deficiency to High or Moderate by impact) so that the register remains internally consistent. Whether to replace this procedure's SOX-framed scheme with the canonical scheme outright, or to retain it with this crosswalk, is a maintainer decision recorded in the project's pending-decisions queue.

---

## 5. Reporting

5.1 A control testing summary report is issued quarterly. It records the controls tested in the period, the result of each, the deficiencies and material weaknesses opened, the status of remediation from prior periods, and the testing coverage achieved against the calendar.

5.2 The report is distributed by recipient and purpose:

| Recipient | Content | Cadence |
| --- | --- | --- |
| **Chief Compliance Officer** | Full summary report | Quarterly |
| **CISO** | Full report, with security-domain results highlighted | Quarterly |
| **Control owners** | The results and findings for their own controls | On test completion (within 5 business days) |
| **Enterprise Risk Committee** | Annual control-testing outcomes within the Governance Status Report, with any open material weaknesses surfaced on detection | Annually, plus on a material weakness |
| **External auditors / certification bodies** | Certification-scope results | As required by the engagement |

5.3 A material weakness is surfaced to the Enterprise Risk Committee when detected (per section 4.2), not held for the next quarterly cycle.

---

## 6. Remediation and re-testing

6.1 Control owners submit a remediation plan for every Deficiency within 10 business days of notification, and for every Material Weakness within 5 business days. The plan names the corrective action, the accountable owner, and the target completion date, and is recorded against the CAPA record.

6.2 Material weaknesses require executive review (the domain executive plus, for enterprise-significant cases, the Enterprise Risk Committee) and remediation within 30 days, or a documented, executive-approved extension where the corrective action cannot complete in that window.

6.3 Overdue remediation is escalated on a defined chain:

| Trigger | Escalation |
| --- | --- |
| Remediation plan not submitted by the deadline (6.1) | GRC Programme Manager escalates to the control owner's manager |
| Target completion date missed | Escalation to the domain executive (CCO, or CISO for security controls) |
| 10 business days past the target date, or a second requested extension | Escalation to the Enterprise Risk Committee, recorded as an accepted-risk decision if remediation is not yet feasible |

6.4 A remediated control is re-tested by Internal Audit before the deficiency is closed in the CAPA Register. The re-test confirms that the control now operates effectively over a sufficient period, not merely that the corrective action was implemented; a re-test that relies only on confirmation that an action was taken is not sufficient to close the finding. The independent effectiveness validation is completed within 90 days of the remediation being reported as implemented.

---

## 7. Control Testing Register

7.1 The GRC Programme Manager maintains the Control Testing Register as the authoritative record of testing activity. Each entry records: the control identifier and framework reference; the control owner; the test type (design or operating effectiveness); the test period and date completed; the tester and the independent reviewer; the population and sample (with a pointer to the evidence package); the result; the per-control effectiveness band (the sustained-effectiveness signal defined in [`governance/register-digital-trust-and-assurance-metrics.md`](../governance/register-digital-trust-and-assurance-metrics.md), derived from the result together with the deficiency recurrence signal and open corrective-action state); any CAPA record opened; and the remediation and re-test status through to validated closure.

7.2 The register is the source for the section 5 reports and for the testing-coverage metric in section 8, and it reconciles to the CAPA Register for every Deficiency and Material Weakness it records.

---

## 8. Metrics

8.1 The control testing programme reports the following measures to the Chief Compliance Officer and, annually, to the Enterprise Risk Committee:

- **Testing coverage**: the proportion of calendar-planned tests completed in the period, and the proportion of in-scope controls tested within their required frequency.
- **Deficiency rate**: Deficiency-and-above results as a proportion of controls tested.
- **Recurrence rate**: the proportion of deficiencies that recur on a control previously remediated and closed (a lead indicator that a prior remediation treated the symptom rather than the cause).
- **Average time to remediate**: from finding notification to validated closure, reported by severity.
- **Per-control effectiveness band**: the sustained-effectiveness band for each in-scope control (Effective, Observation, Deficiency, or Material Weakness), derived from its latest result together with its deficiency recurrence signal and open corrective-action state, as defined in [`governance/register-digital-trust-and-assurance-metrics.md`](../governance/register-digital-trust-and-assurance-metrics.md). Unlike the programme-level measures above, this is a per-control signal reported at the control's residual-risk testing frequency and consumed under the three lines of defence: the first line (control owner) self-monitors it, the second line (risk and compliance) aggregates and challenges it, and the third line (internal audit) validates its basis.

8.2 A rising recurrence rate or a falling testing coverage is itself surfaced as a programme-level observation in the quarterly report.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27001:2022 | §9.1: Monitoring, Measurement, Analysis and Evaluation | Control effectiveness measurement |
| ISO 19011:2018 | Guidelines for Auditing Management Systems | Control testing methodology |
| NIST SP 800-53A | Assessing Security and Privacy Controls | Control testing guidance |
| COBIT 2019 | MEA01: Managed Performance and Conformance Monitoring | Control monitoring and assurance |
| CSA CCM v4.1 | A&A-02, A&A-05: Independent Assessments; Audit Management Process | Continuous control assurance |

---

**End of Document**
