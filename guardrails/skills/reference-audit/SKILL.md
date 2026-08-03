---
name: reference-audit
description: Cadenced reference-breadth audit between a project's content collection and its configured source store, in both directions. Catches the gate-blind "held but unused" class: an authoritative source is held while project documents it could materially improve never engage it, or a project document is touched while newly ingested or updated source material that bears on it goes unnoticed. Run it exhaustively, per touched project document, and per source ingest according to configured modes. It dispatches a semantic judge over the configured worklist, adjudicating each pairing against held source text and project content. It catches what citation gates structurally cannot: breadth needs a judgement about what a document SHOULD engage.
derives_from: ../../governance/evidence-grounded-completion.md
---

# Reference Audit (reference-breadth audit of project content against configured source material)

## Project wiring (the parent library's instantiation; adopters substitute their own)

Portable procedure, concrete names. In the parent GRC library this skill runs with:

- Worklist tool (the recall-oriented triage half): `tools/audit-reference-breadth.py`
  (advisory, always exits 0, explicitly not a gate; every mode passes `--ref-base
  <path-to-the-reference-base-checkout>`; bare beyond that for FULL mode, `--docs <path>
  [<path> ...]` for per-touch with `--update-state` for the state refresh, `--ref-since
  <sha>` / `--ref-items <substring>` for new-ingest, `--include-publications` only under
  an explicit screening decision), with its curated alias map
  `tools/reference-breadth-aliases.json`.
- Complementary acquisition-gap tool (the cited-but-not-held direction):
  `tools/audit-reference-acquisition-gaps.py` (also advisory, never a gate, always
  exits 0).
- Per-document state file (the per-touch delta anchor): the per-document reference-audit state file in the consuming project's working state.
- Run-record directory: the reference-audit run-record directory in the consuming project's working state (dated per-run detail files plus the
  non-dated `history.md`; completed records are swept to the worker-exchange scratch
  archive under the parent's current-week retention model).
- Reference base: the sibling private `grc_library_ref` repository, located via its
  indexes (`INDEX.md`, `catalogue.yml`, `SECTION-INDEX.md`, `COVERAGE-MAP.md`).
- Trust-tier assignments: the standards, frameworks, legislation, and programs buckets
  are authoritative; the templates bucket is template-tier; the books bucket is
  recommendation-tier; the publications bucket is excluded pending screening.

An adopting project maps each bullet to its own tools and reference stores; the
procedure below refers to them generically.

## Overview

The citation gates guard what project content already cites: existence,
well-formedness, currency, and (through `/matrix-fit` and `/claim-fit`) semantic fit and
precision. None of them asks the breadth question that decides whether the project is
making full use of what it actually holds: is there a held authoritative source whose
content would materially improve a project document that never engages it? The reverse
blindness is the same class: a project document gets touched, and nothing checks whether
the source store has gained or updated material that bears on it since the document was
last assessed. Both directions are gate-blind by construction, because a gate can only
inspect citations that exist; breadth is a judgement about citations and content that
do not exist yet.

The class is not hypothetical. The motivating incident in the parent library: an
authoritative source's guidance bore on corpus content the project already
maintained, while no corpus document engaged it, and nothing in the audit programme
could have said so. The lesson had a second edge: the relevant source turned out to be
UNAVAILABLE (never finalized, or not otherwise acquirable) rather than merely held-but-unused,
so the finding was an acquisition gap, not only an engagement gap: the audit surfaces both the
held-but-unused direction and the relevant-but-not-held direction. The reference base is
a curated, licensed asset; a held source no document uses is shelf inventory, and a
corpus document that ignores a held source it should engage is thinner than the project
can afford it to be.

`reference-audit` is the semantic-judge half of a two-part instrument whose
recall-oriented triage half is the advisory worklist tool named in the project wiring.
Ground truth lives in the configured source store, which may be separate from or contained
within the project repository. The worklist tool produces its configured usage
classifications and candidate source/document pairings; in the parent GRC library those
labels are WELL-CITED, THIN, UNCITED, and NO-KEY. The judge reads the held source text and
project document before deciding whether engagement would materially improve it.

