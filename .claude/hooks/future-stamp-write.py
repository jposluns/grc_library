#!/usr/bin/env python3
"""PreToolUse hook (Write|Edit|MultiEdit|Bash): deny writing a FUTURE-dated observed-time literal into a store.

THREAT MODEL. An ACCIDENTAL-DRIFT discipline guard: it catches the model composing times instead of reading
the clock and writing them into a store in its NORMAL record format. It is NOT an adversarial boundary: an
evasion that needs deliberately unusual construction (a variable, a glob, a literal built from parts, a
schedule word placed before the time) is a disclosed residual, not a defect. It fails OPEN on malformed input.

Fleet orchestrator operational guard (generic: no project name is hardcoded). Motivated by an orchestrator
composing timestamps from its own sense of time instead of reading the clock, drifting up to 4h40m ahead,
and persisting those invented times into its durable records (timestamp-from-clock; records-first). An
observed-time record (a heartbeat, a recorded-at) must come from the clock, so one dated in the future is a
composed value. A scheduled value (a deadline, a next run) is legitimately future and is allowed.

Store roots. env ORCH_STORE_ROOT (one or more absolute paths joined by os.pathsep) when set, REPLACING the
default; else any /opt/<project>/private/ directory. For Write/Edit/MultiEdit a relative file_path is
resolved against the payload cwd.

Write. Checked only when tool_input.file_path lies under a store root. The new content's lines are compared
with the existing file's lines as a MULTISET of whole lines: a new line identical to an existing line is an
unchanged carry-over and is exempt (as many times as it occurs there); every other line is checked whole.

Edit and MultiEdit. Checked only under a store root. The COMPLETE resulting file is reconstructed by applying
the edits in tool order to the existing file content (old_string replaced once, or everywhere with
replace_all; an empty old_string creates an empty or absent file), and every line of the result that is not
an unchanged carry-over from the original (the same line multiset diff) is checked WHOLE, so a fragment edit
that repurposes a line (renaming `deadline` to `heartbeat`, or changing only the time on a heartbeat) is
seen on the full resulting line, and a scheduling keyword immediately preceding the literal on that line
still exempts it. The existing file is opened non-blocking, must be a regular file, and at most 4 MiB is
read. When the WHOLE file was read (or it is absent) and an edit cannot apply (an old_string not found), the
call is allowed: the tool itself fails and writes nothing. When the file was NOT read whole (over the 4 MiB
cap, unreadable, or not a regular file), whole-line reconstruction is impossible, so each edit's new_string
lines (less lines identical to its old_string lines) are checked, and the call is denied only when that
fragment itself carries a future literal with no immediately preceding keyword; a time-only fragment (for
example `17:45` to `22:25`) in such a file is not caught (disclosed below). No shell expansion happens in
these tools, so every character is literal (a `$(...)` is text, not a substitution).

Bash. A SIMPLE lexical rule (no redirection, heredoc, or wrapper analysis; quoting is followed only to find
date substitutions): DENY when
the command text contains an explicit store path token (a /opt/<project>/private path, or an ORCH_STORE_ROOT
root, standing alone: not preceded by a path character and followed by `/`, whitespace, a quote, a shell
operator, or the end) AND a future-dated literal that is not inside a `$(date ...)` or backtick `date ...`
substitution (`date` optionally after `env`, VAR=value words, or /bin/ or /usr/bin/). Substitution spans are
found in ONE linear pass that follows shell quoting like the shell does: single quotes (and $'...' with its
backslash escapes) make everything literal, double quotes keep only `$(` and backticks active (a parenthesis
inside quotes is not a delimiter), and each substitution starts its own quoting context; an unmatched opener
or an unterminated quote starts no span, so the literals it would have covered are checked.

Literals and zones. YYYY-MM-DD[T or space]HH:MM(:SS(.fraction)?)? then an optional zone: Z (attached or after
one space); a numeric offset +HH, +HHMM, or +HH:MM, or with - (attached or after one space); or, after one
space, UTC, GMT, or a letter abbreviation of 2 to 6 capitals. This zone grammar and the scheduling keyword
list are duplicated verbatim in stamp-truth-stop.py (python3 -I forbids a sibling import); a self-test
asserts they are identical. Z, UTC, and GMT are UTC; an offset is applied as written; a letter abbreviation
must be the process local zone's abbreviation for that wall time (both DST abbreviations are tried; the
earlier instant is taken if both match); any other abbreviation is an unknown zone and that literal is
SKIPPED, never guessed. A literal with NO zone is read BOTH as UTC and as local time and counts as future only
if it is future under both readings. Each literal is converted in isolation in integer microseconds (an
overflowing or invalid literal is skipped without disabling the rest). A literal more than 60 seconds after
now is future.

Observed-time vs scheduled. A future literal is allowed when a scheduling keyword IMMEDIATELY precedes it on
its line (a whole line of the resulting file, or a line of the Bash command text): the keyword ends at most
SCHED_GAP_TOKENS (3) word tokens before the literal (a word token holds a letter or digit; `:` or `[` do not
count), as in "next_run: T", "due T", "deadline: T", "scheduled for T", "until T", "not before T", "by T".
Keywords (case-insensitive, matched at the start of a word, so a prefix like `expir` covers expires and
expiry): due, deadline, expir, until, next, scheduled, not before, not-before, eta, planned, "target date",
"target:", and `by ` (with its trailing space). A keyword after the literal, or further back, does not
exempt it.

Contract: allow = no stdout, exit 0; deny = the PreToolUse hookSpecificOutput permissionDecision "deny" JSON
on stdout, exit 0. Fail-OPEN (allow) on unparseable input or any internal error: a DISCIPLINE guard, not a
security boundary. Kill-switch: a pool worker, detected as env ORCH_WORKER=1 OR env ORCH_VERIFY_OWNER present
with any value, even empty (orch-verify exports the latter into its worker shells and never sets the former),
allows. Subagent calls are checked too (subagents apply store writes).

RESIDUAL COVERAGE (disclosed per disclose-guard-residuals). Only the ISO-like literal shape above is caught:
a compact sess-YYYYMMDDTHHMMSSZ id, an epoch number, a 12-hour or natural-language time, or a time split
across tokens is not. The keyword test is lexical: a keyword (in a word start, a path, or prose) within three
word tokens before a fabricated literal exempts it (for example "hb (next check) 2099-..."). The carry-over
test is a line multiset, not an alignment: a line that already existed elsewhere in the file is exempt
wherever it lands. Only the first 4 MiB of an existing file count: for a larger file a Write's carry-over
test sees only that prefix, and an Edit is checked on its fragment only, so a time-only fragment edit
(`17:45` to `22:25`) there is a MISS. Bash is lexical by design. FALSE POSITIVES: a command that only READS
or merely NAMES a store path while carrying a future literal is denied (for example `grep 2099-01-01T00:00Z
/opt/p/private/s.md`, a `cp -t /elsewhere` whose SOURCE is in the store, a quoted `>` argument, or a store
path in a comment); rephrase or split the command. MISSES: a store path reached through a variable, a glob,
`cd` (a relative path is never resolved), a symlink, a `..` or doubled-slash spelling, or a script or
program that writes internally; a future literal inside a `$(date ...)` span in a quoted heredoc body or a
comment (text the shell never runs); a literal built from parts; and a write via another tool
(NotebookEdit). A heredoc body is scanned for quotes like command text, so an apostrophe there can hide a
later `$(date ...)` span, which then fails toward denying. A wrong host clock is enforced faithfully.

Self-test: python3 -I -B future-stamp-write.py --self-test
"""

