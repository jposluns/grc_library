#!/usr/bin/env python3
"""Session-state lease audit (gate 63).

Scans [`.working/session-state.md`](.working/session-state.md) and
enforces the WELL-FORMEDNESS of the session-concurrency lease that the
multi-session interlock relies on (design record: the design-decisions
record, "Session-concurrency safety"; the
`/orch` command's step 0 reads this file before anything else).

The lease declares which orchestrator session, if any, currently holds
the shared ``main`` state surfaces. Required fields, one per line, each
a plain ``Field: value`` line (the field name at column zero, a colon and
one space, then the value). The fleet lease tool (orch_store.py) parses
``Active-session``, ``Status`` and ``Last-heartbeat-UTC`` only from lines
that begin with the name and ": ", so the Markdown bold form
(``**Status:** active``) is a finding naming the plain form (maintainer
ruling 2026-10-29 01:10Z); the other three fields use the same form so
the file has one style:

- ``Active-session:`` the active session's branch name, or
  ``none`` when no session holds the lease.
- ``Status:`` ``active`` (a session holds the lease),
  ``winding-down`` (a session is landing its closing handoff PR), or
  ``released`` (no session holds the lease; the clean-close state).
- ``Operating-mode:`` ``fully-attended``, ``attended-autonomous``,
  ``overnight-unattended``, or ``daytime-unattended``. The
  AskUserQuestion-blocking hook reads this and refuses a blocking prompt when
  the mode is unattended, so the value must always be present and current.
- ``Last-heartbeat-UTC:`` a ``YYYY-MM-DDTHH:MM:SSZ`` stamp
  (``date -u +%Y-%m-%dT%H:%M:%SZ``), refreshed at each PR close-out.
- ``Current-task:`` one line of free text.
- ``Worker-dispatches:`` ``none`` or a free-text summary of the
  in-flight worker fan-out (cross-referencing the scratch
  ``claims-ledger.md`` when parallel work is running).

Known limit: the value checks still allow trailing whitespace after a
value, and the lease is read with universal newlines, so a CR before LF
is not seen; orch_store.py reads both into the value and refuses it.

Coherence rules: ``released`` requires ``Active-session: none``;
``active`` and ``winding-down`` require a non-``none`` branch name.
Each field line appears exactly once (a duplicate is a finding), and
the coherence check runs unconditionally alongside the per-field value
checks, so coexisting defects are all reported in one run.

Field order: ``Active-session``, then ``Status``, then
``Last-heartbeat-UTC``. The session-start reader
(``tools/session_facts.py``) reports every session metric UNKNOWN when
those three appear in another order; this gate does not check the order.

Near-miss detection examines each LF-delimited line, including comments
and fences, after optional whitespace and repeated Markdown markers:
a bullet (-, + or *), or digits plus "." or ")", requires following
whitespace; ">" permits none; one or more "#" requires whitespace.
A candidate then starts with zero to two stars or underscores, a nonempty
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
the plain form to write); wrong value shape, which includes a separator
other than one space after the colon, is reported only when no label
fault applies.
Prose and inline code before a token prevent candidate recognition.

Field labels: the session-start reader counts every LF-delimited line
that contains ``Active-session:``, ``Status:`` or
``Last-heartbeat-UTC:`` (case-sensitive, anywhere in the line, including
comments, fences and inline code) and reads none of them when it finds
two. Each such line other than that field's exact field line therefore
gets one finding, unless it already has a near-miss finding for the same
field. The sanctioned spelling for a mention in a comment or in free text
is the field name without a colon directly after it (for example
"the Status field" or "Status `active`").

Exact field lines get one location finding if their start is in an HTML
comment, a fenced block, or a later section, combining reasons.
The scanner recognizes literal "<!--" and "-->" with no nesting; an
unclosed comment extends through EOF. Fences use at least three identical
backticks or tildes after at most three ASCII spaces, with arbitrary info
text except backticks in backtick info. Closing fences use the same
character, at least the opening length, and only trailing whitespace.
An unclosed fence extends through EOF. Comments inside fences and fence
markers inside comments are inert. Outside both, a column-zero ATX heading
(one to six "#" followed by a space, tab or end of line) starts a later
section when an earlier such line or a header-region field line precedes
it; otherwise it is the title.
This is a line scanner, not a Markdown parser: escaped comment delimiters
are still recognized; fences indented over three spaces or inside
containers are not recognized.
Labels are checked independently of those scanner limits. Existing
whole-text field counts, value checks and missing-field exit precedence
remain unchanged.

This gate guards the file's SHAPE only. It deliberately passes on all
three status values: CI runs per-branch and cannot see across
concurrent sessions, so the interlock itself (HOLD-and-surface on a
live lease or a recent unmerged sibling branch) lives in the `/orch`
step-0 procedure, not in CI. A malformed lease would silently disable
that procedure, which is the failure this gate exists to catch.

Exit codes:
    0: a well-formed lease, or an absent operational store (skip).
    1: an invalid value, incoherence, duplicate, near-miss label, extra
       field label, or field line outside the header region.
    2: an unreadable lease or a required field line absent.
"""

from __future__ import annotations

import re
import sys
import unicodedata

