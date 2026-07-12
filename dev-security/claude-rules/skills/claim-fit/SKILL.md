---
name: claim-fit
description: Cadenced citation-precision audit of normative-attribution claims. Catches the gate-blind "attributed value, silent source" class: a sentence ties a specific value (a retention period, a clock, a threshold) to a named normative source, the source exists and the citation is well-formed (so the existence and citation gates pass), but the source does not actually prescribe the attributed value. Run the one-time full Tier-A pass at adoption, then ad-hoc when a claim is in doubt and after any batch that adds or edits normative-value claims. It dispatches a semantic judge over the tiered worklist that the project's recall-oriented pre-filter produces, adjudicating each claim against the held source TEXT in the reference base, then routes confirmed misattributions. It catches what the existence gates structurally cannot: claim precision needs a read of the source clause, not a source-exists check.
derives_from: ../../governance/evidence-grounded-completion.md
---

# Claim Fit (citation-precision audit of normative-attribution claims)

## Project wiring (the parent library's instantiation; adopters substitute their own)

Portable procedure, concrete names. In the parent GRC library this skill runs with:

- Citation, existence, and currency gates (the mechanical floor this skill's precision layer sits on): gates 5 and 6 (the framework-citation hallucination audit and the standards-currency audit), plus the control-code existence gates 48, 49, 54, 58, and 61 for cited control identifiers.
- Recall-oriented pre-filter: `tools/audit-claim-precision.py` (advisory, always exits 0, explicitly not a gate), with `--ref-base <path-to-reference-base-checkout>` to report each named source family's held-state from the reference-base indexes and `--tier A` for the Tier-A-only cadence.
- Mechanical baseline: `tools/run_all_audits.sh` (the all-gates suite step 1 confirms exits 0 before the semantic read).
- Reference base: the sibling private `grc_library_ref` repository, located via its indexes (`grc_library_ref/INDEX.md`, `grc_library_ref/catalogue.yml`, `grc_library_ref/SECTION-INDEX.md`), with the per-source currency confirmation and trust-bucket rules its own conventions define.
- Tier definitions (as the pre-filter implements them): TIER A, a specific value tied to a named normative source in one clause, both orders, judged EVERY row; TIER B, soft-alignment phrasing with no specific value, sampled on cadence.

An adopting project maps each bullet to its own gates, pre-filter, baseline runner, reference base, and tiers; the procedure below refers to them generically.

## Overview

The audit gates that guard citations check existence, well-formedness, and currency, not precision. The citation family confirms a named standard exists with the right year and identifier; the control-code gates confirm a cited code is in its catalogue. None of them asks the question that decides whether a normative-attribution sentence is true: does the cited source actually contain the supporting language the sentence attributes to it? A claim can name a real source, cite it in perfect form, and still attribute to it a value the source never states. That class, "attributed value, silent source", is gate-blind by construction, because precision cannot be decided by a string-and-membership check; it needs a reader to compare the attributed value against the source's own clause.

The class is not hypothetical. The motivating incident in the parent library: a policy attributed a fixed "180-day baseline" to NIST SP 800-53 CA-6 and ISO/IEC 27001 Clause 9.2, and neither source prescribes a fixed interval. The census that shipped with the triage tool surfaced the standing candidate shapes: three carriers attributing a 7-year retention to ISO/IEC 42001 plus EU AI Act Annex IV (the ISO half informs the figure without prescribing it; the Annex IV half, the adoption pass found, carries no retention obligation at all; the value is the corpus's own canonical choice, recorded as such in the project's decision trail), and a 24-hour supplier-notification KPI citing GDPR Article 33(2), which sets "without undue delay", not a fixed clock.

`claim-fit` is the semantic-judge half of a two-part instrument whose recall-oriented triage half is the advisory pre-filter named in the project wiring above (explicitly NOT a gate; always exits 0; CI cannot host the check because the ground truth lives in the sibling private reference repo). The tool tiers the worklist by risk: TIER A rows (a specific value tied to a named normative source in one clause, both orders, the exact motivating-incident shape) are judged EVERY one; TIER B rows (soft-alignment phrasing with no specific value) are sampled on cadence. The skill judges: for each worklisted claim, it reads the cited source's own text in the reference base and decides whether the source prescribes, merely informs, or contradicts the attributed value. The binding rule mirrors the matrix-fit lesson: judge against the held source TEXT, never a remembered meaning, because a remembered meaning is exactly what produced the misattribution.

The verdict vocabulary is four-valued, because the right fix differs by verdict:

- **`prescribed`**: the source states the attributed value; the claim fits as written.
- **`informed-not-prescribed`**: the source motivates the value but does not state it (the 7-year retention shape from the census above). The fix is the ATTRIBUTION PHRASING, never the value: reword to name the value as the corpus's or organization's canonical choice informed by the source, so the sentence stops asserting source language that does not exist.
- **`mis-attributed`**: the source states a different value, or none, where the sentence asserts one (the motivating-incident and Article 33(2) shapes). The fix is the value or the citation, decided per finding.
- **`source-not-held`**: the reference base holds no text for the named source, so no judgement is possible. The claim routes to the maintainer's source-drop queue and is NEVER adjudicated from memory (the evidence-grounded-completion external-version corollary binds here, as does any project egress constraint on fetching new sources).

This skill is a single-pass advisory audit, not a fix-to-fixed-point loop and not a trust-recovery escalation. It runs on a cadence, surfaces confirmed misattributions, and routes or fixes them under the normal in-window / out-of-window triage. It is to normative-value claims what `/matrix-fit` is to control-code citations: the semantic layer over gates that can only check existence.

## When to Use

- **The one-time full Tier-A pass** when the skill is adopted (the whole Tier-A census is small by construction; every row is judged once, establishing the baseline).
- **After any batch that adds or edits normative-value claims** (a substantive content batch, a jurisdiction annex, a KPI or SLA table): run the tool, judge the NEW Tier-A rows the batch introduced, and sample its Tier-B rows.
- **Ad-hoc when a claim is in doubt** (a maintainer flag, a `/validate` or `/full-qa` note about a suspicious attribution, an apply-time uncertainty about whether a source states a value).
- **NOT as a replacement for the citation gates.** The existence, currency, and control-code gates still run on every PR; `claim-fit` is the precision layer on top of them. A claim must pass the gates first; this skill judges precision among claims that already pass.

## Process

### 1. Establish scope and confirm the reference base

Name the scope for this run: the full Tier-A census (the adoption pass), the rows a just-applied batch introduced (the per-batch cadence), or a flagged set (the ad-hoc cadence). Confirm the project's all-gates suite (named in the project wiring above) exits 0 first; a precision pass judges among claims that already pass the mechanical gates. Confirm the reference base is available: its indexes locate the held source texts, and the per-source currency rule applies (confirm a held source is current before relying on it, per the reference base's own invariants; a superseded held text is grounds to defer, not to judge against the stale text silently).

