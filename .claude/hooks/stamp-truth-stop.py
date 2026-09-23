#!/usr/bin/env python3
"""Stop hook: block a turn whose timestamp claims or "Session elapsed" footer disagree with the clock.

THREAT MODEL. An ACCIDENTAL-DRIFT discipline guard: it catches the model composing times instead of reading
the clock and presenting them in its NORMAL status format. It is NOT an adversarial boundary: an evasion that
needs deliberately unusual presentation (an unusual zone, a code span, a quote line, a schedule word placed
before the time) is a disclosed residual, not a defect. It fails OPEN on malformed input.

Fleet orchestrator operational guard (generic: no project name is hardcoded). Motivated by an orchestrator
composing console stamps and "Session elapsed HH:MM" footers from its own sense of time instead of reading
the clock, drifting up to 4h40m ahead (timestamp-from-clock; claims-rest-on-observation). Companion of
clock-inject.py, which feeds the real clock into context; this hook is the check.

TIMESTAMP CLAIM. Anywhere in assistant prose, bracketed or not:
    YYYY-MM-DD[T or space]HH:MM(:SS(.f{1,9})?)? ZONE
ZONE is required: Z (attached or after one space); a numeric offset +HH, +HHMM, or +HH:MM, or with -,
attached or after one space; or, after one space, UTC, GMT, or a letter abbreviation of 2 to 6 capitals.
Z, UTC, and GMT are UTC; an offset is applied as written; a letter abbreviation counts only when it is the
process local zone's abbreviation at that wall time (both DST readings are tried; if both match, the earlier
instant is taken). A time with no zone, or with an abbreviation that is not the local zone, is not a claim
in prose (it is ignored). The zone grammar and the scheduling keyword list are duplicated verbatim in
future-stamp-write.py (python3 -I forbids a sibling import); a self-test asserts they are identical.

EXEMPT TEXT. Lines inside a matched fenced code block (``` or ~~~, closed by a fence of the same character
at least as long; an UNCLOSED fence is not code, so its lines are checked), blockquote lines (starting `>`
after optional whitespace), and inline code spans (a backtick run closed by the next run of the same length
on the same line; an unclosed run opens nothing). For the AHEAD rule only, a NON-leading claim is also exempt
when a scheduling keyword IMMEDIATELY precedes it: the keyword ends at most SCHED_GAP_TOKENS (3) word tokens
before the claim (a word token holds a letter or digit, so `:`, `[`, or `**` do not count), as in "next run
at T", "due T", "deadline: T", "scheduled for T", "until T", "not before T", "by T". Keywords
(case-insensitive, at a word start): due, deadline, expir, until, next, scheduled, not before, not-before,
eta, planned, "target date", "target:", and `by ` with its trailing space. A keyword never exempts a
line-leading status stamp, a keyword AFTER a claim does not exempt it, and a keyword further back does not.

RULES, against the message's reference time REF:
  1. AHEAD: every timestamp claim outside exempt text must be no more than 1 minute after REF.
  2. BEHIND: a STATUS STAMP, a claim that is the first token of its line (after optional whitespace, `*` or
     `_` emphasis, `[`, and one list bullet `-`, `+`, `*`, or `N.`/`N)` followed by whitespace), outside code
     and blockquotes, must be no more than 10 minutes before REF (30 minutes for the final message, which can
     be long in generation). A status stamp is checked for AHEAD and BEHIND whatever keywords its line
     carries. Quoted history mid-line is never checked for BEHIND. A status stamp whose letter abbreviation
     is not the local zone is UNVERIFIABLE and blocks.
  3. ELAPSED FOOTER: the LAST "Session elapsed HH:MM" occurrence in the message that lies outside fenced
     code, blockquote lines, and inline code spans is checked, wherever it sits (a completion marker, a
     `---`, or a quote line after it does not displace it); case-insensitive, with up to eight spaces, tabs,
     `*`, `_`, `:`, `-`, or en or em dash characters between the words and before the number. Its
     tolerance is ASYMMETRIC like the stamps' (fabrication runs ahead): it must be no more than 2 minutes
     AHEAD of (REF - lease start), and no more than 10 minutes BEHIND it (30 minutes for the final message,
     the same long-generation allowance as its status stamp); with no known lease start it is not checked.
     Earlier occurrences (a corrected value earlier on the same line, a worker footer quoted above) are
     ignored.
Every check is per claim in its own try, in integer microseconds (no datetime bound can overflow); a failure
on one claim or entry is skipped and never discards violations already found. Each line is scanned once
(the status prefix and keyword positions are computed once per line; a literal is converted once per
message), so the check is linear in the message.

REF. For a transcript entry, its own recorded `timestamp` (UTC; a naive value is read as UTC); an entry
without a parseable timestamp is skipped, never compared against now. For the payload's
last_assistant_message: the timestamp of the last collected transcript assistant entry when its text matches
(that entry is then not checked twice), else now.

WHICH MESSAGES. The transcript is read backwards; assistant entries (not isMeta, not isSidechain) are
collected until the most recent genuine user message or the RECOVERY BOUNDARY, whichever is later, plus the
last_assistant_message. Recovery boundary: a private per-session state file records OFFSET, the byte offset
just past the last COMPLETE transcript record evaluated (a trailing record with no newline yet that does not
parse is unfinished, and OFFSET never passes it, so it is evaluated once complete), with a SHA-256 of up to
256 bytes before OFFSET. The next Stop (with stop_hook_active or not) evaluates only records starting at or
after OFFSET. The file is written when this hook blocks, and on a pass once a state file exists. LATE-ARRIVAL
EXCEPTION: at a block, when the blocked final message is NOT yet in the transcript, its SHA-256 is recorded
as pending; a later record with that text is skipped ONCE (the pending entry is consumed) because it arrived
after OFFSET only through transcript lag. Pending entries are dropped at any new genuine user message and
when the transcript is reset (shorter than OFFSET, or the bytes before OFFSET changed), which also discards
OFFSET. A blocked final message already in the transcript creates no exception. The boundary is never
inferred from message text. State dir: $XDG_RUNTIME_DIR/clock-truth when XDG_RUNTIME_DIR is absolute, else
/dev/shm/clock-truth-<euid>, created 0700 and used only when it is a real directory owned by this user with
no group or other permission bits; the file is keyed by SHA-256 of transcript_path, opened no-follow,
written via an exclusive temp file and an atomic rename. Any state I/O failure falls back to evaluating the
whole turn, failing toward checking, and never crashes.

Elapsed resolution (same as clock-inject.py). Lease file = env ORCH_LEASE_FILE; else
<CLAUDE_PROJECT_DIR>/.working/session-state.md when CLAUDE_PROJECT_DIR is absolute and that file exists; else
<ORCH_PROJECT_ROOT>/private/session-state.md; else /opt/<project>/private/session-state.md from the payload
cwd (or process cwd). Without ORCH_LEASE_FILE or a CLAUDE_PROJECT_DIR lease the lease FOLLOWS THE CWD; the
fleet should set ORCH_LEASE_FILE. Start = the FIRST line beginning `Active-session:` only; a value other than
<label>-YYYYMMDDTHHMMSSZ, where <label> is 1 to 32 characters of [A-Za-z0-9] (for example `sess-` or
`S88-`), means unknown (for example `none` or a malformed id), and no later line is consulted.

File reads. The lease and transcript are opened non-blocking and must be regular files (a FIFO or device is
treated as unreadable). The lease read is capped at 1 MiB. The transcript is read backwards in 64 KiB chunks,
at most 64 MiB, each record at most 4 MiB (a longer record is skipped unparsed); every scan is linear.

Contract: pass = no stdout, exit 0; block = top-level {"decision": "block", "reason": ...} on stdout, exit 0
(the Claude Code hooks reference, Stop decision control, specifies top-level decision and reason for Stop).
Fail-OPEN silently on unparseable hook input or any internal error outside the per-claim isolation: a
DISCIPLINE guard, not a security boundary. Skipped entirely: a pool worker, detected as env ORCH_WORKER=1 OR
env ORCH_VERIFY_OWNER present with any value, even empty (orch-verify exports the latter into its worker
shells and never sets the former), and a payload carrying agent_id (a subagent's stop).

RESIDUAL COVERAGE (disclosed per disclose-guard-residuals). MISSES: a time without an explicit zone, a
12-hour or natural-language time, a compact sess- id, an epoch number, and a relative claim ("started 3
hours ago") are not checked. A fabricated future time placed mid-line within three word tokens after a
scheduling keyword passes, including everyday prose such as "the next phase at T" or "fixed by Jeff at T"
(the line-leading status stamp is always checked). A fabricated stamp or footer inside a code fence, a `>`
quote line, or an inline code span passes. An unquoted worker footer pasted AFTER the real footer is the one
checked (quote worker output in a fence or a `>` line). A stale footer that lags true elapsed by up to the
BEHIND window (10 minutes, 30 for the final message) passes. FALSE POSITIVES: prose that happens to put the
words "session elapsed" before an HH:MM outside code, for example "the total session elapsed: 14:30 across
all workers", is read as the footer when it is the last such occurrence and blocks on a mismatch; remedy:
put it in a `code span` or a `>` line. AHEAD applies to EVERY zoned claim
(that breadth is the drift catch), so a genuine FUTURE time mentioned mid-line without an immediately
preceding keyword blocks, for example "the cert is valid through 2027-01-01T00:00Z" or "the eclipse occurs
2027-08-02T18:00Z"; remedy: precede it with a keyword ("expires 2027-...", "until 2027-...") or put it in a
`code span`. A correction that repeats the rejected future value in plain prose re-blocks; quote it in a
`code span` or a `>` line, or omit it. A genuinely scheduled time written as the FIRST token of a line blocks
(put a label such as "Next run:" before it). A line-leading historical stamp (a bulleted history list) older
than the BEHIND tolerance blocks (move the time mid-line or into a blockquote). Inline code-span detection is
per line and approximate (an unclosed backtick run hides later spans on that line, so their claims are
checked, failing toward checking). A letter abbreviation is trusted as local when it matches the process
zone's abbreviation; a foreign zone sharing that abbreviation is not distinguished, and a foreign
abbreviation mid-line is ignored. Genuine-user detection is heuristic on entry shape and a fixed list of
notification prefixes. The recovery boundary lives in volatile per-user storage: it is lost on reboot, and
when the state cannot be used the whole turn is re-evaluated, so an already-reported violation can re-block
(bounded by Claude Code's override after 8 consecutive Stop blocks). A record over 4 MiB and anything beyond
64 MiB back are not scanned. Only the host clock is authoritative, so a wrong host clock is enforced
faithfully. The elapsed check is only as right as the lease (a stale, wrong-clock, or cwd-selected foreign
lease yields a false block or a false pass). Subagent output is not checked.

Self-test: python3 -I -B stamp-truth-stop.py --self-test
"""

