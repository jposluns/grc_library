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
- PR-1 (in flight): Sweep 74 (loop-break corpus-wide `/validate`, 2 in-window C1 stale-count findings fixed: TODO.md:155 eleven->twelve governance rules, lint-matrix-control-codes.py:6 eight->nine frameworks) + handoff prune/refresh + this overnight-start transition.

**Open ambiguities / decisions surfaced:** none yet beyond the four resolved directives.
