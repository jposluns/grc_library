#!/usr/bin/env python3
"""Session-state lease audit (gate 63).

Scans [`.working/session-state.md`](.working/session-state.md) and
enforces the WELL-FORMEDNESS of the session-concurrency lease that the
multi-session interlock relies on (design record: the design-decisions
record, "Session-concurrency safety"; the
`/orch` command's step 0 reads this file before anything else).

The lease declares which orchestrator session, if any, currently holds
the shared ``main`` state surfaces. Gate 63 accepts a lease only if the
fleet lease tool (/usr/local/bin/orch_store.py, ``lease()``) and the
fleet's standard reader (/usr/local/bin/orch_session_lease.py,
``decide()``) would also accept it, for everything they check (3b679
round 2). The file is read as bytes, must be UTF-8 and at most 65536
bytes (orch_store's MAX_FILE), and is split on LF only, as both tools
split it. Line 1 is exactly ``# Session state: grc``, and no other line
starts with ``# Session state:``. A CR anywhere (CRLF or a lone CR) is a
finding, and so is trailing whitespace on a field line.

Required fields, one per line, each a plain ``Field: value`` line (the
field name at column zero, a colon and one space, then the value; values
are matched with ASCII-only patterns). orch_store.py parses
``Active-session``, ``Status`` and ``Last-heartbeat-UTC`` only from lines
that begin with the name and ": ", so the Markdown bold form
(``**Status:** active``) is a finding naming the plain form (maintainer
ruling 2026-10-29 01:10Z); the other three fields use the same form so
the file has one style:

- ``Active-session:`` 1 to 128 printable ASCII bytes (0x21 to 0x7E, as
  orch_store requires): the active session's id, or ``none`` when no
  session holds the lease.
- ``Status:`` exactly ``active`` (a session holds the lease) or
  ``released`` (no session holds the lease; the clean-close state),
  case-sensitive; orch_store refuses every other value.
- ``Operating-mode:`` ``fully-attended``, ``attended-autonomous``,
  ``overnight-unattended``, or ``daytime-unattended``. The
  AskUserQuestion-blocking hook reads this and refuses a blocking prompt when
  the mode is unattended, so the value must always be present and current.
- ``Last-heartbeat-UTC:`` a ``YYYY-MM-DDTHH:MM:SSZ`` stamp in ASCII digits
  (``date -u +%Y-%m-%dT%H:%M:%SZ``) that is a real UTC date and time no
  later than now (the standard reader refuses a later one), refreshed at
  each PR close-out.
- ``Current-task:`` one line of free text.
- ``Worker-dispatches:`` ``none`` or a free-text summary of the
  in-flight worker fan-out (cross-referencing the scratch
  ``claims-ledger.md`` when parallel work is running).

Mentions: orch_store.py and the standard reader count every LF-split line
that matches ``\\s*Name\\s*:`` for ``Active-session``, ``Status`` or
``Last-heartbeat-UTC`` under Python's ``re.IGNORECASE`` (Unicode
whitespace and case folding, so ``Actıve-session:`` with a dotless i
counts), and accept only one, the exact field line. Each such line other
than an exact field line is a finding, wherever it is, comments included.

grc's readers (tools/session_facts.py for its three fields, and the
AskUserQuestion-blocking and stop-guard hooks for ``Operating-mode``) read
a field only from a line that starts at column zero with the exact label,
plain ``Name: `` or bold ``**Name:** ``, matching the value with spaces and
tabs only, and only when the line does not start inside an HTML comment
(3b679 round 3).

Free text (3b679 round 3): a line, or the part of a line, inside an HTML
comment (wherever the comment opens, after prose on an earlier line
included), a bullet line (-, + or * then whitespace), a numbered-list line
(ASCII digits, "." or ")", then whitespace), a heading line (one to six
"#" then whitespace or end of line), a blockquote line (">"), each after
optional spaces or tabs, and prose that contains a field name with a
colon, raise no finding. grc's readers do not read those lines, so a
``Current-task``, ``Worker-dispatches`` or ``Operating-mode`` line inside
a comment, even an exact one, is never a finding and never counts as that
field's line. One exception is kept exactly: a line the mention rule
above counts for a store field (``Active-session``, ``Status``,
``Last-heartbeat-UTC``) is still a finding unless it is the exact field
line, because orch_store.py refuses the lease; such a line starts, after
optional Unicode whitespace, with the field name in any letter case and a
colon, so only a column-zero or indented line (in a multi-line comment, a
fence or the body) can be one, never a bullet, quote or prose line or a
line opening a comment (``note <!-- Status: old -->`` and
``<!-- Status: old -->`` are not findings). An exact store field line in
a comment is counted as orch_store counts it: it is a duplicate and is
outside the header region.

The findings that remain on lines other than the exact field lines are
therefore: the title rules, a CR, a refused mention of a store field, and
a near-miss label on a line that is not free text.

Coherence rules: ``released`` requires ``Active-session: none``;
``active`` requires a non-``none`` session id.
Each field line appears exactly once (a duplicate is a finding), and
the coherence check runs unconditionally alongside the per-field value
checks, so coexisting defects are all reported in one run.

Field order: ``Active-session``, then ``Status``, then
``Last-heartbeat-UTC``. The session-start reader
(``tools/session_facts.py``) reports every session metric UNKNOWN when
those three appear in another order; this gate does not check the order.

Near-miss detection examines each LF-delimited line that is not free
text, including fences, after optional whitespace. The label is split
in one linear pass at the first colon (no backtracking pattern).
A candidate starts with zero to two stars or underscores, a nonempty
label without stars or colons (internal spaces and underscores are allowed),
zero to two stars or underscores, optional whitespace, a colon, and zero
to two stars or underscores. It is a
near miss if its normalized label casefolds to a required field name but
that field's exact pattern does not fullmatch the line (so a bold
``**Status:** active`` is a near miss of ``Status: active``). Normalization
maps Unicode category Pd, names containing HYPHEN or the word DASH, and
superscript, subscript and ordinary minus signs to "-", and folds
compatibility forms such as fullwidth letters (NFKC). Comparison removes
whitespace, underscores and dashes before casefolding.
Each near-miss line gets one finding listing every applicable label fault:
its spelling or prefix faults, a space before the colon, and bold or
emphasis markers (stars or underscores anywhere around the label, with
the plain form to write); trailing whitespace, or else wrong value
shape (which includes a separator other than one space after the colon),
is reported only when no label fault applies.
Prose and inline code before a token prevent candidate recognition.

Field labels: every line grc's readers count as an occurrence of a store
field (column zero, ``Name:`` or ``**Name:**``, outside a comment) is the
exact field line, a refused mention or a near miss, so it is reported
under one of those rules; the gate has no separate reader-label rule
since 3b679 round 3. A mention in prose never needs rewording.

Exact field lines get one location finding if their start is in an HTML
comment, a fenced block, or a later section, combining reasons (an exact
``Current-task``, ``Worker-dispatches`` or ``Operating-mode`` line in a
comment is not a field line; see Free text).
The scanner recognizes literal "<!--" and "-->" with no nesting on every
line, inside fences too, exactly as grc's readers do; an unclosed comment
extends through EOF. Fences use at least three identical
backticks or tildes after at most three ASCII spaces, with arbitrary info
text except backticks in backtick info. Closing fences use the same
character, at least the opening length, and only trailing whitespace.
An unclosed fence extends through EOF. Fence markers inside comments are
inert. Outside both, a column-zero ATX heading
(one to six "#" followed by a space, tab or end of line) starts a later
section when an earlier such line or a header-region field line precedes
it; otherwise it is the title.
This is a line scanner, not a Markdown parser: escaped comment delimiters
are still recognized; fences indented over three spaces or inside
containers are not recognized.
Labels are checked independently of those scanner limits. Existing
whole-text field counts, value checks and missing-field exit precedence
remain unchanged.

This gate guards the file's SHAPE only. It deliberately passes on both
status values: CI runs per-branch and cannot see across
concurrent sessions, so the interlock itself (HOLD-and-surface on a
live lease or a recent unmerged sibling branch) lives in the `/orch`
step-0 procedure, not in CI. A malformed lease would silently disable
that procedure, which is the failure this gate exists to catch.

The lease is opened without following a symlink (O_NOFOLLOW) and must be
a regular file (fstat), as orch_store.py and the standard reader open it;
a symlinked lease, or a FIFO, directory or device, is refused naming the
reason.

Exit codes:
    0: a well-formed lease, or an absent operational store (skip).
    1: a title, CR, size, invalid value, incoherence, duplicate,
       near-miss label, refused mention, trailing whitespace, or field
       line outside the header region.
    2: an unreadable, symlinked, non-regular or non-UTF-8 lease, or a
       required field line absent.
"""