import bisect
import datetime
import hashlib
import json
import os
import re
import stat
import sys
import time

UTC = datetime.timezone.utc
US = 1_000_000
MINUTE = 60 * US
AHEAD_US = 1 * MINUTE
BEHIND_US = 10 * MINUTE
FINAL_BEHIND_US = 30 * MINUTE
ELAPSED_AHEAD_US = 2 * MINUTE  # footer AHEAD tolerance; its BEHIND tolerance is the message's `behind`
LEASE_MAX_BYTES = 1 << 20
STATE_MAX_BYTES = 1 << 16
MAX_SCAN_BYTES = 64 << 20
MAX_RECORD_BYTES = 4 << 20
CHUNK = 1 << 16
TAIL_BYTES = 256
MAX_PENDING = 8
MAX_REPORTED = 20
BLOCK_PREFIX = "Clock-truth check (stamp-truth-stop hook) failed"
_EPOCH = datetime.datetime(1970, 1, 1)
_EPOCH_UTC = _EPOCH.replace(tzinfo=UTC)
_ONE_US = datetime.timedelta(microseconds=1)

# Duplicated verbatim in future-stamp-write.py; the self-test asserts the two copies are identical.
SCHED_KEYWORDS = ("due", "deadline", "expir", "until", "next", "scheduled", "not before", "not-before", "eta",
                  "planned", "target date", "target:", "by ")
SCHED_GAP_TOKENS = 3
TIME_GRAMMAR = r"(?<!\d)(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2})(?::(\d{2})(?:\.(\d{1,9}))?)?"
ZONE_GRAMMAR = r"(?:[ ]?(Z)|[ ]?([+-]\d{2}(?::?\d{2})?)|[ ](UTC|GMT|[A-Z]{2,6}))(?![A-Za-z0-9])"

_SCHED_RE = re.compile(r"(?<![a-z0-9])(?:" + "|".join(re.escape(k) for k in SCHED_KEYWORDS) + ")", re.IGNORECASE)
_TOKEN_RE = re.compile(r"\S+")
_WORDCH_RE = re.compile(r"[A-Za-z0-9]")
_CLAIM_RE = re.compile(TIME_GRAMMAR + ZONE_GRAMMAR)
_BTICK_RE = re.compile(r"`+")
_SESS_RE = re.compile(r"[A-Za-z0-9]{1,32}-(\d{8}T\d{6}Z)")
_FOOT_RE = re.compile(r"(?<![A-Za-z0-9])session[ \t*_:\-\u2013\u2014]{1,8}elapsed[ \t*_:\-\u2013\u2014]{0,8}"
                      r"(\d{1,4}):([0-5]\d)(?!\d)", re.IGNORECASE)
_FENCE_RE = re.compile(r"`{3,}|~{3,}")
_BULLET_RE = re.compile(r"(?:[-+*]|\d{1,9}[.)])(?=[ \t])")
_NOT_GENUINE_PREFIXES = ("<task-notification>", "<system-reminder>", "[SYSTEM NOTIFICATION",
                         "<local-command-", "Stop hook feedback", "<user-prompt-submit-hook>")


def _is_worker(env=None):
    """True for an orch-verify pool worker: ORCH_WORKER=1, or ORCH_VERIFY_OWNER present (any value, even empty).
    Kept identical across the fleet hooks (python3 -I forbids a sibling import)."""
    env = os.environ if env is None else env
    return env.get("ORCH_WORKER") == "1" or "ORCH_VERIFY_OWNER" in env


# ---- lease / elapsed (kept identical to clock-inject.py; python3 -I forbids a sibling import) ----

def read_regular(path, limit):
    """Bytes (at most `limit`) of a REGULAR file, or None. Opened non-blocking so a FIFO cannot stall us."""
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | getattr(os, "O_NOCTTY", 0) | getattr(os, "O_CLOEXEC", 0))
    except (OSError, TypeError, ValueError):
        return None
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            return None
        chunks, got = [], 0
        while got < limit:
            b = os.read(fd, min(1 << 16, limit - got))
            if not b:
                break
            chunks.append(b)
            got += len(b)
        return b"".join(chunks)
    except OSError:
        return None
    finally:
        os.close(fd)


def lease_file(cwd=None):
    """Return the lease file path to use, or None when none can be derived."""
    env = os.environ.get("ORCH_LEASE_FILE")
    if env:
        return env
    proj = os.environ.get("CLAUDE_PROJECT_DIR")
    if proj and os.path.isabs(proj):
        cand = os.path.join(proj, ".working", "session-state.md")
        if os.path.isfile(cand):
            return cand
    root = os.environ.get("ORCH_PROJECT_ROOT")
    if root and os.path.isabs(root):
        return os.path.join(root, "private", "session-state.md")
    parts = os.path.abspath(cwd or os.getcwd()).split(os.sep)
    if len(parts) >= 3 and parts[0] == "" and parts[1] == "opt" and parts[2]:
        return os.path.join("/opt", parts[2], "private", "session-state.md")
    return None


def lease_start(path):
    """UTC start from the FIRST `Active-session:` line of `path`, or None (never searches past it)."""
    if not path:
        return None
    data = read_regular(path, LEASE_MAX_BYTES)
    if data is None:
        return None
    for line in data.decode("utf-8", "replace").splitlines():
        if line.startswith("Active-session:"):
            m = _SESS_RE.fullmatch(line[len("Active-session:"):].strip())
            if not m:
                return None
            try:
                return datetime.datetime.strptime(m.group(1), "%Y%m%dT%H%M%SZ").replace(tzinfo=UTC)
            except ValueError:
                return None
    return None


def fmt_elapsed_us(us):
    if us < 0:
        return None
    secs = us // US
    return f"{secs // 3600:02d}:{(secs % 3600) // 60:02d}"


# ---- time arithmetic (integer microseconds since the epoch) ----

def to_us(dt):
    """Epoch microseconds for an aware datetime (exact integer arithmetic, no overflow)."""
    return (dt - _EPOCH_UTC) // _ONE_US


def fmt_us(us):
    try:
        return (_EPOCH_UTC + datetime.timedelta(microseconds=us)).strftime("%Y-%m-%dT%H:%M:%SZ")
    except (OverflowError, ValueError):
        return f"epoch{us // US:+d}s"


def _naive_us(y, mo, d, hh, mi, ss, us):
    return (datetime.datetime(y, mo, d, hh, mi, ss, us) - _EPOCH) // _ONE_US


def _local_us(y, mo, d, hh, mi, ss, abbr):
    """Epoch microseconds for a local wall time whose zone abbreviation is `abbr`, or None."""
    found = []
    for isdst in (0, 1):  # an explicit isdst makes mktime deterministic (no dependence on earlier calls)
        try:
            ts = time.mktime((y, mo, d, hh, mi, ss, 0, 0, isdst))
            lt = time.localtime(ts)
        except (OverflowError, ValueError, OSError):
            continue
        if (lt.tm_year, lt.tm_mon, lt.tm_mday, lt.tm_hour, lt.tm_min, lt.tm_sec) == (y, mo, d, hh, mi, ss) \
                and lt.tm_zone == abbr:
            found.append(int(ts))
    return min(found) * US if found else None


def claim_us(m):
    """Epoch microseconds for a matched claim, or None (invalid fields, or an abbreviation not local then)."""
    try:
        y, mo, d, hh, mi = (int(m.group(i)) for i in range(1, 6))
        ss = int(m.group(6) or 0)
        us = int(((m.group(7) or "") + "000000")[:6])
        z, off, abbr = m.group(8), m.group(9), m.group(10)
        if z or abbr in ("UTC", "GMT"):
            return _naive_us(y, mo, d, hh, mi, ss, us)
        if off:
            digits = off[1:].replace(":", "")
            hours, mins = int(digits[:2]), int(digits[2:] or 0)
            if hours > 18 or mins > 59:
                return None
            base, delta = _naive_us(y, mo, d, hh, mi, ss, us), (hours * 3600 + mins * 60) * US
            return base - delta if off[0] == "+" else base + delta
        loc = _local_us(y, mo, d, hh, mi, ss, abbr)
        return None if loc is None else loc + us
    except (ValueError, OverflowError, OSError, TypeError):
        return None


# ---- the contract ----

def _code_lines(lines):
    """Indexes of lines inside a MATCHED fenced code block (fence lines included); an unclosed fence is text."""
    code, open_i, fch, flen = set(), None, "", 0
    for i, ln in enumerate(lines):
        s = ln.strip(" \t")
        if open_i is None:
            m = _FENCE_RE.match(s)
            if m and not (s[0] == "`" and "`" in s[m.end():]):
                open_i, fch, flen = i, s[0], m.end()
        elif s and len(s) >= flen and s == fch * len(s):
            code.update(range(open_i, i + 1))
            open_i = None
    return code


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


