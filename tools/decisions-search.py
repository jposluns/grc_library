#!/usr/bin/env python3
"""decisions-search: find a recorded maintainer decision before asking about it.

The forcing-function companion to the ``block-answered-question.py`` PreToolUse hook
(TODO section 1.22.6). Before surfacing an ``AskUserQuestion`` on an authorial / policy
decision, the orchestrator runs this tool on the topic's distinctive key(s) and PASTES the
output: a recorded decision means act on it, never re-ask (the clarify-before-acting
compute-first gate, the same executed-not-narrated discipline as ``audit-delivery-status.py``
and ``ref-holds.py``). The hook is the automatic backstop; this tool is the on-demand
search the orchestrator drives and quotes.

It searches the decision stores (whichever exist; adopter-safe):
  - ``.working/pending-decisions.md``     (the live + resolved decision queue)
  - ``../grc_library_private/design-decisions.md``  (the durable design-decision record)
  - ``.working/DONE.md``                  (closed-item ledger, records the disposition)

Usage:
  python3 tools/decisions-search.py 3.69                 # a section number
  python3 tools/decisions-search.py FR-205               # a coded backlog id
  python3 tools/decisions-search.py "MFA scope"          # a free-text phrase
  python3 tools/decisions-search.py 3.68 3.69 3.70       # several keys at once

Matching:
  - A section-number key ("3.69") matches the token with an optional trailing letter
    ("3.69a") but not a longer number ("3.6" does not match "3.69").
  - A coded-id key ("FR-205") matches on a word boundary.
  - Any other argument is treated as a case-insensitive substring phrase.
Exit code: 0 if at least one match is found, 1 if none (so a caller can branch), 2 on a
usage error. Stdlib-only (gate 71).
"""

import re
import sys
from pathlib import Path

STORE_RELPATHS = [
    ".working/pending-decisions.md",
    "../grc_library_private/design-decisions.md",
    ".working/DONE.md",
]


def _project_dir() -> Path:
    # this file lives in <project>/tools/
    return Path(__file__).resolve().parent.parent


def _compile(key: str) -> re.Pattern:
    if re.fullmatch(r"\d+(?:\.\d+)+", key):
        return re.compile(r"(?<![\d.])" + re.escape(key) + r"[a-z]?(?![\d.])")
    if re.fullmatch(r"[A-Za-z]{1,4}-\d+", key):
        return re.compile(r"\b" + re.escape(key) + r"\b")
    return re.compile(re.escape(key), re.IGNORECASE)


def search(keys: list[str]) -> tuple[int, list[str]]:
    base = _project_dir()
    stores: list[tuple[str, str]] = []
    for rel in STORE_RELPATHS:
        p = (base / rel).resolve()
        try:
            stores.append((rel, p.read_text(encoding="utf-8", errors="replace")))
        except OSError:
            continue
    lines_out: list[str] = []
    total = 0
    for key in keys:
        pat = _compile(key)
        for label, text in stores:
            for i, ln in enumerate(text.splitlines(), 1):
                if pat.search(ln):
                    total += 1
                    snippet = ln.strip()
                    if len(snippet) > 400:
                        snippet = snippet[:400] + " ..."
                    lines_out.append(f"[{label}:{i}] (key `{key}`) {snippet}")
    return total, lines_out


def main(argv: list[str]) -> int:
    keys = [a for a in argv[1:] if a.strip()]
    if not keys:
        print(
            "usage: decisions-search.py <key-or-phrase> [<key-or-phrase> ...]\n"
            "  keys: a section number (3.69), a coded id (FR-205), or a phrase (\"MFA scope\")",
            file=sys.stderr,
        )
        return 2
    total, lines = search(keys)
    if total == 0:
        print(
            f"decisions-search: NO recorded decision found for {keys} in the decision "
            f"stores. This may be a genuinely novel decision (safe to ask), OR the topic "
            f"is keyed differently, try a broader phrase before concluding it is unrecorded."
        )
        return 1
    print(
        f"decisions-search: {total} match(es) for {keys} in the decision stores. "
        f"If a recorded decision covers your question, ACT on it, do NOT re-ask:"
    )
    for ln in lines:
        print(f"  {ln}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
