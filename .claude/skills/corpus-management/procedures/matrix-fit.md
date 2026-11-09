---
name: matrix-fit
description: Cadenced semantic-fit audit of a compliance matrix and per-document framework-alignment tables. Catches the gate-blind "valid code, wrong control" class, a control identifier that EXISTS in its catalogue (so the existence gates pass it) but is the WRONG control for the row's document. Run after any batch that adds or edits mapping rows, once when a mapping surface reaches completion, and ad-hoc when a control-code citation is in doubt. A reviewer judges each cited code against the source control TITLE in the reference base, then confirmed mismatches are routed. It catches what the existence-and-membership gates structurally cannot, because semantic fit needs a read of the source title, not a catalogue-membership check.
---

# Matrix Fit (semantic-fit audit of control-code citations)

## Corpus wiring (this repository's instantiation; adopters substitute their own)

Portable procedure, concrete names. In this repository the procedure runs with:

- Existence gates (the mechanical floor this semantic layer sits on): gates 48, 49, 54, 58, and 61 in [`specification-audit-programme.md`](../specs/specification-audit-programme.md) (CSA CCM/AICM catalogue membership, matrix row well-formedness, NIST CSF 2.0 Category codes, ISO/IEC 27001:2022 Annex A codes, COBIT 2019 and ISO 31000:2018 identifiers).
- Judged surfaces: [`compliance/matrix-grc-compliance-alignment.md`](../../../../compliance/matrix-grc-compliance-alignment.md) and the per-document framework-alignment tables.
- Reference base, in-repo half: the validator modules [`ccm_aicm_reference.py`](../tools/ccm_aicm_reference.py), [`nist_csf_reference.py`](../tools/nist_csf_reference.py), [`cobit_iso31000_reference.py`](../tools/cobit_iso31000_reference.py), and [`iso27001_reference.py`](../tools/iso27001_reference.py) (gate-validated codes and titles); [`verify-reference-modules.py`](../tools/verify-reference-modules.py) is the parity aid between those modules and the held source extracts.
- Reference base, held-text half: the adopting project's reference base (a local repository or directory of held source texts, located via its own indexes), holding the full source-text extracts for each cited framework family.
- Mechanical baseline: [`run_all_audits.sh`](../tools/run_all_audits.sh).
- Worklist narrowing: an optional deeper review may supplement the public gates by narrowing the worklist before the read; without one, the worklist is the in-scope row set itself.
- Run records: the adopting project's own working records.

An adopting project maps each bullet to its own gates, surfaces, and sources; the procedure below refers to them generically.

## Overview

The audit gates that guard control-code citations check existence and catalogue membership, not semantic fit: one gate family confirms each cited code is drawn from the right catalogue and well-formed, per framework. None of them asks the question that actually matters for a mapping's correctness: is the control this row cites the *right* control for this row's document? A code can be perfectly valid (it exists, it is in the right catalogue, it is well-formed) and still be the wrong mapping. That class, "valid code, wrong control", is gate-blind by construction, because semantic fit cannot be decided by a string-and-membership check; it needs a reader to compare the document's subject against the cited control's TITLE.

The class is not hypothetical: a forensic pass in this corpus found fifteen valid-but-wrong codes across matrix and source-document rows, and the class had recurred across consecutive changes before this cadence existed. Because semantic fit is not mechanically gate-checkable, the durable instrument is a cadenced audit rather than a new gate: a periodic read of the cited control titles against the row subjects.

This procedure is a single-pass advisory audit, not a fix-to-fixed-point loop. It runs on a cadence (after each mapping batch, once at completion of a mapping surface, and ad-hoc), surfaces confirmed mismatches, and routes or fixes them under the normal in-window / out-of-window triage.

## When to Use

- **After each batch that adds or edits mapping rows.** A batch authors many new mapping rows; a fit pass over the batch's rows catches the valid-but-wrong codes before they compound. This is the primary cadence.
- **Once when a mapping surface is completed.** The completion cadence judges EVERY row of the surface: it is the one systematic pass that covers the anchored-row `loose-supporting` residue a narrowing pre-filter deliberately omits.
- **Ad-hoc when a control-code citation is in doubt** (a maintainer flag, a validation-sweep note, an apply-time uncertainty about which control a row should cite).
- **NOT as a replacement for the existence gates.** The existence gates still run on every change; this audit is the semantic layer on top of them. A row must pass the gates first; this procedure judges fit among rows that already pass.

## Process

### 1. Establish scope and confirm the reference base

