# Worker prompt log

Every prompt the orchestrator injected into a worker's tmux session, one row each.

Keystroke injection into a session running as another user is invisible unless
recorded, so it is recorded. Only the closed verb set in `tools/manage-workers.py`
can appear in the verb column; nothing here is ever composed from worker output.

| UTC | session | runtime | verb | held order | reason | keys sent |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-07-25T14:05:46Z | worker | claude | wake | none | first live test of the injection path; opus queue is empty so this is a harmless no-op probe | `/credit-offload` |
| 2026-07-25T14:14:45Z | worker1 | claude | wake | none | two prio-0 validate-pr sweeps just dispatched; worker1 is idle | `/credit-offload` |
| 2026-07-25T15:40:24Z | codex | codex | wake | none | two codex-family orders have been in available-work since 11:24 and this worker last polled 16m ago | `At your next opportunity, resync your grc_library_scratch clone and check in: claim the next waiting order in your family if you are not already working.` |
| 2026-07-25T15:40:24Z | worker1 | claude | wake | none | heartbeat frozen 40m; validate-pr-1169 is unclaimed and this worker is eligible | `/credit-offload` |
| 2026-07-25T15:42:11Z | codex | codex | wake | none | verifying the two-call send fix: the previous one-call send left the prompt unsubmitted and the maintainer pressed Enter by hand | `At your next opportunity, resync your grc_library_scratch clone and check in: claim the next waiting order in your family if you are not already working.` |
