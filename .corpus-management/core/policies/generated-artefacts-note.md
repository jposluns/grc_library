- `taxonomy.yml`, `docs/portal.md`, and `docs/maturity-scorecard.md` are generated
  from corpus document metadata; `narrative.yml` is generated independently from
  `executive/` page metadata. Never hand-edit generated files; regenerate via
  `tools/build-taxonomy.py`, `tools/build-narrative-registry.py`, and
  `tools/build-portal.py`, and commit the source plus the regenerated output together.
