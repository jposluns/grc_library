# From retention rule to destruction evidence: the governed journey of a record

**Document Title:** From retention rule to destruction evidence: the governed journey of a record\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-08-17\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/standard-records-retention-and-destruction.md`](../../governance/standard-records-retention-and-destruction.md), [`governance/register-data-retention-schedule.md`](../../governance/register-data-retention-schedule.md), [`compliance/procedure-control-testing.md`](../../compliance/procedure-control-testing.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/journeys/journey-record-retention-destruction.md`](journey-record-retention-destruction.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Journey\
**Narrative Status:** Explanatory\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`governance/standard-records-retention-and-destruction.md`](../../governance/standard-records-retention-and-destruction.md), [`governance/register-data-retention-schedule.md`](../../governance/register-data-retention-schedule.md), [`privacy/policy-privacy-and-data-governance.md`](../../privacy/policy-privacy-and-data-governance.md), [`resilience/procedure-backup-and-recovery.md`](../../resilience/procedure-backup-and-recovery.md), [`supply-chain/procedure-supplier-exit-and-data-return.md`](../../supply-chain/procedure-supplier-exit-and-data-return.md), [`compliance/procedure-control-testing.md`](../../compliance/procedure-control-testing.md), [`compliance/template-audit-evidence-package.md`](../../compliance/template-audit-evidence-package.md), [`risk/register-assurance-map.md`](../../risk/register-assurance-map.md)\
**External Sources:** None\
**Claim Classes Present:** citation, composite\
**Review Record:** NR-2026-019\
**Last Reviewed:** 2026-08-17

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Starting state

Organizations hold records they must be able to produce on demand, and records they must one day be able to show were destroyed. The corpus separates the rule from the values it applies to. The [records retention and destruction standard](../../governance/standard-records-retention-and-destruction.md) owns the lifecycle controls: how retention schedules are used (its section 5), how a hold suspends disposal (its section 7, Retention hold and litigation freeze), how destruction is carried out and documented (its section 8), and how the whole control is monitored and audited (its section 11). The [data retention schedule register](../../governance/register-data-retention-schedule.md) states that it implements that standard, and it carries the record-class values themselves: for each record class, a schedule row in the register's Data retention schedule section holds the retention period and its legal basis. On the privacy side, the [privacy and data governance policy](../../privacy/policy-privacy-and-data-governance.md) requires records to be held under approved schedules and destroyed verifiably (its section 4.4).

This journey follows one record, of any class, from the moment its retention rule is identified to the moment independent assurance can speak to its disposition. No retention period, hold condition, destruction method, or test value appears on this page; each stays in the corpus document that owns it, and this page links there. The six stages below are a reader-navigation order across the linked documents, assembled for this page as a composite; they are not a new operating procedure, and the linked corpus documents alone govern how the work is done.

## Stages

### Stage 1: the rule resolves to its source

**What changes.** A statement such as "we keep this for as long as required" stops being an assertion and becomes a pointer. For the record's class, management can name the applicable row in the [data retention schedule register](../../governance/register-data-retention-schedule.md) and the governing sections of the [records retention and destruction standard](../../governance/standard-records-retention-and-destruction.md): its section 5 defines the bases on which minimum retention periods are set and the domain-level minimums, and the register's schedule rows carry the class-level values and their legal rationale. The direction of authority matters and runs one way: the standard governs how the schedule is used, and the register implements the standard. The value itself stays in the register, and this page does not repeat it.

**Why it matters.** The mapping from record class to schedule row is a dependency for every later stage: a hold, a backup decision, or a destruction action can only be judged against a rule that has a named source.

**Signals of progress.** A retention mapping exists for the record class: the class, the applicable schedule row, and the governing standard section, each identified by pointer.

### Stage 2: a hold changes disposition authority

**What changes.** When the record becomes subject to one of the proceedings the standard names, the question "may this be destroyed" stops being a calendar question. Section 7 of the [records retention and destruction standard](../../governance/standard-records-retention-and-destruction.md) owns the retention hold: what triggers it, the controls that apply while it stands, how its status is tracked, and who lifts it. The [data retention schedule register](../../governance/register-data-retention-schedule.md)'s Principles section states how holds interact with the schedule's periods. Management can show, for this record, whether section 7 applies before any disposal decision is made.

