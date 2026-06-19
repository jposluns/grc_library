# CLAUDE.md

## Project
The GRC Library: a CC BY-SA 4.0 corpus of governance, risk, and compliance
documentation in Markdown, plus a stdlib-only Python audit toolchain that keeps the
corpus internally consistent. There is no application runtime — the deliverable is the
documents and the linters that govern them.
- Documents live in domain dirs: `ai/` `architecture/` `compliance/` `dev-security/`
  `governance/` `operations/` `privacy/` `resilience/` `risk/` `security/`
  `supply-chain/`.
- Audit/build tooling lives in `tools/` (~38 `lint-*.py` / `build-*.py`; shared helpers
  in `tools/lint_common.py`). Tests in `tests/`.
- `taxonomy.yml`, the `docs/` portal, and scorecards are generated from document
  metadata — never hand-edit generated files.

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
- Exempt dirs (`.git`, `node_modules`, `__pycache__`, `.claude`,
  `dev-security/claude-rules/`) are skipped by the corpus linters.

## Conventions
- Mirror an existing same-type document's metadata and section shape rather than
  inventing one; changing the model means changing the linters that enforce it.
- External-standard citations must be accurate and current — `lint-citations.py` and
  `lint-standards-currency.py` reject hallucinated or stale references.
- Prose style is enforced by `lint-language.py`; do not fight the linter by hand.

## Testing
- A change is green only when `tools/run_all_audits.sh` reports all gates passing.
- Add a regression fixture in `tests/` (see `tests/README.md`) for any new linter.

## Boundaries
- Never hand-edit generated files (`taxonomy.yml`, `docs/` portal, scorecards);
  regenerate them — CI `--check` fails on drift.
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
Adapted from Karpathy's "Think Before Coding" CLAUDE.md rule
(<https://github.com/multica-ai/andrej-karpathy-skills>, MIT). The library's
audit programme already enforces "surgical changes" and "goal-driven execution"
mechanically through the audit gates and the user-level verification rules; the gap
this section closes is pre-implementation clarification.

## Security and governance requirements
Rules in `.claude/rules/` (sourced from this repo's own `dev-security/claude-rules/`
pack, CC BY-SA 4.0):
- `.claude/rules/secrets.md` — never hardcode credentials (all files).
- `.claude/rules/python.md` — Python patterns for `tools/` audit scripts.
- `.claude/rules/input-validation.md` — input handling for the Markdown-parsing tooling.
- `.claude/rules/cicd-gates.md` — CI/CD pipeline security for `quality.yml`.
- `.claude/rules/governance/gate-discipline.md` — never weaken a gate to silence a
  failure; fix the artefact. Reinforces this project's `## Boundaries` rule and applies
  to all 32 corpus gates plus the D1 CHANGELOG-on-PR delta gate.
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
  `## Boundaries` rules on generated files (`taxonomy.yml`, the `docs/` portal,
  scorecards) and on direct pushes to `main`; binds the version-monotonicity audit to
  branch protection as its primary defence.

As of pack version 1.11.0 (2026-06-01) the `dev-security/claude-rules/` pack covers
security + development-governance discipline. The phased governance rollout announced
at pack version 1.6.0 (security + governance contract) is complete: pack versions
1.7.0, 1.8.0, 1.9.0, 1.10.0, and 1.11.0 delivered the five planned governance rules
(`governance/gate-discipline.md`, `governance/change-tracking.md`,
`governance/evidence-grounded-completion.md`, `governance/clarify-before-acting.md`,
`governance/artefact-and-branch-discipline.md`). Future pack work may add rules under
`governance/` as the discipline expands, but the planned set is now shipped.

The GRC Library pack above is the **primary** source. `.claude/rules/external/` holds a
**supplementary** overlay from third-party sources (TikiTribe, Kariedo, addyosmani — all
MIT, see each dir's LICENSE), provenance-stamped. Overlay rules may overlap or conflict
with the primary layer; the primary GRC pack wins on conflict. The overlay can be pruned
or refreshed independently of the pack. addyosmani's content is engineering-workflow
skills (TDD, code review, CI/CD, security-and-hardening, etc.) in Claude Code's `SKILL.md`
discovery format; scope is engineering practice rather than additional GRC governance.