import bisect
import collections
import datetime
import json
import os
import re
import stat
import sys
import time

UTC = datetime.timezone.utc
US = 1_000_000
FUTURE_SLACK_US = 60 * US
EXISTING_MAX_BYTES = 4 << 20
MAX_REPORTED = 20
_EPOCH = datetime.datetime(1970, 1, 1)
_EPOCH_UTC = _EPOCH.replace(tzinfo=UTC)
_ONE_US = datetime.timedelta(microseconds=1)

# Duplicated verbatim in stamp-truth-stop.py; the self-test asserts the two copies are identical.
SCHED_KEYWORDS = ("due", "deadline", "expir", "until", "next", "scheduled", "not before", "not-before", "eta",
                  "planned", "target date", "target:", "by ")
SCHED_GAP_TOKENS = 3
TIME_GRAMMAR = r"(?<!\d)(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2})(?::(\d{2})(?:\.(\d{1,9}))?)?"
ZONE_GRAMMAR = r"(?:[ ]?(Z)|[ ]?([+-]\d{2}(?::?\d{2})?)|[ ](UTC|GMT|[A-Z]{2,6}))(?![A-Za-z0-9])"

_SCHED_RE = re.compile(r"(?<![a-z0-9])(?:" + "|".join(re.escape(k) for k in SCHED_KEYWORDS) + ")", re.IGNORECASE)
_TOKEN_RE = re.compile(r"\S+")
_WORDCH_RE = re.compile(r"[A-Za-z0-9]")
_STAMP_RE = re.compile(TIME_GRAMMAR + "(?:" + ZONE_GRAMMAR + r")?(?![\d:])")
_OPT_STORE_RE = re.compile(r"^/opt/[^/]+/private(?:/|$)")
_TOKEN_BEFORE = r"(?<![A-Za-z0-9_.~/-])"
_TOKEN_AFTER = r"(?![^/\s'\"`;|&<>()])"
_OPT_TOKEN_RE = re.compile(_TOKEN_BEFORE + r"/opt/[^/\s'\"`;|&<>()$]+/private" + _TOKEN_AFTER)
_DATE_CMD_RE = re.compile(r"[ \t]*(?:(?:(?:/usr)?/bin/)?env[ \t]+)?(?:[A-Za-z_][A-Za-z0-9_]*=[^ \t`()]*[ \t]+){0,4}"
                          r"(?:(?:/usr)?/bin/)?date(?![\w-])")
DATE_LOOKAHEAD = 256


# ---- store paths ----

def store_roots():
    env = os.environ.get("ORCH_STORE_ROOT")
    if not env:
        return None
    return [os.path.normpath(r) for r in env.split(os.pathsep) if r and os.path.isabs(r)]


def under_store(path, cwd=None):
    if not isinstance(path, str) or not path:
        return False
    if not os.path.isabs(path):
        if not cwd:
            return False
        path = os.path.join(cwd, path)
    p = os.path.normpath(path)
    roots = store_roots()
    if roots is not None:
        return any(p == r or p.startswith(r.rstrip("/") + "/") for r in roots)
    return bool(_OPT_STORE_RE.match(p))


def names_store_path(cmd):
    """True when the command text contains an explicit store path token (lexical; see the docstring)."""
    roots = store_roots()
    if roots is None:
        return _OPT_TOKEN_RE.search(cmd) is not None
    return any(re.search(_TOKEN_BEFORE + re.escape(r.rstrip("/") or "/") + _TOKEN_AFTER, cmd) for r in roots)


# ---- literals ----

def _naive_us(y, mo, d, hh, mi, ss, us):
    return (datetime.datetime(y, mo, d, hh, mi, ss, us) - _EPOCH) // _ONE_US


def _local_us(y, mo, d, hh, mi, ss, abbr=None):
    """Epoch us for a local wall time; with `abbr`, only a reading whose zone abbreviation matches."""
    found = []
    for isdst in (0, 1):  # explicit isdst: deterministic, independent of earlier mktime calls
        try:
            ts = time.mktime((y, mo, d, hh, mi, ss, 0, 0, isdst))
            lt = time.localtime(ts)
        except (OverflowError, ValueError, OSError):
            continue
        if (lt.tm_year, lt.tm_mon, lt.tm_mday, lt.tm_hour, lt.tm_min, lt.tm_sec) != (y, mo, d, hh, mi, ss):
            continue
        if abbr is None or lt.tm_zone == abbr:
            found.append(int(ts))
    return min(found) * US if found else None


