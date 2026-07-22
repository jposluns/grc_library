# Changelog (Detailed Mirror)

All notable changes to this repository are recorded in this file with full structured-section detail. The adopter-facing root [`CHANGELOG.md`](../../CHANGELOG.md) carries only a compact one-line entry per change (a `date | version | PR` header plus a short, plain-language summary a general reader can follow); this file is the maintainer-grade audit trail carrying the full detail behind each of those summaries.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](../../specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](../../specification-master-project.md) section 4.5.

The dual-entry convention was introduced in PR #125 (2026-06-21). Historical entries before that date follow the original single-file convention (the root entry was complete; this mirror preserves that pre-split state verbatim from the moment of the split).

## 2026-07-22, Library Version 2026.07.544, PR #1056

Resume close-out for the 2026-07-22 session (the orchestrator's prior session ingested +31 reference items into `grc_library_ref`, catalogue 696 to 727; this session assesses corpus use/cite of them per TODO RB-7). This is the first PR of the resumed session: it runs the loop-break Sweep 116 corpus-wide `/validate`, clears the one aged-follow-up gate artefact, prunes the handoff, and re-acquires the lease.

### Changed
- **[`session-state.md`](../session-state.md)**: lease ACQUIRED for this session (`Status: active`, `Active-session: claude/resume-sweep116-closeout`, fresh heartbeat) after the `/resume` step-0 interlock confirmed the prior lease released and no live sibling session.
- **[`validate-sweeps/history.md`](../validate-sweeps/history.md)**: added the Sweep 116 row (Version 2.0.117); **re-triaged** the aged Sweep-3 follow-up at L133 (added `re-triaged: 2026-07-22` and an explicit `re-triage-by: 2026-08-21`; the default 30-day clock lapsed 2026-07-20 during the multi-day gap, failing gate 43 and the FollowupAgeing regression test), restoring the mechanical baseline to 72 of 72. Kept open as a future-gate candidate, not resolved.
- **[`session-handoff.md`](../session-handoff.md)**: advanced the Resume cursor to Sweep 116; pruned per keep-current-plus-one-prior (removed the 2-prior 2026-07-18b asserted-expectations block, whose substance is durable in the Sweep 113 history row and the CHANGELOG).
- **degradation-watch-log**: a `session-start` row appended in the private companion repo (the `/resume` step 0.4 evidence trail).

### Verification
- Loop-break Sweep 116 `/validate` (OFFLOADED to worker-20260716-b, blocking prio-0, pinned `501d77a2` / ref `3e63317`): **CLEAN PASS, 0 error / 0 warning / 0 note / 0 novel**. The #1054..#1055 delta is `.working`, `.claude`, CHANGELOG, README, and TODO only (no corpus-domain document); the CHANGELOG daily-tier condensation was verified faithful; all #1040-#1042 asserted-clean surfaces corroborated, 0 contradicted. Consumed under elevated QA (worker-b delivery 1 this session; the orchestrator's independent baseline re-derivation matched 70 of 72, same L133 root cause, restored to 72 of 72 by the re-triage).
- Post-commit `run_all_audits.sh` 72 of 72 standalone; the pre-push guard green at push. This PR's own `/validate-pr` and `/retro` batch into the next PR per recursion-avoidance.

## 2026-07-19, Library Version 2026.07.543, PR #1055

Condenses the 2026-07-19 root CHANGELOG entries (PRs #1039-#1054) into one daily summary and prunes the matching detailed-mirror entries, completing the daily-tier condensation for the day during the multi-day session gap. Also records TODO RB-7 (retrieve and ingest four not-held AI-security frameworks the aidefensematrix.com gap analysis surfaced, routed to maintainer-acquisition) and closes the 2026-07-19b/c session, releasing the concurrency lease.

### Changed
- **Root CHANGELOG**: the 16 per-PR 2026-07-19 entries (#1039-#1054) replaced by one `**2026-07-19 (PRs #1039-#1054)**` daily summary, per the §1.22.5 daily-tier model; #1055 (this PR) stays per-PR as the current entry.
- **Detailed mirror**: the matching #1039-#1054 structured entries pruned (git history preserves the full detail); gate 59's parity cutoff floors above them.
- **TODO RB-7**: records the aidefensematrix.com gap-analysis outcome (worker-offloaded, then orchestrator-`_ref`-index-verified with [`ref-holds.py`](../../tools/ref-holds.py)): four not-held AI-security frameworks (OWASP AI Exchange, SANS CAISG v1.4, Google SAIF, Cyber Defense Matrix) routed to maintainer-acquisition, then a corpus use/cite assessment; the matrix itself is NOT acquired (maintainer decision: a derivative CSF-2.0-by-asset-class mapping the project can re-create); OWASP Agentic Top 10 and NIST IR 8596 are HELD-but-uncited breadth items, not acquisitions.
- **The private maintainer-egress-requests queue** (v1.0.3): the four not-held frameworks added as a maintainer-acquisition block (drop-destination `grc_library_ref/ingest/`) for the Wednesday 2026-07-22 resume.
- **Session close**: [`session-state.md`](../session-state.md) lease RELEASED (`Status: released`, `Active-session: none`); [`session-handoff.md`](../session-handoff.md) and [`next-prs.txt`](../next-prs.txt) refreshed with the continuation note and the RB-7 ingest step; the [`validate-pr/history.md`](../validate-pr/history.md) row records the handoff-PR exemption.

### Verification
- Gate 59 (mirror-header-parity) re-run clean after the prune; the pre-push guard (`run_all_audits.sh` + `run-pr-time-checks.sh`) green at push. **Session-closing PR:** per the loop-break rule this PR skips its own trailing `/validate-pr` + `/retro`; the compensating control is the next `/resume` corpus-wide `/validate`, and this session additionally ran Sweep 115 pre-close (0 error / 0 warning over #1044..#1053). The concurrency lease is RELEASED here.

