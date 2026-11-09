- `.claude/skills/corpus-management/data/taxonomy.yml`, `governance/portal.md`, and `governance/maturity-scorecard.md` are generated
  from corpus document metadata; `.claude/skills/corpus-management/data/narrative.yml` is generated independently from
  `executive/` page metadata. Never hand-edit generated files; regenerate via
  `.claude/skills/corpus-management/tools/build-taxonomy.py`, `.claude/skills/corpus-management/tools/build-narrative-registry.py`, and
  `.claude/skills/corpus-management/tools/build-portal.py`, and commit the source plus the regenerated output together.
