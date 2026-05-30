#!/usr/bin/env python3
"""Enforce uniform license declaration across artefact documents.

Every artefact document declares its license in the canonical metadata block:

    **License:** CC0 1.0 Universal

The library's CC0 dedication is a legal commitment: the wording must be
uniform. Variants like "CC0-1.0", "CC0 1.0", "Creative Commons Zero",
or "Public Domain" are drift, not synonyms.

This linter verifies that every artefact's License field is exactly
`CC0 1.0 Universal` (with the metadata block's required trailing hard
break).

Usage:
    python3 tools/lint-license-consistency.py
    python3 tools/lint-license-consistency.py path1 path2 ...

Exit codes:
    0   no findings
    1   one or more license-wording deviations present
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATHS = [str(REPO_ROOT)]

CANONICAL_LICENSE = "CC0 1.0 Universal"
LICENSE_LINE_RE = re.compile(r"^\*\*License:\*\*\s+(.+?)\s*$", re.MULTILINE)

EXEMPT_DIR_PARTS = {".git", "node_modules", "__pycache__"}

# Files exempt from the canonical-license rule because they describe the
# license rule itself or list alternative licenses.
EXEMPT_FILES = {
    # Source-license inventory references catalogue alternative licenses by name.
    "CORPUS_LICENSES.json",
    # NOTICE.md deliberately qualifies the license scope to original content
    # only, distinguishing it from external materials. Its License value is
    # nuanced by design.
    "NOTICE.md",
}


def is_target(path: Path) -> bool:
    if path.suffix != ".md":
        return False
    if any(part in EXEMPT_DIR_PARTS for part in path.parts):
        return False
    if path.name in EXEMPT_FILES:
        return False
    return True


def scan(path: Path) -> list[tuple[int, str]]:
    findings: list[tuple[int, str]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return findings
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.startswith("**License:**"):
            value = line[len("**License:**"):].rstrip()
            # Strip CommonMark hard-break backslash
            if value.endswith("\\"):
                value = value[:-1]
            value = value.strip()
            if value != CANONICAL_LICENSE:
                findings.append(
                    (lineno, f"license value {value!r} differs from canonical {CANONICAL_LICENSE!r}")
                )
    return findings


def iter_targets(paths: list[str]) -> list[Path]:
    targets: list[Path] = []
    seen: set[Path] = set()
    for raw in paths:
        p = Path(raw).resolve()
        if p.is_file() and is_target(p):
            if p not in seen:
                targets.append(p)
                seen.add(p)
        elif p.is_dir():
            for f in p.rglob("*.md"):
                if is_target(f) and f not in seen:
                    targets.append(f)
                    seen.add(f)
    return targets


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Enforce uniform License field across artefact documents."
    )
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS)
    args = parser.parse_args(argv[1:])
    targets = iter_targets(args.paths)
    grouped: dict[Path, list[tuple[int, str]]] = {}
    for t in targets:
        findings = scan(t)
        if findings:
            grouped[t] = findings
    if not grouped:
        print(f"OK: all License fields are exactly {CANONICAL_LICENSE!r} (scanned {len(targets)} files).")
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        rel = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        print(f"=== {rel} ===")
        for lineno, msg in findings:
            print(f"  L{lineno} [license-consistency] {msg}")
        total += len(findings)
    print(f"\nFAIL: {total} license-consistency finding(s) across {len(grouped)} file(s).")
    print(f"License field must be exactly {CANONICAL_LICENSE!r}. Library uses uniform CC0 dedication.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