**Why it matters.** The hold is a prevention against destroying a record the organization is obliged to preserve. Stage 4 has a dependency on hold status being known and current.

**Signals of progress.** A hold-status record exists for the record, showing whether a hold applies and, where one does, its state under the standard's section 7.

### Stage 3: managed copies remain in scope

**What changes.** The record is more than its primary copy, and the control's view widens to match. Under the [backup and recovery procedure](../../resilience/procedure-backup-and-recovery.md), each system's backup scope must be documented (its Requirement 1), backups must be protected against failure modes that include inappropriate retention (its Requirement 3), recovery for AI-related data must consider retention and enforceable deletion requirements (its Requirement 6), and its Requirement 7 addresses the contractual and assurance evidence for supplier-provided backup or recovery, including deletion capability and exit support. Where copies of the record move between jurisdictions, section 4.6 of the [privacy and data governance policy](../../privacy/policy-privacy-and-data-governance.md) owns the cross-border transfer requirements; the permitted mechanisms and review cadence live in the policy. And when a supplier relationship that held the organization's data ends, the [supplier exit and data return procedure](../../supply-chain/procedure-supplier-exit-and-data-return.md) owns the deletion route at its Step 4, Supplier data deletion, including the deletion instruction, the supplier's written confirmation, and what happens when that confirmation cannot be obtained; the actions, roles, and deadlines live in the procedure.

**Why it matters.** Destroying the primary copy while a backup or a supplier still holds the record is not defensible disposal. Coverage of managed copies is a dependency of the destination state this journey describes.

**Signals of progress.** A deletion or retention attestation of the kind the backup procedure's Evidence requirements section names exists for the backup estate, and a supplier-deletion record exists for any supplier exit that involved the record's data.

### Stage 4: disposition uses the governed route

**What changes.** An eligible record leaves the estate through one route. Section 8 of the [records retention and destruction standard](../../governance/standard-records-retention-and-destruction.md) governs when a record becomes eligible for destruction and how destruction is performed: the acceptable methods per media type are defined in its section 8.1, and its section 8.2 requires every destruction action to be logged in the Destruction Register it defines, with the entry contents and certificate requirements stated there. This page names the register and points to it; the fields of an entry are the standard's to define.

**Why it matters.** The destruction record is evidence that the disposal control operated for this specific record. Without it, destruction is an event with no account; the record is the account, readable years later against the rule identified at Stage 1.

**Signals of progress.** A destruction record exists for the disposed record, in the form the standard's section 8.2 requires.

### Stage 5: operation becomes auditable

**What changes.** Individual records of retention, holds, and destruction become reviewable at the control level. The [audit evidence package template](../../compliance/template-audit-evidence-package.md) packages per-control evidence into a bundle prepared for outside review (its Purpose section). Its per-control section template separates implementation evidence, taken at a point in time, from operating evidence, taken over the period, and records a verification basis for each; its package-level sign-off section closes the bundle. The distinction between those two evidence kinds is the template's to define, and the reader takes it from there.

**Why it matters.** An outside reviewer needs to distinguish "this control exists" from "this control operated across the period." The packaged evidence is a contribution to that review being possible at all. The verification basis records, for each item, whether the evidence has already been independently tested or is asserted by its owner.

**Signals of progress.** A per-control evidence package exists for the retention and destruction control, in the template's structure.

### Stage 6: independent testing and assurance close the view

**What changes.** Someone independent of the control examines it. The [control testing procedure](../../compliance/procedure-control-testing.md) owns the methodology: design effectiveness testing and operating effectiveness testing are defined in its sections 2.1 and 2.2, its section 3 governs the working papers and evidence behind each test, its section 4 classifies results and defines the response each classification requires, and its section 6 governs remediation, including re-testing before a finding is closed. The outcome then joins the organization's assurance picture, where records retention is within the assurance map's coverage: the [assurance map register](../../risk/register-assurance-map.md) provides the entry structure its Section 2 defines for that risk area, its Section 6 defines the map's governance, including how material gaps reach the risk reporting the governing body receives, its Section 7 feeds the assurance plans built from the map, and its Section 8 governs how a gap is tracked to closure.

