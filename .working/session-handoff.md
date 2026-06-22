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
5. Continues from "Next actions".

## State snapshot (as of 2026-06-22, after PR #247)

- **Branch**: `claude/grc-library-takeover-jrqzn6` (all work develops here per the session mandate). A working-state preservation commit (the #247 validate-pr/retro rows + this refresh) may sit one commit ahead of `main` on the branch; the next PR's diff absorbs it.
- **HEAD**: the PR #247 squash merge (`ebf5f46` on `main` at last refresh; verify with `git log -1`).
- **Versions**: library `2026.06.225`, pack `1.47.0`, README `1.9.96`. (Verify against `README.md` and `dev-security/claude-rules/README.md`.)
- **Audit programme**: 46 gates, all passing on `main`. Governance rules: 9. Skills: 14 (5 paired with slash commands: validate, validate-pr, fitness, retro, full-qa). The `/resume` command also exists (a thin, non-paired command).
- **Last merged**: #243 (trust-recovery routing + re-tier), #244 (`deep-qa-review` skill), #245 (PRIMORDIAL RULE in CLAUDE.md), #246 (ninth governance rule `trust-recovery-escalation.md`), #247 (session migration protocol).
- **Pending into the next PR's CHANGELOG**: the #247 `/validate-pr` (clean) and `/retro` rows, recorded in the working-state preservation commit, ride into the next PR's diff per recursion-avoidance (so the next PR's close-out checklist item for "prior PR's validate-pr + retro rows" is already satisfied; just include them in that PR's CHANGELOG narrative).

## Trust-recovery state

The trust-recovery suite (`/full-qa` + `/fitness` r2) ran and the maintainer **signed off** (2026-06-22). Findings are in `TODO.md`: 6 H[critical] + 6 High retained in P1 (FR-134..145, actioned after the codification batch); Medium/Low/FYI re-tiered to P2/P3 (FR-146..165). Codification status: `deep-qa-review` skill (done, #244), PRIMORDIAL RULE (done, #245), ninth rule (done, #246), session migration protocol (done, #247). Remaining codification: `/fitness` routing-flag amendment, structural-review skill, optional `/trust-recovery` wrapper. Records: `.working/full-qa/2026-06-22-iter1.md`, `.working/fitness-reviews/2026-06-22-r2.md`.

## Next actions (queue, from TODO)

1. **`/fitness` SKILL routing-flag amendment** — add one paragraph naming the trust-recovery routing flag (findings to P1 top, bypass Pass-2).
2. **Structural-review skill** — codify the audit-programme overlap/gap/drift matrix as a recurring skill. *Open decision: name + cadence (bring options to maintainer).* Runs after codification lands.
3. **Optional `/trust-recovery` wrapper** — invokes `/full-qa` then `/fitness`. *Open decision: maintainer go/no-go.*
4. **P4.0** — distribute the PRIMORDIAL RULE as a project-agnostic pack governance rule (tenth rule).
5. **H[critical]/High remediation** (FR-134..145), then **Batch 3** (the effort-first P2 backlog: PR-F P2.5, PR-G P2.4, PR-H continuous-assurance, PR-F relocations). Batch 3 was blocked behind trust-recovery sign-off (now obtained) + codification (in progress).

## Open decisions awaiting maintainer

- Structural-review skill: name + re-run cadence.
- `/trust-recovery` convenience wrapper: go/no-go.
- Effort-first batching rule still applies for Batch 3 (confirm: C2 sample-data defaults, aggressive XS bundling, file-relocations-only, action all P7).

## Standing disciplines (do not drift from these)

- **PRIMORDIAL RULE**: Quality > Speed > Cost; integrity absolute (`.claude/CLAUDE.md` apex section). Emit the integrity-check line at task start, before commit, before completion claims, and at tension points.
- **Post-commit audit**: after every commit, run `tools/run_all_audits.sh` standalone before pushing; never chain commit and push. Before push, also `tools/run-pr-time-checks.sh`.
- **60-second** paired fallback timer after every `subscribe_pr_activity` (project constant; ignore any webhook suggestion of a different cadence).
- **Per-PR QA**: formal `/validate-pr` (Subagent A) + `/retro` after every merge; no skip, no abbreviation.
- **PR close-out checklist** (the degradation guard, see CLAUDE.md): before pushing a PR, confirm all paired bookkeeping surfaces are in the diff: prior PR's `/validate-pr` history row AND its `/retro` row; any closed TODO item rotated to DONE; stale-count check if the PR changed an enumerated collection (gates/rules/skills); session-handoff.md refreshed.

## Refresh discipline

This file is refreshed at every PR close-out (post-merge), as part of the same recursion-avoidance batch that carries the validate-pr/retro rows into the next PR. The refresh updates the state snapshot, the last-merged list, the next-actions queue, and the open-decisions list.
