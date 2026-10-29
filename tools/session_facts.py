"""Shared read-only lease facts. No log row ever selects a session start.

A field occurrence is an LF-delimited line that starts at column zero with the
exact label, plain (Name:) or bold (**Name:**), and that does not start inside
an HTML comment (3b679 round 3). Comments are tracked across lines: "<!--"
opens one and "-->" closes it wherever either appears, including a comment
that opens after prose on the same line; there is no nesting and an unclosed
comment extends through EOF. Every other line, a mention in prose or a
bullet, quoted, indented or commented copy included, is not an occurrence.
Only a unique occurrence with one value token is usable, written
plain (Name: value) or bold (**Name:** value) so a lease in either form reads;
the label and value are separated by spaces or tabs only, never a line end.
Duplicate or malformed fields make start and elapsed UNKNOWN; compactions
are UNKNOWN with a log and reported as no log without one.
Only the Active-session value can
supply a start, via the labelled orch-<UTC seconds> convention.
Missing, invalid, early or future heartbeats leave the start intact but make
elapsed UNKNOWN and compactions UNKNOWN with a log or no log without one:
activity since the start is unverified.
A heartbeat older than 24h caps both metrics at that last observation.
Accepted compaction rows count inclusively from the session start to now (or
the heartbeat when stale), reading minute-form stamps as zero seconds and
dropping rows after that window without warning, except that a minute-form
row in the start minute with nonzero start seconds makes the count UNKNOWN
with a warning because its position before or after the start is unknown.
With a known session start, a minute-form row in a stale heartbeat's minute
also makes the count UNKNOWN with a warning regardless of heartbeat seconds,
because part of that minute lies after the heartbeat.
Absent logs are distinguished from unreadable logs.
After field ambiguity and release checks, all three usable fields must occur in
Active-session, Status, Last-heartbeat-UTC order or every metric is UNKNOWN;
absent fields retain their existing handling.
Compaction rows begin with | at column zero, followed by a minute-form or
second-form UTC Z timestamp, |, compaction and |, with optional whitespace
between cells; trailing cells are ignored.
Log lines use splitlines; non-matching lines are ignored without a warning.
A matching row with an invalid calendar timestamp makes compactions UNKNOWN
and adds COMPACTIONS_UNREADABLE; unreadable or undecodable logs raise that error.
Known limit: no document structure is parsed, so matching compaction rows at
column zero inside HTML comments or fenced blocks are counted.
When a header field is absent, or written in a form the reader does not count (for example mis-cased as Active-Session
or STATUS, or with the colon outside the bold), a solitary well-formed copy of
that field elsewhere in the file is read in its place, with no warning,
wherever the order rule accepts it: an Active-session copy above Status, a
Status copy between Active-session and the heartbeat, or a heartbeat copy
anywhere below Status. Since 3b328 tools/lint-session-state.py (gate 63)
refuses each such shape tried in review, so the file fails when written.
With two or three uncounted header fields, copies can occupy other positions
accepted by the order rule, including all three in a fenced block at EOF.
"""
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def _reviewed_lint_common():
    """Load reviewed source bytes only; test symlinks before resolving paths."""
    path = Path(os.path.abspath(__file__))
    root = path.parent.parent
    helper = path.parent / "lint_common.py"
    for item in (root, path.parent, path, helper):
        if item.is_symlink():
            raise ImportError("reviewed helper is a symlink: " + str(item))
    if path.parent.name != "tools" or helper.resolve() != root.resolve() / "tools/lint_common.py":
        raise ImportError("reviewed helper outside repository tools")
    module = type(sys)("lint_common")
    module.__file__ = str(helper)
    exec(compile(helper.read_bytes(), str(helper), "exec", dont_inherit=True), module.__dict__)
    return module



resolve_working = _reviewed_lint_common().resolve_working
ISO = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?Z)"
COMPACTION = re.compile(r"\|\s*" + ISO + r"\s*\|\s*compaction\s*\|")
SECONDS = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
NAMES = ("Active-session", "Status", "Last-heartbeat-UTC")
# Plain `Name: value` (gate 63's form since 3b679) or the earlier bold `**Name:** value`.
FIELD = re.compile(r"(\*\*)?(" + "|".join(NAMES) + r"):(?(1)\*\*)[ \t]+(\S+)[ \t]*")
COMMENT_DELIMITER = re.compile(r"<!--|-->")
HEARTBEAT_MAX_AGE_SECONDS = 24 * 60 * 60


class SessionStartError(RuntimeError):
    """Reader error: snapshot reports UNKNOWN; Stop hook prints nothing and exits 0."""


def _parse(value):
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%MZ"):
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    return None


def _read(root, name, error):
    try:
        path = resolve_working(name, repo_root=root, strict=True)
        if path is None:
            return None, None
        with path.open(encoding="utf-8", newline="") as stream:
            return path, stream.read()
    except (OSError, UnicodeDecodeError, RuntimeError) as exc:
        raise SessionStartError(error + ": " + str(exc)) from exc


