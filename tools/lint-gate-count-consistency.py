#!/usr/bin/env python3
"""Cross-file gate-count consistency audit for the audit programme.

The audit programme declares its current gate count in the §6 inventory
table of governance/specification-audit-programme.md (one row per gate).
Many other files in the corpus reference that count in prose: "the N
audit gates", "N-gate audit programme", "gates 1-N", and similar
idioms. When a new gate is added, the §6 inventory grows by one row,
but the prose references elsewhere are easy to miss; the failure mode
surfaced in the PR #59 / PR #61 / PR #63 sequence (each pass missed a
different set of references).

This linter scans the corpus for prose phrases that mention a gate
count and verifies the count matches the §6 inventory's row count. Any
mismatch is flagged.

Patterns scanned (case-insensitive):

  P1  ``N-gate``                   matches hyphenated forms ``X-gate``
  P2  ``N audit gates``            matches ``the X audit gates``
  P3  ``gates 1-N`` / ``gates 1--N`` (also handles en-dashes)
  P4  ``gates 1 through N``
  P5  ``all N gates``

Captured ``N`` is compared to the canonical count from §6. Mismatch
means the prose was not updated when a gate was added or retired.

Scope: ``*.md``, ``*.py``, ``*.sh`` files under the repository root,
minus the exempt set (CHANGELOG.md, generated artefacts, regression
fixtures that intentionally embed stale counts).

Exit codes: 0 pass, 1 findings, 2 internal error (canonical §6 not
parseable).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import NamedTuple

from lint_common import DEFAULT_EXEMPT_DIRS, REPO_ROOT, read_text_safe


SPEC_PATH = REPO_ROOT / "governance" / "specification-audit-programme.md"

# Files that legitimately contain stale gate-count references and must
# not be flagged. CHANGELOG.md is the corpus's historical record;
# generated artefacts are derived; the regression-test fixtures
# intentionally embed wrong-N strings to exercise the linter itself.
EXEMPT_FILES: frozenset[str] = frozenset(
    {
        "CHANGELOG.md",
        "taxonomy.yml",
        "docs/portal.md",
        "docs/maturity-scorecard.md",
        "tests/test_linters.py",
    }
)

# Directories whose contents are out of scope for this audit. The
# pack's tests and fixtures may also embed sample counts.
EXEMPT_DIRS: frozenset[str] = DEFAULT_EXEMPT_DIRS | frozenset(
    {"tests/fixtures"}
)

# File suffixes the linter scans. Markdown is the primary surface;
# Python and shell scripts are included because their docstrings and
# top-of-file comments frequently cite the gate count.
SCAN_SUFFIXES: frozenset[str] = frozenset({".md", ".py", ".sh"})


# Patterns: each is a compiled regex with one capturing group for the
# numeric count. Patterns are matched against non-code-block prose
# only (fenced code blocks would carry too many false positives, e.g.
# scripts referencing test-fixture counts in code comments).
PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("N-gate", re.compile(r"\b(\d+)-gate\b", re.IGNORECASE)),
    ("N audit gates", re.compile(r"\b(\d+)\s+audit\s+gates?\b", re.IGNORECASE)),
    (
        "gates 1-N",
        re.compile(r"\bgates?\s+1[-–—]\s*(\d+)\b", re.IGNORECASE),
    ),
    (
        "gates 1 through N",
        re.compile(r"\bgates?\s+1\s+through\s+(\d+)\b", re.IGNORECASE),
    ),
    ("all N gates", re.compile(r"\ball\s+(\d+)\s+gates?\b", re.IGNORECASE)),
    # P6: bare "<two-digit number> gates" without preceding qualifier.
    # Narrower than the other patterns and added after a Sweep finding
    # in tools/README.md where prose used a bare "<stale-count> gates"
    # phrasing without an "audit" or "all" qualifier; patterns P1-P5
    # missed it. Requires the captured number to be at least 10 (two
    # digits) to avoid matching small physical-gate references that
    # may legitimately appear (e.g. "5 gates of NAND").
    ("N gates", re.compile(r"\b(\d{2,})\s+gates?(?![-\w])", re.IGNORECASE)),
]


class Finding(NamedTuple):
    path: Path
    line: int
    pattern_name: str
    captured: int
    expected: int
    text: str


def parse_canonical_count() -> int:
    """Parse §6 inventory of the audit-programme spec and return the
    row count.

    The §6 inventory is a markdown table with one row per audit gate.
    The header row is ``| # | Gate | Script |`` followed by a
    separator row of dashes. Data rows have numeric first cells.

    Raises ``RuntimeError`` if the inventory cannot be located or
    parsed.
    """
    text = read_text_safe(SPEC_PATH)
    if text is None:
        raise RuntimeError(f"cannot read {SPEC_PATH}")
    lines = text.splitlines()

    # Locate the §6 inventory header.
    inventory_start = None
    for lineno, line in enumerate(lines):
        if line.strip().startswith("## 6.") and "inventory" in line.lower():
            inventory_start = lineno
            break
    if inventory_start is None:
        raise RuntimeError("§6 inventory header not found in spec")

    # Find the table header row after the §6 header. The header row
    # starts with ``| #`` and contains the column ``Gate``.
    table_start = None
    for lineno in range(inventory_start, len(lines)):
        line = lines[lineno].strip()
        if line.startswith("| #") and "Gate" in line:
            table_start = lineno
            break
    if table_start is None:
        raise RuntimeError("§6 inventory table header not found")

    # Count data rows: after the header and the separator row, each
    # subsequent line beginning with ``|`` and a digit is a data row.
    # Stop at the first non-table line.
    count = 0
    for lineno in range(table_start + 2, len(lines)):
        line = lines[lineno].strip()
        if not line.startswith("|"):
            break
        # First cell is the gate number. Strip the leading ``|`` and
        # whitespace, then check the cell is numeric.
        first_cell = line.split("|", 2)[1].strip() if line.count("|") >= 2 else ""
        if first_cell.isdigit():
            count += 1
        else:
            break
    if count == 0:
        raise RuntimeError("§6 inventory has zero data rows")
    return count


def iter_targets(paths: list[str]) -> list[Path]:
    """Yield scannable files. ``paths`` is a list of repo-relative or
    absolute paths; if a path is a directory, it is walked recursively.
    If ``paths`` is empty, the entire repository root is walked. Exempt
    files and directories are skipped in either mode."""
    targets: list[Path] = []
    seen: set[Path] = set()

    def consider(path: Path) -> None:
        if not path.is_file():
            return
        if path.suffix not in SCAN_SUFFIXES:
            return
        try:
            rel = path.resolve().relative_to(REPO_ROOT).as_posix()
            parts = set(path.resolve().relative_to(REPO_ROOT).parts)
        except ValueError:
            # Path is outside the repo (e.g. a temporary fixture).
            rel = path.as_posix()
            parts = set(path.parts)
        if parts & EXEMPT_DIRS:
            return
        if rel in EXEMPT_FILES:
            return
        if path.resolve() in seen:
            return
        targets.append(path.resolve())
        seen.add(path.resolve())

    roots = [Path(p) for p in paths] if paths else [REPO_ROOT]
    for root in roots:
        root = root.resolve() if root.exists() else root
        if root.is_file():
            consider(root)
        elif root.is_dir():
            for path in root.rglob("*"):
                consider(path)
    return sorted(targets)


def scan_file(path: Path, expected: int) -> list[Finding]:
    """Apply all patterns to a single file's text, returning findings."""
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[Finding] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for pattern_name, pattern in PATTERNS:
            for match in pattern.finditer(line):
                captured = int(match.group(1))
                if captured == expected:
                    continue
                findings.append(
                    Finding(
                        path=path,
                        line=lineno,
                        pattern_name=pattern_name,
                        captured=captured,
                        expected=expected,
                        text=line.strip(),
                    )
                )
    return findings


