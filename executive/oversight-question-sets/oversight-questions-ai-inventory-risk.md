# What the governing body should ask about the organization's AI inventory, risks, incidents, suppliers, and change

**Document Title:** What the governing body should ask about the organization's AI inventory, risks, incidents, suppliers, and change\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-08-15\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/guide-ai-board-oversight.md`](../../ai/guide-ai-board-oversight.md), [`ai/template-ai-system-register.md`](../../ai/template-ai-system-register.md), [`ai/register-ai-risk.md`](../../ai/register-ai-risk.md), [`ai/plan-ai-incident-response.md`](../../ai/plan-ai-incident-response.md), [`supply-chain/procedure-third-party-ai-due-diligence.md`](../../supply-chain/procedure-third-party-ai-due-diligence.md), [`risk/template-board-risk-report.md`](../../risk/template-board-risk-report.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/oversight-question-sets/oversight-questions-ai-inventory-risk.md`](oversight-questions-ai-inventory-risk.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Oversight Question Set\
**Narrative Status:** Advisory\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`ai/guide-ai-board-oversight.md`](../../ai/guide-ai-board-oversight.md), [`governance/guideline-minimum-viable-governance-structure.md`](../../governance/guideline-minimum-viable-governance-structure.md), [`ai/template-ai-system-register.md`](../../ai/template-ai-system-register.md), [`ai/register-model-registry.md`](../../ai/register-model-registry.md), [`ai/framework-ai-governance-and-risk.md`](../../ai/framework-ai-governance-and-risk.md), [`ai/register-ai-risk.md`](../../ai/register-ai-risk.md), [`risk/template-risk-appetite-statement.md`](../../risk/template-risk-appetite-statement.md), [`ai/procedure-ai-system-impact-assessment.md`](../../ai/procedure-ai-system-impact-assessment.md), [`risk/procedure-risk-acceptance.md`](../../risk/procedure-risk-acceptance.md), [`governance/policy-exception-and-risk-acceptance-management.md`](../../governance/policy-exception-and-risk-acceptance-management.md), [`risk/template-board-risk-report.md`](../../risk/template-board-risk-report.md), [`ai/plan-ai-incident-response.md`](../../ai/plan-ai-incident-response.md), [`ai/standard-ai-security-and-risk.md`](../../ai/standard-ai-security-and-risk.md), [`supply-chain/procedure-third-party-ai-due-diligence.md`](../../supply-chain/procedure-third-party-ai-due-diligence.md), [`supply-chain/framework-supplier-and-cloud-governance.md`](../../supply-chain/framework-supplier-and-cloud-governance.md), [`supply-chain/register-concentration-risk.md`](../../supply-chain/register-concentration-risk.md), [`supply-chain/template-supplier-offboarding-evidence.md`](../../supply-chain/template-supplier-offboarding-evidence.md), [`ai/procedure-ai-model-lifecycle-management.md`](../../ai/procedure-ai-model-lifecycle-management.md), [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md)\
**External Sources:** None\
**Claim Classes Present:** citation, composite\
**Review Record:** NR-2026-013\
**Last Reviewed:** 2026-08-15

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Context for these questions

Oversight works through questions paired with evidence expectations. A question with no stated evidence expectation invites a narrative answer; each question below therefore carries a note on what a strong answer contains, so the reader can tell evidence from reassurance. The [board oversight guide](../../ai/guide-ai-board-oversight.md) establishes that the governing body is accountable for the organization's use of AI and that this accountability cannot be delegated to the AI system or to management (its section 2), and it provides the corpus's director question set as the governing body's primary oversight instrument (its section 5). This page routes to that set and deliberately does not reproduce it. Use the guide for the standing governance questions on duties, literacy, appetite, and reporting; use this page when examining management's operating evidence in five areas: inventory, material risk, incidents, suppliers, and change.

For each area, the corpus defines the register, record, or report a strong answer draws on, and each note below points to where. The pairing of a question with an evidence expectation is a composite reading across the sources this page lists; the limitations say so.