def literal_us(m):
    """Earliest plausible epoch us for a matched literal, or None (invalid, overflow, or unknown zone)."""
    try:
        y, mo, d, hh, mi = (int(m.group(i)) for i in range(1, 6))
        ss = int(m.group(6) or 0)
        us = int(((m.group(7) or "") + "000000")[:6])
        z, off, abbr = m.group(8), m.group(9), m.group(10)
        naive = _naive_us(y, mo, d, hh, mi, ss, us)
        if z or abbr in ("UTC", "GMT"):
            return naive
        if off:
            digits = off[1:].replace(":", "")
            hours, mins = int(digits[:2]), int(digits[2:] or 0)
            if hours > 18 or mins > 59:
                return None
            delta = (hours * 3600 + mins * 60) * US
            return naive - delta if off[0] == "+" else naive + delta
        loc = _local_us(y, mo, d, hh, mi, ss, abbr)
        if abbr:
            return None if loc is None else loc + us
        return None if loc is None else min(naive, loc + us)
    except (OverflowError, ValueError, OSError, TypeError):
        return None


def sched_exempter(line):
    """A predicate pos -> True when a scheduling keyword ends at most SCHED_GAP_TOKENS word tokens before
    position `pos` of `line` (a word token holds a letter or digit; punctuation-only tokens such as `:` or `[`,
    and the token containing `pos`, are not counted). Linear: keyword ends and tokens are found once per line.
    Duplicated verbatim in the sibling hook; the self-test asserts the two copies are identical."""
    ends = [k.end() for k in _SCHED_RE.finditer(line)]
    if not ends:
        return lambda pos: False
    toks = [(t.start(), t.end()) for t in _TOKEN_RE.finditer(line) if _WORDCH_RE.search(t.group())]
    starts, tends = [s for s, _ in toks], [e for _, e in toks]

    def exempt(pos):
        k = bisect.bisect_right(ends, pos) - 1
        if k < 0:
            return False
        between = bisect.bisect_right(tends, pos) - bisect.bisect_left(starts, ends[k])
        return between <= SCHED_GAP_TOKENS
    return exempt


def future_on_line(line, now_us, base=0, in_subst=None, cache=None):
    """Future literals on one line not immediately preceded by a scheduling keyword. `in_subst(pos)` is true
    for a literal starting at absolute position base+pos that lies inside a date substitution; `cache` maps
    a literal to its converted value so a repeated literal is converted once."""
    found, seen, sched = [], set(), None
    cache = {} if cache is None else cache
    for m in _STAMP_RE.finditer(line):
        lit = m.group(0)
        if lit in seen or (in_subst is not None and in_subst(base + m.start())):
            continue
        if lit not in cache:
            cache[lit] = literal_us(m)
        got = cache[lit]
        if got is None or got - now_us <= FUTURE_SLACK_US:
            continue
        if sched is None:
            sched = sched_exempter(line)
        if not sched(m.start()):
            seen.add(lit)
            found.append(lit)
    return found


def future_in_changed_lines(new, old, now_us):
    """Future observed-time literals on whole lines of `new` that are not unchanged carry-overs from `old`."""
    carry = collections.Counter((old or "").splitlines())
    bad, seen, cache = [], set(), {}
    for line in (new or "").splitlines():
        if carry[line] > 0:
            carry[line] -= 1
            continue
        for lit in future_on_line(line, now_us, cache=cache):
            if lit not in seen:
                seen.add(lit)
                bad.append(lit)
    return bad


def read_existing(path, limit):
    """(text, whole): the text of at most `limit` bytes of a REGULAR file, and whether that is the WHOLE file.
    An absent file is ("", True); a file over `limit`, unreadable, or not regular (FIFO, device) has whole
    False (with "" for the last two)."""
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | getattr(os, "O_NOCTTY", 0) | getattr(os, "O_CLOEXEC", 0))
    except FileNotFoundError:
        return "", True
    except (OSError, TypeError, ValueError):
        return "", False
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            return "", False
        chunks, got = [], 0
        while got <= limit:
            b = os.read(fd, min(1 << 16, limit + 1 - got))
            if not b:
                break
            chunks.append(b)
            got += len(b)
        data = b"".join(chunks)
        return data[:limit].decode("utf-8", "replace"), got <= limit
    except OSError:
        return "", False
    finally:
        os.close(fd)


def apply_edits(original, edits):
    """The file text after applying [(old, new, replace_all)] in order, or None when an edit cannot apply."""
    text = original
    for old, new, every in edits:
        if old == "":
            if text != "":
                return None
            text = new
        elif old not in text:
            return None
        else:
            text = text.replace(old, new) if every else text.replace(old, new, 1)
    return text


# ---- shell (lexical only) ----

def date_spans(cmd):
    """Sorted, merged [start, end) spans of `$(date ...)` and backtick `date ...` substitutions. ONE linear,
    quote-aware pass: each frame on the stack (the top level, a `$(`, a plain `(`, or a backtick) keeps its own
    quote state; inside single quotes (or $'...', which honours backslash escapes) nothing is special; inside
    double quotes only `$(` and backticks open frames and a parenthesis is literal. A span is recorded only
    when its frame closes, so an unmatched opener or an unterminated quote starts no span. The `date` test
    looks ahead a bounded DATE_LOOKAHEAD characters."""
    def is_date(j):
        return _DATE_CMD_RE.match(cmd[j:j + DATE_LOOKAHEAD]) is not None

    # frame: [kind, start, dated, quote]; kind in "top", "$(", "(", "`"; quote in None, "'", "$'", '"'
    spans, stack, i, n = [], [["top", 0, False, None]], 0, len(cmd)
    while i < n:
        c, top = cmd[i], stack[-1]
        q = top[3]
        if q == "'":
            if c == "'":
                top[3] = None
            i += 1
            continue
        if q == "$'":
            if c == "\\":
                i += 2
                continue
            if c == "'":
                top[3] = None
            i += 1
            continue
        if c == "\\":
            i += 2
            continue
        if c == "$" and cmd.startswith("$(", i):
            stack.append(["$(", i, is_date(i + 2), None])
            i += 2
            continue
        if c == "`":
            if top[0] == "`":
                stack.pop()
                if top[2]:
                    spans.append((top[1], i + 1))
            else:
                stack.append(["`", i, is_date(i + 1), None])
            i += 1
            continue
        if q == '"':
            if c == '"':
                top[3] = None
        elif c == "'":
            top[3] = "'"
        elif c == '"':
            top[3] = '"'
        elif c == "$" and cmd.startswith("$'", i):
            top[3] = "$'"
            i += 2
            continue
        elif c == "(":
            stack.append(["(", i, False, None])
        elif c == ")" and top[0] in ("$(", "("):
            stack.pop()
            if top[2]:
                spans.append((top[1], i + 1))
        i += 1
    spans.sort()
    merged = []
    for s, e in spans:
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return merged


