# Session State (concurrency lease)

**Active-session:** claude/pr959-closeout

**Status:** active

**Last-heartbeat-UTC:** 2026-07-15T21:17:59Z

**Current-task:** ACTIVE, UNATTENDED from ~2026-07-15T21:00Z (maintainer away ~1hr; proceed, wind down only on a NAMED degradation signal). The 2026-07-15 resumed session (`/resume` from #954), on the VM, gh-CLI. Merged this session: #955-#958 (Canada AI annex accuracy + FPS AI Strategy v1.0.1; sibling "third review" fix; four public-site text fixes; annex AIA date-anchor v1.0.2), #959 (loop-break Sweep 106 close-out: register "third-review"->"fourth-review" hyphenated third carrier, register v1.5.37). Cross-repo: `grc_library_ref` PR #80 (HIGH AI ingest + two ref-tool fixes). This PR #960: maintainer-flagged TODO stale-item cleanup (closed §2.4 grclibrary.ai + §2.6 Cloudflare watch-paths to DONE, reworded 6 dangling §2.4 refs) + #959's `/validate-pr`+`/retro` + the Sweep 106 tally fix. **NEXT (preloaded maintainer answers 2026-07-15):** (a) #961 = about-page ", CGEIT, CISSP" to ~half the name's height (website, priority); (b) the remaining ~44 `grc_library_ref` ingests as SERIAL batches per `grc_library_ref/ingest/INGEST-PLAN.md`: skip the 3 news announcements + the Responsible-use-of-AI index hub; old-edition items get an upstream currency check (ingest current, mark superseded as historical, never as current); "Choosing secure and verifiable technologies" -> a new international/Australia-ASD subdir; carry the ingest.py programs-stub body/jurisdiction fix; (c) version-maturation content-review-each after the ingest. Session-closing handoff picks up the Sweep 106 C-note handoff-snapshot lag. Lease active.

**Worker-dispatches:** this session dispatched three parallel adversarial fact-check subagents (read-only) over the Canada AI annex, each verifying one instrument cluster against the held `grc_library_ref` primary sources; all findings re-verified by the orchestrator at apply time and the two date/ordinal items confirmed upstream on canada.ca. The `grc_library_scratch` inbox holds 15 pure-research seeds (11 PENDING + 4 UNMAPPED per `tools/audit-delivery-status.py`), all deliberately KEPT in the §3.58 disposition; unchanged this session.

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
