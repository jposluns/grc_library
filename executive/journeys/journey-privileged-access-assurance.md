
# From policy intent to independent assurance: the journey of a privileged-access control

**Document Title:** From policy intent to independent assurance: the journey of a privileged-access control\
**Document Type:** Executive Narrative\
**Version:** 0.0.1\
**Date:** 2026-08-17\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`security/policy-identity-and-access-management.md`](../../security/policy-identity-and-access-management.md), [`security/standard-privileged-access-management.md`](../../security/standard-privileged-access-management.md), [`compliance/procedure-control-testing.md`](../../compliance/procedure-control-testing.md)\
**Classification:** Public\
**Category:** Executive Narrative\
**Review Frequency:** Annual, and a 6-month advisory executive review\
**Repository Path:** [`executive/journeys/journey-privileged-access-assurance.md`](journey-privileged-access-assurance.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0\
**Narrative Type:** Journey\
**Narrative Status:** Explanatory\
**Audience:** Governing body and accountable executive leadership (board, ELT, or senior management, as applicable)\
**Corpus Sources:** [`security/policy-identity-and-access-management.md`](../../security/policy-identity-and-access-management.md), [`security/standard-privileged-access-management.md`](../../security/standard-privileged-access-management.md), [`security/procedure-access-control.md`](../../security/procedure-access-control.md), [`security/procedure-identity-management.md`](../../security/procedure-identity-management.md), [`security/standard-logging-and-monitoring.md`](../../security/standard-logging-and-monitoring.md), [`compliance/procedure-control-testing.md`](../../compliance/procedure-control-testing.md), [`risk/register-assurance-map.md`](../../risk/register-assurance-map.md), [`risk/template-board-risk-report.md`](../../risk/template-board-risk-report.md)\
**External Sources:** None\
**Claim Classes Present:** citation, composite\
**Review Record:** NR-2026-018\
**Last Reviewed:** 2026-08-17

---

> **Authority disclaimer.** This page is an executive narrative. It does not establish requirements; the linked corpus governs. It is provided to support understanding, discussion, and decision-making by the governing body and accountable executive leadership (board, ELT, or senior management, as applicable). It creates no obligation, control, or assurance by itself. Its publication approval is an editorial act only and confers no authority over any corpus document. Where it differs from a corpus document, the corpus document prevails.

## Starting state

Some identities hold the power to change systems, data, and other people's access. That power is privileged access, and the corpus places its governing authority in the [identity and access management policy](../../security/policy-identity-and-access-management.md): its section 4.4 owns the privileged access management requirements, and its section 4.5 owns access review and certification. A published requirement, on its own, gives leadership no way to inspect whether it is implemented, whether it operates day to day, or whether anyone independent of its owner has tested it. That inspection needs four further views: the implementing control, the records its operation leaves behind, the independent test of its design and operation, and the reporting slot where the result reaches leadership. This journey walks one privileged-access control through those views. The stages below are a reader navigation order across linked corpus documents; they are not a new lifecycle, and they add no step to any procedure.

## Stages

The stage order organizes the reader's path through the linked documents. The documents themselves own every requirement, sequence, and value.

### Stage 1: the authority is located

**What changes.** The reader can name the corpus document and sections that govern privileged access. The [identity and access management policy](../../security/policy-identity-and-access-management.md) is that authority: its section 4.4 (privileged access management) owns the requirements for privileged accounts, sessions, and emergency access, and its section 4.5 (access review and certification) owns the requirements for periodically certifying access rights. The requirements themselves, including every period and remediation window, live in those subsections.

**Why it matters.** The located authority is a dependency for everything that follows: the implementing standard, the operating records, and the independent test all attach to the requirement the policy states.

**Signals of progress.** A policy-to-control mapping exists as a reviewable artefact, naming the control that implements the privileged-access requirement.

### Stage 2: implementation becomes inspectable

**What changes.** The reader can follow the requirement into the documents that implement it. The [privileged access management standard](../../security/standard-privileged-access-management.md) defines the implementation approach in its section 4, including the key control set its section 4.2 owns, and it also owns the privileged account lifecycle (its section 5) and the incident route for a suspected privileged-account compromise (its section 6). The [access control procedure](../../security/procedure-access-control.md) operationalizes access request and approval in its section 1 and the additional privileged-access controls in its section 6. The [identity management procedure](../../security/procedure-identity-management.md) owns privileged identity management in its section 3. The control tables, activation rules, approval routes, and timelines live in those sections and are not restated here.

**Why it matters.** An inspectable implementation route is a dependency for Stage 5, the independent test of the control's stated design.

**Signals of progress.** An approved access-control design exists, carrying its references to the standard and procedures that govern it.

### Stage 3: operation leaves evidence

**What changes.** The control's operation can be examined through the records it generates rather than through its owner's assertion. The [access control procedure](../../security/procedure-access-control.md) owns the access review in its section 3, including the review criteria and the handling of access that fails them. The [identity and access management policy](../../security/policy-identity-and-access-management.md) requires identity and access events to be logged and monitored in its section 4.7 (monitoring and logging). The [logging and monitoring standard](../../security/standard-logging-and-monitoring.md) establishes the operating-evidence route: log generation and coverage in its section 4.1, centralized log collection in its section 4.3, retention and protection in its section 4.4, and log review and use in its section 4.8. Event classes, log fields, retention periods, and review cadences live in those sections.

**Why it matters.** Control-generated records are evidence that the control operates. A record can also document a failure; its contents, not its existence, are what the reader assesses.

**Signals of progress.** For a sampled privileged identity, an access decision record, an access-review record, and a privileged-event log extract exist and are retrievable.

### Stage 4: revocation, certification, and termination remain traceable

**What changes.** The reader can see that changes to privileged access follow named corpus routes. The [access control procedure](../../security/procedure-access-control.md) owns access revocation in its section 5; the revocation triggers and their timelines live in that section. The [identity management procedure](../../security/procedure-identity-management.md) owns access certification in its section 5 and identity termination in its section 6; the certification frequencies, the handling of uncertified access, and the termination steps live there. Where a privileged account is suspected compromised, the [privileged access management standard](../../security/standard-privileged-access-management.md)'s section 6 owns the incident route.

**Why it matters.** Traceable revocation, certification, and termination routes are a prevention against privileged access outliving its justification.

**Signals of progress.** For a sampled change (a role change, a departure, or an uncertified access), a revocation or certification record exists and matches the route the linked procedure names.

### Stage 5: assurance becomes independent

**What changes.** The control's design and operation can be evaluated by a tester separate from its owner. The [control testing procedure](../../compliance/procedure-control-testing.md) owns that route end to end: control testing planning in its section 1, the testing methodology in its section 2 (which separates design effectiveness from operating effectiveness), evidence collection in its section 3, testing results and findings in its section 4, and remediation and re-testing in its section 6. Testing methods, sampling approaches, result classes, and response timelines live in those sections. The [identity and access management policy](../../security/policy-identity-and-access-management.md)'s section 4.8 (compliance and audit) ties the policy itself to periodic audit and control assessment.

**Why it matters.** Independent testing is a contribution to the assurance leadership receives: its recorded conclusion is reached apart from the function that runs the control, on the basis of the operating records.

**Signals of progress.** A control-test workpaper, a recorded result, and, where a finding was remediated, a re-test record exist for the control.

### Stage 6: leadership receives the assurance view

**What changes.** Where the control is a critical control or sits in a risk area the assurance map covers, the tested control becomes visible to the governing body through two linked instruments. The [assurance map register](../../risk/register-assurance-map.md) records who provides assurance over each risk area: its Section 1 defines the lines-of-defence model, its Section 2 defines the register's entry structure, and its Section 4 owns the activity-type taxonomy. Its Section 6 sets the map's governance, including the reporting route for material gaps; its Section 7 connects the map to the forward assurance plan; and its Section 8 owns gap management. The [board risk report template](../../risk/template-board-risk-report.md) carries the reporting slot itself: its Section 11 (assurance) defines what the board-level report presents on audit coverage, findings, and independent assurance. The entry fields, taxonomies, rating scale, and gap steps live in the register; the report's row set lives in the template.

**Why it matters.** The assurance-map entry and the report's assurance section are evidence that the control's coverage, and any material gap in it, reached the governing body rather than stopping at the function that operates the control.

**Signals of progress.** An assurance-map entry exists for the relevant access risk area, and the assurance section of the board-level risk report reflects it.

## Destination state

The privileged-access control can now be traced end to end: the requirement in the [identity and access management policy](../../security/policy-identity-and-access-management.md), the implementation in the [privileged access management standard](../../security/standard-privileged-access-management.md), the [access control procedure](../../security/procedure-access-control.md), and the [identity management procedure](../../security/procedure-identity-management.md), the operating records routed through the [logging and monitoring standard](../../security/standard-logging-and-monitoring.md), the independent conclusion under the [control testing procedure](../../compliance/procedure-control-testing.md), and the leadership view in the [assurance map register](../../risk/register-assurance-map.md) and the [board risk report template](../../risk/template-board-risk-report.md). That traceability is what this journey assembles for the reader, and it is all it assembles: each leg of the lineage is owned by the linked document, and the lineage as a whole establishes navigation rather than effectiveness. Whether the control operates in any given organization is answered by the records and test results themselves, which the evidence classes below let the reader request.

## Evidence to request

Each item below is an evidence class the governing body can call for from management, named by type only. Each item is evidence for the named control or outcome, judged against the requirements in the linked corpus document.

- **The policy-to-control mapping**, as evidence that the privileged-access requirements in the [identity and access management policy](../../security/policy-identity-and-access-management.md) (its sections 4.4 and 4.5) have a named implementing control.
- **The approved access-control design**, as evidence for the implementing control's design under the [privileged access management standard](../../security/standard-privileged-access-management.md) (its section 4) and the [access control procedure](../../security/procedure-access-control.md) (its section 6).
- **A privileged-access decision record for a sampled request**, as evidence that the request and approval control in the [access control procedure](../../security/procedure-access-control.md) (its section 1) operated.
- **An access-review record for a sampled period**, as evidence that the review control in the [access control procedure](../../security/procedure-access-control.md) (its section 3) operated.
- **A privileged-event log extract**, as evidence for the log generation and coverage control in the [logging and monitoring standard](../../security/standard-logging-and-monitoring.md) (its section 4.1) and the identity-and-access-event logging requirement in the [identity and access management policy](../../security/policy-identity-and-access-management.md) (its section 4.7).
- **A log-review record**, as evidence that the log review control in the [logging and monitoring standard](../../security/standard-logging-and-monitoring.md) (its section 4.8) operated.
- **The record matching a sampled change**, as evidence that the applicable route operated: access revocation in the [access control procedure](../../security/procedure-access-control.md) (its section 5), or access certification or identity termination in the [identity management procedure](../../security/procedure-identity-management.md) (its sections 5 and 6).
- **A control-test workpaper with its recorded result**, as evidence that independent testing under the [control testing procedure](../../compliance/procedure-control-testing.md) examined the control's design or operation, according to the recorded test type.
- **A re-test record for a remediated finding**, as evidence that the remediation and re-testing route in the [control testing procedure](../../compliance/procedure-control-testing.md) (its section 6) operated.
- **The assurance-map entry for the access risk area**, as evidence that the control's assurance coverage and any gap are recorded and governed per the [assurance map register](../../risk/register-assurance-map.md).
- **The assurance section of the most recent board-level risk report**, as evidence that the assurance view reached the governing body per the [board risk report template](../../risk/template-board-risk-report.md) (its Section 11).

## Limitations

- This page creates no compliance and establishes no requirement. The linked corpus documents govern, and the adopting organization must validate applicability to its own structure, systems, and obligations.
- The six-stage order is a reader navigation order assembled across multiple corpus documents. It is composite content: no corpus document states this sequence, it is not a control lifecycle, it is not an operating procedure, and it adds no step to any corpus route. Composite content requires the adopting organization's own validation.
- Specific values are deliberately absent. Certification periods, review frequencies, activation and revocation timelines, approval routes, control tables, lifecycle contents, log fields and retention periods, testing methods and sampling approaches, result classes and response timelines, assurance ratings, and gap-management steps live only in the linked corpus documents, and the reader must take them from there.
- The corpus documents name specific roles, teams, and tools. This page refers to them generically, and the adopting organization maps them to its own governance model through the linked documents.
- Implementation is not effectiveness, and reading this journey confers understanding only. A stage described here is not evidence that the corresponding control operates in any organization; the evidence classes above are how the reader tests that, and a record or test result can document a failure as well as a pass.
- This page makes no likelihood, frequency, or statistical claim about privileged-access failures or their outcomes.

**End of Document**
