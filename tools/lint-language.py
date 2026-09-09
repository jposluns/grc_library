#!/usr/bin/env python3
"""Language and style audit (grc gate 2): project entry point.

The gate ENGINE is pack-owned source of record at
``.corpus-management/tools/gate_lint_language.py`` (Corpus-Management pack, gate
register ``core/gates.toml``, id ``lint-language``, enforcing the pack's
``language-convention`` clause); this thin wrapper keeps the house
``python3 tools/lint-language.py`` shape (gate 35 parses exactly that) and
supplies the grc-local scan configuration the pack engine deliberately does not
carry: the AIQT bootstrap, the repo root, the default markdown scan roots (the
AUDITED_DOMAIN_DIRS splat; the scan-scope parity gate forbids hardcoding the
run), and lint_common's scan-root iterator (whose default-root exemption differs
from the generic aiqt_corpus form). These wrapper bytes are HAND-MAINTAINED, not
compiler-generated, so gate 99 does NOT own them; the linter-regression suite and
gate 99's entry-point existence check are the wrapper's mechanical coverage.

Usage:
    python3 tools/lint-language.py [paths...]

Exit codes are the engine's: 0 clean; 1 findings.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PACK_TOOLS = REPO_ROOT / ".corpus-management" / "tools"

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import AUDITED_DOMAIN_DIRS, iter_scan_roots_markdown  # noqa: E402  # grc-config/store, stays local


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_language  # the pack-owned engine (source of record)

    if argv:
        md_input = list(argv)
        gen_input = list(argv)
    else:
        md_input = [
            "README.md",
            "NOTICE.md",
            "specification-master-project.md",
            "specification-ingestion.md",
            "instruction-ai-document-ingestion.md",
            # Domain run splatted from lint_common (scan-scope parity gate
            # forbids hardcoding the run).
            *AUDITED_DOMAIN_DIRS,
            # Authored adopter-facing guides; the generated docs/ artefacts
            # are filtered by the engine (GENERATED_DOCS).
            "docs",
            "guardrails",
        ]
        gen_input = list(gate_lint_language.GENERATOR_SOURCES)

    md_files = iter_scan_roots_markdown(md_input, repo_root=REPO_ROOT)
    return gate_lint_language.run(md_files, gen_input, repo_root=REPO_ROOT)


if __name__ == "__main__":
    sys.exit(main())
