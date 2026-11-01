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

The root roll-up and the detailed-mirror sweep are ONE coupled operation,
produced together by the coupled roll-up tool in the private maintainer
repository; a hand-made root roll-up fails the CHANGELOG mirror header-parity
gate (specification gate 59), so the advisory message names that tool rather than inviting a
hand edit. The message deliberately carries no sibling-repo path token (the
cross-repo reference audit flags a private-sibling pointer from a public-tree
file for over-exposure review).

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

Output: besides the human `DAILY SUMMARY DUE for <date>` line (kept for existing
readers), every checked run prints machine-readable lines a later reader can
parse (a run with no usable stdout is refused before it checks anything,
below), framed by a BEGIN/END pair that lets that reader tell a complete report
from a truncated or spliced one:

    D8 BEGIN rev=<40hex|UNKNOWN> today=<YYYY-MM-DD> run=<64hex>
    D8 DUE id=D8-<date>@<rev12|UNKNOWN> date=<date> count=<n> due_since=<date+1>T00:00:00Z
    DAILY SUMMARY DUE for <date>: ...       (one DUE pair per due date, oldest first)
    OK: ...                                 (instead of the DUE pairs when none is due)
    D8 END rev=<40hex|UNKNOWN> today=<YYYY-MM-DD> run=<64hex> due=<n> rc=0

`run` is the SHA-256 (hex) of the UTF-8 text `rev=<rev> today=<date>`, a LF,
then every line between BEGIN and END, each followed by a LF.

Reader rule: a report is complete only when its BEGIN and END lines carry
the same `run` and name the same `rev` and `today`, `run` recomputed over
that `rev`, that `today` and every line between them equals it, and the END
line ends `due=<n> rc=0` with `<n>` the number of `D8 DUE` lines between them.
A BEGIN or END line counts only when it matches its whole grammar line above,
with no other text anywhere on it, so an END line with a token added between
`run=` and `due=`, or after `rc=0`, is not an END line.
Anything else is not a complete report: a BEGIN with no such END, lines cut
from or added to the lines between (a run's BEGIN and END around another
run's lines), or an END line cut short or altered after `run` (`due=` and
`rc=` are outside the digest, so the count is checked on its own).

The report carries no time of day. It has two clock inputs (audit programme
principle 1): the UTC date, and the elapsed time of each git call, which has a
30-second limit (`GIT_TIMEOUT`), so a call that runs past it makes `rev`
UNKNOWN (below) where a quicker one would give the SHA. Its other inputs are the CHANGELOG bytes and
`rev`, and `rev` depends on more than the repository (below), so the current
date is not D8's only input from outside the repository. Two qualifications
apply: the git environment decides whether a revision is available at all
(a SHA or UNKNOWN, below), and the human line after `D8 NOT-FOUND` or `D8
REFUSED` also depends on the path as given, the interpreter, the operating
system and stdout's encoding. `D8-<date>` is the stable item key;
`@<rev12>` binds it to the checked revision, and is `@UNKNOWN` when the
revision is. `rev` is HEAD's commit only when the CHANGELOG bytes read are
exactly that commit's blob for that path, read with replacement objects disabled (a
replacement ref cannot substitute another blob; grafts rewrite only parents,
which D8 never reads); otherwise it is UNKNOWN rather than a guess. Whether
`rev` is a SHA or UNKNOWN therefore depends not only on the CHANGELOG and the
commit but also on the git found on PATH, its configuration and environment
(GIT_DIR selects the repository; a broken GIT_CONFIG_GLOBAL or the
safe.directory ownership check makes git fail; a SHA-256 repository gives no
40-hex SHA), and checkout filters (CRLF conversion makes the working-tree
bytes differ from the blob): the same CHANGELOG at the same commit can give
the SHA in one environment and UNKNOWN in another. This fails safe: UNKNOWN
never names a commit, and a SHA is printed only for its blob's exact bytes.
The blob is read at the commit the first git call returned (`<rev>:./<name>`),
never at `HEAD` again, so a HEAD that moves between the two calls cannot bind
one commit to another commit's bytes.
In CI, where D8 runs only for a pull request, `rev` is GitHub's temporary merge
commit of the pull request's head into its base branch (the workflow's default
checkout), not the head commit itself.

Every git call disables replacement objects twice, by the --no-replace-objects
flag and by GIT_NO_REPLACE_OBJECTS=1. Each does so on its own; both are kept
as defence in depth, and the test suite pins each separately, so removing
either alone fails a test. Each git call reads no standard input and has a
timeout, and a timeout is a git failure like any other.

