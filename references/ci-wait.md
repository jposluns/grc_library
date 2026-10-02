# CI and background-wait discipline (reference)

Relocated from `.claude/CLAUDE.md` `## PR activity subscription discipline` (3b177-d);
read at every CI or background wait, like a skill. The always-on core stays inline in
CLAUDE.md; gate 80 enforces the pointer pair via .claude/playbooks/PLAYBOOK-MANIFEST.yml.

PR workflow step 3 (waiting for CI to settle) and any subsequent wait for review comments
use `mcp__github__subscribe_pr_activity`. Subscriptions deliver failure events, comments,
and reviews into the conversation as they happen, but do not reliably deliver success
transitions or every state change, so a subscription alone can sit indefinitely on a
silent-success event.

The discipline: every `mcp__github__subscribe_pr_activity` call in the same turn arms a
paired 60-second fallback timer via `Bash` with `run_in_background: true`, command shape
`sleep 60 && echo "60s fallback timer fired - check PR #N status"`. When the webhook fires
or the timer completes (whichever comes first), check PR state with
`mcp__github__pull_request_read` (`get_check_runs` for CI, `get_status` for combined commit
status) and act on the actual result. If the PR is still in flight, re-arm a fresh
60-second timer. On merge, the subscription auto-unsubscribes; stop the timer with
`TaskStop` on the background task ID. The 60-second cadence balances latency against API
cost. This operationalizes the webhook-subscriptions discipline in
`.claude/rules/governance/action-before-explanation-of-inaction.md` and the
subscribe-over-poll pattern in `.claude/rules/governance/evidence-grounded-completion.md`.

**No-MCP (gh-CLI) sessions: read the GitHub Actions runs for the PR head SHA, bounded and
fail-loud, and DO NOT idle on it.** When the session has no GitHub MCP (`mcp__github__*`
absent from the tool list, so the PR mechanism is the `gh` CLI), there is no
`subscribe_pr_activity`. The `gh pr checks` subcommand (including its watch flag) does NOT
work in this project and is never prescribed or run: the project's fine-grained PAT cannot
read the GitHub Checks API, so every `gh pr checks` invocation fails regardless of PR
state. The readable surface is the Actions RUNS list for the PR's head SHA
(`gh api "repos/jposluns/grc_library/actions/runs?head_sha=<SHA>"`). Two failure modes are
FORBIDDEN: (a) bare `sleep 60 && echo "check status"` fallback timers, which pair with a
subscription that does not exist and self-check nothing, so they sprawl into overlapping
low-signal waits; and (b) a hand-rolled wait that can spin or exit SILENTLY (an unbounded
loop, or one that swallows an API error as "still pending"). Instead run ONE
timeout-bounded, fail-loud loop via `Bash` `run_in_background` that prints the terminal
state on EVERY exit path, shaped:
`timeout 1200 bash -c 'while :; do n=$(gh api "repos/jposluns/grc_library/actions/runs?head_sha=<SHA>" --jq "[.workflow_runs[] | select(.status == \"completed\") | .name] | unique | map(select(. == \"Repository quality checks\" or . == \"PR attribution\")) | length") || exit 9; [ "$n" -eq 2 ] && exit 0; sleep 30; done'; echo "runs-wait exited rc=$?"; gh api "repos/jposluns/grc_library/actions/runs?head_sha=<SHA>" --jq '.workflow_runs[] | .name + ": " + .status + "/" + (.conclusion // "pending")'`.
The loop exits 0 ONLY when each REQUIRED check is LISTED for the SHA, BY NAME, with
status `completed`: the required workflow runs are "Repository quality checks" and
"PR attribution" (the workflows carrying the required checks "Lint markdown corpus" and
"PR attribution (title and body)"; keep the loop's name list in step with
`REQUIRED_CHECKS`/`REQUIRED_WORKFLOWS` in `tools/merge-when-green.py`). Runs REGISTER
GRADUALLY after a push, so "every listed run is completed" is a KNOWN FALSE-DONE and is
never an exit condition: a required run that has not yet appeared keeps the loop waiting.
An API error exits 9 (loud, never a silent spin); the `timeout` caps the wait
at a hard ceiling (rc 124 on expiry); and the trailing `echo` plus the final per-run read
print the terminal state on EVERY exit path (pass, fail, API error, or timeout), so
silence is impossible. rc 0 means COMPLETED, not green: read the printed per-run
conclusions, and treat `tools/merge-when-green.py <N> --repo jposluns/grc_library
--dry-run` as the FINAL confirmed-green check before relying on a green reading (it reads
the PR's `statusCheckRollup`, which the PAT can read, and refuses on anything pending,
missing, or non-successful). Run exactly one such task; stop it with `TaskStop` once
settled. **Do NOT idle-block on the notification:** per the **Background-task check SOP**
below, check on the 60-second cadence and ACTIVELY PROBE (the same
`actions/runs?head_sha=<SHA>` read, unpiped) once past the check's typical duration (about
1-2 minutes here), because a stuck or silently-exited wait is indistinguishable from
"still running". Never hand-roll a CI-wait loop on a check command whose flags you have
not verified in THIS environment, and never leave a wait unbounded or silent. (The harness
also blocks foreground `sleep N && <cmd>` chains, so the wait always runs via
`run_in_background` or `Monitor`, never a foreground sleep.) lab_infra's fleet
`ci-status.sh --wait` will REPLACE this loop when it ships; until then the loop above is
the prescribed form (grc has no `ci-status.sh`).

**Background-task check SOP.** The same 60-second
cadence governs EVERY background task (a subagent, a background command, an external
wait), not only PR CI waits: check on every background task every 60 seconds until it
completes, re-arming the timer at each firing. Past the task's typical duration, do not
keep waiting passively for a completion notification; actively probe the task (a
`SendMessage` status check to a subagent, a state read for an external process), because
a background agent can stop silently WITHOUT delivering its result, and the completion
notification alone does not distinguish "still running" from "stalled". The stall tells:
no report past the typical duration, a dangling worktree, or liveness signals that stop
advancing.

**No long-interval check-ins.** Never ask for, propose,
or schedule a long-interval self check-in (an hour-out `send_later`, a deferred "I'll
check back later" of any shape), including when a harness or subscription boilerplate
suggests one: the 60-second cadence above IS the check-in mechanism, applied until the
awaited thing finishes or is confirmed looped, dead, or failed. A long-interval timer
adds nothing the 60-second loop does not already cover and costs the maintainer an
approval prompt.
