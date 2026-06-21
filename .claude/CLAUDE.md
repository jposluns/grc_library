# CLAUDE.md

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
corpus internally consistent. There is no application runtime — the deliverable is the
documents and the linters that govern them.
- Documents live in domain dirs: `ai/` `architecture/` `compliance/` `dev-security/`
  `governance/` `operations/` `privacy/` `resilience/` `risk/` `security/`
  `supply-chain/`.
- Audit/build tooling lives in `tools/` as `lint-*.py` and `build-*.py` scripts;
  shared helpers in `tools/lint_common.py`. Tests in `tests/`. Exact counts drift as
  gates are added; the source of truth for the current set is
  `tools/run_all_audits.sh` and `.github/workflows/quality.yml`.
- `taxonomy.yml`, `docs/portal.md`, and `docs/maturity-scorecard.md` are generated
  from document metadata — never hand-edit generated files; regenerate via
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
`tools/run_all_audits.sh`, and `.pre-commit-config.yaml` in lock-step — a gate added to
one must be added to all (the gate-parity audit enforces this).

## Structure
- `tools/lint_common.py` — shared file discovery, exemption sets, helpers.
- A new audit = a `tools/lint-*.py` + wiring in all four surfaces (workflow, runner,
  pre-commit, audit-programme spec) + a regression fixture.
- Exempt dirs are defined in `tools/lint_common.py` as `DEFAULT_EXEMPT_DIRS`
  (`.git`, `node_modules`, `__pycache__`, `.claude`, `.working`); individual linters add
  their own per-tool exempt prefixes on top (e.g. `dev-security/claude-rules/`,
  `tools/`, `docs/` carve-outs) — consult each `lint-*.py` for its specific set
  rather than treating the common set as the full list.
- `.working/` — maintainer working space holding per-run records from `/validate`,
  `/fitness`, and other maintainer-invoked activities. The contents are
  frozen-state archives (cross-references accurate as-of write-time, not maintained
  against subsequent corpus changes), exempt from corpus audit gates, and not
  intended for adopter consumption. See [`.working/README.md`](../.working/README.md)
  for the convention and subdirectory inventory. Adopters cloning the library can
  delete `.working/` outright or keep it as historical reference; either is fine.

## Conventions
- Mirror an existing same-type document's metadata and section shape rather than
  inventing one; changing the model means changing the linters that enforce it.
- External-standard citations must be accurate and current — `lint-citations.py` and
  `lint-standards-currency.py` reject hallucinated or stale references.
- Prose style is enforced by `lint-language.py`; do not fight the linter by hand.

## Language convention
The library uses **Canadian English first, Commonwealth (UK / Australian) English
second, other dialects last.** Canadian English shares its `-ize` / `-ization`
orthography with American English (an inheritance from the Oxford convention adopted
in Canadian usage), so the `-ize` rule that `tools/lint-language.py` enforces is the
Canadian-orthography manifestation of the convention, not a generic American mandate.
Where Canadian English has no opinion (vocabulary or grammar features that vary across
other English dialects), Commonwealth forms are preferred; where neither has an
opinion, other dialects' usage is acceptable. Em-dashes (`—`) and en-dashes (`–`) are
forbidden in prose regardless of dialect; use commas, colons, or parentheses.

## Testing
- A change is green only when `tools/run_all_audits.sh` reports all gates passing.
- Add a regression fixture in `tests/` (see `tests/README.md`) for any new linter.

## PR workflow
PRs in this repository follow a fixed pattern that the assistant is authorised to
drive end-to-end on the maintainer's behalf:

1. Develop on a named feature branch (never on `main`); confirm
   `tools/run_all_audits.sh` passes standalone **after each commit** on the
   feature branch, not only before the final push. Git-history-aware gates
   (gate 40 in this project, plus any future gate that examines commit
   graph) only see committed state, so running the audit on the working
   tree before committing misses what would happen post-commit. Running
   between commits catches gate 40-class issues locally, before CI does.
   Before pushing, additionally run `tools/run-pr-time-checks.sh` to
   exercise the PR-only delta gates (D1 CHANGELOG-on-PR, D2 per-PR
   version-bump) plus gate 45 (TODO staleness) locally — these gates
   need a git history range relative to the merge base and are
   therefore not part of `run_all_audits.sh`. The two runners together
   cover every gate the CI workflow runs.
2. Push with `git push -u origin <branch>` and open the PR via
   `mcp__github__create_pull_request`.
3. Wait for the `Lint markdown corpus` CI check; on failure, fix and re-push.
4. On green CI, merge via `mcp__github__merge_pull_request`. The maintainer does not
   gate-keep merges of PRs they have personally authored. `mergeable_state: blocked`
   is the branch-protection state immediately before merge, not a human-review gate;
   the merge attempt resolves it.
5. After merge: sync local `main`, delete the feature branch locally, confirm the
   remote branch is gone.
