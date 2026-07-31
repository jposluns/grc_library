# Worker dispatch mechanics and delivery trays (reference)

**Read this at the worker-dispatch boundary, like a skill: when constructing or pinning a worker
order, managing a codex worker, or processing the delivery trays.**
[`.claude/CLAUDE.md`](../.claude/CLAUDE.md) carries the lean always-on core (the pin-to-a-containing-SHA
and codex-single-shot gists, plus the two always-on clauses: inbox issues jump the queue, and sweep
the trays at each boundary); this file carries the full order-construction and tray mechanics and
their rationale. Relocated from CLAUDE.md by roadmap C part 2 (the activity-scoped rule loader); the
always-on residue kept inline in CLAUDE.md is deliberate defence-in-depth and is not a duplication to
trim. This is project-only operational machinery (the tmux, exec-dispatch, and file-drop specifics),
NOT pack material. The mechanical backstops are the [`tools/exec-dispatch.py`](../tools/exec-dispatch.py)
dispatch-time REFUSAL/WARNING checks and [`tools/collect-deliveries.py`](../tools/collect-deliveries.py)'s
two completeness layers; this prose is the explanation, the tools are the guard.

## Pin an order to a SHA that CONTAINS what the order references

Three orders on 2026-07-25 asserted something untrue at their own pinned SHA, and each cost a worker
cycle: one named a function that existed only on an unmerged branch, one pinned a merge SHA that
PREDATED the backlog item the order told the worker to read, and one carried a worker exclusion as
prose that nothing enforced.

**The rule is narrower than "pin to a merge SHA", which was already the practice and was not enough.**
The correction adopted after alert 2026-07-23-a made a pinned SHA REACHABLE (never a PR branch head
that vanishes on squash-merge). It did not make the SHA CONTAIN what the order references. So: pin to
a commit that contains every path, item and identifier the order tells the worker to read, which for
an order derived from backlog item N means the commit that CREATED item N, not merely a later one.

**Two mechanical backstops now exist at dispatch**, and their severities differ on purpose:
- **A REFUSAL** when `not_worker` names a worker id the exchange has never seen, because that input is
  exact and a vacuous exclusion silently disables an independence control.
- **A WARNING** when a referenced path or `TODO N.M` item is absent at the pinned SHA, because that
  extraction is heuristic and a false refusal on a legitimate dispatch would get the check bypassed.

**Read the dispatch output.** Both backstops are useless if the dispatch line scrolls past unread, and
a warning is exactly the shape that gets skimmed. The orchestrator's own habit is the primary control;
these are defence in depth.

## Codex workers are single-shot: dispatch, check in, then re-check every 10 minutes

Maintainer-directed 2026-07-25, after the codex session minted four worker ids in under two hours and
every one went stale. A Codex chat cannot be resumed by the control plane: once it returns a final
response its heartbeat daemon can hold a claim but nothing continues the semantic pass, which its own
continuation brief records as a confirmed limit. So a Codex worker is effectively SINGLE-SHOT PER NUDGE
rather than a standing worker, and treating it like an Opus worker leaves orders sitting in
`available-work` beside a fleet that reads as live.

The orchestrator therefore MANAGES codex directly rather than waiting on it:

1. **Dispatch** the order to the codex family as normal.
2. **Immediately issue a check-in** (`--send wake`), because the order will not otherwise be noticed.
3. **If nothing has arrived in 10 minutes, issue another check-in. Repeat.** A fresh worker id appearing
   is normal and expected here: the protocol deliberately refuses to let a replacement session inherit a
   prior session's claim, so id churn is the mechanism working rather than a fault to chase.

It is also the reason a codex order should be scoped to ONE self-contained pass: a task needing several
turns will not survive the boundary, so split it rather than hoping the worker persists.

## Delivery tray: one place to look, and issues jump the queue

The exchange stores a delivery at `<family>/outbox/<worker-id>/<order-id>.md`, so answering "what is
delivered and unprocessed?" means walking every family crossed with every minted worker id. Doing that
by hand mis-reported the fleet once on 2026-07-25 (a stale `list-pending` read was described as "7
stranded orders" when all ten had in fact been delivered). Two trays now separate the traffic, and the
separation is the point (maintainer-directed 2026-07-25):

- **`inbox/`** carries HIGH-PRIORITY issues a worker raises, read as soon as noticed. A worker writes one
  the moment it hits a blocker, a malformed order, an out-of-scope defect, or an independence conflict,
  rather than burying it in a result the orchestrator may not read for hours. This matters more now that
  workers run HEADLESS, with no pane being watched.
- **`inbox/deliveries/`** carries routine order results, processed at the next boundary, named
  `<worker-id>__<order-id>.md` so both ids survive without parsing the body. The orchestrator needs the
  worker id for the elevated-QA trust window (keyed on worker plus model) and for independence routing.

Mixing them would destroy what makes the issue channel work, namely that its list is short and every item
on it matters, so a delivery never lands in bare `inbox/`.

**Run [`tools/collect-deliveries.py`](../tools/collect-deliveries.py) at each task boundary**: it sweeps
completed deliveries into the tray and files each served order under `done/orders/`. Two independent
completeness layers gate the move, because they catch different failures. `deliver` publishes via an
atomic rename from a `.md.tmp` name in the same directory, so any `*.md` in an outbox has all its bytes;
and the last non-blank line must be `<!-- END OF DELIVERY -->`, which is the author's assertion that the
work was finished rather than merely fully written. A file failing either is LEFT IN PLACE and REPORTED
individually, never silently skipped, because a file sitting untouched with no explanation is the same
silence-reads-as-health failure as a stalled worker that still heartbeats while no longer doing work.

Its report names BOTH planes (tray count and still-in-outbox count) rather than summing them, because the
sweep only runs while the orchestrator is alive, so a tray-only reading under-reports between sessions.
That is the single-plane blindness still live in the scratch `list-workers`. `--dry-run` is the read-only
status form and `--oneline` the statusline form.
