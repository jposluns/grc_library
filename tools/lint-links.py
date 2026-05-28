#!/usr/bin/env python3
"""Repository-internal link checker for the GRC Documentation Library.

Validates that every relative markdown link target inside the repository
resolves to a file that exists. External links (http, https, mailto) are
ignored. Anchors after `#` are not validated.

Usage:
    python3 tools/lint-links.py [paths...]

Exits non-zero if any link target is unresolved.
"""

from __future__ import annotations

import os
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Match markdown links: [text](target) where target is not an external URL.
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
EXTERNAL = re.compile(r"^(https?:|mailto:|tel:|ftp:|#)")


def iter_markdown_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        path = REPO_ROOT / p
        if path.is_file() and path.suffix == ".md":
            files.append(path)
        elif path.is_dir():
            for f in path.rglob("*.md"):
                files.append(f)
    return sorted(set(files))


def resolve_link(source: Path, target: str) -> Path:
    """Resolve `target` relative to the directory containing `source`."""
    # Strip fragment (#anchor) from the end of the target.
    target_no_anchor = target.split("#", 1)[0]
    if not target_no_anchor:
        return source  # pure-anchor link
    target_path = (source.parent / target_no_anchor).resolve()
    return target_path


def check_file(path: Path) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    in_code = False
    with path.open("r", encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.rstrip("\n")
            if line.lstrip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            for m in LINK_RE.finditer(line):
                target = m.group(1)
                if EXTERNAL.match(target):
                    continue
                resolved = resolve_link(path, target)
                # The resolved path must exist and be inside REPO_ROOT.
                try:
                    resolved.relative_to(REPO_ROOT)
                except ValueError:
                    findings.append((lineno, target, "resolves outside repo"))
                    continue
                if not resolved.exists():
                    findings.append((lineno, target, "target does not exist"))
    return findings


def main(argv: list[str]) -> int:
    paths = argv[1:] or [
        "README.md",
        "NOTICE.md",
        "specification-master-project.md",
        "specification-ingestion.md",
        "instruction-ai-document-ingestion.md",
        "ai",
        "compliance",
        "dev-security",
        "governance",
        "operations",
        "privacy",
        "resilience",
        "risk",
        "security",
        "supply-chain",
        "tools",
        "docs",
    ]

    files = iter_markdown_files(paths)
    grouped: dict[str, list[tuple[int, str, str]]] = defaultdict(list)
    total = 0
    for f in files:
        for finding in check_file(f):
            grouped[f.relative_to(REPO_ROOT).as_posix()].append(finding)
            total += 1

    if not grouped:
        print("OK: no broken links.")
        return 0

    for relpath in sorted(grouped):
        print(f"=== {relpath} ===")
        for lineno, target, reason in grouped[relpath]:
            print(f"  L{lineno} -> {target}  ({reason})")

    print(f"\nFAIL: {total} broken link(s) across {len(grouped)} file(s).")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
