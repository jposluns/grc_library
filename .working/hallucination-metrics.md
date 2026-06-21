# Worker Hallucination Metrics

Tracks the rate at which research-assistant (worker subagent) drafts contain claims that the orchestrator catches and corrects at apply-time, versus the rate at which those errors slip past apply-time and ship to `main`.

This file is **maintainer working state**. It is not a versioned corpus document; it is not subject to corpus audit gates; it is exempt under the `.working/` directory exemption. The file is updated opportunistically as the orchestrator catches and ships work; precision matters less than the trend signal.

The metric is the operational counterpart to the **research-assistant discipline** in [`dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md`](../dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md). The discipline says "verify worker claims at apply-time"; the metric says "how often does the discipline catch something". A rising metric suggests the worker prompt needs tightening; a falling metric suggests the discipline is converging on a robust worker model.

---

## Definitions

- **Worker draft**: a research file produced by a background subagent. Used as input by the orchestrator; not pasted unmodified.
- **Apply-time catch**: the orchestrator identifies a worker error during apply-time verification (re-reading target files, running contradiction searches) and corrects it before the PR is committed.
- **Shipped escape**: an error that survived apply-time verification and was caught only after the PR merged (by `/validate`, by CI on `main`, by a subsequent reader, or by the maintainer).

The ratio `shipped escapes / total worker errors` is the discipline's leak rate. The discipline aims to keep apply-time catch rate high and shipped escape rate low.

---

## Current state (as of PR #176, 2026-06-21)

| Metric | Count | Notes |
| --- | --- | --- |
| Worker-driven PRs shipped under the research-assistant discipline | ~30 | Discipline introduced mid-session; precise count includes all Phase 1 bundles plus the meta-PRs that used research drafts. |
| Apply-time catches | ~5 | Stale version numbers, file-path confabulations, PR / FR cross-references, ISO/IEC publication years. |
| Shipped escapes (caught post-merge) | 2 | P1.3 worker drafted a non-existent file path (caught pre-apply by orchestrator's `find`, so technically apply-time, but borderline); Sweep 15 worker cited `ISO/IEC 29134:2023` which is unverified (caught by `/validate` Sweep 15, fixed in PR #167). |
| Apply-time catch rate (catches / (catches + escapes)) | ~5 / ~7 = 71% | Sample size is small; trend signal more than calibrated rate. |
| Shipped escape rate (escapes / worker-driven PRs) | ~2 / ~30 = 7% | Each escape was low-impact (single citation year, single file path) and was caught within the next sweep or fitness pass. |

The two shipped escapes were both caught within one cycle of the validation programme. No worker error has shipped that was not caught at the next regression interval.

---

## Update protocol

When the orchestrator catches a worker error at apply-time:

1. Increment the apply-time-catches count in the table above.
2. Add a one-line note to the **catches log** below, dated and PR-keyed.
3. The catch is also documented in the closing PR's CHANGELOG-detailed entry under a "Discipline observation" or equivalent section (per the research-assistant discipline's tracking convention).

When a worker error is discovered post-merge (a shipped escape):

1. Increment the shipped-escapes count in the table above.
2. Add a one-line note to the **escapes log** below.
3. The fix is shipped in the next regression PR (a `/validate` close-out, a `/fitness` close-out, or a dedicated correction PR). That PR's CHANGELOG entry notes the escape.

The metrics table itself is updated **opportunistically**, not on every PR. A periodic refresh (every 5-10 PRs, or at session-pause) is sufficient. The precision matters less than the trend direction.

---

## Catches log

Reverse-chronological. Each entry: date, PR number where the catch occurred, one-line description.

