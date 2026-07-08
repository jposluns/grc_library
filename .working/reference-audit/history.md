# Reference-Audit Reference-Breadth Audit History

**Version:** 1.0.0\
**Date:** 2026-07-08\
**License:** CC BY-SA 4.0

Reverse-chronological table of every `/reference-audit` invocation against this library. New rows on top. Each row summarizes one reference-breadth audit run (FULL, per-touch, or new-ingest mode); detail for findings-producing runs lives in a per-run file `YYYY-MM-DD-<scope>.md` linked from the **Detail** column. A zero-finding or empty-candidate run gets a history row with `Detail` = `none`.

`/reference-audit` judges the gate-blind SP 800-154 "held but unused" class in both directions: an authoritative held source that corpus documents which its content would materially improve never engage, and a touched corpus document that newly ingested or updated reference material bears on. It is the breadth layer beside `/matrix-fit` (control-code fit) and `/claim-fit` (claim precision), not a substitute for them or for the citation gates. See the [`reference-audit` SKILL](../../dev-security/claude-rules/skills/reference-audit/SKILL.md) for the seven-step process and the [`/reference-audit`](../../.claude/commands/reference-audit.md) slash command. Cadence: FULL mode as a `/deep-assessment` member and ad-hoc; per-touch mode on every substantive corpus-document PR (delta-anchored by [`doc-state.md`](doc-state.md), judge dispatched only on a non-empty candidate set); new-ingest mode after reference-base changes.

This file is maintainer working state, exempt from corpus audit gates.

## Run entries

| Date | Mode and scope | Worklist | Judge | Findings | Resulting PR | Detail | Summary |
|---|---|---|---|---|---|---|---|
