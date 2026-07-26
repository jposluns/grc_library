---
description: Recover a project whose orchestrator died or ran out of usage mid-session. A new session (often a new identity) assesses read-only, reports and asks, then recovers the interrupted work, winds down to a clean green `main`, and hands off to a same-session `/resume`. Change NOTHING until the maintainer gives an express, work-naming GO.
---

# /restore-broken

The recovery counterpart to [`/resume`](resume.md). `/resume` rebuilds from a CLEAN
session-closing handoff. `/restore-broken` is for the case where there is NO clean handoff: the
previous orchestrator **died, ran out of usage, or was interrupted mid-session**, so `main`, the
lease, the handoff, and the delivery tray are in a partly-applied, internally-inconsistent state,
and often the recovering session is a DIFFERENT identity than the one that died.

The goal is not to guess what the dead session intended. It is to (1) observe the true state
without changing it, (2) surface it to the maintainer with a plan and the decisions only they can
make, (3) recover the interrupted unit of work with independent verification, (4) land a clean,
green, reconciled `main`, and (5) hand off to a same-session `/resume` whose corpus-wide `/validate`
is the compensating control that catches anything the recovery missed.

**Run this recovery on a HIGH reasoning effort.** A broken-orchestrator takeover is exactly the
gate-blind, high-stakes work where a missed nuance is expensive (the motivating run caught a faithful
ledger de-fusion that a lower-effort pass would likely have waved through on a length mismatch). Drop
back to the routine effort only after the handoff is clean.

## PRIMORDIAL CONSTRAINT: change nothing until an express GO

The assessment phase is **strictly read-only**. No edit, commit, push, merge, lease write, order
dispatch, or tray move until the maintainer gives an express, work-naming GO on a named phase. This
is [`express-authorization-before-execution`](../rules/governance/express-authorization-before-execution.md)
applied to recovery: an interrupted state is exactly where a confident wrong action does the most
damage. Reading, listing, and read-only `git` / `gh` / API calls are the only actions in Phase A.

## Phase A: assess (read-only)

Emit the AIQT check line, then observe. Do NOT infer state you can read.

1. **Identity and environment.** `id`; list the launch root and every sibling repo; establish which
   user this session runs as versus which user the dead orchestrator ran as (a takeover is common).
2. **The interrupted unit.** For the primary repo: current branch, `git log` versus `origin/main`,
   unpushed commits (`origin/main..HEAD`), a dirty working tree, stashes, other worktrees, shallow?
   Enumerate open PRs (`gh pr list`) and recently merged PRs. Identify the branch and commits the
   dead session was building but never pushed or merged.
3. **The durable state records.** Read in full: the session handoff, the concurrency lease
   (`session-state.md`), the overnight-PR status file, `next-prs.txt`, `open-findings.md`,
   `pending-decisions.md`, `TODO.md` forward sections, and any transition or handoff document a
   departing worker or the maintainer left at the launch root or in the inbox. Note where the lease
   and handoff DISAGREE with live HEAD (that gap is the fingerprint of the interruption).
4. **The worker and exchange state.** Worker liveness across families; the delivery tray
   (`inbox/deliveries/`) and the issue channel (`inbox/*.md`); orders claimed-but-undelivered. Many
   tray deliveries may already be reflected in merged PRs but never swept to `done/`: assess each; do
   NOT assume the tray count is the unprocessed count.
5. **SAFETY: does ending this turn change anything?** Check for a **Stop / SessionEnd / PostToolUse
   hook** (project `settings.json` AND user-level) that auto-commits or auto-pushes on turn end. If
   one exists and the tree is dirty, ending the turn is itself a mutation: account for it before
   proceeding. Confirm git identity, that the token grants the access the orchestrator role needs
   (`gh api repos/<owner>/<repo> --jq .permissions`, read-only), and which **PreToolUse guard hooks**
   are active (they will shape recovery). Run the permission-model health check if the project ships
   one (`check_perms.sh --check`) so a manual permission slip is caught before it bites a worker.
6. **The lease's recorded operating-mode is a trap.** If the dead session left an unattended
   `Operating-mode`, the AskUserQuestion-blocking hook will REFUSE interactive questions until the
   mode is reconciled. Until then, **ask the maintainer in plain prose** rather than via the question
   tool; do not change the lease to unblock the tool before the maintainer has authorized any write.
