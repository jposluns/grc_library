#!/usr/bin/env python3
"""Version-date consistency audit for the library CHANGELOG and README.

This linter enforces two invariants about the library's CalVer
(``YYYY.MM.patch``) version recorded in [README.md] and the dated
section headings in [CHANGELOG.md]:

  1. The most recent CHANGELOG section heading (matching the pattern
     ``## YYYY-MM-DD, Library Version YYYY.MM.patch``) has a date whose
     ``YYYY-MM`` equals the library version's ``YYYY.MM``.

  2. The current README.md ``**Library Version:**`` field equals the
     library version recorded in the most recent CHANGELOG heading.

Why both invariants are needed:

The first invariant catches the failure mode where an author dates a
CHANGELOG entry for today's calendar date but carries over the prior
month's ``YYYY.MM`` in the library version. This is what happened on
2026-06-01 when six successive phases used ``2026.05.x`` while every
entry was dated ``2026-06-01``; the existing version-monotonicity
audit treats ``2026.05.x`` as monotonic (tuple comparison) and does
not validate the month against the entry's date. Per
``specification-master-project.md`` section 4.5, ``YYYY.MM`` is the
year and month of the most recent merge to ``main`` and ``patch``
resets to 0 when the month rolls over.

The second invariant catches the drift case where the README's
``**Library Version:**`` is bumped without a CHANGELOG entry, or a
CHANGELOG entry is added with a higher version than the README
records. Both halves must agree because the README is the
adopter-facing snapshot pointer and the CHANGELOG is the audit trail
that explains how the snapshot got to this state.

Usage:

    python3 tools/lint-version-date-consistency.py
    python3 tools/lint-version-date-consistency.py \\
        --changelog tests/tmp/fake-changelog.md \\
        --readme tests/tmp/fake-readme.md

The ``--changelog`` and ``--readme`` flags override the default
file locations (``CHANGELOG.md`` and ``README.md`` at the repo root)
and are used by the gate-35 regression test suite for synthetic
fixtures.

Exit codes:
    0 - both invariants hold (or the CHANGELOG has no Library Version
        headings yet, treated as a pass-with-note).
    1 - one or more inconsistency findings.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Heading shape:  ## YYYY-MM-DD, Library Version YYYY.MM.patch
CHANGELOG_HEADING_RE = re.compile(
    r"^##\s+(\d{4})-(\d{2})-(\d{2}),\s+Library Version\s+(\d+)\.(\d+)\.(\d+)\s*$",
    re.MULTILINE,
)

# README field: **Library Version:** YYYY.MM.patch
README_VERSION_RE = re.compile(
    r"\*\*Library Version:\*\*\s+(\d+)\.(\d+)\.(\d+)"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify CHANGELOG entry dates match their Library Version YYYY.MM "
        "and that the README's Library Version matches the most recent CHANGELOG entry."
    )
    parser.add_argument(
        "--changelog",
        default=str(REPO_ROOT / "CHANGELOG.md"),
        help="Path to the CHANGELOG file (default: repo root CHANGELOG.md).",
    )
    parser.add_argument(
        "--readme",
        default=str(REPO_ROOT / "README.md"),
        help="Path to the README file (default: repo root README.md).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    changelog_path = Path(args.changelog)
    readme_path = Path(args.readme)
    findings: list[str] = []

    try:
        changelog_text = changelog_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: cannot read changelog at {changelog_path}: {exc}", file=sys.stderr)
        return 1
    try:
        readme_text = readme_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: cannot read readme at {readme_path}: {exc}", file=sys.stderr)
        return 1

    # Find the FIRST (most recent) Library-Version heading in the CHANGELOG.
    first_match = CHANGELOG_HEADING_RE.search(changelog_text)
    if not first_match:
        print(
            f"OK: no Library Version section heading found in "
            f"{changelog_path.name}; nothing to verify."
        )
        return 0

    date_y, date_m, date_d = (int(first_match.group(i)) for i in (1, 2, 3))
    ver_y, ver_m, ver_p = (int(first_match.group(i)) for i in (4, 5, 6))

    # Invariant 1: the entry's date YYYY-MM must equal the version's YYYY.MM.
    # Rationale: specification-master-project.md section 4.5 defines YYYY.MM
    # as the year and month of the merge to main. The CHANGELOG heading
    # date is the source of truth for "when this happened"; the version
    # must agree.
    if (date_y, date_m) != (ver_y, ver_m):
        findings.append(
            f"{changelog_path.name}: most recent entry is dated "
            f"{date_y:04d}-{date_m:02d}-{date_d:02d} but the Library "
            f"Version is {ver_y}.{ver_m:02d}.{ver_p}; the YYYY-MM portion "
            f"of the date and the YYYY.MM portion of the version must "
            f"match per specification-master-project.md section 4.5."
        )

    # Invariant 2: README's Library Version equals the most recent CHANGELOG
    # entry's version. The README is the canonical "current snapshot" pointer.
    readme_match = README_VERSION_RE.search(readme_text)
    if not readme_match:
        findings.append(
            f"{readme_path.name}: no '**Library Version:** YYYY.MM.patch' "
            f"field found in the metadata block."
        )
    else:
        rl_y, rl_m, rl_p = (int(readme_match.group(i)) for i in (1, 2, 3))
        if (rl_y, rl_m, rl_p) != (ver_y, ver_m, ver_p):
            findings.append(
                f"{readme_path.name} records Library Version "
                f"{rl_y}.{rl_m:02d}.{rl_p}, but the most recent "
                f"{changelog_path.name} entry uses "
                f"{ver_y}.{ver_m:02d}.{ver_p}; the two must agree."
            )

    if not findings:
        return 0

    print(f"=== {changelog_path.name} / {readme_path.name} ===")
    for finding in findings:
        print(f"  {finding}")
    print(
        f"\nFAIL: {len(findings)} version-date inconsistency finding(s). "
        f"See specification-master-project.md section 4.5 for the CalVer rule."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
