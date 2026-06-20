#!/usr/bin/env python3
"""Verify a pull request modifies CHANGELOG.md or carries a Changelog: opt-out trailer.

This is a CI-only delta gate, not part of the 39-gate corpus audit programme. The
39 corpus gates check repository state at HEAD; this script compares HEAD to the
PR's merge-base and asserts the diff includes CHANGELOG.md, unless any commit in
the PR range carries a `Changelog: <one-line-reason>` trailer in its message body.

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
import os
import re
import subprocess
import sys

CHANGELOG_PATH = "CHANGELOG.md"
TRAILER_PATTERN = re.compile(
    r"^\s*Changelog:\s*(\S.*?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def git(*args: str) -> str:
    """Run `git <args>` and return stdout, stripped. Raises on non-zero exit."""
    return subprocess.check_output(["git", *args], text=True).strip()


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
            f"In GitHub Actions, ensure actions/checkout uses fetch-depth: 0.",
            file=sys.stderr,
        )
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

    if CHANGELOG_PATH in changed:
        print(
            f"OK: {CHANGELOG_PATH} is in the diff "
            f"({len(changed)} file(s) total)."
        )
        return 0

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

    print(
        f"FAIL: {len(changed)} file(s) changed but {CHANGELOG_PATH} is not "
        f"in the diff.",
        file=sys.stderr,
    )
    print("", file=sys.stderr)
    print(
        "Either add an entry to CHANGELOG.md describing this change, or add a",
        file=sys.stderr,
    )
    print(
        "'Changelog: <one-line-reason>' trailer to any commit in the PR body to",
        file=sys.stderr,
    )
    print(
        "opt out (e.g. for trivial corrections that don't warrant an entry).",
        file=sys.stderr,
    )
    print("", file=sys.stderr)
    print("Changed files:", file=sys.stderr)
    for path in changed:
        print(f"  {path}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