from __future__ import annotations

import errno
import os
import re
import stat
import sys
import unicodedata
from datetime import datetime, timezone

from lint_common import REPO_ROOT, print_degraded, resolve_working


# Plain `Field: value` lines: the name at column zero, then ": " (one space),
# the form the fleet lease tool (orch_store.py) parses. ASCII-only classes, and
# no trailing whitespace (orch_store reads it into the value).
FIELD_PATTERNS = {
    "Active-session": re.compile(r"^Active-session: (\S+)$", re.MULTILINE | re.ASCII),
    "Status": re.compile(r"^Status: (\S+)$", re.MULTILINE | re.ASCII),
    "Operating-mode": re.compile(r"^Operating-mode: (\S+)$", re.MULTILINE | re.ASCII),
    "Last-heartbeat-UTC": re.compile(
        r"^Last-heartbeat-UTC: (\S+)$", re.MULTILINE | re.ASCII
    ),
    "Current-task": re.compile(
        r"^Current-task: (\S(?:.*\S)?)$", re.MULTILINE | re.ASCII
    ),
    "Worker-dispatches": re.compile(
        r"^Worker-dispatches: (\S(?:.*\S)?)$", re.MULTILINE | re.ASCII
    ),
}

# orch_store.py: the exact first line, one title line, MAX_FILE, the field
# names its lease() reads (FIELDS) and its Active-session value rule.
TITLE = "# Session state: grc"
TITLE_PREFIX = "# Session state:"
MAX_BYTES = 65536
STORE_FIELDS = ("Active-session", "Status", "Last-heartbeat-UTC")
SESSION_RE = re.compile(r"[!-~]{1,128}")
MENTION_PATTERNS = {
    name: re.compile(r"\s*%s\s*:" % re.escape(name), re.IGNORECASE)
    for name in STORE_FIELDS
}

