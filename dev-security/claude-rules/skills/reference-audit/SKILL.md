---
name: reference-audit
description: Cadenced reference-breadth audit between the corpus and the held reference base, in both directions. Catches the gate-blind SP 800-154 class, "held but unused": an authoritative source sits in the reference base while corpus documents that its content would materially improve never engage it, and, in the reverse direction, a corpus document is touched while newly ingested or updated reference material that bears on it goes unnoticed. Run it exhaustively (the FULL mode, a deep-assessment member and a standing cadence), per touched corpus document (the per-touch mode, delta-filtered against a per-document state file), and per reference ingest (the new-ingest mode). It dispatches a semantic judge over the recall-oriented worklist that `tools/audit-reference-breadth.py` produces, adjudicating each candidate pairing against the held source text and the corpus document, then routes confirmed improvements under the normal triage. It catches what the citation gates structurally cannot: breadth needs a judgement about what a document SHOULD engage, not a check of what it already cites.
derives_from: ../../governance/evidence-grounded-completion.md
---

# Reference Audit (reference-breadth audit of corpus against the held reference base)

## Overview

The citation gates guard what the corpus already cites: existence, well-formedness,
currency, and (through `/matrix-fit` and `/claim-fit`) semantic fit and precision. None
of them asks the breadth question that decides whether the corpus is making full use of
what the project actually holds: is there a held authoritative source whose content
would materially improve a corpus document that never engages it? The reverse blindness
is the same class: a corpus document gets touched, and nothing checks whether the
reference base has gained or updated material that bears on it since the document was
last assessed. Both directions are gate-blind by construction, because a gate can only
inspect citations that exist; breadth is a judgement about citations and content that
do not exist yet.

The class is not hypothetical. The motivating incident (maintainer-directed 2026-07-07):
NIST SP 800-154's guidance was relevant to held corpus content while the corpus did not
engage it, and nothing in the audit programme could have said so. The reference base is
a curated, licensed asset; a held source no document uses is shelf inventory, and a
corpus document that ignores a held source it should engage is thinner than the project
can afford it to be.

`reference-audit` is the semantic-judge half of a two-part instrument whose
recall-oriented triage half is the advisory tool `tools/audit-reference-breadth.py`
(explicitly NOT a gate; always exits 0; CI cannot host the check because the ground
truth lives in the sibling private reference repo). The tool classifies every in-scope
reference item by corpus usage (WELL-CITED / THIN / UNCITED / NO-KEY) and produces, per
corpus document, a topic-ranked candidate list of held items the document does not
cite. The skill judges: for each worklisted pairing, it reads the held source's text
and the corpus document and decides whether an engagement would materially improve the
document. The binding rule mirrors the matrix-fit and claim-fit lesson: judge against
the held source TEXT and the document's own content, never a remembered meaning of
either.

