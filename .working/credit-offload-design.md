# Credit-offload: a multi-worker QA + research queue (design of record)

**Version:** 1.3.2\
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

### Reference-read basis and multi-worker resync (current state, gap, target; TODO §3.85)

The topology above states the TARGET: a worker reads BOTH `grc_library` and `grc_library_ref` from the per-machine cache at the order's pinned SHA. The current implementation reaches that target for `grc_library` (the `/tmp/grc_library_working` per-order `git worktree` at the pinned `grc_library_sha`) but NOT yet for `grc_library_ref`: on the VM the maintainer maintains a single shared `/tmp/grc_library_ref` copy, re-synced (`rsync -av --delete`) after each ref update, and workers read it directly. That is a shared-mutable-state gap:

- A ref update mid-order silently changes what a running worker reads, so the worker's ref read is NOT pinned to its order's `grc_library_ref_sha` the way its `grc_library` read is.
- With multiple concurrent worker sessions there is no per-worker signal that a resync is due, so a worker can read stale reference text without knowing (the "how do multiple workers know to resync?" question the maintainer raised, 2026-07-16).

Target model (TODO §3.85): give the ref the same per-order-pinned read basis as `grc_library` (a ref worktree or clone checked out at the order's `grc_library_ref_sha`), retiring the shared `/tmp/grc_library_ref` copy and its manual rsync; OR, if a shared cache is kept for cost, have the serve loop compare the order's `grc_library_ref_sha` to the cache HEAD and resync-on-mismatch before claiming, so a worker never reads a ref SHA older than its order pins. Until §3.85 lands, the orchestrator-side control is the standing "re-sync `/tmp/grc_library_ref` after any ref update" SOP (`.claude/CLAUDE.md` `## Credit-offload mode` "Worker read basis"), and an order should not be served against a ref SHA newer than the shared cache holds.

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

## Worker allocation and specialization (one-at-a-time + role-based soft split)

The allocation model (maintainer-steered 2026-07-16, refined into the soft split below and codified in `tools/credit-offload-queue.py`, `queue/README.md`, and `workers/README.md` on scratch):

- **One order at a time.** A worker claims exactly one order, serves it to delivery, then claims the next; it never holds two concurrently. Concurrent holds multiply the stale-reclaim and worktree-collision surface for no throughput gain: the fleet's parallelism comes from MULTIPLE workers each serving one order, not one worker multiplexing. This matches the lease/fencing model, which fences one `(order, token)` per holder.
- **Role-based SOFT specialization.** Each worker registers a `role` (`qa` | `research` | `any`). The maintainer's initial steer was a HARD split (one worker QA, one worker research) to keep the two work-classes separated; the refinement is a SOFT split to avoid idling: a worker PREFERS an order matching its role but FALLS BACK to any eligible order when its role's queue is empty. A hard split idles a QA worker whenever the QA queue drains while research orders wait (and the reverse), wasting exactly the spare capacity the scheme exists to use. The soft split keeps the maintainer's separation as the DEFAULT while never leaving a live worker idle beside serveable work.
- **Egress-natural role bias.** The split is also egress-natural: research orders typically need egress (fetching sources), qa orders are typically `egress-none` (judged against held text + the live corpus at a pinned SHA). A worker's detected egress class therefore already biases which orders it CAN claim; `role` layers an intra-eligible PREFERENCE on top of that hard eligibility constraint. An `egress none` worker gravitates naturally to qa work; a full-egress worker can serve either.
- **Claim precedence** (each poll, as the serve loop instructs): among `pending` orders the worker is eligible for (`egress-needs` and `capability-needs` satisfied), a **blocking** order (the resume `/validate`) outranks the role preference and is taken by whichever worker frees first regardless of role, so the one blocking QA pass per session is never starved; among the remaining (non-blocking) orders the worker prefers one matching its `role` kind and falls back to any eligible order when its role's queue is empty, taking the highest-priority claimable order in each case. An `any`-role worker just takes the highest-priority claimable order. **Note (the serve-loop's actual guarantee):** a non-blocking priority-1 order (for example a per-PR `/validate-pr`, which is `priority: 1, blocking: false`) does NOT currently preempt a role-specialized worker's role-kind preference; only `blocking` orders do. Giving all priority-1 orders precedence over the role preference (so urgent QA is never starved behind a role rule even when non-blocking) is a candidate serve-loop strengthening tracked in TODO §3.83; it has no live impact while the fleet is all `any`-role.

## Blocking model

Orders carry a `blocking` flag and a `priority`. The **resume loop-break `/validate` blocks** (the orchestrator enqueues it at resume and waits, polling, for the result before proceeding, one wait per session, only when >=1 worker is live; with 0 workers it self-runs). **`/validate-pr`, the semantic-fit cadences, and research/draft seeds are non-blocking** (consumed at the next PR boundary). Blocking outranks background in priority.

## Trust and re-verification

Findings from a worker are hypotheses until confirmed (the research-assistant discipline). The orchestrator **re-verifies each positive finding** before routing (cheap relative to the sweep, so the net saving holds) and **trusts a clean/zero-finding** result as it trusts its own inline subagents, the worker's result file carries the subagent returns as the proof-of-run. The orchestrator writes the audit-trail rows (`validate-sweeps/history.md`, `validate-pr/history.md`) because those are `grc_library` files the worker cannot write. Mandatory-QA discipline is unchanged: the offloaded run is the full formal pass; abbreviation is never authorized, and if no worker serves an order before it goes stale the orchestrator runs the pass itself.

