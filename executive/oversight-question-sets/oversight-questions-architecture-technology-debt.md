# What the governing body should ask about enterprise architecture and accumulated technology debt

**Document Title:** What the governing body should ask about enterprise architecture and accumulated technology debt\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-08-15\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`architecture/framework-enterprise-architecture.md`](../../architecture/framework-enterprise-architecture.md), [`architecture/standard-architecture-decision-records.md`](../../architecture/standard-architecture-decision-records.md), [`architecture/standard-technology-radar.md`](../../architecture/standard-technology-radar.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/oversight-question-sets/oversight-questions-architecture-technology-debt.md`](oversight-questions-architecture-technology-debt.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Oversight Question Set\
**Narrative Status:** Advisory\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`architecture/framework-enterprise-architecture.md`](../../architecture/framework-enterprise-architecture.md), [`architecture/standard-architecture-decision-records.md`](../../architecture/standard-architecture-decision-records.md), [`architecture/standard-technology-radar.md`](../../architecture/standard-technology-radar.md), [`architecture/procedure-architecture-review.md`](../../architecture/procedure-architecture-review.md), [`risk/standard-enterprise-risk-management.md`](../../risk/standard-enterprise-risk-management.md), [`risk/template-board-risk-report.md`](../../risk/template-board-risk-report.md), [`governance/policy-exception-and-risk-acceptance-management.md`](../../governance/policy-exception-and-risk-acceptance-management.md), [`operations/procedure-patch-management.md`](../../operations/procedure-patch-management.md), [`security/procedure-vulnerability-management.md`](../../security/procedure-vulnerability-management.md), [`dev-security/standard-software-evaluation-acceptance-and-lifecycle.md`](../../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md)\
**External Sources:** None\
**Claim Classes Present:** citation, composite\
**Review Record:** NR-2026-007\
**Last Reviewed:** 2026-08-15

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Context for these questions

Technology debt is the accumulated cost of past technology decisions that remain in place: aging systems, deferred upgrades, expedient shortcuts, and standards deviations left unresolved. The enterprise risk taxonomy in the [enterprise risk management standard](../../risk/standard-enterprise-risk-management.md) recognizes this class of exposure explicitly: its Technology risk category names legacy-system obsolescence and technology lifecycle waste among its subcategories (its section 4).

The governing body does not manage architecture, and these questions do not ask it to. Its oversight concern is narrower and harder: whether the organization can see the debt it carries, takes new debt on deliberately and on the record, winds down what it has decided to leave behind, and brings the resulting risk into the enterprise risk picture rather than leaving it inside engineering.

The corpus equips that oversight through several instruments rather than one document. The [enterprise architecture framework](../../architecture/framework-enterprise-architecture.md) defines the architecture practice, its capability map and heatmap, its target-state and transition planning, its governance forums, and its integration with enterprise risk. The [architecture decision records standard](../../architecture/standard-architecture-decision-records.md) requires significant decisions, including decisions accepting material technical debt, to be recorded durably. The [technology radar standard](../../architecture/standard-technology-radar.md) governs the deliberate adoption and, just as deliberately, the winding down of technologies. The [architecture review procedure](../../architecture/procedure-architecture-review.md) provides informed challenge before commitment. Lifecycle controls in the [patch management procedure](../../operations/procedure-patch-management.md), the [vulnerability management procedure](../../security/procedure-vulnerability-management.md), and the [software evaluation, acceptance and lifecycle standard](../../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md) address systems approaching or past the end of vendor support. Treating these instruments together as a single oversight subject called technology debt is a synthesis this page makes; see the limitations.

Each question below is paired with a note on what a strong answer contains. The questions organize a line of inquiry; they do not prescribe any particular architecture, investment level, or outcome.

## Questions

### Can we see the debt we hold?

**1. Where is our technology debt recorded, and who owns the record?**
A strong answer names the specific records the corpus provides for this: architecture decision records for accepted debt per the [architecture decision records standard](../../architecture/standard-architecture-decision-records.md), the capability heatmap the [enterprise architecture framework](../../architecture/framework-enterprise-architecture.md) describes, which overlays the capability map with technical-debt and risk signals (its Section 3), and Technology-category entries in the enterprise risk register per the [enterprise risk management standard](../../risk/standard-enterprise-risk-management.md). A weak answer locates the knowledge in individual engineers rather than in any record.

**2. Which business capabilities depend on the systems in the worst condition?**
A strong answer connects systems to business impact through the capability map, which the [enterprise architecture framework](../../architecture/framework-enterprise-architecture.md) treats as the spine of the practice, mapping each system and each product to the capabilities it supports (its Section 3). An answer given only in system names, with no line to a customer or business consequence, has not used the instrument the corpus provides.

**3. Which production systems are at or approaching the end of vendor support?**
End of vendor support means security fixes stop arriving while exposure continues. A strong answer comes from the standing end-of-life tracking the corpus requires, in the [patch management procedure](../../operations/procedure-patch-management.md) (its section 5) and the [vulnerability management procedure](../../security/procedure-vulnerability-management.md) (its section 5), with the forward timeline those documents define, not from a survey assembled for this meeting.

### Do we take new debt on deliberately?

**4. When we last accepted material technical debt, where is that decision recorded, and what repayment expectation was recorded with it?**
The [architecture decision records standard](../../architecture/standard-architecture-decision-records.md) places decisions accepting material technical debt inside its scope (its section 2) and expects the record to include the expected cost of repayment (its section 4). A strong answer produces the records. The standard also states that the absence of a record for a contested decision is itself a finding (its section 13), so "we had no time to write it down" concedes the finding rather than excusing it.

**5. Which significant architecture decisions went ahead without review, and how would we know?**
The [architecture review procedure](../../architecture/procedure-architecture-review.md) defines which changes are review-worthy (its Step 1), requires accepted risks from a review to be recorded on the relevant risk register (its Step 6), and requires implementation drift to be routed back through review (its Step 7). A strong answer shows these paths operating: review-worthy changes are triaged, accepted risks reach the risk register, and implementation drift is routed back through review.

**6. What exceptions to our technology standards are open right now, and what keeps them from becoming permanent?**
Exceptions bear on debt when they outlive their rationale. The [exception and risk acceptance policy](../../governance/policy-exception-and-risk-acceptance-management.md) requires exceptions to be time-bound with defined duration and renewal limits (its section 4.3) and tracked in a central register (its section 4.5). Time-bounding is a prevention against silent permanence. A strong answer reports the aggregate picture from that register, including exceptions nearing their limits, not a case-by-case recollection.

### Are we working debt down?

**7. What technologies have we decided to stop investing in, and what is the wind-down path for each?**
The [technology radar standard](../../architecture/standard-technology-radar.md) gives the organization a deliberate stance per technology, including a Hold state for technologies not to be used for new work (its section 4), and requires each Hold placement to carry a sunset path for retiring existing use (its sections 6 and 13). A strong answer shows Hold placements that actually exist, each with a named owner and a wind-down route. The standard's own principles state that the radar is not an aspiration list.

**8. For systems past the end of support that remain in production, who approved that, and under what conditions?**
The [patch management procedure](../../operations/procedure-patch-management.md) does not permit an end-of-life system in production outside the exception path it defines, with compensating controls and recurring review until the system is decommissioned or replaced (its section 5). A strong answer produces the approval and the conditions for every such system. A system in this state that no one approved is the finding.

**9. Is retirement actually happening, or only planned?**
The [software evaluation, acceptance and lifecycle standard](../../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md) requires a recurring review of each product covering vendor support status and end-of-life timeline, and requires obsolete or unsupported software to be retired through its defined workflow (its section 10). A strong answer includes completed retirements from the recent past, with dates. A list containing only future intentions is a plan, not evidence of a working practice.

### Does the debt reach our risk picture and our direction?

**10. How does architecture and technology risk reach the enterprise risk register, and this governing body?**
The [enterprise architecture framework](../../architecture/framework-enterprise-architecture.md) integrates the architecture practice with enterprise risk by feeding architecture risk into the enterprise risk register (its Section 8), and the [enterprise risk management standard](../../risk/standard-enterprise-risk-management.md) gives that risk a home in its Technology category (its section 4). A strong answer traces a real architecture risk from its origin to the register and onward to the reporting this body receives, in the top-risk and emerging-risk sections the [board risk report template](../../risk/template-board-risk-report.md) defines (its sections 4 and 5).

**11. What is our target-state architecture, and where are we against it?**
The [enterprise architecture framework](../../architecture/framework-enterprise-architecture.md) requires a documented current state, a target state for a defined planning horizon, an articulated gap, transition architectures, and a roadmap, refreshed at the cadence it sets (its Section 4). A strong answer presents the gap and the movement since the last update.

**12. How is architecture quality measured between the big reviews?**
The [enterprise architecture framework](../../architecture/framework-enterprise-architecture.md) expects continuous measurement through fitness functions, covering areas such as deployment, reliability, security, cost, and complexity, rather than point-in-time assessment alone (its Section 9). A strong answer shows these fitness-function measures tracked as trend lines over time, rather than point-in-time assessment alone.

## Evidence to request

Each item below is an evidence class the governing body can call for from management, and each is evidence for a named control or outcome.

- **The architecture decision records that accept material technical debt**, with their recorded repayment expectations, as evidence that debt acceptance operates on the record per the [architecture decision records standard](../../architecture/standard-architecture-decision-records.md).
- **The capability heatmap with its technical-debt overlay**, as evidence that debt is visible at portfolio level per the [enterprise architecture framework](../../architecture/framework-enterprise-architecture.md).
- **The current technology radar, its Hold placements, and their sunset paths**, as evidence that wind-down is deliberately managed per the [technology radar standard](../../architecture/standard-technology-radar.md).
- **The end-of-life tracking output and the exception records for any end-of-life system in production**, as evidence that the lifecycle controls in the [patch management procedure](../../operations/procedure-patch-management.md) and the [vulnerability management procedure](../../security/procedure-vulnerability-management.md) operate.
- **Recent architecture review outcomes, including risks accepted**, as evidence that the review process operates and that accepted risks are recorded on the risk register, per the [architecture review procedure](../../architecture/procedure-architecture-review.md).
- **The exception register view for technology-standard exceptions**, with ages and renewal counts against the limits the [exception and risk acceptance policy](../../governance/policy-exception-and-risk-acceptance-management.md) defines, as evidence that exceptions stay time-bound.
- **The Technology-category entries in the enterprise risk register**, as evidence that architecture risk reaches enterprise risk management per the [enterprise risk management standard](../../risk/standard-enterprise-risk-management.md).
- **The most recent board risk report**, checked for whether technology and architecture risk appears in its top-risk or emerging-risk sections, as evidence that the reporting route in the [board risk report template](../../risk/template-board-risk-report.md) carries this risk class to the governing body.
- **Evidence that recently decommissioned software went through the retirement workflow**, per the [software evaluation, acceptance and lifecycle standard](../../dev-security/standard-software-evaluation-acceptance-and-lifecycle.md).

## Limitations

- This page creates no compliance and imposes no requirement. The linked corpus documents govern; where this page differs from a corpus document, the corpus document prevails.
- This page is advisory. It organizes a line of questioning; it does not prescribe an architecture, a technology choice, an investment level, or any answer to its own questions. Every decision remains with the reader's organization.
- This page carries composite claims. The corpus has no single technology-debt document; the framing of technology debt as one oversight subject, assembled from architecture, risk, exception, and lifecycle sources, is synthesized by this page, and the adopting organization validates that reading against its own governance. Its forums, registers, and approval authorities may be structured or named differently from those the corpus baseline describes.
- The corpus documents this page points to carry the specific thresholds, timelines, day counts, review cadences, classifications, and named approval authorities. This page routes to them and does not reproduce them. That routing is a contribution to the corpus's status as the single source for every value.
- This page makes no claim about how likely any failure is, and none of its statements should be read as a probability or a frequency.

**End of Document**
