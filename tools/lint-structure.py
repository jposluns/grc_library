#!/usr/bin/env python3
"""Structural index integrity checker for the GRC Documentation Library.

Asserts that:

1. Every active markdown file in each domain folder appears in that
   domain's README.md Active Documents table.
2. Every active markdown file (excluding READMEs, exempt files, draggable
   AI-context rule files, tooling, and the privacy deprecated annex)
   appears in `governance/register-document-index-and-classification.md`.
3. Every entry in those tables points to a file that exists.

Usage:
    python3 tools/lint-structure.py
    python3 tools/lint-structure.py --root /path/to/alt-repo

The ``--root`` flag overrides the repository root the linter scans (used
by the gate-36 regression test suite to point at a synthetic minimal
repository fixture). Default: the actual repo root, derived from this
file's location.

Exits non-zero on any finding.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DOMAINS = [
    "ai",
    "architecture",
    "compliance",
    "dev-security",
    "governance",
    "operations",
    "privacy",
    "resilience",
    "risk",
    "security",
    "supply-chain",
]

# Files explicitly exempt from the structural-membership requirement.
EXEMPT_FROM_INDEX = {
    # Superseded artefacts: present for history, not active.
    "privacy/annex-regional-privacy-requirements.md",
}

# Directories whose contents are exempt from the structural-membership rule.
# Phase 23.62 removed `tools/` and `docs/` because the per-domain walk
# (`iter_domain_files`) is restricted to the DOMAINS list and never
# reaches those directories.
EXEMPT_DIRECTORY_PREFIXES = (
    "dev-security/claude-rules/",
)

LINK_TARGET_RE = re.compile(r"\[`([^`]+)`\]\(([^)]+)\)")


def iter_domain_files(domain: str) -> list[Path]:
    base = REPO_ROOT / domain
    if not base.is_dir():
        return []
    files = []
    for f in base.rglob("*.md"):
        rel = f.relative_to(REPO_ROOT).as_posix()
        if f.name == "README.md":
            continue
        if rel in EXEMPT_FROM_INDEX:
            continue
        if any(rel.startswith(p) for p in EXEMPT_DIRECTORY_PREFIXES):
            continue
        files.append(f)
    return sorted(files)


def parse_referenced_paths(text: str) -> set[str]:
    """Return the set of repository-relative paths referenced by markdown links."""
    refs = set()
    for m in LINK_TARGET_RE.finditer(text):
        display = m.group(1)
        if display.endswith(".md"):
            refs.add(display)
    return refs


def main(argv: list[str]) -> int:
    global REPO_ROOT
    parser = argparse.ArgumentParser(
        description="Structural index integrity checker."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Override repository root (for isolation testing).",
    )
    args = parser.parse_args(argv[1:])
    if args.root is not None:
        REPO_ROOT = args.root.resolve()

    findings: list[str] = []

    # Load the canonical index register text once.
    index_path = REPO_ROOT / "governance" / "register-document-index-and-classification.md"
    if not index_path.exists():
        print(f"FAIL: {index_path} not found.")
        return 1
    index_text = index_path.read_text(encoding="utf-8")
    indexed = parse_referenced_paths(index_text)

    # Check that every active document is in the index register.
    for domain in DOMAINS:
        for f in iter_domain_files(domain):
            rel = f.relative_to(REPO_ROOT).as_posix()
            if rel not in indexed:
                findings.append(f"index miss: {rel} not referenced by governance/register-document-index-and-classification.md")

    # Check that every active document is in its domain README.
    for domain in DOMAINS:
        readme = REPO_ROOT / domain / "README.md"
        if not readme.exists():
            findings.append(f"missing README: {domain}/README.md")
            continue
        readme_refs = parse_referenced_paths(readme.read_text(encoding="utf-8"))
        for f in iter_domain_files(domain):
            rel = f.relative_to(REPO_ROOT).as_posix()
            if rel not in readme_refs:
                findings.append(f"domain README miss: {rel} not referenced by {domain}/README.md")

    # Verify referenced paths in the index actually exist on disk.
    for ref in indexed:
        target = REPO_ROOT / ref
        if not target.exists():
            findings.append(f"index broken: governance/register-document-index-and-classification.md "
                            f"references non-existent {ref}")

    # Verify referenced paths in each domain README actually exist on disk.
    for domain in DOMAINS:
        readme = REPO_ROOT / domain / "README.md"
        if not readme.exists():
            continue
        for ref in parse_referenced_paths(readme.read_text(encoding="utf-8")):
            target = REPO_ROOT / ref
            if not target.exists():
                findings.append(f"README broken: {domain}/README.md references non-existent {ref}")

    if not findings:
        print("OK: no structural findings.")
        return 0

    grouped = defaultdict(list)
    for f in findings:
        category = f.split(":", 1)[0]
        grouped[category].append(f)
    for cat in sorted(grouped):
        print(f"=== {cat} ===")
        for f in grouped[cat]:
            print(f"  {f}")

    print(f"\nFAIL: {len(findings)} structural finding(s).")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