Trust tiers are load-bearing (maintainer decisions, 2026-07-08). The standards,
frameworks, legislation, and programs buckets are AUTHORITATIVE: a confirmed finding
supports a citation-grade improvement. The templates bucket is TEMPLATE-tier: a
confirmed finding supports a template-content improvement (the corpus template or
policy adopting structure or coverage from the held template), never a normative
citation. The books bucket is RECOMMENDATION-tier only, never authoritative: a
book-sourced suggestion must be corroborated against a trusted source before anything
normative rests on it, and a book is engaged by topic rather than cited by identifier.
The publications bucket is EXCLUDED by default (screen-first tier; the
`publication-screening` process (`/screen-publications`) now exists, so its inclusion
awaits the screening wave that flips `pending` register rows to `screened` plus the
maintainer's inclusion decision).

The verdict vocabulary is four-valued, because the right action differs by verdict:

- **`adopt-citation`**: the held authoritative source materially bears on the document;
  the improvement is engagement with a citation (a framework-alignment row, a normative
  anchor, a cross-reference). Authoritative tier only.
- **`adopt-content`**: the held item's content or structure would improve the document
  without a normative citation (the template tier's natural verdict; also authoritative
  sources whose value to the document is structural).
- **`recommend`**: a book-tier candidate whose engagement is worth surfacing; the
  suggestion carries the corroboration obligation and is never itself an authority.
- **`no-fit`**: the topic match is spurious; the pairing is dropped with a one-line
  reason (the tool over-collects by design, so most candidates on a well-referenced
  document will be `no-fit`).

This skill is a single-pass advisory audit, not a fix-to-fixed-point loop and not a
trust-recovery escalation. It runs on its cadences, surfaces confirmed improvement
candidates, and routes or applies them under the normal in-window / out-of-window
triage. It is to reference breadth what `/matrix-fit` is to control-code fit and
`/claim-fit` is to claim precision: the semantic layer over gates that can only check
what already exists.

## When to Use

- **FULL mode on the standing cadence**: as a member of every `/deep-assessment` run,
  and ad-hoc when the maintainer wants the exhaustive both-directions picture. Every
  in-scope reference item is classified and every corpus document gets a candidate
  list.
- **Per-touch mode on every substantive corpus-document PR**: when a PR touches a
  corpus document's body, run the tool in `--docs` mode for the touched documents. The
  per-document state file makes the steady-state cost near zero: with no reference-base
  change since the document's last audit, the candidate set is empty and no judge is
  dispatched. The judge fires only on a non-empty candidate set.
- **New-ingest mode after reference-base changes**: when the reference base ingests or
  updates items, run `--ref-since <sha>` (or `--ref-items <substring>`) to list the
  corpus documents each changed item topically matches and does not cite, and judge
  those pairings.
- **NOT as a replacement for the citation gates or the sibling semantic audits.** The
  existence, currency, and fit layers still run on their own cadences; this skill is
  the breadth layer beside them. A confirmed `adopt-citation` finding lands as a
  normal corpus change that passes all of those gates.

## Process

### 1. Establish scope, mode, and the reference baseline

Name the mode for this run (FULL, per-touch with the touched document list, or
new-ingest with the reference delta) and confirm `tools/run_all_audits.sh` exits 0
first; a breadth pass proposes additions to a corpus that already passes its gates.
Confirm the reference base is available and locate it via its indexes
(`grc_library_ref/INDEX.md`, `grc_library_ref/catalogue.yml`,
`grc_library_ref/SECTION-INDEX.md`, `grc_library_ref/COVERAGE-MAP.md`); the per-source
currency rule applies to any source a finding will rest on (confirm the held source is
current upstream this turn before recommending engagement with it; a superseded held
text is grounds to route a version-update item, never to recommend silently).

### 2. Run the advisory triage tool to generate the worklist

Run `python3 tools/audit-reference-breadth.py --ref-base
<path-to-grc_library_ref-checkout>` in the mode's form: bare for FULL; `--docs <path>
[<path> ...]` for per-touch; `--ref-since <sha>` or `--ref-items <substring>` for
new-ingest. The tool always exits 0; its output is a recall-oriented worklist (per-item
usage classification plus topic-ranked candidate pairings), never a defect list: the
lexical matcher deliberately over-collects, and a listed pairing is a candidate to
judge, not a finding. NO-KEY rows on non-book items are alias-curation work for
`tools/reference-breadth-aliases.json` (fix the alias in the same run); NO-KEY on books
is expected. In per-touch mode, an empty candidate set for every touched document ends
the run at this step with a one-line note in the PR's QA trail; no judge is dispatched
on an empty set.

### 3. Dispatch the reference-breadth judge over the worklist

Dispatch one or more subagents (or perform the read directly for a small worklist) to
judge each candidate pairing. The judge brief: read the corpus document in full, locate
the held item's text via the reference-base indexes and read the relevant sections, and
return one of the four verdicts (`adopt-citation` / `adopt-content` / `recommend` /
`no-fit`) with the CONCRETE improvement named (which section of the document, engaging
which part of the source, to what effect) and the source passage or structure QUOTED or
pinpointed as evidence. The binding rules: judge against the held text and the live
document, never memory, a title, or topic labels alone (a title-inferred verdict is the
dominant judge failure mode); respect the tier ceiling (a book can never yield
`adopt-citation`; a template yields `adopt-content`); and a verdict without named
evidence is a hypothesis, not a finding. In FULL mode, additionally judge the per-item
classifications: an UNCITED or THIN authoritative item gets an explicit disposition
(genuine gap worth routing, or legitimately out of corpus scope with a one-line
reason).

### 4. Synthesize and apply-time-verify each candidate

The orchestrator re-reads each `adopt-citation`, `adopt-content`, and `recommend`
verdict's evidence (the cited source passage in the reference base and the named
document section) before treating it as a finding; the judge produces research, the
orchestrator confirms. A judge false positive (the document already engages the source
under different phrasing; the source passage does not say what the verdict claims; the
improvement is already covered by a sibling document the judge did not read) is refuted
here, not routed. For each confirmed finding, draft the improvement per its verdict and
tier: a citation-grade engagement for `adopt-citation`, a content or structure adoption
for `adopt-content`, and a corroboration-gated suggestion for `recommend` (name the
trusted source that would corroborate it, or route the corroboration as part of the
item).

### 5. Triage and route findings

Small confirmed improvements in the current scope are fixed in-window (apply the
change, bump the touched document's Version and Date in the same commit, record the
correction in the CHANGELOG-detailed entry). Substantive improvements (a new
framework-alignment row set, a section rewrite, a multi-document engagement) are routed
to TODO with the evidence attached, surfaced to the maintainer with named options
rather than silently scheduled. FULL-mode structural outcomes route durably: confirmed
under-used authoritative items to a TODO improvement item; confirmed out-of-scope items
recorded in the run record so the next run does not re-adjudicate them. Findings
refuted at apply-time are recorded with the refutation, not routed; findings that
dedupe against an existing backlog item are cross-referenced, not duplicated.

### 6. Update the per-document state

In per-touch mode, after the touched documents' candidate sets are adjudicated (or
found empty), run the tool again with `--docs <touched paths> --update-state` so the
state file (`.working/reference-audit/doc-state.md`) records the reference-base HEAD
each document was audited against, and commit the state refresh with the PR's QA batch.
In FULL mode, refresh the state for every corpus document the run adjudicated. The
state file is the delta anchor that keeps the per-touch cadence near-free at steady
state; a document with no state row is treated as never audited and gets the full
candidate set on its next touch.

### 7. Record and surface

Surface confirmed findings inline in chat (per-finding: document path, the held item
and its tier, the verdict, the concrete improvement, and the action taken or option
surfaced). Write the run to `.working/reference-audit/` as a dated per-run record file
(`YYYY-MM-DD-<scope>.md`, swept to the scratch archive under the current-week model)
and append a row to the non-dated `history.md`; a zero-finding or empty-candidate run
still gets a history row (the proof-of-discipline), with no detail file. The pass
terminates when the worklist is adjudicated, confirmed findings are applied or routed,
the state is updated for the run's scope, and the run is recorded; it is a single
advisory pass, not a fix-to-fixed-point loop.

## Red Flags

- Judging a pairing from the reference item's title or topic labels instead of reading
  the held text and the document. A title-inferred verdict is the dominant judge
  failure mode (the high-assurance-verification negatives lesson).
- Letting a book-tier candidate produce a normative citation, or letting any
  recommendation-tier suggestion ship without its corroboration obligation named. The
  tier ceiling is a maintainer decision, not a heuristic.
- Treating the triage tool's worklist as a defect list. It is recall-oriented; on a
  well-referenced document most candidates will judge `no-fit`, and that is the tool
  working as designed, not wasted effort.
- Dispatching a judge on an empty per-touch candidate set, or padding an empty run into
  a report. The empty set IS the steady-state result; record the one-line note and end.
- Routing a judge verdict without the orchestrator's own re-read of the evidence.
  Apply-time verification is the false-positive filter; a judge can miss that the
  document already engages the source under different phrasing.
- Skipping the `--update-state` refresh after a per-touch adjudication. A stale state
  row re-inflates the next touch's candidate set and erodes the near-free steady state
  the delta design exists to provide.
- Recommending engagement with a held source without confirming it is current upstream
  this turn. A superseded held text routes a version-update item first (the
  reference-version-currency SOP), and the breadth finding waits on the current text.
- Running this as a substitute for `/matrix-fit`, `/claim-fit`, or the citation gates.
  Breadth, fit, precision, and existence are four different questions; this skill only
  answers breadth.

## Verification

The pass is complete on a given run when:

- The mode and scope were named and the mechanical baseline was clean
  (`tools/run_all_audits.sh` exit 0) before the semantic read.
- The triage tool was run in the mode's form and its worklist (plus anything the
  maintainer flagged) was the judge's input; non-book NO-KEY rows were resolved by
  alias curation or explicitly deferred.
- Every judged pairing carries a verdict with named evidence (source passage or
  structure, document section); in FULL mode, every UNCITED and THIN authoritative item
  carries an explicit disposition.
- The orchestrator re-read each candidate finding's evidence and refuted or confirmed
  it; refutations are recorded, not routed.
- Confirmed in-scope findings were applied (Version and Date bumped, CHANGELOG entry
  written) or routed to TODO with named options where substantive or authorial; tier
  ceilings were respected end to end.
- The per-document state was refreshed for the run's scope and committed with the
  run's PR batch.
- The run was recorded (history row always; dated detail file when findings exist) and
  findings were surfaced inline in chat.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The citation gates pass, so the document's referencing is fine." | The gates check what the document already cites. Breadth asks what it should engage and does not; no gate can answer that. |
| "The topic matches, so the source belongs in the document." | Topic overlap is the tool's recall heuristic, not a finding. Only a read of the held text against the document decides; most matches are `no-fit`. |
| "The book says exactly what the document needs, so cite it." | Books are recommendation-tier by maintainer decision: never authoritative, never cited as a normative anchor. Corroborate against a trusted source first, or the suggestion waits. |
| "The per-touch run found nothing, so running it was waste." | The empty set at steady state is the design working: it certifies the document was checked against the current reference base at near-zero cost, and the state row proves it. |
| "The item is held, so the corpus must use it somewhere." | Some held items are legitimately out of corpus scope. The FULL-mode disposition records that judgement once, with a reason, instead of re-litigating it every run. |
| "The state file is bookkeeping; skip the refresh this once." | The state row is the delta anchor. One skipped refresh silently re-inflates the next run's worklist and hides which reference changes the document was actually assessed against. |

## See Also

- Canonical rule [`evidence-grounded-completion`](../../governance/evidence-grounded-completion.md):
  the assertion-side discipline this skill applies to breadth judgements (a claim that a
  source would improve a document requires reading both, not inferring from a title),
  including the external-version-currency corollary that gates any engagement
  recommendation on an upstream-confirmed current source.
- Related skill [`matrix-fit`](../matrix-fit/SKILL.md) (`/matrix-fit`): the sibling
  semantic audit for control-code fit; the advisory-tool-plus-cadenced-judge pattern and
  the judge-against-the-source rule both come from it.
- Related skill [`claim-fit`](../claim-fit/SKILL.md) (`/claim-fit`): the sibling
  precision audit for normative-attribution claims; a breadth finding that adds a
  normative value to a document hands the new claim to claim-fit's cadence.
- Related skill [`deep-assessment`](../deep-assessment/SKILL.md) (`/deep-assessment`):
  the periodic whole-project assessment whose semantic-instruments phase invokes this
  skill in FULL mode.
- Related skill [`publication-screening`](../publication-screening/SKILL.md)
  (`/screen-publications`): the admission-control screen that gates this skill's
  publications tier; a publication is a candidate here only once its screening register
  row is `screened` (recommendation tier, never authoritative), and `pending` /
  `quarantined` items are never candidates.
- The advisory tool [`tools/audit-reference-breadth.py`](../../../../tools/audit-reference-breadth.py):
  the recall-oriented triage step that feeds this skill's worklist (not a gate; always
  exits 0; `--docs` for per-touch with `--update-state` for the delta anchor,
  `--ref-since` / `--ref-items` for new-ingest, `--include-publications` only under an
  explicit screening decision), with its curated alias map
  [`tools/reference-breadth-aliases.json`](../../../../tools/reference-breadth-aliases.json).
- The advisory tool [`tools/audit-reference-acquisition-gaps.py`](../../../../tools/audit-reference-acquisition-gaps.py):
  the complementary cited-but-not-held direction to this skill's breadth judgement. Where
  this skill and `audit-reference-breadth.py` ask whether the corpus USES what the base
  holds, the acquisition tool asks whether the corpus CITES a source the base does NOT
  hold (an acquisition candidate for the ref-base acquisition queue and the maintainer
  source-drop list), diffing the corpus canonical-citations register against the ref
  catalogue. Also advisory, never a gate; always exits 0.
- The reference base: the `grc_library_ref` repo located via its indexes, with the
  per-source currency confirmation, the superseded-archival workflow, and the
  trust-bucket rules the `grc_library_ref` repo's own conventions define.