7. **Is anything still running?** Hunt for a leftover automation the dead session started that is
   still acting: cron, systemd user timers, `at`, detached processes (a worker-nudge or poll loop),
   background tasks. A log file whose mtime has stopped advancing is evidence the automation died with
   the session; a still-advancing one is a live process to stop (with authorization).

## Phase B: report and ask (prose; get an express GO)

Report, scannable, no diffs dumped to chat:
- The interrupted-unit state (branch, unpushed commits, dirty files, is it green?).
- The safety findings (turn-end safe? identity and permissions OK? which hooks active?).
- The exchange backlog (tray, issues) and worker liveness.
- Any external assessment left for triage.
- A **phased recovery plan** and the decisions only the maintainer can make, recommendation first:
  how to handle the interrupted PR (verify-then-land / review-first / park); worker bring-up timing;
  ordering. Then **wait for an express GO** naming the phase(s) to start.

## Phase C: recover (only after GO)

1. **Verify the interrupted unit by observation, not inheritance.** Inherited work is a HYPOTHESIS
   ([`evidence-grounded-completion`](../rules/governance/evidence-grounded-completion.md)): run the
   full audit suite and PR-time checks standalone; independently re-read the diff; for any recovered
   or reconstructed data (a repaired ledger, a restored record), confirm each piece traces to a real
   prior git revision (`git show <sha>:<path>`, pickaxe `-S`), never accepting "restored" on trust.
2. **Independent adversarial verification.** For a substantive interrupted unit, put an INDEPENDENT
   refute-briefed lens on it before it lands. If workers are live, offload it (durable in the exchange
   even if this session is fragile); else self-run inline. Re-verify positive findings at source; fix
   real defects before landing; never land a defect you found.
3. **Land or park** the unit per the maintainer decision, logging any protected-branch bypass.
4. **Reconcile identity and lease.** ACQUIRE the lease under THIS session and the CORRECT operating
   mode (the takeover mode the maintainer set, for example daytime attended-autonomous), replacing the
   dead session's stale declaration.
5. **Reconcile the delivery tray.** Archive already-processed deliveries to `done/`; surface
   genuinely-open findings and route or fix them. Move, never delete; the tray move is the only
   processed-marker.
6. **Triage any external assessment** against the live backlog and merged PRs; re-verify positives at
   source; present the routed set for maintainer sign-off, never self-closing it.

## Phase D: wind down to a clean green `main`

Land the recovered working state as a **session-closing handoff PR** (a green, merged PR), per the
[`session-lifecycle`](../rules/governance/session-lifecycle.md) closing-handoff discipline: refresh
the handoff (state snapshot, next-actions and deferred queue, **asserted expectations** scoped to what
recovery touched, green-at-`<sha>`), RELEASE the lease. The closing PR is exempt from its own trailing
per-PR QA (loop-break); the compensating control is the next `/resume`'s corpus-wide `/validate`. **Do
not close over a large UNVALIDATED substantive PR**: the interrupted unit gets its verification (Phase
C) BEFORE the closing handoff.

## Phase E: same-session /resume (the catch-net)

The maintainer brings workers up (if not already) and, in the SAME conversation (re-opened in a durable
tmux if the recovering session was not in one), sends `/resume`. Resuming in the same session is
deliberately stronger than a fresh one: it keeps the context the recovery built AND rebuilds state from
the now-clean `main`. The resume runs its lease step-0, verifies the handoff snapshot against live files
**for real, never shortcutting from memory just because "I remember"**, and runs the loop-break
corpus-wide `/validate` (offloaded to the now-live workers) as the compensating control, cross-checking
the recovery's asserted-clean claims. A contradiction of an asserted-clean surface is a genuine recovery
miss to escalate; ordinary findings route to the backlog. Then continue the deferred queue.

## The failure modes this command exists to prevent

- **Trusting the dead session's "done".** Its last state is a hypothesis; a repaired ledger or a
  merged-but-unvalidated PR is exactly where an escaped defect hides.
- **Changing state before observing it** (or before the express GO), turning a recoverable interrupt
  into a harder-to-reverse mess.
- **Assuming turn-end is inert** when a Stop hook would auto-commit the dirty tree.
- **Letting a stale lease's unattended mode silently suppress the questions** the recovery needs to ask.
- **Reading the tray count as the unprocessed count** and re-actioning already-merged findings.
- **Winding down over an unvalidated interrupted PR**, or resuming without running the compensating
  `/validate`.
