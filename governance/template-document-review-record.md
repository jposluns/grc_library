# Document Review Record Template

**Document Title:** Document Review Record Template\
**Document Type:** Template\
**Version:** 1.0.1\
**Date:** 2026-06-02\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/procedure-library-quality-and-review-cadence.md`](procedure-library-quality-and-review-cadence.md), [`governance/register-document-review-schedule.md`](register-document-review-schedule.md), [`governance/framework-continuous-assurance-and-improvement.md`](framework-continuous-assurance-and-improvement.md), [`governance/procedure-continuous-improvement-register.md`](procedure-continuous-improvement-register.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material change to the review procedure or schedule schema\
**Repository Path:** [`governance/template-document-review-record.md`](template-document-review-record.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This template structures the record produced when a single document is reviewed under the library quality and review cadence procedure. The record captures who reviewed, what was assessed, what was found, the disposition, the actions, and the sign-off.

A document review record is intentionally short. Long reviews are an anti-pattern; the review is to confirm continued fitness, not to rewrite the document inside the review.

---

## Scope

This template applies to:

1. Periodic reviews triggered by the document's stated review frequency.
2. Event-triggered reviews (material change, framework change, regulatory change).
3. Reviews triggered by audit findings or reader feedback.
4. Reviews conducted at retirement decisions.

It does not replace the substantive editing of a document; substantive change runs through the ordinary contribution flow and produces a new version.

---

## Template structure

### Section A: identification

| Field | Description |
| --- | --- |
| Document path | Repository-relative path to the document under review |
| Document title | Title from the metadata block |
| Document version at review | The Version field as it stood at the start of the review |
| Document date at review | The Date field as it stood at the start of the review |
| Review type | Periodic, event-triggered, audit-finding-triggered, feedback-triggered, retirement |
| Review trigger | The specific trigger if event-, finding-, or feedback-triggered |
| Reviewer role | The owner role conducting the review |
| Reviewer | Named individual or "role" if attribution is to the role only |
| Review date | The date the review was completed |
| Linked schedule entry | Pointer to the document review schedule entry |

### Section B: assessment

The reviewer confirms each of the following or records a finding.

| Assessment area | Confirmed or finding |
| --- | --- |
| Currency | The document remains current against the technology, threat, framework, and regulatory environment |
| Accuracy | The technical and substantive content is correct |
| Framework references | The framework references are accurate against current publishing-body materials |
| Cross-references | The Related Documents links resolve and remain meaningful |
| Sanitisation | No real organisation identifiers, real personnel names, internal system names, IP addresses, customer names, vendor names, or other sanitisation residue |
| Language and style | Oxford English `-ize` endings; no em or en dashes; "ensure that" rather than bare "ensure"; sentence case for H2-H6 headings |
| Metadata correctness | All 13 metadata fields present and accurate |
| Auto-generated artefact alignment | Taxonomy, portal, scorecard, and index alignment confirmed |
| Coherence with adjacent documents | No contradiction with related documents in adjacent domains |
| Reader feedback | Any open feedback on this document considered |
| Audit findings | Any open audit findings on this document considered |
| Compliance considerations | Regulatory or sector compliance touch-points remain accurate |

### Section C: findings

| Field | Description |
| --- | --- |
| Finding identifier | Sequential identifier within the review |
| Finding description | What is wrong or out-of-date |
| Severity | Cosmetic, minor, material, blocking |
| Linked section | Section, table, or paragraph within the document |
| Proposed treatment | Edit, link fix, reference update, retire, supersede, no action |
| Owner | Who will action the finding |
| Target date | When the finding will be addressed |

Where no findings arise, the section states "No findings".

### Section D: disposition

| Disposition | Meaning | Effect on document |
| --- | --- | --- |
| No change | The document remains current as-is | Date and Version unchanged; review recorded |
| Minor revision | Small corrections (typos, broken links, framework version refresh, language fixes) | Patch version increment; Date updated; commit references the review |
| Material revision | Content changes that materially alter the document's substance | Minor version increment where consistent with the library version-bump rules; Date updated; commit references the review |
| Supersede | The document is replaced by a successor | The successor is produced; the predecessor's status updates per the document architecture framework |
| Retire | The document is no longer relevant | The document is removed from the active set; archived per the records retention schedule |

The disposition is a single choice; rationale is recorded.

### Section E: actions

| Action | Description |
| --- | --- |
| Identifier | Sequential identifier within the review |
| Description | What will be done |
| Owner | Who will do it |
| Target date | When it will be done |
| Status | Open, in progress, complete |
| Closure note | When complete, a brief note recording the outcome |

Actions that exceed a defined ageing threshold escalate per the library quality and review cadence procedure.

### Section F: sign-off

| Field | Description |
| --- | --- |
| Reviewer sign-off | Reviewer confirms the review was conducted to the assessment items in Section B |
| Date of sign-off | The date the review record was signed off |
| Approver (where required) | For material revisions and retirements, the approver role per the metadata block |
| Approver date | The date the approver signed |
| Linked commit | The repository commit that closes the review (where applicable) |

---

## Style and length expectations

| Expectation | Description |
| --- | --- |
| Length | A single review record fits comfortably on one page; sustained long records indicate the review is doing the wrong job |
| Specificity | Findings cite the document section or paragraph |
| Honest | Where the document is found to be out-of-date, the record says so; cosmetic acceptance is not a review |
| Traceability | Linked to the schedule entry and to any commits the review produces |
| Archive-friendly | The record is durable; future readers can understand what was reviewed and why |

---

## Worked example (illustrative; not a real review)

| Field | Example value |
| --- | --- |
| Document path | [`security/standard-logging-and-monitoring.md`](../security/standard-logging-and-monitoring.md) |
| Document version at review | 1.2.3 |
| Document date at review | 2025-09-12 |
| Review type | Periodic |
| Reviewer role | Chief Information Security Officer |
| Review date | 2026-09-12 |
| Currency | Confirmed |
| Accuracy | Confirmed |
| Framework references | Finding: NIST SP 800-92 referenced; minor refresh required to align with the current revision number |
| Cross-references | Confirmed |
| Sanitisation | Confirmed |
| Language and style | Confirmed |
| Metadata correctness | Confirmed |
| Auto-generated artefact alignment | Confirmed |
| Coherence with adjacent documents | Confirmed |
| Reader feedback | None open |
| Audit findings | None open |
| Compliance considerations | Confirmed |
| Disposition | Minor revision |
| Actions | F-01: refresh the NIST SP 800-92 reference; owner: CISO; target date: 2026-09-26 |
| Reviewer sign-off | CISO; 2026-09-12 |
| Linked commit | (Recorded when the action closes) |

---

## Operating expectations

1. A review record is produced for every periodic review and for every event-triggered review.
2. Records are kept in the library or in a linked repository; they survive personnel turnover.
3. Records are concise; long-form revisions are not done inside the review record.
4. Findings have a named owner and a target date; aged-out findings escalate.
5. Records reconcile to the document review schedule and the document's metadata.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO 9001:2015 | §7.5 Documented information; §9.3 Management review | Quality management |
| ISO/IEC 27001:2022 | A.5.36 Compliance with policies; A.5.37 Documented operating procedures; A.5.35 Independent review of information security | Information security cross-walk |
| ISO 19011:2018 | Guidelines for auditing management systems | Audit and review baseline |
| ISO 30301 | Management systems for records | Records discipline |
| ISO/IEC 42001:2023 | §9.3 Management review | AI management system cross-walk |
| COBIT 2019 | MEA02 Managed assurance | Governance of enterprise IT |
| ITIL 4 | Continual improvement | Service management |

---

## Limitations

This template is a CC BY-SA 4.0 baseline. The specific layout, tooling, and storage location for review records are organisation-specific. The template expresses the minimum content and the cadence integration; adopting organisations adapt the surface form to their tooling.

---

**End of Document**
