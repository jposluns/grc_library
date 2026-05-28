# Document Review Schedule Register

**Document Title:** Document Review Schedule Register 
**Document Type:** Register 
**Version:** 0.0.1 
**Date:** 2026-05-28 
**Owner:** Governance Library Maintainer 
**Approving Authority:** Governance Library Maintainer 
**Related Documents:** [`governance/procedure-library-quality-and-review-cadence.md`](procedure-library-quality-and-review-cadence.md), [`governance/template-document-review-record.md`](template-document-review-record.md), [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md), [`governance/framework-continuous-assurance-and-improvement.md`](framework-continuous-assurance-and-improvement.md), [`governance/procedure-continuous-improvement-register.md`](procedure-continuous-improvement-register.md) 
**Classification:** Public 
**Category:** Core Governance 
**Review Frequency:** Continuous; refreshed in line with document additions, retirements, and conducted reviews 
**Repository Path:** [`governance/register-document-review-schedule.md`](register-document-review-schedule.md) 
**Confidentiality:** Public 
**License:** CC0 1.0 Universal 

---

## Purpose

This register defines how the per-document review schedule is maintained for this library. The schedule itself is held as structured data; this register describes the schema, the maintenance rules, the operating cadence, and the connection to the review-cadence checker and the document review record template.

The objective is that no active document drifts past its review-frequency without a deliberate decision.

---

## Scope

This register applies to:

1. All active documents listed in the document index and classification register.
2. Auto-generated artefacts whose review cadence is tied to their source data.
3. Cross-cutting artefacts (top-level README, NOTICE, SECURITY, CONTRIBUTING, the two specifications, the changelog).

It does not cover documents retired from active service; those follow the records retention schedule.

---

## Schema

Each schedule entry has:

| Field | Description |
| --- | --- |
| Document path | Repository-relative path to the document |
| Document title | Title from the document's metadata block |
| Document type | Type from the document's metadata block |
| Domain | Owning domain |
| Owner role | Owner role from the document's metadata block |
| Last review date | The Date field from the document's metadata block, treated as the most recent material review |
| Review frequency | The Review Frequency field from the document's metadata block, normalised to a number of months |
| Next review due | Computed from last review date plus review frequency |
| Status | Current, due-soon, overdue, blocked, retired |
| Lag | For overdue entries, the number of days past the due date |
| Linked review records | Pointers to the document review records produced for this document |

The schedule is derived from the documents themselves; the documents are the source of truth, the schedule is a view.

---

## Review frequency normalisation

The Review Frequency field in document metadata is expressed in human-readable language. For scheduling, the values are normalised as follows.

| Stated frequency | Normalised months | Comment |
| --- | --- | --- |
| Quarterly | 3 | |
| 6 to 12 months | 12 | Lower-end window used for action threshold |
| Annual | 12 | |
| Biennial | 24 | |
| Continuous | Continuous | Audit-driven; not date-driven |
| Continuous / Quarterly | 3 | |
| Continuous / Monthly | 1 | |
| Upon material change to ... | Event-driven | Combined with the time-based cadence stated |
| Per release | Event-driven | Tied to the release calendar |

Documents that state both a periodic cadence ("Annual") and an event trigger ("and upon material change to ...") use the periodic cadence for the schedule and treat the event trigger as a separate signal.

---

## Status values

| Status | Definition |
| --- | --- |
| Current | The document is within its review-frequency window |
| Due-soon | The document is within a defined warning window before the due date |
| Overdue | The document is past its due date |
| Action-threshold | The document is past its due date by more than the action threshold; escalation triggered |
| Blocked | The document is overdue with a documented blocker recorded against it |
| Retired | The document is no longer active; schedule entry preserved for history |

The warning window and the action threshold are set by the maintenance practice. Initial defaults: warning window = 30 days, action threshold = 90 days.

---

## Maintenance rules

