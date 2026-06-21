# PR-Scoped Validation Sweeps

**Version:** 1.0.0\
**Date:** 2026-06-21\
**License:** CC BY-SA 4.0

Per-PR validation records from the `/validate-pr` skill (`validation-sweep-pr-scoped`). Each row in `history.md` records one PR-scoped sweep; per-PR detail files at `YYYY-MM-DD-PR-<N>.md` exist only when findings were surfaced.

See [`dev-security/claude-rules/skills/validation-sweep-pr-scoped/SKILL.md`](../../dev-security/claude-rules/skills/validation-sweep-pr-scoped/SKILL.md) for the skill specification.

## Relationship to corpus-wide validation

This activity records **PR-scoped** validation runs that happen after every merge. The corpus-wide validation activity records under [`.working/validate-sweeps/`](../validate-sweeps/) cover deeper, less-frequent sweeps that examine the whole corpus (every 10 merges or maintainer-triggered).

The two are complementary:

- **`/validate-pr`** (this activity): fast per-merge check. Subagent A on the PR's diff plus a cross-reference check.
- **`/validate`** (corpus-wide activity): comprehensive periodic check. Subagents A + B + C across the whole corpus.

## Convention

- Every `/validate-pr` invocation appends a row to `history.md` regardless of findings.
- Per-PR detail files (`YYYY-MM-DD-PR-<N>.md`) are created only when findings exist; zero-finding sweeps leave just the history row.
- Records are frozen-state artefacts: file paths and line numbers are accurate as-of the moment of the sweep, not maintained against subsequent corpus changes.

## Audit-gate exemption

`.working/` is in `DEFAULT_EXEMPT_DIRS` per `tools/lint_common.py`; this activity inherits the exemption. Records are maintainer working state, not adopter-facing corpus content.
