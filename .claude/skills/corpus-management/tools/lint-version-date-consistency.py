#!/usr/bin/env python3
"""Version-date consistency audit for the library CHANGELOG and README.

This linter enforces invariants about the library's CalVer
(``YYYY.MM.patch``) version recorded in [README.md] and the dated
section headings in [.working/CHANGELOG.md]. Invariants 1 and 2 read a
per-change heading; invariant 3 reads a weekly summary heading:

  1. The most recent CHANGELOG entry heading (matched in BOTH the compact
     ``**YYYY-MM-DD | YYYY.MM.patch | PR #N**`` form the root-CHANGELOG
     reformat introduced and the legacy ``## YYYY-MM-DD, Library Version
     YYYY.MM.patch`` form) has a date whose ``YYYY-MM`` equals the library
     version's ``YYYY.MM``.

  2. The current README.md ``**Library Version:**`` field equals the
     library version recorded in the most recent CHANGELOG heading.

  3. The README.md ``**Library Version:**`` field's ``YYYY.MM`` is not
     earlier than the ``YYYY-MM`` of the newest weekly summary heading's
     week (its Monday), read in both the ``**Week of YYYY-MM-DD (PRs
     #FIRST-#LAST)**`` form (or ``(PRs #FIRST)``) and the legacy ``## Week of
     YYYY-MM-DD`` form, the root grammar of gate 59 and delta check D1
     (``changelog_diff.WEEKLY_HEADER_RE`` and ``LEGACY_WEEK_HEADING_RE``).
     A weekly heading whose date is not a valid calendar date is a finding.

What the weekly-only changelog leaves checkable. Under the weekly-only public
changelog rule the public changelog carries weekly summaries only, so it holds no
per-change heading and names no library version: invariants 1 and 2 then
find nothing to read. A weekly heading names only the Monday of a week
whose changes have all merged, so the README version, which records the
year and month of the most recent merge, can be no earlier than that
Monday's year and month (invariant 3). Not checked here: a README month
later than the newest weekly heading, which is legitimate because the summary
of the current week is written only after the week ends; and the month of a
change that no weekly heading summarizes yet. A monthly heading
(``**YYYY-MM (PRs #FIRST-#LAST)**``) is not read. The patch number is
checked in the PR range instead, by the README version-floor check below.

README version-floor check (in a PR range the README version never falls below
the merge base's; an unchanged version passes). With ``--base REF`` (and
``--head REF``, default HEAD) the audit runs this check alone: the README.md
``**Library Version:**`` at the head is not below the one at the merge base of
the two refs, compared as ``(year, month, patch)``, so within a month the patch
never falls below the merge base's (an unchanged version passes), and a new month
may reset it. A README.md that is absent, or that has no
Library Version field, at either end is a finding that names that end, and so is
a field whose value is not a valid ``YYYY.MM.patch`` (README_VERSION_RE, built from
the README field grammar, whose label starts a line). The range
is resolved as the delta checks resolve it (``lint_common.resolve_pr_range``), so
a collapsed range, a missing base or more than one merge base exits 2. The full
audit runner (``run_all_audits.sh``) runs this audit without a range, so the check
runs in ``.claude/skills/corpus-management/tools/run-pr-time-checks.sh`` (as "Gate 29
README version-floor check", beside the delta checks), which the pre-push guard runs,
and not in CI: the pull-request job in ``.github/workflows/quality.yml`` does not run
it. A README ahead of the version a
changelog heading names is not checked, because a weekly heading names none.

Fail closed. A changelog that holds no weekly summary heading of either form
and no per-change heading fails (exit 1, naming the condition; exit 2 for an
explicit --changelog, as before): the gate never passes having compared nothing.

Coverage kept across the weekly-only changelog. At main d7387bf3 the audit read
only per-change headings (the legacy ``## YYYY-MM-DD, Library Version ...`` form,
with or without its PR clause, and the compact ``**YYYY-MM-DD | ... | PR #N**``
form). Each case is mapped to a test on the new input, the newest weekly heading
and the README, that fails when weekly reading is switched off
(VersionDateConsistencyTests in tests/test_linters.py):

    case at d7387bf3                          test on the new input
    inv. 1, legacy form, version month        test_case_v1_inv3_legacy_week_heading_readme_prior_month_flagged
      earlier than the date month               (flagged by inv. 3: a week heading names
                                                no version, so inv. 1 has nothing to read)
    inv. 1, compact form, same                test_case_v2_inv3_bold_week_heading_readme_prior_month_flagged
                                                (flagged by inv. 3, as for v1)
    inv. 1, legacy form with PR clause        test_case_v3_inv3_single_pr_week_heading_readme_prior_month_flagged
                                                (flagged by inv. 3, as for v1)
    inv. 1, version month LATER than the      not checked, by design: a README month
      date month                                later than the
                                                newest week is legitimate (that week's
                                                summary is written after it ends); pinned
                                                by test_weekly_heading_readme_same_or_later_month_passes
    inv. 2, README behind the newest          test_case_v5_readme_not_bumped_into_newest_week_month_flagged
      version, across a month
    inv. 2, README behind or ahead within     covered for a README that falls, in the PR
      the month (patch drift) or ahead          range, by the README version-floor check
                                                (--base), in
                                                ReadmeVersionRiseOnPrTests:
                                                test_patch_rise_passes,
                                                test_patch_fall_flagged,
                                                test_month_change_with_patch_reset_passes,
                                                test_earlier_month_flagged,
                                                test_field_missing_at_head_flagged,
                                                test_field_missing_at_merge_base_flagged;
                                                a README ahead is not checked (a weekly
                                                heading names no version)
    README without a Library Version field    test_case_v7_weekly_heading_readme_without_version_field_flagged
    each heading form parsed (passes when     test_case_v8_each_weekly_form_with_matching_readme_passes
      consistent)
    the most recent heading is the one        test_case_v9_newest_week_compared_wherever_it_sits
      compared
    default changelog with no heading:        replaced by fail-closed:
      pass with a note                          test_default_changelog_without_any_heading_fails_closed
    explicit changelog with no heading:       unchanged (FileArgRefusalTests)
      exit 2

Why both invariants are needed:

The first invariant catches the failure mode where an author dates a
CHANGELOG entry for today's calendar date but carries over the prior
month's ``YYYY.MM`` in the library version. In the earlier repository,
this happened on 2026-06-01, when six successive entries used
``2026.05.x`` while every entry was dated ``2026-06-01``; the
version-monotonicity audit treats ``2026.05.x`` as monotonic (tuple
comparison) and does not validate the month against the entry's date. Per
``governance/specification-master-project.md`` section 4.5, ``YYYY.MM`` is the
year and month of the most recent merge to ``main`` and ``patch``
resets to 0 when the month rolls over.

The second invariant catches the drift case where the README's
``**Library Version:**`` is bumped without a CHANGELOG entry, or a
CHANGELOG entry is added with a higher version than the README
records. Both halves must agree because the README is the
adopter-facing snapshot pointer and the CHANGELOG is the audit trail
that explains how the snapshot got to this state.

Usage:

    python3 .claude/skills/corpus-management/tools/lint-version-date-consistency.py
    python3 .claude/skills/corpus-management/tools/lint-version-date-consistency.py \\
        --changelog tests/tmp/fake-changelog.md \\
        --readme tests/tmp/fake-readme.md
    python3 .claude/skills/corpus-management/tools/lint-version-date-consistency.py \\
        --base origin/main --head HEAD

The ``--changelog`` and ``--readme`` flags override the default
file locations (``.working/CHANGELOG.md`` and ``README.md`` at the repo root)
and are used by the gate-36 regression test suite for synthetic
fixtures.

Exit codes:
    0 - every invariant that applies holds.
    1 - one or more inconsistency findings, the default changelog has neither
        a Library Version heading nor a weekly summary heading (fail-closed), or
        the default changelog or readme cannot be read.
    2 - an explicit --changelog or --readme is empty, not a regular file,
        unreadable or not UTF-8, or an explicit changelog has neither a
        Library Version heading nor a weekly summary heading (nothing would
        be verified).

    With --base, the README version-floor check alone: 0 the head's README
    Library Version is not below the merge base's; 1 it is below, or a README
    without a valid field at either end; 2 the range cannot be resolved (as the
    delta checks refuse it), README.md cannot be read at an end, --head without
    --base, or --base with --changelog or --readme.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

# The tool's own directory, appended to the END of sys.path (gate 109), so the
# sibling modules resolve under python3 -I and a file planted beside the tool
# cannot shadow the standard library.
sys.path.append(str(Path(__file__).resolve().parent))
# The weekly heading forms of the public changelog, shared with delta check D1.
from changelog_diff import LEGACY_WEEK_HEADING_RE, WEEKLY_HEADER_RE  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[4]

# Heading shape:
#   ## YYYY-MM-DD, Library Version YYYY.MM.patch
#   ## YYYY-MM-DD, Library Version YYYY.MM.patch, PR #N
# The trailing PR clause is the convention from library version
# 2026.06.25 forward. It is optional, so historical entries that
# predate the convention continue to parse.
CHANGELOG_HEADING_RE = re.compile(
    r"^##\s+(\d{4})-(\d{2})-(\d{2}),\s+Library Version\s+(\d+)\.(\d+)\.(\d+)"
    r"(?:,\s+PR\s+#\d+)?"
    r"\s*$",
    re.MULTILINE,
)

# The compact heading, same six capture groups, optional PR clause and
# optional summary tail.
COMPACT_HEADING_RE = re.compile(
    r"^\*\*(\d{4})-(\d{2})-(\d{2}) \| (\d+)\.(\d+)\.(\d+)"
    r"(?: \| PR #\d+)?\*\*(?: - .*)?$",
    re.MULTILINE,
)

# README field grammar. The defining rule is governance/specification-master-project.md
# section 4.5: "The library version is `YYYY.MM.patch` where:", "`YYYY` is the
# four-digit year", "`MM` is the two-digit month" and "`patch` is a sequential counter
# that increments on every merge to `main` within the same `YYYY.MM` window. It resets
# to `0` when the month rolls over." The value productions quote the words they come
# from; label, sep and end describe the field as README.md's metadata block writes it.
# The pattern is built from these productions alone (README_LABEL to README_END):
#
#   field  = line-start label sep value end
#   label  = "**Library Version:**"      the field as README.md's metadata block shows it
#   sep    = 1*(SP / HTAB)               the value sits on the label's line ([ \t]+, not
#                                        \s+, which crosses a line end)
#   value  = year "." month "." patch    "`YYYY.MM.patch`"
#   year   = 4DIGIT                      "`YYYY` is the four-digit year"
#   month  = "0" %x31-39 / "1" %x30-32   "`MM` is the two-digit month": 01 to 12
#   patch  = "0" / %x31-39 *DIGIT        "a sequential counter" that "resets to `0`": 0,
#                                        or a number with no leading zero
#   DIGIT  = %x30-39                     ASCII 0 to 9 only ([0-9], not \d, which in a
#                                        str pattern matches any Unicode digit)
#   end    = SP / HTAB / CR / LF / "\" [CR] LF / end-of-text
#                                        looked at, not consumed: a space, tab, carriage
#                                        return or line feed, a backslash line break (a
#                                        backslash, an optional carriage return, then a
#                                        line feed) or the end of the text
#
# line-start is the start of the text or the position after a line feed, so a prose
# mention of the label inside a line ("The **Library Version:** field ...") is not the
# field. Any other character joined to the value is refused, not cut off: 2026.11.0.7,
# 2026.11.0-rc1, 2026.11.0:1, 2026.11.0/1, 2026.11.0,1, and a backslash that does not
# start a line break (2026.11.0\1, and 2026.11.0\.7 and 2026.11.0\-rc1, which Markdown
# renders as 2026.11.0.7 and 2026.11.0-rc1).
README_LABEL = r"\*\*Library Version:\*\*"
README_SEP = r"[ \t]+"
README_YEAR = r"([0-9]{4})"
README_MONTH = r"(0[1-9]|1[0-2])"
README_PATCH = r"(0|[1-9][0-9]*)"
README_END = r"(?=[ \t\r\n]|\\\r?\n|\Z)"
README_VERSION_RE = re.compile(
    "^" + README_LABEL + README_SEP + README_YEAR + r"\." + README_MONTH + r"\."
    + README_PATCH + README_END,
    re.MULTILINE,
)
# The field's label alone, at the start of a line (line-start label above). The first
# such label is the field read, so a malformed value is named as malformed, not reported
# as missing or passed over for a later valid field.
README_FIELD_RE = re.compile("^" + README_LABEL, re.MULTILINE)

# The README the version-floor check reads at both ends of a PR range.
README_PATH = "README.md"


def readme_field(text: str) -> tuple[bool, re.Match[str] | None]:
    """The first README ``**Library Version:**`` field (its label at the start of a line)
    as ``(label found, match)``; the match is None when there is no such label or the
    first such label's value is malformed."""
    label = README_FIELD_RE.search(text)
    if not label:
        return False, None
    return True, README_VERSION_RE.match(text, label.start())


