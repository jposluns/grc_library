# Rule sources

Sources for the generated `.claude/rules/corpus-management/` tree. The compiler machinery and the
rules-sync recognition (gate 37 reads the pack's ownership register, never a directory skip) shipped
fixture-tested in compile PR-2; the first clause-transfer wave (compile PR-3) transferred the
`language-convention.md` rule here (the first live file-kind rule, generated to
`.claude/rules/corpus-management/language-convention.md` and recognized live by gate 37); compile PR-4 transferred the `authoring-conventions.md`
rule (the second file-kind rule, generated to `.claude/rules/corpus-management/authoring-conventions.md`).
Edit a rule
source here and regenerate via `python3 tools/build-corpus-management.py`, never the generated output.
