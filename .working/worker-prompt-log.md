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
| 2026-07-25T15:42:11Z | codex | codex | wake | none | verifying the two-call send fix: the previous one-call send left the prompt unsubmitted and the maintainer pressed Enter by hand | `At your next opportunity, resync your grc_library_scratch clone and check in: claim the next waiting order in your family if you are not already working.` |
| 2026-07-25T16:05:10Z | worker | claude | reload | none | worker contract changed: issues now go to inbox/ as an immediate drop, and deliver is atomic plus sentinel-stamped | `When you finish your current task, re-read your worker contract at grc_library_scratch/AGENTS.md and your skills, then continue.` |
| 2026-07-25T16:05:11Z | worker1 | claude | reload | none | worker contract changed: issues now go to inbox/ as an immediate drop, and deliver is atomic plus sentinel-stamped | `When you finish your current task, re-read your worker contract at grc_library_scratch/AGENTS.md and your skills, then continue.` |
| 2026-07-25T16:07:25Z | worker | claude | reload | none | correcting the previous reload, which pointed this Claude worker at the Codex contract | `When you finish your current task, re-read your worker contract at grc_library_scratch/CLAUDE.md and your skills, then continue.` |
| 2026-07-25T17:04:46Z | codex | codex | wake | none | a codex-family finder order is waiting: hunt-unsound-guard-inputs | `At your next opportunity, resync your grc_library_scratch clone and check in: claim the next waiting order in your family if you are not already working.` |
| 2026-07-25T18:08:18Z | codex | codex | wake | none | reclaimed hunt-unsound-guard-inputs from a worker stale 63m while holding it; a fresh session should claim it | `At your next opportunity, resync your grc_library_scratch clone and check in: claim the next waiting order in your family if you are not already working.` |
| 2026-07-25T20:39:09Z | mailz | codex | wake | none | Check in: re-register your heartbeat and claim from available-work. QA orders are queued and the fleet reads only 2 live of 4. | `At your next opportunity, resync your grc_library_scratch clone and check in: claim the next waiting order in your family if you are not already working.` |
| 2026-07-25T20:39:10Z | codex | codex | wake | none | Check in: re-register your heartbeat and claim from available-work. QA orders are queued and the fleet reads only 2 live of 4. | `At your next opportunity, resync your grc_library_scratch clone and check in: claim the next waiting order in your family if you are not already working.` |
| 2026-07-25T21:04:48Z | worker | claude | wake | none | URGENT re selftest-gaps orders: tools/audit-selftest-discriminability.py at pinned SHA dd28405d RECURSES INTO ITSELF if run with no arguments, spawning runaway processes. Run it ONLY as 'python3 tools/audit-selftest-discriminability.py tools/<one-tool>.py'. Never bare. Also the gap figures quoted in your brief are VOID (they came from a self-contaminating run); measure them yourself and report what you measure. Fix lands in PR #1175. | `/credit-offload` |
| 2026-07-25T21:04:49Z | worker1 | claude | wake | none | URGENT re selftest-gaps orders: tools/audit-selftest-discriminability.py at pinned SHA dd28405d RECURSES INTO ITSELF if run with no arguments, spawning runaway processes. Run it ONLY as 'python3 tools/audit-selftest-discriminability.py tools/<one-tool>.py'. Never bare. Also the gap figures quoted in your brief are VOID (they came from a self-contaminating run); measure them yourself and report what you measure. Fix lands in PR #1175. | `/credit-offload` |
| 2026-07-26T00:26:26Z | worker | claude | wake | none | validate-pr-1178 needs an opus claimant; 78ff is excluded as the Sweep 122 author | `/credit-offload` |
| 2026-07-26T00:48:30Z | codex | codex | wake | none | overnight nudge cadence, round 5 | `If you are currently working on an order, ignore this message and carry on. If you are not, then at your next opportunity resync your grc_library_scratch clone ` |
| 2026-07-26T00:54:02Z | worker1 | claude | wake | none | validate-pr-1179 is blocking prio-0 and unclaimed while opus capacity is idle | `/credit-offload` |
| 2026-07-26T00:54:04Z | worker | claude | wake | none | validate-pr-1179 is blocking prio-0 and unclaimed while opus capacity is idle | `/credit-offload` |
| 2026-07-26T00:54:56Z | worker | claude | wake | none | overnight nudge cadence, round 1 | `/credit-offload` |
| 2026-07-26T00:54:57Z | worker1 | claude | wake | none | overnight nudge cadence, round 1 | `/credit-offload` |
| 2026-07-26T00:58:36Z | codex | codex | wake | none | overnight nudge cadence, round 2 | `If you are currently working on an order, ignore this message and carry on. If you are not, then at your next opportunity resync your grc_library_scratch clone ` |
| 2026-07-26T00:58:47Z | worker | claude | wake | none | overnight nudge cadence, round 2 | `/credit-offload` |
| 2026-07-26T00:58:48Z | worker1 | claude | wake | none | overnight nudge cadence, round 2 | `/credit-offload` |
