# Citation Verifications Register

**Document Title:** Citation Verifications Register\
**Document Type:** Register\
**Version:** 1.0.0\
**Date:** 2026-05-29\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/specification-citation-verification.md`](specification-citation-verification.md), [`governance/register-canonical-citations.md`](register-canonical-citations.md), [`governance/register-document-index-and-classification.md`](register-document-index-and-classification.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Per the verification freshness rule in [`governance/specification-citation-verification.md`](specification-citation-verification.md) §11: each entry re-verified every 12 months from its last Date checked\
**Repository Path:** [`governance/register-citation-verifications.md`](register-citation-verifications.md)\
**Confidentiality:** Public\
**License:** CC0 1.0 Universal

---

## Purpose

This register records every verification performed against an entry in the Canonical Citations Register ([`register-canonical-citations.md`](register-canonical-citations.md)) under the methodology in the Citation Verification Specification ([`specification-citation-verification.md`](specification-citation-verification.md)).

Each row is a dated, source-anchored, evidence-bearing claim that a citation in the canonical register has been checked against the publisher's own canonical domain. Rows are append-only: a re-verification adds a new row rather than overwriting the prior one, preserving the historical trail.

This register answers the question **"How do we know the canonical citations are correct?"** by recording, for every citation:

- Which publisher page was fetched.
- What that page actually said (captured verbatim).
- When the check was performed.
- What confidence the verification carries.
- What snapshot URL provides a third-party-attested record of the publisher page at the verification date.

---

## How to read this register

Each row records one verification event. Multiple rows per Standard ID are normal: a re-verification produces a new row.

For a quick view of a citation's current status, read the most recent row for that Standard ID. The `Date checked` field shows recency; the `Result` field shows whether the check passed; the `Confidence` field shows the strength of evidence.

For audit purposes, every row remains in the register indefinitely. Removing a row would destroy the verification trail.

---

## Schema

Each row carries the following fields (per Citation Verification Specification §8):

| Field | Description |
| --- | --- |
| **Standard ID** | Identifier as it appears in the Canonical Citations Register. |
| **Verified Field** | Which field of the canonical-citations entry was verified (existence / version / publication-date / supersedence / topic / ID format). For full-row verification: "all". |
| **Publisher** | Publisher name. |
| **Primary URL** | The publisher's canonical-domain URL fetched. |
| **Wayback URL** | The `web.archive.org` snapshot URL captured at verification time. |
| **Secondary URL** | Optional Tier 2 corroborating URL. Empty where no corroborating source was found. |
| **Captured text** | Verbatim publisher page text supporting the claim. The publisher's actual words. |
| **Result** | Match / Diverged / Not found. |
| **Divergence detail** | If Diverged: register said X; publisher said Y. Empty otherwise. |
| **Confidence** | A (publisher + Tier 2 corroborating), B (publisher only), C (secondary-only), D (un-verifiable). Per Citation Verification Specification §9. |
| **Date checked** | ISO 8601 date of the verification. |
| **Verifier** | Identifier of the verifier (role, system identifier, or "maintainer"). |
| **Notes** | Anything else worth recording: caveats, ambiguities, methodology divergences. |
| **Resolution** | For D-rated rows: what was done (corrected / removed / pending). Empty for A, B, C ratings. |

---

## Verification log

Rows are recorded in the verification log below in chronological order of verification, oldest first.

The register is initially empty. Verifications begin in the first verification sub-phase under the Citation Verification Specification.

| Standard ID | Verified Field | Publisher | Primary URL | Wayback URL | Secondary URL | Captured text | Result | Divergence detail | Confidence | Date checked | Verifier | Notes | Resolution |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

*No verifications recorded yet. First verification sub-phase pending.*

---

## D-rated resolutions log

When a verification produces a D rating, the resolution is recorded both in the row above and in this log for visibility.

| Standard ID | Date flagged | Reason | Resolution decision | Resolution date | Downstream-reference impact |
| --- | --- | --- | --- | --- | --- |

*No D-rated entries recorded yet.*

---

## Coverage summary

This section is updated at the end of each verification batch. It summarises, for the Canonical Citations Register's current contents, how many entries are verified and at what confidence.

| Metric | Count |
| --- | --- |
| Total entries in Canonical Citations Register | _Pending first batch._ |
| Entries verified at confidence A | 0 |
| Entries verified at confidence B | 0 |
| Entries verified at confidence C | 0 |
| Entries verified at confidence D (pending resolution) | 0 |
| Entries un-verified | _Pending first batch._ |
| Entries with verification older than 12 months | 0 |

---

## Cross-references

- [`governance/specification-citation-verification.md`](specification-citation-verification.md): the methodology this register implements.
- [`governance/register-canonical-citations.md`](register-canonical-citations.md): the register whose entries are verified here.
- `tools/lint-citation-verification-freshness.py` (planned): linter to flag entries older than 12 months.

---

**End of Document**
