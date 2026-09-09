# Pack tooling

The pack-owned compiler lives here: `corpus_mgmt_compiler.py` (an importable module name, and
directly runnable). It reads the generation ruleset (`../gensrc.toml`), validates the manifest,
ownership, and clause registers against it (any disagreement is a configuration error, exit 2), and
renders every declared output deterministically: sorted-rule order, strict UTF-8 with LF endings, no
timestamps, digests, or environment values in any output, atomic temp-file-plus-rename writes.

Gate engines also live here as pack source of record. `gate_lint_language.py` is the engine for grc gate 2 (the language-and-style audit), transferred verbatim in compile PR-5 with only wiring deltas; its project entry point is the thin `tools/lint-language.py` wrapper, which supplies the grc scan roots. Gate 99 owns the compiler and generated outputs, NOT the gate-engine or wrapper bytes: the engine is authored pack source (like the compiler), and the wrapper is hand-maintained project wiring; the linter-regression suite (gate 36) and the gate register's entry-point existence check cover them instead.

Modes and exit codes:

- default (no flag): generate; writes owned outputs that changed. Generation never deletes and never
  places sentinels (sentinel placement is an authored act).
- `--check`: the drift gate (grc gate 99); renders in memory, writes nothing, exits 1 on drift.
- `--root <path>` / `--pack-root <path>` / `--aiqt-root <path>`: explicit project, pack, and AIQT
  roots for standalone adoption; defaults resolve from the compiler's own location inside the pack.
- Exit codes: 0 clean; 1 drift findings; 2 configuration or internal error.

In grc_library the entry point is the thin wrapper `tools/build-corpus-management.py` at the project
root, which bootstraps the vendored AIQT generic core (the compiler reuses its `read_text_safe` for
text reads) and forwards its arguments here.
