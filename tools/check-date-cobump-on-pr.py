#!/usr/bin/env python3
"""Per-PR Version-Date co-bump delta gate (D4).

When a pull request bumps a versioned document's ``**Version:**`` field,
the project's version-bump discipline requires the same change to set the
document's ``**Date:**`` field to the date of that change (the commit
date). This delta gate catches the residual failure mode that gates 31
and 40 leave open: a Version bump whose Date was *not* co-bumped to the
commit date.

Why the existing gates leave a gap:

  - Delta gate D2 (``check-version-bump-on-pr.py``) catches a body change
    with no Version bump, but says nothing about the Date.
  - Gate 40 (corpus version-bump-recency) is the HEAD-state counterpart
    of D2; it too is silent on the Date.
  - Gate 31 (document-date-staleness) compares the Date against the
    file's most-recent commit date but tolerates a 1-day lag (to absorb
    timezone-boundary commits). The recurring residue this gate targets
    ("Version bumped, Date left one day stale", observed at PR #325 on
    the audit-programme spec and PR #352 on the pack README) falls
    inside that 1-day tolerance, so gate 31 passes it.

This gate is *delta-scoped*: it inspects only the files a PR changed
between its merge-base and head, and only those whose Version actually
bumped in the PR. A HEAD-state form of this check is unviable because
the corpus carries a large pre-existing population of historical
Version bumps whose Dates were not co-bumped by today's strict standard
(a 2026-05-31 mass commit alone accounts for dozens); a HEAD gate would
need an unmanageable grandfathering exempt list. The delta form never
sees that history, so it has zero historical false-positive surface and
needs no baseline / grandfathering.

The expected Date for a bumped document is the UTC committer date of the
most-recent commit in the PR range that touched the file (the bump
commit). Comparing against that commit date, rather than against the
base Date, is what makes the gate FP-free for same-day sequential PRs:
when a document is bumped twice on the same UTC day, its Date is already
today and the bump commit is dated today, so they match and the gate
stays silent.

This is a CI-only delta gate, not part of the corpus audit programme in
governance/specification-audit-programme.md section 6; it is documented
there in section 6.1 (PR-only delta gates) alongside D1/D2/D3 and is
exempt from gate 35's parity audit (its inputs, a git history range and
the PR base ref, are not available to ``tools/run_all_audits.sh`` or
``.pre-commit-config.yaml``).

Exempt files: CHANGELOG.md (its body is the version history itself);
generated artefacts (taxonomy.yml, docs/portal.md,
docs/maturity-scorecard.md); files without a Version metadata field.

Usage:
    # In CI (uses GITHUB_BASE_REF):
    python3 tools/check-date-cobump-on-pr.py

    # Locally, comparing HEAD to a specific base:
    python3 tools/check-date-cobump-on-pr.py origin/main
    python3 tools/check-date-cobump-on-pr.py origin/main HEAD

Exit codes:
    0 : Every versioned document whose Version bumped in the PR carries a
        Date equal to the bump commit's UTC date, or the diff is empty,
        or no versioned document bumped.
    1 : One or more documents bumped Version without co-bumping Date.
    2 : Invocation or environment error (cannot determine base/head,
        git failure).
"""

from __future__ import annotations

import argparse
import datetime
import os
import subprocess
import sys

from lint_common import head_version, parse_iso_date, parse_metadata_block


# Files exempt from the co-bump requirement (same set as D2).
EXEMPT_FILES: frozenset[str] = frozenset(
    {
        "CHANGELOG.md",
        "taxonomy.yml",
        "docs/portal.md",
        "docs/maturity-scorecard.md",
    }
)

# Directory prefixes whose files are exempt.
EXEMPT_PREFIXES: tuple[str, ...] = (
    ".git/",
    "node_modules/",
    "__pycache__/",
)

