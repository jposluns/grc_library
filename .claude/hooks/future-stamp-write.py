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
defaults entirely; else any /opt/<project>/private/ directory, PLUS <CLAUDE_PROJECT_DIR>/.working when
CLAUDE_PROJECT_DIR is an absolute path and <CLAUDE_PROJECT_DIR>/.working/session-state.md exists as a
regular file (os.path.isfile, the same lease file clock-inject.py's lease discovery uses; a relative
CLAUDE_PROJECT_DIR is ignored, as in clock-inject.py). That lease file marks an in-repo orchestrator store: an
incidental `.working` without it (build scratch, fixtures), or with a session-state.md that is not a regular
file, is not a store. So a project keeping its store in-repo needs no env-prefixed launch and no committed
absolute host path, and ORCH_STORE_ROOT, when set, still overrides this root like every other default. For Write/Edit/MultiEdit a relative file_path is resolved against the payload cwd.

Write. Checked only when tool_input.file_path lies under a store root. The new content's lines are compared
with the existing file's lines as a MULTISET of whole lines: a new line identical to an existing line is an
unchanged carry-over and is exempt (as many times as it occurs there); every other line is checked whole. A
markdown table row is compared together with its table context (see the table-header exemption below).

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

Bash. A SIMPLE lexical rule (no heredoc or wrapper analysis, and no binding of a write to its target;
quoting is followed only to find write indicators and date substitutions): DENY when
the command text contains an explicit store path token (a /opt/<project>/private path, the
<CLAUDE_PROJECT_DIR>/.working root spelled absolutely, or an ORCH_STORE_ROOT root, standing alone: not preceded by a path character and followed by `/`, whitespace, a quote, a shell
operator, or the end) AND a WRITE indicator AND a future-dated literal. A write indicator is, outside quotes
and `#` comments, an output redirection (`>`, `>>`, `>|`, `&>`, an fd-prefixed `N>`, or `<>`) whose target
is not /dev/null (an fd duplication is not one: a `>&` whose operand, after optional whitespace and after
dequoting, is a descriptor number, a number followed by `-`, or `-`, such as `2>&1`, `>&2`, `1>& 2`, or
`>&'2'`), or a command word, by basename and in any position of any simple command, among tee, cp, mv,
install, dd, truncate, ed, and ex, or sed or perl with an in-place option (`-i`, a short cluster of letters
and digits holding i such as `-pi`, `-i.bak`, `-0777pi`, `-0pi`, or `-l0pi`, or `--in-place`) later in the
same simple command; an unterminated quote, an unterminated substitution, or a redirection with no target
counts as a write. A `$(...)` or backtick substitution, unquoted OR inside double quotes, is executable
text: its body is scanned as its own independent command stream with its own quoting context (as
date_spans() does), so `x="$(printf ... | tee <store file>)"` shows the tee write. Inside a `$(...)`, an
unquoted `case` word in COMMAND POSITION (the first word of the substitution, or the first word after a
separator `;`, `|`, `&`, a newline, `(`, `)`, or after one of the reserved words `{`, `then`, `do`, `else`,
`!`, `if`, `elif`, `while`, `until` that is itself in command position) opens a case
construct until its unquoted `esac` in command position, and while one is open a `)` is a pattern
terminator, not the substitution's end, so `$(case x in x) printf ... > <store file>;; esac)` shows its
write, while a `case` argument (`x="$(rg case <store file>)"`) is an ordinary word. A command with no write
indicator (a read such as `grep` or `rg` over the store) is allowed. The future-dated
literal must not be inside a `$(date ...)` or backtick `date ...`
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

Table-header exemption (Write, and Edit/MultiEdit on a reconstructed whole file only). A future literal in a
markdown table row is ALSO allowed when the header cell of its column carries a scheduling keyword (the same
keyword regex, on the stripped header cell text), so `| Item | Due |` over `|---|---|` over a row whose Due
cell holds a future time is allowed. This is additive: the keyword-on-line rule above is unchanged. Table
context is tracked over EVERY line of the resulting file, including unchanged carry-over lines that are not
themselves checked, so a new row under an existing header is exempt. The recognized forms follow GFM: a
header is a line holding at least one unescaped `|` (a leading pipe is optional), immediately followed by a
delimiter row (the whole stripped line is cells of an optional colon, ONE or more hyphens, and an optional
colon, pipe-separated, containing at least one pipe, leading and trailing pipes optional) with the same cell
count as the header. Each following line is a row of that table unless it ends the table: a line with no
unescaped pipe is still a row for continuation (GFM continues a table on a pipe-free line, so a later piped
row keeps its header exemption), but a pipe-free row NEVER receives a header-column exemption: it is checked
like an ordinary line, so only the keyword-on-its-own-line rule can exempt its literals; a blank line, or a line whose stripped
form starts with a list marker (`-`, `*`, or `+`, or digits then `.` or `)`), or an ATX heading (one to six `#`), each followed by
whitespace or the line end, a `>` blockquote, or a code fence (three backticks or tildes) ends it; a `#` not
forming an ATX heading (a row such as `#123 | ...`) does not. As in GFM, leading and trailing pipes are
optional on every line independently: a header with a leading pipe (`| Item | Due |`) may be followed by a
bare row (`release | ...`), and each row's columns are counted from its own leading pipe, if any.
Cells are split on unescaped `|` only (a `\\|` does not split, so it
does not shift columns); a leading pipe (only whitespace before it) opens the first cell and a trailing pipe
closes the last, so a literal lies in column k when k unescaped pipes (not counting a leading one) precede
it. The header line and the delimiter row are themselves checked normally, as ordinary lines. A row's
carry-over is keyed by its table context: a row line is an unchanged carry-over only when the same line
existed in the old file as a row under the SAME header line and delimiter row, so when an edit changes a
table's header or delimiter (repurposing a `Due` column as `Observed`, say), or moves a row into or out of
a table, EVERY row of that table is checked as changed, even rows identical to lines of the old file.
Each distinct (header, delimiter) context is given an integer id once, shared by the old- and new-file scans,
so a row's carry-over key never re-compares the header text (linear in rows, flat in header length).

Contract: allow = no stdout, exit 0; deny = the PreToolUse hookSpecificOutput permissionDecision "deny" JSON
on stdout, exit 0. Fail-OPEN (allow) on unparseable input or any internal error: a DISCIPLINE guard, not a
security boundary. Kill-switch: a pool worker, detected as env ORCH_WORKER=1 OR env ORCH_VERIFY_OWNER present
with any value, even empty (orch-verify exports the latter into its worker shells and never sets the former),
allows. Subagent calls (a payload carrying agent_id or agent_type) are DELIBERATELY checked exactly like
main-session calls, with no skip: a subagent applies store writes on the orchestrator's behalf, and a helper
can compose a timestamp that is then relayed into a record, so exempting it would open the very drift path
this hook guards. Only the pool-worker kill-switch above allows.

