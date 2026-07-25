#!/usr/bin/env python3
"""Detect a recycled TODO item number or a stale item-number counter (gate 78).

``TODO.md`` states the permanent-id rule at the bottom of the file: "TODO
numbers are permanent and never recycled (2026-07-15) ... each priority
section carries a ``Next item number:`` counter, maintained on every TODO
edit; new and split-out items each draw the next number and advance the
counter, closed numbers retire with their item, and existing items are not
renumbered when the file is reorganized (so a number maps to exactly one
item across the file's whole history and lookups by number stay
unambiguous)."

Nothing enforced it, and it was broken twice. PR #1151 created a
``### 3.108`` although ``§3.108`` had been retired to ``.working/DONE.md``
by PR #1130, and left the P1 counter at ``1.23`` while ``### 1.23`` was
live; a pre-push verifier caught both. A class-width check then found a
further live violation predating #1151 at ``§3.100``. This gate is the
mechanical backstop (TODO section 3.110).

Two checks, both keyed on the two files the rule spans:

  A. RECYCLE. A live ``### N.M`` heading in ``TODO.md`` whose number is
     also recorded as retired in a ``.working/DONE.md`` heading. Such a
     number denotes two items, which is exactly what the rule forbids.

  B. COUNTER. A ``**Next item number: X.**`` counter pointing at a number
     already used in its section, live in ``TODO.md`` or retired in
     ``DONE.md``. A counter at or below the highest used number hands the
     next author a colliding id.

Design decisions, stated because each has a false-positive or
false-negative cost:

  1. RETIRED-ID PARSE. ``DONE.md`` entry headings carry the retired id as a
     ``§N.M`` token, but in several shapes: ``### §3.108 ASVS ...``,
     ``### TODO §3.100: ...``, ``### PR #466: §4.5 S4: ...``, and
     multi-id ``### §3.11 + §3.13 + §3.14: ...``. Some entries
     legitimately carry no id at all. This gate takes the ``§``-prefixed
     ids that appear BEFORE THE LAST COLON of the heading, or, when the
     heading has no colon, every ``§``-prefixed id outside parentheses.
     Rationale: the convention places the retired id ahead of the title,
     while a LATER ``§`` mention is usually a destination or a
     cross-reference (``### TODO §2.5 (... re-homed to §2.17-§2.21): ...``
     retires 2.5, not 2.17 through 2.21).

     FALSE-NEGATIVE RISK, and it is large: a ``DONE.md`` entry with no
     ``§N.M`` in its heading is invisible to this gate. At the time of
     writing, 539 ``DONE.md`` headings carry 140 distinct ids, so most
     entries state no id. The gate therefore catches recycling of a number
     whose retirement was RECORDED, and cannot catch recycling of a number
     whose retirement was not. Closing that gap needs a ``DONE.md``
     heading convention (always carry the retired id), which is a separate
     change; this gate is deliberately the recorded-retirement half rather
     than nothing.

     Sub-bullet ids (``§5.9-R1``, ``§6.3-R3``) are NOT retired item
     numbers, so the id pattern requires a bare dotted number and rejects
     a ``-R<n>`` suffix. Otherwise closing a sub-bullet would read as
     retiring its parent.

  2. REDIRECT STUBS ARE NOT EXEMPT, deliberately. The rule's one exception
     is the series-consolidation move, where "the content moves to a new
     series child X.Y.Z and a forward redirect stub is left at the
     original number (both close together)". A stub (for example
     ``### 2.24 ... MOVED to 2.25.1 (Series A)``) is a LIVE heading holding
     its number on purpose, so it is correctly part of the live set: the
     number is alive, not retired. Exempting stubs would be wrong, because
     a number that is simultaneously stub-alive in ``TODO.md`` and retired
     in ``DONE.md`` is a genuine inconsistency the gate should report. No
     current stub collides, so this costs nothing today and keeps the
     check honest if the convention is applied loosely later.

  3. NON-``N.M`` SERIES. The ``TF-`` series has its own
     ``Next item number: TF-3.`` counter, so it is checked, with its
     integer as the ordinal. The reference-base ids (``SR-1``, ``RB-R6``,
     ``Group ...``, ``Reference-base ...``) have NO counter and no
     retirement convention in ``DONE.md``, so they are OUT OF SCOPE and
     are skipped rather than half-checked. Stated so a later reader does
     not mistake the silence for a clean result.

  4. EXEMPTIONS. A ``DONE.md`` entry that records a PARTIAL close against
     a still-open umbrella item legitimately names a live number (for
     example ``### TODO §3.57 (apply wave complete; item stays open for
     the matrix TSC-column residual): ...``). Those are listed in
     ``EXEMPT`` keyed by ``(id, distinctive_heading_substring)`` with a
     rationale, so an exemption cannot silently widen to a different entry.
     A line-number key was tried first and REJECTED on measurement: one
     unrelated PR shifted both entries by 4 lines and both exemptions
     lapsed, which would make the gate re-fire on ordinary edits. A
     substring survives line drift while still binding to one entry.

Exit codes:

  0   no recycled number and no stale counter.
  1   one or more findings.
  2   a required file is missing or unparseable.

Usage:

    python3 tools/lint-todo-number-permanence.py
    python3 tools/lint-todo-number-permanence.py --root <dir>

Stdlib-only Python 3.11.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parent.parent

TODO_REL = "TODO.md"
DONE_REL = ".working/DONE.md"

# A live backlog heading: '### 3.109 <title>' or '### 2.25.1 <title>' or
# '### 1.19.10a <title>' or '### TF-2 <title>'. A leading section marker is
# tolerated ('### §3.109 ...') though TODO does not currently use one.
LIVE_HEADING_RE = re.compile(
    r"^###\s+(?:§\s*)?((?:\d+(?:\.\d+)+[a-z]?)|TF-\d+)(?=[\s:]|$)"
)

# A retired id inside a DONE.md heading, always section-marked. Rejects a
# '-R<n>' sub-bullet suffix (see design note 1).
RETIRED_ID_RE = re.compile(r"§\s*((?:\d+(?:\.\d+)+[a-z]?)|TF-\d+)(?!-R\d)(?![\d.])")

# '**Next item number: 3.110.**' / '**Next item number: TF-3.**'
COUNTER_RE = re.compile(
    r"^\*\*Next item number:\s*((?:\d+\.\d+)|TF-\d+)\.\*\*"
)

PAREN_RE = re.compile(r"\([^()]*\)")

# (id, distinctive DONE.md heading substring) -> rationale. A partial close
# recorded against a still-open umbrella item. Keyed by a heading SUBSTRING, not
# by line number: a line key looked tighter but re-fired on any unrelated edit
# that shifted DONE.md (measured: one PR moved these two entries by 4 lines and
# both exemptions lapsed), which would make the gate unusable per-commit. The
# substring is narrow enough that the exemption cannot widen to another entry.
# (id, distinctive DONE.md heading substring) -> rationale. Keyed by a heading
# SUBSTRING, not by line number: a line key looked tighter but re-fired on any
# unrelated edit that shifted DONE.md (measured: one PR moved two entries by 4
# lines and both exemptions lapsed), which would make the gate unusable
# per-commit. Each substring below was checked to match exactly ONE of DONE.md's
# 543 entry headings, so an exemption cannot widen to another entry.
#
# THIS DICT'S COMPLETENESS, NOT THE PARSE, IS THIS GATE'S FALSE-POSITIVE SURFACE:
# the parse cannot tell a partial or sub-item close from a full retirement, so
# every legitimate live-and-retired coexistence must be enumerated here with its
# reason, and any future partial close against a still-open umbrella must add its
# own row in the same PR that records the close.
#
# Two classes, both audited at grc_library 331afaec:
#   PRE-RULE GRANDFATHER: the number was reassigned to different work BEFORE the
#     2026-07-15 permanent-id rule (TODO.md:633). Closed set: it cannot grow,
#     because post-2026-07-15 reassignment is the violation this gate reports.
#     Unfixable forward by design: the same rule forbids renumbering an existing
#     item, so renumbering these to clear the gate would break the rule it
#     enforces.
#   PARTIAL CLOSE: the DONE entry closed part of an item, or one sub-item of it,
#     and the SAME item is legitimately still live. Open-ended: this class stays
#     live maintenance (the 5.9 row below is dated 2026-07-24, after the rule).
EXEMPT: dict[tuple[str, str], str] = {
    # --- pre-rule grandfathers (7 ids, 8 rows: 3.14 collides on two DONE lines) ---
    ("3.2", "CHANGELOG detailed-mirror per-PR-header parity check"): (
        "PRE-RULE GRANDFATHER. The live row (authoritative standards register) drew "
        "3.2 in 60641dc7 (2026-07-09, the one-item-one-action TODO restructure), "
        "after the unrelated gate-59 item that held 3.2 retired on 2026-07-01 "
        "(bdb37ea5, PR #521). Both halves predate the 2026-07-15 rule."
    ),
    ("3.3", "Citation-verification consistency cross-check"): (
        "PRE-RULE GRANDFATHER. The live row (CLAUDE.md removal-ledger cadence) was "
        "renumbered into 3.3 by 60641dc7 (2026-07-09) and still carries its "
        "'(was 3.12)' breadcrumb; the unrelated citation-consistency item that held "
        "3.3 retired 2026-07-01 (a9feaef9, PR #522). Both predate 2026-07-15."
    ),
    ("3.9", "document the scratch `ref/` base as the standing citation"): (
        "PRE-RULE GRANDFATHER. The live row (require-registration citation-currency "
        "gate) drew 3.9 in 60641dc7 (2026-07-09); the unrelated ref-base "
        "documentation item that held 3.9 retired 2026-07-01 (2330abe0, PR #515). "
        "Both predate 2026-07-15."
    ),
    ("3.13", "protected `.claude/CLAUDE.md` wind-down"): (
        "PRE-RULE GRANDFATHER. 3.13 was reassigned twice pre-rule: 7afb1f64 "
        "(2026-07-01) gave it to the audit-surfaced gate extensions after the "
        "CLAUDE.md-optimization item retired in the same-day wind-down (ca1ef503, "
        "PR #523), and 60641dc7 (2026-07-09) split that into the live "
        "mutation-probe item. Both predate 2026-07-15."
    ),
    ("3.14", "protected `.claude/CLAUDE.md` wind-down"): (
        "PRE-RULE GRANDFATHER. The live row (ETSI Securing-AI alignment map) was "
        "renumbered from 3.16 into the freed 3.14 by 60641dc7 (2026-07-09) and "
        "still carries its '(was 3.16)' breadcrumb; the prior 3.14 retired "
        "2026-07-01 in this multi-id wind-down entry (ca1ef503, PR #523). Both "
        "predate 2026-07-15."
    ),
    ("3.14", "tooling half"): (
        "PRE-RULE GRANDFATHER, and NOT a partial close despite how the heading "
        "reads. The umbrella whose tooling half closed here was "
        "'### 3.14 Reinforce the section-close cross-FILE cleanup checklist line "
        "...' (TODO.md:196 at 2330abe0, 2026-07-01), which has since fully "
        "retired; 60641dc7 (2026-07-09) then renumbered the unrelated ETSI item "
        "into 3.14. The live 3.14 is not the item this entry trimmed. Both "
        "predate 2026-07-15."
    ),
    ("4.5", "gate 56 bare-normative-shall audit"): (
        "PRE-RULE GRANDFATHER. This entry closed sub-item S4 of the old "
        "'### 4.5 Audit-gate candidates from the 2026-06-22 review' on 2026-06-29 "
        "(e08f9c5f, PR #466); 0cce6a2b (2026-06-30, the priority-prefixed "
        "renumber) then reassigned 4.5 to the fork-facing reference-base item that "
        "is live today (retitled, not renumbered, by d3543457 on 2026-07-12). Both "
        "predate 2026-07-15."
    ),
    ("4.6", "QA-cadence mechanical enforcement closed as satisfied"): (
        "PRE-RULE GRANDFATHER. The old 4.6 (QA-cadence mechanical enforcement) was "
        "closed in full as satisfied on 2026-06-29 (057fd160, PR #471), its "
        "unmechanizable half becoming a standing CLAUDE.md convention rather than a "
        "live item; 7afb1f64 (2026-07-01) then reassigned 4.6, and 60641dc7 "
        "(2026-07-09) split that into the live fork update-assessment item. Both "
        "predate 2026-07-15."
    ),
    # --- partial closes against a still-open umbrella (open-ended class) ---
    ("3.57", "apply wave complete"): (
        "PARTIAL CLOSE against a still-open umbrella. The DONE.md heading says so "
        "in its own words: '(apply wave complete; item stays open for the matrix "
        "TSC-column residual)', and the body confirms '§3.57 stays open only for "
        "the deferred matrix TSC-column mapping'. TODO 3.57 is legitimately live."
    ),
    ("5.9", "NYC-LL144"): (
        "PARTIAL CLOSE against a still-open umbrella. The entry retires the "
        "NYC-LL144 CANDIDATE inside section 5.9 ('NYC-LL144 candidate reconciled "
        "and struck', PR #1136, 2026-07-24), not the umbrella, whose body ends "
        "'§5.9 stays open.' Note the heading does not say so, unlike the 3.57 "
        "entry, so this exemption rests on reading the entry body. Note also the "
        "date: this partial close is POST-rule, which is why this class is not a "
        "closed historical set."
    ),
}


def _ordinal(item_id: str) -> tuple[str, int] | None:
    """Map an id to (section, ordinal) for counter comparison.

    '3.109' -> ('3', 109); '2.25.1' -> ('2', 25) (a series child occupies
    its parent's ordinal); 'TF-2' -> ('TF', 2). Returns None for an id this
    gate does not order.
    """
    if item_id.startswith("TF-"):
        return ("TF", int(item_id.split("-", 1)[1]))
    parts = item_id.split(".")
    if len(parts) < 2:
        return None
    m = re.match(r"(\d+)", parts[1])
    if not m:
        return None
    return (parts[0], int(m.group(1)))


def parse_live(text: str) -> dict[str, list[int]]:
    """Live item ids in TODO.md -> the line numbers declaring them."""
    live: dict[str, list[int]] = {}
    for lineno, line in enumerate(text.splitlines(), start=1):
        m = LIVE_HEADING_RE.match(line)
        if m:
            live.setdefault(m.group(1), []).append(lineno)
    return live


def done_headings(text: str) -> dict[int, str]:
    """DONE.md line number -> heading text, for exemption matching."""
    return {
        n: line for n, line in enumerate(text.splitlines(), start=1)
        if line.startswith("### ")
    }


def parse_retired(text: str) -> dict[str, list[int]]:
    """Retired ids recorded in DONE.md headings -> their line numbers.

    See design note 1 for the before-the-last-colon rule and its
    false-negative cost.
    """
    retired: dict[str, list[int]] = {}
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not line.startswith("### "):
            continue
        head = line[4:]
        scope = head[: head.rfind(":")] if ":" in head else head
        # Parentheticals are stripped in BOTH branches: a bracketed aside names
        # a DESTINATION or a provenance note, never the retired id. Without
        # this, '### TODO §2.5 (... re-homed to §2.17-§2.21): ...' reads as
        # retiring 2.17 through 2.21, which was a measured false positive.
        scope = PAREN_RE.sub(" ", scope)
        for m in RETIRED_ID_RE.finditer(scope):
            retired.setdefault(m.group(1), []).append(lineno)
    return retired


def parse_counters(text: str) -> dict[str, tuple[str, int]]:
    """'**Next item number: X.**' -> (raw value, declaring line number)."""
    counters: dict[str, tuple[str, int]] = {}
    for lineno, line in enumerate(text.splitlines(), start=1):
        m = COUNTER_RE.match(line)
        if m:
            raw = m.group(1)
            ordinal = _ordinal(raw)
            if ordinal is not None:
                counters[ordinal[0]] = (raw, lineno)
    return counters


def _exempt(item_id: str, heading: str) -> bool:
    """True if (id, heading) matches a recorded partial-close exemption."""
    for (exempt_id, marker) in EXEMPT:
        if exempt_id == item_id and marker in heading:
            return True
    return False


def find_recycled(
    live: dict[str, list[int]],
    retired: dict[str, list[int]],
    done_lines_text: dict[int, str],
) -> list[tuple[str, list[int], list[int]]]:
    """Live ids that DONE.md also records as retired, minus exemptions."""
    findings = []
    for item_id in sorted(set(live) & set(retired), key=lambda s: (_ordinal(s) or ("", 0))):
        done_lines = [
            ln for ln in retired[item_id]
            if not _exempt(item_id, done_lines_text.get(ln, ""))
        ]
        if done_lines:
            findings.append((item_id, live[item_id], done_lines))
    return findings


def find_stale_counters(
    live: dict[str, list[int]],
    retired: dict[str, list[int]],
    counters: dict[str, tuple[str, int]],
) -> list[tuple[str, str, int, int, list[str]]]:
    """Counters pointing at an already-used ordinal in their section."""
    findings = []
    for section, (raw, lineno) in sorted(counters.items()):
        target = _ordinal(raw)
        if target is None:
            continue
        used: dict[int, list[str]] = {}
        for source in (live, retired):
            for item_id in source:
                o = _ordinal(item_id)
                if o is not None and o[0] == section:
                    used.setdefault(o[1], []).append(item_id)
        blocking = sorted(n for n in used if n >= target[1])
        if blocking:
            names = sorted({name for n in blocking for name in used[n]})
            findings.append((section, raw, lineno, max(used), names))
    return findings


def main(argv: list[str]) -> int:
    global REPO_ROOT
    parser = argparse.ArgumentParser(
        description="Detect a recycled TODO item number or a stale item-number counter."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Override the repository root TODO.md and .working/DONE.md are read "
             "from (used by the regression fixtures for synthetic isolation).",
    )
    args = parser.parse_args(argv[1:])
    if args.root is not None:
        REPO_ROOT = args.root.resolve()

    todo_path = REPO_ROOT / TODO_REL
    done_path = REPO_ROOT / DONE_REL
    for path in (todo_path, done_path):
        if not path.is_file():
            print(f"ERROR: required file missing: {path}", file=sys.stderr)
            return 2
    try:
        todo_text = todo_path.read_text(encoding="utf-8")
        done_text = done_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: cannot read a required file: {exc}", file=sys.stderr)
        return 2

    live = parse_live(todo_text)
    retired = parse_retired(done_text)
    counters = parse_counters(todo_text)

    recycled = find_recycled(live, retired, done_headings(done_text))
    stale = find_stale_counters(live, retired, counters)

    if not recycled and not stale:
        print(
            f"OK: {len(live)} live TODO item(s), {len(retired)} recorded retired "
            f"number(s), {len(counters)} counter(s); no recycled number, no stale counter."
        )
        return 0

    if recycled:
        print("=== recycled item numbers (a number denoting two items) ===")
        for item_id, todo_lines, done_lines in recycled:
            tl = ", ".join(f"TODO.md:{n}" for n in todo_lines)
            dl = ", ".join(f".working/DONE.md:{n}" for n in done_lines)
            print(f"  §{item_id}: live at {tl}; recorded retired at {dl}")

    if stale:
        print("=== counters pointing at an already-used number ===")
        for section, raw, lineno, highest, names in stale:
            print(
                f"  TODO.md:{lineno}: section {section} counter is '{raw}' but "
                f"{', '.join('§' + n for n in names)} already exist(s) "
                f"(highest used ordinal {highest}); advance it past {highest}"
            )

    total = len(recycled) + len(stale)
    print(f"\nFAIL: {total} item-number permanence finding(s).")
    print("TODO numbers are permanent and never recycled: a closed number retires with")
    print("its item, and every edit advances its section's 'Next item number' counter.")
    print("Fix the artefact (renumber the new item, or advance the counter); do not")
    print("weaken this gate. A legitimate partial-close entry against a still-open")
    print("umbrella item goes in EXEMPT with its rationale and its DONE.md line.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
