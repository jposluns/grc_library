#!/usr/bin/env python3
"""Cleanup aid for stale worker-output under /tmp (P-1.16): identify and (with --apply)
stage-for-removal the old worker clones / briefs / logs that this project's dispatches leave
in /tmp, WITHOUT ever touching a live session's scratchpad, a system dir/socket, another
user's files, or an actively-running worker's workspace.

SAFETY MODEL (a destructive-capable tool: safety is the point). Two independent gates, so a
single mistake cannot select something dangerous:
  1. POSITIVE allow-list (`is_worker_output`): a candidate MUST match a known worker-output name
     pattern (`grc_` / `grc-` / `codex-`). Everything else, system dirs like `systemd-private-*`,
     SSH / tmux sockets, other users' /tmp entries, ad-hoc files, is NEVER a candidate. A negative
     protect-list over all of /tmp is NOT a safe destructive scope (codex vp116 finding 1), so the
     positive allow-list is the primary scope and the tool errs toward LEAVING, not deleting.
  2. PROTECT-LIST (`is_protected`): even within the allow-list, exclude any dot-prefixed name, any
     `claude-*` Claude Code session scratchpad, the staging dir (its live basename, resolved), and
     `--keep` names.
Plus an age gate: an entry is eligible only if untouched for `--days` (>= MIN_DAYS; a near-zero age
is refused, codex finding 3). Liveness uses the newest of the entry's own mtime and, for a READABLE
directory, its top-level children's mtimes (codex finding 2: a workspace mutating files in place can
have a stale dir mtime). For a worker-owned dir whose children are unreadable, the dir mtime is the
best available signal; the conservative default --days plus the short worker lifecycle bound this.

REMOVAL: `rm -rf` on /tmp is currently HARNESS-blocked (the OS allows sudo). So --apply MOVES eligible
entries into a private staging dir (default /tmp/deleteme) via `shutil.move`. Immediately before each
move it RE-VERIFIES the entry (still allow-listed + not protected + still old + not a symlink + same
device/inode as the scan), so an entry touched between scan and move (a TOCTOU race, codex finding 4)
is refused, not moved. A move that fails (worker-owned, needs sudo) is REPORTED (exit 1), never
silently swallowed. There is deliberately NO unguarded `--emit-rm` delayed-script mode (codex finding 4):
the guarded, re-verified move is the only mutation path; a future sudo-removal mode would carry the
same guards.

Usage:
    python3 tools/cleanup-tmp-worker-output.py                 # DRY-RUN: list eligible worker-output
    python3 tools/cleanup-tmp-worker-output.py --days 3        # eligibility age (default 3, min 0.5)
    python3 tools/cleanup-tmp-worker-output.py --sizes         # add best-effort du totals (slow)
    python3 tools/cleanup-tmp-worker-output.py --apply         # guarded MOVE eligible -> /tmp/deleteme
    python3 tools/cleanup-tmp-worker-output.py --self-test

Exit codes: 0 (dry-run reported, or --apply completed with no failure/skip); 1 (--apply had a
move-failure or a pre-move re-verify refusal, all reported); 2 (usage error, or /tmp not usable).
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import time
from pathlib import Path

TMP = Path("/tmp")
PROTECT_EXACT = {"deleteme"}
# POSITIVE allow-list: a candidate name MUST match one of these known worker-output patterns.
# This is the destructive SCOPE. Deliberately tight: the project's worker clones / scratch / codex
# worktrees are `grc_*`, `grc-*`, `codex-*`; anything else (system, sockets, other users, ad-hoc)
# is out of scope and left alone.
WORKER_OUTPUT_RE = re.compile(r"^(grc[_-]|codex-)", re.IGNORECASE)
MIN_DAYS = 0.5  # a smaller age would select freshly-touched entries; refuse it


def is_worker_output(name: str) -> bool:
    """POSITIVE allow-list (the destructive scope): True only for a known worker-output name.
    PURE (name-only), so a system dir, a socket, or another user's entry is never a candidate."""
    return bool(WORKER_OUTPUT_RE.match(name))


def is_protected(name: str, keep: set[str], staging_name: str = "deleteme") -> bool:
    """A /tmp entry NAME is protected (never eligible) even if it is worker-output-shaped: a
    dot-prefixed name, a `claude-*` session scratchpad, the live staging dir's basename, an exact
    PROTECT_EXACT name, or a --keep name. PURE, so it is directly unit-testable."""
    if name.startswith("."):
        return True
    if name.startswith("claude-"):
        return True
    if name == staging_name or name in PROTECT_EXACT or name in keep:
        return True
    return False


def eligible(entries: list[tuple[str, float]], now: float, days: float,
             keep: set[str], staging_name: str = "deleteme") -> list[str]:
    """PURE: from [(name, effective_mtime_epoch), ...] return the sorted names eligible for cleanup:
    worker-output (positive allow-list) AND not protected AND older than `days` (effective mtime
    <= now - days*86400). Age is the liveness proxy, so a recently-touched entry is never eligible."""
    cutoff = now - days * 86400.0
    return sorted(
        name for name, mt in entries
        if is_worker_output(name) and not is_protected(name, keep, staging_name) and mt <= cutoff
    )


