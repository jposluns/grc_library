# Library Quality and Review Cadence Procedure

**Document Title:** Library Quality and Review Cadence Procedure\
**Document Type:** Procedure\
**Version:** 1.0.7\
**Date:** 2026-06-20\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/charter-governance-library.md`](charter-governance-library.md), [`governance/framework-continuous-assurance-and-improvement.md`](framework-continuous-assurance-and-improvement.md), [`governance/framework-document-architecture-and-interrelationship.md`](framework-document-architecture-and-interrelationship.md), [`governance/procedure-continuous-improvement-register.md`](procedure-continuous-improvement-register.md), [`governance/procedure-grc-programme-management-and-annual-review.md`](procedure-grc-programme-management-and-annual-review.md), [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md), [`governance/register-document-review-schedule.md`](register-document-review-schedule.md), [`governance/template-document-review-record.md`](template-document-review-record.md), [`specification-master-project.md`](../specification-master-project.md), [`specification-ingestion.md`](../specification-ingestion.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material change to library structure, tooling, or maintenance practice\
**Repository Path:** [`governance/procedure-library-quality-and-review-cadence.md`](procedure-library-quality-and-review-cadence.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure governs the continuous quality and review of artefacts in this CC BY-SA 4.0 governance library. It complements the continuous assurance and improvement framework (which is library-wide) by setting concrete cadence, drift-detection, refresh, and retirement practice for individual documents.

The objective is that the library remains useful, current, and internally coherent without any single maintenance event becoming heroic.

---

## Scope

This procedure applies to:

1. Every active document in the library across all domains.
2. Auto-generated artefacts (taxonomy, portal, maturity scorecard).
3. Tooling under `tools/` that supports library quality.
4. Cross-cutting artefacts at the repository root (README, NOTICE, SECURITY, CONTRIBUTING, the two specifications, the changelog).

It does not govern external consumers' own forks; it governs the canonical repository.

---

## Procedure

### Step 1: Establish the review schedule

| Activity | Description |
| --- | --- |
| Source of truth | The review schedule register lists each document, its owner, its review frequency, its last review date, and its next review due date |
| Population | Schedule entries derived from each document's metadata block (Date and Review Frequency fields) |
| Refresh | The schedule is refreshed when documents are added, retired, or rewritten |
| Visibility | The schedule is published in the repository and surfaced via tooling |

### Step 2: Detect overdue reviews

| Activity | Description |
| --- | --- |
| Detector | The review-cadence checker ([`tools/check-review-cadence.py`](../tools/check-review-cadence.py)) compares each document's Date and Review Frequency against the current date |
| Cadence | The checker runs as part of CI; it also runs on demand by maintainers |
| Findings | Overdue documents are listed with the lag (days past due) and the responsible owner role |
| Threshold for action | Documents more than a defined lag past due are escalated |

### Step 3: Conduct a document review

For each document under review, the responsible owner role conducts the following:

| Activity | Description |
| --- | --- |
| Re-read | The owner re-reads the document for currency, accuracy, and continued utility |
| Framework alignment check | The framework references are verified against current public versions |
| Cross-reference check | The Related Documents list is checked; broken or outdated cross-references are corrected |
| Sanitisation check | The document is rechecked against the sanitisation rules; any residue is removed |
| Language and style check | The document is checked against the language rules (Oxford `-ize`, no em or en dashes, "ensure that", sentence-case headings) |
| Disposition | The owner records one of: No change, Minor revision, Material revision, Supersede, Retire |
| Date and version | Where the document is changed, Date and Version are updated per the ingestion specification |
| Review record | The review is recorded per the document review record template |

### Step 4: Apply the disposition

| Disposition | Action |
| --- | --- |
| No change | Date stays the same; review record states the document remains current; the next review due date is calculated from the original Date |
| Minor revision | Patch version increment (0.0.x); document content updated; commit references the review |
| Material revision | Minor version increment (0.x.0) where consistent with the library version-bump rules; document content updated; commit references the review |
| Supersede | A successor document is produced; the predecessor's status changes per the lifecycle in the document architecture framework |
| Retire | The document is removed from the active set per the retirement procedure; archived per the records retention schedule |

### Step 5: Maintain auto-generated artefacts

| Artefact | Action |
| --- | --- |
| [`taxonomy.yml`](../taxonomy.yml) | Regenerated by [`tools/build-taxonomy.py`](../tools/build-taxonomy.py) whenever metadata changes |
| [`docs/portal.md`](../docs/portal.md) | Regenerated by [`tools/build-portal.py`](../tools/build-portal.py) whenever metadata changes |
| [`docs/maturity-scorecard.md`](../docs/maturity-scorecard.md) | Regenerated by [`tools/build-portal.py`](../tools/build-portal.py) whenever metadata changes |
| [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md) | Manually maintained; cross-checked against the directory listings on every release |
| [`governance/register-document-review-schedule.md`](register-document-review-schedule.md) | Regenerated or hand-maintained per the review schedule rebuild approach in force |
| Domain READMEs | Updated whenever a document is added, retired, or renamed in the domain |

### Step 6: Run the standing audits

| Audit | Tool | Pass criterion |
| --- | --- | --- |
| Metadata | [`tools/lint-metadata.py`](../tools/lint-metadata.py) | No findings |
| Language | [`tools/lint-language.py`](../tools/lint-language.py) | No findings |
| Links | [`tools/lint-links.py`](../tools/lint-links.py) | No broken links |
| Structure | [`tools/lint-structure.py`](../tools/lint-structure.py) | No findings |
| Review cadence | [`tools/check-review-cadence.py`](../tools/check-review-cadence.py) | Overdue documents below the action threshold |
| Taxonomy in sync | `tools/build-taxonomy.py --check` | In sync |
| Portal and scorecard in sync | `tools/build-portal.py --check` | In sync |

The full 40-gate audit programme (see [`governance/specification-audit-programme.md`](specification-audit-programme.md) §6 for the canonical gate inventory) runs in CI and pre-commit; any failure blocks merge unless an explicit exception is recorded.

### Step 7: Periodic library-level review

| Activity | Cadence |
| --- | --- |
| Library health report | Quarterly: a short summary of overdue reviews, audit-finding trends, content additions and retirements, drift hot-spots, and tooling status |
| Sanitisation sweep | Quarterly: a sanitisation spot-check across documents touched in the period |
| Framework reference refresh | Semi-annual: a spot-check that framework references are current against publishing bodies |
| Tooling review | Annual: tooling is reviewed for currency, accuracy, and coverage |
| Maintenance practice review | Annual: this procedure is reviewed; lessons from the period feed into changes |
| Specifications review | Annual: the master and ingestion specifications are reviewed |

### Step 8: Drift and emerging issues

| Source of drift | Treatment |
| --- | --- |
| Audit findings | Treated as defects; tracked to closure |
| Reader feedback | Captured in the continuous improvement register |
| Framework changes | Triggered framework-reference updates per the affected document set |
| Regulatory changes | Triggered review of documents whose alignment depends on the regulation |
| New domain coverage gap | Considered for a future content phase |
| Tooling gap | Considered for a future tooling phase |
| Cross-document drift | Treated as a structural issue rather than a single-document issue |

---

## Roles

| Role | Responsibility |
| --- | --- |
| Governance Library Maintainer | Owns this procedure; coordinates library quality |
| Domain owners | Conduct reviews for their domain's documents per the listed cadence |
| Document owner roles | Identified in each document's metadata block; accountable for that document's review |
| Tooling maintainer | Keeps the audit tooling functional and accurate |
| Contributors | Bring issues, suggestions, and corrections via the continuous improvement register |

The Governance Library Maintainer is not the sole reviewer; the role coordinates and prompts the reviewers identified per document.

---

## Cadence summary

| Activity | Cadence |
| --- | --- |
| Per-document review | Per the document's stated Review Frequency |
| Audit suite execution | Continuous (CI and pre-commit) |
| Quarterly library health report | Quarterly |
| Quarterly sanitisation spot-check | Quarterly |
| Framework reference spot-check | Semi-annual |
| Tooling review | Annual |
| Specifications review | Annual |
| Maintenance practice review | Annual |

---

## Quality expectations

| Quality | Indicator |
| --- | --- |
| Currency | Overdue review backlog kept below the action threshold |
| Coherence | Cross-document references remain valid; cross-framework alignment matrices remain accurate |
| Accuracy | Framework references are accurate against current versions |
| Discoverability | Each domain README and the governance index remain accurate |
| Sanitisation | No real organisation identifiers; the library remains organisation-neutral |
| Language quality | The audit suite remains clean |
| Auto-generated artefacts | In sync with metadata at all times |
| Reader feedback | Captured, considered, and closed out |

---

## Operating expectations

1. Every active document has a named owner role and a stated review frequency.
2. Audit failures are not stockpiled; they are treated as defects on the date they appear.
3. Periodic review is conducted by the document owner role; the Governance Library Maintainer coordinates, prompts, and tracks.
4. Quarterly library health is reported; sustained quality issues escalate to the library maintainer.
5. Document retirement is a deliberate decision recorded in the changelog and the document architecture framework.

---

## Framework alignment

| Framework | Reference | Relevance |
| --- | --- | --- |
| ISO/IEC 27001:2022 | A.5.36 Compliance with policies; A.5.37 Documented operating procedures | Information security cross-walk |
| ISO 9001:2015 | §7.5 Documented information; §9 Performance evaluation | Quality management |
| COBIT 2019 | APO01 Manage the I&T management framework | Governance of enterprise IT |
| ITIL 4 | Continual improvement practice | Service management |
| ISO/IEC 42001:2023 | §9 Performance evaluation; §10 Improvement | AI management system cross-walk |
| NIST CSF 2.0 | Govern function | Risk integration |

---

## Limitations

This procedure is a CC BY-SA 4.0 baseline. The specific cadences, thresholds, and tooling are organisation-specific. The procedure expresses the maintenance outcomes and a workable cadence; adopting organisations select the depth that matches their library size and the maturity of their maintenance practice.

---

**End of Document**
