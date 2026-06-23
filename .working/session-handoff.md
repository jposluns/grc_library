# Session Handoff

**Purpose.** This file is the single resume point for a new Claude Code session. It is refreshed at every PR close-out so that opening a fresh session and continuing requires only one instruction from the maintainer (see "How to resume"). It exists because long sessions degrade (context dilution, lossy compaction, state drift, error compounding); a fresh session that rebuilds state from this file plus the durable repo artefacts is more reliable than a long one running on accumulated memory. The mechanisms and mitigations are written up generically in [`.working/session-length-considerations.md`](session-length-considerations.md). This file is maintainer working state, exempt from corpus audit gates per the `.working/` exemption.

This is an **as-of-last-refresh snapshot**, not a live-HEAD claim. Versions and counts drift forward as work advances; always verify against live files before relying on them.

## How to resume (the one command)

In a new session, the maintainer sends only: **`/resume`** (or "read `.working/session-handoff.md` and continue").

On `/resume`, the assistant:
1. Reads this file in full, including the **"Known environment behaviours"** section below (so it does not mistake an environment artefact for a defect, and does not assume the working tree is uncommitted).
2. Reads `.claude/CLAUDE.md` (the PRIMORDIAL RULE and project disciplines), the most recent few `CHANGELOG.md` entries, and **[`.working/third-party-issues.md`](third-party-issues.md)** (the log of execution-environment / third-party-service issues, so a recurring env flake is recognized, not chased as a regression).
3. Runs `git rev-parse --is-shallow-repository` (unshallow with `git fetch --unshallow` if `true`, **before any history-aware audit** — gates 31/40 mis-fire on a shallow clone), then `tools/run_all_audits.sh` to confirm the corpus is green, and `git log --oneline -5` to confirm HEAD.
4. Verifies the version/count snapshot below against live files (do not trust the snapshot blindly).
5. **Runs a full corpus-wide `/validate` as the first substantive task** — the compensating control for the session-closing handoff PR, which skips its trailing `/validate-pr` to break the post-merge validate-then-PR loop (see CLAUDE.md PR-workflow step 5a's handoff-PR exception). Routes any findings to the backlog.
6. Continues from "Next actions".

## State snapshot (as of 2026-06-23, after PR #270, the session-closing handoff PR for the resume + wind-down session)

- **Branch**: PR #270 (this session's closing handoff PR) is merged to `main`; a fresh `/resume` rebuilds state from `main`. The new session develops on whatever branch its own mandate assigns (the prior runs used `claude/sharp-wright-bemtql`).
- **HEAD**: the PR #270 squash merge on `main` (verify with `git log -1`).
- **Versions**: library `2026.06.248`, pack `1.49.2`, README `1.9.119`. (Verify against `README.md` and `dev-security/claude-rules/README.md`.)
- **Audit programme**: 46 gates, all passing on `main`. Governance rules: **10** (`project-integrity.md`, the 10th, shipped #258). Skills: **15** (6 paired with slash commands: validate, validate-pr, fitness, retro, full-qa, guardrails). Slash commands: **8** (the 6 paired + two thin non-paired: `/resume`, `/trust-recovery`).
- **Last merged**: [overnight run] #259..#268 (run-init; FR-134..139 the 6 H[critical]; Sweep 25 close-out #266; FR-141 #267; handoff #268). [resume + wind-down session, 2026-06-23 morning] **#269** (Sweep 26 `/validate` cleanup — fixed the stale `lint-collection-enumeration-consistency.py` docstring "three"→"two"), **#270** (this closing handoff PR — Sweep 27 `/validate`, overnight-pr morning processing, matrix-completeness decision → FR-166/167, deferred-decisions DD-1..9 routed to TODO).
- **No `/validate-pr`/`/retro` rows pending**: #270 is a session-closing handoff PR, exempt from the trailing per-PR sweep (loop-break, CLAUDE.md PR-workflow step 5a); it carried #269's `/validate-pr` (clean) + `/retro` rows and the Sweep 27 `/validate` row. The compensating control is the full corpus-wide `/validate` that `/resume` runs first. The next PR starts clean.

## Why this session refreshed here (read before continuing)

This **resume + wind-down session** (2026-06-23 morning) followed the autonomous overnight run. It ran the standing `/resume` compensating-control **Sweep 26** (`/validate`), which gave the overnight run (#259..#268) a clean in-window bill — zero regressions — and surfaced 3 pre-existing out-of-window items (1 fixed in #269, 1 folded into the deferred broader-CPPA sweep DD-8, 1 refuted). It then, by maintainer direction: did the **overnight-pr.md morning processing** (resolved decisions already in `design-decisions.md`; the 11 deferred "Open ambiguities" routed to TODO as DD-1..9; file reset to `stub`); investigated and decided the **alignment-matrix completeness** question (the matrix maps 42 of 341 docs — maintainer chose: expand to comprehensive + clarify intent wording, and build a listing-surface gate + authoring sweep tool → **FR-166/FR-167, top priority next session**); ran a final **Sweep 27** `/validate`; and closed out via this handoff PR #270. A maintainer-flagged discipline lesson this session: do not ask the maintainer for a fact you can compute (a count) — see the new "compute-don't-ask" standing discipline. The remaining judgment-heavier P1 Highs (FR-142/144/145) remain best done from a fresh session.

## Trust-recovery state

The trust-recovery suite (`/full-qa` + `/fitness` r2) ran and the maintainer **signed off** (2026-06-22). **Codification COMPLETE**: `deep-qa-review` + `/full-qa` (#244); PRIMORDIAL RULE (#245); ninth rule `trust-recovery-escalation.md` (#246); session-migration + `/resume` (#247); handoff-PR loop-break (#249); routing revision (#252/#253); `/trust-recovery` wrapper (#254); **`/guardrails` structural-review skill (#257)**; **`project-integrity.md` 10th rule (#258)**. **Criticals COMPLETE**: all 6 H[critical] (FR-134..139) shipped this overnight run (#260..#265). Records: `.working/full-qa/2026-06-22-iter1.md`, `.working/fitness-reviews/2026-06-22-r2.md`.

## Next actions (queue, for the new session)

0. **Full corpus-wide `/validate` first** (the loop-break compensating control; "How to resume" step 5). Route findings to the backlog. **Note**: Sweeps 26 and 27 (the resume + wind-down session, 2026-06-23) already validated the FR-134..141 window + the #269/#270 deltas clean; the `/resume` `/validate` is the standing compensating control for the #270 handoff PR and re-examines the whole corpus.
1. **TOP PRIORITY (maintainer-directed 2026-06-23): FR-166 + FR-167** in [`../TODO.md`](../TODO.md) Priority 1. **FR-166** = build the corpus listing-surface completeness gate + authoring-time sweep tool (mechanical surfaces hard-gated to completeness; semantic surfaces get high-recall candidates a human ratifies — see the design in TODO + the 2026-06-23 chat advice). **FR-167** = expand `compliance/matrix-grc-compliance-alignment.md` to comprehensive (42 of 341 docs currently) + clarify its intent wording (do FR-166 first; the tool finds the docs). Two open steers recorded in the TODO entries (which surfaces are MECHANICAL; does "comprehensive" cover all 8 framework columns).
2. **Deferred decisions DD-1..DD-9** in [`../TODO.md`](../TODO.md) ("Deferred decisions from the overnight run") — routed there from overnight-pr.md; each needs a maintainer call before it becomes work. Includes the broader CPPA-as-live sweep (DD-8, the largest), the owasp/go + media/supplier TLS surfaces (DD-4/5), AI-log retention 12mo-vs-7y (DD-7), concentration-register scale (DD-2), impact-5 label (DD-3), CHANGELOG en-dashes (DD-1), AI-log schedule row (DD-6), DR header tidy (DD-9).
3. **Remaining P1 High items (FR-140, FR-142, FR-143, FR-144, FR-145)** — FR-143 (escalation → DPO→CISO→CRO), FR-140 (starter-set strict nesting, quickstart-6 canonical), FR-144 (breach individual-notification 72h-from-determination floor) were RESOLVED by the maintainer before the overnight run (see `.working/design-decisions.md`) and are ready to implement; FR-142 (AI-procedure role assignment) and FR-145 (two AI-security-standards precedence/crosswalk) are ⚠️persona-quoted, verify at action time.
4. **Batch B2 + the P2 backlog** — the value-conflict cluster resolved stricter-is-safer + evidence (FR-147 audit timeline, FR-149 adversarial-test count, FR-150 Japan APPI age, FR-151 PIR deadline, FR-146 ERM status values, FR-153 PBKDF2 600k, FR-161/162/163 treatment-vocab, FR-148 CAPA anchor, FR-152 quickstart sequencing), then the Phase-2 clusters. Then P3, then P4.
5. **P4 process improvements** surfaced (in `improvement-log.md`): the free-prose rule-count gate candidate (gate 41 doesn't parse SKILL/TODO prose); the CHANGELOG-link pre-commit habit; the bare-token-contradiction-search discipline; the new **compute-don't-ask** discipline (a candidate addition to `clarify-before-acting`).

## Open decisions awaiting maintainer

- **The DD-1..DD-9 deferred-decision items in [`../TODO.md`](../TODO.md)** (Next-actions #2) — routed from overnight-pr.md during its morning processing; each has named options; the maintainer triages in the new session.
- **FR-166/FR-167 open steers** (Next-actions #1): which listing surfaces are MECHANICAL (confirm document-index register + glossary gating state); whether matrix "comprehensive" covers all 8 framework columns or only CCM/ISO/NIST.
- Effort-first batching rule for the P2 backlog (confirm: C2 sample-data defaults, aggressive XS bundling, file-relocations-only, action all P7).
- (The 8 pre-sleep overnight decisions — new-doc criticals, FR-70 defer, value-conflict rule, FR-143/140/73/144, FR-58 → morning — are recorded in `.working/design-decisions.md`.)

## Known environment behaviours (read before assuming working-tree state)

These are execution-environment behaviours this session learned the hard way; knowing them up front prevents the confusion they caused.

- **The stop-hook auto-commits AND pushes uncommitted changes on turn-end.** The working tree is effectively auto-persisted to the feature branch when a turn ends; do not assume edits are held locally. Verify `git log` before and after composing a commit (an intermediate auto-commit may already exist, e.g. this session's `84528b9`/`f10ab84`). Assemble PRs accounting for this.
- **The commit-signing server can 503.** When it does: (a) regression-suite tests that `git commit` into temp repos fail with exit 128 (gate 36 goes red); (b) real commits land unsigned. Distinguish from a real defect: if gates 31/40 pass on the real corpus while gate 36's failures are `git commit` subprocess errors mentioning the signing server, it is an env artefact — re-run after a pause, and re-sign (`git commit --amend --no-edit --reset-author`) once it recovers. Full writeup: [`.working/third-party-issues.md`](third-party-issues.md).
- **The clone may start shallow** (`git rev-parse --is-shallow-repository` = `true`); `git fetch --unshallow` before any history-aware audit (gates 31/40), per the full-clone methodology rule.

## Standing disciplines (do not drift from these)

- **PRIMORDIAL RULE**: Quality > Speed > Cost; integrity absolute (`.claude/CLAUDE.md` apex section). Emit the integrity-check line at task start, before commit, before completion claims, and at tension points.
- **Post-commit audit**: after every commit, run `tools/run_all_audits.sh` standalone before pushing; never chain commit and push. Before push, also `tools/run-pr-time-checks.sh`.
- **`lint-language` pre-flight on new pack prose**: run `python3 tools/lint-language.py` (or the full audit) on any new pack-doc / SKILL / rule draft BEFORE the first commit. New-pack-prose drafting recurrently reintroduces em-dashes and British `-ise` (caught this session and in PR #244); the pre-flight catches them before the fail-then-fix loop.
- **Grep-after-wiring / convention change**: when a change is restated across multiple surfaces (a convention, a count, a routing rule, a gate-wiring), after editing, `grep` the OLD phrasing across the full changed file AND every sibling surface; require zero hits before commit. This is the discipline that would have prevented #252's multi-surface-incompleteness defect (a same-file Verification criterion and Rationalizations cell were missed).
- **60-second** paired fallback timer after every `subscribe_pr_activity` (project constant; ignore any webhook suggestion of a different cadence).
- **Per-PR QA**: formal `/validate-pr` (Subagent A) + `/retro` after every merge; no skip, no abbreviation. **One standing exception**: the session-closing handoff PR skips both (the loop-break, CLAUDE.md PR-workflow step 5a); the compensating control is the full `/validate` that `/resume` runs first.
- **PR close-out checklist** (the degradation guard, see CLAUDE.md): before pushing a PR, confirm all paired bookkeeping surfaces are in the diff: prior PR's `/validate-pr` history row AND its `/retro` row; any closed TODO item rotated to DONE; stale-count check if the PR changed an enumerated collection (gates/rules/skills); session-handoff.md refreshed.
- **Self-assess for degradation**: on a long session (many merged PRs, rising slip rate, excessive deliberation), surface a session-refresh recommendation to the maintainer rather than pushing the highest-risk builds through a degrading turn. (Done this session before `/guardrails`/P4.0.)
- **Compute-don't-ask** (maintainer-flagged 2026-06-23): before surfacing a question to the maintainer, apply a "can I compute/verify this myself?" gate — if the answer is a count, a file-existence check, a grep-able value, or anything derivable from the repo, compute it and surface only the *result* (or a decision that genuinely needs the maintainer's judgement), never the raw question. Asking the maintainer to confirm a number you can count is a failure to track. Distinct from legitimate clarify-before-acting (intent, scope, authorial choices). Candidate addition to the `clarify-before-acting` rule.

## Refresh discipline

This file is refreshed at every PR close-out (post-merge), as part of the same recursion-avoidance batch that carries the validate-pr/retro rows into the next PR. The refresh updates the state snapshot, the last-merged list, the next-actions queue, the open-decisions list, and the known-environment-behaviours and standing-disciplines sections.