The questions are entity-neutral. They presume nothing about whether the asking body is a board, a board committee, or senior management holding the equivalent authority. The corpus's guidance on fitting its governance roles to smaller structures is the [minimum viable governance structure guideline](../../governance/guideline-minimum-viable-governance-structure.md).

## Questions

**Theme: inventory. Do we know what is running?**

- *Which AI systems do we operate or rely on, and when was the inventory last verified as complete?* A strong answer produces the register, not a summary of it. The [AI system register template](../../ai/template-ai-system-register.md) defines the fields a live register carries, including lifecycle status, the owner roles, the risk tier, and a next review date per system (its register fields section). Beneath it at model level, the [model registry](../../ai/register-model-registry.md) sets the deployment-entry gate and the periodic completeness-review expectation it sets in its operating expectations.
- *How would we find the AI in use that never came through approval?* A strong answer describes a control operating, not a policy stating that unapproved use is forbidden. The [AI governance and risk framework](../../ai/framework-ai-governance-and-risk.md) defines the shadow AI control boundary and what it must cover (its shadow AI control boundary section), and the register template's review questions begin with whether the system is recorded before use.
- *For each system in the highest risk tiers, who owns the system, the data, and the controls today?* A strong answer names the current accountable roles in the register's owner fields and shows the separate role-to-incumbent mapping is kept current as people move. The [board oversight guide](../../ai/guide-ai-board-oversight.md) names responsibility for an AI outcome attributed to the system or the vendor rather than an accountable person as a governance red flag (its section 6).
- *Which models and external dependencies sit underneath these systems?* A strong answer reads from the [model registry](../../ai/register-model-registry.md), whose schema and lineage tracking record what each model was built from and what depends on it.

**A weak answer in this theme:** a count with no date of last verification, or an inventory that contains only the systems the presenting team already knew about.

**Theme: material risk. Are we inside the appetite this body approved?**

- *What are our material AI risks, and are they within appetite?* A strong answer reads the [AI risk register](../../ai/register-ai-risk.md) against the approved [risk appetite statement](../../risk/template-risk-appetite-statement.md), whose Parts 2 and 3 carry the appetite categories and the tolerance boundaries. The register's schema records each risk's rating, owner, treatment, and review date.
- *For the systems in the highest risk tiers, what did their impact assessments conclude?* A strong answer produces the assessment records, with the tier assigned at the [impact assessment procedure](../../ai/procedure-ai-system-impact-assessment.md)'s Step 7 and the decision recorded at its Step 9, including the residual risk, conditions, and control owner the approval must record.
- *What residual AI risk have we formally accepted, who approved each acceptance, and when does it expire?* A strong answer produces acceptance records carrying the fields the [risk acceptance procedure](../../risk/procedure-risk-acceptance.md) requires, including owner, compensating controls, and expiry, approved at the authority the [exception and risk acceptance policy](../../governance/policy-exception-and-risk-acceptance-management.md) sets for the risk level (its section 4.2). An acceptance with no expiry, or an expiry that keeps rolling forward without reassessment, is itself a finding.
- *How does AI risk reach this body on a cadence, rather than only after something breaks?* A strong answer is the AI and emerging-technology section of the periodic risk report (the [board risk report template](../../risk/template-board-risk-report.md), its Section 9), delivered on the cadence the template sets.

**A weak answer in this theme:** risk reported only when an incident occurs. The [board oversight guide](../../ai/guide-ai-board-oversight.md) lists exactly that pattern among its governance red flags (its section 6).

**Theme: incidents. Would we recognize one, and could we reconstruct it?**

