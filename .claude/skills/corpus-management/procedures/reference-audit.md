---
name: reference-audit
description: Cadenced reference-breadth audit between a project's content collection and its configured source store, in both directions. Catches the gate-blind "held but unused" class, an authoritative source that is held while project documents it could materially improve never engage it, and the reverse, a project document touched while newly ingested or updated source material that bears on it goes unnoticed. Run it exhaustively, per touched project document, and per source ingest according to configured modes. A reviewer adjudicates each candidate pairing against held source text and project content. It catches what citation gates structurally cannot, because breadth needs a judgement about what a document SHOULD engage.
---

# Reference Audit (reference-breadth audit of project content against configured source material)

## Corpus wiring (this repository's instantiation; adopters substitute their own)

Portable procedure, concrete names. In this repository the procedure runs with:

- Reference base: the adopting project's reference base of held source texts, located via its own indexes (an index file, a catalogue, a section index, a coverage map).
- Acquisition bibliography: [`reference-acquisition-manifest.md`](../registers/reference-acquisition-manifest.md), the public bibliography of the sources this corpus engages, from which an adopter can build its own reference base.
- Trust-tier assignments (the maintainer sets them): standards, frameworks, legislation, and programs are authoritative; templates are template-tier; books are recommendation-tier; publications are screen-first, excluded until screened (see [`publication-screening.md`](publication-screening.md)).
- Mechanical baseline: [`run_all_audits.sh`](../tools/run_all_audits.sh).
- Worklist narrowing and per-document state: an optional deeper review may supplement the public gates by classifying item usage and pairing candidates mechanically; without one, candidates are collected by topic search, and the per-document audit state is kept in the project's own working records.

An adopting project maps each bullet to its own reference stores and records; the procedure below refers to them generically.

## Overview

The citation gates guard what project content already cites: existence, well-formedness, currency, and (through the fit and precision audits) semantics. None of them asks the breadth question: is there a held authoritative source whose content would materially improve a project document that never engages it? The reverse blindness is the same class: a project document gets touched, and nothing checks whether the source store has gained or updated material that bears on it since the document was last assessed. Both directions are gate-blind by construction, because a gate can only inspect citations that exist; breadth is a judgement about citations and content that do not exist yet.

The class occurred in the earlier repository: an authoritative source's guidance bore on content that repository already maintained, while no document there engaged it, and nothing in its audit programme could have said so. In that case the relevant source also proved to be unavailable rather than merely held-but-unused, so the finding was an acquisition gap, not only an engagement gap; the audit surfaces both the held-but-unused direction and the relevant-but-not-held direction.

Trust tiers are load-bearing, and the project's tier assignments bind this procedure. An authoritative-tier finding supports a citation-grade improvement. A template-tier finding supports a content improvement, never a normative citation. A recommendation-tier finding is never authoritative: the suggestion must be corroborated against a trusted source before anything normative rests on it. A screen-first tier is EXCLUDED by default: an item becomes a candidate only after the screening register row flips to `screened`, plus the maintainer's inclusion decision.

The verdict vocabulary is four-valued, because the right action differs by verdict:

- **`adopt-citation`**: the held authoritative source materially bears on the document; the improvement is engagement with a citation. Authoritative tier only.
- **`adopt-content`**: the held item's content or structure would improve the document without a normative citation (the template tier's natural verdict).
- **`recommend`**: a recommendation-tier candidate whose engagement is worth surfacing; the suggestion carries the corroboration obligation and is never itself an authority.
- **`no-fit`**: the topic match is spurious; the pairing is dropped with a one-line reason (candidate collection over-collects by design, so most candidates on a well-referenced document will be `no-fit`).

This procedure is a single-pass advisory audit, not a fix-to-fixed-point loop.

## When to Use

