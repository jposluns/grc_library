# Change-impact surface map, first-pass scope draft (TODO §1.18)

**Status: FIRST-PASS SCOPE DRAFT for maintainer review and revision.** §1.18 is flagged
"needs some thinking and revision; expect a written scope + maintainer review before build".
This is prepared overnight input, not a design to build from as-is. It organizes the surface
enumeration already in the TODO §1.18 text into a "when you change X, update ALL of these"
map, folds in the existing partial coverage (rather than duplicating it), and works the D8
pilot. The maintainer revises before any build.

## The problem (from §1.18)

A gate / lint / rule / skill / count change touches more surfaces than the existing partial
guards cover, and the PROSE surfaces drift. Evidence from this session alone: D8 (#989)
shipped without updating the `change-tracking` pack rule's discipline description, and §1.17
was added without updating the P1-count prose (caught only by the pre-push verifier).

## Existing partial coverage (fold in, do NOT duplicate)

- **Gate 35**: four-surface tooling parity (workflow, runner, pre-commit, spec §6 table).
- **Gate 39**: gate-count idioms in scanned surfaces.
- **D6**: pack-README version + version-history row.
- **Close-out-checklist prose-count line**: prose counts checked for staleness after the
  verifier loop.
- **Gate 37**: pack-rule vs `.claude/rules/` copy parity (overlay-stripped).

## Draft per-change-type surface maps (to be validated + revised)

### Change type A: new or changed audit gate / linter
GATED (gate 35): workflow, runner, pre-commit, spec §6 inventory table. FREE-PROSE (drift-prone, no gate): spec §6 detailed-prose enumeration (the `Gate N is a ...` + `Gate N is appended ...` pair); spec §5 grouped-list; the per-gate §6 narrative (only if detection logic changed); the module docstring; a regression fixture; a PR-time `Dn` step name in `WORKFLOW_DELTA_GATE_STEPS` (if a delta check). COUNT ripple (gate 39 counts idioms but not every prose count): README, spec, `.claude/CLAUDE.md` raw-count mentions, tool docstrings, the website prose (counts auto-recompute from the taxonomy/README, but pack/discipline/gate PROSE does not), adopter-facing MD.

### Change type B: new or changed pack rule
GATED (gate 37): both trees (`dev-security/claude-rules/` + `.claude/rules/`) in sync. FREE-PROSE: the pack README rule-index one-liner + scope row + version-history table (D6 covers the version); `.claude/CLAUDE.md` rule-index one-liner; the pack rule COUNT prose. PORTABILITY: a portable discipline that a gate or convention mechanizes belongs DESCRIBED project-agnostically in its pack rule so adopters enforce it (the QA-completion codification, deferred item 12, is a worked instance of this direction).

### Change type C: new or changed skill
GATED: gate 32 (`derives_from`), gate 41 (README tree), gate 44 (step-parity), PAIRS registry. FREE-PROSE: `.claude/CLAUDE.md` cadence-section (if the skill has a cadence), the pack README skills table, the slash-command file, the skill COUNT prose; `lint-language.py` pre-flight on new prose.

### Change type D: a count change (gates / rules / skills / doc-types)
No single gate covers all prose counts. Surfaces: README, the spec, `.claude/CLAUDE.md`, tool docstrings, the website pack/discipline prose, adopter MD. Discipline: counts are computed AFTER the verifier loop closes (the #612 timing rule), and grepped at BARE-TOKEN width across ALL file types (`.md`, `.py`, `.yml`, `.json`, `.sh`, `.claude/`, `.working/`), not `.md` alone.

## D8 worked example (the pilot; retroactively apply the map)

D8 (the CHANGELOG-length gate, #989) is change type A. Retroactive gaps to close: (1) add the CHANGELOG-length-ceiling DISCIPLINE to the `change-tracking` pack rule project-agnostically (it currently describes only the compact FORM, not a ceiling); (2) check + update the website + adopter-facing MD surfaces that describe the CHANGELOG discipline. This validates the map on a real recent gate.

## Deliverables (per §1.18; for maintainer confirmation)

1. A documented surface map (the tables above, revised).
2. A close-out-checklist section keyed by change type.
3. A mechanizable gate where feasible for the multi-surface-incompleteness class (the free-prose surfaces are the hard part; a full mechanization may not be feasible, in which case the checklist is the residual guard, the same convention-level residual as the QA-abbreviation half).

## Open scoping questions for the maintainer

- How far to mechanize vs leave to the close-out checklist? The free-prose surfaces (spec detailed-prose, website prose, count prose) resist a clean gate.
- Is the website (`grclibrary.ai`) prose in scope for a mechanical check, or a manual close-out step (it is a separate deploy; neither repo's CI sees it)?
- Should this subsume or cross-reference the existing gate 35 / gate 39 / D6 rather than re-implement?