6. After every merge (this step is durable across sessions): consult
   [`TODO.md`](../TODO.md)'s forward-looking sections and list the upcoming next
   five planned PRs in the chat. If new items have surfaced during the just-
   finished work (proposals from the maintainer, new follow-ups from the PR's
   own findings, design questions deferred), add them to TODO BEFORE the list
   is published — the list comes from TODO, not from memory. This is the
   project-specific instantiation of the PR finalization protocol in
   [`.claude/rules/governance/change-tracking.md`](../.claude/rules/governance/change-tracking.md);
   it makes the queue auditable and gives the maintainer a redirect point
   before the next PR's work begins.
7. TODO/DONE rotation discipline: when a PR closes a TODO item, the item is
   deleted from TODO in the same PR and an entry is added to
   [`.working/DONE.md`](../.working/DONE.md) (the closed-TODO ledger, keyed by
   PR number with the original backlog ID as a cross-reference). The rotation
   lives in the same commit so reviewers see it in one place. TODO holds only
   forward-looking content; historical "PRs completed" lists, "design
   decisions made this session" subsections, or "recently shipped" annotations
   belong in DONE, not in TODO. See the change-tracking pack rule's PR
   finalization protocol section for the project-agnostic discipline.

This is the project-specific routine that promotes "merge my own green PR" into the
safe set per user-level Rule 8 point 1. Actions outside this routine (merging a PR
the maintainer did not author, force-pushing a protected branch, deleting a branch
the assistant did not create) are not in the safe set and require explicit
confirmation under the confirm-before-destructive-action discipline.

## Version-bump discipline

The library carries three version surfaces, and recurring CI failures (most
recently PR #169's gate 40 catch) trace back to losing track of which surface
bumps when across a multi-commit PR. The rule, one sentence per surface:

1. **Per-document `Version` field**: bump in the same commit that changes the
   document's body. Every commit. No exceptions. Gate 40 (corpus
   version-bump-recency) examines commit-by-commit history, so a body change
   without a version bump in the same commit fails the gate even when the final
   state of the branch looks correct.
2. **Library CalVer in [`README.md`](../README.md)** (the `Library Version`
   line, format `2026.MM.NNN`): bump once per PR, in the last commit before
   push. Bumping CalVer in every intermediate commit creates needless churn;
   bumping only in the last commit keeps the value consumers see aligned with
   what actually ships.
3. **README `Version` field** (the `Version` line in [`README.md`](../README.md)'s
   metadata block): bump once per PR, in the same commit as the CalVer bump.
   The two are conceptually paired (the README *is* the library's version
   statement), so they move together.

**Operationalization**: at each commit, ask three questions:
1. Did this commit change a versioned document's body? → Bump that document's
   Version in this commit.
2. Is this the last commit before push? → Bump library CalVer in
   [`README.md`](../README.md) and the README's own Version field in the same
   commit.
3. Did `tools/run_all_audits.sh` pass after this commit? → If not, fix before
   pushing. Gate 36 (linter regression) exercises gate 40's logic in test form
   and catches the per-document-bump omission locally before CI does.

The post-commit `run_all_audits.sh` discipline (already specified in `## PR
workflow` step 1) is the catch-net for this rule: if the three questions are
asked and the audit passes, the rule has held.

## Boundaries
- Never hand-edit generated files (`taxonomy.yml`, `docs/portal.md`,
  `docs/maturity-scorecard.md`); regenerate them — CI `--check` fails on drift.
- Never weaken or delete an audit gate to make a document pass; fix the document.
- Never commit secrets or real PII — `lint-secrets-in-content.py` /
  `lint-pii-in-content.py` gate this, and history rewrites are costly.
- Do not push directly to `main`; develop on a branch (rewriting shared history breaks
  open branches and the version-monotonicity audit).
- No exception path is offered for the audit gates or the pack rules under
  `.claude/rules/governance/`. The three pack rules that reference "the project's
  exception register" as an opt-out channel (`gate-discipline`, `change-tracking`,
  `evidence-grounded-completion`) find no such register in this project: if a gate
  fails or a rule's protocol cannot be satisfied in a PR, the artefact is fixed or the
  PR is descoped. This is the strict-mode stance that each pack rule's exception
  section defaults to when no register exists; it is restated here so the absence is
  explicit rather than inferred.
- If a protected-branch force-push is ever genuinely necessary (credential leaked into
  history, copyright violation must be expunged, malformed merge corrupted the branch),
  follow the procedure in `dev-security/claude-rules/governance/artefact-and-branch-discipline.md`:
  document the technical reason; obtain governance-authority approval; notify
  collaborators in advance; preserve the pre-rewrite ref under
  `refs/preservation/<short-reason>-<YYYY-MM-DD>/<original-ref-name>` so the original
  history remains auditable; re-run the version-monotonicity audit after the rewrite
  to confirm no version-bearing commits were dropped.