RESIDUAL COVERAGE (disclosed per disclose-guard-residuals). Only the ISO-like literal shape above is caught:
a compact sess-YYYYMMDDTHHMMSSZ id, an epoch number, a 12-hour or natural-language time, or a time split
across tokens is not. The keyword test is lexical: a keyword (in a word start, a path, or prose) within three
word tokens before a fabricated literal exempts it (for example "hb (next check) 2099-..."). The carry-over
test is a line multiset (a table row keyed by its header and delimiter), not an alignment: a line that
already existed elsewhere in the file, in the same table context, is exempt wherever it lands. Only the first 4 MiB of an existing file count: for a larger file a Write's carry-over
test sees only that prefix, and an Edit is checked on its fragment only, so a time-only fragment edit
(`17:45` to `22:25`) there is a MISS. The table-header exemption applies only to whole files: the fragment
path (an Edit on a file not read whole) and Bash get no table context, so a future literal in a table row
under a scheduling header cell is denied there unless a keyword immediately precedes it on its own line (a
disclosed false positive). Table continuation follows GFM's pipe rules but recognizes only a subset of its
block-interruption rules (a blank line, a list marker, an ATX heading, a blockquote, or a fence end the
table), and that mismatch errs in BOTH directions. A MISS: a line GFM would end the table on for another
reason (an HTML block or a thematic break, say) is treated as a row here, so a literal in its
scheduling-header column is exempt, as is every later non-blank line up to the next recognized block end. A
FALSE POSITIVE: a new table GFM would start after such an unrecognized block is not recognized (its header and
delimiter row read as rows of the old table), so its scheduling column gets no exemption; and a line this hook
treats as a block start where GFM would not (for example a list-marker shape GFM does not let interrupt the
table) ends the table early, so a later row loses its header exemption.
The header rule is lexical like the keyword rule: a keyword-bearing header cell
exempts every literal in its column of a row holding an unescaped pipe. A pipe-free row gets no header
exemption, so a bare scheduled value on its own pipe-free row under a scheduling header cell 0 (a GFM
one-cell row) is denied (a disclosed false positive); the remedy is a scheduling keyword immediately before
the value on that line, or a pipe that makes it a piped row. MISS (disclosed): because GFM keeps a table
open through pipe-free lines until a blank line, prose written directly under a table with no blank line
stays in it, and a later prose line that happens to hold an unescaped pipe (a shell pipe, say) is read as a
piped row, so text before its first pipe gets column 0's header exemption; leave a blank line after a
table. Bash is lexical by design. FALSE POSITIVES: the write indicator is not
bound to the store path, so a command that writes ELSEWHERE while merely naming a store path and carrying a
future literal is denied (for example a `cp -t /elsewhere` whose SOURCE is in the store, `grep ... <store
file> > /dev/shm/out`, or a store path in a comment of a command that writes elsewhere), as is a command
where a write-command name is only an argument (`grep tee <store file>`) or a `>` sits unquoted in a heredoc
body, or where an `i` in a sed or perl short cluster is really an option argument rather than the in-place
switch (`sed -ei...`, `perl -Mstrict`); rephrase or split the command. MISSES: a store path reached through a variable, a glob,
`cd` (a relative path is never resolved, so a Bash write to `.working/...` is missed), a symlink, a `..` or doubled-slash spelling; a write
through a program or script with no write indicator in the command text (`python -c`, `python3 script.py`,
`awk -i inplace`, `rsync`, `ln`, an editor, a heredoc-fed interpreter), or a script that writes internally;
a future literal inside a `$(date ...)` span in a quoted heredoc body or a
comment (text the shell never runs); a literal built from parts; and a write via another tool
(NotebookEdit). The .working root is taken from the hook process's CLAUDE_PROJECT_DIR and checked for
existence of its session-state.md at each call; when that variable is unset or relative, or the lease file
is absent or not a regular file, or the store is reached by a different spelling, an in-repo store is not
covered. Because CLAUDE_PROJECT_DIR is set automatically by the host, ANY project whose `.working/` holds a
regular session-state.md file is treated as a store by this hook, whatever else that `.working` is used for;
set ORCH_STORE_ROOT to override. A heredoc body is scanned for quotes like command text, so an apostrophe there can hide a
later `$(date ...)` span, which then fails toward denying. date_spans() is not case-aware: a case pattern
`)` inside a `$(date ...)` or enclosing substitution ends that span early, which only shrinks the exempt
span (fails toward denying); the write test's case tracking is a lexical command-position rule, not a
parse: it does not follow a backtick frame (where `)` never closes anyway), and exotic placements (a `case`
after a leading redirection or after an unlisted reserved word such as `time`, a pattern word spelled `case`
after `;;`, or a keyword produced by an alias or eval) are not emulated; such a construct can end the
substitution early and hide a write inside it (a MISS) or leave it unterminated (a false deny). A wrong host clock is enforced faithfully.

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
    """(explicit roots, whether the /opt/<project>/private default applies); see the docstring."""
    env = os.environ.get("ORCH_STORE_ROOT")
    if env:
        return [os.path.normpath(r) for r in env.split(os.pathsep) if r and os.path.isabs(r)], False
    proj = os.environ.get("CLAUDE_PROJECT_DIR")
    if proj and os.path.isabs(proj):
        cand = os.path.normpath(os.path.join(proj, ".working"))
        # the lease file marks an in-repo orchestrator store (clock-inject.py's lease discovery uses it too);
        # an incidental .working (build scratch, fixtures) without it is not a store
        if os.path.isfile(os.path.join(cand, "session-state.md")):
            return [cand], True
    return [], True


def under_store(path, cwd=None):
    if not isinstance(path, str) or not path:
        return False
    if not os.path.isabs(path):
        if not cwd:
            return False
        path = os.path.join(cwd, path)
    p = os.path.normpath(path)
    roots, opt_default = store_roots()
    if any(p == r or p.startswith(r.rstrip("/") + "/") for r in roots):
        return True
    return opt_default and bool(_OPT_STORE_RE.match(p))


def names_store_path(cmd):
    """True when the command text contains an explicit store path token (lexical; see the docstring)."""
    roots, opt_default = store_roots()
    if any(re.search(_TOKEN_BEFORE + re.escape(r.rstrip("/") or "/") + _TOKEN_AFTER, cmd) for r in roots):
        return True
    return opt_default and _OPT_TOKEN_RE.search(cmd) is not None


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


def future_on_line(line, now_us, base=0, in_subst=None, cache=None, extra_exempt=None):
    """Future literals on one line not immediately preceded by a scheduling keyword. `in_subst(pos)` is true
    for a literal starting at absolute position base+pos that lies inside a date substitution; `cache` maps
    a literal to its converted value so a repeated literal is converted once; `extra_exempt(pos)`, when
    given, is an ADDITIONAL exemption for a literal starting at line position pos (the table-header rule)."""
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
        if not sched(m.start()) and not (extra_exempt is not None and extra_exempt(m.start())):
            seen.add(lit)
            found.append(lit)
    return found


# a GFM delimiter row (whole stripped line): cells of optional colon, 1+ hyphens, optional colon
_DELIM_ROW_RE = re.compile(r"\|?[ \t]*:?-+:?[ \t]*(?:\|[ \t]*:?-+:?[ \t]*)*\|?")


def _pipes(line):
    """Positions of the unescaped `|` characters of `line` (a `\\|` does not split a cell). Linear."""
    return [i for i, c in enumerate(line) if c == "|" and (i == 0 or line[i - 1] != "\\")]


def _leading_pipe(line, pipes):
    """1 when the first unescaped pipe of `line` has only whitespace before it (a leading pipe), else 0."""
    return 1 if pipes and not line[:pipes[0]].strip() else 0


