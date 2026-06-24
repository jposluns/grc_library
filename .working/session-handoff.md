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
5. **Runs a full corpus-wide `/validate` as the first substantive task** (this will be **Sweep 36** — the loop-break compensating control for the session-closing handoff PR #300, which skips its trailing `/validate-pr` + `/retro`). Routes any findings to the backlog.
6. Continues from "Next actions" — **which this time is the OVERNIGHT MISSION below.**

## ⏰ OVERNIGHT MISSION (the goal for the next session) — read this first

**Maintainer authorization (2026-06-24):** the next session is an **autonomous overnight run of about 8 hours**. The maintainer types `/resume`, then sleeps. **Goal: close out ALL the XS and S items, and as many of the Medium (M) items as possible, from [`TODO.md`](../TODO.md), for the maintainer to review in the morning.** This is a standing maintainer-authorized autonomous window (not an abbreviation of QA — every per-PR discipline below still runs).

### Work-list (effort-ordered, lowest-first per the TODO convention). Snapshot as of this handoff; re-read TODO live, it is the source of truth.

**XS (4) — do these first, quick mechanical wins:**
- The **3 working-state relocations** (TODO P-listing-surface area, the old "relocation bundle R1/R2/R3"): `tools/sweep-preflight-exemptions.json` → `.working/validate-sweeps/`; the 6-file citation-verification cluster → `.working/citation-verifications/`; `governance/register-main-branch-protection.md` → `.working/`. Follow the **PR #116 precedent** (slim moved-doc metadata, update `**Repository Path:**`, delete index/README rows in the SAME PR, update tool load-path constants, regenerate taxonomy/portal/scorecard, leave historical CHANGELOG refs). **R2 (citation cluster) is the heavy/risky one — its own PR, extra grep-completeness care; full ripple map is in the PRIOR handoff (git history of this file, the #297 version) and in the relevant tools' load-path constants.** Do R1/R2/R3 as **3 separate PRs** (always-split).
- **Day-1-floor risk-artefact drift** (TODO, `(M, XS)`): the two six-artefact-floor definitions disagree on the sixth artefact. Maintainer pre-stated recommendation is option (A) (make `risk/policy-enterprise-governance-and-risk-management.md` canonical in both); proceed with (A) unless re-reading shows it wrong, and flag in the PR for morning review.

**S (6):**
- **Generalize the handoff-PR QA loop-break into the pack layer** `(M, S)`: name the session-closing-handoff-PR exception in the `validation-sweep-pr-scoped` SKILL + `ai-assistant-workflow-disciplines.md`. Run `lint-language.py` pre-flight (new pack prose). Pack version bump.
- **S4 gate-48 section-aware title check** `(S)` (TODO §4.5, surfaced by #299 `/validate-pr`): extend `tools/lint-ccm-aicm-citations.py` to check CCM-section rows against `CCM_V41` and AICM-section rows against `AICM_V11` (catches the I&S-07 / IAM-11 cross-catalogue divergence the union-dict check misses).
- **FR-62** `(M, S)`: AI jurisdiction annexes absent (cross-references P5.8) — likely needs scoping; if it balloons past S, defer with a note.
- **Sweep 3 follow-up** `(L, S)`: cross-document term/identifier consistency manual pass.
- **B2** `(L, S)` and **DD-10** `(L, S)`: BOTH **egress-gated** (EDPB/WP29 citations; addyosmani upstream skill count). **Attempt the web fetch; if 403/blocked, defer with a note — do NOT fabricate** (no-fabrication discipline). These two may not be closable overnight if egress is blocked, as it has been all recent sessions.

**M (18) — work through as many as possible after XS+S:**
- **Risk-vocabulary harmonization DD-2/DD-3/DD-11** `(M, M)`: one coherent PR to the canonical ERM scale (disposition recorded in TODO).
- **DD-4/DD-5 TLS 1.3** `(M, M)`: rewrite `go.md` coherently to 1.3 + raise the 2 governed surfaces (disposition recorded).
- **DD-8 CPPA-as-live scrub** `(M, M)`: one coherent sweep, PRESERVE the US-annex "CPPA = California Privacy Protection Agency" sense (disposition recorded).
- **FR-58** (inheritance vocabulary), **FR-140** (adopter starter-set divergence — note this overlaps the Day-1-floor XS item; reconcile together), **FR-145** (two AI-security standards, decided: keep both + crosswalk; verify overlap at action time), **FR-73** (AI ethics independence), all `(H, M)` content items.
- **FR-15, FR-23, FR-24, FR-63, FR-74, FR-99, FR-154** `(M, M)` content items (several are deliberately-thin baselines — calibrate before "fixing"; FR-154 explicitly says calibrate first).
- The **P4 process/meta items** with M effort (§4.2, §4.3, §4.4, §4.6, §4.10) as time allows.

### How to run the overnight mission (autonomy with the maintainer asleep)

- **Follow the overnight-work protocol** ([`change-tracking.md`](../dev-security/claude-rules/governance/change-tracking.md) overnight section): at mission start, set [`.working/overnight-pr.md`](overnight-pr.md) `Status: in-flight` and accumulate design decisions, surfaced ambiguities, and morning-review flags there. The morning-processing step (first thing the maintainer's next interaction triggers, or the assistant on request) routes it and resets to `stub`. **Gate 46 fails on `Status: done`**, so leave it `in-flight` while working and only set `done` at the very end if you stop cleanly.
- **Per-PR QA is NOT abbreviated overnight.** Every merged PR gets the formal `/validate-pr` + `/retro` (no skip — the only standing exception is a session-closing handoff PR). Post-commit `run_all_audits.sh` + pre-push `run-pr-time-checks.sh` every PR. CI-green-then-merge via the subscription + 60s-fallback-timer discipline. **Always-split**: one coherent change per PR.
- **Directional choices with the maintainer asleep:** (a) if TODO already records a maintainer disposition (most DD items do), proceed on it; (b) if a NEW directional choice is needed and a wrong guess is bounded to a quick edit, make a **documented sensible default**, state it in the PR description, and add it to a **morning-review list** in `overnight-pr.md`; (c) if a wrong guess would be costly or hard to unwind (a breaking change, a deletion, a public-API or precedence decision), **defer the item to morning** rather than guess. Bias toward shipping the unambiguous items and deferring the genuinely-ambiguous ones; do not block the whole mission on one ambiguous item.
- **No fabrication, ever** — egress-gated citation items defer rather than invent (B2, DD-10).
- **Self-monitor for degradation** per the SOP below: if quality genuinely declines (not just steady-state QA-caught misses), wind down to a clean handoff rather than pushing through.
- **Leave a clear morning-review summary**: what shipped (PR list), what was deferred and why, what needs a maintainer decision, and the updated TODO/DONE state.

## State snapshot (as of 2026-06-24, after the session-closing handoff PR #300)

- **Branch**: the **session-closing handoff PR #300** carries the **#299 `/validate-pr` finding-fix** ([`dev-security/register-compliance-controls-and-gap-register.md`](../dev-security/register-compliance-controls-and-gap-register.md) I&S-07 title `Migration to Hosted Environments` → the CCM v4.1 value `Migration to Cloud Environments`; `1.0.2`→`1.0.3`), the batched **#299 `/validate-pr` row + detail file** and **#299 `/retro` row**, the new TODO item **S4** (gate-48 section-aware check), and this handoff refresh. Once #300 merges, a fresh `/resume` rebuilds state from `main`.
- **HEAD**: `c245c0c` PR #299 on `main` (verify with `git log -1`); #300 merges on top. Immediately prior: #298 (CCM/AICM reconciliation), #297 (prior handoff), #296 (PR-I), #295, #294.
- **Versions** (post-#300): library `2026.06.278`, pack `1.49.4`, README `1.9.149`. (Verify against `README.md`.)
- **Audit programme**: **48 numbered gates** + **3 PR-only delta gates (D1/D2/D3)**; all passing on `main`. **Gate 48 = the new CSA CCM/AICM citation-accuracy audit.** Governance rules: **10**. Skills: **15** (6 paired). Slash commands: **8**.
- **Last merged**: **#299** (gate 48 + gap-register full title alignment). Before it: **#298** (corpus-wide CCM/AICM citation reconciliation grounded in the maintainer-supplied authoritative catalogues), **#297** (prior handoff).
- **`/validate` cadence**: Sweep 35 ran this session (#298 close-out). The next `/resume` runs **Sweep 36** (the loop-break control for handoff PR #300).

## This session's work (2026-06-24, the CCM/AICM session) — read before continuing

This session **resumed via `/resume`**, ran **Sweep 35**, and pivoted entirely to a **maintainer-directed CCM/AICM citation-accuracy programme** triggered by Sweep 35's findings:
- Sweep 35 found A-1 (`GRM`→`GRC` stale CCM domain code in the cross-framework matrix) and B-1 (AI-log retention `12 months`→`7 years`). Verifying A-1 surfaced a **systemic** problem: `GOV` cited as a CCM domain (no such domain) across ~9 docs, plus superseded `IVS` (→`I&S` in v4.1.0), fabricated `NET`, out-of-range `IPY-05`, and AICM at the superseded v1.0.3.
- The **maintainer uploaded the authoritative CSA CCM v4.1.0 and AICM v1.1.0 catalogues** (XLSX + guidance PDFs) and directed a full reconciliation. **Licence note: the catalogues carry an explicit no-redistribution clause**, so they were used only in the session scratchpad (NOT committed); a fair-use index ([`tools/ccm_aicm_reference.py`](../tools/ccm_aicm_reference.py) — domain codes, control-ID ranges, canonical titles, no normative content) is the in-repo durable reference.
- **#298** shipped the corpus-wide reconciliation (GOV→GRC with real A&A/AICM add-backs, IVS→I&S ×34 incl. pack, NET→I&S, IPY-05→IPY-04, AICM v1.0.3→v1.1, CCM v4 tightened to v4.1; 0 residual per a catalogue-derived validator).
- **#299** shipped **gate 48** (`lint-ccm-aicm-citations.py`, domain/range + code-to-title checks, 4-surface wired + regression fixture, count 47→48) backed by the fair-use reference, plus a full v4.1/v1.1 title alignment of the compliance-controls gap register (whose catalogue had been authored against an older CCM version).
- **Quality held** (no drift). The per-PR `/validate-pr` caught one residual each time (the incomplete-mechanical-sweep pattern, now 4 occurrences this session-window: #294/#296/#298/#299) — all steady-state QA-caught, none a rising error rate. The #299 residual (I&S-07 cross-catalogue title) is fixed in this handoff PR #300; the gate-48 section-aware enhancement (TODO S4) is the durable fix.

## On the maintainer's standing licensing question (CCM/AICM/ISO private-repo idea)

The maintainer asked whether storing purchased standards (CCM, AICM, ISO, etc.) in a private GitHub repo would let the assistant reference them for validation without a licence violation. Summary of the answer given (for the overnight session's awareness, not an action item): licences are **not uniform** — NIST (public domain) and OWASP (open) can be stored freely; **CSA CCM/AICM** are "personal, non-commercial, no-redistribution" (a private repo is grey, and the third-party-host + automated-access angle adds risk); **ISO** single-user licences typically **forbid network/server storage** even in a private repo (highest risk). The robust, licence-clean pattern (already instantiated this session) is to store **derived factual reference data** (codes, ranges, clause numbers, canonical titles — the fair-use index the gate consumes), NOT the full normative texts, and to re-supply the full texts per session (scratchpad, ephemeral) for deeper checks. No action queued unless the maintainer revisits it.

## Open decisions awaiting maintainer (for morning review)

- Anything the overnight session defers or defaults will be listed in [`.working/overnight-pr.md`](overnight-pr.md) and in the morning-review summary. The maintainer reviews those in the morning.
- The larger-track decisions (FR-167 batches 2..N, the High[critical] net-new docs FR-30/31/32/34 + FR-70/71/72/73, the L/XL items) remain queued and are OUT of the overnight XS/S/M scope.

## Trust-recovery state

The trust-recovery suite (`/full-qa` + `/fitness` r2) ran and the maintainer **signed off** (2026-06-22). Codification COMPLETE (see prior handoff history). Not re-triggered this session; quality held throughout the CCM/AICM programme.

## Known environment behaviours (read before assuming working-tree state)

- **The stop-hook auto-commits AND pushes uncommitted changes on turn-end.** The working tree is auto-persisted to the feature branch; verify `git log` rather than assuming edits are held locally.
- **The squash-merge commit on `main` shows locally as `E noreply@github.com`** (GitHub's own merge commit; Verified in the GitHub UI, not locally verifiable). After syncing the branch to `main` the tip equals `origin/main`; **do NOT `git commit --amend`** it (that rewrites merged `main` history). Set `git config user.email noreply@anthropic.com && git config user.name Claude` so your own feature-branch commits are attributed correctly.
- **The commit-signing server can 503** — distinguish from a real defect (gates 31/40 pass on the real corpus while gate 36's failures are `git commit` subprocess errors); re-run after a pause. Full writeup: [`.working/third-party-issues.md`](third-party-issues.md).
- **The clone may start shallow**; `git fetch --unshallow` before any history-aware audit (gates 31/40).

## Standing disciplines (do not drift from these)

- **PRIMORDIAL RULE**: Quality > Speed > Cost; integrity absolute. Emit the integrity-check line at task start, before commit, before completion claims, and at tension points.
- **Post-commit audit**: after every commit, run `tools/run_all_audits.sh` standalone before pushing; never chain commit and push. Before push, also `tools/run-pr-time-checks.sh`.
- **`lint-language` pre-flight on new pack prose** before the first commit (catches em-dashes / British `-ise`).
- **Grep-after-wiring / convention change**: after editing a restated-across-surfaces value, `grep` the OLD form across the full changed file AND every sibling surface; zero hits before commit.
- **Corpus-wide-grep / special-case-the-edge discipline** (reinforced by this session's 4-occurrence incomplete-mechanical-sweep pattern): a mechanical bulk edit (a rename, a relabel, a title alignment) must verify EVERY adjacent field and special-case the known edge cases (e.g. the controls whose value differs across two reference sources), not apply one convenient rule uniformly.
- **60-second** paired fallback timer after every `subscribe_pr_activity`.
- **Per-PR QA**: formal `/validate-pr` (Subagent A) + `/retro` after every merge; no skip, no abbreviation. **One standing exception**: the session-closing handoff PR skips both (loop-break); the compensating control is the corpus-wide `/validate` that `/resume` runs first.
- **PR close-out checklist** (the degradation guard): prior PR's `/validate-pr` row AND `/retro` row both batched in; closed TODO items rotated to DONE; stale-count check if an enumerated collection changed; session-handoff.md refreshed.
- **Self-assess for degradation / session-continuation SOP**: continue while quality holds; wind down on actual drift/hallucination/mistakes (not caught by the QA layer), OR when a very large series remains and we want no mid-operation interruption. Steady-state misses the per-PR `/validate-pr` catches are NOT drift.
- **Compute-don't-ask**: before surfacing a question, apply a "can I compute/verify this myself?" gate; surface only the result or a decision that genuinely needs maintainer judgement.

## Refresh discipline

This file is refreshed at every PR close-out (post-merge), as part of the recursion-avoidance batch that carries the validate-pr/retro rows into the next PR.
