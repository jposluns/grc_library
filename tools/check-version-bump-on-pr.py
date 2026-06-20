#!/usr/bin/env python3
"""Per-PR version-bump delta gate.

When a pull request substantively modifies a versioned document (a
markdown file carrying a ``**Version:**`` metadata field), the
document's Version field should bump in the same PR. This delta gate
detects PRs that change a versioned document's body without bumping
its Version field, catching the omission before merge.

This is a CI-only delta gate, not part of the 40-gate corpus audit
programme in governance/specification-audit-programme.md §6. The §6
corpus gates check repository state at HEAD; this script compares
HEAD to the PR's merge-base and asserts that every changed versioned
document has a bumped Version field.

Exempt files: CHANGELOG.md (its body is the version history itself);
generated artefacts (taxonomy.yml, docs/portal.md,
docs/maturity-scorecard.md); files without a Version metadata field
(e.g. plain README boilerplate, governance/charter notes that the
project chose not to version-control via metadata).

Usage:
    # In CI (uses GITHUB_BASE_REF):
    python3 tools/check-version-bump-on-pr.py

    # Locally, comparing HEAD to a specific base:
    python3 tools/check-version-bump-on-pr.py origin/main
    python3 tools/check-version-bump-on-pr.py origin/main HEAD

Exit codes:
    0 : Every changed versioned document has a bumped Version field,
        or the diff is empty, or only exempt files were touched.
    1 : One or more versioned documents changed without a Version bump.
    2 : Invocation or environment error (cannot determine base/head,
        git failure).
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


# Files exempt from the version-bump requirement.
EXEMPT_FILES: frozenset[str] = frozenset(
    {
        "CHANGELOG.md",
        "taxonomy.yml",
        "docs/portal.md",
        "docs/maturity-scorecard.md",
    }
)

# Directory prefixes whose files are exempt (e.g. node_modules, .git).
EXEMPT_PREFIXES: tuple[str, ...] = (
    ".git/",
    "node_modules/",
    "__pycache__/",
)

# Match a metadata-block Version line. The pattern requires the line
# to be one of the first 30 lines of the file (the metadata block) so
# that documentation prose elsewhere demonstrating the metadata format
# (e.g. ``**Version:** <x.y.z: ...>`` in a README's "How to add a
# document" section) does not match. The 30-line cap is generous;
# metadata blocks in this corpus are typically 13 fields plus a leading
# title and blank line, well under 30 lines.
METADATA_HEAD_LINES = 30
VERSION_LINE_PATTERN = re.compile(
    r"^\s*\*\*(?:Library )?Version:\*\*\s+(\S.*?)\s*\\?\s*$",
    re.MULTILINE,
)


def git(*args: str) -> str:
    """Run ``git <args>`` and return stdout, stripped. Raises on non-zero exit."""
    return subprocess.check_output(["git", *args], text=True).strip()


def git_show(ref: str, path: str) -> str | None:
    """Return file content at ``ref:path`` or ``None`` if the file is absent."""
    try:
        return subprocess.check_output(
            ["git", "show", f"{ref}:{path}"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return None


def extract_version(text: str | None) -> str | None:
    """Return the metadata-block Version: (or Library Version:) field
    value from text, or ``None`` if the file has no metadata-block
    version. The match is restricted to the first ``METADATA_HEAD_LINES``
    lines so documentation prose elsewhere in the file demonstrating
    the metadata format does not match.
    """
    if text is None:
        return None
    head = "\n".join(text.splitlines()[:METADATA_HEAD_LINES])
    match = VERSION_LINE_PATTERN.search(head)
    if match is None:
        return None
    return match.group(1).strip()


def is_exempt(path: str) -> bool:
    if path in EXEMPT_FILES:
        return True
    if any(path.startswith(prefix) for prefix in EXEMPT_PREFIXES):
        return True
    if not path.endswith(".md"):
        return True
    return False


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check that every versioned document changed in a PR has a "
            "bumped Version field."
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

    findings: list[tuple[str, str]] = []
    versioned_checked = 0
    skipped_no_version = 0
    skipped_exempt = 0
    for path in changed:
        if is_exempt(path):
            skipped_exempt += 1
            continue
        base_content = git_show(merge_base, path)
        head_content = git_show(head, path)
        # File added in the PR (no base content): exempt; new files start
        # at their initial Version and need not "bump".
        if base_content is None:
            continue
        # File deleted in the PR (no head content): not relevant.
        if head_content is None:
            continue
        base_version = extract_version(base_content)
        head_version = extract_version(head_content)
        # File has no Version field at either ref: exempt by design.
        if base_version is None and head_version is None:
            skipped_no_version += 1
            continue
        # File has a Version field at head but not at base (or vice versa):
        # the file gained or lost its Version field, which is a metadata
        # change that itself counts as a version event.
        if base_version is None or head_version is None:
            versioned_checked += 1
            continue
        versioned_checked += 1
        if base_version == head_version:
            findings.append(
                (
                    path,
                    f"Version field is `{head_version}` at both {merge_base[:8]} "
                    f"and {head}; the file's body changed but Version did not bump.",
                )
            )

    if not findings:
        print(
            f"OK: {versioned_checked} changed versioned document(s) have a "
            f"bumped Version field. {skipped_exempt} exempt file(s), "
            f"{skipped_no_version} non-versioned file(s) skipped."
        )
        return 0

    for path, message in findings:
        print(f"FAIL {path}: {message}", file=sys.stderr)
    print(
        f"\n{len(findings)} versioned document(s) changed without a Version bump. "
        f"Bump the **Version:** field of each, or move the change to a separate "
        f"PR if the change does not warrant a version bump (uncommon: most body "
        f"edits to a versioned document do warrant a bump).",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