### 2. Run the advisory triage tool to generate the worklist

Run the recall-oriented pre-filter named in the project wiring, pointing it at the reference base (restrict to Tier A for the Tier-A-only cadence). The tool always exits 0; its output is a recall-oriented worklist, tiered, with each named source family's held-state reported best-effort from the reference-base indexes. Treat the worklist as the judge's input-narrowing step, NOT a defect list: a listed row is a candidate to read, and a lexical extractor deliberately over-collects (a spurious row costs the judge seconds; a missed row ships a misattribution). Add any claim the maintainer or a prior QA note flagged even if the extractor did not list it.

### 3. Dispatch the citation-precision judge over the worklist

Dispatch one or more subagents (or perform the read directly for a small worklist) to judge each claim. The judge brief: locate the named source's held text via the reference-base indexes, read the specific clause, article, or annex the claim points at, and return one of the four verdicts (`prescribed` / `informed-not-prescribed` / `mis-attributed` / `source-not-held`) with the source passage QUOTED as evidence. The binding rules: judge against the held source text, never memory or plausibility; a verdict without a quoted source passage (or, for `source-not-held`, without the index lookup that failed) is a hypothesis, not a finding; and an un-held source is never adjudicated from recall, whatever the judge's confidence. Every judgement quotes the claim's location as `path:line`, the attributed value, the named source, and the source passage (or the index evidence of absence).

### 4. Synthesize and apply-time-verify each candidate against the source text

The orchestrator re-reads each candidate `mis-attributed` and `informed-not-prescribed` verdict's source passage in the reference base before treating it as a finding (the judge produces research; the orchestrator confirms). A judge false positive (a passage the judge missed elsewhere in the source, a version mismatch, an over-literal reading of a clause the source states in different words) is refuted here, not routed. For each confirmed finding, draft the fix per the verdict: a rephrased attribution for `informed-not-prescribed` (the value stands; the sentence stops asserting source language), a corrected value or citation for `mis-attributed` (which one is a per-finding call, surfaced to the maintainer when the value is an authorial choice), and a source-drop queue entry for `source-not-held`. When an attribution is rephrased, grep the full touched file for sibling carriers of the same attribution at bare-token width (the same value-plus-source pair recurs across policy families).

### 5. Triage and route findings

For confirmed findings in the current scope, fix them in-window: apply the fix, bump the touched document's Version and Date in the same commit, and record the correction in the CHANGELOG-detailed entry. Where the fix requires an authorial decision (which of value-vs-citation is wrong; whether a canonical corpus value should be re-anchored), surface it to the maintainer with named options rather than silently picking. Confirmed findings outside the current scope are surfaced with named options (fix-now vs route-to-backlog), not auto-deferred. Findings refuted at apply-time are recorded with the refutation, not routed. Findings that dedupe against an existing backlog item are cross-referenced, not duplicated.

### 6. Record and surface