def weekly_headings(changelog_text: str) -> list[tuple[int, str, date | None]]:
    """Every weekly summary heading as ``(line number, line, week date or None)``.

    Lines are split on LF only, as gate 59 reads the root, and a CR before the LF
    is part of the line ending. The date is None when it is not a valid calendar
    date.
    """
    found: list[tuple[int, str, date | None]] = []
    for lineno, raw in enumerate(changelog_text.split("\n"), start=1):
        line = raw[:-1] if raw.endswith("\r") else raw
        match = WEEKLY_HEADER_RE.match(line) or LEGACY_WEEK_HEADING_RE.match(line)
        if not match:
            continue
        try:
            week = date.fromisoformat(match.group(1))
        except ValueError:
            week = None
        found.append((lineno, line, week))
    return found


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify CHANGELOG entry dates match their Library Version YYYY.MM "
        "and that the README's Library Version matches the most recent CHANGELOG entry, "
        "and that the README's YYYY.MM is not earlier than the newest weekly summary heading's week."
    )
    parser.add_argument(
        "--changelog",
        default=None,
        help="Path to the CHANGELOG file (default: repo root .working/CHANGELOG.md).",
    )
    parser.add_argument(
        "--readme",
        default=None,
        help="Path to the README file (default: repo root README.md).",
    )
    parser.add_argument(
        "--base",
        default=None,
        help="Base ref of a PR range. With it, only the README version-floor check runs: "
        "the README Library Version at --head must not be below the one at the merge base.",
    )
    parser.add_argument(
        "--head",
        default=None,
        help="Head ref of the PR range (default: HEAD); only with --base.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.head is not None and args.base is None:
        print("ERROR: --head needs --base; nothing would be verified.", file=sys.stderr)
        return 2
    if args.base is not None:
        if args.changelog is not None or args.readme is not None:
            print("ERROR: --base runs the README version-floor check alone, which reads "
                  "README.md from git at both ends; it takes no --changelog or --readme.",
                  file=sys.stderr)
            return 2
        return readme_rise_check(args.base, args.head or "HEAD")
    # An explicitly named file must be a regular file (in the earlier repository, an empty
    # value was Path('.'), a directory read failed only with exit 1, and a wrong file passed
    # as "nothing to verify"). Explicitness is whether the flag was given at all (in the
    # earlier repository, comparing the value to the default string treated an explicitly
    # passed default path as omitted).
    explicit = {"--changelog": args.changelog is not None, "--readme": args.readme is not None}
    if args.changelog is None:
        args.changelog = str(REPO_ROOT / ".working/CHANGELOG.md")
    if args.readme is None:
        args.readme = str(REPO_ROOT / "README.md")
    changelog_path = Path(args.changelog)
    readme_path = Path(args.readme)
    for flag, value in (("--changelog", args.changelog), ("--readme", args.readme)):
        if explicit[flag] and (not value.strip() or not Path(value).is_file()):
            print(f"ERROR: {flag} {value!r}: not a regular file; nothing would be verified.",
                  file=sys.stderr)
            return 2
    findings: list[str] = []

    try:
        changelog_text = changelog_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:  # in the earlier repository, a non-UTF-8 file raised a traceback
        print(f"ERROR: cannot read changelog at {changelog_path}: {exc}", file=sys.stderr)
        return 2 if explicit["--changelog"] else 1
    try:
        readme_text = readme_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"ERROR: cannot read readme at {readme_path}: {exc}", file=sys.stderr)
        return 2 if explicit["--readme"] else 1

    # Find the FIRST (most recent) Library-Version heading in the CHANGELOG.
    candidates = [m for m in (CHANGELOG_HEADING_RE.search(changelog_text),
                              COMPACT_HEADING_RE.search(changelog_text)) if m]
    first_match = min(candidates, key=lambda m: m.start()) if candidates else None
    weekly = weekly_headings(changelog_text)
    if not first_match and not weekly and explicit["--changelog"]:
        print(f"ERROR: --changelog {changelog_path}: no Library Version section heading or "
              f"weekly summary heading found; an explicitly named changelog must carry one.",
              file=sys.stderr)
        return 2
    if not first_match and not weekly:
        # Fail closed: with no heading of either kind there is nothing to compare the README
        # version with, and a pass would hide that.
        print(
            f"FAIL: {changelog_path.name} holds no weekly summary heading ('## Week of "
            f"YYYY-MM-DD' or '**Week of YYYY-MM-DD (PRs #A-#B)**') and no per-change "
            f"Library Version heading, so the README version cannot be compared with "
            f"it; the gate fails closed."
        )
        return 1

    has_field, readme_match = readme_field(readme_text)
    if has_field and not readme_match:
        findings.append(
            f"{readme_path.name}: the '**Library Version:**' field is not a valid "
            f"'YYYY.MM.patch' (a four-digit year, a month 01 to 12, a patch from 0 with no "
            f"leading zero, in ASCII digits on the label's line, and nothing joined "
            f"after it); see "
            f"governance/specification-master-project.md section 4.5."
        )
    elif not readme_match:
        findings.append(
            f"{readme_path.name}: no '**Library Version:** YYYY.MM.patch' "
            f"field found in the metadata block."
        )
    if first_match:
        per_change_findings(first_match, readme_match, changelog_path, readme_path, findings)
    if weekly:
        weekly_findings(weekly, readme_match, changelog_path, readme_path, findings)

    if not findings:
        return 0

    print(f"=== {changelog_path.name} / {readme_path.name} ===")
    for finding in findings:
        print(f"  {finding}")
    print(
        f"\nFAIL: {len(findings)} version-date inconsistency finding(s). "
        f"See governance/specification-master-project.md section 4.5 for the CalVer rule."
    )
    return 1


