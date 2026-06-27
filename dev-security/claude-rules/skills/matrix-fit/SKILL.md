---
name: matrix-fit
description: Cadenced semantic-fit audit of the compliance matrix and per-document framework-alignment tables. Catches the gate-blind "valid code, wrong control" class: a control identifier that EXISTS in its catalogue (so the existence gates 48/49/54 pass it) but is the WRONG control for the row's document. Run after each FR-167 matrix-expansion batch, once at matrix completion, and ad-hoc when a control-code citation is in doubt. It dispatches a semantic judge over the recall-oriented worklist that `tools/audit-matrix-semantic-fit.py` produces, adjudicating each cited code against the source control TITLE in the reference base, then routes confirmed mismatches. It catches what the existence-and-membership gates structurally cannot: semantic fit needs a read of the source title, not a catalogue-membership check.
derives_from: ../../governance/evidence-grounded-completion.md
---

# Matrix Fit (semantic-fit audit of control-code citations)

## Overview

The audit gates that guard control-code citations check existence and catalogue membership, not semantic fit. Gate 48 confirms a CSA CCM / AICM code is cited from the right catalogue; gate 49 confirms a matrix row's codes are well-formed and in-catalogue; gate 54 confirms NIST CSF 2.0 codes in any per-document framework table are valid Category codes. None of them asks the question that actually matters for a mapping's correctness: is the control this row cites the *right* control for this row's document? A code can be perfectly valid (it exists, it is in the right catalogue, it is well-formed) and still be the wrong mapping. That class, "valid code, wrong control", is gate-blind by construction, because semantic fit cannot be decided by a string-and-membership check; it needs a reader to compare the document's subject against the cited control's TITLE.

The class is not hypothetical. The 2026-06-27 trust-recovery `/full-qa` found eight matrix rows and seven source-doc framework-table rows carrying valid-but-wrong codes, all remediated in PR #392; the same class had recurred across PRs #390/#391/#392 (improvement-log #392). Because semantic fit is not mechanically gate-checkable, the durable instrument is a cadenced audit rather than a new gate: a periodic human-or-subagent read of the cited control titles against the row subjects, scoped by a cheap pre-filter so the read is tractable.