Exit status is 0 whatever is due and in every case listed below: the
finding is advisory (offload the coupled roll-up run to a worker), never a
push blocker. The exceptions to exit 0, a complete list, all lie outside
D8's checking of the CHANGELOG:
  * an unknown option or a missing option value is argparse's usage error
    (exit 2);
  * a run with no usable stdout, as when the process starts with file
    descriptor 1 closed (Python then sets `sys.stdout` to None, and `print`
    writes nothing) or stdout's descriptor or stream is closed, is refused
    before anything is checked, and its exit is non-zero in every case, so a
    report that could not be delivered never reads as a pass. When stderr is
    writable, D8 writes one line giving the reason to stderr and exits 3; with
    no stderr at all (file descriptor 2 also closed at startup, so
    `sys.stderr` is None) it writes nothing and exits 3. This check runs
    first, before the options are parsed, so with no usable stdout an unknown
    option, `--help` and `--self-test` are refused the same way. When stderr
    exists but cannot be written (the device is full, as on /dev/full), the
    exit is still non-zero: D8 catches the failed write and returns 3. Which
    code the process ends with depends on stderr's buffering: unbuffered
    (`python3 -u`), nothing is left to write and the exit is 3; with stderr's
    default buffering, the unwritten line stays in stderr's buffer, the
    interpreter's final flush of it fails again, and the exit is the
    interpreter's flush-failure status instead. Only a non-zero exit is part
    of this contract for this case (observed on CPython 3.14.4: 3 unbuffered,
    120 buffered);
  * a write to stdout that fails, because the reader has closed it (a broken
    pipe) or the device is full (ENOSPC, as on /dev/full), is the
    interpreter's error, and D8 then exits non-zero, never 0, with no complete
    report delivered. The exact code depends on when the write fails and is
    not part of this contract, nor is the wording of the interpreter's message
    on stderr. Observed on CPython 3.14.4: 120 when only the interpreter's final
    flush of stdout fails (block-buffered, a pipe or a file, the default, with
    a report smaller than the buffer); 1 unbuffered (`python3 -u`), where the
    first line D8 prints fails; and 120 when, block-buffered, a write fails
    mid-run (a report larger than the buffer, 128 KiB on Python 3.14), because
    the final flush then fails again. Exit 120 on a failed final flush has
    been CPython behaviour since 3.6 (the `sys.exit` documentation). Python
    3.11, which CI runs, was not observed; its buffer size can differ, which
    changes only which of these cases a given report reaches;
  * `--self-test` exits 1 when one of its cases fails;
  * a usage error or `--self-test` (which reports its cases on stderr) may
    end with the interpreter's own status instead when stderr is absent (file
    descriptor 2 closed at startup) or cannot be written (the device is full,
    as on /dev/full). Observed on CPython 3.14.4: `--no-such-option` exits 120
    with stderr on /dev/full under stderr's default buffering (2 unbuffered,
    and 2 with no stderr), and `--self-test` with every case passing exits 120
    with stderr on /dev/full (1 unbuffered) and 1 with no stderr. A checked
    run and `--help` write nothing to stderr, and were observed to exit 0 in
    each of these cases;
  * a signal that terminates the interpreter ends D8 with that signal's
    status, as does a failure of the interpreter itself (it cannot start, or
    runs out of memory).
When there is nothing to report, D8 prints one machine-readable line and one
human line instead of a report (no BEGIN/END), and still exits 0:

    D8 NOT-FOUND today=<date> rc=0                       the path resolves to
                                                         nothing (no entry, a
                                                         dangling symlink, or a
                                                         component that is not
                                                         a directory)
    D8 REFUSED reason=unreadable today=<date> rc=0       the path cannot be read
    D8 REFUSED reason=not-utf8 today=<date> rc=0         the file is not UTF-8
    D8 REFUSED reason=bad-date today=<date> rc=0         a per-PR entry's date is
                                                         impossible (2026-02-30),
                                                         once or repeated, or is
                                                         not in ASCII digits

One malformed per-PR date refuses the whole report (`D8 REFUSED
reason=bad-date`), so no other due date is reported until that line is fixed.
This is deliberate (stricter is safer): a partial report would read as complete.

