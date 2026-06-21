# `.working/` — Maintainer Working Space

This directory holds operational artefacts produced by maintainer-invoked tooling: per-run records, detailed reports, working drafts, and other outputs that assist the maintainer but are not part of the published GRC library content.

## What `.working/` is

- **Maintainer-only working state.** The files here are reference material for the library maintainer, used to justify decisions, track per-run outputs, and capture detail that does not belong in the canonical corpus.
- **Frozen-state archives.** Each file is a snapshot at the moment it was written. Cross-references and links are accurate as-of that moment and are not maintained against subsequent corpus changes.
- **Exempt from audit gates.** This directory is listed in `tools/lint_common.py` `DEFAULT_EXEMPT_DIRS`. Broken-link drift, language-style drift, citation staleness, and orphan status here are expected and do not fail CI.

## What `.working/` is not

- **Not library content.** Adopters reading the corpus do not need to read `.working/`. The library's normative content lives in the domain directories (`ai/`, `compliance/`, `governance/`, etc.) and the dev-security claude-rules pack.
- **Not generated artefacts.** `docs/portal.md`, `docs/maturity-scorecard.md`, and `taxonomy.yml` are mechanically generated from corpus metadata. `.working/` is hand-curated or AI-assisted but human-reviewed; not a build output.
- **Not for adopter consumption.** Adopters cloning the library should treat `.working/` as the upstream maintainer's local state; delete it, ignore it, or keep it as historical context — their choice.

## Contents

Each subdirectory holds output of one specific maintainer activity; top-level files hold cumulative history or other high-level state. New entries are added as activities ship.

### Subdirectories

| Subdirectory | Purpose | Created by |
| --- | --- | --- |
| [`validate-sweeps/`](validate-sweeps/) | Per-iteration records from `/validate` invocations (full subagent transcripts, orchestrator synthesis, resulting PR). One file per iteration. | PR #115 |

### Top-level files

| File | Purpose | Created by |
| --- | --- | --- |
| [`validate-sweeps-history.md`](validate-sweeps-history.md) | Cumulative log of `/validate` invocations: failure-mode class taxonomy, sweep entries, false-positive memory, recurring-class summary. The summary counterpart to the per-iteration files in `validate-sweeps/`. | Moved from `governance/register-sweep-history.md` in PR #116 |

**To add a new subdirectory or top-level file**: append a row to the appropriate table above with a one-line purpose statement and the PR / skill / activity that creates content in it.

## Fork guidance

If you fork or clone this library as a starting point for your own GRC programme:

- **You may safely delete `.working/`** — nothing in the library's canonical content depends on it.
- **You may keep it as historical reference** — the contents document decisions the upstream maintainer made and may inform your own adaptation.
- **You should not extend the upstream `.working/` with your own working state** — create a fresh `.working/` for your own outputs; mixing the two histories defeats the audit-trail value on both sides.

## License

The contents of this directory inherit the library's CC BY-SA 4.0 license (see [`LICENSE`](../LICENSE)). Files written here by AI coding assistants may include verbatim subagent transcripts; those are derivative works of the corpus they review and carry the same license.