Trust tiers are load-bearing maintainer decisions, and the project's tier assignments
bind this skill. An authoritative-tier finding supports a citation-grade improvement. A
template-tier finding supports a template-content improvement (a project template or
policy adopting structure or coverage from the held template), never a normative
citation. A recommendation-tier finding is never authoritative: the suggestion must be
corroborated against a trusted source before anything normative rests on it, and the
item is engaged by topic rather than cited by identifier. A screen-first tier is EXCLUDED
by default: an item becomes a candidate only after the screening process flips its
screening-register row to `screened`, plus the maintainer's inclusion decision. The
parent GRC library's assignments are the ones named in the project wiring: standards,
frameworks, legislation, and programs are authoritative, templates are template-tier,
books are recommendation-tier, and publications are screen-first, admitted only through
the `publication-screening` process (`/screen-publications`).

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
  in-scope source item is classified and every in-scope project document gets a
  candidate list.
- **Per-touch mode on every substantive project-document change**: when a change touches
  a project document's body, run the triage tool in its per-touch form for the touched
  documents. The per-document state file makes the steady-state cost near zero: with no
  source-store change since the document's last audit, the candidate set is empty and
  no judge is dispatched. The judge fires only on a non-empty candidate set.
- **New-ingest mode after source-store changes**: when the source store ingests or
  updates items, run the triage tool in its new-ingest form (scoped to the source
  delta) to list the project documents each changed item topically matches and does not
  cite, and judge those pairings.
- **NOT as a replacement for the citation gates or the sibling semantic audits.** The
  existence, currency, and fit layers still run on their own cadences; this skill is
  the breadth layer beside them. A confirmed `adopt-citation` finding lands as a
  normal project-content change that passes all of those gates.

## Process

### 1. Establish scope, mode, and the reference baseline

Name the configured mode and scope for this run and confirm that the project's full audit
suite exits 0 first; a breadth pass proposes additions to project content that already
passes its configured gates. Confirm that the configured source store is available and
locate held items through its index; apply the per-source currency rule to any source a
finding will rest on.

### 2. Run the advisory triage tool to generate the worklist

Run the triage tool named in the project wiring against the configured source store in
the selected mode: whole-collection for FULL, touched documents for per-touch, or the
source delta for new-ingest. Treat its output as a recall-oriented worklist, never a
defect list. Resolve tool-specific unmapped identifiers according to the configured alias
and trust-tier rules. In the parent GRC library, non-book NO-KEY rows require alias
curation while book NO-KEY rows are expected. An empty per-touch candidate set ends the
run with a one-line QA note and no judge dispatch.

### 3. Dispatch the reference-breadth judge over the worklist

Dispatch one or more subagents (or perform the read directly for a small worklist) to
judge each candidate pairing. The judge brief: read the project document in full, locate
the held item's text via the source store's indexes and read the relevant sections, and
return one of the four verdicts (`adopt-citation` / `adopt-content` / `recommend` /
`no-fit`) with the CONCRETE improvement named (which section of the document, engaging
which part of the source, to what effect) and the source passage or structure QUOTED or
pinpointed as evidence. The binding rules: judge against the held text and the live
document, never memory, a title, or topic labels alone (a title-inferred verdict is the
dominant judge failure mode); respect the trust-tier ceiling the project assigns (in the
parent GRC library, a book can never yield `adopt-citation`, and a template yields
`adopt-content`); and a verdict without named evidence is a hypothesis, not a finding.
In FULL mode, additionally judge the per-item classifications: an UNCITED or THIN
authoritative item gets an explicit disposition (genuine gap worth routing, or
legitimately outside project-content scope with a one-line reason).

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