`matrix-fit` is that audit. It is the semantic-judge half of a two-part instrument whose recall-oriented triage half is the advisory tool `tools/audit-matrix-semantic-fit.py` (shipped in PR #394, explicitly NOT a gate). The tool narrows scope: it lists the matrix and source-doc rows that lack any lexical anchor between the document subject and its cited control titles, so the judge can focus there first. The skill judges: for each worklisted row (and any other row the maintainer flags), it reads the cited control's TITLE in the reference base and decides whether the mapping fits. The design lesson from PR A is binding: judge against the source control TITLE, not a lexical proxy, because a correct GRC mapping routinely shares no vocabulary with the document title (the tool's own worklist is recall-oriented precisely because the lexical signal is too weak to certify correctness).

This skill is a single-pass advisory audit, not a fix-to-fixed-point loop and not a trust-recovery escalation. It runs on a cadence (after each FR-167 matrix-expansion batch, once at matrix completion, and ad-hoc), surfaces confirmed mismatches, and routes or fixes them under the normal in-window / out-of-window triage. It is to control-code *fit* what `/validate` is to corpus drift: a periodic read of a surface the mechanical gates cannot fully cover.

## When to Use

- **After each FR-167 matrix-expansion batch.** A batch authors many new mapping rows; a fit pass over the batch's worklist catches the valid-but-wrong codes before they compound across later batches. This is the primary cadence.
- **Once at matrix completion.** When the last domain batch lands, a full-matrix fit pass is the closing check on the comprehensive matrix.
- **Ad-hoc when a control-code citation is in doubt** (a maintainer flag, a `/validate` or `/full-qa` note about a loose supporting code, an apply-time uncertainty about which control a row should cite).
- **NOT as a replacement for the existence gates.** Gates 48/49/54 still run on every PR; `matrix-fit` is the semantic layer on top of them, not a substitute. A row must pass the gates first; this skill judges fit among rows that already pass.

## Process

### 1. Establish scope and confirm the reference base

Name the scope for this run: a single domain section (the FR-167-batch cadence), the whole matrix (the completion cadence), or a maintainer-flagged set of rows (the ad-hoc cadence). Confirm `tools/run_all_audits.sh` exits 0 first; a fit pass judges among rows that already pass the existence gates, so a red gate is a defect to fix mechanically before the semantic read. Confirm the reference base is available: the in-repo validator modules [`tools/ccm_aicm_reference.py`](../../../../tools/ccm_aicm_reference.py) and [`tools/nist_csf_reference.py`](../../../../tools/nist_csf_reference.py) carry the gate-validated control codes and titles, and the scratch reference base `grc_library_scratch/ref/standards/` carries the full source-text extracts (the CSA CCM v4.1 catalogue CSV, the NIST CSF 2.0 text, and the other source families). The judge reads control TITLES from these, never from memory.

### 2. Run the advisory pre-filter to generate the worklist

Run `python3 tools/audit-matrix-semantic-fit.py` (add `--matrix-only` or `--source-docs-only` to match the scope from step 1). The tool always exits 0; its output is a recall-oriented worklist of rows that lack any lexical anchor between the document subject and the cited control titles. Treat the worklist as the judge's input-narrowing step, NOT a defect list: a listed row is a candidate to read, a non-listed row is deprioritized (not certified correct). Add to the worklist any row the maintainer or a prior `/validate` / `/full-qa` note flagged (the known residual case is the loose-supporting-code-on-an-anchored-row, which the tool intentionally does not list, e.g. the Sweep-61 `TVM-06` note on a pen-testing standard).

### 3. Dispatch the semantic-fit judge over the worklist

Dispatch one or more subagents (or perform the read directly for a small worklist) to judge each worklisted row. The judge brief carries the shared preamble: read the cited control's TITLE from the reference base for every code on the row, compare it against the row's document subject, and decide fit (`fits` / `mismatch` / `loose-supporting`) with the source title quoted as evidence. The binding rule: judge against the source control TITLE, not a lexical proxy or a remembered meaning. A code that exists and is in-catalogue can still be a mismatch; only the title comparison decides. Every judgement quotes the control code, its source title, and the row location as `path:line`; a judgement without a quoted source title is a hypothesis, not a finding.

### 4. Synthesize and apply-time-verify each candidate against the source control title

The orchestrator re-reads each candidate mismatch's source title in the reference base before treating it as a finding, exactly as the research-assistant discipline requires (the judge produces research; the orchestrator confirms). A worker false positive (a correct mapping the lexical signal flagged, the dominant case on a clean corpus) is refuted here, not routed. For each confirmed mismatch, identify the correct control by reading candidate titles in the reference base, so the finding carries both the wrong code and the proposed right code with both titles quoted. When a mismatch is fixed, re-read the paired description cell in the same row for echoes of the old code's meaning (the migration-leaves-stale-prose class, CLAUDE.md close-out checklist).

### 5. Triage and route findings

For confirmed mismatches in the current scope (the batch just authored, or the maintainer-flagged set), fix them in-window: correct the code, bump the matrix or source document's Version and Date, and record the correction in the CHANGELOG-detailed entry. For confirmed mismatches outside the current scope (pre-existing rows surfaced incidentally), surface them to the maintainer with named options (fix-now vs route-to-backlog) rather than auto-deferring. Findings refuted at apply-time are recorded with the refutation, not routed. Findings that dedupe against an existing backlog item are cross-referenced, not duplicated.

### 6. Record and surface

Surface confirmed findings inline in chat (per-finding: row `path:line`, the wrong code and its source title, the proposed right code and its source title, fix-in-window vs routed). Write the run to the project's matrix-fit record location and append a history row; a zero-finding run still gets a history row (the proof-of-discipline), with no detail file. The pass terminates when the worklist is judged, the confirmed findings are routed or fixed, and the run is recorded; it is a single advisory pass, not a fix-to-fixed-point loop.

## Red Flags

- Judging fit from the code's familiarity or a remembered meaning instead of reading the source control TITLE. The PR-A design lesson is that the title is the only evidence; a remembered meaning is the failure mode that produced the valid-but-wrong codes in the first place.
- Treating the advisory tool's worklist as a defect list. It is recall-oriented triage; most listed rows are correct-but-lexically-distinct mappings. The skill adjudicates; the tool only narrows scope.
- Treating a non-listed row as certified correct. The tool deprioritizes anchored rows; the loose-supporting-code-on-an-anchored-row case is exactly what the tool does not list and the judge must still catch when flagged.
- Routing a judge finding without the orchestrator's own re-read of the source title. Apply-time verification is the false-positive filter; on a clean corpus the dominant case is a correct mapping the lexical signal flagged.
- Fixing a code without re-reading the paired description cell for stale prose echoing the old code's meaning (the migration-leaves-stale-prose class).
- Running this as a substitute for the existence gates, or skipping it because "the gates passed". The gates and this skill cover orthogonal classes; passing the gates says nothing about fit.

## Verification

The pass is complete on a given run when:

- The scope was named and the mechanical baseline was clean (`tools/run_all_audits.sh` exit 0) before the semantic read.
- The advisory pre-filter was run and its worklist (plus any maintainer-flagged rows) was the judge's input.
- Every worklisted row was judged against the source control TITLE read from the reference base, with the title quoted as evidence.
- The orchestrator re-read each candidate mismatch's source title and refuted or confirmed it; refutations are recorded, not routed.
- Confirmed in-scope mismatches were fixed (code corrected, Version and Date bumped, CHANGELOG entry written) and out-of-scope mismatches were surfaced with named options.
- The run was recorded (history row always; detail file when findings exist) and findings were surfaced inline in chat.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Gates 48/49/54 pass, so the codes are fine." | Those gates check existence and catalogue membership, not fit. A valid code can be the wrong control; only a title read decides. |
| "The worklist is short / empty, so the matrix is clean." | The worklist is recall-oriented triage, not a verdict. A short worklist narrows the read; it does not certify the unlisted rows, and the loose-supporting-code case is deliberately off the worklist. |
| "I recognize this code; it fits." | Recognition is a remembered meaning, the exact failure mode this skill exists to catch. Read the source title. |
| "The judge flagged it, so it is wrong; route it." | The lexical signal flags many correct mappings. Re-read the source title at apply-time before routing; on a clean corpus most flags are false positives. |
| "Semantic fit should just be a gate." | It is not mechanically checkable (correct GRC mappings routinely share no vocabulary with the document title). A blocking gate would be decorative; the cadenced audit is the durable instrument. |

## See Also

- Canonical rule [`evidence-grounded-completion`](../../governance/evidence-grounded-completion.md): the assertion-side discipline this skill applies to control-code citations (a claim that a row's mapping is correct requires reading the source title, not inferring it).
- Related skill [`citation-quote-verification`](../citation-quote-verification/SKILL.md): the sibling that verifies cited *quotes* match source text; this skill verifies cited *control codes* match the source control's subject. Both check what the format-and-membership gates cannot.
- Related skill [`validation-sweep`](../validation-sweep/SKILL.md) (`/validate`): the corpus-wide drift sweep whose notes can flag a control-code fit doubt for this skill to adjudicate.
- Related skill [`deep-qa-review`](../deep-qa-review/SKILL.md) (`/full-qa`): the trust-recovery forensic pass whose citation-forensic lens first surfaced the valid-but-wrong-control class at scale; this skill is the routine cadenced instrument that pass motivated.
- The advisory tool [`tools/audit-matrix-semantic-fit.py`](../../../../tools/audit-matrix-semantic-fit.py): the recall-oriented triage step that feeds this skill's worklist (not a gate; always exits 0).
- The reference base: the in-repo validator modules [`tools/ccm_aicm_reference.py`](../../../../tools/ccm_aicm_reference.py) and [`tools/nist_csf_reference.py`](../../../../tools/nist_csf_reference.py) (gate-validated codes and titles) and the scratch `grc_library_scratch/ref/standards/` full-text extracts (source control titles).
