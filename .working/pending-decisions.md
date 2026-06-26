# Pending Decisions

**Status:** empty

This file is the durable queue for the **attended-autonomous operating mode** (see the
`## Attended-autonomous operating mode` section in [`.claude/CLAUDE.md`](../.claude/CLAUDE.md)):
when the assistant surfaces a decision that is genuinely the maintainer's and no answer
arrives (here, because the `AskUserQuestion` primitive errored repeatedly this session, a
transient permission-stream failure), it records the decision here and continues, rather
than stalling.

On `/resume`, the assistant reads this file first, surfaces the still-`pending` entries to
the maintainer, resolves those tasks, and only then continues to the next queued items.

## Entries

No pending decisions.

The 2026-06-26 §5.3 register-classification decision was resolved by the maintainer
(Option A: `register-coverage-gaps.md` stays corpus; `register-document-review-schedule.md`
migrates to `.project-governance/`) and **applied in PR #381** (the Phase-2 migration). It is
rotated out of this queue at the #382 handoff per the resolved-entry convention. The audit
trail lives in the separation spec §5.3/§5.4, the #381 CHANGELOG entry, and
[`DONE.md`](DONE.md).
- **Status**: resolved (Option A); review-schedule migration queued.
