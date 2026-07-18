# Deferred protected-file changes (overnight → daytime apply queue)

**Purpose / persistent reminder (maintainer-directed 2026-07-05).** In OVERNIGHT mode,
protected-file edits are DEFERRED: they need the maintainer's authorization (a click/tap the
maintainer cannot give while away), per the A1 answer at the 2026-07-05 resume ("in overnight
mode I won't be there to authorize claude.md changes; do not pause asking me for
authorization, anything that requires me to click/tap must be deferred to day time runs").
Protected surfaces are `.claude/` (including `.claude/CLAUDE.md`, commands, hooks, settings)
and the `dev-security/claude-rules/` governance pack. This file is the persistent staging
area for those deferred changes; it lives in `.working/` (not protected), so it can be
written during the overnight run and survives across sessions on `main`.

**Mode-transition protocol (overnight → daytime).** When the maintainer switches the session
from overnight to daytime / attended mode:

1. **Finish the then-current PR** (do not abandon it mid-flight).
2. **Then clear this backlog**: apply every prepared protected-file change below, each as its
   own PR or a coherently-grouped one, with `tools/lint-language.py` run on the new/edited
   pack prose BEFORE the first commit, and full per-PR `/validate-pr` + `/retro`.
3. **Rotate each item out** of this file as it lands (record in CHANGELOG + DONE as usual);
   when the file is empty it holds only this header.

The items below are **drafted in advance during the overnight run** so the daytime apply is
quick: the content is ready and only the authorized apply + QA remains.

---

## Prepared items (apply at daytime, in this order)

_Landed in PR #652 (2026-07-05): item 1 (codify the mode-transition protocol in CLAUDE.md,
now the `Overnight-to-daytime protected-backlog clearance` paragraph in the
`## Attended-autonomous operating mode` section) and item 5(a) (reword the rule-3 fallback to
drop the longer-check-in option). Landed in PR #654 (2026-07-05): item 2 (the pack-tree ATLAS
technique-ID currency refresh, TODO 3.18 closed: eight `AML.T0048` re-pointed to `AML.T0053`
and two gloss drifts corrected against the held ATLAS 2026.06 CSVs). Landed in PR #655
(2026-07-05): item 3 (the guardrail-review SKILL cadence clause, TODO 3.15 D-F2 closed: the
auto-prompt bullet now names gate 60 and states the deferral is bounded, warn at drift 1 to 2,
fail at 3). Landed in PR #656 (2026-07-05): item 4's PACK surfaces (the D-F3 corollary clauses
on the pack CLAUDE.md rule-index one-liner, the pack README tree blurb, and the pack README
scope row; pack `1.54.6`). Landed in PR #657 (2026-07-05): item 4's remaining
project-CLAUDE.md clause, so TODO 3.15 D-F3 is now FULLY closed and item 4 is rotated out.
Item 5's remaining r5 close-out-checklist clauses re-scope from the former #657 bundle to a
focused #658 (maintainer-directed 2026-07-05: after #657, small Priority 3 and Priority 1
items first to clear TODO count; the larger GR-P design track, item 6, defers). Landed in PR #674 (2026-07-06): item 5's remaining `/claim-fit` cadence-section clause, applied as a new `## Normative-attribution claim-precision cadence (/claim-fit)` section in `.claude/CLAUDE.md` sibling to `/matrix-fit`, so item 5 is fully rotated out. Landed in PR #813 (2026-07-11): item 7 (changelog-restructure prose), the current-week model documented in the change-tracking rule (both copies) and the `change-tracking-write-entry` skill (pack copy only; there is NO `.claude/` skill copy, contrary to the prepared note), plus an advisory per-PR detailed-mirror-sweep close-out bullet and the current-week model / `.gitattributes` export-ignore / deferred compact root-entry format described in `.claude/CLAUDE.md`. The compact-format ADOPTION and the initial completed-weeks sweep remain the deferred root-reformat (TODO 3.16, post-deep-assessment). Landed in PR #969 (2026-07-16): item 10 (credit-offload phase 3 orchestrator wiring), applied as the `/resume` step-6 blocking-resume-`/validate` enqueue/wait/consume + step-3 queue/results check and the `## Credit-offload mode` section of `.claude/CLAUDE.md`, with the design-of-record (`credit-offload-design.md`) updated to phase-3-applied plus the two worker-lifecycle hooks; TODO §3.80 phase-3 sub-item rotated. Items 6, 8, and 9 remain: item 6 (the GR-P design track); and, staged 2026-07-15 overnight, item 8 (the §3.22 D7 handoff-snapshot marker fix, whose CLAUDE.md convention-guard note is the protected part) and item 9 (the §3.12 See-Also parity gate, whose gate-count bump ripples into the protected CLAUDE.md)._

### 6. [TODO 4.7 GR-P1..P5] Pack design improvements (design-tier)

- **Targets:** the `dev-security/claude-rules/` pack (rules, skills, README, overlay pointers).
- **Prep status:** design-tier, larger; draft the shape proposals during the overnight run if
  time permits after the corpus/tooling/P2 work, else leave prep notes. GR-P1 session-lifecycle
  pack rule; GR-P2 rule operative-core condense; GR-P3 third-occurrence-to-gate escalation;
  GR-P4 overlay primary-wins pointers + pruning stance; GR-P5 `derives_from` re-point + exception-
  register hoist + the CLAUDE.md Boundaries-line wrong-trio correction. These are their own PRs.

### 8. [TODO §3.22] Fix the D7 handoff-snapshot version-token check defeated by the #746 restructure