| Trigger | Action |
| --- | --- |
| New document added | A schedule entry is created from the metadata |
| Document retired | The entry is marked Retired; preserved for history |
| Document Date or Review Frequency changed | The entry is recomputed |
| Review conducted | The Date in the document is updated; the schedule recomputes |
| Document renamed | The path in the entry is updated |
| Domain ownership changed | The owner role in the entry is updated |
| Tooling update | The review-cadence checker is updated alongside |

Schedule entries are kept consistent with document metadata; any divergence is a finding.

---

## Operating cadence

| Activity | Cadence |
| --- | --- |
| Schedule recompute | On every CI run via the review-cadence checker |
| Owner-role prompt | Owner roles are notified by the maintainer when documents enter the due-soon or overdue state |
| Quarterly health report | Schedule status fed into the library health report |
| Annual schema review | Schema and normalisation table reviewed annually |

---

## Integration with tooling

| Tool | Role |
| --- | --- |
| `tools/check-review-cadence.py` | Parses metadata, computes status, and reports overdue and action-threshold entries |
| `tools/build-taxonomy.py` | Produces the taxonomy that feeds the schedule build |
| CI | Runs the cadence checker on every push |
| Pre-commit | Optional cadence check in pre-commit |

Where this register and the checker disagree, the checker output is treated as primary; the discrepancy is itself a finding.

---

## Reporting

| Report | Contents |
| --- | --- |
| Overdue list | Documents past their due date, sorted by lag |
| Due-soon list | Documents within the warning window |
| Action-threshold list | Documents past the action threshold |
| Blocked list | Documents with a documented blocker |
| Owner-role summary | Counts of overdue entries per owner role |
| Domain summary | Counts of overdue entries per domain |
| Schedule trend | Movement of the overdue count across reporting periods |

---

## Operating expectations

1. The review-cadence checker is run on every CI pass; failures are addressed promptly.
2. Document owners receive prompts when their documents enter the due-soon and overdue states.
3. Blocking conditions are recorded against documents; a document is not silently overdue.
4. Schedule entries reconcile to document metadata; reconciliation drift is a finding.
5. The schedule's schema and normalisation table are reviewed annually; the maintenance procedure approves any change.

---

## Worked example schedule fragment (illustrative)

| Path | Owner | Last review | Frequency | Next due | Status |
| --- | --- | --- | --- | --- | --- |
| `governance/charter-governance-library.md` | Governance Library Maintainer | 2026-05-27 | 12 months | 2027-05-27 | Current |
| `security/policy-information-security.md` | Chief Information Security Officer | 2026-05-27 | 12 months | 2027-05-27 | Current |
| `ai/framework-ai-governance-and-risk.md` | Chief AI Officer | 2026-05-27 | 12 months | 2027-05-27 | Current |
| `risk/template-operational-risk-register.md` | Chief Risk Officer | 2026-05-28 | 12 months | 2027-05-28 | Current |
| `architecture/standard-technology-radar.md` | Chief Technology Officer | 2026-05-28 | 3 months | 2026-08-28 | Current |

The fragment above is illustrative; the actual schedule is produced by tooling.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO 9001:2015 | §7.5.2 Creating and updating; §7.5.3 Control of documented information | Quality management |
| ISO/IEC 27001:2022 | A.5.36 Compliance with policies; A.5.37 Documented operating procedures | Information security cross-walk |
| COBIT 2019 | APO01 Manage the I&T management framework | Governance of enterprise IT |
| ITIL 4 | Continual improvement | Service management |
| ISO 30301 | Management systems for records | Records discipline |
| ISO/IEC 42001:2023 | §7.5 Documented information; §9 Performance evaluation | AI management system cross-walk |

---

## Limitations

This register is a public-domain baseline. The actual schedule values, the warning window, the action threshold, and the cadence checker's specific behaviour are organisation-specific. The register expresses the schema and the maintenance rules; the schedule itself is generated and refreshed continuously.

---

**End of Document**
