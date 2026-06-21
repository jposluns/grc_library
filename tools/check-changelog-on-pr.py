#!/usr/bin/env python3
"""Verify a pull request modifies CHANGELOG.md (and its detailed mirror) or carries a Changelog: opt-out trailer.

This is a CI-only delta gate, not part of the corpus audit programme. The
corpus gates check repository state at HEAD; this script compares HEAD to the
PR's merge-base and asserts the diff includes CHANGELOG.md AND its detailed mirror
at `.working/changelog-details/CHANGELOG-detailed.md`, unless any commit in the PR
range carries a `Changelog: <one-line-reason>` trailer in its message body.

The dual-entry requirement was introduced in PR #125 (2026-06-21): the root
CHANGELOG.md carries lead-paragraph summaries; the detailed mirror carries the full
structured-section entries (Added / Changed / Removed / Fixed / Security / Verification).
Both must move in lock-step. A PR that modifies one without the other is a discipline
failure caught by this gate.

The library's CONTRIBUTING.md and audit-programme spec require a CHANGELOG entry
for substantive batches. This script enforces that requirement mechanically at PR
time, closing the gap where a maintainer (human or AI) modifies content and forgets
to update CHANGELOG.md (or its mirror).

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
CHANGELOG_DETAILED_PATH = ".working/changelog-details/CHANGELOG-detailed.md"
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

    root_changed = CHANGELOG_PATH in changed
    detailed_changed = CHANGELOG_DETAILED_PATH in changed

    if root_changed and detailed_changed:
        print(
            f"OK: both {CHANGELOG_PATH} and {CHANGELOG_DETAILED_PATH} are in the diff "
            f"({len(changed)} file(s) total)."
        )
        return 0

    # Check for opt-out trailer before reporting any specific failure shape.
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

    # No trailer; classify the failure mode.
    if not root_changed and not detailed_changed:
        print(
            f"FAIL: {len(changed)} file(s) changed but neither {CHANGELOG_PATH} "
            f"nor {CHANGELOG_DETAILED_PATH} is in the diff.",
            file=sys.stderr,
        )
    elif root_changed and not detailed_changed:
        print(
            f"FAIL: {CHANGELOG_PATH} was modified but its detailed mirror "
            f"{CHANGELOG_DETAILED_PATH} was not. The dual-entry convention "
            f"requires both files to move in lock-step.",
            file=sys.stderr,
        )
    else:
        # detailed_changed and not root_changed
        print(
            f"FAIL: {CHANGELOG_DETAILED_PATH} was modified but the root "
            f"{CHANGELOG_PATH} was not. The dual-entry convention requires "
            f"both files to move in lock-step.",
            file=sys.stderr,
        )

    print("", file=sys.stderr)
    print(
        f"Either add an entry to BOTH {CHANGELOG_PATH} (lead paragraph only) and",
        file=sys.stderr,
    )
    print(
        f"{CHANGELOG_DETAILED_PATH} (full structured entry), or add a",
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
