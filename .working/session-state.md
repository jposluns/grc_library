# Session State (concurrency lease)

**Active-session:** claude/website-landing-restructure-pr6

**Status:** active

**Last-heartbeat-UTC:** 2026-07-15T01:03:20Z

**Current-task:** ACTIVE on branch `claude/website-landing-restructure-pr6` (resumed VM orchestrator session; ATTENDED-autonomous, green CI = merge authority). Continuing the maintainer's live-review of the public grclibrary.ai site (live on Cloudflare Pages, custom domain assigned) after the takeover of the crashed cloud session (`claude/cloudflare-public-website-2d7sis`, which merged #918-#920 then died). **Live-review round merged:** #921 (layout/link/housekeeping polish), #922 (11 per-domain on-site pages + register links + SEO + hero `.dek` fix), #923 (title-as-link on landing cards + domain doc names + tighter domain spacing), #924 (landing contents sidebar). **Adoption round (goal: getting people to adopt):** #925 merged the dedicated `/pack` governance-pack page (13 rules + 23 skills + 3 adoption modes + contents sidebar, footer link). **In flight, PR6 (#926):** the landing restructure, a new 6-card "Get started" section placed 3rd (links to existing corpus docs: decision-tree / worked-example-adoption / template-quickstart / matrix / adopter-guide / maturity self-assessment), hero primary CTA -> Get started, §03 pack slimmed to a `/pack` teaser (3 highlight cards), the CC BY-SA licence split into its own closing §07 "Licence & reuse", sections renumbered §01-§07, sidebar + footer nav updated, dead `.adopt-grid`/`.adopt-card` CSS removed; batches #925 QA (2 internal notes fixed: build.py docstring + this lease). After #926 the whole website effort (PR1 #921 -> PR6 #926) is complete; remaining is the maintainer's Cloudflare console (watch-paths incl. the 11 domain dirs) + the publish go. Corpus-wide `/validate` + P1/P2 batch remain deliberately SKIPPED (crash-resume, not a QA-skipping handoff; `main` green 69/69). Green-at `e50fc22` (#925) = 69/69. §2.4 stays OPEN until publish. Standing cleanup: DRY the landing/pack contents-sidebar CSS into the shared partial. See [`session-handoff.md`](session-handoff.md) for the full state.

**Worker-dispatches:** PR5 (#925) dispatched the #924 post-merge `/validate-pr` (SHIP, 0 findings) and a refute-briefed skeptical verifier on the `/pack` page (SHIP-WITH-NOTES: one Medium rule-description accuracy fix + a CSS-duplication note). PR6 (#926) dispatched the #925 post-merge `/validate-pr` (SHIP-WITH-NOTES, 2 internal notes fixed here) and a refute-briefed skeptical verifier on the landing restructure (SHIP, 0 defects; content-preservation confirmed, the ShareAlike licence block byte-identical). All respected read-only-git on the shared tree. The `grc_library_scratch` inbox holds 15 pure-research seeds (11 PENDING + 4 UNMAPPED per `tools/audit-delivery-status.py`), all deliberately KEPT in the §3.58 disposition; unchanged this session.

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
