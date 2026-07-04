# Standard Version Upgrade Procedure

**Document Title:** Standard Version Upgrade Procedure\
**Document Type:** Procedure\
**Version:** 1.0.1\
**Date:** 2026-07-04\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/register-canonical-citations.md`](register-canonical-citations.md), [`governance/specification-citation-verification.md`](specification-citation-verification.md), [`governance/procedure-library-quality-and-review-cadence.md`](procedure-library-quality-and-review-cadence.md), [`governance/specification-audit-programme.md`](specification-audit-programme.md), [`specification-ingestion.md`](../specification-ingestion.md), [`README.md`](../README.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon any change to the citation-verification methodology or the standards-currency tooling\
**Repository Path:** [`governance/procedure-standard-version-upgrade.md`](procedure-standard-version-upgrade.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This procedure governs how the library transitions from one edition of an external standard it cites to a newer edition (for example, a published revision of an ISO/IEC standard, a new NIST Special Publication revision, or a new COBIT release). It exists because ad-hoc, one-location edits produce drift: a version bumped in the document a maintainer happened to be reading while the same citation stays stale elsewhere, or a plausible-but-nonexistent edition year introduced during a hurried update.

The objective is that a standard-version upgrade is a single, corpus-wide, evidence-grounded campaign: every cited location is found, each is classified and updated per its kind, the canonical-citations register records the supersession, and the standards-currency gate confirms the result. The procedure complements the per-document review cadence in [`procedure-library-quality-and-review-cadence.md`](procedure-library-quality-and-review-cadence.md) (which governs when a document is reviewed) by governing how a specific external-version change propagates across all documents at once.

---

## Scope

This procedure applies when an external standard, framework, or regulation that the library cites is republished in a new edition, revision, or version, and the library intends to adopt the new edition. It covers:

1. Standards and frameworks recorded in [`register-canonical-citations.md`](register-canonical-citations.md) (ISO/IEC, NIST, CSA, ISACA COBIT, OWASP, MITRE, and the other publishers on the §7 allow-list of [`specification-citation-verification.md`](specification-citation-verification.md)).
2. Legislation and regulation whose consolidated in-force version changes, where the corpus cites a dated version.

It does not govern:

- The decision of whether to adopt a new edition at all (a maintainer judgment informed by the change's materiality); this procedure begins once that decision is made.
- Correcting a citation that was wrong when written (a hallucinated or mis-transcribed reference); that is a defect fix under the normal review and audit flow, not a version upgrade.
- Internal per-document version fields (the library's own semantic versions), which follow the version-bump discipline, not this procedure.

---

## Procedure

### Step 1: Establish the authoritative diff

Obtain the publisher's own statement of what changed between the old and new edition. Where the publisher issues a transition or correspondence guide (ISO frequently does; NIST publishes revision summaries), that guide is the authoritative input for classifying each citation later. Record the new edition's identifier exactly as the publisher writes it (standard ID, edition, year), so that later steps compare against the publisher's form rather than a paraphrase.

Confirm the new edition against the publisher's canonical source per [`specification-citation-verification.md`](specification-citation-verification.md) §6: the upstream publisher page is the version authority. A locally held copy is believed-current storage, not the authority, so a load-bearing version is confirmed upstream before the campaign proceeds.

### Step 2: Sweep the corpus for every cited location

Find every location the old edition is cited. Use both:

- A repository-wide text search (`grep`) for the standard ID and the old edition year, across all domain directories, not only the domain where the standard is most obviously relevant.
- The [`register-canonical-citations.md`](register-canonical-citations.md) row for the standard, which records the canonical form and is the index of where the citation is authoritative.

The sweep is corpus-wide by construction: a standard cited in one domain is frequently cited in a framework-alignment table, a crosswalk, or a jurisdiction annex elsewhere. A search scoped to the input set (the documents a maintainer expected to touch) confirms only that those documents are clean, never that the corpus is clean.

### Step 3: Classify each citation

Classify each cited location as one of:

- **Positional-only**: the citation names the standard as a reference or alignment marker, and the edition year is incidental to the surrounding prose (for example, a framework-alignment table cell, a "see also" reference). A positional citation needs only its edition marker updated.
- **Substantive**: the surrounding prose relies on the specific content of the old edition (a requirement paraphrased, a clause number cited, a control mapped to a named section). A substantive citation may need the prose rewritten if the new edition changed the content the prose depends on.

Use the Step 1 transition guide to decide: a clause that was renumbered or a requirement that was reworded makes every citation of that clause substantive; an edition with no material change to the cited content leaves its citations positional.

### Step 4: Apply the updates per classification

- **Positional citations**: bump the edition marker (the year or revision) to the new edition. This is a mechanical edit; it does not by itself change the document's meaning.
- **Substantive citations**: rewrite the dependent prose to match the new edition's content, and bump the containing document's per-document `Version` and `Date` in the same commit, per the version-bump discipline (a body change co-bumps Version and Date).

Do not silently widen the edit beyond the citation and its dependent prose. If the new edition suggests a larger content revision, that is a separate reviewed change, surfaced rather than folded in.

### Step 5: Update the registers and mark the supersession

Update [`register-canonical-citations.md`](register-canonical-citations.md): set the row's current version, publication date, and the superseded-version note (the old edition, marked superseded with its effective date), and co-bump the register's own `Version` and `Date`. Record the verification of the new edition in the Citation Verifications Register (the project-governance register at `.project-governance/register-citation-verifications.md`, kept off the deliverable-corpus surface) per the methodology in [`specification-citation-verification.md`](specification-citation-verification.md): a new edition is a new verifiable claim and gets its own row, capturing the publisher page that attests the new edition. The register is append-only; a re-verification adds a row rather than overwriting the prior one, so the supersession trail is preserved.

### Step 6: Confirm the standards-currency gate

Run the standards-currency audit ([`tools/lint-standards-currency.py`](../tools/lint-standards-currency.py), gate 6 in the audit programme) standalone and confirm it recognizes the supersession: the old edition is no longer flagged as current, and no stale reference to the old edition survives outside a historical or explicitly-superseded context. A surviving flag means Step 2's sweep missed a location; return to Step 2 for that location rather than suppressing the gate.

### Step 7: Record the campaign

Add a CHANGELOG entry covering the upgrade (root summary plus the detailed mirror, per the change-tracking discipline). Where the substantive rewrites span more than one commit or pull request, the campaign is multi-PR: record a backlog item tracking the remaining locations so the campaign is not left half-applied, and rotate it to the closed-item ledger when the last location lands. A single positional-only bump that touches one register row and a handful of markers is a single PR and needs only its CHANGELOG entry.

---

## Roles

| Role | Responsibility |
| --- | --- |
| Governance Library Maintainer | Decides whether to adopt a new edition; approves the campaign; performs or directs the publisher-source confirmation (Step 1) and the verification capture (Step 5), which the citation-verification methodology assigns to a human verifier. |
| AI assistant (under maintainer direction) | Prepares the corpus sweep (Step 2), the classification worklist (Step 3), and the mechanical positional updates (Step 4); drafts the register and CHANGELOG edits for the maintainer to confirm; runs the standards-currency gate (Step 6). |

The human-versus-AI split for the publisher-source capture in Steps 1 and 5 follows [`specification-citation-verification.md`](specification-citation-verification.md) §3: the AI prepares and records, the human captures the primary publisher text.

---

## Operating expectations

- The campaign is corpus-wide, not document-local: Step 2's completeness is what prevents the drift this procedure exists to stop.
- A version upgrade never suppresses the standards-currency gate to pass; a surviving flag is signal that a cited location was missed.
- A positional bump and a substantive rewrite are different edits with different consequences; classifying before editing (Step 3) keeps a mechanical year-bump from being mistaken for, or bundled with, a content change.
- The publisher's own source is the version authority at every step where a version is asserted; a locally held copy informs the reading but does not settle the version.

---

## Framework alignment

| Requirement | ISO/IEC 27001:2022 | NIST CSF 2.0 | COBIT 2019 | ISO 9001 |
| --- | --- | --- | --- | --- |
| Controlled change to referenced requirements | A.5.36, A.5.37 | GV.OC, GV.PO | APO01, BAI06 | §7.5, §8.5.6 |
| Documented-information currency | A.5.37 | GV.OC | BAI08 | §7.5.3 |
| Verification against an authoritative source | A.5.36 | GV.OV | MEA01 | §9.1 |

---

## Limitations

This procedure is a CC BY-SA 4.0 baseline. The specific tooling (the standards-currency gate, the canonical-citations register, the verifications register) is this library's implementation; an adopting organization substitutes its own equivalents. The procedure expresses the outcome (a corpus-wide, evidence-grounded, gate-confirmed edition transition) and a workable sequence; the depth of the classification step and the multi-PR campaign tracking scale with the size of the corpus and the materiality of the edition change.

---

**End of Document**