def per_change_findings(first_match, readme_match, changelog_path: Path, readme_path: Path,
                        findings: list[str]) -> None:
    """Invariants 1 and 2, against the most recent per-change heading."""
    date_y, date_m, date_d = (int(first_match.group(i)) for i in (1, 2, 3))
    ver_y, ver_m, ver_p = (int(first_match.group(i)) for i in (4, 5, 6))

    # Invariant 1: the entry's date YYYY-MM must equal the version's YYYY.MM.
    # Rationale: governance/specification-master-project.md section 4.5 defines YYYY.MM
    # as the year and month of the merge to main. The CHANGELOG heading
    # date is the source of truth for "when this happened"; the version
    # must agree.
    if (date_y, date_m) != (ver_y, ver_m):
        findings.append(
            f"{changelog_path.name}: most recent entry is dated "
            f"{date_y:04d}-{date_m:02d}-{date_d:02d} but the Library "
            f"Version is {ver_y}.{ver_m:02d}.{ver_p}; the YYYY-MM portion "
            f"of the date and the YYYY.MM portion of the version must "
            f"match per governance/specification-master-project.md section 4.5."
        )

    # Invariant 2: README's Library Version equals the most recent CHANGELOG
    # entry's version. The README is the canonical "current snapshot" pointer.
    if readme_match:
        rl_y, rl_m, rl_p = (int(readme_match.group(i)) for i in (1, 2, 3))
        if (rl_y, rl_m, rl_p) != (ver_y, ver_m, ver_p):
            findings.append(
                f"{readme_path.name} records Library Version "
                f"{rl_y}.{rl_m:02d}.{rl_p}, but the most recent "
                f"{changelog_path.name} entry uses "
                f"{ver_y}.{ver_m:02d}.{ver_p}; the two must agree."
            )