from lint_common import REPO_ROOT, print_degraded, resolve_working


# Plain `Field: value` lines: the name at column zero, then ": " (one space),
# the form the fleet lease tool (orch_store.py) parses.
FIELD_PATTERNS = {
    "Active-session": re.compile(r"^Active-session: (\S+)\s*$", re.MULTILINE),
    "Status": re.compile(r"^Status: (\S+)\s*$", re.MULTILINE),
    "Operating-mode": re.compile(r"^Operating-mode: (\S+)\s*$", re.MULTILINE),
    "Last-heartbeat-UTC": re.compile(
        r"^Last-heartbeat-UTC: (\S+)\s*$", re.MULTILINE
    ),
    "Current-task": re.compile(r"^Current-task: (\S.*?)\s*$", re.MULTILINE),
    "Worker-dispatches": re.compile(
        r"^Worker-dispatches: (\S.*?)\s*$", re.MULTILINE
    ),
}

VALID_STATUSES = {"active", "winding-down", "released"}

# Operating mode (the AskUserQuestion-blocking hook reads this: it blocks a blocking
# prompt when the mode contains "unattended", so the value must be reliably present).
VALID_MODES = {
    "fully-attended",
    "attended-autonomous",
    "overnight-unattended",
    "daytime-unattended",
}

HEARTBEAT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


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


LABEL_RE = re.compile(
    r"^(?P<prefix>\s*(?:(?:[-+*]|\d+[.)])\s+|>\s*|#+\s+)*)"
    r"(?P<open>[*_]{0,2})(?P<label>[^*:]+?)"
    r"(?P<close>[*_]{0,2})(?P<space>\s*):(?P<after>[*_]{0,2})"
)
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")

# The fields tools/session_facts.py reads (its NAMES): it counts every line
# containing "<name>:" as an occurrence and reads none when there are two.
READER_FIELDS = ("Active-session", "Status", "Last-heartbeat-UTC")


def field_line_errors(text: str) -> list[str]:
    """Find near-miss labels, extra field labels and misplaced field lines."""
    invalid: list[str] = []
    comment = False
    fence = ""
    title_seen = False
    header_field_seen = False
    later_heading = False
    for number, line in enumerate(text.split("\n"), 1):
        exact = next(
            (field for field, pattern in FIELD_PATTERNS.items()
             if pattern.fullmatch(line)), None
        )
        near = None
        token = LABEL_RE.match(line)
        if token and exact is None:
            label = token.group("label")
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
                if token.group("prefix"):
                    faults.append("leading whitespace or Markdown marker")
                if token.group("space"):
                    faults.append("space before the colon")
                if "".join(token.group("open", "close", "after")):
                    faults.append(
                        f"bold or emphasis markers, write the plain form "
                        f"`{near}: <value>`"
                    )
                if not faults:
                    faults.append("wrong value shape")
                invalid.append(
                    f"field line `{near}:` at line {number} "
                    f"has a near-miss label ({', '.join(faults)})"
                )
        for name in READER_FIELDS:
            if name + ":" in line and name not in (exact, near):
                invalid.append(
                    f"field label `{name}:` also appears at line {number}, "
                    f"which the session-start reader counts as a second "
                    f"field line (drop the colon from a mention)"
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
            continue
        if not comment and marker and (
            marker.group(1)[0] == "~" or "`" not in marker.group(2)
        ):
            fence = marker.group(1)
            continue
        for delimiter in re.finditer(r"<!--|-->", line):
            if delimiter.group() == "<!--":
                comment = True
            else:
                comment = False
    return invalid


def check_text(text: str) -> tuple[list[str], list[str]]:
    """Validate lease text; return (missing_field_errors, value_errors)."""
    missing: list[str] = []
    invalid: list[str] = []
    values: dict[str, str] = {}

    for field, pattern in FIELD_PATTERNS.items():
        matches = list(pattern.finditer(text))
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
    if status is not None and status.lower() not in VALID_STATUSES:
        invalid.append(
            f"Status value `{status}` is invalid; permitted values: "
            f"active, winding-down, released"
        )

    mode = values.get("Operating-mode")
    if mode is not None and mode.lower() not in VALID_MODES:
        invalid.append(
            f"Operating-mode value `{mode}` is invalid; permitted values: "
            f"fully-attended, attended-autonomous, overnight-unattended, daytime-unattended"
        )

    heartbeat = values.get("Last-heartbeat-UTC")
    if heartbeat is not None and not HEARTBEAT_RE.match(heartbeat):
        invalid.append(
            f"Last-heartbeat-UTC value `{heartbeat}` is not a "
            f"YYYY-MM-DDTHH:MM:SSZ stamp (use `date -u +%Y-%m-%dT%H:%M:%SZ`)"
        )

    session = values.get("Active-session")
    if status is not None and session is not None:
        status_lc = status.lower()
        if status_lc == "released" and session.lower() != "none":
            invalid.append(
                f"Status `released` requires `Active-session: none`, "
                f"found `{session}`"
            )
        if status_lc in {"active", "winding-down"} and session.lower() == "none":
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

    try:
        text = session_state.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: cannot read {rel}: {exc}", file=sys.stderr)
        return 2

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
