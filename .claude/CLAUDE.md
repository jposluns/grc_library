# CLAUDE.md

> **Condense note (PR #441):** this file was condensed per the maintainer's "keep
> actionable rules, cut rationale/war-stories/duplication" directive (Option B). Every
> rule and procedure step is retained; the removed rationale, war-stories, and provenance
> are preserved verbatim with analysis in
> [`.working/claude-md-considerations.md`](../.working/claude-md-considerations.md), which
> is reviewed each `/retro` and the periodic hallucination-metrics pass so a removal can be
> restored if its "evidence the removal was wrong" signal appears.

## PRIMORDIAL RULE: PROJECT INTEGRITY (HIGHEST PRECEDENCE)

This rule has the highest precedence in this project. It sits above every other section of this file and above the user-level / project-layer reconciliation note immediately below it: that note governs *which rule source wins* on a rule-source conflict; this rule governs *which optimization dimension wins* on a quality / speed / cost conflict. The two are complementary, not competing.

**Priority ordering, lexicographic and absolute: Quality > Speed > Cost.** The integrity of the project is absolute. This rule overrides all other optimization pressures, including token economy, latency, and the assistant's own inclination to complete quickly.

### 1. Priority enforcement
- Quality is never traded for speed; speed is never traded for cost.
- When two dimensions conflict, the higher-priority dimension wins outright. Optimize for cost only after quality and speed obligations are fully satisfied.
- "Done faster" or "done cheaper" is never a justification for "done worse".

### 2. Integrity (non-negotiable)
- Correctness over apparent completion. Do not stub, mock, hardcode, or simulate a result to appear finished.
- No silent changes. State every modification. Do not expand scope without instruction.
- No suppression. Do not comment out, weaken, skip, or delete tests, assertions, type checks, linting, audit gates, or error handling to force a pass. (This is the `gate-discipline` pack rule at apex precedence.)
- No fabrication. Do not invent function names, APIs, configuration keys, citations, or behaviour. If unknown, stop and say so. (This is `evidence-grounded-completion` at apex precedence.)
- Failing states are surfaced, never concealed.

### 3. Escalation
If any constraint forces a quality compromise, halt and escalate the tradeoff to the maintainer explicitly. Do not resolve it silently in favour of speed or cost. (This is `clarify-before-acting` applied to optimization-dimension tradeoffs.)

### 4. Self-reminder cadence
The assistant has no internal timer. Re-anchor to this rule at these semantic checkpoints:
- At the start of every task or plan.
- Before `git commit` or any equivalent persistence action.
- Before declaring any task, step, or TODO item complete.
- At every point where quality, speed, and cost are in tension.

At each checkpoint, emit one line, then confirm compliance or halt:
`Integrity check: Quality > Speed > Cost. Project integrity absolute.`

The project-agnostic distributable form ships as the pack governance rule [`governance/project-integrity.md`](../dev-security/claude-rules/governance/project-integrity.md).

---

User-level rules in `~/.claude/CLAUDE.md` govern the assistant's general behaviour
(verification before assertion, evidence-grounded completion, action-before-explanation
of inaction, clarify-before-acting on ambiguous choices). This file wins on
project-specific matters (workflows, terminology, what counts as routine in this repo)
and fills in domain-specific conventions that the user-level rules deliberately don't
encode. On genuine conflict between the two layers, surface it rather than silently
pick which layer to honour.

## Project
The GRC Library: a CC BY-SA 4.0 corpus of governance, risk, and compliance
documentation in Markdown, plus a stdlib-only Python audit toolchain that keeps the
corpus internally consistent. There is no application runtime: the deliverable is the
documents and the linters that govern them.
- Documents live in domain dirs: `ai/` `architecture/` `compliance/` `dev-security/`
  `governance/` `operations/` `privacy/` `resilience/` `risk/` `security/`
  `supply-chain/`.
- Audit/build tooling lives in `tools/` as `lint-*.py` and `build-*.py` scripts;
  shared helpers in `tools/lint_common.py`. Tests in `tests/`. Exact counts drift as
  gates are added; the source of truth for the current set is
  `tools/run_all_audits.sh` and `.github/workflows/quality.yml`.
- `taxonomy.yml`, `docs/portal.md`, and `docs/maturity-scorecard.md` are generated
  from document metadata: never hand-edit generated files; regenerate via
  `tools/build-taxonomy.py` and `tools/build-portal.py` and commit the source plus
  the regenerated output together.

## Why
Every document carries a 13-field metadata block and a fixed section model so the
corpus is machine-auditable. The audit programme (gate inventory in
`governance/specification-audit-programme.md` §6) enforces that model so governance
content stays citable, cross-linked, and free of drift, secrets, or PII.

## Commands
- Full audit sweep (all gates, CI order): `tools/run_all_audits.sh`
- Stop on first failure: `FAIL_FAST=1 tools/run_all_audits.sh`
- One gate: `python3 tools/<lint-name>.py`
- Linter regression tests: `python3 tools/run-linter-regression.py`
- Pre-commit (mirrors CI): `pre-commit run --all-files`
- Regenerate derived artefacts: `python3 tools/build-taxonomy.py`,
  `python3 tools/build-portal.py` (CI checks sync via `--check`)

CI source of truth: `.github/workflows/quality.yml`. Keep `quality.yml`,
`tools/run_all_audits.sh`, and `.pre-commit-config.yaml` in lock-step: a gate added to
one must be added to all (the gate-parity audit enforces this).

## Structure
- `tools/lint_common.py` — shared file discovery, exemption sets, helpers.
- A new audit = a `tools/lint-*.py` + wiring in all four surfaces (workflow, runner,
  pre-commit, audit-programme spec) + a regression fixture.
- Exempt dirs are defined in `tools/lint_common.py` as `DEFAULT_EXEMPT_DIRS`
  (`.git`, `node_modules`, `__pycache__`, `.claude`, `.working`); individual linters add
  their own per-tool exempt prefixes on top (e.g. `dev-security/claude-rules/`,
  `tools/`, `docs/` carve-outs): consult each `lint-*.py` for its specific set
  rather than treating the common set as the full list.
- `.working/` — maintainer working space holding per-run records from `/validate`,
  `/fitness`, and other maintainer-invoked activities. The contents are
  frozen-state archives (cross-references accurate as-of write-time), exempt from corpus
  audit gates, and not intended for adopter consumption. See
  [`.working/README.md`](../.working/README.md) for the convention and subdirectory
  inventory. Adopters cloning the library can delete `.working/` outright or keep it.

## Conventions
- Mirror an existing same-type document's metadata and section shape rather than
  inventing one; changing the model means changing the linters that enforce it.
- External-standard citations must be accurate and current — `lint-citations.py` and
  `lint-standards-currency.py` reject hallucinated or stale references.
- Prose style is enforced by `lint-language.py`; do not fight the linter by hand.

## Language convention
The library uses **Canadian English first, Commonwealth (UK / Australian) English
second, other dialects last.** Canadian English shares its `-ize` / `-ization`
orthography with American English (the Oxford convention adopted in Canadian usage),
so the `-ize` rule that `tools/lint-language.py` enforces is the Canadian-orthography
manifestation of the convention, not a generic American mandate. Where Canadian English
has no opinion, Commonwealth forms are preferred; where neither has an opinion, other
dialects' usage is acceptable. Em-dashes (`—`) and en-dashes (`–`) are forbidden in
prose regardless of dialect; use commas, colons, or parentheses.

## Testing
- A change is green only when `tools/run_all_audits.sh` reports all gates passing.
- Add a regression fixture in `tests/` (see `tests/README.md`) for any new linter.

## Date and timezone convention

The assistant works in **UTC** for all date-bearing fields and "today" calculations.
Per-document `Date` fields, fitness-review file names (`YYYY-MM-DD-rN.md`), `/validate-pr`
record file names (`YYYY-MM-DD-PR-<N>.md`), CHANGELOG entry date headers, and the
fitness-review history's `Date` and `Originating run` cells are all UTC dates.

Maintainer-side note: the maintainer is in `America/Toronto` (GMT-5 standard / GMT-4
daylight). The project's audit-trail dates are therefore offset 5 or 4 hours from the
maintainer's wall clock. When the maintainer says "today" in conversation, that may
correspond to the previous UTC day if it is before 19:00-20:00 EST locally; the assistant
writes the UTC date into artefacts but stays aware that the maintainer's local "today"
can lag by one day. Where there is potential for ambiguity, use the UTC date.

## PR workflow
PRs in this repository follow a fixed pattern that the assistant is authorized to
drive end-to-end on the maintainer's behalf:

1. Develop on a named feature branch (never on `main`); confirm
   `tools/run_all_audits.sh` passes standalone **after each commit** on the feature
   branch, not only before the final push (the history-aware gates 40/31/45 see only
   committed state, so a between-commits run catches what a working-tree run misses).
   Before pushing, run both runners as a single pre-push gate:
   `tools/pre-push-guard.sh && git push -u origin <branch>`. The guard chains
   `run_all_audits.sh` (corpus gates from HEAD) then `run-pr-time-checks.sh` (the PR-only
   delta gates D1-D4 plus the history-aware trio 45/40/31 against the merge base),
   stopping non-zero on the first failure, so a gate defect blocks the push instead of
   flipping CI red after the fact. The two runners together cover every gate CI runs.
   Git hooks do not fire in this environment, so the `&&`-chained guard is what actually
   enforces the pre-push runner (the same pattern as `preflight-changelog.py && git
   commit`); an "intermediate" push that skips the guard is the momentum-bypass failure
   the guard closes (improvement-log #438/#439).
2. Push with the pre-push guard: `tools/pre-push-guard.sh && git push -u origin
   <branch>`. On a green guard, open the PR via `mcp__github__create_pull_request`.
3. Wait for the `Lint markdown corpus` CI check using the subscription discipline in
   `## PR activity subscription discipline` below; on failure, fix and re-push.
4. On green CI, merge via `mcp__github__merge_pull_request`. The maintainer does not
   gate-keep merges of PRs they have personally authored. `mergeable_state: blocked`
   is the branch-protection state immediately before merge, not a human-review gate;
   the merge attempt resolves it.
5. After merge: sync local `main`, delete the feature branch locally, confirm the
   remote branch is gone.
5a. Invoke `/validate-pr` to run the PR-scoped post-merge validation sweep (dispatches
   Subagent A on the just-merged PR's diff plus a cross-reference check on files citing
   the touched files). Records to [`.working/validate-pr/`](../.working/validate-pr/).
   Triage findings as in-window (hot-fix PR or include in next PR) or out-of-window
   (surface to maintainer with named options). **Handoff-PR exception (loop-break):** the
   session-closing handoff PR does NOT run a trailing `/validate-pr` or `/retro`; the
   compensating control is the next session's `/resume` corpus-wide `/validate`. Record
   the exemption in the handoff PR's `.working/validate-pr/history.md` row **Findings cell**
   (the cell `tools/lint-bookkeeping-parity.py` (gate 50) reads to detect the handoff
   exemption): the marker must be `SKIPPED` together with `handoff`, or the phrase
   `handoff-PR exception`, never a bare `n/a`. Putting the marker in the Summary cell only
   (leaving the Findings cell `n/a`) leaves the row undetected as a handoff: it passes
   while the PR is the highest-numbered (exempt as in-flight) but gate 50 flags it the
   moment the next PR demotes it (the #445/#450 recurrence, fixed in #446/#451). Fuller
   prose may still go in the Summary cell. (See `## Session migration and PR close-out
   checklist` item 3.)
5b. Invoke `/retro` to run the post-merge retrospective per the
   [`pr-retrospective`](../dev-security/claude-rules/skills/pr-retrospective/SKILL.md)
   skill: append one row to [`.working/improvement-log.md`](../.working/improvement-log.md).
   Pattern and Proposed-improvement entries (if any) surface in chat. The register-row
   commit batches into the next PR per the recursion-avoidance rule.
5c. Refresh [`.working/session-handoff.md`](../.working/session-handoff.md) with the
   current state snapshot, last-merged list, next-actions queue, and open decisions. At a
   **session-closing** handoff PR, also refresh the `## Asserted expectations` section
   (the surfaces this session mechanically verified, scoped to what it touched, plus known
   soft spots NOT asserted clean), the **green-at-`<sha>`** snapshot line, and the
   [`.working/session-metrics.md`](../.working/session-metrics.md) row (these are the
   loop-break compensating control's cheap signals the next `/resume` `/validate`
   cross-checks against). The refresh commit batches into the next PR per
   recursion-avoidance. See `## Session migration and PR close-out checklist`.
6. After every merge (durable across sessions): consult [`TODO.md`](../TODO.md)'s
   forward-looking sections and list the upcoming next five planned PRs in the chat. If
   new items surfaced during the just-finished work, add them to TODO BEFORE the list is
   published (the list comes from TODO, not from memory). This is the project-specific
   instantiation of the PR finalization protocol in
   [`.claude/rules/governance/change-tracking.md`](../.claude/rules/governance/change-tracking.md).
7. TODO/DONE rotation discipline: when a PR closes a TODO item, the item is deleted from
   TODO in the same PR and an entry is added to [`.working/DONE.md`](../.working/DONE.md)
   (the closed-TODO ledger, keyed by PR number with the original backlog ID as a
   cross-reference). The rotation lives in the same commit. TODO holds only
   forward-looking content; historical lists belong in DONE, not in TODO. **"TODO item"
   is backlog-item-keyed, not FR/§-keyed**: a `FR-N` item, a numbered `§N.M` subsection,
   AND a prose-named or maintainer-directed item recorded in TODO (e.g. "OT post-ingestion
   validation", a maintainer directive captured as a backlog line) all rotate the same way.
   The #495 miss (a prose-named item closed without rotation, the old `FR-N`/`§`-keyed
   reflex skipping it) is why this is spelled out; the D5 PR-time check now detects the
   `FR-N CLOSED` and prose `clos... the ... item/directive` closure forms too, not only
   `clos... TODO §`.

This is the project-specific routine that promotes "merge my own green PR" into the
safe set per user-level Rule 8 point 1. Actions outside this routine (merging a PR
the maintainer did not author, force-pushing a protected branch, deleting a branch
the assistant did not create) require explicit confirmation under the
confirm-before-destructive-action discipline.

## Session migration and PR close-out checklist

Long sessions degrade (context dilution, lossy compaction, state drift, error
compounding), and the assistant has no reliable internal gauge of this, so the defence
is external. Two mechanisms:

1. **Session handoff.** [`.working/session-handoff.md`](../.working/session-handoff.md)
   is the single resume point for a new session: branch, versions, counts, last-merged
   PRs, trust-recovery state, the next-actions queue, open decisions, the standing
   disciplines, the **green-at-`<sha>`** mechanical baseline, and (at session close) the
   **asserted-expectations** section the receiving `/resume` `/validate` cross-checks
   against. It is refreshed at every PR close-out (as part of the recursion-avoidance
   batch). To resume, the maintainer sends only `/resume` (the
   [`commands/resume.md`](commands/resume.md) command), which reads the handoff, verifies
   the snapshot against live files, and continues from the queue. Prefer starting a fresh
   session at batch boundaries over running a long one.

2. **PR close-out checklist.** Before pushing any PR, confirm every paired bookkeeping
   surface is in the diff (the recurring degradation failure is a correct substantive
   change with a *paired* surface dropped):
   - The prior merged PR's `/validate-pr` history row AND its `/retro` row are both
     present (they batch into this PR per recursion-avoidance).
   - Every TODO item this PR closes is deleted from TODO and added to
     [`.working/DONE.md`](../.working/DONE.md) in the same diff. **Backlog-item-keyed, not
     FR/§-keyed**: a prose-named or maintainer-directed item (not just an `FR-N` or a
     numbered `§N.M`) is a TODO item that rotates the same way (the #495 miss; see
     PR-workflow step 7).
   - If this PR changed an enumerated collection (gates, governance rules, skills), every
     prose count of that collection was checked for staleness (prose counts are not
     gated).
   - [`.working/session-handoff.md`](../.working/session-handoff.md) is refreshed. At a
     session-closing handoff PR, the `## Asserted expectations` section, the
     green-at-`<sha>` snapshot line, and the
     [`.working/session-metrics.md`](../.working/session-metrics.md) row are refreshed too
     (scoped to what this session actually verified; orchestrator main-loop tokens
     recorded as `not instrumented`, never fabricated; never placed in `CHANGELOG.md`).
   - **If this is the first PR of a resumed session** (the `/resume` `/validate`
     close-out), the handoff was **pruned** per its `## Refresh and pruning discipline`:
     keep current + 1 prior in each per-session stack, delete older blocks and superseded
     one-off sections, keep the standing sections in full, and migrate-before-delete any
     un-recorded load-bearing item. See `/resume` command step 6a.
   - If the PR adds or edits **new pack prose** (a SKILL, a rule, a slash command, or new
     prose in the pack README/CLAUDE.md), `tools/lint-language.py` was run on it **before
     the first commit** (new-pack-prose drafting recurrently reintroduces em-dashes and
     British `-ise`).
   - If the PR changed a **convention, count, routing rule, or gate-wiring that is
     restated across surfaces**, the OLD phrasing was grepped across the full changed file
     AND every sibling surface, with zero hits confirmed before commit (the
     multi-surface-incompleteness guard). For a **count, value, or term correction**, the
     contradiction grep is on the BARE token (`grep -nE '\b18\b'`), not a phrasing-specific
     string (`18 spot-scanned`): a phrasing-specific grep misses word-order variants of the
     same stale value on other lines. (PR #443 corrected a count on two lines but its
     phrasing-specific grep missed a third line whose word order differed; a bare-token
     scan would have caught it. See the #443 row in
     [`.working/validate-pr/history.md`](../.working/validate-pr/history.md).)
   - If the PR makes a **corpus-wide completion claim** (a token harmonization, rename, or
     reconcile asserted complete across the corpus), the completion-verification grep was run
     over the **full corpus file set, not the change's own input set**: an input-set grep
     confirms only that *what was touched* is clean, never that *the corpus* is clean, so it
     self-corroborates a file-discovery omission. This is the scope-width companion to the
     bare-token line above (which fixes pattern-width). (PR #455's FR-44 `shall`->`must` sweep
     asserted "0 normative shall remain" from a grep of its own enumerated 17-document input
     set, missing an eligible Policy document that was never in the set; the next session's
     corpus-wide `/validate` (Sweep 75) caught it and #458 fixed it. See the #458 rows in
     [`.working/validate-pr/history.md`](../.working/validate-pr/history.md) and
     [`.working/improvement-log.md`](../.working/improvement-log.md).)
   - `tools/preflight-changelog.py` was run **before the first commit** (as `python3
     tools/preflight-changelog.py && git commit ...`). It gates em/en dashes and unlinked
     path-shaped references in the *added* CHANGELOG lines, exiting non-zero so the `&&`
     chain blocks on a defect. It is an aid, not a new gate; the authoritative gates run
     in CI.
   - **Paired-surface completeness** (the update-one-of-a-pair guard): when a change
     updates one field of a paired structure, the sibling field was updated in the same
     commit. Two recurring instances: (a) if the PR bumps the pack README metadata
     `Version`, the paired `## Version history` table row was added in the same commit;
     (b) when the PR migrates a control code (or any coded value) in a framework-mapping
     or crosswalk table, the paired description cell in the same row was re-read for echoes
     of the OLD code's function or meaning (the prose half is not mechanically gateable,
     so the checklist line is the guard; the worker-brief template carries the migration
     form as DO rail 8 for fan-out workers).
   - **Section-close cross-FILE cleanup** (the §N-orphan guard): when this PR closes a
     numbered TODO §-section (deletes its heading), grep the WHOLE repo for `§N` and
     `PN.M` references to it, not only `TODO.md` siblings. CLAUDE.md and tool docstrings
     are recurring cross-FILE carriers, and each live (non-frozen-`.working`) citer is
     reworded (or has its `§` dropped) in the same PR. The intra-doc-ref gate catches a
     surviving `§N` only INSIDE the same `.md` file; a tool docstring's "queued §N" or a
     CLAUDE.md "queued PN gate" is gate-blind and surfaces only at the next PR's
     `/validate-pr`. (#469's §4.10 close left the `tools/lint-bookkeeping-parity.py`
     docstring stale; #471's §4.6 close left it and a CLAUDE.md line stale; #472 fixed
     both. The intra-TODO-only cleanup of #469 is the evidence the grep must span files.)
     This explicitly includes gate-exempt files carrying a FORWARD `§N` / `PN.M` pointer
     (this file and anything under `.claude/`, plus a tool docstring): a TODO renumber or
     section-close can leave a stale forward pointer in a gate-exempt file, and the
     intra-doc-ref gate does not scan the gate-exempt trees at all, so such a pointer is
     invisible to every gate and is caught only by this whole-repo grep, not by CI
     (Sweep 78 B-1).
   - **Gate-39 count-phrasing** (the P7 trap): when prose in a gate-39-SCANNED surface (a
     tool docstring, a `governance/` spec, `TODO.md`, `README.md`, or any other corpus
     `.md`) cites a gate by its number, phrase it as `gates N and M` (the digits AFTER
     `gates`), never as a two-digit number followed by one short word followed by `gate(s)`.
     Gate 39's P7 pattern reads that run as a stale gate-count claim and fails the build;
     citing two numbered gates in sequence, or a `§<two-digit-section> as gate <M>`
     phrasing, both trip it (#471 amended `TODO.md`, #472 the
     `tools/lint-bookkeeping-parity.py` docstring). The fix is always to put the number
     after `gates` or to drop the adjacency. NOTE: `CHANGELOG.md`, `.claude/`, and
     `.working/` are in gate 39's exempt set (`EXEMPT_FILES` plus `DEFAULT_EXEMPT_DIRS`),
     so the trap does NOT fire there; it is the SCANNED surfaces above that the phrasing
     rule protects (the earlier worry that a CHANGELOG entry could trip it was mistaken).
   - **Audit-gate change completeness** (the gate multi-surface guard): when a PR adds,
     renumbers, or changes the detection logic of an audit gate, every parallel surface is
     updated in the same PR. The four runtime surfaces gate 35 checks (the workflow, the
     runner, the pre-commit config, and the
     [`governance/specification-audit-programme.md`](../governance/specification-audit-programme.md)
     §6 inventory table) are the gated half; the recurring misses are the FREE-PROSE
     surfaces no parity gate inspects: the §6 *detailed-prose* enumeration (the `Gate N is
     a ...` description plus the `Gate N is appended ...` sentence every gate carries), the
     §5 grouped-list, and, when the detection logic changes, the §6 narrative for that gate,
     plus the module docstring and the regression fixture. Gate 35 checks the §6 table and
     gate 39 counts its rows; neither reads the §6 detailed-prose paragraph or the per-gate
     narrative, so those slip (Sweep 77 found gate 57's detailed-prose pair absent after the
     gate shipped in #468; Sweep 38 found gate 48's §6 narrative stale after its logic
     changed in #308 and #309). A PR-only delta check Dn also needs its step name added to
     `WORKFLOW_DELTA_GATE_STEPS`.
   - **Full-file-grep and parallel-case re-verification for prose corrections** (the
     prose-fact completeness guard): when a PR corrects a fact, a count, an overstatement,
     or a stale claim, or rewrites a clause that enumerates parallel cases, grep the FULL
     touched file (every line and string: comments, docstrings, assertion messages, and the
     narrative and currency-summary surfaces, not only the first list or table edited) for
     the offending phrase with zero residual confirmed before commit, and re-verify EVERY
     enumerated parallel case rather than only the one named. This extends the bare-token
     line above from convention and count changes to prose-fact corrections (#340 missed a
     fourth carrier in an assertion-message string) and the corpus-wide-scrub scope to every
     surface of a touched file (#320 edited a framework-list row but missed the same file's
     update-summary narrative bullet; Sweep 41 then found a third carrier in a
     cross-jurisdiction summary row).
   - **Generated-artefact regen order** (the false-clean guard): after any per-document
     `Version` bump, regenerate `taxonomy.yml` FIRST, then `docs/portal.md` and
     `docs/maturity-scorecard.md` (which derive from the taxonomy); a `build-portal.py
     --check` taken before the taxonomy regen completes returns a false-clean against the
     stale taxonomy (the #318 and #323 gate-33 and gate-34 amend loops).
   - CHANGELOG (root + detailed) and version bumps are present; the pre-push guard
     (`run_all_audits.sh` + `run-pr-time-checks.sh`) is green.

   The mechanizable half of QA-cadence enforcement (the former TODO §4.6, closed
   as satisfied in #471) is gate 50's Check 1, which fails when an in-window merged
   PR has no `/validate-pr` plus `/retro` row. The abbreviated-marker half (a row
   that exists but records a sham QA pass) is not mechanizable on free prose, so for
   that residual this checklist plus the `## Throughput pressure does not authorize
   QA abbreviation` section are the convention-level guard.

3. **Closing-handoff-PR discipline (a session's last act is a green merge).** A session
   ends by landing its working-state on `main` as a green, merged PR (the
   *session-closing handoff PR*) so the next session's `/resume` rebuilds state from
   `main` rather than from an unmerged feature branch. This closing PR is the one case
   exempt from the trailing `/validate-pr` + `/retro` (PR-workflow step 5a's handoff-PR
   exception): running them would start a post-merge validate-then-PR loop with no
   terminating next PR at the session boundary. The compensating control is stronger:
   `/resume` runs a full corpus-wide `/validate` as its first task. The closing PR records,
   in the handoff's `## Asserted expectations` section, what this session mechanically
   verified (scoped to touched surfaces) plus the green-at-`<sha>` baseline, which the
   receiving `/validate` cross-checks (a contradiction of a claimed-clean touched surface
   is a genuine miss, escalated). The closing PR's `.working/validate-pr/history.md` row
   records the exemption with the gate-50-recognized marker (`SKIPPED` with `handoff`, or
   `handoff-PR exception`) in its **Findings cell**, never a bare `n/a`: that cell is what
   `tools/lint-bookkeeping-parity.py` reads to classify the row as handoff-exempt, so a
   marker placed only in the Summary cell leaves the row flagged the moment the next PR
   demotes it from highest-numbered (the #445/#450 recurrence; #450 followed the prior
   wording that said "Summary cell", which this PR corrects).

## Multi-session orchestration

For partitionable backlog work, the default first move is to fan out research workers
per the research-assistant discipline, then apply their diffs serially through the
validate-then-apply gate. The full model lives in the runbook
[`.working/multi-session-orchestration.md`](../.working/multi-session-orchestration.md):
the two worker primitives (in-session `Agent` subagent fan-out, available now;
separate-session external-collaborator workers, pending maintainer-provisioned
least-privilege accounts that write to `grc_library_scratch` only), the Model-B
eligibility checklist (what is and is not partitionable), the `grc_library_scratch`
exchange channel and its inbox-not-bypass invariants, and the trust-split `ref/`
reference base (`standards/` trusted, `publications/` screened).

The serial-apply, CI-gating, per-PR `/validate-pr` + `/retro`, and validate-then-apply
invariants are unchanged: parallelism lives only in the research stage, never in the
apply stage, and worker or scratch provenance never reduces the QA a change receives
(there is no trusted-worker fast path). Corpus-wide sweeps, renames, convention
migrations, and the single-file FR-167 matrix are NOT partitionable and stay
single-session. The project-agnostic form is the partitionable-work SOP in the
[`ai-assistant-workflow-disciplines`](rules/governance/ai-assistant-workflow-disciplines.md)
pack rule (its §2).

## Compliance-matrix semantic-fit cadence (`/matrix-fit`)

The compliance matrix ([`compliance/matrix-grc-compliance-alignment.md`](../compliance/matrix-grc-compliance-alignment.md))
and per-document framework-alignment tables carry control-code citations whose
*semantic fit* (is the cited control the right one for the row's document?) the existence
gates 48/49/54 cannot check: a code can exist, be in the right catalogue, and still be the
wrong control. Semantic fit is not mechanically gate-checkable, so the durable instrument
is a cadenced audit, the [`matrix-fit`](../dev-security/claude-rules/skills/matrix-fit/SKILL.md)
skill (slash command `/matrix-fit`): it judges each cited code against the source control
TITLE in the reference base, scoped by the recall-oriented worklist
[`tools/audit-matrix-semantic-fit.py`](../tools/audit-matrix-semantic-fit.py) produces.

Run `/matrix-fit` on this cadence:
1. **After each FR-167 matrix-expansion batch**, over that batch's worklist (the primary
   cadence; the first real firing is FR-167 batch 10, ai).
2. **Once at matrix completion**, over the whole matrix (the closing check).
3. **Ad-hoc** when a control-code citation is in doubt.

It is NOT a gate and NOT a substitute for gates 48/49/54; it is the semantic layer on top
of them (a row must pass the existence gates first). Findings are fixed in-window or routed
under the normal triage; a zero-finding run still gets a history row. This cadence shipped
across two PRs: the PR A advisory tool in #394 and the PR B skill in #399.

## Reference-version currency (scratch `ref/` is storage, upstream is the authority)

The project-specific operationalization of the `evidence-grounded-completion` rule's
external-version-currency corollary, for the scratch `ref/` reference base.

**The check order, whenever an externally-versioned reference (a standard, framework, or
dataset such as MITRE ATT&CK / ATLAS, ISO, CSA, NIST) is load-bearing for a task:**
1. **Find what scratch holds, via its index, not a guess.** Consult the scratch reference
   index ([`grc_library_scratch/ref/INDEX.md`](../../grc_library_scratch/ref/INDEX.md),
   `ref/catalogue.yml`, `ref/SECTION-INDEX.md`, `ref/COVERAGE-MAP.md`) to find the held
   artefact and its recorded version. (MITRE lives under `ref/frameworks/`, not
   `ref/standards/`.)
2. **Validate the current version upstream this turn.** The authoritative answer to "is
   this current?" is the upstream / primary source (the vendor's releases page or
   repository), never the scratch copy, a stored note, or memory. Scratch is
   believed-current STORAGE, not a version authority.
3. **Act only after both.**

**On discovering upstream is newer than scratch holds (the version-update SOP):**
- Updating scratch is part of SOP, via the superseded-archival workflow (download the new
  version into scratch; keep the old but move its files, extracted text plus original, into
  scratch's retained-version store `ref/.superseded/` (bucket-mirrored layout and
  `REGISTER.md` per scratch `CONTRIBUTING.md`); update `catalogue.yml` and the index docs).
  The full workflow lives in the
  [`multi-session-orchestration`](../.working/multi-session-orchestration.md) runbook §6.
- **If the update needs a license or a maintainer download** (cannot be auto-fetched, or
  egress is blocked per the DD-10 known issue), **pause and ask the maintainer.** On no
  response, apply the graceful-degradation default: defer the current item and move on to
  the next independent item (record it in
  [`pending-decisions.md`](../.working/pending-decisions.md)).
- **Never write or rely on a superseded version unless the maintainer explicitly
  authorizes** working from the older one. A register row, a citation, or a mapping must
  carry the upstream-confirmed current version, or the item waits.

Scratch writes go via MCP PR (the local git proxy 403s direct scratch pushes, per
[`third-party-issues.md`](../.working/third-party-issues.md)), so the scratch half of any
update is a separate cross-repo step. The version-currency register is TODO §1.5.

## Attended-autonomous operating mode

Between fully-attended and overnight mode there is a third, default-for-active-sessions
mode: **attended-autonomous**. The maintainer is reachable but not watching every step
(glanceable every 15-20 minutes), and the assistant keeps moving rather than blocking on
each merge or decision. Its three standing rules:

1. **Green CI = merge authority.** When a PR's `Lint markdown corpus` check is green, the
   assistant merges it and proceeds to the next task WITHOUT asking the maintainer to
   authorize the merge; the maintainer redirects by exception. It is NOT overnight mode:
   logging stays normal (per-PR `/validate-pr` + `/retro`, CHANGELOG, handoff), and the
   autonomous-conflict "skip-to-morning" rule does not apply (the maintainer is reachable).

2. **Stricter-is-safer always.** On a cross-value conflict (two documents disagree on a
   number, a control mapping, a regime status), resolve toward the more conservative value
   where one is clearly safer, or toward the external-standard- or
   canonical-internal-source-supported value where one governs; document the choice and
   its evidence. This holds in every mode, not only overnight.

3. **The pending-decisions graceful-degradation mechanism.** When the next action depends
   on a decision that is genuinely the maintainer's (per `clarify-before-acting`), the
   assistant surfaces it with named options AND arms a short timer (default about 2
   minutes; mechanically a background `sleep`). If the maintainer answers before the timer
   fires, act on the answer. If the timer fires with no answer, do NOT stall and do NOT
   guess an authorial decision; take exactly one of two logged paths:
   - **Apply a stricter-safe default** when rule 2 yields a defensible, more-conservative,
     evidence-backed option AND the action is reversible / on-branch. Record it in
     [`.working/pending-decisions.md`](../.working/pending-decisions.md) as "proceeded with
     X (stricter-safe default); confirm or redirect on resume", and continue.
   - **Defer-and-skip** when the decision is genuinely authorial, irreversible, or
     outward-facing, so there is no safe default. Record it as "deferred-blocked: needs
     maintainer", route AROUND it to the next independent task (never guess), and hold any
     task that depends on the deferred decision.
   The reversibility gate from `action-before-explanation-of-inaction` governs which path
   applies: a timeout never auto-proceeds on a destructive or outward-facing action. If
   every remaining task depends on the one pending decision, wrap a clean handoff or idle
   on a longer check-in rather than guessing.

**Mode-exit priority ordering (maintainer-directed 2026-07-02).** When a session switches
AWAY from overnight mode (to attended-autonomous, daytime-unattended, or fully-attended),
the work priority is fixed: (1) **overnight cleanup** first (route and reset
[`.working/overnight-pr.md`](../.working/overnight-pr.md), batch the pending QA rows, fix
what the overnight window's sweeps surfaced); (2) then **fixing of issues**; (3) then
**tooling and protections** (gates, guardrails, machinery); (4) then **new work**. The
ordering is standing; it is not re-asked at each mode exit. (Decision record:
[`.working/design-decisions.md`](../.working/design-decisions.md).)

On `/resume` the assistant reads
[`.working/pending-decisions.md`](../.working/pending-decisions.md) first, surfaces the
still-pending entries (confirming "proceeded" stricter-safe defaults for redirect, asking
"deferred-blocked" questions), and resolves those tasks before the next queued items. In the
same step it reads [`.working/verifier-overrides.md`](../.working/verifier-overrides.md) and
surfaces every `pending` verifier override for maintainer review: an override made in an
unattended run (the orchestrator judged a skeptical-verifier finding a false positive and
proceeded against it) is never silently closed; it is surfaced at the next attended boundary
(end of the unattended run, return to attended mode, or at latest this resume) with the
finding, the overruling reasoning, and the recorded revert path, and the maintainer, not the
assistant, resolves it to `reviewed`.

## Wind-down decision framework (surface the handoff choice, do not take it silently)

**The default is to continue, not to hand off.** Concluding that a session-closing handoff
is the right next step is USUALLY the wrong call: empirically, about 13 of the last 15 times
the assistant proposed a handoff it was not the right decision (maintainer observation,
2026-06-29). A handoff is warranted ONLY on evidence of issues (the trigger below). Session
length, context "heaviness", "this is getting long", and "a large / substantial /
fresh-context-best series remaining" are NOT, by themselves, valid triggers; the assistant
keeps working through them, sustaining quality with skeptical verifier subagents (see the
note in the trigger section) rather than reaching for a handoff. The maintainer is welcome
to be offered a handoff to consider before a substantial, critical, or long piece of work
begins, but that is a non-default SUGGESTION for the maintainer's choice, never the
assistant's default, and absent the maintainer's decision the assistant continues. The one
narrow evidence-grounded exception to "heavy context is never a trigger" is a
run of *expected chained large PRs* for which the project's OWN historical metrics (the
[`hallucination-metrics.md`](../.working/hallucination-metrics.md) and
[`session-metrics.md`](../.working/session-metrics.md) ledgers) show a measured quality
decline on comparable prior runs: that is a NAMED, externally-observable signal (the
metrics), not the un-instrumented "I feel degraded", and it warrants OFFERING the handoff
as a suggestion before the run begins (still the maintainer's choice, still never an
auto-handoff). Context-heaviness with no such metric behind it is not a quasi-trigger; the
assistant keeps working and sustains quality with skeptical verifier subagents. On the
rare occasion a handoff IS warranted (genuine evidence of degradation), taking it silently
is the same failure the `clarify-before-acting` and `action-before-explanation-of-inaction`
rules forbid: narrating an inaction (the handoff) as if forced, without surfacing the
capability assessment that would let the maintainer redirect.

**The trigger.** Whenever the assistant concludes a session-closing handoff is the right
next step, it does NOT act silently. It surfaces the decision (via `AskUserQuestion`) with
all three of:

1. **Its justification** for winding down, stated in objective signals, not a subjective
   "I feel done": actual drift, hallucination, or mistakes the QA layer did not catch (the
   ONLY class of valid trigger). **An un-instrumented internal state is NOT a valid
   justification**, and neither is the *size or shape of the work remaining*. "Context is
   heavy", "this is getting long", "I feel degraded", "a large / substantial /
   fresh-context-best series is next", and "a migration / rename / corpus-wide sweep is
   next" are all INVALID triggers: the first three have no instrument behind them (per the
   `evidence-grounded-completion` un-observable-state corollary), and the rest are
   work-shape, not evidence of a problem. A large series ahead is worked through PR-by-PR
   (each PR is its own focused unit) with skeptical verifier subagents sustaining quality,
   NOT handed off. The trigger must be a NAMED, externally-observable signal of an actual
   problem: a failing check, a `/validate` or `/validate-pr` finding, a maintainer
   correction, or a concrete self-inconsistency that can be quoted. Absent such a signal,
   the default is to continue. **Calibration:** the bar to even *propose* a handoff is high
   (see the intro's empirical observation and its offer-as-non-default note, the single
   source for both); the assistant does not propose a handoff absent the named evidence above.
2. **A per-PR likelihood-of-success assessment** for each of the pending next-five PRs
   (from `TODO.md`), each anchored to objective tractability factors: partitionable vs
   single-session; incremental-edit vs fresh-context-class; count of cross-surface
   bookkeeping touchpoints; unresolved authorial decisions in the way; whether references
   are in hand. These factors inform how to SEQUENCE the next PRs and how heavily to verify
   each (a fresh-context-class PR gets a skeptical verifier subagent, not a handoff); they
   are never themselves a wind-down trigger (the only trigger is the degradation evidence in
   item 1). This assessment is produced only once a handoff has been evidence-triggered, to
   help the maintainer weigh continue-vs-handoff, not to manufacture a handoff from work shape.
3. **Named options** (the `clarify-before-acting` shape, recommended option first):
   - **A. Handoff** (the conservative resolution of this already-evidence-triggered
     decision; NOT the session-level default, which is to continue per the intro above).
   - **B. The assistant's recommended order of additional PRs with high likelihood of
     success** (small, partitionable, low-risk items where objective signals support
     continuing).
   - **C. An alternative order at slightly higher risk.**
   - **D. "Do more than we should."** A deliberate impulse-check for the case where a
     handoff has ALREADY been evidence-triggered and the temptation is to override it and
     push on anyway (this is NOT the ordinary case of continuing a large series, which is
     the correct default): if the maintainer picks D, the assistant reminds the maintainer
     not to be stupid and hands off immediately (a Ulysses pact).

**The timeout (graceful degradation).** This decision uses the same roughly-2-minute
background-`sleep` timer as the attended-autonomous mechanism. If the maintainer answers
before it fires, act on the answer. If it fires with no answer, **proceed with option A
(handoff)**: the conservative, reversible, no-regret resolution of an already-triggered
wind-down decision. (This timeout is reached only once a handoff has been legitimately
triggered by degradation evidence; it is not the session-level default, which is to
continue.) A no-answer timeout NEVER auto-selects B, C, or D. The one carve-out: in an
overnight run the overnight conflict rules govern instead.

**Turning overnight mode OFF is never a no-answer default.** Do NOT end
overnight mode unless the maintainer explicitly says so; if unsure, pause and ask. If the
roughly-2-minute window fires with no answer, **MAINTAIN overnight mode** and re-ask the
next time the maintainer messages. A session-closing handoff silently ends an overnight
run, so the overnight-OFF decision is carved out of the wind-down no-answer-to-handoff
default above: it requires an explicit maintainer signal, never a timeout (the recurrence
the maintainer flagged after the #425 wind-down default ended an overnight run while they
were briefly up).

**Quality > Speed remains the tiebreaker, and B/C are bounded.** Choosing B or C does NOT
relax any discipline: each additional PR still gets its full per-PR `/validate-pr` +
`/retro` (no abbreviation), and the assistant re-runs the degradation read at EACH PR
boundary, so "do N more" is really "do one more, re-assess, repeat" and self-terminates
early if quality signals turn. If a degradation signal appears mid-run, the assistant
winds down regardless of the option chosen, surfacing why.

## Throughput pressure does not authorize QA abbreviation

When a long batch of PRs is in flight, when the session window feels tight, or when the
queue of next-PRs is calling for progress, the assistant does NOT have discretion to
substitute an abbreviated check, a spot-check, a memory-only review, an
orchestrator-self-check, a "quick scan", or any other informal shape for the formal
`/validate-pr` invocation that step 5a mandates, for the formal `/retro` that step 5b
mandates, or for a corpus-wide `/validate` when the sweep cadence calls for one.

"Abbreviated /validate-pr, 0 findings" is NOT a sanctioned shape. The two sanctioned
shapes are (a) the full formal `/validate-pr` dispatch with Subagent A on the diff and a
cross-reference check on touched files, recorded in
[`.working/validate-pr/`](../.working/validate-pr/) and the history row, OR (b) an explicit
maintainer-authorized exception recorded inline in the history row's Summary cell with the
rationale. Anything else is a discipline failure.

The per-PR QA cadence IS the pace of the PR workflow. "I'll catch it on the next one" or
"the validate at the end of the batch will cover this" is the failure mode this rule
prevents (it is what failed when Sweep 22 surfaced four in-window errors across 11 PRs
recorded as "abbreviated spot-check, 0 findings"). If the assistant feels pressure to
abbreviate, the right move is to surface the pressure to the maintainer in one sentence
rather than act on it unilaterally. This is the
[`clarify-before-acting`](rules/governance/clarify-before-acting.md) rule's application to
QA-cadence pressure.

## PR activity subscription discipline

PR workflow step 3 (waiting for CI to settle) and any subsequent wait for review comments
use `mcp__github__subscribe_pr_activity`. Subscriptions deliver failure events, comments,
and reviews into the conversation as they happen, but do not reliably deliver success
transitions or every state change, so a subscription alone can sit indefinitely on a
silent-success event.

The discipline: every `mcp__github__subscribe_pr_activity` call in the same turn arms a
paired 60-second fallback timer via `Bash` with `run_in_background: true`, command shape
`sleep 60 && echo "60s fallback timer fired - check PR #N status"`. When the webhook fires
or the timer completes (whichever comes first), check PR state with
`mcp__github__pull_request_read` (`get_check_runs` for CI, `get_status` for combined commit
status) and act on the actual result. If the PR is still in flight, re-arm a fresh
60-second timer. On merge, the subscription auto-unsubscribes; stop the timer with
`TaskStop` on the background task ID. The 60-second cadence balances latency against API
cost. This operationalizes the webhook-subscriptions discipline in
`.claude/rules/governance/action-before-explanation-of-inaction.md` and the
subscribe-over-poll pattern in `.claude/rules/governance/evidence-grounded-completion.md`.

## Version-bump discipline

The library carries four version-bearing surfaces per document. The rule, one sentence
per surface:

1. **Per-document `Version` field**: bump in the same commit that changes the document's
   body. Every commit. No exceptions. (Gate 40, version-bump-recency, examines
   commit-by-commit history.)
2. **Per-document `Date` field**: bump to today's date (UTC) in the same commit that
   changes the document's body. Every commit. No exceptions. (Gate 31,
   document-date-staleness, fails if the lag exceeds 1 day.) When in doubt, set Date to
   today.
3. **Library CalVer in [`README.md`](../README.md)** (the `Library Version` line, format
   `2026.MM.NNN`): bump once per PR, in the last commit before push.
4. **README `Version` field** (the `Version` line in [`README.md`](../README.md)'s
   metadata block): bump once per PR, in the same commit as the CalVer bump (the two move
   together).

**Enforcement.** The pre-push guard (`tools/pre-push-guard.sh`, PR-workflow step 1) runs
`run_all_audits.sh` (gate 40, plus gate 36 which exercises gates 31/40 in test form) and
`run-pr-time-checks.sh` (D2 per-PR version-bump, D4 per-PR Version-Date co-bump) before
the push, so a missed bump blocks the push instead of flipping CI red. At each commit ask:
did this commit change a versioned document's body (bump its Version AND Date), and is this
the last commit before push (bump library CalVer and the README Version field)?

## Boundaries
- Never hand-edit generated files (`taxonomy.yml`, `docs/portal.md`,
  `docs/maturity-scorecard.md`); regenerate them — CI `--check` fails on drift.
- Never weaken or delete an audit gate to make a document pass; fix the document.
- Never commit secrets or real PII — `lint-secrets-in-content.py` /
  `lint-pii-in-content.py` gate this, and history rewrites are costly.
- Do not push directly to `main`; develop on a branch (rewriting shared history breaks
  open branches and the version-monotonicity audit).
- No exception path is offered for the audit gates or the pack rules under
  `.claude/rules/governance/`. The three pack rules that reference "the project's exception
  register" (`gate-discipline`, `change-tracking`, `evidence-grounded-completion`) find no
  such register in this project: if a gate fails or a rule's protocol cannot be satisfied,
  the artefact is fixed or the PR is descoped. This is the strict-mode stance each pack
  rule's exception section defaults to when no register exists.
- If a protected-branch force-push is ever genuinely necessary (credential leaked into
  history, copyright violation must be expunged, malformed merge corrupted the branch),
  follow the procedure in
  `dev-security/claude-rules/governance/artefact-and-branch-discipline.md`: document the
  technical reason; obtain governance-authority approval; notify collaborators in advance;
  preserve the pre-rewrite ref under
  `refs/preservation/<short-reason>-<YYYY-MM-DD>/<original-ref-name>`; re-run the
  version-monotonicity audit after the rewrite.

## Behavioral rule: clarify before acting
When the request has more than one reasonable interpretation, or an external value (date,
timezone, library version, README version, target branch, whether a change warrants a
CHANGELOG entry, whether to bump per-document versions) is ambiguous, surface the ambiguity
in one sentence and ask before proceeding. Don't silently pick. The authoritative form
lives in `.claude/rules/governance/clarify-before-acting.md` (the pack rule) and as Rule 9
in `~/.claude/CLAUDE.md` (the user-level memory form).

## Communication conventions

These govern how the assistant writes to the maintainer in chat (assistant voice), not corpus prose.

- **No decorative honesty-intensifiers.** Do not preface statements with "honestly", "to be honest", "frankly", "candidly", "in truth", or similar. Every statement the assistant makes is held to the `evidence-grounded-completion` standard without exception, so marking some statements as honest falsely implies a contrast class of statements that are less so. State caveats and self-assessments plainly, without the intensifier.
- **Use `IMPORTANT:` for emphasis.** When a point is significant enough that the maintainer should not skim past it, prefix that paragraph with `IMPORTANT:`. This is the sanctioned emphasis marker. Reserve it for genuinely high-signal points so it does not degrade into noise.
- **"Suggest" and "advise" invite assessment, not just compliance.** When the maintainer prefaces a request with "I suggest", "I advise", or similar, read it as: the maintainer believes this is the right path but is not fully certain and wants the assistant to assess it and give feedback. The assistant's primary function in that case is to help the maintainer reach the best decision, which includes surfacing a better alternative or a concern and pushing back when warranted (the `surface-counterproductive-instructions` discipline), not silently complying. A firm directive with no hedge is followed directly.

## Security and governance requirements
Rules in `.claude/rules/` (sourced from this repo's own `dev-security/claude-rules/` pack,
CC BY-SA 4.0). The rule files are authoritative; the one-line purpose is an index:
- `.claude/rules/secrets.md` — never hardcode credentials (all files).
- `.claude/rules/python.md` — Python patterns for `tools/` audit scripts.
- `.claude/rules/input-validation.md` — input handling for the Markdown-parsing tooling.
- `.claude/rules/cicd-gates.md` — CI/CD pipeline security for `quality.yml`.
- `.claude/rules/governance/gate-discipline.md` — never weaken a gate to silence a failure;
  fix the artefact.
- `.claude/rules/governance/change-tracking.md` — every PR carries a CHANGELOG entry (terse
  or substantive); no skip path; the paired DONE ledger is the at-a-glance index.
- `.claude/rules/governance/evidence-grounded-completion.md` — never claim completion, and
  never assert a property of an artefact you have not read, without running the
  verification protocol first (enumerate, re-read, quote, contradiction-search, distinguish
  mechanical from semantic, state unverified items).
- `.claude/rules/governance/clarify-before-acting.md` — surface ambiguity in one sentence
  and ask before proceeding.
- `.claude/rules/governance/artefact-and-branch-discipline.md` — generated artefacts are
  read-only (edit source, regenerate, commit both halves; CI `--check`); protected branches
  are append-only (no direct push, no force-push, PR-only merges).
- `.claude/rules/governance/action-before-explanation-of-inaction.md` — never explain why
  an external action cannot proceed without first attempting it (when safe and reversible)
  or naming it and asking (when destructive).
- `.claude/rules/governance/validate-inference-before-action.md` — when the next action
  depends on an inferred premise (a state claim not observed this turn), validate via tool
  call before acting (the action-side counterpart of evidence-grounded-completion).
- `.claude/rules/governance/ai-assistant-workflow-disciplines.md` — five disciplines for
  multi-PR work: research-assistant (workers research, orchestrator authors); pipeline
  construction (parallel research, serial apply, CI gating); apply-time worker correction;
  always split when in doubt; background work during CI waits. It also carries the
  **skeptical pre-push verification** standard (a tiered standard layered on the disciplines,
  not a sixth): no standing verifier for quick-fix / bookkeeping changes, one refute-briefed
  verifier subagent pre-push for substantive changes, the full high-assurance harness for
  sensitive changes; a verifier finding is validated then fixed-and-re-verified (three-iter
  cap, then defer to maintainer review); overruling a verifier is never silent (logged with
  the finding, the reasoning, and the revert path in
  [`.working/verifier-overrides.md`](../.working/verifier-overrides.md), surfaced at the next
  attended boundary). This project tracks the
  apply-time-catch vs shipped-escape ratio in
  [`.working/hallucination-metrics.md`](../.working/hallucination-metrics.md) and dispatches
  workers from [`.working/worker-brief-template.md`](../.working/worker-brief-template.md).
- `.claude/rules/governance/trust-recovery-escalation.md` — the escalation tier when
  discipline failures put a maintainer's confidence in a window of work in question: the
  two-skill suite (`/full-qa` forensic pass then `/fitness` persona pass, both via
  `/trust-recovery`), severity-tiered routing (none dropped, apply-time-verified, deduped),
  full-clone methodology, and termination only on explicit maintainer sign-off.
- `.claude/rules/governance/project-integrity.md` — the apex rule: project-agnostic
  distribution of this file's PRIMORDIAL RULE (lexicographic Quality > Speed > Cost; the
  integrity non-negotiables; the self-reminder checkpoints).
- `.claude/rules/governance/surface-counterproductive-instructions.md` — a clear
  instruction is not automatically a correct one; when executing it as given would reduce
  efficiency/effectiveness/productivity, lower quality, destroy done work, contradict a
  stated goal, or rest on a stale-state belief, stop, consider, and surface the concern with
  named options before executing (the charitable-interpretation corollary; the anti-over-ask
  calibration). The requestor-facing counterpart to `clarify-before-acting`.
- `.claude/rules/governance/high-assurance-verification.md` — the heavier pre-apply harness
  for *sensitive* changes (gate-blind on correctness, delicate at scale, costly to get
  wrong): research fan-out, a mechanical signal pass over the negatives, two independent
  adversarial verifiers (false-negative and false-positive lenses), a programmatic invariant
  floor, and a deterministic scripted apply plus re-parse, so apply-correctness does not rest
  on orchestrator in-context precision. The proactive counterpart to
  `trust-recovery-escalation`; its sensitive items persist across sessions in
  [`.working/high-assurance/register.md`](../.working/high-assurance/register.md), surfaced
  at `/resume`.

The `dev-security/claude-rules/README.md` is the authoritative pack version history and
future-work signalling; pack changes are tracked through the library's CHANGELOG and
per-rule version metadata.

The GRC Library pack above is the **primary** source. `.claude/rules/external/` holds a
**supplementary** overlay from third-party sources (TikiTribe, Kariedo, addyosmani — all
MIT, see each dir's LICENSE), provenance-stamped. Overlay rules may overlap or conflict
with the primary layer; the primary GRC pack wins on conflict. The overlay can be pruned
or refreshed independently. addyosmani's content is engineering-workflow skills (TDD, code
review, CI/CD, security-and-hardening, etc.) in Claude Code's `SKILL.md` discovery format;
scope is engineering practice rather than additional GRC governance.
