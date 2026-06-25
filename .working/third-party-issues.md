# Third-Party and Infrastructure Issues

**Version:** 1.0.2\
**Date:** 2026-06-25\
**License:** CC BY-SA 4.0

A running log of third-party service and execution-environment issues encountered during maintenance of this library: outages, flakes, and misconfigurations in infrastructure the project depends on but does not own (the commit-signing service, the remote execution sandbox, CI runners, external citation sources, MCP servers). The purpose is to distinguish environment artifacts from genuine corpus or tooling defects, so a future session does not mistake an infrastructure flake for a regression and chase a non-existent bug.

This file is maintainer working state, exempt from corpus audit gates per the `.working/` directory exemption. Entries are reverse-chronological (newest first). Each entry records: what was observed, the diagnosis, the impact, how it was distinguished from a real defect, and the resolution.

## Entries

### 2026-06-25: git proxy rejects writes to `grc_library_scratch` after the first push (HTTP 403)

**Observed.** While seeding the multi-session exchange repo `grc_library_scratch`, the
local git proxy (`127.0.0.1:41729`) accepted the FIRST push (a tiny probe that created
`main` from empty) and then returned `HTTP 403 (curl 22)` on EVERY subsequent push to
that repo, including a clean, tiny, fast-forward text-only push. Reads worked
throughout (`git ls-remote` rc=0). Writes to `grc_library` via the same proxy worked
throughout (the overnight feature branch pushed fine, rc=0). Writes to
`grc_library_scratch` via the GitHub MCP API (`create_or_update_file`, `push_files`,
a different transport) ALSO worked.

