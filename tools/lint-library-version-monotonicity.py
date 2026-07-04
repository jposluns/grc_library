#!/usr/bin/env python3
"""Enforce that library and document versions never decrease.

The library uses Calendar Versioning (CalVer) of the form `YYYY.MM.patch`
for the library as a whole, recorded in `README.md` as
`**Library Version:** YYYY.MM.patch`. Individual documents use semantic
versioning of the form `x.y.z` in their metadata.

This linter compares the working tree's versions to the prior committed
state (`origin/main` if available, falling back to `HEAD~1`) and fails
if any version went backwards or skipped to a lower value.

Catches:
- A version going BACKWARDS (a rollback or collision). An unchanged value
  passes, so a forgotten bump is the CHANGELOG-coupling and per-PR delta
  checks' and the reviewer's territory, not this gate's.
- Accidentally rewriting an older value in a metadata field.
- Per-document semver going backwards on a change that should have
  bumped forward.

Usage:
    python3 tools/lint-library-version-monotonicity.py
    python3 tools/lint-library-version-monotonicity.py --prior-readme PATH

The ``--prior-readme`` flag overrides the git-based "prior state"
lookup for the library-version check only: the linter parses CalVer
from the given file and compares to the current README.md. Used by
the gate-36 regression test suite to exercise the version-comparison
logic without a git fixture. The document-versions check is skipped
in this mode (it requires real git history).

Exit codes:
    0   versions are monotonic non-decreasing, OR the prior state is
        unavailable (no git history, or no diff against the base ref).
        Unavailable-prior-state is treated as a pass with a printed note
        rather than a separate exit code.
    1   one or more versions decreased.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from lint_common import DEFAULT_EXEMPT_DIRS, iter_non_code_lines

REPO_ROOT = Path(__file__).resolve().parent.parent

CALVER_RE = re.compile(r"\*\*Library Version:\*\*\s+(\d+)\.(\d+)\.(\d+)")
SEMVER_RE = re.compile(r"^\*\*Version:\*\*\s+(\d+)\.(\d+)\.(\d+)")


def parse_calver(text: str) -> tuple[int, int, int] | None:
    """Find the first ``**Library Version:** YYYY.MM.patch`` outside a fenced code block."""
    for _, line in iter_non_code_lines(text):
        m = CALVER_RE.search(line)
        if m:
            return tuple(int(x) for x in m.groups())  # type: ignore[return-value]
    return None


def parse_semver(text: str) -> tuple[int, int, int] | None:
    """Find the first ``**Version:** x.y.z`` outside a fenced code block.

    Reading the version only from non-code lines prevents template metadata
    blocks (e.g. the contributor template inside ``CONTRIBUTING.md``'s fenced
    code region, or the ``docs/worked-example.md`` walkthrough) from being
    mistaken for the file's real metadata. See the regression fixture in
    ``tests/test_linters.py::LibraryVersionMonotonicityTests`` for the
    template-version-ignored case.
    """
    for _, line in iter_non_code_lines(text):
        m = SEMVER_RE.match(line)
        if m:
            return tuple(int(x) for x in m.groups())  # type: ignore[return-value]
    return None


def git_show(ref: str, path: str) -> str | None:
    """Return file content at the given git ref, or None if unavailable."""
    try:
        return subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), "show", f"{ref}:{path}"],
            stderr=subprocess.DEVNULL,
        ).decode("utf-8")
    except subprocess.CalledProcessError:
        return None


def find_prior_ref() -> str | None:
    """Return a git ref naming the prior committed state.

    On a feature branch, prefer origin/main as the comparison point.
    When HEAD matches origin/main (we're on main, or main is up to date),
    fall through to HEAD~1. Local `main` is not used because it can be stale.
    """
    def sha(ref: str) -> str | None:
        try:
            return subprocess.check_output(
                ["git", "-C", str(REPO_ROOT), "rev-parse", "--verify", ref],
                stderr=subprocess.DEVNULL,
            ).decode().strip()
        except subprocess.CalledProcessError:
            return None

    head = sha("HEAD")
    origin_main = sha("origin/main")
    if origin_main and head and origin_main != head:
        return "origin/main"
    # Fallback: HEAD~1.
    if sha("HEAD~1"):
        return "HEAD~1"
    return None


def check_library_version(prior_ref: str) -> tuple[bool, str]:
    """Return (ok, message). ok=True if current >= prior."""
    current_path = REPO_ROOT / "README.md"
    current = parse_calver(current_path.read_text(encoding="utf-8"))
    prior_text = git_show(prior_ref, "README.md")
    prior = parse_calver(prior_text) if prior_text else None
    if current is None:
        return (False, "Library Version not found in current README.md")
    if prior is None:
        return (True, f"current {current} (no prior to compare)")
    if current < prior:
        return (
            False,
            f"Library Version decreased: current {'.'.join(map(str, current))} "
            f"< prior {'.'.join(map(str, prior))}",
        )
    return (True, f"current {'.'.join(map(str, current))} >= prior {'.'.join(map(str, prior))}")


def check_document_versions(prior_ref: str) -> list[tuple[str, str]]:
    """Return list of (path, message) for documents whose version decreased."""
    findings: list[tuple[str, str]] = []
    # Walk markdown files in artefact domains; skip non-artefact directories.
    skip_dirs = DEFAULT_EXEMPT_DIRS
    for path in REPO_ROOT.rglob("*.md"):
        if any(part in skip_dirs for part in path.parts):
            continue
        rel = path.relative_to(REPO_ROOT).as_posix()
        # Skip README.md (covered by library version check above).
        if rel == "README.md":
            continue
        # Skip CHANGELOG (no Version metadata field).
        if rel == "CHANGELOG.md":
            continue
        try:
            current_text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        current = parse_semver(current_text)
        if current is None:
            continue
        prior_text = git_show(prior_ref, rel)
        if prior_text is None:
            continue
        prior = parse_semver(prior_text)
        if prior is None:
            continue
        if current < prior:
            findings.append(
                (
                    rel,
                    f"Version decreased: current {'.'.join(map(str, current))} "
                    f"< prior {'.'.join(map(str, prior))}",
                )
            )
    return findings


def check_library_version_against_text(prior_text: str) -> tuple[bool, str]:
    """Variant of check_library_version that takes prior README text directly.

    Used by the ``--prior-readme`` mode to exercise the version-comparison
    logic without invoking git.
    """
    current_path = REPO_ROOT / "README.md"
    current = parse_calver(current_path.read_text(encoding="utf-8"))
    prior = parse_calver(prior_text)
    if current is None:
        return (False, "Library Version not found in current README.md")
    if prior is None:
        return (False, "Library Version not found in supplied prior README")
    if current < prior:
        return (
            False,
            f"Library Version decreased: current {'.'.join(map(str, current))} "
            f"< prior {'.'.join(map(str, prior))}",
        )
    return (True, f"current {'.'.join(map(str, current))} >= prior {'.'.join(map(str, prior))}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Enforce that library and document versions never decrease."
    )
    parser.add_argument(
        "--prior-readme",
        type=Path,
        default=None,
        help="Compare against the CalVer in this file instead of git history "
             "(library-version check only; document-versions skipped).",
    )
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    if args.prior_readme is not None:
        prior_text = args.prior_readme.read_text(encoding="utf-8")
        lib_ok, lib_msg = check_library_version_against_text(prior_text)
        if lib_ok:
            print(f"OK: library version is monotonic non-decreasing (vs supplied prior).")
            print(f"  Library: {lib_msg}")
            return 0
        print(f"FAIL [library]: {lib_msg}")
        return 1

    prior_ref = find_prior_ref()
    if prior_ref is None:
        print("OK: no prior committed state available; monotonicity not checked.")
        return 0
    lib_ok, lib_msg = check_library_version(prior_ref)
    doc_findings = check_document_versions(prior_ref)
    if lib_ok and not doc_findings:
        print(f"OK: library and document versions are monotonic non-decreasing (vs {prior_ref}).")
        print(f"  Library: {lib_msg}")
        return 0
    if not lib_ok:
        print(f"FAIL [library]: {lib_msg}")
    if doc_findings:
        print(f"FAIL [documents]: {len(doc_findings)} version regression(s) vs {prior_ref}:")
        for rel, msg in doc_findings:
            print(f"  {rel}: {msg}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
