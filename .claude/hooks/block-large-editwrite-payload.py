#!/usr/bin/env python3
"""PreToolUse hook (Edit / Write / MultiEdit): a large tool payload IS the forbidden console wall.

PR1b ACTIVATION CANDIDATE, hardened 2026-08-09 against the seed deep review
(`inbox/deliveries/seed-review-pr1b-codex.md`). Wiring: install as
`.claude/hooks/block-large-editwrite-payload.py` under a DEDICATED matcher
`"Edit|Write|MultiEdit"`, command
`python3 "$CLAUDE_PROJECT_DIR"/.claude/hooks/block-large-editwrite-payload.py`.
The pinned settings only has `"Edit|Write"`, so leaving that matcher unchanged makes the MultiEdit
support here dead code and leaves MultiEdit an open bypass. A dedicated entry also avoids silently
invoking every existing Edit/Write sibling hook on MultiEdit payloads they were never tested against.

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
    * Write to an EXISTING file diffs the new `content` against the file on disk, so a byte-identical
      rewrite renders nothing and no longer warns.
    * LINES and CHARACTERS are evaluated INDEPENDENTLY, never selected against each other.

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

  3. A Write that CREATES a file is still allowed at any size (WARN_ON_LARGE_CREATE = False). There
     is no red/green comparison and no sanctioned `sed -i` alternative for a file that does not
     exist yet, and the pinned hard-rule sentence is limited to changes to EXISTING files. This is a
     REAL hole in the "a large tool payload is the wall" headline -- a 5,000-line create does render
     5,000 green rows -- so it is a constant the orchestrator can flip, not a silent exclusion.

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
    batching is being punished or correctly caught.

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

PATH CONTRACT for Write. `file_path` is expected to be ABSOLUTE. A relative path is resolved against
`CLAUDE_PROJECT_DIR` first and the hook process cwd second, because the hook process cwd is not the
tool call's cwd and an existing project file must not be mistaken for a new file (which would skip
the guard entirely). If the harness ever guarantees absolute paths, this fallback becomes dead code
and can be deleted; until it is verified, the fallback is the safe reading.

Exit protocol (Claude Code hooks): exit 0 allows the tool call; exit 2 blocks it and feeds stderr
back to the model as the reason. FAIL-OPEN on any parse error or unreadable path.

Console format: three headers. The status header states what ACTUALLY happened -- `WARNING` when the
call proceeds, `BLOCKED` only when it does not -- followed by `WHY:` and `CONSIDER-INSTEAD:`.

RECONCILIATION OWED AT `.claude/CLAUDE.md:868` -- ORCHESTRATOR MUST RESOLVE IN THIS PR:
  * the prose calls this a hard rule, forbids more than "a couple of short lines", and reserves Edit
    for one short line. This hook allows 6 rendered rows and only WARNS at 7. Either align the
    constants and the severity with the prose, or state in the prose that this hook is a permissive
    telemetry warning and NOT mechanical enforcement of the full hard rule. Do not leave both
    statements standing.
  * the same sentence describes Write in terms of `old_string` and `new_string`; Write takes
    `content`. Correct the payload description and name MultiEdit explicitly.

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
INCLUDE_OLD_STRING = True

# A Write that CREATES a file renders green rows but has no sanctioned sed alternative.
# See design decision 3. Flip to True to guard creates too.
WARN_ON_LARGE_CREATE = False

# Upper bound on how much of an existing file the hook will read to compute the rendered delta.
MAX_COMPARE_BYTES = 2_000_000

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

    Kept as a public helper because the threshold arithmetic and the fixtures both read it. A
    terminal newline terminates the last logical line rather than adding a blank one.
    """
    rows = _lines(text)
    return (len(rows), len(text)) if rows else (0, 0)


