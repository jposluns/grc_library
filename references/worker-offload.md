# Mandatory worker offload and dispatch (reference)

**Read this at the worker-dispatch boundary, like a skill: when dispatching or managing workers, or
deciding whether to self-run offloadable work.** [`.claude/CLAUDE.md`](../.claude/CLAUDE.md) carries
the lean always-on core (the offload principle, the offloadable list, and the stays-orchestrator-side
list); this file carries the full dispatch mechanics and rationale. Relocated from CLAUDE.md by
roadmap C part 2 (the activity-scoped rule loader); the always-on residue kept inline in CLAUDE.md is
deliberate defence-in-depth and is not a duplication to trim. The mechanical backstop is the
`block-orchestrator-self-qa.py` PreToolUse hook; this prose is the explanation, the hook is the guard.

This is the operational form of the orchestration primordial rule near the top of CLAUDE.md. The hard
rule (maintainer-directed 2026-07-19; expanded 2026-07-26; restructured for the `orch-verify` dispatcher 2026-08-21):

1. **If a worker CAN do it, a worker DOES it. No debate, no self-run (maintainer-directed 2026-07-26).**
   Anything offloadable (see the inline list in CLAUDE.md) is GIVEN to a worker the moment it comes
   up; the orchestrator does not do it itself. The orchestrator's usage credits are the scarce,
   slow-to-renew resource, and self-running offloadable work is exactly what exhausts them: a prior
   week's self-run QA burned the orchestrator out mid-day and cost a worker account an extended lockout. The default is OFFLOAD; self-running an offloadable task is the exception that needs a
   stated reason (a genuine dispatch failure from an actual attempt AND the maintainer alerted).
2. **Spawn workers ON DEMAND with the global `orch-verify` dispatcher; do NOT gate offload on a
   liveness check.** `orch-verify` spawns a FRESH read-only worker per call and runs it to completion:
   `orch-verify <claude|codex|gemini> <prompt-file> [workdir] [--expensive] [--model <m>] [--effort <l>]`.
   It chooses the account itself via `orch-rank` (team tier for workers, then priority, then live-count
   spread, then soonest reset), so there is no manual account selection and no order-id to pin. The
   worker runs read-only (Claude under a read-only settings file, Codex `--sandbox read-only`, Gemini
   in plan mode) in `[workdir]` (default the current directory) and returns its stdout plus a
   `WORKER_STATUS` line; the prompt file is any readable file `<=100KB`. Because a worker is spawned per
   call, there is **no standing pool whose liveness could be read** (maintainer-directed 2026-08-10:
   "we ONLY exec dispatch"). Earlier text here described a "standing-poll fleet sitting idle" whose
   empty reading was never a licence to self-run; that framing is now wrong in a way that still
   misleads, because there is no standing pool at all, so a liveness reading answers no question worth
   asking and treating an empty or stale one as a signal is a guard-input failure (on 2026-08-10 the
   orchestrator ran a since-retired check, read two seven-thousand-minute-stale rows, and reported
   "there is no fleet" as a blocker). **The rule is simply: DISPATCH.** Never check first, never gate on
   liveness, never self-run because a reading looked empty. Parallelism is DISTINCT families and
   multiple concurrent `orch-verify` calls (run in the background), each holding its own per-worker
   lease; the account pool and dispatch policy live in the shared worker registry that `orch-rank`
   selects from (managed via `orch --set`), not in this repo.
3. **SHA-pin in the brief, not on the command line.** `orch-verify` has no order-id or pinned-checkout
   argument, and the worker reads the working tree at `[workdir]`. So when a review must be pinned to a
   specific commit, NAME the SHA in the prompt-file brief (and, where the worker must judge a specific
   change, embed the diff or the file excerpts in the brief) rather than relying on a checkout flag.
   Commit the artefact under review before dispatching, so the worker reads a committed state and any
   `file:line` finding is reproducible against that SHA.
4. **20-minute reissue.** If a worker has not delivered in 20 minutes, issue the SAME order again (a
   second `orch-verify` call; `orch-rank` ranks by live-count among its keys, so it PREFERS a
   less-loaded account without manual selection, though it does NOT guarantee a distinct one) and take
   whichever returns first; the late delivery is read as a cross-reference, never re-adjudicated.
