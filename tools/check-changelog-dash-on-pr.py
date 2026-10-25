#!/usr/bin/env python3
"""Verify a pull request introduces no em dashes or en dashes in newly-added CHANGELOG.md lines.

This is a PR-time delta gate (D3), not part of the corpus audit programme (it runs in quality.yml on pull_request and locally via the pre-push guard). The
corpus gates check repository state at HEAD; this script compares HEAD to the
PR's merge-base and inspects only the lines the PR ADDS to CHANGELOG.md, failing
if any added line contains an em dash (U+2014) or en dash (U+2013).

The root CHANGELOG.md is also in tools/lint-language.py's default whole-file
scan set. This delta gate retains the PR-diff check introduced for DD-1
(2026-06-23): it rejects em/en dashes anywhere in added lines, including in
code that the language gate skips. Historical lines are outside this delta
check, but remain covered by the language gate under its normal rules.

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
    2 : invocation or environment error (cannot determine base/head, git failure,
        a diff the shared parser cannot read exactly, a CHANGELOG.md that is a
        symbolic link or a submodule in the head or the diff, or git selecting
        another repository or work tree than it finds by itself), or
        CANNOT-EVALUATE: base and head resolve to the same commit (a collapsed,
        empty range), so nothing was evaluated.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import PrRangeError, resolve_pr_range  # noqa: E402  # grc-config/store, stays local
from changelog_diff import (  # noqa: E402  # shared added-line diff reader (3b399)
    ChangelogDiffUnreadable, GitQueryFailed, GitSelectsAnotherTree, added_line_diff,
    check_git_selects_root, parse_added_lines, refuse_links)

CHANGELOG_PATH = "CHANGELOG.md"
DASH_PATTERN = re.compile(r"[\u2014\u2013]")  # em dash or en dash


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

    # Unified diff of CHANGELOG.md only, zero context, read by the shared pinned
    # diff and hunk-count parser (3b399): each hunk by its header's line counts and
    # the bytes split on LF only, so an added line whose text starts with "++" is
    # read, and a CR, U+2028 or U+0085 inside an added line does not split it. The
    # ":(top)" pathspec names the root CHANGELOG.md from any subdirectory (3b399 round 3);
    # the runner drops GIT_LITERAL_PATHSPECS, which made git read it as a file name (round 4).
    # git must select the repository it finds by itself (a sibling GIT_DIR printed "not
    # modified"), and the head's CHANGELOG.md must be a regular file even when the diff does
    # not show it (round 5). Selection is checked BEFORE range resolution (3b530): a sibling
    # GIT_DIR usually also collapses the range, and the precise wrong-repository diagnosis
    # must win over the generic collapsed-range refusal.
    try:
        check_git_selects_root()
        refuse_links([CHANGELOG_PATH], args.head)
    except GitSelectsAnotherTree as exc:
        print(f"ERROR: {exc}; unset GIT_DIR or GIT_WORK_TREE and rerun.", file=sys.stderr)
        return 2
    except GitQueryFailed as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except ChangelogDiffUnreadable as exc:
        print(f"ERROR: the {CHANGELOG_PATH} diff could not be read: {exc}", file=sys.stderr)
        return 2

    try:
        merge_base, head = resolve_pr_range(args.base, args.head)
    except PrRangeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    try:
        diff = added_line_diff([merge_base, head], [":(top)" + CHANGELOG_PATH])
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git diff failed: {exc}", file=sys.stderr)
        return 2

    if not diff:
        print(f"OK: {CHANGELOG_PATH} not modified between {merge_base[:8]} and {head}.")
        return 0

    try:
        added_lines = parse_added_lines(diff)
    except ChangelogDiffUnreadable as exc:
        print(f"ERROR: the {CHANGELOG_PATH} diff could not be read: {exc}", file=sys.stderr)
        return 2

    offending: list[str] = []
    for _path, added in added_lines:
        if DASH_PATTERN.search(added):
            offending.append(added.strip())

    if not offending:
        print(f"OK: no em/en dashes in added {CHANGELOG_PATH} lines.")
        return 0

    print(
        f"FAIL: {len(offending)} newly-added {CHANGELOG_PATH} line(s) contain an "
        f"em dash or en dash. Replace with a comma, colon, or parentheses "
        f"(this delta check covers added lines; lint-language.py also scans "
        f"the whole root CHANGELOG.md under its normal rules):",
        file=sys.stderr,
    )
    for added in offending:
        print(f"  {added[:160]}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