VALID_STATUSES = {"active", "released"}

# Operating mode (the AskUserQuestion-blocking hook reads this: it blocks a blocking
# prompt when the mode contains "unattended", so the value must be reliably present).
VALID_MODES = {
    "fully-attended",
    "attended-autonomous",
    "overnight-unattended",
    "daytime-unattended",
}

HEARTBEAT_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
HEARTBEAT_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def map_dashes(label: str) -> str:
    """Map Unicode hyphens and dashes to the ASCII hyphen."""
    return "".join(
        "-" if (
            unicodedata.category(char) == "Pd"
            or "HYPHEN" in unicodedata.name(char, "")
            or "DASH" in unicodedata.name(char, "").split()
            or char in "\u207b\u208b\u2212"
        ) else char
        for char in label
    )


def normalize_label(label: str) -> str:
    """Map dashes, fold compatibility forms (NFKC), then map dashes again."""
    return map_dashes(unicodedata.normalize("NFKC", map_dashes(label)))


def label_token(line: str) -> dict[str, str] | None:
    """Split LINE's leading label at its first colon in one linear pass.

    The parts are prefix (leading whitespace), open and close (zero to two
    stars or underscores), label (nonempty, no star), space (whitespace
    before the colon) and after (zero to two stars or underscores).
    """
    colon = line.find(":")
    if colon < 0:
        return None
    head = line[:colon]
    body = head.lstrip()
    core = body.rstrip()
    stripped = core.lstrip("*_")
    open_ = core[:min(2, len(core) - len(stripped))]
    rest = core[len(open_):]
    trimmed = rest.rstrip("*_")
    close = rest[len(rest) - min(2, len(rest) - len(trimmed)):] if rest != trimmed else ""
    label = rest[:len(rest) - len(close)]
    if not label or "*" in label:
        return None
    tail = line[colon + 1:colon + 3]
    after = tail[:len(tail) - len(tail.lstrip("*_"))]
    return {"prefix": head[:len(head) - len(body)], "open": open_, "label": label,
            "close": close, "space": body[len(core):], "after": after}


