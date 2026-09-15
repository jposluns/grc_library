#!/usr/bin/env python3
"""Validate intra-document section references.

Library documents frequently reference their own sections by number,
e.g. "see §5.4" or "per Section 11.3". If the document is renumbered or
restructured, such references can silently become broken; a control
referencing "per §5.1.2" is unenforceable if §5.1.2 was removed.

This linter:

- Extracts the numeric section identifiers from headings in each
  document (headings of the form ``## N. Title``, ``### N.N Title``,
  ``#### N.N.N Title``).
- Finds intra-document references of the form ``§N``, ``§N.N``,
  ``§N.N.N``, ``Section N``, ``Section N.N``, ``Section N.N.N`` in the
  document body.
- Fails if any reference's numeric identifier does not match a heading.

Cross-document references are filtered out before the resolution check
via the ``is_cross_doc_context`` heuristic, which detects context
phrases such as "the X Standard §5.4", "the [linked doc] §5.4",
"specification ... §5.4", external framework names (ISO, NIST, OWASP,
etc.), and other markers that the reference is to a different document.

EXEMPT_FILES carries a small set of meta-documents (templates,
worklists) whose section references are by convention not to their own
headings.

Usage:
    python3 tools/lint-intra-doc-refs.py
    python3 tools/lint-intra-doc-refs.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more intra-document references that do not resolve
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import REPO_ROOT, iter_markdown_targets  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

DEFAULT_PATHS = [str(REPO_ROOT)]

# Files exempt because they legitimately discuss intra-document
# section references (the patterns this linter checks).
EXEMPT_FILES = {
    "CHANGELOG.md",
    "specification-citation-verification.md",
}
# Phase 23.62 removed `lint-intra-doc-refs.py` from this set: the
# linter scans `.md` only, so the .py entry was unreachable.


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_intra_doc_refs  # the pack-owned engine (source of record)
    return gate_lint_intra_doc_refs


def scan(path: Path) -> list[tuple[int, str, str]]:
    """Thin shim delegating to the pack engine's pure check.

    Kept in the wrapper as a module-global because the scan-scope regression
    test patches ``mod.scan`` and runs ``main``; the check (HEADING_RE,
    REF_PATTERNS, extract_sections, is_cross_doc_context, scan) lives in the
    pack engine (gate_lint_intra_doc_refs.py).
    """
    return _engine().scan(path)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Validate intra-document section references."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    targets = iter_markdown_targets(args.paths, exempt_files=EXEMPT_FILES)
    grouped: dict[Path, list[tuple[int, str, str]]] = {}
    for t in targets:
        findings = scan(t)
        if findings:
            grouped[t] = findings
    if not grouped:
        print(f"OK: all intra-document section references resolve (scanned {len(targets)} files).")
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        try:
            rel = path.relative_to(REPO_ROOT)
        except ValueError:
            rel = path
        print(f"=== {rel} ===")
        for lineno, ref, excerpt in findings:
            print(f"  L{lineno} [intra-doc-ref] \u00a7{ref} not a heading in this document: {excerpt}")
        total += len(findings)
    print(f"\nFAIL: {total} unresolved intra-document reference(s) across {len(grouped)} file(s).")
    print(
        "References to \u00a7N or Section N inside a document must match a heading "
        "in the same document. If the reference is to another document, include "
        "a markdown link or name the document explicitly."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
