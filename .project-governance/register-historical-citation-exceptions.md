# Historical-Context Citation Exceptions Register

**Document Title:** Historical-Context Citation Exceptions Register\
**Document Type:** Register\
**Version:** 1.0.9\
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
- The sentence is pinned verbatim and must stand as its own paragraph in the citing document: the whole line from column 1 (not in a list, heading, quotation, table or indented block), with a blank line above and below, and exactly one sentence ending in `.`, `!` or `?`. The sentence is plain ASCII text: letters, digits, spaces and the marks . , ; : ' " ( ) / % - only. A citing document that carries raw HTML or any HTML comment, a line the line model reads as a fence (after any leading whitespace) other than a three-character fence at column 1, with no backtick in a backtick fence's info string, closed by a bare line of the same character, or a line separator other than LF or CRLF cannot hold a sanctioned sentence. Any edit to it, a second copy of it outside a code block, or moving it into a longer paragraph makes the row invalid, and an invalid row blocks.
- The citation appears in the sentence exactly once, written as in the Citation column. Another written form of the same edition in the same sentence is not sanctioned.
- This register has exactly one Exceptions section, headed exactly `## Exceptions` (every heading in this register is plain ASCII text and at the top level, not inside a list item or indented; no setext heading and no blockquote is used; and no other line may render, or could render, as an Exceptions heading), holding only this table, padded with ASCII spaces and tabs only, with no two rows naming the same path, sentence and citation, each row starting at column 1; the register holds no fenced block, HTML comment or raw HTML, and uses only LF or CRLF line endings. The gate refuses anything else.
- A row sanctions only the citation it names. Any other citation in the same sentence, or on the same line, is checked as usual.

## Schema

- **Exception ID**: `HCE-NNN`, unique, never reused.
- **Path**: the repository-relative Markdown path of the citing document.
- **Citation**: exactly one registered identifier with a registered superseded edition, written as it appears in the sentence (for example `ISO/IEC 27001:2013`).
- **Sentence**: the whole sentence, verbatim, with no pipe character. A sentence containing a full stop followed by a space before its end (for example a citation written with `Rev. 4`) reads as two sentences and cannot be sanctioned.
- **Reason**: why the historical citation is needed.
- **Upstream check location** and **Last verified (UTC)**: the publisher evidence for the historical fact, and the past UTC date it was checked.

## Exceptions

| Exception ID | Path | Citation | Sentence | Reason | Upstream check location | Last verified (UTC) |
| --- | --- | --- | --- | --- | --- | --- |

## Maintenance

- Add a row in the same pull request as the sentence it sanctions.
- Remove the row in the same pull request that removes or rewrites the sentence.
- Re-check the evidence at each quarterly review.
