<!-- PENDING-DECISIONS-EMPTY -->
# Pending Decisions

**Status:** empty

No decisions are pending. This file is the durable queue for the **attended-autonomous
operating mode** (see the `## Attended-autonomous operating mode` section in
[`.claude/CLAUDE.md`](../.claude/CLAUDE.md)): when the assistant surfaces a decision that is
genuinely the maintainer's and no answer arrives within the short timeout window (default
about 2 minutes), it records the decision here and continues, rather than stalling.

Each entry, while the queue is non-empty, carries:

- **Question**: the decision, in one sentence.
- **Options**: the named alternatives that were surfaced (with the recommended one marked).
- **Originating task**: the PR or task the decision arose in.
- **Interim action**: either `proceeded: <X> (stricter-safe default)` with its evidence, OR
  `deferred-blocked: no safe default` (the task was skipped and routed around, not guessed).
- **Status**: `pending` or `resolved`.

On `/resume`, the assistant reads this file first, surfaces the still-`pending` entries to the
maintainer (confirming each "proceeded" stricter-safe default for redirect, and asking each
"deferred-blocked" question), resolves those tasks, and only then continues to the next queued
items. A resolved entry is rotated out of the queue, the way a closed TODO item is.

This file is maintainer working state, exempt from corpus audit gates per the `.working/`
directory exemption. It is distinct from [`overnight-pr.md`](overnight-pr.md): that file is the
maintainer-asleep overnight-run lifecycle; this file is the reachable-but-not-watching attended
mode's decision queue, and normal per-PR logging (CHANGELOG, `/validate-pr`, `/retro`, handoff)
applies throughout.
