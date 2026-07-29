#!/usr/bin/env python3
"""Advisory pre-push reminder (D8): flag past UTC dates whose per-PR CHANGELOG
entries have not yet been collapsed into a single daily roll-up.

This is a CI/pre-push advisory check, not a corpus audit gate and not a blocking
delta gate. The root CHANGELOG.md records one compact entry per merged PR:

    **YYYY-MM-DD | X.Y.Z | PR #N** - one-line summary

At the close of a UTC day the orchestrator is meant to collapse that day's
per-PR entries into one daily roll-up entry (and prune the matching detailed
mirror rows):

    **YYYY-MM-DD | X.Y.Z | PRs #A-#B (N PRs)** - one-line day summary

The roll-up is easy to forget, because a day's per-PR entries are individually
correct and nothing else complains. This check scans CHANGELOG.md and, for any
UTC date STRICTLY BEFORE today (UTC) that still carries MORE THAN ONE per-PR
entry (i.e. was never collapsed), WARNS so the next PR carries the roll-up.

It deliberately does NOT warn for:
  * today's date (per-PR entries for the current UTC day are the correct state,
    the day is not over yet),
  * a date already in daily-roll-up form (`PRs #A-#B`), which contributes zero
    per-PR entries to the count,
  * a date with a single lone per-PR entry (already effectively one line).

Scope: root CHANGELOG.md only. HTML-commented regions (e.g. the retained mirror
of a pruned entry) are ignored so a commented-out entry never counts.

Exit status is ALWAYS 0: the finding is advisory (offload the roll-up draft to a
worker), never a push blocker.

Usage:
    python3 tools/check-daily-changelog-rollup.py
    python3 tools/check-daily-changelog-rollup.py --changelog path/to/CHANGELOG.md
    python3 tools/check-daily-changelog-rollup.py --self-test
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from collections import defaultdict
from pathlib import Path

CHANGELOG_PATH = "CHANGELOG.md"

# A compact CHANGELOG entry header:
#   **YYYY-MM-DD | version | PR #N** - ...        (per-PR)
#   **YYYY-MM-DD | version | PRs #A-#B (N PRs)** - ...   (daily roll-up)
# The prfield capture stops at the closing '**'; "PRs" (plural) marks a roll-up,
# "PR #" (singular) marks a per-PR entry.
ENTRY_RE = re.compile(
    r"^\*\*(?P<date>\d{4}-\d{2}-\d{2})\s*\|[^|]*\|\s*(?P<prfield>PRs?\b[^*]*?)\s*\*\*"
)

# Strip HTML-commented regions (including multi-line) before scanning, so a
# retained-but-commented per-PR entry never inflates a date's count.
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)

# A MILESTONE entry (`**YYYY-MM-DD | MILESTONE:** ...`) is a persistent
# project-milestone record, explicitly EXCLUDED from daily/weekly roll-ups
# (maintainer-directed 2026-07-29): it floats above the day's per-PR entries
# and is never condensed. Recognized by the `| MILESTONE` marker in the bold
# header so a milestone written with any trailing field can never be counted.
MILESTONE_RE = re.compile(r"^\*\*\d{4}-\d{2}-\d{2}\s*\|\s*MILESTONE\b", re.IGNORECASE)


def find_rollups_due(text: str, today: datetime.date) -> list[tuple[str, int]]:
    """Return [(date, per_pr_count), ...] for past dates with > 1 per-PR entry.

    A "past" date is any entry date strictly before ``today``. Roll-up entries
    (`PRs #A-#B`) are not counted. Result is sorted by date (oldest first).
    """
    per_pr_by_date: dict[str, int] = defaultdict(int)
    for raw in COMMENT_RE.sub("", text).splitlines():
        stripped = raw.strip()
        if MILESTONE_RE.match(stripped):
            continue  # milestone entries are never rolled up (see MILESTONE_RE)
        m = ENTRY_RE.match(stripped)
        if not m:
            continue
        prfield = m.group("prfield").strip()
        if prfield.startswith("PRs"):
            continue  # already a daily roll-up: contributes no per-PR entries
        if not prfield.startswith("PR #"):
            continue  # unrecognized shape; ignore rather than miscount
        per_pr_by_date[m.group("date")] += 1

    due: list[tuple[str, int]] = []
    for date_str, count in per_pr_by_date.items():
        if count <= 1:
            continue  # a lone entry is already effectively collapsed
        if datetime.date.fromisoformat(date_str) >= today:
            continue  # today (or, defensively, future): not yet due
        due.append((date_str, count))
    return sorted(due)


def report(due: list[tuple[str, int]], stream=sys.stdout) -> int:
    """Print the advisory lines. Returns the number of dates flagged."""
    if not due:
        print(
            "OK: every past UTC date in CHANGELOG.md is either a single daily "
            "roll-up or a lone entry; no summarization outstanding.",
            file=stream,
        )
        return 0
    for date_str, count in due:
        print(
            f"DAILY SUMMARY DUE for {date_str}: {count} per-PR entries not yet "
            f"rolled up; the next PR should include the daily roll-up "
            f"(offload the draft)",
            file=stream,
        )
    return len(due)


def _self_test() -> int:
    import unittest

    TODAY = datetime.date(2026, 7, 26)

    def entry(date: str, pr: int) -> str:
        return f"**{date} | 2026.07.{pr} | PR #{pr}** - summary for {pr}."

    def rollup(date: str, a: int, b: int, n: int) -> str:
        return (
            f"**{date} | 2026.07.{b} | PRs #{a}-#{b} ({n} PRs)** - "
            f"day summary for {date}."
        )

    class T(unittest.TestCase):
        def test_past_day_with_multiple_per_pr_is_due(self):
            prs = [1150, 1151, 1152]  # three per-PR entries, yesterday
            txt = "\n".join(entry("2026-07-25", p) for p in prs)
            due = find_rollups_due(txt, TODAY)
            self.assertEqual(len(due), 1)
            self.assertEqual(due[0][0], "2026-07-25")
            self.assertEqual(due[0][1], len(prs))  # dynamic count

        def test_today_multiple_per_pr_is_not_due(self):
            prs = list(range(1180, 1191))  # eleven per-PR entries for today
            txt = "\n".join(entry("2026-07-26", p) for p in prs)
            self.assertEqual(len(find_rollups_due(txt, TODAY)), 0)

        def test_past_day_already_rolled_up_is_not_due(self):
            txt = rollup("2026-07-24", 1108, 1145, 38)
            self.assertEqual(len(find_rollups_due(txt, TODAY)), 0)

        def test_past_day_single_entry_is_not_due(self):
            txt = entry("2026-07-25", 1177)
            self.assertEqual(len(find_rollups_due(txt, TODAY)), 0)

        def test_commented_entries_do_not_count(self):
            live = rollup("2026-07-19", 1039, 1054, 16)
            buried = "\n".join(entry("2026-07-19", p) for p in (1039, 1040, 1041))
            txt = f"{live}\n<!--\n{buried}\n-->\n"
            self.assertEqual(len(find_rollups_due(txt, TODAY)), 0)

        def test_multiple_past_days_each_flagged(self):
            fixtures = {
                "2026-07-23": [1068, 1069, 1070],
                "2026-07-24": [1108, 1109],
            }
            lines = [entry(d, p) for d, prs in fixtures.items() for p in prs]
            due = find_rollups_due("\n".join(lines), TODAY)
            self.assertEqual(len(due), len(fixtures))  # dynamic count
            self.assertEqual(
                {d: c for d, c in due},
                {d: len(prs) for d, prs in fixtures.items()},
            )

        def test_milestone_entry_is_never_counted(self):
            # A milestone floats above the day's per-PR entries and must never
            # inflate a date's roll-up count nor be flagged for rollup itself.
            milestone = "**2026-07-25 | MILESTONE:** A persistent milestone."
            prs = [1150, 1151, 1152]
            txt = milestone + "\n" + "\n".join(entry("2026-07-25", p) for p in prs)
            due = find_rollups_due(txt, TODAY)
            self.assertEqual(len(due), 1)
            self.assertEqual(due[0][1], len(prs))  # milestone NOT added to the 3
            self.assertEqual(len(find_rollups_due(milestone, TODAY)), 0)

        def test_empty_corpus(self):
            self.assertEqual(len(find_rollups_due("", TODAY)), 0)

        def test_report_line_count_matches_due(self):
            import io

            due = [("2026-07-24", 2), ("2026-07-25", 3)]
            buf = io.StringIO()
            self.assertEqual(report(due, stream=buf), len(due))

    suite = unittest.TestLoader().loadTestsFromTestCase(T)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--changelog",
        default=CHANGELOG_PATH,
        help=f"path to the root CHANGELOG.md (default: {CHANGELOG_PATH})",
    )
    ap.add_argument(
        "--self-test",
        action="store_true",
        help="run the inline self-test on constructed fixtures and exit",
    )
    args = ap.parse_args(argv)

    if args.self_test:
        return _self_test()

    path = Path(args.changelog)
    if not path.is_file():
        print(
            f"check-daily-changelog-rollup: {path} not found; nothing to check "
            f"(advisory, exit 0).",
        )
        return 0

    today = datetime.datetime.now(datetime.timezone.utc).date()
    due = find_rollups_due(path.read_text(encoding="utf-8"), today)
    report(due)
    # Advisory only: findings are roll-up-draft candidates, never a push blocker.
    return 0


if __name__ == "__main__":
    sys.exit(main())
