#!/usr/bin/env python3
"""Sweep aged working records out of grc_library into the grc_library_private archive.

The current-week model (maintainer decision 2026-07-08; destination repointed
from grc_library_scratch to grc_library_private for TODO section 1.19.9): the
in-repo ``.working/`` keeps only the CURRENT ISO week's records, and everything
older lives in the ``grc_library_private`` archive, organized as weekly
Monday-dated files. Four kinds of record are swept:

  1. the completed-week detailed-CHANGELOG entries (``## `` per-PR entries in
     ``.working/changelog-details/CHANGELOG-detailed.md``);
  2. the dated per-run record files under the RECORD_SUBDIRS (a filename
     beginning ``YYYY-MM-DD``);
  3. (TODO section 1.19.9) the aged table ROWS of the ROLLUP_REGISTERS
     (``.working/validate-pr/history.md`` and ``.working/improvement-log.md``),
     whose history FILES stay in-repo but whose rows older than the current
     week move out. Gate 50's dynamic per-register floor (effective_floor)
     scopes a swept-out PR below the floor, so it is out of scope, not flagged
     missing. Only these two registers are row-swept (they are the gate-50
     Check-1 inputs); the other history.md registers keep their rows in-repo
     (guardrail-reviews for the gate-60 newest-row safety; the rest have no
     dynamic cutoff prepared). See ROLLUP_REGISTERS; and
  4. (TODO section 1.22.3) the completed one-off directories in ONEOFF_DIRS,
     each swept WHOLE (every file moves to the archive and the dir is removed
     in-repo). The list is explicit and orchestrator-maintained, never
     auto-detected, so a live dir cannot be swept by accident. See ONEOFF_DIRS.

The broader-surface entry sweeps TODO section 1.22.3 also names (aged DONE.md
entries, the resolved-and-aged tail of pending-decisions.md) are surfaced by the
read-only ``--staleness-report`` for awareness, but their DESTRUCTIVE sweep is
NOT enabled in this cut: they await a maintainer decision on the DONE cutoff
width, a DONE effective_floor analogous to the roll-up floor, and the
conservative resolved-AND-aged entry-boundary predicate for pending-decisions
(see ``results/research-1223-working-cycleout.md``, the risk section).

The gate-read index files (each RECORD_SUBDIRS ``history.md``), the operational
files (``session-handoff.md``, ``session-state.md``, ``DONE.md`` and the like),
and every ``README.md`` STAY in-repo (only the two ROLLUP_REGISTERS have their
aged ROWS swept).

This is NOT a corpus audit gate. It is an orchestrator tool run as a per-PR
follow-up step (like ``/validate-pr``), and once at the initial migration.

Data-safety: ``--prune`` refuses to remove or rewrite anything in grc_library
unless ``--verify-archived DIR`` confirms every to-be-removed artefact already
exists in the grc_library_private archive DIR, and every rewrite is guarded by
a re-parse assertion (the mirror and each roll-up register must re-parse to
EXACTLY the kept set before any write; all assertions run before any write, so a
mismatch aborts with nothing changed). The intended sequence is:

    1. python3 tools/sweep-working-records-to-private.py --emit-archive <private>/archive
    2. (commit + push + verify the grc_library_private side landed)
    3. python3 tools/sweep-working-records-to-private.py --prune --verify-archived <private>/archive

Removed rows and files also remain in grc_library's git history, so a swept
record is never lost even independent of the grc_library_private copy; the
archive is the convenient browsable copy, git history is the durable one.

Modes (mutually exclusive; default --dry-run):
    --dry-run           report what would be swept; touch nothing.
    --emit-archive DIR  write the weekly detailed-CHANGELOG archive files, copy
                        the dated record files, write the per-register aged
                        roll-up rows, and copy each ONEOFF_DIRS directory whole
                        into DIR (the grc_library_private archive). Does NOT
                        modify grc_library.
    --prune             rewrite the in-repo detailed mirror to current-week-only,
                        rewrite each roll-up register to its kept (current-week)
                        rows, delete the swept dated record files, remove each
                        ONEOFF_DIRS directory whole, then delink any now-absent
                        history.md Detail-column links. Requires --verify-archived
                        DIR (every archived artefact, including every one-off-dir
                        file, must be present in DIR before anything is removed).
    --staleness-report  read-only advisory: report aged-but-unswept content
                        across the broader .working surface (TODO section
                        1.22.3), including an advisory count of aged DONE.md and
                        resolved-and-aged pending-decisions.md entries whose
                        destructive sweep is not yet enabled. Touches nothing.
    --delink-history    delink (to plain text) each RECORD_SUBDIRS history.md
                        Detail-column link whose dated target file is absent
                        in-repo (swept to the archive). Idempotent; touches no
                        link whose target is still present. Standalone form of
                        the step --prune runs; use it to heal history files after
                        a prune that predated this step (the #708 finding).

Options:
    --as-of YYYY-MM-DD  treat this date's ISO week (Monday) as the current week
                        to KEEP in-repo (default: the ISO week of the newest
                        detailed-CHANGELOG entry).
    --root DIR          grc_library root (default: the repo this script lives in).
    --verify-archived DIR   the grc_library_private archive dir to check before --prune.

Exit codes: 0 success; 1 a safety check failed (e.g. --prune without a
complete archive, or a re-parse assertion mismatch); 2 usage error.
"""

