#!/usr/bin/env python3
"""PreToolUse hook (Edit / Write / MultiEdit): a large tool payload IS the forbidden console wall.

PR1b ACTIVATION CANDIDATE, hardened 2026-08-09 against the seed deep review
(`inbox/deliveries/seed-review-pr1b-codex.md`) and re-hardened 2026-08-09 against the dual-family
validation of PR #1472 (`inbox/deliveries/vpr-1472-codex.md` findings 7, 8, 9, 10 and
`inbox/deliveries/vpr-1472-claude.md` F9 / F10).

WIRING, as SHIPPED and as verified against the file it is wired in. This hook lives at
`.claude/hooks/block-large-editwrite-payload.py` and `.claude/settings.json` wires it under the
PreToolUse matcher `"Edit|Write"` (see WIRED_MATCHER below), command
`python3 "$CLAUDE_PROJECT_DIR"/.claude/hooks/block-large-editwrite-payload.py`.
A hook matcher is an UNANCHORED regex over the tool name, so `"Edit|Write"` also matches
`MultiEdit`, which is the working assumption the repo already documents for the sibling hook on the
same matcher (`.claude/hooks/block-public-working-write.py:15`, "Fires on Edit, Write, MultiEdit,
NotebookEdit, and Bash"). The MultiEdit support below is therefore LIVE, not dead code, and no
third alternative in the matcher is needed. `settings_matcher()` re-reads that JSON so this
paragraph is checked MECHANICALLY by the self-test instead of trusted; if the wiring is ever
changed, the self-test fails until this paragraph is changed with it.

WHY THIS EXISTS. The Edit and Write tools RENDER their payload as a red/green diff in the console.
That render is not a side effect of the edit, it IS the wall the "never render a file diff in chat"
section forbids -- which is why the maintainer restated the rule as a HARD one on 2026-07-27, after
repeated violations of the softer form: "For any change to an EXISTING file beyond a couple of short
lines, do NOT use Edit or Write: use `sed -i` with a targeted single-line pattern, or a `python`
read-insert-write via a shell heredoc, neither of which renders a diff. Reserve the Edit tool for a
genuinely tiny (one short line) change." The sibling `block-git-diff-content-dump.py` closes the
`git diff` route to the same wall; this hook closes the editor-tool route, which is the larger of
the two in practice because every authoring turn goes through it.

WHAT IT MEASURES, and this is the part the seed got wrong twice.

  The seed measured the LARGEST SINGLE FIELD: `max(lines(old_string), lines(new_string))` for an
  Edit, and the largest field of the largest single edit for a MultiEdit. Two consequences, both
  confirmed by the review's probes:
    * `max()` over `(lines, chars)` TUPLES is lexicographic, so a six-line short `old_string` beat a
      one-line 1,300-character `new_string` and the independent CHARACTER threshold never saw it.
    * a six-line old plus a six-line new renders TWELVE rows, and fifty one-line MultiEdits render
      fifty hunks; both measured as "6" and "1" and were allowed.

  This version measures the RENDER:
    * RENDERED ROWS for one edit = removed rows + added rows, after trimming the common leading and
      trailing lines. That trim is what makes the measure honest in both directions: an Edit whose
      `old_string` and `new_string` are identical renders NOTHING and is now allowed (it warned
      before), and a large anchor with a single changed line renders two rows, not forty.
    * TOTALS are summed across every edit in the call, so a MultiEdit is measured as the wall the
      maintainer actually sees. This REVERSES the seed's stated "largest single edit, not the sum"
      decision, on the review's finding that the old rule contradicted the hook's own headline.
    * REPLACE_ALL is multiplied out. An Edit with `replace_all: true` renders ONE HUNK PER
      OCCURRENCE, so the per-occurrence delta is counted once for the per-hunk thresholds and
      TIMES the occurrence count for the totals. The count is read from the target under the same
      size contract as Write; when it cannot be established the count is UNKNOWN_MULTIPLICITY, a
      conservative stand-in that WARNS rather than failing open (`kind` is marked `assumed` so the
      register can exclude those rows from threshold calibration).
    * Write to an EXISTING file diffs the new `content` against the file on disk, so a byte-identical
      rewrite renders nothing and no longer warns.
    * Write to an existing file the hook CANNOT READ for comparison (over MAX_COMPARE_BYTES, or an
      unreadable path) counts EVERY existing row as removed and every new row as added, because
      without the old text there is no common context to trim. This is what makes an oversized
      DELETION visible: `content: ""` against a 1,100,000-line file measured ZERO before, since the
      fallback measured only the empty new payload.
    * Write that CREATES a file is measured too, as a pure green block (see design decision 3).
    * LINES and CHARACTERS are evaluated INDEPENDENTLY, never selected against each other. Both are
      counted the same way on every path: `rendered_delta` is the single entry point, so characters
      always EXCLUDE line terminators. The one exception is documented at `_uncomparable_delta`,
      where the existing side can only be had as a BYTE size, which over-counts by its newlines.

  Four thresholds, tripped independently, first hit named in the message:
      LINE_THRESHOLD        per hunk, rendered rows
      CHAR_THRESHOLD        per hunk, rendered characters
      TOTAL_LINE_THRESHOLD  whole tool call, rendered rows
      TOTAL_CHAR_THRESHOLD  whole tool call, rendered characters

  NOTE FOR CALIBRATION: LINE_THRESHOLD's UNIT CHANGED. It used to count payload lines; it now counts
  RENDERED ROWS, and a replacement renders roughly two rows per changed line. 6 rendered rows is
  therefore about a 3-line replacement. Do not read the old and new fire counts as the same series.

THE DESIGN DECISIONS, surfaced deliberately because they are the reviewable substance:

  1. BLOCK_SEVERITY = "warn" (default). Values: "block" (exit 2), "warn" (exit 0 + stderr), "off".
     WARN is proposed, against the sibling hooks' BLOCK default, for one reason: this guard fires on
     the single most common tool call in an authoring session, and its remedy (`sed -i`, a heredoc
     rewrite) is materially harder than the remedy for the other two hooks, which is one flag or one
     dispatch command. A hard block at the wrong threshold does not produce sed; it produces a
     stalled turn and a guard that gets switched off, and a switched-off guard protects nothing. The
     honest cost of WARN is that a warning can be read and ignored -- exactly the failure mode
     recorded against the predecessor offload guard's WARN arm. The resolution is SEQUENCED, not
     permanent: ship WARN, let the register accumulate real fire counts and rendered sizes, then
     flip to "block" at a threshold the data justifies.

  2. THE THRESHOLD NUMBERS ARE GUESSES. The rule says "a couple of short lines", which reads as 2.
     6 rendered rows per hunk and 12 across the call are proposed instead, and the gap is deliberate:
     at 2 the guard fires on nearly every real edit, and a guard that fires constantly is noise that
     trains the reader to skip it. These four numbers are the single most important thing for the
     orchestrator to calibrate rather than accept, and the register below now produces the data to
     do it.

  3. A Write that CREATES a file is MEASURED and WARNED (WARN_ON_LARGE_CREATE = True). The seed set
     this False, reasoning that there is no red/green comparison and no sanctioned `sed -i`
     alternative for a file that does not exist yet, and that the pinned hard-rule sentence is
     limited to changes to EXISTING files. Validation rejected that reasoning as the largest hole in
     the hook's own headline: a 5,000-line create renders 5,000 green rows, which is the wall the
     rule exists to prevent, and the absence of a `sed` remedy does not make the payload small.
     There IS a rendering-free remedy for a create, and the warning names it: a quoted heredoc
     (`cat > <file> <<'EOF'`). The constant remains, so the behaviour is a calibration decision the
     orchestrator can revert exactly, but its default is now True.

REGISTER -- IMPLEMENTED, no longer deferred. The seed said WARN for a week, then calibrate from
register data, while also saying this hook does not log fires; that combination cannot produce the
evidence it promises. `log_fire()` appends one row per fire to `/home/grc/grc_working/guard-fires.tsv`
in the four-column shape the shipped self-QA hook uses. It records tool kind, per-hunk and total
rows and characters, which threshold tripped, the four threshold values, and the outcome
(WARN-ALLOWED / BLOCK / BYPASS-AUTHORIZED). It records NO file content, NO path, and NO payload text.
It returns False rather than raising, and the caller ignores the result, so a logging failure can
never change a decision. STANDING RECOMMENDATION, unchanged from the seed: `log_fire` now exists in
two hooks and should be extracted into `_hookutil.py` in a follow-up rather than copied a third time.

WHAT THE REGISTER MUST SHOW BEFORE THE SEVERITY FLIP:
  * fires per authoring day, split by tool kind, so the noise cost of "block" is a number;
  * the distribution of rendered rows and characters at the fire, so the thresholds are set at a
    real knee rather than at 6;
  * the share of fires tripped by TOTAL_* rather than the per-hunk thresholds, which decides whether
    batching is being punished or correctly caught;
  * the share of fires whose `kind` carries `assumed` or `uncomparable`, which are ESTIMATES and
    must be excluded from any threshold arithmetic drawn from the other rows.

ESCAPE, and it is a FILE, not an environment variable. `touch /home/grc/grc_working/.allow-large-edit`
is honoured ONCE and consumed. An env var was considered and REJECTED for a concrete reason recorded
against an earlier hook: a hook inherits the HARNESS environment, never the environment of a tool
call, so the actor cannot set an env var for its own next Edit -- an env-var escape is the APPEARANCE
of an escape rather than one. CONSUMPTION IS NOW ATOMIC AND VERIFIED, per the review: the sentinel
must be a REGULAR FILE and not a symlink, it is consumed by `os.replace` into a private name so two
concurrent calls cannot both win, and a bypass is granted ONLY when that consumption SUCCEEDS. The
seed entered the bypass branch on a bare `exists()` and ignored unlink failure, so a directory, a
symlink, a permission failure or a race could all grant an unconsumable standing bypass. The
sentinel is still only tested AFTER a threshold trips, so an ordinary small edit cannot burn it.
At the WARN default the escape is inert; it exists so the flip to "block" is a one-token change.

PATH CONTRACT for Write, and now for a replace_all Edit as well. `file_path` is expected to be
ABSOLUTE. A relative path is resolved against `CLAUDE_PROJECT_DIR` first and the hook process cwd
second, because the hook process cwd is not the tool call's cwd and an existing project file must not
be mistaken for a new file (which previously skipped the guard entirely, and now downgrades a
red/green measurement to a green-block one). If the harness ever guarantees absolute paths, this
fallback becomes dead code and can be deleted; until it is verified, the fallback is the safe
reading.

Exit protocol (Claude Code hooks): exit 0 allows the tool call; exit 2 blocks it and feeds stderr
back to the model as the reason. FAIL-OPEN on any parse error or unreadable path.

Console format: three headers. The status header states what ACTUALLY happened -- `WARNING` when the
call proceeds, `BLOCKED` only when it does not -- followed by `WHY:` and `CONSIDER-INSTEAD:`.

HOW THIS HOOK RELATES TO THE PROSE at `.claude/CLAUDE.md:868`, stated rather than deferred. That
sentence is a HARD rule and reserves the Edit tool for one short line. This hook is NOT full
mechanical enforcement of it: it allows 6 rendered rows per hunk and 12 across a call, it WARNS
instead of blocking, and its numbers are the guesses of design decision 2. It is a permissive
telemetry backstop for the far end of the rule, sized so the register can tell the maintainer where
the real knee is. The prose remains the rule; this hook is the floor under it, not a restatement of
it, and nothing here licenses a payload the prose forbids.

Self-test: `python3 "$CLAUDE_PROJECT_DIR"/.claude/hooks/block-large-editwrite-payload.py --self-test`
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# "block" -> exit 2 | "warn" -> exit 0 with a stderr notice | "off" -> silent allow.
# See design decision 1 in the docstring before changing this.
BLOCK_SEVERITY = "warn"

# PER HUNK, in RENDERED ROWS (removed + added, common context trimmed). See design decision 2.
LINE_THRESHOLD = 6

# PER HUNK, in rendered characters. Catches the few-but-enormous-lines shape a row count is blind
# to: three 900-character lines wrap into thirty rendered rows. Set to 0 to disable.
CHAR_THRESHOLD = 1200

# WHOLE TOOL CALL. A MultiEdit of fifty one-line edits is one call and one wall.
# Set either to 0 to disable that trip.
TOTAL_LINE_THRESHOLD = 12
TOTAL_CHAR_THRESHOLD = 2400

# Tools whose payload renders as a console diff.
EDIT_TOOLS = {"Edit", "MultiEdit"}
WRITE_TOOLS = {"Write"}

# Count removed rows as well as added rows. A large DELETION has a tiny new_string and renders a
# large RED block, so counting only additions misses half the walls by construction. This is a
# stated deviation from the order (which specifies new_string); set False to revert it exactly.
# It also governs the removed side of the uncomparable-existing-file fallback.
INCLUDE_OLD_STRING = True

# A Write that CREATES a file renders a green wall and IS measured. See design decision 3.
# Flip to False to restore the seed's unbounded-create hole exactly.
WARN_ON_LARGE_CREATE = True

# Upper bound on how much of an existing file the hook will read to compute the rendered delta.
MAX_COMPARE_BYTES = 2_000_000

# Upper bound on how much of an over-MAX_COMPARE_BYTES file the hook will STREAM to count its
# newlines. Streaming counts bytes in bounded chunks and never holds the file in memory, so this is
# a time bound, not a memory one. Above it the line count is estimated from the byte size.
MAX_SCAN_BYTES = 64_000_000

# Bytes per line assumed when a file is too large even to stream. Only ever applied above
# MAX_SCAN_BYTES, where any plausible divisor lands orders of magnitude above every threshold.
ASSUMED_LINE_BYTES = 40

# Occurrence count assumed for a replace_all Edit whose true multiplicity cannot be read. Any value
# above TOTAL_LINE_THRESHOLD makes a rendering replace_all warn; this one also survives the totals
# being raised without revisiting this line. It is an ESTIMATE and is marked as such in `kind`.
UNKNOWN_MULTIPLICITY = 999

# The matcher this hook is wired under in `.claude/settings.json`. The self-test compares this
# constant against the docstring AND against the shipped JSON, so the wiring paragraph above cannot
# drift from the wiring itself the way it did at 22df0be2.
WIRED_MATCHER = "Edit|Write"
HOOK_BASENAME = "block-large-editwrite-payload.py"

WORKING_ROOT = Path(os.environ.get("GRC_DROP_ROOT", "/home/grc/grc_working"))
ESCAPE_FILE = WORKING_ROOT / ".allow-large-edit"
FIRE_LOG = WORKING_ROOT / "guard-fires.tsv"


def _lines(text) -> list:
    """Logical lines of a payload. [] for anything that is not a non-empty string."""
    if not isinstance(text, str) or not text:
        return []
    return text.splitlines() or [""]


def _measure(text) -> tuple:
    """(lines, chars) of a payload. (0, 0) for anything that is not a non-empty string.

    Kept as a public helper because the fixtures read it. NOTE the unit: `chars` here INCLUDES line
    terminators, where `rendered_delta` excludes them. No decision path uses this function any more
    for exactly that reason (claude F10); it is measurement documentation, not measurement.
    """
    rows = _lines(text)
    return (len(rows), len(text)) if rows else (0, 0)


def rendered_delta(old, new) -> tuple:
    """(rows, chars) a red/green render would actually show for old -> new.

    Common leading and trailing lines are trimmed, because the renderer shows them as unchanged
    context rather than as red/green rows. Identical strings therefore measure zero, and a large
    anchor with one changed line measures two rows, not the size of the anchor.

    This is the SINGLE measurement entry point for every path (edit, create, existing-file Write),
    so characters are counted the same way everywhere: line contents only, terminators excluded.
    """
    o = _lines(old)
    n = _lines(new)
    head = 0
    while head < len(o) and head < len(n) and o[head] == n[head]:
        head += 1
    tail = 0
    while tail < len(o) - head and tail < len(n) - head and o[len(o) - 1 - tail] == n[len(n) - 1 - tail]:
        tail += 1
    removed = o[head:len(o) - tail] if INCLUDE_OLD_STRING else []
    added = n[head:len(n) - tail]
    rows = len(removed) + len(added)
    chars = sum(len(x) for x in removed) + sum(len(x) for x in added)
    return rows, chars


def _resolve(path):
    """Absolute Path for a tool-supplied file_path. See PATH CONTRACT in the docstring."""
    p = Path(str(path))
    if p.is_absolute():
        return p
    root = os.environ.get("CLAUDE_PROJECT_DIR") or ""
    if root:
        candidate = Path(root) / p
        if candidate.exists():
            return candidate
    return p


def _read_existing(path):
    """The current text of an existing file, or None when it cannot be compared."""
    try:
        if path.stat().st_size > MAX_COMPARE_BYTES:
            return None
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None


def existing_metrics(path):
    """(bytes, lines) of an existing file that is too large or too broken to diff, or None.

    Needed because a file over MAX_COMPARE_BYTES still has a KNOWN size and a countable number of
    lines, and codex finding 8 turned on the hook throwing both away: an oversized file overwritten
    with `content: ""` was measured as zero rendered rows and allowed.

    Newlines are counted by STREAMING the file in bounded chunks, so nothing large is held in
    memory. Above MAX_SCAN_BYTES the count is ESTIMATED from the byte size, which at that scale is
    orders of magnitude above every threshold either way. Line semantics match `_lines`: a file that
    does not end in a newline still has a final logical line, and an empty file has none.
    """
    try:
        size = path.stat().st_size
    except OSError:
        return None
    if size <= 0:
        return 0, 0
    if size > MAX_SCAN_BYTES:
        return size, max(1, size // ASSUMED_LINE_BYTES)
    newlines = 0
    last = b""
    try:
        with path.open("rb") as fh:
            while True:
                chunk = fh.read(1 << 20)
                if not chunk:
                    break
                newlines += chunk.count(b"\n")
                last = chunk[-1:]
    except OSError:
        return size, max(1, size // ASSUMED_LINE_BYTES)
    return size, newlines + (0 if last == b"\n" else 1)


def _uncomparable_delta(path, content) -> tuple:
    """(rows, chars) for a Write whose existing target could not be read for comparison.

    Every existing row is assumed REMOVED and every new row ADDED, because with no old text there
    is no common context to trim. That is deliberately the over-warning direction, and it is what
    makes an oversized DELETION visible at all: the seed measured only the empty new payload here
    and reported (0, 0) for wiping out a 1,100,000-line file.

    UNIT NOTE: the removed side is the file's BYTE size, which counts the newlines that the added
    side (`rendered_delta`) excludes. That over-counts characters slightly and never under-counts.
    The removed side honours INCLUDE_OLD_STRING, like every other removal measurement here.
    """
    rows, chars = rendered_delta("", content)
    metrics = existing_metrics(path)
    if metrics is None or not INCLUDE_OLD_STRING:
        return rows, chars
    size, lines = metrics
    return rows + lines, chars + size


def replacement_count(raw_path, edit) -> tuple:
    """(count, assumed) for how many times one Edit's replacement is RENDERED.

    (1, False) unless `replace_all` is set. With replace_all the console shows ONE HUNK PER
    OCCURRENCE, which codex finding 7 caught being measured as a single replacement: `x` -> `y`
    with replace_all over a 1,000-line file rendered 2,000 rows and was measured as 2.

    The count is read from the target under the same size contract as Write. When it cannot be
    established -- no path, a missing or unreadable target, a file over MAX_COMPARE_BYTES, or an
    empty `old_string` -- the count is UNKNOWN_MULTIPLICITY with assumed=True, because an unbounded
    replace_all must WARN rather than fail open. `assumed` reaches the register through `kind`, so
    calibration can drop these rows instead of reading 999 as a measurement.
    """
    if not isinstance(edit, dict) or not edit.get("replace_all"):
        return 1, False
    old = edit.get("old_string")
    if not isinstance(old, str) or not old or not raw_path:
        return UNKNOWN_MULTIPLICITY, True
    try:
        before = _read_existing(_resolve(raw_path))
    except Exception:
        return UNKNOWN_MULTIPLICITY, True
    if before is None:
        return UNKNOWN_MULTIPLICITY, True
    return max(1, before.count(old)), False


def _kind(base: str, *flags) -> str:
    """'Edit', or 'Edit(replace_all,assumed)': the tool kind plus any measurement caveats.

    The caveats travel into BOTH the console message and the register row, because a total that was
    multiplied by an assumed occurrence count, or built from a file that could not be read, is not
    the same evidence as a measured one and must not be calibrated against as if it were.
    """
    live = [f for f in flags if f]
    return base + ("(" + ",".join(live) + ")" if live else "")


def payload_size(payload: dict) -> tuple:
    """(hunk_lines, hunk_chars, total_lines, total_chars, kind) of the console render.

    kind is '' when nothing renders. Lines and characters are carried INDEPENDENTLY: nothing here
    selects one candidate over another, which is the seed's lexicographic-tuple defect. Per-hunk
    figures are the largest SINGLE rendered hunk; totals are the whole call, replace_all multiplied
    out.
    """
    tool = payload.get("tool_name") or payload.get("toolName") or ""
    ti = payload.get("tool_input") or payload.get("toolInput") or {}
    if not isinstance(ti, dict):
        return 0, 0, 0, 0, ""

    if tool in EDIT_TOOLS:
        raw = ti.get("file_path") or ti.get("path") or ""
        edits = ti.get("edits")
        if isinstance(edits, list) and edits:
            hunk_lines = hunk_chars = total_lines = total_chars = 0
            any_all = any_assumed = False
            for e in edits:
                if not isinstance(e, dict):
                    continue
                rows, chars = rendered_delta(e.get("old_string"), e.get("new_string"))
                count, assumed = replacement_count(raw, e)
                any_all = any_all or bool(e.get("replace_all"))
                any_assumed = any_assumed or (assumed and rows > 0)
                hunk_lines = max(hunk_lines, rows)
                hunk_chars = max(hunk_chars, chars)
                total_lines += rows * count
                total_chars += chars * count
            return (hunk_lines, hunk_chars, total_lines, total_chars,
                    _kind("MultiEdit", "replace_all" if any_all else "",
                          "assumed" if any_assumed else ""))
        rows, chars = rendered_delta(ti.get("old_string"), ti.get("new_string"))
        count, assumed = replacement_count(raw, ti)
        kind = _kind("Edit", "replace_all" if ti.get("replace_all") else "",
                     "assumed" if (assumed and rows > 0) else "")
        return rows, chars, rows * count, chars * count, kind

    if tool in WRITE_TOOLS:
        raw = ti.get("file_path") or ti.get("path") or ""
        if not raw:
            return 0, 0, 0, 0, ""                        # unresolvable path -> fail open
        try:
            path = _resolve(raw)
            exists = path.is_file()
            occupied = path.exists() and not exists
        except Exception:
            return 0, 0, 0, 0, ""
        if occupied:
            return 0, 0, 0, 0, ""    # a directory or a device: not a create, and nothing renders
        content = ti.get("content")
        if not exists:
            if not WARN_ON_LARGE_CREATE:
                return 0, 0, 0, 0, ""                    # seed behaviour, revertible: decision 3
            rows, chars = rendered_delta("", content)     # a create renders a pure green block
            return rows, chars, rows, chars, _kind("Write", "new-file")
        before = _read_existing(path)
        if before is None:
            rows, chars = _uncomparable_delta(path, content)
            return rows, chars, rows, chars, _kind("Write", "uncomparable")
        rows, chars = rendered_delta(before, content)
        return rows, chars, rows, chars, "Write"

    return 0, 0, 0, 0, ""


def over_threshold(lines: int, chars: int, total_lines=None, total_chars=None) -> str:
    """The name of the FIRST threshold that tripped, or '' when none did.

    Every threshold is tested independently against its own metric. The seed compared a single
    selected (lines, chars) pair, so a payload could be over CHAR_THRESHOLD and never be seen.
    """
    if total_lines is None:
        total_lines = lines
    if total_chars is None:
        total_chars = chars
    if LINE_THRESHOLD and lines > LINE_THRESHOLD:
        return "lines"
    if CHAR_THRESHOLD and chars > CHAR_THRESHOLD:
        return "chars"
    if TOTAL_LINE_THRESHOLD and total_lines > TOTAL_LINE_THRESHOLD:
        return "total-lines"
    if TOTAL_CHAR_THRESHOLD and total_chars > TOTAL_CHAR_THRESHOLD:
        return "total-chars"
    return ""


def _limit_text(trip: str, lines: int, chars: int, total_lines: int, total_chars: int) -> str:
    return {
        "lines": "%d rendered rows in one hunk > LINE_THRESHOLD %d" % (lines, LINE_THRESHOLD),
        "chars": "%d rendered characters in one hunk > CHAR_THRESHOLD %d" % (chars, CHAR_THRESHOLD),
        "total-lines": "%d rendered rows in this call > TOTAL_LINE_THRESHOLD %d"
                       % (total_lines, TOTAL_LINE_THRESHOLD),
        "total-chars": "%d rendered characters in this call > TOTAL_CHAR_THRESHOLD %d"
                       % (total_chars, TOTAL_CHAR_THRESHOLD),
    }.get(trip, trip)


def _why_text(kind: str, blocking: bool) -> str:
    """The WHY paragraph, which must describe the payload the actor ACTUALLY sent.

    A create has no red side and no `sed` remedy, so the existing-file sentence would be wrong for
    it, and saying nothing was worse: the seed's message told the actor that creating a file is
    "always allowed" while the guard is now measuring exactly that.
    """
    outcome = "The call has been refused." if blocking else "This is a WARNING; the call proceeds."
    if "new-file" in kind:
        return ("WHY: the Write tool RENDERS the whole of a new file as green rows in the console, "
                "and at this size that render IS the wall the maintainer ruled out on 2026-07-27. "
                "A create has no red side and no `sed` remedy, which is why it went unmeasured "
                "before; it does have a remedy that renders nothing, and it is below. " + outcome)
    if "uncomparable" in kind:
        return ("WHY: the Edit/Write tools RENDER their payload as a red/green diff in the console, "
                "and that render IS the wall the maintainer ruled out on 2026-07-27. This target "
                "was too large to read for a line-by-line comparison, so the figures above assume "
                "the whole existing file is replaced; a rewrite or a deletion at this size is a "
                "wall either way. " + outcome)
    return ("WHY: the Edit/Write tools RENDER their payload as a red/green diff in the console, and "
            "that render IS the wall the maintainer ruled out on 2026-07-27 after repeated "
            "violations. For a change to an EXISTING file beyond a couple of short lines the "
            "sanctioned tools are the ones that render nothing. " + outcome)


def _alternatives(kind: str) -> str:
    """The CONSIDER-INSTEAD block, matched to the payload shape.

    Heredoc delimiters are QUOTED on purpose: the sibling `block-git-diff-content-dump.py` scans an
    UNQUOTED heredoc body as live shell text, so an unquoted form here would prescribe a command a
    sibling guard can refuse.
    """
    if "new-file" in kind:
        return (
            "    cat > <file> <<'EOF'                       # write the NEW file in one shot\n"
            "    <content>                                  # renders nothing; quote the delimiter\n"
            "    EOF\n"
            "    python3 - <<'PY'                           # or build it programmatically\n"
            "    open('<file>', 'w').write('<content>')\n"
            "    PY\n"
        )
    return (
        "    sed -i 's/<old>/<new>/' <file>              # targeted single-line substitution\n"
        "    sed -i '<a>,<b>s/<old>/<new>/' <file>       # line-range-scoped where a token repeats\n"
        "    python3 - <<'PY'                            # read-insert-write, renders nothing\n"
        "    p='<file>'; s=open(p).read()\n"
        "    s = s.replace('<old>', '<new>')\n"
        "    open(p,'w').write(s)\n"
        "    PY\n"
    )


def _message(kind: str, lines: int, chars: int, trip: str, blocking: bool,
             total_lines=None, total_chars=None) -> str:
    if total_lines is None:
        total_lines = lines
    if total_chars is None:
        total_chars = chars
    head = "BLOCKED" if blocking else "WARNING"
    limit = _limit_text(trip, lines, chars, total_lines, total_chars)
    note = ""
    if "replace_all" in kind:
        note = ("  NOTE: replace_all renders ONE HUNK PER OCCURRENCE, so the call total above is "
                "the per-occurrence render times the number of occurrences"
                + (" (not readable here, so a conservative count was assumed).\n"
                   if "assumed" in kind else ".\n"))
    return (
        head + " (console payload-wall guardrail): this " + kind + " payload is " + limit + ".\n"
        "\n"
        + _why_text(kind, blocking) + "\n"
        "\n"
        "CONSIDER-INSTEAD:\n"
        + _alternatives(kind)
        + "\n"
        + note
        + "  Reserve Edit/Write for a genuinely tiny change. A large CREATE is measured too, as a "
        "green wall (WARN_ON_LARGE_CREATE).\n"
        + ("  If this payload genuinely has to go through the editor tool, that is a MAINTAINER "
           "decision. Ask for it, and they authorize it from a shell:\n"
           "    touch " + str(ESCAPE_FILE) + "     # honoured once, then consumed\n"
           if blocking else
           "  Prefer sed/heredoc for the next one.\n")
    )


def consume_escape() -> bool:
    """Consume the once-only sentinel ATOMICALLY. True only when this call actually took it.

    Modelled on the shipped self-QA hook. A directory, a symlink, an unwritable parent, or a losing
    race all return False, because a bypass that cannot be consumed is a standing bypass.
    """
    path = ESCAPE_FILE
    try:
        if os.path.islink(str(path)) or not path.is_file():
            return False
    except OSError:
        return False
    claimed = path.with_name(path.name + ".consumed." + str(os.getpid()))
    try:
        os.replace(str(path), str(claimed))              # atomic: only one racer can win
    except OSError:
        return False
    try:
        os.unlink(str(claimed))
    except OSError:
        pass                                             # already claimed; the bypass stands
    return True


def log_fire(event: str, detail: str) -> bool:
    """Append one row to the shared fire register. True on a written row, False on any failure.

    Row: <utc-iso-Z> TAB <event> TAB <hook> TAB <detail>, the four-column shape already used by the
    shipped self-QA hook. The CALLER ignores the result: a logging failure must never change a
    decision. `detail` carries SIZES ONLY, never payload text or a path.
    """
    try:
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        row = "\t".join([stamp, event, "block-large-editwrite-payload",
                         " ".join(str(detail).split())]) + "\n"
        with FIRE_LOG.open("a", encoding="utf-8") as fh:
            fh.write(row)
        return True
    except Exception:
        return False


def fire_detail(kind: str, lines: int, chars: int, total_lines: int, total_chars: int,
                trip: str) -> str:
    """The bounded, content-free telemetry row body that calibration will read.

    `kind` carries the measurement caveats (`replace_all`, `assumed`, `uncomparable`, `new-file`)
    and never a space, so the row stays parseable as whitespace-separated key=value pairs.
    """
    return ("kind=%s hunk_lines=%d hunk_chars=%d total_lines=%d total_chars=%d trip=%s "
            "thresholds=%d/%d/%d/%d severity=%s"
            % (kind, lines, chars, total_lines, total_chars, trip, LINE_THRESHOLD, CHAR_THRESHOLD,
               TOTAL_LINE_THRESHOLD, TOTAL_CHAR_THRESHOLD, BLOCK_SEVERITY))


def settings_matcher(settings_path=None, needle: str = HOOK_BASENAME) -> str:
    """The matcher of the `.claude/settings.json` group that wires this hook, or ''.

    Documentation self-checking, NEVER a decision input: the wiring paragraph in the docstring
    contradicted the shipped JSON at 22df0be2 (claude F9 / codex finding 10) precisely because
    nothing compared them. The self-test does, through this function. Returns '' on any error,
    including a settings file that is simply not there (an isolated copy of this hook).
    """
    try:
        path = (Path(settings_path) if settings_path
                else Path(__file__).resolve().parent.parent / "settings.json")
        data = json.loads(path.read_text(encoding="utf-8"))
        for groups in (data.get("hooks") or {}).values():
            for group in groups or []:
                for hook in (group.get("hooks") or []):
                    if needle in str(hook.get("command") or ""):
                        return str(group.get("matcher") or "")
    except Exception:
        return ""
    return ""


def decide(payload: dict):
    """(action, message, detail) with action in {'allow', 'warn', 'block', 'bypass'}.

    Touches the filesystem to stat and read the Write target, to count replace_all occurrences, and
    to consume the escape sentinel -- the last only AFTER a threshold has tripped, so an ordinary
    edit cannot burn it.
    """
    if BLOCK_SEVERITY == "off":
        return "allow", "", ""
    lines, chars, total_lines, total_chars, kind = payload_size(payload)
    if not kind:
        return "allow", "", ""
    trip = over_threshold(lines, chars, total_lines, total_chars)
    if not trip:
        return "allow", "", ""
    detail = fire_detail(kind, lines, chars, total_lines, total_chars, trip)
    blocking = BLOCK_SEVERITY == "block"
    if blocking and consume_escape():
        return "bypass", (
            "AUTHORIZED LARGE-PAYLOAD BYPASS CONSUMED: " + kind + " payload of " + str(total_lines)
            + " rendered rows / " + str(total_chars) + " rendered characters allowed because "
            + str(ESCAPE_FILE) + " was present. It has been CONSUMED, so the next such payload "
            "blocks again. Record why this one had to go through the editor tool."
        ), detail
    return (("block" if blocking else "warn"),
            _message(kind, lines, chars, trip, blocking, total_lines, total_chars),
            detail)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0                                          # fail-open on a malformed payload
    try:
        action, message, detail = decide(payload)
    except Exception:
        return 0                                          # fail-open on anything unexpected
    if action == "allow":
        return 0
    log_fire({"warn": "WARN-ALLOWED", "block": "BLOCK", "bypass": "BYPASS-AUTHORIZED"}[action],
             detail)
    print(message, file=sys.stderr)
    return 2 if action == "block" else 0


def _self_test() -> int:
    import io
    import tempfile
    import unittest

    def edit(new="", old="", tool="Edit", path="/tmp/x.md", **extra):
        ti = {"file_path": str(path), "old_string": old, "new_string": new}
        ti.update(extra)
        return {"tool_name": tool, "tool_input": ti}

    def multi(edits, path="/tmp/x.md"):
        return {"tool_name": "MultiEdit",
                "tool_input": {"file_path": str(path), "edits": edits}}

    def write(path, content):
        return {"tool_name": "Write", "tool_input": {"file_path": str(path), "content": content}}

    def nlines(n, width=4, seed="x"):
        return "\n".join(seed * width for _ in range(n))

    def vlines(n, width=4):
        """n DISTINCT lines, so a delta against nlines(n) is a full replacement."""
        return "\n".join(("%0*d" % (width, i)) for i in range(n))

    def run_main(payload):
        """(exit_code, stderr, stdout) from an ACTUAL main() call."""
        saved = (sys.stdin, sys.stdout, sys.stderr)
        sys.stdin = io.StringIO(json.dumps(payload))
        sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
        try:
            code = main()
            return code, sys.stderr.getvalue(), sys.stdout.getvalue()
        finally:
            sys.stdin, sys.stdout, sys.stderr = saved

    class T(unittest.TestCase):
        def setUp(self):
            global ESCAPE_FILE, FIRE_LOG, BLOCK_SEVERITY, LINE_THRESHOLD, CHAR_THRESHOLD, \
                TOTAL_LINE_THRESHOLD, TOTAL_CHAR_THRESHOLD, INCLUDE_OLD_STRING, \
                WARN_ON_LARGE_CREATE, MAX_COMPARE_BYTES, MAX_SCAN_BYTES
            self._root = Path(tempfile.mkdtemp())
            self._saved = (ESCAPE_FILE, FIRE_LOG, BLOCK_SEVERITY, LINE_THRESHOLD, CHAR_THRESHOLD,
                           TOTAL_LINE_THRESHOLD, TOTAL_CHAR_THRESHOLD, INCLUDE_OLD_STRING,
                           WARN_ON_LARGE_CREATE, MAX_COMPARE_BYTES, MAX_SCAN_BYTES)
            ESCAPE_FILE = self._root / ".allow-large-edit"
            FIRE_LOG = self._root / "guard-fires.tsv"

        def tearDown(self):
            global ESCAPE_FILE, FIRE_LOG, BLOCK_SEVERITY, LINE_THRESHOLD, CHAR_THRESHOLD, \
                TOTAL_LINE_THRESHOLD, TOTAL_CHAR_THRESHOLD, INCLUDE_OLD_STRING, \
                WARN_ON_LARGE_CREATE, MAX_COMPARE_BYTES, MAX_SCAN_BYTES
            (ESCAPE_FILE, FIRE_LOG, BLOCK_SEVERITY, LINE_THRESHOLD, CHAR_THRESHOLD,
             TOTAL_LINE_THRESHOLD, TOTAL_CHAR_THRESHOLD, INCLUDE_OLD_STRING,
             WARN_ON_LARGE_CREATE, MAX_COMPARE_BYTES, MAX_SCAN_BYTES) = self._saved

        # --- scope ---------------------------------------------------------------------------
        def test_unrelated_tool_allowed(self):
            self.assertEqual(decide({"tool_name": "Bash",
                                     "tool_input": {"command": nlines(500)}})[0], "allow")

        def test_missing_tool_input_allowed(self):
            self.assertEqual(decide({"tool_name": "Edit"})[0], "allow")
            self.assertEqual(decide({})[0], "allow")

        def test_non_dict_tool_input_allowed(self):
            self.assertEqual(decide({"tool_name": "Edit", "tool_input": "oops"})[0], "allow")

        # --- Edit ----------------------------------------------------------------------------
        def test_tiny_edit_allowed(self):
            self.assertEqual(decide(edit(new="one short line"))[0], "allow")

        def test_edit_at_threshold_allowed(self):
            self.assertEqual(decide(edit(new=vlines(LINE_THRESHOLD)))[0], "allow")

        def test_edit_over_threshold_warns(self):
            action, msg, _d = decide(edit(new=vlines(LINE_THRESHOLD + 1)))
            self.assertEqual(action, "warn")
            self.assertIn("sed -i", msg)
            self.assertIn("WARNING", msg)

        def test_large_deletion_is_caught_via_old_string(self):
            # the new_string is one line; the RED block is 40 rows
            self.assertEqual(decide(edit(new="x", old=vlines(40)))[0], "warn")

        def test_include_old_string_false_reverts_to_the_order_as_written(self):
            global INCLUDE_OLD_STRING
            INCLUDE_OLD_STRING = False
            self.assertEqual(decide(edit(new="x", old=vlines(40)))[0], "allow")

        # --- review finding 2: the render, not the largest field -------------------------------
        def test_six_old_plus_six_new_renders_twelve_rows_and_warns(self):
            # The seed measured this as (6, 11) and ALLOWED it. Twelve rows render.
            action, msg, _d = decide(edit(old=nlines(6, seed="a"), new=nlines(6, seed="b")))
            self.assertEqual(action, "warn")
            self.assertIn("rendered rows", msg)

        def test_rendered_delta_counts_removed_plus_added(self):
            self.assertEqual(rendered_delta("a\nb\nc", "x\ny\nz"), (6, 6))

        # --- review finding 4: false WARNs on a small or empty rendered delta -------------------
        def test_identical_old_and_new_render_nothing(self):
            same = vlines(7)
            self.assertEqual(rendered_delta(same, same), (0, 0))
            self.assertEqual(decide(edit(old=same, new=same))[0], "allow")

        def test_large_anchor_with_one_changed_line_is_two_rows(self):
            old = vlines(40)
            new = old.replace("0007", "SEVN")
            self.assertEqual(rendered_delta(old, new)[0], 2)
            self.assertEqual(decide(edit(old=old, new=new))[0], "allow")

        # --- review finding 1: the CHARACTER threshold must be independent ----------------------
        def test_char_threshold_is_not_lost_to_a_larger_line_count(self):
            # The seed's lexicographic max picked the 6-line field and never saw 1,300 characters.
            payload = edit(old=nlines(3), new="a" * (CHAR_THRESHOLD + 100))
            lines, chars, tl, tc, kind = payload_size(payload)
            self.assertLessEqual(lines, LINE_THRESHOLD)
            self.assertGreater(chars, CHAR_THRESHOLD)
            self.assertEqual(over_threshold(lines, chars, tl, tc), "chars")
            action, msg, _d = decide(payload)
            self.assertEqual(action, "warn")
            self.assertIn("CHAR_THRESHOLD", msg)

        def test_six_short_old_lines_plus_one_huge_new_line_is_caught(self):
            # The review's exact false-ALLOW probe: size was (6, 11, 'Edit') and it passed.
            payload = edit(old=nlines(6), new="z" * 1300)
            self.assertEqual(decide(payload)[0], "warn")

        def test_few_but_enormous_lines_trip_the_char_threshold(self):
            action, msg, _d = decide(edit(new="a" * (CHAR_THRESHOLD + 1)))
            self.assertEqual(action, "warn")
            self.assertIn("CHAR_THRESHOLD", msg)

        def test_char_threshold_disabled_by_zero(self):
            global CHAR_THRESHOLD, TOTAL_CHAR_THRESHOLD
            CHAR_THRESHOLD = 0
            TOTAL_CHAR_THRESHOLD = 0
            self.assertEqual(decide(edit(new="a" * 100000))[0], "allow")

        # --- codex finding 7: replace_all renders one hunk PER OCCURRENCE -----------------------
        def _thousand_x(self):
            target = self._root / "1000-x-lines.txt"
            target.write_text(nlines(1000, width=1), encoding="utf-8")
            return target

        def test_replace_all_counts_every_occurrence(self):
            # codex finding 7's exact probe: payload_size() was (2, 2, 2, 2, 'Edit') -> allow.
            target = self._thousand_x()
            payload = edit(path=target, old="x", new="y", replace_all=True)
            lines, chars, total_lines, total_chars, kind = payload_size(payload)
            self.assertEqual((lines, chars), (2, 2))          # one occurrence still renders 2 rows
            self.assertEqual(total_lines, 2000)               # 1,000 occurrences, 2 rows each
            self.assertEqual(total_chars, 2000)
            self.assertIn("replace_all", kind)
            self.assertNotIn("assumed", kind)
            action, msg, _d = decide(payload)
            self.assertEqual(action, "warn")
            self.assertIn("TOTAL_LINE_THRESHOLD", msg)
            self.assertIn("ONE HUNK PER OCCURRENCE", msg)

        def test_the_same_edit_without_replace_all_is_one_replacement(self):
            target = self._thousand_x()
            lines, chars, total_lines, total_chars, kind = payload_size(
                edit(path=target, old="x", new="y"))
            self.assertEqual((total_lines, total_chars), (2, 2))
            self.assertEqual(kind, "Edit")
            self.assertEqual(decide(edit(path=target, old="x", new="y"))[0], "allow")

        def test_replace_all_of_a_few_occurrences_still_allowed(self):
            target = self._root / "three.txt"
            target.write_text("x\nkeep\nx\nkeep\nx\n", encoding="utf-8")
            payload = edit(path=target, old="x", new="y", replace_all=True)
            self.assertEqual(payload_size(payload)[2], 6)     # 3 occurrences x 2 rendered rows
            self.assertEqual(decide(payload)[0], "allow")

        def test_replace_all_multiline_occurrence_is_multiplied(self):
            target = self._root / "blocks.txt"
            target.write_text("a\nb\n" * 4, encoding="utf-8")
            payload = edit(path=target, old="a\nb", new="c\nd", replace_all=True)
            lines, chars, total_lines, _tc, _k = payload_size(payload)
            self.assertEqual(lines, 4)                        # 2 removed + 2 added per occurrence
            self.assertEqual(total_lines, 16)                 # times 4 occurrences
            self.assertEqual(decide(payload)[0], "warn")      # 16 > TOTAL_LINE_THRESHOLD

        def test_replace_all_with_unreadable_target_warns_conservatively(self):
            # Multiplicity cannot be established: a missing path must WARN, not fail open.
            payload = edit(path=self._root / "nope.txt", old="x", new="y", replace_all=True)
            lines, chars, total_lines, _tc, kind = payload_size(payload)
            self.assertEqual(lines, 2)
            self.assertEqual(total_lines, 2 * UNKNOWN_MULTIPLICITY)
            self.assertIn("assumed", kind)
            action, msg, _d = decide(payload)
            self.assertEqual(action, "warn")
            self.assertIn("conservative count was assumed", msg)

        def test_replace_all_over_max_compare_bytes_warns_conservatively(self):
            global MAX_COMPARE_BYTES
            MAX_COMPARE_BYTES = 4
            target = self._thousand_x()
            self.assertIn("assumed", payload_size(
                edit(path=target, old="x", new="y", replace_all=True))[4])
            self.assertEqual(decide(edit(path=target, old="x", new="y", replace_all=True))[0],
                             "warn")

        def test_replace_all_that_renders_nothing_is_still_allowed(self):
            # An identical old/new pair renders zero rows, so any multiplicity is zero rows.
            same = vlines(7)
            payload = edit(path=self._root / "nope.txt", old=same, new=same, replace_all=True)
            self.assertEqual(payload_size(payload)[2], 0)
            self.assertEqual(decide(payload)[0], "allow")

        def test_replacement_count_contract(self):
            target = self._thousand_x()
            self.assertEqual(replacement_count(target, {"old_string": "x", "new_string": "y"}),
                             (1, False))
            self.assertEqual(replacement_count(target, {"old_string": "x", "new_string": "y",
                                                        "replace_all": True}), (1000, False))
            self.assertEqual(replacement_count("", {"old_string": "x", "replace_all": True}),
                             (UNKNOWN_MULTIPLICITY, True))
            self.assertEqual(replacement_count(target, {"old_string": "", "replace_all": True}),
                             (UNKNOWN_MULTIPLICITY, True))
            self.assertEqual(replacement_count(target, {"old_string": "absent-token",
                                                        "replace_all": True}), (1, False))
            self.assertEqual(replacement_count(target, "not-a-dict"), (1, False))

        # --- MultiEdit: the TOTAL render, a deliberate reversal of the seed ----------------------
        def test_multiedit_total_render_is_measured_not_the_largest_edit(self):
            # DELIBERATE REVERSAL: the seed allowed this ("largest single edit, not the sum").
            # Fifty one-line edits render one hundred rows in a single tool call.
            small = [{"old_string": "a", "new_string": "b"} for _ in range(50)]
            lines, chars, total_lines, total_chars, kind = payload_size(multi(small))
            self.assertEqual(lines, 2)
            self.assertEqual(total_lines, 100)
            action, msg, _d = decide(multi(small))
            self.assertEqual(action, "warn")
            self.assertIn("TOTAL_LINE_THRESHOLD", msg)

        def test_multiedit_of_a_few_tiny_edits_still_allowed(self):
            small = [{"old_string": "a", "new_string": "b"} for _ in range(5)]
            self.assertEqual(decide(multi(small))[0], "allow")

        def test_multiedit_single_large_hunk_trips_the_per_hunk_threshold(self):
            edits = [{"old_string": "a", "new_string": "b"},
                     {"old_string": "", "new_string": vlines(LINE_THRESHOLD + 1)}]
            action, msg, _d = decide(multi(edits))
            self.assertEqual(action, "warn")
            self.assertIn("LINE_THRESHOLD", msg)

        def test_multiedit_replace_all_entry_is_multiplied_out(self):
            target = self._thousand_x()
            edits = [{"old_string": "keep", "new_string": "kept"},
                     {"old_string": "x", "new_string": "y", "replace_all": True}]
            lines, chars, total_lines, total_chars, kind = payload_size(multi(edits, path=target))
            self.assertEqual(lines, 2)
            self.assertEqual(total_lines, 2 + 2000)
            self.assertIn("replace_all", kind)
            self.assertEqual(decide(multi(edits, path=target))[0], "warn")

        def test_multiedit_malformed_entries_ignored(self):
            self.assertEqual(decide(multi(["not-a-dict", None]))[0], "allow")

        def test_total_thresholds_disabled_by_zero(self):
            global TOTAL_LINE_THRESHOLD, TOTAL_CHAR_THRESHOLD
            TOTAL_LINE_THRESHOLD = 0
            TOTAL_CHAR_THRESHOLD = 0
            small = [{"old_string": "a", "new_string": "b"} for _ in range(50)]
            self.assertEqual(decide(multi(small))[0], "allow")

        # --- codex finding 9: a large CREATE is a green wall and must be measured ----------------
        def test_large_new_file_write_is_measured_and_warns(self):
            # codex finding 9's exact probe: exit 0, no warning, payload_size() (0,0,0,0,'').
            target = self._root / "brand-new.md"
            lines, chars, total_lines, total_chars, kind = payload_size(write(target, nlines(5000)))
            self.assertEqual(lines, 5000)
            self.assertEqual(total_lines, 5000)
            self.assertIn("new-file", kind)
            action, msg, _d = decide(write(target, nlines(5000)))
            self.assertEqual(action, "warn")
            self.assertIn("LINE_THRESHOLD", msg)
            self.assertFalse(target.exists(), "the guard must not create the target")

        def test_large_new_file_write_warns_end_to_end(self):
            code, err, out = run_main(write(self._root / "brand-new-e2e.md", nlines(5000)))
            self.assertEqual((code, out), (0, ""))
            self.assertIn("WARNING", err)
            self.assertNotIn("BLOCKED", err)
            row = FIRE_LOG.read_text(encoding="utf-8").rstrip("\n").split("\t")
            self.assertIn("kind=Write(new-file)", row[3])

        def test_create_default_is_guarded(self):
            self.assertTrue(WARN_ON_LARGE_CREATE,
                            "codex finding 9: a large create must not fail open by configuration")

        def test_small_new_file_write_allowed(self):
            self.assertEqual(decide(write(self._root / "tiny-new.md", "one line\n"))[0], "allow")

        def test_create_guard_can_be_reverted_by_the_constant(self):
            global WARN_ON_LARGE_CREATE
            WARN_ON_LARGE_CREATE = False
            self.assertEqual(decide(write(self._root / "brand-new-3.md", nlines(5000)))[0], "allow")

        def test_create_warning_offers_a_heredoc_and_never_claims_creates_are_allowed(self):
            _a, msg, _d = decide(write(self._root / "brand-new-4.md", nlines(5000)))
            self.assertIn("cat > <file> <<'EOF'", msg)
            self.assertIn("green rows", msg)
            self.assertNotIn("always allowed", msg)
            self.assertNotIn("sed -i", msg, "a create has no sed remedy; do not prescribe one")

        def test_create_char_units_match_the_edit_path(self):
            # claude F10: the create path used _measure(), whose chars INCLUDE newlines.
            body = "abcd\nefgh\n"
            self.assertEqual(payload_size(write(self._root / "units.md", body))[1], 8)
            self.assertEqual(rendered_delta("", body)[1], 8)
            self.assertEqual(_measure(body)[1], 10)

        # --- Write to an existing file -----------------------------------------------------------
        def test_write_to_existing_file_over_threshold_warns(self):
            target = self._root / "exists.md"
            target.write_text("old\n", encoding="utf-8")
            self.assertEqual(decide(write(target, vlines(LINE_THRESHOLD + 1)))[0], "warn")

        def test_write_to_existing_file_tiny_allowed(self):
            target = self._root / "exists.md"
            target.write_text("old\n", encoding="utf-8")
            self.assertEqual(decide(write(target, "one line"))[0], "allow")

        def test_write_of_identical_existing_content_renders_nothing(self):
            # review finding 4: a byte-identical 400-line rewrite WARNed in the seed.
            target = self._root / "same.md"
            body = vlines(400)
            target.write_text(body, encoding="utf-8")
            self.assertEqual(decide(write(target, body))[0], "allow")

        def test_write_of_one_changed_line_in_a_large_file_allowed(self):
            target = self._root / "big.md"
            body = vlines(400)
            target.write_text(body, encoding="utf-8")
            self.assertEqual(decide(write(target, body.replace("0100", "MMMM")))[0], "allow")

        def test_write_with_no_path_fails_open(self):
            self.assertEqual(decide({"tool_name": "Write",
                                     "tool_input": {"content": nlines(500)}})[0], "allow")

        def test_write_directory_target_fails_open(self):
            # An EXISTING non-file target is not a create: the tool call cannot succeed and nothing
            # renders, so measuring it as a 500-row green wall would be a false WARN.
            self.assertEqual(decide(write(self._root, nlines(500)))[0], "allow")
            self.assertEqual(payload_size(write(self._root, nlines(500)))[4], "")

        def test_relative_write_path_resolves_against_project_dir(self):
            # review finding 5: resolving against the hook process cwd can mistake an existing
            # project file for a new file and skip the guard entirely.
            target = self._root / "rel.md"
            target.write_text("old\n", encoding="utf-8")
            saved = os.environ.get("CLAUDE_PROJECT_DIR")
            os.environ["CLAUDE_PROJECT_DIR"] = str(self._root)
            try:
                self.assertEqual(decide(write("rel.md", vlines(LINE_THRESHOLD + 1)))[0], "warn")
            finally:
                if saved is None:
                    os.environ.pop("CLAUDE_PROJECT_DIR", None)
                else:
                    os.environ["CLAUDE_PROJECT_DIR"] = saved

        # --- codex finding 8: an oversized DELETION must be measured as the deletion -------------
        def test_deletion_of_a_comparable_file_warns(self):
            target = self._root / "deleteme.md"
            target.write_text(vlines(50), encoding="utf-8")
            lines, _c, total_lines, _tc, kind = payload_size(write(target, ""))
            self.assertEqual(lines, 50)
            self.assertEqual(kind, "Write")
            self.assertEqual(decide(write(target, ""))[0], "warn")

        def test_oversized_deletion_warns_instead_of_measuring_the_empty_payload(self):
            # codex finding 8's probe: _read_existing() None -> payload_size() (0,0,0,0,'Write').
            global MAX_COMPARE_BYTES
            MAX_COMPARE_BYTES = 4
            target = self._root / "huge.md"
            body = vlines(50)
            target.write_text(body, encoding="utf-8")
            self.assertIsNone(_read_existing(target))
            lines, chars, total_lines, total_chars, kind = payload_size(write(target, ""))
            self.assertEqual(lines, 50, "every removed row must be counted")
            self.assertEqual(chars, len(body))
            self.assertIn("uncomparable", kind)
            action, msg, _d = decide(write(target, ""))
            self.assertEqual(action, "warn")
            self.assertIn("too large to read", msg)

        def test_oversized_rewrite_counts_both_sides(self):
            global MAX_COMPARE_BYTES
            MAX_COMPARE_BYTES = 4
            target = self._root / "huge2.md"
            target.write_text(vlines(50), encoding="utf-8")
            self.assertEqual(payload_size(write(target, vlines(30)))[0], 80)  # 50 red + 30 green

        def test_uncomparable_existing_file_still_warns_on_identical_content(self):
            # Unchanged direction of travel: with no comparison possible the fallback over-warns.
            global MAX_COMPARE_BYTES
            MAX_COMPARE_BYTES = 4
            target = self._root / "huge3.md"
            body = vlines(50)
            target.write_text(body, encoding="utf-8")
            self.assertEqual(decide(write(target, body))[0], "warn")

        def test_uncomparable_deletion_respects_include_old_string(self):
            global MAX_COMPARE_BYTES, INCLUDE_OLD_STRING
            MAX_COMPARE_BYTES = 4
            INCLUDE_OLD_STRING = False
            target = self._root / "huge4.md"
            target.write_text(vlines(50), encoding="utf-8")
            self.assertEqual(payload_size(write(target, ""))[0], 0)
            self.assertEqual(decide(write(target, ""))[0], "allow")

        def test_existing_metrics_line_semantics(self):
            trailing = self._root / "trailing.txt"
            trailing.write_text("a\nb\n", encoding="utf-8")
            self.assertEqual(existing_metrics(trailing), (4, 2))
            bare = self._root / "bare.txt"
            bare.write_text("a\nb", encoding="utf-8")
            self.assertEqual(existing_metrics(bare), (3, 2))
            empty = self._root / "empty.txt"
            empty.write_text("", encoding="utf-8")
            self.assertEqual(existing_metrics(empty), (0, 0))
            self.assertIsNone(existing_metrics(self._root / "absent.txt"))

        def test_existing_metrics_estimates_above_the_scan_cap(self):
            global MAX_SCAN_BYTES
            MAX_SCAN_BYTES = 4
            target = self._root / "over-scan.txt"
            target.write_text(vlines(50), encoding="utf-8")
            size, lines = existing_metrics(target)
            self.assertEqual(size, target.stat().st_size)
            self.assertGreaterEqual(lines, 1)

        def test_existing_metrics_streams_a_multi_chunk_file(self):
            target = self._root / "multi-chunk.txt"
            target.write_text("y" * (1 << 21) + "\n", encoding="utf-8")
            self.assertEqual(existing_metrics(target)[1], 1)

        # --- severity -----------------------------------------------------------------------------
        def test_block_severity_block(self):
            global BLOCK_SEVERITY
            BLOCK_SEVERITY = "block"
            action, msg, _d = decide(edit(new=vlines(LINE_THRESHOLD + 1)))
            self.assertEqual(action, "block")
            self.assertIn("BLOCKED", msg)
            self.assertIn(str(ESCAPE_FILE), msg)

        def test_block_severity_off(self):
            global BLOCK_SEVERITY
            BLOCK_SEVERITY = "off"
            self.assertEqual(decide(edit(new=vlines(500)))[0], "allow")

        # --- escape sentinel: atomic, verified consumption ------------------------------------------
        def test_escape_consumed_only_in_block_mode(self):
            global BLOCK_SEVERITY
            BLOCK_SEVERITY = "block"
            ESCAPE_FILE.write_text("", encoding="utf-8")
            action, msg, _d = decide(edit(new=vlines(LINE_THRESHOLD + 1)))
            self.assertEqual(action, "bypass")
            self.assertIn("CONSUMED", msg)
            self.assertFalse(ESCAPE_FILE.exists())
            self.assertEqual(decide(edit(new=vlines(LINE_THRESHOLD + 1)))[0], "block")

        def test_escape_not_burned_by_a_small_edit(self):
            global BLOCK_SEVERITY
            BLOCK_SEVERITY = "block"
            ESCAPE_FILE.write_text("", encoding="utf-8")
            self.assertEqual(decide(edit(new="one line"))[0], "allow")
            self.assertTrue(ESCAPE_FILE.exists())

        def test_escape_ignored_in_warn_mode(self):
            ESCAPE_FILE.write_text("", encoding="utf-8")
            self.assertEqual(decide(edit(new=vlines(LINE_THRESHOLD + 1)))[0], "warn")
            self.assertTrue(ESCAPE_FILE.exists(), "warn mode must not spend an authorization")

        def test_escape_directory_grants_nothing(self):
            # review finding 6: the seed entered the bypass branch on a bare exists().
            global BLOCK_SEVERITY
            BLOCK_SEVERITY = "block"
            ESCAPE_FILE.mkdir()
            self.assertEqual(decide(edit(new=vlines(LINE_THRESHOLD + 1)))[0], "block")
            self.assertTrue(ESCAPE_FILE.is_dir(), "a directory sentinel must survive untouched")

        def test_escape_symlink_grants_nothing(self):
            global BLOCK_SEVERITY
            BLOCK_SEVERITY = "block"
            real = self._root / "real-target"
            real.write_text("", encoding="utf-8")
            ESCAPE_FILE.symlink_to(real)
            self.assertEqual(decide(edit(new=vlines(LINE_THRESHOLD + 1)))[0], "block")
            self.assertTrue(real.exists(), "a symlinked sentinel must not consume its target")

        def test_escape_consumption_is_once_only_under_repetition(self):
            global BLOCK_SEVERITY
            BLOCK_SEVERITY = "block"
            ESCAPE_FILE.write_text("", encoding="utf-8")
            actions = [decide(edit(new=vlines(LINE_THRESHOLD + 1)))[0] for _ in range(3)]
            self.assertEqual(actions, ["bypass", "block", "block"])

        def test_consume_escape_returns_false_when_absent(self):
            self.assertFalse(consume_escape())

        # --- register / calibration telemetry --------------------------------------------------------
        def test_log_fire_writes_a_four_column_row(self):
            self.assertTrue(log_fire("WARN-ALLOWED", "detail  with   spaces\nand a newline"))
            row = FIRE_LOG.read_text(encoding="utf-8").rstrip("\n")
            self.assertEqual(len(row.split("\t")), 4)
            self.assertNotIn("\n", row)
            self.assertIn("block-large-editwrite-payload", row)

        def test_log_fire_returns_false_when_unwritable(self):
            global FIRE_LOG
            FIRE_LOG = self._root / "no-such-dir" / "guard-fires.tsv"
            self.assertFalse(log_fire("WARN-ALLOWED", "x"))

        def test_warn_is_logged_with_the_calibration_fields(self):
            code, err, out = run_main(edit(new=vlines(LINE_THRESHOLD + 1)))
            self.assertEqual(code, 0)
            self.assertTrue(FIRE_LOG.exists(), "a WARN fire must be logged")
            row = FIRE_LOG.read_text(encoding="utf-8").rstrip("\n").split("\t")
            self.assertEqual(row[1], "WARN-ALLOWED")
            for field in ("kind=", "hunk_lines=", "hunk_chars=", "total_lines=", "total_chars=",
                          "trip=", "thresholds=", "severity="):
                self.assertIn(field, row[3])

        def test_estimated_kinds_are_marked_in_the_register(self):
            # Calibration must be able to drop rows whose totals are assumptions, not measurements.
            code, err, out = run_main(edit(path=self._root / "nope.txt", old="x", new="y",
                                           replace_all=True))
            self.assertEqual(code, 0)
            detail = FIRE_LOG.read_text(encoding="utf-8").rstrip("\n").split("\t")[3]
            self.assertIn("kind=Edit(replace_all,assumed)", detail)

        def test_fire_detail_carries_no_payload_content_or_path(self):
            secret = "SECRET-PAYLOAD-TEXT"
            code, err, out = run_main(edit(new="\n".join([secret] * 20)))
            self.assertEqual(code, 0)
            written = FIRE_LOG.read_text(encoding="utf-8")
            self.assertNotIn(secret, written)
            self.assertNotIn("/tmp/x.md", written)

        def test_log_failure_never_costs_a_warning(self):
            global FIRE_LOG
            FIRE_LOG = self._root / "no-such-dir" / "guard-fires.tsv"
            code, err, out = run_main(edit(new=vlines(LINE_THRESHOLD + 1)))
            self.assertEqual(code, 0)
            self.assertIn("WARNING", err)

        def test_allow_writes_no_register_row(self):
            run_main(edit(new="one short line"))
            self.assertFalse(FIRE_LOG.exists(), "an allowed call must not log a fire")

        # --- end-to-end protocol ----------------------------------------------------------------------
        def test_warn_protocol_is_exit_zero_no_stdout_stderr_warning(self):
            code, err, out = run_main(edit(new=vlines(LINE_THRESHOLD + 1)))
            self.assertEqual(code, 0)
            self.assertEqual(out, "")
            self.assertIn("WARNING", err)
            self.assertNotIn("BLOCKED", err)

        def test_block_protocol_is_exit_two(self):
            global BLOCK_SEVERITY
            BLOCK_SEVERITY = "block"
            code, err, out = run_main(edit(new=vlines(LINE_THRESHOLD + 1)))
            self.assertEqual(code, 2)
            self.assertEqual(out, "")
            self.assertIn("BLOCKED", err)

        def test_allow_protocol_is_silent(self):
            code, err, out = run_main(edit(new="one short line"))
            self.assertEqual((code, err, out), (0, "", ""))

        def test_malformed_payload_fails_open(self):
            saved = (sys.stdin, sys.stdout, sys.stderr)
            sys.stdin = io.StringIO("not json")
            sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
            try:
                self.assertEqual(main(), 0)
            finally:
                sys.stdin, sys.stdout, sys.stderr = saved

        def test_hostile_paths_never_raise_through_main(self):
            # Every new filesystem read (occurrence count, byte size, newline scan) must fail open.
            for payload in (edit(path="\0bad", old="x", new="y", replace_all=True),
                            write("\0bad", nlines(50)),
                            write(self._root / "absent-dir" / "f.md", nlines(50))):
                code, err, out = run_main(payload)
                self.assertIn(code, (0, 2))
                self.assertEqual(out, "")

        # --- measurement purity ---------------------------------------------------------------------
        def test_measure(self):
            self.assertEqual(_measure(""), (0, 0))
            self.assertEqual(_measure(None), (0, 0))
            self.assertEqual(_measure("a"), (1, 1))
            self.assertEqual(_measure("a\nb"), (2, 3))
            self.assertEqual(_measure("a\n"), (1, 2))

        def test_rendered_delta_edges(self):
            self.assertEqual(rendered_delta(None, None), (0, 0))
            self.assertEqual(rendered_delta("", "a"), (1, 1))
            self.assertEqual(rendered_delta("a", ""), (1, 1))
            self.assertEqual(rendered_delta("a\nb", "a\nb"), (0, 0))

        def test_crlf_text_at_the_boundary(self):
            body = "\r\n".join("%04d" % i for i in range(LINE_THRESHOLD + 1))
            self.assertEqual(rendered_delta("", body)[0], LINE_THRESHOLD + 1)
            self.assertEqual(decide(edit(new=body))[0], "warn")

        def test_over_threshold_pure_and_independent(self):
            self.assertEqual(over_threshold(LINE_THRESHOLD, 0), "")
            self.assertEqual(over_threshold(LINE_THRESHOLD + 1, 0), "lines")
            self.assertEqual(over_threshold(1, CHAR_THRESHOLD + 1), "chars")
            self.assertEqual(over_threshold(1, 1, TOTAL_LINE_THRESHOLD + 1, 1), "total-lines")
            self.assertEqual(over_threshold(1, 1, 1, TOTAL_CHAR_THRESHOLD + 1), "total-chars")

        def test_kind_composition(self):
            self.assertEqual(_kind("Edit"), "Edit")
            self.assertEqual(_kind("Edit", "", ""), "Edit")
            self.assertEqual(_kind("Edit", "replace_all", "assumed"), "Edit(replace_all,assumed)")
            self.assertNotIn(" ", _kind("Write", "new-file"))

        # --- the message must be actionable and must not lie about what happened -----------------------
        def test_message_names_the_alternatives_and_the_three_headers(self):
            msg = _message("Edit", 40, 900, "lines", False)
            for needle in ("WARNING", "WHY:", "CONSIDER-INSTEAD:", "sed -i", "python3 - <<",
                           "WARN_ON_LARGE_CREATE"):
                self.assertIn(needle, msg)

        def test_warn_message_never_says_blocked(self):
            self.assertNotIn("BLOCKED", _message("Edit", 40, 900, "lines", False))

        def test_block_message_uses_the_blocked_header(self):
            msg = _message("Edit", 40, 900, "lines", True)
            self.assertIn("BLOCKED", msg)
            self.assertIn("WHY:", msg)
            self.assertIn("CONSIDER-INSTEAD:", msg)

        def test_each_trip_has_its_own_message_text(self):
            for trip, needle in (("lines", "LINE_THRESHOLD"), ("chars", "CHAR_THRESHOLD"),
                                 ("total-lines", "TOTAL_LINE_THRESHOLD"),
                                 ("total-chars", "TOTAL_CHAR_THRESHOLD")):
                self.assertIn(needle, _message("Edit", 40, 9000, trip, False, 40, 9000))

        def test_no_message_prescribes_a_command_a_sibling_hook_refuses(self):
            # Every heredoc this hook recommends must QUOTE its delimiter: the sibling Bash hook
            # scans an unquoted heredoc body as live shell text and can refuse it.
            for kind in ("Edit", "Write", "Write(new-file)", "Write(uncomparable)"):
                msg = _message(kind, 40, 900, "lines", False)
                for line in msg.splitlines():
                    if "<<" in line:
                        self.assertRegex(line, r"<<'[A-Z]+'")

        # --- claude F9 / codex finding 10: the wiring paragraph must match the wiring --------------
        def test_docstring_states_the_shipped_matcher(self):
            doc = __doc__ or ""
            self.assertIn('`"' + WIRED_MATCHER + '"`', doc)
            self.assertEqual(WIRED_MATCHER, "Edit|Write")

        def test_docstring_carries_no_contradictory_wiring_instruction(self):
            doc = __doc__ or ""
            for stale in ("Edit|Write|MultiEdit", "DEDICATED matcher", "dead code and leaves",
                          "open bypass", "ORCHESTRATOR MUST RESOLVE", "RECONCILIATION OWED"):
                self.assertNotIn(stale, doc,
                                 "the file must not instruct a wiring it is not wired with")

        def test_docstring_does_not_claim_creates_are_always_allowed(self):
            doc = __doc__ or ""
            self.assertNotIn("still allowed at any size", doc)
            self.assertNotIn("always allowed", doc)
            self.assertIn("MEASURED and WARNED", doc)

        def test_docstring_matches_a_settings_file_that_wires_this_hook(self):
            settings = self._root / "settings.json"
            settings.write_text(json.dumps({"hooks": {"PreToolUse": [
                {"matcher": "Bash", "hooks": [{"command": "python3 other.py"}]},
                {"matcher": WIRED_MATCHER,
                 "hooks": [{"command": 'python3 "$CLAUDE_PROJECT_DIR"/.claude/hooks/'
                                       + HOOK_BASENAME}]}]}}), encoding="utf-8")
            self.assertEqual(settings_matcher(settings), WIRED_MATCHER)

        def test_settings_matcher_is_inert_on_anything_unreadable(self):
            self.assertEqual(settings_matcher(self._root / "no-settings.json"), "")
            bad = self._root / "bad.json"
            bad.write_text("{not json", encoding="utf-8")
            self.assertEqual(settings_matcher(bad), "")
            empty = self._root / "empty.json"
            empty.write_text("{}", encoding="utf-8")
            self.assertEqual(settings_matcher(empty), "")

        def test_shipped_settings_agrees_with_the_docstring_when_present(self):
            # In the repo this asserts the real wiring. In an isolated copy of the hook there is no
            # settings.json to read, and the check is skipped rather than faked.
            wired = settings_matcher()
            if not wired:
                self.skipTest("no .claude/settings.json beside this hook")
            self.assertEqual(wired, WIRED_MATCHER,
                             "settings.json and the docstring must not disagree again")

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        sys.exit(_self_test())
    sys.exit(main())