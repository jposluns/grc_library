# Session State (concurrency lease)

**Active-session:** claude/website-sidebars-scrollspy

**Status:** active

**Last-heartbeat-UTC:** 2026-07-15T15:59:19Z

**Current-task:** ACTIVE. The 2026-07-15 resumed session (`/resume` from #942) holds the lease, now on branch `claude/website-sidebars-scrollspy`, attended-autonomous on the VM, gh-CLI (no GitHub MCP). Working the maintainer's **website-adjustment batch** (website updates take priority this session). Merged so far this session through #950 (Sweep 105 close-out #943; pack card-links #944; landing §05 lede #945; For-AI page + robots/sitemap/llms #946; AUTHORS attribution link #947; §2.16 residual #948; §3.76 parity guard #949; "License" spelling #950). This PR (#951) is batch **item 2**: contents sidebars on the For-AI, per-domain, and Contributors pages + DRY the sidebar CSS into the shared head-style + scrollspy trio-highlight (grid-row-peer Standards sub-links light together); it folds the #950 `/validate-pr` fix and batches #950's QA. **NEXT:** batch item (3) landing polish (orange eyebrow taglines every section; green-check line -> boxed CTA), then per-type listing pages + chips, then §2.15 standards-source links, then §3.75 web->corpus link-integrity, THEN the maintainer-gated §2.4 publish go (Cloudflare console). Tooling follow-up §3.77 (CHANGELOG link-gate `.html`/`.css`/`.js` extensions) after the website batch.

**Worker-dispatches:** the #950 `/validate-pr` dispatched Subagent A (read-only-git on the shared tree), 1 low finding (three bare `.web/templates/*.html` paths in the #950 detailed entry, fixed in this PR #951). This PR (#951) dispatched one refute-briefed skeptical verifier (substantive multi-surface change), which found no defect (pack-clipping non-regression, div balance, landing de-dup, scrollspy correctness, anchor resolution, generator health all clean; static/cascade analysis, live-browser visual not runtime-tested). The `grc_library_scratch` inbox holds 15 pure-research seeds (11 PENDING + 4 UNMAPPED per `tools/audit-delivery-status.py`), all deliberately KEPT in the §3.58 disposition; unchanged this session.

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
