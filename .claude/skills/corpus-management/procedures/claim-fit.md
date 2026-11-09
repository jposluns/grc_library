---
name: claim-fit
description: Cadenced citation-precision audit of normative-attribution claims. Catches the gate-blind "attributed value, silent source" class, a sentence that ties a specific value (a retention period, a clock, a threshold) to a named normative source, where the source exists and the citation is well-formed (so the existence and citation gates pass) but the source does not actually prescribe the attributed value. Run the one-time full Tier-A pass at adoption, after any batch that adds or edits normative-value claims, on a periodic Tier-B coverage sweep, and ad-hoc when a claim is in doubt. A reviewer adjudicates each claim against the held source TEXT in the reference base, one verdict per cited (value, source) pair, then routes confirmed misattributions. It catches what the existence gates structurally cannot, because claim precision needs a read of the source clause, not a source-exists check.
---

# Claim Fit (citation-precision audit of normative-attribution claims)

## Corpus wiring (this repository's instantiation; adopters substitute their own)

Portable procedure, concrete names. In this repository the procedure runs with:

- Citation, existence, and currency gates (the mechanical floor this precision layer sits on): gates 5 and 6 in [`specification-audit-programme.md`](../specs/specification-audit-programme.md) (the framework-citation hallucination audit and the standards-currency audit), plus the control-code existence gates 48, 49, 54, 58, and 61.
- Mechanical baseline: [`run_all_audits.sh`](../tools/run_all_audits.sh).
- Reference base: the adopting project's reference base of held source texts, located via its own indexes, with the per-source currency confirmation its own conventions define.
- Worklist narrowing: an optional deeper review may supplement the public gates by extracting and tiering candidate claims; without one, the worklist is built by hand from the in-scope diff or document set.
- Tier definitions: TIER A, a specific value tied to a named normative source in one clause, both orders, judged EVERY row; TIER B, soft-alignment phrasing with no specific value, sampled on cadence.
- Sibling-carrier search: [`check-class-completeness.py`](../tools/check-class-completeness.py) is the named instrument for finding sibling carriers of a corrected value-plus-source pair.
- Run records: the adopting project's own working records.

An adopting project maps each bullet to its own gates, baseline runner, reference base, and tiers; the procedure below refers to them generically.

## Overview

The audit gates that guard citations check existence, well-formedness, and currency, not precision. None of them asks the question that decides whether a normative-attribution sentence is true: does the cited source actually contain the supporting language the sentence attributes to it? A claim can name a real source, cite it in perfect form, and still attribute to it a value the source never states. That class, "attributed value, silent source", is gate-blind by construction; it needs a reader to compare the attributed value against the source's own clause.

