# Session State (concurrency lease)

**Active-session:** claude/r3-machinery-staging-and-closeprep

**Status:** active

**Last-heartbeat-UTC:** 2026-07-14T12:02:00Z

**Current-task:** ACTIVE, **unattended/overnight** (maintainer-set at the 2026-07-14 resume, re-confirmed "going back to sleep" ~08:58Z: no idle-stop, green CI = merge authority, stricter-safe defaults on no-answer, full per-PR `/validate-pr` + `/retro`, overnight ends only on an explicit signal). Loop-break **Sweep 102** ran CLEAN. The **r3 High + value + tail remediation is COMPLETE**: DA-ASVS #902 (high-assurance harness), FR-200 #903, FR-201 #904, FR-202..205 #905, FR tail #906, RB-ETSI primary + DA-ISO20000 resolved #907. Shipped since: #908 (CHANGELOG compact reformat + advisory guard, §3.65), #909 (r3 machinery low-precision, §3.64), #910 (ISO 20000 reference-breadth review, §3.67). Shipped since: #910 (ISO 20000 reference-breadth, §3.67), #911 (ISO 20000-1 clause-accuracy, §3.72, 11 corrections/7 docs). Shipped since: #912 (FR-201 vuln-SLA SoT completion, §3.68 partial). Now on **#913** (r3 machinery G3 = gate 50 Check 5 register row-order guard, DONE; + batched #912 QA). Remaining machinery: G1 + handoff-D-check are protected-tree (`.claude/`) -> daytime/authorized apply (G1 maintainer-VM-authorized; handoff-D-check needs the recursion-avoidance convention carve-out confirmed). Next overnight: coverage-refresh scratch sync, P3 cleanup, session-closing handoff. Routed forks await maintainer (§3.66/3.68-authorial/3.69/3.70/3.71, FR-214/215/217/219). HONEST SIGNAL: heavy decision-oscillation on the machinery this deep (first-pass-judgment strain; 0 adopter escapes, all in-window-caught); recommend the protected machinery + forks be handled fresh/attended. Routed forks await maintainer (§3.66/3.69/3.70/3.71, FR-214/215/217/219). All resume decisions banked in [`pending-decisions.md`](pending-decisions.md). Green-at `fb8f5a1` (#907) = 69/69 (verified this session).

**Worker-dispatches:** Sweep 102 dispatched three read-only `/validate` subagents (A recent-PR / B stale-reference / C audit-programme), all returned clean. No apply-stage workers this session. The `grc_library_scratch` inbox holds 15 pure-research seeds (11 PENDING + 4 UNMAPPED per `tools/audit-delivery-status.py`), all deliberately KEPT in the §3.58 disposition and schedule-gated; no seed is apply-ready or dispatched.

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
