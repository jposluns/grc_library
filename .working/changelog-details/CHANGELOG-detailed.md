# Changelog (Detailed Mirror)

All notable changes to this repository are recorded in this file with full structured-section detail. The adopter-facing root [`CHANGELOG.md`](../../CHANGELOG.md) carries only a compact one-line entry per change (a `date | version | PR` header plus a short, plain-language summary a general reader can follow); this file is the maintainer-grade audit trail carrying the full detail behind each of those summaries.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely; individual document versions follow semantic versioning as defined in [`specification-ingestion.md`](../../specification-ingestion.md). The library as a whole carries a Calendar Versioning (CalVer) version of the form `YYYY.MM.patch`; see [`specification-master-project.md`](../../specification-master-project.md) section 4.5.

The dual-entry convention was introduced in PR #125 (2026-06-21). Historical entries before that date follow the original single-file convention (the root entry was complete; this mirror preserves that pre-split state verbatim from the moment of the split).

**Worker-provenance convention (decided 2026-07-23, TODO 3.19):** a reference to a scratch-side worker result or manifest is written as plain backticked text in a `repo:path` form (naming the scratch repo and the result file), never a cross-repo markdown link. A cross-repo relative link target resolves only against a fresh sibling checkout at `main`, not a stale local tree, and cross-repo links are un-gate-checkable; the plain-text form keeps the provenance readable and grep-able without the fragility.

## 2026-07-27, Library Version 2026.07.685, PR #1195 (post-wind-down resume close-out)

The first-PR close-out of the 2026-07-26 post-emergency-wind-down resume. Batches the Sweep 124
close-out, #1194's QA rows, one backlog re-scope, a new Priority-1 series, and two maintainer-directed
codifications.

### Added

- **TODO Priority-1 series 1.26** (goal-description umbrella + phases 1.26.1 to 1.26.4): consolidate,
  harmonize, and distribute the quality machinery across AI toolchains (deduplicate/simplify the
  machinery; integrate the community's CC BY-SA ShareAlike contributions from team members and adopters
  on local/custom models; reach true public-pack parity; distribute aligned packs, Codex first, then a
  generic tool-agnostic form). ON HOLD pending all Priority-3 tooling. Placed at the top of P1; P1
  counter advanced to 1.27.

### Changed