- **Why deferred (2026-07-15 overnight):** the fix must reword `.claude/CLAUDE.md`'s D7 convention-guard note (protected). Applying only the non-protected tool/test halves would leave a multi-surface inconsistency (the note would still say "Current truth line"), so the whole item applies together at daytime.
- **Non-protected parts (apply in the same daytime PR):**
  - `tools/check-handoff-snapshot-on-pr.py`: D7 locates the `Current truth` marker line via `snapshot_line()`, but the #746 restructure moved the version tokens onto a separate `**Version snapshot (D7 validates these tokens):**` sub-line, so D7 parses 0 tokens and passes trivially. Fix: add a `VERSION_SNAPSHOT_MARKER = "Version snapshot"` and have `snapshot_line()` return the line containing THAT marker (the tokens live there); keep the `Current truth` block-presence check for the malformed-handoff error path. Confirmed against the live handoff, the labelled tokens (library / README / pack / spec + gate / rules / skills / commands / Document-types) are on the `Version snapshot` sub-line, NOT the `Current truth` line.
  - `tests/test_linters.py` D7 tests (`check-handoff-snapshot-on-pr.py` class, ~line 1660): the fixtures put tokens on the `Current truth` line (the old shape); update them to the real two-line shape (a `Current truth` line plus a `Version snapshot` sub-line carrying the tokens) so the reconciled / stale-token / duplicate-token cases exercise the fixed marker. Re-confirm the stale-token test fails on a token located on the sub-line.
- **Protected part (the reason for deferral):**
  - `.claude/CLAUDE.md`: the D7 note in `## Session migration and PR close-out checklist` reads "any labelled version token on the `Current truth` line disagrees with that surface's live header". Reword "on the `Current truth` line" to "on the `Version snapshot` sub-line of the `Current truth` block", so the convention-guard matches the fixed D7.
- **QA:** pre-push guard + two HA verifiers (a PR-time-check behaviour change); confirm D7 now flags a deliberately-stale token in the fixture and passes on the reconciled handoff. Rotate §3.22 to DONE on apply.

### 9. [TODO §3.12] Bidirectional See-Also parity gate (new gate 70)

- **Why deferred (2026-07-15 overnight):** adding a gate increments the gate count (69 to 70), which ripples into gate-count prose across surfaces INCLUDING the protected `.claude/CLAUDE.md` (and possibly the pack), so the count-consistency update needs a protected edit; also high-touch, better applied attended.
- **Design:** a new `tools/lint-see-also-parity.py` (gate 70): for each skill A whose `## See Also` lists skill B as a "Related skill" link, assert B's See Also links back to A (per `skill-authoring-discipline` step 6; gate 32 checks only `derives_from`, gate 41 the README tree, gate 44 step-parity, none check See-Also reciprocity). Directly mechanizable. Guard-first: it must pass on the CURRENT skills, so first census the existing skills' See-Also "Related skill" links for any non-reciprocal pair and fix those (or the gate cannot ship green).
- **Surfaces (audit-gate-change completeness, gate 35 + gate 39):** the new linter + wiring in all four surfaces (`.github/workflows/quality.yml`, `tools/run_all_audits.sh`, `.pre-commit-config.yaml`, the `governance/specification-audit-programme.md` §5 grouped-list + §6 inventory-table row + §6 detailed narrative), a regression fixture (a reciprocal-pass + a one-way-fail case), and the module docstring. PLUS the gate-count bump 69 to 70 everywhere cited (README, spec, `.claude/CLAUDE.md` where it cites the raw count, tool docstrings), grepped at bare-token width across ALL file types and verified by gate 39.
- **QA:** guard-first (land the gate green on current skills) + two HA verifiers; full 69-to-70 count-ripple bare-token grep. Rotate §3.12 to DONE on apply. **STALE-NUMBER NOTE (2026-07-18):** this item was staged before gates 70 (sibling-stub-guard) and 71 (stdlib-only) shipped, so its "gate 70" / "69-to-70" figures are stale; at apply the new gate is **72** and the count ripple is **71-to-72**. The applier recomputes the gate number + count from the live inventory.

### 11. [TODO §1.15a part (b)] Cross-repo write-guard CLAUDE.md convention line

- **Why deferred (2026-07-18 overnight):** part (a), the mechanical `tools/repo-guard.sh` wrapper + its regression test, SHIPPED non-protected (in the §1.15a PR). Part (b) is the standing project-CLAUDE.md discipline line, which is a protected `.claude/CLAUDE.md` edit.
- **Prepared content (apply at daytime):** add a standing discipline line to `.claude/CLAUDE.md` (near the AIQT self-reminder / RM-10 unpiped-verification conventions): "Before every Write/Edit and every repo-mutating git command across the colocated repos (`grc_library` / `grc_library_ref` / `grc_library_scratch` / `grc_library_private`), confirm the target repo matches intent, `git rev-parse --show-toplevel` for git (or route the command through `tools/repo-guard.sh <repo> -- <cmd>`, which refuses on a mismatch), and the absolute-path prefix for Write/Edit; prefix git sequences with an explicit `cd /home/jposluns/<repo> &&`." Rotate §1.15a to DONE on apply (part (a) already shipped).
- **QA:** `lint-language.py` on the new CLAUDE.md prose before commit; per-PR `/validate-pr` + `/retro`. Non-protected half (the wrapper + test) already covered by its own PR.

---

_Empty of items = nothing deferred. Add an item whenever an overnight task turns out to need a
protected-file edit; draft its content here rather than deferring it as a bare pointer._
