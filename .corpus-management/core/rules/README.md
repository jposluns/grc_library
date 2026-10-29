# Rule sources

Sources for the generated Corpus-Management rules. Only `language-convention.md` and
`normative-wording.md` remain full rules in `.claude/rules/corpus-management/`.
Other bodies are generated to `.claude/references/corpus-management/` and read on demand through
the rule index, which ships with the corpus-management skill
(`.claude/skills/corpus-management/rule-index.md`).
Gate 37 recognizes the always-loaded files through the ownership register; gate 99 owns every
file in `.claude/rules/corpus-management/`, `.claude/references/corpus-management/` and
`.claude/skills/corpus-management/`, and the generated block body in `.claude/CLAUDE.md`.
Edit sources here and regenerate with `python3 tools/build-corpus-management.py`.
