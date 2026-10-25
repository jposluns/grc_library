# From AI idea to retirement: the governed life of an AI system

**Document Title:** From AI idea to retirement: the governed life of an AI system\
**Document Type:** Executive Narrative\
**Version:** 0.0.4\
**Date:** 2026-08-31\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`ai/framework-ai-governance-and-risk.md`](../../ai/framework-ai-governance-and-risk.md), [`ai/procedure-ai-system-impact-assessment.md`](../../ai/procedure-ai-system-impact-assessment.md), [`ai/procedure-ai-model-lifecycle-management.md`](../../ai/procedure-ai-model-lifecycle-management.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/journeys/journey-ai-idea-to-retirement.md`](journey-ai-idea-to-retirement.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Journey\
**Narrative Status:** Explanatory\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`ai/guide-ai-board-oversight.md`](../../ai/guide-ai-board-oversight.md), [`ai/framework-ai-governance-and-risk.md`](../../ai/framework-ai-governance-and-risk.md), [`ai/template-ai-system-register.md`](../../ai/template-ai-system-register.md), [`ai/procedure-ai-system-impact-assessment.md`](../../ai/procedure-ai-system-impact-assessment.md), [`risk/annex-ai-risk-methodology.md`](../../risk/annex-ai-risk-methodology.md), [`ai/procedure-training-data-governance.md`](../../ai/procedure-training-data-governance.md), [`ai/standard-ai-security-and-risk.md`](../../ai/standard-ai-security-and-risk.md), [`ai/standard-ai-access-and-agent-permissions.md`](../../ai/standard-ai-access-and-agent-permissions.md), [`ai/standard-ai-testing-validation-and-documentation.md`](../../ai/standard-ai-testing-validation-and-documentation.md), [`ai/procedure-ai-evaluation.md`](../../ai/procedure-ai-evaluation.md), [`ai/charter-ai-governance-council.md`](../../ai/charter-ai-governance-council.md), [`governance/policy-exception-and-risk-acceptance-management.md`](../../governance/policy-exception-and-risk-acceptance-management.md), [`operations/procedure-change-management-and-configuration-control.md`](../../operations/procedure-change-management-and-configuration-control.md), [`ai/procedure-ai-model-lifecycle-management.md`](../../ai/procedure-ai-model-lifecycle-management.md), [`ai/plan-ai-incident-response.md`](../../ai/plan-ai-incident-response.md), [`ai/procedure-ai-audit.md`](../../ai/procedure-ai-audit.md), [`governance/standard-records-retention-and-destruction.md`](../../governance/standard-records-retention-and-destruction.md), [`supply-chain/template-supplier-offboarding-evidence.md`](../../supply-chain/template-supplier-offboarding-evidence.md)\
**External Sources:** None\
**Claim Classes Present:** citation, composite\
**Review Record:** NR-2026-008\
**Last Reviewed:** 2026-08-15

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Starting state

Somewhere in the organization, a team has an idea for an AI system. The organization is not starting from nothing: the [AI board oversight guide](../../ai/guide-ai-board-oversight.md) sets out the governing body's role relative to management and its relationship to enterprise risk governance (its section 4). What does not yet exist is anything attached to the idea itself: no record, no owner, no risk classification, no controls, and no route to a decision. The [AI governance and risk framework](../../ai/framework-ai-governance-and-risk.md) defines a lifecycle model that runs from intake to retirement, with a governance requirement and an evidence class for each stage. This journey follows one system along that lifecycle. It is a composite illustration: it depicts no identifiable organization, and the adopting organization maps each stage onto its own structure through the linked corpus documents.

## Stages

### Stage 1: the idea is recorded

**What changes.** Before the system is used, it is recorded. This journey is at the member labelled **Intake**, the first of the [AI governance and risk framework](../../ai/framework-ai-governance-and-risk.md)'s eleven-stage lifecycle model; use the framework for that member's governance requirement and evidence class. The [AI system register template](../../ai/template-ai-system-register.md) provides the reusable structure for that record, and the [AI system impact assessment procedure](../../ai/procedure-ai-system-impact-assessment.md) defines what registration captures at its Step 1. The framework also draws a shadow AI control boundary over unapproved AI services and tools; use the framework's Shadow AI boundary for its coverage and intake conditions. The [AI model lifecycle management procedure](../../ai/procedure-ai-model-lifecycle-management.md) governs the AI system inventory in its section 1; use that section for the inventory's ownership and review cadence.

**Why it matters.** The register entry is a dependency for the stages that follow: the classification, testing, and approval records this journey describes attach to it. The shadow AI boundary is a prevention against AI use that has bypassed intake escaping governance.

**Signals of progress.** The Intake record and the Shadow AI records the framework names exist and are reviewable.

### Stage 2: the system is classified and assessed

**What changes.** The recorded system is given a risk tier and an impact assessment. The [AI risk methodology annex](../../risk/annex-ai-risk-methodology.md) requires each AI system to be assigned a risk tier on the basis its AI system risk classification section defines, before the risk assessment methodology is applied, and requires the tier classification to be documented; the tier set and its regulatory mapping live in the annex. The [AI system impact assessment procedure](../../ai/procedure-ai-system-impact-assessment.md) walks the registered system through its ten steps, assigns a risk tier at its Step 7, defines required controls at its Step 8, and lists its required outputs; use the procedure for those steps. Where a training, fine-tuning, or reinforcement-learning pipeline will consume a dataset, the [training data governance procedure](../../ai/procedure-training-data-governance.md) owns **Step 4: Approval to train**; use that step for the pre-consumption approvals, their triggers, and the approver roles.

**Why it matters.** The assigned tier is a dependency for Stage 4, where the corpus sets testing and approval requirements by tier. The completed assessment is evidence that the organization examined what the system is, whom it affects, and what risk it carries before any deployment decision.

**Signals of progress.** A documented tier, an assessment record, and a defined control set exist for the system, and training-data approvals are recorded before a pipeline consumes the data.

### Stage 3: controls are designed before the build completes

**What changes.** The controls the system will run under are defined while it is still being built. The [AI security and risk standard](../../ai/standard-ai-security-and-risk.md) sets the minimum security and risk controls for AI systems in its section 4; individual controls there carry their own lifecycle timing, and this page points to the section for the baseline rather than reproducing it. Where the system is agentic, with a model that invokes tools, the [AI access and agent permissions standard](../../ai/standard-ai-access-and-agent-permissions.md) governs the AI-to-tool surface in its section 6; the specific requirements live in the standard. For this stage, use the member labelled **Design and Configuration** in the [AI governance and risk framework](../../ai/framework-ai-governance-and-risk.md)'s eleven-stage lifecycle for its governance requirement and evidence class.

**Why it matters.** The design-stage artefacts are evidence for the framework's **Design and Configuration** member, and they are a contribution to the Stage 4 decision, whose record the impact-assessment procedure's Step 9 defines.

**Signals of progress.** The architecture record, control design, and threat model exist as reviewable artefacts, and an agentic system has its tool allow-list and confirmation rules defined under the standard.

### Stage 4: testing, evaluation, and the approval decision

**What changes.** The system faces its gates. The [AI testing, validation and documentation standard](../../ai/standard-ai-testing-validation-and-documentation.md) sets the testing requirements in its sections 5 and 8; the gate definitions and the per-tier table live in the standard. Under the [AI evaluation procedure](../../ai/procedure-ai-evaluation.md), the evaluation report goes to the chartered AI oversight body for its review (the procedure's Step 4); review timing lives in the procedure. The oversight body's mandate and its deployment-approval authority are defined in its [corpus charter](../../ai/charter-ai-governance-council.md) (its Scope of authority section), which this page routes to for the body's name, composition, committee relationships, and the classes of AI system deployment it may approve or reject. The [AI system impact assessment procedure](../../ai/procedure-ai-system-impact-assessment.md) requires the approving authority, at its Step 9, to decide from the closed outcome set the procedure lists and to record the fields Step 9 defines. Where an exception would carry risk beyond the organization's appetite, the [exception and risk acceptance management policy](../../governance/policy-exception-and-risk-acceptance-management.md) governs its acceptance and maintenance in its sections 4.2 and 4.3, with the approval levels, terms, and ceiling values in the policy.

**Why it matters.** The testing gates are the standard's pre-production requirement; the standard defines what they cover. A recorded Step 9 decision is evidence that the decision gate operated; interpret its outcome and record through the impact-assessment procedure's Step 9, and route any beyond-appetite acceptance through the exception policy.

**Signals of progress.** Test results exist for the gates the standard requires at the system's tier, a recorded Step 9 decision exists, and any beyond-appetite acceptance appears in the exception register as a time-bound entry.

### Stage 5: governed release and life in production

**What changes.** The approved system is released and operated. The [AI model lifecycle management procedure](../../ai/procedure-ai-model-lifecycle-management.md) owns seven ordered lifecycle sections; this journey engages the members labelled **Production deployment** (section 3) and **Ongoing monitoring** (section 4). Use those members for their deployment controls and records, the per-model threshold structure, the below-threshold review and its outcomes, and the monitoring-reporting requirements. The change lifecycle itself is defined in the [change management and configuration control procedure](../../operations/procedure-change-management-and-configuration-control.md). If an AI incident occurs, the [AI incident response plan](../../ai/plan-ai-incident-response.md) defines the AI incident classes and their detection triggers, the severity criteria, the response lifecycle, and the evidence preserved for the incident severities the plan names. The [AI audit procedure](../../ai/procedure-ai-audit.md) adds independent assurance; use its section 7 for the reporting lines and cadence.

**Why it matters.** The recorded thresholds feed the **Ongoing monitoring** review the procedure defines; use that member for its review trigger. Monitoring records, incident records, and audit reports are the evidence to inspect when testing whether the monitoring, incident-response, and assurance controls operated after go-live; their contents and outcomes, including any nonconformities or incomplete responses, are what the reader assesses, since a record can also document a control failure.

**Signals of progress.** The deployment, monitoring-review, and audit-reporting records the linked procedures require exist and are reviewable.

### Stage 6: a material change requires reassessment and an updated approval

**What changes.** A production system can change in the ways the framework's **Material change thresholds** name. The [AI governance and risk framework](../../ai/framework-ai-governance-and-risk.md) defines when a change is material across the dimensions its threshold table names; the threshold values are library defaults an organization may calibrate, and they live in the framework. At the member labelled **Change** in the framework's eleven-stage lifecycle, use the framework for that member's governance requirement and evidence class. The [AI model lifecycle management procedure](../../ai/procedure-ai-model-lifecycle-management.md) sets the retraining requirements in its section 5, and under the [AI evaluation procedure](../../ai/procedure-ai-evaluation.md) a rejected system's return to service is governed by its Step 5, with material defined by the framework's threshold table. Changes to production systems follow the [change management and configuration control procedure](../../operations/procedure-change-management-and-configuration-control.md); use that procedure for its change controls.

**Why it matters.** The framework's **Change** member carries the reassessment stage's rationale and evidence class; use the linked framework for them. Its evidence, which the framework's **Change** member defines, is what the reader inspects to confirm the reassessment.

**Signals of progress.** Change records exist for the system's changes, and reassessments and approval updates exist where the framework's thresholds were crossed.

### Stage 7: retirement leaves evidence behind

**What changes.** The system reaches the end of its life. This journey engages the member labelled **Decommissioning** (section 7) in the [AI model lifecycle management procedure](../../ai/procedure-ai-model-lifecycle-management.md)'s seven ordered lifecycle sections; use that member for its decommissioning triggers and ordered checklist. The [AI security and risk standard](../../ai/standard-ai-security-and-risk.md) requires AI systems to be retired under the decommissioning controls its section 4.11 defines. The [records retention and destruction standard](../../governance/standard-records-retention-and-destruction.md) requires AI training datasets, test results, and model versions to be retained to support audit and reproducibility obligations (its section 9) and requires destruction actions to be logged in the destruction register it defines (its section 8.2). Where retiring the system also ends the relationship with a supplier that held the organization's data, the [supplier offboarding evidence template](../../supply-chain/template-supplier-offboarding-evidence.md) provides the structure for the data return and destruction evidence (its Section 3); its scope is third-party relationships that are ending, so where the supplier relationship continues, the deletion evidence is governed by the instrument that applies to that case rather than by this template.

**Why it matters.** The retained decommission record and the destruction documentation are evidence to inspect when testing whether the retirement controls operated. The retention requirements serve the longer-lived obligations the retention standard defines, which outlast the system itself.

**Signals of progress.** The completed checklist, the deletion or retention attestations, and the updated inventory status exist, and the records the retention standard requires are retrievable after the system is switched off.

## Destination state

The system no longer runs, and the intended evidence trail spans its life: the records the corpus defines are meant to show what tier it carried, what was tested, who approved it and on what conditions, how it behaved in production, what changed and who reassessed it, and how it ended. Whether that trail is complete for any given system is what the evidence classes below are used to test. Nothing about the destination depends on this particular system: the same recorded path is what the next idea enters at Stage 1. The destination is not an organization without AI risk; it is an organization whose AI risk is recorded, classified, tested, approved, monitored, and finally retired, with the records the corpus requires available to show it.

## Evidence to request

Each item below is an evidence class the governing body can call for from management, and each is evidence for a named control or outcome. Judge each against the linked corpus document, which carries the specific requirements.

- **The AI inventory entry for a sampled system**, as evidence for the recording control, per the [AI governance and risk framework](../../ai/framework-ai-governance-and-risk.md) and the structure in the [AI system register template](../../ai/template-ai-system-register.md).
- **The completed impact assessment with its tier decision and required outputs**, as evidence for the classification and assessment controls in the [AI risk methodology annex](../../risk/annex-ai-risk-methodology.md) and the [AI system impact assessment procedure](../../ai/procedure-ai-system-impact-assessment.md).
- **Training-data approval records for a trained or fine-tuned system**, as evidence for the approval-to-train control in the [training data governance procedure](../../ai/procedure-training-data-governance.md).
- **The architecture record, control design, and threat model**, as evidence for the design-stage controls in the [AI governance and risk framework](../../ai/framework-ai-governance-and-risk.md) and the control baseline in the [AI security and risk standard](../../ai/standard-ai-security-and-risk.md), including the agent surface in the [AI access and agent permissions standard](../../ai/standard-ai-access-and-agent-permissions.md) where the system invokes tools.
- **Tier-matched test results and the evaluation report**, as evidence for the testing gates in the [AI testing, validation and documentation standard](../../ai/standard-ai-testing-validation-and-documentation.md) and the review in the [AI evaluation procedure](../../ai/procedure-ai-evaluation.md).
- **The Step 9 approval record**, as evidence that the approval control operated, per the [AI system impact assessment procedure](../../ai/procedure-ai-system-impact-assessment.md) and the authority defined in the oversight body's [corpus charter](../../ai/charter-ai-governance-council.md).
- **Exception register entries touching AI systems that were determined to exceed risk appetite**, as evidence for the beyond-appetite acceptance route the [exception and risk acceptance management policy](../../governance/policy-exception-and-risk-acceptance-management.md) defines (its section 4.2).
- **The deployment record and the associated change records**, as evidence for the governed-release controls in the [AI model lifecycle management procedure](../../ai/procedure-ai-model-lifecycle-management.md) and the [change management and configuration control procedure](../../operations/procedure-change-management-and-configuration-control.md).
- **Monitoring review records and any AI incident records**, to inspect when testing whether the monitoring and incident-response controls operated, assessing their contents and outcomes rather than treating their existence as proof, per the [AI model lifecycle management procedure](../../ai/procedure-ai-model-lifecycle-management.md) and the [AI incident response plan](../../ai/plan-ai-incident-response.md).
- **AI audit reports and the governance reporting they feed**, as evidence for the independent assurance control and its reporting line in the [AI audit procedure](../../ai/procedure-ai-audit.md); the [AI board oversight guide](../../ai/guide-ai-board-oversight.md) describes what the governing body should expect to receive on AI (its section 7).
- **The decommissioning checklist, destruction documentation, and, where the system's retirement also ends a supplier relationship, the supplier offboarding evidence for a retired system**, to inspect when testing whether the retirement controls operated, per the [AI model lifecycle management procedure](../../ai/procedure-ai-model-lifecycle-management.md), the [records retention and destruction standard](../../governance/standard-records-retention-and-destruction.md), and the [supplier offboarding evidence template](../../supply-chain/template-supplier-offboarding-evidence.md), which applies where a supplier relationship is ending.

## Limitations

- This page creates no compliance and establishes no requirement. The linked corpus documents govern, and the adopting organization must validate applicability to its own structure, jurisdictions, and systems.
- This journey is a composite illustration assembled across multiple corpus documents. The seven-stage sequence, the starting and destination states, and every "why it matters" and "signals of progress" reading are synthesized rather than stated by any single source, and composite content requires the adopting organization's own validation.
- The corpus documents name specific oversight bodies and roles. This page refers to them generically (the chartered AI oversight body, the approving authority, a named role), and the reader takes the actual names, compositions, and committee relationships from the linked documents. The adopting organization maps them to its own governance model, which may combine or rename them.
- Specific values are deliberately absent. Tier sets and tier labels, testing requirements per tier, review timing, monitoring and reporting cadences, material-change threshold values, exception terms and ceilings, approval levels, and retention periods live only in the linked corpus documents, and the reader must take them from there.
- Reading this journey confers understanding only. A stage described here is not evidence that the corresponding control operates in any organization; the evidence classes above are how the reader tests that.
- This page makes no likelihood, frequency, or statistical claim about AI failures or their outcomes.

**End of Document**