def _entry_mtime(p: Path) -> float | None:
    """Newest of p's own mtime and (for a READABLE, non-symlink dir) its top-level children's
    mtimes, so a workspace mutating files in place is not judged stale by a lagging dir mtime.
    None if p cannot be lstat'd. Children are best-effort: a worker-owned dir whose children are
    unreadable falls back to the dir's own mtime (the best available signal)."""
    try:
        st = p.lstat()
    except OSError:
        return None
    newest = st.st_mtime
    if os.path.isdir(p) and not os.path.islink(p):
        try:
            for child in os.scandir(p):
                try:
                    newest = max(newest, child.stat(follow_symlinks=False).st_mtime)
                except OSError:
                    continue
        except OSError:
            pass  # unreadable dir: keep the dir's own mtime
    return newest


def _scan(root: Path = TMP) -> list[tuple[str, float, tuple[int, int]]]:
    """[(name, effective_mtime, (device, inode)), ...] for each top-level entry. The (device,
    inode) identity is captured so --apply can confirm the entry did not change since the scan."""
    out = []
    for entry in os.scandir(root):
        p = Path(entry.path)
        mt = _entry_mtime(p)
        if mt is None:
            continue
        try:
            st = p.lstat()
            ident = (st.st_dev, st.st_ino)
        except OSError:
            continue
        out.append((entry.name, mt, ident))
    return out


def _dir_size(p: Path) -> int | None:
    import subprocess
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


def _resolve_staging(raw: str, keep: set[str]) -> tuple[Path, str] | None:
    """Validate the staging dir: it must resolve to a path directly under /tmp, must not be a
    symlink, and its basename must not itself be worker-output-shaped (else it could be selected).
    Returns (resolved_path, basename) or None on rejection (message printed)."""
    p = Path(raw)
    if p.is_symlink():
        print(f"ERROR: --staging {raw} is a symlink; refusing (staging must be a real dir).", file=sys.stderr)
        return None
    resolved = p.resolve()
    if resolved.parent != TMP.resolve():
        print(f"ERROR: --staging must be directly under {TMP} (got {resolved}).", file=sys.stderr)
        return None
    name = resolved.name
    if is_worker_output(name) and name not in keep:
        print(f"ERROR: --staging basename {name!r} matches the worker-output pattern; pick another "
              f"(it would be a cleanup candidate).", file=sys.stderr)
        return None
    return resolved, name


