# Citation Verification Worklist Template

**Document Title:** Citation Verification Worklist Template\
**Document Type:** Template\
**Version:** 1.0.0\
**Date:** 2026-05-29\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/specification-citation-verification.md`](specification-citation-verification.md), [`governance/register-citation-verifications.md`](register-citation-verifications.md), [`governance/register-canonical-citations.md`](register-canonical-citations.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Annual and upon material change to the Citation Verification Specification\
**Repository Path:** [`governance/template-citation-verification-worklist.md`](template-citation-verification-worklist.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This template is the working artefact for a citation verification batch under the Citation Verification Specification ([`specification-citation-verification.md`](specification-citation-verification.md)). It enforces the AI/human operating split defined in that specification §3: the AI verifier pre-fills the worklist, the human verifier fetches publisher pages and captures verbatim text, and the AI verifier transcribes the captured text into the Citation Verifications Register.

A worklist is per batch. Copy this template at the start of each batch and rename it (for example, `worklist-citation-verification-batch-q2-iso-iec.md`). Worklists are working artefacts; the authoritative record is the Citation Verifications Register.

---

## 2. How to use this template

### 2.1 At batch start (AI verifier)

1. Copy this template to a new file with a batch-specific name.
2. Update the metadata block (title, version, date, batch identifier).
3. Identify the canonical citations entries in scope of this batch (typically a publisher cluster or a category section).
4. Pre-fill the worklist table below: one row per Standard ID, with Publisher, Expected primary URL, Field(s) to verify, and Expected value from the Canonical Citations Register.
5. Where the publisher's catalogue URL pattern is non-obvious, record the pattern in §3.

### 2.2 During the batch (human verifier)

For each row in the worklist:

1. Open the Expected primary URL in an ordinary browser. Verify the URL bar shows the expected domain and TLS is in use. If the page redirects to a non-allow-listed domain, flag and stop for that row.
2. Locate the text on the publisher page that supports (or refutes) the Expected value. Copy the verbatim text into the Captured text column. Do not paraphrase. Do not summarise.
3. Submit the publisher page to the Wayback Machine via `https://web.archive.org/save/<publisher-url>` and record the resulting snapshot URL in the Wayback URL column. If a same-day snapshot already exists, the existing snapshot URL is acceptable.
4. Where Tier 2 corroboration is found, record the corroborating URL in the Secondary URL column.
5. Record the Result (Match / Diverged / Not found) and any Divergence detail.
6. Assign Confidence per Citation Verification Specification §10.
7. Sign the Captured by column with your identifier.

### 2.3 At batch close (AI verifier, with human review)

1. The AI verifier reads each completed row and appends a corresponding row to the Citation Verifications Register, faithfully reproducing the captured text. The `Recorded by` field of the register row identifies the AI verifier.
2. Where Result is Diverged, the AI verifier proposes register edits to the Canonical Citations Register. The human verifier approves each edit before commit.
3. Where Result is Not found and Confidence is D, the AI verifier flags the canonical-citations entry and lists downstream library references for human disposition (corrected / removed).
4. After all rows are recorded, the human verifier spot-checks at least five entries by re-opening the recorded URLs and confirming the captured text still matches the publisher page. Per Citation Verification Specification §8.6.
5. The batch is closed. The worklist may be retained for evidence or deleted; the register row remains as the authoritative record.

---

## 3. Publisher URL patterns (batch-specific notes)

| Publisher | Catalogue URL pattern | Notes |
| --- | --- | --- |
| _Example: ISO_ | _Example: `https://www.iso.org/standard/<n>.html`_ | _Example: numeric ID is the publication number, not the standard number._ |

_Replace the example row with actual rows for this batch's publishers._

---

## 4. Worklist

Pre-filled by the AI verifier from the Canonical Citations Register. Captured columns are filled by the human verifier during the batch. Recorded-into-register column is filled by the AI verifier at batch close.

| Standard ID | Publisher | Expected primary URL | Field(s) to verify | Expected value (from register) | Captured text (verbatim from publisher page) | Wayback URL | Secondary URL | Result | Divergence detail | Captured by | Confidence | Date checked | Recorded into register | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| _Example: ISO/IEC 27001_ | _ISO_ | _https://www.iso.org/standard/82875.html_ | _existence, current version, publication date_ | _2022; published 2022-10_ |  |  |  |  |  |  |  |  |  |  |

_Add one row per Standard ID in scope of this batch. Delete the example row before submitting the batch._

---

## 5. Closing notes

| Field | Value |
| --- | --- |
| Batch identifier |  |
| Standards in batch |  |
| Batch opened |  |
| Batch closed |  |
| Spot-check entries (per Citation Verification Specification §8.6) |  |
| Spot-check verifier |  |
| Recorded register rows | (URL or anchor links into `register-citation-verifications.md`) |
| Downstream library edits triggered | (URL or commit hash) |

---

**End of Document**
