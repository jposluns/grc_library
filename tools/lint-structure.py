#!/usr/bin/env python3
"""Structural index-integrity checker - grc wrapper over the pack-owned engine.

Verify that every active domain document is referenced by the central document-index
register AND by its own domain README, and that every path those two surfaces
reference exists on disk.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE check
(parse_referenced_paths, iter_domain_files, collect_findings) lives in the
pack-owned engine (.corpus-management/tools/gate_lint_structure.py, source of
record), fully parameterized by repo_root + the corpus structure config. This
wrapper supplies the grc domain list, the grc index-register relative path, the grc
exempt sets, and the --root handling and grouped reporting.
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PACK_TOOLS = REPO_ROOT / ".corpus-management" / "tools"

DOMAINS = [
    "ai",
    "architecture",
    "compliance",
    "crypto",
    "dev-security",
    "governance",
    "operations",
    "privacy",
    "resilience",
    "risk",
    "security",
    "supply-chain",
]

# The central document-index register, relative to the repository root.
INDEX_REL_PATH = "governance/register-document-index-and-classification.md"

# Files explicitly exempt from the structural-membership requirement.
EXEMPT_FROM_INDEX = {
    # Superseded artefacts: present for history, not active.
    "privacy/annex-regional-privacy-requirements.md",
}

# Directories whose contents are exempt from the structural-membership rule.
EXEMPT_DIRECTORY_PREFIXES = (
    "guardrails/",
)


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_structure  # the pack-owned engine (source of record)
    return gate_lint_structure


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

    eng = _engine()

    # Terminal case: the central index register is missing.
    index_path = REPO_ROOT / INDEX_REL_PATH
    if not index_path.exists():
        print(f"FAIL: {index_path} not found.")
        return 1

    findings = eng.collect_findings(
        REPO_ROOT,
        DOMAINS,
        INDEX_REL_PATH,
        EXEMPT_FROM_INDEX,
        EXEMPT_DIRECTORY_PREFIXES,
    )

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