Only an open failing with ENOENT, or with ENOTDIR because a component of the
path is not a directory, is `D8 NOT-FOUND`; any other error opening or reading
the path, or a path that is not a regular file, is `D8 REFUSED
reason=unreadable`. The machine-readable lines carry neither the path nor any
error text; the human line after `D8 NOT-FOUND` or `D8 REFUSED` also carries
the path as given and, after `D8 REFUSED`, error text specific to the
interpreter and operating system (the system's error message, or the UTF-8
decoder's or the date parser's message). The path is the `--changelog` argument
exactly as given, not pathlib's normalized form. A character in the human line
that stdout's encoding cannot represent is written as a backslash escape, so
neither the path nor the error text can stop D8 exiting 0; every report line is
ASCII by construction.
Whatever stdout's encoding and error handler, every character in the human
line outside printable ASCII (0x20 to 0x7E) is written as a backslash escape
(`\\x0a`, `\\x85`, `\\u2026`, `\\udc85`) before the line is written, so the
human line is plain ASCII and no encoding sees any other character in it.
Escaping only the controls, U+2028, U+2029 and the surrogates was not
enough, because a non-ASCII character left unescaped can encode to a
byte that another encoding reads as a line break: cp1252 writes U+2026
as the byte 0x85, which ISO-8859-1 reads as a line break (NEL), and that
set left U+2026 unescaped. Surrogates are escaped because the
`surrogateescape` error handler writes a surrogate (a path byte that is
not UTF-8 decodes to one) back as that byte. Under an encoding that
writes ASCII as ASCII (UTF-8, ISO-8859-1 and cp1252 among them), read by a
reader that reads ASCII as ASCII, the human line is therefore exactly one line,
always begins `check-daily-changelog-rollup: `, and no path or error text can
make D8 print a line of the grammar above. An encoding that does not write
ASCII as ASCII (cp037, an EBCDIC code page, writes `e` as the byte 0x85; UTF-16
writes two bytes per character) changes every line D8 prints, the
machine-readable lines too. A backslash is printed as is: the human line is for
people, not for parsing. argparse's usage error on stderr is escaped the same
way, its message (which quotes an unknown argument) and the program name, so an
argument cannot make D8 print a line of the grammar above either.
D8 also opens the `--changelog` argument exactly as given: an empty argument
fails with ENOENT, and a regular file named with a trailing `/` or `/.` fails with
ENOTDIR, so each is `D8 NOT-FOUND`; only the revision lookup uses the
normalized form's directory and name.

Git failing, absent, timing out or printing bytes that do not decode refuses
only the revision: git's output is read as bytes, and the report runs with
rev=UNKNOWN.

Usage:
    python3 tools/check-daily-changelog-rollup.py
    python3 tools/check-daily-changelog-rollup.py --changelog path/to/CHANGELOG.md
    python3 tools/check-daily-changelog-rollup.py --self-test
"""

from __future__ import annotations

import argparse
import datetime
import errno
import hashlib
import io
import os
import re
import stat
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

CHANGELOG_PATH = "CHANGELOG.md"

# The checked revision, or this marker when it cannot be read (never a guess).
REV_UNKNOWN = "UNKNOWN"
REV_RE = re.compile(r"[0-9a-f]{40}")

# Seconds each git call may take before it counts as failed (round 5, claude N5).
GIT_TIMEOUT = 30

# The only open errors that mean the path resolves to nothing (round 5, codex
# E1; round 9, claude N5): ENOENT, which a dangling symlink also gives, and
# ENOTDIR, where a component of the path is not a directory, so no file can be
# at it. Every other error hides what may be there: a refusal.
ABSENT_ERRNOS = frozenset({errno.ENOENT, errno.ENOTDIR})

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


class Refusal(Exception):
    """Nothing can be reported: ``reason`` is the D8 REFUSED token."""

    def __init__(self, reason: str, detail: str) -> None:
        super().__init__(detail)
        self.reason = reason


def find_rollups_due(text: str, today: datetime.date) -> list[tuple[str, int]]:
    """Return [(date, per_pr_count), ...] for past dates with > 1 per-PR entry.

    A "past" date is any entry date strictly before ``today``. Roll-up entries
    (`PRs #A-#B`) are not counted. Result is sorted by date (oldest first).
    Raises Refusal("bad-date") for a per-PR entry whose date is not a real
    calendar date in ASCII digits (``\\d`` also matches other scripts' digits).
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
        date_str = m.group("date")
        try:
            if not date_str.isascii():
                raise ValueError("not in ASCII digits")
            datetime.date.fromisoformat(date_str)
        except ValueError as exc:
            raise Refusal(
                "bad-date", f"per-PR entry date {ascii(date_str)} is not a calendar date ({exc})"
            ) from None
        per_pr_by_date[date_str] += 1

    due: list[tuple[str, int]] = []
    for date_str, count in per_pr_by_date.items():
        if count <= 1:
            continue  # a lone entry is already effectively collapsed
        if datetime.date.fromisoformat(date_str) >= today:
            continue  # today (or, defensively, future): not yet due
        due.append((date_str, count))
    return sorted(due)


def read_changelog(path: str) -> bytes | None:
    """Return the bytes of the regular file at ``path``, or None when nothing is there.

    ``path`` is opened exactly as given, never normalized: pathlib turns ``""``
    into ``.`` and drops a trailing ``/`` or ``/.``, which hides the ENOENT or
    ENOTDIR the open of the given argument fails with (round 7, codex E1).

    Absence is decided by the open's own error (ABSENT_ERRNOS), never by a
    separate Path.is_file(), which reports an unsearchable parent or an
    over-long name as absent on one Python version and raises on another
    (round 5, codex E1). Raises Refusal("unreadable") for any other error and
    for a path that is not a regular file; the open does not wait on a FIFO.
    """
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0))
    except OSError as exc:
        if exc.errno in ABSENT_ERRNOS:
            return None
        raise Refusal("unreadable", f"cannot be read ({exc.strerror or exc})") from None
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise Refusal("unreadable", "cannot be read (not a regular file)")
        with open(fd, "rb", closefd=False) as stream:
            return stream.read()
    except OSError as exc:
        raise Refusal("unreadable", f"cannot be read ({exc.strerror or exc})") from None
    finally:
        os.close(fd)