from __future__ import annotations

import argparse
import datetime
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DETAILED_MIRROR_REL = ".working/changelog-details/CHANGELOG-detailed.md"

# Per-run record subdirectories under .working/. In each, dated files
# (filename begins YYYY-MM-DD) are per-run records eligible to sweep;
# history.md, README.md, and any other non-dated file STAY in-repo.
RECORD_SUBDIRS = (
    "validate-pr",
    "validate-sweeps",
    "full-qa",
    "fitness-reviews",
    "guardrail-reviews",
    "claim-fit",
    "matrix-fit",
    "deep-assessment",
    "reference-audit",
)

DATE_ANYWHERE = re.compile(r"(\d{4}-\d{2}-\d{2})")
DATED_FILENAME = re.compile(r"^(\d{4}-\d{2}-\d{2})")
ENTRY_HEADER = re.compile(r"^## ")

# Roll-up registers whose AGED table ROWS sweep to grc_library_private (TODO
# section 1.19.9). Only these two are row-swept: they are the gate-50 Check-1
# inputs, for which PR A added the dynamic per-register floor (effective_floor)
# so a swept-out PR falls below the floor and is out of scope, not flagged
# missing. Their history FILES stay in-repo; only rows older than the current
# week move out. The other .working history.md registers KEEP their rows in-repo
# this cut: guardrail-reviews/history.md because gate 60 reads its newest row (a
# row-sweep there is pure risk for no cutoff benefit; its newest-row safety is
# satisfied by not sweeping it), and the rest (validate-sweeps, full-qa,
# fitness-reviews, claim-fit, matrix-fit, deep-assessment/register,
# reference-audit) because no dynamic cutoff is prepared for them (gate 50
# Check 5 reads the deep-assessment register row order). Their DATED per-run
# files still sweep via RECORD_SUBDIRS as before.
ROLLUP_REGISTERS = (
    ".working/validate-pr/history.md",
    ".working/improvement-log.md",
)

# A dated table row in a roll-up register, e.g. "| 2026-07-08 | #713 | ... |".
# Both registers start a data row with "| YYYY-MM-DD |"; every other line (the
# title, Version/Date metadata, prose, section headers, the "| Date | PR | ..."
# table header, the "|---|" separator, and blank lines) is kept in place.
ROLLUP_ROW_DATE = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|")

# Completed one-off .working/ directories that sweep WHOLE (TODO section 1.22.3).
# Unlike RECORD_SUBDIRS (where only dated files sweep and history.md/README.md
# stay), a one-off dir is a finished workstream with no live gate reader: the
# ENTIRE directory (every file) moves to the archive and the dir is removed
# in-repo. This list is EXPLICIT and orchestrator-maintained, NEVER
# auto-detected: a directory is added here only once its workstream is fully
# done and confirmed to have no audit-gate reader, so a live dir can never be
# swept by accident. The two seeded entries are the pack-hygiene consolidation
# leftovers; a grep of tools/*.py for either name returned zero references on
# 2026-07-23, so neither is gate-read. Confirm the same before adding any entry.
ONEOFF_DIRS = (
    "pack-hygiene-acceptance",
    "pack-hygiene-fragments",
)

