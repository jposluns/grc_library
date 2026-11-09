# CLAUDE.md

Adopter seed. This file ships with the public corpus for an organization that clones it;
replace or extend it to match your own workflows, but keep the compiler-owned block intact
and keep the Boundaries section in force.

## Project

GRC Library: a CC BY-SA 4.0 Markdown governance/risk/compliance corpus with Python audit
tooling; no application runtime. Stdlib-only tooling except the sanctioned `idna` dependency
for exact UTS-46 PII checking (`requirements.txt`).
Domain directories: `ai/`, `architecture/`, `compliance/`, `crypto/`, `dev-security/`,
`governance/`, `operations/`, `privacy/`, `resilience/`, `risk/`, `security/`,
`supply-chain/`.
Corpus tooling lives in the Corpus-Management skill at `.claude/skills/corpus-management/`
(`.claude/skills/corpus-management/tools/lint-*.py`, `.claude/skills/corpus-management/tools/build-*.py`, shared `.claude/skills/corpus-management/tools/lint_common.py`, tests in `.claude/skills/corpus-management/tests/`).
Current gate inventory: `.claude/skills/corpus-management/tools/run_all_audits.sh` and
`.github/workflows/quality.yml`. Repository slash commands live in `.claude/commands/`.
<!-- corpus-management:begin claude-generated-artefacts-note (compiler-owned; edit .claude/skills/corpus-management/src/core/policies/generated-artefacts-note.md, then run: python3 .claude/skills/corpus-management/tools/build-corpus-management.py) -->
- `.claude/skills/corpus-management/data/taxonomy.yml`, `governance/portal.md`, and `governance/maturity-scorecard.md` are generated
  from corpus document metadata; `.claude/skills/corpus-management/data/narrative.yml` is generated independently from
  `executive/` page metadata. Never hand-edit generated files; regenerate via
  `.claude/skills/corpus-management/tools/build-taxonomy.py`, `.claude/skills/corpus-management/tools/build-narrative-registry.py`, and
  `.claude/skills/corpus-management/tools/build-portal.py`, and commit the source plus the regenerated output together.
<!-- corpus-management:end claude-generated-artefacts-note -->

## Why

Every document has 13-field metadata and fixed sections. The audit programme
(`.claude/skills/corpus-management/specs/specification-audit-programme.md` section 6)
enforces auditable, citable, cross-linked content without drift, secrets or PII.

## AIQT baseline