Surface confirmed findings inline in chat (per-finding: claim `path:line`, the attributed value, the named source, the verdict with the quoted source passage, the fix applied or the option surfaced). Write the run to the project's claim-fit record location and append a history row; a zero-finding run still gets a history row (the proof-of-discipline), with no detail file. The pass terminates when the worklist is judged, the confirmed findings are routed or fixed, and the run is recorded; it is a single advisory pass, not a fix-to-fixed-point loop.

## Red Flags

- Judging a claim from the source's remembered content or general reputation instead of reading the held text. The remembered meaning is the failure mode that produced the misattribution.
- Adjudicating a `source-not-held` claim anyway "because the answer is well known". No held text, no judgement; the claim routes to the source-drop queue.
- Treating the triage tool's worklist as a defect list. It is recall-oriented; most Tier-A rows on a clean corpus will judge `prescribed`, and Tier-B rows are soft-alignment claims that mostly fit.
- Fixing an `informed-not-prescribed` finding by changing the VALUE. The value is frequently the corpus's own canonical choice (the canonical-choice class the census above illustrates); the defect is the attribution phrasing, and silently changing a canonical value is an authorial decision the maintainer owns.
- Routing a judge verdict without the orchestrator's own re-read of the source passage. Apply-time verification is the false-positive filter; a judge can miss the prescribing clause elsewhere in a long source.
- Rephrasing one carrier of a misattributed value while sibling carriers of the same value-plus-source pair survive. Grep at bare-token width across the touched file and the corpus before claiming the class fixed.
- Running this as a substitute for the citation gates, or skipping it because "the gates passed". The gates and this skill cover orthogonal classes; a well-formed citation says nothing about precision.

## Verification

The pass is complete on a given run when:

- The scope was named and the mechanical baseline was clean (the project's all-gates suite exit 0) before the semantic read.
- The triage tool was run and its worklist (plus any flagged claims) was the judge's input.
- Every in-scope Tier-A row was judged against the held source text with the passage quoted (or verdicted `source-not-held` on index evidence); the run's Tier-B sample is named.
- The orchestrator re-read each candidate finding's source passage and refuted or confirmed it; refutations are recorded, not routed.
- Confirmed in-scope findings were fixed per their verdict class (Version and Date bumped, CHANGELOG entry written) or surfaced with named options where the fix is authorial; `source-not-held` claims are queued for the maintainer's source drops.
- The run was recorded (history row always; detail file when findings exist) and findings were surfaced inline in chat.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The citation gates pass, so the claim is fine." | The gates check the source exists and the citation is well-formed, not that the source states the attributed value. Only a read of the clause decides. |
| "Everyone knows GDPR Article 33 says 72 hours." | Article 33(1) does; the census's flagged carrier cites 33(2), which says "without undue delay". The clause read, not the reputation, is the evidence. |
| "The source is not held, but I am confident what it says." | An un-held source is never adjudicated from memory (the external-version corollary). Route to the source-drop queue. |
| "The source does not state the value, so the value is wrong." | Often the value is the corpus's own canonical choice the source merely informs. The fix is the attribution phrasing; changing the value is the maintainer's call. |
| "The worklist is short, so the corpus is precise." | The worklist is recall-oriented triage over lexical shapes; unlisted prose can still misattribute in shapes the extractor does not match. A short worklist narrows the read; it certifies nothing. |
| "Claim precision should just be a gate." | It is not mechanically checkable, and the ground truth lives in a private reference base CI cannot see. The cadenced audit is the durable instrument (the same conclusion the matrix-fit design reached). |

## See Also

- Canonical rule [`evidence-grounded-completion`](../../governance/evidence-grounded-completion.md): the assertion-side discipline this skill applies to normative attributions (a claim that a source states a value requires reading the source, not inferring it), including the external-version-currency corollary that forbids judging un-held or unconfirmed sources from memory.
- Related skill [`matrix-fit`](../matrix-fit/SKILL.md) (`/matrix-fit`): the sibling semantic audit for control-code fit; this skill applies the same pattern (advisory recall-oriented tool plus cadenced semantic judge) to attributed values. The two-PR shipping precedent and the judge-against-the-source rule both come from it.
- Related skill [`citation-quote-verification`](../citation-quote-verification/SKILL.md): verifies cited *quotes* match source text verbatim; this skill verifies attributed *values and requirements* are actually prescribed by the source. A quote can be verbatim while the surrounding attribution overstates it.
- Related skill [`validation-sweep`](../validation-sweep/SKILL.md) (`/validate`): the corpus-wide drift sweep whose notes can flag an attribution doubt for this skill to adjudicate.
- Related skill [`publication-screening`](../publication-screening/SKILL.md) (`/screen-publications`): the admission-control screen for the untrusted publications bucket; once a screened publication's claim enters the corpus, its precision is this skill's cadence to adjudicate like any other attributed value.
- The recall-oriented pre-filter named in the project wiring above: the triage step that feeds this skill's worklist (not a gate; always exits 0; a Tier-A-only mode for the judge-every-row tier; a reference-base flag to report source held-state from the reference-base indexes).
- The reference base named in the project wiring above: located via its own indexes, with the per-source currency confirmation and trust-bucket rules its own conventions define.
