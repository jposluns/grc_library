# Overnight PR

**Status:** in-flight

This file is the durable handoff record for a maintainer-authorized autonomous overnight
session. It is `stub` when no overnight session is in flight (the default state).

Lifecycle (audit gate 46 enforces it: passes on `stub` and `in-flight`, fails on `done`):

- `stub`: no overnight session in flight. This file holds only this protocol description, the `Status: stub` line, and (after a routed run) a short closure note recording where the last run's content went.
- `in-flight`: an overnight session is active. The assistant fills the file with the authorization scope, design decisions made, files being authored or modified, build progress, and open ambiguities. Each overnight PR ships `in-flight`.
- `done`: the session ended. The next-morning processing PR routes the content to the durable ledgers (design decisions to [`design-decisions.md`](design-decisions.md), closed work to [`DONE.md`](DONE.md), queued follow-ups to [`../TODO.md`](../TODO.md)) and resets this file to `stub`.

## Current run: 2026-07-06 overnight (resume session `claude/resume-tl5rez`)

**Authorization scope.** The maintainer switched the session to overnight mode by direct
message ("I am going to sleep shortly. Change to overnight mode.") on 2026-07-06, immediately
after resolving the four TODO 3.21 residuals by chat: (a) normalize the compliance-matrix
C-TPAT cell to bare `C-TPAT`; (b) reword the five `tools/` PR-delta bare-"ensure" strings to
`ensure that`; (c) apply the verifier's round-3 wording to the master spec's line-214
monotonicity claim; (d) leave the three `PCI DSS v4` cloud-baseline family-label citations
(no change). Those four are corpus/tool changes outside the protected trees, so they are the
first overnight PR (#667). Overnight constraints in force: protected-file edits (`.claude/`,
`dev-security/claude-rules/`) are DEFERRED (staged, not applied, since the maintainer cannot
authorize a click/tap while asleep); green `Lint markdown corpus` CI is merge authority;
conflicts and authorial decisions defer to the morning rather than being guessed; full per-PR
`/validate-pr` + `/retro` (never abbreviated); 60-second background-task cadence.

**Files modified this run (PR #667, TODO 3.21 close).**
- `compliance/matrix-grc-compliance-alignment.md` (Version 1.11.11 -> 1.11.12): C-TPAT
  framework-key cell normalized to bare `C-TPAT`.
- `specification-master-project.md` (Version 1.6.6 -> 1.6.7): line-214 monotonicity reword.
- `tools/check-changelog-dash-on-pr.py`, `tools/check-changelog-on-pr.py`,
  `tools/check-date-cobump-on-pr.py`, `tools/check-todo-rotation-on-pr.py`,
  `tools/check-version-bump-on-pr.py`: bare "ensure" -> `ensure that` (one string each).
- `taxonomy.yml`, `docs/portal.md`, `docs/maturity-scorecard.md`: regenerated from the two
  metadata bumps.
- `TODO.md`: section 3.21 deleted (closed); `.working/DONE.md`: #667 entry added.
- Carries the batched #666 `/validate-pr` (0 findings) + `/retro` rows (interim commit
  `b37d610`).

**Design decisions made this run.**
- 3.21(a): applied the maintainer's explicit A1 (bare `C-TPAT`) as chosen. Observation for
  the maintainer (non-blocking, not acted on): the matrix framework-key column's sibling
  cells carry fuller programme names (e.g. "Partners in Protection (Canada Border Services
  Agency)"), so bare `C-TPAT` is slightly less consistent with the column than a full
  "Customs-Trade Partnership Against Terrorism" expansion would be; the maintainer's informed
  choice was bare `C-TPAT` (it removes the document-title-quote, which was the actual 3.21(a)
  defect). A future full-name-consistency pass over that column is a possible new item, not
  raised as one absent a signal.
- 3.21(c): before shipping the approved wording, re-verified the asserted gate identities
  against the linter docstrings: gate 13 = library/document version-monotonicity (skips
  `CHANGELOG.md`, non-decrease, an unchanged value passes); gate 29 invariant 2 couples the
  README Library Version to the latest CHANGELOG heading; gate 59's GR-1 extension asserts
  CHANGELOG Library-Version strict ordering. The wording is factually correct, not merely
  trusted.

**Deferred to the daytime protected-backlog queue (drafted this run for a quick apply).**
- The `/claim-fit` cadence-section clause for `.claude/CLAUDE.md` (the last TODO 3.15 r5
  close-out item), drafted into [`deferred-protected-changes.md`](deferred-protected-changes.md)
  so the daytime apply is content-ready and only the authorized apply plus per-PR QA remain.

