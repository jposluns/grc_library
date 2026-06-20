---
name: citation-quote-verification
description: Before any completion claim on a change that touches a document containing external-source citations (verbatim quotes, paraphrased synthesis, or framework references with article / section / clause locators), verify each citation's text against the cited source at the cited location. Catches the failure mode where a confidently-cited quote does not actually appear in the source, or a paraphrase mis-represents the source's meaning. Catches what the mechanical citation linters (format and currency) cannot reach: quote-to-source correspondence.
derives_from: ../../governance/evidence-grounded-completion.md
---

# Citation Quote Verification

## Overview

A citation has three properties a reader will rely on: format (is it well-formed and resolvable), currency (is the source still the current version), and correspondence (does the quoted or paraphrased text actually appear at the cited location and faithfully represent the source). The mechanical citation linters (`tools/lint-citations.py` for framework identifiers; `tools/lint-standards-currency.py` for version recency) check the first two. They do not check the third.

This skill closes that gap. Before any completion claim on a change that touches citation-bearing content, each citation in the modified region is verified by reading the source, locating the cited passage, and confirming the document's text matches.

The failure mode this skill targets is the most-cited-but-least-checked: a confidently-asserted quote that does not appear in the cited source, or a paraphrase whose meaning has drifted from what the source actually says. Mechanical linters cannot catch this because correspondence is a semantic check, not a format check.

## When to Use

- Before stating "done", "fixed", "complete", or any synonym on a change that touches a document with external-source citations (any of: markdown-link references with quoted text, ``> blockquote`` passages, paraphrased synthesis attributed to a named source, framework references with specific article / section / clause locators).
- Before declaring a new governance document, register, or annex complete when that document contains citations.
- Before claiming a citation refresh (e.g., bumping a standard's version reference) is complete, since refreshing the version identifier does not by itself verify the cited passage still appears at the same location in the new version.
- When the [`evidence-grounded-completion`](../evidence-grounded-completion/SKILL.md) skill's contradiction-search step (step 4) surfaces a citation, this skill is the next layer of verification.

## Process

For each citation in the modified region:

1. **Identify the cited source**. Resolve the citation to a fetchable artefact (a URL, a known standard document, a referenced annex). Quote the citation's location identifier (URL, section, article, paragraph, clause number) so the verification has a single target.
2. **Locate the cited passage at the source**. Fetch or open the source, navigate to the cited location, and identify the corresponding passage. If the citation does not specify a location precise enough to locate (e.g., "see NIST CSF" with no section), the citation itself is the failure, surface it as such.
3. **Compare for correspondence**:
   - For **verbatim quotes**: the quoted text must appear verbatim at the cited location, modulo trivial whitespace and quotation-mark conventions. Any other deviation is a finding.
   - For **paraphrased synthesis**: the paraphrase must faithfully represent the source's meaning. A faithful paraphrase preserves the source's normative force (must / should / may / could), its scope (which actors, which conditions), and its key qualifiers (exceptions, time-bounded conditions). A drift in any of those is a finding.
   - For **framework references with locators** (e.g., "ISO 27001 §A.5.36"): the locator must resolve to a section in the current edition that addresses the cited topic. A locator that points to a section about a different topic is a finding (the standard may have been re-restructured between editions).
4. **Quote your evidence**. For each verification, record: the citation as it appears in the document; the source location you fetched / opened; the corresponding source text; whether the match is verbatim / faithful-paraphrase / drift. Paraphrases do not count as evidence, name the actual source text.
5. **Surface drift**. For each finding, classify: missing-from-source (quote does not appear at cited location); drifted-meaning (paraphrase departs from source); stale-locator (article / section number no longer addresses the topic); unresolvable-citation (source is not fetchable / location is not specifiable). Each class has a different remediation.

## Red Flags

- Verifying a citation against the assertion's own self-reference (the document's own footnote rather than the actual source).
- Trusting a paraphrase's plausibility instead of reading the source.
- Treating "the standard moved this content to a new section" as an acceptable drift without flagging it.
- Skipping the verification for "obvious" or "well-known" citations, well-known citations drift too (e.g., a NIST SP version revision often re-numbers controls).
- Declaring "verified" without quoting the source text the verification was grounded in.

## Verification

This skill is complete when:

- Every citation in the modified region has been resolved to a fetchable / openable source.
- Each citation has been matched against the cited location, with the source text quoted in the verification record.
- Each finding (missing / drifted / stale / unresolvable) has been classified and surfaced for remediation.
- Citations the skill could not verify (source not fetchable in the current environment) are listed by name as unverified rather than silently included in the "passed" set.

If any of these is missing, the skill is incomplete and a completion claim that touches the citation-bearing document is not yet permitted.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The citation is well-formed; that is enough." | Format is one of three properties. Correspondence is the one this skill checks. |
| "I cited a section number, so the quote must be there." | Section numbers change between editions. The quote can drift. |
| "Paraphrases don't need verification; they're not exact quotes." | Paraphrase drift is the most common citation defect because it looks innocent. |
| "I read this source years ago; I remember what it says." | Memory drifts faster than the source. Fetch it. |
| "The corpus has too many citations to verify them all." | Verify the ones in the modified region. The pre-existing ones are the maintainer's call. |

## See Also

- Canonical rule [`governance/evidence-grounded-completion.md`](../../governance/evidence-grounded-completion.md): the per-claim verification protocol this skill applies to citations specifically.
- Related skill [`evidence-grounded-completion`](../evidence-grounded-completion/SKILL.md): the generic verification protocol. This skill is its citation-specific specialisation.
- Related skill [`validation-sweep`](../validation-sweep/SKILL.md): when the sweep surfaces a citation finding, this skill is the targeted follow-up.
- Mechanical gates that operate at a different layer: `tools/lint-citations.py` (citation format), `tools/lint-standards-currency.py` (citation currency). Together with this skill, the three cover citation format, currency, and correspondence.