def _lead_end(line):
    """Index where the permitted status-stamp prefix of `line` ends: whitespace, one bullet, then `*`, `_`,
    `[`, and whitespace. A claim starting exactly there is a line-leading status stamp."""
    i, n = 0, len(line)
    while i < n and line[i] in " \t":
        i += 1
    b = _BULLET_RE.match(line, i)
    if b:
        i = b.end()
    while i < n and line[i] in " \t*_[":
        i += 1
    return i


def _code_spans(line):
    """Sorted [start, end) inline code spans on one line: a backtick run closed by the next run of the same
    length (runs of other lengths inside are content); an unclosed run opens nothing. Linear."""
    spans, open_len, open_start = [], 0, 0
    for r in _BTICK_RE.finditer(line):
        n = r.end() - r.start()
        if not open_len:
            open_len, open_start = n, r.start()
        elif n == open_len:
            spans.append((open_start, r.end()))
            open_len = 0
    return spans


def _in_spans(spans, pos):
    k = bisect.bisect_right(spans, (pos, float("inf"))) - 1
    return k >= 0 and pos < spans[k][1]


def _minutes(off_us):
    mins = round(off_us / MINUTE)
    return f"{abs(mins)} min {'AHEAD' if mins > 0 else 'BEHIND'}"


def _check_claim(m, status, sched, ref, behind, where, cache=None):
    """A violation string for one claim, or None. `status`: the claim is a line-leading status stamp.
    `sched`: a scheduling keyword immediately precedes it (never set for a status stamp). `cache` maps a
    literal to its converted value so a repeated literal is converted once."""
    literal = m.group(0)
    if cache is not None and literal in cache:
        got = cache[literal]
    else:
        got = claim_us(m)
        if cache is not None:
            cache[literal] = got
    if got is None:
        abbr = m.group(10)
        if status and abbr:
            local_abbr = datetime.datetime.now(UTC).astimezone().tzname()
            return (f"status stamp {literal} in {where}: UNVERIFIABLE, {abbr} is not the local zone abbreviation "
                    f"({local_abbr}) valid at that wall time; use UTC, Z, a numeric offset, or the local zone")
        return None
    diff = got - ref
    if diff > AHEAD_US and (status or not sched):
        return f"timestamp {literal} in {where}: {_minutes(diff)} of when it was written ({fmt_us(ref)})"
    if status and -diff > behind:
        return f"status stamp {literal} in {where}: {_minutes(diff)} of when it was written ({fmt_us(ref)})"
    return None


def check_message(text, ref, start, where, behind):
    """Violation strings for one assistant message written at `ref` (epoch us); `start` is epoch us or None."""
    bad, seen, cache = [], set(), {}
    lines = text.splitlines()
    code = _code_lines(lines)
    foot = None  # the last "Session elapsed" occurrence outside code and quotes
    for i, line in enumerate(lines):
        if i in code or line.lstrip().startswith(">"):
            continue
        spans = _code_spans(line) if "`" in line else []
        lead = exempt = None
        for m in _CLAIM_RE.finditer(line):
            try:
                if spans and _in_spans(spans, m.start()):
                    continue
                if lead is None:
                    lead = _lead_end(line)
                status = m.start() == lead
                sched = False
                if not status:
                    if exempt is None:
                        exempt = sched_exempter(line)
                    sched = exempt(m.start())
                v = _check_claim(m, status, sched, ref, behind, where, cache)
            except Exception:
                continue  # isolate one claim
            if v and v not in seen:
                seen.add(v)
                bad.append(v)
        for m in _FOOT_RE.finditer(line):
            if not (spans and _in_spans(spans, m.start())):
                foot = m
    if start is not None and foot is not None:
        true_el = ref - start
        try:
            off = (int(foot.group(1)) * 60 + int(foot.group(2))) * MINUTE - true_el
            if true_el >= 0 and (off > ELAPSED_AHEAD_US or -off > behind):
                bad.append(f"\"{' '.join(foot.group(0).split())}\" (last elapsed footer in {where}): true elapsed "
                           f"when written was {fmt_elapsed_us(true_el)} ({_minutes(off)})")
        except Exception:
            pass
    return bad


# ---- transcript ----

def _reverse_records(fd, size, floor=0):
    """Yield (start_offset, record) last-first for non-empty records starting at or after `floor`. Linear:
    pieces of a record are kept as a list and joined once; a record over MAX_RECORD_BYTES is not accumulated
    and yields None in place of its bytes."""
    pos, lower = size, max(floor, size - MAX_SCAN_BYTES, 0)
    tail, tail_len, over = [], 0, False
    while pos > lower:
        n = min(CHUNK, pos - lower)
        pos -= n
        chunk = os.pread(fd, n, pos)
        if len(chunk) != n:
            raise OSError("short read")
        j = n
        while True:
            k = chunk.rfind(b"\n", 0, j)
            piece = chunk[k + 1:j]
            if not over:
                tail.append(piece)
                tail_len += len(piece)
                if tail_len > MAX_RECORD_BYTES:
                    over, tail = True, []
            if k < 0:
                break
            if over:
                yield pos + k + 1, None
            elif tail_len:
                yield pos + k + 1, b"".join(reversed(tail))
            tail, tail_len, over, j = [], 0, False, k
    if pos == lower and (lower == 0 or lower == floor):
        if over:
            yield pos, None
        elif tail_len:
            yield pos, b"".join(reversed(tail))


def _entry_texts(content):
    if isinstance(content, str):
        return [content]
    out = []
    if isinstance(content, list):
        for blk in content:
            if isinstance(blk, dict) and blk.get("type") == "text" and isinstance(blk.get("text"), str):
                out.append(blk["text"])
    return out


def _content(entry):
    msg = entry.get("message")
    return msg.get("content") if isinstance(msg, dict) else None


def _has_tool_result(content):
    return isinstance(content, list) and any(isinstance(b, dict) and b.get("type") == "tool_result"
                                             for b in content)


def _is_genuine_user(entry):
    if entry.get("type") != "user" or entry.get("isMeta") or entry.get("isSidechain"):
        return False
    content = _content(entry)
    if _has_tool_result(content):
        return False
    texts = _entry_texts(content)
    if not texts:
        return False
    return not texts[0].lstrip().startswith(_NOT_GENUINE_PREFIXES)


def _parse_ts(value):
    """Epoch us from a transcript timestamp; a naive value is UTC (the transcript format); else None."""
    if not isinstance(value, str):
        return None
    try:
        dt = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            return (dt - _EPOCH) // _ONE_US
        return (dt.replace(tzinfo=None) - _EPOCH) // _ONE_US - dt.utcoffset() // _ONE_US
    except (ValueError, OverflowError, TypeError):
        return None


def _tail_sha(fd, offset):
    """SHA-256 of up to TAIL_BYTES of the transcript just before `offset` (None at offset 0)."""
    if offset <= 0:
        return None
    n = min(TAIL_BYTES, offset)
    b = os.pread(fd, n, offset - n)
    if len(b) != n:
        raise OSError("short read")
    return hashlib.sha256(b).hexdigest()


def turn_messages(path, floor=0, floor_tail=None):
    """This turn's assistant text after byte offset `floor`, as a dict:
    msgs: [(text, written_at_us_or_None)] oldest first, after the later of the last genuine user message and
          `floor`;
    size: the transcript size, or None when it is unreadable or not a regular file;
    end:  the offset just past the last COMPLETE record (an unfinished trailing record, one with no newline
          yet that does not parse, is never passed, so it is read again once complete);
    tail: the SHA-256 of the bytes just before `end`;
    reset: True when `floor` was unusable (beyond the end, or the bytes before it changed), so the whole turn
          was read from the start;
    user: True when a genuine user message was met after the floor."""
    out = {"msgs": [], "size": None, "end": 0, "tail": None, "reset": False, "user": False}
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | getattr(os, "O_NOCTTY", 0) | getattr(os, "O_CLOEXEC", 0))
    except (OSError, TypeError, ValueError):
        return out
    msgs = []
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            return out
        size = st.st_size
        if floor and (floor > size or floor_tail is None or _tail_sha(fd, floor) != floor_tail):
            floor, out["reset"] = 0, True
        terminated = size == 0 or os.pread(fd, 1, size - 1) == b"\n"
        end, first = (size if terminated else floor), True
        for off, raw in _reverse_records(fd, size, floor):
            trailing, first = first and not terminated, False
            try:
                entry = json.loads(raw) if raw is not None else None
            except Exception:
                entry = None  # malformed or unfinished; isolated
            if trailing and isinstance(entry, dict):
                end = size  # a parseable record lacking only its newline is complete
            elif trailing:
                end = off  # unfinished: stop the boundary before it
            if not isinstance(entry, dict):
                continue
            try:
                if _is_genuine_user(entry):
                    out["user"] = True
                    break
                if entry.get("type") == "assistant" and not entry.get("isSidechain") and not entry.get("isMeta"):
                    texts = _entry_texts(_content(entry))
                    if texts:
                        msgs.append(("\n".join(texts), _parse_ts(entry.get("timestamp"))))
            except Exception:
                continue  # isolate a malformed entry
        out["size"], out["end"], out["tail"] = size, end, _tail_sha(fd, end)
    except OSError:
        out["size"] = None  # keep whatever was collected; no boundary can be trusted
    finally:
        os.close(fd)
    msgs.reverse()
    out["msgs"] = msgs
    return out


# ---- recovery-boundary state ----