# An entry header in a `###`/`##`-structured ledger (DONE.md, the resolved tail
# of pending-decisions.md). Used ONLY by the read-only --staleness-report; the
# destructive row/entry sweep of these two files is deliberately NOT enabled in
# this cut (it awaits a maintainer decision on the DONE cutoff width, a DONE
# effective_floor analogous to gate 50's roll-up floor, and the conservative
# resolved-AND-aged entry-boundary predicate for pending-decisions). See
# results/research-1223-working-cycleout.md, the risk section.
ENTRY_HEADER_H23 = re.compile(r"^#{2,3} ")
RESOLVED_MARKER = re.compile(r"\bRESOLVED\b|\bCLOSED\b", re.I)


def oneoff_dirs_present(root: Path) -> list[str]:
    """The ONEOFF_DIRS that actually exist under .working/ in-repo (order preserved)."""
    base = root / ".working"
    return [d for d in ONEOFF_DIRS if (base / d).is_dir()]


def oneoff_missing_from_archive(root: Path, arch: Path) -> list[str]:
    """The archive paths of one-off-dir files NOT present under arch/oneoff-dirs/.

    This is the verify-before-prune check for the one-off sweep (the whole
    data-safety guarantee of the only new destructive path): an empty list means
    every in-repo one-off file is archived and the prune may proceed; a non-empty
    list means the prune MUST refuse. Extracted from the inline prune loop into a
    named, self-tested helper so a future edit cannot silently regress the refusal.
    """
    missing: list[str] = []
    for name in oneoff_dirs_present(root):
        src = root / ".working" / name
        for f in sorted(src.rglob("*")):
            if f.is_file():
                rel = f.relative_to(src)
                p = arch / "oneoff-dirs" / name / rel
                if not p.is_file():
                    missing.append(str(p))
    return missing


def iter_entries(text: str, header_re: "re.Pattern[str]"):
    """Yield (header_line, entry_text) for each header-delimited entry in text.

    An entry runs from a line matching header_re to the next such header or EOF.
    Content before the first header (the preamble) is not yielded. Line-level, no
    structural parse; used by the read-only staleness report to count aged
    entries in a `###`/`##`-structured ledger without rewriting anything.
    """
    lines = text.splitlines(keepends=True)
    cur_header: str | None = None
    cur: list[str] = []
    for line in lines:
        if header_re.match(line):
            if cur_header is not None:
                yield cur_header, "".join(cur)
            cur_header = line
            cur = [line]
        elif cur_header is not None:
            cur.append(line)
    if cur_header is not None:
        yield cur_header, "".join(cur)


def count_aged_entries(
    text: str,
    header_re: "re.Pattern[str]",
    current_week: datetime.date,
    require_resolved: bool = False,
) -> int:
    """Count header-delimited entries whose header date is before current_week
    (advisory only). If require_resolved, count only entries whose text carries a
    RESOLVED/CLOSED marker (the conservative resolved-AND-aged predicate for
    pending-decisions). An entry whose header has no parseable date is skipped
    (never counted as sweepable), so the count is a conservative lower bound.
    """
    n = 0
    for header, body in iter_entries(text, header_re):
        m = DATE_ANYWHERE.search(header)
        if not m:
            continue
        if monday_of(datetime.date.fromisoformat(m.group(1))) >= current_week:
            continue
        if require_resolved and not RESOLVED_MARKER.search(body):
            continue
        n += 1
    return n


def rollup_archive_name(monday: datetime.date) -> str:
    return f"{monday.isoformat()}_rows.md"


def register_stem(rel: str) -> str:
    """A filesystem-safe archive subdir stem for a register path, e.g.
    ``.working/validate-pr/history.md`` -> ``validate-pr-history`` and
    ``.working/improvement-log.md`` -> ``improvement-log``."""
    return rel[len(".working/"):].removesuffix(".md").replace("/", "-")