def bash_future(cmd, now_us):
    """Future observed-time literals in a Bash command that names a store path (else [])."""
    if not names_store_path(cmd):
        return []
    spans = date_spans(cmd)
    starts = [s for s, _ in spans]

    def in_subst(pos):
        k = bisect.bisect_right(starts, pos) - 1
        return k >= 0 and pos < spans[k][1]

    bad, seen, cache, base = [], set(), {}, 0
    for line in cmd.split("\n"):
        for lit in future_on_line(line, now_us, base, in_subst, cache):
            if lit not in seen:
                seen.add(lit)
                bad.append(lit)
        base += len(line) + 1
    return bad


def _s(value):
    return value if isinstance(value, str) else ""


def evaluate(payload, now):
    """Return a list of offending future literals (empty = allow). `now` is an aware datetime."""
    now_us = (now - _EPOCH_UTC) // _ONE_US
    tool = payload.get("tool_name")
    ti = payload.get("tool_input") or {}
    if not isinstance(ti, dict):
        return []
    cwd = payload.get("cwd") if isinstance(payload.get("cwd"), str) else None
    if tool in ("Write", "Edit", "MultiEdit"):
        fp = ti.get("file_path")
        if not under_store(fp, cwd):
            return []
        if not os.path.isabs(fp):
            fp = os.path.join(cwd, fp)
        original, whole = read_existing(fp, EXISTING_MAX_BYTES)
        if tool == "Write":
            return future_in_changed_lines(_s(ti.get("content")), original, now_us)
        if tool == "Edit":
            edits = [(_s(ti.get("old_string")), _s(ti.get("new_string")), ti.get("replace_all") is True)]
        else:
            edits = [(_s(e.get("old_string")), _s(e.get("new_string")), e.get("replace_all") is True)
                     for e in (ti.get("edits") or []) if isinstance(e, dict)]
        if whole:
            result = apply_edits(original, edits)
            # an edit that cannot apply to the WHOLE file makes the tool itself fail: nothing is written
            return [] if result is None else future_in_changed_lines(result, original, now_us)
        # not read whole (over the cap, unreadable, not regular): no reconstruction is possible, so each
        # fragment is checked on its own lines; a time-only fragment here is a disclosed miss
        bad, seen = [], set()
        for old, new, _every in edits:
            for lit in future_in_changed_lines(new, old, now_us):
                if lit not in seen:
                    seen.add(lit)
                    bad.append(lit)
        return bad
    if tool == "Bash":
        cmd = ti.get("command")
        return bash_future(cmd, now_us) if isinstance(cmd, str) else []
    return []


def _deny(bad, now):
    local = now.astimezone()
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "Blocked: this write to a durable store carries observed-time literal(s) dated in the FUTURE: "
                + ", ".join(repr(b) for b in bad[:MAX_REPORTED])
                + (f" and {len(bad) - MAX_REPORTED} more" if len(bad) > MAX_REPORTED else "")
                + f". The real clock now reads {now.strftime('%Y-%m-%dT%H:%M:%SZ')} "
                f"({local.strftime('%Y-%m-%d %H:%M:%S')} {local.tzname()}). A record timestamp is read from the "
                "clock, never composed: use $(date -u +%Y-%m-%dT%H:%M:%SZ) in a shell write, or run `date -u` and "
                "copy its output. A genuinely scheduled value is allowed when a schedule word immediately precedes "
                "it (due, deadline, expires, until, next run, scheduled for, not before, eta, planned, target date, "
                "by). A Bash command "
                "is checked lexically: any command naming a store path with a future literal outside a "
                "$(date ...) substitution is denied, even one that only reads; split or rephrase it."
            ),
        }
    }))
    return 0


def _is_worker(env=None):
    """True for an orch-verify pool worker: ORCH_WORKER=1, or ORCH_VERIFY_OWNER present (any value, even empty).
    Kept identical across the fleet hooks (python3 -I forbids a sibling import)."""
    env = os.environ if env is None else env
    return env.get("ORCH_WORKER") == "1" or "ORCH_VERIFY_OWNER" in env


def main(argv):
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    if _is_worker():
        return 0
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            return 0
        now = datetime.datetime.now(UTC)
        bad = evaluate(payload, now)
    except Exception:
        return 0  # fail-open
    if bad:
        return _deny(bad, now)
    return 0


