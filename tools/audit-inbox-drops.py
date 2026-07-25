#!/usr/bin/env python3
"""Advisory report of UNPROCESSED maintainer-and-worker drops in the file-drop inbox.

WHY THIS EXISTS. A drop is work handed to the orchestrator OUTSIDE the order queue: the
maintainer places a document, or a worker delivers something the orchestrator never ordered
(a brief, a diagnosis, design input) and which therefore has no order id and no outbox. On
2026-07-25 a 13KB external deep assessment sat unread in that directory for an entire
overnight run, and NOTHING could have surfaced it: the drop root is outside every repository
so no audit gate walks it, ``audit-delivery-status.py`` reconciles worker OUTBOX deliveries
rather than drops, and the orchestrator's own task list is built from the order queue, which a
drop is never part of. Two of that assessment's findings concerned the orchestrator's own
conduct, so the cost of not reading it was real. This tool is the missing instrument.

WHAT COUNTS AS PROCESSED. The LOCATION is the marker, deliberately, so nothing has to be
inferred: a drop still in ``inbox/`` is unprocessed, and a processed drop is MOVED to
``done/drops/<YYYY-MM>/``. That mirrors how a consumed delivery moves to
``done/deliveries/<YYYY-MM>/``. Inference was tried and is not sound: a reference-scan over the
merged records returned false negatives at roughly a 30 percent rate, because the orchestrator
records a drop's CONTENT without always naming its filename.

TWO TRAPS THIS AVOIDS, both named when the gap was routed (TODO 3.117):
- **Transient staging is not a drop.** The orchestrator stages diffs and scratch files in the
  same directory for workers to read. Anything matching ``TRANSIENT_SUFFIXES`` or
  ``TRANSIENT_PREFIXES`` is reported separately as staging, never as unprocessed work.
- **Age is not evidence.** An old drop can be unread and a new one already consumed, so age is
  reported as CONTEXT (how long something has been waiting) and never used to decide status.

It is advisory: every reporting path exits 0, so it can be run at any boundary without
gating anything. Only ``--self-test`` can exit non-zero, on a self-test failure. stdlib-only,
and a no-op when the drop root is absent (the adopter case).
"""
from __future__ import annotations

import argparse
import datetime
import os
import sys
from pathlib import Path

DEFAULT_ROOT = "/home/grc/grc_working"
ROOT_ENV = "GRC_WORKING"
DROP_DIRNAME = "inbox"
DONE_DROPS = ("done", "drops")

# Orchestrator staging, not maintainer work. Reported separately so it is visible but never
# counted as something awaiting a read.
TRANSIENT_SUFFIXES = (".diff", ".patch", ".log", ".tmp")
TRANSIENT_PREFIXES = ("pending-", "staging-", "scratch-")


def root_dir(explicit: str | None) -> Path | None:
    if explicit:
        p = Path(explicit)
        if not p.is_dir():
            print(f"audit-inbox-drops: --root {explicit} does not resolve; nothing to report.")
            return None
        return p
    env = os.environ.get(ROOT_ENV)
    if env and Path(env).is_dir():
        return Path(env)
    p = Path(DEFAULT_ROOT)
    return p if p.is_dir() else None


def age_days(p: Path) -> float:
    try:
        mtime = p.stat().st_mtime
    except OSError:
        return 0.0
    now = datetime.datetime.now(datetime.timezone.utc).timestamp()
    return max(0.0, (now - mtime) / 86400.0)


def is_transient(name: str) -> bool:
    low = name.lower()
    return low.endswith(TRANSIENT_SUFFIXES) or low.startswith(TRANSIENT_PREFIXES)


def survey(root: Path):
    """Return (unprocessed, staging, archived_count, unreadable)."""
    drop_dir = root / DROP_DIRNAME
    unprocessed, staging, unreadable = [], [], []
    if drop_dir.is_dir():
        try:
            entries = sorted(drop_dir.iterdir())
        except OSError:
            unreadable.append(drop_dir)
            entries = []
        for p in entries:
            if not p.is_file() or p.name == "README.md":
                continue
            (staging if is_transient(p.name) else unprocessed).append(p)
    archived = 0
    base = root.joinpath(*DONE_DROPS)
    if base.is_dir():
        try:
            for mdir in base.iterdir():
                if mdir.is_dir():
                    archived += sum(1 for q in mdir.iterdir() if q.is_file())
        except OSError:
            unreadable.append(base)
    return unprocessed, staging, archived, unreadable


