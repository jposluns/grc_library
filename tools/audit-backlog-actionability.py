#!/usr/bin/env python3
"""Backlog actionability enumeration across BOTH backlog lists, so a "queue
exhausted / all blocked / hold" claim cannot be made without confronting every
open item on either list (anti-false-completeness layer 1).

WHY THIS EXISTS. A completeness claim ("everything left is blocked, so I am
stopping") was made from a PARTIAL review and was wrong: actionable items
remained. Nothing mechanical forced the claimant to confront EVERY backlog item
first. This tool does: it enumerates every open item in the PUBLIC ``TODO.md``
AND the PRIVATE ``grc_library_private/P-TODO.md`` and, per item, reports whether
it is BLOCKED.

THE AUTHORITATIVE BLOCKER SIGNAL IS THE TAG, NOT PROSE. An item is counted
BLOCKED only if it carries a ``[BLOCKED:<reason>]`` tag. That tag is a
maintainer-GRANTED status: the assistant never self-applies it (a PreToolUse
hook rejects a ``[BLOCKED]`` written without a matching maintainer approval
record), it proposes a block in ``.working/pending-decisions.md`` and only an
approved block becomes a tag. So "all blocked" is assertable only when EVERY
open item on BOTH lists literally carries an approved ``[BLOCKED:...]`` tag,
which is essentially never. Until the maintainer approves blocks, every item
reads ACTIONABLE, which is the honest state.

PROSE SIGNAL IS ADVISORY ONLY. The closed keyword set below (``egress-gated``,
``DEFERRED``, ``maintainer-decision`` ...) no longer decides blocked-vs-actionable;
it is surfaced as an ADVISORY "this item's prose mentions a blocker; propose a
``[BLOCKED]`` tag for it?" hint. An item with a prose signal but no approved tag
is still ACTIONABLE (the safe direction: it forces a disposition, it does not
hide a blocker behind an unapproved self-assessment).

It is ADVISORY, NOT a gate: it always exits 0, is not wired into
``quality.yml`` / ``run_all_audits.sh`` / ``.pre-commit-config.yaml``, and is
portable-clone-tolerant (a missing list is a no-op for that list; an adopter with
no private sibling simply audits the public list). Regression coverage:
``BacklogActionabilityTests`` in ``tests/test_linters.py``.

USAGE
  python3 tools/audit-backlog-actionability.py
      Enumerate every open item on both lists; print the full table, the summary
      counts, and the ACTIONABLE list.
  python3 tools/audit-backlog-actionability.py --actionable-only
      Print only the summary and the ACTIONABLE list.
  python3 tools/audit-backlog-actionability.py --todo PATH --ptodo PATH
      Override either list path (testing / non-default layout).

Stdlib-only (gate 71). Python 3.11.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TODO_PATH = REPO_ROOT / "TODO.md"
# The private backlog lives in the maintainer's private sibling; adopters have no
# such sibling and simply audit the public list (resolve_sibling no-op).
PTODO_PATH = REPO_ROOT.parent / "grc_library_private" / "P-TODO.md"

# An open backlog item heading: ``### <id> <title>`` where <id> is a section
# number (``N.M`` / ``N.M.K``, optional trailing letter), a private ``P-n.m`` id,
# or a coded id (``SR-1`` / ``RB-R6`` / ``GR-GAP-1``). ``## `` section headers are
# NOT items.
ITEM_HEADING_RE = re.compile(
    r"^### (?P<id>P-\d+(?:\.\d+){1,2}[a-z]?"
    r"|\d+(?:\.\d+){1,2}[a-z]?"
    r"|[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\b[ \t]*(?P<title>.*)$"
)

# The AUTHORITATIVE blocker signal: a ``[BLOCKED:<reason>]`` tag (maintainer-granted).
BLOCKED_TAG_RE = re.compile(r"\[BLOCKED:[^\]]*\]")

# ADVISORY prose-signal set (closed). Detected only to SUGGEST proposing a block;
# it never counts an item blocked. Kept deliberately narrow to avoid false hints.
PROSE_SIGNAL_TOKENS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"egress[- ]gated|egress[- ]blocked", re.I), "egress"),
    (re.compile(r"source[- ]gated|source[- ]not[- ]held|pending held source"
                r"|pending maintainer source|blocked on .{0,30}ingest", re.I),
     "source"),
    (re.compile(r"maintainer[- ](decision|decided|gated|collaborative|"
                r"sign[- ]off|owned)", re.I), "maintainer-decision"),
    (re.compile(r"\bNOT automated\b|explicitly NOT automated"), "maintainer-decision"),
    (re.compile(r"\bDEFERRED\b|\bdeferred\b"), "deferred"),
    (re.compile(r"\bIN PROGRESS\b"), "in-progress"),
    (re.compile(r"fresh[- ]session|fresh[- ]context|attended[- ]preferred"
                r"|attended/fresh|fresh session", re.I), "fresh-session"),
    (re.compile(r"\(standing\)|,\s*standing\)|standing (?:tracker|watch)"
                r"|stays open by design", re.I), "standing"),
]


def parse_items(text: str, source: str) -> list[tuple[str, str, str, str]]:
    """Return ``(id, title, block_text, source)`` for every open ``### `` item.

    A block runs from its item heading to the next item heading, the next ``## ``
    section header, or end of file, so a signal is detected only within the item's
    own text. ``source`` labels which list the item came from (``public`` /
    ``private``)."""
    lines = text.splitlines()
    items: list[tuple[str, str, str, str]] = []
    cur: tuple[str, str] | None = None
    body: list[str] = []

    def flush() -> None:
        if cur is not None:
            items.append((cur[0], cur[1].strip(), "\n".join(body), source))

    for line in lines:
        m = ITEM_HEADING_RE.match(line)
        if m:
            flush()
            cur = (m.group("id"), m.group("title"))
            body = [line]
        elif line.startswith("## "):
            flush()
            cur = None
            body = []
        elif cur is not None:
            body.append(line)
    flush()
    return items


def is_blocked(block_text: str) -> bool:
    """True iff the item carries an (approved) ``[BLOCKED:...]`` tag."""
    return bool(BLOCKED_TAG_RE.search(block_text))


def prose_signals(block_text: str) -> list[str]:
    """Sorted distinct ADVISORY prose blocker-signals (never authoritative)."""
    return sorted({cls for pat, cls in PROSE_SIGNAL_TOKENS if pat.search(block_text)})


def read_list(path: Path, source: str) -> tuple[list[tuple[str, str, str, str]], bool]:
    """Return (items, present). A missing list is a no-op for that list."""
    if not path.is_file():
        return [], False
    return parse_items(path.read_text(encoding="utf-8", errors="replace"), source), True


def build_report(public_text: str,
                 private_text: str | None = None) -> tuple[list, int, int]:
    """Return (rows, blocked_count, actionable_count). Each row is
    ``(id, title, source, blocked_bool, prose_list)``."""
    items = parse_items(public_text, "public")
    if private_text is not None:
        items += parse_items(private_text, "private")
    rows = []
    blocked = 0
    for item_id, title, block, source in items:
        b = is_blocked(block)
        rows.append((item_id, title, source, b, prose_signals(block)))
        if b:
            blocked += 1
    return rows, blocked, len(rows) - blocked


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--actionable-only", action="store_true",
                    help="print only the summary and the ACTIONABLE list")
    ap.add_argument("--todo", default=str(TODO_PATH), help="public TODO.md path")
    ap.add_argument("--ptodo", default=str(PTODO_PATH),
                    help="private P-TODO.md path (no-op if absent)")
    args = ap.parse_args(argv)

    todo = Path(args.todo)
    if not todo.is_file():
        print(f"advisory: TODO.md not found at {todo} (portable clone); no-op.")
        return 0
    public_text = todo.read_text(encoding="utf-8", errors="replace")

    ptodo = Path(args.ptodo)
    private_text = ptodo.read_text(encoding="utf-8", errors="replace") \
        if ptodo.is_file() else None
    private_note = "" if private_text is not None \
        else f" (private list {ptodo} absent; public-only)"

    rows, blocked, actionable = build_report(public_text, private_text)

    def trunc(t: str, w: int = 52) -> str:
        t = t.strip()
        return t if len(t) <= w else t[: w - 3] + "..."

    if not args.actionable_only:
        print(f"Backlog actionability enumeration (both lists){private_note}:")
        print(f"{'id':<10} {'list':<8} {'BLOCKED?':<9} {'prose-signal':<20} title")
        print("-" * 100)
        for item_id, title, source, b, sig in rows:
            bl = "BLOCKED" if b else "-"
            ps = ",".join(sig) if sig else ""
            print(f"{item_id:<10} {source:<8} {bl:<9} {ps:<20} {trunc(title)}")

    print(f"\n{len(rows)} open item(s) across both lists; {blocked} BLOCKED "
          f"(approved [BLOCKED:] tag); {actionable} ACTIONABLE.")
    print("An item is BLOCKED only via a maintainer-approved [BLOCKED:<reason>] "
          "tag. 'all blocked' is assertable only when EVERY item carries one.")

    # Advisory: items whose PROSE mentions a blocker but that carry no approved tag
    # are ACTIONABLE and are candidates to PROPOSE for a [BLOCKED] tag (never self-tag).
    propose = [(i, t, sig) for i, t, s, b, sig in rows if sig and not b]
    if propose:
        print(f"\nPROSE-SIGNAL, NO APPROVED TAG ({len(propose)}) "
              f"-- ACTIONABLE now; propose a [BLOCKED] tag via pending-decisions.md:")
        for item_id, title, sig in propose:
            print(f"  - {item_id}  [{','.join(sig)}]  {trunc(title)}")

    actionable_rows = [(i, t, s) for i, t, s, b, sig in rows if not b]
    if actionable_rows:
        print(f"\nACTIONABLE ({len(actionable_rows)}):")
        for item_id, title, source in actionable_rows:
            print(f"  - {item_id}  ({source})  {trunc(title)}")
    else:
        print("\n(no actionable items: every open item on both lists carries an "
              "approved [BLOCKED:] tag. Verify each before any all-blocked claim.)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
