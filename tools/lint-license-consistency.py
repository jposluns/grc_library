#!/usr/bin/env python3
"""Enforce uniform license declaration across artefact documents.

Every artefact document declares its license in the canonical metadata block:

    **License:** CC BY-SA 4.0

The library's CC BY-SA 4.0 dedication is a legal commitment: the wording
must be uniform. Variants like "CC BY-SA", "CC-BY-SA-4.0", "Creative
Commons Attribution-ShareAlike", or "BY-SA 4.0" are drift, not synonyms
(SPDX-style `CC-BY-SA-4.0` is reserved for machine-readable manifests
such as `CITATION.cff`, where it is canonical instead).

This linter verifies that every artefact's License field is exactly
`CC BY-SA 4.0` (with the metadata block's required trailing hard break).

Exempted: ``NOTICE.md`` (governance-level licence-notice file that
deliberately qualifies licence scope to original content only).

Usage:
    python3 tools/lint-license-consistency.py
    python3 tools/lint-license-consistency.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more license-wording deviations present
"""


from __future__ import annotations

import argparse
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import REPO_ROOT, iter_markdown_targets  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

DEFAULT_PATHS = [str(REPO_ROOT)]

# Files exempt from the canonical-license rule because they describe the
# license rule itself or list alternative licenses.
EXEMPT_FILES = {
    # NOTICE.md deliberately qualifies the license scope to original content
    # only, distinguishing it from external materials. Its License value is
    # nuanced by design.
    "NOTICE.md",
}


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_license_consistency  # the pack-owned engine (source of record)
    return gate_lint_license_consistency


def scan(path: Path) -> list[tuple[int, str]]:
    """Thin shim delegating to the pack engine's pure check.

    Kept in the wrapper as a module-global because the scan-scope regression
    test patches ``mod.scan`` and runs ``main``; the canonical string and the
    check live in the pack engine (gate_lint_license_consistency.py).
    """
    return _engine().scan(path)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Enforce uniform License field across artefact documents."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    canonical = _engine().CANONICAL_LICENSE
    targets = iter_markdown_targets(args.paths, exempt_files=EXEMPT_FILES)
    grouped: dict[Path, list[tuple[int, str]]] = {}
    for t in targets:
        findings = scan(t)
        if findings:
            grouped[t] = findings
    if not grouped:
        print(f"OK: all License fields are exactly {canonical!r} (scanned {len(targets)} files).")
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        rel = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        print(f"=== {rel} ===")
        for lineno, msg in findings:
            print(f"  L{lineno} [license-consistency] {msg}")
        total += len(findings)
    print(f"\nFAIL: {total} license-consistency finding(s) across {len(grouped)} file(s).")
    print(f"License field must be exactly {canonical!r}. Library uses uniform CC BY-SA 4.0 licence.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
