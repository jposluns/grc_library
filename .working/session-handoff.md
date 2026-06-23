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

## State snapshot (as of 2026-06-23, after PR #255, the session-closing handoff PR)

- **Branch**: PR #255 (this session's closing handoff PR) is merged to `main`; a fresh `/resume` rebuilds state from `main`. The new session develops on whatever branch its own mandate assigns (this session used `claude/resume-oojneh`).
- **HEAD**: the PR #255 squash merge on `main` (verify with `git log -1`).
- **Versions**: library `2026.06.233`, pack `1.47.2`, README `1.9.104`. (Verify against `README.md` and `dev-security/claude-rules/README.md`.)
- **Audit programme**: 46 gates, all passing on `main`. Governance rules: **9** (the 10th, `project-integrity.md`, is queued as P4.0 — next session). Skills: **14** (5 paired with slash commands: validate, validate-pr, fitness, retro, full-qa). Slash commands: **7** (the 5 paired + two thin non-paired: `/resume` and `/trust-recovery`).
- **Last merged**: #250 (`/resume` Sweep 23 close-out), #251 (P1–P4 decision capture), #252 (trust-recovery routing convention → severity-tiered), #253 (routing-revision completion in deep-qa SKILL + third-party-issues log), #254 (`/trust-recovery` wrapper), #255 (this closing handoff PR + resume-hardening guardrails).
- **No `/validate-pr`/`/retro` rows pending**: #255 is a session-closing handoff PR, exempt from the trailing per-PR sweep (loop-break, CLAUDE.md PR-workflow step 5a); it carried #254's rows. The compensating control is the full corpus-wide `/validate` that `/resume` runs first. The next PR starts clean.

## Why this session refreshed here (read before continuing)

This session ran long (resume + Sweep 23 + PRs #250–#255). Late in the turn the slip rate rose: three em-dash / British-`-ise` slips in new pack prose, and one multi-surface-incompleteness defect that reached a merged PR (#252 shipped a self-contradicting SKILL, caught by its own `/validate-pr`, fixed in #253). All were caught by the gates / `lint-language` / `/validate-pr` (nothing defective shipped to `main` uncaught), but the rising slip rate plus the two highest-multi-surface-wiring builds still ahead (`/guardrails`, `project-integrity.md`) made a refresh the quality-first choice (maintainer-endorsed 2026-06-23). The next session does those two builds with clean context and the hardened guardrails below.

## Trust-recovery state

The trust-recovery suite (`/full-qa` + `/fitness` r2) ran and the maintainer **signed off** (2026-06-22). Findings in `TODO.md`: 6 H[critical] + 6 High retained in P1 (FR-134..145, canonical values now **locked** — see the TODO P1 block note); Medium/Low/FYI re-tiered to P2/P3 (FR-146..165). **Codification status (nearly complete)**: `deep-qa-review` skill + `/full-qa` (#244); PRIMORDIAL RULE (#245); ninth rule `trust-recovery-escalation.md` (#246); session migration protocol + `/resume` (#247); handoff-PR loop-break (#249); **routing-flag amendment folded into the severity-tiered routing revision (#252/#253)**; **`/trust-recovery` wrapper (#254)**. **Remaining codification**: the **`/guardrails`** structural-review skill (name + cadence DECIDED — see Next actions). Then P4.0. Records: `.working/full-qa/2026-06-22-iter1.md`, `.working/fitness-reviews/2026-06-22-r2.md`.

## Next actions (queue, for the new session)

0. **Full corpus-wide `/validate` first** (the loop-break compensating control; "How to resume" step 5). Route findings to the backlog.
1. **`/guardrails` structural-review skill (DECIDED, build it)** — the "guard rail review" of the governance machinery's structural integrity (overlap / gap / drift across rules, skills, gates, and their four wiring surfaces). **Name LOCKED**: slash command `/guardrails`, skill `guardrail-review`. **Cadence**: maintainer-triggered + an auto-prompt after any PR that adds/removes/renames a rule, skill, or gate. Full multi-surface build: new SKILL + command + gate-44 PAIRS registration + step-parity + pack-skills enumeration (14 → 15) + pack version bump. **Apply the grep-after-wiring discipline** (see Known environment behaviours) given this is exactly the multi-surface shape that slipped this session.
2. **P4.0 — `project-integrity.md` (10th governance rule)** — distribute the PRIMORDIAL RULE as a project-agnostic pack rule `dev-security/claude-rules/governance/project-integrity.md`, standalone PR. Closes the `project-integrity` forward-reference (currently a code-span in TODO P4.0, zero dangling-link debt). Wire across the four enumeration surfaces + `.claude/rules/` mirror + rule-count (collection-enumeration gate). This is the maintainer's target-before-this-session-boundary item, deferred to the new session for clean-context quality.
3. **H[critical]/High criticals remediation (FR-134..145)** — canonical values LOCKED (see TODO P1 block note: FR-134 procedure scoring; FR-135 TLS 1.3 everywhere incl `operations:184`; FR-136 retention-schedule authoritative+tiered; FR-137 DSAR 3y; FR-138 scrub CPPA→PIPEDA Schedule 1; FR-139 1h RPO binding). Per maintainer sequencing, criticals come AFTER the codification batch (i.e., after #1 and #2).
4. **Batch 3** — the effort-first P2 backlog (PR-F P2.5, PR-G P2.4, PR-H continuous-assurance, PR-F relocations). Plus P4.1/P4.4/P4.5 (shapes decided — see TODO annotations).

## Open decisions awaiting maintainer

- Effort-first batching rule for Batch 3 (confirm: C2 sample-data defaults, aggressive XS bundling, file-relocations-only, action all P7).
- (The structural-review skill name/cadence and the `/trust-recovery` wrapper go/no-go were DECIDED this session; the 6 H[critical] canonical values, TLS, routing convention, and P4.0/P4.1/P4.4/P4.5 shapes are all LOCKED in TODO + design-decisions.)

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

## Refresh discipline

This file is refreshed at every PR close-out (post-merge), as part of the same recursion-avoidance batch that carries the validate-pr/retro rows into the next PR. The refresh updates the state snapshot, the last-merged list, the next-actions queue, the open-decisions list, and the known-environment-behaviours and standing-disciplines sections.
