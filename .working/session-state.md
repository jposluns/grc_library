# Session State (concurrency lease)

**Active-session:** claude/website-card-links-pr3

**Status:** active

**Last-heartbeat-UTC:** 2026-07-14T23:26:56Z

**Current-task:** ACTIVE on branch `claude/website-card-links-pr3` (resumed VM orchestrator session; ATTENDED-autonomous, green CI = merge authority). Continuing the maintainer's live-review of the public grclibrary.ai site (live on Cloudflare Pages, custom domain assigned) after the takeover of the crashed cloud session (`claude/cloudflare-public-website-2d7sis`, which merged #918-#920 then died). **Merged this session:** #921 (layout/link/housekeeping polish + #920 QA) and #922 (11 per-domain on-site pages + register links + SEO + hero `.dek` width fix + #921 QA). **In flight, PR3 (#923):** made titles into links, each landing feature-card keyword (the approved mapping: STRUCTURED/STYLE->master spec, CROSS-LINKED->portal, PRACTICAL->adopter-guide, INTEGRITY->audit-programme, CITATIONS->citations-register, ALIGNMENT->matrix, GENERATED->maturity-scorecard, TESTED->tests README, and the 6 pack-rule names->their rule files) links to its corpus page; each domain-page document NAME is now the link to its GitHub source (the separate "GitHub" link dropped, a ↗ marks the off-site jump); and the domain-page section/hero spacing is tightened so the document list is reachable without much scrolling (maintainer-flagged, notably on iPad). **Queued PR4 (maintainer-approved):** a sticky left sidebar (the 6 section links + a Domains heading + the 11 domain links) that collapses to a boxed Contents panel on narrow screens, to show breadth up front. Corpus-wide `/validate` + P1/P2 batch remain deliberately SKIPPED (crash-resume, not a QA-skipping handoff; `main` green 69/69). Green-at `34496d0` (#922) = 69/69. §2.4 stays OPEN until the maintainer's publish go. See [`session-handoff.md`](session-handoff.md) for the full state.

**Worker-dispatches:** PR2 (#922) ran two read-only in-session subagents to completion: the #921 post-merge `/validate-pr` Subagent A (SHIP-WITH-NOTES, 1 note fixed in #922) and a refute-briefed skeptical verifier on the per-domain-pages generator + content boundary (SHIP-WITH-NOTES, 0 critical/high, 0 boundary leaks; the dev-security dangling-colon intro + two low findings all fixed in #922). PR3 (#923) dispatched the #922 post-merge `/validate-pr` Subagent A (read-only-git on `34496d0`; result batched into #923). All respected read-only-git on the shared tree. The `grc_library_scratch` inbox holds 15 pure-research seeds (11 PENDING + 4 UNMAPPED per `tools/audit-delivery-status.py`), all deliberately KEPT in the §3.58 disposition; unchanged this session.

This file is the session-concurrency lease: the declared half of the two-part interlock
that protects the shared `main` state surfaces (the session handoff, [`../TODO.md`](../TODO.md),
[`DONE.md`](DONE.md), the QA history registers, the detailed CHANGELOG mirror, and the four
version surfaces) from a second orchestrator session resuming while a prior one is still
live. The full design, including the honest limitation that this is an advisory interlock
and not a hard mutex, is recorded in [`design-decisions.md`](design-decisions.md) under
"Session-concurrency safety".

Lifecycle (audit gate 63 enforces the SHAPE; the `/resume` step-0 procedure enforces the
interlock, because CI runs per-branch and cannot see across concurrent sessions):

- **Acquire**: at session start, right after the `/resume` step-0 check passes, the
  session writes `Active-session: <its branch>`, `Status: active`, and a fresh
  `date -u +%Y-%m-%dT%H:%M:%SZ` heartbeat.
- **Refresh**: the heartbeat is re-stamped at each PR close-out (it batches into the
  recursion-avoidance refresh alongside the session handoff).
- **Release**: the session-closing handoff PR sets `Status: released` and
  `Active-session: none`, so a cleanly-closed session leaves a released lease on `main`.

The declared state above is only the LAST-MERGED session's view. The other half of the
interlock is external: `/resume` step 0 also runs a `git fetch` cross-check of unmerged
`origin/claude/*` branches for commits inside the 60-minute staleness window (the crash
net for a session that died without releasing). Status `active` or `winding-down` with a
heartbeat inside the window means a session is likely live: HOLD and surface to the
maintainer; do not proceed on a timeout. A not-`released` lease with a heartbeat OLDER
than the window is surfaced as an abandoned-session takeover decision instead.
