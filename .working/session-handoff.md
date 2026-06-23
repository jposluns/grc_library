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

## State snapshot (as of 2026-06-23, session-closing handoff after the DD-triage + Track-1-start session)

- **Branch**: the session-closing handoff PR is merged to `main`; a fresh `/resume` rebuilds state from `main`. The new session develops on whatever branch its mandate assigns.
- **HEAD**: the handoff PR squash merge on `main` (verify with `git log -1`). Immediately prior: #277, #278, #279.
- **Versions**: library `2026.06.257`, pack `1.49.3` (unchanged this session), README `1.9.128`, matrix `compliance/matrix-grc-compliance-alignment.md` `1.1.0`, audit-programme spec `1.16.0` (#278 bumped it), DR plan `1.3.2` (#279). (Verify against `README.md` / `dev-security/claude-rules/README.md`.)
- **Audit programme**: **47 numbered gates** + **3 PR-only delta gates (D1/D2/D3)** — **D3 (CHANGELOG-dash-on-PR) is new this session (#278)**; all passing on `main`. Governance rules: **10**. Skills: **15** (6 paired). Slash commands: **8**.
- **Last merged this session**: **#277** (Sweep 30 close-out: five "Cloud Controls Matrix v5"→v4.1 citation fixes + gate-27 broadened with the spelled-out form + regression test); **#278** (DD-1 new-entries-only: delta gate D3 so new CHANGELOG entries are dash-free, history untouched); **#279** (DD-9: DR backup-requirements header → "All systems" + the three #278 `/validate-pr` close-out fixes). The **#279 `/validate-pr` + `/retro` rows + the DD-9 TODO→DONE rotation** are carried by THIS handoff PR (committed on the branch, landed on `main` by the handoff merge).
- **`/validate` cadence**: Sweep 30 ran this session (the `/resume` loop-break control); the next `/resume` runs **Sweep 31**.

## All 16 maintainer decisions triaged this session (dispositions in TODO)

The maintainer triaged the full open-decision set 2026-06-23 (DD-1..DD-12, the S1/S2/S3 gate candidates, B2, FR-145, the FR-167 domain order). Dispositions are recorded in [`../TODO.md`](../TODO.md) (the "Deferred decisions ... TRIAGED" resolutions block, §4.5, the B2 line, the FR-145 line, the FR-167 line). **Shipped already: DD-1 (#278), DD-9 (#279).** The rest are now queued work, NOT open decisions. Summary of what each became:
- **DD-2/3/11** → harmonize the three risk-scoring docs fully to the canonical ERM scale (one PR).
- **DD-4/5** → pack stays ASVS-accurate (rewrite `go.md` to 1.3); raise the two governed surfaces (media-handling, supplier questionnaire) to 1.3.
- **DD-6/7** → canonical 7-year AI-log retention; reconcile the checklist's "12 months" up + add an AI-decision-logs row to the retention schedule.
- **DD-8** → one coherent CPPA-as-live scrub sweep (preserve the US-annex "California Privacy Protection Agency" sense).
- **DD-10** → verify the upstream addyosmani skill count via web, then align README + setup-generator (needs a web fetch).
- **DD-12** → fix NET→IVS in the matrix AND migrate `PR.IP`→strict CSF 2.0 codes corpus-wide (the PR.IP half is large, corpus-wide).
- **Gates** → build ALL THREE (S1 retention-consistency, S2 role-definition-consistency, S3 citation-precision).
- **B2** → add the five EDPB/WP soft-law citations to the canonical-citations register (dedicated S PR).
- **FR-145** → keep both AI security standards; add a scope/precedence note + crosswalk.
- **FR-167** → domain order = smallest-first (risk → dev-security → supply-chain → resilience → operations → compliance → governance → security → ai → privacy), then the 8 partials.

## Why this session refreshed here (read before continuing)

This **DD-triage + Track-1-start session** (2026-06-23) opened with `/resume`, ran **Sweep 30** (the loop-break `/validate`; it caught a NEW out-of-window finding, five hallucinated "Cloud Controls Matrix v5" citations evading the gate's abbreviated-form check, fixed + gate-broadened in #277), then the maintainer triaged all 16 open decisions, and the session began **Track 1** (the quick-win track): DD-1 (#278) and DD-9 (#279) shipped. The session paused (this handoff) on a degradation self-assessment: three PR cycles deep with the TODO/DONE rotation miss recurring two PRs running (DD-1 caught by #278's sweep, DD-9 by #279's), with the two remaining quick-wins (B2 citations, DD-10 web-verify) being the most error-prone for a long turn. **Maintainer directive (2026-06-23): in the new session, after completing the first task, STOP and assess with the maintainer how best to proceed — do NOT auto-run through the queue.**

## Trust-recovery state

The trust-recovery suite (`/full-qa` + `/fitness` r2) ran and the maintainer **signed off** (2026-06-22). **Codification COMPLETE**: `deep-qa-review` + `/full-qa` (#244); PRIMORDIAL RULE (#245); ninth rule `trust-recovery-escalation.md` (#246); session-migration + `/resume` (#247); handoff-PR loop-break (#249); routing revision (#252/#253); `/trust-recovery` wrapper (#254); **`/guardrails` structural-review skill (#257)**; **`project-integrity.md` 10th rule (#258)**. **Criticals COMPLETE**: all 6 H[critical] (FR-134..139) shipped this overnight run (#260..#265). Records: `.working/full-qa/2026-06-22-iter1.md`, `.working/fitness-reviews/2026-06-22-r2.md`.

## Next actions (queue, for the new session)

0. **Full corpus-wide `/validate` first** (Sweep 31; the loop-break compensating control, "How to resume" step 5). Route findings to the backlog. It re-examines the whole corpus including the #277/#278/#279 deltas.
1. **MAINTAINER DIRECTIVE (2026-06-23): after completing the first task, STOP and assess with the maintainer how best to proceed.** The "first task" is the mandatory Sweep 31 `/validate` (item 0); after it, do NOT auto-run through the queue — surface a checkpoint and let the maintainer direct. The queue below is the menu to assess against, ordered by the tracks agreed this session.
2. **Track 1 (quick-wins) remaining**: **B2** (add the five EDPB/WP soft-law citations to [`../governance/register-canonical-citations.md`](../governance/register-canonical-citations.md) — Guidelines 07/2020, 3/2018, 28/2024, Opinion 05/2014, WP248 rev.01; dedicated S PR); **DD-10** (verify the upstream addyosmani skill count via web fetch, then align README + `setup-generator-prompt.md`). DD-10 needs network egress; if the environment blocks it, surface and defer.
3. **Track 2 (consistency sweeps)**: **DD-2/3/11** (harmonize the 3 risk docs to the canonical ERM scale); **DD-6/7** (AI-log 7-year retention + schedule-schedule row) — pairs with **S1** gate; **DD-4/5** (TLS: rewrite `go.md` to 1.3, raise the 2 governed surfaces); **DD-8** (one coherent CPPA-as-live scrub sweep).
4. **Track 3 (gates)**: build **S1** (retention-consistency, with DD-6/7), **S2** (role-definition-consistency), **S3** (citation-precision) — one gate per PR (lint + 4-surface wiring + regression fixture each).
5. **Track 4 (large)**: **DD-12** — NET→IVS (matrix-local, tiny) + the **corpus-wide `PR.IP`→CSF 2.0 migration** (large; PR.IP is used well beyond the matrix; scope carefully).
6. **Track 5 (TOP substantive priority): FR-167 batches 2..N** — comprehensive matrix expansion, **smallest-first** (risk 15 → dev-security 17 → supply-chain 18 → resilience 22 → operations 27 → compliance 30 → governance 31 → security 34 → ai 34 → privacy 42), then the 8 partials. Scope + framework convention RESOLVED; ai/dev-security are NEW sections. **Two #275 follow-ups to fold into the first FR-167 batch**: (a) document `N/A` in the matrix legend at `compliance/matrix-grc-compliance-alignment.md`:36; (b) refresh the FR-167 item in [`../TODO.md`](../TODO.md) for batch-1 progress. Per-batch method: research agents produce candidates → orchestrator reads each doc + verifies EVERY cell at apply-time. The worker-brief-template (v1.1.0) carries the FR-167 framework-code crib + control-identifier-verification rail.
7. **Track 6 (independent)**: High[critical] net-new docs (FR-30/31/32/34 privacy templates, FR-70/71/72/73) and **FR-145** (AI-standards precedence note + crosswalk; ⚠️ verify overlap at action time). No prior decision needed.
8. **New P4 process candidate (from #279 `/retro`)**: a **mechanical TODO/DONE rotation gate** — flag any TODO resolution marked "SHIPPED in #N" whose id still appears as an open backlog item or is absent from `.working/DONE.md`. Escalated from a convention reminder because the rotation miss recurred twice running (#278 DD-1, #279 DD-9). Plus the standing P4 candidates in [`improvement-log.md`](improvement-log.md): the denylist/idiom-variant-coverage gate-authoring note (#277); the broaden-the-count-gate word-form extension; the free-prose rule-count gate.

## Open decisions awaiting maintainer

- **The post-first-task checkpoint** (Next-actions #1): the maintainer wants to assess how to proceed after the new session's first task (Sweep 31). This is the live open item.
- All 16 of the prior session's open decisions (DD-1..DD-12, S1/S2/S3, B2, FR-145, FR-167 order) are **RESOLVED** (dispositions in TODO); they are queued work now, not open questions.
- Effort-first batching rule for the P2 backlog (confirm: C2 sample-data defaults, aggressive XS bundling, file-relocations-only, action all P7) — still open if/when the P2 backlog is reached.
- (The 8 pre-sleep overnight decisions are recorded in `.working/design-decisions.md`.)

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
