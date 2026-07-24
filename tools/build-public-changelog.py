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
    --condense-completed-week   the RECURRING weekly-rollup wiring (TODO section
                  1.19.10a). At a week boundary it condenses the public root's
                  COMPLETED-week per-PR entries (those in ISO weeks strictly
                  before --as-of's week; the current week stays per-PR) into one
                  weekly placeholder each and appends them to the private
                  full-source, mirroring the sweep tool's emit-verify-prune:
                  --emit-private PATH appends the completed entries (dedup-safe),
                  then --prune (with --verify-private PATH) rewrites the public
                  root once the private side is confirmed, guarded by a re-parse
                  assertion. The placeholder carries the raw per-PR lines in an
                  HTML comment; the one-paragraph weekly summary is AUTHORED by
                  the orchestrator (this tool scaffolds, a human condenses), so
                  the first restructuring run is an ATTENDED close-out step. This
                  is an AVAILABLE close-out step, NOT auto-run and NOT a CI gate.
                  This recurring mode is week-based by section 1.19.10a's design;
                  the finer daily tier (section 1.22.5) applies only to the
                  one-time --emit projection scaffold, not this recurring path.
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


def _strip_html_comments(text: str) -> str:
    """Remove ``<!-- ... -->`` blocks.

    The weekly placeholder carries the raw per-PR lines inside an HTML comment
    as condensation material; they are invisible to a reader and to the
    projection, so the re-parse assertion strips comments before checking that
    no VISIBLE per-PR entry from a completed week survives the rewrite."""
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def week_placeholder(monday: datetime.date, week_entries: list[dict]) -> str:
    """A weekly placeholder paragraph plus an HTML-comment block carrying the raw
    per-PR lines as condensation material (an author later replaces the block
    with an at-most-4-sentence weekly accomplishments summary, then deletes it)."""
    prs = [e["pr"] for e in week_entries if e["pr"] is not None]
    rng = _pr_range(prs) if prs else "no PR numbers"
    out = [
        f"**Week of {monday.isoformat()} (PRs {rng})**",
        "",
        "<!-- CONDENSE-SCAFFOLD: author a one-paragraph weekly accomplishments "
        "summary (at most 4 sentences) from the per-PR material below, then "
        "delete this comment block. -->",
        "<!--",
    ]
    # Neutralize any literal "-->" inside a per-PR summary so it cannot prematurely
    # close the HTML comment (which would leak the following raw lines into the
    # visible public root). "--&gt;" renders as "-->" for the human author and is
    # inert as a comment terminator.
    out += [e["raw"].replace("-->", "--&gt;")
            for e in sorted(week_entries, key=lambda x: x["date"], reverse=True)]
    out += ["-->"]
    return "\n".join(out)


def condense_plan(public_text: str, as_of: datetime.date) -> dict | None:
    """Return a condensation plan, or None if the public root has no per-PR entries.

    ``boundary`` is True when there are per-PR entries in weeks STRICTLY BEFORE
    as-of's ISO week. This is the general trigger: in steady state (only the
    current week per-PR, older weeks already condensed) it is exactly the
    week-boundary no-op the spec describes, but it also correctly handles a first
    or catch-up run where the current week AND older uncondensed weeks coexist."""
    w_new = monday_of(as_of)
    preamble, entries = parse_entries(public_text)
    if not entries:
        return None
    w_top = monday_of(max(e["date"] for e in entries))
    completed = [e for e in entries if monday_of(e["date"]) < w_new]
    kept = [e for e in entries if monday_of(e["date"]) >= w_new]
    return {"boundary": bool(completed), "w_new": w_new, "w_top": w_top,
            "preamble": preamble, "entries": entries,
            "completed": completed, "kept": kept}


def private_append(private_text: str, completed: list[dict]) -> str:
    """Insert the completed entries' raw lines into the private full-source after
    its preamble, newest-first, dedup-safe (skip any raw line already present).

    Ordering note: the normal path condenses ONE completed week at a time, so the
    appended block is that week's entries and lands correctly above the (older)
    existing entries. In a mixed catch-up batch (an absent older entry appended
    while a newer entry is already present), the absent entry lands at the top,
    which can violate strict global newest-first order in the private artefact.
    This is harmless: the private full-source is a durable record and the
    verify-before-prune check is a substring test, order-independent; it is not a
    safety property. Dedup is by exact raw line, so a reworded summary would not
    match and could re-appear (a human-visible nuance, not corruption)."""
    lines = private_text.splitlines()
    i = 0
    while i < len(lines) and not ENTRY_RE.match(lines[i]):
        i += 1
    preamble, rest = lines[:i], lines[i:]
    existing = {ln for ln in rest if ENTRY_RE.match(ln)}
    add = [e["raw"] for e in sorted(completed, key=lambda x: x["date"], reverse=True)
           if e["raw"] not in existing]
    return "\n".join(preamble + add + rest) + "\n"


def private_missing(private_text: str, completed: list[dict]) -> list[str]:
    """The completed entries (as ``date|pr`` keys) whose raw line is NOT present in
    the private full-source; a non-empty result blocks the prune."""
    return [f"{e['date'].isoformat()}|{e['pr']}" for e in completed
            if e["raw"] not in private_text]


def render_public_condensed(plan: dict) -> str:
    """Rewrite the public root: preamble, the kept per-PR entries (newest-first),
    then one weekly placeholder per completed week (newest week first)."""
    kept = sorted(plan["kept"], key=lambda x: x["date"], reverse=True)
    by_week: dict[datetime.date, list[dict]] = {}
    for e in plan["completed"]:
        by_week.setdefault(monday_of(e["date"]), []).append(e)
    body = [e["raw"] for e in kept]
    for wk in sorted(by_week, reverse=True):
        body += ["", week_placeholder(wk, by_week[wk])]
    pre = plan["preamble"].rstrip()
    if pre:
        return (pre + "\n\n" + "\n".join(body)).rstrip() + "\n"
    return "\n".join(body).rstrip() + "\n"


def condense_completed_week(public_text: str, as_of: datetime.date,
                            emit_private: bool = False,
                            private_text: str | None = None,
                            prune: bool = False) -> tuple[str, str, str | None, str | None]:
    """Return ``(status, message, new_public_or_None, new_private_or_None)``.

    ``emit_private`` computes the dedup-safe private append; ``prune`` computes the
    condensed public root (requires ``private_text`` and the verify check passing);
    neither is a dry-run plan. The public rewrite is guarded by a re-parse
    assertion on the comment-stripped text (no VISIBLE completed-week per-PR entry
    survives), mirroring the sweep tool's emit-verify-prune contract."""
    plan = condense_plan(public_text, as_of)
    if plan is None:
        return ("noop", "no per-PR entries in the public root", None, None)
    if not plan["boundary"]:
        return ("noop", f"no per-PR entries before as-of week {plan['w_new']}; "
                "nothing to condense", None, None)
    if emit_private:
        new_priv = private_append(private_text or "", plan["completed"])
        return ("emit", f"{len(plan['completed'])} completed-week entr(y/ies) "
                "appended to the private full-source (dedup-safe)", None, new_priv)
    if prune:
        if private_text is None:
            return ("safety", "prune requires --verify-private PATH", None, None)
        missing = private_missing(private_text, plan["completed"])
        if missing:
            return ("safety", f"{len(missing)} completed entr(y/ies) not in the "
                    f"private full-source; refusing to prune. First: {missing[0]}",
                    None, None)
        new_pub = render_public_condensed(plan)
        _, reparsed = parse_entries(_strip_html_comments(new_pub))
        kept_raws = {e["raw"] for e in plan["kept"]}
        if len(reparsed) != len(plan["kept"]) or {e["raw"] for e in reparsed} != kept_raws:
            return ("safety", "re-parse assertion failed (rewritten public does not "
                    "reduce to exactly the kept per-PR set); refusing", None, None)
        weeks = len({monday_of(e["date"]) for e in plan["completed"]})
        return ("prune", f"{len(plan['completed'])} entr(y/ies) condensed into "
                f"{weeks} weekly placeholder(s); {len(plan['kept'])} kept per-PR",
                new_pub, None)
    return ("plan", f"boundary: {len(plan['completed'])} completed-week entr(y/ies) "
            f"to condense, {len(plan['kept'])} kept per-PR", None, None)


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

    class C(unittest.TestCase):
        # --condense-completed-week fixtures. as-of 2026-07-15 (ISO week Mon
        # 2026-07-13). PRs 100/99 are in that week (kept); PRs 98/97 are the
        # prior week (Mon 2026-07-06, completed).
        AS_OF = datetime.date(2026, 7, 15)
        PUBLIC = (
            "# Changelog\n\nintro line\n\n"
            "**2026-07-15 | 2026.07.9 | PR #100** - cur one.\n\n"
            "**2026-07-14 | 2026.07.8 | PR #99** - cur two.\n\n"
            "**2026-07-08 | 2026.07.7 | PR #98** - prior week a.\n\n"
            "**2026-07-06 | 2026.07.6 | PR #97** - prior week b.\n"
        )
        CURRENT_ONLY = (
            "# Changelog\n\nintro line\n\n"
            "**2026-07-15 | 2026.07.9 | PR #100** - cur one.\n\n"
            "**2026-07-14 | 2026.07.8 | PR #99** - cur two.\n"
        )

        def test_noop_when_all_in_current_week(self):
            status, _, new_pub, new_priv = condense_completed_week(
                self.CURRENT_ONLY, self.AS_OF, prune=True, private_text="")
            self.assertEqual(status, "noop")
            self.assertIsNone(new_pub)

        def test_plan_partitions_completed_and_kept(self):
            plan = condense_plan(self.PUBLIC, self.AS_OF)
            self.assertTrue(plan["boundary"])
            self.assertEqual({e["pr"] for e in plan["completed"]}, {98, 97})
            self.assertEqual({e["pr"] for e in plan["kept"]}, {100, 99})

        def test_prune_placeholder_shape_and_keeps_current(self):
            priv = self.PUBLIC  # private already holds every entry, so verify passes
            status, _, new_pub, _ = condense_completed_week(
                self.PUBLIC, self.AS_OF, prune=True, private_text=priv)
            self.assertEqual(status, "prune")
            self.assertIn("**Week of 2026-07-06 (PRs #97-#98)**", new_pub)
            self.assertIn("**2026-07-15 | 2026.07.9 | PR #100** - cur one.", new_pub)

        def test_reparse_sees_only_kept_after_comment_strip(self):
            status, _, new_pub, _ = condense_completed_week(
                self.PUBLIC, self.AS_OF, prune=True, private_text=self.PUBLIC)
            self.assertEqual(status, "prune")
            _, reparsed = parse_entries(_strip_html_comments(new_pub))
            self.assertEqual({e["pr"] for e in reparsed}, {100, 99})

        def test_prune_refuses_when_private_missing_a_completed_entry(self):
            # Private holds only PR #98's line, not #97's -> refuse.
            priv = "# Changelog\n\n**2026-07-08 | 2026.07.7 | PR #98** - prior week a.\n"
            status, msg, new_pub, _ = condense_completed_week(
                self.PUBLIC, self.AS_OF, prune=True, private_text=priv)
            self.assertEqual(status, "safety")
            self.assertIsNone(new_pub)

        def test_private_append_is_dedup_safe(self):
            plan = condense_plan(self.PUBLIC, self.AS_OF)
            # Private already holds PR #98; appending {98, 97} must add #97 once
            # and NOT double #98.
            priv = "# Changelog\n\n**2026-07-08 | 2026.07.7 | PR #98** - prior week a.\n"
            out = private_append(priv, plan["completed"])
            self.assertEqual(out.count("| PR #98** - prior week a."), 1)
            self.assertEqual(out.count("| PR #97** - prior week b."), 1)

        def test_literal_comment_close_in_summary_is_neutralized(self):
            # A completed entry whose summary contains a literal "-->" must not
            # prematurely close the placeholder's HTML comment and leak the
            # following raw lines into the visible public root.
            public = (
                "# Changelog\n\nintro line\n\n"
                "**2026-07-15 | 2026.07.9 | PR #100** - cur one.\n\n"
                "**2026-07-08 | 2026.07.7 | PR #98** - migrate a --> b then more.\n\n"
                "**2026-07-06 | 2026.07.6 | PR #97** - prior week b.\n"
            )
            status, _, new_pub, _ = condense_completed_week(
                public, self.AS_OF, prune=True, private_text=public)
            self.assertEqual(status, "prune")
            # The re-parse (after comment-strip) sees only the kept current entry.
            _, reparsed = parse_entries(_strip_html_comments(new_pub))
            self.assertEqual({e["pr"] for e in reparsed}, {100})
            # The literal close was neutralized (summary "-->" became "--&gt;"), so
            # only the two structural comment terminators remain (the CONDENSE-SCAFFOLD
            # note and the raw-block comment); a leaked summary close would make 3.
            self.assertEqual(new_pub.count("-->"), 2)
            self.assertIn("--&gt;", new_pub)

    runner = unittest.TextTestRunner(verbosity=1)
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite([loader.loadTestsFromTestCase(T),
                                loader.loadTestsFromTestCase(C)])
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", default=True)
    mode.add_argument("--emit", metavar="PATH")
    mode.add_argument("--condense-completed-week", action="store_true",
                      help="recurring weekly-rollup mode (TODO 1.19.10a): condense "
                           "the public root's completed-week per-PR entries to "
                           "weekly placeholders and append them to the private "
                           "full-source; available close-out step, NOT auto-run.")
    mode.add_argument("--self-test", action="store_true")
    ap.add_argument("--source", default=str(REPO_ROOT / "CHANGELOG.md"))
    ap.add_argument("--as-of")
    ap.add_argument("--months", type=int, default=3)
    ap.add_argument("--emit-private", metavar="PATH",
                    help="condense mode: append completed-week per-PR entries to "
                         "the private full-source at PATH (dedup-safe).")
    ap.add_argument("--verify-private", metavar="PATH",
                    help="condense mode: private full-source to confirm before --prune.")
    ap.add_argument("--prune", action="store_true",
                    help="condense mode: rewrite the public root, condensing "
                         "completed weeks to placeholders (requires "
                         "--condense-completed-week and --verify-private).")
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

    if args.condense_completed_week:
        public_text = src.read_text(encoding="utf-8")
        priv_path = args.emit_private or args.verify_private
        priv_text = (Path(priv_path).read_text(encoding="utf-8")
                     if priv_path and Path(priv_path).is_file() else None)
        if args.emit_private and priv_text is None and not Path(args.emit_private).parent.is_dir():
            print(f"advisory: private full-source parent for {args.emit_private} "
                  "absent (private repo not present); nothing to do.")
            return 0
        status, msg, new_pub, new_priv = condense_completed_week(
            public_text, as_of, emit_private=bool(args.emit_private),
            private_text=priv_text, prune=args.prune)
        print(f"[{status}] {msg}")
        if status == "safety":
            return 1
        if args.emit_private and new_priv is not None:
            Path(args.emit_private).write_text(new_priv, encoding="utf-8")
            print(f"wrote private full-source {args.emit_private}")
        if args.prune and new_pub is not None:
            src.write_text(new_pub, encoding="utf-8")
            print(f"rewrote public root {src} (condensed)")
        return 0

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