def checked_revision(path: Path, data: bytes) -> str:
    """Return HEAD's commit when ``data`` is exactly that commit's blob for ``path``.

    HEAD is resolved once, to a commit; the blob is then read at that commit
    (``<rev>:./<name>``), never at ``HEAD`` again, so a HEAD that moves
    between the two calls cannot bind one commit to another's bytes (round 7).
    Anything else (no repository, git unavailable or failing, output that does
    not decode, an untracked or edited file, a non-SHA-1 object format) returns
    REV_UNKNOWN: the checked bytes are then not provably that revision's.
    Replacement objects are disabled and the graft file is empty, so
    ``<rev>:./<name>`` names the blob physically in that commit's tree (round
    3, codex E1).
    """
    env = {**os.environ, "GIT_NO_REPLACE_OBJECTS": "1", "GIT_GRAFT_FILE": os.devnull}

    def git(*args: str) -> str | None:
        # Bytes, decoded here: git's diagnostics may hold any bytes (round 3, codex E2).
        try:
            proc = subprocess.run(
                ["git", "--no-replace-objects", "-C", str(path.parent), *args],
                capture_output=True, env=env, stdin=subprocess.DEVNULL, timeout=GIT_TIMEOUT,
            )
            out = proc.stdout.decode("ascii").strip()
        except (OSError, UnicodeDecodeError, subprocess.TimeoutExpired):
            return None
        return out if proc.returncode == 0 else None

    rev = git("rev-parse", "--verify", "--quiet", "HEAD^{commit}")
    if not rev or not REV_RE.fullmatch(rev):
        return REV_UNKNOWN
    blob = git("rev-parse", "--verify", "--quiet", f"{rev}:./{path.name}")
    if blob != hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest():
        return REV_UNKNOWN
    return rev


def usable_stdout() -> bool:
    """False when there is no stdout a report can be written to.

    A process started with file descriptor 1 closed has ``sys.stdout`` None,
    and print then writes nothing: D8 exited 0 with no output (round 11,
    claude W3). A closed stream, or a descriptor fstat reports bad, is also
    unusable. A stream with no descriptor (a StringIO under test) is usable:
    its writes decide. fstat reads the descriptor's state and changes nothing.
    """
    stream = sys.stdout
    if stream is None or getattr(stream, "closed", False):
        return False
    try:
        fd = stream.fileno()
    except (AttributeError, io.UnsupportedOperation):
        return True
    except (OSError, ValueError):
        return False
    try:
        os.fstat(fd)
    except OSError:
        return False
    return True


# The exit status of a run refused for want of a usable stdout (round 11).
NO_STDOUT_EXIT = 3


