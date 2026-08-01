#!/usr/bin/env python3
"""Cleanup aid for stale worker-output under /tmp (P-1.16): identify and (with --apply)
stage-for-removal the old worker clones / briefs / logs that accumulate in /tmp across
sessions, WITHOUT ever touching a live session's scratchpad, a system socket, or an
actively-running worker's workspace.

WHY: worker dispatches leave clones (grc_*, codex-*, grc-validate-*, grc_qa_clone*), venvs,
and scratch dirs in /tmp; over weeks these reach many GB. This tool is the recurring cleanup
the maintainer asked for (2026-08-01), designed SAFE-BY-DEFAULT: it is DRY-RUN unless --apply,
and it EXCLUDES a hard protect-list so it can never remove something in use.

PROTECT-LIST (never selected, regardless of age):
  - Any dot-prefixed entry (`.X11-unix`, `.ICE-unix`, `.font-unix`, `.XIM-unix`, `.Test-unix`
    system sockets AND worker-infra dot-dirs like `.agents` / `.codex` / `.working`).
  - `claude-*` (Claude Code session scratchpad roots: this live session AND any other, so a
    concurrent session is never disturbed).
  - The staging dir itself (`deleteme`) and this tool's own configured keep names.
  - Anything whose mtime is NEWER than --days (an actively-running worker's dir is recent, so
    age is the liveness proxy: only entries untouched for --days are eligible).

REMOVAL: `rm -rf` on /tmp is currently DENIED by the harness sandbox, so --apply MOVES eligible
entries into a staging dir (`/tmp/deleteme/`, override with --staging) via `mv`; a later step
(or the maintainer, or a permission grant for `rm -rf /tmp/*`) empties the staging dir. A move
that fails on permission (a worker-owned entry) is REPORTED, not silently skipped, so nothing is
assumed removed that was not (the evidence-grounded-completion discipline for a destructive op).

Usage:
    python3 tools/cleanup-tmp-worker-output.py                 # DRY-RUN: list eligible + total size
    python3 tools/cleanup-tmp-worker-output.py --days 3        # eligibility age (default 3)
    python3 tools/cleanup-tmp-worker-output.py --apply         # MOVE eligible entries to /tmp/deleteme
    python3 tools/cleanup-tmp-worker-output.py --emit-rm       # print a `sudo rm -rf` script (run it yourself)
    python3 tools/cleanup-tmp-worker-output.py --self-test

Exit codes: 0 (dry-run reported, or --apply completed with no move-failure); 1 (--apply had at
least one move-failure, reported); 2 (usage error, or /tmp not readable).
"""
from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

TMP = Path("/tmp")
# Names never selected even when old. `claude-` and dot-prefix are handled by rule, not listed.
PROTECT_EXACT = {"deleteme"}


def is_protected(name: str, keep: set[str]) -> bool:
    """A /tmp entry NAME is protected (never eligible) if it is dot-prefixed (system socket or
    worker-infra dir), a Claude Code session root (`claude-*`), the staging dir, or a keep name.
    PURE (name-only) so it is directly unit-testable."""
    if name.startswith("."):
        return True
    if name.startswith("claude-"):
        return True
    if name in PROTECT_EXACT or name in keep:
        return True
    return False


def eligible(entries: list[tuple[str, float]], now: float, days: float, keep: set[str]) -> list[str]:
    """PURE: from [(name, mtime_epoch), ...] return the sorted names eligible for cleanup: not
    protected AND older than `days` (mtime <= now - days*86400). Age is the liveness proxy, so an
    actively-written worker dir (recent mtime) is never eligible."""
    cutoff = now - days * 86400.0
    return sorted(name for name, mt in entries if not is_protected(name, keep) and mt <= cutoff)


def _scan(root: Path = TMP) -> list[tuple[str, float]]:
    out = []
    for p in root.iterdir():
        try:
            out.append((p.name, p.stat().st_mtime))
        except OSError:
            continue  # vanished / unreadable; skip (reported by count delta if needed)
    return out


def _dir_size(p: Path) -> int | None:
    """du -sb in bytes; None if unreadable (worker-owned) so the caller shows '?' not a
    misleading 0. stderr is suppressed (du spams 'Permission denied' on worker-owned dirs)."""
    try:
        out = subprocess.check_output(["du", "-sb", str(p)], text=True, stderr=subprocess.DEVNULL)
        return int(out.split()[0])
    except (subprocess.CalledProcessError, OSError, ValueError, IndexError):
        return None


def _human(n: float) -> str:
    size = float(n)
    for unit in ("B", "K", "M", "G", "T"):
        if size < 1024 or unit == "T":
            return f"{size:.0f}{unit}" if unit == "B" else f"{size:.1f}{unit}"
        size /= 1024.0
    return f"{size:.1f}T"