- **FULL mode on a standing cadence**, and ad-hoc when the maintainer wants the exhaustive both-directions picture. Every in-scope source item is classified; every candidate pairing is judged.
- **Per-touch mode on every substantive project-document change**: collect candidates for the touched documents only. The per-document audit state makes the steady-state cost near zero: with no source-store change since the document's last audit, the candidate set is empty and no review is needed.
- **New-ingest mode after source-store changes**: when the source store ingests or updates items, list the project documents each changed item topically matches and does not cite, and judge those pairings.
- **NOT as a replacement for the citation gates or the sibling semantic audits.** Existence, currency, fit, and precision run on their own cadences; this is the breadth layer beside them. A confirmed `adopt-citation` finding lands as a normal content change that passes all of those gates.

## Process

### 1. Establish scope, mode, and the reference baseline

Name the mode and scope for this run and confirm the project's full audit suite exits 0 first; a breadth pass proposes additions to content that already passes its gates. Confirm the source store is available and locate held items through its indexes; apply the per-source currency rule to any source a finding will rest on (confirm current upstream this run before recommending engagement; a superseded held text routes a version-update item first).

### 2. Build the candidate worklist

Collect candidate (source item, project document) pairings for the scope: whole-collection for FULL, touched documents for per-touch, the source delta for new-ingest. Pair by topic: the source's subject terms against each document's subject and section headings. An optional deeper review may supplement the public gates by classifying per-item usage (well-cited / thin / uncited / unmatched) and ranking candidate pairings mechanically; treat any such output as a recall-oriented worklist, never a defect list. An empty per-touch candidate set ends the run with a one-line record and no review.

### 3. Judge each candidate pairing

For each candidate pairing, read the project document in full, locate the held item's text via the source store's indexes and read the relevant sections, and return one of the four verdicts with the CONCRETE improvement named (which section of the document, engaging which part of the source, to what effect) and the source passage or structure QUOTED or pinpointed as evidence. The binding rules: judge against the held text and the live document, never memory, a title, or topic labels alone (a title-inferred verdict is the dominant failure mode); respect the trust-tier ceiling (a recommendation-tier item can never yield `adopt-citation`; a template yields `adopt-content`); a verdict without named evidence is a hypothesis, not a finding. In FULL mode, additionally give every uncited or thinly-cited authoritative item an explicit disposition: a genuine gap worth routing, or legitimately outside project-content scope with a one-line reason.

### 4. Apply-time-verify each candidate

Re-read each `adopt-citation`, `adopt-content`, and `recommend` verdict's evidence (the cited source passage and the named document section) before treating it as a finding. A false positive (the document already engages the source under different phrasing; the passage does not say what the verdict claims; a sibling document already covers it) is refuted here, not routed. For each confirmed finding, draft the improvement per its verdict and tier: a citation-grade engagement for `adopt-citation`, a content or structure adoption for `adopt-content`, and a corroboration-gated suggestion for `recommend` (name the trusted source that would corroborate it, or route the corroboration as part of the item).

### 5. Triage and route findings

Small confirmed improvements in the current scope are fixed in-window: apply the change, bump the touched document's Version and Date in the same commit, and record it in the project's change record. Substantive improvements (a framework-alignment row set, a section rewrite, a multi-document engagement) are routed to the project's backlog with the evidence attached and surfaced to the maintainer with named options, never silently scheduled. FULL-mode structural outcomes route durably: under-used authoritative items to the backlog; confirmed out-of-scope items recorded in the run record so the next run does not re-adjudicate them. Refutations are recorded, not routed; duplicates are cross-referenced against the existing backlog, not re-added.

### 6. Update the per-document audit state

After adjudication (or an empty candidate set), record for each audited document the source-store revision it was audited against, in the project's own working records, and commit that record with the change's QA batch. The state record is the delta anchor that keeps the per-touch cadence near-free at steady state; a document with no state record is treated as never audited and gets the full candidate set on its next touch. Keep the state record accurate: where a refresh fails or is interrupted, repair or rebuild the affected rows from the runs actually performed before relying on it again.

### 7. Record and present

Surface confirmed findings to the maintainer directly (per finding: document path, the held item and its tier, the verdict, the concrete improvement, and the action taken or option surfaced). Record the run (mode, scope, worklist, verdicts, dispositions, state refresh) in the project's own working records; a zero-finding or empty-candidate run still gets a one-line record (the proof-of-discipline). The pass terminates when the worklist is adjudicated, confirmed findings are applied or routed, the state is updated for the run's scope, and the run is recorded; it is a single advisory pass, not a fix-to-fixed-point loop.