## Behavioral rule: clarify before acting
When the request has more than one reasonable interpretation, or an external value
(date, timezone, library version, README version, target branch, whether a change
warrants a CHANGELOG entry, whether to bump per-document versions) is ambiguous,
surface the ambiguity in one sentence and ask before proceeding. Don't silently pick.
The library's audit programme already enforces "surgical changes" and "goal-driven
execution" mechanically through the audit gates and the user-level verification
rules; the gap this section closes is pre-implementation clarification. The
authoritative current form of this discipline lives in
`.claude/rules/governance/clarify-before-acting.md` (the pack rule, project-agnostic)
and as Rule 9 in `~/.claude/CLAUDE.md` (the user-level memory form); originally
adapted from Karpathy's "Think Before Coding" CLAUDE.md rule
(<https://github.com/multica-ai/andrej-karpathy-skills>, MIT).

## Security and governance requirements
Rules in `.claude/rules/` (sourced from this repo's own `dev-security/claude-rules/`
pack, CC BY-SA 4.0):
- `.claude/rules/secrets.md` — never hardcode credentials (all files).
- `.claude/rules/python.md` — Python patterns for `tools/` audit scripts.
- `.claude/rules/input-validation.md` — input handling for the Markdown-parsing tooling.
- `.claude/rules/cicd-gates.md` — CI/CD pipeline security for `quality.yml`.
- `.claude/rules/governance/gate-discipline.md` — never weaken a gate to silence a
  failure; fix the artefact. Reinforces this project's `## Boundaries` rule and applies
  to every gate the audit programme exposes (see `tools/run_all_audits.sh` for the
  current set, including the CHANGELOG-on-PR delta gate).
- `.claude/rules/governance/change-tracking.md` — every change to user-visible content
  carries a CHANGELOG entry by default, with a documented `Changelog: skip` trailer the
  only sanctioned opt-out. Generalises the D1 CHANGELOG-on-PR delta gate, the
  link-coverage gate, and the version-monotonicity audit into a portable discipline.
- `.claude/rules/governance/evidence-grounded-completion.md` — never claim completion
  ("done", "fixed", "ready", "shipped", "good catch"), and never assert a property of an
  artefact you have not read (that a file contains, lacks, or requires something), without
  running the verification protocol first (enumerate, re-read, quote, contradiction-search,
  distinguish mechanical from semantic verification, state unverified items). Pack-distributable
  form of the user-level Rules 6 and 7 (added 2026-05-31 and 2026-06-19); reinforces this
  project's existing Rules 1-5 about verification before dependent actions.
- `.claude/rules/governance/clarify-before-acting.md` — surface ambiguity in one
  sentence and ask before proceeding. Pack-distributable form of this project's
  `## Behavioral rule: clarify before acting` section; generalises that rule into a
  project-agnostic discipline applicable wherever an AI coding assistant participates.
- `.claude/rules/governance/artefact-and-branch-discipline.md` — generated artefacts
  are read-only (edit the source, run the generator, commit both halves together; CI
  verifies via `--check` mode); protected branches are append-only (no direct push;
  no force-push; PR-only merges). Pack-distributable form of this project's
  `## Boundaries` rules on generated files (`taxonomy.yml`, `docs/portal.md`,
  `docs/maturity-scorecard.md`) and on direct pushes to `main`; binds the
  version-monotonicity audit to
  branch protection as its primary defence.
- `.claude/rules/governance/action-before-explanation-of-inaction.md` — never explain
  why an external action cannot or will not proceed without first attempting it (when
  the action is safe and reversible) or naming it and asking (when it is destructive).
  Pack-distributable form of the user-level Rule 8 (added 2026-06-19);
  operationalises this project's `## PR workflow` discipline (the merge of a green PR
  via MCP is a safe action and should be attempted, not narrated as "blocked").
- `.claude/rules/governance/validate-inference-before-action.md` — when the next
  action depends on an inferred premise (a state claim not directly observed in the
  current turn), validate the premise via tool call before taking the action.
  Action-side counterpart of the evidence-grounded-completion rule (which is the
  assertion-side). Added 2026-06-21 after a recurring failure mode where an
  orchestrator inferred premises (subagent-skip justification, fix-completeness,
  corpus-state) without validating; each inference cascaded into downstream rework.
  The immediate trigger was a fix-completeness inference (PR #111's close-out
  inferring the fix complete after one occurrence) that Sweep 9 iteration 2 caught.

The `dev-security/claude-rules/` pack covers security and development-governance
discipline. The initial governance rollout completed at pack version 1.11.0
(2026-06-01) with the first five `governance/` rules listed above; pack version
1.21.0 (Library 2026.06.38) extended the set with the sixth rule; pack version
1.27.0 added the seventh rule (`validate-inference-before-action.md`). See
`dev-security/claude-rules/README.md` for the authoritative pack version history
and future-work signalling. Pack changes are tracked through the library's
CHANGELOG and per-rule version metadata.

The GRC Library pack above is the **primary** source. `.claude/rules/external/` holds a
**supplementary** overlay from third-party sources (TikiTribe, Kariedo, addyosmani — all
MIT, see each dir's LICENSE), provenance-stamped. Overlay rules may overlap or conflict
with the primary layer; the primary GRC pack wins on conflict. The overlay can be pruned
or refreshed independently of the pack. addyosmani's content is engineering-workflow
skills (TDD, code review, CI/CD, security-and-hardening, etc.) in Claude Code's `SKILL.md`
discovery format; scope is engineering practice rather than additional GRC governance.
