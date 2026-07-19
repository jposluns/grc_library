# Changelog (Detailed Mirror)

All notable changes to this repository are recorded in this file with full structured-section detail. The adopter-facing root [`CHANGELOG.md`](../../CHANGELOG.md) carries only a compact one-line entry per change (a `date | version | PR` header plus a short, plain-language summary a general reader can follow); this file is the maintainer-grade audit trail carrying the full detail behind each of those summaries.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](../../specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](../../specification-master-project.md) section 4.5.

The dual-entry convention was introduced in PR #125 (2026-06-21). Historical entries before that date follow the original single-file convention (the root entry was complete; this mirror preserves that pre-split state verbatim from the moment of the split).

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