def report(root: Path, oneline: bool) -> int:
    unprocessed, staging, archived, unreadable = survey(root)
    if oneline:
        print(f"drops: {len(unprocessed)} unprocessed / {len(staging)} staging "
              f"/ {archived} archived")
        return 0
    print(f"inbox-drop reconciliation (advisory) under {root}")
    print(f"  unprocessed: {len(unprocessed)}   staging: {len(staging)}   "
          f"archived: {archived}")
    if unprocessed:
        print("\nUNPROCESSED (still in inbox/, so not yet read; age is context, not status):")
        for p in sorted(unprocessed, key=age_days, reverse=True):
            kb = p.stat().st_size / 1024.0
            print(f"  {age_days(p):5.1f}d  {kb:7.1f}KB  {p.name}")
        print("\n  Process each, then MOVE it to done/drops/<YYYY-MM>/ so the location records")
        print("  that it was read. Do not infer processed-ness from age or from a grep.")
    else:
        print("\n  No unprocessed drops.")
    if staging:
        print("\nSTAGING (orchestrator scratch, not work awaiting a read):")
        for p in staging:
            print(f"  {p.name}")
    for u in unreadable:
        print(f"\n  note: {u} is not readable, so its contents are NOT reflected above.")
    return 0


def self_test() -> int:
    import tempfile
    failures = []
    total = [0]  # a list so `check` can mutate it without a nonlocal declaration

    def check(name, got, want):
        total[0] += 1
        ok = got == want
        print(f"  {'PASS' if ok else 'FAIL'}: {name} -> {got}" + ("" if ok else f" (expected {want})"))
        if not ok:
            failures.append(name)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / DROP_DIRNAME).mkdir()
        # a real drop, a staging diff, an archived drop
        (root / DROP_DIRNAME / "codex-brief.md").write_text("x")
        (root / DROP_DIRNAME / "pending-1157.diff").write_text("x")
        (root / DROP_DIRNAME / "notes.log").write_text("x")
        (root / DROP_DIRNAME / "README.md").write_text("x")
        arch = root.joinpath(*DONE_DROPS) / "2026-07"
        arch.mkdir(parents=True)
        (arch / "old-brief.md").write_text("x")
        un, st, ar, _ = survey(root)
        check("a real drop is unprocessed", [p.name for p in un], ["codex-brief.md"])
        check("a .diff is staging, not a drop", "pending-1157.diff" in [p.name for p in st], True)
        check("a .log is staging", "notes.log" in [p.name for p in st], True)
        check("README is ignored", any(p.name == "README.md" for p in un + st), False)
        check("archived drops are counted", ar, 1)
        # an OLD drop is still unprocessed: age must not decide status
        old = root / DROP_DIRNAME / "ancient.md"
        old.write_text("x")
        past = datetime.datetime.now(datetime.timezone.utc).timestamp() - 400 * 86400
        os.utime(old, (past, past))
        un2, _, _, _ = survey(root)
        check("age does not mark a drop processed", "ancient.md" in [p.name for p in un2], True)
        # an absent drop root is a clean no-op
        empty = Path(td) / "empty"
        empty.mkdir()
        un3, st3, ar3, _ = survey(empty)
        check("absent drop dir is a no-op", (un3, st3, ar3), ([], [], 0))

    # Both numbers derive from the actual check count. A hardcoded denominator decouples the
    # reported total from reality, so a later added check goes silently uncounted and a reader
    # auditing coverage from this output under-counts it (found by the #1167 sweep, which
    # observed seven PASS lines above a "6/6" total).
    print(f"\nself-test: {total[0] - len(failures)}/{total[0]} passed" if not failures
          else f"\nself-test: FAILED ({len(failures)} of {total[0]})")
    return 1 if failures else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", help="file-drop exchange root (default $GRC_WORKING or the VM path)")
    ap.add_argument("--oneline", action="store_true", help="one short line, for a statusline")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    root = root_dir(a.root)
    if root is None:
        print("audit-inbox-drops: no file-drop exchange root present; nothing to report.")
        return 0
    return report(root, a.oneline)


if __name__ == "__main__":
    sys.exit(main())
