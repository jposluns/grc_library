#!/usr/bin/env python3
"""Verify a pull request introduces no em dashes or en dashes in newly-added CHANGELOG.md lines.

This is a CI-only delta gate (D3), not part of the corpus audit programme. The
corpus gates check repository state at HEAD; this script compares HEAD to the
PR's merge-base and inspects only the lines the PR ADDS to CHANGELOG.md, failing
if any added line contains an em dash (U+2014) or en dash (U+2013).

Rationale (DD-1, 2026-06-23): the prose convention forbids em dashes and en dashes
(see tools/lint-language.py), but CHANGELOG.md is deliberately outside that
whole-file linter's scan set because its ~1500 lines of append-only historical
entries accumulated ~130 dashes before the convention was enforced, and rewriting
historical entries risks altering their meaning. This delta gate enforces the
convention going forward on NEW entries only, leaving history untouched: a PR's
added CHANGELOG lines must use commas, colons, or parentheses instead of dashes.

Scope: root CHANGELOG.md only. The detailed mirror at
.working/changelog-details/CHANGELOG-detailed.md is maintainer working state,
exempt from the corpus gates, and is not checked here.

Usage:
    # In CI (uses GITHUB_BASE_REF):
    python3 tools/check-changelog-dash-on-pr.py

    # Locally, comparing HEAD to a specific base:
    python3 tools/check-changelog-dash-on-pr.py origin/main
    python3 tools/check-changelog-dash-on-pr.py origin/main HEAD

Exit codes:
    0 : no em/en dashes in added CHANGELOG.md lines, or the diff does not touch it.
    1 : one or more added CHANGELOG.md lines contain an em dash or en dash.
    2 : invocation or environment error (cannot determine base/head, git failure).
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

CHANGELOG_PATH = "CHANGELOG.md"
DASH_PATTERN = re.compile(r"[—–]")  # em dash or en dash


def git(*args: str) -> str:
    """Run `git <args>` and return stdout, stripped. Raises on non-zero exit."""
    return subprocess.check_output(["git", *args], text=True).strip()


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check that a pull request introduces no em/en dashes in newly-added "
            "CHANGELOG.md lines (DD-1 new-entries-only delta gate)."
        ),
    )
    parser.add_argument(
        "base",
        nargs="?",
        help=(
            "Base ref to diff against (default: origin/$GITHUB_BASE_REF in CI; "
            "must be supplied explicitly when running locally)."
        ),
    )
    parser.add_argument(
        "head",
        nargs="?",
        default="HEAD",
        help="Head ref (default: HEAD).",
    )
    args = parser.parse_args(argv[1:])

    base = args.base
    if not base:
        github_base = os.environ.get("GITHUB_BASE_REF")
        if not github_base:
            print(
                "ERROR: base ref not provided and GITHUB_BASE_REF is unset. "
                "Pass a base ref as the first positional argument when running "
                "locally (e.g. origin/main).",
                file=sys.stderr,
            )
            return 2
        base = f"origin/{github_base}"

    head = args.head

    try:
        merge_base = git("merge-base", base, head)
    except subprocess.CalledProcessError as exc:
        print(
            f"ERROR: could not determine merge-base of {base}..{head}: {exc}. "
            f"In GitHub Actions, ensure that actions/checkout uses fetch-depth: 0.",
            file=sys.stderr,
        )
        return 2

    # Unified diff of CHANGELOG.md only, zero context, so every '+' line is a
    # genuine addition (not a context line).
    try:
        diff = git("diff", "--unified=0", merge_base, head, "--", CHANGELOG_PATH)
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git diff failed: {exc}", file=sys.stderr)
        return 2

    if not diff:
        print(f"OK: {CHANGELOG_PATH} not modified between {merge_base[:8]} and {head}.")
        return 0

    offending: list[str] = []
    for line in diff.splitlines():
        # Added content lines start with a single '+' (the file header is '+++').
        if line.startswith("+") and not line.startswith("+++"):
            added = line[1:]
            if DASH_PATTERN.search(added):
                offending.append(added.strip())

    if not offending:
        print(f"OK: no em/en dashes in added {CHANGELOG_PATH} lines.")
        return 0

    print(
        f"FAIL: {len(offending)} newly-added {CHANGELOG_PATH} line(s) contain an "
        f"em dash or en dash. Replace with a comma, colon, or parentheses "
        f"(the prose convention forbids em/en dashes; historical entries are "
        f"exempt, new ones are not):",
        file=sys.stderr,
    )
    for added in offending:
        print(f"  {added[:160]}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
