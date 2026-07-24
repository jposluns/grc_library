#!/usr/bin/env python3
"""Rule-scope-table completeness audit (gate 74; TODO section 1.18 PR-2).

The pack README's "Rule files and their scope" table
(``dev-security/claude-rules/README.md``) is exhaustive by design: it lists
every pack rule file (``core`` / ``ai`` / ``pipeline`` / ``governance`` /
``languages``) with its when-to-use. It is a rule-enumeration surface gate 41
does not cover: gate 41 (collection-enumeration consistency) checks the
directory tree, the two CLAUDE.md bullet lists, and (since the section 3.56a
guard-3 addition) the rule-provenance register, not this table, so a new
rule silently misses a row (the 14th governance rule
``decision-classification-before-enacting`` was added with no scope-table row).

This gate closes that surface. It compares the table's rows to the on-disk rule
files and flags a MISSING row (a rule file with no row) or an EXTRA row (a row
whose target is not a rule file under the category subdirs).

Scope and precision (precision-first: the gate never false-PASSES a real
missing or extra row; a malformed table may over-strictly false-FAIL, which is
the safe direction and does not occur on the well-formed live table):

  * It reads ONLY the "Rule files and their scope" table region: from the exact
    heading line ``## Rule files and their scope``, through the
    ``| File | When to Use |`` header, until the next ``---`` / ``## `` / a
    non-table line. This excludes the version-history table (which links rule
    files heavily in its prose cells) and the directory tree (which names every
    rule, including one absent from the scope table), so a rule mentioned
    elsewhere in the README but missing from this table is still flagged.
  * A row keys to a rule file by its FIRST cell's backticked link only
    (``| [`governance/x.md`](governance/x.md) | ... |`` gives ``governance/x.md``).
    A second link inside the When-to-Use cell (several ``languages`` rows link
    the mobile-security standard, and the capacitor-ionic row links two more) is
    never read, so it cannot mis-key a row.
  * The EXPECTED set is every ``<root>/<category>/*.md`` for the five categories
    (``core`` / ``ai`` / ``pipeline`` / ``governance`` / ``languages``), keyed as
    ``<category>/<file>.md``, excluding a ``README.md`` basename (a category
    subdir never carries a table row). Top-level standalone files
    (``rule-provenance.md`` and similar) are NOT rule files and are NOT expected;
    a row pointing at one is reported EXTRA.
  * PRESENCE only, never order: the rows may be regrouped freely.

Exit codes: 0 the table lists exactly the on-disk rule set; 1 MISSING/EXTRA
findings; 2 environment error (no README under --root, or the table not found).

Single-surface: the scope table lives only in the pack README, not the
``.claude/`` mirror, so there is no gate-37 dual-tree implication.

Stdlib-only (gate 71). Python 3.11.

Usage:
    python3 tools/lint-rule-scope-table.py [--root DIR]

``--root`` defaults to ``dev-security/claude-rules`` (the dir holding README.md
and the category subdirs); the regression fixtures pass a synthetic root.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lint_common import REPO_ROOT

CATEGORY_DIRS = ("core", "ai", "pipeline", "governance", "languages")
DEFAULT_ROOT = REPO_ROOT / "dev-security" / "claude-rules"
SCOPE_HEADING = "## Rule files and their scope"
TABLE_HEADER_RE = re.compile(r"^\|\s*File\s*\|\s*When to Use\s*\|\s*$")
# First-cell backticked link only: matches the File column, never a When-to-Use link.
# Leading whitespace is tolerated so an indented row keys consistently with the
# `.strip()`-based region terminator below (no over-strict false-FAIL on an indented row).
ROW_LINK_RE = re.compile(r"^\s*\|\s*\[`([^`]+)`\]")


def _is_separator(line: str) -> bool:
    """True for a markdown table separator row (only |, -, :, spaces)."""
    return line.strip().startswith("|") and set(line.strip()) <= set("|-: ")


def scope_rows(readme_text: str):
    """Return the set of first-cell link targets in the scope table, or None if
    the table cannot be located (an environment/structure error the caller
    reports as exit 2). The scan is bounded to the table region."""
    lines = readme_text.splitlines()
    n = len(lines)
    i = 0
    while i < n and lines[i].strip() != SCOPE_HEADING:
        i += 1
    if i >= n:
        return None
    # advance to the header row, but stop if the next section starts first
    i += 1
    while i < n and not TABLE_HEADER_RE.match(lines[i]):
        if lines[i].startswith("## "):
            return None
        i += 1
    if i >= n:
        return None
    i += 1  # consume the header row
    if i < n and _is_separator(lines[i]):
        i += 1  # consume the separator row
    rows = set()
    while i < n:
        stripped = lines[i].strip()
        if stripped.startswith("## ") or stripped == "---" or not stripped.startswith("|"):
            break
        m = ROW_LINK_RE.match(lines[i])
        if m:
            rows.add(m.group(1).strip())
        i += 1
    return rows


def on_disk_rules(root: Path) -> set[str]:
    """Expected set: <root>/<category>/*.md as '<category>/<file>.md', excluding
    a README.md basename."""
    expected: set[str] = set()
    for cat in CATEGORY_DIRS:
        d = root / cat
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.md")):
            if p.name == "README.md":
                continue
            expected.add(f"{cat}/{p.name}")
    return expected


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--root", default=str(DEFAULT_ROOT),
        help="claude-rules dir holding README.md and the category subdirs")
    args = ap.parse_args(argv[1:])
    root = Path(args.root)
    readme = root / "README.md"
    if not readme.is_file():
        print(f"ERROR: no README.md under --root {root}", file=sys.stderr)
        return 2
    rows = scope_rows(readme.read_text(encoding="utf-8"))
    if rows is None:
        print(f"ERROR: '{SCOPE_HEADING}' table not found in {readme}",
              file=sys.stderr)
        return 2
    expected = on_disk_rules(root)
    missing = sorted(expected - rows)
    extra = sorted(rows - expected)
    if not missing and not extra:
        print(f"OK: the 'Rule files and their scope' table lists all "
              f"{len(expected)} rule files (no missing or extra rows).")
        return 0
    for m in missing:
        print(f"[scope-table] MISSING: rule file {m} has no row in the "
              f"'Rule files and their scope' table")
    for e in extra:
        print(f"[scope-table] EXTRA: table row {e} is not an on-disk rule file "
              f"under the category subdirs")
    print(f"\nFAIL: {len(missing)} missing, {len(extra)} extra row(s) "
          f"({readme}).", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
