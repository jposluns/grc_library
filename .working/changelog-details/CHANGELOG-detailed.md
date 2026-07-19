# Changelog (Detailed Mirror)

All notable changes to this repository are recorded in this file with full structured-section detail. The adopter-facing root [`CHANGELOG.md`](../../CHANGELOG.md) carries only a compact one-line entry per change (a `date | version | PR` header plus a short, plain-language summary a general reader can follow); this file is the maintainer-grade audit trail carrying the full detail behind each of those summaries.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](../../specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](../../specification-master-project.md) section 4.5.

The dual-entry convention was introduced in PR #125 (2026-06-21). Historical entries before that date follow the original single-file convention (the root entry was complete; this mirror preserves that pre-split state verbatim from the moment of the split).

## 2026-07-19, Library Version 2026.07.543, PR #1055

Condenses the 2026-07-19 root CHANGELOG entries (PRs #1039-#1054) into one daily summary and prunes the matching detailed-mirror entries, completing the daily-tier condensation for the day during the multi-day session gap (the day-boundary trigger would otherwise not fire until the next session, several days out).

### Changed
- **Root CHANGELOG**: the 16 per-PR 2026-07-19 entries (#1039-#1054) replaced by one `**2026-07-19 (PRs #1039-#1054)**` daily summary, per the §1.22.5 daily-tier model; #1055 (this PR) stays per-PR as the current entry.
- **Detailed mirror**: the matching #1039-#1054 structured entries pruned (git history preserves the full detail); gate 59's parity cutoff floors above them.

### Verification
- Gate 59 (mirror-header-parity) re-run clean after the prune; the full audit suite green at push. The concurrency lease stays ACTIVE (the session continues past #1054 for a maintainer-requested gap analysis); a later PR closes the session and releases the lease.

