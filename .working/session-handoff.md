# Session Handoff

**Purpose.** This file is the single resume point for a new Claude Code session. It is refreshed at every PR close-out so that opening a fresh session and continuing requires only one instruction from the maintainer (see "How to resume"). It exists because long sessions degrade (context dilution, lossy compaction, state drift, error compounding); a fresh session that rebuilds state from this file plus the durable repo artefacts is more reliable than a long one running on accumulated memory. The mechanisms and mitigations are written up generically in [`.working/session-length-considerations.md`](session-length-considerations.md). This file is maintainer working state, exempt from corpus audit gates per the `.working/` exemption.

This is an **as-of-last-refresh snapshot**, not a live-HEAD claim. Versions and counts drift forward as work advances; always verify against live files before relying on them.

## How to resume (the one command)

In a new session, the maintainer sends only: **`/resume`** (or "read `.working/session-handoff.md` and continue").

On `/resume`, the assistant:
1. Reads this file in full.
2. Reads `.claude/CLAUDE.md` (the PRIMORDIAL RULE and project disciplines) and the most recent few `CHANGELOG.md` entries.
3. Runs `git rev-parse --is-shallow-repository` (unshallow if `true`), then `tools/run_all_audits.sh` to confirm the corpus is green, and `git log --oneline -5` to confirm HEAD.
4. Verifies the version/count snapshot below against live files (do not trust the snapshot blindly).
5. **Runs a full corpus-wide `/validate` as the first substantive task** — the compensating control for the session-closing handoff PR, which skips its trailing `/validate-pr` to break the post-merge validate-then-PR loop (see CLAUDE.md PR-workflow step 5a's handoff-PR exception). Routes any findings to the backlog.
6. Continues from "Next actions".

## State snapshot (as of 2026-06-22, after PR #250)

- **Branch**: `claude/resume-oojneh` (this session's mandate; all work develops here). PR #250 is merged to `main`; the working branch was reset to `origin/main` post-merge, so the next PR builds on the merged state.
- **HEAD**: the PR #250 squash merge on `main` (`7b06816`; verify with `git log -1`).
- **Versions**: library `2026.06.228`, pack `1.47.0`, README `1.9.99`. (Verify against `README.md` and `dev-security/claude-rules/README.md`.)
- **Audit programme**: 46 gates, all passing on `main`. Governance rules: 9. Skills: 14 (5 paired with slash commands: validate, validate-pr, fitness, retro, full-qa). The `/resume` command also exists (a thin, non-paired command).
- **Last merged**: #246 (ninth governance rule `trust-recovery-escalation.md`), #247 (session migration protocol), #248 (session-length lesson + closing handoff), #249 (handoff-PR QA loop-break), #250 (`/resume` Sweep 23 close-out: corpus-wide `/validate` compensating control + one stale-count fix).
- **Pending `/validate-pr`/`/retro` rows to batch into the NEXT PR**: PR #250's `/validate-pr` (0 findings) and `/retro` rows are written to `.working/validate-pr/history.md` (Version `1.2.54`) and `.working/improvement-log.md` (Version `1.0.33`) but NOT yet committed — they batch into the next substantive PR per recursion-avoidance, alongside this handoff refresh. (The earlier "no rows pending" state was specific to the #248/#249 handoff-PR exemption; #250 is a normal PR and produced normal rows.)

## Trust-recovery state

The trust-recovery suite (`/full-qa` + `/fitness` r2) ran and the maintainer **signed off** (2026-06-22). Findings are in `TODO.md`: 6 H[critical] + 6 High retained in P1 (FR-134..145, actioned after the codification batch); Medium/Low/FYI re-tiered to P2/P3 (FR-146..165). Codification status: `deep-qa-review` skill (done, #244), PRIMORDIAL RULE (done, #245), ninth rule (done, #246), session migration protocol (done, #247). Remaining codification: `/fitness` routing-flag amendment, structural-review skill, optional `/trust-recovery` wrapper. Records: `.working/full-qa/2026-06-22-iter1.md`, `.working/fitness-reviews/2026-06-22-r2.md`.

## Next actions (queue, from TODO)

0. **Full corpus-wide `/validate` first** (the loop-break compensating control; see "How to resume" step 5). **DONE this session**: Sweep 23 (full A/B/C dispatch), 1 in-window note (stale "eight governance rules" at `.claude/CLAUDE.md:263`) fixed in PR #250; cross-document drift cluster confirmed-but-already-tracked, deduped not re-routed.
0a. **Maintainer-requested P1–P4 analysis + decisions (2026-06-22, this session): DONE.** Decisions locked and captured in TODO annotations + `.working/design-decisions.md`. Summary: 6 H[critical] canonical values accepted as recommended; TLS 1.3 everywhere incl `operations:184` unconditionally; trust-recovery routing → severity-tiered (crit+high→P1, med+low→P2), "routing flag only"; P4.0 = `project-integrity.md` 10th rule standalone after codification; P4.1 = skill-family + prescriptive-only + existing-pack bump; P4.4 = JS/TS+Go+Java baseline, point-to-OWASP; P4.5 = build S1, defer S2/S3.
1. **Trust-recovery routing-convention revision (NEXT substantive PR)** — severity-tiered routing across ~8 surfaces (rule + mirror; `deep-qa-review` SKILL + `/full-qa`; `library-fitness-review` SKILL [the routing-flag amendment folds in] + `/fitness`; pack `CLAUDE.md` + project `.claude/CLAUDE.md` bullets; check pack README). Pack rule/SKILLs stay project-agnostic; project P1/P2 mapping in `.claude/CLAUDE.md`+TODO. Pack version bump. See TODO trust-recovery codification item + design-decisions.
2. **Structural-review skill** — codify the audit-programme overlap/gap/drift matrix as a recurring skill. *Still open: name + cadence (not decided this session).*
3. **Optional `/trust-recovery` wrapper** — invokes `/full-qa` then `/fitness`. *Still open: go/no-go (not decided this session).*
4. **P4.0** — distribute the PRIMORDIAL RULE as `project-integrity.md` (10th rule), standalone PR after the codification batch.
5. **H[critical]/High remediation** (FR-134..145, canonical values now locked — see TODO), then **Batch 3** (effort-first P2 backlog). Per maintainer sequencing, criticals come *after* the codification batch.

## Open decisions awaiting maintainer

- Structural-review skill: name + re-run cadence (not decided this session).
- `/trust-recovery` convenience wrapper: go/no-go (not decided this session).
- Effort-first batching rule still applies for Batch 3 (confirm: C2 sample-data defaults, aggressive XS bundling, file-relocations-only, action all P7).

## Standing disciplines (do not drift from these)

- **PRIMORDIAL RULE**: Quality > Speed > Cost; integrity absolute (`.claude/CLAUDE.md` apex section). Emit the integrity-check line at task start, before commit, before completion claims, and at tension points.
- **Post-commit audit**: after every commit, run `tools/run_all_audits.sh` standalone before pushing; never chain commit and push. Before push, also `tools/run-pr-time-checks.sh`.
- **60-second** paired fallback timer after every `subscribe_pr_activity` (project constant; ignore any webhook suggestion of a different cadence).
- **Per-PR QA**: formal `/validate-pr` (Subagent A) + `/retro` after every merge; no skip, no abbreviation. **One standing exception**: the session-closing handoff PR skips both (the loop-break, CLAUDE.md PR-workflow step 5a); the compensating control is the full `/validate` that `/resume` runs first.
- **PR close-out checklist** (the degradation guard, see CLAUDE.md): before pushing a PR, confirm all paired bookkeeping surfaces are in the diff: prior PR's `/validate-pr` history row AND its `/retro` row; any closed TODO item rotated to DONE; stale-count check if the PR changed an enumerated collection (gates/rules/skills); session-handoff.md refreshed.

## Refresh discipline

This file is refreshed at every PR close-out (post-merge), as part of the same recursion-avoidance batch that carries the validate-pr/retro rows into the next PR. The refresh updates the state snapshot, the last-merged list, the next-actions queue, and the open-decisions list.
