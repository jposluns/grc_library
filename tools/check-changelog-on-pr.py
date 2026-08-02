#!/usr/bin/env python3
"""Verify a pull request modifies CHANGELOG.md or carries a Changelog: opt-out trailer.

This is a CI-only delta gate, not part of the corpus audit programme. The
corpus gates check repository state at HEAD; this script compares HEAD to the
PR's merge-base and asserts the diff includes CHANGELOG.md, unless any commit in the PR
range carries a `Changelog: <one-line-reason>` trailer in its message body.

The former two-file lock-step (root CHANGELOG.md plus a detailed mirror, introduced in
PR #125, 2026-06-21) no longer applies to the public diff: as of PR #1235 (2026-07-29,
the working-state move to the private sibling) the detailed mirror lives in the
private-sibling working-state store (cross-repo, invisible to a public PR diff), so this
gate enforces ONLY the root CHANGELOG.md.

The library's CONTRIBUTING.md and audit-programme spec require a CHANGELOG entry
for substantive batches. This script enforces that requirement mechanically at PR
time, closing the gap where a maintainer (human or AI) modifies content and forgets
to update CHANGELOG.md.

Opt-out: any commit in the PR can include a line of the form

    Changelog: trivial typo correction

in its commit message body. Any single matching trailer in any commit in the PR
range satisfies the gate; no path-based exemptions are applied.

Usage:
    # In CI (uses GITHUB_BASE_REF):
    python3 tools/check-changelog-on-pr.py

    # Locally, comparing HEAD to a specific base:
    python3 tools/check-changelog-on-pr.py origin/main
    python3 tools/check-changelog-on-pr.py origin/main HEAD

Exit codes:
    0 : CHANGELOG.md is in the diff, or an opt-out trailer is present, or the
        diff is empty.
    1 : CHANGELOG.md is not in the diff and no opt-out trailer is present.
    2 : Invocation or environment error (cannot determine base/head, git failure).
"""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path
import sys

from lint_common import PrRangeError, git, resolve_pr_range

CHANGELOG_PATH = "CHANGELOG.md"

# The detailed CHANGELOG mirror moved to the private-sibling working-state store
# (grc_library_private/.working/changelog-details/) in the .working/ -> _private
# migration. It is a cross-repo surface, invisible to a public PR diff, so this
# PR-time gate requires only the PUBLIC root CHANGELOG.md.

TRAILER_PATTERN = re.compile(
    r"^\s*Changelog:\s*(\S.*?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check that a pull request modifies CHANGELOG.md, or carries a "
            "Changelog: opt-out trailer in any commit."
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

    try:
        merge_base, head = resolve_pr_range(args.base, args.head)
    except PrRangeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    try:
        changed_raw = git("diff", "--name-only", merge_base, head)
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git diff failed: {exc}", file=sys.stderr)
        return 2

    changed = [line for line in changed_raw.splitlines() if line]

    if not changed:
        print(f"OK: no files changed between {merge_base[:8]} and {head}.")
        return 0

    root_changed = CHANGELOG_PATH in changed
    if root_changed:
        print(
            f"OK: {CHANGELOG_PATH} is in the diff ({len(changed)} file(s) total)."
        )
        return 0

    # Root CHANGELOG.md not changed; check for an opt-out trailer before failing.
    try:
        commit_shas = git("log", "--format=%H", f"{merge_base}..{head}").splitlines()
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git log failed: {exc}", file=sys.stderr)
        return 2

    for sha in commit_shas:
        body = git("log", "-1", "--format=%B", sha)
        match = TRAILER_PATTERN.search(body)
        if match:
            reason = match.group(1)
            print(
                f"OK: commit {sha[:8]} carries opt-out trailer: "
                f"'Changelog: {reason}'."
            )
            return 0

    # No trailer.
    print(
        f"FAIL: {len(changed)} file(s) changed but {CHANGELOG_PATH} is not in the diff.",
        file=sys.stderr,
    )
    print("", file=sys.stderr)
    print(
        f"Add an entry to {CHANGELOG_PATH} (the root changelog; the detailed structured",
        file=sys.stderr,
    )
    print(
        "entry now lives in the private-sibling working-state mirror, cross-repo and not",
        file=sys.stderr,
    )
    print(
        "part of the public diff), or add a 'Changelog: <one-line-reason>' trailer to any",
        file=sys.stderr,
    )
    print(
        "commit in the PR body to opt out (e.g. for trivial corrections).",
        file=sys.stderr,
    )
    print("", file=sys.stderr)
    print("Changed files:", file=sys.stderr)
    for path in changed:
        print(f"  {path}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