## Red Flags

- Judging a pairing from the source item's title or topic labels instead of reading the held text and the document. A title-inferred verdict is the dominant failure mode.
- Letting a recommendation-tier candidate produce a normative citation, or letting any recommendation-tier suggestion ship without its corroboration obligation named. The maintainer sets the tier ceiling; it is not a heuristic.
- Treating the candidate worklist as a defect list. It is recall-oriented; on a well-referenced document most candidates will judge `no-fit`, and that is the design working, not wasted effort.
- Reviewing an empty per-touch candidate set, or padding an empty run into a report. The empty set IS the steady-state result; record the one-line note and end.
- Routing a verdict without your own re-read of the evidence. Apply-time verification is the false-positive filter; a reviewer can miss that the document already engages the source under different phrasing.
- Skipping the state-refresh step after a per-touch adjudication. A stale state record re-inflates the next touch's candidate set and erodes the near-free steady state.
- Recommending engagement with a held source without confirming it is current upstream this run. A superseded held text routes a version-update item first.
- Running this as a substitute for the fit audit, the precision audit, or the citation gates. Breadth, fit, precision, and existence are four different questions; this procedure only answers breadth.

## Verification

The pass is complete on a given run when:

- The mode and scope were named and the mechanical baseline was clean before the semantic read.
- The candidate worklist was built for the mode's scope (plus anything the maintainer flagged) and was the review's input.
- Every judged pairing carries a verdict with named evidence (source passage or structure, document section); in FULL mode, every uncited and thinly-cited authoritative item carries an explicit disposition.
- Each candidate finding's evidence was re-read and refuted or confirmed; refutations were recorded, not routed.
- Confirmed in-scope findings were applied (Version and Date bumped, change record written) or routed with named options where substantive or authorial; tier ceilings were respected end to end.
- The per-document audit state was refreshed for the run's scope and committed with the run's change batch.
- The run was recorded and findings were presented to the maintainer.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The citation gates pass, so the document's referencing is fine." | The gates check what the document already cites. Breadth asks what it should engage and does not; no gate can answer that. |
| "The topic matches, so the source belongs in the document." | Topic overlap is a recall heuristic, not a finding. Only a read of the held text against the document decides; most matches are `no-fit`. |
| "The book says exactly what the document needs, so cite it." | Books are recommendation-tier, a tier the maintainer sets: never authoritative, never cited as a normative anchor. Corroborate against a trusted source first, or the suggestion waits. |
| "The per-touch run found nothing, so running it was waste." | The empty set at steady state is the design working: it certifies the document was checked against the current reference base at near-zero cost, and the state record proves it. |
| "The item is held, so the project must use it somewhere." | Some held items are legitimately outside project-content scope. The FULL-mode disposition records that judgement once, with a reason, instead of re-litigating it every run. |
| "The state record is bookkeeping; skip the refresh this once." | The state record is the delta anchor. One skipped refresh silently re-inflates the next run's worklist and hides which source changes the document was actually assessed against. |

## See Also

- Related procedure [`matrix-fit.md`](matrix-fit.md): the sibling semantic audit for control-code fit; the judge-against-the-source rule comes from it.
- Related procedure [`claim-fit.md`](claim-fit.md): the sibling precision audit for normative-attribution claims; a breadth finding that adds a normative value to a document hands the new claim to that cadence.
- Related procedure [`publication-screening.md`](publication-screening.md): the admission-control screen that gates this procedure's publications tier; a publication is a candidate here only once its screening register row is `screened` (recommendation tier, never authoritative), and `pending` / `quarantined` items are never candidates.
- The acquisition bibliography [`reference-acquisition-manifest.md`](../registers/reference-acquisition-manifest.md): the public record of the sources this corpus engages, usable to build a reference base.
- The canonical gate inventory: [`specification-audit-programme.md`](../specs/specification-audit-programme.md).