- *What counts as an AI incident here?* A strong answer produces the defined AI incident classes with their detection triggers and the severity criteria, as the [AI incident response plan](../../ai/plan-ai-incident-response.md) sets them out. An organization that has not defined the classes cannot report against them.
- *What AI incidents and near misses occurred in the period, and what did they change?* A strong answer combines the incidents section of the periodic risk report (the [board risk report template](../../risk/template-board-risk-report.md), its Section 6) with post-incident review outputs. The plan's post-incident review asks whether the evaluation suite would have detected the regression, whether the register was complete and current, and whether the supplier's contractual obligations were met, so each incident becomes a test of the other controls on this page.
- *For a serious incident, could we reconstruct what the system did?* A strong answer shows the evidence the [AI incident response plan](../../ai/plan-ai-incident-response.md) requires preserved for the incident severities it names, in classes including prompt logs, tool invocation logs, action lineage, and model version metadata (its evidence requirements section).
- *Are AI incidents escalated through the same incident discipline as everything else?* A strong answer shows AI incidents classified and escalated through incident management, covering the AI-specific incident types the [AI security and risk standard](../../ai/standard-ai-security-and-risk.md) lists (its section 4.10).

**A weak answer in this theme:** "we had no AI incidents" from an organization with no defined AI incident classes. Absence of detection is not absence of events.

**Theme: suppliers. Who puts AI into our operations, and on what terms?**

- *Which suppliers put AI into our operations, and what did due diligence conclude for each?* A strong answer produces the completed pre-engagement checklist and the supplier classification for each, per the [third-party AI due diligence procedure](../../supply-chain/procedure-third-party-ai-due-diligence.md) (its sections 4 and 5).
- *Do our contracts give us incident notification, model version change notification, audit rights, and deletion on exit?* A strong answer shows the contractual AI requirements in that procedure's section 6 evidenced supplier by supplier, not asserted in general.
- *Where are we concentrated, and what happens if a critical AI provider fails, changes terms, or becomes unavailable?* A strong answer reads from the [concentration risk register](../../supply-chain/register-concentration-risk.md) across the dimensions it tracks, together with the supplier and concentration section of the periodic risk report (the [board risk report template](../../risk/template-board-risk-report.md), its Section 8).
- *When we exit an AI supplier, can we show our data and models were returned or deleted?* A strong answer produces the completed offboarding record in the form the [supplier offboarding evidence template](../../supply-chain/template-supplier-offboarding-evidence.md) defines, with the exit and deletion steps of the [third-party AI due diligence procedure](../../supply-chain/procedure-third-party-ai-due-diligence.md) (its section 8) behind it.

**A weak answer in this theme:** a completed questionnaire presented as assurance. The [supplier and cloud governance framework](../../supply-chain/framework-supplier-and-cloud-governance.md) sets out a fuller evidence set for an adopting organization to maintain, including the due diligence record, the contract control schedule, assurance evidence, and reassessment records (its evidence requirements section).

**Theme: change. Who checks the system after it changes?**

- *What counts as a material change to an AI system, and what reassessment follows one?* A strong answer shows the last change classified against the material change thresholds the [AI governance and risk framework](../../ai/framework-ai-governance-and-risk.md) defines once for the whole corpus (its material change thresholds section), and the reassessment record produced when a threshold is crossed.
- *When a provider changes a model underneath us, how do we find out, and what happens next?* A strong answer shows version change notification operating under contract (the [third-party AI due diligence procedure](../../supply-chain/procedure-third-party-ai-due-diligence.md), its section 6.6) and a reassessment following the procedure's triggers (its section 7.4), classified against the framework's thresholds.
- *Are retrained or updated models re-tested to the same bar as new ones?* A strong answer produces retraining validation records. The [AI model lifecycle procedure](../../ai/procedure-ai-model-lifecycle-management.md) applies the same testing and validation requirements to retraining as to pre-deployment (its section 5).
- *Do AI changes pass through the organization's change discipline?* A strong answer produces change records with approvals, rollback plans, and post-implementation review, per the [change management procedure](../../operations/procedure-change-management-and-configuration-control.md) (its sections 2, 6, and 7).

