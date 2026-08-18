# Mandatory worker offload and dispatch (reference)

**Read this at the worker-dispatch boundary, like a skill: when dispatching or managing workers, or
deciding whether to self-run offloadable work.** [`.claude/CLAUDE.md`](../.claude/CLAUDE.md) carries
the lean always-on core (the offload principle, the offloadable list, and the stays-orchestrator-side
list); this file carries the full dispatch mechanics and rationale. Relocated from CLAUDE.md by
roadmap C part 2 (the activity-scoped rule loader); the always-on residue kept inline in CLAUDE.md is
deliberate defence-in-depth and is not a duplication to trim. The mechanical backstop is the
`block-orchestrator-self-qa.py` PreToolUse hook; this prose is the explanation, the hook is the guard.

This is the operational form of the orchestration primordial rule near the top of CLAUDE.md. The hard
rule (maintainer-directed 2026-07-19, expanded to six points 2026-07-26):

1. **If a worker CAN do it, a worker DOES it. No debate, no self-run (maintainer-directed 2026-07-26).**
   Anything offloadable (see the inline list in CLAUDE.md) is GIVEN to a worker the moment it comes
   up; the orchestrator does not do it itself. The orchestrator's usage credits are the scarce,
   slow-to-renew resource, and self-running offloadable work is exactly what exhausts them: a prior
   week's self-run QA burned the orchestrator out mid-day and cost a worker account an extended lockout. The default is OFFLOAD; self-running an offloadable task is the exception that needs a
   stated reason (a genuine exec-dispatch failure from an actual attempt AND the maintainer alerted).
2. **Spawn workers ON DEMAND with [`tools/exec-dispatch.py`](../tools/exec-dispatch.py); do NOT gate
   offload on `list-workers`.** The exec'd-worker system spawns a FRESH worker per order:
   `python3 tools/exec-dispatch.py --dispatch --family {claude|codex|gemini} --model <m> --effort <e>
   --account <acct> --order-id <id> --prompt-file <path>` (the prompt file MUST live under
   the job directory named in the `_private` worker-accounts config (`wrapper.job_dir`); the account pool and dispatch policy live in the `_private`
   worker-accounts config; parallelism is DISTINCT accounts, one purpose per account, until the
   per-account-concurrency backlog item lands). **`list-workers` IS RETIRED and there is no fleet to
   poll** (maintainer-directed 2026-08-10: "list-workers shouldn't exist anymore, we ONLY exec
   dispatch"). Earlier text here described a "standing-poll fleet sitting idle" whose empty reading
   was never a licence to self-run. That framing is now wrong in a way that still misleads: there is
   no standing pool at all, so a liveness reading answers no question worth asking, and treating an
   empty or stale one as a signal is a guard-input failure. On 2026-08-10 the orchestrator ran the
   retired check, read two seven-thousand-minute-stale rows, and reported "there is no fleet" as a
   blocker. **The rule is simply: DISPATCH.** Never check first, never gate on liveness, never
   self-run because a reading looked empty.
3. **20-minute reissue.** If a worker has not delivered in 20 minutes, issue the SAME order to another
   worker (a distinct account) and take whichever returns first; the late delivery is read as a
   cross-reference, never re-adjudicated.
4. **Every QA pass gets one worker per available family (claude, codex, and gemini).** Give the identical
   order to one worker of each family and assess the deliveries together: different models surface
   different perspectives, so the cross-family read is how nothing is missed. Reconcile them; a finding
   in only one family's delivery is triaged on its own merits. This is the operational form of the
   permanent triple-family QA standard, which applies to EVERY QA pass (each member an exec-dispatch
   worker, one per family; the Claude member is a claude-family exec-dispatch worker, NEVER the in-session
   Agent tool, per `block-orchestrator-self-qa.py`). On token or tooling unavailability the panel drops
   to the families that can run (triple to dual to single), never a discretionary downgrade.
5. **Keep dispatched workers busy: one on QA, the rest pre-loading the next ~10 items.** Never let an
   available account sit idle. Reserve one worker for the QA cadence (`/validate-pr`, `verify`,
   sweeps) and keep the others producing research and draft candidates for the upcoming queue, so the
   orchestrator always has a delivery to APPLY rather than a dispatch to wait on.
6. **If NO worker of any family is available (every account limited or out), ALERT the maintainer** or
   obtain authorization to proceed without workers. Zero available capacity is a condition to surface,
   not to route around in silence. Worker ids recorded in this public repo are ANONYMIZED aliases; the
   raw `<family>-<account>-<timestamp>` id and all account names stay in `_private` only.

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
wait). It, and the high-assurance adversarial verifiers, now run as exec-dispatch WORKERS like every
other QA pass: `block-orchestrator-self-qa.py` blocks the in-session agent-spawning tools (Task/Agent/Workflow/SendMessage) for reasoning offload,
so there is no remaining orchestrator-side QA exception and no override allowlist (the actor-created once-only
sentinel is the only escape (a speed bump plus an audit record, not a security boundary)). The exec-dispatch transport (the file-drop plane and the on-demand
`run-codex-worker` / `exec-dispatch.py` invocation) makes the offloaded verify a bounded wait rather
than an unbounded block.

**No-workers fallback (narrow).** A worker is SPAWNED ON DEMAND, so no liveness reading is ever the
fallback condition, and `list-workers` is retired outright. The inline fallback is reserved for a genuine
exec-dispatch FAILURE, every eligible account limited/exhausted (an auth or quota error surfaced from an
actual exec attempt) or the transport down. In that narrow case only, self-run inline AFTER alerting the
maintainer, and record the reason. If such an inline self-run cannot be completed by the
orchestrator alone (an inline `/validate-pr` can reach that point), the only in-session route to a
second agent is an explicitly authorized in-session Task/Agent/Workflow/SendMessage dispatch that
first consumes the once-only sentinel `block-orchestrator-self-qa.py` requires; the reason goes in
the QA row. Offload is best-effort for AVAILABILITY, but the CHOICE to use an
available worker is mandatory, and the mandatory-QA discipline is unchanged (an offloaded run is the full
formal pass, abbreviation is never authorized).

**Worker-elasticity corollary (maintainer-directed 2026-07-19).** The ORCHESTRATOR is the scarce
singleton; WORKERS ARE ELASTIC (the maintainer can spin up more). So when parallelizable work exceeds
available concurrent worker capacity, PROACTIVELY tell the maintainer and request more workers, rather than quietly
serializing work through too few. Under-requesting wastes the orchestrator's own scarce time on
serialization the maintainer would gladly parallelize.

The design of record is `grc_library_private/credit-offload-design.md`; the orchestrator-side
operating discipline is `grc_library_private/orchestrator-claude.md` (`## Credit-offload mode`,
group A1).