def _fields(text):
    occurrences = {name: [] for name in NAMES}
    first = {}
    comment = False
    for index, raw in enumerate((text or "").split("\n")):
        line = raw.removesuffix("\r")
        if not comment:
            for name in NAMES:
                if line.startswith((name + ":", "**" + name + ":**")):
                    first.setdefault(name, index)
                    occurrences[name].append(line)
        for delimiter in COMMENT_DELIMITER.finditer(line):
            comment = delimiter.group() == "<!--"
    fields, ambiguous = {}, []
    for name, lines in occurrences.items():
        if not lines:
            continue
        match = FIELD.fullmatch(lines[0]) if len(lines) == 1 else None
        if match is None or match[2] != name:
            detail = (f"appears {len(lines)} times" if len(lines) > 1
                      else "has a malformed occurrence")
            ambiguous.append(name + " " + detail)
        else:
            fields[name] = match[3]
    return fields, ambiguous, first


def session_metrics(root: Path, now: datetime | None = None):
    """Return lease facts, preserving every applicable diagnostic."""
    now = now or datetime.now(timezone.utc)
    lease = _read(root, "session-state.md", "SESSION_START_UNREADABLE")
    fields, ambiguous, first = _fields(lease[1])
    out_of_order = False
    if not ambiguous:
        session = fields.get("Active-session", "")
        status = fields.get("Status", "").lower()
        if status == "released" or session.lower() == "none":
            raise SessionStartError("SESSION_START_RELEASED: lease is released")
        out_of_order = (len(fields) == len(NAMES) and not
                        first["Active-session"] < first["Status"] < first["Last-heartbeat-UTC"])
        if out_of_order:
            ambiguous.append("fields are out of order: Active-session, Status, Last-heartbeat-UTC")
    warnings = []
    start, source, dt = "UNKNOWN", "UNKNOWN", None
    if ambiguous:
        warnings.append("AMBIGUOUS LEASE FIELD: " + ", ".join(ambiguous))
    else:
        if session and status == "active":
            match = re.fullmatch("orch-(" + SECONDS + ")", session)
            dt = _parse(match[1]) if match else None
            source = ("derived from Active-session orch-<UTC start> convention" if dt else
                      "start unknown because the lease id does not record one")
        if dt is not None:
            if dt > now:
                raise SessionStartError("SESSION_START_FUTURE: lease start is after now")
            start = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            warnings.append("SESSION_START_UNKNOWN: " + (
                "the lease id does not record a start time" if session and
                status == "active" else "no usable live lease start"))
    end = None
    stale_heartbeat = False
    if not ambiguous:
        heartbeat = fields.get("Last-heartbeat-UTC", "")
        hb = _parse(heartbeat) if re.fullmatch(SECONDS, heartbeat) else None
        unverified = ": activity since the start is unverified; elapsed and compactions UNKNOWN"
        if hb is None:
            warnings.append("MISSING OR INVALID HEARTBEAT" + unverified)
        elif dt is not None and hb < dt:
            warnings.append("HEARTBEAT BEFORE START" + unverified)
        elif hb > now:
            warnings.append("FUTURE HEARTBEAT" + unverified)
        elif (now - hb).total_seconds() > HEARTBEAT_MAX_AGE_SECONDS:
            warnings.append("STALE HEARTBEAT: lease not refreshed since " + heartbeat
                            + " (older than 24h; elapsed and compactions end at last heartbeat)")
            end = hb
            stale_heartbeat = True
        else:
            end = now
    _, content = _read(root, "degradation-watch-log.md", "COMPACTIONS_UNREADABLE")
    stamps, invalid = [], False
    start_minute_ambiguous = False
    end_minute_ambiguous = False
    for line in (content or "").splitlines():
        match = COMPACTION.match(line)
        if match:
            stamp = _parse(match[1])
            if stamp is None:
                invalid = True
            else:
                stamps.append(stamp)
                if (dt is not None and dt.second != 0 and len(match[1]) == 17
                        and stamp == dt.replace(second=0)):
                    start_minute_ambiguous = True
                if (dt is not None and stale_heartbeat and len(match[1]) == 17
                        and stamp == end.replace(second=0)):
                    end_minute_ambiguous = True
    if invalid:
        warnings.append("COMPACTIONS_UNREADABLE: invalid row timestamp")
    if start_minute_ambiguous:
        warnings.append("AMBIGUOUS COMPACTION: a minute-form compaction row in the session's "
                        "start minute cannot be placed before or after the start")
    if end_minute_ambiguous:
        warnings.append("AMBIGUOUS COMPACTION: a minute-form compaction row in the minute "
                        "of the last heartbeat cannot be placed before or after it")
    if _read(root, "session-state.md", "SESSION_START_UNREADABLE") != lease:
        raise SessionStartError("SESSION_START_STALE: lease changed while reading snapshot")
    compactions = "UNKNOWN" if content is not None or out_of_order else None
    elapsed = "UNKNOWN"
    if dt is not None and end is not None:
        seconds = int((end - dt).total_seconds())
        elapsed = f"{seconds // 3600}h{seconds % 3600 // 60}m"
        if (content is not None and not invalid and not start_minute_ambiguous
                and not end_minute_ambiguous):
            compactions = sum(dt <= stamp <= end for stamp in stamps)
    return dict(start=start, elapsed=elapsed, compaction_rows=compactions,
                lease_warning="; ".join(warnings), start_source=source)