# Free text (never a field and never a near miss): a bullet, a numbered-list
# item, a heading, a blockquote, or a line that opens an HTML comment.
FREE_TEXT_RE = re.compile(
    r"[ \t]*(?:[-+*](?:[ \t]|$)|[0-9]+[.)](?:[ \t]|$)|#{1,6}(?:[ \t]|$)|>|<!--)"
)
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
# HTML comment delimiters, recognized on every line (inside fences too) exactly
# as tools/session_facts.py and the two mode-reading hooks track them.
COMMENT_DELIMITER = re.compile(r"<!--|-->")


def comment_starts(lines: list[str]) -> list[bool]:
    """Return, for each line, whether it starts inside an HTML comment."""
    states: list[bool] = []
    comment = False
    for line in lines:
        states.append(comment)
        for delimiter in COMMENT_DELIMITER.finditer(line):
            comment = delimiter.group() == "<!--"
    return states


def exact_field(line: str, commented: bool) -> str | None:
    """Return the field whose exact field line LINE is, if any.

    A line that starts inside an HTML comment is never a field line for the
    fields orch_store.py does not read: grc's readers skip it.
    """
    return next(
        (field for field, pattern in FIELD_PATTERNS.items()
         if pattern.fullmatch(line) and (field in STORE_FIELDS or not commented)),
        None,
    )


def field_line_errors(text: str) -> list[str]:
    """Find near-miss labels, refused mentions and misplaced field lines."""
    invalid: list[str] = []
    fence = ""
    title_seen = False
    header_field_seen = False
    later_heading = False
    lines = text.split("\n")
    for number, (line, comment) in enumerate(zip(lines, comment_starts(lines)), 1):
        exact = exact_field(line, comment)
        free = comment or FREE_TEXT_RE.match(line) is not None
        near = None
        token = None if free else label_token(line)
        if token and exact is None:
            label = token["label"]
            normalized = normalize_label(label)
            near = next(
                (name for name in FIELD_PATTERNS
                 if re.sub(r"[\s_-]", "", normalized).casefold()
                 == name.replace("-", "").casefold()), None
            )
            if near is not None:
                faults = []
                if re.sub(r"[\s_-]", "", normalized) != near.replace("-", ""):
                    faults.append("wrong case")
                if normalized.casefold() != near.casefold():
                    faults.append("wrong separators")
                if map_dashes(label) != label:
                    faults.append("non-ASCII hyphen")
                if normalized != map_dashes(label):
                    faults.append("compatibility character")
                if token["prefix"]:
                    faults.append("leading whitespace")
                if token["space"]:
                    faults.append("space before the colon")
                if token["open"] + token["close"] + token["after"]:
                    faults.append(
                        f"bold or emphasis markers, write the plain form "
                        f"`{near}: <value>`"
                    )
                if not faults and FIELD_PATTERNS[near].fullmatch(line.rstrip()):
                    faults.append("trailing whitespace")
                if not faults:
                    faults.append("wrong value shape")
                invalid.append(
                    f"field line `{near}:` at line {number} "
                    f"has a near-miss label ({', '.join(faults)})"
                )
        if exact is not None and line != line.rstrip():
            invalid.append(
                f"field line `{exact}:` at line {number} has trailing whitespace"
            )
        for name, mention in MENTION_PATTERNS.items():
            if name not in (exact, near) and mention.match(line):
                invalid.append(
                    f"line {number} mentions the `{name}:` field in a form "
                    f"orch_store.py refuses (it counts every line that starts "
                    f"with the name and a colon, in any letter case, and "
                    f"accepts only the exact `{name}: <value>` line)"
                )

        if not comment and not fence and re.match(r"#{1,6}(?:[ \t]|$)", line):
            if title_seen or header_field_seen:
                later_heading = True
            title_seen = True
        if exact is not None:
            regions = []
            if comment:
                regions.append("HTML comment")
            if fence:
                regions.append("fenced code block")
            if later_heading:
                regions.append("later heading")
            if regions:
                invalid.append(
                    f"field line `{exact}:` at line {number} "
                    f"is outside the header region ({', '.join(regions)})"
                )
            else:
                header_field_seen = True

        marker = FENCE_RE.match(line)
        if fence:
            if marker and marker.group(1)[0] == fence[0] and (
                len(marker.group(1)) >= len(fence) and not marker.group(2).strip()
            ):
                fence = ""
        elif not comment and marker and (
            marker.group(1)[0] == "~" or "`" not in marker.group(2)
        ):
            fence = marker.group(1)
    return invalid


