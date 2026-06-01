# Library Health Report Template

**Document Title:** Library Health Report Template\
**Document Type:** Template\
**Version:** 0.0.1\
**Date:** 2026-05-28\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/procedure-library-quality-and-review-cadence.md`](procedure-library-quality-and-review-cadence.md), [`governance/register-document-review-schedule.md`](register-document-review-schedule.md), [`governance/template-document-review-record.md`](template-document-review-record.md), [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material change to the library quality and review cadence procedure\
**Repository Path:** [`governance/template-library-health-report.md`](template-library-health-report.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template structures the quarterly library health report referenced by the library quality and review cadence procedure. The report aggregates the state of the library's documents, derived artefacts, tooling, and review cadence; surfaces drift; and proposes corrective actions.

The objective is that the library's maintainer (and, where applicable, contributors and adopting organisations) can see, in a single short document each quarter, whether the library remains healthy and where attention is needed.

---

## Scope

This template applies to:

1. The quarterly library health report itself (the deliverable described in [`governance/procedure-library-quality-and-review-cadence.md`](procedure-library-quality-and-review-cadence.md) Section 7).
2. Ad-hoc health reports produced in response to a material event.
3. The annual health-summary report combining the four quarterly reports.

It does not apply to per-document review records (which use the document review record template) or to operational reporting (which is per the operations domain).

---

## Template structure

### Section A: identification

| Field | Description |
| --- | --- |
| Report period | The window the report covers (e.g. 2026-Q1, 2026-Q2) |
| Report date | When the report was finalized |
| Prepared by | The Governance Library Maintainer or designated reviewer |
| Audience | Library maintainer, contributors, and any subscribed adopting organisations |
| Version | Report version |
| Linked source data | Pointers to the underlying audit outputs and registers |

### Section B: executive summary

One paragraph (3-5 sentences) stating:

- The overall library posture (improving, stable, deteriorating, requiring attention)
- The most material change since the last report
- The most material risk to address before the next report
- Any decision the audience is invited to make

### Section C: audit suite status

Aggregated output of the 32 automated audits (see [`governance/specification-audit-programme.md`](specification-audit-programme.md) §6 for the canonical gate inventory):

| Audit | Status | Findings count | Notes |
| --- | --- | --- | --- |
| [`lint-metadata.py`](../tools/lint-metadata.py) | Pass / Fail | 0 / N | Brief note on findings if any |
| [`lint-language.py`](../tools/lint-language.py) | Pass / Fail | 0 / N | |
| [`lint-links.py`](../tools/lint-links.py) | Pass / Fail | 0 / N | |
| [`lint-structure.py`](../tools/lint-structure.py) | Pass / Fail | 0 / N | |
| [`lint-citations.py`](../tools/lint-citations.py) | Pass / Fail | 0 / N | |
| [`lint-roles.py`](../tools/lint-roles.py) | Pass / Fail | 0 / N | |
| [`lint-shall-near-uncertainty.py`](../tools/lint-shall-near-uncertainty.py) | Pass / Fail | 0 / N | |
| [`check-review-cadence.py`](../tools/check-review-cadence.py) | Pass / Action / Fail | Current / Due-soon / Overdue / Action-threshold | Summary of overdue documents |
| `build-taxonomy.py --check` | In sync / Out of sync | n/a | |
| `build-portal.py --check` | In sync / Out of sync | n/a | |

For each non-pass: brief description, file(s) affected, remediation plan, target date.

### Section D: content additions and retirements

| Activity | Count | Examples |
| --- | --- | --- |
| Documents added in the period | N | List of new documents |
| Documents materially revised (minor or major version bump) | N | List with rationale |
| Documents patched (patch version increment) | N | List with rationale |
| Documents deprecated | N | List with rationale |
| Documents retired | N | List with rationale |
| Tooling additions or changes | N | List with rationale |

### Section E: review cadence state

Aggregated from [`check-review-cadence.py`](../tools/check-review-cadence.py):

| Status | Count | Notes |
| --- | --- | --- |
| Current | N | |
| Due-soon (within 30 days) | N | List the documents |
| Overdue (past due, within action threshold) | N | List with lag |
| Past action threshold | N | List with escalation status |
| Event-driven (no periodic cadence) | N | |

Per-owner-role breakdown for documents in due-soon / overdue / action-threshold.

### Section F: drift hot-spots

For each drift indicator, describe the observed pattern, the affected documents, and the corrective action plan:

| Indicator | Description |
| --- | --- |
| Framework citation drift | New framework references that should be verified against primary sources |
| Cross-document inconsistency | Pairs of documents that say different things about the same control |
| Owner-role overload | Roles assigned an excessive number of responsibilities |
| Forum proliferation | New named forums introduced without consolidation guidance |
| Sanitisation residue | Real organisation identifiers, regional scoping, internal hostnames |
| Phantom dependencies | References to documents or frameworks that don't exist |

### Section G: incidents and lessons

| Field | Description |
| --- | --- |
| Material defects detected | Defects that materially affected library usefulness or accuracy |
| Source of detection | How each was found (audit, contributor, reader feedback, external review) |
| Time to detection | Period between defect introduction and detection |
| Time to remediation | Period between detection and full remediation |
| Lessons learned | Pattern that should be addressed in the audit suite or maintenance practice |
| Linked corrective phases | References to CHANGELOG phases addressing each item |

### Section H: contributor activity

| Indicator | Count or note |
| --- | --- |
| Contributions in the period | Number of pull requests merged |
| New contributors | Number of first-time contributors |
| Feedback received | Number of content-feedback items received (via the channels in CONTRIBUTING.md) |
| Feedback addressed | Number of feedback items closed; outstanding count |

### Section I: adopter signal

Where signals are available:

| Indicator | Note |
| --- | --- |
| Known adopters | Number of organisations known to be using the library (where the organisation has self-identified) |
| Reported defects from adopters | Defects raised by adopting organisations |
| Sector-annex usage | Which sector annexes are most frequently downloaded or referenced |
| Common adapter modifications | Patterns observed in fork-and-adapt usage where visible |

### Section J: next-period plan

| Activity | Target |
| --- | --- |
| Open audit findings to resolve | List |
| Overdue reviews to complete | List with target dates |
| Planned phases or significant content additions | List |
| Tooling improvements | List |
| Framework reference refreshes | Per the semi-annual cadence |
| Sanitisation sweep | Per the quarterly cadence |

### Section K: sign-off

| Field | Description |
| --- | --- |
| Maintainer sign-off | Governance Library Maintainer confirms the report reflects the library state |
| Sign-off date | The date the report was finalized |
| Linked commit | The repository commit at which the report was prepared |

---

## Worked example fragment (illustrative)

| Period | Posture | Material change | Material risk |
| --- | --- | --- | --- |
| 2026-Q3 (illustrative) | Stable | Phase 12 corrective campaign closed all critical and high findings from the comprehensive audit. | Continued attention to citation accuracy as the AI domain frameworks evolve. |

A full report would include the per-audit table, per-document review status, per-finding incident summary, and the next-period plan.

---

## Cadence

| Report | Cadence | Deliverable date |
| --- | --- | --- |
| Quarterly health report | Quarterly | Within the first month of the following quarter |
| Annual health summary | Annual | Within the first month of the following year, combining the four quarterly reports |
| Ad-hoc health report | As required | Within the timeline the triggering event warrants |

---

## Operating expectations

1. The report is produced from the audit-suite output, the document review schedule, the CHANGELOG, and the continuous improvement register; it does not require fresh investigation each quarter.
2. The report is concise; long-form analysis lives in linked source artefacts.
3. Each report is committed to the repository under a stable path (for example `docs/health-reports/`) and is part of the library's history.
4. The first quarterly report establishes the baseline; subsequent reports compare against it.
5. Material findings escalate per the library quality and review cadence procedure.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO 9001:2015 | §9 Performance evaluation | Quality management |
| ISO/IEC 27001:2022 | §9.3 Management review | Information security management review |
| ISO/IEC 42001:2023 | §9.3 Management review | AI management system review |
| COBIT 2019 | MEA01 Monitor, Evaluate and Assess Performance and Conformance | Governance of enterprise IT |
| ITIL 4 | Continual improvement | Service management |

---

## Limitations

This template is a CC BY-SA 4.0 baseline. The specific report contents, the audience, the publication mechanism, and the integration with adjacent reports are organisation-specific. The library itself uses this template to produce its own quarterly health reports.

---

**End of Document**
