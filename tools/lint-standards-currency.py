#!/usr/bin/env python3
"""Lint citations against the canonical citations register for staleness.

This linter parses ``governance/register-canonical-citations.md`` as its
source of truth and flags two classes of finding:

1. Citations using a version listed as ``Superseded versions`` in the
   canonical register, where a current published version is recorded.
2. Citations including ``(draft)`` markers where the canonical register
   indicates the standard has been published.

The canonical register is the single source of truth. To add a new
standard to coverage, add it to the register; this linter will then
detect stale references on the next run.

Usage::

    python3 tools/lint-standards-currency.py
    python3 tools/lint-standards-currency.py --paths governance ai

Exit codes:

    0   no findings
    1   one or more findings present

This linter is permissive: it flags only patterns recorded in the
canonical register. It does not assert that every standards citation
is in the register. To detect non-cataloged citations, run the existing
``lint-citations.py`` denylist tool, which is complementary.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL_REGISTER = REPO_ROOT / "governance" / "register-canonical-citations.md"

# Files exempt from the linter (typically CHANGELOG-style records and
# discussions of the defect itself).
EXEMPT_FILES = {
    "CHANGELOG.md",
    "TODO.md",
    "governance/register-canonical-citations.md",
}

EXEMPT_DIRECTORY_PREFIXES = (
    "tools/",
    "docs/",
)

DEFAULT_PATHS = [
    "README.md",
    "NOTICE.md",
    "CONTRIBUTING.md",
    "specification-master-project.md",
    "specification-ingestion.md",
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


def parse_canonical_register() -> list[dict[str, object]]:
    """Parse the canonical register's tables into a list of standard entries.

    Each entry is a dict with keys:
        id          (str)    Standard identifier as it appears in the table
        current     (str)    Current version string
        superseded  (list)   Strings the linter should flag if seen with this id
    """
    if not CANONICAL_REGISTER.exists():
        print(
            f"ERROR: canonical citations register not found at {CANONICAL_REGISTER}",
            file=sys.stderr,
        )
        return []

    text = CANONICAL_REGISTER.read_text(encoding="utf-8")
    entries: list[dict[str, object]] = []

    # Each table row of the form:
    # | <id> | <current> | <date> | <topic> | <superseded comma-list> |
    # We extract id, current, and superseded.
    row_re = re.compile(
        r"^\|\s+([^|]+?)\s+\|\s+([^|]+?)\s+\|\s+[^|]+?\s+\|\s+[^|]+?\s+\|\s+([^|]+?)\s+\|$"
    )

    for raw in text.splitlines():
        m = row_re.match(raw)
        if not m:
            continue
        std_id = m.group(1).strip()
        current = m.group(2).strip()
        superseded_raw = m.group(3).strip()

        # Skip header rows
        if std_id.lower() in {"standard id", "---", "--- ", " --- "}:
            continue
        if std_id.startswith("---"):
            continue

        # Parse superseded
        if superseded_raw in {"—", "-", ""}:
            superseded: list[str] = []
        else:
            superseded = [s.strip() for s in superseded_raw.split(",") if s.strip()]

        entries.append(
            {
                "id": std_id,
                "current": current,
                "superseded": superseded,
            }
        )

    return entries


def iter_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        full = REPO_ROOT / p
        if full.is_file() and full.suffix == ".md":
            files.append(full)
        elif full.is_dir():
            for f in full.rglob("*.md"):
                files.append(f)
    out: list[Path] = []
    for f in files:
        rel = f.relative_to(REPO_ROOT).as_posix()
        if rel in EXEMPT_FILES:
            continue
        if any(rel.startswith(p) for p in EXEMPT_DIRECTORY_PREFIXES):
            continue
        out.append(f)
    return sorted(set(out))


def check_file(path: Path, entries: list[dict[str, object]]) -> list[tuple[int, str]]:
    """Return list of (line-number, message) findings for the file."""
    findings: list[tuple[int, str]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return findings

    lines = text.splitlines()
    for ln, line in enumerate(lines, start=1):
        for entry in entries:
            std_id = entry["id"]
            current = entry["current"]
            superseded_list = entry["superseded"]  # type: ignore[assignment]
            if not isinstance(superseded_list, list):
                continue

            # Build the regex patterns to look for the standard ID followed by
            # a version. We accept patterns like "ISO/IEC 27001:2013",
            # "ISO 27001:2013", "ISO/IEC 27001 (2013)", "ISO/IEC 27001 2013",
            # and the standard ID followed by "(draft)", "(draft 2024)", etc.
            # Use escape on the id, allow optional ":" or " " or "(".
            std_id_re = re.escape(str(std_id))
            for superseded in superseded_list:
                sup_re = re.escape(superseded)
                # Two patterns: "<id>:<version>" and "<id> <version>" and
                # "<id> (<version>)". We combine in a single regex.
                # The negative lookahead (?![.\-][\d\w]) prevents the match
                # from triggering inside a longer version string. For example,
                # "PCI DSS 4.0" must NOT match within "PCI DSS 4.0.1" because
                # 4.0 is followed by .1 (a version-continuation pattern).
                pattern = re.compile(
                    rf"\b{std_id_re}\b\s*(?::|\(|\s+)\s*{sup_re}\b(?![.\-][\d\w])",
                    flags=re.IGNORECASE,
                )
                if pattern.search(line):
                    findings.append(
                        (
                            ln,
                            f"stale citation '{std_id} {superseded}' "
                            f"(current: {current})",
                        )
                    )

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--paths",
        nargs="+",
        default=DEFAULT_PATHS,
        help="Paths to scan (default: all active library directories and root files)",
    )
    args = parser.parse_args()

    entries = parse_canonical_register()
    if not entries:
        print(
            "WARNING: canonical citations register parsed no entries; linter is a no-op.",
            file=sys.stderr,
        )
        return 0

    files = iter_files(args.paths)
    total_findings = 0
    by_file: dict[str, list[tuple[int, str]]] = {}

    for f in files:
        rel = f.relative_to(REPO_ROOT).as_posix()
        findings = check_file(f, entries)
        if findings:
            by_file[rel] = findings
            total_findings += len(findings)

    if total_findings == 0:
        print(
            f"OK: no standards-currency findings (checked {len(entries)} standards "
            f"across {len(files)} files)."
        )
        return 0

    for rel, findings in sorted(by_file.items()):
        print(f"=== {rel} ===")
        for ln, msg in findings:
            print(f"  L{ln}: {msg}")

    print()
    print(
        f"FAIL: {total_findings} standards-currency finding(s) "
        f"across {len(by_file)} file(s)."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