The class is not hypothetical. The motivating incident in this corpus: a policy attributed a fixed "180-day baseline" to NIST SP 800-53 CA-6 and ISO/IEC 27001 Clause 9.2, and neither source prescribes a fixed interval. Two further illustrative shapes: three carriers attributing a 7-year retention to ISO/IEC 42001 plus EU AI Act Annex IV (the ISO half informs the figure without prescribing it; the Annex IV half carries no retention obligation at all; the value was the project's own canonical choice), and a 24-hour supplier-notification KPI citing GDPR Article 33(2), which sets "without undue delay", not a fixed clock.

The verdict vocabulary is four-valued, because the right fix differs by verdict:

- **`prescribed`**: the source states the attributed value; the claim fits as written.
- **`informed-not-prescribed`**: the source engages or motivates the topic but states NO specific value. The fix is the ATTRIBUTION PHRASING, never the value: reword to name the value as the project's or organization's canonical choice informed by the source.
- **`mis-attributed`**: the source, which IS held, states a DIFFERENT value, or is held-but-silent on the topic where the sentence asserts one. The fix is the value or the citation, decided per finding. The discriminator from `informed-not-prescribed` has two prongs: first, a source that states a DIFFERENT value is `mis-attributed` whether or not it engages the topic; second, when the source states NO specific value, ENGAGEMENT decides (engages the topic: `informed-not-prescribed`; held but silent: `mis-attributed`). If the reference base holds NO text for the source at all, the verdict is `source-not-held`, not `mis-attributed`.
- **`source-not-held`**: the reference base holds no text for the named source, so no judgement is possible. The finding FIRST triggers an acquisition attempt via the project's ingest path; only a failed or constrained attempt produces an acquisition-queue entry, which then carries named options (the maintainer provides the source, the task defers and routes around it, or the claim is reworded so it no longer depends on the unheld source). The claim is NEVER adjudicated from memory, and routing to the queue without first attempting the acquisition is the foreclosed shortcut.

This procedure is a single-pass advisory audit, not a fix-to-fixed-point loop. It is to normative-value claims what [`matrix-fit.md`](matrix-fit.md) is to control-code citations: the semantic layer over gates that can only check existence.

## When to Use

- **The one-time full Tier-A pass** when the procedure is adopted (the whole Tier-A census is small by construction; every row is judged, each cited source assessed, establishing the baseline).
- **After any batch that adds or edits normative-value claims** (a substantive content batch, a jurisdiction annex, a KPI or SLA table): judge the new Tier-A rows the batch introduced and sample the batch's own Tier-B rows. This cadence is batch-scoped and does not advance the global Tier-B coverage cycle below.
- **Periodically, the Tier-B coverage sweep** (the global pass): the whole Tier-B population is too large to judge every run, so a standing cadence works through it a sample at a time until the entire census has been judged once, then restarts.
- **Ad-hoc when a claim is in doubt** (a maintainer flag, a validation-sweep note about a suspicious attribution, an apply-time uncertainty about whether a source states a value).
- **NOT as a replacement for the citation gates.** The existence, currency, and control-code gates still run on every change; this audit is the precision layer on top of them.

## Process

### 1. Establish scope and confirm the reference base

Name the scope for this run: the full Tier-A census (the adoption pass), the claims a just-applied batch introduced (the per-batch cadence), a flagged set (the ad-hoc cadence), or the next Tier-B coverage sample (the periodic sweep). Confirm the project's all-gates suite exits 0 first; a precision pass judges among claims that already pass the mechanical gates. Confirm the reference base is available: its indexes locate the held source texts, and the per-source currency rule applies (confirm a held source is current before relying on it; a superseded held text is grounds to defer, never to judge against silently). Every verdict cites the held source's own reference-base `path:line` where the passage was read this run, or, for `source-not-held`, the executed index lookup that returned nothing, both from an index lookup executed in THIS run, never a note, a prior run's record, or memory.

### 2. Build the worklist

Collect the in-scope normative-attribution claims: every sentence that ties a specific value to a named normative source (Tier A, judged exhaustively), and the soft-alignment phrasings with no specific value (Tier B, sampled). Build the list from the scope's diff or document set by searching for value shapes (numbers with units, clocks, thresholds) beside source names. An optional deeper review may supplement the public gates by extracting and tiering the worklist mechanically; treat any such output as input-narrowing, never a defect list (a lexical extractor deliberately over-collects; a spurious row costs seconds, a missed row ships a misattribution). Add any claim the maintainer or a prior QA note flagged.

### 3. Judge each claim against the held source text

For each worklisted claim, locate the named source's held text via the reference-base indexes, read the specific clause, article, or annex the claim points at, and return, FOR EACH (attributed value, named source) PAIR on the claim, one of the four verdicts with the source passage QUOTED as evidence. A claim that cites SEVERAL sources for one value is judged once PER source: the same value can draw a DIFFERENT verdict per source (the 7-year example above: `(7 years, ISO/IEC 42001)` is `informed-not-prescribed` while `(7 years, EU AI Act Annex IV)` is `mis-attributed`). The binding rules: judge against the held source text, never memory or plausibility, and an un-held source is never adjudicated from recall, whatever the reviewer's confidence. Every judgement (one row per (value, source) pair) quotes the claim's `path:line`, the attributed value, the named source, the source passage, AND the held source's own reference-base `path:line` where that passage was read in THIS run, or, for `source-not-held`, the executed index lookup that returned nothing; a verdict carrying neither is rejected.

**Tier-B sampling (the periodic coverage sweep).** In-scope Tier-A rows are judged exhaustively every run; the Tier-B population is sampled. Each sweep run samples a default N rows (10 is proportionate to a census of this corpus's size; the final run of a cycle may draw fewer), STRATIFIED by the joint (cited source family x document domain) cell so the sample spreads across families and domains, with strata rotated across runs so every stratum is reached over the cadence. A sweep run draws WITHOUT REPLACEMENT against the rows earlier sweep runs already judged: the run record carries the cycle number, the sampled rows (keyed by document path plus cited source plus a short claim-text anchor, NOT a bare line number, since edits shift lines), and a reset marker when the cycle completes. Coverage counts only ADJUDICATED rows: a drawn row whose verdict was not recorded (deferred or `source-not-held`) stays in the un-judged pool and is re-drawn, so the coverage figure reflects real adjudication, never a mere draw. One residue is disclosed at the point of use: the claim-text anchor changes under a genuine reword and needs manual reconciliation. The per-batch and ad-hoc cadences sample only their own scoped Tier-B rows and do not advance the coverage cycle.

### 4. Apply-time-verify each candidate against the source text

Re-read each candidate `mis-attributed` and `informed-not-prescribed` verdict's source passage in the reference base before treating it as a finding. A false positive (a prescribing passage missed elsewhere in the source, a version mismatch, an over-literal reading of a clause the source states in different words) is refuted here, not routed. For each confirmed finding, draft the fix per the verdict; for a multi-source claim the composite fix derives from the VECTOR of per-pair verdicts (for example prescribed-by-A plus silent-in-B: attribute the value to A alone, or split the attribution so each source carries only what it prescribes). When an attribution is rephrased, search the full touched file AND the corpus for sibling carriers of the same value-plus-source pair at bare-token width (the same pair recurs across policy families); the corpus wiring names the instrument.

### 5. Triage and route findings

Confirmed findings in the current scope are fixed in-window: apply the fix, bump the touched document's Version and Date in the same commit, and record the correction in the project's change record. Where the fix requires an authorial decision (which of value-vs-citation is wrong; whether a canonical project value should be re-anchored), surface it to the maintainer with named options rather than silently picking. Confirmed findings outside the current scope are surfaced with named options (fix-now vs route-to-backlog), not auto-deferred. Findings refuted at apply-time are recorded with the refutation, not routed; findings that dedupe against an existing backlog item are cross-referenced, not duplicated.

### 6. Record and present

Surface confirmed findings to the maintainer directly, one per (value, source) pair: the claim `path:line`, the attributed value, the named source, the verdict with the quoted source passage and its held-source reference-base `path:line` (or, for `source-not-held`, the executed index lookup that returned nothing), and the fix applied or the option surfaced. Record the run (scope, worklist size, verdicts, dispositions, and for a coverage sweep the sampling record of step 3) in the project's own working records; a zero-finding run still gets a one-line record (the proof-of-discipline). The pass terminates when the worklist is judged, the confirmed findings are routed or fixed, and the run is recorded; it is a single advisory pass, not a fix-to-fixed-point loop.

## Red Flags

- Judging a claim from the source's remembered content or general reputation instead of reading the held text. The remembered meaning is the failure mode that produced the misattribution.
- Adjudicating a `source-not-held` claim anyway "because the answer is well known". No held text, no judgement; the claim triggers an acquisition attempt FIRST, and routes to the acquisition queue only on a failed or constrained attempt.
- Recording a verdict, or a held/not-held holdings claim, from a note or a prior run's record instead of the held-source reference-base `path:line` (or, for `source-not-held`, the executed index lookup that returned nothing) cited from an index lookup executed THIS run.
- Fixing an `informed-not-prescribed` finding by changing the VALUE. The value is frequently the project's own canonical choice; the defect is the attribution phrasing, and silently changing a canonical value is an authorial decision the maintainer owns.
- Routing a candidate verdict without your own re-read of the source passage. Apply-time verification is the false-positive filter; a reviewer can miss the prescribing clause elsewhere in a long source.
- Rephrasing one carrier of a misattributed value while sibling carriers of the same value-plus-source pair survive. Search at bare-token width before claiming the class fixed.
- Running this as a substitute for the citation gates, or skipping it because "the gates passed". A well-formed citation says nothing about precision.

## Verification

The pass is complete on a given run when:

- The scope was named and the mechanical baseline was clean before the semantic read.
- Every in-scope Tier-A row was judged against the held source text, EACH (value, source) pair on a multi-source claim assessed, with the passage quoted and the held source's reference-base `path:line` cited (or the row verdicted `source-not-held` on an executed index lookup that returned nothing). For a Tier-B coverage-sweep run, the sample was drawn per the step-3 discipline and named in the run record; for a per-batch or ad-hoc run, the Tier-B rows sampled within that scope were named.
- Every verdict cited the held source's own reference-base `path:line` from an index lookup executed in THIS run (a `source-not-held` verdict cited the executed index lookup that returned nothing), and any currency claim was validated upstream this run rather than inferred from the index.
- Each candidate finding's source passage was re-read and refuted or confirmed; refutations were recorded, not routed.
- Confirmed in-scope findings were fixed per their verdict class (Version and Date bumped, change record written) or surfaced with named options where the fix is authorial; `source-not-held` claims triggered an acquisition attempt first and were queued only on a failed or constrained attempt.
- Any in-scope row not judged (deferred, routed, or `source-not-held`) was NAMED with its blocker in the record; none was silently dropped.
- The run was recorded and findings were presented to the maintainer.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The citation gates pass, so the claim is fine." | The gates check the source exists and the citation is well-formed, not that the source states the attributed value. Only a read of the clause decides. |
| "Everyone knows GDPR Article 33 says 72 hours." | Article 33(1) does; the flagged carrier among the illustrative shapes cites 33(2), which says "without undue delay". The clause read, not the reputation, is the evidence. |
| "The source is not held, but I am confident what it says." | An un-held source is never adjudicated from memory. Attempt acquisition FIRST; route to the acquisition queue only on a failed or constrained attempt. |
| "The reference base held this last run, or a note says it is held." | Holdings is determined by an index lookup executed THIS run, cited by the held-source reference-base `path:line` (or the failed index lookup for a `source-not-held` call); a note or a prior run's record is not a holdings authority. |
| "The source does not state the value, so the value is wrong." | Often the value is the project's own canonical choice the source merely informs. The fix is the attribution phrasing; changing the value is the maintainer's call. |
| "Claim precision should just be a gate." | It is not mechanically checkable, and the ground truth lives in a held reference base an ordinary mechanical gate cannot see. The cadenced audit is the durable instrument. |

## See Also

- Related procedure [`matrix-fit.md`](matrix-fit.md): the sibling semantic audit for control-code fit; the judge-against-the-source rule comes from it.
- Related procedure [`validation-sweep.md`](validation-sweep.md): the corpus-wide drift sweep whose notes can flag an attribution doubt for this audit to adjudicate.
- Related procedure [`publication-screening.md`](publication-screening.md): the admission-control screen for configured untrusted sources; once a screened source's claim enters project content, its precision is this audit's cadence to adjudicate like any other attributed value.
- The canonical gate inventory: [`specification-audit-programme.md`](../specs/specification-audit-programme.md).
