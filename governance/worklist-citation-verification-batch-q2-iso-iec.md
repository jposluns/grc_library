# Citation Verification Worklist - Batch Q2: ISO and ISO/IEC standards

**Document Title:** Citation Verification Worklist: Batch Q2 (ISO and ISO/IEC)\
**Document Type:** Worklist\
**Version:** 1.0.0\
**Date:** 2026-05-29\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/specification-citation-verification.md`](specification-citation-verification.md), [`governance/template-citation-verification-worklist.md`](template-citation-verification-worklist.md), [`governance/register-citation-verifications.md`](register-citation-verifications.md), [`governance/register-canonical-citations.md`](register-canonical-citations.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** This worklist is a per-batch working artefact; it does not have a recurring review cadence. The authoritative record is the Citation Verifications Register.\
**Repository Path:** [`governance/worklist-citation-verification-batch-q2-iso-iec.md`](worklist-citation-verification-batch-q2-iso-iec.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## 1. Purpose

This is the working worklist for the second batch (Q2) of citation verification under the Citation Verification Specification ([`specification-citation-verification.md`](specification-citation-verification.md)).

Scope: every ISO and ISO/IEC entry in the Canonical Citations Register at the time of batch open (24 entries). This deliberately includes ISO 16484, which appears in the register's sector-specific section but is an ISO standard and is naturally grouped here for batch efficiency.

The AI verifier has prepared this worklist (§4 pre-filled per Citation Verification Specification §8.1). The human verifier executes the fetches and captures verbatim text (per §8.2 and §8.3). The AI verifier transcribes captured text into the Citation Verifications Register at batch close (per §8.4).

---

## 2. How to use this worklist

For each row in §4:

1. Open the **Expected primary URL** in a browser. If a page is not found, use the **Search fallback URL** to locate the correct page; record the actual URL used.
2. Verify the page is served from `iso.org` under TLS. If a redirect leaves `iso.org`, stop for that row and flag.
3. On the publisher page, locate the displayed standard ID, edition, publication year, status, and (where applicable) replacement/superseded relationships. Copy verbatim into the **Captured text** cell. Do not paraphrase.
4. Submit the publisher page to `https://web.archive.org/save/<publisher-url>` and record the resulting snapshot URL in **Wayback URL**.
5. Where a corroborating Tier 2 source exists (ANSI, BSI, DIN catalogue entry for the same standard), record it in **Secondary URL**.
6. Compare publisher metadata against **Expected value (from register)**. Record **Result** (Match / Diverged / Not found) and any **Divergence detail**.
7. Assign **Confidence** per Citation Verification Specification §10.
8. Sign **Captured by**.

At batch close: notify the AI verifier with the completed worklist, who appends rows to the Citation Verifications Register and proposes any canonical-citations corrections for your approval.

---

## 3. Publisher URL patterns and gotchas

### 3.1 URL patterns

ISO publishes catalogue pages at two URL patterns:

- **Catalogue page**: `https://www.iso.org/standard/<publication-id>.html` where `<publication-id>` is ISO's internal publication identifier (not the standard number). This page shows: standard ID, full title, edition, status (Published / Under development / Withdrawn), publication date, abstract, and replacement relationships.
- **OBP (Online Browsing Platform) preview**: `https://www.iso.org/obp/ui/en/#iso:std:iso:<n>:ed-<e>:v1:en` for ISO standards, or `https://www.iso.org/obp/ui/en/#iso:std:iso-iec:<n>:ed-<e>:v1:en` for ISO/IEC. This shows scope, normative references, and the first portion of the text. Useful for confirming standard ID and edition; less complete than the catalogue page for status and supersedence.

The **catalogue page** is the primary verification target. The OBP page is corroborative.

### 3.2 Finding the publication ID