def _self_test() -> int:
    checks = []
    keep: set[str] = set()
    # protect rules
    checks.append(("dot-protected", is_protected(".X11-unix", keep) and is_protected(".agents", keep)))
    checks.append(("claude-session-protected", is_protected("claude-1004", keep) and is_protected("claude-1005", keep)))
    checks.append(("staging-protected", is_protected("deleteme", keep)))
    checks.append(("keep-name-protected", is_protected("special", {"special"})))
    checks.append(("normal-not-protected", not is_protected("grc_copy_123", keep)))
    # eligibility by age
    now = 1_000_000.0
    day = 86400.0
    entries = [
        ("grc_copy_old", now - 5 * day),      # old, eligible
        ("codex-recent", now - 0.5 * day),    # recent, NOT eligible
        ("claude-1004", now - 30 * day),      # old but PROTECTED (session)
        (".agents", now - 30 * day),          # old but PROTECTED (dot)
        ("grc-validate-x", now - 3.5 * day),  # old, eligible
        ("deleteme", now - 30 * day),         # PROTECTED (staging)
    ]
    el = eligible(entries, now, 3.0, keep)
    checks.append(("eligible-picks-old-unprotected", el == ["grc-validate-x", "grc_copy_old"]))
    checks.append(("eligible-excludes-recent", "codex-recent" not in el))
    checks.append(("eligible-excludes-protected", "claude-1004" not in el and ".agents" not in el and "deleteme" not in el))
    # boundary: exactly at cutoff is eligible (<=)
    checks.append(("cutoff-boundary-inclusive", eligible([("b", now - 3 * day)], now, 3.0, keep) == ["b"]))
    # keep override
    checks.append(("keep-excludes", eligible([("mine", now - 9 * day)], now, 3.0, {"mine"}) == []))
    bad = [n for n, ok in checks if not ok]
    if bad:
        print(f"cleanup-tmp-worker-output self-test: FAIL {bad}")
        return 1
    print(f"cleanup-tmp-worker-output self-test: OK ({len(checks)} checks)")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--days", type=float, default=3.0, help="eligible if untouched for this many days (default 3)")
    ap.add_argument("--apply", action="store_true", help="MOVE eligible entries to the staging dir")
    ap.add_argument("--staging", default="/tmp/deleteme", help="staging dir for --apply (default /tmp/deleteme)")
    ap.add_argument("--emit-rm", action="store_true", help="print a `sudo rm -rf` script for the eligible set; do not act")
    ap.add_argument("--sizes", action="store_true", help="compute du sizes (slow; best-effort, worker-owned dirs show ?)")
    ap.add_argument("--keep", nargs="*", default=[], help="extra top-level names to protect")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv[1:])
    if args.self_test:
        return _self_test()
    if not TMP.is_dir() or not os.access(TMP, os.R_OK):
        print(f"ERROR: {TMP} is not readable.", file=sys.stderr)
        return 2
    keep = set(args.keep)
    now = time.time()
    names = eligible(_scan(), now, args.days, keep)
    if not names:
        print(f"No /tmp entries eligible for cleanup (none untouched > {args.days:g} days outside the protect-list).")
        return 0
    if args.sizes:
        sizes = {n: _dir_size(TMP / n) for n in names}
        known = sum(v for v in sizes.values() if v is not None)
        n_unk = sum(1 for v in sizes.values() if v is None)
        tail = f", plus {n_unk} of unknown size (worker-owned)" if n_unk else ""
        print(f"{len(names)} eligible /tmp entr(y/ies), untouched > {args.days:g} days, "
              f"known total ~{_human(known)}{tail}:")
        for n in names:
            sz = sizes[n]
            print(f"  {n}  (~{_human(sz) if sz is not None else '?'})")
    else:
        print(f"{len(names)} eligible /tmp entr(y/ies), untouched > {args.days:g} days "
              f"(re-run with --sizes for du totals):")
        for n in names:
            print(f"  {n}")
    if args.emit_rm:
        print("\n# Run with sudo to remove (review first):")
        for n in names:
            print(f"sudo rm -rf {shlex.quote(str(TMP / n))}")
        return 0
    if not args.apply:
        print(f"\nDRY-RUN: nothing moved. Re-run with --apply to MOVE these to {args.staging}, "
              f"or --emit-rm for a sudo rm script.")
        return 0
    staging = Path(args.staging)
    try:
        staging.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"ERROR: cannot create staging dir {staging}: {exc}", file=sys.stderr)
        return 2
    failures = []
    moved = 0
    for n in names:
        src = TMP / n
        try:
            shutil.move(str(src), str(staging / n))
            moved += 1
        except (OSError, shutil.Error) as exc:
            failures.append((n, str(exc)))
    print(f"\nMOVED {moved}/{len(names)} to {staging}.")
    if failures:
        print(f"{len(failures)} could NOT be moved (likely worker-owned; use --emit-rm + sudo):", file=sys.stderr)
        for n, err in failures:
            print(f"  {n}: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
