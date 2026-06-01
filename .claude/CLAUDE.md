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
corpus is machine-auditable. The 32-gate audit programme enforces that model so
governance content stays citable, cross-linked, and free of drift, secrets, or PII.

## Commands
- Full audit sweep (32 gates, CI order): `tools/run_all_audits.sh`
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

## Behavioral rule: clarify before acting
When the request has more than one reasonable interpretation, or an external value
(date, timezone, library version, README version, target branch, whether a change
warrants a CHANGELOG entry, whether to bump per-document versions) is ambiguous,
surface the ambiguity in one sentence and ask before proceeding. Don't silently pick.
Adapted from Karpathy's "Think Before Coding" CLAUDE.md rule
(<https://github.com/multica-ai/andrej-karpathy-skills>, MIT). The library's
audit programme already enforces "surgical changes" and "goal-driven execution"
mechanically through the 32 gates and the user-level verification rules; the gap
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

As of pack version 1.8.0 (2026-06-01) the `dev-security/claude-rules/` pack covers
security + development-governance discipline. Pack version 1.6.0 announced the
broadened contract; pack version 1.7.0 delivered the first governance rule
(`governance/gate-discipline.md`); pack version 1.8.0 delivered the second
(`governance/change-tracking.md`). Subsequent governance rules (evidence-grounded
completion, clarify-before-acting, artefact-and-branch discipline) arrive in later
phased releases and will be listed here as they land.

The GRC Library pack above is the **primary** source. `.claude/rules/external/` holds a
**supplementary** overlay from third-party sources (TikiTribe, Kariedo — both MIT, see
each dir's LICENSE), provenance-stamped. Overlay rules may overlap or conflict with the
primary layer; the primary GRC pack wins on conflict. The overlay can be pruned or
refreshed independently of the pack.
