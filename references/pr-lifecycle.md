# PR lifecycle and close-out (reference)

**Read this at the PR-close-out boundary, like a skill.** `.claude/CLAUDE.md` carries the
lean checklist (each item names its enforcing gate/hook); this file carries the full detail
and rationale. Relocated from CLAUDE.md by TODO 3.139.1 / PR #1249 (roadmap C phase 1) to right-size the
every-turn load; the disciplines are unchanged. Project-only operational machinery (not pack
material). The un-gated grep-disciplines keep a terse reminder in CLAUDE.md as their live
control until the roadmap-C phase-2 delta gate (D9, #1250) lands.

---

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
   commit`).
2. Push with the pre-push guard: `tools/pre-push-guard.sh && git push -u origin
   <branch>`. Run EVERY verification command (the guard, `run_all_audits.sh`,
   `run-pr-time-checks.sh`, the linter-regression runner, a generator `--check`)
   STANDALONE and UNPIPED (never `guard | tail && push`, never `audits | tail`, nor any
   other pipe or truncating sink): a pipe masks the exit code so the dependent action
   proceeds past a failure. When long output must be tamed, use the fail-loud wrapper
   [`tools/tail-safe.sh`](../tools/tail-safe.sh) (preserves the exit code) or redirect to
   a file and read the tail plus a directly-captured `$?`; the PreToolUse hook
   [`.claude/hooks/block-verification-pipes.py`](../.claude/hooks/block-verification-pipes.py)
   refuses the named verification commands piped to truncating sinks (defence in depth,
   not a substitute for the habit). Read the verification's own terminal
   PASS/FAIL line before relying on any chain. On a green guard, open the PR via
   `mcp__github__create_pull_request`.
3. Wait for the `Lint markdown corpus` CI check using the subscription discipline in
   `## PR activity subscription discipline` in `.claude/CLAUDE.md`; on failure, fix and re-push.
4. On green CI, merge via `mcp__github__merge_pull_request` (or `gh pr merge --squash`
   in a no-MCP session). The maintainer does not gate-keep merges of PRs they have
   personally authored.
   **CORRECTED 2026-07-25 (codex deep-assessment M-04): a plain merge attempt does NOT
   resolve `mergeable_state: blocked`.** This file previously claimed it did; that was
   false against the live protection config, which requires one approval, so the plain
   merge fails with `REVIEW_REQUIRED` / "base branch policy prohibits the merge". The
   working path is the maintainer's always-bypass (`gh pr merge --admin`, or the
   equivalent), which the same finding identifies as a governance-enforcement risk
   precisely because it is invisible when used.
   **So every bypass merge is LOGGED.** The maintainer's decision (2026-07-25) is to
   retain the emergency path and make its use auditable rather than remove it. Append
   one row to `grc_library_private/.working/merge-bypass-log.md` for each
   `--admin` merge, recording the PR, the pre-merge CI state, and a one-line
   justification. An unlogged bypass merge is a discipline failure; the log is what
   converts an always-on bypass from an unaudited hole into a recorded exception. If a
   future protection change makes a plain merge succeed, prefer it and stop bypassing.
   **This is now GATED, not merely conventional (gate 50's Check 6, added 2026-07-25).**
   The convention did not hold: five consecutive merges (#1170 to #1174) shipped with no
   row on a single day, noticed only when the log was read for an unrelated reason. The
   check requires a row for every in-window merged PR, exempts the highest-numbered PR as
   in flight, floors the window at the log's own oldest row, and counts a row by its
   PRESENCE whatever its Mechanism cell says, so a future plain merge is recorded honestly
   rather than forced to keep reading `--admin`. Write the row AFTER the merge from the
   OBSERVED CI state, never in anticipation of one.
5. After merge: sync local `main`, delete the feature branch locally, confirm the
   remote branch is gone.
5a. As the PR's FINALIZING QA step, BEFORE merge, invoke `/validate-pr` (dispatches
   Subagent A on THIS PR's own diff plus a cross-reference check on files citing the
   touched files). Records to `grc_library_private/.working/validate-pr/`, and the history
   row records THIS PR's OWN number. The synchronous sequence is: open the PR, wait for the
   first green CI, run `/validate-pr` (then `/retro`, step 5b) against the branch synced to
   current `main`, disposition every finding in-window, write the rows and records, commit
   them into the SAME PR, let CI re-run on the row-carrying commit, then merge (step 4/5).
   No placeholder row and no back-fill into a later PR: the row that records PR N lands IN
   PR N. The prior recursion-avoidance batching is retired; gate 50's Check 1 now requires
   each PR's own rows (window inclusive of `max_pr`) and fails a row that records the QA as
   `DISPATCHED` / `RESULT PENDING` and never `RETURNED`.
   **Read-only-git subagent rule (shared-tree safety):** any subagent this or `/validate`
   dispatches, and any skeptical-verifier subagent, inspects version history READ-ONLY
   (`git show <sha>:<path>`, `git diff`, `git log`) and MUST NOT `git checkout` / `switch`
   / `reset` / `stash` on the shared working tree, because the orchestrator may be on a
   concurrent feature branch. Brief every dispatched subagent
   accordingly; a transient `tests/tmp/*` regression-suite FAIL, or a gate-50 flag for a
   concurrently-in-flight sibling PR whose synchronous rows have not yet merged, is a
   concurrent-run artefact, not a defect.
   Triage findings as in-window (fix in THIS PR before finalizing; a hot-fix PR only if the
   fix genuinely cannot land in-PR) or out-of-window
   (surface to maintainer with named options). **Handoff-PR fallback (loop-termination only):**
   the session-closing handoff PR normally runs its OWN synchronous `/validate-pr` and
   `/retro` like any other PR (the sync model records the rows in-PR, so no recursion
   arises). The documented FALLBACK, retained only for the genuine loop-termination edge
   where the handoff PR's own QA cannot be self-contained within it at the session boundary,
   is to skip the trailing `/validate-pr` / `/retro`; the independent compensating read is
   the next session's `/resume` corpus-wide `/validate`. When the fallback is taken, record
   the exemption in the handoff PR's `grc_library_private/.working/validate-pr/history.md` row **Findings cell**
   (the cell `tools/lint-bookkeeping-parity.py` (gate 50) reads to detect the handoff
   exemption): the marker must be `SKIPPED` together with `handoff`, or the phrase
   `handoff-PR exception`, never a bare `n/a`. Putting the marker in the Summary cell only
   (leaving the Findings cell `n/a`) leaves the row undetected as a handoff: it fails gate 50
   the moment a later PR exists. Fuller
   prose may still go in the Summary cell. (See `## Session migration and PR close-out
   checklist` item 3.)
5b. Immediately after `/validate-pr` returns and BEFORE merge, invoke `/retro` to run the
   retrospective per the
   [`pr-retrospective`](../dev-security/claude-rules/skills/pr-retrospective/SKILL.md)
   skill: append one row to `grc_library_private/.working/improvement-log.md`.
   Pattern and Proposed-improvement entries (if any) surface in chat. The register row lands
   in THIS PR (recording this PR's own number), committed before the PR is finalized; the
   synchronous model retired the recursion-avoidance batching, so the row is never deferred
   to a later PR.
5c. Refresh `grc_library_private/.working/session-handoff.md` with the
   current state snapshot, last-merged list, next-actions queue, and open decisions. The mechanical facts (versions, gate and rule and skill and command counts, HEAD sha, session figures) come from `python3 tools/handoff-snapshot.py`, a read-only aggregator; paste its verified block rather than hand-deriving the numbers. At a
   **session-closing** handoff PR, also refresh the `## Asserted expectations` section
   (the surfaces this session mechanically verified, scoped to what it touched, plus known
   soft spots NOT asserted clean), the **green-at-`<sha>`** snapshot line, and the
   `session-metrics` row (these are the
   loop-break compensating control's cheap signals the next `/resume` `/validate`
   cross-checks against). The refresh commit lands in THIS PR, committed before it is
   finalized (the synchronous model retired the recursion-avoidance batching). See `## Session migration and PR close-out checklist`.
6. After every merge (durable across sessions): consult [`TODO.md`](../TODO.md)'s
   forward-looking sections and list the upcoming next five planned PRs in the chat. If
   new items surfaced during the just-finished work, add them to TODO BEFORE the list is
   published (the list comes from TODO, not from memory). This is the project-specific
   instantiation of the PR finalization protocol in
   [`.claude/rules/governance/change-tracking.md`](../.claude/rules/governance/change-tracking.md).
   **The same next-five list is written to `grc_library_private/.working/next-prs.txt`
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
   (an already-done item still shown as `next:`) is the signal that a PR
   shipped without refreshing it, so every PR touches `next-prs.txt` even when the queue is
   otherwise unchanged.
7. TODO/DONE rotation discipline: when a PR closes a TODO item, the item is deleted from
   TODO in the same PR and an entry is added to `grc_library_private/.working/DONE.md`
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

This is the project-specific routine that promotes "merge my own green PR" into the
safe set per user-level Rule 8 point 1. Actions outside this routine (merging a PR
the maintainer did not author, force-pushing a protected branch, deleting a branch
the assistant did not create) require explicit confirmation under the
confirm-before-destructive-action discipline.

## Session migration and PR close-out checklist

Long sessions degrade (context dilution, lossy compaction, state drift, error
compounding), and the assistant has no reliable internal gauge of this, so the defence
is external. Two mechanisms:

1. **Session handoff.** `grc_library_private/.working/session-handoff.md`
   is the single resume point for a new session: branch, versions, counts, last-merged
   PRs, trust-recovery state, the next-actions queue, open decisions, the standing
   disciplines, the **green-at-`<sha>`** mechanical baseline, and (at session close) the
   **asserted-expectations** section the receiving `/resume` `/validate` cross-checks
   against. It is refreshed at every PR close-out (committed in the same PR, per the synchronous QA model). To resume, the maintainer sends only `/resume` (the
   [`commands/resume.md`](../.claude/commands/resume.md) command), which reads the handoff, verifies
   the snapshot against live files, and continues from the queue. Prefer starting a fresh
   session at batch boundaries over running a long one.

2. **PR close-out checklist.** Before pushing any PR, confirm every paired bookkeeping
   surface is in the diff (the recurring degradation failure is a correct substantive
   change with a *paired* surface dropped):
   - THIS PR's OWN `/validate-pr` history row AND its `/retro` row are both
     present (they land in THIS PR, recording this PR's own number, per the synchronous QA model, rather than being batched forward from the prior PR).
   - Every TODO item this PR closes is deleted from TODO and added to
     `grc_library_private/.working/DONE.md` in the same diff. **Backlog-item-keyed, not
     FR/§-keyed**: a prose-named or maintainer-directed item (not just an `FR-N` or a
     numbered `§N.M`) is a TODO item that rotates the same way.
   - If this PR changed an enumerated collection (gates, governance rules, skills), every
     prose count of that collection was checked for staleness (prose counts are not
     gated). Counts are computed AFTER the verifier loop closes, from the suite run or
     the diff, never during drafting: a count written mid-draft goes stale inside its own
     PR when a later verifier round changes the figure.
   - **If this is the first PR of a resumed session** (the `/resume` `/validate`
     close-out), the handoff was **pruned** per its `## Refresh and pruning discipline`:
     keep current + 1 prior in each per-session stack, delete older blocks and superseded
     one-off sections, keep the standing sections in full, and migrate-before-delete any
     un-recorded load-bearing item. See `/resume` command step 6a.
   - If the PR adds or edits **new pack prose** (a SKILL, a rule, a slash command, or new
     prose in the pack README/CLAUDE.md), `tools/lint-language.py` was run on it **before
     the first commit** (new-pack-prose drafting recurrently reintroduces em-dashes and
     British `-ise`); and because that `lint-language.py` run's fence-aware scan of a
     `.claude/` file can be silently truncated by an unbalanced fence that gate 66
     (`tools/lint-unbalanced-fences.py`) never sees in its default walk (which exempts
     `.claude/`), `tools/lint-unbalanced-fences.py` was run on the SAME explicit paths (it
     accepts explicit path arguments), so an unbalanced fence in that prose is caught
     rather than silently suppressing the language scan's tail.
   - If the PR changed a **convention, count, routing rule, or gate-wiring that is
     restated across surfaces**, the OLD phrasing was grepped across the full changed file
     AND every sibling surface, with zero hits confirmed before commit (the
     multi-surface-incompleteness guard). For a **count, value, or term correction**, the
     contradiction grep is on the BARE token (`grep -nE '\b18\b'`), not a phrasing-specific
     string (`18 spot-scanned`): a phrasing-specific grep misses word-order variants of the
     same stale value on other lines. **Counterpart discipline on the CLAIM side (the #1161
     lesson): bare-token width is right for the SEARCH but wrong for the CLAIM when the token
     is a legitimate substring of real content.** A completion claim must name the SLOT, not
     the string. "No fabricated title survives anywhere in the corpus" was refuted as literally
     stated, because the fabricated phrase `Post-Quantum Cryptography Readiness` is the leading
     substring of the corpus's own document title `Post-Quantum Cryptography Readiness Roadmap`
     and so appears legitimately in eight places; the checkable claim is "no fabricated title
     survives IN A TITLE SLOT for SP 800-208", which is what the corpus's own record said. So
     run the grep at bare-token width, then scope the CLAIM to the slot the token must not
     occupy, because an unscoped claim invites a false refutation from the next verifier who
     runs the same grep and reads the hit count. The same
     bare-token width applies to ENUMERATIONS, not only scalar counts: on a gate-list
     widening, grep both the comma form and the slash form of the old list (`48, 49, 54`
     AND `48/49/54`), since an enumeration is a value that carries its own separators; and it applies to REFUTATION searches, not only correction greps:
     when a verifier or the orchestrator hunts evidence AGAINST a claim, the hunt runs at
     bare-token width too, because a phrasing-specific refutation grep can fail to refute
     a claim that is false in a differently-worded carrier.
   - If the PR makes a **corpus-wide completion claim** (a token harmonization, rename, or
     reconcile asserted complete across the corpus), the completion-verification grep was run
     over the **full corpus file set, not the change's own input set**: an input-set grep
     confirms only that *what was touched* is clean, never that *the corpus* is clean, so it
     self-corroborates a file-discovery omission. This is the scope-width companion to the
     bare-token line above (which fixes pattern-width).
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
     surfaces the parity gates do not check for accuracy: the §5 grouped-list, the per-gate
     §6 narrative when the detection logic changes, the module docstring, and the regression
     fixture (the §6 *detailed-prose* presence pair, the `Gate N is a ...` description plus
     the `Gate N is appended ...` sentence, is now covered by gate 64, so it no longer
     silently slips, though its ACCURACY stays sweep-and-review territory). Gate 35 checks
     the §6 table, gate 39 counts its rows, and gate 64 checks the §6 detailed-prose
     presence; none reads the §5 grouped-list or the per-gate narrative, so those slip (Sweep
     77 found gate 57's detailed-prose pair absent after #468, the seam gate 64 was later
     built to close; Sweep 38 found gate 48's §6 narrative stale after its logic changed in
     #308 and #309). A PR-only delta check Dn also needs its step name added to
     `WORKFLOW_DELTA_GATE_STEPS`. This bullet is the type-A row of the `## Change-impact
     surface map` in `.claude/CLAUDE.md`; see it for the B/C/D change types and the website surface.
   - **Change-impact completeness across all surfaces** (originated in §1.18; the generalization of
     the audit-gate bullet above to every change type): for EVERY gate, pack-rule, skill, or
     count change in the PR, run the `## Change-impact surface map` in `.claude/CLAUDE.md` for that change type
     and confirm each surface, gated AND free-prose AND website, is in the diff. The WEBSITE
     is a first-class paired surface: identify the `grclibrary.ai` (`.web/templates/`) prose
     to update EARLY and apply it in the SAME PR. A rule or skill is linked TWICE in
     `pack.html` (the sidenav AND a body `<li>`), so confirm BOTH; a rule- or skill-COUNT
     change touches the three count surfaces (`pack.html` meta-description, `pack.html` body
     count, `landing.html` pack CTA); a gate change touches NO website surface. The map names
     the covering gate for each gated surface, so this bullet is the free-prose-plus-website
     half the gates do not enforce.
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
     skeptical verifier or the `/validate-pr`, so the recurrence is in the
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
   - **Version-and-Date move together, in the SAME edit** (the D2/D4 pair; three occurrences on
     2026-07-26 alone, past the codification threshold). Every file with a `Version` field also has a
     `Date` field, and the two delta gates check the pair from opposite ends: **D2** fails when a
     file's body changed and its `Version` did not, **D4** fails when a `Version` moved and its `Date`
     did not match the bump commit's UTC date. So touching either half alone fails one of them, and
     the two failures look unrelated in the log while being the same mistake. Bump both in the one
     edit rather than remembering the second afterwards. **Two traps specifically.** A UTC rollover
     mid-PR silently makes every already-correct `Date` stale, so a long session must re-check the
     whole set rather than only the files it just touched. And a LATER commit that moves a `Date` to
     satisfy D4 is itself a body change post-dating the `Version` bump, which then trips gate 40, so
     the repair for a D4 failure is to move the `Version` forward too, not only the `Date`.
     **The practical remedy, adopted after a FIFTH catch in one session: run
     `python3 tools/lint-version-bump-recency.py` immediately BEFORE each commit**, in the same
     `&&` chain as `preflight-changelog.py`. It is seconds, it reads the same committed history
     gate 40 does, and it names the file. The checklist bullet alone did not work, because the
     failure is one of TIMING rather than knowledge: the guard reports it about six minutes into a
     run, long after the edit, and by then the fix costs a whole extra guard cycle. Catching it at
     commit time costs nothing. Note the one wrinkle: the check reads COMMITTED state, so on a
     staged-but-uncommitted bump it still reports the old failure; run it after the commit to
     confirm, or accept that a clean run before the commit means the PREVIOUS commit was clean.
     **MECHANICAL BACKSTOP, maintainer-directed after the fifth catch:**
     [`block-unbumped-version-commit.py`](../.claude/hooks/block-unbumped-version-commit.py), a PreToolUse hook
     that refuses a `git commit` whose staged diff changes a versioned document's BODY without
     staging its `Version`. It reads the staged diff, so its input can answer the question, and it
     fails OPEN on any error. It also WARNS, without blocking, when a corpus `Version` moved and no
     generated artefact is staged. It deliberately does NOT check `Date` against the commit date
     (delta gate D4 owns that, and the commit date does not exist yet at PreToolUse time) and skips
     `--amend`. The narrow escape hatch is a `VersionBump: none <reason>` line in the commit
     message, which exists because a guard with no stated exception gets bypassed wholesale the
     first time it is wrong. The convention above remains the primary control; this is defence in
     depth, and it was earned by that convention failing five times in one session.
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
     `grc_library_private/.working/reference-audit/doc-state.md`
     refresh is in the PR's QA batch. An empty candidate set is recorded as the one-line
     steady-state note, not skipped silently. (Convention-guarded; the mechanical
     staleness backstop is a queued TODO item.)
   - **The ROOT CHANGELOG never loses history; it is SUMMARIZED, never removed (maintainer-directed 2026-07-26).** [`CHANGELOG.md`](../CHANGELOG.md) is one of the few history/status files that must go back to the PROJECT START and is NEVER swept, pruned, or moved to `_private`: old per-PR entries are only summarized IN PLACE (daily then weekly roll-ups condense them to `**date | version | PRs #A-#B (N PRs)**` and `**Week of ...**` blocks that STAY in the root). Only the DETAILED mirror (`grc_library_private/.working/changelog-details/`) is swept to `_private`; the root roll-up and the mirror sweep are SEPARATE processes, and no move-to-`_private` process touches the root. The ONLY sanctioned removal from the root is a surgical edit fixing an AI error (for example expunging leaked private info). #1177 wrongly REMOVED six weekly summaries from the root; #1192 restored them, and the D8 reminder plus this rule foreclose the recurrence.
   - **Detailed-mirror current-week sweep** (the changelog-restructure current-week model;
     the pack rule's current-week-model section is the authoritative description): the
     `grc_library_private/.working/changelog-details/CHANGELOG-detailed.md`
     is intended to hold only the CURRENT week's entries, with completed weeks (and, per
     §1.19.9, the aged roll-up ROWS of `validate-pr/history.md` and `improvement-log.md`)
     swept to the `grc_library_private` archive as weekly Monday-dated files by
     a private-side process (the former in-public-repo `sweep-working-records-to-private.py` was
     RETIRED with the working-state move to the private sibling; the detailed mirror now lives in
     `grc_library_private/.working/`, its completed weeks are archived within the private repository,
     and git history retains every entry regardless). Any such archiving is an advisory close-out follow-up,
     NOT a gate: it is cross-repo (neither repo's CI can see the other), the same cross-repo
     shape as the `/validate-pr` sweep and the `audit-brief-freshness.py` advisory
     tool, and the sweep removes tree content only (this
     repo's git history and the grc_library_private archive both retain the full trail, and the `.working/
     export-ignore` in [`.gitattributes`](../.gitattributes) keeps release tarballs fork-clean
     regardless). Gate 59's mirror-header-parity cutoff is the dynamic floor `max(CUTOFF_PR,
     oldest mirror PR)`, so a swept (archive-only) entry is out of parity scope, not
     flagged missing. The write path is unchanged (new entries still prepend to the
     mirror). The initial completed-weeks sweep has already run, so the mirror holds the
     recent (current-week) window rather than the full history (older weeks live in the
     `grc_library_private` archive and in git history); the standing action is the per-PR
     sweep of any newly-completed week at close-out. The compact root-entry format (`**YYYY-MM-DD | X.Y.Z | PR #N** -
     summary`, plain hyphen, no em/en dash) is ADOPTED as the standard go-forward root shape: the
     3b plain-language wave (#855-#862) converted the whole back-catalogue to it, so every new root
     entry uses this one-line form while the detailed mirror keeps the full structured sections.
     TODO 3.16's only remaining residual is the deferred, maintainer-gated git-history collapse.
   - **Daily-changelog-rollup reminder (D8, midnight-UTC cadence).** If the pre-push guard's D8 check prints `DAILY SUMMARY DUE for <date>`, the next PR carries that date's daily roll-up (collapse its per-PR root entries to one `**date | version | PRs #A-#B (N PRs)**` summary) AND prunes the matching detailed-mirror rows to the `grc_library_private/changelog-archive/`. D8 is advisory (exit 0, never blocks), so the reminder is ACTIONED not skipped; the roll-up draft is a small worker offload (`tools/check-daily-changelog-rollup.py` is the check).
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
   `main` rather than from an unmerged feature branch. Under the synchronous QA model this closing PR normally runs its OWN `/validate-pr` +
   `/retro` before it is finalized, like any other PR, with the rows committed inside it (the
   sync model records rows in-PR, so no recursion arises). A documented FALLBACK is retained
   for the one genuine loop-termination edge, a handoff PR whose own QA cannot be
   self-contained within it at the session boundary: in that case only, it skips the trailing
   `/validate-pr` + `/retro`. Independently of the fallback, `/resume` runs a full corpus-wide
   `/validate` as its first task, valuable on its own merits as a fresh-session drift-catch
   (the whole corpus, not one PR's diff) rather than merely compensation for a skip. The closing PR records,
   in the handoff's `## Asserted expectations` section, what this session mechanically
   verified (scoped to touched surfaces) plus the green-at-`<sha>` baseline, which the
   receiving `/validate` cross-checks (a contradiction of a claimed-clean touched surface
   is a genuine miss, escalated). The closing PR's `grc_library_private/.working/validate-pr/history.md` row
   records the exemption with the gate-50-recognized marker (`SKIPPED` with `handoff`, or
   `handoff-PR exception`) in its **Findings cell**, never a bare `n/a`: that cell is what
   `tools/lint-bookkeeping-parity.py` reads to classify the row as handoff-exempt, so a
   marker placed only in the Summary cell leaves the row flagged the moment the next PR
   demotes it from highest-numbered.

   **A SESSION MUST NOT CLOSE WITH A LARGE UNVALIDATED PR (maintainer-directed 2026-07-25).**
   The handoff exemption covers exactly ONE PR, the closing handoff, and only because that PR is
   bookkeeping. It does not extend to the PR before it, and it is not a licence to let the QA
   cadence lapse as a session winds down. **A DISPATCHED ORDER IS WORK ORDERED, NEVER WORK DONE.** Under the synchronous model this is now structural, not merely conventional: a substantive PR cannot be finalized until its own `/validate-pr` has RETURNED and its row is committed in-PR, so "merged with QA still dispatched" is a contradiction the finalizing sequence forecloses. The historical incident below predates that cutover; the discipline it teaches is retained as the reason the cutover exists.

   The 2026-07-25 session closed with #1176 carrying 22 files, 813 insertions, and SIX
   backlog-item closures, its `/validate-pr` merely DISPATCHED: no worker ever claimed the order,
   so the last substantive PR of the session merged unvalidated and six closures went unchecked.
   A wrongly-closed backlog item is invisible afterwards, which is precisely why that PR needed
   the sweep more than most, not less.

   So, before the closing handoff PR is opened:
   - **Every merged PR in the session except the handoff itself has a `/validate-pr` result that
     RETURNED, with its findings dispositioned.** A row reading `DISPATCHED, RESULT PENDING`
     does NOT satisfy this, however honestly it is worded. Honest prose recording an absence is
     the right way to record it and is not a substitute for the thing being absent.
   - **If the order is outstanding, WAIT for it.** If no worker will serve it (no eligible
     claimant, an independence conflict, a stalled fleet), SELF-RUN it inline: on this one
     conflict the mandatory-QA rule outranks the mandatory-offload rule, never the reverse.
     Alert the maintainer and request another worker at the same time, per the
     worker-elasticity corollary, but do not let the ask become the reason the QA never ran.
   - **If it genuinely cannot be run before close, the closing handoff does not go out.** Keep
     the session open, or land the substantive PR's QA as its own PR first. Closing is the
     assistant's choice; closing over an unvalidated substantive PR is not.
   - **Keep the last substantive PR of a session SMALL.** The exposure is the product of the
     PR's size and the chance its QA does not return, so a wind-down is the wrong moment for a
     wide, multi-surface, or closure-bearing change. Sequence those earlier in the session.

   **AN UNDELIVERED `/validate-pr` IS BLOCKING, AND A SLOW WORKER IS RE-ISSUED (maintainer-directed
   2026-07-26).** The rule above says the result must RETURN; this says what to do while it does not.
   An outstanding `/validate-pr` BLOCKS, so it is not something to note and work around. If the
   holding worker has not delivered in a reasonable time, **issue the SAME order to a second worker**
   rather than waiting further, and **accept whichever delivers first** as the authoritative result,
   dispositioning its findings normally. If the slower one then arrives, it is NOT discarded and NOT
   re-adjudicated as a competing verdict: it is read as a CROSS-REFERENCE, purely to check that the
   accepted result missed nothing. A finding present only in the late delivery is triaged on its own
   merits; agreement between the two is corroboration and is worth recording as such.

   Two properties make this safe rather than wasteful. Duplicating a READ-ONLY QA order costs a
   worker cycle and nothing else, since neither worker writes to the repository. And it converts a
   stalled order from an indefinite block into a bounded one, which matters because the whole failure
   this section exists to prevent is a QA order that quietly never runs. Where the two workers are
   independent of each other, the second reading is a genuine second lens and the corroboration is
   worth more than the time it cost.

   **The mechanical half is now BUILT (PR #1248).** Gate 50's Check 1 no longer exempts
   the highest-numbered PR (its window is inclusive of `max_pr`, since the synchronous QA lands
   each PR's rows in the PR itself) and it classifies a THIRD row state, a validate-pr row that
   is PRESENT but records the QA as `DISPATCHED` / `RESULT PENDING` and never `RETURNED`, as a
   FAILURE on any in-window PR. So an honest `DISPATCHED, RESULT PENDING` row no longer reads
   GREEN: the parity gate fails until the QA has RETURNED and its row records that, which the
   synchronous model requires before the PR is finalized. (Sweep 122 Part 3 identified the old
   presence-only hole from the gate's own contract; the pending-row state follows the precedent
   of the two exemptions Check 1 already detects mechanically, one by exactly this kind of
   Findings-cell marker.) This convention is now the defence-in-depth PARTNER of a live gate,
   not the sole control, which is the stronger half of the pair.
