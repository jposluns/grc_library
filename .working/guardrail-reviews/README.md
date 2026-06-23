# Guardrail-review activity

Per-run records of the `/guardrails` (canonical skill name `guardrail-review`)
structural-integrity review of the governance machinery. `/guardrails` is the
periodic guard-rail review: a judgment-based pass over the rules, skills, and audit
gates (plus their wiring surfaces) for **overlap** (redundant or contradictory
coverage), **gap** (a stated discipline no gate enforces, a recurring failure mode no
rule names), and **drift** (a meaning diverged across wiring surfaces below the
mechanical parity gates' resolution). It is distinct from the content sweeps
(`/validate`, `/validate-pr`) and the trust-recovery suite (`/full-qa`, `/fitness`):
those review the corpus or a window of work, while `/guardrails` reviews the machinery
itself. The skill is specified at
[`dev-security/claude-rules/skills/guardrail-review/SKILL.md`](../../dev-security/claude-rules/skills/guardrail-review/SKILL.md);
the slash-command entry point is [`.claude/commands/guardrails.md`](../../.claude/commands/guardrails.md).

This directory is maintainer working state, exempt from corpus audit gates per the
`.working/` directory exemption. Records are frozen-state archives: `path:line`
references are accurate as-of write-time, not maintained against later corpus changes.

## Convention

- One record per run: `YYYY-MM-DD-rN.md` (UTC date per `.claude/CLAUDE.md`).
- Sections: one per lens (overlap, gap, drift); an orchestrator-synthesis-and-verification
  section; a findings-routed section.
- A row is appended to [`history.md`](history.md) on every run; zero-finding runs get a
  history row but no per-run record file (the row alone is the persistent trace).
- The review is a single pass (not a fix-to-fixed-point loop): structural findings are
  maintainer-decision proposals, routed to the backlog tagged `[guardrails]`, tiered by
  severity, none dropped.

## Cadence

Maintainer-triggered, and auto-prompted after any PR that adds, removes, or renames a
rule, skill, or gate (the machinery inventory changed, so its coherence is exactly what
the mechanical parity gates cannot re-confirm).
