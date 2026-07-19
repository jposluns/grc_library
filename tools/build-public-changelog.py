#!/usr/bin/env python3
"""Project the root CHANGELOG.md into the tiered public form (TODO section 1.19.10).

The tiered public-CHANGELOG model (maintainer-approved, locked at the #1020
handoff): the public root ``CHANGELOG.md`` keeps only a recency-tiered
projection, while the full per-PR record (the compact root entries and the
detailed mirror) is the private source. FOUR tiers (TODO section 1.22.5 added the
daily tier on top of the original three), by the entry date relative to the run's
"current day" and "current week":

  1. CURRENT DAY: the per-PR compact entries are kept VERBATIM
     (``**YYYY-MM-DD | X.Y.Z | PR #N** - <summary>``).
  2. PREVIOUS DAYS STILL IN THE CURRENT WEEK: each day collapses to ONE daily
     paragraph, headed ``**YYYY-MM-DD (PRs #FIRST-#LAST)**``, with a short
     accomplishments summary (at most 4 sentences), condensed once the next day
     begins (the day-boundary trigger).
  3. OLDER, WITHIN 3 MONTHS: each completed ISO week (Monday-Sunday) collapses to
     ONE weekly paragraph, headed ``**Week of YYYY-MM-DD (PRs #FIRST-#LAST)**``,
     with a short accomplishments summary (the locked shape: at most 4 sentences).
  4. OLDER THAN 3 MONTHS: each calendar month collapses to one monthly paragraph,
     headed ``**YYYY-MM (PRs #FIRST-#LAST)**``.

WHY A SCAFFOLD, NOT A FULL GENERATOR. A week can hold dozens of PRs; a faithful
"at most 4 sentences" accomplishments paragraph is an AUTHORED condensation, not
a mechanical join, so this tool cannot write the final prose. It produces the
tiered STRUCTURE and, for each collapsed week/month, a placeholder paragraph
carrying the PR range and the constituent per-PR summaries as raw material, which
the orchestrator/maintainer condenses at the one-time tiering migration (TODO
section 1.19.10 slice 2). This is the "maintainer-side generated projection" the
model names: the tool scaffolds, a human authors the summary.

NOT A CI --check GATE. Unlike the taxonomy/portal generators, this projection is
NOT verified by CI: its source (the full per-PR record) moves to
``grc_library_private`` under section 1.19.10, and no public gate may reach a
private sibling (the sibling-independence invariant, ``check-portability.sh``).
It is a maintainer-side generator run when the tiering is refreshed.

D8 INTERACTION. The PR-time length gate D8 (``check-changelog-length-on-pr.py``)
and its advisory sibling (``audit-changelog-entry-length.py``) match ONLY the
per-PR compact header ``**YYYY-MM-DD | X.Y.Z | PR #N** - ...``; a daily
(``**YYYY-MM-DD (PRs ...)**``), weekly (``**Week of ...**``), or monthly
(``**YYYY-MM ...**``) paragraph header does NOT match, so those tiers are out of
D8's scope with no gate change. Only the CURRENT-DAY per-PR tier is length-gated,
which is the intended behaviour.

Modes (mutually exclusive; default --dry-run):
    --dry-run     report the tiering plan (counts per tier); touch nothing.
    --emit PATH   write the tiered projection to PATH (default: stdout is NOT
                  used; PATH must be given). This produces a SCAFFOLD whose
                  weekly/monthly paragraphs are placeholders to be authored; it
                  is the slice-2 migration input, not a finished artefact.
    --self-test   run the inline unit tests and exit.

Options:
    --source PATH   the per-PR CHANGELOG source (default: CHANGELOG.md).
    --as-of DATE    YYYY-MM-DD; that DAY is kept per-PR verbatim and earlier days
                    in its ISO week collapse to daily paragraphs (default: today, UTC).
    --months N      the within-N-months weekly-tier window (default 3).

Exit codes: 0 success; 2 usage error.
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# A compact root entry. The `| PR #N` segment is OPTIONAL: the oldest ~34
# entries (the pre-PR-number era, 2026-05-31 to 2026-06-19) use the form
# `**YYYY-MM-DD | VERSION** - summary` with no PR number, while later entries add
# `| PR #N`. Both must be projected (dropping the no-PR entries would lose the
# earliest weeks). group(3) (the PR number) is None for a no-PR entry.
ENTRY_RE = re.compile(
    r"^\*\*(\d{4}-\d{2}-\d{2}) \| ([^|]+?)(?: \| PR #(\d+))?\*\* - (.+)$"
)


def monday_of(d: datetime.date) -> datetime.date:
    return d - datetime.timedelta(days=d.weekday())


def parse_entries(text: str) -> tuple[str, list[dict]]:
    """Split the source into (preamble, entries).

    ``preamble`` is every line up to the first per-PR entry. ``entries`` is an
    ordered list of dicts (date, version, pr, summary, raw) for each per-PR
    compact line; non-entry lines after the first entry (blank separators) are
    not carried (the tiered output re-inserts its own spacing).
    """
    lines = text.splitlines()
    preamble: list[str] = []
    i = 0
    while i < len(lines) and not ENTRY_RE.match(lines[i]):
        preamble.append(lines[i])
        i += 1
    entries: list[dict] = []
    for line in lines[i:]:
        m = ENTRY_RE.match(line)
        if not m:
            continue
        entries.append(
            {
                "date": datetime.date.fromisoformat(m.group(1)),
                "version": m.group(2).strip(),
                "pr": int(m.group(3)) if m.group(3) else None,
                "summary": m.group(4).strip(),
                "raw": line,
            }
        )
    return "\n".join(preamble), entries


def tier_of(d: datetime.date, as_of: datetime.date, current_week: datetime.date,
            window_start: datetime.date) -> str:
    """Return 'current', 'daily', 'weekly', or 'monthly' for an entry date.

    Daily model (TODO section 1.22.5): the CURRENT DAY (``as_of``) is kept per-PR
    verbatim; each PREVIOUS DAY still within the current week collapses to ONE
    daily summary paragraph; older weeks/months collapse as before. A previous
    day is condensed once the next day begins (the day-boundary trigger)."""
    if d == as_of:
        return "current"
    if monday_of(d) >= current_week:
        return "daily"
    if d >= window_start:
        return "weekly"
    return "monthly"


def _pr_range(prs: list[int]) -> str:
    lo, hi = min(prs), max(prs)
    return f"#{lo}" if lo == hi else f"#{lo}-#{hi}"


def _entry_tag(e: dict) -> str:
    """The scaffold-bullet tag for an entry: its PR number, or its version for a
    pre-PR-number (no-PR) entry."""
    return f"PR #{e['pr']}" if e["pr"] is not None else f"v{e['version']}"


def _group_label(grp: list[dict]) -> str:
    """A tier-header label: a PR range when the group has PR entries, else a
    version range (the pre-PR-number weeks). ``grp`` is newest-first, so
    ``grp[-1]`` is the oldest and ``grp[0]`` the newest."""
    prs = [e["pr"] for e in grp if e["pr"] is not None]
    if prs:
        return f"PRs {_pr_range(prs)}"
    return f"versions {grp[-1]['version']} to {grp[0]['version']}"


def project(entries: list[dict], as_of: datetime.date,
            current_week: datetime.date, window_start: datetime.date) -> str:
    """Return the tiered projection body (no preamble)."""
    current: list[dict] = []
    daily: dict[datetime.date, list[dict]] = {}
    weekly: dict[datetime.date, list[dict]] = {}
    monthly: dict[str, list[dict]] = {}
    for e in entries:
        t = tier_of(e["date"], as_of, current_week, window_start)
        if t == "current":
            current.append(e)
        elif t == "daily":
            daily.setdefault(e["date"], []).append(e)
        elif t == "weekly":
            weekly.setdefault(monday_of(e["date"]), []).append(e)
        else:
            monthly.setdefault(e["date"].strftime("%Y-%m"), []).append(e)

    out: list[str] = []
    # Current day: verbatim per-PR entries, newest-first (source order).
    for e in current:
        out.append(e["raw"])
        out.append("")
    # Daily tier (previous days still in the current week): newest day first.
    for day in sorted(daily, reverse=True):
        grp = daily[day]
        out.append(f"**{day.isoformat()} ({_group_label(grp)})**")
        out.append("")
        out.append(
            f"<!-- TIER-SCAFFOLD: author an accomplishments summary of at most "
            f"4 sentences for {day.isoformat()} ({len(grp)} entries); raw "
            f"per-entry material below, delete after authoring. -->"
        )
        for e in grp:
            out.append(f"- {_entry_tag(e)}: {e['summary']}")
        out.append("")
    # Weekly tier: newest week first.
    for wk in sorted(weekly, reverse=True):
        grp = weekly[wk]
        out.append(f"**Week of {wk.isoformat()} ({_group_label(grp)})**")
        out.append("")
        out.append(
            f"<!-- TIER-SCAFFOLD: author an accomplishments summary of at most "
            f"4 sentences for this week ({len(grp)} entries); raw per-entry "
            f"material below, delete after authoring. -->"
        )
        for e in grp:
            out.append(f"- {_entry_tag(e)}: {e['summary']}")
        out.append("")
    # Monthly tier: newest month first.
    for mo in sorted(monthly, reverse=True):
        grp = monthly[mo]
        out.append(f"**{mo} ({_group_label(grp)})**")
        out.append("")
        out.append(
            f"<!-- TIER-SCAFFOLD: author a monthly accomplishments summary for "
            f"{mo} ({len(grp)} entries); raw per-entry material below, delete "
            f"after authoring. -->"
        )
        for e in grp:
            out.append(f"- {_entry_tag(e)}: {e['summary']}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def plan_counts(entries: list[dict], as_of: datetime.date,
                current_week: datetime.date,
                window_start: datetime.date) -> dict[str, int]:
    counts = {"current": 0, "daily": 0, "weekly": 0, "monthly": 0}
    for e in entries:
        counts[tier_of(e["date"], as_of, current_week, window_start)] += 1
    return counts


def self_test() -> int:
    import unittest

    class T(unittest.TestCase):
        def _entries(self):
            src = (
                "# Changelog\n\nintro line\n\n"
                "**2026-07-15 | 2026.07.9 | PR #100** - recent one.\n\n"
                "**2026-07-14 | 2026.07.8 | PR #99** - recent two.\n\n"
                "**2026-07-08 | 2026.07.7 | PR #98** - last week a.\n\n"
                "**2026-07-06 | 2026.07.6 | PR #97** - last week b.\n\n"
                "**2026-05-04 | 2026.05.1** - may pre-PR internal.\n\n"
                "**2026-03-10 | 2026.03.1 | PR #50** - old one.\n"
            )
            return parse_entries(src)

        def test_parse(self):
            pre, entries = self._entries()
            self.assertIn("# Changelog", pre)
            # The no-PR entry (2026-05-04) parses with pr=None, not dropped.
            self.assertEqual([e["pr"] for e in entries],
                             [100, 99, 98, 97, None, 50])

        def test_tiers(self):
            _, entries = self._entries()
            as_of = datetime.date(2026, 7, 15)
            cw = monday_of(as_of)  # 2026-07-13
            ws = datetime.date(2026, 4, 15)  # ~3 months before as-of
            counts = plan_counts(entries, as_of, cw, ws)
            # 100 (07-15 == as_of) current-day; 99 (07-14, same week) -> daily;
            # 98/97 (wk 07-06) + the no-PR 05-04 -> weekly; 50 (March) -> monthly.
            self.assertEqual(
                counts, {"current": 1, "daily": 1, "weekly": 3, "monthly": 1})

        def test_project_keeps_current_verbatim_and_scaffolds_rest(self):
            _, entries = self._entries()
            as_of = datetime.date(2026, 7, 15)
            cw = monday_of(as_of)
            ws = datetime.date(2026, 4, 15)
            body = project(entries, as_of, cw, ws)
            self.assertIn("**2026-07-15 | 2026.07.9 | PR #100** - recent one.", body)
            # A previous day still in the current week -> a daily summary paragraph.
            self.assertIn("**2026-07-14 (PRs #99)**", body)
            self.assertIn("**Week of 2026-07-06 (PRs #97-#98)**", body)
            self.assertIn("**2026-03 (PRs #50)**", body)
            self.assertIn("TIER-SCAFFOLD", body)
            # A current-week PR is NOT re-listed under a weekly scaffold bullet.
            self.assertNotIn("- PR #100:", body)
            # No-PR entry: bucketed (NOT dropped), with a version-range header
            # and a version-tagged bullet.
            self.assertIn(
                "**Week of 2026-05-04 (versions 2026.05.1 to 2026.05.1)**", body)
            self.assertIn("- v2026.05.1: may pre-PR internal.", body)
            # Full conservation: every source entry appears exactly once, as a
            # verbatim current entry OR a scaffold bullet (6 in, 6 out).
            verbatim = len([ln for ln in body.splitlines() if ENTRY_RE.match(ln)])
            bullets = len([ln for ln in body.splitlines() if ln.startswith("- ")])
            self.assertEqual(verbatim + bullets, 6)

    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(T))
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", default=True)
    mode.add_argument("--emit", metavar="PATH")
    mode.add_argument("--self-test", action="store_true")
    ap.add_argument("--source", default=str(REPO_ROOT / "CHANGELOG.md"))
    ap.add_argument("--as-of")
    ap.add_argument("--months", type=int, default=3)
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    src = Path(args.source)
    if not src.is_file():
        print(f"ERROR: source not found at {src}", file=sys.stderr)
        return 2
    as_of = (datetime.date.fromisoformat(args.as_of) if args.as_of
             else datetime.datetime.now(datetime.timezone.utc).date())
    current_week = monday_of(as_of)
    # Window start: approximate N months as N*30 days before as_of, floored to a
    # Monday so a week is wholly inside or outside the weekly tier.
    window_start = monday_of(as_of - datetime.timedelta(days=args.months * 30))

    preamble, entries = parse_entries(src.read_text(encoding="utf-8"))
    counts = plan_counts(entries, as_of, current_week, window_start)
    print(f"Source: {src} ({len(entries)} per-PR entries)")
    print(f"Current day (verbatim per-PR): {as_of.isoformat()}")
    print(f"Weekly tier window start: {window_start.isoformat()} "
          f"(within {args.months} months)")
    print(f"Tiers: {counts['current']} current-day per-PR, "
          f"{counts['daily']} to daily paragraphs, "
          f"{counts['weekly']} to weekly paragraphs, "
          f"{counts['monthly']} to monthly paragraphs.")

    if args.emit:
        body = project(entries, as_of, current_week, window_start)
        out = (preamble.rstrip() + "\n\n" + body) if preamble.strip() else body
        Path(args.emit).write_text(out, encoding="utf-8")
        print(f"Emitted tiered projection SCAFFOLD to {args.emit} "
              f"(weekly/monthly paragraphs are placeholders to author).")
        return 0

    print("\n(dry-run; nothing written. Use --emit PATH to write the scaffold.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