This project is developed under the AIQT discipline (https://aiqt.ai): accuracy, integrity,
quality and trust are never traded for progress, speed or cost. The pinned AIQT rule set
lives under `.claude/aiqt/`; the generated per-rule indexes below are complete (ordinary
links are navigation, not startup imports), and the always-loaded language convention is
`.claude/rules/corpus-management/language-convention.md`.
<!-- AIQT-RULES-BEGIN -->
- aiqt: [`aiqt/00-project-integrity.md`]; [`aiqt/10-ACCUR-citation-from-opened-file.md`]; [`aiqt/10-ACCUR-claims-rest-on-observation.md`]; [`aiqt/10-ACCUR-completeness-claim-enumerates-its-set.md`]; [`aiqt/10-ACCUR-corroborate-external-claims.md`]; [`aiqt/10-ACCUR-count-carries-its-predicate.md`]; [`aiqt/10-ACCUR-disclose-guard-residuals.md`]; [`aiqt/10-ACCUR-evidence-grounded-completion.md`]; [`aiqt/10-ACCUR-guard-input-soundness.md`]; [`aiqt/10-ACCUR-measured-and-estimated-figures-stay-separate.md`]; [`aiqt/10-ACCUR-no-fabrication.md`]; [`aiqt/10-ACCUR-observe-before-asserting-behaviour.md`]; [`aiqt/10-ACCUR-partial-read-is-not-the-whole.md`]; [`aiqt/10-ACCUR-read-before-characterizing.md`]; [`aiqt/10-ACCUR-reference-capture.md`]; [`aiqt/10-ACCUR-reproduce-before-fix.md`]; [`aiqt/10-ACCUR-timestamp-from-clock.md`]; [`aiqt/10-ACCUR-validate-inference-before-action.md`]; [`aiqt/10-ACCUR-verify-fix-in-commit.md`]; [`aiqt/10-INTEG-anything-wrong-fixed-first.md`]; [`aiqt/10-INTEG-attestation-is-harness-owned.md`]; [`aiqt/10-INTEG-branch-and-merge-on-green.md`]; [`aiqt/10-INTEG-branch-rooted-on-live-main.md`]; [`aiqt/10-INTEG-check-fails-closed-on-unreadable.md`]; [`aiqt/10-INTEG-commit-identity.md`]; [`aiqt/10-INTEG-consumer-follows-its-producer.md`]; [`aiqt/10-INTEG-explicit-binding-over-ambient-context.md`]; [`aiqt/10-INTEG-gate-discipline.md`]; [`aiqt/10-INTEG-generated-artefact-source-only.md`]; [`aiqt/10-INTEG-licence-compatibility.md`]; [`aiqt/10-INTEG-no-concealed-failure.md`]; [`aiqt/10-INTEG-preserve-uncommitted-work.md`]; [`aiqt/10-INTEG-protected-branch-integrity.md`]; [`aiqt/10-INTEG-required-step-remains-required.md`]; [`aiqt/10-INTEG-rerun-pass-is-still-failure.md`]; [`aiqt/10-INTEG-review-in-flight-pins-its-artefact.md`]; [`aiqt/10-INTEG-safe-retries.md`]; [`aiqt/10-INTEG-separate-task-changes.md`]; [`aiqt/10-INTEG-stage-then-promote-on-green.md`]; [`aiqt/10-INTEG-track-launched-work.md`]; [`aiqt/10-INTEG-validation-gates-apply.md`]; [`aiqt/10-INTEG-workers-produce-inert-data.md`]; [`aiqt/10-QUALI-absolute-paths.md`]; [`aiqt/10-QUALI-change-carries-check.md`]; [`aiqt/10-QUALI-compatibility-or-migration.md`]; [`aiqt/10-QUALI-confirm-execution-target.md`]; [`aiqt/10-QUALI-defence-in-depth-default.md`]; [`aiqt/10-QUALI-elapsed-aware-timer-restore.md`]; [`aiqt/10-QUALI-findings-are-fixed-not-argued.md`]; [`aiqt/10-QUALI-goal-fidelity-across-trajectory.md`]; [`aiqt/10-QUALI-high-assurance-verification.md`]; [`aiqt/10-QUALI-kill-timeout-exceeds-callee-wait.md`]; [`aiqt/10-QUALI-lightweight-verifier-workers.md`]; [`aiqt/10-QUALI-match-surrounding-code.md`]; [`aiqt/10-QUALI-minimize-dependencies.md`]; [`aiqt/10-QUALI-self-guardrail-from-error.md`]; [`aiqt/10-QUALI-smallest-correct-change.md`]; [`aiqt/10-QUALI-surface-counterproductive-instructions.md`]; [`aiqt/10-QUALI-test-hermeticity.md`]; [`aiqt/10-QUALI-verifier-delivery-completeness.md`]; [`aiqt/10-QUALI-verifier-diversity.md`]; [`aiqt/10-TRUST-ai-toolchain-register.md`]; [`aiqt/10-TRUST-assess-advise-discussion-only.md`]; [`aiqt/10-TRUST-atomic-claim-from-pool.md`]; [`aiqt/10-TRUST-change-record.md`]; [`aiqt/10-TRUST-change-tracking-ext.md`]; [`aiqt/10-TRUST-clarify-before-acting.md`]; [`aiqt/10-TRUST-concurrency-lease.md`]; [`aiqt/10-TRUST-continue-by-default.md`]; [`aiqt/10-TRUST-express-authorization-before-execution.md`]; [`aiqt/10-TRUST-human-oversight-and-autonomy-threshold.md`]; [`aiqt/10-TRUST-no-console-diff-dumps.md`]; [`aiqt/10-TRUST-orchestrator-mistakes-register.md`]; [`aiqt/10-TRUST-reconcile-record-against-reality.md`]; [`aiqt/10-TRUST-records-first.md`]; [`aiqt/10-TRUST-session-close-on-green.md`]; [`aiqt/10-TRUST-session-resume-from-handoff.md`]; [`aiqt/10-TRUST-standing-constraints-persist.md`]; [`aiqt/10-TRUST-trust-recovery-escalation.md`]; [`aiqt/10-TRUST-trust-recovery-ext.md`]; [`aiqt/20-PROGR-decision-classification-before-enacting.md`]; [`aiqt/20-PROGR-repeated-failure-triggers-premise-review.md`]; [`aiqt/30-SPEED-background-work-during-ci-waits.md`]; [`aiqt/40-COST-cost-tier.md`]
- security: [`security/SECA-resource-bounds.md`]; [`security/SECA-verified-restore-path.md`]; [`security/SECC-data-boundary.md`]; [`security/SECC-egress-destinations.md`]; [`security/SECC-keep-secrets-out.md`]; [`security/SECC-least-privilege-retrieval.md`]; [`security/SECC-no-cross-context-bleed.md`]; [`security/SECC-no-hidden-context-disclosure.md`]; [`security/SECC-rotate-leaked-secret.md`]; [`security/SECI-authentication.md`]; [`security/SECI-authorization.md`]; [`security/SECI-config-is-executable-trust-gate.md`]; [`security/SECI-cryptography.md`]; [`security/SECI-dependency-provenance.md`]; [`security/SECI-fail-closed.md`]; [`security/SECI-federated-identity-flow.md`]; [`security/SECI-file-upload-handling.md`]; [`security/SECI-guardrail-config-integrity.md`]; [`security/SECI-human-authorization.md`]; [`security/SECI-input-validation.md`]; [`security/SECI-inter-agent-trust.md`]; [`security/SECI-key-management.md`]; [`security/SECI-least-privilege-tools.md`]; [`security/SECI-log-redaction.md`]; [`security/SECI-operator-deception.md`]; [`security/SECI-output-encoding.md`]; [`security/SECI-output-handling.md`]; [`security/SECI-pin-referenced-instructions.md`]; [`security/SECI-poisoning-resistance.md`]; [`security/SECI-prefer-removing-a-path.md`]; [`security/SECI-preview-has-no-side-effects.md`]; [`security/SECI-prompt-trust-hierarchy.md`]; [`security/SECI-protect-audit-records.md`]; [`security/SECI-reject-vulnerable-versions.md`]; [`security/SECI-release-integrity.md`]; [`security/SECI-safe-deserialization.md`]; [`security/SECI-secure-configuration.md`]; [`security/SECI-security-logging.md`]; [`security/SECI-session-token-management.md`]; [`security/SECI-ssrf-prevention.md`]; [`security/SECI-symlink-resolution.md`]; [`security/SECI-threat-model-boundaries.md`]; [`security/SECI-tool-argument-validation.md`]; [`security/SECI-untrusted-content.md`]; [`security/SECI-verify-dependency-exists.md`]; [`security/SECP-data-minimization.md`]; [`security/SECP-data-residency-retention.md`]; [`security/SECP-purpose-limitation.md`]; [`security/SECP-synthetic-fixture-data.md`]
<!-- AIQT-RULES-END -->

## Commands

- Full audit sweep (all gates, CI order): `.claude/skills/corpus-management/tools/run_all_audits.sh`
- Stop on first failure: `FAIL_FAST=1 .claude/skills/corpus-management/tools/run_all_audits.sh`
- One gate: `python3 .claude/skills/corpus-management/tools/<lint-name>.py`
- Linter regression tests: `python3 .claude/skills/corpus-management/tools/run-linter-regression.py`
- Pre-commit (mirrors CI): `pre-commit run --all-files`
- Regenerate derived artefacts (`.claude/skills/corpus-management/tools/build-*.py`,
  `python3`-run; CI `--check` verifies sync): `build-taxonomy.py`,
  `build-narrative-registry.py`, `build-portal.py`, `build-relationship-model.py`,
  `build-todo-number-allocation.py`, `build-corpus-management.py`,
  `build-citation-publishers.py`

CI source of truth: `.github/workflows/quality.yml`. Keep `quality.yml`,
`.claude/skills/corpus-management/tools/run_all_audits.sh`, and `.pre-commit-config.yaml` in
lock-step: a gate added to one must be added to all (the gate-parity audit enforces this).

## Structure

- `.claude/skills/corpus-management/tools/lint_common.py` holds discovery, exemptions and
  helpers; consult it for the exempt-directory set and per-linter prefixes (the common set is
  not exhaustive).
- New audit: a `lint-*.py` tool, workflow/runner/pre-commit/audit-programme-spec wiring, and
  a regression fixture in `.claude/skills/corpus-management/tests/`.

## Conventions

The Corpus-Management skill owns authoring conventions
(`.claude/references/corpus-management/authoring-conventions.md`) and the language convention
above. Before creating, editing, reviewing or auditing a corpus document or any file a corpus
gate scans, when a corpus gate fails, or when answering a question about a corpus rule, load
the `corpus-management` skill and read its `rule-index.md`, which names the rule body to read
first.
Edit sources under `.claude/skills/corpus-management/src/`, never outputs; regenerate via
`.claude/skills/corpus-management/tools/build-corpus-management.py`. Gate 99 owns generated
bytes.

## Testing

- A change is green only when `run_all_audits.sh` reports all gates passing.
- Add a regression fixture (see `.claude/skills/corpus-management/tests/README.md`) for any
  new linter.

## Date convention

Use UTC for all date fields and "today": document `Date` fields, CHANGELOG headers and dated
record filenames. Local "today" may lag UTC by a day; write UTC dates and resolve ambiguity
with UTC.

## Version-bump discipline

Four version-bearing surfaces:
1. Per-document `Version`: bump in the same commit that changes the document body. Every
   commit, no exceptions (gate 40).
2. Per-document `Date`: bump to today (UTC) in the same commit (gate 31; when in doubt,
   today).
3. Library CalVer in `README.md` (`YYYY.MM.NNN`): once per PR, in the last commit before
   push.
4. README `Version` field: once per PR with the CalVer; an earlier README-body commit
   carries `VersionBump: none <reason>`.
A tracked commit-time hook auto-bumps or blocks a missed per-document bump; gate 40 and the
delta gates remain the authority.

## Boundaries

- Never hand-edit generated files; edit sources, regenerate, and commit both together; CI
  `--check` fails on drift (see the compiler-owned block above and
  `build-relationship-model.py` for `governance/relationship-model.generated.json`).
- Never weaken, skip or delete a gate, test or assertion to force a pass; fix the document.
- Never commit secrets or real PII (`lint-secrets-in-content.py`, `lint-pii-in-content.py`);
  history rewrites are costly.
- Never push directly to `main`; develop on a feature branch and merge by PR.

## Guard hooks (tracked settings seed)

`.claude/settings.json` registers five guard hooks from `.claude/hooks/`, each launched as
`/usr/bin/python3 -I "$CLAUDE_PROJECT_DIR"/.claude/hooks/<name>.py`. They enforce the last
three Boundaries items and the version-bump discipline mechanically:
- `block-branch-to-main-edit.py` (Edit|Write): blocks edits while the repo is on `main`.
- `block-unbumped-version-commit.py` (Bash): auto-bumps or blocks a commit that changes a
  versioned document body without bumping it.
- `block-bulk-git-add.py` (Bash): refuses tree-sweep staging; name the paths you stage.
- `block-verification-pipes.py` (Bash): refuses verification commands piped into truncating
  filters; use `.claude/skills/corpus-management/tools/tail-safe.sh` instead.
- `block-repeated-tool-failure.py` (Bash): breaks the resubmit-the-blocked-command loop.
Two helpers (`_hookutil.py`, `_hook_state.py`) ship beside them; hook state lives in the
gitignored `.claude/hooks/.state/`. Register local additions in the untracked
`.claude/settings.local.json`, never by editing the tracked seed in place.

## Adopter working files and private store

- `.working/TODO.md` and `.working/CHANGELOG.md` are this clone's backlog and changelog
  home; the backlog and changelog gates read them.
- Operational records you do not want in the public tree (decision logs, review history,
  drafts) belong in a private store outside this repository. Run `/adopt` to set one up;
  `.claude/skills/corpus-management/adopter-config.json` holds the configuration. The public
  gates degrade gracefully when no store is configured.