Name the scope for this run: the rows a just-authored batch introduced (the per-batch cadence), the whole mapping surface (the completion cadence), or a flagged set of rows (the ad-hoc cadence). Confirm the project's full audit-gate suite exits 0 first; a red gate is a defect to fix mechanically before the semantic read. Confirm the reference base is available: the gate-validated control codes and titles, and the full source-text extracts for each cited framework family. The reviewer reads control TITLES from these, never from memory. Every fit verdict cites the held source's own reference-base `path:line` for the control TITLE it read, located via an executed reference-base index read performed in THIS run (never a note, a prior run's record, or memory); a held extract's CURRENCY is validated upstream this run, not inferred from the index; the one exception is a `title-not-held` verdict, which has no held title to cite and instead carries the same executed index read as its absence evidence.

### 2. Build the worklist

The worklist for the per-batch cadence is the batch's rows; for the ad-hoc cadence, the flagged rows; for the COMPLETION cadence, EVERY row of the surface. Add any row the maintainer or a prior sweep note flagged. An optional deeper review may supplement the public gates by pre-filtering rows that lack a lexical anchor between the document subject and the cited control titles; treat any such pre-filter output as input-narrowing, never a defect list (a listed row is a candidate to read, a non-listed row is deprioritized, not certified correct).

### 3. Judge each worklisted row against the source control title

For each worklisted row, the reviewer reads the cited control's TITLE from the reference base for every code on the row, compares it against the row's document subject, and decides fit (`fits` / `mismatch` / `loose-supporting` / `title-not-held`) with the source title quoted as evidence. The binding rule: judge against the source control TITLE, not a lexical proxy or a remembered meaning; a code that exists and is in-catalogue can still be a mismatch. Every fit judgement quotes the control code, its source title, the row location as `path:line`, AND the held source title's own reference-base `path:line` where that title was read in THIS run; a judgement without the quoted title or without its held-source `path:line` is a hypothesis, not a finding; the one exception is a `title-not-held` verdict, which carries its executed reference-base index read as the absence evidence instead.

**The fit rubric** (judged against the row document's SUBJECT, quoting the source title):

- `fits`: the control's stated scope covers the row's primary subject.
- `loose-supporting`: a genuine but partial or secondary FIT to the subject, a supporting code sitting beside a CORRECT primary anchor (indicative breadth), never the row's principal control and never standing in for a wrong one.
- `mismatch`: the code does not fit the row's subject. This INCLUDES a same-family wrong-sibling (right family, wrong specific control). Family membership never establishes fit; this is the exact valid-code-wrong-control class the procedure exists to catch.
- `title-not-held`: no held source (neither a validator title map nor a reference-base extract, established by the executed index read THIS run) carries the cited control's title, so no fit judgement is possible for that code. The finding FIRST triggers an acquisition attempt via the project's ingest path; only a failed or constrained attempt produces an acquisition-queue entry, with the code's judgement deferred, never guessed from memory. The row's OTHER codes are still judged normally.

For a borderline call the title does not settle, the reviewer MAY additionally read and quote the control's full specification text in the reference base with its OWN held-source `path:line` as supplementary grounding; the title citation is never dropped, only supplemented.

**The indicative-citation convention governs literal presence, NOT fit.** This corpus cites matrix control codes INDICATIVELY: a code is a representative pointer to a control family or topic and need not appear verbatim in the referenced document. So a STRANDED code (cited on the row but absent from the document text) is not a defect on that ground alone; it is still judged for fit, and a code that mis-fits the subject is a `mismatch` whether or not the document reproduces it. Where a code sits on a representative-versus-strict-reproduce boundary the maintainer has not resolved, route it to the maintainer rather than auto-verdicting.

### 4. Apply-time-verify each candidate against the source control title

Re-read each candidate `mismatch` AND each candidate `loose-supporting` verdict's source title in the reference base before treating it as confirmed. A candidate that is really `fits` (or really `mismatch`) on re-read is reclassified, not recorded as first judged. A false positive (a correct mapping that a lexical signal flagged, the dominant case on a clean corpus) is refuted here, not routed. For each confirmed mismatch, identify the correct control by reading candidate titles, so the finding carries both the wrong code and the proposed right code with both titles quoted. When a mismatch is fixed, re-read the paired description cell in the same row for echoes of the old code's meaning. A candidate `title-not-held` is verified by your OWN executed reference-base index read (a holdings-absence claim carries the full inventory burden), and is reclassified to the normal rubric when the title is in fact held.

### 5. Triage and route findings

Confirmed mismatches in the current scope are fixed in-window: correct the code, bump the matrix or source document's Version and Date, and record the correction in the project's change record. Confirmed mismatches outside the current scope are surfaced to the maintainer with named options (fix-now vs route-to-backlog), not auto-deferred. Findings refuted at apply-time are recorded with the refutation, not routed; findings that dedupe against an existing backlog item are cross-referenced, not duplicated.

A confirmed `loose-supporting` verdict is NOT a mismatch and is never "corrected": it is KEPT as an indicative mapping and RECORDED in the run record with its row `path:line`, the retained code, its source title and held-source `path:line`, and the indicative-retention rationale. A confirmed `title-not-held` is ROUTED acquisition-first: attempt the ingest, and only a failed or constrained attempt produces an acquisition-queue entry, with the code's judgement deferred, never guessed; a successful ingest is followed by re-judging the code against the now-held title.

### 6. Record and present

Surface confirmed findings to the maintainer directly: a `mismatch` carries the row `path:line`, the wrong code and its source title, the proposed right code and its source title, each title's held-source reference-base `path:line`, and fix-in-window vs routed; a retained `loose-supporting` carries the row `path:line`, the code, its source title and held-source `path:line`, and the retention rationale; a `title-not-held` carries the code, the row `path:line`, the executed reference-base index read evidence for the absence, and its acquisition attempt or routing. Record the run (scope, worklist, verdict counts, dispositions) in the project's own working records; a run with no `mismatch`, retained `loose-supporting`, or `title-not-held` still gets a one-line record (the proof-of-discipline). The pass terminates when the worklist is judged, the confirmed findings are routed or fixed, and the run is recorded; it is a single advisory pass, not a fix-to-fixed-point loop.

## Red Flags

- Judging fit from the code's familiarity or a remembered meaning instead of reading the source control TITLE. A remembered meaning is the failure mode that produced the valid-but-wrong codes in the first place.
- Treating a pre-filter's worklist as a defect list, or a non-listed row as certified correct.
- Recording a fit verdict, or a held-status claim for a cited framework, from a note or a prior run's record instead of the held-source title `path:line` cited from an executed reference-base index read THIS run (a `title-not-held` verdict instead cites the executed index read that established the absence).
- Routing a candidate finding without your own re-read of the source title (the one exception: a confirmed `title-not-held` rests on your own executed index read, there being no held title to re-read).
- Fixing a code without re-reading the paired description cell for stale prose echoing the old code's meaning.
- Running this as a substitute for the existence gates, or skipping it because "the gates passed". The gates and this audit cover orthogonal classes.

## Verification

The pass is complete on a given run when:

- The scope was named and the mechanical baseline was clean before the semantic read.
- Every worklisted row was judged against the source control TITLE read from the reference base, with the title quoted and its held-source reference-base `path:line` cited from an executed index read in THIS run (the one exception: a `title-not-held` verdict, which cited its executed index read absence evidence instead); for a COMPLETION-cadence run, every row of the surface was judged.
- Each candidate `mismatch` and `loose-supporting` was re-read and refuted, reclassified, or confirmed; refutations were recorded, not routed.
- Confirmed in-scope mismatches were fixed (code corrected, Version and Date bumped, change record written) and out-of-scope mismatches were surfaced with named options.
- Any `title-not-held` verdict rested on your own executed reference-base index read THIS run and carried its acquisition attempt or routing, and the row's other codes were still judged.
- Any worklisted row not judged (deferred or routed) was NAMED with its blocker; none was silently dropped.
- The run was recorded and findings were presented to the maintainer.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The existence gates pass, so the codes are fine." | Those gates check existence and catalogue membership, not fit. A valid code can be the wrong control; only a title read decides. |
| "I recognize this code; it fits." | Recognition is a remembered meaning, the exact failure mode this audit exists to catch. Read the source title. |
| "The reference base held this title last run, or a note says it is held." | Holdings is determined by an executed reference-base index read THIS run, cited by the held-source title `path:line`; a note or a prior run's record is not a holdings authority, and a `title-not-held` call carries the executed index read instead. |
| "A flagged row must be wrong; route it." | A lexical signal flags many correct mappings. Re-read the source title at apply-time before routing; on a clean corpus most flags are false positives. |
| "Semantic fit should just be a gate." | It is not mechanically checkable (correct GRC mappings routinely share no vocabulary with the document title). A blocking gate would be decorative; the cadenced audit is the durable instrument. |

## See Also

- Related procedure [`claim-fit.md`](claim-fit.md): the same semantic-layer pattern applied to normative-value ATTRIBUTION claims; this procedure judges control-code fit, that one judges value precision, both above the existence gates.
- Related procedure [`validation-sweep.md`](validation-sweep.md): the corpus-wide drift sweep whose notes can flag a control-code fit doubt for this audit to adjudicate.
- The validator-module parity aid [`verify-reference-modules.py`](../tools/verify-reference-modules.py): confirms the in-repo code-and-title modules still match the held source extracts.
- The canonical gate inventory: [`specification-audit-programme.md`](../specs/specification-audit-programme.md).
