# CLAUDE.md

> **Condense note (PR #441):** this file was condensed per the maintainer's "keep
> actionable rules, cut rationale/war-stories/duplication" directive (Option B). Every
> rule and procedure step is retained; the removed rationale, war-stories, and provenance
> are preserved verbatim with analysis in
> [`.working/claude-md-considerations.md`](../.working/claude-md-considerations.md), which
> is reviewed each `/retro` and the periodic hallucination-metrics pass so a removal can be
> restored if its "evidence the removal was wrong" signal appears.

## PRIMORDIAL RULE: PROJECT INTEGRITY, THE AIQT PRINCIPLE (HIGHEST PRECEDENCE)

This rule has the highest precedence in this project. It sits above every other section of this file and above the user-level / project-layer reconciliation note immediately below it: that note governs *which rule source wins* on a rule-source conflict; this rule governs *which optimization dimension wins* on an AIQT-tier / speed / cost conflict. The two are complementary, not competing.

**The AIQT Principle, the priority ordering: (Accuracy = Integrity = Quality = Trust) > Speed > Cost.** The four facets (Accuracy: every claim matches its source and every state assertion rests on an observation; Integrity: no stubbing, suppression, fabrication, or silent change; Quality: the project's standard of craft, complete across every paired surface; Trust: warranted by the record and granted by the maintainer, never claimed by the assistant) form ONE non-negotiable top tier with no internal ranking among them; the tier is lexicographically above Speed, and Speed above Cost. A conflict among the four is a framing defect to surface, not a priority call. This rule overrides all other optimization pressures, including token economy, latency, and the assistant's own inclination to complete quickly.

### 1. Priority enforcement
- Nothing on the AIQT tier is ever traded for speed; speed is never traded for cost.
- When tiers conflict, the higher tier wins outright. Optimize for cost only after the AIQT tier and speed obligations are fully satisfied.
- "Done faster" or "done cheaper" is never a justification for "done worse".

### 2. Integrity (non-negotiable)
- Correctness over apparent completion. Do not stub, mock, hardcode, or simulate a result to appear finished.
- No silent changes. State every modification. Do not expand scope without instruction.
- No suppression. Do not comment out, weaken, skip, or delete tests, assertions, type checks, linting, audit gates, or error handling to force a pass. (This is the `gate-discipline` pack rule at apex precedence.)
- No fabrication. Do not invent function names, APIs, configuration keys, citations, or behaviour. If unknown, stop and say so. (This is `evidence-grounded-completion` at apex precedence.)
- Failing states are surfaced, never concealed.

### 3. Escalation
If any constraint forces a compromise on the AIQT tier, halt and escalate the tradeoff to the maintainer explicitly. Do not resolve it silently in favour of speed or cost. (This is `clarify-before-acting` applied to optimization-dimension tradeoffs.)

### 4. Self-reminder cadence
The assistant has no internal timer. Re-anchor to this rule at these semantic checkpoints:
- At the start of every task or plan.
- Before `git commit` or any equivalent persistence action.
- Before declaring any task, step, or TODO item complete.
- At every point where the AIQT tier, speed, and cost are in tension.

At each checkpoint, emit one line, then confirm compliance or halt:
`AIQT check: (Accuracy = Integrity = Quality = Trust) > Speed > Cost. Non-negotiable.`

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
   delta gates D1-D8 plus the history-aware trio 45/40/31 against the merge base),
   stopping non-zero on the first failure, so a gate defect blocks the push instead of
   flipping CI red after the fact. The two runners together cover every gate CI runs.
   Git hooks do not fire in this environment, so the `&&`-chained guard is what actually
   enforces the pre-push runner (the same pattern as `preflight-changelog.py && git
   commit`); an "intermediate" push that skips the guard is the momentum-bypass failure
   the guard closes (improvement-log #438/#439).
2. Push with the pre-push guard: `tools/pre-push-guard.sh && git push -u origin
   <branch>`. Run EVERY verification command (the guard, `run_all_audits.sh`,
   `run-pr-time-checks.sh`, the linter-regression runner, a generator `--check`)
   STANDALONE and UNPIPED (never `guard | tail && push`, never `audits | tail`, nor any
   other pipe or truncating sink): a pipe masks the exit code so the dependent action
   proceeds past a failure, the RM-10 failure shape (seven pipe-masked incidents: #569,
   #583, the #608 push, a fourth self-caught before the #615 push, a fifth display-only
   pipe self-caught before the post-#618 branch push, a sixth post-commit
   `run_all_audits | tail` with a pipe-masked exit capture, self-caught in the slice-3
   build, and a seventh post-amend `run_all_audits | tail` self-caught and re-run
   unpiped in the #628 build). When long output must be tamed, use the fail-loud wrapper
   [`tools/tail-safe.sh`](../tools/tail-safe.sh) (preserves the exit code) or redirect to
   a file and read the tail plus a directly-captured `$?`; the PreToolUse hook
   [`.claude/hooks/block-verification-pipes.py`](hooks/block-verification-pipes.py)
   refuses the named verification commands piped to truncating sinks (defence in depth,
   not a substitute for the habit; incident seven ran unblocked in a worker-restarted
   session, the hook-firing limitation later closed as a documented harness limitation in #677). Read the verification's own terminal
   PASS/FAIL line before relying on any chain. On a green guard, open the PR via
   `mcp__github__create_pull_request`.
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
   **Read-only-git subagent rule (shared-tree safety):** any subagent this or `/validate`
   dispatches, and any skeptical-verifier subagent, inspects version history READ-ONLY
   (`git show <sha>:<path>`, `git diff`, `git log`) and MUST NOT `git checkout` / `switch`
   / `reset` / `stash` on the shared working tree, because the orchestrator may be on a
   concurrent feature branch (the #866 collision: a subagent's `git checkout` to judge the
   merge commit switched the orchestrator's branch and mis-branched a commit onto local
   `main`, caught fail-loud at PR-create and repaired). Brief every dispatched subagent
   accordingly; a transient `tests/tmp/*` regression-suite FAIL or a gate-50 flag for a
   not-yet-batched later PR's QA row is a concurrent-run artefact, not a defect. (The pack
   half of this codification landed in the workflow-disciplines rule in #871.)
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
   **The same next-five list is written to [`.working/next-prs.txt`](../.working/next-prs.txt)
   as part of THIS PR's own diff (not a post-merge step), so merging the PR cycles the file,
   and the console `next:` statusline that reads it, forward to the next work item.** Each PR
   drops the item it just closed and reflects the current next-five (drawn from TODO); the
   file is a committed, between-session-durable projection of the queue. **Format
   (maintainer-directed 2026-07-14): the items go on a SINGLE first line
   (`1) ...; 2) ...; 3) ...`), because the console `next:` statusline surfaces ONLY that
   first line and truncates it at roughly 120 characters. Keep the first line to roughly
   120 characters or under, make each item a very brief few-word description (not a full
   sentence), and fit at least three items so the statusline gives a useful "what's next"
   glance. Put any longer detail or the further-out queue on a following `# then:` comment
   line, which the statusline does not surface.** A stale entry there
   (an already-done item still shown as `next:`, the #847-era drift) is the signal that a PR
   shipped without refreshing it, so every PR touches `next-prs.txt` even when the queue is
   otherwise unchanged.
7. TODO/DONE rotation discipline: when a PR closes a TODO item, the item is deleted from
   TODO in the same PR and an entry is added to [`.working/DONE.md`](../.working/DONE.md)
   (the closed-TODO ledger, keyed by PR number with the original backlog ID as a
   cross-reference). The DONE entry names the closed item's number and gives a clean
   one-to-two-sentence summary of what the item was and how it was accomplished, and that
   same summary is surfaced in chat at the moment of completion (in addition to DONE and the
   CHANGELOG), per the change-tracking rule's completion-summary convention. The rotation
   lives in the same commit. TODO holds only
   forward-looking content; historical lists belong in DONE, not in TODO. **"TODO item"
   is backlog-item-keyed, not FR/§-keyed**: a `FR-N` item, a numbered `§N.M` subsection,
   AND a prose-named or maintainer-directed item recorded in TODO (e.g. "OT post-ingestion
   validation", a maintainer directive captured as a backlog line) all rotate the same way.
   The #495 miss (a prose-named item closed without rotation, the old `FR-N`/`§`-keyed
   reflex skipping it) is why this is spelled out; the D5 PR-time check now detects EIGHT
   closure forms (three since the 2026-06-30 broadening, widened to six by #576, to
   seven after the #607 miss, and to eight in #675 for the #637/#640 shapes): (1) the canonical section form
   `clos... TODO §`; (2) the coded-id `XX-N CLOSED` marker (any two-to-four-letter
   uppercase id, e.g. `FR-58 CLOSED` or `GR-13 CLOSED`, widened from the FR-only form by
   GR-13 in #559); (3) the prose `clos... the ... item/directive` form, which also
   matches the `TODO item` and `bullet(s)` nouns with a decimal-dot-tolerant clause run
   (the #595 widening); (4) the section-name closure form (`section-N.M ...
   closed/closure`, hyphenated); (5) the item-number closure form (`items N and M
   closed`); (6) the rotation-assertion form (`rotated to the DONE ledger`, plus the
   guarded short `rotated to DONE` with negations excluded, the #595 widening, plus a
   markdown-linked DONE target for the #640 rotated-to-linked-path shape, added in #675);
   (7) the space-separated `TODO section N.M ... closed/closure` form (case-insensitive,
   forward-only window; the #607 lead's phrasing, which forms 1, 4, and 6 all missed);
   and (8) the bare `TODO N.M ... closed/closure` form (a decimal section token with no
   `section` word and no `§`, case-insensitive, forward-only; the #637 lead's phrasing
   that forms 1 and 7 missed, added in #675).

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
   - **Worker-brief coverage pairing** (the staged-brief sync, TODO section 4.4's
     standing whole-backlog-coverage design): if this PR's diff changes `TODO.md`'s item
     set (adds, closes, renumbers, or materially rescopes an item), the scratch coverage
     sync is queued or done in the same close-out: each NEW item gets a staged brief or
     an eligibility verdict in `grc_library_scratch`'s `research/COVERAGE.md`, each
     consumed work-unit's seed directory is removed at DELIVERY time (the maintainer's
     2026-07-04 delivery-time convention: the whole `research/<work-unit-id>/` directory
     is deleted when the delivery merges scratch-side and the coverage row re-points at
     the inbox delivery path, so a consumed seed is never mistaken for an open one; a
     closed item with no delivery still drops its row at close), and a renumber
     updates the affected rows' section anchors (the stable id is the durable key).
     Briefs are a wipeable derived projection of TODO; TODO wins on any conflict. The
     sync ships as a scratch PR. Advisory instrument (orchestrator-side, not a CI gate,
     because neither repo's CI can see the other):
     [`tools/audit-brief-freshness.py`](../tools/audit-brief-freshness.py) reports the
     index's PRs-behind age, dead brief target paths, and dead coverage-row TODO
     anchors.
   - If this PR changed an enumerated collection (gates, governance rules, skills), every
     prose count of that collection was checked for staleness (prose counts are not
     gated). Counts are computed AFTER the verifier loop closes, from the suite run or
     the diff, never during drafting: a count written mid-draft goes stale inside its own
     PR when a later verifier round changes the figure (the #612 timing rule).
   - [`.working/session-handoff.md`](../.working/session-handoff.md) is refreshed, and the
     refresh RECONCILES rather than appends: re-read the retained tail (the prior blocks'
     queue statements and standing-SOP claims) for directives the new text supersedes and
     mark them historical (the #619 line), and re-read the `Current truth` state-snapshot
     line and reconcile EVERY value on it (merged-through, versions, "rides the next PR"
     claims) to the state the current PR itself produces, since a snapshot refreshed in
     the same diff that falsifies it is the append-not-reconcile shape that fired the
     three-occurrence rule at #628 (#619, #622, #628). The version-token subset of this
     reconcile is now mechanically backstopped by the D7 handoff-snapshot freshness
     PR-time check ([`tools/check-handoff-snapshot-on-pr.py`](../tools/check-handoff-snapshot-on-pr.py)):
     when a PR touches the handoff, D7 fails if any labelled version token on the
     `Current truth` line disagrees with that surface's live header at the PR head, or
     if a surface carries more than one token. The prose halves (the merged-through
     number, the green-at-`<sha>`, the "in flight" branch name, the "rides the next PR"
     annotation) stay convention-guarded here, since D7 is version-tokens-only. At a
     session-closing handoff PR, the `## Asserted expectations` section, the
     green-at-`<sha>` snapshot line, and the
     [`.working/session-metrics.md`](../.working/session-metrics.md) row are refreshed too
     (scoped to what this session actually verified; orchestrator main-loop tokens
     recorded as `not instrumented`, never fabricated; never placed in `CHANGELOG.md`).
   - **Worker-provenance marker** (the gate-50 check-3 convention): if this PR applied a
     scratch-inbox worker delivery, the detailed-mirror CHANGELOG entry carries a
     `**Worker provenance:**` line naming the delivery path (normally
     `inbox/<worker-id>/MANIFEST.md`). Gate 50 validates the marker's shape; whether an
     application is MARKED at all is this checklist line's job (free prose, not
     mechanizable), the same convention-level residual as the QA-abbreviation half.
   - The **session-concurrency lease** [`.working/session-state.md`](../.working/session-state.md)
     heartbeat is re-stamped (`date -u +%Y-%m-%dT%H:%M:%SZ`) in the same refresh batch, and
     its `Current-task` / `Worker-dispatches` lines are updated if stale. Lifecycle:
     ACQUIRE at `/resume` step 0 (branch name, `Status: active`, fresh heartbeat), REFRESH
     at every PR close-out, optionally `Status: winding-down` while the session-closing
     handoff PR is being assembled (gate 63 validates it as a live state; the `/resume`
     step-0 interlock treats it like `active`), RELEASE in the session-closing handoff PR
     (`Status: released`, `Active-session: none`). Gate 63 guards the file's shape; the
     interlock decision is
     `/resume` step 0's (60-minute staleness window, advisory HOLD, git cross-check of
     unmerged `origin/claude/*` siblings). Design record:
     [`.working/design-decisions.md`](../.working/design-decisions.md), "Session-concurrency
     safety".
   - **Sync scratch every PR** (maintainer-directed 2026-07-17; the §3.93 recurrence-prevention).
     Before relying on any credit-offload / scratch state at close-out, `cd` to the
     `grc_library_scratch` checkout and `git fetch origin && git reset --hard origin/main`
     (or read via `git show origin/main:<path>`), **delivery pending or not**, so the
     coordination plane (the `workers/` liveness registry, `queue/`, `results/`) is current at
     every PR boundary. The local scratch checkout does NOT auto-sync, and the
     `credit-offload-queue.py list-workers` / `list-pending` and `results/` reads operate on
     that local checkout, so a worker delivery pushed to scratch `origin/main` is invisible
     until you fetch. Skipping this is the 2026-07-16 / 2026-07-17 stale-scratch-read
     recurrence (a wrong "workers stale / order unclaimed" report from an un-synced checkout
     while a worker had already delivered on `origin/main`). A per-tick fetch is likewise
     mandatory inside any scratch poll loop. Mechanical backstop queued: the queue tool's
     read subcommands auto-fetch origin (§3.93(c), a `grc_library_scratch` PR).
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
     [`.working/validate-pr/history.md`](../.working/validate-pr/history.md).) The same
     bare-token width applies to ENUMERATIONS, not only scalar counts: on a gate-list
     widening, grep both the comma form and the slash form of the old list (`48, 49, 54`
     AND `48/49/54`), since an enumeration is a value that carries its own separators
     (the #614 catch); and it applies to REFUTATION searches, not only correction greps:
     when a verifier or the orchestrator hunts evidence AGAINST a claim, the hunt runs at
     bare-token width too, because a phrasing-specific refutation grep can fail to refute
     a claim that is false in a differently-worded carrier (the #594 extension).
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
   - **Summary/description-lag completeness** (the paired-surface-lag guard; four in-window
     occurrences #650-#653, past the codification threshold): when this PR marks a summary or
     status surface resolved or landed, OR a mid-PR verifier reword changes a term or value on
     a primary surface, update (or grep-confirm clean) the paired detail or description surface
     in the same commit. Convention-level, since the lag is on free prose no gate inspects.
   - **Section-close cross-FILE cleanup** (the §N-orphan guard): when this PR closes a
     numbered TODO §-section (deletes its heading), grep the WHOLE repo for `§N` and
     `PN.M` references to it, AND for the section's BARE tokens (the coded item ids and
     distinctive names the section carried, e.g. `GR-8`, per the bare-token width above;
     the #593 fold), not only `TODO.md` siblings. CLAUDE.md and tool docstrings
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
     (Sweep 78 B-1). **Reference-KEY-WIDTH axis (the §3.46 codification):** the grep
     must cover every KEY FORM the closed thing is cited by, not only the bare `§N`.
     Beyond `§N` / `PN.M` / bare tokens, this includes RANGE notation (`§A-§B`, `§A to
     §B`: a `§1.5-§1.8` residual range stays stale when only its last member closes) and
     the differently-keyed `item N` form a staging or deferred-backlog file uses (e.g. a
     `deferred-protected-changes.md` "item 7" that a TODO §-section points at). A
     bare-`§N` grep misses both, so run the close-out grep over the whole key-form family,
     the reference-key companion to the completion-grep guard's file-type-width axis. This
     class recurred three times in one session (the #814 `§3.36`-vs-`item 7` misname; the
     #817 `§1.5-§1.8` range left stale when #818 closed §1.8; and the #818 CLAUDE.md `§1.8`
     line), each a bare-`§N` grep missing a non-bare key form.
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
     cross-jurisdiction summary row). A third axis on top of pattern width and scope width
     is SEPARATOR TOLERANCE: a completion-claim or contradiction grep must be run in a
     pipe-permitting proximity form (`grep -E 'TOKEN1.{0,80}TOKEN2'`, plus the reversed
     window where token order can vary), never as an adjacent-phrase literal, because a
     table-cell pipe, a parenthesis, or a word-order variant defeats the literal phrase
     while the defect survives (first-commit zero-residual claims were refuted pre-push in
     both #603 and #606; in #606 specifically the adjacent-phrase-literal grep was
     pipe-defeated by table cells and missed four carriers the proximity form caught).
     A fourth axis is FILE-TYPE WIDTH: a rename, cutover, token-migration, or completion
     grep runs over ALL file types the token can inhabit (`.py` tool sources and their
     docstrings, `.yml` workflow and config, `.json`, `.sh`, and the gate-exempt `.claude/`
     and `.working/` trees), not `.md` alone, because the corpus's `.md`-centric grep reflex
     leaves a renamed or retired token live in a tool docstring, a workflow step name, a
     config key, or a CLAUDE.md pointer that no markdown-scoped grep sees (the pattern-width
     and scope-width axes above are both implicitly `.md`-scoped; the #688/#689 log-mining
     retros surfaced this as a distinct gap, and the #746-to-#811 recycled-section-number
     stale CLAUDE.md pointer is the same class). Run the completion or contradiction grep
     with NO `--include=*.md` filter (or explicitly add the non-`.md` types), and confirm
     zero residual across every file type before the completion claim. This is the file-type
     companion to the `## Session migration and PR close-out checklist` §N-orphan-cleanup
     line, which already requires the whole-repo (not just sibling-`.md`) grep on a
     section-close; the axis generalizes it to every rename or completion grep.
   - **Grep-claim fidelity** (the record-vs-output guard): any record or CHANGELOG clause
     that characterizes a grep result (zero residuals, N hits, one legitimate) is written
     FROM the pasted output of that grep at authoring time, never from memory of an
     earlier run (third occurrence made it a pattern: #603, #606, #625). This pairs with
     the separator-tolerance line above, which governs the grep's FORM; this line governs
     the claim's fidelity to what the grep actually returned.
   - **Meta-prose state-claim measurement** (the measured-not-inferred guard): when a
     CHANGELOG, TODO, DONE, or `.working` record clause characterizes an artefact's own state
     (a count, a designation form, a bare-vs-joint distribution, a fixture shape, what a file
     contains or lacks), MEASURE it with a `grep` or a read at authoring time and write the
     clause from that output, never from the mental model. This is the
     `evidence-grounded-completion` read-before-characterizing rule applied at
     BOOKKEEPING-authoring time (as distinct from corpus-authoring time), generalizing the
     Grep-claim-fidelity bullet above from grep-result claims to any artefact-state claim.
     Third-occurrence codification (#662 a currency caveat asserted an unverified year for a
     resolution; #663 a gap bullet asserted "left bare" without measuring the mixed
     bare-and-joint corpus distribution; #664 a CHANGELOG bullet asserted "bare-form fixtures"
     when the fixtures are joint-form): all three were caught in-window by the pre-push
     skeptical verifier or the post-merge `/validate-pr`, so the recurrence is in the
     authoring, not the catching. A recurring sub-shape of this guard (the #630/#631/#633
     count-and-label granularity pattern) is a COUNT stated next to an ENUMERATION at a
     different granularity, or a figure TRANSCRIBED from a subagent's output: recount the
     enumeration in the same edit, state both granularities where a fix-count and a
     location-count diverge, and never transcribe a subagent's figure without recounting it
     against the underlying enumeration (a subagent's arithmetic is a hypothesis, not a
     measurement).
   - **CHANGELOG count-reflex** (the mid-PR figure-drift guard): when a figure in a
     drafted CHANGELOG entry changes during verifier rounds (a findings count, a fixture
     count, a suite size), bare-token grep the WHOLE entry, all sections in both files,
     for the superseded figure before push (the #620 catch: an entry corrected in one
     clause kept the stale figure in another).
   - **Generated-artefact regen order** (the false-clean guard): after any per-document
     `Version` bump, regenerate `taxonomy.yml` FIRST, then `docs/portal.md` and
     `docs/maturity-scorecard.md` (which derive from the taxonomy); a `build-portal.py
     --check` taken before the taxonomy regen completes returns a false-clean against the
     stale taxonomy (the #318 and #323 gate-33 and gate-34 amend loops).
   - **Accepted-unverified tracker** (the evidence-grounded-completion corollary): if this PR
     accepted anything as unverified or unvalidated (proceeded on it, annotated a claim as
     unverified-for-now, or relied on a value not confirmed current), a TODO item tracking its
     verification is in the diff (or already exists and is cross-referenced). The FR-59 Mexico
     and Brazil-citation accepted-unverified trackers (both since primary-verified and closed)
     are the pattern.
   - **Per-touch reference-breadth check** (the `/reference-audit` per-touch obligation):
     if this PR changes a corpus document's body, the per-touch run
     (`python3 tools/audit-reference-breadth.py --docs <touched paths>`, judge on any
     non-empty candidate set, then `--update-state`) is done and the
     [`.working/reference-audit/doc-state.md`](../.working/reference-audit/doc-state.md)
     refresh is in the PR's QA batch. An empty candidate set is recorded as the one-line
     steady-state note, not skipped silently. (Convention-guarded; the mechanical
     staleness backstop is a queued TODO item.)
   - **Detailed-mirror current-week sweep** (the changelog-restructure current-week model;
     the pack rule's current-week-model section is the authoritative description): the in-repo
     [`.working/changelog-details/CHANGELOG-detailed.md`](../.working/changelog-details/CHANGELOG-detailed.md)
     is intended to hold only the CURRENT week's entries, with completed weeks swept to the
     `grc_library_scratch` archive as weekly Monday-dated files by
     [`tools/sweep-working-records-to-scratch.py`](../tools/sweep-working-records-to-scratch.py)
     (data-safe: `--emit-archive <scratch>/archive` to write the archives, then `--prune
     --verify-archived <scratch>/archive` which refuses to remove anything not already
     archived, emit-verify-then-prune). Running the sweep is an advisory close-out follow-up,
     NOT a gate: it is cross-repo (neither repo's CI can see the other), the same cross-repo
     shape as the `/validate-pr` post-merge sweep and the `audit-brief-freshness.py` advisory
     tool, and the sweep removes tree content only (this
     repo's git history and the scratch archive both retain the full trail, and the `.working/
     export-ignore` in [`.gitattributes`](../.gitattributes) keeps release tarballs fork-clean
     regardless). Gate 59's mirror-header-parity cutoff is the dynamic floor `max(CUTOFF_PR,
     oldest in-repo mirror PR)`, so a swept (archive-only) entry is out of parity scope, not
     flagged missing. The write path is unchanged (new entries still prepend to the in-repo
     mirror). The initial completed-weeks sweep has already run, so the mirror holds the
     recent (current-week) window rather than the full history (older weeks live in the
     `grc_library_scratch` archive and in git history); the standing action is the per-PR
     sweep of any newly-completed week at close-out. The compact root-entry format (`**YYYY-MM-DD | X.Y.Z | PR #N** -
     summary`, plain hyphen, no em/en dash) is ADOPTED as the standard go-forward root shape: the
     3b plain-language wave (#855-#862) converted the whole back-catalogue to it, so every new root
     entry uses this one-line form while the detailed mirror keeps the full structured sections.
     TODO 3.16's only remaining residual is the deferred, maintainer-gated git-history collapse.
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
exchange channel and its inbox-not-bypass invariants, and the trust-split
`grc_library_ref` reference base (`standards/` trusted, `publications/` screened).

The serial-apply, CI-gating, per-PR `/validate-pr` + `/retro`, and validate-then-apply
invariants are unchanged: parallelism lives only in the research stage, never in the
apply stage, and worker or scratch provenance never reduces the QA a change receives
(there is no trusted-worker fast path). Corpus-wide sweeps, renames, convention
migrations, and the single-file FR-167 matrix are NOT partitionable and stay
single-session. The project-agnostic form is the partitionable-work SOP in the
[`ai-assistant-workflow-disciplines`](rules/governance/ai-assistant-workflow-disciplines.md)
pack rule (its §2).

**Start-side worker-collision check (the complement to the close-out coverage-pairing
line).** Before starting to build any backlog item, check the scratch `claims-ledger.md`
and `research/COVERAGE.md` for an in-flight claim or a pending inbox delivery covering it:
a claimed or delivered item is apply-work (validate-then-apply on the delivery), not
build-work, so beginning to build it duplicates a worker's effort or collides with a
pending delivery. Nothing else in the queueing flow makes a fresh session look at scratch
before it picks up a TODO item, so this is the start-side of the same loop the close-out
`Worker-brief coverage pairing` checklist line closes at the other end (that line syncs
briefs and verdicts for the item set; this check consults claims and deliveries before
building). It fires not only at `/resume` (whose step-0 sibling-branch cross-check is its
concurrency analogue) but whenever the queue is resumed mid-session and the next item is
picked. The operational form (where to look, what an in-flight claim row versus a delivered
inbox row means) is in the runbook
[`.working/multi-session-orchestration.md`](../.working/multi-session-orchestration.md).
**This check is EXECUTED, not narrated.** Run
`python3 tools/audit-delivery-status.py --item <backlog-id>` (e.g. `--item 3.13`, `--item
FR-60`, `--item SR-3`) and PASTE its output before building any backlog item: a
`DELIVERED ... (apply-work)` result means validate-then-apply on the named delivery, never a
from-scratch build; a `no delivery ... (build-work)` result clears the build. A spoken
conclusion ("no collision, build-work") not backed by the tool's same-turn output is a
discipline failure (the 2026-07-09 recurrence: the check was asserted clear for TODO 3.13
while a `positional-token-lint-313` delivery sat in the inbox and a from-scratch rebuild was
begun; the tool makes the check evidence-producing so a narrated pass is no longer possible).

**Delivery-status-claim discipline (evidence, not memory).** Any assertion about the
delivery pipeline's state, that the backlog is applied / cleared / done, that a specific
delivery is applied, or that an item is blocked / gated, MUST quote the same-turn output of
`python3 tools/audit-delivery-status.py` (the full reconciliation: the PENDING / APPLIED /
UNMAPPED buckets and the review-set count), never a mental model. The tool is advisory
(cross-repo, un-gated, so nothing mechanical forces it); this discipline is the forcing
function, and running it is a standing `/resume` step-3 action alongside
`audit-brief-freshness.py`. A per-item blocking reason (egress-gated, source-gated,
authorial, maintainer-schedule-gated) is recorded PER ITEM against the authoritative
per-item verdict in the scratch `research/COVERAGE.md` and
[`pending-decisions.md`](../.working/pending-decisions.md); it is NEVER generalized across
items from one item's reason (the 2026-07-09 recurrence: about twenty applicable content
deliveries were mislabeled "egress-gated" by generalizing FR-59's blocker, and the backlog
was declared applied; the reconciliation report lists the review set that refutes such a
claim). This is `evidence-grounded-completion` applied to the delivery pipeline: the status
claim is composed FROM the tool's output, not from inference.

## Credit-offload mode

The orchestrator's usage credits are the scarce resource. The token-heavy passes it runs are
of two kinds: the read-only analysis passes (the QA sweeps and the semantic-fit cadences) and
the research/drafting seeds. Both are cleanly detachable from the author-apply-route-merge
critical path, so **credit-offload** moves them onto standing worker sessions on other accounts
(the existing Mode-B research-worker model, generalized to the QA passes), on a polling work
queue with a lease/fencing lifecycle. The design of record is
[`.working/credit-offload-design.md`](../.working/credit-offload-design.md); the coordination
plane and the worker-side protocol live in `grc_library_scratch` (`queue/`, `results/`,
`workers/`, the `tools/credit-offload-queue.py` helper, and the `/credit-offload` worker
command). This section is the ORCHESTRATOR-side discipline.

- **Offloadable (read-only, produces findings/drafts):** `/validate`, `/validate-pr`,
  `/matrix-fit`, `/claim-fit`, `/reference-audit`, `/screen-publications`, `verify`,
  `/fitness`, `/full-qa`, the read-only probe phases of `/deep-assessment`, AND research/draft
  seeds. **Stays orchestrator-side:** authoring corpus prose, applying diffs, routing findings,
  writing the audit-trail rows (a worker cannot write `grc_library`), merging, and the pre-push
  skeptical verifier (it sits on the critical path before push, so offloading it adds a blocking
  wait; kept orchestrator-side pending the periodic reassessment, TODO §3.81).
- **Worker-availability gate (best-effort, never a QA skip).** Before an offloadable pass, read
  the scratch `workers/` liveness registry (`python3 tools/credit-offload-queue.py
  list-workers`). **>= 1 live worker:** enqueue the pass as a queue order pinned to an exact
  `grc_library` SHA and consume its result at the next PR boundary. **0 live workers (or an
  order goes stale unserved):** self-run the pass inline, exactly as before. Offload is pure
  best-effort; the mandatory-QA discipline is UNCHANGED (an offloaded run is the full formal
  pass, abbreviation is never authorized, and an unserved order falls back to a self-run).
- **The blocking resume `/validate`.** The one pass the orchestrator WAITS on is the loop-break
  corpus-wide `/validate` at `/resume` (step 6): when a worker is live it is enqueued as a
  `blocking`, priority-0 order and the orchestrator polls the results plane for the delivery
  before recording the sweep row; with 0 workers it self-runs. Every other offloadable pass
  (per-PR `/validate-pr`, the semantic-fit cadences, research seeds) is NON-blocking, consumed
  at the next PR boundary. **Wind-down pre-positioning (maintainer-directed 2026-07-16).** At
  wind-down the orchestrator ALSO enqueues the corpus-wide `/validate` immediately, pinned to
  the session-closing handoff PR's merge SHA, so a live worker can run it during the
  between-session gap; the next `/resume` then checks the results plane FIRST and consumes a
  delivered result (re-verifying positives per the consume discipline) instead of running the
  sweep fresh, self-running or re-enqueuing only if the result is absent or stale. Strictly
  better than enqueue-at-resume (it uses the idle gap), but best-effort: it pays off only when
  a live worker's `grc_library` clone can fetch the handoff SHA, and `/resume` never records a
  sweep row from a stale or absent result.
- **Consume discipline (trust model).** A worker finding is a hypothesis until the orchestrator
  confirms it: **re-verify every POSITIVE finding at source** before routing (cheap relative to
  the sweep, so the net saving holds), and **trust a clean/zero-finding result** as inline
  subagents are trusted (the result file carries the subagent returns as the proof-of-run). The
  orchestrator, not the worker, writes the `grc_library` audit-trail rows
  (`validate-sweeps/history.md`, `validate-pr/history.md`), because the worker cannot write
  `grc_library`. There is no trusted-worker fast path; worker provenance never reduces the QA a
  change receives.
- **New-worker QA-trust tiers: ELEVATED then routine (maintainer-directed 2026-07-16).** The
  routine consume discipline above (re-verify positives, trust clean-with-proof-of-run) applies
  only AFTER a worker is trust-established. A worker's clean QA result is a trust assertion, and
  trust is session-scoped and instance-scoped, so it is re-established each orchestrator session.
  The window is keyed on **`(worker-id + model)`**: a model change (for example Opus 4.8 to
  Fable 5) RE-TRIGGERS the elevated window for the same worker-id, because a different model has
  different failure modes. It applies to **QA-kind deliveries only** (`/validate`, `/validate-pr`,
  `/matrix-fit`, `/claim-fit`, `/reference-audit`, `/screen-publications`, `verify`, `/fitness`,
  `/full-qa`, read-only `/deep-assessment` phases), where "clean" is a trust assertion; research
  and draft seeds already get full orchestrator re-authoring at apply (the research-assistant
  discipline), so they are outside this window. For the first **2 to 3 QA-kind deliveries** from a
  `(worker + model)` each session, apply **ELEVATED QA** before trusting the result:
  1. **Proof-of-run genuineness:** the result must carry real subagent returns (pre-flight
     counts, per-finding `path:line`, token spend); a bare "clean" with no proof-of-run is a RED
     FLAG, not a pass.
  2. **Independent re-derivation** of everything mechanically derivable (the pinned SHA and delta
     scope, the counts, the gate results, the pre-flight numbers): re-run/re-count yourself and
     confirm they match the worker's claims. This is the strongest guard, since mechanical facts
     cannot be faked.
  3. **Re-verify EVERY finding at source** (not just positives).
  4. **A graduated adversarial auditor:** delivery 1 = a dedicated false-negative auditor subagent
     (hunt for what the worker MISSED, and for sham/scope errors); deliveries 2 to 3 = the above
     three steps without a separate auditor, escalating to a fresh auditor only on a red flag.
  The **2 to 3 count is a floor, not a cap**: it means at least that many CLEAN elevated passes
  before relaxing to routine. Any confirmed miss, sham, or scope error RESETS the window and is
  ESCALATED to the maintainer, and the worker is treated as UNVALIDATED (self-run its passes,
  trust no result) until re-established. Track the per-`(worker + model)` elevated-pass count for
  the session in the session working-state (`session-state.md` Worker-dispatches); it resets each
  session by construction. **Honest limitation:** elevated QA raises the bar but does not
  guarantee detection; a worker fabricating an internally-consistent proof-of-run is a residual
  risk it reduces but cannot eliminate, which is why step 2 (independent re-derivation of
  mechanical facts) is load-bearing. See the design-of-record trust model in
  [`.working/credit-offload-design.md`](../.working/credit-offload-design.md).
- **Honest limitation.** Credit-offload SHIFTS cost across accounts; it does not reduce total
  spend, and the orchestrator still pays to verify positives and to run the pre-push verifier.
  The net saving is real only when the other accounts have spare capacity.
- **Metrics tab (maintainer-directed 2026-07-16).** Maintain the running productivity/savings tab
  [`.working/credit-offload-metrics.md`](../.working/credit-offload-metrics.md): append one row per
  offloaded delivery (order, kind, worker + model, the worker's best-effort estimated token spend as
  a conservative proxy for **estimated orchestrator credits conserved**, the consuming PR, notes) and
  keep the per-session roll-up current. At each MAJOR ACTIVITY, a worker delivering a result and a PR
  finishing, surface a short (a couple of lines) chat tally of the session's passes and estimated
  orchestrator credits conserved. Always label the figure an ESTIMATE (workers cannot read an exact
  in-session count) and carry the shift-not-reduce caveat. There is deliberately NO per-DONE-entry
  line (maintainer choice). The session-closing handoff folds the roll-up into the `session-metrics.md`
  row. Design-of-record: [`.working/credit-offload-design.md`](../.working/credit-offload-design.md)
  `## Metrics and reporting`.
- **Orchestrator coordination-plane reads: fetch scratch FIRST (§3.93).** Every orchestrator
  read of the scratch coordination plane, the `workers/` liveness registry
  (`credit-offload-queue.py list-workers`), the `queue/` (`list-pending` or an order file),
  and `results/`, is preceded by `cd <grc_library_scratch> && git fetch origin && git reset
  --hard origin/main` (or is done via `git show origin/main:<path>`). The local scratch
  checkout does NOT auto-sync, so a working-tree read after no fetch (or a bare fetch) reports
  stale state: a worker delivery pushed to scratch `origin/main` is invisible until you fetch.
  This governs the `/resume` step-3 credit-offload check, the availability gate above, any
  consume, AND a per-tick fetch inside any poll loop. Never characterize worker / queue /
  result state, "workers stale", "order unclaimed", "not delivered", from an un-synced
  checkout (the 2026-07-16 / 2026-07-17 recurrence: a wrong worker-restart ask while a worker
  had already delivered on `origin/main`). The primary standing form is the **sync-scratch-every-PR**
  close-out line in `## Session migration and PR close-out checklist`; the mechanical backstop
  (the queue tool's `list-workers` / `list-pending` auto-fetching origin) is queued as §3.93(c),
  a `grc_library_scratch` PR.
- **Worker read basis.** A worker reads `grc_library` and `grc_library_ref` READ-ONLY at the
  order's pinned SHA via a local worktree cache; on this VM the maintainer maintains
  `/tmp/grc_library_ref` as the worker's ref read copy, so **re-sync `/tmp/grc_library_ref`
  (`rsync -av --delete`, not `-avn`) after any `grc_library_ref` update** or workers read stale
  reference text.
- **Command-count note.** The `/credit-offload` worker command lives in `grc_library_scratch`'s
  `.claude/commands/`, NOT in `grc_library`, so it does NOT change the `grc_library` slash-command
  count (which is 15 as of the §1.19.6 `/adopt` addition); this section adds no user-facing
  count-bearing collection to `grc_library`.

## Compliance-matrix semantic-fit cadence (`/matrix-fit`)

The compliance matrix ([`compliance/matrix-grc-compliance-alignment.md`](../compliance/matrix-grc-compliance-alignment.md))
and per-document framework-alignment tables carry control-code citations whose
*semantic fit* (is the cited control the right one for the row's document?) the existence
gates 48/49/54/58/61 cannot check: a code can exist, be in the right catalogue, and still be the
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

It is NOT a gate and NOT a substitute for gates 48/49/54/58/61; it is the semantic layer on top
of them (a row must pass the existence gates first). Findings are fixed in-window or routed
under the normal triage; a zero-finding run still gets a history row. This cadence shipped
across two PRs: the PR A advisory tool in #394 and the PR B skill in #399.

## Normative-attribution claim-precision cadence (`/claim-fit`)

Corpus documents attribute specific values (a retention period, a clock, a threshold) to
named normative sources. Whether the cited source actually PRESCRIBES the attributed value,
its precision, the citation gates cannot check: the existence, currency, and control-code
gates confirm a source exists and the citation is well-formed, not that the source states the
value. That class, "attributed value, silent source" (the FR-120 shape: a fixed 180-day
baseline attributed to NIST SP 800-53 CA-6 and ISO/IEC 27001 Clause 9.2, neither of which
prescribes a fixed interval), is gate-blind by construction. The durable instrument is a
cadenced audit, the [`claim-fit`](../dev-security/claude-rules/skills/claim-fit/SKILL.md) skill
(slash command `/claim-fit`): it judges each worklisted claim against the held source TEXT in
the reference base (four verdicts: `prescribed`, `informed-not-prescribed`, `mis-attributed`,
`source-not-held`), scoped by the recall-oriented worklist
[`tools/audit-claim-precision.py`](../tools/audit-claim-precision.py) produces.

Run `/claim-fit` on this cadence:
1. **The one-time full Tier-A pass at adoption** (done in #630, establishing the baseline).
2. **After any batch that adds or edits normative-value claims** (a P2 content batch, a
   jurisdiction annex, a KPI or SLA table), judging the new Tier-A rows the batch introduced
   and sampling its Tier-B rows.
3. **Ad-hoc** when a claim is in doubt (a maintainer flag, a `/validate` or `/full-qa` note, an
   apply-time uncertainty about whether a source states a value).

It is NOT a gate and NOT a substitute for the citation gates; it is the precision layer on top
of them (a claim must pass the existence and currency gates first). An
`informed-not-prescribed` finding is fixed by the attribution PHRASING, never the value (the
value is often the corpus's own canonical choice); a `source-not-held` claim routes to the
maintainer's source-drop queue, never adjudicated from memory. Findings are fixed in-window or
routed under the normal triage; a zero-finding run still gets a history row. This cadence
shipped across two PRs: the advisory tool
[`tools/audit-claim-precision.py`](../tools/audit-claim-precision.py) in #621 and the skill
plus the adoption pass in #630.

## Whole-project deep assessment (`/deep-assessment`)

The routine cadence examines changes (per-PR sweeps), recent drift (corpus sweeps), and
named semantic classes (`/matrix-fit`, `/claim-fit`). None of it examines the quality system
itself from outside: the gates check the corpus, the skills check the corpus and the gates'
outputs, and the same assistant lineage that authors the content built the machinery. The
[`deep-assessment`](../dev-security/claude-rules/skills/deep-assessment/SKILL.md) skill (slash
command `/deep-assessment`) is the rare, maintainer-invoked, multi-session instrument for that
residual: a deliberate whole-project pass that runs the existing instruments formally AND
probes what they cannot see, the width of the gates' own detection patterns (via the
[`tools/audit-gate-mutation.py`](../tools/audit-gate-mutation.py) probe and the
[`tools/audit-gate-blindspots.py`](../tools/audit-gate-blindspots.py) blind-spot map), the
semantic accuracy of citations against held source texts, the adoptability of the library by a
fresh reader, the integrity of the delivery pipeline, and the honesty of the QA ledgers. It is
the proactive counterpart to `/trust-recovery`: the trust-recovery suite run at maintainer
direction without a discipline-failure trigger, inheriting that rule's findings-routing (every
confirmed finding routed, tiered by severity, none dropped), apply-time verification, and
maintainer-sign-off-as-the-only-terminal-state conventions.

It is NOT cadenced and NOT self-invoked: it runs only on the maintainer's explicit invocation,
and it terminates only on the maintainer's explicit sign-off (an empty finding set is presented
for sign-off, never self-declared complete). A run spans sessions; its phase state lives in the
durable register [`.working/deep-assessment/register.md`](../.working/deep-assessment/register.md),
and the `/resume` step-7 surfacing of an `in-progress` run keeps a session boundary from
silently truncating the pass. Per-run detail lives beside the register as dated files
(`.working/deep-assessment/YYYY-MM-DD-rN.md`, the fitness-review filename convention); the
register itself is non-dated and stays in-repo. This cadence shipped across two PRs: the two
advisory gate-efficacy tools (`audit-gate-blindspots.py`, `audit-gate-mutation.py`) in #701 and
the skill, command, register, and hooks in #702.

**Coverage obligation (maintainer-directed 2026-07-08).** The skill is count-free and
inventory-deriving: step 1 re-derives the live instrument inventory from the repo at run time,
so the live inventory of quality machinery is the assessment's scope by construction, and any
future quality-check process, tool, gate, skill, or check is included automatically with no
edit to the skill. The obligation runs the other way too: adding a quality-check instrument
carries the duty to keep `/deep-assessment` covering it (a new gate gains a mutation-probe
variant, a new slash-command or skill joins the phase-3 invocation set, a new advisory tool
joins the phase-3 aids).

## Reference-breadth cadence (`/reference-audit`)

The corpus cites what it cites; nothing mechanical asks whether it engages the BEST of
what the project holds. That class, "held but unused" (an authoritative source the
reference base holds that no corpus document engages, and the reverse, a touched
document that newly ingested reference material bears on), is gate-blind by
construction. It was surfaced by the SP 800-154 lesson, where a source relevant to
corpus content went unengaged and turned out to be unavailable (NIST SP 800-154 was
never finalized, a relevant-but-unavailable source rather than a held one). The durable instrument is a cadenced audit, the
[`reference-audit`](../dev-security/claude-rules/skills/reference-audit/SKILL.md) skill
(slash command `/reference-audit`): it judges candidate document-to-source pairings
against the held source TEXT and the live document, scoped by the recall-oriented
worklist [`tools/audit-reference-breadth.py`](../tools/audit-reference-breadth.py)
produces (per-item usage classification plus topic-ranked candidates; curated aliases
in [`tools/reference-breadth-aliases.json`](../tools/reference-breadth-aliases.json)).

Run `/reference-audit` on this cadence:

1. **FULL mode as a `/deep-assessment` member** (the exhaustive both-directions pass),
   and ad-hoc when the maintainer wants the whole picture.
2. **Per-touch mode on every substantive corpus-document PR**: run the tool in
   `--docs` mode for the touched documents. The per-document state file
   [`.working/reference-audit/doc-state.md`](../.working/reference-audit/doc-state.md)
   delta-filters the candidate set to reference items added or updated since the
   document's last audit, so the steady-state cost is near zero; the judge is
   dispatched only on a non-empty candidate set, and `--update-state` refreshes the
   anchor with the PR's QA batch.
3. **New-ingest mode after reference-base changes** (`--ref-since <sha>` or
   `--ref-items <substring>`): judge the corpus documents each changed item topically
   matches and does not cite.

Trust tiers are load-bearing (maintainer decisions, 2026-07-08): standards,
frameworks, legislation, and programs are authoritative (citation-grade improvements);
templates are template-tier (content improvements, never normative citations); books
are recommendation-tier only, never authoritative (corroborate against a trusted
source before anything normative rests on a book-sourced suggestion); publications are
excluded pending the publications-assessment process. It is NOT a gate and NOT a
substitute for the citation gates, `/matrix-fit`, or `/claim-fit`; it is the breadth
layer beside them. Findings are fixed in-window or routed under the normal triage; a
zero-finding or empty-candidate run still gets a history row.

## Publications screening (`/screen-publications`)

The reference base's `publications/` bucket is untrusted by default, and an untrusted
document in an AI's reference context is a trust boundary (bias, factual error, or
prompt-injection content can steer corpus authoring; the OWASP LLM01/LLM05 classes the
corpus's own AI guidance describes). The formal control is the
[`publication-screening`](../dev-security/claude-rules/skills/publication-screening/SKILL.md)
skill (slash command `/screen-publications`): provenance and integrity, the mechanical
instruction-content scan
([`tools/scan-publication-instruction-content.py`](../tools/scan-publication-instruction-content.py)),
corroboration of load-bearing claims against trusted sources, then a per-publication
verdict recorded in the reference base's `publications/SCREENING.md` register, which
the reference-base validation gate enforces (a missing row, an unknown status, or an
orphan row fails it).

Run `/screen-publications` on this cadence:

1. **On every new `publications/` ingest** (the register row ships in the same change
   that catalogues the item).
2. **On the pending backlog** (the screening wave over `pending` rows; partitionable
   worker research applied through validate-then-apply).
3. **Ad-hoc before reliance** on a publication whose row is `pending`, stale, or in
   doubt.

The standing rules: a `pending` publication's content never informs corpus work;
`screened` gates admission to AI context and never upgrades trust (load-bearing claims
are corroborated at use time, and normative claims cite the trusted source);
`quarantined` extracts carry a DO-NOT-USE banner and go to the maintainer;
`discard-candidate` items route to the maintainer, never a silent delete. Honest-backstop framing: the
process raises the bar against poisoned reference input; it does not by itself guarantee
detection. It is NOT a gate and NOT a substitute for use-time corroboration; it is the
admission-control layer for the one untrusted reference bucket. This cadence shipped
across two PRs: the reference-base register + validate check (`grc_library_ref` PR #29)
and the pack skill + `/screen-publications` command + scanner + wiring (this PR).

## Reference-version currency (`grc_library_ref` is storage, upstream is the authority)

The project-specific operationalization of the `evidence-grounded-completion` rule's
external-version-currency corollary, for the `grc_library_ref` reference base.

**`_ref` is a REQUIRED maintainer-orchestrator dependency; its absence fails LOUD (§1.19.7
`_ref`-required gate).** Reference-checking against the held ground truth is critical to
content correctness, so for the maintainer a missing `grc_library_ref` is a broken setup to
FIX, never a state to silently work around. `/resume` step 3 acts on `detect-env`'s
`ref_availability` decision: on `maintainer` identity with `_ref` NOT readable it HALTs and
surfaces the `--add-dir` fix, and no reference-dependent (content) work proceeds until access
is granted and the session re-resumed. The sibling-reaching tools' graceful degradation
(`lint_common.resolve_sibling` no-op, §1.19.2) is ADOPTER-ONLY: an adopter legitimately has no
`_ref` (the committed reference-acquisition manifest + `/adopt` `.ref` bootstrap cover it), so
graceful there is correct, whereas for the maintainer it would mask the missing dependency.

**The check order, whenever an externally-versioned reference (a standard, framework, or
dataset such as MITRE ATT&CK / ATLAS, ISO, CSA, NIST) is load-bearing for a task:**
1. **Find what `grc_library_ref` holds, via its index, not a guess.** Consult the
   `grc_library_ref` reference index
   ([`grc_library_ref/INDEX.md`](../../grc_library_ref/INDEX.md),
   `grc_library_ref/catalogue.yml`, `grc_library_ref/SECTION-INDEX.md`,
   `grc_library_ref/COVERAGE-MAP.md`) to find the held
   artefact and its recorded version. (MITRE lives under `grc_library_ref/frameworks/`, not
   `grc_library_ref/standards/`.) **A held / not-held claim is EXECUTED, not narrated:** run
   `python3 tools/ref-holds.py <query>` and quote its output (HELD with the path, or
   NOT-FOUND-IN-INDEX), never a partial filename grep. A `grep` may FIND a file, but its
   ABSENCE from a partial/filtered grep never proves not-held (the 2026-07-17 recurrence: a
   `grep -rlE '27002' ... | head -1` grabbed a vendor publication and wrongly concluded
   ISO/IEC 27002:2022 was not held, when the index lists it plainly; `ref-holds.py "27002"`
   returns HELD). This is the same executed-not-narrated forcing function as
   `audit-delivery-status.py` for delivery-status claims, and the
   `evidence-grounded-completion` "inventory/absence claims require the index, not a partial
   look" corollary.
2. **Validate the current version upstream this turn.** The authoritative answer to "is
   this current?" is the upstream / primary source (the vendor's releases page or
   repository), never the `grc_library_ref` copy, a stored note, or memory. `grc_library_ref` is
   believed-current STORAGE, not a version authority.
3. **Act only after both.**

**On discovering upstream is newer than `grc_library_ref` holds (the version-update SOP):**
- Updating `grc_library_ref` is part of SOP, via the superseded-archival workflow (download the new
  version into `grc_library_ref`; keep the old but move its files, extracted text plus original, into
  `grc_library_ref`'s retained-version store `grc_library_ref/.superseded/` (bucket-mirrored layout and
  `REGISTER.md` per `grc_library_ref` `CONTRIBUTING.md`); update `catalogue.yml` and the index docs).
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

`grc_library_ref` writes go via PR (the local git proxy 403s direct pushes, per
[`third-party-issues.md`](../.working/third-party-issues.md)), so the `grc_library_ref` half of any
update is a separate cross-repo step. The version-currency register shipped in #505 (the full `needs-reconfirm` sweep ran in #751); the P1 reference-currency residuals (§1.5 through §1.8) are all now closed.

## Missing-reference-document SOP (maintainer-directed 2026-07-12)

When a task needs a reference document that `grc_library_ref` does not hold and that is
load-bearing for the work (a standard, regulation, RTS/ITS, framework, or dataset that a
citation or an attributed normative value depends on), do NOT proceed on the gap and do NOT
merely route it as a `source-not-held` finding. The standing procedure is:

1. **PAUSE** the current task at the point the missing reference is needed.
2. **Attempt to download it** from its authoritative / primary source and **ingest it into
   `grc_library_ref`** via the ingest workflow (drop in `ingest/`, dedupe, identify, route to
   the right bucket, extract to `--full-text.md`, catalogue in `catalogue.yml`, regenerate the
   indexes, run the ref gate; the full workflow is in the
   [`multi-session-orchestration`](../.working/multi-session-orchestration.md) runbook §6 and
   `grc_library_ref` `CONTRIBUTING.md`). Then continue the task against the now-held source.
   (The `grc_library_ref` write is a cross-repo PR per the git-proxy constraint above.)
3. **If the download fails** (egress-blocked per the DD-10 known issue, licensed or paywalled,
   or otherwise unavailable), surface it to the maintainer with named options:
   - **(a)** the maintainer downloads or provides the document (the usual resolution when it is
     licensed or egress-blocked);
   - **(b)** **defer the current task** until the document is ingested (the DEFAULT in unattended
     mode via the roughly-2-minute graceful-degradation timer: record the deferral in
     [`pending-decisions.md`](../.working/pending-decisions.md) as deferred-blocked, route around
     to the next independent item, and hold anything that depends on it);
   - **(c)** something else, for example reword the artefact so it does not depend on the missing
     reference, or cite the source corroboratively-only with an accepted-unverified tracker.

This generalizes the `## Reference-version currency` pause-and-ask clause (which covers the
version-update case) to ANY missing load-bearing reference: routing a `source-not-held` finding
without first attempting the download is the shortcut this SOP forecloses. The project-agnostic
pack distribution of this SOP shipped in the pack's
[`evidence-grounded-completion`](rules/governance/evidence-grounded-completion.md) rule
(the missing-load-bearing-reference corollary in its `## Un-observable state, inventory, and
external-version currency` section; TODO §3.53, 2026-07-12).

## Attended-autonomous operating mode

Between fully-attended and overnight mode there is a third, default-for-active-sessions
mode: **attended-autonomous**. The maintainer is reachable but not watching every step
(glanceable every 15-20 minutes), and the assistant keeps moving rather than blocking on
each merge or decision. Its three standing rules:

1. **Green CI = merge authority.** When a PR's `Lint markdown corpus` check is green, the
   assistant merges it and proceeds to the next task WITHOUT asking the maintainer to
   authorize the merge; the maintainer redirects by exception. The property that
   distinguishes it from overnight mode is the conflict path alone: the "skip-to-morning"
   rule does not apply because the maintainer is reachable and decisions are asked, not
   deferred. Logging is identical in BOTH modes (per-PR `/validate-pr` + `/retro`,
   CHANGELOG, handoff; overnight logging is never abbreviated).

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
   every remaining task depends on the one pending decision, wrap a clean handoff rather
   than guessing (the no-long-interval-check-ins clause in `## PR activity subscription
   discipline` forecloses idling on a deferred check-in).

**Mode-exit priority ordering (maintainer-directed 2026-07-02).** When a session switches
AWAY from overnight mode (to attended-autonomous, daytime-unattended, or fully-attended),
the work priority is fixed: (1) **overnight cleanup** first (route and reset
[`.working/overnight-pr.md`](../.working/overnight-pr.md), batch the pending QA rows, fix
what the overnight window's sweeps surfaced); (2) then **fixing of issues**; (3) then
**tooling and protections** (gates, guardrails, machinery); (4) then **new work**. The
ordering is standing; it is not re-asked at each mode exit. (Decision record:
[`.working/design-decisions.md`](../.working/design-decisions.md).)

**Overnight-to-daytime protected-backlog clearance (maintainer-directed 2026-07-05).** On
switching from overnight to daytime or attended mode, first finish the then-current PR, then
clear the deferred protected-file backlog staged in
[`.working/deferred-protected-changes.md`](../.working/deferred-protected-changes.md) (the
`.claude/` and `dev-security/claude-rules/` pack edits that overnight mode defers because
they need maintainer authorization). During the overnight run, prepare those changes in
advance by drafting their content into that file, so the daytime apply is quick (content
ready, only the authorized apply plus per-PR QA remains).

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

**No idle-stop in unattended mode.** In overnight or any unattended mode, never stop to ask
which authorized item to do next, and never hold or idle on the grounds that remaining work
is substantial, fiddly, higher-risk-this-deep-in-context, or that the clean low-risk queue is
exhausted: these are the invalid triggers the wind-down framework already forbids
(context-heaviness, work-shape, un-instrumented internal state), restated here at the point of
action, because reading them in the wind-down section did not prevent acting against them. The
standing priority ordering already answers what is next; proceed on the highest-priority
authorized independent item with the appropriate skeptical-verifier tier. Stop only for (a) a
genuine named-degradation trigger, or (b) a genuinely authorial decision no standing directive
answers, and even then use the graceful-degradation mechanism (a stricter-safe default, or
defer-and-skip to the next independent item), never a blocking question that idles the run
until the maintainer wakes. Substantial or best-fresh-context work is done PR-by-PR with
skeptical verifiers, never deferred to the maintainer in unattended mode. Two caught pre-push
slips, or any defect the guard or verifier catches before it escapes, are the verification
layer working, not a degradation signal. (Codified after the 2026-07-06 overnight run stopped
to ask the maintainer which authorized P2 item to take, idling the run.)

**Mechanical backstop (never a blocking prompt in unattended mode).** The session's mode is
recorded in the `**Operating-mode:**` field of
[`.working/session-state.md`](../.working/session-state.md) (gate-63-validated:
`fully-attended` / `attended-autonomous` / `overnight-unattended` / `daytime-unattended`), and a
PreToolUse hook [`block-askuserquestion-unattended.py`](hooks/block-askuserquestion-unattended.py)
BLOCKS an `AskUserQuestion` call when the recorded mode is unattended, so a blocking prompt cannot
idle the run. When unattended, record the decision as pending
([`pending-decisions.md`](../.working/pending-decisions.md) or the relevant register) and continue.
Set the field to the true mode at each mode transition; a stale `attended-*` value defeats the hook
(the hook is defence-in-depth, not a substitute for keeping the field current). Motivating
recurrence: the 2026-07-17 r4 deep-assessment Phase-8 sign-off was posed as an `AskUserQuestion`
during overnight mode and idled the run ~7 hours while the work it blocked was already unblocked.

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
assistant's default, and absent the maintainer's decision the assistant continues. Session depth is a
legitimate CONTRIBUTING factor to OFFERING a handoff as a non-default suggestion (that offer
regime, just above, distinct from the evidence-triggered PROPOSAL the trigger section below
governs), one of many potential reasons but NEVER the SOLE reason (maintainer calibration,
2026-07-09): it is weighed alongside other signals, and warrants OFFERING a handoff for the
maintainer's choice (never an auto-handoff) in two named cases. (i) A very-long-run of *expected chained large PRs* ahead,
especially where the project's OWN historical metrics (the
[`hallucination-metrics.md`](../.working/hallucination-metrics.md) and
[`session-metrics.md`](../.working/session-metrics.md) ledgers) show a measured quality
decline on comparable prior runs, a NAMED, externally-observable signal, not the
un-instrumented "I feel degraded". (ii) Excessively-sensitive work whose integrity requires
fresh context with no accumulated session history to skew it, the canonical case being the
first `/deep-assessment` run, which must open on a fresh session so prior findings and
framing do not bias it. Depth ALONE, with no long-run-ahead, no sensitivity reason, and no
metric behind it, is still NOT a trigger: the assistant keeps working and sustains quality
with skeptical verifier subagents. On the
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
   source for both); the assistant does not propose a handoff, concluding it warranted and
   surfacing it as this trigger section describes, absent the named evidence above. The one
   carve-out is OFFERING a handoff as a non-default suggestion in the two contributing-factor
   cases the intro names (a very-long-run-ahead with a measured metric decline, or
   excessively-sensitive fresh-context work): that is the maintainer's call to weigh, not the
   assistant concluding a handoff is warranted, so it does not require the degradation
   evidence a PROPOSAL under this section does.
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

**The AIQT tier above Speed remains the tiebreaker, and B/C are bounded.** Choosing B or C does NOT
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

**No-MCP (gh-CLI) sessions: use `gh pr checks --watch`, bounded and fail-loud, and DO NOT idle
on it.** When the session has no GitHub MCP (`mcp__github__*` absent from the tool list, so the
PR mechanism is the `gh` CLI), there is no `subscribe_pr_activity`. Two failure modes are
FORBIDDEN, both observed 2026-07-12: (a) bare `sleep 60 && echo "check status"` fallback timers,
which pair with a subscription that does not exist and self-check nothing, so they sprawl into
overlapping low-signal waits; and (b) a hand-rolled `until`/`sleep` loop keyed on an unverified
check command, which spins SILENTLY FOREVER if the command errors. (The concrete incident: a
loop used `gh pr checks <N> --json name,bucket`, but `--json` is UNSUPPORTED by `gh pr checks`
in this gh version, so `s=""` every iteration, the `until` condition could never become true,
and the loop ran 30-plus minutes producing nothing while the orchestrator idled on a completion
notification that could never fire.) Instead use the purpose-built, self-bounding primitive
`gh pr checks <N> --watch --interval 30`, run via `Bash` `run_in_background`, wrapped in a hard
`timeout` and made fail-loud so it can NEVER be silent:
`timeout 1200 gh pr checks <N> --watch --interval 30; echo "watch exited rc=$?"; gh pr checks <N>`.
`--watch` exits when the checks finish (rc 0 = all pass, non-zero = failure); the `timeout` caps
the wait at a hard ceiling; the trailing `echo` plus `gh pr checks <N>` print the terminal state
on EVERY exit path (pass, fail, or timeout), so silence is impossible. Run exactly one such task;
stop it with `TaskStop` once settled. **Do NOT idle-block on the notification:** per the
**Background-task check SOP** below, check on the 60-second cadence and ACTIVELY PROBE (`gh pr checks
<N>`, unpiped) once past the check's typical duration (about 1-2 minutes here), because a stuck
or silently-exited wait is indistinguishable from "still running". Never hand-roll a CI-wait
loop on a check command whose flags you have not verified in THIS environment, and never leave a
wait unbounded or silent. (The harness also blocks foreground `sleep N && <cmd>` chains, so the
wait always runs via `run_in_background` or `Monitor`, never a foreground sleep.)

**Background-task check SOP (maintainer-directed 2026-07-02).** The same 60-second
cadence governs EVERY background task (a subagent, a background command, an external
wait), not only PR CI waits: check on every background task every 60 seconds until it
completes, re-arming the timer at each firing. Past the task's typical duration, do not
keep waiting passively for a completion notification; actively probe the task (a
`SendMessage` status check to a subagent, a state read for an external process), because
a background agent can stop silently WITHOUT delivering its result, and the completion
notification alone does not distinguish "still running" from "stalled". The stall tells:
no report past the typical duration, a dangling worktree, or liveness signals that stop
advancing. (Motivating incident: the #582 post-merge sweep agent stalled silently mid-run
and was recovered only when the maintainer prompted an investigation and an
orchestrator status probe followed.)

**No long-interval check-ins (maintainer-directed 2026-07-04).** Never ask for, propose,
or schedule a long-interval self check-in (an hour-out `send_later`, a deferred "I'll
check back later" of any shape), including when a harness or subscription boilerplate
suggests one: the 60-second cadence above IS the check-in mechanism, applied until the
awaited thing finishes or is confirmed looped, dead, or failed. A long-interval timer
adds nothing the 60-second loop does not already cover and costs the maintainer an
approval prompt.

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
  register" (`gate-discipline`, `change-tracking`, `artefact-and-branch-discipline`) find no
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
- **Proactive assessment is standing, not "suggest"-scoped (maintainer-directed 2026-07-02).** Proactively surface a better, more-efficient, or higher-quality alternative, and disagree when a choice looks against the project's best interests, any time you see one, not only when the maintainer says "suggest" or "advise". Surface the disagreement with its reasoning and give the maintainer an opportunity to change their mind; the maintainer retains override. This is the [`surface-counterproductive-instructions`](rules/governance/surface-counterproductive-instructions.md) discipline as a standing default, governed by the AIQT tier > Speed > Cost; its calibration section still applies (the bar is material impact, surfaced once and concisely, and an informed override is final).
- **"Suggest" and "advise" invite assessment, not just compliance.** When the maintainer prefaces a request with "I suggest", "I advise", or similar, read it as: the maintainer believes this is the right path but is not fully certain and wants the assistant to assess it and give feedback. The assistant's primary function in that case is to help the maintainer reach the best decision, which includes surfacing a better alternative or a concern and pushing back when warranted, not silently complying. A firm directive with no hedge is followed directly once any standing-assessment concern (the bullet above) has been surfaced or none exists.

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
  mechanical from semantic, state unverified items). Three corollaries extend it where the
  observation is not a single readable file: un-observable state (context depth, a felt sense
  of doneness) is never assertable and never a wind-down, stop, or defer trigger (that
  requires a named externally-observable signal); inventory, absence, and held-version claims
  need the collection's own index, not a partial look; and external-version currency is
  answered only by the upstream source verified this turn, never a stored note, a cached copy,
  or a local catalogue.
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
  distribution of this file's PRIMORDIAL RULE (the AIQT Principle, (Accuracy = Integrity = Quality = Trust) > Speed > Cost; the
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
- `.claude/rules/governance/session-lifecycle.md` — the session-lifecycle and
  operating-modes discipline for multi-session work: a durable reconciled handoff record,
  explicit operator-set operating modes (fully attended / attended-autonomous with green-CI
  merge authority as the default / unattended with no-idle-stop), graceful degradation for
  blocked operator decisions (an absolute reversibility gate so a timeout never
  auto-executes a destructive action), evidence-gated wind-down (continue is the default),
  the closing green-merge with its loop-break compensating control, and an advisory
  concurrency lease. The project-agnostic distillation of this file's own attended-autonomous,
  wind-down, session-migration/close-out, and concurrency-lease sections plus the `/resume`
  interlock; those sections remain here as the project-specific operationalization (concrete
  files, the timer value, the mode-exit ordering).

The `dev-security/claude-rules/README.md` is the authoritative pack version history and
future-work signalling; pack changes are tracked through the library's CHANGELOG and
per-rule version metadata.

**PROJECT-OVERLAY convention (the `.claude/rules/` copies).** A `.claude/rules/` rule
copy may carry ONE trailing block starting with the marker line
`<!-- PROJECT-OVERLAY: not part of the distributable pack -->`: THIS PROJECT'S
operational content (concrete register paths, slash commands, gate numbers, relocated
lineage). An overlay block lives ONLY in a `.claude/rules/` copy and NEVER in a
`dev-security/claude-rules/` pack file; gate 37 strips the block before comparing the
pair and mechanically fails if the marker appears in a mapped pack source (an overlay
leak into the distributable). The pack is complete and fully usable without any
overlay; a fork adopter may delete or replace overlay blocks freely. An assistant
editing a rule edits the pack body (both trees, same commit) for portable discipline
and the overlay (local copy only) for project wiring; the two are never mixed. This is
distinct from the third-party external overlay described next.

The GRC Library pack above is the **primary** source. `.claude/rules/external/` holds a
**supplementary** overlay from third-party sources (TikiTribe, Kariedo, addyosmani — all
MIT, see each dir's LICENSE), provenance-stamped. Overlay rules may overlap or conflict
with the primary layer; the primary GRC pack wins on conflict. The overlay can be pruned
or refreshed independently: the pruning stance is that the overlay is reviewed at each
periodic pack review, a near-duplicate wrapper the primary pack already covers is a prune
candidate, and a stale upstream file is refreshed from source or dropped rather than left
to diverge. Each overlay directory carries a `PROVENANCE.md` recording this precedence and
pruning stance beside its `LICENSE`. addyosmani's content is engineering-workflow skills (TDD, code
review, CI/CD, security-and-hardening, etc.) in Claude Code's `SKILL.md` discovery format;
scope is engineering practice rather than additional GRC governance.
