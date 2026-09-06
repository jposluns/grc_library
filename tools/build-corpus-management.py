#!/usr/bin/env python3
"""Corpus-Management pack compiler wrapper (gate 99).

The real compiler is pack-owned source at
``.corpus-management/tools/corpus_mgmt_compiler.py`` (so the pack stays
standalone-adoptable and is the source of record); this thin grc entry point
exists so the gate wiring keeps the house ``python3 tools/X.py`` shape (gate
35 parses exactly that), and so the vendored AIQT generic core is
bootstrapped the standard way (``aiqt_bootstrap``) before the compiler's
lazy ``aiqt_corpus`` import.

Usage:
    python3 tools/build-corpus-management.py            # generate (writes owned outputs)
    python3 tools/build-corpus-management.py --check    # gate 99: drift check, writes nothing

Exit codes are the compiler's: 0 clean; 1 drift findings (``--check``); 2
configuration or internal error.

Stdlib-only Python 3.11 plus the vendored AIQT generic core.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PACK_TOOLS = REPO_ROOT / ".corpus-management" / "tools"

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import corpus_mgmt_compiler  # the pack-owned compiler (source of record)

    if "--root" not in argv:
        argv = ["--root", str(REPO_ROOT), *argv]
    return corpus_mgmt_compiler.main(argv)


if __name__ == "__main__":
    sys.exit(main())