# Field extraction is shared with the corpus linters (GR-3 wave 2:
# ``lint_common.head_version`` for the Version window, and
# ``parse_metadata_block`` + ``parse_iso_date`` for the Date). An
# annotated or malformed Date value (``parse_iso_date`` returns
# ``None``) is treated as a missing canonical line, a FAIL for a
# bumped file, as under the retired private regex. One finding-text
# delta: a shape-valid but calendar-invalid Date (e.g. 2026-02-30)
# previously drew its own "not a valid ISO date" message; it now folds
# into the missing-canonical-line message. The failing exit is the
# same either way.


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


def bump_commit_date_utc(merge_base: str, head: str, path: str) -> datetime.date | None:
    """Return the UTC committer date of the most-recent commit in the
    range ``merge_base..head`` that touched ``path``, or ``None`` if no
    such commit exists (defensive; the path is in the diff, so one
    normally does)."""
    try:
        stamp = git(
            "log",
            "-1",
            "--format=%cI",
            f"{merge_base}..{head}",
            "--",
            path,
        )
    except subprocess.CalledProcessError:
        return None
    if not stamp:
        return None
    try:
        dt = datetime.datetime.fromisoformat(stamp)
    except ValueError:
        return None
    return dt.astimezone(datetime.timezone.utc).date()


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
            "Check that every versioned document whose Version bumped in a "
            "PR also co-bumped its Date to the bump commit's date."
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
    bumped_checked = 0
    skipped_exempt = 0
    skipped_no_version_event = 0
    for path in changed:
        if is_exempt(path):
            skipped_exempt += 1
            continue
        base_content = git_show(merge_base, path)
        head_content = git_show(head, path)
        # File added (no base) or deleted (no head) in the PR: not a bump event.
        if base_content is None or head_content is None:
            continue
        base_version = head_version(base_content)
        head_version_value = head_version(head_content)
        # No Version field at either ref: not a versioned document.
        if base_version is None and head_version_value is None:
            skipped_no_version_event += 1
            continue
        # A Version event in this PR = the Version field changed value, or
        # was gained / lost. If unchanged, this gate has nothing to assert
        # (D2 governs whether a missing bump is itself a defect).
        if base_version == head_version_value:
            skipped_no_version_event += 1
            continue
        bumped_checked += 1
        head_date_raw = parse_metadata_block(head_content).fields.get("Date")
        head_date = (
            parse_iso_date(head_date_raw) if head_date_raw is not None else None
        )
        # An absent Date line AND an annotated / malformed value both land
        # here: parse_iso_date returns None on anything but a bare ISO
        # date, matching the retired private regex, which only ever
        # matched the canonical `**Date:** YYYY-MM-DD` shape.
        if head_date is None:
            findings.append(
                (
                    path,
                    f"Version bumped to `{head_version_value}` but the file has no "
                    f"canonical `**Date:** YYYY-MM-DD` metadata line to co-bump.",
                )
            )
            continue
        commit_date = bump_commit_date_utc(merge_base, head, path)
        if commit_date is None:
            # Defensive: the file is in the diff but no range commit touched
            # it (e.g. a merge artefact). Nothing reliable to compare against.
            continue
        if head_date != commit_date:
            findings.append(
                (
                    path,
                    f"Version bumped to `{head_version_value}` but Date is "
                    f"`{head_date.isoformat()}`, not the bump commit's UTC date "
                    f"`{commit_date.isoformat()}`; co-bump the Date in the same "
                    f"change.",
                )
            )

    if not findings:
        print(
            f"OK: {bumped_checked} document(s) bumped Version in this PR; "
            f"each co-bumped its Date to the bump commit's date. "
            f"{skipped_exempt} exempt file(s), "
            f"{skipped_no_version_event} non-bumping file(s) skipped."
        )
        return 0

    for path, message in findings:
        print(f"FAIL {path}: {message}", file=sys.stderr)
    print(
        f"\n{len(findings)} document(s) bumped Version without co-bumping Date "
        f"to the commit date. The version-bump discipline requires bumping both "
        f"`**Version:**` and `**Date:**` in the same change; set each flagged "
        f"document's `**Date:**` to the date its Version-bumping commit was made "
        f"(UTC).",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
