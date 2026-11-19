#!/usr/bin/env python3
"""Refuse a pull request that adds a per-change or daily line to the public .working/CHANGELOG.md.

This is a PR-time delta gate (D1), not part of the corpus audit programme (it runs in the 1 pull_request job of quality.yml and locally via the pre-push guard). The
corpus gates check repository state at HEAD; this script compares HEAD to the
PR's merge-base and reads the lines the PR adds to .working/CHANGELOG.md.

The public .working/CHANGELOG.md carries weekly summaries only (maintainer-directed
2026-11-13): a weekly paragraph headed ``**Week of YYYY-MM-DD (PRs #FIRST-#LAST)**`` and, for
periods older than 3 months, a monthly paragraph headed ``**YYYY-MM (PRs #FIRST-#LAST)**``.
Each change's own record (its per-change entry and its detailed entry) goes to the private
per-change record, outside this repository. So a pull request no longer has to touch the
public file, and no ``Changelog:`` trailer is needed or read: a trailer cannot excuse a
refused line.

WHAT IT REFUSES. Every line the PR adds to .working/CHANGELOG.md is read with the shared
pinned diff and hunk-count parser (``changelog_diff``), and the head file's lines are
classified at their start and after every ``str.splitlines()`` boundary inside them
(``changelog_diff.public_line_kind``), so an entry after a CR, U+2028 or U+0085 is still read.
An added line fails when it is, or holds after such a boundary:
  * a per-change entry: a line that opens, after markup only, with a full ``YYYY-MM-DD`` date
    (``**2026-11-12 | 2026.11.93 | PR #29** - ...``, a daily roll-up or a dated legacy header),
    or a ``PR #N:`` bullet;
  * a daily summary heading (``**YYYY-MM-DD (PRs #A-#B)**``);
  * an unauthored scaffold marker (``TIER-SCAFFOLD`` or ``CONDENSE-SCAFFOLD``);
  * any other heading or bold line that is not a weekly or monthly heading (a period heading
    with no PR range, or with a range that does not rise, among them);
  * a text line that is not part of a weekly or monthly paragraph: in the head file, the
    nearest heading above it must be a weekly or monthly heading or a legacy
    ``## Week of YYYY-MM-DD`` section, or there must be none (the preamble under the title).
Blank lines, weekly and monthly headings and the lines of their paragraphs, lines of the
legacy weekly sections and preamble lines pass.

NOT COVERED: whether a weekly or monthly range names exactly the PRs of its period (gate 59
checks that when the private mirror is present), a paragraph's length (D7) and its dashes
(D3), a line the PR removes or leaves unchanged, and a date or PR number written with digits
outside 0-9 (the shapes are ASCII-only; gate 59's strict character rule refuses such a
character in the public file).

Usage:
    # In CI (uses GITHUB_BASE_REF):
    python3 .claude/skills/corpus-management/tools/check-changelog-on-pr.py

    # Locally, comparing HEAD to a specific base:
    python3 .claude/skills/corpus-management/tools/check-changelog-on-pr.py origin/main
    python3 .claude/skills/corpus-management/tools/check-changelog-on-pr.py origin/main HEAD

Exit codes:
    0 : .working/CHANGELOG.md is not in the diff, or every line the PR adds to it passes.
    1 : one or more added .working/CHANGELOG.md lines are refused (each named with its line
        number in the head file).
    2 : Invocation or environment error (cannot determine base/head, git failure, a diff the
        shared parser cannot read exactly, a .working/CHANGELOG.md that is a symbolic link or a
        submodule in the head or the diff, a head file that is not UTF-8, or git selecting
        another repository or work tree than it finds by itself), or CANNOT-EVALUATE: base and
        head resolve to the same commit, or the range changes no file (an empty diff), so
        nothing was evaluated.
"""

from __future__ import annotations

import argparse
import subprocess
import sys

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack .claude/skills/corpus-management/tools/ on sys.path
from aiqt_corpus import git  # noqa: E402  # generic core (behaviour-identical to lint_common)
from lint_common import PrRangeError, empty_pr_range_message, resolve_pr_range  # noqa: E402  # grc-config/store, stays local
from changelog_diff import (  # noqa: E402  # shared added-line diff reader and public line shapes
    STRUCTURAL_KINDS, ChangelogDiffUnreadable, GitQueryFailed, GitSelectsAnotherTree,
    added_line_diff, check_git_selects_root, parse_numbered_added_lines, public_line_kind,
    public_line_parts, read_blob, refuse_links)

CHANGELOG_PATH = ".working/CHANGELOG.md"

# Sections whose text lines are part of the public weekly record: the preamble (no heading
# yet, or the title), a weekly or monthly paragraph, and a legacy weekly section.
PARAGRAPH_SECTIONS = (None, "title", "weekly", "monthly", "legacy-weekly")

