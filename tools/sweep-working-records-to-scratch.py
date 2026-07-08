#!/usr/bin/env python3
"""Sweep completed-week working records out of grc_library into the scratch archive.

The current-week model (maintainer decision 2026-07-08): the in-repo
``.working/`` keeps only the CURRENT week's per-run records and the current
week's detailed-CHANGELOG entries; everything older lives in the
``grc_library_scratch`` archive, organized as weekly Monday-dated files. The
gate-read index files (each subdir's ``history.md``), the operational files
(``session-handoff.md``, ``session-state.md``, ``DONE.md``,
``improvement-log.md`` and the like), and every ``README.md`` STAY in-repo;
only the dated per-run record files and the completed-week detailed-CHANGELOG
entries are swept.

This is NOT a corpus audit gate. It is an orchestrator tool run as a per-PR
follow-up step (like ``/validate-pr``), and once at the initial migration.

Data-safety: ``--prune`` refuses to remove anything from grc_library unless
``--verify-archived DIR`` confirms every to-be-removed artefact already exists
in the scratch archive DIR. The intended sequence is:

    1. python3 tools/sweep-working-records-to-scratch.py --emit-archive <scratch>/archive
    2. (commit + verify the scratch side landed)
    3. python3 tools/sweep-working-records-to-scratch.py --prune --verify-archived <scratch>/archive

Removed files also remain in grc_library's git history, so a swept record is
never lost even independent of the scratch copy; the archive is the convenient
browsable copy, git history is the durable one.

Modes (mutually exclusive; default --dry-run):
    --dry-run           report what would be swept; touch nothing.
    --emit-archive DIR  write the weekly detailed-CHANGELOG archive files and
                        copy the dated record files into DIR (the scratch
                        archive). Does NOT modify grc_library.
    --prune             rewrite the in-repo detailed mirror to current-week-only
                        and delete the swept dated record files from grc_library.
                        Requires --verify-archived DIR.

Options:
    --as-of YYYY-MM-DD  treat this date's ISO week (Monday) as the current week
                        to KEEP in-repo (default: the ISO week of the newest
                        detailed-CHANGELOG entry).
    --root DIR          grc_library root (default: the repo this script lives in).
    --verify-archived DIR   the scratch archive dir to check before --prune.

Exit codes: 0 success; 1 a safety check failed (e.g. --prune without a
complete archive); 2 usage error.
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
)

DATE_ANYWHERE = re.compile(r"(\d{4}-\d{2}-\d{2})")
DATED_FILENAME = re.compile(r"^(\d{4}-\d{2}-\d{2})")
ENTRY_HEADER = re.compile(r"^## ")


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


def plan(root: Path, current_week: datetime.date):
    """Return (preamble, keep_entries, sweep_by_week, sweep_records)."""
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
    return preamble, keep, by_week, records


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", default=True)
    mode.add_argument("--emit-archive", metavar="DIR")
    mode.add_argument("--prune", action="store_true")
    ap.add_argument("--as-of")
    ap.add_argument("--root", default=str(REPO_ROOT))
    ap.add_argument("--verify-archived", metavar="DIR")
    args = ap.parse_args(argv)

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

    preamble, keep, by_week, records = plan(root, current_week)

    print(f"Current week kept in-repo: week of {current_week.isoformat()} (Monday)")
    print(f"Detailed entries: {len(keep)} kept in-repo, "
          f"{sum(len(v) for v in by_week.values())} to sweep across {len(by_week)} week(s).")
    for wk in sorted(by_week):
        print(f"  archive week {wk.isoformat()}: {len(by_week[wk])} entries -> {weekly_archive_name(wk)}")
    print(f"Dated record files to sweep: {len(records)}")

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
        mirror.write_text(new_mirror, encoding="utf-8")
        for _, f in records:
            f.unlink()
        print(f"Pruned: mirror rewritten to {len(keep)} current-week entries "
              f"(re-parse assertion passed); {len(records)} record file(s) "
              f"removed. Archive verified present.")
        return 0

    print("\n(dry-run; nothing changed. Use --emit-archive then --prune to apply.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
