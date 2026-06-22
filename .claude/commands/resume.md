Resume the previous session from the durable handoff record. This is the single command the maintainer sends to continue work in a fresh session.

Execute these steps in order:

1. **Read [`.working/session-handoff.md`](../../.working/session-handoff.md) in full.** It is the as-of-last-refresh snapshot of branch, versions, counts, last-merged PRs, trust-recovery state, the next-actions queue, open decisions awaiting the maintainer, and the standing disciplines.

2. **Read [`.claude/CLAUDE.md`](../CLAUDE.md)** (the PRIMORDIAL RULE and project disciplines) and the most recent few entries of [`CHANGELOG.md`](../../CHANGELOG.md) to ground the recent history.

3. **Verify state against live files, do not trust the snapshot blindly** (the snapshot drifts forward between refreshes): run `git rev-parse --is-shallow-repository` (if `true`, `git fetch --unshallow` before any history-aware audit); `git log --oneline -5` to confirm HEAD; `tools/run_all_audits.sh` to confirm the corpus is green; and check the library/pack/README versions in `README.md` and `dev-security/claude-rules/README.md` against the snapshot.

4. **Surface a one-screen orientation to the maintainer**: current verified state (branch, HEAD, versions, gate/rule/skill counts), what merged most recently, and the next 1-3 planned actions from the queue. Note any drift between the snapshot and live state.

5. **Run a full corpus-wide `/validate` as the first substantive task** — before resuming the queue. This is the compensating control for the session-closing handoff PR, which intentionally skips its trailing `/validate-pr` to avoid the post-merge validate-then-PR loop (a handoff PR's `/validate-pr` would produce ledger rows that need a new PR, whose merge would trigger another `/validate-pr`, with no terminating "next substantive PR" at a session boundary). The corpus-wide `/validate` is stronger than the skipped per-PR sweep would have been: it re-examines the whole corpus, not just the handoff PR's diff, so anything the prior session's closing PR(s) might have introduced is caught here. Record its findings per the `/validate` skill and route any to the backlog before continuing.

6. **Continue from "Next actions"** in the handoff file, honouring all standing disciplines (PRIMORDIAL RULE: Quality > Speed > Cost; post-commit audit before push; 60-second PR-activity fallback timer; formal per-PR `/validate-pr` + `/retro` for every non-handoff PR; the PR close-out checklist).

If the handoff file is missing or stale (its snapshot contradicts live state materially), say so explicitly and reconstruct state from `TODO.md`, the last several `CHANGELOG.md` entries, and `.working/` records before continuing.
