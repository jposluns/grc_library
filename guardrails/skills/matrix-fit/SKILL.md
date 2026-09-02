---
name: matrix-fit
description: Cadenced semantic-fit audit of a compliance matrix and per-document framework-alignment tables. Catches the gate-blind "valid code, wrong control" class: a control identifier that EXISTS in its catalogue (so the existence gates pass it) but is the WRONG control for the row's document. Run after any batch that adds or edits mapping rows, once when a mapping surface reaches completion, and ad-hoc when a control-code citation is in doubt. It dispatches a semantic judge over the worklist the project's recall-oriented pre-filter produces, adjudicating each cited code against the source control TITLE in the reference base, then routes confirmed mismatches. It catches what the existence-and-membership gates structurally cannot: semantic fit needs a read of the source title, not a catalogue-membership check.
derives_from: ../../governance/evidence-grounded-completion.md
---

# Matrix Fit (semantic-fit audit of control-code citations)

## Project wiring (the parent library's instantiation; adopters substitute their own)

Portable procedure, concrete names. In the parent GRC library this skill runs with:

- Existence gates (the mechanical floor this skill's semantic layer sits on):
  gates 48, 49, 54, 58, and 61 (CSA CCM/AICM catalogue membership, matrix row
  well-formedness, NIST CSF 2.0 Category codes, ISO/IEC 27001:2022 Annex A codes,
  COBIT 2019 and ISO 31000:2018 identifiers).
- Recall-oriented pre-filter: `tools/audit-matrix-semantic-fit.py` (advisory,
  always exits 0, explicitly not a gate).
- Second worklist feeder: `tools/audit-stranded-matrix-code.py` (the advisory
  stranded-control-code scan; its confirmed strands are fit candidates).
- Judged surfaces: `compliance/matrix-grc-compliance-alignment.md` and the
  per-document framework-alignment tables.
- Reference base: the in-repo validator modules (`tools/ccm_aicm_reference.py`,
  `tools/nist_csf_reference.py`, `tools/cobit_iso31000_reference.py`,
  `tools/iso27001_reference.py`) and the `grc_library_ref` repository's
  source-text extracts.
- Primary cadence trigger: each matrix-expansion batch of the standing
  matrix-completion backlog item.

- QA execution (this project): the pass itself runs as the TRIPLE-FAMILY QA panel (the CLAUDE.md standard), the identical brief given to one Claude-, one Codex-, and one Gemini-family orch-verify worker with the verdicts reconciled; the Process's "dispatch one or more subagents (or perform the read directly)" wording describes the WORKER's own internal execution, never an in-session Task/Agent dispatch by the maintainer orchestrator, which the offload rule forbids and the block-orchestrator-self-qa hook blocks.
- Held-source citation and holdings/currency basis (P-1.56, from the 2026-08-31 stale-note `grc_library_ref` incident): every fit verdict cites the HELD SOURCE's own reference-base `path:line` for the control TITLE it read (the validator module or the `grc_library_ref` extract) as a REQUIRED field alongside the quoted title, and a verdict without it is REJECTED, because a title recalled from a note or from memory has no reference-base location to cite. That location comes from OPENING the held source (the validator module or the `grc_library_ref` extract), located via an EXECUTED `python3 tools/ref-holds.py <framework>` plus a reference-base INDEX read performed in THIS run (ref-holds and the index locate the held source and are the authority for what is HELD; the in-repo validator modules are current-by-construction; the `path:line` is where the title sits, read this run), never a note, a prior run's record, or memory. CURRENCY of a `grc_library_ref` extract is a SEPARATE question, validated UPSTREAM this run per the reference-version-currency SOP, never inferred from the index (believed-current STORAGE, not a version authority).

An adopting project maps each bullet to its own gates, pre-filter, surfaces, and
sources; the procedure below refers to them generically.

## Overview

The audit gates that guard control-code citations check existence and catalogue membership, not semantic fit: one gate family confirms each cited code is drawn from the right catalogue and well-formed, per framework (the parent library's concrete gate list is in the project wiring above). None of them asks the question that actually matters for a mapping's correctness: is the control this row cites the *right* control for this row's document? A code can be perfectly valid (it exists, it is in the right catalogue, it is well-formed) and still be the wrong mapping. That class, "valid code, wrong control", is gate-blind by construction, because semantic fit cannot be decided by a string-and-membership check; it needs a reader to compare the document's subject against the cited control's TITLE.

The class is not hypothetical. A trust-recovery forensic pass in the parent library found fifteen valid-but-wrong codes across matrix and source-document rows, and the class had recurred across consecutive changes before this cadence existed. Because semantic fit is not mechanically gate-checkable, the durable instrument is a cadenced audit rather than a new gate: a periodic human-or-subagent read of the cited control titles against the row subjects, scoped by a cheap pre-filter so the read is tractable.

`matrix-fit` is that audit. It is the semantic-judge half of a two-part instrument whose recall-oriented triage half is the advisory pre-filter named in the project wiring (explicitly NOT a gate). The pre-filter narrows scope: it lists the matrix and source-doc rows that lack any lexical anchor between the document subject and its cited control titles, so the judge can focus there first. The skill judges: for each worklisted row (and any other row the maintainer flags), it reads the cited control's TITLE in the reference base and decides whether the mapping fits. The design lesson from the pre-filter's construction is binding: judge against the source control TITLE, not a lexical proxy, because a correct GRC mapping routinely shares no vocabulary with the document title (the pre-filter's own worklist is recall-oriented precisely because the lexical signal is too weak to certify correctness).

This skill is a single-pass advisory audit, not a fix-to-fixed-point loop and not a trust-recovery escalation. It runs on a cadence (after each mapping batch, once at completion of a mapping surface, and ad-hoc), surfaces confirmed mismatches, and routes or fixes them under the normal in-window / out-of-window triage. It is to control-code *fit* what `/validate` is to project-wide drift: a periodic read of a surface the mechanical gates cannot fully cover.

## When to Use

- **After each batch that adds or edits mapping rows** (in the parent library, a matrix-expansion batch). A batch authors many new mapping rows; a fit pass over the batch's worklist catches the valid-but-wrong codes before they compound across later batches. This is the primary cadence.
- **Once when a mapping surface is completed.** When the last planned batch lands, a full-surface fit pass is the closing check on the completed mapping. The completion cadence judges EVERY row of the surface, not only the pre-filter worklist: it is the one systematic pass that covers the anchored-row `loose-supporting` residue the recall pre-filter deliberately omits. The per-batch and ad-hoc cadences stay worklist-scoped.
- **Ad-hoc when a control-code citation is in doubt** (a maintainer flag, a `/validate` or `/full-qa` note about a loose supporting code, an apply-time uncertainty about which control a row should cite).
- **NOT as a replacement for the existence gates.** The existence gates still run on every change; `matrix-fit` is the semantic layer on top of them, not a substitute. A row must pass the gates first; this skill judges fit among rows that already pass.

## Process

### 1. Establish scope and confirm the reference base

Name the scope for this run: the rows a just-authored batch introduced (the per-batch cadence), the whole mapping surface (the completion cadence), or a maintainer-flagged set of rows (the ad-hoc cadence). Confirm that the project's full audit-gate suite exits 0 first; a fit pass judges among rows that already pass the existence gates, so a red gate is a defect to fix mechanically before the semantic read. Confirm that the reference base named in the project wiring is available: the gate-validated control codes and titles, and the full source-text extracts for each cited framework family. The judge reads control TITLES from these, never from memory. Every fit verdict cites the held source's own reference-base `path:line` for the control TITLE it read from the held source this run (the source located via an EXECUTED `ref-holds` + index read; the Project-wiring held-source-citation requirement), never a note, a prior run's record, or memory; a held source extract's CURRENCY is validated upstream this run, not inferred from the index.

### 2. Run the advisory pre-filter to generate the worklist

Run the pre-filter named in the project wiring, scoped to match the scope from step 1 where the pre-filter supports scoping. The pre-filter always exits 0; its output is a recall-oriented worklist of rows that lack any lexical anchor between the document subject and the cited control titles. Treat the worklist as the judge's input-narrowing step, NOT a defect list: a listed row is a candidate to read, a non-listed row is deprioritized (not certified correct). Add to the worklist any row the maintainer or a prior `/validate` / `/full-qa` note flagged (the known residual case is a loose supporting code on an already-anchored row, which the pre-filter intentionally does not list). A second, complementary feeder is the stranded-control-code scan named in the project wiring: a code it confirms is cited on a mapping row but ABSENT from the referenced document is a fit candidate to fold into the worklist alongside the recall pre-filter's rows (a stranded code is not itself a mismatch, per the indicative-citation convention in step 3, but it is judged for fit like any other). **For the COMPLETION cadence the worklist is EVERY row of the surface**, not the pre-filter's output: the pre-filter and the stranded scan narrow only the per-batch and ad-hoc cadences, so the completion pass is the systematic coverage of the anchored-row `loose-supporting` residue neither triage lists.

### 3. Dispatch the semantic-fit judge over the worklist

Dispatch one or more subagents (or perform the read directly for a small worklist) to judge each worklisted row. The judge brief carries the shared preamble: read the cited control's TITLE from the reference base for every code on the row, compare it against the row's document subject, and decide fit (`fits` / `mismatch` / `loose-supporting`) with the source title quoted as evidence. The binding rule: judge against the source control TITLE, not a lexical proxy or a remembered meaning. A code that exists and is in-catalogue can still be a mismatch; the source read decides, title first (the supplementary full-text ladder in the rubric below applies only to a borderline call). Every judgement quotes the control code, its source title, the row location as `path:line`, AND the held source title's own reference-base `path:line` where that title was read in THIS run; a judgement without a quoted source title OR without its held-source `path:line` is a hypothesis, not a finding (P-1.56: a title from a note or from memory has no reference-base location to cite).

**The fit rubric** (judged against the row document's SUBJECT, quoting the source title):
- `fits`: the control's stated scope covers the row's primary subject.
- `loose-supporting`: a genuine but partial or secondary FIT to the subject, a supporting code sitting beside a CORRECT primary anchor (indicative breadth), never the row's principal control and never standing in for a wrong one.
- `mismatch`: the code does not fit the row's subject. This INCLUDES a same-family wrong-sibling (a code from the right family but the wrong specific control for the subject, e.g. A.5.1 "Policies for information security" where A.5.2 "Information security roles and responsibilities" belongs). Family membership never establishes fit; only the subject comparison does, and this is the exact valid-code-wrong-control class the skill exists to catch.

The source TITLE is the primary evidence AND the mandatory carrier: every verdict quotes the source title and its held-source `path:line` (P-1.56), whichever verdict it is. For any borderline call the title does not settle (a `fits`-versus-`mismatch`, `fits`-versus-`loose-supporting`, or `loose-supporting`-versus-`mismatch` boundary), the judge MAY additionally read and quote the control's full specification text in the reference base with its OWN held-source `path:line` as supplementary grounding; the title citation is never dropped or replaced, only supplemented, so the mandatory carrier is always satisfied.

**The indicative-citation convention governs literal presence, NOT fit (maintainer-decided 2026-09-02).** The master compliance matrix cites control codes INDICATIVELY: a code is a representative pointer to a control family or topic, and it need NOT appear verbatim in the referenced document to be legitimate (the strict-reproduce restructure is off). So a STRANDED code (cited on the row but absent from the document text) is not a defect on that ground alone. This convention is about literal presence ONLY: every cited code is STILL judged for fit against the row's subject by the rubric above, and a code that MIS-FITS the subject is a `mismatch` whether or not the document reproduces it. The convention widens what may be cited; it never excuses a wrong control. Where a code sits on a representative-versus-strict-reproduce boundary the maintainer has not resolved for that surface, route it to the pending decision rather than auto-verdicting.

### 4. Synthesize and apply-time-verify each candidate against the source control title

The orchestrator re-reads each candidate `mismatch` AND each candidate `loose-supporting` verdict's source title in the reference base before treating it as confirmed, exactly as the research-assistant discipline requires (the judge produces research; the orchestrator confirms). A candidate `loose-supporting` that is really a `fits` or a `mismatch` on re-read is reclassified here, not recorded as retained. A worker false positive (a correct mapping the lexical signal flagged, the dominant case on a clean corpus) is refuted here, not routed. For each confirmed mismatch, identify the correct control by reading candidate titles in the reference base, so the finding carries both the wrong code and the proposed right code with both titles quoted. When a mismatch is fixed, re-read the paired description cell in the same row for echoes of the old code's meaning (the migration-leaves-stale-prose class).

### 5. Triage and route findings

For confirmed mismatches in the current scope (the batch just authored, or the maintainer-flagged set), fix them in-window: correct the code, bump the matrix or source document's Version and Date, and record the correction in the project's detailed change record (the CHANGELOG-detailed entry in the parent GRC library). For confirmed mismatches outside the current scope (pre-existing rows surfaced incidentally), surface them to the maintainer with named options (fix-now vs route-to-backlog) rather than auto-deferring. Findings refuted at apply-time are recorded with the refutation, not routed. Findings that dedupe against an existing backlog item are cross-referenced, not duplicated.

A confirmed `loose-supporting` verdict (re-verified in step 4) is NOT a mismatch and is never "corrected": it is KEPT as an indicative mapping and RECORDED in the run's detail file (step 6) with its row `path:line`, the retained code, its source title and held-source `path:line`, and the indicative-retention rationale, so a later reader sees the code was judged and deliberately retained. Only `mismatch` verdicts are fixed in-window or routed; a `fits` verdict needs no action beyond the count in the history row.

### 6. Record and surface

Surface confirmed findings inline in chat: a `mismatch` per-finding carries the row `path:line`, the wrong code and its source title, the proposed right code and its source title, each title's held-source reference-base `path:line`, and fix-in-window vs routed; a retained `loose-supporting` carries the row `path:line`, the code, its source title and held-source `path:line`, and the indicative-retention rationale. Write the run to the project's matrix-fit record location and append a history row; a run with ANY judged `mismatch` OR retained `loose-supporting` verdict also writes a detail file recording each of them, while a run with neither still gets its history row alone (the proof-of-discipline), with no detail file. The pass terminates when the worklist is judged, the confirmed findings are routed or fixed, and the run is recorded; it is a single advisory pass, not a fix-to-fixed-point loop.

## Red Flags

- Judging fit from the code's familiarity or a remembered meaning instead of reading the source control TITLE. The pre-filter's founding design lesson is that the source read, title first, is the only evidence (the held full control text is supplementary grounding for a borderline call, never a remembered meaning); a remembered meaning is the failure mode that produced the valid-but-wrong codes in the first place.
- Treating the advisory pre-filter's worklist as a defect list. It is recall-oriented triage; most listed rows are correct-but-lexically-distinct mappings. The skill adjudicates; the pre-filter only narrows scope.
- Treating a non-listed row as certified correct. The pre-filter deprioritizes anchored rows; the loose-supporting-code-on-an-anchored-row case is exactly what the pre-filter does not list and the judge must still catch when flagged.
- Routing a judge finding without the orchestrator's own re-read of the source title. Apply-time verification is the false-positive filter; on a clean corpus the dominant case is a correct mapping the lexical signal flagged.
- Recording a fit verdict, or a held-status claim for a cited framework, from a note or a prior run's record instead of an executed `ref-holds` + index read with the held-source title `path:line` cited THIS run (the 2026-08-31 stale-note incident this cadence's P-1.56 requirement exists to prevent).
- Fixing a code without re-reading the paired description cell for stale prose echoing the old code's meaning (the migration-leaves-stale-prose class).
- Running this as a substitute for the existence gates, or skipping it because "the gates passed". The gates and this skill cover orthogonal classes; passing the gates says nothing about fit.

## Verification

The pass is complete on a given run when:

- The scope was named and the mechanical baseline was clean (the project's full audit-gate suite exit 0) before the semantic read.
- The advisory pre-filter was run and its worklist (plus any maintainer-flagged rows) was the judge's input.
- Every worklisted row was judged against the source control TITLE read from the reference base, with the title quoted as evidence; for a COMPLETION-cadence run, every row of the surface was judged, not only the worklisted subset.
- Every fit verdict cited the held source title's own reference-base `path:line` from an executed `ref-holds` + index read in THIS run (not a note, a prior run's record, or memory); any held source extract currency claim was validated upstream this run rather than inferred from the index.
- The orchestrator re-read each candidate `mismatch` AND each candidate `loose-supporting` source title and refuted, reclassified, or confirmed it; refutations are recorded, not routed.
- Confirmed in-scope mismatches were fixed (code corrected, Version and Date bumped, CHANGELOG entry written) and out-of-scope mismatches were surfaced with named options.
- The run was recorded (history row always; a detail file when any `mismatch` or retained `loose-supporting` verdict exists) and findings were surfaced inline in chat.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The existence gates pass, so the codes are fine." | Those gates check existence and catalogue membership, not fit. A valid code can be the wrong control; only a title read decides. |
| "The worklist is short / empty, so the matrix is clean." | The worklist is recall-oriented triage, not a verdict. A short worklist narrows the read; it does not certify the unlisted rows, and the loose-supporting-code case is deliberately off the worklist. |
| "I recognize this code; it fits." | Recognition is a remembered meaning, the exact failure mode this skill exists to catch. Read the source title. |
| "The reference base held this title last run, or a note says it is held." | Holdings is determined by an executed `ref-holds` + index read THIS run, cited by the held-source title `path:line`; a note or a prior run's record is not a holdings authority, and a held source extract's currency is validated upstream, never inferred from the index. |
| "The judge flagged it, so it is wrong; route it." | The lexical signal flags many correct mappings. Re-read the source title at apply-time before routing; on a clean corpus most flags are false positives. |
| "Semantic fit should just be a gate." | It is not mechanically checkable (correct GRC mappings routinely share no vocabulary with the document title). A blocking gate would be decorative; the cadenced audit is the durable instrument. |

## See Also

- Canonical rule [`evidence-grounded-completion`](../../governance/evidence-grounded-completion.md): the assertion-side discipline this skill applies to control-code citations (a claim that a row's mapping is correct requires reading the source title, not inferring it).
- Related skill [`citation-quote-verification`](../citation-quote-verification/SKILL.md): the sibling that verifies cited *quotes* match source text; this skill verifies cited *control codes* match the source control's subject. Both check what the format-and-membership gates cannot.
- Related skill [`validation-sweep`](../validation-sweep/SKILL.md) (`/validate`): the corpus-wide drift sweep whose notes can flag a control-code fit doubt for this skill to adjudicate.
- Related skill [`deep-qa-review`](../deep-qa-review/SKILL.md) (`/full-qa`): the trust-recovery forensic pass whose citation-forensic lens first surfaced the valid-but-wrong-control class at scale; this skill is the routine cadenced instrument that pass motivated.
- The advisory pre-filter named in the project wiring: the recall-oriented triage step that feeds this skill's worklist (not a gate; always exits 0).
- The reference base named in the project wiring: the gate-validated control codes and titles plus the full source-text extracts from which the judge reads control TITLES.
- Related skill [`claim-fit`](../claim-fit/SKILL.md) (`/claim-fit`): the same semantic-layer pattern applied to normative-value ATTRIBUTION claims (is the attributed value actually prescribed by the cited source?); this skill judges control-code fit, that one judges value precision, both above the existence gates.