Since the publication ID is not the same as the standard number, the Expected primary URLs below are best-effort guesses based on common patterns observed for adjacent standards. Where a URL returns "Page not found", use the **Search fallback URL** (`https://www.iso.org/search.html?q=<standard-id>`) to find the correct page, then record the actual URL used.

### 3.3 Status field interpretation

- **Published**: standard is current. Edition number and publication date as displayed are verifiable.
- **Under development**: standard is not yet published. If the canonical citations register lists a year for this standard, that year is likely wrong; treat as Diverged or Not found.
- **Withdrawn**: standard is superseded or no longer maintained. The page typically shows the replacement standard ID. If the canonical citations register treats this standard as current, that is a finding.

### 3.4 Multi-part standards

ISO 16484 is a multi-part standard (parts 1, 2, 3, 5, 6, 7 etc. published over multiple years). Verify each part separately. The Expected primary URL for ISO 16484 below is for the part-1 page; record additional URLs in the Notes column for the other parts encountered.

### 3.5 ISO/IEC 27036 part-2 specifically

ISO/IEC 27036 is a multi-part standard. The register entry is specifically ISO/IEC 27036-2 (Common requirements / Supplier relationships, depending on which part is intended). Verify the specific part-2 catalogue page, not the series page.

### 3.6 Known register-side claims worth particular attention

The AI verifier flags the following entries as warranting careful human attention:

- **ISO/IEC 42005**: register claims "2025-05". Confirm exact publication date displayed on iso.org.
- **ISO/IEC 42006**: register claims "2025". This standard had a long draft phase. Confirm it is now published and the displayed publication year matches.
- **ISO 37001**: register claims "2025" current with "2016" superseded. Confirm the 2025 edition is published; the AI verifier's training-time belief was that 2025 was upcoming, which may be wrong in either direction by now.
- **ISO/IEC 38500**: register claims "2024" with "2015" superseded. Confirm the 2024 edition is published.
- **ISO/IEC 5259**: register claims "2024": confirm the part(s) and publication years. ISO/IEC 5259 is a multi-part series; the year may apply to only one part.
- **ISO/IEC 27033**: register claims "2020": this is a multi-part series; some parts have later editions. Confirm the displayed standard structure matches register intent.

These flags are AI-verifier orientation, not verification. The human verifier should treat the publisher page as authoritative regardless of what the AI flagged.

---

## 4. Worklist

