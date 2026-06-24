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

## State snapshot (as of 2026-06-23, after PR #291 — the new session resumed via `/resume`, ran Sweep 33, shipped #289 + #290 + #291, then closed on a degradation signal)

- **Branch**: the **session-closing handoff PR #292** carries the **#291 `/validate-pr` finding-fix** (index-register BYOD descriptor "MAM controls" → "MAM and MDM controls", register `1.27.31` → `1.27.32`), the **#291 `/validate-pr` (1 in-window note, fixed) history row + detail file**, the **#291 `/retro` row**, and this handoff refresh. Once #292 merges, a fresh `/resume` rebuilds state from `main`. The new session develops on whatever branch its mandate assigns.
- **HEAD**: `ba8274b` PR #291 (PR-F security/crypto bundle) on `main` (verify with `git log -1`). Immediately prior: #290 (PR-E), #289 (Sweep 33 close-out), #288 (handoff), #287 (PR-C), #286 (Sweep 32 close-out).
- **Versions** (post-#292): library `2026.06.270`, pack `1.49.3` (unchanged), README `1.9.141`. Per-doc bumped in #291 (PR-F): policy-encryption-and-key-management `1.3.4`, policy-byod `1.1.0`, standard-developer-security-requirements `1.1.0`, procedure-patch-management `1.0.2`, breach-response procedure `1.4.12`, template-recovery-runbook `1.0.3`. In #292: register-document-index-and-classification `1.27.32`. (Verify against `README.md`.)
- **Audit programme**: **47 numbered gates** + **3 PR-only delta gates (D1/D2/D3)**; all passing on `main`. Governance rules: **10**. Skills: **15** (6 paired). Slash commands: **8**.
- **Last merged**: **#291** (PR-F: 6-item security/crypto bundle, FR-153/BYOD/FR-90/84/85/86; all directional choices maintainer-confirmed; `/validate-pr` found 1 in-window cross-ref note, fixed in #292). Before it: **#290** (PR-E), **#289** (Sweep 33 close-out). The **#291 `/validate-pr` + `/retro` rows** are carried by #292.
- **`/validate` cadence**: Sweep 33 ran this session (the `/resume` loop-break control for handoff PR #288); the next `/resume` runs **Sweep 34** (the loop-break compensating control for the session-closing handoff PR #292, which skips its trailing `/validate-pr` + `/retro`).

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

This session (2026-06-23) **resumed via `/resume`** and ran a long, productive turn: the loop-break **Sweep 33 `/validate`** (1 in-window note fixed in **#289**, 0 out-of-window), then **PR-E (#290)**, the 10-item adopter/docs-UX bundle (FR-64/65/66/78/152/69/68/156/157/158, all directional choices maintainer-confirmed, 0 `/validate-pr` findings), then **PR-F (#291)**, the 6-item security/crypto bundle (FR-153 PBKDF2 with the previously-unspecified HMAC hash now named SHA-256/600,000; the BYOD MDM/MAM structural rewrite; FR-90 browser hardening; FR-84/85/86). #291's `/validate-pr` cross-reference check surfaced one in-window note (the index register's BYOD descriptor "MAM controls" gone stale), fixed in this session-closing handoff PR #292. The session **closes here on a degradation signal**: the #291 `/retro` recorded a 2nd-occurrence redundant-re-ask (the four PR-F directional questions were re-asked after they had already been answered and #291 opened) late in a three-merge turn (#289/#290/#291 + the sweep + QA cycles). Per the self-assess-for-degradation discipline, the right move was to stop and land a small session-closing handoff PR (#292: the #291 QA rows + the index-register finding-fix + this refresh) and resume fresh for PR-H, rather than push a fourth substantive PR through a degrading turn. Per the handoff-PR exception (CLAUDE.md PR-workflow step 5a), #292 skips its own trailing `/validate-pr` + `/retro` (loop-break); the compensating control is the corpus-wide Sweep 34 the next `/resume` runs first.

## Trust-recovery state

The trust-recovery suite (`/full-qa` + `/fitness` r2) ran and the maintainer **signed off** (2026-06-22). **Codification COMPLETE**: `deep-qa-review` + `/full-qa` (#244); PRIMORDIAL RULE (#245); ninth rule `trust-recovery-escalation.md` (#246); session-migration + `/resume` (#247); handoff-PR loop-break (#249); routing revision (#252/#253); `/trust-recovery` wrapper (#254); **`/guardrails` structural-review skill (#257)**; **`project-integrity.md` 10th rule (#258)**. **Criticals COMPLETE**: all 6 H[critical] (FR-134..139) shipped this overnight run (#260..#265). Records: `.working/full-qa/2026-06-22-iter1.md`, `.working/fitness-reviews/2026-06-22-r2.md`.

## Next actions (queue, for the new session)

0. **Full corpus-wide `/validate` first** (Sweep 34; the loop-break compensating control for the session-closing handoff PR #292, "How to resume" step 5). Route findings to the backlog. Re-examines the whole corpus including the #289-#291 deltas. (Sweep 33 ran in this session; its 1 finding was fixed in #289.)
1. **Resume the XS/S batch-reduction** (maintainer-directed 2026-06-23). The maintainer grouped all XS/S items in P1-P3 into ~10 coherent PRs and wants them shipped, **asking the maintainer for each directional choice with a recommended option** (standing instruction). **DONE: PR-A #282 (FR-142/143; FR-144 re-scoped), PR-B #283 + #284 (FR-161/162/163/146), PR-C #287 (FR-147/148/101/102/100/77/83), PR-E #290 (FR-64/65/66/78/152/69/68/156/157/158), PR-F #291 (FR-153/BYOD/FR-90/84/85/86, all directional choices maintainer-confirmed).** **PR-H is the immediate next** (carries the batched #291 `/validate-pr` + `/retro` rows once #292 merges, OR they are already carried by #292; PR-H starts clean). Remaining PRs, in order:
   - **PR-H** (governance/registers + ESG): FR-120, B2 (5 EDPB/WP citations), FR-155, **FR-53 (DECIDED: document the Classification-vs-Confidentiality distinction, non-breaking)**, FR-109, DD-6/7 (7-yr AI-log retention + schedule row), FR-75, FR-76.
   - **PR-I** (cross-doc consistency + generated/FYI): FR-12, FR-149, FR-150, FR-151, Sweep-3 follow-up, FR-159, FR-160, FR-165.
   - **PR-J** (working-state relocations, mechanical, no maintainer input): the 3 relocations (sweep-preflight-exemptions.json; citation-verification cluster; register-main-branch-protection.md). ⚠ relocation effort often exceeds XS (sibling-refs + index/taxonomy/portal regen).
   - **PR-K1** (pack prose, no input): generalize the handoff-PR QA loop-break into the `validation-sweep-pr-scoped` SKILL + `ai-assistant-workflow-disciplines.md`. Run `lint-language.py` pre-flight before first commit.
   - **PR-K2** (DD-10): addyosmani upstream skill-count reconcile — **needs web egress**; attempt the fetch, surface + defer if blocked.
   - **FR-144 template PR** (re-scoped from PR-A): create an adopter-fillable breach-notification regulator register template + wire into [`../privacy/procedure-data-protection-and-privacy-breach-response.md`](../privacy/procedure-data-protection-and-privacy-breach-response.md) §6. Ask the maintainer the template home/shape.
   - **FR-62**: recalibrate from S to L (content-creation: new AI jurisdiction annexes) and route to P5.8; NOT a small-batch item.
2. **After the XS/S batch**: the larger tracks — DD-2/3/11 (risk-vocab, M), DD-4/5 (TLS, M), DD-8 (CPPA scrub, M), DD-12 (NET→IVS + corpus-wide PR.IP migration, L), the S1/S2/S3 gates, **FR-167 batches 2..N** (comprehensive matrix, smallest-first: risk 15 → dev-security 17 → supply-chain 18 → resilience 22 → operations 27 → compliance 30 → governance 31 → security 34 → ai 34 → privacy 42, then the 8 partials; fold the two #275 follow-ups into batch 2), and the High[critical] net-new docs (FR-30/31/32/34, FR-70/71/72/73) + FR-145.
3. **Process candidates** (this session's `/retro`s + TODO 4.8/4.9/4.10): the TODO/DONE rotation gate (4.10); the hallucination-metrics-table refresh (4.9); consolidate one close-out-checklist line — before the first commit, after all prose + version bumps, run `lint-changelog-link-coverage.py` + a Version-bump scan + (if any per-doc Version changed) `build-taxonomy.py`/`build-portal.py`; and extend the bare-token contradiction search to every touched doc's sample/example tables after a field/enum reconcile (the #283→#284 lesson).

## Open decisions awaiting maintainer

- **Per-PR directional choices for the remaining XS/S batch** (PR-E/F/H/I and the FR-144 template): the maintainer's standing instruction is to be **asked each time, with a recommended option, for any reconcile-direction choice**. FR-53 is already decided (document the distinction). The session asks the rest as it reaches each PR. (PR-C #287's directional choices are resolved.)
- The larger-track decisions (DD-2/3/11, DD-4/5, DD-8, DD-12, S1/S2/S3, FR-167, FR-145) are RESOLVED in disposition (queued work; see the triage block above and TODO).
- Effort-first batching rule for the remaining P2 backlog — still open if/when reached.
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
- **Self-assess for degradation / session-continuation SOP** (maintainer-clarified 2026-06-24): **continue while quality holds; wind down only on actual drift, hallucination, or mistakes, OR when a very large series of items remains and we want to ensure there is no interruption in the middle.** Do NOT preemptively swap sessions at a mere merge count: a preventative swap is safe but yields no metrics on the real degradation threshold, and the maintainer wants that threshold observed. The wind-down trigger is observed quality decline (a rising slip rate, a hallucination, a mistake that is not caught by the QA layer), not turn length per se. Steady-state misses that the per-PR `/validate-pr` catches (e.g. the missed-parallel-carrier class seen at #294 and #296) are NOT drift — they are the constant miss-rate the QA layer exists to catch; report them honestly in `/retro` as data points and continue. (Supersedes the earlier "surface a refresh recommendation on a long session" phrasing, which over-weighted merge count.)
- **Compute-don't-ask** (maintainer-flagged 2026-06-23): before surfacing a question to the maintainer, apply a "can I compute/verify this myself?" gate — if the answer is a count, a file-existence check, a grep-able value, or anything derivable from the repo, compute it and surface only the *result* (or a decision that genuinely needs the maintainer's judgement), never the raw question. Asking the maintainer to confirm a number you can count is a failure to track. Distinct from legitimate clarify-before-acting (intent, scope, authorial choices). Candidate addition to the `clarify-before-acting` rule.

## Refresh discipline

This file is refreshed at every PR close-out (post-merge), as part of the same recursion-avoidance batch that carries the validate-pr/retro rows into the next PR. The refresh updates the state snapshot, the last-merged list, the next-actions queue, the open-decisions list, and the known-environment-behaviours and standing-disciplines sections.
