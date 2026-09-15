#!/usr/bin/env python3
"""Enforce ISO 8601 (YYYY-MM-DD) date format in document metadata.

Every artefact document records its `**Date:**` field in the canonical
metadata block. This linter verifies that the field's value matches
the YYYY-MM-DD pattern and represents a real calendar date.

Scope:
- Metadata `**Date:** ...` line in every markdown file with a metadata block.
- Does not enforce ISO format for inline dates in prose (would produce
  false positives on legitimate phrasings like "the EU AI Act 2024").
- **Fenced code blocks are skipped.** A `**Date:**` line inside a
  ``` ``` ``` block is documentation showing the metadata-block
  format (e.g., as in README, CONTRIBUTING, the ingestion spec), not
  the file's own metadata. Skipping code blocks via the shared
  `iter_non_code_lines` helper is the structurally-correct way to
  distinguish "real metadata" from "documentation example", instead
  of maintaining an inline allowlist of files known to contain
  examples.

Catches:
- Non-ISO date formats: "April 30, 2026", "4/30/2026", "30/04/2026", "2026/5/30".
- Two-digit years: "26-05-30".
- Implausible values: "2026-13-45".
- Missing zero-padding: "2026-5-30".
- Years outside the plausible 1900-2100 range.

Placeholder permissions:
- ``YYYY-MM-DD`` and ``<YYYY-MM-DD>`` are permitted ONLY in files whose
  name starts with ``template-`` or ``worklist-``. Those files carry
  fill-in markers by design.
- Placeholder Date values in production artefacts are flagged as
  findings. The previous file-identity allowlist
  (``PLACEHOLDER_EXEMPT_FILES``) was retired in Phase 23.57 in favour
  of the code-block-skipping rule above.

Usage:
    python3 tools/lint-date-format.py
    python3 tools/lint-date-format.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more findings present
"""


from __future__ import annotations

import argparse
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import REPO_ROOT, iter_markdown_targets  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

DEFAULT_PATHS = [str(REPO_ROOT)]


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_date_format  # the pack-owned engine (source of record)
    return gate_lint_date_format


def scan(path: Path) -> list[tuple[int, str]]:
    """Thin shim delegating to the pack engine's pure check.

    Kept in the wrapper as a module-global because the scan-scope regression
    test patches ``mod.scan`` and runs ``main``; the check logic (ISO_DATE_RE,
    validate_date, PLACEHOLDER_VALUES, scan) lives in the pack engine
    (gate_lint_date_format.py, source of record).
    """
    return _engine().scan(path)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Enforce ISO 8601 date format in document metadata."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    targets = iter_markdown_targets(args.paths)
    grouped: dict[Path, list[tuple[int, str]]] = {}
    for t in targets:
        findings = scan(t)
        if findings:
            grouped[t] = findings
    if not grouped:
        print(f"OK: all Date metadata fields are ISO 8601 (scanned {len(targets)} files).")
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        rel = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        print(f"=== {rel} ===")
        for lineno, msg in findings:
            print(f"  L{lineno} [date-format] {msg}")
        total += len(findings)
    print(f"\nFAIL: {total} date-format finding(s) across {len(grouped)} file(s).")
    print("Metadata Date fields must be ISO 8601 YYYY-MM-DD with zero padding.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