**Why it matters.** Test results are evidence for whether the retention control operates, and evidence of a failure is as valuable to the reader as evidence of success. The assurance-map entry is a contribution to leadership seeing retention alongside every other assured risk area rather than as an isolated compliance topic.

**Signals of progress.** A test workpaper exists for the retention control, a re-test record exists where a finding was remediated, and an assurance-map entry covers the records-retention risk area.

## Destination state

For one record, leadership can trace the whole account by pointer: the rule and its schedule row, the hold status at the time of disposal, the treatment of backup and supplier-held copies, the destruction record, the packaged evidence, the independent test result, and, where records retention is within the map's coverage, the assurance-map view that carries a material gap to the governing body. Every value in that account lives in a linked corpus document rather than on this page. This destination is a composite reading assembled across the eight linked sources; describing it here is not a claim that the control operates, or has ever operated, in any adopting organization. Whether the account is complete for a given record is what the evidence classes below are for.

## Evidence to request

Each item below is an evidence class the governing body can call for from management, named by type only; the linked corpus document defines the artefact's required contents. Each is evidence for a named control or outcome.

- **A retention mapping for a sampled record class**, as evidence for the schedule-resolution control: the class, its schedule row in the [data retention schedule register](../../governance/register-data-retention-schedule.md), and the governing section of the [records retention and destruction standard](../../governance/standard-records-retention-and-destruction.md).
- **A hold-status record for a sampled record**, as evidence for the retention-hold control in the [records retention and destruction standard](../../governance/standard-records-retention-and-destruction.md) (its section 7).
- **A deletion or retention attestation for the backup estate**, as evidence that a retention or deletion requirement reaches backup operations under the [backup and recovery procedure](../../resilience/procedure-backup-and-recovery.md) (its Evidence requirements section).
- **A supplier-deletion record for a completed supplier exit**, where one has occurred, as evidence for the supplier-deletion route in the [supplier exit and data return procedure](../../supply-chain/procedure-supplier-exit-and-data-return.md) (its Step 4).
- **A destruction record for a disposed record**, as evidence for the secure-destruction control in the [records retention and destruction standard](../../governance/standard-records-retention-and-destruction.md) (its section 8), read together with the monitoring its section 11 defines.
- **A per-control evidence package for the retention and destruction control**, as evidence that the control's operation is packaged for independent review in the structure of the [audit evidence package template](../../compliance/template-audit-evidence-package.md).
- **A test workpaper, and a re-test record where a finding was remediated**, as evidence for independent testing of the control under the [control testing procedure](../../compliance/procedure-control-testing.md); assess the recorded result and any findings rather than treating the workpaper's existence as the answer.
- **The assurance-map entry for the records-retention risk area**, as evidence that the area sits inside the assurance coverage and gap reporting the [assurance map register](../../risk/register-assurance-map.md) defines.

## Limitations

- This page creates no compliance and establishes no requirement. The linked corpus documents govern, and the adopting organization must validate applicability against its own legal, regulatory, and operational context, including the jurisdictions its records touch.
- The six-stage sequence is explanatory navigation assembled for this page. No single corpus source states it, it prescribes no operating order, and composite content of this kind requires the adopting organization's own validation.
- Specific values are deliberately absent. Retention periods and their bases, hold triggers and controls, destruction methods and register contents, supplier-deletion actions and timeframes, evidence-package fields, testing methods, samples, and result classifications, and assurance ratings live only in the linked corpus documents, and the reader must take them from there.
- The corpus documents name specific roles and bodies for these controls. This page refers to them generically, and the adopting organization maps them onto its own structure, which may combine or rename them.
- Reading this journey confers understanding only. A stage described here says nothing about whether the corresponding control operates in any organization; that question belongs to the evidence classes above, and a record produced under them can document a control failure as readily as a success.
- This page makes no likelihood, frequency, or statistical claim.

**End of Document**
