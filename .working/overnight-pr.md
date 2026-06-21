# Overnight PR

**Status:** stub

<!-- OVERNIGHT-PR-STUB -->

No overnight session is currently in flight. This file is the stub form per the overnight-work protocol documented in [`dev-security/claude-rules/governance/change-tracking.md`](../dev-security/claude-rules/governance/change-tracking.md).

## Protocol summary

When the maintainer authorizes an overnight session (assistant works autonomously while the maintainer is asleep or otherwise unavailable):

1. The assistant updates this file's `Status` field from `stub` to `in-flight` in the first overnight PR.
2. The assistant fills the file with the standard overnight-PR sections: authorization scope, design decisions made, files being authored / modified, files NOT touched, build progress, open ambiguities surfaced.
3. Each overnight PR ships with `Status: in-flight`. The gate [`tools/lint-overnight-file.py`](../tools/lint-overnight-file.py) accepts `in-flight` as a valid state.
4. At the end of the overnight session, the assistant updates `Status` to `done` to signal that the morning-processing PR is required.
5. The next morning's first PR processes the file's content: routes design decisions to [`design-decisions.md`](design-decisions.md), closed work to [`DONE.md`](DONE.md), queued follow-ups to [`../TODO.md`](../TODO.md); resets this file to the stub form.
6. The gate accepts only `stub` and `in-flight` as valid `Status` values. `done` causes a gate failure, reminding the maintainer that the morning processing is overdue.

## Permitted values for `Status`

- `stub` — no overnight session is in flight. This is the default state and the post-processing state.
- `in-flight` — overnight session is active. The assistant is currently filling or maintaining the file.
- `done` — overnight session has ended; the next-morning processing PR must route content and reset this file to `stub`. The audit gate fails on this value.

Any other `Status` value triggers a gate failure.