def main(argv: list[str]) -> int:
    try:
        expected = parse_canonical_count()
    except RuntimeError as exc:
        print(f"ERROR: cannot determine canonical gate count: {exc}", file=sys.stderr)
        return 2

    paths = argv[1:]
    targets = iter_targets(paths)
    all_findings: list[Finding] = []
    for path in targets:
        all_findings.extend(scan_file(path, expected))

    if not all_findings:
        print(
            f"OK: gate-count references consistent with §6 inventory "
            f"({expected} gates) across {len(targets)} files."
        )
        return 0

    # Group findings by file for readable output.
    by_file: dict[Path, list[Finding]] = {}
    for finding in all_findings:
        by_file.setdefault(finding.path, []).append(finding)
    for path in sorted(by_file):
        rel = path.relative_to(REPO_ROOT).as_posix()
        print(f"=== {rel} ===")
        for finding in by_file[path]:
            print(
                f"  L{finding.line} [{finding.pattern_name}] "
                f"captured {finding.captured}, expected {finding.expected}: "
                f"{finding.text[:120]}"
            )
    print(
        f"\nFAIL: {len(all_findings)} stale gate-count reference(s) across "
        f"{len(by_file)} file(s).",
        file=sys.stderr,
    )
    print(
        f"The §6 inventory of {SPEC_PATH.relative_to(REPO_ROOT)} "
        f"declares {expected} gates. Each finding above shows a prose "
        f"reference that does not match. Update the prose to the "
        f"current count.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