def _table_cells(line, pipes):
    """The cell texts of a table line split on its unescaped pipes (`pipes`, non-empty): a leading pipe opens
    the first cell and a trailing pipe closes the last, so neither adds an empty cell."""
    bounds = [-1] + pipes + [len(line)]
    cells = [line[bounds[k] + 1:bounds[k + 1]] for k in range(len(bounds) - 1)]
    if not line[pipes[-1] + 1:].strip():
        cells.pop()
    return cells[_leading_pipe(line, pipes):]


def _delim_cell_count(s):
    """The cell count of a stripped GFM delimiter row (it must contain a pipe), else None."""
    if "|" not in s or not _DELIM_ROW_RE.fullmatch(s):
        return None
    s = s[1:] if s.startswith("|") else s
    s = s[:-1] if s.endswith("|") else s
    return s.count("|") + 1


def _row_exempter(line, pipes, sched_cols):
    """A predicate pos -> True when position `pos` of table row `line` lies in a column whose header cell
    carries a scheduling keyword (column k: k unescaped pipes, not counting a leading one, precede pos)."""
    lead = _leading_pipe(line, pipes)

    def exempt(pos):
        return (bisect.bisect_right(pipes, pos) - lead) in sched_cols
    return exempt


_BLOCK_START_RE = re.compile(r"(?:[-*+]|[0-9]+[.)]|#{1,6})(?:[ \t]|$)|>|```|~~~")


def _ends_table(line, pipes):
    """True when `line` cannot continue the table it follows: it is blank or starts a new block (a list
    marker, an ATX heading (`#` to `######` then whitespace or the line end), a `>` blockquote, or a code
    fence). A pipe-free line continues the table as a one-cell row (GFM), so `pipes` does not decide it; a
    leading pipe is optional on a row whatever the header had (GFM)."""
    s = line.strip()
    return not s or bool(_BLOCK_START_RE.match(s))


def _table_walk(text, tables=True, ids=None):
    """Yield (line, ctx, extra) for every line of `text`, linearly. ctx is an integer id of the table context
    (header line, delimiter row) for a row of a markdown table (see the docstring's GFM forms), assigned once
    per distinct context through `ids` (a dict shared across scans, so equal contexts get equal ids and a row
    key never compares the header text again), and None for any other line (a header and a delimiter row
    included); extra is the row's header-keyword exempter, or None (always None for a pipe-free row, which
    keeps the table open but gets no header exemption). With tables False, every line is
    (line, None, None)."""
    ids = {} if ids is None else ids
    prev, ctx, sched = None, None, None  # prev: (line, pipes) of a possible header; ctx, sched: table
    for line in text.splitlines():
        if not tables:
            yield line, None, None
            continue
        pipes = _pipes(line)
        if ctx is not None:
            if not _ends_table(line, pipes):
                # only a row with an unescaped pipe gets the header exemption; a pipe-free row keeps the
                # table open (GFM) but is checked as an ordinary line
                yield line, ctx, (_row_exempter(line, pipes, sched) if sched and pipes else None)
                continue
            ctx = None  # a new block (see _ends_table) ends the table
        if prev is not None:
            ncols = _delim_cell_count(line.strip())
            if ncols is not None:
                hcells = _table_cells(*prev)
                if ncols == len(hcells):
                    ctx = ids.setdefault((prev[0], line), len(ids))
                    sched = {k for k, c in enumerate(hcells) if _SCHED_RE.search(c.strip())}
                    prev = None
                    yield line, None, None
                    continue
        prev = (line, pipes) if pipes else None
        yield line, None, None


def future_in_changed_lines(new, old, now_us, tables=True):
    """Future observed-time literals on whole lines of `new` that are not unchanged carry-overs from `old`.
    With `tables`, markdown-table context is tracked over EVERY line of `new` (carry-overs included, though
    they are not checked), so a row's literal is also exempt when its column's header cell holds a keyword;
    and a row is a carry-over only under the same header and delimiter it had in `old`."""
    ids = {}  # table context -> integer id, shared by both scans (a row key never re-compares a header)
    carry = collections.Counter((ctx, line) for line, ctx, _x in _table_walk(old or "", tables, ids))
    bad, seen, cache = [], set(), {}
    for line, ctx, extra in _table_walk(new or "", tables, ids):
        if carry[(ctx, line)] > 0:
            carry[(ctx, line)] -= 1
            continue
        for lit in future_on_line(line, now_us, cache=cache, extra_exempt=extra):
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


WRITE_COMMANDS = frozenset(("tee", "cp", "mv", "install", "dd", "truncate", "ed", "ex"))
INPLACE_COMMANDS = frozenset(("sed", "perl"))
_INPLACE_OPT_RE = re.compile(r"-[A-Za-z0-9]*i|--in-place(?:=|$)")
_FD_DUP_RE = re.compile(r"[0-9]+-?|-")
_SHELL_SEPARATORS = ";|&\n"
_CMD_PREFIX_WORDS = frozenset(("{", "then", "do", "else", "!", "if", "elif", "while", "until"))  # the next word is again in command position


def _shell_tokens(cmd):
    """Lexical shell token STREAMS of `cmd` in ONE linear pass: a list holding the top-level stream and one
    stream per `$(...)` or backtick substitution, each a list of ("w", dequoted word), ("s",) for a separator
    (`;`, `|`, `&`, `(`, `)`, a newline), and ("r", dup) for an output redirection (dup True for the `>&`
    form, whose operand may name a descriptor). A substitution, unquoted or inside double quotes, is its own
    frame with its own quoting context (as in date_spans()), its body a separate stream, and it leaves a `$`
    placeholder in the enclosing word. Single quotes and $'...' make everything literal; double quotes make
    every operator literal except a substitution opener; a backslash escapes the next character; an unquoted
    `#` at a word start comments out the rest of its line. Inside a `$(...)`, an unquoted `case` word in
    command position opens a case construct until its unquoted `esac` in command position, and while one is
    open a `)` is a pattern terminator (a separator), not the end of the substitution. Command position is
    the first word of the substitution or the first word after a separator, `(`, `)`, or a reserved word
    (`{`, `then`, `do`, `else`, `!`, `if`, `elif`, `while`, `until`) that is itself in command position, so a
    `case` argument (`rg case <file>`, `rg then case <file>`) is not a keyword. Returns None for an
    unterminated quote or substitution."""
    # frame: [kind, toks, word chars, has word, in double quotes, paren depth, open cases, word quoted,
    # command position]; kind in "top", "$(", "`"
    streams, stack, i, n = [], [["top", [], [], False, False, 0, 0, False, True]], 0, len(cmd)

    def flush(f):
        if f[3]:
            w = "".join(f[2])
            f[1].append(("w", w))
            if f[0] == "$(" and not f[7] and f[8]:
                if w == "case":
                    f[6] += 1
                elif w == "esac" and f[6]:
                    f[6] -= 1
            f[8] = f[8] and not f[7] and w in _CMD_PREFIX_WORDS  # only a reserved word keeps the position
        f[2], f[3], f[7] = [], False, False

    def sep(f):
        f[1].append(("s",))
        f[8] = True

    while i < n:
        f, c = stack[-1], cmd[i]
        if c == "\\":
            if i + 1 < n and cmd[i + 1] != "\n":
                f[2].append(cmd[i + 1])
                f[3] = f[7] = True
            i += 2
            continue
        if c == "`" and f[0] == "`":
            flush(f)
            streams.append(f[1])
            stack.pop()
            i += 1
            continue
        if c == "`" or (c == "$" and cmd.startswith("$(", i)):
            f[2].append("$")  # the substitution's value, in the enclosing word
            f[3] = f[7] = True
            stack.append([c if c == "`" else "$(", [], [], False, False, 0, 0, False, True])
            i += 1 if c == "`" else 2
            continue
        if f[4]:
            if c == '"':
                f[4] = False
            else:
                f[2].append(c)
            i += 1
            continue
        if c == "'" or (c == "$" and cmd.startswith("$'", i)):
            if c == "$":
                i += 1
            esc, j = c == "$", i + 1
            while j < n and cmd[j] != "'":
                if esc and cmd[j] == "\\" and j + 1 < n:
                    j += 1
                f[2].append(cmd[j])
                j += 1
            if j >= n:
                return None
            f[3], f[7], i = True, True, j + 1
            continue
        if c == '"':
            f[3] = f[4] = f[7] = True
            i += 1
            continue
        if c == "#" and not f[3]:
            nl = cmd.find("\n", i)
            i = n if nl < 0 else nl
            continue
        if c == ">" or (c == "&" and cmd.startswith("&>", i)):
            flush(f)
            amp = c == "&"
            i += 2 if amp else 1
            dup = False
            if i < n and cmd[i] in ">|":
                i += 1
            elif not amp and i < n and cmd[i] == "&":
                i += 1
                dup = True
            f[1].append(("r", dup))
            continue
        if c == ")" and f[0] == "$(" and f[5] == 0:
            flush(f)
            if f[6]:  # a case pattern terminator inside the substitution, not its closing paren
                sep(f)
                i += 1
                continue
            streams.append(f[1])
            stack.pop()
            i += 1
            continue
        if c in "()":
            if f[0] == "$(":
                f[5] += 1 if c == "(" else -1
            flush(f)
            sep(f)
            i += 1
            continue
        if c in _SHELL_SEPARATORS:
            flush(f)
            sep(f)
            i += 1
            continue
        if c.isspace() or c == "<":
            flush(f)
            i += 1
            continue
        f[2].append(c)
        f[3] = True
        i += 1
    if len(stack) > 1 or stack[0][4]:
        return None
    flush(stack[0])
    streams.append(stack[0][1])
    return streams


