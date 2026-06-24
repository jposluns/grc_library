# Session Handoff

**Purpose.** This file is the single resume point for a new Claude Code session. It is refreshed at every PR close-out so that opening a fresh session and continuing requires only one instruction from the maintainer (see "How to resume"). It exists because long sessions degrade (context dilution, lossy compaction, state drift, error compounding); a fresh session that rebuilds state from this file plus the durable repo artefacts is more reliable than a long one running on accumulated memory. The mechanisms and mitigations are written up generically in [`.working/session-length-considerations.md`](session-length-considerations.md). This file is maintainer working state, exempt from corpus audit gates per the `.working/` exemption.

This is an **as-of-last-refresh snapshot**, not a live-HEAD claim. Versions and counts drift forward as work advances; always verify against live files before relying on them.

## How to resume (the one command)

In a new session, the maintainer sends only: **`/resume`** (or "read `.working/session-handoff.md` and continue").

On `/resume`, the assistant:
1. Reads this file in full, including the **"Known environment behaviours"** section below.
2. Reads `.claude/CLAUDE.md` (the PRIMORDIAL RULE and project disciplines), the most recent few `CHANGELOG.md` entries, and **[`.working/third-party-issues.md`](third-party-issues.md)**.
3. Runs `git rev-parse --is-shallow-repository` (unshallow with `git fetch --unshallow` if `true`, **before any history-aware audit**), then `tools/run_all_audits.sh` to confirm the corpus is green, and `git log --oneline -5` to confirm HEAD.
4. Verifies the version/count snapshot below against live files.
5. **Runs a full corpus-wide `/validate` as the first substantive task** — the loop-break compensating control for whatever session-closing handoff PR last closed (which skips its trailing `/validate-pr` + `/retro`). The next such sweep is **Sweep 40**. (Sweep 39 already ran at this session's resume, covering the #313/#314 deltas because the prior session paused without a session-closing handoff PR; it found and fixed two pre-existing matrix inconsistencies in close-out PR #315.) Routes any findings to the backlog.
6. Continues from "Next actions" below.

## Next actions (the queue for the next session)

The 2026-06-24 work is complete and merged through **#318**. The resume session ran Sweep 39 (#315), recovered the multi-session orchestration design record + queued the §4.11 codification track (#316), shipped FR-167 batch 3 (Dev-security matrix, 17 docs, #317), and completed DD-4/DD-5 TLS 1.3 (#318). The remaining backlog is **M content clusters** plus the larger FR-167 batches. Re-read [`../TODO.md`](../TODO.md) live; it is the source of truth. Effort-ordered:

- **M content clusters (dispositions recorded in TODO where noted):**
  - **DD-8 — CPPA-as-live scrub** (`M, M`): scrub the live-regime sense CPPA→PIPEDA in [`security/procedure-security-incident-response.md`](../security/procedure-security-incident-response.md):176/:182, the document-index Frameworks tags for the three already-scrubbed docs, and [`risk/standard-enterprise-risk-management.md`](../risk/standard-enterprise-risk-management.md):255; triage softer framework-list mentions; **PRESERVE the US-annex "CPPA = California Privacy Protection Agency" sense** (the edge case). One coherent sweep PR.
  - The **High-severity content items** FR-73 (AI ethics independence), FR-58 (inheritance vocabulary), FR-140 (adopter starter-set count divergence + Tier 1 omissions; the "6th artefact" sub-part already closed in #303), FR-145 (two AI-security standards: keep both + crosswalk, verify overlap at action time).
  - The **Medium content items** FR-15, FR-23, FR-24, FR-63, FR-74, FR-99, FR-154 (several are deliberately-thin baselines; calibrate before "fixing", FR-154 explicitly says so).
  - The **P4 process/meta items** (§4.2 effort-sizing convention, §4.3 standard-version-upgrade process, §4.4 pack language coverage, §4.6 QA-cadence mechanical gate, §4.10 TODO/DONE rotation gate, §4.8 retro-log open loops).
- **S remaining (mostly blocked/needs-scoping):** **FR-62** (AI jurisdiction annexes; likely needs scoping, defer if it balloons past S), **Sweep 3 follow-up** (manual term/identifier consistency pass), **B2** + **DD-10** (both egress-gated; attempt the fetch, defer if 403/blocked, NEVER fabricate). **R1** was closed won't-move (#307); **R2** (the 6-file citation-cluster relocation) is deferred with a convention-conflict note in TODO and **needs a maintainer decision** (active-corpus citers + two linters hardcode the paths; a `.working/` move conflicts with the no-`.working/`-link convention).
- **Larger tracks (deliberately scheduled, OUT of the routine batch):** FR-167 (comprehensive matrix; batch 1 Architecture #275, batch 2 Risk #313, batch 3 Dev-security #317 done; **next batch 4 = supply-chain, 18 docs**, then resilience 22, operations 27, compliance 30, governance 31, security 34, ai 34, privacy 42), the High[critical] net-new privacy/governance docs (FR-30/31/32/34, FR-70/71/72/73), the L/XL items, and the **§4.11 multi-session / multi-worker orchestration codification track** (maintainer-scheduled; default after P1/P2; design record in [`design-decisions.md`](design-decisions.md)).

The maintainer-directed running order (2026-06-23) remains: FR-167, then the deferred-decision work, then smallest-items-in-batches. Maintainer direction supersedes at any time. **Maintainer (2026-06-24) chose DD-4/DD-5 as the next-after-#317 item (done #318); the next deferred-decision item is DD-8.**

**Pending maintainer action (not executable in the assistant's environment):** two stale remote branches are verified content-in-main and safe to delete, but the git proxy here rejects ref deletions and the GitHub MCP has no delete-branch tool: `claude/resume-review-h95prg` (`da8e051` recovered to main #316; `9e4fa87` superseded) and `update-contributors` (`AUTHORS.md` already byte-identical on main). Delete via the GitHub UI or `git push origin --delete` from an environment that accepts ref deletions.

**Worker-brief-template guard-rail candidates surfaced this session (queued, not yet applied):** (1) a target doc's OWN self-cited control codes may be mislabeled (verify against the reference, do not propagate); (2) AICM codes are not CCM v4.1; (3) after any per-document Version bump, regenerate taxonomy/portal/scorecard BEFORE the commit (#317/#318 `/retro`s).

## This session's work (2026-06-24) — read before continuing

**Update (resume session, post-narrative):** after the two-part day below, the prior session continued to ship #313 (FR-167 batch 2) and #314 (project-governance separation spec, which closed R2), then paused without a session-closing handoff PR. This resume session ran Sweep 39 (the loop-break control covering the #313/#314 deltas) and shipped close-out #315. The narrative below covers the morning continuation through #310 only.

A two-part day. **Overnight run** (autonomous, maintainer asleep): shipped #301 (Sweep 36 close-out, CCM/AICM citation-residual completion), #302 (gate-count word-form), #303 (Day-1-floor option A), #304 (R3 relocation), and prepared #305 (loop-break generalization into the pack) which could not be merged then because the GitHub MCP server disconnected after #304. **Morning continuation** (this session, resumed via `/resume` with the maintainer awake; the screenshot of the prior session surfaced the unmerged #305):

- Opened and merged **#305** (once the MCP reconnected) — the loop-break-generalize pack-layer change, carrying the batched #304 QA rows.
- Ran **Sweep 37** (the #305 loop-break compensating control): corpus clean except the two pre-known operations-file CCM v4.0 domain-name residuals → fixed in **#306** (F1 cloud-baseline "Infrastructure Security"; F2 physical-security cited the wrong control I&S-03="Network Security", resolved by the maintainer to the DCS physical-access trio).
- **#307**: morning-processed the overnight file (reset to stub), closed relocation R1 won't-move.
- **#308 (S4)** + **#309 (S5)**: the gate-48 enhancement pair — S4 section-aware + cross-catalogue title check (catches the I&S-07 confusion); S5 bare-domain-code check (the family-list/crosswalk residual class), precision-first and FP-free (maintainer chose "build now, precision-first" after the FP surface was surfaced).
- **#310 (DD-2/3/11)**: risk-vocabulary harmonization to the canonical ERM scale across four risk-scoring docs (impact-5 → Catastrophic; likelihood Moderate → Medium; rating-top "Critical" preserved; the corpus-wide grep caught a 4th carrier beyond the 3 named).

**Quality held throughout** — every non-handoff PR got a formal `/validate-pr` (all 0 in-window findings after the apply-time fixes) + `/retro`; the post-commit audits caught the expected bookkeeping consequences (artefact regen, TODO sweep-cursor, link-coverage) and they were fixed before push, never reaching CI as a surprise.

## State snapshot (as of 2026-06-24, post-#318; session-closing handoff PR #319)

- **Branch**: this session's substantive work merged through **#318**. The session-closing handoff PR (**#319**) lands the batched #318 `/validate-pr` + `/retro` rows and this handoff refresh on `main`, so a fresh `/resume` rebuilds from `main` with no unmerged feature-branch state to recover. The local `claude/awesome-noether-yeynzj` remote branch was auto-pruned on #318's merge and re-pushed for #319.
- **HEAD**: `main` at **#319** once the handoff PR merges (verify with `git log -1`). Immediately prior: #318 (DD-4/DD-5 TLS 1.3), #317 (FR-167 batch 3 Dev-security matrix), #316 (orchestration design-record recovery + §4.11), #315 (Sweep 39 close-out), #314 (project-governance separation).
- **Versions** (post-#319): library `2026.06.297`, pack `1.49.8`, README `1.9.168`. (Verify against `README.md`.)
- **Audit programme**: **48 numbered gates** + **3 PR-only delta gates (D1/D2/D3)**; all passing on `main`. Gate 48 (CSA CCM/AICM citation-accuracy) has the S4 section-aware + cross-catalogue title check and the S5 bare-domain-code check. Governance rules: **10**. Skills: **15** (6 paired). Slash commands: **8**. The matrix now has a comprehensive Dev-security section (17 docs, #317).
- **Last merged**: **#318** (DD-4/DD-5 TLS 1.3: `go.md` TLS example to TLS 1.3, supplier-questionnaire Q5.4 raised, pack `1.49.8`). Before it: #317 (FR-167 b3), #316 (orchestration recovery + §4.11), #315 (Sweep 39), #314, #313, #312. (#319 is this session-closing handoff PR.)
- **`/validate` cadence**: **Sweep 39** ran at this session's resume (covering the #313/#314 deltas, since the prior session paused without a handoff PR; close-out #315, 2 pre-existing matrix findings fixed). The next `/resume` runs **Sweep 40** (the loop-break compensating control for this session-closing handoff PR #319, which skips its own trailing `/validate-pr` + `/retro`).

## Open decisions awaiting maintainer

- **R2 relocation**: CLOSED by principle in #314 (the project-governance separation spec classifies the 6-file citation-verification cluster as project governance, so it migrates in Phase 1). The Phase-1 migration, the queued directional-dependency gate (§7.3), and the 2 deferred §5.3 classifications are now forward-looking TODO items, not open decisions awaiting the maintainer.
- The larger-track decisions (FR-167 batches 2..N, the High[critical] net-new docs, the L/XL items) remain queued and scheduled deliberately.

## Trust-recovery state

The trust-recovery suite (`/full-qa` + `/fitness` r2) ran and the maintainer **signed off** (2026-06-22). Codification COMPLETE. Not re-triggered since; quality held throughout the 2026-06-24 overnight run, morning continuation, and the resume session (Sweep 38 + close-out #312, both warnings fixed first try, post-commit + pre-push green).

## Known environment behaviours (read before assuming working-tree state)

- **The stop-hook auto-commits AND pushes uncommitted changes on turn-end.** The working tree is auto-persisted to the feature branch; verify `git log` rather than assuming edits are held locally.
- **The squash-merge commit on `main` shows locally as `E noreply@github.com`** (GitHub's own merge commit; Verified in the GitHub UI, not locally verifiable). After syncing the branch to `main` the tip equals `origin/main`; **do NOT `git commit --amend`** it (that rewrites merged `main` history). Set `git config user.email noreply@anthropic.com && git config user.name Claude` so your own feature-branch commits are attributed correctly.
- **A squash-merge makes the local feature branch diverge from `main`** (the squash commit is new; the local pre-squash commit is its content but a different SHA), so `git merge --ff-only origin/main` fails after a merge; use `git reset --hard origin/main` to re-sync the feature branch (the local commit's content is in the squash, preserved in reflog).
- **The GitHub MCP server can disconnect mid-session** (it did 2026-06-24 after #304, blocking #305's open/merge). `git push` over HTTPS keeps working; only the MCP-routed GitHub-API operations are affected. If `mcp__github__*` tools vanish: keep committing and pushing via `git`, record the pending-merge state in the handoff, and resume the PR lifecycle when MCP returns. Do NOT merge by any non-MCP path. Full writeup: [`third-party-issues.md`](third-party-issues.md).
- **The commit-signing server can 503** — distinguish from a real defect (gates 31/40 pass on the real corpus while gate 36's failures are `git commit` subprocess errors); re-run after a pause. Full writeup: [`third-party-issues.md`](third-party-issues.md).
- **The clone may start shallow**; `git fetch --unshallow` before any history-aware audit (gates 31/40).

## Standing disciplines (do not drift from these)

- **PRIMORDIAL RULE**: Quality > Speed > Cost; integrity absolute. Emit the integrity-check line at task start, before commit, before completion claims, and at tension points.
- **Post-commit audit**: after every commit, run `tools/run_all_audits.sh` standalone before pushing; never chain commit and push. Before push, also `tools/run-pr-time-checks.sh`.
- **`lint-language` pre-flight on new pack prose** before the first commit (catches em-dashes / British `-ise`). (Relevant for DD-4/5's `go.md` rewrite.)
- **Pre-commit dash-grep on new root `CHANGELOG.md` lines** (`grep -nP "\xe2\x80\x93|\xe2\x80\x94"`): the D3 dash gate is PR-time only, so a late-assembled CHANGELOG entry can slip an em-dash that surfaces at pre-push; grep the added lines before the first commit.
- **Grep-after-wiring / convention change**: after editing a restated-across-surfaces value, `grep` the OLD form across the full changed file AND every sibling surface; zero hits before commit.
- **Corpus-wide-grep / special-case-the-edge / find-every-carrier**: a mechanical bulk edit (a rename, a relabel, a title alignment) must verify EVERY adjacent field, special-case the known edge cases (e.g. preserve rating "Critical" while fixing impact-5; the DD-2/3/11 grep found a 4th carrier beyond the 3 named), and search corpus-wide for the OLD form, not apply one convenient rule uniformly.
- **Sweep close-out bookkeeping triplet**: a `/validate` close-out PR regenerates the generated artefacts (after per-doc version bumps), advances the TODO sweep cursor (gate 45 + the gate-36 TodoStaleness regression both enforce it), and bumps `validate-sweeps/history.md`'s own Version. The post-commit audit catches all three; doing them pre-commit avoids the fail-then-fix loop.
- **60-second** paired fallback timer after every `subscribe_pr_activity`.
- **Per-PR QA**: formal `/validate-pr` (Subagent A) + `/retro` after every merge; no skip, no abbreviation. **One standing exception**: the session-closing handoff PR skips both (loop-break); the compensating control is the corpus-wide `/validate` that `/resume` runs first. (This exception is now generalized into the pack layer, #305.)
- **PR close-out checklist** (the degradation guard): prior PR's `/validate-pr` row AND `/retro` row both batched in; closed TODO items rotated to DONE (every path-shaped code span in a CHANGELOG entry linked, changed or merely mentioned); stale-count check if an enumerated collection changed; session-handoff.md refreshed.
- **Self-assess for degradation / session-continuation SOP**: continue while quality holds; wind down on actual drift/hallucination/mistakes (not caught by the QA layer), OR when a very large series remains and we want no mid-operation interruption. Steady-state misses the per-PR `/validate-pr` catches are NOT drift. (This session wound down here, at a clean boundary after a long, productive run, with the large M-cluster series queued for a fresh session.)
- **Compute-don't-ask**: before surfacing a question, apply a "can I compute/verify this myself?" gate; surface only the result or a decision that genuinely needs maintainer judgement. (Counterpart: surface a genuine design tradeoff before building, as S5's FP surface was surfaced with named options rather than guessed.)

## Refresh discipline

This file is refreshed at every PR close-out (post-merge), as part of the recursion-avoidance batch that carries the validate-pr/retro rows into the next PR.