**Forward queue for the rest of this overnight run (non-protected).** Coverage-refresh scratch
sync (brief-freshness index behind + dead anchors; scratch PR); scratch `originals/README.md`
refresh; then non-protected P3/P2 items as the queue allows. All protected-file items stay
deferred.

**Subsequent PRs this run (after #667).**
- **PR #668** (TODO 3.21(d) follow-through): normalized the three cloud-hardening baseline
  `PCI DSS v4` cells to `v4.0.1` after the maintainer's mid-flight clarification (full latest
  version unless quoting another document); recorded the standing preference in
  `design-decisions.md`. Library 2026.07.156, README 1.9.517.
- **PR #669** (TODO 1.9 root-cause record): read-only investigation pinned why the
  PreToolUse pipe-guard hook does not fire in resumed/child sessions (`CLAUDE_PROJECT_DIR`
  is unset, so the `settings.json` hook command interpolates to a nonexistent path);
  established no portable corpus-side fix exists (harness-level). Disposition deferred to the
  maintainer (`pending-decisions.md`); 1.9 stays OPEN. Library 2026.07.157, README 1.9.518.
- **PR #670** (TODO 3.15 #637 F4/F6, acronym-linter digit-initial blind spot): widened gate
  20's `GLOSSARY_ROW_RE` and `INLINE_DEF_RE` to `[A-Z0-9]`-initial (numeronym rows such as
  `3PL` are now parsed/matched) with three fixtures; the paired lowercase-tolerant inline
  pattern was assessed corpus-wide and REJECTED with evidence (over-capture false positives),
  the Title-Case requirement documented as a deliberate FP control. Surfaced for maintainer
  confirmation. Carries the batched #669 QA rows.
- **PR #671** (TODO 3.15 r4 G-7, QA-report intake runbook subsection): codified the
  three-layer QA-report intake channel (worker report as hypotheses, independent validation
  subagent, transcription-fidelity verifier) as `multi-session-orchestration.md` §5.2, with
  the maintainer's standing revisit note. `.working/`-only, protected-free. Carries the
  batched #670 QA rows.

**DAYTIME-DEFERRED this run (protected-entangled, investigated not shipped).** TODO 3.15
#637 F3 (D5 eighth closure-form + form-6 link widening): the full-history FP census was run
and BOTH widenings validated false-positive-free (patterns recorded in the TODO F3 bullet),
but the build is deferred to the daytime protected-backlog clearance because the closure-form
COUNT is restated in the protected `.claude/CLAUDE.md` ("detects SEVEN closure forms"), which
must co-update to EIGHT in the same PR (multi-surface completeness). Overnight mode cannot
apply a protected edit, and shipping the linter/spec/tests while the CLAUDE.md count stayed
"seven" would strand a cross-surface inconsistency. Note for the mode exit: a class of P3
tooling items that touch a gate/form count restated in `.claude/CLAUDE.md` is overnight-blocked
this way and belongs in the daytime protected-backlog clearance.

**PDF assessment (maintainer-attached, 2026-07-06).** Two LinkedIn-sourced PDFs were assessed
for the scratch `publications/` bucket. Outcome: NET NO INGEST. (1) The Anthropic "Zero Trust
for AI Agents" ebook is ALREADY ingested (scratch `ref/publications/` catalogue row + full-text
extract present), so the upload is a content-duplicate and was discarded. (2) The RAND-style
tabletop-exercise insights PDF was discarded as low org-GRC-reference value. No scratch PR
resulted. Recorded here per the maintainer's request to note the assessment outcome.

**MORNING DELIVERABLE (owed to the maintainer).** A written recommendation on the maintainer's
time-decay suggestion (publications, and ONLY publications, devalued as time passes; NOT
standards, NOT frameworks; framed as a suggestion to assess, not a directive). To be delivered
in the morning.

**Open ambiguities / morning items.** The three still-parked items from the prior attended
round are unaffected: none. The `/claim-fit` clause needs the maintainer's authorization (a
protected touch); it is staged, not applied. TODO 1.9 disposition is a maintainer decision
(close-as-harness-limitation vs track-harness-feedback), in `pending-decisions.md`. The PR
#670 lowercase-tolerant-pattern rejection is surfaced for the maintainer to confirm or
reopen.