def check_text(
    text: str, now: datetime | None = None
) -> tuple[list[str], list[str]]:
    """Validate lease text; return (missing_field_errors, value_errors)."""
    missing: list[str] = []
    invalid: list[str] = []
    values: dict[str, str] = {}

    lines = text.split("\n")
    if lines[0] != TITLE:
        invalid.append(f"line 1 must be exactly `{TITLE}`, found {lines[0]!r}")
    titles = [number for number, line in enumerate(lines, 1)
              if line.startswith(TITLE_PREFIX)]
    if len(titles) != 1:
        invalid.append(
            f"{len(titles)} lines start with `{TITLE_PREFIX}` "
            f"(lines {', '.join(map(str, titles)) or 'none'}); exactly one may"
        )
    returns = [number for number, line in enumerate(lines, 1) if "\r" in line]
    if returns:
        invalid.append(
            f"a carriage return (CR) appears on {len(returns)} line(s), first "
            f"at line {returns[0]}; the lease is split on LF only, so write "
            f"LF line endings and no other CR"
        )
    size = len(text.encode("utf-8", "surrogatepass"))
    if size > MAX_BYTES:
        invalid.append(
            f"the lease is {size} bytes; orch_store.py refuses more than {MAX_BYTES}"
        )

    commented = comment_starts(lines)
    for field, pattern in FIELD_PATTERNS.items():
        matches = [pattern.fullmatch(line) for line, note in zip(lines, commented)
                   if exact_field(line, note) == field]
        if not matches:
            missing.append(
                f"required field line `{field}: <value>` is absent"
            )
            continue
        if len(matches) > 1:
            invalid.append(
                f"field line `{field}:` appears {len(matches)} times; "
                f"each field appears exactly once"
            )
        values[field] = matches[0].group(1)

    status = values.get("Status")
    if status is not None and status not in VALID_STATUSES:
        invalid.append(
            f"Status value `{status}` is invalid; permitted values "
            f"(case-sensitive): active, released"
        )

    mode = values.get("Operating-mode")
    if mode is not None and mode.lower() not in VALID_MODES:
        invalid.append(
            f"Operating-mode value `{mode}` is invalid; permitted values: "
            f"fully-attended, attended-autonomous, overnight-unattended, daytime-unattended"
        )

    heartbeat = values.get("Last-heartbeat-UTC")
    if heartbeat is not None and not HEARTBEAT_RE.fullmatch(heartbeat):
        invalid.append(
            f"Last-heartbeat-UTC value `{heartbeat}` is not a "
            f"YYYY-MM-DDTHH:MM:SSZ stamp (use `date -u +%Y-%m-%dT%H:%M:%SZ`)"
        )
    elif heartbeat is not None:
        try:
            stamp = datetime.strptime(heartbeat, HEARTBEAT_FORMAT).replace(
                tzinfo=timezone.utc)
        except ValueError:
            invalid.append(
                f"Last-heartbeat-UTC value `{heartbeat}` is not a real UTC "
                f"date and time"
            )
        else:
            if stamp > (now or datetime.now(timezone.utc)):
                invalid.append(
                    f"Last-heartbeat-UTC value `{heartbeat}` is later than now; "
                    f"the standard reader refuses it"
                )

    session = values.get("Active-session")
    if session is not None and not SESSION_RE.fullmatch(session):
        invalid.append(
            f"Active-session value {session!r} is not 1 to 128 printable "
            f"ASCII characters (0x21 to 0x7E)"
        )
    if status is not None and session is not None:
        if status == "released" and session.lower() != "none":
            invalid.append(
                f"Status `released` requires `Active-session: none`, "
                f"found `{session}`"
            )
        if status == "active" and session.lower() == "none":
            invalid.append(
                f"Status `{status}` requires a branch name in "
                f"Active-session, found `none`"
            )

    invalid.extend(field_line_errors(text))
    return missing, invalid