def report(
    due: list[tuple[str, int]],
    stream=sys.stdout,
    *,
    rev: str = REV_UNKNOWN,
    today: datetime.date,
) -> int:
    """Print the BEGIN line, the advisory lines and the END line.

    ``today`` is required (round 14, claude W2): it is the date main() read
    once and checked against, so a run that crosses UTC midnight cannot print
    one date while it computed the due dates for another. Returns the number
    of dates flagged.
    """
    body: list[str] = []
    if not due:
        body.append(
            "OK: every past UTC date in CHANGELOG.md is either a single daily "
            "roll-up or a lone entry; no summarization outstanding."
        )
    for date_str, count in due:
        due_since = datetime.date.fromisoformat(date_str) + datetime.timedelta(days=1)
        body.append(
            f"D8 DUE id=D8-{date_str}@{rev[:12] if rev != REV_UNKNOWN else rev} "
            f"date={date_str} count={count} "
            f"due_since={due_since.isoformat()}T00:00:00Z"
        )
        body.append(
            f"DAILY SUMMARY DUE for {date_str}: {count} per-PR entries not yet "
            f"rolled up; the next PR should include the daily roll-up, run via "
            f"the coupled roll-up tool (rollup-changelog.py) in the private "
            f"maintainer repository, which writes the root roll-up and the "
            f"detailed-mirror sweep together (offload the run); a hand-made "
            f"root roll-up fails the CHANGELOG mirror header-parity gate"
        )
    frame = f"rev={rev} today={today.isoformat()} run={run_digest(rev, today, body)}"
    print(f"D8 BEGIN {frame}", file=stream)
    for line in body:
        print(line, file=stream)
    # rc is the exit status: 0 (advisory; the module docstring lists the
    # exceptions, none of them a result of D8's checking).
    print(f"D8 END {frame} due={len(due)} rc=0", file=stream)
    return len(due)


def run_digest(rev: str, today: datetime.date, body: list[str]) -> str:
    """The run identifier BEGIN and END carry (see the module docstring)."""
    text = f"rev={rev} today={today.isoformat()}\n" + "".join(f"{line}\n" for line in body)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# The ASCII characters outside printable ASCII: C0 controls (LF and CR among
# them) and DEL. plain() escapes these by this table and every non-ASCII
# character by backslashreplace. Escaping only controls, U+2028, U+2029 and
# surrogates (rounds 8 and 15) left U+2026, which a cp1252 stdout writes as
# the byte 0x85, NEL in ISO-8859-1 (round 16, codex ERROR).
LINE_SAFE = {c: f"\\x{c:02x}" for c in (*range(0x20), 0x7F)}


def plain(text: str) -> str:
    """``text`` with every character outside printable ASCII (0x20 to 0x7E)
    written as a backslash escape (``\\x0a``, ``\\x85``, ``\\u2026``, ``\\udc85``)."""
    return text.translate(LINE_SAFE).encode("ascii", "backslashreplace").decode("ascii")


def say(text: str) -> None:
    """Print a human line as exactly one line of printable ASCII (plain()).

    A path holding LF split the line, so a crafted path printed a complete
    forged BEGIN/OK/END report (round 8, claude W1), and a path holding
    U+2026 did the same through a cp1252 stdout read as ISO-8859-1 (round
    16): the line is escaped before stdout's encoding sees it. A path or
    error text stdout's encoding cannot represent raised UnicodeEncodeError:
    exit 1 after a machine line saying rc=0 (round 6, claude E1); an ASCII
    line leaves no such character.
    """
    print(plain(text))