**A weak answer in this theme:** "the vendor manages model updates." The [board oversight guide](../../ai/guide-ai-board-oversight.md) places accountability for the organization's AI use with the governing body and states that it cannot be delegated to the AI system or to management (its section 2); the contractual notification and reassessment controls above exist because providers change models.

## Evidence to request

Each item below is an evidence class the governing body can call for from management, and each is evidence for a named control or outcome.

- **The current AI system register extract and model registry extract**, as evidence of the inventory and ownership controls, in the structures the [AI system register template](../../ai/template-ai-system-register.md) and the [model registry](../../ai/register-model-registry.md) define.
- **The AI risk register read against the approved appetite statement**, as evidence that material AI risk is tracked against the appetite the governing body approved, per the [AI risk register](../../ai/register-ai-risk.md) and the [risk appetite statement](../../risk/template-risk-appetite-statement.md).
- **Impact assessment records with their approval decisions for the highest-tier systems**, as evidence that the assessment gate operated, per the [impact assessment procedure](../../ai/procedure-ai-system-impact-assessment.md) (its Steps 7 and 9).
- **Risk acceptance and exception records with owners, compensating controls, and expiries**, as evidence for the risk acceptance control, per the [risk acceptance procedure](../../risk/procedure-risk-acceptance.md) and the [exception and risk acceptance policy](../../governance/policy-exception-and-risk-acceptance-management.md).
- **The periodic risk report's AI, incident, and supplier sections, with their delivery record**, as evidence for the reporting expectation the [board oversight guide](../../ai/guide-ai-board-oversight.md) sets (its section 7), in the structure of the [board risk report template](../../risk/template-board-risk-report.md).
- **The defined AI incident classes and the most recent post-incident review output**, as evidence that the incident path is defined and has been exercised, per the [AI incident response plan](../../ai/plan-ai-incident-response.md).
- **Per-supplier due diligence records and the contract control schedule**, as evidence for supplier governance, per the [third-party AI due diligence procedure](../../supply-chain/procedure-third-party-ai-due-diligence.md) and the [supplier and cloud governance framework](../../supply-chain/framework-supplier-and-cloud-governance.md).
- **The concentration risk register extract**, as evidence that concentration exposure is identified and treated, per the [concentration risk register](../../supply-chain/register-concentration-risk.md).
- **Completed offboarding evidence for the most recent AI supplier exit**, as evidence that exits are controlled, per the [supplier offboarding evidence template](../../supply-chain/template-supplier-offboarding-evidence.md).
- **The last material change classification and its reassessment record, with the change records behind it**, as evidence that change control engages for AI, per the [AI governance and risk framework](../../ai/framework-ai-governance-and-risk.md), the [AI model lifecycle procedure](../../ai/procedure-ai-model-lifecycle-management.md), and the [change management procedure](../../operations/procedure-change-management-and-configuration-control.md).

## Limitations

- This page creates no compliance and imposes no requirement. The linked corpus documents govern; where this page differs from a corpus document, the corpus document prevails.
- These questions are advisory. They organize a line of questioning; the decision about what to ask, and what to accept as an answer, remains entirely with the reader's organization.
- This page carries composite claims. The pairing of each question with an evidence expectation, and the weak-answer characterizations, are synthesized across the listed corpus sources, and the adopting organization validates that reading against its own governance model, committee structure, and delegation of authority.
- This set is not exhaustive. The [board oversight guide](../../ai/guide-ai-board-oversight.md) covers director duties, literacy, appetite setting, and reporting expectations; this page extends that instrument into operating evidence and does not repeat it.
- Every threshold, cadence, severity level, tier name, register field, and approval authority lives in the corpus documents this page links. This page routes to them and does not reproduce them; that routing is a contribution to the corpus's status as the single source for every value.
- Expected evidence describes what the corpus defines, not what any given organization has implemented. A gap between the two is itself an oversight finding, to be handled through the risk and exception routes the corpus provides rather than by softening the question.
- This page makes no claim about how likely any failure is, and none of its statements should be read as a probability or a frequency.

**End of Document**