def main() -> int:
    session_state = resolve_working("session-state.md")
    if session_state is None:
        # The session-concurrency lease is maintainer-only working state. Once
        # `.working/` moves to the operational store, it is absent in public CI and
        # in an adopter clone, so the gate no-ops there (graceful degradation);
        # on the maintainer's machine the operational store (or the private-sibling fallback) supplies it and the
        # protocol is enforced.
        print(
            "OK: session-state lease not present (maintainer-only working state; "
            "skipping in public CI / adopter clone)."
        )
        print_degraded(
            "gate 63",
            "gate 63 skipped the session-state lease well-formedness check "
            "(no private store supplies session-state.md); this pass attests nothing about it."
        )
        return 0

    try:
        rel = session_state.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        rel = session_state.as_posix()

    # Bytes, decoded strictly and never newline-translated: orch_store.py
    # splits the raw bytes on LF and keeps every CR in the line. Opened without
    # following a symlink and refused unless a regular file, as orch_store.py
    # and the standard reader open it (O_NONBLOCK: a FIFO cannot hang the gate).
    try:
        fd = os.open(session_state, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
                     | os.O_CLOEXEC)
    except OSError as exc:
        reason = ("it is a symlink, which orch_store.py refuses"
                  if exc.errno == errno.ELOOP else exc.strerror or str(exc))
        print(f"ERROR: cannot read {rel}: {reason}", file=sys.stderr)
        return 2
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            print(f"ERROR: cannot read {rel}: not a regular file, which "
                  f"orch_store.py refuses", file=sys.stderr)
            return 2
        with os.fdopen(fd, "rb", closefd=False) as stream:
            text = stream.read().decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"ERROR: cannot read {rel}: {exc}", file=sys.stderr)
        return 2
    finally:
        os.close(fd)

    missing, invalid = check_text(text)

    # Report BOTH classes before exiting so coexisting defects surface in
    # one run; a missing field still takes exit-code precedence (2 over 1).
    for message in missing:
        print(f"ERROR: {rel}: {message}", file=sys.stderr)
    for message in invalid:
        print(f"FAIL: {rel}: {message}", file=sys.stderr)

    if missing:
        return 2

    if invalid:
        return 1

    print(f"OK: {rel} lease is well-formed.")
    return 0


if __name__ == "__main__":
    # 3b50b2g: this tool takes no argument; an unknown or surplus one
    # used to be ignored with exit 0, so it is refused (exit 2) before the check runs.
    import os as _os
    sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    from lint_common import strict_flags as _strict_flags
    _strict_flags(sys.argv[1:], ())
    sys.exit(main())