Small confirmed improvements in the current scope are fixed in-window: apply the
change, bump the touched document's Version and Date in the same commit, and record the
correction in the project's detailed change log (the `CHANGELOG-detailed` entry in the
parent GRC library). Substantive improvements (a new framework-alignment row set, a
section rewrite, a multi-document engagement) are routed to the project's TODO backlog
with the evidence attached, surfaced to the maintainer with named options rather than
silently scheduled. FULL-mode structural outcomes route durably: confirmed
under-used authoritative items to a TODO improvement item; confirmed out-of-scope items
recorded in the run record so the next run does not re-adjudicate them. Findings
refuted at apply-time are recorded with the refutation, not routed; findings that
dedupe against an existing backlog item are cross-referenced, not duplicated.

### 6. Update the per-document state

In per-touch mode, after the touched documents' candidate sets are adjudicated or found
empty, refresh the configured per-document state with the source-store revision each
document was audited against and commit it with the change's QA batch. In FULL mode,
refresh state for every project document the run adjudicated. The state file is the delta anchor that keeps the per-touch
cadence near-free at steady state; a document with no state row is treated as never
audited and gets the full candidate set on its next touch.

### 7. Record and surface

Surface confirmed findings inline in chat (per-finding: document path, the held item
and its tier, the verdict, the concrete improvement, and the action taken or option
surfaced). Write the run to the run-record surface named in the project wiring, as a
dated per-run record file plus a row appended to its non-dated history record, using
that wiring's naming (the parent GRC library uses `YYYY-MM-DD-<scope>.md` plus
`history.md`); a zero-finding or empty-candidate run still gets a history row (the
proof-of-discipline), with no detail file. The pass terminates when the worklist is
adjudicated, confirmed findings are applied or routed, the state is updated for the
run's scope, and the run is recorded; it is a single advisory pass, not a
fix-to-fixed-point loop.

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
- Skipping the state-refresh step after a per-touch adjudication. A stale state row
  re-inflates the next touch's candidate set and erodes the near-free steady state the
  delta design exists to provide.
- Recommending engagement with a held source without confirming it is current upstream
  this turn. A superseded held text routes a version-update item first (the
  reference-version-currency SOP), and the breadth finding waits on the current text.
- Running this as a substitute for `/matrix-fit`, `/claim-fit`, or the citation gates.
  Breadth, fit, precision, and existence are four different questions; this skill only
  answers breadth.

## Verification

The pass is complete on a given run when:

- The mode and scope were named and the mechanical baseline was clean (the project's
  full audit suite exited 0) before the semantic read.
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
  run's change batch.
- The run was recorded (history row always; dated detail file when findings exist) and
  findings were surfaced inline in chat.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The citation gates pass, so the document's referencing is fine." | The gates check what the document already cites. Breadth asks what it should engage and does not; no gate can answer that. |
| "The topic matches, so the source belongs in the document." | Topic overlap is the tool's recall heuristic, not a finding. Only a read of the held text against the document decides; most matches are `no-fit`. |
| "The book says exactly what the document needs, so cite it." | Books are recommendation-tier by maintainer decision: never authoritative, never cited as a normative anchor. Corroborate against a trusted source first, or the suggestion waits. |
| "The per-touch run found nothing, so running it was waste." | The empty set at steady state is the design working: it certifies the document was checked against the current reference base at near-zero cost, and the state row proves it. |
| "The item is held, so the project must use it somewhere." | Some held items are legitimately outside project-content scope. The FULL-mode disposition records that judgement once, with a reason, instead of re-litigating it every run. |
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
- The advisory worklist tool named in the project wiring: the recall-oriented triage
  step that feeds this skill's worklist (not a gate; always exits 0; a per-touch form
  with a state-refresh flag for the delta anchor, new-ingest forms for reference deltas,
  and publications included only under an explicit screening decision), with its curated
  alias map, also named in the project wiring.
- The complementary acquisition-gap advisory tool named in the project wiring covers
  the cited-but-not-held direction: where this skill asks whether project content uses
  what the configured source store holds, that tool asks whether project content cites
  a source the store does not hold. In the parent GRC library it diffs the
  canonical-citations register against the reference catalogue and routes candidates to
  configured acquisition surfaces. It remains advisory, never a gate.
- The reference base named in the project wiring, located via its indexes, with the
  per-source currency confirmation, the superseded-archival workflow, and the
  trust-bucket rules the reference base's own conventions define.
