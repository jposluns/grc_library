# Historical-Context Citation Exceptions Register

**Document Title:** Historical-Context Citation Exceptions Register\
**Document Type:** Register\
**Version:** 1.0.15\
**Date:** 2026-09-26\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`governance/register-canonical-citations.md`](../governance/register-canonical-citations.md), [`governance/specification-citation-verification.md`](../governance/specification-citation-verification.md)\
**Classification:** Public\
**Category:** Core Governance\
**Review Frequency:** Quarterly, and whenever a sanctioned sentence or its document changes (the gate refuses a row whose sentence no longer matches)\
**Repository Path:** [`.project-governance/register-historical-citation-exceptions.md`](register-historical-citation-exceptions.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose

This register is the only sanctioned way to cite a superseded edition as history, for example to record that the 2019 edition of one standard extended an earlier edition of another. Each row sanctions one citation in one sentence of one document. Citations that are not sanctioned here are checked as usual: a stale citation the established check recognizes keeps blocking the standards-currency gate, and a stale form found only by discovery stays advisory in report mode.

## Policy

- Use a row only for a sentence that describes the past. The gate refuses a sentence carrying common present-tense wording, but that screen is a vocabulary heuristic; the reviewer of the row confirms the sentence makes no claim about what a superseded edition requires, states or governs today.
- The sentence is pinned verbatim and must stand as its own paragraph in the citing document: the whole line from column 1 (not in a list, heading, quotation, table or indented block), with a blank line above and below, and exactly one sentence ending in `.`, `!` or `?`. The sentence is plain ASCII text: letters, digits, spaces and the marks . , ; : ' " ( ) / % - only. A citing document that carries raw HTML or any HTML comment, a line the line model reads as a fence (after any leading whitespace) other than a three-character fence at column 1, with no backtick in a backtick fence's info string, closed by a bare line of the same character, or a line separator other than LF or CRLF cannot hold a sanctioned sentence. Any edit to it, a second copy of it outside a fenced code block (an indented code block is counted), or moving it into a longer paragraph makes the row invalid, and an invalid row blocks.
- The citation appears in the sentence exactly once, written as in the Citation column. Another written form of the same edition in the same sentence is not sanctioned.
- The rows are recorded in the data file [`register-historical-citation-exceptions.toml`](register-historical-citation-exceptions.toml), which is what the gate reads. The table below is generated from it by `python3 tools/build-historical-citation-exceptions.py`, and the gate refuses a table that differs from the data, and any line ending other than LF, front matter, raw HTML, comment, fence marker, math markup, image, table or pipe character elsewhere on this page. Prose that imitates a row is not detected, so review of this page is the control for it. This page is exempt from the gate's citation scan (its schema example and table quote superseded editions), so keep other citations off it. Edit the data file, never the table; how this page renders cannot change what is sanctioned.
- A row sanctions only the citation it names. Any other citation in the same sentence, or on the same line, is checked as usual.

## Schema

Each row is one table in the data file's `exception` array (usually written as an `[[exception]]` block), with exactly these keys, under `schema_version = 1`:

- **id**: `HCE-NNN`, unique, never reused.
- **path**: the repository-relative Markdown path of the citing document.
- **citation**: exactly one registered identifier with a registered superseded edition, written as it appears in the sentence (for example `ISO/IEC 27001:2013`).
- **sentence**: the whole sentence, verbatim, in plain ASCII. A sentence containing a full stop followed by a space before its end (for example a citation written with `Rev. 4`) reads as two sentences and cannot be sanctioned.
- **reason**: why the historical citation is needed.
- **upstream** and **verified**: the publisher evidence for the historical fact (an `https://` URL that names a host), and the past UTC date it was checked (a TOML date, `YYYY-MM-DD`).

Every value is a single line of printable ASCII with no leading, trailing or doubled space.

## Exceptions

<!-- BEGIN-GENERATED historical-citation-exceptions: edit the .toml data file, then run python3 tools/build-historical-citation-exceptions.py -->

| Exception ID | Path | Citation | Sentence | Reason | Upstream check location | Last verified (UTC) |
| --- | --- | --- | --- | --- | --- | --- |

<!-- END-GENERATED historical-citation-exceptions -->

## Maintenance

- Add a row to the data file in the same pull request as the sentence it sanctions, then run `python3 tools/build-historical-citation-exceptions.py`.
- Remove the row from the data file in the same pull request that removes or rewrites the sentence, then rerun the build tool.
- Re-check the evidence at each quarterly review.
