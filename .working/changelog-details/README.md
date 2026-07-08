# `.working/changelog-details/`: Maintainer Detailed Changelog

This subdirectory holds the verbose, structured-section changelog entries that the project's change-tracking discipline produces. The root `CHANGELOG.md` carries only the lead paragraph of each entry (the public-facing summary); the full structured entries (Added / Changed / Removed / Fixed / Security / Verification / Discipline observation sections) live here.

The split was introduced in PR #125 (2026-06-21) at maintainer direction. Rationale: the root CHANGELOG is the artefact adopters and downstream consumers read; verbose maintainer-grade detail clutters that surface. Maintainer-grade detail is preserved here, exempt from corpus audit gates, available to anyone who wants the full audit trail without imposing on the public summary.

## Current-week model (2026-07-08, maintainer decision)

The in-repo `CHANGELOG-detailed.md` keeps only the **current week's** entries; completed weeks are swept to the `grc_library_scratch` archive as weekly Monday-dated files (`YYYY-MM-DD_detailed.md`, keyed to the week's Monday). This keeps the in-repo mirror small and browser-openable while the full audit trail accumulates in the wipeable exchange repo (and remains in this repo's git history regardless). The write path is unchanged: new entries still prepend to `CHANGELOG-detailed.md`; only completed weeks leave it.

- **Sweep tool:** [`tools/sweep-working-records-to-scratch.py`](../../tools/sweep-working-records-to-scratch.py) (not an audit gate; an orchestrator follow-up step). It is data-safe: `--emit-archive` writes the weekly archives to scratch, and `--prune` refuses to remove anything from this repo unless `--verify-archived` confirms every artefact already exists in the archive.
- **Gate 59 (mirror header-parity):** its cutoff is now a dynamic floor, `max(CUTOFF_PR, oldest PR still in the in-repo mirror)`, so a swept (now scratch-only) entry is correctly out of parity scope rather than flagged missing, while a genuine in-window drift still fails.
- **Rollout:** the machinery (this tool + the dynamic gate) landed first; the initial sweep of completed weeks and the per-PR sweep-step wiring follow in subsequent PRs. Until the initial sweep runs, this file still holds the full history.

## Files in this subdirectory

| File | Purpose |
|---|---|
| `README.md` | This file: static convention info |
| `CHANGELOG-detailed.md` | The full historical CHANGELOG content with all structured sections. New entries append at the top; same chronological convention as the root CHANGELOG. |

## Per-entry content split

For each substantive change (any PR producing a CHANGELOG entry):

**Root `CHANGELOG.md` keeps**:
- The `## YYYY-MM-DD, Library Version X.Y.Z, PR #NNN` header
- The first paragraph after the header (lead summary, executive-facing)
- The `---` entry separator

**`CHANGELOG-detailed.md` keeps**:
- Everything from the root entry, PLUS
- All `### Added / Changed / Removed / Fixed / Security` sections with file-by-file detail
- The `### Verification` section
- Any `### Discipline gap`, `### Pattern observation`, `### Discipline observation` sections
- Any `### Why this is a separate PR` or design-rationale sections

## What goes where for new PRs

When a contributor adds a CHANGELOG entry, they:

1. Write the full structured entry (lead + Added/Changed/Verification/etc.) in `CHANGELOG-detailed.md`, prepended at the top.
2. Write the lead paragraph (only) at the top of root `CHANGELOG.md`.
3. Both modifications land in the same PR.

The PR-time delta gate (`tools/check-changelog-on-pr.py`) verifies BOTH files were modified when the root CHANGELOG was; missing the detailed mirror fails the gate. The `Changelog: skip` trailer is honoured for trivial PRs.

## Audit-gate exemption

`.working/` is in `tools/lint_common.py` `DEFAULT_EXEMPT_DIRS`. `CHANGELOG-detailed.md` is exempt from:
- Broken-link audit (gate 3)
- Language-style audit (gate 2)
- Citation-currency audit
- Orphan-document audit
- Version-monotonicity audit (per-document)

The PR-time delta gate at `tools/check-changelog-on-pr.py` is an explicit override that does scan this directory for the dual-entry requirement; it runs only on `pull_request` events per `quality.yml`, not on general audit runs.

## Adopter guidance

If you fork this library:
- **Keep the root `CHANGELOG.md` convention** (lead paragraphs only). The pattern demonstrates how to maintain a clean public changelog at zero cost going forward.
- **`CHANGELOG-detailed.md` is upstream maintainer's working state.** You may keep it as historical reference of how the library evolved, or delete and start fresh from your first PR. Either is fine.
- **Going forward, your own contributions** populate `CHANGELOG-detailed.md` in your fork, mirroring your root entries. If you choose not to maintain a detailed changelog, configure `tools/check-changelog-on-pr.py` to skip the dual-entry requirement.

## Convention version

- 1.0.0 (2026-06-21, PR #125), initial split. Historical content (all 112 prior entries) copied verbatim from pre-trim root CHANGELOG; root then trimmed to lead paragraphs.

## Relationship to the change-tracking governance rule

The `dev-security/claude-rules/governance/change-tracking.md` rule was amended in PR #125 to:
- Recognise the split: the structured sections requirement (Added/Changed/Removed/Fixed/Security/Verification) applies to the **detailed** file; the root keeps only the lead paragraph.
- Preserve the `Changelog: skip (reason: ...)` trailer convention for trivial PRs.
- Acknowledge that the detailed file's location is project-specific (this project uses `.working/changelog-details/CHANGELOG-detailed.md`); adopters may relocate.

The rule mirror at `.claude/rules/governance/change-tracking.md` carries the same amendment; the claude-rules sync linter (gate 37) enforces parity.
