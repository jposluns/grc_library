# Session State (concurrency lease)

**Active-session:** claude/website-text-fixes

**Status:** active

**Last-heartbeat-UTC:** 2026-07-15T19:14:47Z

**Current-task:** ACTIVE. The 2026-07-15 resumed session (`/resume` from #954), attended-autonomous on the VM, gh-CLI. Merged this session: #955 (Canada AI annex accuracy corrections + new AI Strategy for the Federal Public Service 2025-2027 section, v1.0.1), #956 (the same "third review" fix in the integrated AI-and-privacy procedure, surfaced by #955's cross-ref). This PR #957 ships four public-site text fixes (landing hero two-line, landing §01 one-line, about "thirty years", For-AI hero colour-per-line) and batches #956's `/validate-pr` + `/retro`. **STILL PENDING this session:** the version-maturation initiative (per-doc Versions under 1.0.1 -> 1.0.1, maintainer-flagged 2026-07-15, next after this website PR); the standing loop-break corpus-wide `/validate` (Sweep 106) over #943..#954; and the `grc_library_ref` ingest of the 71 Canada.ca source files the maintainer added to `ingest/` (resynced 2026-07-15; maintainer to give ingest instructions). Lease active.

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