def _sha(text):
    return hashlib.sha256(text.encode("utf-8", "surrogatepass")).hexdigest()


def default_state_dir():
    x = os.environ.get("XDG_RUNTIME_DIR")
    if x and os.path.isabs(x):
        return os.path.join(x, "clock-truth")
    return f"/dev/shm/clock-truth-{os.geteuid()}"


def _private_dir(path):
    """`path` as a private (0700-or-stricter, own-uid, real) directory, or raise OSError."""
    try:
        os.mkdir(path, 0o700)
    except FileExistsError:
        pass
    st = os.lstat(path)
    if not stat.S_ISDIR(st.st_mode) or st.st_uid != os.geteuid() or st.st_mode & 0o077:
        raise OSError("state dir is not private")
    return path


def _is_hash(h):
    return isinstance(h, str) and len(h) == 64 and all(c in "0123456789abcdef" for c in h)


def load_state(sdir, tp):
    """(offset, tail hash or None, [pending late-arrival hashes]); (0, None, []) when absent or unusable."""
    empty = (0, None, [])
    try:
        d = _private_dir(sdir)
        fd = os.open(os.path.join(d, _sha(tp)), os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW |
                     getattr(os, "O_CLOEXEC", 0))
    except (OSError, TypeError, ValueError):
        return empty
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_uid != os.geteuid():
            return empty
        obj = json.loads(os.read(fd, STATE_MAX_BYTES))
        off, tail, pending = obj.get("offset"), obj.get("tail"), obj.get("pending")
        if obj.get("v") != 2 or type(off) is not int or off < 0 or not isinstance(pending, list) \
                or not (tail is None or _is_hash(tail)) or (off > 0) != (tail is not None) \
                or not all(_is_hash(h) for h in pending):
            return empty
        return off, tail, pending[-MAX_PENDING:]
    except (OSError, ValueError, AttributeError):
        return empty
    finally:
        os.close(fd)


def save_state(sdir, tp, offset, tail, pending):
    """Record the boundary and pending late-arrival hashes; any failure is swallowed (the next Stop checks
    the whole turn)."""
    tmp = None
    try:
        d = _private_dir(sdir)
        final = os.path.join(d, _sha(tp))
        tmp = f"{final}.{os.getpid()}.{os.urandom(4).hex()}.tmp"
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0), 0o600)
        try:
            os.write(fd, json.dumps({"v": 2, "offset": offset, "tail": tail,
                                     "pending": list(pending)[-MAX_PENDING:]}).encode())
        finally:
            os.close(fd)
        os.replace(tmp, final)
        tmp = None
    except Exception:
        pass
    finally:
        if tmp is not None:
            try:
                os.unlink(tmp)
            except OSError:
                pass


def evaluate(payload, now, start, sdir=None):
    """Return a block reason string, or None to pass. `now` and `start` are aware datetimes (start may be None)."""
    bad, seen, over = [], set(), [0]  # a bounded report list; `seen` dedupes in O(1); `over` counts the rest

    def add(vs):
        for v in vs:
            if v in seen:
                continue
            seen.add(v)
            if len(bad) < MAX_REPORTED:
                bad.append(v)
            else:
                over[0] += 1

    now_us = to_us(now)
    start_us = to_us(start) if start is not None else None
    lam = payload.get("last_assistant_message")
    lam = lam if isinstance(lam, str) and lam.strip() else None
    tp = payload.get("transcript_path")
    tp = tp if isinstance(tp, str) and tp else None
    sdir = sdir or default_state_dir()
    offset, tail, pending = load_state(sdir, tp) if tp else (0, None, [])
    had_state = bool(offset or pending)
    t = turn_messages(tp, offset, tail) if tp else {"msgs": [], "size": None}
    msgs = t["msgs"]
    if t.get("reset") or t.get("user"):
        pending = []  # a reset transcript or a new genuine user message invalidates the late-arrival exception
    lam_in_transcript = lam is not None and any(text.strip() == lam.strip() for text, _ in msgs)
    lam_ref = now_us
    if lam is not None and msgs and msgs[-1][0].strip() == lam.strip():
        if msgs[-1][1] is not None:
            lam_ref = msgs[-1][1]
        msgs = msgs[:-1]  # checked below as the final message
    if lam is not None:
        try:
            add(check_message(lam, lam_ref, start_us, "your final message", FINAL_BEHIND_US))
        except Exception:
            pass
    remaining = list(pending)
    n = len(msgs)
    for i, (text, ref) in enumerate(msgs, 1):
        h = _sha(text.strip())
        if h in remaining:
            remaining.remove(h)  # the already-reported final message arriving late: skipped once, consumed
            continue
        if ref is None:
            continue  # no trustworthy written_at
        try:
            add(check_message(text, ref, start_us, f"earlier message {i} of {n} this turn", BEHIND_US))
        except Exception:
            continue
    if tp and t["size"] is not None:
        if bad:
            late = [_sha(lam.strip())] if lam is not None and not lam_in_transcript else []
            save_state(sdir, tp, t["end"], t["tail"], remaining + late)
        elif had_state:
            save_state(sdir, tp, t["end"], t["tail"], remaining)
    if not bad:
        return None
    shown = bad + ([f"... and {over[0]} more distinct violation(s) not listed"] if over[0] else [])
    local = now.astimezone()
    el = fmt_elapsed_us(now_us - start_us) if start_us is not None else None
    return (BLOCK_PREFIX + ": these clock claims do not match the real clock.\n- " + "\n- ".join(shown) +
            f"\nTRUE values now: local [{local.strftime('%Y-%m-%d %H:%M:%S')} {local.tzname()}], "
            f"UTC [{now.strftime('%Y-%m-%dT%H:%M:%SZ')}], session elapsed "
            f"{el if el else 'unknown (no parseable Active-session lease id)'}.\n"
            "Checked: every date-time with an explicit zone in your prose must not be ahead of when it was "
            "written; a stamp that starts a line must also be recent; the LAST \"Session elapsed HH:MM\" footer "
            "outside code and quotes must match the lease. Code fences, `>` quote lines, and `code spans` are "
            "exempt. A genuine FUTURE time mid-line (a deadline, an expiry, a planned run) is allowed only when a "
            "schedule word immediately precedes it (due, deadline, expires, until, next run at, scheduled for, "
            "not before, by, ...) or when it is in a `code span`; a line-leading stamp is always checked. To "
            "quote the rejected value in a correction, put it in a `code span` or a `>` line, or leave it out. "
            "Re-read the clock with `date` and `date -u` (never compose a time from memory or context), then send "
            "a short corrected message with the correct stamp and, as its last footer, the correct elapsed value. "
            "Messages before this block are not re-checked.")


def main(argv):
    if len(argv) > 1 and argv[1] == "--self-test":
        return _self_test()
    if _is_worker():
        return 0
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict) or payload.get("agent_id"):
            return 0
        cwd = payload.get("cwd") if isinstance(payload.get("cwd"), str) else None
        now = datetime.datetime.now(UTC)
        reason = evaluate(payload, now, lease_start(lease_file(cwd)))
    except Exception:
        return 0  # fail-open silently
    if reason:
        print(json.dumps({"decision": "block", "reason": reason}))
    return 0


