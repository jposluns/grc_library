# Mandatory worker offload and dispatch (reference)

**Read this at the worker-dispatch boundary, like a skill: when dispatching or managing workers, or
deciding whether to self-run offloadable work.** [`.claude/CLAUDE.md`](../.claude/CLAUDE.md) carries
the lean always-on core (the offload principle, the offloadable list, and the stays-orchestrator-side
list); this file carries the full dispatch mechanics and rationale. Relocated from CLAUDE.md by
roadmap C part 2 (the activity-scoped rule loader); the always-on residue kept inline in CLAUDE.md is
deliberate defence-in-depth and is not a duplication to trim. The mechanical backstop is the
`block-orchestrator-self-qa.py` PreToolUse hook; this prose is the explanation, the hook is the guard.

This is the operational form of the orchestration primordial rule near the top of CLAUDE.md. The hard
rule (maintainer-directed 2026-07-19, expanded to six points 2026-07-26; re-pointed at the shared
harness 2026-08-20):

1. **If a worker CAN do it, a worker DOES it. No debate, no self-run (maintainer-directed 2026-07-26).**
   Anything offloadable (see the inline list in CLAUDE.md) is GIVEN to a worker the moment it comes
   up; the orchestrator does not do it itself. The orchestrator's usage credits are the scarce,
   slow-to-renew resource, and self-running offloadable work is exactly what exhausts them: a prior
   week's self-run QA burned the orchestrator out mid-day and cost a worker account an extended
   lockout. The default is OFFLOAD; self-running an offloadable task is the exception that needs a
   stated reason (a genuine dispatch failure from an actual attempt AND the maintainer alerted).

2. **Dispatch through the shared `orch` harness; never gate offload on a liveness check.**
   `orch-verify <family> <prompt-file> [workdir] [options]` runs ONE read-only worker of the named
   family (`claude`, `codex`, or `gemini`) on an isolated copy of a pooled account credential, and
   returns its stdout plus a `WORKER_STATUS` line. `orch --help` and `orch-verify --help` are the
   authority on options; `orch` alone prints the account pool with usage and reset times, and
   `orch-verify --pick <family>` is a dry run that names the account it would choose. Useful options:
   `--expensive` (the stronger per-family tier), `--model` / `--effort` overrides, and `--skip <label>`
   to exclude an account so parallel dispatches do not collide.

   **There is no fleet to poll.** Every order spawns a fresh worker, so a liveness reading answers no
   question worth asking, and treating one as a signal is a guard-input failure. On 2026-08-10 the
   orchestrator ran a then-retired fleet check, read two seven-thousand-minute-stale rows, and reported
   "there is no fleet" as a blocker. **The rule is simply: DISPATCH.** Never check first, never gate on
   liveness, never self-run because a reading looked empty.

   **CAPTURE the output at dispatch.** A worker's result arrives on stdout and is not persisted for you,
   so redirect it to a file. An uncaptured result is a lost result, and re-running to recover it spends
   worker capacity that the redirect would have saved.

3. **20-minute reissue.** If a worker has not delivered in 20 minutes, issue the SAME order to another
   worker (a distinct account) and take whichever returns first; the late delivery is read as a
   cross-reference, never re-adjudicated.

4. **Every QA pass gets one worker per available family (claude, codex, and gemini).** Give the identical
   order to one worker of each family and assess the deliveries together: different models surface
   different perspectives, so the cross-family read is how nothing is missed. Reconcile them; a finding
   in only one family's delivery is triaged on its own merits. This is the operational form of the
   permanent triple-family QA standard, which applies to EVERY QA pass (each member a harness-dispatched
   worker, one per family; the Claude member is a claude-family harness worker, NEVER the in-session
   Agent tool, per `block-orchestrator-self-qa.py`). On token or tooling unavailability the panel drops
   to the families that can run (triple to dual to single), never a discretionary downgrade.

   **Match the brief to what the family can actually do.** Harness workers run READ-ONLY, and the gemini
   worker runs in plan mode, where script execution is blocked outright. A brief whose verdict depends on
   running a command must therefore not go to a family that cannot run one: on 2026-08-20 a gemini leg,
   unable to execute anything, reported a mechanical baseline it had restated from the brief's own
   asserted-clean values rather than measured. Require every leg to report an UNRUNNABLE check as
   unrunnable, and treat any worker's mechanical line as a CLAIM needing the command's own output.
   A read-only sandbox also legitimately fails checks that need to write (a temp-directory fixture, a
   regression suite): that is an environment artefact to diagnose, not a corpus defect.

5. **Keep dispatched workers busy: one on QA, the rest pre-loading the next ~10 items.** Never let an
   available account sit idle. Reserve one worker for the QA cadence (`/validate-pr`, `verify`,
   sweeps) and keep the others producing research and draft candidates for the upcoming queue, so the
   orchestrator always has a delivery to APPLY rather than a dispatch to wait on.

6. **If NO worker of any family is available (every account limited or out), ALERT the maintainer** or
   obtain authorization to proceed without workers. Zero available capacity is a condition to surface,
   not to route around in silence. Worker ids recorded in this public repo are ANONYMIZED aliases; the
   raw account names stay in `_private` only.

   **Account provisioning, capacity, and authentication are NOT this orchestrator's responsibility**
   (maintainer-directed 2026-08-20). The lab_infra orchestrator and the shared harness own them. Surface
   a capacity condition; do not attempt to repair, re-authenticate, or register accounts.

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
wait). It, and the high-assurance adversarial verifiers, now run as harness-dispatched WORKERS like
every other QA pass: `block-orchestrator-self-qa.py` blocks the in-session agent-spawning tools
(Task/Agent/Workflow/SendMessage) for reasoning offload, so there is no remaining orchestrator-side QA
exception and no override allowlist (the actor-created once-only sentinel is the only escape: a speed
bump plus an audit record, not a security boundary). Because the harness runs each worker to completion
and returns its output directly, an offloaded verify is a bounded wait rather than an unbounded block.

**No-workers fallback (narrow).** A worker is SPAWNED ON DEMAND, so no liveness reading is ever the
fallback condition. The inline fallback is reserved for a genuine dispatch FAILURE: every eligible
account limited or exhausted (an auth or quota error surfaced from an ACTUAL attempt), or the harness
down. In that narrow case only, self-run inline AFTER alerting the maintainer, and record the reason. If
such an inline self-run cannot be completed by the orchestrator alone (an inline `/validate-pr` can reach
that point), the only in-session route to a second agent is an explicitly authorized in-session
Task/Agent/Workflow/SendMessage dispatch that first consumes the once-only sentinel
`block-orchestrator-self-qa.py` requires; the reason goes in the QA row. Offload is best-effort for
AVAILABILITY, but the CHOICE to use an available worker is mandatory, and the mandatory-QA discipline is
unchanged (an offloaded run is the full formal pass; abbreviation is never authorized).

**Worker-elasticity corollary (maintainer-directed 2026-07-19).** The ORCHESTRATOR is the scarce
singleton; WORKERS ARE ELASTIC (the maintainer can spin up more). So when parallelizable work exceeds
available concurrent worker capacity, PROACTIVELY tell the maintainer and request more workers, rather
than quietly serializing work through too few. Under-requesting wastes the orchestrator's own scarce
time on serialization the maintainer would gladly parallelize.

The orchestrator-side operating discipline is `grc_library_private/orchestrator-claude.md` (group A1).