def _self_test():
    import importlib.util
    import inspect
    import io
    import shutil
    import subprocess
    import tempfile
    import unittest

    class T(unittest.TestCase):
        def setUp(self):
            self._tz = os.environ.get("TZ")
            self._root = os.environ.pop("ORCH_STORE_ROOT", None)
            os.environ["TZ"] = "EST5EDT,M3.2.0,M11.1.0"  # pinned zone, no tzdata needed
            time.tzset()
            base = "/dev/shm" if os.path.isdir("/dev/shm") else None
            self.tmp = tempfile.mkdtemp(prefix="clk.", dir=base)
            self.now = datetime.datetime(2026, 9, 23, 17, 45, 0, tzinfo=UTC)
            self.store = "/opt/proj/private/session-state.md"

        def tearDown(self):
            shutil.rmtree(self.tmp, ignore_errors=True)
            for k, v in (("TZ", self._tz), ("ORCH_STORE_ROOT", self._root)):
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
            time.tzset()

        def ev(self, tool, cwd="/opt/proj/guardrails", **ti):
            return evaluate({"tool_name": tool, "tool_input": ti, "cwd": cwd}, self.now)

        def store_file(self, text):
            fp = os.path.join(self.tmp, "state.md")
            with open(fp, "w") as f:
                f.write(text)
            os.environ["ORCH_STORE_ROOT"] = self.tmp
            return fp

        # -- Write / Edit / MultiEdit --
        def test_future_utc_literal_into_store_denied(self):
            self.assertEqual(self.ev("Write", file_path=self.store, content="hb: 2026-09-23T22:25:00Z"),
                             ["2026-09-23T22:25:00Z"])

        def test_future_local_literal_edit_denied(self):
            fp = self.store_file("a\n")
            self.assertTrue(self.ev("Edit", file_path=fp, old_string="a", new_string="[2026-09-23 14:10 EDT]"))

        def test_multiedit_future_denied(self):
            fp = self.store_file("x\ny\n")
            self.assertTrue(self.ev("MultiEdit", file_path=fp, edits=[{"old_string": "x", "new_string": "ok"},
                                                                      {"old_string": "y", "new_string": "at 2026-09-24T01:00Z"}]))

        def test_past_literal_passes(self):
            self.assertEqual(self.ev("Write", file_path=self.store, content="2026-09-23T17:44:30Z 2026-09-01 10:00"), [])

        def test_within_60s_slack_passes(self):
            self.assertEqual(self.ev("Edit", file_path=self.store, old_string="", new_string="2026-09-23T17:45:50Z"), [])

        def test_non_store_path_passes(self):
            self.assertEqual(self.ev("Write", file_path="/opt/proj/guardrails/x.md", content="2099-01-01T00:00Z"), [])

        def test_write_substitution_text_is_literal(self):
            self.assertEqual(self.ev("Write", file_path=self.store, content="$(echo 2099-01-01T00:00Z)"),
                             ["2099-01-01T00:00Z"])
            self.assertTrue(self.ev("Write", file_path=self.store, content="$(date -d 2099-01-01T00:00Z)"))

        def test_date_only_passes(self):
            self.assertEqual(self.ev("Write", file_path=self.store, content="due 2099-12-31, review 2027-01-01"), [])

        def test_offset_literal_resolved(self):
            self.assertEqual(self.ev("Write", file_path=self.store, content="2026-09-23T19:00+02:00"), [])
            self.assertTrue(self.ev("Write", file_path=self.store, content="2026-09-23T23:00+02:00"))

        def test_spaced_numeric_zone(self):
            # finding (codex r2): a space-separated numeric zone was dropped and the literal read as naive
            os.environ["TZ"] = "UTC0"
            time.tzset()
            self.assertEqual(self.ev("Write", file_path=self.store, content="[2026-09-23 22:45 +05]"), [])
            self.assertEqual(self.ev("Write", file_path=self.store, content="[2026-09-23 13:45 -09]"),
                             ["2026-09-23 13:45 -09"])

        def test_zone_abbreviations(self):
            self.assertEqual(self.ev("Write", file_path=self.store, content="[2026-09-23 17:45 UTC]"), [])
            self.assertTrue(self.ev("Write", file_path=self.store, content="[2026-09-23 22:25 UTC]"))
            os.environ["TZ"] = "JST-9"
            time.tzset()
            self.assertEqual(self.ev("Write", file_path=self.store, content="[2026-09-24 02:45 JST]"), [])
            self.assertTrue(self.ev("Write", file_path=self.store, content="[2026-09-24 07:25 JST]"))

        def test_unknown_zone_skipped(self):
            self.assertEqual(self.ev("Write", file_path=self.store, content="[2099-01-01 10:00 XYZT]"), [])

        def test_naive_literal_future_under_both_readings(self):
            self.assertTrue(self.ev("Write", file_path=self.store, content="hb: 2026-09-23 18:25"))
            self.assertEqual(self.ev("Write", file_path=self.store, content="hb: 2026-09-23 17:30"), [])

        def test_dst_fold_deterministic(self):
            now = datetime.datetime(2026, 11, 1, 5, 45, tzinfo=UTC)
            ev = lambda c: evaluate({"tool_name": "Write", "tool_input": {"file_path": self.store, "content": c},
                                     "cwd": "/"}, now)
            self.assertEqual(ev("hb [2026-11-01 01:30 EDT]"), [])
            self.assertTrue(ev("hb [2026-11-01 01:30 EST]"))

        def test_overflow_literal_isolated(self):
            self.assertEqual(self.ev("Write", file_path=self.store,
                                     content="0001-01-01T00:00+01:00\n9999-12-31T23:59-01:00 heartbeat 2099-01-01T00:00Z"),
                             ["9999-12-31T23:59-01:00", "2099-01-01T00:00Z"])  # integer arithmetic: no overflow

        def test_scheduled_keyword_allowed(self):
            for line in ("next_run: 2099-01-01T09:30:00Z", "Deadline 2099-01-01 09:00 UTC", "expires 2099-01-01T00:00Z",
                         "not-before: 2099-01-01T00:00Z", "ETA 2099-01-01T00:00Z", "done by 2099-01-01T00:00Z"):
                self.assertEqual(self.ev("Write", file_path=self.store, content=line), [], line)
            for line in ("metadata: 2099-01-01T00:00Z", "beta 2099-01-01T00:00Z", "Last-heartbeat: 2099-01-01T00:00Z"):
                self.assertTrue(self.ev("Write", file_path=self.store, content=line), line)

        def test_unchanged_line_carry_over_allowed(self):
            fp = self.store_file("hb: 2099-01-01T00:00Z\nother\n")
            self.assertEqual(self.ev("Write", file_path=fp, content="hb: 2099-01-01T00:00Z\nother\nnew line\n"), [])
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="other", new_string="changed"), [])

        def test_repurposed_timestamp_on_changed_line_denied(self):
            fp = self.store_file("deadline: 2099-01-01T00:00Z\n")
            self.assertTrue(self.ev("Write", file_path=fp, content="Last-heartbeat: 2099-01-01T00:00Z\n"))
            fp = self.store_file("hb: 2099-01-01T00:00Z\n")
            self.assertTrue(self.ev("Write", file_path=fp, content="hb: 2099-01-01T00:00Z\nhb: 2099-01-01T00:00Z\n"))

        def test_edit_fragments_reconstructed_on_whole_lines(self):
            # finding (codex r2): Edit checked the replacement fragment, not the changed file line
            fp = self.store_file("deadline: 2099-01-01T00:00Z\nheartbeat: 2026-09-23T17:45Z\n"
                                 "next_run: 2099-03-01T00:00Z\n")
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="deadline", new_string="heartbeat"),
                             ["2099-01-01T00:00Z"])
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="17:45", new_string="22:25"),
                             ["2026-09-23T22:25Z"])
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="2099-03-01", new_string="2099-04-01"), [])
            self.assertEqual(self.ev("MultiEdit", file_path=fp, edits=[
                {"old_string": "heartbeat: 2026-09-23T17:45Z", "new_string": "heartbeat: X"},
                {"old_string": "X", "new_string": "2026-09-23T23:00Z"}]), ["2026-09-23T23:00Z"])
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="99-0", new_string="99-1", replace_all=True), [])
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="T17:45Z", new_string="T17:45Z\nhb: 2099-02-02T00:00Z",
                                     replace_all=True), ["2099-02-02T00:00Z"])

        def test_edit_old_string_absent_on_whole_file_allowed(self):
            # finding (gemini r3 M2): a non-applying edit fell back to naked fragments (false deny); on a file
            # read whole the tool itself fails, so the call is allowed
            fp = self.store_file("a\n")
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="zzz", new_string="hb 2099-01-01T00:00Z"), [])
            fp = self.store_file("deadline: 2026-09-23T17:45Z\n")
            self.assertEqual(self.ev("MultiEdit", file_path=fp, edits=[
                {"old_string": "2026-09-23T17:45Z", "new_string": "2099-01-01T00:00Z"},
                {"old_string": "nope", "new_string": "y"}]), [])
            self.assertEqual(self.ev("Edit", file_path=os.path.join(self.tmp, "absent.md"), old_string="x",
                                     new_string="hb 2099-01-01T00:00Z"), [])

        def test_edit_beyond_read_cap_checks_fragment(self):
            # finding (codex r3 m): past the cap the hook cannot reconstruct; the fragment is checked on its own
            fp = self.store_file("x\n" * (EXISTING_MAX_BYTES // 2) + "hb: 2026-09-23T17:45Z\n")
            self.assertEqual(read_existing(fp, EXISTING_MAX_BYTES)[1], False)
            self.assertTrue(self.ev("Edit", file_path=fp, old_string="hb: 2026-09-23T17:45Z",
                                    new_string="hb: 2026-09-23T22:25Z"))
            self.assertTrue(self.ev("Edit", file_path=fp, old_string="zzz", new_string="hb: 2099-01-01T00:00Z"))
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="17:45", new_string="22:25"), [])  # disclosed
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="x", new_string="next run 2099-01-01T00:00Z"), [])
            fp2 = self.store_file("x\n" * (EXISTING_MAX_BYTES // 2 - 1))
            self.assertEqual(read_existing(fp2, EXISTING_MAX_BYTES)[1], True)

        def test_fifo_existing_content_does_not_block(self):
            fifo = os.path.join(self.tmp, "fifo")
            os.mkfifo(fifo)
            code = ("import importlib.util as u;s=u.spec_from_file_location('m',%r);m=u.module_from_spec(s);"
                    "s.loader.exec_module(m);print(repr(m.read_existing(%r, 10)))" % (os.path.abspath(__file__), fifo))
            r = subprocess.run([sys.executable, "-I", "-B", "-c", code], capture_output=True, text=True, timeout=5)
            self.assertEqual(r.stdout.strip(), "('', False)")

        def test_store_root_env_override(self):
            os.environ["ORCH_STORE_ROOT"] = self.tmp
            self.assertEqual(self.ev("Write", file_path=self.store, content="2099-01-01T00:00Z"), [])
            self.assertTrue(self.ev("Write", file_path=os.path.join(self.tmp, "a.md"), content="2099-01-01T00:00Z"))
            self.assertTrue(self.ev("Bash", command=f"echo 2099-01-01T00:00Z >> {self.tmp}/a.md"))
            self.assertEqual(self.ev("Bash", command=f"echo 2099-01-01T00:00Z >> {self.tmp}x/a.md"), [])

        def test_relative_path_under_store_cwd(self):
            r = evaluate({"tool_name": "Write", "cwd": "/opt/proj/private",
                          "tool_input": {"file_path": "notes.md", "content": "2099-01-01T00:00Z"}}, self.now)
            self.assertTrue(r)

        # -- Bash: the simple lexical rule --
        def test_bash_future_into_store_denied(self):
            for cmd in ("echo 'Last-heartbeat-UTC: 2026-09-23T19:00:00Z' >> /opt/proj/private/session-state.md",
                        "printf 'hb 2099-01-01T00:00Z' | tee -a /opt/proj/private/a.md",
                        "sed -i 's/x/2099-01-01T00:00Z/' /opt/proj/private/a.md",
                        "cp /dev/shm/2099-01-01T00:00Z /opt/proj/private/",
                        "printf '%s' '$(echo 2099-01-01T00:00Z)' > /opt/proj/private/log.md"):
                self.assertTrue(self.ev("Bash", command=cmd), cmd)

        def test_bash_parse_evasions_now_denied(self):
            # findings (codex/gemini r2): comment heredoc, wrapper options, and $(echo ...) evaded parsing
            for cmd in ("# <<EOF\nprintf '%s\\n' 'hb: 2099-01-01T00:00Z' > /opt/proj/private/s.md",
                        "printf '%s\\n' '<<EOF'\nprintf 'hb: 2099-01-01T00:00Z' > /opt/proj/private/s.md",
                        "echo 2099-01-01T00:00Z | env -i tee /opt/proj/private/s.md",
                        "echo 2099-01-01T00:00Z | sudo -n tee /opt/proj/private/s.md",
                        "echo $(echo 2099-01-01T00:00Z) > /opt/proj/private/a.md",
                        "echo \"hb: `echo 2099-01-01T00:00Z`\" > '/opt/proj/private/a.md'",
                        "dd of=/opt/proj/private/a.md <<< 2099-01-01T00:00Z"):
                self.assertTrue(self.ev("Bash", command=cmd), cmd)

        def test_bash_documented_false_positives(self):
            # documented: a command that names a store path and carries a future literal is denied lexically
            for cmd in ("printf '%s\\n' '>' /opt/proj/private/s.md 2099-01-01T00:00Z",
                        "cp -t /dev/shm/ /opt/proj/private/report-2099-01-01T00:00Z.md",
                        "grep 2099-01-01T00:00Z /opt/proj/private/s.md",
                        "echo 'hb 2099-01-01T00:00Z' >> /opt/proj/guardrails/n.md # cf /opt/proj/private/old.md"):
                self.assertTrue(self.ev("Bash", command=cmd), cmd)

        def test_bash_date_substitution_passes(self):
            for cmd in ('echo "hb: $(date -u +%Y-%m-%dT%H:%M:%SZ) $(date -d \'2099-01-01 10:00\')" >> '
                        "/opt/proj/private/s.md",
                        "echo `date -d '2099-01-01 10:00'` >> /opt/proj/private/s.md",
                        "echo \"$(TZ=UTC date -d '2099-01-01T00:00Z' +%s)\" > /opt/proj/private/s.md",
                        "echo $( /bin/date -d \"$(printf x) 2099-01-01T00:00Z\" ) > /opt/proj/private/s.md"):
                self.assertEqual(self.ev("Bash", command=cmd), [], cmd)
            self.assertTrue(self.ev("Bash", command="echo $(date -u) 2099-01-01T00:00Z > /opt/proj/private/s.md"))
            self.assertTrue(self.ev("Bash", command="echo $(date -u 2099-01-01T00:00Z > /opt/proj/private/s.md"))

        def test_bash_without_store_token_allowed(self):
            for cwd, cmd in (("/opt/proj/private", "printf '%s' 2099-01-01T00:00Z > /dev/shm/example"),
                             ("/opt/proj/private", "echo 2099-01-01T00:00Z > notes.md"),  # documented miss (cwd)
                             ("/", "echo 2099-01-01T00:00Z > /opt/proj/private.bak/x"),
                             ("/", "echo 2099-01-01T00:00Z > /x/opt/proj/private/y"),
                             ("/", "cat /opt/proj/private/s.md; echo past 2026-09-01T00:00Z > /dev/shm/x")):
                self.assertEqual(self.ev("Bash", cwd=cwd, command=cmd), [], cmd)

        def test_bash_heredoc_is_plain_text(self):
            self.assertTrue(self.ev("Bash", command="cat <<'EOF' >> /opt/proj/private/s.md\nhb: 2099-01-01T00:00Z\nEOF"))
            self.assertEqual(self.ev("Bash", command="cat <<EOF >> /opt/proj/private/s.md\nhb: $(date -u)\nEOF"), [])
            self.assertEqual(self.ev("Bash", command="cat <<'EOF' > /dev/shm/x\nhb: 2099-01-01T00:00Z\nEOF"), [])
            self.assertTrue(self.ev("Bash", command="echo 'unterminated 2099-01-01T00:00Z > /opt/proj/private/s"))

        def test_bash_scheduled_keyword_allowed(self):
            self.assertEqual(self.ev("Bash", command="echo 'next_run: 2099-01-01T09:30Z' >> /opt/proj/private/s.md"),
                             [])

        def test_bash_scan_is_linear(self):
            # finding (codex r2): unmatched $( openers rescanned the suffix quadratically
            code = ("import importlib.util as u,datetime;s=u.spec_from_file_location('m',%r);m=u.module_from_spec(s);"
                    "s.loader.exec_module(m);n=datetime.datetime(2026,9,23,17,45,tzinfo=datetime.timezone.utc);"
                    "c=': > /opt/proj/private/s # '+'$('*500000+'`'*100001+'$(A=B'*50000+' 2099-01-01T00:00Z';"
                    "print(m.evaluate({'tool_name':'Bash','tool_input':{'command':c}},n))" % os.path.abspath(__file__))
            r = subprocess.run([sys.executable, "-I", "-B", "-c", code], capture_output=True, text=True, timeout=5)
            self.assertIn("2099-01-01T00:00Z", r.stdout)

        def test_main_deny_shape_and_fail_open(self):
            payload = json.dumps({"tool_name": "Write", "tool_input": {"file_path": self.store,
                                                                       "content": "2099-01-01T00:00:00Z"}})
            for stdin_text, env, want_deny in ((payload, {}, True), ("not json", {}, False),
                                               (payload, {"ORCH_WORKER": "1"}, False),
                                               (payload, {"ORCH_VERIFY_OWNER": "guardrails"}, False),
                                               (payload, {"ORCH_VERIFY_OWNER": ""}, False)):
                old_in, old_out, old_env = sys.stdin, sys.stdout, dict(os.environ)
                sys.stdin, sys.stdout = io.StringIO(stdin_text), io.StringIO()
                try:
                    os.environ.pop("ORCH_WORKER", None)
                    os.environ.pop("ORCH_VERIFY_OWNER", None)
                    os.environ.update(env)
                    rc = main(["future-stamp-write.py"])
                    out = sys.stdout.getvalue()
                finally:
                    sys.stdin, sys.stdout = old_in, old_out
                    os.environ.clear()
                    os.environ.update(old_env)
                self.assertEqual(rc, 0)
                if want_deny:
                    h = json.loads(out)["hookSpecificOutput"]
                    self.assertEqual((h["hookEventName"], h["permissionDecision"]), ("PreToolUse", "deny"))
                    self.assertIn("2099-01-01T00:00:00Z", h["permissionDecisionReason"])
                else:
                    self.assertEqual(out, "")

        def test_shared_grammar_identical_to_sibling(self):
            sib = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stamp-truth-stop.py")
            spec = importlib.util.spec_from_file_location("sts_sibling", sib)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            self.assertEqual(mod.SCHED_KEYWORDS, SCHED_KEYWORDS)
            self.assertEqual(mod.SCHED_GAP_TOKENS, SCHED_GAP_TOKENS)
            self.assertEqual((mod.TIME_GRAMMAR, mod.ZONE_GRAMMAR), (TIME_GRAMMAR, ZONE_GRAMMAR))
            self.assertEqual((mod._SCHED_RE.pattern, mod._SCHED_RE.flags), (_SCHED_RE.pattern, _SCHED_RE.flags))
            self.assertEqual((mod._TOKEN_RE.pattern, mod._WORDCH_RE.pattern), (_TOKEN_RE.pattern, _WORDCH_RE.pattern))
            self.assertEqual(inspect.getsource(mod.sched_exempter), inspect.getsource(sched_exempter))

        # -- round 4 --
        def test_r4_date_span_respects_quoting(self):
            # finding (codex r3 M2): a quoted paren inside $(date ...) extended the span over a later literal
            deny = ("echo \"$(date '+(')\" \"hb: 2099-01-01T00:00Z\" > /opt/p/private/s.md; echo ')'",
                    "echo '$(date -d 2099-01-01T00:00Z)' > /opt/p/private/s.md",
                    "echo $'$(date \\' 2099-01-01T00:00Z' > /opt/p/private/s.md",
                    "echo \"(\" $(date -u) \")\" hb 2099-01-01T00:00Z > /opt/p/private/s.md",
                    "echo \"$(date -u\" 2099-01-01T00:00Z > /opt/p/private/s.md")
            for cmd in deny:
                self.assertTrue(self.ev("Bash", command=cmd), cmd)
            allow = ("echo \"$(date '+%H:%M (%Z)' -d 2099-01-01T00:00Z)\" > /opt/p/private/s.md",
                     "echo \"hb $(date -d \"2099-01-01T00:00Z\")\" > /opt/p/private/s.md",
                     "echo \"$(date -d \"$(echo ')') 2099-01-01T00:00Z\")\" > /opt/p/private/s.md",
                     "echo `date -d '2099-01-01T00:00Z'` > /opt/p/private/s.md")
            for cmd in allow:
                self.assertEqual(self.ev("Bash", command=cmd), [], cmd)

        def test_r4_env_prefix_date_span(self):
            # finding (gemini r3 m1): `env TZ=UTC date` was not a date substitution
            for cmd in ("echo \"hb $(env TZ=UTC date -d 2099-01-01T00:00Z)\" > /opt/proj/private/s.md",
                        "echo \"hb $(/usr/bin/env TZ=UTC date -d 2099-01-01T00:00Z)\" > /opt/proj/private/s.md"):
                self.assertEqual(self.ev("Bash", command=cmd), [], cmd)
            self.assertTrue(self.ev("Bash", command="echo $(/usrdate 2099-01-01T00:00Z) > /opt/proj/private/s.md"))
            self.assertTrue(self.ev("Bash", command="echo $(envdate 2099-01-01T00:00Z) > /opt/proj/private/s.md"))

        def test_r4_keyword_must_immediately_precede(self):
            for line in ("hb: 2099-01-01T00:00Z next", "target branch pushed, hb: 2099-01-01T00:00Z",
                         "next we did a b c and hb 2099-01-01T00:00Z"):
                self.assertTrue(self.ev("Write", file_path=self.store, content=line), line)
            for line in ("next run at 2099-01-01T00:00Z", "target date: 2099-01-01T00:00Z", "due: **[2099-01-01T00:00Z]**"):
                self.assertEqual(self.ev("Write", file_path=self.store, content=line), [], line)

        def test_r4_scan_is_linear(self):
            content = "2026-09-23T17:45Z " * 100000
            t0 = time.monotonic()
            self.assertEqual(self.ev("Write", file_path=self.store, content=content), [])
            self.assertEqual(self.ev("Bash", command="echo " + content + "> /opt/proj/private/s.md"), [])
            self.assertLess(time.monotonic() - t0, 1.0)
            t0 = time.monotonic()
            self.assertEqual(self.ev("Write", file_path=self.store, content="next " + "2099-01-01T00:00Z x " * 50000),
                             ["2099-01-01T00:00Z"])
            self.assertLess(time.monotonic() - t0, 1.0)

        def test_r5_many_distinct_literals_linear_and_bounded(self):
            # finding (codex r4, sibling pattern): the fragment path scanned the growing list per literal
            lits = [f"2099-{1 + i % 12:02d}-{1 + (i // 12) % 28:02d}T{(i // 336) % 24:02d}:{(i // 8064) % 60:02d}Z"
                    for i in range(40000)]
            fp = self.store_file("x\n" * (EXISTING_MAX_BYTES // 2 + 1))  # over the cap: the fragment path
            t0 = time.monotonic()
            r = self.ev("MultiEdit", file_path=fp, edits=[{"old_string": "x", "new_string": "\n".join(lits[:20000])},
                                                          {"old_string": "x", "new_string": "\n".join(lits[20000:])}])
            w = self.ev("Write", file_path=os.path.join(self.tmp, "w.md"), content=" ".join(lits))
            self.assertLess(time.monotonic() - t0, 1.0)
            self.assertEqual((len(r), len(w)), (40000, 40000))
            old_out = sys.stdout
            sys.stdout = io.StringIO()
            try:
                _deny(w, self.now)
                reason = json.loads(sys.stdout.getvalue())["hookSpecificOutput"]["permissionDecisionReason"]
            finally:
                sys.stdout = old_out
            self.assertIn(f" and {40000 - MAX_REPORTED} more", reason)
            self.assertLess(len(reason), 2000)

        def test_r4_threat_model_stated(self):
            self.assertIn("THREAT MODEL", __doc__.split("\n\n")[1])

    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(T))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