5. **Every QA pass gets one worker per available family (claude, codex, and gemini).** Give the identical
   order to one `orch-verify` worker of each family and assess the deliveries together: different models
   surface different perspectives, so the cross-family read is how nothing is missed. Reconcile them; a
   finding in only one family's delivery is triaged on its own merits. This is the operational form of
   the permanent triple-family QA standard, which applies to EVERY QA pass (each member an `orch-verify`
   worker, one per family; the Claude member is a claude-family `orch-verify` worker, NEVER the in-session
   Agent tool, per `block-orchestrator-self-qa.py`). On token or tooling unavailability the panel drops
   to the families that can run (triple to dual to single), never a discretionary downgrade. RESIDUE: a
   read-only worker cannot complete the mechanical audit baseline (a gate test writes a temp fixture, so
   `run_all_audits.sh` fails under the read-only sandbox); the orchestrator runs the mechanical baseline
   itself (a deterministic Bash verification, not offloadable reasoning) as the authoritative half of the
   panel.
6. **Keep the run moving: dispatch QA and research/draft `orch-verify` calls in parallel.** Because each
   call runs to completion, parallelize by launching several concurrent background calls rather than by
   keeping a standing pool busy: one on the QA cadence (`/validate-pr`, `verify`, sweeps) and the others
   producing research and draft candidates for the upcoming queue, so the orchestrator always has a
   delivery to APPLY rather than a dispatch to wait on.
7. **If NO worker of any family is available (every account limited or out), ALERT the maintainer** or
   obtain authorization to proceed without workers. Zero available capacity is a condition to surface,
   not to route around in silence. Worker ids and account labels recorded in this public repo are
   ANONYMIZED: the raw `<family>-<account>-<timestamp>` id, all account names, and the account label a
   worker's `WORKER_STATUS` line prints stay in `_private` only, and are sanitized out of any id or
   status quoted into a public artefact.

The offloadable / stays-orchestrator-side split is the always-on residue kept inline in CLAUDE.md:
**offloadable** covers `/validate`, `/validate-pr`, `/matrix-fit`, `/claim-fit`, `/reference-audit`,
`/screen-publications`, `verify`, `/full-qa`, `/fitness`, the read-only `/deep-assessment` probe
phases, research / draft seeds, the pre-push skeptical verifier, and the high-assurance adversarial
verifiers (the QA-to-workers transition is complete); **stays orchestrator-side** covers authoring corpus
prose, applying diffs, routing findings, writing audit-trail rows, merging, and interacting with the
maintainer.

**Pre-push verifier and high-assurance adversarial verifiers now run as workers (maintainer-directed
2026-07-19, sequenced with the transport; transition COMPLETE).** The pre-push skeptical verifier was
the one orchestrator-side QA exception (it is on the critical path, so offloading it adds a blocking
wait). It, and the high-assurance adversarial verifiers, now run as `orch-verify` WORKERS like every
other QA pass: `block-orchestrator-self-qa.py` blocks the in-session agent-spawning tools (Task/Agent/Workflow/SendMessage) for reasoning offload,
so there is no remaining orchestrator-side QA exception and no override allowlist (the actor-created once-only
sentinel is the only escape (a speed bump plus an audit record, not a security boundary)). Because
`orch-verify` runs the worker synchronously and returns its stdout directly (no async delivery tray to
poll), the offloaded verify is a direct call rather than an unbounded poll; `orch-verify` sets no
worker timeout, so a stalled CLI can still block, which the 20-minute reissue (point 4) mitigates.

**No-workers fallback (narrow).** A worker is SPAWNED ON DEMAND, so no liveness reading is ever the
fallback condition. The inline fallback is reserved for a genuine dispatch FAILURE, every eligible
account limited/exhausted (an auth or quota error surfaced from an actual `orch-verify` attempt) or the
transport down. In that narrow case only, self-run inline AFTER alerting the maintainer, and record the
reason. If such an inline self-run cannot be completed by the orchestrator alone (an inline
`/validate-pr` can reach that point), the only in-session route to a second agent is an explicitly
authorized in-session Task/Agent/Workflow/SendMessage dispatch that first consumes the once-only
sentinel `block-orchestrator-self-qa.py` requires; the reason goes in the QA row. Offload is
best-effort for AVAILABILITY, but the CHOICE to use an available worker is mandatory, and the
mandatory-QA discipline is unchanged (an offloaded run is the full formal pass, abbreviation is never
authorized).

**Worker-elasticity corollary (maintainer-directed 2026-07-19).** The ORCHESTRATOR is the scarce
singleton; WORKERS ARE ELASTIC (the maintainer can spin up more). So when parallelizable work exceeds
available concurrent worker capacity, PROACTIVELY tell the maintainer and request more workers, rather than quietly
serializing work through too few. Under-requesting wastes the orchestrator's own scarce time on
serialization the maintainer would gladly parallelize.

The design of record is `grc_library_private/credit-offload-design.md`; the orchestrator-side
operating discipline is `grc_library_private/orchestrator-claude.md` (`## Credit-offload mode`,
group A1).
