#!/usr/bin/env python3
"""Corpus-heuristic version-bump-recency audit.

For each versioned document in the corpus (markdown file with a
``**Version:**`` or ``**Library Version:**`` field in its metadata
block), this linter compares two commits:

  - the most recent commit that touched the file at all, and
  - the most recent commit that touched a Version line in the file.

If they differ, the file's body has been modified since its last
Version field bump, indicating a missed bump.

This is the corpus-side counterpart of delta gate D2 (the PR-only
version-bump check in ``tools/check-version-bump-on-pr.py``). D2
catches the failure mode at PR time, comparing the PR head to its
merge-base; this linter catches it from HEAD using git log heuristics,
covering the case where a body change landed without a Version bump
through any path (squash commit, direct push, batch merge).

Scope: ``*.md`` files under the repository root, minus the exempt set.
The linter requires a versioned-metadata field (the shared
``lint_common.head_version`` helper returns non-None; GR-3 wave 2
retired this file's private window regex for it) to bring a file into
scope; files without a Version field are silently skipped.

Exempt: CHANGELOG.md (the file is itself the version history;
metadata is not bumped per change); generated artefacts (taxonomy.yml,
docs/portal.md, docs/maturity-scorecard.md), which are regenerated
not edited; and the hidden directories under DEFAULT_EXEMPT_DIRS.

Exit codes: 0 pass, 1 findings, 2 internal error (git failure).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from lint_common import DEFAULT_EXEMPT_DIRS, REPO_ROOT, head_version, read_text_safe


# Files exempt from the recency requirement.
EXEMPT_FILES: frozenset[str] = frozenset(
    {
        "CHANGELOG.md",
        "taxonomy.yml",
        "docs/portal.md",
        "docs/maturity-scorecard.md",
        "docs/reference-acquisition-manifest.md",
    }
)

# Regex (passed to ``git log -G``) that matches a Version metadata line
# at the start of a line. The double-escape (``\\*``) is correct: git
# log's regex backend reads a single backslash.
GIT_VERSION_REGEX = r"^\*\*(Library )?Version:\*\*"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def iter_targets(root: Path) -> list[Path]:
    """Walk the repository root, yielding markdown files with a
    metadata-block Version field, minus the exempt set."""
    targets: list[Path] = []
    for path in root.rglob("*.md"):
        try:
            rel = path.relative_to(root).as_posix()
            parts = set(path.relative_to(root).parts)
        except ValueError:
            continue
        if parts & DEFAULT_EXEMPT_DIRS:
            continue
        if rel in EXEMPT_FILES:
            continue
        if head_version(read_text_safe(path)) is None:
            continue
        targets.append(path)
    return sorted(targets)


def last_file_commit(rel: str) -> str | None:
    try:
        out = git("log", "-1", "--format=%H", "--", rel)
    except subprocess.CalledProcessError:
        return None
    return out or None


def last_version_commit(rel: str) -> str | None:
    """Return the SHA of the most recent commit that modified a
    Version metadata line in ``rel``. Returns None if no such commit
    exists (e.g. the file was just added and the Version line has not
    been changed since)."""
    try:
        out = git("log", "-1", "--format=%H", "-G", GIT_VERSION_REGEX, "--", rel)
    except subprocess.CalledProcessError:
        return None
    return out or None


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit the corpus for versioned documents whose body has changed "
            "more recently than their Version field."
        ),
    )
    parser.add_argument(
        "--root",
        default=str(REPO_ROOT),
        help="Repository root to scan (default: REPO_ROOT).",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help=(
            "Optional explicit paths to check instead of walking the root. "
            "Used by the regression test."
        ),
    )
    args = parser.parse_args(argv[1:])
    root = Path(args.root).resolve()

    if args.paths:
        targets = [Path(p).resolve() for p in args.paths if p.endswith(".md")]
    else:
        targets = iter_targets(root)

    findings: list[tuple[str, str, str]] = []
    scanned = 0
    skipped_single_commit = 0
    for path in targets:
        try:
            rel = path.relative_to(root).as_posix()
        except ValueError:
            rel = path.as_posix()
        scanned += 1
        file_commit = last_file_commit(rel)
        if file_commit is None:
            # Path not tracked yet (new file in the working tree); skip.
            continue
        version_commit = last_version_commit(rel)
        if version_commit is None:
            # File exists in history but no commit touched a Version line.
            # This typically means the file was added once with the Version
            # field present and nothing since. If the file's only commit
            # added the Version field, file_commit == version_commit would
            # hold and we would not be here. Skip to avoid noise.
            skipped_single_commit += 1
            continue
        if file_commit != version_commit:
            findings.append((rel, file_commit[:8], version_commit[:8]))

    if not findings:
        print(
            f"OK: {scanned} versioned document(s) scanned; "
            f"all have a Version field bumped at or after their most-recent "
            f"body change. {skipped_single_commit} document(s) had no "
            f"Version-line commit history (likely single-commit add)."
        )
        return 0

    for rel, file_sha, version_sha in findings:
        print(
            f"FAIL {rel}: last body commit {file_sha}, "
            f"last Version-line commit {version_sha}; "
            f"the body has changed since the Version was last bumped."
        )
    print(
        f"\n{len(findings)} versioned document(s) have body changes that "
        f"post-date the file's last Version bump. Each finding is the "
        f"corpus-heuristic counterpart of delta gate D2 (which catches the "
        f"same shape at PR time). Resolve by bumping the document's Version "
        f"field, or document the divergence per the project's exception "
        f"protocol.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