- **[`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) `## Communication conventions`:** the no-diff rule is
  strengthened to a mechanical command-level ban (maintainer-directed 2026-07-26, after repeated
  violations): never run a command whose output is a +/- unified diff (`git diff` / `git show <commit>`
  without `--stat`/`--name-only`); inspect changes with `--stat`/`--name-only`, `git status --short`,
  `grep`/`wc`, or a targeted read.
- **[`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) `## Mandatory worker offload`:** the worker-first
  doctrine (maintainer-directed 2026-07-26): if a worker CAN do it, a worker DOES it (no self-run);
  spawn on demand with [`tools/exec-dispatch.py`](../../tools/exec-dispatch.py) and never gate offload
  on a `list-workers` count of zero; 20-minute reissue to another account; super-sensitive tasks go to
  BOTH a Codex and a Claude worker; keep the fleet busy (one on QA, the rest pre-loading the next items);
  and a privacy note that worker ids in the public repo are anonymized aliases only.
- **[`TODO.md`](../../TODO.md) section 3.128** re-scoped to the per-worker-display residual with a STATUS
  line marking W1/W2 FIXED in #1189 (Sweep 124 W1; the item's prose had contradicted the shipped code).

### Also (batched close-out bookkeeping)

- Sweep 124 recorded in [`validate-sweeps/history.md`](../validate-sweeps/history.md) (0 error / 1
  warning / 1 note; the #1185 to #1194 window ships clean; all asserted-clean claims corroborated, zero
  contradicted) and the handoff Resume cursor advanced to Sweep 124.
- #1194's QA rows batched: the merge-bypass row, the validate-pr-1194 row (subsumed by Sweep 124), the
  retro-1194 row, and the two Sweep 124 findings recorded and dispositioned in
  [`open-findings.md`](../open-findings.md).
- Handoff Current-truth snapshot version tokens reconciled to the #1195 head; the keep-current-plus-one
  block prune is deferred to the session-closing handoff.

### Verification

- `tools/run_all_audits.sh`: all 78 gates pass (standalone).
- Pre-push guard (both runners) green before push.

## 2026-07-26, Library Version 2026.07.684, PR #1194 (#1193 close-out completion)

### Changed

- [`governance/specification-audit-programme.md`](../../governance/specification-audit-programme.md)
  section 6, the D7 narrative: the enumerated surface list is synced to the surfaces D7 actually tracks
  after #1193 changed them. It named "the runbook, and the guardrail-review, validate-pr,
  improvement-log, and claim-fit history registers", but #1193 removed the first three from D7's
  `SURFACES` and "the runbook" was never a D7 surface, so the sentence now names only the library
  CalVer and README Version, the pack README Version, this specification's Version, and the claim-fit
  history register. Version bumped 1.17.31 to 1.17.32. (validate-pr-1193 W1, plus the pre-existing N1
  "runbook" mis-name, both fixed here.)

### Removed

- TODO section 3.135 is deleted from [`TODO.md`](../../TODO.md) (it was fully closed by #1193) and a
  matching entry added to [`.working/DONE.md`](../DONE.md), completing the TODO-to-DONE rotation #1193
  dropped. (validate-pr-1193 W2.)

### Also (the #1193 close-out bookkeeping this PR batches in)

- [`.working/merge-bypass-log.md`](../merge-bypass-log.md): the #1193 `--admin` bypass row (gate 50
  Check 6), written from the observed pre-merge `gh pr checks 1193` state.
- [`.working/validate-pr/history.md`](../validate-pr/history.md) plus the record file
  [`2026-07-26-PR-1193.md`](../validate-pr/2026-07-26-PR-1193.md): the validate-pr-1193 row and detail
  (0 error / 2 warning / 1 note; both warnings fixed in this PR).
- [`.working/improvement-log.md`](../improvement-log.md): the retro-1193 row.
- [`.working/open-findings.md`](../open-findings.md): both warnings recorded and dispositioned FIXED
  in this PR.
- [`.working/session-state.md`](../session-state.md): this session's concurrency lease acquired.

### Context

#1193 merged during the maintainer-directed emergency wind-down of the prior session, so its close-out
was truncated; the post-merge validate-pr-1193 (run at this resume) surfaced the two dropped
paired-surface steps, both hot-fixed here. Both the pre-merge skeptical verifier and validate-pr-1193
confirmed the #1193 change itself is CLEAN (exemptions exact in D2/D4, D7 removals correct, no orphaned
reader, version bump correct).

### Verification

- `tools/run_all_audits.sh`: all 78 gates pass (standalone).
- Generated artefacts ([`taxonomy.yml`](../../taxonomy.yml), [`docs/portal.md`](../../docs/portal.md),
  [`docs/maturity-scorecard.md`](../../docs/maturity-scorecard.md)) regenerated after the spec Version
  bump and confirmed in sync (`--check`).
- Pre-push guard (both runners) green before push.

## 2026-07-26, Library Version 2026.07.683, PR #1193 (drop Version+Date from append-only .working logs, TODO 3.135)

### Changed

- Drops the `Version` and `Date` metadata lines from the five append-only `.working` history logs
  ([`.working/validate-pr/history.md`](../validate-pr/history.md),
  [`.working/improvement-log.md`](../improvement-log.md),
  [`.working/merge-bypass-log.md`](../merge-bypass-log.md),
  [`.working/guardrail-reviews/history.md`](../guardrail-reviews/history.md),
  [`.working/open-findings.md`](../open-findings.md)), which bumped every PR for no reader benefit
  (TODO 3.135, maintainer-approved). These are append-only logs, so a whole-file version carries no
  information a reader uses; the per-row content is the record.
- The per-PR version gates exempt these files: D2 ([`tools/check-version-bump-on-pr.py`](../../tools/check-version-bump-on-pr.py))
  and D4 ([`tools/check-date-cobump-on-pr.py`](../../tools/check-date-cobump-on-pr.py)) add them to
  `EXEMPT_FILES` (the D4 exemption is load-bearing: without it the removal PR itself fails D4). Gate 40
  and the [`block-unbumped-version-commit.py`](../../.claude/hooks/block-unbumped-version-commit.py)
  hook already exclude `.working/`, so they need no edit.
  D7 ([`tools/check-handoff-snapshot-on-pr.py`](../../tools/check-handoff-snapshot-on-pr.py)) drops the
  three `SURFACES` rows for the now-unversioned logs.
- Self-disarming: the version gates key on Version presence, so future appends pass without the
  exemptions (they are regression insurance).

### Also

- Batches the #1192 close-out, the first close-out written with NO Version bumps on these logs.

## 2026-07-26, Library Version 2026.07.682, PR #1192 (daily-rollup reminder D9 + restore previous-week summaries)

### Added

- [`tools/check-daily-changelog-rollup.py`](../../tools/check-daily-changelog-rollup.py) + a D9 wiring
  in [`tools/run-pr-time-checks.sh`](../../tools/run-pr-time-checks.sh): an ADVISORY pre-push check that
  scans the root CHANGELOG for any past UTC date still carrying more than one per-PR entry (never
  collapsed into its daily roll-up) and WARNS `DAILY SUMMARY DUE for <date>`. It exits 0 (never blocks),
  so the reminder is surfaced at every PR and the daily roll-up cannot be silently skipped; a close-out
  checklist line in [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) names the action. Self-test 8/8.

### Fixed

- [`CHANGELOG.md`](../../CHANGELOG.md): restores six previous-week summary blocks (Week of 2026-07-06,
  06-29, 06-22, 06-15, 06-01, 05-25) that #1177 ("the week condensation") had removed from the root,
  recovered verbatim from the pre-#1177 revision. The root now carries the full weekly-summary history
  again below the current per-PR and daily-roll-up entries.

### Also

- Batches the #1191 close-out (bypass, validate-pr SHIP, retro rows + detail file).

## 2026-07-26, Library Version 2026.07.681, PR #1191 (daily roll-up of older root CHANGELOG entries)

### Changed

- [`CHANGELOG.md`](../../CHANGELOG.md): the root changelog's 2026-07-25, 07-24, 07-23, and 07-22
  entries (121 per-PR one-liners) are collapsed into one faithful daily-summary entry per day, in the
  form `**YYYY-MM-DD | <latest version that day> | PRs #A-#B (N PRs)** - <summary>`. The 2026-07-26
  entries are kept per-PR. Per-day PR coverage was verified against the actual entry counts
  (07-25=33, 07-24=38, 07-23=38, 07-22=12) so no PR is dropped. The corresponding older per-PR detailed-mirror entries (#1178 and earlier) are swept to a private
  archive (`grc_library_private/changelog-archive/`), moving the mirror-parity gate dynamic cutoff to
  #1179; the full per-PR detail is preserved in that archive and in git history. Restores the daily-summary
  discipline for older days while keeping the current day granular.

### Also

- Batches the #1190 close-out (bypass, validate-pr SHIP, retro rows + detail file).

## 2026-07-26, Library Version 2026.07.680, PR #1190 (internal tooling + working-record maintenance)

Internal `.working`/tooling maintenance for the local project; no corpus or adopter-facing change.

## 2026-07-26, Library Version 2026.07.679, PR #1189 (token-spend parser: connector allowlist + DOTALL, TODO 3.128)

### Fixed

- [`tools/audit-token-spend.py`](../../tools/audit-token-spend.py) (TODO 3.128, validate-pr-1176 W1 +
  W2): the parser decided attribution by proximity plus a negation BLOCKLIST, so two defects survived.
  W1: a figure in a `## Token spend` SECTION read UNKNOWN because the gap pattern had no `re.DOTALL`
  (measured ~14 of 36 tray deliveries). W2: the closed negation enumeration let `withheld`, `declined`,
  and `unavailable` through, fabricating an adjacent budget number. Both are now closed by an
  input-authority rule (the finding's own recommendation): the `NEGATION` blocklist is replaced by a
  gap-CONNECTOR ALLOWLIST (`gap_is_connector`), so the gap between the spend phrase and the number may
  hold only whitespace, punctuation, and a small set of joining words; any OTHER alphabetic word means
  the number belongs to a neighbouring clause and the parser refuses (reads UNKNOWN). This fails CLOSED
  on every future synonym, not just an enumerated set. `re.S` (DOTALL) is added to the three patterns,
  which is safe precisely because the allowlist rejects prose the newly-reachable span would drag in.

### Verification

- `python3 tools/audit-token-spend.py --self-test` -> 43/43 (9 new `find_reported_spend` reality
  fixtures: the section-format figure now parses to 8400; `withheld`/`declined`/`unavailable` and the
  compact `withheld. Budget 8,000` / `declined. Budget 8,000` forms all read None; the #1175
  not-reported case still reads None; a plain figure and a connector-word gap still parse). The two
  COMPACT forms are the true guard (the old blocklist returned 8000 on them; the new allowlist returns
  None), confirmed behaviourally.

### Also (the #1188 close-out batch)

- The #1188 bypass, `/validate-pr` (SHIP, CLEAN 0 findings), and `/retro` rows, plus the
  [`.working/validate-pr/2026-07-26-PR-1188.md`](../validate-pr/2026-07-26-PR-1188.md) detail file.

## 2026-07-26, Library Version 2026.07.678, PR #1188 (corrective: stale-ledger + handoff sweep + two follow-ups)

### Fixed

- [`.working/open-findings.md`](../open-findings.md): two rows read OPEN when the issues were already
  fixed (a stale ledger). The `submit_state`/`composer_region` E1 row is corrected to FIXED in #1180
  (`e7eea68e`, the runtime-explicit region locator + the E1 reality fixture). The #1179 spec
  bare-positional-refs row is corrected to FIXED in #1181 (`13861709`); attribution corrected from an
  earlier "#1176" claim after git-verifying the occurrence counts (present at #1176, gone at #1181).
- [`.working/session-handoff.md`](../session-handoff.md): swept two now-false directives from the
  resume record (validate-pr-1186 F-1): the "do not run the sweep `--prune` until 3.129 lands" hold
  (3.129 landed in #1186) and the "exec-worker system not built" note (built in #1185, extended in
  #1187).

### Added

- [`TODO.md`](../../TODO.md): two tracked follow-ups. **3.140** (validate-pr-1186 F-2): hoist
  `_check_body` to module scope and add reality fixtures for the two generated-body prune paths and the
  non-UTF-8 branch (an observer-testability gap). **3.141**: per-account worker concurrency greater
  than 1 via config-dir snapshots (design drafted; lower priority now that the `--account` override
  gives cross-account parallelism). Counter advanced to 3.142.

### Also (the #1187 close-out batch)

- The #1187 bypass, `/validate-pr` (SHIP, 1 INFO out-of-scope), and `/retro` rows, plus the
  [`.working/validate-pr/2026-07-26-PR-1187.md`](../validate-pr/2026-07-26-PR-1187.md) detail file.

### Verification

- The two ledger corrections were verified at source (the #1180 fix in
  [`tools/manage-workers.py`](../../tools/manage-workers.py); the #1181 removal via `git grep -F`
  returning zero for `1.19.1` and `3.56a`). Pre-push guard both runners
  green; independent skeptical verifier before push.

## 2026-07-26, Library Version 2026.07.677, PR #1187 (exec-dispatch --account override + #1186 close-out)

### Changed

- [`tools/exec-dispatch.py`](../../tools/exec-dispatch.py): added an `--account` override so a dispatch
  can target a SPECIFIC eligible account instead of the auto-pick. A new pure `pick_account(config,
  family, model, now, account=None)` resolves the target: without `account` it returns the top eligible
  (unchanged behaviour); with `account` it returns that exact account IF eligible, else `None` with a
  reason that distinguishes an unknown account from a known-but-ineligible one. `dispatch()` and the
  `--dispatch` / `--dry-run` CLI paths thread it through, and a failed resolution surfaces loudly (NOT
  DISPATCHED with the reason) rather than silently falling back.

### Why

The wrapper holds a per-account flock that serializes same-account jobs at 1, and the dispatcher had no
in-flight registry, so N concurrent auto-dispatches all picked the top account (`work-a`) and ran
SERIALLY. Confirmed live from the process table: four concurrent workers all on one account, one running
while three blocked on the flock. Targeting a distinct eligible account per concurrent job gives real
parallelism (each account's flock serializes only its own one job). This is the cheap unlock for
concurrent worker prep; per-account concurrency greater than 1 via config-dir snapshots is a separate,
later item. My earlier "config-dir race" diagnosis was wrong (the flock makes it safe-but-serial, not a
race); corrected here.

### Also (the #1186 close-out batch)

- [`.working/merge-bypass-log.md`](../merge-bypass-log.md), [`.working/validate-pr/history.md`](../validate-pr/history.md),
  and [`.working/improvement-log.md`](../improvement-log.md): the #1186 bypass, `/validate-pr` (SHIP, 2
  LOW routed), and `/retro` rows, plus the [`.working/validate-pr/2026-07-26-PR-1186.md`](../validate-pr/2026-07-26-PR-1186.md)
  detail file.

### Verification

- `python3 tools/exec-dispatch.py --self-test` -> OK (17 checks; 6 new `pick_account` cases covering
  auto-pick, targeting an eligible non-top account, targeting the personal account, rejecting a
  known-but-limited account, rejecting an unknown account, and family-scoped resolution).
- `--dry-run --account work-b` prints PICK; `--dry-run --account personal-a` (limited) prints
  REJECTED with the reason. Verified live: a `work-b`-targeted worker ran in parallel with the
  `work-a` flock queue.

## 2026-07-26, Library Version 2026.07.676, PR #1186 (sweep-prune fail-open fix + CLAUDE.md-right-size series)

The fix-first PR of the resumed session: it closes the one open error-class finding (TODO 3.129, the
working-records sweep `--prune` fail-open) and carries the mandatory batched QA rows for #1185. It also
records, but does not yet execute, the CLAUDE.md right-sizing series.

### Fixed
- **TODO 3.129, the destructive-path fail-open in [`tools/sweep-working-records-to-private.py`](../../tools/sweep-working-records-to-private.py).**
  The verify-before-prune guard checked archive-copy EXISTENCE (`is_file()`), not content, so `--prune`
  could delete a source whose archive copy was present-but-divergent (stale, truncated, hand-edited):
  silent data loss on the only destructive path, whose own docstring called the check "the whole
  data-safety guarantee". Fixed with content comparison on ALL FOUR destructive paths, not only the
  one named in the finding: the whole-file copies (records, one-off dirs) byte-compare source against
  archive via a new `_files_identical`; the generated-body archives (weekly changelog-details, roll-up
  rows) recompute the body from new `weekly_archive_body` / `rollup_archive_body` helpers that are the
  SINGLE source of truth shared by both `--emit-archive` and the verify (so the two can never drift),
  and compare. Reality-fixture self-tests added per the guard-input discipline (a present-but-divergent
  archive MUST refuse; `_files_identical` identical/divergent/absent), suite 8/8. Clears the standing
  "do not run `--prune` until 3.129 lands" gate. The open-findings row is marked FIXED atomically with
  the code in this same PR.

### Added
- **TODO series `3.139` (umbrella goal) + `3.139.1`-`3.139.4`**: right-size the ~1960-line every-turn
  CLAUDE.md by moving activity-scoped and already-backstopped prose to `references/` and `_private`,
  keeping only apex rules + behavioral core + a lean playbook index (~800-900 lines target). The
  discipline-to-backstop map is recorded in the umbrella. This is the RECORD only; the work waits
  behind the fix phase (3.127, 3.128, #1179-refutation).
- **Numbering convention**: a multi-phase project takes the next umbrella number as a goal-description
  heading (not a task); its `.Y` children are the independently-closeable tasks (never bundled).

### Verification
- `sweep-working-records-to-private.py --self-test`: 8/8 (incl. the divergence reality-fixtures);
  `py_compile` clean. Batched #1185 QA rows (validate-pr PASS/CLEAN, retro, `--admin` bypass row from
  observed `gh pr checks 1185`) are accurate to what happened. Version+Date co-bumps on every touched
  versioned log.
- A pre-push skeptical verifier (independent exec'd worker, opus/high, briefed to refute) tried and
  FAILED to break any of the four destructive paths, confirmed the emit output is byte-identical to
  pre-refactor (so emit and verify cannot drift), and confirmed the guard fails closed on missing and
  divergent archives. Its one non-blocking, fail-closed observation, that `_check_body`'s `read_text`
  would raise an uncaught `UnicodeDecodeError` on a corrupt (invalid-UTF-8) archive (a traceback
  rather than a clean refusal, no data loss), was HARDENED pre-push: a corrupt/undecodable archive now
  refuses cleanly the same as a divergent one.

## 2026-07-26, Library Version 2026.07.675, PR #1185 (exec-worker dispatch tool + loop-break /validate)

The orchestrator-side control plane for the on-demand exec'd worker harness that the maintainer's
post-resume first task built (root-owned validating wrappers + narrow sudoers + per-account config
dirs under one `worker_agents` Linux user + a read-only worker contract; design of record in
the `_private` companion repo's design-of-record file, project-only operational machinery, not pack
material).

### Added
- [`tools/exec-dispatch.py`](../../tools/exec-dispatch.py): reads the `_private` account-config, filters accounts by family + model +
  usage-state (`limited_until` excludes an out-of-usage account until its reset), orders them
  non-personal-first then by priority-set (exhaust-a-set-then-next) then tier weight, mints a fresh
  per-exec worker id, and launches the family wrapper via `sudo` with `--model` / `--effort`. Pure
  decision logic (now injected for testability) behind a thin dispatch shell; `--self-test` (11
  checks, count printed dynamically so it cannot drift), `--dry-run` (shows the eligible-ordered accounts + the pick + who is excluded and why),
  `--dispatch`. Stdlib-only, in the class of the other project-only worker tools
  (`manage-workers`, `audit-worker-saturation`, `collect-deliveries`).

### Changed
- [`.working/worker-brief-template.md`](../worker-brief-template.md): new DO-list **rail 18** codifying that a worker is READ-ONLY on
  the shared `grc_library` tree and cannot run gates that write into it (canonical case: gate 36, the
  linter-regression suite, writes fixtures to in-tree `tests/tmp/` by design). A worker reports such a
  gate as not-runnable-in-sandbox, never a corpus FAIL; it stays orchestrator-side.

### Verification
- Sweep 123 (this PR): the loop-break `/validate` over #1181..#1184, offloaded to the new exec'd
  worker (work-a/opus), returned **CLEAN** (0 error / 0 warning / 1 environment note) in 7m26s;
  all four targeted confirmations CONFIRMED and all six handoff asserted-expectations CORROBORATED,
  zero contradictions. The orchestrator spot-verified the worker's proof-of-run at source (gate count
  78, the #1181 Sweep-91 orphan's real ancestor `e94b6923`, counts 15/24/16, §3.129 open), so the
  clean verdict is not a confabulated pass. `exec-dispatch.py --self-test`: 11 checks OK, including the
  maintainer's core case (personal-a claude excluded while `limited` until Wed, re-eligible after).
- A pre-push skeptical verifier (offloaded to an independent exec'd worker, opus/high, briefed to
  REFUTE) found the core dispatch logic sound and raised three minor findings, ALL fixed pre-push
  before this PR was pushed: (1) the self-test printed a hardcoded "8 checks" while 10 `check()` calls
  ran and that figure had propagated into this entry, the exact miscount-a-self-test class the repo
  fixed at #1147, now made a dynamic `len()` (11 checks after a regression case was added); (2) one
  self-test assertion was vacuous (re-asserted the family invariant `all([])`-style rather than the
  model filter), rewritten to exercise the `model not in models` branch; (3) `parse_usage_limit`
  false-fired on benign prose quoting the word "limit" (it flagged the verifier's OWN report), the
  loose pattern removed and a regression case added, with the docstring corrected to state its
  deliberately-conservative bias honestly.

### Discipline observation
- The tool is the harness's control plane; the harness itself (wrappers, sudoers, per-account configs,
  read-only settings, safe.directory, the codex `-C` clone) is host/`_private` operational state
  outside this repo, so this PR ships only the in-repo tool + the worker-brief rail + the bookkeeping.
- TODO 3.138 queued: worker full-suite `/validate` via a per-job writable checkout (so a worker can
  run the write-requiring gate 36 in isolation), the principled successor to NOTE-1.

## 2026-07-26, Library Version 2026.07.674, PR #1184 (orchestrator-takeover session-closing handoff)

The session-closing handoff for the 2026-07-26 orchestrator-takeover session. Per the loop-break
discipline it skips its own trailing per-PR QA; the compensating control is the next `/resume`'s
corpus-wide `/validate`, cross-checked against the refreshed Asserted-expectations block.

### Changed
- [`.working/session-handoff.md`](../session-handoff.md): the resume queue rewritten for the takeover
  close (first task the interactive exec'd-worker setup; then the loop-break `/validate`, 3.128 +
  `/sitrep`, the codex deep-assessment, the Phase-3 tray, and the close-out efficiency tooling); a new
  Asserted-expectations block (#1181-#1183 all merged and validated CLEAN; inventory 78/15/24/16); and
  the locked decisions recorded so `/resume` does not re-ask.
- [`.working/session-state.md`](../session-state.md): the concurrency lease RELEASED (`Status: released`,
  `Active-session: none`).
- [`.working/next-prs.txt`](../next-prs.txt): the resume queue.

### Added
- #1183's `/validate-pr` (CLEAN), `/retro`, and `--admin` bypass rows batch in per recursion-avoidance.
- [`TODO.md`](../../TODO.md) items 3.133-3.137: the close-out-efficiency cluster (a PR close-out
  scaffolding tool, auto-bump-on-commit, dropping the Version field from append-only `.working` logs, a
  handoff-snapshot generator, and a fix-loop quick guard), maintainer-directed to execute EARLY in P3,
  from the takeover's fresh-eyes observations. TODO 3.132 (guardrail G-1) resolved by the maintainer's
  decision to accept the recorded-retirement half.

### Verification
- Session-closing handoff (loop-break exempt from its own trailing QA); `tools/pre-push-guard.sh` green.

Handoff note: the resume's FIRST task is the interactive, step-by-step setup of the orchestrator-managed
exec'd codex + claude workers (single fresh `worker_agents` user, per-account config dirs via
`CLAUDE_CONFIG_DIR` / `CODEX_HOME`, root-owned sudo wrappers), whose full design and the maintainer's
locked decisions live in the exec-worker decision note in the `grc_library_private` companion repo, with
a staged prep-instructions file for the setup. A DGX-Spark local-model worker (free, highest-priority)
is noted there as a future worker host, not an orchestrator relocation.

## 2026-07-26, Library Version 2026.07.673, PR #1183 (/restore-broken recovery command)

Adds a slash command that codifies recovery of a project whose orchestrator died, ran out of usage, or was interrupted
mid-session. It is the recovery counterpart to `/resume`: where `/resume` rebuilds from a CLEAN session-closing
handoff, `/restore-broken` handles the case where there is no clean handoff and the lease, handoff, and delivery tray
are internally inconsistent. This PR ships the command as the reusable form of the takeover this session performed.

### Added
- [`.claude/commands/restore-broken.md`](../../.claude/commands/restore-broken.md): a five-phase protocol (assess
  read-only; report and ask for an express GO; recover with independent verification; wind down to a clean green
  branch; same-session resume as the compensating control). It bakes in the specific traps this takeover hit: the
  turn-end-safety check for an auto-commit stop hook, the stale-lease unattended-mode that silently blocks interactive
  questions, the tray-count-is-not-the-unprocessed-count trap, the permission-model health check, and the "verify the
  interrupted unit as a hypothesis, not an inheritance" discipline. It recommends running recovery on a HIGH reasoning
  effort, since a broken-orchestrator takeover is exactly the high-stakes work where a missed nuance is expensive.
- [`TODO.md`](../../TODO.md) item 3.130: a tracked follow-up to add the PORTABLE pack form of the recovery discipline
  (a recovery subsection in the pack `session-lifecycle` rule), per the pack-parity coupling.
- [`TODO.md`](../../TODO.md) item 3.131: a maintainer-requested P3 tooling item to log each worker's headless console
  events (claim / heartbeat / deliver / error) to a searchable dated per-worker file under `grc_working/logs/`, so
  headless worker and codex-exec output is greppable and tailable after the fact.
- [`.working/guardrail-reviews/`](../guardrail-reviews/): guardrail-review **r16** (detail file `2026-07-26-r16.md` plus
  a history row), auto-prompted because the new `/restore-broken` command tipped the machinery-drift cadence (gate 60) to
  3. Offloaded to a worker and orchestrator-re-verified at source. Verdict COHERENT (inventory 78 gates / 15 rules / 24
  skills / 16 commands; 0 overlap, 0 drift); one LOW gap (G-1: gate 78 enforces only the recorded-retirement half of the
  absolute never-recycle rule, its DONE.md-heading-id closure unqueued) routed to [`TODO.md`](../../TODO.md) item 3.132 as
  a maintainer-decision proposal.

### Changed
- The prior PR's QA rows batch in per recursion-avoidance: #1182's `/validate-pr` row, `/retro` row, and `--admin`
  bypass row.

### Verification
- The new command lints clean (language, unbalanced-fence checks on its explicit path); pre-push guard green
  (78 audit gates plus all PR-time checks). An independent pre-push refute-briefed verification confirmed the command's
  referenced files, rules, and phase steps are accurate and that it invents nothing.

## 2026-07-26, Library Version 2026.07.672, PR #1182 (orchestrator-takeover reconciliation)

Bookkeeping for an orchestrator handover. A new orchestrator session took over after the prior 2026-07-25
overnight-unattended session ran out of usage mid-work on #1181; the takeover ran read-only assessment first, then
verified and landed the interrupted #1181 (independent adversarial pre-push verify: nothing invented, nothing lost),
merged clean at `13861709` via `--admin`. This PR reconciles the takeover state.

### Changed
- [`.working/session-state.md`](../session-state.md): the concurrency lease reconciled to the takeover session
  (`Active-session: claude/takeover-reconcile`, `Operating-mode: attended-autonomous`, fresh heartbeat),
  with a current-task narrative of the takeover and the deferred queue.
- [`.working/next-prs.txt`](../next-prs.txt): refreshed to the post-takeover queue.

### Added
- [`.working/validate-pr/history.md`](../validate-pr/history.md): the #1181 row (RETURNED PASS, 0 findings). Its QA
  was an independent adversarial PRE-PUSH verify (`verify-1181-ledger-repair`, an Opus 4.8 worker on the file-drop
  transport), which per-row traced every restored ledger row to real git history and proved de-fusion completeness
  by word-multiset diff; re-verified by the orchestrator at source before merge.
- [`.working/improvement-log.md`](../improvement-log.md): the #1181 `/retro` row. Lesson: order-premise accuracy is
  the orchestrator's job, not the worker's to rescue; a rough structural grep is not a measurement, and the order
  carried a diff miscount the worker flagged.
- [`.working/merge-bypass-log.md`](../merge-bypass-log.md): the #1181 `--admin` bypass row, written after the merge
  from the observed `gh pr checks` output (green CI).
- [`.working/open-findings.md`](../open-findings.md) plus [`TODO.md`](../../TODO.md) item 3.129: a recorded
  destructive fail-open in [`tools/sweep-working-records-to-private.py`](../../tools/sweep-working-records-to-private.py).
  Its verify-before-prune guard checks archive-copy EXISTENCE, not content, so `--prune` could delete a source whose
  archive copy is present-but-wrong. Surfaced by the takeover tray reconciliation, re-verified at source. Imminence is
  low (manual close-out step), but the fix gates any `--prune` run.
- [`.working/worker-prompt-log.md`](../worker-prompt-log.md): the prior session's final worker-nudge rounds, restored
  (they were uncommitted in the working tree when it ran out of usage).

### Verification
- Pre-push guard green: 78 audit gates plus all PR-time checks (D1 to D8, gates 45/40/31). The takeover also
  established and verified the worker-access permission model across the launch root (workers read-only on the corpus,
  denied the shared scratch and private repos, read-write only on the exchange), with a re-runnable check script.

Discipline observation: this PR is orchestrator-only bookkeeping (authoring the audit-trail rows, the lease, the
CHANGELOG), which the mandatory-offload rule keeps orchestrator-side; the two live Opus 4.8 workers served only the
read-only #1181 verification and the tray reconciliation that fed it.

## 2026-07-26, Library Version 2026.07.671, PR #1181 (seven lost QA rows restored, none invented)

Seven rows of the validation-sweep and matrix-fit ledgers had been silently destroyed by editing mistakes. All seven
are restored, every one recovered from an intact prior revision of its own ledger file, and **nothing is synthesized**.

### Why seven and not six

TODO 3.73 recorded ONE escape of the ledger-fusion class. A worker measuring detector candidates found **five** fused
rows in [`validate-sweeps/history.md`](../validate-sweeps/history.md) and one in
[`matrix-fit/history.md`](../matrix-fit/history.md); an independent re-scan by a different worker, using three signals
none of which was the original over-width one (sequence gap, foreign detail reference, header-role reset), re-found all
six and confirmed no seventh FUSION.

The seventh loss is a different mechanism, and it is why the re-scan's verdict was right about fusions and incomplete
about lost rows. **Sweep 91 was OVERWRITTEN, not fused.** In `8d198b2c` an Edit anchored on the Sweep 91 line and
replaced it with Sweep 92's, deleting it outright. An overwrite leaves a perfectly well-formed, width-normal table, so
no fusion detector can see it; the only signal is the sequence gap, which the re-scan DID measure and then correctly
declined to reconstruct from, because inventing a row identifier from a gap would have been fabrication. A one-command
history search (`git log -S"91 iter 1"`) resolved the gap into a real row.

**The detail that would have destroyed evidence.** Sweep 91's Summary cell survived, orphaned mid-line between Sweep 92
and Sweep 90. The fusion reconstruction treats a fused line as row A truncated at header width plus the absorbed tail,
which would have dropped that orphan entirely, deleting the last trace of Sweep 91 while appearing to repair the line.
The cell was verified byte-identical at 1502 characters against `e94b6923` before being rebuilt into a row.

### How the repair was applied

Deterministically, with a re-parse, rather than by hand, per the high-assurance apply discipline. Three properties are
worth recording because each was a decision:

- **Identity, not byte-equality.** A first pass demanded the surviving tail match its intact revision exactly and
  refused to apply when two rows differed. The differences turned out to be the dash-removal sweep (an em-dash rewritten
  to a comma or to `none`) and the de-link, against common prefixes of 254 to 2927 characters. So the surviving tail is
  NEWER and correct, and demanding equality would have restored stale prose. The check became a prefix-identity proof
  and the tail is kept as-is.
- **The de-link rule.** Each recovered row references its per-run detail file as a markdown link, and all five of those
  files were swept to the private archive and de-linked across the rest of the ledger. A verbatim restore would have
  reintroduced five dead links among nine valid ones and silently undone that migration. Stated honestly by the worker
  who found it: this would NOT fail CI, because `.working/` is gate-exempt, which is exactly the condition that let the
  fusions survive.
- **Line numbers move.** All six locators shifted by one between the pin and the applying tree, so they were re-derived
  immediately before the edit rather than trusted from the delivery.

### Verification

Post-repair re-parse: **zero fusions remain** in either ledger, and **zero unexplained sequence gaps**. The four
over-width rows still present in [`validate-sweeps/history.md`](../validate-sweeps/history.md) are the known prose-pipe false positives, not fusions. The
apparent duplicates at Sweeps 9 and 10 are legitimate multi-iteration rows (`9 iter 1/2/3`). Gaps 1 to 8 predate the
ledger, whose earliest row is Sweep 9 on 2026-06-20.


### Added, after the maintainer asked for it directly

**[`block-unbumped-version-commit.py`](../../.claude/hooks/block-unbumped-version-commit.py), a
PreToolUse hook for the per-commit version discipline.** Five misses in one session, with a close-out
checklist bullet written between the third and the fifth and two more misses after it. That is the
signature of a control at the wrong layer: the knowledge was present and the timing was not. Gates 40
and D2 already catch this, but they speak six minutes later at pre-push, by which point the repair is
itself a new commit touching the file. That is how one miss becomes a chain, and it did: a D4 repair
that moved a `Date` became a gate-40 failure, whose repair became a gate-33 failure.

It reads the STAGED diff, so its input can answer the question asked of it, and blocks a staged body
change to a versioned document with no staged `Version`. It separately WARNS, without blocking, when
a corpus `Version` moved and no generated artefact is staged, which is the sixth-instance shape;
warns rather than blocks because a blocked commit cannot be fixed without unstaging.

Three deliberate non-features, each recorded because each is a place a broader hook would have been
worse. It does NOT check `Date` against the commit date: delta gate D4 owns that, the commit date
does not exist yet at PreToolUse time, and inventing one would be a check whose input cannot answer
it. It skips `--amend`, whose diff is not the staged set alone. And it fails OPEN on every error
path, the same trade [`block-on-open-findings.py`](../../.claude/hooks/block-on-open-findings.py) records, because a guard that blocks all work when
it breaks is removed within a day.

The escape hatch is a `VersionBump: none <reason>` line in the commit message. A guard with no stated
exception gets bypassed wholesale with `--no-verify` the first time it is wrong, which is strictly
worse than a hatch that leaves its reason where a reviewer can see it.

**Verified three ways rather than by fixture alone:** self-test 17/17, wired into the linter
regression suite, and a LIVE end-to-end probe against a real staged change (blocked without a bump,
cleared with one, opt-out honoured, probe reverted). The self-test earned its keep immediately by
catching a real bug: the matcher tested for the substring `git commit`, which never appears, because
the wrong-repo guard requires `git -C <root> commit` and that is the only form this project runs.

### Discipline observation

**A worker declined to certify its own completeness claim, and it was right to.** The worker that found the six fusions
also wrote the detector, and said so: a fusion its signal cannot see is invisible to its own re-scan, so it asked for an
independent check with a different signal. That check found no seventh fusion and its unresolved gap caveat is what led
to the overwritten row. Neither worker found Sweep 91 alone; the combination did, plus one history search neither had
been asked to run. The lesson belongs to the ORDER rather than to either worker: a completeness order over a numbered
ledger must ask explicitly for a history search on every unresolved sequence gap, because a gap is either a number never
used or a row deleted, and only history tells them apart.

## 2026-07-26, Library Version 2026.07.669, PR #1180 (the QA that was closed over came back FAIL)

`validate-pr-1176`, the order the 2026-07-25 session closed without waiting for, finally ran. It came back **FAIL with
one error and two warnings**. That is the maintainer's directive vindicated in the most direct way available: had the
order stayed unserved, an error-severity defect would have sat on `main` indefinitely with the parity gate green
throughout.

### Fixed

**A residual FALSE-SUBMITTED path in `submit_state` (E1, error).** The #1175 fix normalized whitespace so a probe
spanning a tmux line-wrap still matches. That repaired the MATCH and left the REGION wrong.
[`composer_region`](../../tools/manage-workers.py) took `rules[-2]` when two horizontal rules were present and
`rules[-1]` otherwise, which cannot distinguish "one rule because this is Codex" from "one rule because the payload is
tall enough that the composer's TOP border has scrolled out of the captured tail". In the second case `rules[-1] + 1`
selects the status line BELOW the composer, which can never hold the payload, so the probe is absent and the function
answers `submitted` for a prompt still sitting in the box.

It is reachable rather than theoretical, and worst exactly where it matters most: the bottom border is almost always
inside a 12-line tail, the top leaves it once the payload wraps to roughly ten lines, and the probe is the payload's
FIRST 40 characters, which is precisely the part that scrolls away first. So the check failed most readily for the long
payloads the original fix was written to handle. Same failure direction as V1175-1, which this project graded error.

The fix tells the locator WHICH runtime it is reading, since the caller already resolved it, and returns INDETERMINATE
where it genuinely cannot tell: a Claude pane showing one rule now refuses rather than guessing. Pinned by a reality
fixture built from the actual failing pane shape. Self-test 47 to 53 cases. Two pre-existing Codex cases were corrected
to pass the runtime the real caller passes, rather than the new refusal being relaxed to accommodate them.

### Changed

**An undelivered per-change QA is BLOCKING, and a slow worker is RE-ISSUED (maintainer-directed).** #1178 established
that the result must RETURN; this says what to do while it does not. Where the holding worker has not delivered in a
reasonable time, the SAME order goes to a second worker and whichever returns first is authoritative. A later arrival
is neither discarded nor re-adjudicated as a competing verdict: it is read as a CROSS-REFERENCE confirming the accepted
result missed nothing, and a finding present only in the late delivery is triaged on its own merits. Safe because a
read-only QA order costs a worker cycle and nothing else, and it converts a stalled order from an indefinite block into
a bounded one. Portable half in the pack's
[`session-lifecycle.md`](../../dev-security/claude-rules/governance/session-lifecycle.md) section 5.

**The integrity checkpoint gains a minimum cadence (maintainer-directed).** The checkpoint list was semantic, and a
semantic list is exactly what a long run erodes, because every checkpoint is one the actor must notice. This session
the assistant went two entire PRs without emitting the AIQT line and re-anchored only when the maintainer asked whether
it had forgotten. The cadence now has a floor that does not depend on noticing, at least once per PR, and the emission
must be SELF-ACKNOWLEDGED rather than recited: a clause or two naming what, on that specific change, the tier is being
held against. A bare recited line is the decorative form and discharges nothing. Portable half in
[`project-integrity.md`](../../dev-security/claude-rules/governance/project-integrity.md).

### Added

TODO **3.126** (the disposition cell needs a structural fix, not a third round of matcher hardening), **3.127**
(`submit_state` residuals beyond the fixed one), **3.128** (the token-spend parser loses 12 of 31 real figures and
invents others). Counter advanced 3.126 to 3.129.

### Discipline observation

**My own #1178 fix reproduced the class it was closing, and a worker caught it.** `validate-pr-1178` found that the new
disposition-vocabulary matcher fails in BOTH directions: it false-BLOCKS six real dispositions because `startswith`
demands the vocabulary word first, and it false-PASSES five narrations that open with a terminal word and then negate
it. The sharpest is `**routed** but nobody took it`: correct markup, correct vocabulary, and it says in plain words
that nothing was decided. I hardened a predicate instead of fixing its input, which is verbatim the anti-pattern
[`validate-inference-before-action`](../../.claude/rules/governance/validate-inference-before-action.md) names, and I
did it in the same edit where I cited that rule. Routed as 3.126 for a structural fix rather than a third pattern.

**Both `/validate-pr` rows that read DISPATCHED now read their returned result.** That is the #1178 directive working on
its first outing, and the reason the row wording matters: an honest pending row still satisfies gate 50 Check 1, so
nothing mechanical would have chased either of them.

## 2026-07-26, Library Version 2026.07.668, PR #1179 (the inbox drops triaged, and what each one turned out to be)

The eight unprocessed inbox drops were read. Four were worker-raised `issue-*` items dispositioned in #1178; the
other four are larger documents, and one of them carried nine decisions nobody had seen.

### Why this needed its own PR

The file-drop `inbox/` is the channel for work handed to the orchestrator OUTSIDE the order queue, so no gate walks
it, [`tools/audit-delivery-status.py`](../../tools/audit-delivery-status.py) does not reconcile it (it reads worker
OUTBOXES), and nothing in the task list is built from it. A drop can therefore sit unread indefinitely while every
instrument reports health. One here had.

### Changed

**TODO 2.20 is now EGRESS-GATED, cross-referenced as MEG-48 (maintainer-directed).** A worker completed everything
around the single blocking field and then correctly refused to finish: `last_checked` records that someone verified
an entry AGAINST UPSTREAM, so no amount of held material can establish it, and proposing a date would have been an
inference presented as a verification. Ready to apply once the upstream pass happens: the item identification,
per-item held-source evidence, drafted `checked_edition` for all six, and paste-ready hunks with the date left as a
placeholder. The **EU Digital Omnibus** goes first, being the only one of the six awaiting a dateable adoption event
rather than a routine refresh, and its status bears on the EU AI Act entry too. The request block is in the
maintainer's egress queue in `grc_library_private`.

**TODO 3.56's numbering is settled as LEAVE AS IS (maintainer-decided).** [`TODO.md`](../../TODO.md) tracks the item as `3.56` while
[`DONE.md`](../DONE.md) records three post-rule partial closes against `3.56a`. The ids genuinely differ, so nothing resolves to
the wrong item and gate 78 is correct to stay silent. Normalizing either side would make the gate fire three times
on three legitimate partial closes, needing three `EXEMPT` rows that exist only to silence a self-inflicted firing.
Recorded in the item so the question is not re-opened.

### Added

**TODO 3.125, codex worker guard rails phase 1.** The maintainer's report is that codex workers misdescribe what
they are doing and need to be called out before they actually work. The mechanism is structural rather than
behavioural: a codex worker's heartbeat is stamped by a background daemon that is a SEPARATE code path from the
work, so a worker whose turn ended an hour ago still reads `LIVE` and answers a status question from context rather
than from state. The drop's first measurement was then corrected by its own author, before this item
was committed, and the corrected picture is worse. Not two sessions dying at startup: one genuinely dead, and one
that went **163 minutes between its first heartbeat and its second** and is alive still. Since 163 minutes is about
eight times the 20-minute stale window, a LIVE codex worker reads as DEAD for most of its life, which makes the
stale-scan capable of reclaiming an order from a worker that is mid-gap and still working it, so two workers could
deliver the same order id. The maintainer
chose guard rails before the VM-local runner, and chose to split this phase out because it is load-bearing and
testable alone: the heartbeat moves INTO the claim-and-serve loop so that when work stops the heartbeat stops, and
every liveness verdict is DERIVED from artefacts the worker does not author. The corrected timestamps are the reality fixture, and a third change is added: the
stale-scan must not reclaim from the codex family until the cadence is fixed. This is the genuine fix behind TODO 3.116, which was closed with a stall signal that could not
fire.

**TODO 3.123**, the answered-question guardrail's own blind spot, and **TODO 3.124**, two verified `_ref` catalogue
defects. Counter advanced 3.123 to 3.126.

### Fixed and refuted

**One drop finding is REFUTED, and re-measuring is what showed it.** Drop D2 reported eleven positional references
in the audit-programme spec, five already broken, including a `TODO section 3.9` resolving to a DIFFERENT item
through pre-rule number recycling. That would have been the never-recycle harm sitting in corpus prose, invisible to
the gate built to catch it. Re-measured on live `main`: `grep -c 'TODO section'` on that file returns **0**, because
#1176 converted all eleven citations to closing-PR anchors, and Sweep 122 independently confirmed the same zero. The
drop was written against a pre-#1176 tree. Routing it unexamined would have sent the orchestrator to fix something
already fixed, and asserted a live defect that does not exist.

**Two `_ref` catalogue defects are ROUTED, not applied, and deliberately so.** D4: the `notes` field on the EU
Implementing Regulation (EU) 2025/454 entry describes an Australian statute, and the Australian entry has no `notes`
of its own, so the text was moved onto the wrong entry rather than duplicated. D5: a Canada TB Directive title
presents a compliance transition that ended 2026-06-24 as still running. Both are held-evidence findings needing no
egress. Neither has been re-verified at source by the orchestrator, because `_ref` is a separate repository and the
fix is a separate PR; the routing says so explicitly rather than implying the worker's verification is mine.

### Discipline observation

**The answered-question guardrail false-negatived on a question the maintainer had answered in writing.** Before
surfacing drop D1 (whether to widen gate 69 to `docs/`), [`tools/decisions-search.py`](../../tools/decisions-search.py)
was run as the rule requires and reported `NO recorded decision found`. The maintainer had answered exactly that
question the same day, and their words are quoted verbatim in [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md)'s defence-in-depth section. The
tool's `SEARCH_STORES` covers the pending queue, the private design-decisions record and the closed-work ledger, and
does NOT cover CLAUDE.md, which is where standing directives live. So D1 was NOT re-asked, the recorded answer being
to widen; and the gap is queued as 3.123. This is the fifth instance in one week of a guard whose logic is sound and
whose input cannot answer the question asked of it.

**A scripted multi-replace reported success while matching nothing.** Two ledger rows kept their old text through a
`python3` `str.replace` pass that printed a success line, and only a follow-up grep caught it. `Edit` fails loudly on
a near-miss; `replace` no-ops silently. Recorded in the retro as a habit to change, not just an incident.