def partition_rollup_rows(
    text: str, current_week: datetime.date
) -> tuple[str, dict[datetime.date, list[str]]]:
    """Split a roll-up register into (kept_text, swept_by_week).

    A dated table row (a line matching ``ROLLUP_ROW_DATE``) whose ISO week is
    strictly before ``current_week`` is swept; every other line (title,
    Version/Date, prose, section headers, the table header + separator, blank
    lines, and recent dated rows) is kept in place, line-for-line. This is
    deliberately line-level so a register with prose sections or multiple table
    blocks (the improvement-log) is handled without a structural parse.
    ``swept_by_week`` maps each Monday to the swept row lines in the order they
    appeared (newest-first within the register is preserved).
    """
    kept_lines: list[str] = []
    swept_by_week: dict[datetime.date, list[str]] = {}
    for line in text.splitlines(keepends=True):
        m = ROLLUP_ROW_DATE.match(line)
        if m:
            d = datetime.date.fromisoformat(m.group(1))
            if monday_of(d) < current_week:
                swept_by_week.setdefault(monday_of(d), []).append(line)
                continue
        kept_lines.append(line)
    return "".join(kept_lines), swept_by_week


def count_rollup_rows(text: str) -> int:
    """The number of dated table rows in a roll-up register."""
    return sum(1 for ln in text.splitlines() if ROLLUP_ROW_DATE.match(ln))


def monday_of(d: datetime.date) -> datetime.date:
    return d - datetime.timedelta(days=d.weekday())


def parse_detailed(text: str) -> tuple[str, list[tuple[datetime.date, str]]]:
    """Split the detailed mirror into (preamble, [(entry_date, entry_text), ...]).

    An entry runs from a ``## `` header line to the next ``## `` or EOF.
    The entry date is the first YYYY-MM-DD appearing in the header line
    (handles both ``## 2026-07-08, ...`` and ``## Initial public release
    (2026-05-31, ...)``).
    """
    lines = text.splitlines(keepends=True)
    preamble_lines: list[str] = []
    i = 0
    while i < len(lines) and not ENTRY_HEADER.match(lines[i]):
        preamble_lines.append(lines[i])
        i += 1
    preamble = "".join(preamble_lines)

    entries: list[tuple[datetime.date, str]] = []
    cur_header_date: datetime.date | None = None
    cur_lines: list[str] = []

    def flush() -> None:
        if cur_lines and cur_header_date is not None:
            entries.append((cur_header_date, "".join(cur_lines)))

    while i < len(lines):
        line = lines[i]
        if ENTRY_HEADER.match(line):
            flush()
            m = DATE_ANYWHERE.search(line)
            if not m:
                raise ValueError(f"detailed entry header without a date: {line!r}")
            cur_header_date = datetime.date.fromisoformat(m.group(1))
            cur_lines = [line]
        else:
            cur_lines.append(line)
        i += 1
    flush()
    return preamble, entries


def newest_entry_date(entries: list[tuple[datetime.date, str]]) -> datetime.date:
    return max(d for d, _ in entries)


def dated_record_files(root: Path) -> list[tuple[datetime.date, Path]]:
    out: list[tuple[datetime.date, Path]] = []
    base = root / ".working"
    for sub in RECORD_SUBDIRS:
        d = base / sub
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.md")):
            m = DATED_FILENAME.match(f.name)
            if not m:
                continue  # history.md, README.md, etc. stay
            out.append((datetime.date.fromisoformat(m.group(1)), f))
    return out


def weekly_archive_name(monday: datetime.date) -> str:
    return f"{monday.isoformat()}_detailed.md"


# A history.md link to a dated per-run record file, whether a same-dir Detail-column
# link (``[`2026-06-22-PR-187.md`](2026-06-22-PR-187.md)``) or a cross-subdir
# Detail/Summary-cell reference (``[text](../validate-sweeps/2026-06-28-sweep71-iter1.md)``).
# The target may carry a relative path prefix; a URL target (``\w+://``) is excluded so an
# external link that happens to embed a dated ``.md`` is never touched. The present-check
# below (resolved relative to the file's own dir) is what decides delink-vs-keep, so a
# broader match here only widens the candidate set, never delinks a present target.
HISTORY_DATED_LINK = re.compile(r"\[([^\]]*)\]\((?!\w+://)([^)]*\d{4}-\d{2}-\d{2}[^)]*\.md)\)")


