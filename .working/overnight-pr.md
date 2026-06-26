<!-- OVERNIGHT-PR-IN-FLIGHT -->
# Overnight PR

**Status:** in-flight

## Authorization scope (2026-06-26)

The maintainer ran an attended session (assess the improvement log and hallucination
metrics, then build the resulting guard rails), directed the full set of recommended
mechanisms plus a full `.working/` em-dash conformance pass, then went to sleep with the
instruction to plan the next 20 PRs. This file records the resulting autonomous overnight
run.

**Authorized for autonomous execution (green-CI = merge, full per-PR `/validate-pr` +
`/retro`, stricter-is-safer on any conflict):** the integrity-tooling phase agreed this
session (Phase A to C of the 20-PR plan), namely:
- Full `.working/` em-dash conformance (separator `### PR #N:` colon, Detail placeholder
  `none`, prose to comma, ranges to hyphen). Convention defined in #352; bulk apply in
  #353; the prose-hygiene gate in #354.
- Tier-1 prose-hygiene gate (em/en-dash forbidden in `.working/` prose, allowed inside
  inline code spans; plus link-coverage over the CHANGELOG detailed mirror; full-scan plus
  a `--staged` pre-commit mode).
- Tier-2 gate family: directory-scan-scope parity meta-check (TODO 62), directional-
  dependency gate (TODO 61), the gate-50 coverage verification plus any QA-cadence/rotation
  residual, gate-49 extension to per-document reference tables (TODO 88).
- Discipline codification: candidate E (pre-AskUserQuestion turn-scan), prose-fact-
  correction full-file-grep line, the §4.15 functional-category-index currency, and the
  two maintainer-directed regular disciplines (`.working/` standardization as a wind-down
  activity; hallucination-metrics refresh at every wind-down).

**Held for maintainer confirmation on waking (NOT executed autonomously):** Phase D, the
semantic content backlog (FR-167 matrix batches 5 to 11; the decided-content series FR-73
/ FR-58 / FR-145 / the deepen-all thin baselines / the H[critical] net-new docs). These
are semantic mappings and new prose whose correctness the gates do not catch, and `.working/`
content is gate-exempt so green CI is not a safety net for them. Read-only research prep for
FR-167 batch 5 may be staged but not merged.

## The 20-PR plan (chat-surfaced 2026-06-26)

#352 (MERGED) pack convention conformance. #353 bulk `.working/` conformance; #354 Tier-1
hygiene gate (51); #355 dir-scan-scope parity (52); #356 directional-dependency gate (53);
#357 gate-50 coverage verification plus §4.6/§4.10 residual; #358 gate-49 extension; #359
discipline codification (candidate E plus prose-fact grep plus §4.15); #360 the two regular
wind-down disciplines plus the metrics refresh. #361 to #372 = Phase D (held).

## Design decisions made this session

- `.working/` em-dash full conformance INCLUDING the separator convention: DONE header
  separator becomes `### PR #N:` (colon); history-table zero-finding Detail placeholder
  becomes `none`; em/en-dashes inside inline code spans are preserved as literals (regex
  char classes, frozen historical quotes, the rule-statement glyphs). Maintainer-chosen
  2026-06-26. Pack templates defined in #352; bulk apply in #353.
- `.working/` cleanup is authorized broadly (any old non-conforming file may be edited) and
  becomes a regular wind-down activity (codify in #360).
- Hallucination-metrics refresh becomes a regular wind-down step (codify in #360).

## Build progress

- #352 MERGED: pack convention conformance (separator plus Detail placeholder defined).
- #353 in progress: bulk `.working/` conversion (74 files, ~1299 prose lines; 11 code-span
  literals preserved) plus Sweep 49 row plus cursor plus #352 QA rows plus pack README Date
  fix.

## Surfaced ambiguities / deferred

- Phase D content work deferred to maintainer (semantic, not gate-caught).
- The two standing maintainer actions (seed scratch reference binaries; provision the
  external-collaborator worker account) remain pending, recorded in
  [`session-handoff.md`](session-handoff.md).
