# Session State (concurrency lease)

**Active-session:** none

**Status:** released

**Operating-mode:** attended-autonomous

**Last-heartbeat-UTC:** 2026-07-19T22:58:12Z

**Current-task:** SESSION CLOSED at #1055. Lease RELEASED after the aidefensematrix.com gap analysis: the matrix itself is NOT acquired (maintainer decision: a derivative mapping the project can re-create), and the 4 not-held AI-security frameworks it references (OWASP AI Exchange, SANS CAISG v1.4, Google SAIF, Cyber Defense Matrix) are routed to `grc_library_private/maintainer-egress-requests.md` v1.0.3 + TODO RB-7 for maintainer-acquisition ahead of the Wednesday 2026-07-22 resume, when the orchestrator ingests whatever is provided + assesses corpus use/cite. (Prior 2026-07-19b flow, for the record:) 2026-07-19b resumed session (`/resume` from #1043; on the VM, gh-CLI, no GitHub MCP; ATTENDED). The maintainer-LOCKED order was COMPLETE: (1) **§1.19.12 CLAUDE.md sensitivity-trim** = #1044; (2) **self-guard bundle** = #1045 (repeat-block hook) + #1049 (decision-guardrail: act/ask/name-a-blocker + write-before-enact log); (3) **credit-offload bundle** = this PR #1050 (public tail: §3.87 socket revision + §3.103) + scratch PR #173 (idle-liveness heartbeat + progress/session_start fields + alert 2026-07-19-a cleared) + two `grc_library_private` pushes (design-of-record + orchestrator-claude A1 restart-advice + **elevated-QA window -> 1 clean pass**); (4) **§1.22.2 stub-README fix** = #1047. NEXT (maintainer-directed 2026-07-19): the **decision-preload protocol** ("AI-only-works-when-watched" fix): after each merge scan the next 10 TODO items for needed decisions, queue to `pending-decisions.md`, and FLUSH via `AskUserQuestion` the moment the maintainer is present; codify as a CLAUDE.md standing section + a TODO item, and record the ~30-line screen limit. Then the 4 decided seeds, the P3 quick-win wave, and §1.22.3/4/7.

**Worker-dispatches:** both `worker-20260716-a` (role any), `worker-20260716-b` (role qa), VM, Opus 4.8, RESTARTED by the maintainer 2026-07-19 ~07:16 Toronto (fresh sessions; each `(worker+model)` elevated window RE-ESTABLISHES). **worker-b delivery 1 this session = Sweep 114 (elevated QA):** genuine proof-of-run, F1 correctly caught, no worker miss (consume at first close-out). **worker-a:** claimed `research-119-12-trim-movemap` (in progress). The three maintainer-directed bundle-3 protocol changes are now CODIFIED (`_private`): elevated-QA window -> **1 clean elevated pass** (was 2-to-3, reset-on-miss unchanged); workers stamp **session_start** at register (queue-tool field, scratch #173); orchestrator restart-advice is **mode-dependent** with a socket-era programmatic-restart path (orchestrator-claude A1 + TODO §3.87). Both workers LIVE (fresh heartbeats post-#173-merge). Fetch scratch `origin/main` before every coordination-plane read (§3.93); prefer `git -C <scratch>` (or an absolute script path) for sibling tools/git.

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
