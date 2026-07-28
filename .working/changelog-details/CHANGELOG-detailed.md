# Changelog (Detailed Mirror)

All notable changes to this repository are recorded in this file with full structured-section detail. The adopter-facing root [`CHANGELOG.md`](../../CHANGELOG.md) carries only a compact one-line entry per change (a `date | version | PR` header plus a short, plain-language summary a general reader can follow); this file is the maintainer-grade audit trail carrying the full detail behind each of those summaries.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](../../specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](../../specification-master-project.md) section 4.5.

The dual-entry convention was introduced in PR #125 (2026-06-21). Historical entries before that date follow the original single-file convention (the root entry was complete; this mirror preserves that pre-split state verbatim from the moment of the split).

**Worker-provenance convention (decided 2026-07-23, TODO 3.19):** a reference to a scratch-side worker result or manifest is written as plain backticked text in a `repo:path` form (naming the scratch repo and the result file), never a cross-repo markdown link. A cross-repo relative link target resolves only against a fresh sibling checkout at `main`, not a stale local tree, and cross-repo links are un-gate-checkable; the plain-text form keeps the provenance readable and grep-able without the fragility.

## 2026-07-28, Library Version 2026.07.708, PR #1218

Overnight-session resume close-out (the first PR of the 2026-07-28 overnight-unattended session, resumed from the #1217 handoff).

### Changed
- Recorded **Sweep 127** in [`.working/validate-sweeps/history.md`](../validate-sweeps/history.md): the DUAL-FAMILY loop-break corpus-wide `/validate` over the #1213..#1216 deltas (head `9fd2dd2d`=#1216), PRE-QUEUED at the #1217 wind-down and consumed at this overnight resume. Both families delivered; complementary yield (claude caught 3 ISO/IEC 27001:2022 A.6.2 to A.6.7 citation errors in remote-working/BYOD contexts plus a secrets A.5.17 warning; codex caught the [`tools/lint-audit-gate-parity.py`](../../tools/lint-audit-gate-parity.py) docstring D1-D8 to D1-D9 drift). All 6 #1216 asserted-expectations were CORROBORATED and ZERO contradicted; the citation errors are pre-existing latent defects in documents #1216 did not touch, so ordinary findings rather than misses. Loop-break control for #1217 PASSES. The 6 fixable findings are FIXED in the follow-on fix PR; the remainder ROUTED to TODO.
- Advanced the Resume cursor to Sweep 127 and PRUNED [`.working/session-handoff.md`](../session-handoff.md) to current-plus-one-prior per per-session stack.
- Acquired the concurrency lease in [`.working/session-state.md`](../session-state.md) (Status active, overnight-unattended).

### Verification
- Pre-push guard green (both runners, 78 gates). The codex vpr-1216 HOLD (a read-only worker could not read the maintainer-private changelog archive) was RESOLVED by the orchestrator confirming [`grc_library_private/changelog-archive/2026-07-27-daily.md`] holds all 20 swept #1195-#1214 entries.

## 2026-07-28, Library Version 2026.07.707, PR #1217 (2026-07-27b session-closing handoff)

Session-closing handoff for the 2026-07-27b session (`/resume` at 22:02Z, attended-autonomous winding to overnight). Working-state only; no corpus or code change.

### Changed
- Refreshed [`.working/session-handoff.md`](../session-handoff.md) with new Next-actions / State-snapshot / Asserted-expectations blocks for the 2026-07-27b close, carrying the maintainer-directed overnight plan: deep-assessment component-by-component DUAL-FAMILY (codex + claude) sequential over all worker-capable components, then `/fitness` broken out to the 10 personas each run by both families to compare. The 3.147 token-rotation measurement is flagged MORNING/ATTENDED-only (lockout risk), not overnight.
- Released the concurrency lease in [`.working/session-state.md`](../session-state.md) (Status: released, Active-session: none).
- Batched #1216's dual-family validate-pr (PASS) + retro + merge-bypass rows; refreshed [`.working/next-prs.txt`](../next-prs.txt).
- Pre-queued the overnight component-1 orders (`vda-c1-validate` claude + codex) and the `vpr-1216` dual-family orders.

### Verification
- Pre-push guard green (both runners, 78 gates) before push. #1216's validate-pr returned PASS (dual-family: claude authoritative 0e/0w/2-benign-notes; codex delivered as cross-reference, no contradicting finding).

## 2026-07-28, Library Version 2026.07.706, PR #1216 (2026-07-27 daily CHANGELOG roll-up)

D9 daily roll-up, past midnight UTC. Bookkeeping only.

### Changed
- [`CHANGELOG.md`](../../CHANGELOG.md): the 20 per-PR root entries for 2026-07-27 (PRs #1195-#1214, versions 2026.07.685 to 2026.07.704) collapsed into one 76-word daily roll-up line (`**2026-07-27 | 2026.07.685..2026.07.704 | PRs #1195-#1214 (20 PRs)** - ...`), keeping the adopter-facing root scannable.
- [`.working/changelog-details/CHANGELOG-detailed.md`](CHANGELOG-detailed.md): the matching 20 detailed-mirror entries pruned to the private changelog archive (grc_library_private, changelog-archive, the 2026-07-27-daily file) (data-safe: emitted + verified all 20 present before pruning), so the in-repo mirror holds the current window and gate 59 stays green (parity floor rises to #1215).

### Verification
- Gate 59 (mirror-header-parity) green after the sweep; the roll-up summary was drafted by an offloaded worker (range corrected to #1195-#1214) and verified at source (20 entries, dash-free, 76 words).
- Library 2026.07.705 to 2026.07.706, README 1.10.66 to 1.10.67 (Date 2026-07-28).
- Batches PR #1215's `/validate-pr` (dual-family) + `/retro` + merge-bypass rows.

## 2026-07-28, Library Version 2026.07.705, PR #1215 (pr-closeout.py: the PR close-out scaffolder, TODO 3.133)

Roadmap B efficiency tooling. Closes TODO 3.133 (the biggest per-PR efficiency lever).

### Added
- [`tools/pr-closeout.py`](../../tools/pr-closeout.py): the mechanical per-PR close-out scaffolder (938 lines, stdlib-only). It computes a merged PR's merge/base SHA and CI state (via git/gh, degrading gracefully), bumps every staged versioned file's Version AND Date, emits correctly-columned row templates for the backward surfaces (merge-bypass-log, validate-pr history + optional detail file, improvement-log) and the forward CHANGELOG root + detailed-mirror headers, and refreshes next-prs.txt. It names the two PR identities explicitly (backward rows describe the just-merged PR N; forward surfaces describe the PR M being assembled, default N+1 with a loud caveat) and ships a `--closeout-only` mode. Default mode is PREVIEW (writes nothing); mutations are dry-run-guarded and idempotent; ledger rows are anchored on the header line (never re-matching the next row, the fused-row mitigation). The orchestrator still AUTHORS all content; the tool removes the error-prone placement and the D2/D4/D7 co-bump trap.
- A regression test `test_pr_closeout_self_test` in [`tests/test_linters.py`](../../tests/test_linters.py), wiring the tool's 47-check `--self-test` into the linter-regression suite (gate 36) so it cannot rot.

### Verification / discipline observation
- **Dual-family review** (maintainer's new standing rule: all QA goes to both a claude and a codex worker). The claude lens caught a MUST-fix the self-test masked: `render_retro_row` emitted a BARE PR cell (`1214`) while the live improvement-log uses `#1213`, causing format drift and a double-insert risk (the idempotency token compared bare `1214`, so a house-format `#1214` row would not match). Fixed: `render_retro_row` now emits `#N`, the idempotency token is `f"#{merged_pr}"`, and the fixture was corrected to the `#N` convention so the test validates it. The codex lens wandered into reading skill files (a codex-focus issue, noted); the claude finding was the actionable one.
- Self-test 47/47 at HEAD; the wired regression test passes; stdlib-only (gate 71 safe); no language findings.
- Not run on real surfaces this PR; the #1214 close-out rows here were authored by hand, with the tool available for the next close-out.
- Library 2026.07.704 to 2026.07.705, README 1.10.65 to 1.10.66, Date 2026-07-28 (UTC rollover mid-session: forward surfaces dated 2026-07-28, #1214's backward merge-date rows stay 2026-07-27).
- Batches PR #1214's `/validate-pr` (PASS) + `/retro` + merge-bypass rows.
