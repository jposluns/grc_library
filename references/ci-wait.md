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
(`actions/runs?head_sha=<SHA>`). Two failure modes are
FORBIDDEN: (a) bare `sleep 60 && echo "check status"` fallback timers, which pair with a
subscription that does not exist and self-check nothing, so they sprawl into overlapping
low-signal waits; and (b) a hand-rolled wait that can spin or exit SILENTLY (an unbounded
loop, or one that swallows an API error as "still pending"). Instead run ONE
timeout-bounded, fail-loud loop via `Bash` `run_in_background` where permitted.
Replace `<SHA>` with the PR head SHA; execute the complete subshell as one command:

```bash
(
  if timeout --kill-after=1 1199 bash <<'WAIT'
while :; do
  echo "Reading Actions runs; previous snapshot (if any) may be stale."
  snapshot=$(gh api --paginate --slurp \
    "repos/jposluns/grc_library/actions/runs?head_sha=<SHA>&per_page=100" --jq '
      [.[].workflow_runs[]] as $runs |
      ["Repository quality checks", "PR attribution"] as $required |
      [$runs[] | select(.name as $name | $required | index($name))] as $relevant |
      ($required[] as $name |
        [$relevant[] | select(.name == $name)] as $matches |
        if ($matches | length) == 0 then "\($name): missing"
        else $matches[] | "\(.name): \(.status)/\(.conclusion // "pending")" end),
      (if any($relevant[]; .status == "completed" and .conclusion != "success")
       then "failed"
       elif all($required[]; . as $name | any($relevant[]; .name == $name))
         and all($relevant[]; .status == "completed")
       then "completed"
       else "pending" end)
    ') || { api_rc=$?; echo "Actions API/query failed rc=$api_rc; current state unknown."; exit 9; }
  printf '%s\n' "$snapshot"
  case "${snapshot##*$'\n'}" in
    completed) exit 0 ;;
    failed) exit 1 ;;
    pending) sleep 30 ;;
    *) echo "Invalid wait state; current state unknown."; exit 9 ;;
  esac
done
WAIT
  then rc=0; else rc=$?; fi
  printf 'runs-wait exited rc=%s; last snapshot may be stale or absent.\n' "$rc"
  exit "$rc"
)
```

The loop matches each REQUIRED workflow BY NAME across every API page and requires
ALL its listed runs to be completed, including pending reruns beside older successes.
The required workflows are "Repository quality checks" and "PR attribution", carrying
the required checks "Lint markdown corpus" and "PR attribution (title and body)".
Keep the names in step with `REQUIRED_CHECKS`/`REQUIRED_WORKFLOWS` in
`tools/merge-when-green.py`. Runs REGISTER GRADUALLY: a missing required name keeps
waiting; unrelated workflows cannot substitute for it.

Every snapshot prints missing names and each required run's status/conclusion.
Any completed required run with a non-success conclusion exits 1; API/query errors
exit 9 and report their original status. The deadline is 1199 seconds plus at most
one second of forced-stop grace (1200 seconds total); timeout exits 124, or 137 if
forced termination is needed. The enclosing subshell prints and returns the captured
status even under `set -e`. ALL API calls, including pagination, are inside the
deadline; there is no final diagnostic API read to hang or overwrite a failure.
On API error or timeout the last printed snapshot may be stale or absent, so current
CI state is unknown. rc 0 requires every listed required run to succeed; still use
`tools/merge-when-green.py <N> --repo jposluns/grc_library --dry-run` as the FINAL
confirmed-green check before merge (it reads the PR's current `statusCheckRollup`
and refuses pending, missing, or non-successful checks).

Run exactly one such task. **Do NOT idle-block on the notification:** per the
**Background-task check SOP** below, check on the 60-second cadence and ACTIVELY PROBE
once past typical duration (about 1-2 minutes here). Bound any separate probe too:
`timeout --kill-after=1 59 gh api "repos/jposluns/grc_library/actions/runs?head_sha=<SHA>"`,
un-piped, preserving its exit status. Never hand-roll a wait on unverified flags or
leave it unbounded or silent. A foreground-only worker executes the same bounded
command synchronously; the background-task machinery applies only where permitted.
lab_infra's fleet `ci-status.sh --wait` will REPLACE this loop when it ships; until
then the loop above is the prescribed form (grc has no `ci-status.sh`).

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