REASONS = {
    "per-change": "per-change entry (it belongs in the private per-change record, not the "
                  "public weekly record)",
    "daily": "daily summary heading (the public record carries weekly and monthly summaries "
             "only)",
    "scaffold": "unauthored scaffold marker (author the weekly summary and remove the "
                "scaffold)",
    "heading": "a heading that is not a weekly or monthly heading (**Week of YYYY-MM-DD "
               "(PRs #FIRST-#LAST)** or **YYYY-MM (PRs #FIRST-#LAST)**, the range rising)",
}


def refusals(added_numbers: set[int], head_text: str) -> list[str]:
    """One message per refused part of an added line of ``head_text``, the head file, whose
    added lines are numbered ``added_numbers`` (LF line numbers, from one)."""
    out: list[str] = []
    section: str | None = None  # the kind of the nearest structural line above
    for number, part in public_line_parts(head_text):
        kind = public_line_kind(part)
        if number in added_numbers:
            reason = REASONS.get(kind)
            if reason is None and kind == "text" and section not in PARAGRAPH_SECTIONS:
                reason = ("not part of a weekly or monthly paragraph (the nearest heading "
                          f"above it is a {section} line)")
            if reason is not None:
                out.append(f"{CHANGELOG_PATH}:{number}: {reason}: {part.strip()[:120]}")
        if kind in STRUCTURAL_KINDS:
            section = kind
    return out


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Refuse a pull request that adds a per-change entry, a daily summary heading or "
            "any other line outside a weekly or monthly paragraph to .working/CHANGELOG.md."
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

    # git must select the repository it finds by itself, and the head's .working/CHANGELOG.md
    # must be a regular file even when the diff does not show it (shared with D3 and D7).
    # Selection is checked before range resolution, so the precise wrong-repository
    # diagnosis wins over the generic collapsed-range refusal.
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
    except (OSError, UnicodeDecodeError) as exc:
        print(f"ERROR: git failed: {exc}", file=sys.stderr)
        return 2

    try:
        merge_base, head = resolve_pr_range(args.base, args.head)
    except PrRangeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    # Every git read below refuses with exit 2 on any failure: a nonzero
    # exit, git not running at all (OSError), or output the locale codec
    # cannot decode (UnicodeDecodeError). It never ends in a traceback.
    try:
        changed_raw = git("diff", "--name-only", merge_base, head)
    except (subprocess.CalledProcessError, OSError, UnicodeDecodeError) as exc:
        print(f"ERROR: git diff failed: {exc}", file=sys.stderr)
        return 2

    changed = [line for line in changed_raw.splitlines() if line]

    if not changed:
        print(empty_pr_range_message(merge_base, head), file=sys.stderr)
        return 2

    try:
        diff = added_line_diff([merge_base, head], [":(top)" + CHANGELOG_PATH])
    except (subprocess.CalledProcessError, OSError) as exc:
        print(f"ERROR: git diff failed: {exc}", file=sys.stderr)
        return 2

    if not diff:
        print(f"OK: {CHANGELOG_PATH} not modified between {merge_base[:8]} and {head} "
              f"({len(changed)} file(s) changed); the public record is weekly.")
        return 0

    try:
        added = {number for path, number, _ in parse_numbered_added_lines(diff)
                 if path == CHANGELOG_PATH}
    except ChangelogDiffUnreadable as exc:
        print(f"ERROR: the {CHANGELOG_PATH} diff could not be read: {exc}", file=sys.stderr)
        return 2

    if not added:
        print(f"OK: no line added to {CHANGELOG_PATH}.")
        return 0

    try:
        head_text = read_blob(head, CHANGELOG_PATH).decode("utf-8")
    except GitQueryFailed as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except UnicodeDecodeError as exc:
        print(f"ERROR: {CHANGELOG_PATH} at {head} is not UTF-8: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"ERROR: git show failed: {exc}", file=sys.stderr)
        return 2

    refused = refusals(added, head_text)
    if not refused:
        print(f"OK: {len(added)} added {CHANGELOG_PATH} line(s) belong to the weekly record "
              "(weekly or monthly paragraphs, legacy weekly sections or the preamble).")
        return 0

    print(
        f"FAIL: {len(refused)} added {CHANGELOG_PATH} line(s) are not part of the weekly "
        "public record. The public changelog carries only weekly paragraphs "
        "(**Week of YYYY-MM-DD (PRs #FIRST-#LAST)**) and, older than 3 months, monthly "
        "paragraphs (**YYYY-MM (PRs #FIRST-#LAST)**); write each change's own entry to the "
        "private per-change record instead:",
        file=sys.stderr,
    )
    for row in refused:
        print(f"  {row}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