def delink_absent_history_links(root: Path) -> int:
    """Delink each RECORD_SUBDIRS ``history.md`` Detail-column link whose dated
    target file is absent in-repo (swept to the archive), leaving the link TEXT
    in place as plain text (the filename stays a reference; the swept file lives
    in git history and the grc_library_private archive). Idempotent: a link whose target is
    still present in-repo (a current-week record) is untouched, and re-running
    changes nothing. Returns the count of links delinked. This keeps the retained
    history.md index files free of the dangling links a prune would otherwise
    leave (the #708 post-merge finding), and runs automatically at the end of a
    ``--prune`` so future weekly sweeps self-heal."""
    base = root / ".working"
    total = 0

    def make_repl(sub_dir: Path):
        def repl(m: "re.Match[str]") -> str:
            nonlocal total
            if (sub_dir / m.group(2)).is_file():
                return m.group(0)  # target present in-repo: keep the link
            total += 1
            return m.group(1)  # target absent (swept): delink to the link text
        return repl

    for sub in RECORD_SUBDIRS:
        sub_dir = base / sub
        hist = sub_dir / "history.md"
        if not hist.is_file():
            continue
        text = hist.read_text(encoding="utf-8")
        new = HISTORY_DATED_LINK.sub(make_repl(sub_dir), text)
        if new != text:
            hist.write_text(new, encoding="utf-8")
    return total


def plan(root: Path, current_week: datetime.date):
    """Return (preamble, keep_entries, sweep_by_week, sweep_records, rollups).

    ``rollups`` maps each ROLLUP_REGISTERS rel-path to
    ``(kept_text, swept_by_week)`` (TODO section 1.19.9); a register absent
    in-repo is skipped.
    """
    mirror = root / DETAILED_MIRROR_REL
    preamble, entries = parse_detailed(mirror.read_text(encoding="utf-8"))
    keep = [(d, t) for d, t in entries if monday_of(d) >= current_week]
    sweep = [(d, t) for d, t in entries if monday_of(d) < current_week]
    by_week: dict[datetime.date, list[str]] = {}
    for d, t in sweep:
        by_week.setdefault(monday_of(d), []).append(t)
    records = [
        (d, f) for d, f in dated_record_files(root) if monday_of(d) < current_week
    ]
    rollups: dict[str, tuple[str, dict[datetime.date, list[str]]]] = {}
    for rel in ROLLUP_REGISTERS:
        p = root / rel
        if not p.is_file():
            continue
        rollups[rel] = partition_rollup_rows(
            p.read_text(encoding="utf-8"), current_week
        )
    return preamble, keep, by_week, records, rollups


