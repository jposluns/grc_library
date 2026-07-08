# Overnight PR

**Status:** stub

This file is the durable handoff record for a maintainer-authorized autonomous overnight
session. It is `stub` when no overnight session is in flight (the default state).

Lifecycle (audit gate 46 enforces it: passes on `stub` and `in-flight`, fails on `done`):

- `stub`: no overnight session in flight. This file holds only this protocol description, the `Status: stub` line, and (after a routed run) a short closure note recording where the last run's content went.
- `in-flight`: an overnight session is active. The assistant fills the file with the authorization scope, design decisions made, files being authored or modified, build progress, and open ambiguities. Each overnight PR ships `in-flight`.
- `done`: the session ended. The next-morning processing PR routes the content to the durable ledgers (design decisions to [`design-decisions.md`](design-decisions.md), closed work to [`DONE.md`](DONE.md), queued follow-ups to [`../TODO.md`](../TODO.md)) and resets this file to `stub`.

<!-- OVERNIGHT-PR-STUB -->

## Last run closure note: 2026-07-07 and 2026-07-08 overnight (routed by the 2026-07-08 `/resume` close-out PR, ending overnight mode)

The maintainer directed the resumed session to end overnight mode, morning-process this file, ask the deferred questions, and begin attended-autonomous daytime mode. This close-out routes the two overnight run sections (2026-07-07 NUC daytime-then-overnight, and 2026-07-08 overnight) and resets to `stub`.

Runs covered: the 2026-07-07 session (Sweep 88 + TODO 1.12 close, then the reference-library split #687-#689, then the reference-base ingests, tracked separately in `grc_library_ref`) and the 2026-07-08 overnight run (#694 `/full-qa` follow-up fixes; #695 changelog-restructure PR 1 machinery; #696 TODO 1.11 ANPD residual; #697 FR-63 adoption worked example closing §2.7; #698 README companion-catalogue row + register-ageing-tool deferral). Session merged through #698 and closed at the #699 session-closing handoff.

Content routing (morning-processing):
- **Design decisions** to [`design-decisions.md`](design-decisions.md): the changelog-restructure current-week model and the reference-library split were already recorded in-run (via TODO §3.19 and the #687-#689/#695 CHANGELOG entries and `design-decisions.md`); no un-routed design decision remained.
- **Closed work** to [`DONE.md`](DONE.md): routed per-PR during the runs (#687-#698 each carry their DONE entries).
- **Queued follow-ups** to [`../TODO.md`](../TODO.md) and [`pending-decisions.md`](pending-decisions.md): the blocked/deferred set (changelog PR 2 sweep-to-scratch privacy-gate decision, PR 3 root reformat/compress, the 3.16/3.17 alignment maps, the register-ageing classifier, the egress-priority items, the git-history collapse) is recorded in `pending-decisions.md` / TODO / the session-handoff CLOSING block, surfaced to the maintainer at this resume. TODO 3.19 tracks the changelog-restructure remainder.
- **Reference-repo open ambiguities (recorded here for provenance):** the fast-follow reference-source `license:` schema shape (formal field vs codify-the-convention; default codify-the-convention) and a reference-source re-snapshot currency-watch cadence are `grc_library_ref` concerns, tracked in that repo's own backlog, not in grc_library TODO (the reference base moved out of this corpus in the #687-#689 split).
- **Noise discarded**: the build-progress and files-modified lists.

Maintainer items surfaced from the runs: the deferred-question queue (changelog PR 2/PR 3, alignment maps, register-ageing tool, egress-priority items, git-history collapse) is surfaced at the 2026-07-08 `/resume` for triage.