### New-worker QA-trust tiers: elevated then routine (maintainer-directed 2026-07-16)

The routine trust above (re-verify positives, trust clean-with-proof-of-run) applies only AFTER a worker is trust-established. Because a clean QA result is a trust assertion, and trust is session-scoped and instance-scoped, it is re-established each orchestrator session, keyed on **`(worker-id + model)`** (a model change, for example Opus 4.8 to Fable 5, re-triggers the window for the same worker-id, since a different model has different failure modes). The window applies to **QA-kind deliveries only** (the `command` values `validate` / `validate-pr` / `matrix-fit` / `claim-fit` / `reference-audit` / `screen-publications` / `verify` / `fitness` / `full-qa` / `deep-assessment-readonly`), where a clean claim asserts no defect escaped; research/draft seeds are outside it (they already get full orchestrator re-authoring at apply).

For the first **2 to 3 QA-kind deliveries** from a `(worker + model)` each session, the orchestrator applies **ELEVATED QA** before trusting the result:

1. **Proof-of-run genuineness:** the result must carry real subagent returns (pre-flight counts, per-finding `path:line`, token spend); a bare "clean" with no proof-of-run is a red flag, not a pass.
2. **Independent re-derivation** of everything mechanically derivable (the pinned SHA and delta scope, the counts, the gate results, the pre-flight numbers): re-run/re-count and confirm they match the worker's claims. This is the load-bearing guard, because mechanical facts cannot be faked.
3. **Re-verify EVERY finding at source** (not only positives).
4. **A graduated adversarial auditor:** delivery 1 gets a dedicated false-negative auditor subagent (hunt for what the worker missed, plus sham/scope errors); deliveries 2 to 3 use steps 1 to 3 without a separate auditor, escalating to a fresh auditor only on a red flag.

The 2-to-3 count is a **floor, not a cap** (at least that many CLEAN elevated passes before relaxing to routine). Any confirmed miss, sham, or scope error resets the window, is escalated to the maintainer, and the worker is treated as UNVALIDATED (self-run its passes; trust no result) until re-established. The per-`(worker + model)` elevated-pass count for the session is tracked in the session working-state (`session-state.md` Worker-dispatches) and resets each session by construction. **Honest limitation:** elevated QA raises the bar but does not guarantee detection; a worker fabricating an internally-consistent proof-of-run is a residual risk it reduces but cannot eliminate, which is why step 2 is load-bearing. The project instantiation is the `## Credit-offload mode` "New-worker QA-trust tiers" bullet in [`.claude/CLAUDE.md`](../.claude/CLAUDE.md).

## Order schema

Each order (a file under the scratch queue) carries: `id`, `kind` (`qa` | `research`), `command` (the skill/verb), `params` (delta window, target paths, brief path, asserted-expectations), the pinned `grc_library` SHA and `grc_library_ref` SHA to run against, `egress-needs`, `capability-needs` (a required model capability, e.g. a Fable-5-class capability; `none` for the common case), `priority`, `blocking`, `status` (`pending` | `claimed` | `done` | `rejected`), `claimed-by`, `claimed-at`, `heartbeat`, `fencing-token`, and `result-path`. A worker claims only an order whose `egress-needs` its detected egress class can satisfy AND whose `capability-needs` its model provides (so a cloud worker with blocked egress never claims an order it would only fail and let go stale, and a capability-gated order waits for a worker whose model can serve it). The worker-side registry (`workers/<id>.md`) additionally carries the worker's `role` (`qa` | `research` | `any`) driving the soft-specialization preference above; `role` is a worker attribute, not an order attribute. Mode, egress, and model are detected via `tools/detect-env.py` and the worker's `register` invocation.

## Metrics and reporting

Richer metrics on scratch (per-order cost, per-worker spend, queue depth over time, worker utilization, check-in/out events) back on-demand detailed reports, so the maintainer can validate whether the offload actually nets out. Each worker logs its token spend into its result and a scratch metrics file (a `session-metrics` analogue). Net saving is real only if the other accounts have spare capacity; the scheme SHIFTS cost across accounts rather than reducing total spend.

**Orchestrator-side running tab (maintainer-directed 2026-07-16).** The orchestrator maintains a
running productivity/savings tab in [`credit-offload-metrics.md`](credit-offload-metrics.md): one row
per offloaded delivery (order, kind, worker + model, the worker's best-effort estimated token spend as
a conservative proxy for **estimated orchestrator credits conserved**, the consuming PR, and notes) plus
a per-session roll-up. The chosen surface is that ledger PLUS a short (a couple of lines) chat tally at
each MAJOR ACTIVITY, a worker delivering a result and a PR finishing, reporting the session's passes and
estimated orchestrator credits conserved; there is deliberately NO per-DONE-entry line. The metric is
always labelled an ESTIMATE (workers cannot read an exact in-session count) and carries the standing
caveat that credit-offload shifts cost across accounts rather than reducing total spend, and that the
orchestrator still pays a small consume/verify cost (and the pre-push verifier) on its own account. The
session-closing handoff folds the roll-up figure into the `session-metrics.md` row.

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