def weekly_findings(weekly: list[tuple[int, str, date | None]], readme_match,
                    changelog_path: Path, readme_path: Path, findings: list[str]) -> None:
    """Invariant 3: the README CalVer is not earlier than the newest weekly heading's week."""
    for lineno, line, week in weekly:
        if week is None:
            findings.append(
                f"{changelog_path.name}:{lineno}: weekly heading {line!r} has no valid "
                f"calendar date, so the README version cannot be compared with it."
            )
    dated = [(week, lineno, line) for lineno, line, week in weekly if week is not None]
    if not dated or not readme_match:
        return
    newest, lineno, line = max(dated)
    rl_y, rl_m, rl_p = (int(readme_match.group(i)) for i in (1, 2, 3))
    if (rl_y, rl_m) < (newest.year, newest.month):
        findings.append(
            f"{readme_path.name} records Library Version {rl_y}.{rl_m:02d}.{rl_p}, "
            f"but the newest weekly summary heading ({changelog_path.name}:{lineno}: "
            f"{line}) is the week of {newest.isoformat()}; the version's YYYY.MM must "
            f"not be earlier than that week's YYYY-MM, because every change the week "
            f"summarizes merged on or after its first day."
        )


def readme_calver(text: str | None) -> tuple[int, int, int] | None:
    """The README ``**Library Version:**`` as ``(year, month, patch)``, or None when the
    text is None (no README.md), has no such field or its first such field is malformed."""
    match = readme_field(text)[1] if text is not None else None
    if not match:
        return None
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def readme_rise_check(base: str, head: str) -> int:
    """README version-floor check: the README Library
    Version at ``head`` is not below the one at the merge base of ``base`` and ``head``;
    an unchanged version passes.

    A README.md absent at either end fails closed as a finding (exit 1, "there is no
    README.md"): the absent-file branch is reached, not dropped, because git_show_strict
    returns None when git ls-tree lists no entry at that path, and raises only when git
    itself fails (a listing failure, or a listed blob whose read fails), which is an
    execution error (exit 2). ReadmeVersionRiseOnPrTests.test_field_missing_at_merge_base_flagged
    covers the absent case."""
    import subprocess

    # The range reads are shared with the delta checks; imported here so the
    # audit without a range needs no sibling but changelog_diff.
    from lint_common import PrRangeError, git_show_strict, resolve_pr_range

    try:
        merge_base, head_ref = resolve_pr_range(base, head)
    except PrRangeError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    versions: dict[str, tuple[int, int, int] | None] = {}
    findings: list[str] = []
    for end, ref in (("merge base", merge_base), ("head", head_ref)):
        try:
            text = git_show_strict(ref, README_PATH)
        except (subprocess.CalledProcessError, OSError, ValueError) as exc:
            print(f"ERROR: cannot read {README_PATH} at the {end} {ref}: {exc}", file=sys.stderr)
            return 2
        versions[end] = readme_calver(text)
        if versions[end] is None:
            if text is None:
                absent = "there is no README.md"
            elif readme_field(text)[0]:
                absent = "its value is not a valid YYYY.MM.patch"
            else:
                absent = "it has no field"
            findings.append(
                f"{README_PATH} at the {end} ({ref}) has no '**Library Version:** "
                f"YYYY.MM.patch' field ({absent}), so the version floor cannot be checked."
            )
    old, new = versions["merge base"], versions["head"]
    if old is not None and new is not None and new < old:
        findings.append(
            f"{README_PATH} records Library Version {new[0]}.{new[1]:02d}.{new[2]} at the "
            f"head ({head_ref}), below {old[0]}.{old[1]:02d}.{old[2]} at the merge base "
            f"({merge_base}); compared as (year, month, patch), the head version never "
            f"falls below the merge base's (an unchanged version passes; a new month may "
            f"reset the patch)."
        )
    if findings:
        for finding in findings:
            print(f"FAIL {finding}")
        print(f"\nFAIL: {len(findings)} README version-floor finding(s); in a PR range "
              f"the README version never falls below the merge base's (an unchanged "
              f"version passes).")
        return 1
    print(f"OK: {README_PATH} Library Version {new[0]}.{new[1]:02d}.{new[2]} at the head is not "
          f"below {old[0]}.{old[1]:02d}.{old[2]} at the merge base {merge_base}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