def bash_writes(cmd):
    """True when the command text shows a WRITE indicator (lexical; see the docstring) in ANY of its token
    streams (the top level or any substitution body, each with independent state): an unquoted output
    redirection (`>`, `>>`, `>|`, `&>`, `N>`, `<>`) whose target is not /dev/null and not a `>&` descriptor
    duplication; or, in any simple command, a word (its basename) among WRITE_COMMANDS, or sed or perl
    followed in the same simple command by an in-place option (`-i`, a letter-and-digit short cluster
    holding i such as `-pi`, `-i.bak`, or `-0777pi`, or `--in-place`). An unterminated quote or
    substitution, or a redirection with no target, fails toward writing (True)."""
    streams = _shell_tokens(cmd)
    return True if streams is None else any(_stream_writes(toks) for toks in streams)


def _stream_writes(toks):
    """True when one token stream of _shell_tokens shows a write indicator (see bash_writes)."""
    inplace, target = False, None  # target: None, or the dup flag of a redirection awaiting its operand
    for t in toks:
        if t[0] == "r":
            if target is not None:
                return True
            target = t[1]
            continue
        if t[0] == "s":
            if target is not None:
                return True
            inplace = False
            continue
        w = t[1]
        if target is not None:
            if w != "/dev/null" and not (target and _FD_DUP_RE.fullmatch(w)):
                return True
            target = None
            continue
        base = os.path.basename(w)
        if base in WRITE_COMMANDS:
            return True
        if base in INPLACE_COMMANDS:
            inplace = True
        elif inplace and _INPLACE_OPT_RE.match(w):
            return True
    return target is not None


