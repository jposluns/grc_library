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

## Codex workers are single-shot: exec-dispatch runs the pass to completion

A Codex chat cannot be resumed once it returns a final response (its own continuation brief records this
as a confirmed limit), so a Codex worker is SINGLE-SHOT: one self-contained pass per dispatch. Under the
exec-dispatch model ([`exec-dispatch.py`](../tools/exec-dispatch.py), which invokes `run-codex-worker`),
the dispatch RUNS THE JOB TO COMPLETION as a background subprocess and delivers to the tray, so there is
no wake to issue and no poll to manage: dispatch, then wait for the delivery, checking the worker log and
the delivery tray on the background-task cadence.

Because a codex pass is single-shot, scope each codex order to ONE self-contained pass: a task needing
several turns will not survive the boundary, so split it rather than hoping the worker persists.

(Historical, the retired standing-codex model: before exec-dispatch, codex ran as a standing tmux session
that had to be nudged with `--send wake` and re-checked every 10 minutes because a control plane cannot
wake an idle turn, and a replacement session was refused a prior session's claim so worker-id churn was
expected. exec-dispatch removed that entirely: run-codex-worker runs the pass and exits, so the nudge, the
10-minute re-check loop, and the id-churn management no longer apply.)

A codex review that COMPLETES but never lands in the tray (the stranded-verdict class diagnosed
2026-08-08) is recovered with [`tools/recover-codex-verdict.py`](../tools/recover-codex-verdict.py):
`--scan` lists verdict-bearing logs with no matching delivery, and a targeted run writes a
RECOVERED-FROM-LOG delivery into the tray. A recovery is a LOWER-TRUST artefact (the banner states the
residue); the orchestrator re-verifies positive findings at source exactly as for a normal delivery.

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
That is the single-plane blindness the retired scratch `list-workers` exhibited. `--dry-run` is the read-only
status form and `--oneline` the statusline form.
