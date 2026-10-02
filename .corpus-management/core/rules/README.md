# Rule sources

Sources for the generated Corpus-Management rules. Only `language-convention.md` and
`normative-wording.md` remain full rules in `.claude/rules/corpus-management/`, alongside `INDEX.md`.
Other bodies are generated to `.claude/references/corpus-management/` and read on demand.
Gate 37 recognizes the always-loaded files through the ownership register; gate 99 owns the
bytes of both locations. Edit sources here and regenerate with `python3 tools/build-corpus-management.py`.
