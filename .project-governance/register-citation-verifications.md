# Citation Verifications Register

**Document Title:** Citation Verifications Register\
**Document Type:** Register\
**Version:** 1.1.2\
**Date:** 2026-07-02\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/specification-citation-verification.md`](../governance/specification-citation-verification.md), [`governance/register-canonical-citations.md`](../governance/register-canonical-citations.md), [`governance/register-document-index-and-classification.md`](../governance/register-document-index-and-classification.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Per the verification freshness rule in [`governance/specification-citation-verification.md`](../governance/specification-citation-verification.md) §12: each entry re-verified every 12 months from its last Date checked\
**Repository Path:** [`.project-governance/register-citation-verifications.md`](register-citation-verifications.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register records every verification performed against an entry in the Canonical Citations Register ([`register-canonical-citations.md`](../governance/register-canonical-citations.md)) under the methodology in the Citation Verification Specification ([`specification-citation-verification.md`](../governance/specification-citation-verification.md)).

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

Each row carries the following fields (per Citation Verification Specification §9). The schema reflects the AI/human operating model defined in Citation Verification Specification §3: the `Captured by` field identifies the human verifier who fetched the publisher page; the `Recorded by` field identifies the actor (typically the AI verifier in a clerical role) who appended the row to this register.

| Field | Description |
| --- | --- |
| **Standard ID** | Identifier as it appears in the Canonical Citations Register. For allow-list domain-mapping verifications, the publisher name. |
| **Verified Field** | Which field of the canonical-citations entry was verified (existence / version / publication-date / supersedence / topic / ID format / allow-list domain mapping). For full-row verification: "all". |
| **Publisher** | Publisher name. |
| **Primary URL** | The publisher's canonical-domain URL fetched. |
| **Wayback URL** | The `web.archive.org` snapshot URL captured at verification time. |
| **Secondary URL** | Optional Tier 2 corroborating URL. Empty where no corroborating source was found. |
| **Captured text** | Verbatim publisher page text supporting the claim. The publisher's actual words. |
| **Captured by** | Identifier of the human verifier who fetched the page and captured the text (per Citation Verification Specification §3.4). A row whose `Captured by` field implies AI primary capture is invalid and not a verification. |
| **Result** | Match / Diverged / Not found. |
| **Divergence detail** | If Diverged: register said X; publisher said Y. Empty otherwise. |
| **Confidence** | A (publisher + Tier 2 corroborating), B (publisher only), C (secondary-only), D (un-verifiable). Per Citation Verification Specification §10. |
| **Date checked** | ISO 8601 date of the verification. |
| **Recorded by** | Identifier of the actor who appended the row (typically the AI verifier acting as recorder; may be the same human as `Captured by` when the human recorded the row directly). |
| **Notes** | Anything else worth recording: caveats, ambiguities, methodology divergences. |
| **Resolution** | For D-rated rows: what was done (corrected / removed / pending). Empty for A, B, C ratings. |

---

## Verification log

Rows are recorded in the verification log below in chronological order of verification, oldest first.

The register is initially empty. Verifications begin in the first verification sub-phase under the Citation Verification Specification.

| Standard ID | Verified Field | Publisher | Primary URL | Wayback URL | Secondary URL | Captured text | Captured by | Result | Divergence detail | Confidence | Date checked | Recorded by | Notes | Resolution |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

*No verifications recorded yet. First verification sub-phase pending.*

---

## D-rated resolutions log

When a verification produces a D rating, the resolution is recorded both in the row above and in this log for visibility.

| Standard ID | Date flagged | Reason | Resolution decision | Resolution date | Downstream-reference impact |
| --- | --- | --- | --- | --- | --- |

*No D-rated entries recorded yet.*

---

## Coverage summary

This section is updated at the end of each verification batch. It summarizes, for the Canonical Citations Register's current contents, how many entries are verified and at what confidence.

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

- [`governance/specification-citation-verification.md`](../governance/specification-citation-verification.md): the methodology this register implements.
- [`governance/register-canonical-citations.md`](../governance/register-canonical-citations.md): the register whose entries are verified here.
- [`tools/lint-citation-verification-freshness.py`](../tools/lint-citation-verification-freshness.py): linter that flags entries older than 12 months. Shipped as gate 27 of the audit programme per [`governance/specification-audit-programme.md`](../governance/specification-audit-programme.md) §6.

---

**End of Document**