def _self_test() -> int:
    checks = []
    keep: set[str] = set()
    # POSITIVE allow-list: only grc_/grc-/codex- match; system/socket/other-user/ad-hoc do NOT
    checks.append(("allow-grc_", is_worker_output("grc_copy_123") and is_worker_output("grc-pr1300.abc")))
    checks.append(("allow-codex", is_worker_output("codex-m05-0XKI2R")))
    checks.append(("deny-systemd", not is_worker_output("systemd-private-abc")))
    checks.append(("deny-socket", not is_worker_output(".X11-unix") and not is_worker_output("ssh-XXXX")))
    checks.append(("deny-adhoc", not is_worker_output("A.cut") and not is_worker_output("stygia-pages-venv")))
    checks.append(("deny-other-user", not is_worker_output("pymp-abcd") and not is_worker_output("tmp1234")))
    # protect-list
    checks.append(("dot-protected", is_protected(".X11-unix", keep) and is_protected(".agents", keep)))
    checks.append(("claude-protected", is_protected("claude-1004", keep)))
    checks.append(("staging-protected", is_protected("deleteme", keep) and is_protected("mystage", keep, "mystage")))
    checks.append(("keep-protected", is_protected("grc-special", {"grc-special"})))
    # eligibility: worker-output + not-protected + old
    now, day = 1_000_000.0, 86400.0
    entries = [
        ("grc_copy_old", now - 5 * day),        # worker-output, old -> eligible
        ("codex-recent", now - 0.1 * day),      # worker-output, RECENT -> not eligible
        ("systemd-private-x", now - 30 * day),  # OLD but NOT worker-output -> not eligible
        ("claude-1004", now - 30 * day),        # worker-output? no; also protected -> not eligible
        ("grc-validate-x", now - 3.5 * day),    # worker-output, old -> eligible
        ("deleteme", now - 30 * day),           # protected staging -> not eligible
        ("A.cut", now - 30 * day),              # old but NOT worker-output -> not eligible
    ]
    el = eligible(entries, now, 3.0, keep)
    checks.append(("eligible-only-worker-output-old", el == ["grc-validate-x", "grc_copy_old"]))
    checks.append(("eligible-excludes-recent", "codex-recent" not in el))
    checks.append(("eligible-excludes-systemd", "systemd-private-x" not in el))
    checks.append(("eligible-excludes-adhoc", "A.cut" not in el))
    checks.append(("cutoff-boundary-inclusive", eligible([("grc-b", now - 3 * day)], now, 3.0, keep) == ["grc-b"]))
    checks.append(("just-recent-excluded", eligible([("grc-b", now - 2.99 * day)], now, 3.0, keep) == []))
    checks.append(("keep-excludes", eligible([("grc-mine", now - 9 * day)], now, 3.0, {"grc-mine"}) == []))
    checks.append(("staging-name-excludes", eligible([("grc-stage", now - 9 * day)], now, 3.0, keep, "grc-stage") == []))
    bad = [n for n, ok in checks if not ok]
    if bad:
        print(f"cleanup-tmp-worker-output self-test: FAIL {bad}")
        return 1
    print(f"cleanup-tmp-worker-output self-test: OK ({len(checks)} checks)")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--days", type=float, default=3.0, help="eligible if untouched for this many days (default 3, min 0.5)")
    ap.add_argument("--apply", action="store_true", help="guarded MOVE eligible entries to the staging dir")
    ap.add_argument("--staging", default="/tmp/deleteme", help="staging dir for --apply (default /tmp/deleteme)")
    ap.add_argument("--sizes", action="store_true", help="compute du sizes (slow; worker-owned dirs show ?)")
    ap.add_argument("--keep", nargs="*", default=[], help="extra top-level names to protect")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv[1:])
    if args.self_test:
        return _self_test()
    # age validation (codex finding 3): refuse a non-finite / non-positive / too-small age
    import math
    if not math.isfinite(args.days) or args.days < MIN_DAYS:
        print(f"ERROR: --days must be a finite value >= {MIN_DAYS} (got {args.days}); a smaller age "
              f"would select freshly-touched entries.", file=sys.stderr)
        return 2
    if not TMP.is_dir() or not os.access(TMP, os.R_OK):
        print(f"ERROR: {TMP} is not readable.", file=sys.stderr)
        return 2
    keep = set(args.keep)
    resolved = _resolve_staging(args.staging, keep) if args.apply else (Path(args.staging), Path(args.staging).name)
    if resolved is None:
        return 2
    staging_path, staging_name = resolved
    now = time.time()
    scan = _scan(TMP)
    scan_ident = {name: ident for name, _, ident in scan}
    names = eligible([(n, mt) for n, mt, _ in scan], now, args.days, keep, staging_name)
    if not names:
        print(f"No /tmp worker-output eligible for cleanup (none matching the allow-list, unprotected, "
              f"and untouched > {args.days:g} days).")
        return 0
    if args.sizes:
        sizes = {n: _dir_size(TMP / n) for n in names}
        known = sum(v for v in sizes.values() if v is not None)
        n_unk = sum(1 for v in sizes.values() if v is None)
        tail = f", plus {n_unk} of unknown size (worker-owned)" if n_unk else ""
        print(f"{len(names)} eligible worker-output entr(y/ies), untouched > {args.days:g} days, "
              f"known total ~{_human(known)}{tail}:")
        for n in names:
            sz = sizes[n]
            print(f"  {n}  (~{_human(sz) if sz is not None else '?'})")
    else:
        print(f"{len(names)} eligible worker-output entr(y/ies), untouched > {args.days:g} days "
              f"(--sizes for du totals):")
        for n in names:
            print(f"  {n}")
    if not args.apply:
        print(f"\nDRY-RUN: nothing moved. Re-run with --apply to guarded-MOVE these to {staging_path}.")
        return 0
    try:
        staging_path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"ERROR: cannot create staging dir {staging_path}: {exc}", file=sys.stderr)
        return 2
    failures, skipped, moved = [], [], 0
    cutoff = now - args.days * 86400.0
    for n in names:
        src = TMP / n
        # PRE-MOVE re-verify (codex finding 4, TOCTOU): the name is still allow-listed + not
        # protected; the entry still exists, is not a symlink, is still old, and is the SAME
        # device/inode we scanned. Any change -> refuse (skip + report), never move.
        if not is_worker_output(n) or is_protected(n, keep, staging_name):
            skipped.append((n, "no longer a candidate")); continue
        try:
            st = src.lstat()
        except OSError as exc:
            skipped.append((n, f"vanished/unstat-able: {exc}")); continue
        if os.path.islink(src):
            skipped.append((n, "is now a symlink")); continue
        if (st.st_dev, st.st_ino) != scan_ident.get(n):
            skipped.append((n, "device/inode changed since scan")); continue
        if _entry_mtime(src) > cutoff:
            skipped.append((n, "touched since scan (now recent)")); continue
        dest = staging_path / n
        if os.path.exists(dest) or os.path.islink(dest):
            skipped.append((n, "destination already exists")); continue
        try:
            shutil.move(str(src), str(dest))
            moved += 1
        except (OSError, shutil.Error) as exc:
            failures.append((n, str(exc)))
    print(f"\nMOVED {moved}/{len(names)} to {staging_path}.")
    rc = 0
    if skipped:
        print(f"{len(skipped)} REFUSED by the pre-move re-verify (not moved):", file=sys.stderr)
        for n, why in skipped:
            print(f"  {n}: {why}", file=sys.stderr)
        rc = 1
    if failures:
        print(f"{len(failures)} could NOT be moved (likely worker-owned; needs the permission exception):", file=sys.stderr)
        for n, err in failures:
            print(f"  {n}: {err}", file=sys.stderr)
        rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