def rendered_delta(old, new) -> tuple:
    """(rows, chars) a red/green render would actually show for old -> new.

    Common leading and trailing lines are trimmed, because the renderer shows them as unchanged
    context rather than as red/green rows. Identical strings therefore measure zero, and a large
    anchor with one changed line measures two rows, not the size of the anchor.
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


def payload_size(payload: dict) -> tuple:
    """(hunk_lines, hunk_chars, total_lines, total_chars, kind) of the console render.

    kind is '' when nothing renders. Lines and characters are carried INDEPENDENTLY: nothing here
    selects one candidate over another, which is the seed's lexicographic-tuple defect.
    """
    tool = payload.get("tool_name") or payload.get("toolName") or ""
    ti = payload.get("tool_input") or payload.get("toolInput") or {}
    if not isinstance(ti, dict):
        return 0, 0, 0, 0, ""

    if tool in EDIT_TOOLS:
        edits = ti.get("edits")
        if isinstance(edits, list) and edits:
            hunk_lines = hunk_chars = total_lines = total_chars = 0
            for e in edits:
                if not isinstance(e, dict):
                    continue
                rows, chars = rendered_delta(e.get("old_string"), e.get("new_string"))
                hunk_lines = max(hunk_lines, rows)
                hunk_chars = max(hunk_chars, chars)
                total_lines += rows
                total_chars += chars
            return hunk_lines, hunk_chars, total_lines, total_chars, "MultiEdit"
        rows, chars = rendered_delta(ti.get("old_string"), ti.get("new_string"))
        return rows, chars, rows, chars, "Edit"

    if tool in WRITE_TOOLS:
        raw = ti.get("file_path") or ti.get("path") or ""
        if not raw:
            return 0, 0, 0, 0, ""                        # unresolvable path -> fail open
        try:
            path = _resolve(raw)
            exists = path.is_file()
        except Exception:
            return 0, 0, 0, 0, ""
        content = ti.get("content")
        if not exists:
            if not WARN_ON_LARGE_CREATE:
                return 0, 0, 0, 0, ""                    # creating a new file: design decision 3
            rows, chars = _measure(content)
            return rows, chars, rows, chars, "Write"
        before = _read_existing(path)
        if before is None:
            rows, chars = _measure(content)              # unreadable: measure the payload itself
        else:
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


def _message(kind: str, lines: int, chars: int, trip: str, blocking: bool,
             total_lines=None, total_chars=None) -> str:
    if total_lines is None:
        total_lines = lines
    if total_chars is None:
        total_chars = chars
    head = "BLOCKED" if blocking else "WARNING"
    limit = _limit_text(trip, lines, chars, total_lines, total_chars)
    return (
        head + " (console payload-wall guardrail): this " + kind + " payload is " + limit + ".\n"
        "\n"
        "WHY: the Edit/Write tools RENDER their payload as a red/green diff in the console, and that "
        "render IS the wall the maintainer ruled out on 2026-07-27 after repeated violations. For a "
        "change to an EXISTING file beyond a couple of short lines the sanctioned tools are the ones "
        "that render nothing. " + ("The call has been refused." if blocking else
                                   "This is a WARNING; the call proceeds.") + "\n"
        "\n"
        "CONSIDER-INSTEAD:\n"
        "    sed -i 's/<old>/<new>/' <file>              # targeted single-line substitution\n"
        "    sed -i '<a>,<b>s/<old>/<new>/' <file>       # line-range-scoped where a token repeats\n"
        "    python3 - <<'PY'                            # read-insert-write, renders nothing\n"
        "    p='<file>'; s=open(p).read()\n"
        "    s = s.replace('<old>', '<new>')\n"
        "    open(p,'w').write(s)\n"
        "    PY\n"
        "\n"
        "  Reserve Edit/Write for a genuinely tiny change, or for CREATING a new file (always "
        "allowed).\n"
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
    """The bounded, content-free telemetry row body that calibration will read."""
    return ("kind=%s hunk_lines=%d hunk_chars=%d total_lines=%d total_chars=%d trip=%s "
            "thresholds=%d/%d/%d/%d severity=%s"
            % (kind, lines, chars, total_lines, total_chars, trip, LINE_THRESHOLD, CHAR_THRESHOLD,
               TOTAL_LINE_THRESHOLD, TOTAL_CHAR_THRESHOLD, BLOCK_SEVERITY))


def decide(payload: dict):
    """(action, message, detail) with action in {'allow', 'warn', 'block', 'bypass'}.

    Touches the filesystem to stat and read the Write target, and to consume the escape sentinel --
    the latter only AFTER a threshold has tripped, so an ordinary edit cannot burn it.
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

    def edit(new="", old="", tool="Edit"):
        return {"tool_name": tool, "tool_input": {"file_path": "/tmp/x.md",
                                                  "old_string": old, "new_string": new}}

    def multi(edits):
        return {"tool_name": "MultiEdit",
                "tool_input": {"file_path": "/tmp/x.md", "edits": edits}}

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
                WARN_ON_LARGE_CREATE
            self._root = Path(tempfile.mkdtemp())
            self._saved = (ESCAPE_FILE, FIRE_LOG, BLOCK_SEVERITY, LINE_THRESHOLD, CHAR_THRESHOLD,
                           TOTAL_LINE_THRESHOLD, TOTAL_CHAR_THRESHOLD, INCLUDE_OLD_STRING,
                           WARN_ON_LARGE_CREATE)
            ESCAPE_FILE = self._root / ".allow-large-edit"
            FIRE_LOG = self._root / "guard-fires.tsv"

        def tearDown(self):
            global ESCAPE_FILE, FIRE_LOG, BLOCK_SEVERITY, LINE_THRESHOLD, CHAR_THRESHOLD, \
                TOTAL_LINE_THRESHOLD, TOTAL_CHAR_THRESHOLD, INCLUDE_OLD_STRING, \
                WARN_ON_LARGE_CREATE
            (ESCAPE_FILE, FIRE_LOG, BLOCK_SEVERITY, LINE_THRESHOLD, CHAR_THRESHOLD,
             TOTAL_LINE_THRESHOLD, TOTAL_CHAR_THRESHOLD, INCLUDE_OLD_STRING,
             WARN_ON_LARGE_CREATE) = self._saved

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

        def test_multiedit_malformed_entries_ignored(self):
            self.assertEqual(decide(multi(["not-a-dict", None]))[0], "allow")

        def test_total_thresholds_disabled_by_zero(self):
            global TOTAL_LINE_THRESHOLD, TOTAL_CHAR_THRESHOLD
            TOTAL_LINE_THRESHOLD = 0
            TOTAL_CHAR_THRESHOLD = 0
            small = [{"old_string": "a", "new_string": "b"} for _ in range(50)]
            self.assertEqual(decide(multi(small))[0], "allow")

        # --- Write ------------------------------------------------------------------------------
        def test_write_to_new_file_always_allowed(self):
            target = self._root / "brand-new.md"
            self.assertEqual(decide(write(target, nlines(5000)))[0], "allow")

        def test_write_create_guard_can_be_enabled(self):
            global WARN_ON_LARGE_CREATE
            WARN_ON_LARGE_CREATE = True
            target = self._root / "brand-new-2.md"
            self.assertEqual(decide(write(target, nlines(5000)))[0], "warn")

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
            self.assertEqual(decide(write(self._root, nlines(500)))[0], "allow")

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

        def test_uncomparable_existing_file_falls_back_to_payload_size(self):
            # Over MAX_COMPARE_BYTES the hook cannot compute a delta, so it measures the payload
            # itself. That is the conservative direction: it can over-warn, never under-warn.
            global MAX_COMPARE_BYTES
            saved = MAX_COMPARE_BYTES
            MAX_COMPARE_BYTES = 4
            try:
                target = self._root / "huge.md"
                body = vlines(50)
                target.write_text(body, encoding="utf-8")
                self.assertIsNone(_read_existing(target))
                # byte-identical content still warns here, because no comparison was possible
                self.assertEqual(decide(write(target, body))[0], "warn")
            finally:
                MAX_COMPARE_BYTES = saved

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

        # --- the message must be actionable and must not lie about what happened -----------------------
        def test_message_names_the_alternatives_and_the_three_headers(self):
            msg = _message("Edit", 40, 900, "lines", False)
            for needle in ("WARNING", "WHY:", "CONSIDER-INSTEAD:", "sed -i", "python3 - <<",
                           "CREATING a new file"):
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

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        sys.exit(_self_test())
    sys.exit(main())