def self_test() -> int:
    """Inline unit tests for the section-1.19.9 roll-up-row logic (kept behind
    --self-test, not in tests/, so the gate-36 regression runner does not adopt
    this advisory tool as a gated test)."""
    import unittest
    import tempfile

    class RollupTests(unittest.TestCase):
        def test_partition_keeps_recent_sweeps_old(self):
            text = (
                "# Register\n\n"
                "| Date | PR | X |\n"
                "|---|---|---|\n"
                "| 2026-07-15 | 100 | recent |\n"   # week of 07-13: keep
                "| 2026-07-06 | 99 | old |\n"       # week of 07-06: sweep
                "| 2026-06-30 | 98 | older |\n"     # week of 06-29: sweep
                "\nSome trailing prose line.\n"
            )
            kept, swept = partition_rollup_rows(text, datetime.date(2026, 7, 13))
            self.assertIn("2026-07-15", kept)             # recent row kept
            self.assertIn("Some trailing prose line", kept)  # non-row kept
            self.assertIn("| Date | PR | X |", kept)      # table header kept
            self.assertNotIn("2026-07-06", kept)          # old rows swept out
            self.assertNotIn("2026-06-30", kept)
            self.assertEqual(sum(len(v) for v in swept.values()), 2)
            self.assertEqual(
                set(swept),
                {datetime.date(2026, 6, 29), datetime.date(2026, 7, 6)},
            )
            # Re-partitioning the kept text finds nothing further to sweep
            # (the prune re-parse assertion relies on this).
            _, reswept = partition_rollup_rows(kept, datetime.date(2026, 7, 13))
            self.assertEqual(reswept, {})

        def test_count_rollup_rows(self):
            text = ("| 2026-07-15 | a |\n| Date | b |\nprose\n"
                    "| 2026-07-06 | c |\n")
            self.assertEqual(count_rollup_rows(text), 2)  # only the 2 dated rows

        def test_register_stem(self):
            self.assertEqual(
                register_stem(".working/validate-pr/history.md"),
                "validate-pr-history",
            )
            self.assertEqual(
                register_stem(".working/improvement-log.md"), "improvement-log"
            )

        def test_oneoff_dirs_present(self):
            # TODO section 1.22.3: only ONEOFF_DIRS that exist in-repo are returned,
            # and only directories (a same-named file does not count).
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                base = root / ".working"
                (base / ONEOFF_DIRS[0]).mkdir(parents=True)
                (base / "validate-pr").mkdir(parents=True)  # a live dir, not one-off
                self.assertEqual(oneoff_dirs_present(root), [ONEOFF_DIRS[0]])

        def test_iter_entries(self):
            text = (
                "preamble line, not an entry\n"
                "### Entry A (2026-07-06)\nbody a1\nbody a2\n"
                "### Entry B (2026-07-15)\nbody b1\n"
            )
            entries = list(iter_entries(text, ENTRY_HEADER_H23))
            self.assertEqual(len(entries), 2)  # preamble excluded
            self.assertTrue(entries[0][0].startswith("### Entry A"))
            self.assertIn("body a2", entries[0][1])

        def test_count_aged_entries(self):
            text = (
                "### Old resolved (2026-07-06)\nRESOLVED here\n"
                "### Old open (2026-06-30)\nstill open\n"
                "### Recent (2026-07-15)\nRESOLVED but recent\n"
                "### No date here\nbody\n"
            )
            cw = datetime.date(2026, 7, 13)
            # aged (any disposition): the two entries dated before the week of 07-13
            self.assertEqual(count_aged_entries(text, ENTRY_HEADER_H23, cw), 2)
            # aged AND resolved: only the 07-06 one (the 06-30 is open; 07-15 recent)
            self.assertEqual(
                count_aged_entries(text, ENTRY_HEADER_H23, cw, require_resolved=True),
                1,
            )
            # an entry whose header has no date is never counted (conservative)

        def test_oneoff_missing_from_archive(self):
            # TODO section 1.22.3: the verify-before-prune check for the one-off
            # sweep refuses (non-empty list) on an incomplete archive and passes
            # (empty list) only when every in-repo one-off file is archived. This
            # locks the ONLY new destructive path's data-safety guard under --self-test.
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                arch = Path(td) / "arch"
                d = root / ".working" / ONEOFF_DIRS[0]
                (d / "sub").mkdir(parents=True)
                (d / "a.md").write_text("x", encoding="utf-8")
                (d / "sub" / "b.md").write_text("y", encoding="utf-8")
                # empty archive: both files missing, so the prune must refuse.
                self.assertEqual(len(oneoff_missing_from_archive(root, arch)), 2)
                # complete archive: nothing missing, so the prune may proceed.
                adest = arch / "oneoff-dirs" / ONEOFF_DIRS[0]
                (adest / "sub").mkdir(parents=True)
                (adest / "a.md").write_text("x", encoding="utf-8")
                (adest / "sub" / "b.md").write_text("y", encoding="utf-8")
                self.assertEqual(oneoff_missing_from_archive(root, arch), [])

    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(
        unittest.defaultTestLoader.loadTestsFromTestCase(RollupTests)
    )
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", default=True)
    mode.add_argument("--emit-archive", metavar="DIR")
    mode.add_argument("--prune", action="store_true")
    mode.add_argument("--delink-history", action="store_true")
    mode.add_argument("--staleness-report", action="store_true",
                      help="read-only advisory: report aged-but-unswept content "
                           "across the broader .working surface (TODO section "
                           "1.22.3); touches nothing, always exits 0")
    ap.add_argument("--as-of")
    ap.add_argument("--root", default=str(REPO_ROOT))
    ap.add_argument("--verify-archived", metavar="DIR")
    ap.add_argument("--self-test", action="store_true",
                    help="run the inline roll-up-row unit tests and exit")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    root = Path(args.root).resolve()
    mirror = root / DETAILED_MIRROR_REL
    if not mirror.is_file():
        print(f"ERROR: detailed mirror not found at {mirror}", file=sys.stderr)
        return 2

    _, entries = parse_detailed(mirror.read_text(encoding="utf-8"))
    if args.as_of:
        current_week = monday_of(datetime.date.fromisoformat(args.as_of))
    else:
        current_week = monday_of(newest_entry_date(entries))

    preamble, keep, by_week, records, rollups = plan(root, current_week)

    print(f"Current week kept in-repo: week of {current_week.isoformat()} (Monday)")
    print(f"Detailed entries: {len(keep)} kept in-repo, "
          f"{sum(len(v) for v in by_week.values())} to sweep across {len(by_week)} week(s).")
    for wk in sorted(by_week):
        print(f"  archive week {wk.isoformat()}: {len(by_week[wk])} entries -> {weekly_archive_name(wk)}")
    print(f"Dated record files to sweep: {len(records)}")
    for rel, (_, swept) in sorted(rollups.items()):
        n = sum(len(v) for v in swept.values())
        print(f"Roll-up rows to sweep from {rel}: {n} row(s) across "
              f"{len(swept)} week(s).")
    oneoff = oneoff_dirs_present(root)
    print(f"One-off completed dir(s) to sweep whole: {len(oneoff)} "
          f"({', '.join(oneoff) or 'none'}).")

    if args.staleness_report:
        # Read-only advisory (TODO section 1.22.3): the existing-tool sweep
        # backlog above, plus an ADVISORY count of the broader-surface content
        # whose DESTRUCTIVE sweep is not yet enabled (DONE aged entries, the
        # resolved-and-aged tail of pending-decisions). These two counts are
        # informational only; no cutoff/floor/predicate decision is applied here.
        print("\n--- staleness report (advisory; TODO section 1.22.3) ---")
        done = root / ".working" / "DONE.md"
        pend = root / ".working" / "pending-decisions.md"
        if done.is_file():
            n = count_aged_entries(
                done.read_text(encoding="utf-8"), ENTRY_HEADER_H23, current_week
            )
            print(f"DONE.md: {n} entr(y/ies) with a header date before the "
                  f"current week (ADVISORY; destructive DONE sweep NOT enabled, "
                  f"pending a maintainer cutoff + DONE effective_floor decision).")
        if pend.is_file():
            n = count_aged_entries(
                pend.read_text(encoding="utf-8"), ENTRY_HEADER_H23,
                current_week, require_resolved=True,
            )
            print(f"pending-decisions.md: {n} resolved-and-aged entr(y/ies) "
                  f"(ADVISORY; destructive sweep NOT enabled, pending the "
                  f"conservative entry-boundary predicate decision).")
        print("(staleness report only; nothing changed.)")
        return 0

    if args.emit_archive:
        outdir = Path(args.emit_archive).resolve()
        (outdir / "changelog-details").mkdir(parents=True, exist_ok=True)
        for wk, texts in sorted(by_week.items()):
            body = (
                f"# Detailed CHANGELOG archive, week of {wk.isoformat()} (Monday)\n\n"
                f"Swept from grc_library `.working/changelog-details/` under the "
                f"current-week model. Newest-first within the week.\n\n"
                + "".join(texts)
            )
            (outdir / "changelog-details" / weekly_archive_name(wk)).write_text(
                body, encoding="utf-8"
            )
        for d, f in records:
            sub = f.parent.name
            dest = outdir / "records" / sub
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dest / f.name)
        for rel, (_, swept) in rollups.items():
            stem = register_stem(rel)
            rdir = outdir / "rollup-rows" / stem
            rdir.mkdir(parents=True, exist_ok=True)
            for wk, rows in sorted(swept.items()):
                body = (
                    f"# Roll-up rows archive: {rel}, week of {wk.isoformat()} "
                    f"(Monday)\n\nSwept from grc_library `{rel}` under the "
                    f"current-week model (TODO section 1.19.9). Rows in their "
                    f"original (newest-first) order.\n\n" + "".join(rows)
                )
                (rdir / rollup_archive_name(wk)).write_text(body, encoding="utf-8")
        # One-off completed directories (TODO section 1.22.3): copy each WHOLE
        # dir tree into archive/oneoff-dirs/<name>/. Does NOT modify grc_library.
        for name in oneoff_dirs_present(root):
            src = root / ".working" / name
            dest = outdir / "oneoff-dirs" / name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
        print(f"Emitted archive to {outdir}")
        return 0

    if args.prune:
        if not args.verify_archived:
            print("ERROR: --prune requires --verify-archived DIR", file=sys.stderr)
            return 1
        arch = Path(args.verify_archived).resolve()
        missing: list[str] = []
        for wk in by_week:
            p = arch / "changelog-details" / weekly_archive_name(wk)
            if not p.is_file():
                missing.append(str(p))
        for d, f in records:
            p = arch / "records" / f.parent.name / f.name
            if not p.is_file():
                missing.append(str(p))
        for rel, (_, swept) in rollups.items():
            stem = register_stem(rel)
            for wk in swept:
                p = arch / "rollup-rows" / stem / rollup_archive_name(wk)
                if not p.is_file():
                    missing.append(str(p))
        # One-off dirs: every in-repo file must exist under archive/oneoff-dirs/
        # (extracted to the self-tested oneoff_missing_from_archive helper so the
        # verify-before-prune refusal for this destructive path cannot silently regress).
        oneoff_present = oneoff_dirs_present(root)
        missing.extend(oneoff_missing_from_archive(root, arch))
        if missing:
            print("ERROR: refusing to prune; these archive files are missing:",
                  file=sys.stderr)
            for m in missing:
                print(f"  {m}", file=sys.stderr)
            return 1
        new_mirror = preamble + "".join(t for _, t in keep)
        # Data-safety re-parse assertion: parse the CONSTRUCTED mirror in
        # memory and confirm it re-parses to EXACTLY the kept current-week
        # entries (same header lines, same order), before touching disk. If
        # the by-date partition ever regressed (dropping or duplicating an
        # entry), this aborts with nothing changed. This is the compensating
        # control for gate 59's floor-boundary limitation (a dropped
        # floor-defining entry is invisible to gate 59): the sweep guarantees
        # here that the in-repo mirror is exactly the kept set.
        _, reparsed = parse_detailed(new_mirror)
        expected_headers = [t.splitlines()[0] for _, t in keep]
        got_headers = [t.splitlines()[0] for _, t in reparsed]
        if got_headers != expected_headers:
            print(
                "ERROR: post-rewrite re-parse mismatch (the constructed mirror "
                "would drop or duplicate an entry); aborting, nothing changed.",
                file=sys.stderr,
            )
            return 1
        # Roll-up register re-parse assertions (TODO section 1.19.9), ALL run
        # BEFORE any write so a mismatch aborts with nothing changed: each
        # rewritten register must hold EXACTLY (original - swept) dated rows and
        # re-partition to zero further sweepable rows.
        for rel, (kept_text, swept) in rollups.items():
            swept_n = sum(len(v) for v in swept.values())
            orig_n = count_rollup_rows((root / rel).read_text(encoding="utf-8"))
            kept_n = count_rollup_rows(kept_text)
            _, reswept = partition_rollup_rows(kept_text, current_week)
            if kept_n != orig_n - swept_n or reswept:
                print(
                    f"ERROR: {rel} row-rewrite re-parse mismatch (orig {orig_n}, "
                    f"swept {swept_n}, kept {kept_n}, residual-sweepable "
                    f"{sum(len(v) for v in reswept.values())}); aborting, nothing "
                    f"changed.", file=sys.stderr)
                return 1
        # All assertions passed: apply the writes.
        mirror.write_text(new_mirror, encoding="utf-8")
        for _, f in records:
            f.unlink()
        rollup_row_total = 0
        for rel, (kept_text, swept) in rollups.items():
            (root / rel).write_text(kept_text, encoding="utf-8")
            rollup_row_total += sum(len(v) for v in swept.values())
        # One-off dirs: archive verified above, so remove each WHOLE dir in-repo.
        for name in oneoff_present:
            shutil.rmtree(root / ".working" / name)
        delinked = delink_absent_history_links(root)
        print(f"Pruned: mirror rewritten to {len(keep)} current-week entries "
              f"(re-parse assertion passed); {len(records)} record file(s) "
              f"removed; {rollup_row_total} roll-up row(s) swept from "
              f"{len(rollups)} register(s); {len(oneoff_present)} one-off "
              f"dir(s) removed ({', '.join(oneoff_present) or 'none'}). Archive "
              f"verified present. Delinked {delinked} now-absent history.md "
              f"Detail-column link(s).")
        return 0

    if args.delink_history:
        delinked = delink_absent_history_links(root)
        print(f"Delinked {delinked} history.md Detail-column link(s) whose dated "
              f"target file is absent in-repo (swept to the archive). Idempotent.")
        return 0

    print("\n(dry-run; nothing changed. Use --emit-archive then --prune to apply.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
