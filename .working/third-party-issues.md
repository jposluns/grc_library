# Third-Party and Infrastructure Issues

**Version:** 1.0.0\
**Date:** 2026-06-22\
**License:** CC BY-SA 4.0

A running log of third-party service and execution-environment issues encountered during maintenance of this library: outages, flakes, and misconfigurations in infrastructure the project depends on but does not own (the commit-signing service, the remote execution sandbox, CI runners, external citation sources, MCP servers). The purpose is to distinguish environment artifacts from genuine corpus or tooling defects, so a future session does not mistake an infrastructure flake for a regression and chase a non-existent bug.

This file is maintainer working state, exempt from corpus audit gates per the `.working/` directory exemption. Entries are reverse-chronological (newest first). Each entry records: what was observed, the diagnosis, the impact, how it was distinguished from a real defect, and the resolution.

## Entries

### 2026-06-22: Commit-signing server 503 outage

**Observed.** During the trust-recovery routing-convention revision (PR #252), the commit-signing server returned HTTP 503 (`signing operation failed: signing server returned status 503`). Two distinct symptoms:

1. **Gate 36 (linter regression suite) went red.** Two tests in the `VersionBumpRecencyTests` class (`test_stale_version_after_body_change_flagged` and a sibling) failed with `subprocess.CalledProcessError ... git commit ... non-zero exit status 128`. Those tests create a temporary git repository and `git commit` into it to build their fixtures; the commit-signing hook intercepts the commit, calls the signing server, and the 503 made the commit fail hard, so the test harness could not build its git fixtures.
2. **A real commit was left unsigned.** The routing-revision commit was created but GitHub-unverified (the stop-hook flagged it: missing signature). A `git commit --amend --no-edit --reset-author` attempted while the server was still down produced a commit with `No signature`.

**Diagnosis.** A transient outage of the execution environment's commit-signing service, not a corpus or tooling defect. The outage lasted across roughly two re-run cycles, then cleared on its own.

**How it was distinguished from a real defect (the key discipline).** The failing gate-36 tests exercise gates 31 (document-date-staleness) and 40 (version-bump-recency); **those two linters passed on the real corpus in the same `run_all_audits.sh` run**, and the other 44 gates passed. The only failures were `git commit` subprocess errors carrying the literal `503` signing-server message. So the *linter logic* was sound; only the *test harness's ability to create git fixtures* was blocked. This is the same class of false positive as the shallow-clone gate-31/40 artifact recorded in the `deep-qa-review` skill's step-0 rule: an environment artifact that looks like a gate failure but is not a corpus defect. Per the gate-discipline rule, the failure was surfaced (not pushed through silently) and escalated to the maintainer rather than the gate being weakened.

**Impact.** Bounded. No corpus or tooling defect; the work was correct. The cost was: one escalation round to the maintainer, two regression re-runs, and a commit re-sign once the server recovered.

**Resolution.** The server recovered on its own; the regression suite then passed 116/116, the full audit returned 46/46, and the commit was re-signed (`git commit --amend --no-edit --reset-author`) so the branch tip was verified before push. The squash-merge produces a fresh GitHub-signed commit on `main` regardless of feature-branch commit signatures.

**Lesson for a future session.** If `run_all_audits.sh` shows gate 36 red while gates 31/40 pass standalone on the real corpus, and the regression failures are `git commit` subprocess errors mentioning the signing server, treat it as a signing-server outage (environment artifact), not a regression. Re-run after a pause; if it persists, surface to the maintainer rather than weakening the gate or pushing an unverified commit.