| Standard ID | Publisher | Expected primary URL | Search fallback URL | Field(s) to verify | Expected value (from register) | Captured text (verbatim from publisher page) | Wayback URL | Secondary URL | Result | Divergence detail | Captured by | Confidence | Date checked | Recorded into register | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ISO/IEC 27001 | ISO | `https://www.iso.org/standard/27001` | `https://www.iso.org/search.html?q=ISO%2FIEC+27001` | all | Current: 2022; published 2022-10; topic: Information security management systems - requirements; supersedes 2013 |  |  |  |  |  |  |  |  |  | Canonical IS standard. |
| ISO/IEC 27002 | ISO | `https://www.iso.org/standard/75652.html` | `https://www.iso.org/search.html?q=ISO%2FIEC+27002` | all | Current: 2022; published 2022-02; topic: Information security controls; supersedes 2013 |  |  |  |  |  |  |  |  |  | A.5-A.8 control set foundation. |
| ISO/IEC 27005 | ISO | `https://www.iso.org/standard/80585.html` | `https://www.iso.org/search.html?q=ISO%2FIEC+27005` | all | Current: 2022; published 2022-10; topic: Information security risk management; supersedes 2018 |  |  |  |  |  |  |  |  |  |  |
| ISO/IEC 27017 | ISO | `https://www.iso.org/standard/43757.html` | `https://www.iso.org/search.html?q=ISO%2FIEC+27017` | all | Current: 2015; published 2015-12; topic: Cloud-service-specific information security controls; no superseded versions recorded |  |  |  |  |  |  |  |  |  | Confirm no later edition has been published. |
| ISO/IEC 27018 | ISO | `https://www.iso.org/standard/76559.html` | `https://www.iso.org/search.html?q=ISO%2FIEC+27018` | all | Current: 2019; published 2019-01; topic: Protection of PII in public clouds acting as PII processors; no superseded versions recorded |  |  |  |  |  |  |  |  |  | Confirm no later edition. |
| ISO/IEC 27033 | ISO | `https://www.iso.org/standard/63461.html` | `https://www.iso.org/search.html?q=ISO%2FIEC+27033` | all | Current: 2020; topic: Network security architecture and segmentation; no superseded versions recorded |  |  |  |  |  |  |  |  |  | Multi-part standard; capture which part(s) are at 2020 and which are at later years. |
| ISO/IEC 27036-2 | ISO | `https://www.iso.org/standard/59680.html` | `https://www.iso.org/search.html?q=ISO%2FIEC+27036-2` | all | Current: 2014; published 2014-08; topic: Information security for supplier relationships; no superseded versions recorded |  |  |  |  |  |  |  |  |  | Verify the 2014 edition is current and that no 2022+ revision has superseded. |
| ISO/IEC 27701 | ISO | `https://www.iso.org/standard/71670.html` | `https://www.iso.org/search.html?q=ISO%2FIEC+27701` | all | Current: 2019; published 2019-08; topic: Privacy information management extension to ISO/IEC 27001 |  |  |  |  |  |  |  |  |  | Confirm 2025 revision (if any) has not superseded. |
| ISO 22301 | ISO | `https://www.iso.org/standard/75106.html` | `https://www.iso.org/search.html?q=ISO+22301` | all | Current: 2019; published 2019-10; topic: Business continuity management systems |  |  |  |  |  |  |  |  |  |  |
| ISO 31000 | ISO | `https://www.iso.org/standard/65694.html` | `https://www.iso.org/search.html?q=ISO+31000` | all | Current: 2018; published 2018-02; topic: Risk management: principles and guidelines |  |  |  |  |  |  |  |  |  |  |
| ISO/IEC 38500 | ISO | `https://www.iso.org/standard/81684.html` | `https://www.iso.org/search.html?q=ISO%2FIEC+38500` | all | Current: 2024; published 2024; topic: Governance of IT for the organization; supersedes 2015 | _Flagged in §3.6._ |  |  |  |  |  |  |  |  |  |
| ISO/IEC 23894 | ISO | `https://www.iso.org/standard/77304.html` | `https://www.iso.org/search.html?q=ISO%2FIEC+23894` | all | Current: 2023; published 2023-02; topic: AI risk management guidance |  |  |  |  |  |  |  |  |  |  |
| ISO/IEC 42001 | ISO | `https://www.iso.org/standard/81230.html` | `https://www.iso.org/search.html?q=ISO%2FIEC+42001` | all | Current: 2023; published 2023-12; topic: AI management systems: requirements |  |  |  |  |  |  |  |  |  |  |
| ISO/IEC 42005 | ISO | `https://www.iso.org/standard/44545.html` | `https://www.iso.org/search.html?q=ISO%2FIEC+42005` | all | Current: 2025; published 2025-05; topic: AI system impact assessment | _Flagged in §3.6._ |  |  |  |  |  |  |  |  |  |
| ISO/IEC 42006 | ISO | `https://www.iso.org/standard/44546.html` | `https://www.iso.org/search.html?q=ISO%2FIEC+42006` | all | Current: 2025; published 2025; topic: Requirements for bodies providing audit and certification of AI management systems; supersedes draft, draft 2024, 2024 draft | _Flagged in §3.6._ |  |  |  |  |  |  |  |  |  |
| ISO 28000 | ISO | `https://www.iso.org/standard/79612.html` | `https://www.iso.org/search.html?q=ISO+28000` | all | Current: 2022; published 2022-03; topic: Security management systems for the supply chain; supersedes 2007 |  |  |  |  |  |  |  |  |  |  |
| ISO 28001 | ISO | `https://www.iso.org/standard/45654.html` | `https://www.iso.org/search.html?q=ISO+28001` | all | Current: 2007; published 2007; topic: Best practices for implementing supply chain security |  |  |  |  |  |  |  |  |  | Confirm no later edition has been published. |
| ISO 15489 | ISO | `https://www.iso.org/standard/62542.html` | `https://www.iso.org/search.html?q=ISO+15489` | all | Current: 2016; published 2016-04; topic: Records management |  |  |  |  |  |  |  |  |  | Multi-part standard (1 and 2); confirm the part(s) intended. |
| ISO 50001 | ISO | `https://www.iso.org/standard/69426.html` | `https://www.iso.org/search.html?q=ISO+50001` | all | Current: 2018; published 2018-08; topic: Energy management systems |  |  |  |  |  |  |  |  |  |  |
| ISO/IEC 5259 | ISO | `https://www.iso.org/standard/81088.html` | `https://www.iso.org/search.html?q=ISO%2FIEC+5259` | all | Current: 2024; published 2024; topic: Data quality for AI and machine learning | _Flagged in §3.6 (multi-part)._ |  |  |  |  |  |  |  |  |  |
| ISO 37301 | ISO | `https://www.iso.org/standard/75080.html` | `https://www.iso.org/search.html?q=ISO+37301` | all | Current: 2021; published 2021-04; topic: Compliance management systems |  |  |  |  |  |  |  |  |  |  |
| ISO 37001 | ISO | `https://www.iso.org/standard/65034.html` | `https://www.iso.org/search.html?q=ISO+37001` | all | Current: 2025; published 2025; topic: Anti-bribery management systems; supersedes 2016 | _Flagged in §3.6._ |  |  |  |  |  |  |  |  |  |
| ISO/IEC 17021 | ISO | `https://www.iso.org/standard/61651.html` | `https://www.iso.org/search.html?q=ISO%2FIEC+17021` | all | Current: 2015; published 2015; topic: Conformity assessment - requirements for bodies providing audit and certification of management systems |  |  |  |  |  |  |  |  |  | Multi-part; -1 is the foundational part. |
| ISO 16484 | ISO | `https://www.iso.org/standard/37300.html` | `https://www.iso.org/search.html?q=ISO+16484` | all | Current: parts published 2010 to 2020; topic: Building automation and control systems (BACS) | _Flagged in §3.4 (multi-part). Per-part verification required._ |  |  |  |  |  |  |  |  |  |

**Total entries in batch: 24.**

The Expected primary URLs above are AI-verifier best-effort. Where a URL does not resolve to the expected page, use the Search fallback URL and record the actual URL used. The AI verifier acknowledges that the publication IDs may be wrong; the URL pattern is correct but the numeric IDs are guesses.

---

## 5. Closing notes

| Field | Value |
| --- | --- |
| Batch identifier | Q2 - ISO and ISO/IEC |
| Standards in batch | 24 |
| Batch opened | 2026-05-29 |
| Batch closed |  |
| Spot-check entries (per Citation Verification Specification §8.6) |  |
| Spot-check verifier |  |
| Recorded register rows |  |
| Downstream library edits triggered |  |

---

## 6. After batch close

When the batch is complete:

1. The human verifier notifies the AI verifier with the completed worklist.
2. The AI verifier appends one row to the Citation Verifications Register per worklist row, faithfully reproducing captured text.
3. The AI verifier proposes any required edits to the Canonical Citations Register (e.g., updates to current version, supersedence list, topic text) for human approval before commit.
4. The AI verifier identifies downstream library references that would be affected by any corrections; the human verifier approves the fix list.
5. The worklist file may be deleted or retained per maintainer preference; the verifications register row remains as the authoritative record.

---

**End of Document**