def bash_future(cmd, now_us):
    """Future observed-time literals in a Bash command that names a store path AND shows a write
    indicator (else [])."""
    if not names_store_path(cmd) or not bash_writes(cmd):
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
        # fragment is checked on its own lines with no table context; a time-only fragment here is a disclosed miss
        bad, seen = [], set()
        for old, new, _every in edits:
            for lit in future_in_changed_lines(new, old, now_us, tables=False):
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
                "is checked lexically: a command naming a store path that also shows a write (a `>` redirection "
                "not to /dev/null, or tee, cp, mv, install, dd, truncate, ed, ex, or sed/perl -i) is denied when it "
                "carries a future literal outside a $(date ...) substitution; a read-only command is allowed."
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
            self._proj = os.environ.pop("CLAUDE_PROJECT_DIR", None)
            os.environ["TZ"] = "EST5EDT,M3.2.0,M11.1.0"  # pinned zone, no tzdata needed
            time.tzset()
            base = "/dev/shm" if os.path.isdir("/dev/shm") else None
            self.tmp = tempfile.mkdtemp(prefix="clk.", dir=base)
            self.now = datetime.datetime(2026, 9, 23, 17, 45, 0, tzinfo=UTC)
            self.store = "/opt/proj/private/session-state.md"

        def tearDown(self):
            shutil.rmtree(self.tmp, ignore_errors=True)
            for k, v in (("TZ", self._tz), ("ORCH_STORE_ROOT", self._root), ("CLAUDE_PROJECT_DIR", self._proj)):
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

        def test_project_working_root(self):
            # peer request: an in-repo store at <CLAUDE_PROJECT_DIR>/.working, added to the /opt default
            work = os.path.join(self.tmp, ".working")
            fp = os.path.join(work, "x.md")
            os.environ["CLAUDE_PROJECT_DIR"] = self.tmp
            self.assertFalse(under_store(fp))  # directory absent: not a store
            self.assertEqual(self.ev("Bash", command=f"echo 2099-01-01T00:00Z >> {fp}"), [])
            os.makedirs(work)
            self.assertFalse(under_store(fp))  # an incidental .working without the lease file: not a store
            self.assertEqual(self.ev("Write", file_path=fp, content="2099-01-01T00:00Z"), [])
            lease = os.path.join(work, "session-state.md")
            os.makedirs(lease)
            self.assertFalse(under_store(fp))  # session-state.md is a directory, not a regular file: not a store
            os.rmdir(lease)
            with open(lease, "w") as f:
                f.write("lease\n")
            self.assertTrue(under_store(fp))
            self.assertTrue(under_store(".working/x.md", cwd=self.tmp))
            self.assertFalse(under_store(os.path.join(self.tmp, ".workingx", "x.md")))
            self.assertTrue(self.ev("Write", file_path=fp, content="2099-01-01T00:00Z"))
            self.assertTrue(self.ev("Bash", command=f"echo 2099-01-01T00:00Z >> {fp}"))
            self.assertTrue(under_store(self.store))  # the /opt/<project>/private default still applies
            self.assertTrue(self.ev("Bash", command="echo 2099-01-01T00:00Z >> /opt/proj/private/s.md"))
            os.environ["CLAUDE_PROJECT_DIR"] = os.path.relpath(self.tmp)  # relative: ignored
            self.assertFalse(under_store(fp))
            self.assertTrue(under_store(self.store))
            os.environ["CLAUDE_PROJECT_DIR"] = self.tmp
            other = tempfile.mkdtemp(dir=self.tmp)
            os.environ["ORCH_STORE_ROOT"] = other  # the override still replaces every default
            self.assertFalse(under_store(fp))
            self.assertFalse(under_store(self.store))
            self.assertEqual(self.ev("Bash", command=f"echo 2099-01-01T00:00Z >> {fp}"), [])
            self.assertTrue(under_store(os.path.join(other, "a.md")))

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
            # documented: the write indicator is not bound to the store path, so a write ELSEWHERE is denied
            for cmd in ("cp -t /dev/shm/ /opt/proj/private/report-2099-01-01T00:00Z.md",
                        "grep 2099-01-01T00:00Z /opt/proj/private/s.md > /dev/shm/out",
                        "grep tee /opt/proj/private/s.md 2099-01-01T00:00Z",
                        "echo 'hb 2099-01-01T00:00Z' >> /opt/proj/guardrails/n.md # cf /opt/proj/private/old.md"):
                self.assertTrue(self.ev("Bash", command=cmd), cmd)

        def test_r7_read_only_store_inspection_allowed(self):
            # peer finding (grc, MEDIUM): a read-only command naming a store path was denied; the old
            # documented false positives for a read (grep, a quoted `>` argument) now pass
            for cmd in ("rg -n '2099-01-01T00:00Z' /opt/proj/private/pending-decisions.md",
                        "grep -c 2099-01-01T00:00Z /opt/proj/private/s.md",
                        "grep -n 2099-01-01T00:00Z /opt/proj/private/s.md 2>/dev/null | head -5",
                        "rg 2099-01-01T00:00Z /opt/proj/private/ 2>&1 | wc -l",
                        "cat /opt/proj/private/defect.md | grep '2099-01-01T00:00Z >> x'",
                        "printf '%s\\n' '>' /opt/proj/private/s.md 2099-01-01T00:00Z",
                        "sed -n '/2099-01-01T00:00Z/p' /opt/proj/private/s.md",
                        "ls /opt/proj/private/ # 2099-01-01T00:00Z > x",
                        "rg -i 2099-01-01T00:00Z /opt/proj/private/s.md | sed 's/a/b/'"):
                self.assertEqual(self.ev("Bash", command=cmd), [], cmd)

        def test_r7_write_indicators_still_denied(self):
            for cmd in ("echo 2099-01-01T00:00Z >> /opt/proj/private/s.md",
                        "echo 2099-01-01T00:00Z>/opt/proj/private/s.md",
                        "echo 2099-01-01T00:00Z 1> /opt/proj/private/s.md",
                        "echo 2099-01-01T00:00Z &> /opt/proj/private/s.md",
                        "echo 2099-01-01T00:00Z >| /opt/proj/private/s.md",
                        "echo 2099-01-01T00:00Z >&/opt/proj/private/s.md",
                        "printf 'hb 2099-01-01T00:00Z' | tee -a /opt/proj/private/s.md",
                        "printf 'hb 2099-01-01T00:00Z' | '/usr/bin/tee' /opt/proj/private/s.md",
                        "cp /dev/shm/x /opt/proj/private/2099-01-01T00:00Z.md",
                        "mv /dev/shm/2099-01-01T00:00Z.md /opt/proj/private/",
                        "install -m 600 /dev/shm/2099-01-01T00:00Z /opt/proj/private/x",
                        "truncate -s 0 /opt/proj/private/2099-01-01T00:00Z.md",
                        "sed -i.bak 's/x/2099-01-01T00:00Z/' /opt/proj/private/s.md",
                        "sed -Ei 's/x/2099-01-01T00:00Z/' /opt/proj/private/s.md",
                        "sed --in-place 's/x/2099-01-01T00:00Z/' /opt/proj/private/s.md",
                        "perl -pi -e 's/x/2099-01-01T00:00Z/' /opt/proj/private/s.md",
                        "echo 'unterminated 2099-01-01T00:00Z /opt/proj/private/s"):
                self.assertTrue(self.ev("Bash", command=cmd), cmd)
            # sed/perl without an in-place option, and a -i on another command, are reads
            self.assertFalse(bash_writes("sed 's/a/b/' /opt/p/private/s.md"))
            self.assertFalse(bash_writes("grep -i x f; sed 's/a/b/' g"))
            self.assertTrue(bash_writes("grep x f; sed -i 's/a/b/' g"))
            self.assertFalse(bash_writes("cmd 2>&1 >&2 1>&- | cat"))
            self.assertFalse(bash_writes("echo \\> x"))
            self.assertTrue(bash_writes("cat f >"))

        def test_r7_bash_writes_is_linear(self):
            t0 = time.monotonic()
            for cmd in ("'" + "a" * 400000, "x " * 200000, "2>&1 " * 100000, "\\" * 400000, "$'\\'" * 100000):
                bash_writes(cmd)
            self.assertLess(time.monotonic() - t0, 2.0)

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

        # -- round 6: markdown-table header exemption --
        def tw(self, *lines):
            return self.ev("Write", file_path=self.store, content="\n".join(lines) + "\n")

        def test_r6_table_header_keyword_column_allowed(self):
            # finding (codex r5 MAJOR): the scheduling keyword lived in the header cell, not on the row's line
            self.assertEqual(self.tw("| Item | Due | Owner |", "|---|---|---|", "| x | 2099-01-01T00:00Z | me |"), [])
            self.assertEqual(self.tw("| Item | Next run |", "| :--- | ---: |", "| x | 2099-01-01T00:00Z |",
                                     "| y | 2099-02-01T00:00Z |"), [])
            self.assertEqual(self.tw("  | Item | Due", "  ---|:---:", "  | x | 2099-01-01T00:00Z"), [])

        def test_r6_table_non_keyword_column_denied(self):
            self.assertEqual(self.tw("| Item | Seen |", "|---|---|", "| x | 2099-01-01T00:00Z |"),
                             ["2099-01-01T00:00Z"])
            self.assertEqual(self.tw("| Due | Seen |", "|---|---|", "| 2099-01-01T00:00Z | 2099-02-01T00:00Z |"),
                             ["2099-02-01T00:00Z"])

        def test_r6_table_ended_row_denied(self):
            self.assertTrue(self.tw("| Item | Due |", "|---|---|", "| x | 2099-01-01T00:00Z |", "",
                                    "| y | 2099-02-01T00:00Z |"))
            # round 11: a pipe-free line is a one-cell row (GFM), so it no longer ends the table
            self.assertEqual(self.tw("| Item | Due |", "|---|---|", "text", "| y | 2099-02-01T00:00Z |"), [])

        def test_r6_table_without_delimiter_denied(self):
            for lines in (("| Item | Due |", "| x | 2099-01-01T00:00Z |"),
                          ("| Item | Due |", "|---|", "| x | 2099-01-01T00:00Z |"),  # cell count mismatch
                          ("| Item | Due |", "", "|---|---|", "| x | 2099-01-01T00:00Z |"),
                          ("| Item | Due |", "|---|---|x", "| x | 2099-01-01T00:00Z |"),  # not a delimiter row
                          ("| Item | Due |", "| |---|", "| x | 2099-01-01T00:00Z |"),  # an empty delimiter cell
                          ("Item Due", "---|---", "x | 2099-01-01T00:00Z"),  # a header needs an unescaped pipe
                          ("Item \\| Due", "---|---", "x | 2099-01-01T00:00Z")):
                self.assertTrue(self.tw(*lines), lines)

        def test_r6_table_escaped_pipe_does_not_shift_columns(self):
            self.assertEqual(self.tw("| Item | Due |", "|---|---|", "| a \\| b | 2099-01-01T00:00Z |"), [])
            self.assertTrue(self.tw("| Item \\| Due | Seen |", "|---|---|", "| x | 2099-01-01T00:00Z |"))
            self.assertTrue(self.tw("| Seen | Due |", "|---|---|", "| a \\| 2099-02-01T00:00Z | c |"))

        def test_r6_table_header_carried_over_edit_allowed(self):
            fp = self.store_file("# log\n| Item | Due |\n|---|---|\n| a | 2026-09-01T00:00Z |\n")
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="| a | 2026-09-01T00:00Z |",
                                     new_string="| a | 2026-09-01T00:00Z |\n| b | 2099-01-01T00:00Z |"), [])
            fp = self.store_file("| Item | Seen |\n|---|---|\n| a | 2026-09-01T00:00Z |\n")
            self.assertTrue(self.ev("Edit", file_path=fp, old_string="| a | 2026-09-01T00:00Z |",
                                    new_string="| a | 2026-09-01T00:00Z |\n| b | 2099-01-01T00:00Z |"))

        def test_r6_table_context_absent_on_fragment_path_and_bash(self):
            # disclosed: no table context on the Bash path or the fragment path
            self.assertTrue(self.ev("Bash", command="printf '| Item | Due |\n|---|---|\n| x | 2099-01-01T00:00Z |\n' "
                                                    ">> /opt/proj/private/s.md"))
            fp = self.store_file("x\n" * (EXISTING_MAX_BYTES // 2 + 1))  # over the cap: the fragment path
            self.assertTrue(self.ev("Edit", file_path=fp, old_string="x",
                                    new_string="| Item | Due |\n|---|---|\n| x | 2099-01-01T00:00Z |"))

        def test_r6_table_scan_is_linear(self):
            rows = ["| x | 2099-01-01T00:00Z |"] * 50000
            t0 = time.monotonic()
            self.assertEqual(self.tw("| Item | Due |", "|---|---|", *rows), [])
            self.assertEqual(self.tw(*(["| a | b |"] * 50000)), [])
            self.assertLess(time.monotonic() - t0, 1.0)

        # -- round 7 (codex round-6 findings) --
        def test_r7_dq_substitution_write_seen(self):
            # finding 1 (HIGH): a write inside a double-quoted command substitution was hidden
            for cmd in ("result=\"$(printf '%s\\n' 'heartbeat: 2099-01-01T00:00Z' | tee /opt/p/private/s.md)\"",
                        "r=\"`printf 'hb 2099-01-01T00:00Z' | tee /opt/p/private/s.md`\"",
                        "r=\"x $(echo \"$(printf 'hb 2099-01-01T00:00Z' > /opt/p/private/s.md)\") y\"",
                        "r=\"$(sed -i 's/a/2099-01-01T00:00Z/' /opt/p/private/s.md)\"",
                        "r=\"$(echo ')' | tee /opt/p/private/s.md) 2099-01-01T00:00Z\"",
                        "echo \"$(printf 2099-01-01T00:00Z\" > /opt/p/private/s.md"):  # unterminated
                self.assertTrue(self.ev("Bash", command=cmd), cmd)
            # substitutions stay independent: a write-free substitution and quoted text remain reads
            for cmd in ("n=\"$(grep -c 2099-01-01T00:00Z /opt/p/private/s.md)\"",
                        "grep \"$(echo 2099-01-01T00:00Z)\" /opt/p/private/s.md 2>&1",
                        "grep '$(tee x)' /opt/p/private/s.md 2099-01-01T00:00Z",
                        "grep \"\\$(tee x)\" /opt/p/private/s.md 2099-01-01T00:00Z",
                        "echo \"$(sed 's/a/b/' /opt/p/private/s.md)\" -i 2099-01-01T00:00Z"):
                self.assertEqual(self.ev("Bash", command=cmd), [], cmd)
            self.assertTrue(bash_writes("sed \"$(echo x)\" -i f"))  # the outer stream continues past a substitution

        def test_r7_perl_digit_clusters_in_place(self):
            # finding 2 (HIGH): a perl switch cluster with digits hid the in-place i
            for cmd in ("perl -0777pi -e 's/old/2099-01-01T00:00Z/' /opt/p/private/s.md",
                        "perl -0pi -e 's/old/2099-01-01T00:00Z/' /opt/p/private/s.md",
                        "perl -l0pi -e 's/old/2099-01-01T00:00Z/' /opt/p/private/s.md",
                        "perl -0777 -pi.bak -e 's/old/2099-01-01T00:00Z/' /opt/p/private/s.md",
                        "sed -E -s -i 's/x/2099-01-01T00:00Z/' /opt/p/private/s.md",
                        "sed -nEi 's/x/2099-01-01T00:00Z/' /opt/p/private/s.md"):
                self.assertTrue(self.ev("Bash", command=cmd), cmd)
            for cmd in ("perl -0777 -ne 'print if /2099-01-01T00:00Z/' /opt/p/private/s.md",
                        "sed -n -E '/2099-01-01T00:00Z/p' /opt/p/private/s.md"):
                self.assertEqual(self.ev("Bash", command=cmd), [], cmd)

        def test_r7_gfm_table_forms(self):
            # finding 3 (MED): no outer pipes, and a one-hyphen delimiter, are valid GFM tables
            self.assertEqual(self.tw("Item | Due", "---|---", "x | 2099-01-01T00:00Z"), [])
            self.assertEqual(self.tw("| Item | Due |", "|-|-|", "| x | 2099-01-01T00:00Z |"), [])
            self.assertEqual(self.tw("| Item | Due |", "|--|--|", "| x | 2099-01-01T00:00Z |"), [])
            self.assertEqual(self.tw("Item | Due |", "|:-|-:|", "| x | 2099-01-01T00:00Z |"), [])
            self.assertEqual(self.tw("Item | Due", "- | -", "x | 2099-01-01T00:00Z", "y | 2099-02-01T00:00Z"), [])
            self.assertEqual(self.tw("Due | Seen", "---|---", "2099-01-01T00:00Z | 2099-02-01T00:00Z"),
                             ["2099-02-01T00:00Z"])
            self.assertEqual(self.tw("Item | Due", "---|---", "x | 2099-01-01T00:00Z", "no pipe here",
                                     "y | 2099-02-01T00:00Z"), [])  # round 11: a pipeless line is a row (GFM)

        def test_r7_header_repurpose_rechecks_rows(self):
            # finding 4 (MED): a header or delimiter change must re-check every row of its table
            fp = self.store_file("| Item | Due |\n|---|---|\n| x | 2099-01-01T00:00Z |\n")
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="Due", new_string="Observed"),
                             ["2099-01-01T00:00Z"])
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="| Item | Due |", new_string="| Due | Seen |"),
                             ["2099-01-01T00:00Z"])  # column shift
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="|---|---|\n", new_string=""),
                             ["2099-01-01T00:00Z"])  # the row leaves its table
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="Due", new_string="Due date"), [])
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="|---|---|", new_string="|:--|--:|"), [])
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="| Item |", new_string="| Thing |"), [])
            fp = self.store_file("| A | Seen |\n|---|---|\n| r | 2026-09-01T00:00Z |\n\n"
                                 "| B | Due |\n|---|---|\n| x | 2099-01-01T00:00Z |\n")
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="\n\n| B | Due |\n|---|---|\n", new_string="\n"),
                             ["2099-01-01T00:00Z"])  # the row joins the Seen table
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="| r |", new_string="| s |"), [])

        def test_r7_spaced_and_quoted_fd_duplication(self):
            # finding 5 (MED): the redirection operand is classified whole, after dequoting
            for cmd in ("grep 2099-01-01T00:00Z /opt/p/private/s.md 1>& 2",
                        "grep 2099-01-01T00:00Z /opt/p/private/s.md >&'2'",
                        "grep 2099-01-01T00:00Z /opt/p/private/s.md 2>& \"1\"",
                        "grep 2099-01-01T00:00Z /opt/p/private/s.md >& -",
                        "grep 2099-01-01T00:00Z /opt/p/private/s.md 3>&1-",
                        "grep 2099-01-01T00:00Z /opt/p/private/s.md >& /dev/null"):
                self.assertEqual(self.ev("Bash", command=cmd), [], cmd)
            for cmd in ("echo 2099-01-01T00:00Z >& /opt/p/private/s.md",
                        "echo 2099-01-01T00:00Z >&'/opt/p/private/s.md'",
                        "echo 2099-01-01T00:00Z &> 2 # /opt/p/private/s.md",
                        "echo 2099-01-01T00:00Z >& 2x /opt/p/private/s.md",
                        "echo 2099-01-01T00:00Z >& $fd /opt/p/private/s.md"):
                self.assertTrue(self.ev("Bash", command=cmd), cmd)

        def test_r7_subagent_store_write_is_checked(self):
            # finding 6 (refuted, intended): a subagent's store write is checked, never skipped
            for extra in ({"agent_id": "a1b2"}, {"agent_id": "a1b2", "agent_type": "general-purpose"}):
                payload = dict({"tool_name": "Write", "cwd": "/",
                                "tool_input": {"file_path": self.store, "content": "hb 2099-01-01T00:00Z"}}, **extra)
                self.assertEqual(evaluate(payload, self.now), ["2099-01-01T00:00Z"], extra)
                payload = dict({"tool_name": "Bash", "cwd": "/", "tool_input": {
                    "command": "echo 'hb 2099-01-01T00:00Z' >> /opt/proj/private/s.md"}}, **extra)
                self.assertTrue(evaluate(payload, self.now), extra)
            self.assertIn("DELIBERATELY checked", __doc__)

        def test_r7_shell_tokens_linear(self):
            t0 = time.monotonic()
            for cmd in ('"$(' * 100000, '"$(x)"' * 100000, '"`x`"' * 100000, "$((" * 100000 + "))" * 100000,
                        "1>& 2 " * 100000):
                bash_writes(cmd)
            self.assertLess(time.monotonic() - t0, 2.0)

        # -- round 8 (codex round-7 findings) --
        def test_r8_new_block_ends_table(self):
            # finding 1 (HIGH): a list item, heading, blockquote, or fence after a Due table inherited its context
            hdr = ("| Item | Due |", "|---|---|", "| a | 2026-09-01T00:00Z |")
            for tail in (("- heartbeat | 2099-01-02T00:00Z",), ("* hb | 2099-01-02T00:00Z",),
                         ("+ hb | 2099-01-02T00:00Z",), ("1. hb | 2099-01-02T00:00Z",), ("2) hb | 2099-01-02T00:00Z",),
                         ("# hb | 2099-01-02T00:00Z",), ("> hb | 2099-01-02T00:00Z",),
                         ("```text | x", "| b | 2099-01-02T00:00Z |"), ("~~~ | x", "| b | 2099-01-02T00:00Z |"),
                         ("", "hb | 2099-01-02T00:00Z"), ("hb 2099-01-02T00:00Z",)):
                self.assertEqual(self.tw(*(hdr + tail)), ["2099-01-02T00:00Z"], tail)
            # still rows: a leading-pipe row, a row of a pipeless-header table, a hyphen cell that is no list marker
            self.assertEqual(self.tw(*(hdr + ("  | b | 2099-01-02T00:00Z |",))), [])
            self.assertEqual(self.tw("Item | Due", "---|---", "x | 2026-09-01T00:00Z", "y | 2099-01-02T00:00Z"), [])
            self.assertEqual(self.tw("Item | Due", "---|---", "-| 2099-01-02T00:00Z"), [])
            # a new table may start right after the interrupting block
            self.assertEqual(self.tw(*(hdr + ("# next", "| Item | Due |", "|---|---|",
                                              "| b | 2099-01-02T00:00Z |"))), [])

        def test_r10_bare_row_under_leading_pipe_header(self):
            # codex round-8 [H]: GFM leading pipes are optional per line, so a bare row continues a `| ... |` table
            self.assertEqual(self.tw("| Item | Due |", "|---|---|", "release | 2099-01-01T00:00Z"), [])
            self.assertEqual(self.tw("| Item | Due |", "|---|---|", "| a | x |", "release | 2099-01-01T00:00Z |"), [])
            # the column is counted from the row's own leading pipe: a bare row's Item column is not exempt
            self.assertEqual(self.tw("| Item | Due |", "|---|---|", "2099-01-01T00:00Z | x"),
                             ["2099-01-01T00:00Z"])
            # the genuine block-ending checks still end it
            for gap in ("", "- x", "# h", "> q", "```"):
                self.assertEqual(self.tw("| Item | Due |", "|---|---|", gap, "release | 2099-01-01T00:00Z"),
                                 ["2099-01-01T00:00Z"], gap)
            self.assertNotIn("stricter than GFM", __doc__)

        def test_r11_pipe_free_row_continues_table(self):
            # codex round-10 [H]: GFM example 202, a pipe-free body row continues the table (one cell, column 0)
            body = "| Item | Due |\n|---|---|\nTBD\nrelease | %s\n"
            self.assertEqual(self.tw(*(body % "2099-01-01T00:00Z").splitlines()), [])
            fp = os.path.join(self.tmp, "r11.md")
            os.environ["ORCH_STORE_ROOT"] = self.tmp  # round 12: the Edit must reach a store path to count
            with open(fp, "w") as f:
                f.write(body % "2026-09-01T00:00Z")
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="2026-09-01T00:00Z",
                                     new_string="2099-01-01T00:00Z"), [])
            # control: the same Edit with the row's pipe removed (no header exemption) is denied, so the
            # allow above comes from the table rule, not from the path falling outside the store
            with open(fp, "w") as f:
                f.write(body.replace("release | ", "release ") % "2026-09-01T00:00Z")
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="2026-09-01T00:00Z",
                                     new_string="2099-01-01T00:00Z"), ["2099-01-01T00:00Z"])
            os.environ.pop("ORCH_STORE_ROOT")  # tw() writes to the default store path
            # a blank line still ends the table
            self.assertEqual(self.tw("| Item | Due |", "|---|---|", "TBD", "", "release | 2099-01-01T00:00Z"),
                             ["2099-01-01T00:00Z"])

        def test_r11_pipe_free_line_is_column_zero(self):
            # a pipe-free paragraph line after a table stays in it until a blank line, but (round 12) it never
            # gets a header exemption: it is checked like an ordinary line, even under a scheduling cell 0
            self.assertEqual(self.tw("| Item | Due |", "|---|---|", "| a | x |", "hb 2099-01-01T00:00Z"),
                             ["2099-01-01T00:00Z"])
            self.assertEqual(self.tw("| Item | Due |", "|---|---|", "| a | x |", "note", "more text",
                                     "release | 2099-01-01T00:00Z"), [])
            self.assertEqual(self.tw("| Item | Due |", "|---|---|", "note", "", "hb 2099-01-01T00:00Z",
                                     "release | 2099-01-01T00:00Z"),
                             ["2099-01-01T00:00Z"])
            self.assertEqual(self.tw("| Due | Item |", "|---|---|", "| x | a |", "2099-01-01T00:00Z"),
                             ["2099-01-01T00:00Z"])
            # the keyword-on-its-own-line rule still exempts a pipe-free row
            self.assertEqual(self.tw("| Due | Item |", "|---|---|", "| x | a |", "due 2099-01-01T00:00Z"), [])
            # and the table stays open past it: a later piped row keeps its Due exemption
            self.assertEqual(self.tw("| Due | Item |", "|---|---|", "note", "| 2099-01-01T00:00Z | a |"), [])
            self.assertNotIn("a line with no unescaped pipe, or", __doc__)
            self.assertNotIn("so it is exempt only when header cell 0 carries a keyword", __doc__)

        def test_r12_pipe_free_heartbeat_under_due_header_denied(self):
            # codex round-11 [H]: a pipe-free line under `| Due | Item |` inherited column 0's exemption, so
            # a fabricated future heartbeat was allowed through Write, Edit, and MultiEdit
            fut = "2099-01-01T00:00Z"
            body = "| Due | Item |\n| --- | --- |\n| 2099-02-01T09:00Z | release |\nLast-heartbeat: %s\n"
            fp = os.path.join(self.tmp, "r12.md")
            os.environ["ORCH_STORE_ROOT"] = self.tmp
            self.assertEqual(self.ev("Write", file_path=fp, content=body % fut), [fut])
            with open(fp, "w") as f:
                f.write(body % "2026-09-01T00:00Z")
            self.assertEqual(self.ev("Edit", file_path=fp, old_string="2026-09-01T00:00Z", new_string=fut), [fut])
            self.assertEqual(self.ev("MultiEdit", file_path=fp,
                                     edits=[{"old_string": "2026-09-01T00:00Z", "new_string": fut}]), [fut])
            # the piped Due row itself stays exempt (unchanged scheduled row, and a fresh one)
            self.assertEqual(self.ev("Write", file_path=fp, content=body % "2026-09-01T00:00Z"), [])
            self.assertIn("A pipe-free row gets no header", __doc__)

        def test_r8_table_context_carry_over_scales(self):
            # finding 2 (MED perf): a row key compared the full header text, so time grew with header x rows
            times = []
            for hl in (10000, 160000):
                old = "\n".join(["| Item | Due | " + "h" * hl + " |", "|---|---|---|"]
                                 + ["| x | 2026-09-01T00:00Z | y |"] * 160000) + "\n"
                t0 = time.monotonic()
                self.assertEqual(future_in_changed_lines(old, old, 0), [])
                times.append(time.monotonic() - t0)
            self.assertLess(times[1], 3.0)
            self.assertLess(times[1], 2.0 * times[0] + 0.2)  # flat in header length

        def test_r8_case_pattern_paren_in_substitution(self):
            # finding 3 (HIGH, exotic): a case pattern `)` closed the $(...) frame early, hiding the write
            deny = ('result="$(case ok in ok) printf \'%s\\n\' \'hb 2099-01-02T00:00Z\' > /opt/p/private/s.md;; esac)"',
                    'r=$(case ok in (ok) tee /opt/p/private/s.md <<< "2099-01-02T00:00Z";; esac)',
                    'r="$(case a in a) case b in b) :;; esac; printf 2099-01-02T00:00Z > /opt/p/private/s.md;; esac)"')
            for cmd in deny:
                self.assertTrue(bash_writes(cmd), cmd)
                self.assertEqual(self.ev("Bash", command=cmd), ["2099-01-02T00:00Z"], cmd)
            # a quoted case/esac is no keyword, and a read inside a case construct stays a read
            allow = ('r="$(case ok in ok) grep 2099-01-02T00:00Z /opt/p/private/s.md;; esac)"',
                     'r="$(echo \'case\'; grep 2099-01-02T00:00Z /opt/p/private/s.md)"')
            for cmd in allow:
                self.assertFalse(bash_writes(cmd), cmd)
                self.assertEqual(self.ev("Bash", command=cmd), [], cmd)

        def test_r9_hash_row_continues_pipeless_table(self):
            # round 9 finding 1 (HIGH, false deny): any `#` line ended a table, so an issue-number row lost its
            # Due-column exemption; only an ATX heading (1 to 6 `#` then whitespace or the line end) ends one
            for rows in (("#123 | 2099-12-31T00:00Z",), ("x | 2026-09-01T00:00Z", "#7 | 2099-12-31T00:00Z"),
                         ("####### | 2099-12-31T00:00Z",), ("#tag | 2099-12-31T00:00Z",)):
                self.assertEqual(self.tw("Issue | Due", "---|---", *rows), [], rows)
            for head in ("# h | 2099-12-31T00:00Z", "###### h | 2099-12-31T00:00Z", "#\t| 2099-12-31T00:00Z",
                         "## | 2099-12-31T00:00Z"):
                self.assertEqual(self.tw("Issue | Due", "---|---", head), ["2099-12-31T00:00Z"], head)

        def test_r9_case_counted_only_in_command_position(self):
            # round 9 finding 2 (HIGH, false deny): a `case` ARGUMENT inside a substitution opened a case
            # construct, left the substitution unterminated, and read as a write
            reads = ('x="$(rg case /opt/p/private/s.md | grep 2099-12-31T00:00Z)"',
                     'x="$(echo case; grep 2099-12-31T00:00Z /opt/p/private/s.md)"',
                     'x="$(rg then case /opt/p/private/s.md | grep 2099-12-31T00:00Z)"',
                     'x=$(grep -e esac -e case 2099-12-31T00:00Z /opt/p/private/s.md)')
            for cmd in reads:
                self.assertIsNotNone(_shell_tokens(cmd), cmd)
                self.assertFalse(bash_writes(cmd), cmd)
                self.assertEqual(self.ev("Bash", command=cmd), [], cmd)
            # a case in command position, after a separator or a reserved word, still shows the write inside it
            writes = ('r="$(true; case a in a) printf 2099-12-31T00:00Z > /opt/p/private/s.md;; esac)"',
                      'r="$(if true; then case a in a) tee /opt/p/private/s.md <<< 2099-12-31T00:00Z;; esac; fi)"',
                      'r="$(! case a in a) printf 2099-12-31T00:00Z > /opt/p/private/s.md;; esac)"',
                      'r="$(case a in a) echo esac; printf 2099-12-31T00:00Z > /opt/p/private/s.md;; esac)"')
            for cmd in writes:
                self.assertTrue(bash_writes(cmd), cmd)
                self.assertEqual(self.ev("Bash", command=cmd), ["2099-12-31T00:00Z"], cmd)

        def test_r4_threat_model_stated(self):
            self.assertIn("THREAT MODEL", __doc__.split("\n\n")[1])

    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(T))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
