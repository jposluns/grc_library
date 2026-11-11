#!/usr/bin/env python3
"""Language and style audit (grc gate 2): project entry point.

The gate ENGINE is pack-owned source of record at
``.claude/skills/corpus-management/src/tools/gate_lint_language.py`` (Corpus-Management pack, gate
register ``core/gates.toml``, id ``lint-language``, enforcing the pack's
``language-convention`` clause); this thin wrapper keeps the house
``python3 .claude/skills/corpus-management/tools/lint-language.py`` shape (gate 35 parses exactly that) and
supplies the grc-local scan configuration the pack engine deliberately does not
carry: the AIQT bootstrap, the repo root, the language VOCABULARY (the pack
profile defaults/grc/language.toml, loaded via profile_loader.load('language')
and composed in _language_config(); the engine compiles the ise/yse patterns
from it), the default markdown scan roots (the
AUDITED_DOMAIN_DIRS splat; the scan-scope parity gate forbids hardcoding the
run), and lint_common's scan-root iterator (whose default-root exemption differs
from the generic aiqt_corpus form). These wrapper bytes are HAND-MAINTAINED, not
compiler-generated, so gate 99 does NOT own them; the linter-regression suite and
gate 99's entry-point existence check are the wrapper's mechanical coverage.

Usage:
    python3 .claude/skills/corpus-management/tools/lint-language.py [paths...]

Exit codes are the engine's: 0 clean; 1 findings; plus 2 when an explicit path is
refused (missing, outside this tree, or relative while not run from the tree root).
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
PACK_TOOLS = REPO_ROOT / ".claude" / "skills" / "corpus-management" / "src" / "tools"

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack .claude/aiqt/tools/ (aiqt_corpus via sys.modules, not sys.path)
from lint_common import CORPUS_SCAN_DIRS, guard_explicit_paths, iter_scan_roots_markdown, positional_args  # noqa: E402  # grc-config/store, stays local


def _engine():
    """Import the pack-owned engine, ensuring its .claude/skills/corpus-management/src/tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_language  # the pack-owned engine (source of record)
    return gate_lint_language


def _language_config():
    """Load the gate-2 language vocabulary from the pack profile.

    Returns the engine's ``LanguageVocabulary`` composed from the pack
    reference-vocabulary profile ``.claude/skills/corpus-management/src/defaults/grc/language.toml``
    (loaded via ``profile_loader.load('language')``, lazily). The engine
    compiles the ise/yse patterns from this vocabulary at run() time. Fail-closed:
    a malformed profile raises ProfileError / ValueError, never a silent default.
    """
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import profile_loader  # the pack-owned reference-vocabulary loader

    return _engine().language_vocabulary(**profile_loader.load("language"))


def iter_markdown_files(paths: list[str]) -> list:
    """The effective markdown scope: lint_common scan-root iteration plus the
    engine's GENERATED_DOCS filter. Retained on the wrapper for the scan-scope
    regression and the language-linter test, which observe this scope directly."""
    engine = _engine()
    return engine.filter_markdown_files(
        iter_scan_roots_markdown(paths, repo_root=REPO_ROOT), REPO_ROOT)


def main(argv: list[str] | None = None) -> int:
    argv = positional_args(list(sys.argv[1:] if argv is None else argv), known_flags=())  # '--' separates paths (quick-guard passes one)
    gate_lint_language = _engine()

    if argv:
        # Explicit paths must name files in THIS tree that exist; a missing, out-of-tree,
        # or non-root-relative path is refused (exit 2) rather than silently passing, and
        # accepted paths are normalized to repo-relative form.
        argv = guard_explicit_paths(argv, repo_root=REPO_ROOT)
        md_input = list(argv)
        gen_input = list(argv)
    else:
        md_input = [
            ".working/CHANGELOG.md",
            "README.md",
            "NOTICE.md",
            "governance/specification-master-project.md",
            "governance/specification-ingestion.md",
            ".claude/skills/corpus-management/specs/instruction-ai-document-ingestion.md",
            # Domain run plus the moved specifications and the authored
            # adopter-facing guides (CM/specs, CM/docs), splatted from lint_common
            # (scan-scope parity gate forbids hardcoding the run); the generated
            # governance/ artefacts are filtered by the engine (GENERATED_DOCS).
            *CORPUS_SCAN_DIRS,
        ]
        gen_input = list(gate_lint_language.GENERATOR_SOURCES)

    md_files = iter_scan_roots_markdown(md_input, repo_root=REPO_ROOT)
    return gate_lint_language.run(
        md_files, gen_input, repo_root=REPO_ROOT, vocab=_language_config())


if __name__ == "__main__":
    sys.exit(main())
