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

## ☀️ MORNING HAND-OFF (read this first) — overnight run executed, clean-up pending

The 2026-06-24 autonomous overnight run executed and the maintainer directed a hand-off to a fresh session for the morning clean-up. **First actions for this session, in order:**

1. **Open and merge PR #305.** It is committed and pushed to `claude/aicm-ccm-resume-3jd277` but **UNMERGED**: the GitHub MCP server disconnected mid-session (after #304 merged), so the PR could not be opened or merged via MCP. See [`third-party-issues.md`](third-party-issues.md). #305 = the loop-break-generalize pack-layer change + the batched #304 QA rows + this handoff refresh. Confirm `git log` shows the #305 commit ahead of `main`, open the PR (MCP), confirm CI green, merge. If MCP is still down, surface to the maintainer; do NOT merge by any non-MCP path.
2. **Morning-process [`overnight-pr.md`](overnight-pr.md)** (its `Status` is `in-flight`): route its content (design decisions → [`design-decisions.md`](design-decisions.md); closed work → [`DONE.md`](DONE.md); deferred items → [`../TODO.md`](../TODO.md)), then reset it to `stub`. Gate 46 passes on `in-flight`; this is the required clean-up.
3. **Run the corpus-wide `/validate` (Sweep 37)** as the loop-break compensating control for #305 (the session-closing PR took the handoff exception and skipped its own `/validate-pr` + `/retro`). Route findings.
4. **Review TODO with the maintainer** and let them decide how to proceed.

### What shipped overnight (all MERGED except #305)
- **Sweep 36** (the #300 loop-break `/validate`) found and fixed the CCM/AICM bare-domain-code (IVS/NET/GOV/AUD/EKM) + version-currency residuals that #298's token-scoped reconciliation left → **PR #301** (Sweep 36 close-out, 13 corpus docs + pack README).
- **PR #302**: `guardrail-review` word-form gate count `forty-seven`→`forty-eight` (the second Sweep 36 finding, split by theme).
- **PR #303**: Day-1-floor risk-artefact drift, option A (closed the XS item; partially resolved FR-140).
- **PR #304**: R3 relocation (`register-main-branch-protection.md` → `.working/`, PR #116 precedent).
- **PR #305 (PUSHED, UNMERGED — GitHub MCP outage)**: generalized the handoff-PR QA loop-break into the distributable pack layer (closed the S item). Per-PR QA on #301-#304 was formal `/validate-pr` + `/retro`, all clean (0 substantive findings); the only friction was one known-pattern CHANGELOG em-dash on #302 (D3-caught, amended) and the orchestrator's own filtered-grep that initially under-scoped the EKM residual on Sweep 36 (caught by the unfiltered re-grep before commit).

### Morning-review decisions the maintainer needs to make (detail in [`overnight-pr.md`](overnight-pr.md))
- **I&S-03 probable mis-citation**, `operations/standard-physical-security-of-it-infrastructure.md:108`: cites I&S-03 (catalogue title "Network Security") in a physical-security context, but physical/datacenter security is the CCM `DCS` domain. Surfaced by Sweep 36, NOT fixed (correct replacement needs judgment).
- **R1 relocation pack-design decision**: moving `tools/sweep-preflight-exemptions.json` → `.working/` is functionally safe, but the file is referenced from two *distributable* pack SKILLs; pointing them at a `.working/` path bakes a project-working-dir path into the pack (adopters may delete `.working/`). Options (a) point SKILLs at the new path, (b) genericize the SKILL prose, (c) keep it in `tools/` and close R1 as won't-move. Deferred rather than guess on distributable content.

### Still-queued work (effort-ordered; re-read TODO live, it is the source of truth)
- **XS/S remaining**: **R1** (blocked on the pack-design decision above), **R2** (the 6-file citation-verification cluster → `.working/citation-verifications/`; the maintainer-flagged heavy relocation, own PR, extra grep care), **FR-62** (AI jurisdiction annexes; likely needs scoping), **Sweep 3 follow-up** (manual term/identifier consistency pass), **B2** + **DD-10** (egress-gated; attempt fetch, defer if blocked, never fabricate), and the new **S4 + S5 gate-48 enhancements** (S4 section-aware title check, S5 bare-domain-code check; non-trivial *tooling*, design notes in TODO §4.5 — a gate bug is higher-stakes than a content error, so give these focused attention with full regression tests).
- **M content clusters** (dispositions recorded in TODO): DD-2/3/11 risk-vocabulary harmonization, DD-4/5 TLS 1.3, DD-8 CPPA-as-live scrub, FR-58/140/145/73, FR-15/23/24/63/74/99/154 (several deliberately-thin baselines, calibrate first), the P4 process/meta items.

### The autonomy disciplines that governed the overnight run (kept for reference)

- **Overnight-work protocol** ([`change-tracking.md`](../dev-security/claude-rules/governance/change-tracking.md) overnight section): `overnight-pr.md` is `in-flight` during a run, morning-processing routes it and resets to `stub`. **Gate 46 fails on `Status: done`**; it currently reads `in-flight` (correct for the pending state).
- **Per-PR QA never abbreviated**: every merged PR got the formal `/validate-pr` + `/retro`; the only standing exception is the session-closing PR (the loop-break, taken by #305).
- **Directional choices (maintainer away):** proceed on a recorded TODO disposition; sensible-default-and-flag for a new bounded choice; defer costly/ambiguous/precedence/distributable-pack choices to morning. No fabrication ever.

## State snapshot (as of 2026-06-24, end of the autonomous overnight run; #305 pushed-but-unmerged)

- **Branch**: `claude/aicm-ccm-resume-3jd277`. `main` is at **#304** (last MCP-merged PR). The branch is **one commit ahead of `main`**: the **#305** commit (loop-break-generalize + batched #304 QA rows + this handoff refresh), pushed but UNMERGED due to the GitHub MCP outage. First action: open + merge #305 (see the MORNING HAND-OFF section).
- **HEAD** (branch): the #305 commit. `main` tip: the #304 squash-merge (`git log origin/main -1` to confirm). Verify with `git log --oneline -6`.
- **Versions** (in the #305 commit, become live once #305 merges): library `2026.06.283`, pack `1.49.7`, README `1.9.154`. On `main` (pre-#305): library `2026.06.282`, pack `1.49.6`, README `1.9.153`. (Verify against `README.md`.)
- **Audit programme**: **48 numbered gates** + **3 PR-only delta gates (D1/D2/D3)**; all passing on the #305 committed state. Governance rules: **10**. Skills: **15** (6 paired). Slash commands: **8**.
- **Last merged**: **#304** (R3 relocation). Before it, this session: **#303** (Day-1-floor), **#302** (word-form), **#301** (Sweep 36 close-out). **#305 is pushed, not yet merged.**
- **`/validate` cadence**: **Sweep 36** ran this session (the #300 loop-break; close-out #301). The next `/resume` runs **Sweep 37** (the loop-break control for the session-closing #305, which took the handoff exception).

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