**Diagnosis.** A write restriction specific to `grc_library_scratch` on the local git
proxy: either a very low per-repo write quota (one push, then blocked) or a throttle
from the burst of push attempts that did not clear within the session. NOT an egress
policy denial (the egress proxy at port 34359 reports `recentRelayFailures: []`; the
git proxy at 41729 is a separate component, bypassed by the `127.0.0.0/8` no-proxy
rule). NOT a fast-forward problem (a clean ff push to unchanged `main` still 403'd).
NOT a credential/corpus problem (`grc_library` writes and scratch reads both work).
The earlier hypothesis of a payload SIZE cap was not confirmable: once the burst
tripped the restriction, even a few-KB text push 403'd, so size could not be isolated.

**How it was distinguished from a real defect.** Three transports cross-checked:
git-proxy→`grc_library` (works), git-proxy→`grc_library_scratch` (1 then 403),
MCP→`grc_library_scratch` (works). Only the git-proxy→scratch path is affected, so the
overnight PR workflow (all on `grc_library` via git) is unaffected.

**Impact.** Bounded. The scratch `ref/` text indexes (root `README.md`, the calibrated
`ref/README.md`, `.gitignore`) WERE seeded via the MCP API. The reference BINARIES
(CSA CCM v4.1 / AICM v1.1 / CAIQ catalogues + guidance PDFs, NIST CSF 2.0 PDF, the
AI-security and threat-intel PDFs, ~34 MB) could NOT be pushed: the git-proxy→scratch
path is blocked, and binary content is not safely expressible through the MCP
string-content interface (double-base64 corruption risk). The maintainer chose to
re-upload the binaries tomorrow rather than block the overnight run.

**Resolution / handoff.** Binary seed DEFERRED. The full categorized `ref/` tree is
built and committed locally on the scratch-seed working repo (in the session
scratchpad), ready to push the moment the git-proxy scratch-write restriction clears.
The `ref/README.md` already documents the intended location of every file, so a
re-upload drops cleanly into place. Next session / tomorrow: retry a single paced git
push to scratch; if it still 403s, surface to the maintainer that the git-proxy
scratch-write path needs an infrastructure fix (the repo may need a write-quota raise).

**Lesson for a future session.** To seed `grc_library_scratch`: use the GitHub MCP API
for TEXT files (reliable), and a SINGLE paced git push for binaries (do not burst
multiple pushes; the burst appears to trip the restriction). If the git-proxy
scratch-write path 403s on a clean small push, treat it as the environment restriction
recorded here, not a corpus/credential defect, and fall back to maintainer re-upload.

### 2026-06-24: GitHub MCP server disconnected mid-session

**Observed.** During the autonomous overnight session, after PR #304 merged cleanly, the GitHub MCP server disconnected: the harness reported "86 deferred tools are no longer available (MCP server disconnected): mcp__github__* (55)" (plus the Atlassian set), and instructed not to search for them. All `mcp__github__*` tools (create/merge PR, pull_request_read, subscribe_pr_activity) became unavailable.

**Diagnosis.** A transient disconnection of the execution environment's GitHub MCP integration, not a corpus or tooling defect. `git push` over HTTPS continued to work (it does not depend on the MCP server); only the GitHub-API operations routed through MCP were affected.

**Impact.** Bounded but blocking for the PR lifecycle: PR #305 (the loop-break-generalize pack-layer change) was fully authored, audited green (48/48 + PR-time checks), committed, and pushed to the feature branch, but could NOT be opened or merged via MCP. The session could not complete the green-merge-as-last-act discipline for #305 through the normal MCP flow.

**How it was distinguished from a real defect.** The corpus is green (`run_all_audits.sh` 48/48 on the committed state); the failure is purely the absence of the MCP toolset, reported by the harness, not a gate failure or a git error. `git push` succeeded, confirming the repository and credentials are intact.

**Resolution / handoff.** #301-#304 merged cleanly before the disconnect. #305 is committed and pushed to `claude/aicm-ccm-resume-3jd277`, pending a PR-open + merge once the GitHub MCP reconnects (or the next session, which can open/merge it). The session-handoff records #305 as pushed-but-unmerged so the next `/resume` opens and merges it (and then runs the corpus-wide Sweep 37 loop-break control as usual).

**Lesson for a future session.** If `mcp__github__*` tools vanish mid-session, treat it as an environment disconnection (not a corpus problem): keep committing and pushing via `git` so no work is lost, record the pending-merge state in the handoff, and resume the PR lifecycle when MCP returns. Do not attempt to merge by any non-MCP path (no direct push to `main`).

### 2026-06-22: Commit-signing server 503 outage

**Observed.** During the trust-recovery routing-convention revision (PR #252), the commit-signing server returned HTTP 503 (`signing operation failed: signing server returned status 503`). Two distinct symptoms:

1. **Gate 36 (linter regression suite) went red.** Two tests in the `VersionBumpRecencyTests` class (`test_stale_version_after_body_change_flagged` and a sibling) failed with `subprocess.CalledProcessError ... git commit ... non-zero exit status 128`. Those tests create a temporary git repository and `git commit` into it to build their fixtures; the commit-signing hook intercepts the commit, calls the signing server, and the 503 made the commit fail hard, so the test harness could not build its git fixtures.
2. **A real commit was left unsigned.** The routing-revision commit was created but GitHub-unverified (the stop-hook flagged it: missing signature). A `git commit --amend --no-edit --reset-author` attempted while the server was still down produced a commit with `No signature`.

**Diagnosis.** A transient outage of the execution environment's commit-signing service, not a corpus or tooling defect. The outage lasted across roughly two re-run cycles, then cleared on its own.

**How it was distinguished from a real defect (the key discipline).** The failing gate-36 tests exercise gates 31 (document-date-staleness) and 40 (version-bump-recency); **those two linters passed on the real corpus in the same `run_all_audits.sh` run**, and the other 44 gates passed. The only failures were `git commit` subprocess errors carrying the literal `503` signing-server message. So the *linter logic* was sound; only the *test harness's ability to create git fixtures* was blocked. This is the same class of false positive as the shallow-clone gate-31/40 artifact recorded in the `deep-qa-review` skill's step-0 rule: an environment artifact that looks like a gate failure but is not a corpus defect. Per the gate-discipline rule, the failure was surfaced (not pushed through silently) and escalated to the maintainer rather than the gate being weakened.

**Impact.** Bounded. No corpus or tooling defect; the work was correct. The cost was: one escalation round to the maintainer, two regression re-runs, and a commit re-sign once the server recovered.

**Resolution.** The server recovered on its own; the regression suite then passed 116/116, the full audit returned 46/46, and the commit was re-signed (`git commit --amend --no-edit --reset-author`) so the branch tip was verified before push. The squash-merge produces a fresh GitHub-signed commit on `main` regardless of feature-branch commit signatures.

**Lesson for a future session.** If `run_all_audits.sh` shows gate 36 red while gates 31/40 pass standalone on the real corpus, and the regression failures are `git commit` subprocess errors mentioning the signing server, treat it as a signing-server outage (environment artifact), not a regression. Re-run after a pause; if it persists, surface to the maintainer rather than weakening the gate or pushing an unverified commit.
