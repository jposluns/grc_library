# Overnight PR

**Status:** stub

This file is the durable handoff record for a maintainer-authorized autonomous overnight
session. It is `stub` when no overnight session is in flight (the default state).

Lifecycle (audit gate 46 enforces it: passes on `stub` and `in-flight`, fails on `done`):

- `stub`: no overnight session in flight. This file holds only this protocol description, the `Status: stub` line, and (after a routed run) a short closure note recording where the last run's content went.
- `in-flight`: an overnight session is active. The assistant fills the file with the authorization scope, design decisions made, files being authored or modified, build progress, and open ambiguities. Each overnight PR ships `in-flight`.
- `done`: the session ended. The next-morning processing PR routes the content to the durable ledgers (design decisions to [`design-decisions.md`](design-decisions.md), closed work to [`DONE.md`](DONE.md), queued follow-ups to [`../TODO.md`](../TODO.md)) and resets this file to `stub`.

<!-- OVERNIGHT-PR-STUB -->

## Last run closure note: 2026-07-06 overnight (routed by PR #673, the morning-processing PR)

The 2026-07-06 overnight run (resume session `claude/resume-tl5rez`) shipped PRs #667 through #671: TODO 3.21 close (#667) and its 3.21(d) follow-through (#668, `PCI DSS v4` to `v4.0.1`), the TODO 1.9 PreToolUse-hook-firing root-cause record (#669), the TODO 3.15 #637 F4/F6 acronym-linter digit-initial widening (#670), and the TODO 3.15 r4 G-7 QA-report intake runbook subsection (#671). Each shipped with its own DONE entry and per-PR `/validate-pr` + `/retro` rows.

Content routing (morning-processing):
- **Design decisions** to [`design-decisions.md`](design-decisions.md): the PCI DSS "full latest version" citation-form standing preference (recorded in-run under #668); the 3.21(a) bare `C-TPAT` choice was a per-item maintainer decision recorded in [`DONE.md`](DONE.md) #667, not a standing principle. No un-routed design decision remained.
- **Closed work** to [`DONE.md`](DONE.md): routed per-PR during the run (#667 through #671 each added its entry).
- **Queued follow-ups** to [`../TODO.md`](../TODO.md): none new. The 3.21(a) matrix framework-key full-name-consistency observation was deliberately NOT raised as an item absent a signal (recorded here for provenance only).
- **Deferred to the daytime protected-backlog** ([`deferred-protected-changes.md`](deferred-protected-changes.md)): the `/claim-fit` cadence clause (item 5, content-ready) and TODO 3.15 #637 F3 (D5 eighth closure-form, protected-entangled: the "seven closure forms" count in the protected `.claude/CLAUDE.md` must co-update to eight in the same PR). Both cleared in the daytime session that follows this reset.
- **Noise discarded**: the build-progress and files-modified lists.

Maintainer items surfaced from the run: the morning time-decay-on-publications recommendation (delivered); the two-PDF scratch `publications/` assessment (net no ingest, one duplicate, one low-value); the #670 lowercase-tolerant-inline-pattern rejection (surfaced to confirm or reopen); and the TODO 1.9 close-vs-track disposition (held in [`pending-decisions.md`](pending-decisions.md)).
