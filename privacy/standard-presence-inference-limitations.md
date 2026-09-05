# Presence Inference Limitations Standard

**Document Title:** Presence Inference Limitations Standard\
**Document Type:** Standard\
**Version:** 0.1.1\
**Date:** 2026-09-05\
**Owner:** Data Protection Officer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-workforce-network-monitoring.md`](../security/policy-workforce-network-monitoring.md), [`governance/framework-human-capital-and-ethical-conduct.md`](../governance/framework-human-capital-and-ethical-conduct.md), [`privacy/policy-privacy-and-data-governance.md`](policy-privacy-and-data-governance.md), [`security/framework-insider-risk-programme.md`](../security/framework-insider-risk-programme.md), [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md), [`governance/register-data-retention-schedule.md`](../governance/register-data-retention-schedule.md)\
**Classification:** Public\
**Category:** Privacy\
**Review Frequency:** Annual and upon material privacy, employment-law, framework, or monitoring-technology change\
**Repository Path:** [`privacy/standard-presence-inference-limitations.md`](standard-presence-inference-limitations.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

> **Role-name convention:** This document uses **Data Protection Officer (DPO)** as the canonical privacy-lead role title. Adopters whose organization uses **Chief Privacy Officer (CPO)** for the same accountability set should substitute that title in their fork; adopters maintaining both DPO and CPO as distinct roles add a separate CPO entry to their copy of [`governance/register-role-authority.md`](../governance/register-role-authority.md). See the role authority register for the canonical role definition and adopter-customization guidance.

---

## 1. Purpose

This standard sets normative limits on what may be inferred from network and system presence signals about a person's work. It operationalizes the prohibition in the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md) (Section 7, "Presence is not proof of work") by defining, in enforceable terms, how presence-derived signals may and may not be used, the caveats any presence-derived metric must carry, how the error modes of presence data are handled, and who governs presence metrics.

Presence signals are typically collected in the course of legitimate security and operational activity, under the lawful basis, necessity, and safeguards the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md) requires; that collection is itself an intrusion on workforce privacy, which the parent policy governs. The additional intrusion this standard guards against is the misuse of the resulting signals: the quiet drift from "this account is connected" to "this person is working", and from there to a performance judgement about an individual. This standard forecloses that drift.

---

## 2. Scope

### 2.1 Signals governed

This standard governs inferences drawn from the following classes of signal where they are collected under the Workforce Network Monitoring Policy or another documented lawful basis:

1. Network connection, session, and sign-in telemetry (connection state, session start and end, session duration, authentication timing).
2. Presence and availability signals derived from network connection or system sign-in (for example "online", "away", "active", "idle" indicators in collaboration and directory systems).
3. Device-activity signals generated in the course of work (input activity, application or window focus, event or message volume, activity frequency and timing).

These overlap the signal classes the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md) (Section 2.1) places in scope. This standard does not itself authorize collecting any signal; where a signal class listed here is collected under a documented lawful basis and notice, these interpretation limits apply to it.

### 2.2 Inferences limited

This standard limits inferences about a person's presence, availability, engagement, "at work" status, productivity, output, and contribution, and any performance judgement or employment consequence built on such inferences.

### 2.3 Out of scope

1. Operational-health and capacity telemetry (metrics, latency, saturation) not attributed to an individual, which is governed by the operations observability and telemetry standard, not this standard.
2. Security detection and insider-risk investigation, which operate under the [Insider Risk Programme Framework](../security/framework-insider-risk-programme.md) with its own lawful-basis, validation, and due-process safeguards. This standard governs the interpretation of presence signals as a measure of work; it does not govern their use as a security detection input.
3. Content of communications, which is out of scope of the governing monitoring policy and is not inspected except under that policy's exceptional, defined-approval path.

---

## 3. Definitions

| Term | Definition |
| --- | --- |
| Presence signal | Telemetry indicating that a device or account is connected, signed in, or generating activity on organization systems, including connection state, session duration, sign-in and sign-out timing, and activity volume or frequency. |
| Presence inference | A conclusion drawn from one or more presence signals about a person's state, for example that they are at work, available, engaged, or productive. |
| Presence-derived metric | Any quantitative measure computed from presence signals, for example hours connected, session count, sign-in punctuality, active minutes, or event and message counts. |
| Productivity metric | A measure used to assess an individual's output, contribution, or job performance. |
| False-present | A presence signal indicating connection or activity while the person is not in fact working: an idle always-on session, a shared or loaned device, an automated or keep-alive connection, a background synchronization, or a session left open. |
| False-absent | Absence of a signal, or a below-threshold signal, while the person is in fact working: offline work, deep focus without device input, work on an alternate or unmonitored device, or the use of accessibility tools that alter input patterns. |
| Aggregate form | Presence-derived data combined across a group such that no value is attributable to an identified or identifiable individual. |

---

## 4. Core normative limit: presence is not proof of work

**Presence indicates connection, not contribution.** Network presence, absence, connection duration, sign-in timing, and activity volume indicate that a device or account interacted with organization systems. They do not measure the work a person performed, its quality, or its value.

Accordingly:

1. Presence signals and presence-derived metrics must not be used as a productivity metric or a performance measure.
2. They must not be used as the basis for an individual performance judgement.
3. A bare presence inference must not, by itself, be the basis for an employment consequence (including discipline, ranking, reward, or termination) affecting an individual.

This limit is absolute for a bare, unvalidated presence inference: such an inference, standing alone, is never the basis for an employment consequence. It does not bar an employment consequence that follows from independently validated evidence handled with human review and due process, which the parent policy permits (Section 7, items 1 and 2, requiring human review and contextual validation before any consequence). This standard therefore does not exceed the parent policy, whose rule is that no monitoring signal, by itself, sanctions, ranks, restricts, or penalizes a worker.

This limit also aligns with the data protection accuracy principle: a presence inference is an inference, not a fact, and treating an error-prone inference as a measure of an individual's work is inconsistent with holding personal data accurate for its purpose.

---

## 5. Requirements

### 5.1 Mandatory caveats on presence-derived metrics

Any presence-derived metric that is produced, displayed, or reported must, wherever it appears:

1. Carry a documented statement of what it does and does not measure, stating explicitly that it measures connection or activity and not work, output, or performance.
2. Not be labelled, titled, or presented as a productivity, output, engagement, or performance measure.
3. Not be used for individual ranking, scoring, or comparison.

A presence-derived metric that cannot carry these caveats at its point of use must not be produced in individually attributable form.

### 5.2 False-present and false-absent handling

1. Presence signals are error-prone. Both error modes must be acknowledged wherever presence inferences are drawn: false-present (a signal without corresponding work) and false-absent (work without the expected signal).
2. A presence inference must not be treated as ground truth. It is a hypothesis about a person's state, not a confirmed fact.
3. No adverse consequence for an individual may rest on an unverified presence inference. Where a presence signal appears to warrant attention, it is validated against context by a human before any consequence, consistent with the parent policy's no-automated-discipline rule (Section 7, item 1) and the insider-risk framework's validation-before-escalation safeguard.
4. Absence of a signal must not be read as absence of work, and volume of a signal must not be read as volume of work.

### 5.3 Prohibited inferences and uses

The following are prohibited:

1. **No automated productivity scoring.** Presence signals must not feed an automated system that scores, rates, or ranks an individual's productivity or performance.
2. **No stack-ranking.** Presence-derived metrics must not be used to rank or force-distribute individuals against one another.
3. **No manufactured always-on expectation.** Connection data must not be used to create or enforce an expectation that an individual be continuously present, connected, or immediately responsive. Sign-in timing and connection duration must not be used to infer commitment, diligence, or availability obligations not established by the individual's terms of work.
4. **No off-duty profiling.** Presence signals must not be used to infer an individual's lawful off-duty conduct, location, or personal circumstances beyond the organization-resource interaction, consistent with the parent policy's scope limits (Section 2 and Section 7, item 6).
5. **No secondary-purpose repurposing.** Presence data collected for security or operational purposes must not be repurposed to assess, measure, or compare individual output or performance. A new purpose requires its own lawful basis, assessment, and notice, per the [Privacy and Data Governance Policy](policy-privacy-and-data-governance.md) and the prohibited-uses requirements of the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md) (Section 7).

### 5.4 Aggregation and de-identification

1. Where presence-derived signals are used at all for a legitimate purpose such as capacity or operational planning, they are used in aggregate, de-identified form in preference to individual-level form, and minimized to that form as early as the purpose allows.
2. Individual-level presence data must not be repurposed for performance assessment. Aggregate presence analytics must not be re-individualized to reach a judgement about a specific person.
3. Aggregation must not be used to reconstruct individual patterns where group sizes are small enough that a value is effectively attributable to one person; small-group results are suppressed or further generalized.

### 5.5 Retention and minimization

Presence and presence-derived data is retained only as long as necessary for its stated purpose and is then destroyed or de-identified, per the [Data Retention Schedule](../governance/register-data-retention-schedule.md) and the parent policy (Section 8). Retention periods are organization-defined and recorded in the retention schedule; they are not prescribed by this standard or attributed to any external standard.

---

## 6. Roles and responsibilities

| Role | Responsibility |
| --- | --- |
| **Data Protection Officer (DPO)** | Reviews presence-derived metrics and their uses against the limits in this standard; independently advises on lawful basis, purpose limitation, and accuracy for any presence-based processing. Acting as an independent adviser, the DPO does not determine or approve the operational metrics themselves. |
| **Chief Information Security Officer (CISO)** | Owns the parent monitoring capability; keeps presence signals collected for security from being exposed or configured in a way that enables prohibited performance use. |
| **Metric and analytics owners** | May define presence-derived metrics only for a documented, legitimate, non-performance purpose; attach the mandatory caveats (Section 5.1); and submit each new or materially changed presence metric for DPO review before use. |
| **HR / People Operations** | Prevents presence signals from being used for automated discipline or as a productivity metric; does not receive or act on individual presence data as a performance measure; leads any due-process handling where a validated signal (not a bare presence inference) reaches employment action. |
| **Line managers** | Do not request, receive, or act on individual presence data as a performance or presence measure; route genuine security or conduct concerns through the defined channels rather than direct surveillance of connection data. |
| **Internal Audit** | Provides independent assurance that presence-derived metrics carry the mandatory caveats, are not used for individual ranking or performance judgement, and are minimized to aggregate form where used. |

---

## 7. Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27001:2022 | A.8.16 Monitoring Activities; A.5.34 Privacy and protection of personal identifiable information (PII); A.5.10 Acceptable Use of Information and Other Associated Assets | Bounds the interpretation and use of monitoring output and the handling of personal data derived from it. |
| NIST CSF 2.0 | GV.OC Organizational Context; GV.PO Policy | Governs the policy and organizational-context constraints on how monitoring signals are used. |
| NIST Privacy Framework 1.0 | CT.DP-P Disassociated Processing; CT.DM-P Data Processing Management; CM.AW-P Data Processing Awareness | Limits on inference from presence signals, purpose-limitation on presence telemetry, and mandatory caveats on displayed presence-derived metrics |
| CSA CCM v4.1 | DSP-12 Limitation of Purpose in Personal Data Processing; DSP-08 Data Privacy by Design and Default | Purpose limitation on presence data and privacy-by-default in the design of any presence-derived metric. |
| GDPR (EU) | Article 5(1)(b) purpose limitation; Article 5(1)(d) accuracy; Article 22 automated individual decision-making; Article 88 processing in the context of employment | Aligns the standard's purpose-limitation, accuracy, no-automated-scoring, and employment-context requirements. These principles inform the standard; the standard does not assert that any single article prescribes the specific presence-use limits. |
| UK GDPR | Article 22 replaced by Articles 22A to 22D; Article 88 not adopted; see the United Kingdom privacy annex | The UK position on automated decisions and employment-context processing differs from the EU; do not conflate the two regimes. |

---

## 8. Limitations

This standard is a CC BY-SA 4.0 baseline. It sets limits on inferring work from presence signals; it does not define the productivity or performance measures an organization uses, which belong to legitimate, human-led performance management outside the scope of this standard. Adopting organizations must validate the framework mappings and the applicable employment and privacy law for their jurisdictions, and must not read this standard as authorizing any monitoring; the authority for what monitoring is permitted is the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md), and this standard only constrains how the resulting signals may be interpreted. This standard implements, and does not supersede, the [Workforce Network Monitoring Policy](../security/policy-workforce-network-monitoring.md); where this standard and the parent policy or another authoritative document appear to differ, the parent policy governs, the difference is escalated for resolution, and a specific legal obligation prevails where one applies.

---

**End of Document**