class UsageParser(argparse.ArgumentParser):
    """argparse, with the program name and the usage error's message in plain().

    argparse wrote an unknown argument raw on stderr, so a crafted argument
    printed exact BEGIN and END lines with a valid digest (round 16, claude
    W2). The usage error still exits 2.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.prog = plain(self.prog)

    def error(self, message: str):
        self.print_usage(sys.stderr)
        self.exit(2, f"{self.prog}: error: {plain(message)}\n")


def refuse(token: str, today: datetime.date, shown: str, detail: str) -> None:
    """Print the machine-readable line and the human line for a run with no report.

    ``shown`` is the path exactly as given, not pathlib's normalized form
    (round 6, claude W2).
    """
    print(f"D8 {token} today={today.isoformat()} rc=0")
    say(f"check-daily-changelog-rollup: {shown}{detail} (advisory, exit 0).")


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
            self.assertEqual(report(due, stream=buf, today=TODAY), len(due))

        def test_report_message_names_coupled_rollup_tool(self):
            # Regression (2026-10-15): a root roll-up hand-made from this
            # message alone failed the mirror header-parity gate. The message
            # must route to the coupled tool and name the gate a hand edit
            # fails, without a private-sibling path token (over-exposure).
            import io

            buf = io.StringIO()
            report([("2026-07-25", 3)], stream=buf, today=TODAY)
            msg = buf.getvalue()
            lines = msg.splitlines()
            self.assertEqual(len(lines), 4, lines)
            self.assertTrue(lines[0].startswith("D8 BEGIN rev=UNKNOWN today=2026-07-26 run="))
            self.assertEqual(
                lines[1],
                "D8 DUE id=D8-2026-07-25@UNKNOWN date=2026-07-25 count=3 "
                "due_since=2026-07-26T00:00:00Z",
            )
            self.assertTrue(lines[2].startswith("DAILY SUMMARY DUE for 2026-07-25: 3 "))
            self.assertTrue(lines[3].startswith("D8 END rev=UNKNOWN today=2026-07-26 run="))
            self.assertTrue(lines[3].endswith(" due=1 rc=0"))
            self.assertIn("coupled roll-up tool (rollup-changelog.py)", msg)
            self.assertIn("private maintainer repository", msg)
            self.assertIn(
                "a hand-made root roll-up fails the CHANGELOG mirror "
                "header-parity gate",
                msg,
            )
            self.assertNotIn("library_private", msg)

        def test_report_frames_the_lines_with_one_run_digest(self):
            # BEGIN and END carry the same run digest of rev, today and the
            # lines between; another date or result gives another digest.
            import io

            def lines(due, today):
                buf = io.StringIO()
                report(due, stream=buf, today=today)
                return buf.getvalue().splitlines()

            first = lines([("2026-07-25", 3)], TODAY)
            run = run_digest(REV_UNKNOWN, TODAY, first[1:-1])
            self.assertEqual(first[0], f"D8 BEGIN rev=UNKNOWN today=2026-07-26 run={run}")
            self.assertEqual(first[-1], f"D8 END rev=UNKNOWN today=2026-07-26 run={run} due=1 rc=0")
            self.assertNotIn(f"run={run}", lines([], TODAY)[0])
            self.assertNotIn(f"run={run}", lines([("2026-07-25", 3)], datetime.date(2026, 7, 27))[-1])

        def test_bad_entry_date_is_refused(self):
            # An impossible date (once or repeated) or a date in non-ASCII
            # digits refuses the run rather than raising or being skipped.
            for date in ("2026-02-30", "2026-13-01", "٢٠٢٦-07-25"):
                for n in (1, 2):
                    with self.subTest(date=date, entries=n):
                        txt = "\n".join(entry(date, p) for p in range(1150, 1150 + n))
                        with self.assertRaises(Refusal) as caught:
                            find_rollups_due(txt, TODAY)
                        self.assertEqual(caught.exception.reason, "bad-date")

    suite = unittest.TestLoader().loadTestsFromTestCase(T)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str] | None = None) -> int:
    # A report nobody can read is not a pass (round 11, claude W3): refuse
    # before checking anything, with a non-zero exit. The check runs before
    # the parser is built (round 13, codex E1): Python 3.14's argparse asks
    # stdout whether to colour help when the parser and its options are
    # made, and a closed stream raised ValueError there (exit 1, a traceback).
    if not usable_stdout():
        if sys.stderr is not None:
            try:
                print(
                    "check-daily-changelog-rollup: no usable stdout; nothing checked "
                    f"(exit {NO_STDOUT_EXIT}).",
                    file=sys.stderr,
                )
            except (OSError, ValueError):
                pass
        return NO_STDOUT_EXIT

    ap = UsageParser(
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

    today = datetime.datetime.now(datetime.timezone.utc).date()
    # The open takes the argument exactly as given (round 7, codex E1, claude
    # W1); the normalized form serves only the revision lookup, which runs
    # only after that open found a regular file.
    path = Path(args.changelog)

    # Each refusal is a line and exit 0, never a traceback (round 3, codex E2).
    try:
        data = read_changelog(args.changelog)
        if data is None:
            refuse("NOT-FOUND", today, args.changelog, " not found; nothing to check")
            return 0
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise Refusal("not-utf8", f"is not UTF-8 ({exc.reason} at byte {exc.start})") from None
        due = find_rollups_due(text, today)
    except Refusal as exc:
        refuse(f"REFUSED reason={exc.reason}", today, args.changelog, f": {exc}; nothing checked")
        return 0
    report(due, rev=checked_revision(path, data), today=today)
    # Advisory only: findings are coupled roll-up run candidates, never a push blocker.
    return 0


if __name__ == "__main__":
    sys.exit(main())
