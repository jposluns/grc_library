#!/usr/bin/env python3
"""Convert a session-state lease's bold field lines to the plain form, in place (3b679).

Usage: convert-session-state-lease.py --lease PATH [--dry-run]

Rewrites only the six ``**Field:** value`` lines (Active-session, Status,
Operating-mode, Last-heartbeat-UTC, Current-task, Worker-dispatches) as
``Field: value``. The file is opened read-write without truncation and
without following a link, an exclusive flock is taken on that descriptor
non-blocking with a bounded retry (5 seconds in all, as orch_store.py
takes its lock), the path is re-checked to still name the locked inode
(st_dev, st_ino) immediately after the lock is held and before any read or
write, the bytes are read under the lock, written back over the same inode,
truncated and fsynced, and the inode is confirmed unchanged.

Refused (exit 2, nothing written): a path that is not a regular non-symlink
file, a lock not acquired within 5 seconds, a path that no longer names the
locked inode, a first line other than ``# Session state: grc``, any of the
six fields missing or present more than once (plain or bold), or converted
text that gate 63 (tools/lint-session-state.py) would not pass. A lease
already in the plain form is a no-op (exit 0). --dry-run prints the line
changes and writes nothing.

Crash residual: the write is in place, write then truncate, not an atomic
replace. The converted text is never longer than the original (each
converted line loses four stars), so a crash between the write and the
truncate leaves the converted text followed by the old file's last four
bytes per converted line. Gate 63 refuses that file only when those
leftover bytes form a line it flags (for example a field-line fragment); a
leftover fragment of a trailing free-text line, such as part of the last
"- 2026-..." bullet, passes gate 63. After a crash, compare the lease's
tail with the expected text before relying on it.
"""

from __future__ import annotations

import argparse
import fcntl
import importlib.util
import os
import re
import stat
import sys
import time
from pathlib import Path

LOCK_SECONDS = 5.0
FIELDS =("Active-session", "Status", "Operating-mode", "Last-heartbeat-UTC",
          "Current-task", "Worker-dispatches")
TITLE = b"# Session state: grc"
BOLD = re.compile(rb"\*\*(" + b"|".join(f.encode() for f in FIELDS) + rb"):\*\* (.*)")
PLAIN = re.compile(rb"(" + b"|".join(f.encode() for f in FIELDS) + rb"): (.*)")


class Refused(Exception):
    """The lease is not converted; nothing is written."""


def _gate():
    path = Path(__file__).resolve().parent / "lint-session-state.py"
    if str(path.parent) not in sys.path:
        sys.path.append(str(path.parent))
    spec = importlib.util.spec_from_file_location("_lint_session_state", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def convert(data: bytes) -> tuple[bytes, list[tuple[int, bytes, bytes]]]:
    """Return the converted bytes and the (line number, old, new) changes."""
    lines = data.split(b"\n")
    if lines[0] != TITLE:
        raise Refused("line 1 is not exactly '# Session state: grc'")
    seen: dict[bytes, int] = {}
    changes = []
    for index, line in enumerate(lines):
        match = BOLD.fullmatch(line) or PLAIN.fullmatch(line)
        if not match:
            continue
        name = match.group(1)
        if name in seen:
            raise Refused("field %s appears more than once (lines %d and %d)"
                          % (name.decode(), seen[name] + 1, index + 1))
        seen[name] = index
        if match.re is BOLD:
            new = name + b": " + match.group(2)
            changes.append((index + 1, line, new))
            lines[index] = new
    absent = [f for f in FIELDS if f.encode() not in seen]
    if absent:
        raise Refused("field(s) missing: " + ", ".join(absent))
    converted = b"\n".join(lines)
    try:
        text = converted.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Refused("the lease is not UTF-8: %s" % exc)
    missing, invalid = _gate().check_text(text)
    if missing or invalid:
        raise Refused("the converted lease would fail gate 63: " + "; ".join(missing + invalid))
    return converted, changes


def lock(fd: int) -> None:
    """Take an exclusive flock without blocking, retrying for LOCK_SECONDS in all."""
    deadline = time.monotonic() + LOCK_SECONDS
    while True:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return
        except BlockingIOError:
            if time.monotonic() >= deadline:
                raise Refused("the lease lock was not acquired within %g seconds"
                              % LOCK_SECONDS)
            time.sleep(0.01)


def run(path: str, dry_run: bool) -> int:
    try:
        fd = os.open(path, (os.O_RDONLY if dry_run else os.O_RDWR)
                     | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC)
    except OSError as exc:
        print("REFUSED: cannot open %s without following a link: %s" % (path, exc.strerror),
              file=sys.stderr)
        return 2
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode):
            raise Refused("%s is not a regular file" % path)
        lock(fd)
        try:
            named = os.stat(path, follow_symlinks=False)
        except OSError as exc:
            raise Refused("%s cannot be re-checked under the lock: %s" % (path, exc.strerror))
        if (named.st_dev, named.st_ino) != (before.st_dev, before.st_ino):
            raise Refused("%s no longer names the locked inode" % path)
        data = b""
        while True:
            chunk = os.pread(fd, 65536, len(data))
            if not chunk:
                break
            data += chunk
        converted, changes = convert(data)
        for number, old, new in changes:
            print("line %d: %s -> %s" % (number, old.decode("utf-8"), new.decode("utf-8")))
        if not changes:
            print("OK: %s is already in the plain form; nothing to change." % path)
            return 0
        if dry_run:
            print("DRY RUN: %d line(s) would change; nothing written." % len(changes))
            return 0
        os.lseek(fd, 0, os.SEEK_SET)
        done = 0
        while done < len(converted):
            done += os.write(fd, converted[done:])
        os.ftruncate(fd, len(converted))
        os.fsync(fd)
        after = os.stat(path, follow_symlinks=False)
        if (after.st_dev, after.st_ino) != (before.st_dev, before.st_ino):
            print("ERROR: %s no longer names the converted inode" % path, file=sys.stderr)
            return 1
        print("OK: converted %d line(s) in %s (inode unchanged)." % (len(changes), path))
        return 0
    except Refused as exc:
        print("REFUSED: %s; nothing written." % exc, file=sys.stderr)
        return 2
    finally:
        os.close(fd)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lease", required=True, help="path to session-state.md")
    parser.add_argument("--dry-run", action="store_true", help="print changes, write nothing")
    args = parser.parse_args(argv)
    return run(args.lease, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
