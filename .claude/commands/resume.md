Resume the previous session from the durable handoff record. This is the single command the maintainer sends to continue work in a fresh session.

Execute these steps in order:

1. **Read [`.working/session-handoff.md`](../../.working/session-handoff.md) in full.** It is the as-of-last-refresh snapshot of branch, versions, counts, last-merged PRs, trust-recovery state, the next-actions queue, open decisions awaiting the maintainer, and the standing disciplines.

2. **Read [`.claude/CLAUDE.md`](../CLAUDE.md)** (the PRIMORDIAL RULE and project disciplines) and the most recent few entries of [`CHANGELOG.md`](../../CHANGELOG.md) to ground the recent history.

3. **Verify state against live files, do not trust the snapshot blindly** (the snapshot drifts forward between refreshes): run `git rev-parse --is-shallow-repository` (if `true`, `git fetch --unshallow` before any history-aware audit); `git log --oneline -5` to confirm HEAD; `tools/run_all_audits.sh` to confirm the corpus is green; and check the library/pack/README versions in `README.md` and `dev-security/claude-rules/README.md` against the snapshot.

4. **Surface a one-screen orientation to the maintainer**: current verified state (branch, HEAD, versions, gate/rule/skill counts), what merged most recently, and the next 1-3 planned actions from the queue. Note any drift between the snapshot and live state.

5. **Continue from "Next actions"** in the handoff file, honouring all standing disciplines (PRIMORDIAL RULE: Quality > Speed > Cost; post-commit audit before push; 60-second PR-activity fallback timer; formal per-PR `/validate-pr` + `/retro`; the PR close-out checklist).

If the handoff file is missing or stale (its snapshot contradicts live state materially), say so explicitly and reconstruct state from `TODO.md`, the last several `CHANGELOG.md` entries, and `.working/` records before continuing.
