# Overnight PR

**Status:** in-flight

This file is the durable handoff record for a maintainer-authorized autonomous overnight
session. It is `stub` when no overnight session is in flight (the default state).

Lifecycle (audit gate 46 enforces it: passes on `stub` and `in-flight`, fails on `done`):

- `stub`: no overnight session in flight. This file holds only this protocol description and the `Status: stub` line.
- `in-flight`: an overnight session is active. The assistant fills the file with the authorization scope, design decisions made, files being authored or modified, build progress, and open ambiguities. Each overnight PR ships `in-flight`.
- `done`: the session ended. The next-morning processing PR routes the content to the durable ledgers (design decisions to [`design-decisions.md`](design-decisions.md), closed work to [`DONE.md`](DONE.md), queued follow-ups to [`../TODO.md`](../TODO.md)) and resets this file to `stub`.

## Current overnight session (started 2026-06-28, resumed from session-closing handoff #450)

**Authorization scope (the four maintainer-resolved directives, full detail + audit trail in [`pending-decisions.md`](pending-decisions.md)):**

1. **FULL AUTONOMY**: author and self-merge green P1/P2 PRs, including net-new standalone documents, without holding for morning review. **Mandatory condition**: run the high-assurance adversarial-verification harness (the [`high-assurance-verification`](../dev-security/claude-rules/governance/high-assurance-verification.md) process, independent false-negative + false-positive verifier agents) on ANYTHING net-new before accepting/merging it, recording each net-new item and its harness outcome in [`high-assurance/register.md`](high-assurance/register.md).
2. **Source-absent jurisdictions/regimes (FR-59/61/62)**: cover the ref-base-sourced ones; for each missing source, ATTEMPT to download the primary-source legislation into the appropriate `grc_library_scratch/ref/` directory via the scratch ingestion workflow (MCP PR; egress permitting per DD-10); defer only the truly-unavailable and record it.
3. **Out of overnight scope**: multi-session orchestration tracks (§4.7/4.11/4.16/4.18), FR-48 (H2 rename), FR-167 gap-fill. The procedural closing `/matrix-fit` may still run. **FR-70 (crypto-asset / blockchain) IS in scope** as net-new (gets the harness).
4. **ISO/IEC 27001:2022 Annex A control TITLES are usable** (titles are not proprietary; the proprietary material is the section content the title heads). The ISO title-map may carry verbatim Annex A titles, built from the scratch `ref/standards/ISO/` extracts; do NOT reproduce the ISO control body text. Unblocks the P3 ISO-validation gate-54 extension and the `/matrix-fit` ISO column.

**Standing operating discipline (unchanged):** PRIMORDIAL RULE Quality > Speed > Cost; per-PR `/validate-pr` + `/retro` for every non-handoff PR (no abbreviation); each batch `/validate`'d; serial-apply + CI-gating + validate-then-apply invariants; net-new content gets the high-assurance harness before merge. The STANDING fix-issues-first directive (maintainer 2026-06-27) holds: correction items before new content.

**Planned overnight order:** PR-1 (this Sweep-74 close-out + handoff prune + overnight-start) -> PR-E (the `high-assurance-verification` executable companion SKILL, skill 16->17) -> the correction batch (FR-58 3-label reconcile, §4.24 pack-README rule-table, ERC ~26-doc reconcile, FR-44 shall->must, Sweep-3) + the guard-rail gates (§4.8 apply-time disciplines, §4.5 S1/S2/S3, §4.6 QA-cadence, §4.10 Option-B marked-done detector) -> P1/P2 content under directive 1 (net-new gets the harness; FR-70 crypto in scope; FR-59/61/62 per directive 2) -> the closing FR-167 whole-matrix `/matrix-fit`.

**Progress (updated as PRs land):**
- **#451** (merged): Sweep 74 (loop-break corpus-wide `/validate`, 2 in-window C1 stale-count findings fixed: TODO.md:155 eleven->twelve governance rules, lint-matrix-control-codes.py:6 eight->nine frameworks) + handoff prune/refresh + this overnight-start transition.
- **#452** (merged): fixed the recurring handoff-marker defect at its source: `.claude/CLAUDE.md` step 5a + close-out-checklist item 3 said "Summary cell"; corrected to "Findings cell" so gate 50 detects the handoff exemption (the #445/#450 recurrence root cause).
- **#453** (merged): the `high-assurance-verification` executable companion SKILL + `/high-assurance` command + paired-skill-gate parity + skill-count `16->17` + command-count `9->10` (was queued as PR-E).
- **#454** (merged): completed the pack-README "Rule files and their scope" table by adding governance rules 9-12 (closes TODO §4.24).
- **#455** (merged): FR-44 corpus-wide `shall`->`must` normative-verb harmonization via deterministic scripted apply + re-parse (3 files skipped to preserve a gate-9 filename and backticked word-refs).
- **#456** (merged): ERC reconcile, `Executive`->`Enterprise Risk Committee` across 9 same-body-verified docs; the ambiguous minimum-viable-governance-structure guideline DEFERRED to authorial review.
- **#457** (in flight): this session-closing handoff PR. Batches the #456 `/validate-pr` (1 Low, fixed) + `/retro`, refreshes the handoff, keeps this file `in-flight` so the next `/resume` continues the queue.

**Still queued for the continuing overnight run (next `/resume`):** guard-rail gates (§4.5 S1/S2/S3, §4.6 QA-cadence, §4.10 Option-B), §4.8 apply-time codifications, Sweep-3 follow-up, the ERC guideline-doc authorial reconcile, FR-58 3-label scheme; then P1/P2 net-new content under directive 1 (FR-70 crypto, FR-73, FR-31/32/34/71/72, FR-59/61/62 per directive 2) each via the high-assurance harness; then the closing FR-167 whole-matrix `/matrix-fit`. **Sweep 75** over the #451..#457 deltas is the next loop-break control.

**Open ambiguities / decisions surfaced:** The session-closing wind-down decision was surfaced via `AskUserQuestion`, which errored (the known environment flake; maintainer asleep). Per the wind-down framework + the overnight directive 1 (maintain overnight on no-answer), the no-answer default was option A (session-closing handoff) WITHOUT toggling overnight off; this file stays `in-flight`. The ERC guideline-doc reconcile remains the one genuinely-authorial deferral (narrowed TODO item).
