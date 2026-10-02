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
`subscribe_pr_activity`. The `/orch` resume protocol and lab_infra's 2026-10-02
12:33Z note report that the project's fine-grained token cannot read the Checks API;
the project therefore does not use `gh pr checks` (including its watch flag).
Read the Actions RUNS list for the PR's head SHA
(`actions/runs?head_sha=<SHA>`). Two failure modes are
FORBIDDEN: (a) bare `sleep 60 && echo "check status"` fallback timers, which pair with a
subscription that does not exist and self-check nothing, so they sprawl into overlapping
low-signal waits; and (b) a hand-rolled wait that can spin or exit SILENTLY (an unbounded
loop, or one that swallows an API error as "still pending"). Instead run ONE
timeout-bounded, fail-loud loop via `Bash` `run_in_background` where permitted.
Replace `<SHA>` with the PR head SHA; execute the complete subshell as one command:

```bash
(
  if python3 - <<'WAIT'
import os
import signal
import subprocess
import sys

command = r"""
import json
import subprocess
import sys
import time

required = ("Repository quality checks", "PR attribution")
while True:
    print("Reading Actions runs; previous snapshot (if any) may be stale.", flush=True)
    response = subprocess.run([
        "gh", "api", "--paginate", "--slurp",
        "repos/jposluns/grc_library/actions/runs?head_sha=<SHA>&per_page=100",
    ], stdout=subprocess.PIPE, text=True)
    if response.returncode:
        print(f"Actions API/query failed rc={response.returncode}; current state unknown.", flush=True)
        sys.exit(9)
    try:
        latest = {}
        pages = json.loads(response.stdout)
        for run in (run for page in pages for run in page["workflow_runs"]):
            name = run["name"]
            if name not in required:
                continue
            key = lambda item: (item["run_number"], item["run_attempt"], item["id"])
            if name not in latest or key(run) > key(latest[name]):
                latest[name] = run
        for name in required:
            run = latest.get(name)
            print(f"{name}: {run['status']}/{run['conclusion'] or 'pending'}"
                  if run else f"{name}: missing", flush=True)
        failed = any(run["status"] == "completed" and run["conclusion"] != "success"
                     for run in latest.values())
        completed = len(latest) == len(required) and all(
            run["status"] == "completed" for run in latest.values())
    except (ValueError, KeyError, TypeError) as error:
        print(f"Invalid Actions response: {error}; current state unknown.", flush=True)
        sys.exit(9)
    print("failed" if failed else "completed" if completed else "pending", flush=True)
    if failed:
        sys.exit(1)
    if completed:
        sys.exit(0)
    time.sleep(30)
"""
task = subprocess.Popen([sys.executable, "-c", command], start_new_session=True)
try:
    task.communicate(timeout=1200)
except subprocess.TimeoutExpired:
    try:
        os.killpg(task.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    task.communicate()
    sys.exit(124)
sys.exit(task.returncode if task.returncode >= 0 else 128 - task.returncode)
WAIT
  then rc=0; else rc=$?; fi
  printf 'runs-wait exited rc=%s; last snapshot may be stale or absent.\n' "$rc"
  exit "$rc"
)
```

The snippet needs Bash, Python 3 (stdlib only), and the GitHub CLI. `--paginate`
with `--slurp` returns raw page objects; Python flattens their `workflow_runs` arrays
and selects and evaluates the latest runs. Do not combine `--slurp` with `--jq` or
`--template`: gh rejects those combinations. Regression fixtures enforce the exact
supported arguments and return raw pages, exercising the production flattening.

The loop matches each REQUIRED workflow BY NAME across every API page and judges only
its LATEST run (highest `run_number`, then `run_attempt`, then `id`). An older failed
or pending run is superseded; a newer pending run or attempt still blocks completion.
The required workflows are "Repository quality checks" and "PR attribution", carrying
the required checks "Lint markdown corpus" and "PR attribution (title and body)".
Keep the names in step with `REQUIRED_CHECKS`/`REQUIRED_WORKFLOWS` in
`tools/merge-when-green.py`. Runs REGISTER GRADUALLY: a missing required name keeps
waiting; unrelated workflows cannot substitute for it.

Every snapshot prints missing names and each latest required run's status/conclusion.
Any latest completed required run with a non-success conclusion exits 1; API/query errors
exit 9 and report their original status. The supervisor creates a separate session
and process group (`start_new_session=True` calls `setsid`); at 1200 seconds it sends
KILL to that whole group, including descendants that ignore TERM, and exits 124.
The enclosing subshell prints and returns the captured
status even under `set -e`. ALL API calls, including pagination, are inside the
deadline; there is no final diagnostic API read to hang or overwrite a failure.
On API error or timeout the last printed snapshot may be stale or absent, so current
CI state is unknown. rc 0 requires each latest required run to succeed; still use
`tools/merge-when-green.py <N> --repo jposluns/grc_library --dry-run` as the FINAL
confirmed-green check before merge (it reads the PR's current `statusCheckRollup`
and falls back to Actions runs when the rollup is unreadable for repositories configured
in `ACTIONS_FALLBACK`; it refuses pending, missing, or non-successful checks).

Run exactly one such task. **Do NOT idle-block on the notification:** per the
**Background-task check SOP** below, check on the 60-second cadence and ACTIVELY PROBE
once past typical duration (about 1-2 minutes here). Bound any separate probe with
the same supervisor, setting `timeout=60` and `command` to
`'import subprocess, sys; sys.exit(subprocess.call(["gh", "api", "repos/jposluns/grc_library/actions/runs?head_sha=<SHA>"]))'`,
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
