#!/usr/bin/env python3
"""Advisory report of UNPROCESSED maintainer-and-worker drops in the file-drop inbox.

WHY THIS EXISTS. A drop is work handed to the orchestrator OUTSIDE the order queue: the
maintainer places a document, or a worker delivers something the orchestrator never ordered
(a brief, a diagnosis, design input) and which therefore has no order id and no outbox. A sizeable external deep assessment once sat unread in that directory for an entire
overnight run, and NOTHING could have surfaced it: the drop root is outside every repository
so no audit gate walks it, and the orchestrator's own task list is built from the order queue, which a
drop is never part of. Some of that assessment's findings concerned the orchestrator's own
conduct, so the cost of not reading it was real. This tool is the missing instrument.

WHAT COUNTS AS PROCESSED. The LOCATION is the marker, deliberately, so nothing has to be
inferred: a drop still in ``inbox/`` is unprocessed, and a processed drop is MOVED to
``done/drops/<YYYY-MM>/``. Inference was tried and is not sound: a reference-scan over the
merged records returned false negatives at a high rate, because the orchestrator
records a drop's CONTENT without always naming its filename.

TWO TRAPS THIS AVOIDS, both named when the gap was routed (TODO 3.117):
- **Transient staging is not a drop, and LOCATION marks that too (3.118(c), Option i).** The
  orchestrator stages diffs and scratch files for workers to read under ``inbox/staging/``;
  everything there is reported separately as staging, never as unprocessed work. Anything
  directly in ``inbox/`` is a DROP whatever its name: the retired name-based classification
  false-negatived a genuine drop named like scratch (a real ``notes.log``), so it survives
  only as the one-window ``legacy-staging`` advisory in the report.
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

DEFAULT_ROOT = "/opt/grc/grc_working"
ROOT_ENV = "GRC_WORKING"
DROP_DIRNAME = "inbox"
DONE_DROPS = ("done", "drops")

STAGING_DIRNAME = "staging"  # inbox/staging/: location, not name, marks staging (3.118(c))

# RETIRED from classification (3.118(c) Option i, 2026-08-25): these name patterns no longer
# decide staging vs drop; location does. Kept ONLY to drive the one-deprecation-window
# `legacy-staging` advisory in report(). REMOVE (with is_legacy_staging_name and the advisory
# block plus its self-test checks) once the live exchange inbox/ carries no legacy-named
# loose files, and no later than the first PR after 2026-09-30.
LEGACY_STAGING_SUFFIXES = (".diff", ".patch", ".log", ".tmp")
LEGACY_STAGING_PREFIXES = ("pending-", "staging-", "scratch-")


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


def size_kb(p: Path) -> float:
    """Size in KB, 0.0 when the file vanished after survey (3.118(b)): a drop consumed
    between survey() and the report print must not crash the advisory, whose contract is
    that every reporting path exits 0 (only --self-test may exit non-zero)."""
    try:
        return p.stat().st_size / 1024.0
    except OSError:
        return 0.0


def is_legacy_staging_name(name: str) -> bool:
    """True when a name matches the RETIRED staging patterns; drives ONLY the report()
    legacy-staging advisory, never classification (3.118(c))."""
    low = name.lower()
    return low.endswith(LEGACY_STAGING_SUFFIXES) or low.startswith(LEGACY_STAGING_PREFIXES)


def survey(root: Path):
    """Return (unprocessed, staging, archived_count, unreadable).

    Location is the classification marker at BOTH boundaries (3.118(c)): every file
    DIRECTLY in inbox/ is a drop, whatever its name; staging is whatever lives under
    inbox/staging/, enumerated recursively. Files under any OTHER inbox/ subdirectory
    are not surveyed, unchanged from the prior behaviour (directories were always
    skipped); that residue is deliberate and stated here rather than silent."""
    drop_dir = root / DROP_DIRNAME
    staging_dir = drop_dir / STAGING_DIRNAME
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
            unprocessed.append(p)
    if staging_dir.is_dir():
        try:
            # rglob() suppresses a per-entry OSError (including an unreadable TOP staging
            # dir under Python 3.14), so probe with iterdir() first (which DOES raise on an
            # unreadable dir) to keep inbox/staging/ fail-loud like the drop dir above.
            list(staging_dir.iterdir())
            staging = sorted(q for q in staging_dir.rglob("*") if q.is_file())
        except OSError:
            unreadable.append(staging_dir)
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
            kb = size_kb(p)
            print(f"  {age_days(p):5.1f}d  {kb:7.1f}KB  {p.name}")
        print("\n  Process each, then MOVE it to done/drops/<YYYY-MM>/ so the location records")
        print("  that it was read. Do not infer processed-ness from age or from a grep.")
    else:
        print("\n  No unprocessed drops.")
    legacy = [p for p in unprocessed if is_legacy_staging_name(p.name)]
    if legacy:
        print("\nLEGACY-STAGING ADVISORY: these files match the RETIRED staging-name convention")
        print("but are loose in inbox/, so they are DROPS (counted and listed as unprocessed")
        print("above) - process them like any drop. The name no longer marks staging; put genuine")
        print("scratch in inbox/staging/, and relocate one of these there ONLY if you know it is")
        print("scratch, not a real drop:")
        for p in legacy:
            print(f"  legacy-named drop: {p.name}")
    if staging:
        print("\nSTAGING (inbox/staging/, orchestrator scratch, not work awaiting a read):")
        for p in staging:
            print(f"  {p.relative_to(root / DROP_DIRNAME)}")
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
        # drops directly in inbox/ (location decides, names do not), staged scratch under
        # inbox/staging/ (one nested), an archived drop
        (root / DROP_DIRNAME / "codex-brief.md").write_text("x")
        (root / DROP_DIRNAME / "pending-1157.diff").write_text("x")
        (root / DROP_DIRNAME / "notes.log").write_text("x")
        (root / DROP_DIRNAME / "README.md").write_text("x")
        stage = root / DROP_DIRNAME / STAGING_DIRNAME
        (stage / "deep").mkdir(parents=True)
        (stage / "1234.diff").write_text("x")
        (stage / "candidate.md").write_text("x")
        (stage / "deep" / "nested.log").write_text("x")
        arch = root.joinpath(*DONE_DROPS) / "2026-07"
        arch.mkdir(parents=True)
        (arch / "old-brief.md").write_text("x")
        un, st, ar, _ = survey(root)
        check("every loose inbox/ file is a drop, whatever its name",
              sorted(p.name for p in un),
              ["codex-brief.md", "notes.log", "pending-1157.diff"])
        check("a legacy-named loose file is a DROP now (the 3.118(c) flip)",
              "notes.log" in [p.name for p in un], True)
        check("inbox/staging/ files are staging, whatever their name",
              sorted(p.name for p in st), ["1234.diff", "candidate.md", "nested.log"])
        check("README is ignored", any(p.name == "README.md" for p in un + st), False)
        check("archived drops are counted", ar, 1)
        check("legacy matcher hits a retired pattern",
              is_legacy_staging_name("pending-1157.diff"), True)
        check("legacy matcher passes a normal drop name",
              is_legacy_staging_name("codex-brief.md"), False)
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            report(root, oneline=False)
        out = buf.getvalue()
        check("report counts legacy-named files as unprocessed",
              "unprocessed: 3" in out, True)
        check("report surfaces the legacy-staging advisory",
              "legacy-named drop:" in out, True)
        check("the drop listing precedes the advisory (advisory adds, never replaces)",
              out.index("UNPROCESSED") < out.index("legacy-named drop:"),
              True)
        # 3.118(c) F1 (codex/claude): an unreadable inbox/staging/ must fail LOUD (surface
        # in unreadable), not silently report empty - rglob suppresses the perm error, the
        # iterdir probe restores it. Skipped where the chmod does not bite (e.g. root).
        os.chmod(stage, 0)
        try:
            if not os.access(stage, os.R_OK):
                _, _, _, unr_locked = survey(root)
                check("an unreadable inbox/staging/ fails loud, not silent (F1)",
                      stage in unr_locked, True)
        finally:
            os.chmod(stage, 0o755)
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
        # 3.118(b): a drop consumed between survey() and the report print must not crash;
        # a vanished path sizes to 0.0 rather than raising (the exit-0 reporting contract).
        check("size of a vanished drop is 0.0", size_kb(Path(td) / "nonexistent-gone.md"), 0.0)

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
