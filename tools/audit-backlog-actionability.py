#!/usr/bin/env python3
"""Backlog actionability enumeration: every open TODO item, and whether it
carries a recognized BLOCKER signal, so a "queue exhausted / all blocked / hold"
claim cannot be made without confronting the full list (TODO 3.99 guardrail
sibling; anti-false-completeness layer 1).

WHY THIS EXISTS. A completeness claim ("everything left is blocked / on hold /
maintainer-gated, so I am stopping") was once made from a PARTIAL review and was
wrong: actionable items remained. Nothing mechanical forced the claimant to
confront EVERY backlog item before asserting all-blocked. This tool does: it
enumerates every open item in ``TODO.md`` and, per item, reports whether the
item's own block text carries a blocker signal from a closed, named set. An item
with NO blocker signal is surfaced as ``PRESUMED-ACTIONABLE (needs disposition)``,
so an all-blocked claim must explicitly dispose of each such item rather than
wave at the queue.

HONEST LIMITATION (read before trusting a verdict). This tool is
RECALL-ORIENTED, not a decision procedure. It SURFACES candidates from a
keyword heuristic; it does NOT make the final blocked-vs-actionable call. Two
directions of error are expected and acceptable for its purpose:
  - A false PRESUMED-ACTIONABLE (an item genuinely blocked but phrased without a
    recognized token) is the SAFE direction: it forces a human disposition, it
    does not hide a blocker.
  - A false blocked (an item that carries a blocker WORD in a non-blocking
    sense, for example prose that merely mentions "maintainer decision" about a
    sub-point) is the UNSAFE direction and the reason the tool never DECIDES:
    the orchestrator judges each flagged class against the item text. The tool's
    job is to guarantee the FULL list is confronted, not to adjudicate it.
The blocker-token set is deliberately a CLOSED constant (below); widening it is a
reviewed change, not an inference.

It is ADVISORY, NOT a gate: it always exits 0, it is not wired into
``quality.yml`` / ``run_all_audits.sh`` / ``.pre-commit-config.yaml`` (it makes no
pass/fail claim on repository state), and it is portable-clone-tolerant (if
``TODO.md`` is absent it prints a one-line no-op and exits 0). Its regression
coverage is the ``BacklogActionabilityTests`` class in ``tests/test_linters.py``
(discovered by ``tools/run-linter-regression.py``), not a numbered gate.

USAGE
  python3 tools/audit-backlog-actionability.py
      Enumerate every open TODO item; print the full id/title/blocker-class
      table, the summary counts, and the distinct PRESUMED-ACTIONABLE list.
  python3 tools/audit-backlog-actionability.py --actionable-only
      Print only the summary and the PRESUMED-ACTIONABLE list.

Stdlib-only (gate 71). Python 3.11.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TODO_PATH = REPO_ROOT / "TODO.md"

# An open backlog item heading: ``### <id> <title>`` where <id> is a section
# number (``N.M`` or ``N.M.K``) or a coded id (``SR-1`` / ``RB-R6`` / ``GR-GAP-1``,
# uppercase alnum with at least one hyphen). The ``## Priority N`` section headers
# and the ``## Maintainer or Egress Gated`` MEG index (whose entries are table
# rows, not ``### `` headings) are NOT items and are not matched.
ITEM_HEADING_RE = re.compile(
    r"^### (?P<id>\d+(?:\.\d+){1,2}[a-z]?|[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\b[ \t]*(?P<title>.*)$"
)

# Closed blocker-signal set: (compiled pattern, canonical blocker-class). Order
# is irrelevant (all matches are collected). Patterns are case-insensitive except
# where a specific upper-case marker is the real signal. NB there is deliberately
# NO bare "held" pattern: "held primary" / "(held primary)" means the source is
# PRESENT, which is the OPPOSITE of a blocker, so only the explicit
# source-ABSENT phrasings below count as a source blocker.
BLOCKER_TOKENS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"egress[- ]gated|egress[- ]blocked", re.I), "egress"),
    (re.compile(r"source[- ]gated|source[- ]not[- ]held|pending held source"
                r"|pending maintainer source|blocked on .{0,30}ingest", re.I),
     "source"),
    # maintainer-decision: the order's closed set only. NB "confirm" and "revi"
    # are deliberately EXCLUDED: "maintainer-confirmed <date>" is a provenance
    # stamp meaning the maintainer ALREADY approved the shape (actionable), the
    # OPPOSITE of awaiting a decision, so matching it would false-block.
    (re.compile(r"maintainer[- ](decision|decided|gated|collaborative|"
                r"sign[- ]off|owned)", re.I), "maintainer-decision"),
    (re.compile(r"\bNOT automated\b|explicitly NOT automated"), "maintainer-decision"),
    (re.compile(r"\bDEFERRED\b|\bdeferred\b"), "deferred"),
    (re.compile(r"\bIN PROGRESS\b"), "in-progress"),
    (re.compile(r"fresh[- ]session|fresh[- ]context|attended[- ]preferred"
                r"|attended/fresh|fresh session", re.I), "fresh-session"),
    # standing: the STATUS-TAG forms only, NOT a bare mid-sentence "standing".
    # A bare \bstanding\b over-matches incidental prose ("standing worker
    # sessions", "standing up a reference base", "standing convention going
    # forward"), which would false-block an actionable item, the unsafe
    # direction this tool exists to avoid. So it fires only on the parenthetical
    # ``(standing)`` / effort-tag ``, standing)`` markers, ``standing
    # tracker``/``standing watch``, or ``stays open by design``.
    (re.compile(r"\(standing\)|,\s*standing\)|standing (?:tracker|watch)"
                r"|stays open by design", re.I), "standing"),
]


def parse_items(text: str) -> list[tuple[str, str, str]]:
    """Return ``(id, title, block_text)`` for every open ``### `` item heading.

    A block runs from its item heading to the next item heading, the next ``## ``
    section header, or end of file (whichever comes first), so a class is
    detected only within the item's own text, not a neighbour's.
    """
    lines = text.splitlines()
    items: list[tuple[str, str, str]] = []
    cur: tuple[str, str] | None = None
    body: list[str] = []

    def flush() -> None:
        if cur is not None:
            items.append((cur[0], cur[1].strip(), "\n".join(body)))

    for line in lines:
        m = ITEM_HEADING_RE.match(line)
        if m:
            flush()
            cur = (m.group("id"), m.group("title"))
            body = [line]
        elif line.startswith("## "):
            # A new priority/meta section closes the current item block.
            flush()
            cur = None
            body = []
        elif cur is not None:
            body.append(line)
    flush()
    return items


def classify(block_text: str) -> list[str]:
    """Return the sorted distinct blocker-classes detected in ``block_text`` (an
    empty list means no recognized blocker signal: PRESUMED-ACTIONABLE)."""
    classes = {cls for pat, cls in BLOCKER_TOKENS if pat.search(block_text)}
    return sorted(classes)


def build_report(text: str) -> tuple[list[tuple[str, str, list[str]]], int, int]:
    """Return (rows, blocked_count, actionable_count). Each row is
    ``(id, title, classes)``."""
    rows: list[tuple[str, str, list[str]]] = []
    blocked = 0
    for item_id, title, block in parse_items(text):
        classes = classify(block)
        rows.append((item_id, title, classes))
        if classes:
            blocked += 1
    actionable = len(rows) - blocked
    return rows, blocked, actionable


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--actionable-only", action="store_true",
                    help="print only the summary and the PRESUMED-ACTIONABLE list")
    ap.add_argument("--todo", default=str(TODO_PATH),
                    help="path to TODO.md (default: this repo's TODO.md)")
    args = ap.parse_args(argv)

    todo = Path(args.todo)
    if not todo.is_file():
        print(f"advisory: TODO.md not found at {todo} (portable clone); no-op.")
        return 0

    rows, blocked, actionable = build_report(
        todo.read_text(encoding="utf-8", errors="replace"))

    def trunc(t: str, w: int = 58) -> str:
        t = t.strip()
        return t if len(t) <= w else t[: w - 3] + "..."

    if not args.actionable_only:
        print("Backlog actionability enumeration (advisory; recall-oriented):")
        print(f"{'id':<10} {'blocker-class':<22} title")
        print("-" * 92)
        for item_id, title, classes in rows:
            cls = ",".join(classes) if classes else "NONE (presumed-actionable)"
            print(f"{item_id:<10} {cls:<22} {trunc(title)}")

    print(f"\n{len(rows)} open item(s) total; {blocked} with a blocker signal; "
          f"{actionable} PRESUMED-ACTIONABLE (needs disposition).")
    print("A PRESUMED-ACTIONABLE item is one carrying no recognized blocker "
          "token; the orchestrator must dispose of each before any "
          "all-blocked/queue-exhausted claim.")

    presumed = [(i, t) for i, t, c in rows if not c]
    if presumed:
        print(f"\nPRESUMED-ACTIONABLE ({len(presumed)}):")
        for item_id, title in presumed:
            print(f"  - {item_id}  {trunc(title)}")
    else:
        print("\n(no presumed-actionable items: every open item carries a "
              "blocker signal, which the orchestrator must still verify per item.)")

    # Advisory: always exit 0. This tool surfaces the list; it does not pass/fail.
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