- **2026-06-21, PR #179, CI catch (gate 31)**: orchestrator bumped per-doc Version on six touched files but missed bumping Date on two of them (`security/policy-information-security.md` Date 2026-05-27, lag 25 days; `resilience/template-tabletop-exercise.md` Date 2026-06-02, lag 19 days). Gate 31 (document-date-staleness) caught this in CI; fixed in a follow-up commit on the same branch (Date bumped to 2026-06-21; per-doc Version bumped again per the version-bump-recency rule). **Discipline gap exposed**: the apply-time checklist needs an explicit "did I bump Date on every file whose body changed?" item alongside the Version bump check. Not a worker error; an orchestrator oversight that CI caught (not a shipped escape, but a near-escape worth recording).
- **2026-06-21, PR #179**: worker drafted library bump as `2026.06.151 → 2026.06.152`; actual state was library `2026.06.157` pre-this-PR. Corrected at apply-time to `2026.06.157 → 2026.06.158`.
- **2026-06-21, PR #179**: worker drafted READme bump as `1.9.22 → 1.9.23`; actual state was `1.9.28` pre-this-PR. Corrected at apply-time to `1.9.28 → 1.9.29`.
- **2026-06-21, PR #179**: worker bundled FR-33 (high[critical]) into a velocity batch alongside six mediums; orchestrator split FR-33 out per "always split when in doubt" (different severity tier; substantively larger scope). Not a hallucination per se but a discipline-judgement catch.
- **2026-06-21, PR #178**: worker drafted library bump as `2026.06.150 → 2026.06.151`; actual state was library `2026.06.156` pre-this-PR. Corrected at apply-time to `2026.06.156 → 2026.06.157`.
- **2026-06-21, PR #178**: worker drafted backlog math as `85 → 83`; actual pre-state was 77 open. Corrected at apply-time to `77 → 75`.
- **2026-06-21, PR #178**: worker drafted target PR number as `#169`; actual is #178. Corrected at apply-time. (Common pattern: workers often anchor to the most recent PR they saw, which drifts over multi-PR sessions.)
- **2026-06-21, PR #172**: worker drafted FR-3 as closed in PR #158; actual closing PR is #147. Corrected at apply-time after cross-checking [`.working/DONE.md`](DONE.md).
- **2026-06-21, PR #172**: worker drafted against library `2026.06.150` / README `1.9.21`; current state was `2026.06.152` / `1.9.23` (advanced via PRs #170 / #171). Corrected at apply-time.
- **2026-06-21, P1.3 (PR #169)**: worker referenced `policy-information-security-incident-management.md` which does not exist in the corpus. Caught pre-apply by `find`; substituted with the correct `procedure-security-incident-response.md`.

(Earlier catches not retroactively logged; the discipline started recording at the moment this file was created.)

---

## Escapes log

Reverse-chronological. Each entry: date, original PR, catching mechanism, one-line description.

- **2026-06-21, original PR #162 (FR-29 DPIA template), caught by `/validate` Sweep 15**: worker drafted `ISO/IEC 29134:2023`; the publicly verifiable edition is 2017 with no recorded 2023 republication. Corrected in PR #167 (Sweep 15 close-out).
- **2026-06-21, original PR #169 (P1.3 access-control), borderline apply-time**: worker referenced a non-existent file path. Caught by orchestrator's `find` during apply-time verification, before the file was committed. Counted as apply-time catch in the metrics table; logged here in the escapes register because the worker's draft did contain the error (the discipline caught it at the boundary).

---

## Discipline observations

- **Apply-time `find` for file-path verification** is one of the cheapest worker-error catches. Worker confabulations of plausible-sounding-but-nonexistent filenames are common; a single `find` rules them out in milliseconds.
- **Cross-PR / FR references** are a recurring failure pattern. Workers drafting from session memory rather than from the live closed-PR ledger get these wrong. The orchestrator's verification step is to grep [`DONE.md`](DONE.md) for the referenced PR or FR.
- **Stale version numbers** are mechanical and almost universal in workers drafted before the current PR sequence. Apply-time correction is a quick read of [`README.md`](../README.md)'s Library Version + the target file's Version field.
- **External-standard citation years** are higher-cost catches because they require WebFetch or external verification. The canonical-citations register ([`governance/register-canonical-citations.md`](../governance/register-canonical-citations.md)) is the project's defence; the metric here is the gap between the register and what workers draft.

---

## Future signals to watch

- **Apply-time catch rate trending down** could mean the worker prompt has improved (less hallucination at source) OR that the orchestrator is becoming less vigilant (more escapes downstream). Compare with the shipped-escapes count.
- **Shipped escape rate trending up** is a clear discipline-failure signal. Investigate which class of error is leaking (the catches log surfaces patterns).
- **Specific error class clusters** (e.g., several consecutive citation-year escapes) suggest a structural worker-prompt fix is needed.

The metric is a maintenance signal, not a production gate. Use it to calibrate the discipline; do not use it as a CI requirement.
