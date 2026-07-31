# Mandatory worker offload and dispatch (reference)

**Read this at the worker-dispatch boundary, like a skill: when dispatching or managing workers, or
deciding whether to self-run offloadable work.** [`.claude/CLAUDE.md`](../.claude/CLAUDE.md) carries
the lean always-on core (the offload principle, the offloadable list, and the stays-orchestrator-side
list); this file carries the full dispatch mechanics and rationale. Relocated from CLAUDE.md by
roadmap C part 2 (the activity-scoped rule loader); the always-on residue kept inline in CLAUDE.md is
deliberate defence-in-depth and is not a duplication to trim. The mechanical backstop is the
`block-mandatory-offload.py` PreToolUse hook; this prose is the explanation, the hook is the guard.

This is the operational form of the orchestration primordial rule near the top of CLAUDE.md. The hard
rule (maintainer-directed 2026-07-19, expanded to six points 2026-07-26):

1. **If a worker CAN do it, a worker DOES it. No debate, no self-run (maintainer-directed 2026-07-26).**
   Anything offloadable (see the inline list in CLAUDE.md) is GIVEN to a worker the moment it comes
   up; the orchestrator does not do it itself. The orchestrator's usage credits are the scarce,
   slow-to-renew resource, and self-running offloadable work is exactly what exhausts them: a prior
   week's self-run QA burned the orchestrator out mid-Saturday and cost a worker account a multi-day
   lockout. The default is OFFLOAD; self-running an offloadable task is the exception that needs a
   stated reason (no worker of any family available AND the maintainer alerted).
2. **Spawn workers ON DEMAND with [`tools/exec-dispatch.py`](../tools/exec-dispatch.py); do NOT gate
   offload on `list-workers`.** The exec'd-worker system spawns a FRESH worker per order:
   `python3 tools/exec-dispatch.py --dispatch --family {claude|codex} --model <m> --effort <e>
   --account <acct> --order-id <id> --prompt-file <path>` (the prompt file MUST live under
   `/var/lib/grc-worker-jobs`; the account pool and dispatch policy live in the `_private`
   worker-accounts config; parallelism is DISTINCT accounts, one purpose per account, until the
   per-account-concurrency backlog item lands). A `list-workers` reading of zero is the STANDING-POLL
   fleet sitting idle, NOT "no workers", and is NEVER a licence to self-run: a felt "0 workers" is the
   signal to SPAWN one with exec-dispatch, not to do the work yourself. (This is the mistake that
   recurred 2026-07-26.)
3. **20-minute reissue.** If a worker has not delivered in 20 minutes, issue the SAME order to another
   worker (a distinct account) and take whichever returns first; the late delivery is read as a
   cross-reference, never re-adjudicated.
4. **Super-sensitive tasks get BOTH a Codex and a Claude worker.** Give the identical order to one of
   each family and assess the two deliveries together: different models surface different
   perspectives, so the dual read is how nothing is missed. Reconcile them; a finding in only one is
   triaged on its own merits.
5. **Keep the fleet busy: one worker on QA, the rest pre-loading the next ~10 items.** Never let an
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
phases, and research / draft seeds; **stays orchestrator-side** covers authoring corpus prose,
applying diffs, routing findings, writing audit-trail rows, merging, interacting with the maintainer,
and (transitionally, below) the PRE-PUSH skeptical verifier plus the high-assurance adversarial
verifiers.

**Pre-push verifier moves to workers (maintainer-directed 2026-07-19; DECIDED, sequenced with the
transport).** The pre-push skeptical verifier was the one orchestrator-side QA exception (it is on the
critical path, so offloading it adds a blocking wait). The maintainer decided it ALSO moves to a
worker; the move lands WITH the local-VM file-drop / unix-socket transport ([`TODO.md`](../TODO.md)
§3.87, bumped to near-term) that makes the offloaded verify sub-second instead of a slow git
round-trip. Until that transport lands, the pre-push verifier stays orchestrator-side, and the
`block-mandatory-offload.py` override allowlist treats it (and the high-assurance adversarial
verifiers) as always-allowed, so the guardrail never blocks a legitimate critical-path verifier.

**No-workers fallback.** With zero live workers (or an order that goes stale unserved), self-run the
pass inline, AFTER alerting the maintainer or confirming authorization per rule 2. Offload is
best-effort for AVAILABILITY, but the CHOICE to use an available worker is mandatory; the mandatory-QA
discipline itself is unchanged (an offloaded run is the full formal pass, abbreviation is never
authorized).

**Worker-elasticity corollary (maintainer-directed 2026-07-19).** The ORCHESTRATOR is the scarce
singleton; WORKERS ARE ELASTIC (the maintainer can spin up more). So when parallelizable work exceeds
the live worker pool, PROACTIVELY tell the maintainer and request more workers, rather than quietly
serializing work through too few. Under-requesting wastes the orchestrator's own scarce time on
serialization the maintainer would gladly parallelize.

The design of record is `grc_library_private/credit-offload-design.md`; the orchestrator-side
operating discipline is `grc_library_private/orchestrator-claude.md` (`## Credit-offload mode`,
group A1).
