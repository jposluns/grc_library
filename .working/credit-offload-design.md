# Credit-offload: a multi-worker QA + research queue (design of record)

**Version:** 1.1.0\
**Date:** 2026-07-16\
**License:** CC BY-SA 4.0\
**Status:** IN USE. Phase 1 and the initial phase-2 worker command + onboarding are built on `grc_library_scratch` (scratch PR #168). **Phase 3 (the orchestrator-side wiring) is APPLIED** (2026-07-16, maintainer-authorized attended): the worker-availability check + blocking-resume-`/validate` enqueue/consume is wired into `.claude/commands/resume.md` (step 6, plus a queue/results check in step 3) and the `## Credit-offload mode` section of `.claude/CLAUDE.md`. **Phase 2 write-path is under live test:** the first live worker (`worker-20260716-a`) is exercising the claim/heartbeat/deliver path against the offloaded Sweep 108 `/validate` order. See `## Build phases`.

Maintainer working state, exempt from corpus audit gates. This is the design of record for **credit-offload**: a scheme that moves the token-heavy, read-only analysis passes (QA sweeps and research/drafting) off the orchestrator's account onto standing worker sessions on other accounts, so the orchestrator (which is low on usage credits) spends only on the irreducible author -> apply -> route -> merge work. It generalizes the existing research-worker model (`grc_library_scratch` Mode B: workers research, the orchestrator applies) to also cover the QA passes, on a polling work queue with a lease/fencing lifecycle.

The companion runbook is [`multi-session-orchestration.md`](multi-session-orchestration.md); this file is the credit-offload-specific design, cross-referenced from there.

## Motivation

Per Sweep 107, one corpus-wide `/validate` burned ~609K subagent tokens on the orchestrator's account; each `/validate-pr` Subagent A is ~170K and runs on every merge. Those subagent passes are read-only and produce structured findings, so they are cleanly detachable from the authoring loop. Moving them to worker sessions on other accounts shifts that cost off the orchestrator's account (a net win when the other accounts have spare capacity) and, as a bonus, makes the check more independent (a fresh-context validator has less shared blind spot with the author).

## The split (what offloads, what does not)

- **Offloadable (read-only analysis, produces findings/drafts):** `verify`, `validate`, `validate-pr`, `matrix-fit`, `claim-fit`, `reference-audit`, `screen-publications`, `fitness`, `full-qa`, the read-only probe phases of `deep-assessment`, AND research/drafting seeds (the existing Mode-B research work).
- **Stays orchestrator-side (author -> apply -> route -> merge):** authoring corpus prose, applying diffs, writing the audit-trail rows (the worker cannot write `grc_library`), routing findings to the backlog, merging, and the pre-push skeptical verifier (it sits on the critical path before push; offloading it would add a blocking wait before every substantive push). The pre-push-verifier decision is revisited periodically (TODO item).

## Topology and the split-brain resolution

Workers may run same-VM (different accounts) or in the cloud, possibly at the same time. The coordination state must be a single plane every worker can see, or a mixed VM+cloud pool splits into two coordination planes (split-brain: duplicate claims, lost fencing, results dropped where the orchestrator will not look). The resolution separates two concerns that were being conflated under "shared local dir":

- **Coordination plane = the scratch repo (`grc_library_scratch`), always.** The queue, claims, heartbeats, fencing tokens, the `workers/` liveness registry, the check-in/out log, the metrics, and the result-handoff all live on scratch. It is the one plane visible to every worker regardless of VM-vs-cloud, so it is split-brain-free by construction. Claiming is by git push (first push wins; a non-fast-forward reject makes the loser re-fetch and re-pick); the fencing token plus orchestrator-side result rejection cover the rare double-claim. At a 5-minute poll cadence the git round-trip cost is negligible.
- **Clone/worktree cache = local, per-machine (`/tmp/grc_library_working`).** The heavy read data (the `grc_library` and `grc_library_ref` git objects the worker reads at a pinned SHA) is cached locally. Same-VM accounts share one fetched `.git` per repo (one background fetch loop keeps it fresh, the co-location freshness win); each work order is executed in an ephemeral `git worktree` at the order's pinned SHA (isolated, SHA-pinned, no cross-worker HEAD collision). Cloud workers keep their own clone. This cache is immutable pinned content with no coordination role, so it never causes split-brain, and it does NOT reuse the orchestrator's `/home/jposluns/grc_library/.git` (that would couple the two and re-introduce the shared-tree hazard, grc_library #866); it is an independent clone. `/tmp` is reboot-volatile, so the cache re-populates via fetch after a reboot (acceptable for a cache; a non-`/tmp` path would persist if wanted).

The orchestrator's own setup at `/home/jposluns/{grc_library,grc_library_ref,grc_library_scratch}` is unchanged; `/tmp/grc_library_working` is worker-only and the orchestrator never touches it.

## The lease/fencing lifecycle (multi-worker correctness)

- **Check-out (claim):** a worker atomically claims a `pending` order, writing `claimed-by`, `claimed-at`, and a monotonic **fencing token** (incremented every time the order is claimed).
- **Check-in (heartbeat):** the worker re-stamps a heartbeat every **~5 min** while working.
- **Stale declaration:** if `now - heartbeat > ~20 min`, the coordinator (the orchestrator, or a serving worker) marks the claim stale, increments the fencing token, and returns the order to `pending` for another worker.
- **Fencing (rejects a revoked holder's late write):** every result delivery carries the token it was claimed under; the coordinator accepts a result only if its token matches the order's CURRENT token. A worker declared stale (token incremented) delivers under an old token -> **rejected**. This is the standard fencing-token guarantee; it precisely prevents a credit-exhausted-then-revived worker from dropping a stale payload over re-assigned work.

Lease timing: heartbeat 5 min / stale 20 min (the looser setting, chosen to suit long-running orders such as the deep-assessment phases).

**Worker wind-down and re-register (no full handoff; two light hooks).** A worker needs no
orchestrator-style handoff/resume: it is stateless between orders, and all cross-interruption
state is already externalized to this coordination plane (the queue IS the next-actions list;
"resume" is just re-registration). A per-worker handoff document would be a second coordination
plane (the split-brain hazard this design resolves) and would violate scratch's wipeable
invariant. The lifecycle instead carries two light, protocol-consistent hooks (design assessment
by `worker-20260716-a`, 2026-07-16; developed orchestrator-side into
`tools/credit-offload-queue.py`, `.claude/commands/credit-offload.md`, and `queue/README.md` on
scratch):

- **Worktree cleanup on wind-down/crash.** The happy-path serve loop removes its
  `wt-<order-id>` worktree after delivery, but the graceful-`checkout` path and an ungraceful
  stop do not, so worktrees accumulate in the per-machine cache and a revived worker re-claiming
  the SAME order collides on the existing `wt-<order-id>` path at `git worktree add`. The
  `checkout` operation (and, where the harness allows a stop trap, an ungraceful stop) prunes
  `wt-*` worktrees for orders the worker no longer holds.
- **Reconcile on re-register (the worker-side of the fencing guarantee).** On `register` with an
  existing worker id, the worker scans the queue for orders still stamped `claimed_by=<me>` and,
  for each, compares the order's CURRENT `fencing_token` to the token it last held: if the token
  moved (it was declared stale and reclaimed) it must NOT deliver and drops that worktree; if the
  token still matches and the heartbeat is fresh it may continue a genuinely-live claim. It also
  prunes worktrees for orders now `done`/`pending`. This makes re-registration idempotent and
  self-healing (the worker-side analogue of the orchestrator's resume lease-check), rather than
  assuming a clean slate.

**Deliberate non-goal: intra-order checkpointing.** There is intentionally no way to resume PART
of an order; a worker that dies mid-order loses that work and the order restarts from scratch
under a new claim. Partial-findings delivery would violate the "an offloaded run is the full
formal pass, abbreviation is never authorized" discipline. If resumability inside a long order
is ever wanted, the lever is SMALLER orders (finer granularity), not a per-worker checkpoint file
(which would be a third state surface).

## Worker liveness and token-budget-aware checkout

- **`workers/` liveness registry** (on scratch): each serving worker posts `worker-id`, `mode` (VM|cloud), `egress-class`, and a `last-seen` heartbeat. The orchestrator reads it to decide behaviour: **0 live workers -> never wait, self-run** (offload is pure best-effort); **>=1 live worker -> enqueue offloadable orders (and, for the resume `/validate`, wait on the result)**; mid-session changes adapt (a worker appearing lets the orchestrator start shifting work to it; all workers dropping reverts it to self-run, or it just enqueues non-blocking seeds for later pickup). The orchestrator never burns time waiting on an empty pool.
- **Token-budget-aware graceful checkout (best-effort):** a worker approaching its usage cap (about 90% used) finishes its current task, delivers, then checks out of the `workers/` registry until its usage window resets, using a time-until-reset indication to know how long it is out. **Honest caveat:** whether a Claude worker session can reliably observe its own token usage and reset time in-session is harness-dependent (there is no guaranteed in-session usage API the model can self-poll). So graceful checkout is **best-effort when a usage signal is available**; the fencing/stale-reclaim path is the **guaranteed backstop** for a worker that simply stops (credit-exhausted, no clean checkout). Verify the signal's availability at build time before promising the clean-checkout behaviour.
- **Check-in/check-out log** (on scratch): records every join/leave event (clean low-usage checkouts and orchestrator-declared stale reclaims alike), so the maintainer can see if and when a worker dropped out due to low usage.

## Blocking model

Orders carry a `blocking` flag and a `priority`. The **resume loop-break `/validate` blocks** (the orchestrator enqueues it at resume and waits, polling, for the result before proceeding, one wait per session, only when >=1 worker is live; with 0 workers it self-runs). **`/validate-pr`, the semantic-fit cadences, and research/draft seeds are non-blocking** (consumed at the next PR boundary). Blocking outranks background in priority.

## Trust and re-verification

Findings from a worker are hypotheses until confirmed (the research-assistant discipline). The orchestrator **re-verifies each positive finding** before routing (cheap relative to the sweep, so the net saving holds) and **trusts a clean/zero-finding** result as it trusts its own inline subagents, the worker's result file carries the subagent returns as the proof-of-run. The orchestrator writes the audit-trail rows (`validate-sweeps/history.md`, `validate-pr/history.md`) because those are `grc_library` files the worker cannot write. Mandatory-QA discipline is unchanged: the offloaded run is the full formal pass; abbreviation is never authorized, and if no worker serves an order before it goes stale the orchestrator runs the pass itself.

## Order schema

Each order (a file under the scratch queue) carries: `id`, `kind` (`qa` | `research`), `command` (the skill/verb), `params` (delta window, target paths, brief path, asserted-expectations), the pinned `grc_library` SHA and `grc_library_ref` SHA to run against, `egress-needs`, `priority`, `blocking`, `status` (`pending` | `claimed` | `done` | `rejected`), `claimed-by`, `claimed-at`, `heartbeat`, `fencing-token`, and `result-path`. A worker claims only an order whose `egress-needs` its detected egress class can satisfy (so a cloud worker with blocked egress never claims an order it would only fail and let go stale). Mode and egress are detected via `tools/detect-env.py`.

## Metrics and reporting

Richer metrics on scratch (per-order cost, per-worker spend, queue depth over time, worker utilization, check-in/out events) back on-demand detailed reports, so the maintainer can validate whether the offload actually nets out. Each worker logs its token spend into its result and a scratch metrics file (a `session-metrics` analogue). Net saving is real only if the other accounts have spare capacity; the scheme SHIFTS cost across accounts rather than reducing total spend.

## Build phases

- **Phase 0 (maintainer):** provision the least-privilege worker account(s) (read `grc_library` + `grc_library_ref`, write `grc_library_scratch`); the same-VM shared `/tmp/grc_library_working` clone cache and the worker sessions are launched by the maintainer (permissions bind at session launch).
- **Phase 1 (scratch, built in scratch PR #168, 2026-07-16):** the queue protocol + directory conventions on scratch (`queue/`, `results/`, `workers/`, the check-in/out log, `metrics/`), the `tools/credit-offload-queue.py` helper (claim/heartbeat/fence-check/deliver over the scratch-git plane), the `/credit-offload` worker command (`.claude/commands/credit-offload.md` in scratch), and a first real test order (the Canada.ca reference-breadth research seed).
- **Phase 2 (scratch):** the `/credit-offload` worker command + the worker onboarding shipped initial in scratch PR #168; the remaining hardening is the poll-claim-worktree-dispatch-deliver-checkout loop's write path (UNDER LIVE TEST 2026-07-16: `worker-20260716-a` is exercising it against the offloaded Sweep 108 order), the dispatch table mapping order commands to the corpus skills, the two worker-lifecycle hooks (worktree cleanup on wind-down/crash, reconcile on re-register; see the lease/fencing section), a **serve-loop self-refresh** (`git fetch origin && git reset --hard origin/main` on the scratch clone at the top of each poll cycle, so a running worker adopts helper updates without a restart; the command/CLAUDE wording still needs a `/credit-offload` re-invoke, since it is context-loaded), and the safety rails.
- **Phase 3 (grc_library, protected): APPLIED 2026-07-16 (maintainer-authorized attended).** The orchestrator-side enqueue/consume convention and the credit-offload directive are wired into `/resume` (the worker-availability check + blocking-resume-`/validate` enqueue/wait/consume in step 6, plus a queue/results check in step 3) and the `## Credit-offload mode` section of `.claude/CLAUDE.md` (offloadable set, worker-availability gate, consume/trust discipline, honest limitation, and the `/tmp/grc_library_ref` worker-read-copy re-sync obligation).

## Prohibited / honest limitations

- The scheme shifts cost across accounts; it does not reduce total spend.
- The orchestrator still pays to verify positive findings and to run the pre-push verifier on the critical path.
- Graceful low-usage checkout depends on a harness usage signal that may not exist; the fencing/stale backstop is the guarantee.
- A worker never writes `grc_library` or `grc_library_ref`; it delivers to scratch only, and the orchestrator applies. There is no trusted-worker fast path; worker provenance never reduces the QA a change receives.
