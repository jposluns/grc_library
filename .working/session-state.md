# Session State (concurrency lease)

**Active-session:** claude/website-pack-page-pr5

**Status:** active

**Last-heartbeat-UTC:** 2026-07-15T00:41:57Z

**Current-task:** ACTIVE on branch `claude/website-sidebar-nav-pr4` (resumed VM orchestrator session; ATTENDED-autonomous, green CI = merge authority). Continuing the maintainer's live-review of the public grclibrary.ai site (live on Cloudflare Pages, custom domain assigned) after the takeover of the crashed cloud session (`claude/cloudflare-public-website-2d7sis`, which merged #918-#920 then died). **Merged this session:** #921 (layout/link/housekeeping polish + #920 QA), #922 (11 per-domain on-site pages + register links + SEO + hero `.dek` width fix + #921 QA), #923 (title-as-link on the landing cards + domain doc names, tighter domain spacing + #922 QA). **In flight, PR4 (#924):** a contents-navigation sidebar on the landing page, a boxed in-flow Contents panel by default (phone / iPad-portrait, shown up front) that becomes a sticky left sidebar on wide screens (>= 1080px), listing the 6 section links + a Domains heading + the 11 domain-page links (new `SIDENAV_DOMAINS` generator value); page-scoped to the landing page so about/domain pages are untouched; masthead/footer stay full-bleed. NOTE: the responsive visual behaviour is not browser-verifiable on the VM, so the maintainer reviews the live preview. Corpus-wide `/validate` + P1/P2 batch remain deliberately SKIPPED (crash-resume, not a QA-skipping handoff; `main` green 69/69). Green-at `63b8b42` (#923) = 69/69. §2.4 stays OPEN until the maintainer's publish go; remaining after the site work is the maintainer's Cloudflare console (watch-paths incl. the 11 domain dirs) + publish go. See [`session-handoff.md`](session-handoff.md) for the full state.

**Worker-dispatches:** PR3 (#923) ran the #922 post-merge `/validate-pr` Subagent A (SHIP-WITH-NOTES, 0 error / 2 warning, both fixed in #923). PR4 (#924) dispatched two read-only in-session subagents (running / completed): the #923 post-merge `/validate-pr` Subagent A (read-only-git on `63b8b42`; result batched into #924) and a refute-briefed skeptical verifier on the sidebar restructure + generator addition. Prior PRs' verifiers all returned SHIP / SHIP-WITH-NOTES with every finding fixed in-window. All respected read-only-git on the shared tree. The `grc_library_scratch` inbox holds 15 pure-research seeds (11 PENDING + 4 UNMAPPED per `tools/audit-delivery-status.py`), all deliberately KEPT in the §3.58 disposition; unchanged this session.

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