def _self_test():
    import importlib.util
    import inspect
    import io
    import shutil
    import subprocess
    import tempfile
    import unittest

    def iso(dt):
        return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    def lstamp(dt):
        loc = dt.astimezone()
        return f"[{loc.strftime('%Y-%m-%d %H:%M:%S')} {loc.tzname()}]"

    def ustamp(dt):
        return f"[{dt.strftime('%Y-%m-%dT%H:%M:%SZ')}]"

    def run_main(payload_text, env=None):
        old_in, old_out, old_env = sys.stdin, sys.stdout, dict(os.environ)
        sys.stdin, sys.stdout = io.StringIO(payload_text), io.StringIO()
        try:
            for k in ("ORCH_WORKER", "ORCH_VERIFY_OWNER", "CLAUDE_PROJECT_DIR"):
                os.environ.pop(k, None)
            os.environ.update(env or {})
            rc = main(["stamp-truth-stop.py"])
            return rc, sys.stdout.getvalue()
        finally:
            sys.stdin, sys.stdout = old_in, old_out
            os.environ.clear()
            os.environ.update(old_env)

    def in_subprocess(expr, timeout):
        """Run `expr` (with module m loaded) in a fresh interpreter; return stdout, raising on timeout."""
        code = ("import importlib.util as u,datetime,os,time;os.environ['TZ']='EST5EDT,M3.2.0,M11.1.0';time.tzset();"
                "s=u.spec_from_file_location('m',%r);m=u.module_from_spec(s);s.loader.exec_module(m);"
                "UTC=datetime.timezone.utc;print(%s)" % (os.path.abspath(__file__), expr))
        return subprocess.run([sys.executable, "-I", "-B", "-c", code], capture_output=True, text=True,
                              timeout=timeout).stdout.strip()

    MIN = datetime.timedelta(minutes=1)

    class T(unittest.TestCase):
        def setUp(self):
            # Pin the zone (test hermeticity): a POSIX TZ string needs no tzdata on the host.
            self._env = {k: os.environ.get(k) for k in ("TZ", "ORCH_LEASE_FILE", "ORCH_PROJECT_ROOT",
                                                         "XDG_RUNTIME_DIR", "CLAUDE_PROJECT_DIR")}
            for k in ("ORCH_LEASE_FILE", "ORCH_PROJECT_ROOT", "CLAUDE_PROJECT_DIR"):
                os.environ.pop(k, None)
            os.environ["TZ"] = "EST5EDT,M3.2.0,M11.1.0"
            time.tzset()
            base = "/dev/shm" if os.path.isdir("/dev/shm") else None
            self.tmp = tempfile.mkdtemp(prefix="clk.", dir=base)
            os.environ["XDG_RUNTIME_DIR"] = self.tmp
            self.sdir = os.path.join(self.tmp, "state")
            self.tr = os.path.join(self.tmp, "t.jsonl")
            self.now = datetime.datetime(2026, 9, 23, 17, 45, 0, tzinfo=UTC)
            self.start = datetime.datetime(2026, 9, 23, 14, 18, 0, tzinfo=UTC)  # elapsed 03:27

        def tearDown(self):
            shutil.rmtree(self.tmp, ignore_errors=True)
            for k, v in self._env.items():
                os.environ.pop(k, None)
                if v is not None:
                    os.environ[k] = v
            time.tzset()

        def write(self, entries, mode="w"):
            if mode == "w":  # a fresh transcript path: a real transcript is append-only
                self.tr = os.path.join(self.tmp, f"t{time.monotonic_ns()}.jsonl")
            with open(self.tr, mode) as f:
                for e in entries:
                    f.write((e if isinstance(e, str) else json.dumps(e)) + "\n")

        def user(self, text, ts=None, **extra):
            e = {"type": "user", "timestamp": iso(ts or self.now), "message": {"role": "user", "content": text}}
            e.update(extra)
            return e

        def asst(self, text, ts=None, **extra):
            e = {"type": "assistant", "timestamp": iso(ts or self.now),
                 "message": {"role": "assistant", "content": [{"type": "text", "text": text}]}}
            e.update(extra)
            return e

        def block_entry(self):
            return {"type": "user", "timestamp": iso(self.now),
                    "message": {"role": "user", "content": "Stop hook feedback:\n" + BLOCK_PREFIX + ": ..."}}

        def ev(self, entries=None, sdir=None, now=None, **extra):
            if entries is not None:
                self.write(entries)
            payload = {"transcript_path": self.tr, "hook_event_name": "Stop", "stop_hook_active": False}
            payload.update(extra)
            return evaluate(payload, now or self.now, self.start, sdir or self.sdir)

        def final(self, text, now=None):
            return evaluate({"last_assistant_message": text}, now or self.now, self.start, self.sdir)

        # -- AHEAD: every zoned claim anywhere --
        def test_correct_local_stamp_passes(self):
            self.assertIsNone(self.ev([self.user("go"), self.asst(f"{lstamp(self.now)} done.")]))

        def test_correct_utc_stamp_and_elapsed_pass(self):
            txt = f"{ustamp(self.now)} merged.\nSession elapsed 03:27, 0 compactions"
            self.assertIsNone(self.ev([self.user("go"), self.asst(txt)]))

        def test_stamp_30_min_ahead_blocks(self):
            r = self.ev([self.user("go"), self.asst(f"{lstamp(self.now + 30 * MIN)} x")])
            self.assertIn("30 min AHEAD", r)
            self.assertTrue(r.startswith(BLOCK_PREFIX))
            self.assertIn("TRUE values now: local [2026-09-23 13:45:00 EDT], UTC [2026-09-23T17:45:00Z]", r)

        def test_status_label_future_blocks(self):
            # finding (codex r2): 'Status: [future]' passed because only a message-leading stamp was checked
            self.assertIn("280 min AHEAD", self.final("Status: [2026-09-23T22:25Z] done."))

        def test_unbracketed_local_ahead_blocks(self):
            # finding (claude r2): an unbracketed console stamp was never checked
            self.assertIn("280 min AHEAD", self.final("2026-09-23 18:25 EDT starting phase 3"))
            self.assertIn("280 min AHEAD", self.final("progress at 2026-09-23 18:25:00 EDT, fine"))
            self.assertIn("280 min AHEAD", self.final("2026-09-23 18:25:02 EDT | 2026-09-23T22:25:02Z | x"))

        def test_stamp_after_other_text_blocks(self):
            # finding (gemini r2): any text before the stamp evaded the leading-only check
            self.assertIn("300 min AHEAD", self.final("<thinking>checking clock</thinking>\n"
                                                      "[2026-09-23 22:45:00 UTC] Status update."))

        def test_long_emphasis_prefix_blocks(self):
            # finding (codex r2): a 128-character window hid a stamp after a long permitted prefix
            self.assertIn("AHEAD", self.final("***" + " " * 128 + "[2026-09-23T22:25Z]"))

        def test_numeric_and_spaced_offsets(self):
            self.assertIsNone(self.final("[2026-09-23 22:45 +05] ok"))
            self.assertIsNone(self.final("[2026-09-23 23:15 +05:30] ok"))
            self.assertIn("300 min AHEAD", self.final("[2026-09-23 13:45 -09] x"))
            self.assertIn("300 min AHEAD", self.final("at 2026-09-23T13:45-0900 x"))
            os.environ["TZ"] = "<+05>-5"
            time.tzset()
            self.assertIsNone(self.final(f"{lstamp(self.now)} ok"))

        def test_fractional_seconds(self):
            self.assertIn("280 min AHEAD", self.final("[2026-09-23T22:25:00.000Z] x"))
            self.assertIsNone(self.final("[2026-09-23T17:44:59.123456789Z] x"))

        def test_zoneless_and_foreign_abbreviation_mid_line_ignored(self):
            self.assertIsNone(self.final("the job will run 2026-09-23 22:25 and 2026-09-24T01:00"))
            self.assertIsNone(self.final("their office shows 2026-09-23 22:25 PDT"))

        def test_status_foreign_abbreviation_unverifiable(self):
            self.assertIn("UNVERIFIABLE", self.final("[2026-09-23 13:45:00 PDT] x"))
            self.assertIn("UNVERIFIABLE", self.final("[2026-09-24 09:00 PDT] deploy scheduled"))

        def test_dst_fold_deterministic(self):
            # 2026-11-01 01:30 occurs twice in EST5EDT: EDT = 05:30Z, EST = 06:30Z
            t = datetime.datetime(2026, 11, 1, 5, 30, tzinfo=UTC)
            self.assertIsNone(self.final("[2026-11-01 01:30 EDT] a", t))
            self.assertIn("60 min AHEAD", self.final("[2026-11-01 01:30 EST] a", t))

        # -- exemptions --
        def test_quoted_past_stamp_mid_line_passes(self):
            txt = (f"{lstamp(self.now)} The incident log said \"[2026-09-22T17:45:00Z] failed\" and "
                   "2026-09-20 10:00 UTC earlier.")
            self.assertIsNone(self.final(txt))

        def test_scheduled_future_with_keyword_passes(self):
            for txt in ("The next run is [2026-09-24T17:45:00Z].", "Deadline set for 2026-12-25 09:00:00 EST.",
                        "Retry not before 2026-09-24 01:00 UTC", "ETA 2026-09-24T00:00Z"):
                self.assertIsNone(self.final(txt), txt)

        def test_keyword_never_exempts_leading_status_stamp(self):
            # residual 1 closed: a keyword on the line no longer exempts the line-leading status stamp
            self.assertIn("280 min AHEAD", self.final("[2026-09-23T22:25Z] merged. Next: QA"))
            self.assertIn("280 min AHEAD", self.final("- **2026-09-23 18:25 EDT** deadline met, next up"))
            self.assertIn("BEHIND", self.final("[2026-09-23T16:00Z] Next: QA"))

        def test_keyword_exempts_only_following_non_leading_claim(self):
            now = ustamp(self.now)
            self.assertIsNone(self.final(f"{now} merged; next run [2026-09-24T01:00Z] as planned"))
            self.assertIn("2026-09-24T01:00Z in your final message: 435 min AHEAD",
                          self.final(f"{now} merged; [2026-09-24T01:00Z] retry by then"))
            self.assertIn("AHEAD", self.final("Summary: 2026-09-24T01:00Z done, next QA"))

        def test_fence_and_blockquote_exempt(self):
            txt = "x\n```\n[2099-01-01T00:00Z] in code\n```\n> [2099-01-01T00:00Z] quoted\n  > 2099-01-01 00:00 UTC"
            self.assertIsNone(self.final(txt))
            self.assertIsNone(self.final("x\n~~~~\n2099-01-01T00:00Z\n~~~~~\ny"))

        def test_unclosed_fence_is_checked(self):
            self.assertIn("AHEAD", self.final("x\n```\n[2099-01-01T00:00Z] unclosed"))
            self.assertIn("AHEAD", self.final("```x\n````\n2099-01-01T00:00Z after mismatched fence\n```\n"))

        def test_inline_code_span_exempt(self):
            # round 3 remedy: a code span is the documented way to quote a future or rejected value
            self.assertIsNone(self.final("example `2099-01-01T00:00Z` shape"))
            self.assertIsNone(self.final("example ``a ` 2099-01-01T00:00Z`` shape"))
            self.assertIn("AHEAD", self.final("unclosed `2099-01-01T00:00Z shape"))
            self.assertIn("AHEAD", self.final("`x` then 2099-01-01T00:00Z outside"))

        # -- BEHIND: status stamps only --
        def test_status_stamp_behind_blocks(self):
            r = self.ev([self.user("go"), self.asst(f"{ustamp(self.now - 20 * MIN)} x"), self.asst("done")])
            self.assertIn("20 min BEHIND", r)
            self.assertIn("20 min BEHIND", self.ev([self.user("go"), self.asst(f"- **{ustamp(self.now - 20 * MIN)}**"),
                                                    self.asst("done")]))

        def test_bullet_history_line_behind_blocks(self):
            # documented false positive: a line-leading historical stamp is a status stamp
            self.assertIn("BEHIND", self.final("History:\n- 2026-09-22 10:00 UTC incident began\nok"))
            self.assertIsNone(self.final("History: the incident began 2026-09-22 10:00 UTC.\nok"))

        def test_final_message_behind_tolerance_30(self):
            # finding (gemini r2): a long generation made a correct final status stamp read as BEHIND
            self.assertIsNone(self.final(f"{ustamp(self.now - 12 * MIN)} started long"))
            self.assertIn("35 min BEHIND", self.final(f"{ustamp(self.now - 35 * MIN)} stale"))

        # -- elapsed footer: last non-empty line only --
        def test_wrong_footer_on_last_line_blocks(self):
            for txt in ("status\nSession elapsed 08:07, 1 compaction", "x\nSession elapsed: 08:07", "x\n**Session elapsed** 08:07",
                        "x\n_Session elapsed_: 08:07\n\n", "x\nSession elapsed \u2014 08:07", "x\nsession - elapsed \u2013 08:07"):
                self.assertIn("true elapsed when written was 03:27", self.final(txt), repr(txt))
            self.assertIsNone(self.final("x\n**Session elapsed:** 03:28"))

        def test_footer_quoted_mid_message_passes(self):
            # findings (claude/gemini r2): a worker's footer, or the corrected wrong value, re-blocked
            txt = (f"{lstamp(self.now)} Worker done:\nSession elapsed 05:12\nCorrection: I wrote Session elapsed "
                   "08:07 earlier.\nSession elapsed 03:27")
            self.assertIsNone(self.final(txt))
            self.assertIsNone(self.final("x\n> Session elapsed 05:12"))
            self.assertIsNone(self.final("x\n```\nSession elapsed 05:12\n```\nSession elapsed 03:27\n> Session elapsed 05:12"))
            self.assertIsNone(self.final("x `Session elapsed 05:12` quoted"))

        def test_footer_tolerance_asymmetric(self):
            # finding (claude r4): a flat 2-minute footer tolerance false-blocked a long final wrap-up whose
            # status stamp (same provenance) was tolerated to 30 minutes
            txt = f"{ustamp(self.now)} done.\nSession elapsed 03:27"
            for gap in (3, 7, 25, 30):
                self.assertIsNone(self.final(txt, now=self.now + gap * MIN), gap)
            r = self.final(txt, now=self.now + 35 * MIN)
            self.assertIn("(last elapsed footer in your final message)", r)
            self.assertIn("35 min BEHIND", r)
            # AHEAD stays strict at 2 minutes, final message or not
            self.assertIsNone(self.final("x\nSession elapsed 03:29"))
            self.assertIn("3 min AHEAD", self.final("x\nSession elapsed 03:30"))
            # an earlier message keeps the 10-minute BEHIND window
            ref = to_us(self.now)
            self.assertEqual(check_message("Session elapsed 03:17", ref, to_us(self.start), "x", BEHIND_US), [])
            self.assertIn("11 min BEHIND",
                          check_message("Session elapsed 03:16", ref, to_us(self.start), "x", BEHIND_US)[0])
            self.assertIn("3 min AHEAD",
                          check_message("Session elapsed 03:30", ref, to_us(self.start), "x", BEHIND_US)[0])

        def test_footer_prose_collision_disclosed(self):
            # disclosed false positive: prose naming "session elapsed" before an HH:MM reads as the footer
            self.assertIsNotNone(self.final("The total session elapsed: 14:30 across all workers today."))
            self.assertIsNone(self.final("The total `session elapsed: 14:30` across all workers today."))

        def test_elapsed_unknown_lease_skipped(self):
            self.assertIsNone(evaluate({"last_assistant_message": "Session elapsed 99:00"}, self.now, None, self.sdir))

        # -- reference time --
        def test_final_message_ref_from_matching_entry(self):
            # finding (codex r2): the final message was always compared against now
            t = self.now - 20 * MIN
            ok = f"{ustamp(t)} ok\nSession elapsed 03:07"
            self.assertIsNone(self.ev([self.user("go", t), self.asst(ok, t)], last_assistant_message=ok))
            fab = f"{ustamp(self.now)} fabricated"
            self.assertIn("20 min AHEAD", self.ev([self.user("go", t), self.asst(fab, t)], last_assistant_message=fab))

        def test_entry_timestamp_is_the_reference(self):
            then = self.now - 30 * MIN
            self.assertIsNone(self.ev([self.user("go", then), self.asst(f"{lstamp(then)} early", then),
                                       self.asst(f"{lstamp(self.now)} late")]))

        def test_naive_transcript_timestamp_is_utc(self):
            then = datetime.datetime(2026, 9, 23, 17, 5, tzinfo=UTC)
            e = self.asst(f"{lstamp(then + 40 * MIN)} early but fabricated")
            e["timestamp"] = "2026-09-23T17:05:00"
            self.assertIn("40 min AHEAD", self.ev([self.user("go", then), e, self.asst(f"{lstamp(self.now)} late")]))

        def test_unparseable_transcript_timestamp_skipped_not_now(self):
            e = self.asst(f"{lstamp(self.now - 40 * MIN)} early")
            e["timestamp"] = "yesterday-ish"
            self.assertIsNone(self.ev([self.user("go"), e]))

        # -- isolation --
        def test_overflow_entry_does_not_hide_final(self):
            # finding (codex r2): ref + AHEAD overflowed on a 9999 entry and discarded the final violation
            e = self.asst("[2026-09-23T17:45Z] earlier", ts=None)
            e["timestamp"] = "9999-12-31T23:59:59Z"
            r = self.ev([self.user("go"), e], last_assistant_message="[2099-01-01T00:00Z] final")
            self.assertIn("in your final message", r)

        def test_claim_compare_is_overflow_safe(self):
            # the comparison itself is integer arithmetic: a 9999 reference cannot overflow it
            ref = to_us(datetime.datetime(9999, 12, 31, 23, 59, 59, tzinfo=UTC))
            line = "[9999-12-31T23:59Z] x"
            v = _check_claim(_CLAIM_RE.search(line), True, False, ref, BEHIND_US, "x")
            self.assertIsNone(v)
            line = "[2026-09-23T17:45Z] x"
            self.assertIn("BEHIND", _check_claim(_CLAIM_RE.search(line), True, False, ref, BEHIND_US, "x"))

        def test_year_one_local_zone_no_crash(self):
            # finding (codex r2): [0001-01-01 00:00 JST] under TZ=JST-9 raised in the conversion
            os.environ["TZ"] = "JST-9"
            time.tzset()
            r = self.final("[0001-01-01 00:00 JST] x\n[2099-01-01T00:00Z] y")
            self.assertIn("2099-01-01T00:00Z", r)
            # an invalid claim (month 13) is isolated and never discards a violation on the same message
            self.assertIn("2099-01-01T00:00Z", self.final("[2026-13-01T00:00Z] bad\n[2099-01-01T00:00Z] y"))

        def test_malformed_entries_isolated(self):
            ents = [self.user("go"), self.asst("[2099-01-01T00:00Z] x"), {"type": "assistant", "message": 42},
                    "{not json", "[1,2]"]
            self.assertIsNotNone(self.ev(ents))

        def test_pathological_inputs_linear(self):
            out = in_subprocess("(m.check_message('prose '+'`'*200000+'\\n'+'2026-09-23 '*100000+'\\n'+' '*200000+'x'"
                                "+'[2099-01-01T00:00Z]',0,None,'x',0), m.check_message('Session elapsed'*20000+"
                                "'\\n'+'Session '+'-'*200000,0,0,'x',0))", timeout=5)
            self.assertIn("AHEAD", out)

        # -- which messages --
        def test_only_after_last_genuine_user(self):
            old_bad = self.asst(f"{lstamp(self.now + 3 * 60 * MIN)} old turn")
            notif = self.user("<task-notification>done</task-notification>")
            tool_result = {"type": "user", "message": {"content": [{"type": "tool_result", "content": "x"}]}}
            ents = [old_bad, self.user("next"), self.asst("[2026-09-23T17:44Z] a"), notif, tool_result,
                    self.asst(f"{lstamp(self.now)} b")]
            self.assertIsNone(self.ev(ents))
            ents[2] = self.asst("[2026-09-23T19:00Z] a")
            self.assertIsNotNone(self.ev(ents))

        def test_quoted_block_text_is_not_a_boundary(self):
            # finding (codex r2): a notification quoting the block prefix was taken as this hook's block
            ents = [self.user("go"), self.asst("[2026-09-23T22:25Z] bad"),
                    self.user(f"<task-notification>QA tested {BLOCK_PREFIX}</task-notification>", isMeta=True),
                    self.asst("Done.")]
            self.assertIn("280 min AHEAD", self.ev(ents, last_assistant_message="Done."))

        def test_stop_hook_active_checks_intermediate_messages(self):
            ents = [self.user("go"), self.asst("[2026-09-23T22:25:00Z] x"), self.asst("Done.")]
            self.assertIn("280 min AHEAD", self.ev(ents, stop_hook_active=True, last_assistant_message="Done."))

        def test_recovery_boundary_via_state_file(self):
            bad_text = f"{lstamp(self.now + 40 * MIN)} wrong"
            ents = [self.user("go"), self.asst(bad_text)]
            self.assertTrue(self.ev(ents, last_assistant_message=bad_text).startswith(BLOCK_PREFIX))
            self.assertEqual(len(os.listdir(self.sdir)), 1)
            self.assertEqual(stat.S_IMODE(os.lstat(self.sdir).st_mode), 0o700)
            corrected = (f"{lstamp(self.now)} Correction: I previously wrote a wrong stamp.\n"
                         "Session elapsed 03:27")
            self.write([self.block_entry(), self.asst(corrected)], "a")
            self.assertIsNone(self.ev(stop_hook_active=True, last_assistant_message=corrected))
            # a fresh fabrication after the block is still caught (stop_hook_active or not)
            self.write([self.asst("[2026-09-23T20:00Z] again")], "a")
            self.assertIn("135 min AHEAD", self.ev(stop_hook_active=True, last_assistant_message="fine"))
            self.write([self.asst("[2026-09-23T20:30Z] and again")], "a")
            self.assertIn("165 min AHEAD", self.ev(last_assistant_message="fine"))

        def test_lagging_blocked_final_not_rechecked(self):
            bad_text = "[2026-09-23T20:00Z] wrong"
            self.assertIsNotNone(self.ev([self.user("go")], last_assistant_message=bad_text))
            self.write([self.asst(bad_text), self.block_entry(), self.asst(f"{lstamp(self.now)} fixed")], "a")
            self.assertIsNone(self.ev(last_assistant_message=f"{lstamp(self.now)} fixed"))

        def test_state_unusable_rechecks_whole_turn(self):
            os.mkdir(self.sdir, 0o755)
            os.chmod(self.sdir, 0o755)
            bad_text = "[2026-09-23T20:00Z] wrong"
            self.assertIsNotNone(self.ev([self.user("go"), self.asst(bad_text)], last_assistant_message=bad_text))
            self.write([self.block_entry(), self.asst("fixed")], "a")
            self.assertIn("135 min AHEAD", self.ev(last_assistant_message="fixed"))
            self.assertEqual(os.listdir(self.sdir), [])

        def test_state_offset_past_end_ignored(self):
            bad_text = "[2026-09-23T20:00Z] wrong"
            self.assertIsNotNone(self.ev([self.user("go"), self.asst("pad " * 200), self.asst(bad_text)],
                                         last_assistant_message=bad_text))
            with open(self.tr, "w") as f:  # the same transcript path replaced by a shorter transcript
                f.write(json.dumps(self.user("go")) + "\n" + json.dumps(self.asst("[2026-09-23T20:30Z] new")) + "\n")
            self.assertIn("165 min AHEAD", self.ev(last_assistant_message="ok"))

        def test_state_symlink_not_followed(self):
            self.write([self.user("go"), self.asst("[2099-01-01T00:00Z] x")])
            os.mkdir(self.sdir, 0o700)
            key = os.path.join(self.sdir, hashlib.sha256(self.tr.encode()).hexdigest())
            target = os.path.join(self.tmp, "elsewhere.json")
            size = os.path.getsize(self.tr)
            with open(self.tr, "rb") as f:
                tail = hashlib.sha256(f.read()[-TAIL_BYTES:]).hexdigest()
            with open(target, "w") as f:  # a planted VALID state that, if followed, would hide the whole transcript
                f.write(json.dumps({"v": 2, "offset": size, "tail": tail, "pending": []}))
            os.mkdir(os.path.join(self.tmp, "real"), 0o700)
            shutil.copy(target, os.path.join(self.tmp, "real", os.path.basename(key)))
            self.assertIsNone(self.ev(sdir=os.path.join(self.tmp, "real")))  # the planted state is valid if read
            os.symlink(target, key)
            self.assertIsNotNone(self.ev())

        def test_assistant_meta_entry_skipped(self):
            self.assertIsNone(self.ev([self.user("go"), self.asst("[2099-01-01T00:00Z] x", isMeta=True)]))

        def test_missing_transcript_still_checks_final_message(self):
            rc, out = run_main(json.dumps({"transcript_path": os.path.join(self.tmp, "missing.jsonl"),
                                           "last_assistant_message": "[2099-01-01T00:00Z] x"}))
            obj = json.loads(out)
            self.assertEqual((rc, obj["decision"]), (0, "block"))

        def test_subagent_stop_skipped(self):
            p = {"agent_id": "a1", "last_assistant_message": "[2099-01-01T00:00Z] x"}
            self.assertEqual(run_main(json.dumps(p)), (0, ""))

        def test_worker_kill_switch_and_garbage_silent(self):
            p = json.dumps({"last_assistant_message": "[2099-01-01T00:00Z] x"})
            self.assertEqual(run_main(p, {"ORCH_WORKER": "1"}), (0, ""))
            self.assertEqual(run_main("not json"), (0, ""))

        def test_worker_detected_by_verify_owner(self):
            # finding: orch-verify exports ORCH_VERIFY_OWNER into worker shells and never sets ORCH_WORKER
            p = json.dumps({"last_assistant_message": "[2099-01-01T00:00Z] x"})
            self.assertEqual(json.loads(run_main(p)[1])["decision"], "block")
            for value in ("guardrails", ""):
                self.assertEqual(run_main(p, {"ORCH_VERIFY_OWNER": value}), (0, ""))
            self.assertTrue(_is_worker({"ORCH_VERIFY_OWNER": ""}))
            self.assertTrue(_is_worker({"ORCH_WORKER": "1"}))
            self.assertFalse(_is_worker({"ORCH_WORKER": "0"}))
            self.assertFalse(_is_worker({}))

        def test_lease_label_portability(self):
            lease = os.path.join(self.tmp, "session-state.md")
            want = datetime.datetime(2026, 9, 23, 14, 17, 10, tzinfo=UTC)
            for label in ("sess", "S88", "a", "A" * 32):
                with open(lease, "w") as f:
                    f.write(f"Active-session: {label}-20260923T141710Z\n")
                self.assertEqual(lease_start(lease), want, label)
            for bad in ("A" * 33 + "-20260923T141710Z", "-20260923T141710Z", "S_88-20260923T141710Z",
                        "S88 20260923T141710Z", "S88-20260923T141710"):
                with open(lease, "w") as f:
                    f.write(f"Active-session: {bad}\nActive-session: sess-20200101T000000Z\n")
                self.assertIsNone(lease_start(lease), bad)

        def test_lease_discovery_precedence(self):
            proj = os.path.join(self.tmp, "proj")
            wlease = os.path.join(proj, ".working", "session-state.md")
            own = os.path.join(self.tmp, "own.md")
            os.environ["ORCH_PROJECT_ROOT"] = "/srv/proj"
            os.environ["CLAUDE_PROJECT_DIR"] = proj
            self.assertEqual(lease_file("/opt/x"), "/srv/proj/private/session-state.md")  # absent: falls through
            os.makedirs(os.path.dirname(wlease))
            with open(wlease, "w") as f:
                f.write("Active-session: S88-20260923T141710Z\n")
            self.assertEqual(lease_file("/opt/x"), wlease)
            os.environ["ORCH_LEASE_FILE"] = own
            self.assertEqual(lease_file("/opt/x"), own)
            del os.environ["ORCH_LEASE_FILE"], os.environ["ORCH_PROJECT_ROOT"]
            os.environ["CLAUDE_PROJECT_DIR"] = "rel/proj"
            self.assertEqual(lease_file("/opt/x/y"), "/opt/x/private/session-state.md")
            os.environ["CLAUDE_PROJECT_DIR"] = proj
            self.assertEqual(lease_start(lease_file("/")), datetime.datetime(2026, 9, 23, 14, 17, 10, tzinfo=UTC))

        def test_fifo_transcript_and_lease_do_not_block(self):
            fifo = os.path.join(self.tmp, "fifo")
            os.mkfifo(fifo)
            out = in_subprocess("(m.lease_start(%r), m.evaluate({'transcript_path':%r,'last_assistant_message':"
                                "'[2099-01-01T00:00Z] x'}, datetime.datetime.now(UTC), None, %r) is not None)"
                                % (fifo, fifo, self.sdir), timeout=5)
            self.assertEqual(out, "(None, True)")

        def test_inactive_lease_never_reads_history(self):
            lease = os.path.join(self.tmp, "session-state.md")
            with open(lease, "w") as f:
                f.write("Active-session: none\n## History\nActive-session: sess-20200101T000000Z\n")
            self.assertIsNone(lease_start(lease))

        def test_huge_single_record_is_fast(self):
            with open(self.tr, "w") as f:
                f.write(json.dumps(self.user("go")) + "\n")
                f.write(json.dumps({"type": "user", "message": {"content": [
                    {"type": "tool_result", "content": "x" * (32 << 20)}]}}) + "\n")
                f.write(json.dumps(self.asst("[2099-01-01T00:00Z] x")) + "\n")
            t0 = time.monotonic()
            r = evaluate({"transcript_path": self.tr}, self.now, self.start, self.sdir)
            self.assertLess(time.monotonic() - t0, 2.0)
            self.assertIsNotNone(r)

        def test_reverse_records_exact_with_offsets(self):
            lines = [b"a" * n for n in (0, 1, CHUNK - 1, CHUNK, CHUNK + 1, 3 * CHUNK + 7, 5)]
            data = b"\n".join(lines)
            with open(self.tr, "wb") as f:
                f.write(data)
            fd = os.open(self.tr, os.O_RDONLY)
            try:
                got = list(_reverse_records(fd, len(data)))
                floor = len(b"\n".join(lines[:4])) + 1
                tail = list(_reverse_records(fd, len(data), floor))
            finally:
                os.close(fd)
            self.assertEqual([r for _, r in got], [ln for ln in reversed(lines) if ln])
            for off, rec in got:
                self.assertEqual(data[off:off + len(rec)], rec)
            self.assertEqual([r for _, r in tail], [ln for ln in reversed(lines[4:]) if ln])

        # -- round 4 --
        def test_r4_blocked_text_already_in_transcript_creates_no_exception(self):
            # finding (codex r3 M1): the blocked hash was a persistent exemption across a new user boundary
            bad_text = "[2026-09-23T22:25Z] done."
            self.assertIsNotNone(self.ev([self.user("go"), self.asst(bad_text)], last_assistant_message=bad_text))
            self.write([self.block_entry(), self.asst(f"{lstamp(self.now)} fixed"), self.user("next task"),
                        self.asst(bad_text), self.asst("Done.")], "a")
            self.assertIn("280 min AHEAD", self.ev(last_assistant_message="Done."))
            # the same within one turn (no user boundary): an in-transcript blocked text is no exception
            self.assertIsNotNone(self.ev([self.user("go"), self.asst(bad_text)], last_assistant_message=bad_text))
            self.write([self.block_entry(), self.asst(bad_text), self.asst("Done.")], "a")
            self.assertIn("280 min AHEAD", self.ev(last_assistant_message="Done."))

        def test_r4_pending_consumed_once(self):
            bad_text = "[2026-09-23T20:00Z] wrong"
            self.assertIsNotNone(self.ev([self.user("go")], last_assistant_message=bad_text))  # lagging: pending
            self.write([self.asst(bad_text), self.block_entry(), self.asst("fixed")], "a")
            self.assertIsNone(self.ev(last_assistant_message="fixed"))  # consumed here
            self.write([self.asst(bad_text), self.asst("again fine")], "a")
            self.assertIn("135 min AHEAD", self.ev(last_assistant_message="again fine"))

        def test_r4_pending_dropped_at_genuine_user(self):
            bad_text = "[2026-09-23T20:00Z] wrong"
            self.assertIsNotNone(self.ev([self.user("go")], last_assistant_message=bad_text))
            self.write([self.user("new question"), self.asst(bad_text), self.asst("ok")], "a")
            self.assertIn("135 min AHEAD", self.ev(last_assistant_message="ok"))

        def test_r4_truncation_resets_boundary_and_pending(self):
            # finding (codex r3 M1): a shrunk transcript kept the hash exemption
            bad_text = "[2026-09-23T22:25Z] done."
            self.assertIsNotNone(self.ev([self.user("go"), self.asst("pad " * 300)], last_assistant_message=bad_text))
            with open(self.tr, "w") as f:
                f.write(json.dumps(self.user("go")) + "\n" + json.dumps(self.asst(bad_text)) + "\n")
            self.assertIn("280 min AHEAD", self.ev(last_assistant_message="Done."))

        def test_r4_rewritten_prefix_resets_boundary(self):
            self.assertIsNotNone(self.ev([self.user("go"), self.asst("[2026-09-23T20:00Z] a")],
                                         last_assistant_message="[2026-09-23T20:00Z] a"))
            with open(self.tr, "w") as f:  # same path, different and LONGER content: the tail hash differs
                f.write(json.dumps(self.user("go")) + "\n" + json.dumps(self.asst("[2026-09-23T20:30Z] " + "b" * 400))
                        + "\n" + json.dumps(self.asst("ok")) + "\n")
            self.assertIn("165 min AHEAD", self.ev(last_assistant_message="ok"))

        def test_r4_unfinished_trailing_record_rechecked(self):
            # finding (codex r3 m4): the sampled size acknowledged a half-written record unchecked
            rec = json.dumps(self.asst("[2026-09-23T23:00Z] DIFFERENT"))
            self.write([self.user("go")])
            with open(self.tr, "a") as f:
                f.write(rec[:40])
            self.assertIsNotNone(self.ev(last_assistant_message="[2026-09-23T22:25Z] fabricated"))
            with open(self.tr, "a") as f:
                f.write(rec[40:] + "\n" + json.dumps(self.asst(f"{lstamp(self.now)} ok")) + "\n")
            self.assertIn("315 min AHEAD", self.ev(last_assistant_message=f"{lstamp(self.now)} ok"))

        def test_r4_parseable_trailing_record_is_complete(self):
            self.write([self.user("go")])
            with open(self.tr, "a") as f:
                f.write(json.dumps(self.asst("[2026-09-23T23:00Z] x")))  # no newline yet, but whole
            self.assertIsNotNone(self.ev(last_assistant_message="[2026-09-23T22:25Z] y"))
            with open(self.tr, "a") as f:
                f.write("\n" + json.dumps(self.asst(f"{lstamp(self.now)} ok")) + "\n")
            self.assertIsNone(self.ev(last_assistant_message=f"{lstamp(self.now)} ok"))

        def test_r4_footer_last_occurrence_outside_code(self):
            # findings (codex r3 M3, gemini r3 M1, claude r3 m1): a footer not on the last line was unchecked
            for txt in ("Status.\nSession elapsed 08:07\nWORKER_STATUS: COMPLETE",
                        f"{ustamp(self.now)} ok\nSession elapsed 08:07\n---", "Session elapsed 99:00\n> done",
                        "Session elapsed 08:07\n```\nlog\n```"):
                self.assertIn("true elapsed when written was 03:27", self.final(txt), repr(txt))
            # disclosed: an unquoted worker footer pasted after the real one is the one checked
            self.assertIn("05:12", self.final("x\nSession elapsed 03:27\nWorker said: Session elapsed 05:12"))

        def test_r4_one_line_corrections_pass(self):
            # finding (codex r3 m): truthful corrections re-blocked
            self.assertIsNone(self.final("Correction: I wrote Session elapsed 08:07. Correct is Session elapsed 03:27."))
            self.assertIsNone(self.final("Correction: I previously wrote `[2026-09-23T22:25Z]`, which was wrong. "
                                         "Correct: [2026-09-23T17:45Z]."))
            self.assertIn("AHEAD", self.final("Correction: I previously wrote [2026-09-23T22:25Z], which was wrong."))

        def test_r4_keyword_must_immediately_precede(self):
            # finding (claude r3 m2): an everyday or distant keyword exempted a composed future stamp
            now = lstamp(self.now)
            for txt in (f"{now} pushed to target branch; ran at 2026-09-23 22:25 EDT",
                        f"{now} the next thing I did was finish the long build at 2026-09-23T22:25Z",
                        f"{now} due to load we finished at 2026-09-23T22:25Z"):
                self.assertIn("AHEAD", self.final(txt), txt)
            for txt in (f"{now} next run at 2026-09-24T01:00Z", f"{now} due 2026-09-24T01:00Z",
                        f"{now} deadline: **[2026-09-24T01:00Z]**", f"{now} scheduled for 2026-09-24T01:00Z",
                        f"{now} held until 2026-09-24T01:00Z", f"{now} not before 2026-09-24T01:00Z",
                        f"{now} done by 2026-09-24T01:00Z", f"{now} target date: 2026-09-24T01:00Z",
                        f"{now} Target: 2026-09-24T01:00Z", f"{now} it expires on 2026-09-24T01:00Z"):
                self.assertIsNone(self.final(txt), txt)

        def test_r4_future_fact_false_positive_and_remedy(self):
            # finding (claude r3 M): AHEAD on every zoned claim blocks a future fact; disclosed, with a remedy
            r = self.final(f"{lstamp(self.now)} The TLS cert is valid through 2027-01-01T00:00:00Z.")
            self.assertIn("AHEAD", r)
            self.assertIn("`code span`", r)
            self.assertIn("immediately precedes", r)
            self.assertIsNone(self.final(f"{lstamp(self.now)} The TLS cert is valid through `2027-01-01T00:00:00Z`."))
            self.assertIsNone(self.final(f"{lstamp(self.now)} The TLS cert expires 2027-01-01T00:00:00Z."))

        def test_r4_repeated_stamps_linear(self):
            # finding (codex r3 m5): each claim sliced the growing line prefix (quadratic)
            line = "2026-09-23T17:45Z " * 100000
            t0 = time.monotonic()
            self.assertEqual(check_message(line, to_us(self.now), None, "x", BEHIND_US), [])
            self.assertLess(time.monotonic() - t0, 1.0)
            t0 = time.monotonic()
            r = check_message("next " + "2099-01-01T00:00Z x " * 50000, to_us(self.now), None, "x", BEHIND_US)
            self.assertLess(time.monotonic() - t0, 1.0)
            self.assertEqual(len(r), 1)  # deduplicated

        def test_r5_many_distinct_violations_linear_and_bounded(self):
            # finding (codex r4): add() scanned the growing violation list (quadratic in distinct violations)
            lits = [f"2099-{1 + i % 12:02d}-{1 + (i // 12) % 28:02d}T{(i // 336) % 24:02d}:{(i // 8064) % 60:02d}Z"
                    for i in range(40000)]
            self.assertEqual(len(set(lits)), 40000)
            t0 = time.monotonic()
            r = self.final(" ".join(lits))
            self.assertLess(time.monotonic() - t0, 1.0)
            self.assertEqual(r.count(" in your final message: "), MAX_REPORTED)
            self.assertIn(f"... and {40000 - MAX_REPORTED} more distinct violation(s) not listed", r)

        def test_r4_threat_model_stated(self):
            self.assertIn("THREAT MODEL", __doc__.split("\n\n")[1])

        def test_shared_grammar_identical_to_sibling(self):
            sib = os.path.join(os.path.dirname(os.path.abspath(__file__)), "future-stamp-write.py")
            spec = importlib.util.spec_from_file_location("fsw_sibling", sib)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            self.assertEqual(mod.SCHED_KEYWORDS, SCHED_KEYWORDS)
            self.assertEqual(mod.SCHED_GAP_TOKENS, SCHED_GAP_TOKENS)
            self.assertEqual((mod.TIME_GRAMMAR, mod.ZONE_GRAMMAR), (TIME_GRAMMAR, ZONE_GRAMMAR))
            self.assertEqual((mod._SCHED_RE.pattern, mod._SCHED_RE.flags), (_SCHED_RE.pattern, _SCHED_RE.flags))
            self.assertEqual((mod._TOKEN_RE.pattern, mod._WORDCH_RE.pattern), (_TOKEN_RE.pattern, _WORDCH_RE.pattern))
            self.assertEqual(inspect.getsource(mod.sched_exempter), inspect.getsource(sched_exempter))

    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(T))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
