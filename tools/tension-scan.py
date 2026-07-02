#!/usr/bin/env python3
"""Partial-rewrite tension-marker scan over TODO and ledger blocks (the GR-P3 aid).

The GR-P3 failure class (three occurrences, #563/#564/#565): a scope-adding fix
or rewrite touches PART of a TODO bullet or ledger row while hedges or stale
status framings survive elsewhere in the SAME block ("upstream-CONFIRMED" in
the clause just edited, "NEEDS-UPSTREAM" surviving three clauses later). The
containing block reads self-contradictory, and no gate sees it: the surfaces
are gate-exempt free prose.

This aid re-lints the rewritten line whenever a diff partially rewrites a
block (on these surfaces a block is normally one long physical line, so the
line usually IS the whole block; a status token on an unchanged sibling line
of a multi-line block is outside the scan): for each TODO bullet, ledger
table row, bold-led paragraph, or plain paragraph line that a commit range
MODIFIES (an added line sharing a pairing
key with a removed counterpart in the same file, a rewrite rather than a pure
addition or deletion; keys are the bold lead token, the first two table cells,
and a normalized prefix, matched on ANY so an edit inside one key region still
pairs), it scans the block's NEW text for a status-claim token co-occurring
with a hedge token, and prints every pair hit as an untruncated full line for
judgment.

KNOWN RECALL LIMIT: pairing is line-local, so a rewrite that changes a block's
OPENING words and has no stable bold lead or table cells (a DONE-entry body
whose leading count is the edit, "Seven stale ..." to "Eleven stale ...")
matches no key and escapes. A best-effort trigger is the aid's design point;
treat a clean run as "nothing detected", never "nothing rewritten".

WHY AN AID AND NOT A GATE (the build-time census, 2026-07-02): every candidate
status+hedge pair has legitimate hits on the live surfaces. A census over
TODO.md and the six working ledgers found 91 block-level pair coincidences,
essentially all honest narrative (a retro row narrating "shipped X; pending Y",
the handoff's soft-spots block mixing CONFIRMED with awaiting, and bullets that
QUOTE the marker vocabulary, this aid's own backlog bullet among them). The
bookkeeping-gate family's precision-first bar (a standing gate ships only with
a zero-false-positive census, the D5 precedent) is therefore unreachable for
this class; the mechanizable half is the TRIGGER (a partial rewrite) and the
CANDIDATE list (the pairs), with the contradiction judgment staying human. The
aid prints candidates and always exits 0 on findings-for-judgment; it exits
non-zero only for usage or git errors.

Usage:
    python3 tools/tension-scan.py origin/main          # blocks rewritten since base
    python3 tools/tension-scan.py origin/main HEAD

The close-out convention: run it before pushing any PR that edits TODO or a
ledger row in place; read each printed block END TO END (the splice-seam
lesson) and fix real contradictions, leaving honest narrative alone.

Exit codes:
    0 : scan ran (with or without candidate pairs; the judgment is the reader's)
    2 : usage or git error
"""

from __future__ import annotations

import re
import subprocess
import sys

# The surfaces whose blocks the GR-P3 class lives in: the backlog and the
# working ledgers whose rows are rewritten in place.
SCANNED_FILES = (
    "TODO.md",
    ".working/pending-decisions.md",
    ".working/session-handoff.md",
    ".working/DONE.md",
    ".working/improvement-log.md",
    ".working/validate-pr/history.md",
    ".working/hallucination-metrics.md",
)

# Status-claim tokens: the block asserts a settled state.
STATUS_RE = re.compile(
    r"upstream-CONFIRMED|\bCONFIRMED\b|\bCLOSED\b|\bRESOLVED\b|\bACTIONED\b|\bSHIPPED\b|\b[Ss]hipped\b"
)

# Hedge tokens: the block still carries an unsettled framing.
HEDGE_RE = re.compile(
    r"NEEDS-UPSTREAM|\bTBD\b|\bpending\b|\blikely\b|\bawaiting\b|\bnot yet\b|\bdeferred\b"
)

# A block line: a markdown bullet, a table data row, a bold-led paragraph
# (the pending-decisions "**Status:** ..." shape), or a plain paragraph line
# (the DONE-entry body shape, this aid's own motivating record-drift case),
# including digit-initial paragraphs ("72-hour ..."). Headings, fences, and
# other markup-led lines are excluded; the pairing requirement (a shared key
# on both diff sides of the same file) is what keeps the wide net from
# pairing unrelated prose.
BLOCK_RE = re.compile(r"^\s*(?:- |\| |\*\*|[A-Za-z0-9])")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True)


def block_keys(line: str) -> set[str]:
    """Candidate identities for pairing a rewritten block's old and new versions.

    A block pairs when ANY key matches across the diff sides, because each
    single key fails some real rewrite shape: the bold lead token (the
    '- **(GR-5, ...)**' and '**Status:** ...' shapes) is stable when the
    body is rewritten but changes when the lead itself carries the edited
    status word; the normalized prefix is stable in that case but changes
    when the block's opening value is the edit (a '**Status:** 2 pending'
    to '0 pending' rewrite). Table rows key on their first two cells.
    """
    stripped = line.strip()
    keys: set[str] = set()
    if stripped.startswith("|"):
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        keys.add("cells:" + "|".join(cells[:2]).lower())
    m = re.match(r"(?:-\s+)?\*\*(.+?)\*\*", stripped)
    if m:
        keys.add("lead:" + m.group(1).lower())
    keys.add("prefix:" + re.sub(r"\W+", " ", stripped)[:24].lower())
    return keys


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: tension-scan.py <base-ref> [head-ref]", file=sys.stderr)
        return 2
    base, head = argv[1], (argv[2] if len(argv) > 2 else "HEAD")
    try:
        merge_base = git("merge-base", base, head).strip()
        diff = git("diff", merge_base, head, "--", *SCANNED_FILES)
    except (subprocess.CalledProcessError, OSError) as exc:
        print(f"tension-scan: git failed: {exc}", file=sys.stderr)
        return 2

    # Duplicate keys within a file collapse (set semantics), so two rewritten
    # blocks sharing a key count once; acceptable for an aid whose output is
    # candidates-for-judgment, not a tally.
    removed_keys: set[str] = set()
    added: list[tuple[str, str, set[str]]] = []
    current_file = "?"
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:]
            continue
        if line.startswith("+++ "):
            current_file = "?"  # deleted-file half; do not attribute to the prior file
            continue
        if line.startswith("-") and not line.startswith("---") and BLOCK_RE.match(line[1:]):
            removed_keys.update(f"{current_file}\x00{k}" for k in block_keys(line[1:]))
        elif line.startswith("+") and not line.startswith("+++") and BLOCK_RE.match(line[1:]):
            added.append((current_file, line[1:], block_keys(line[1:])))

    candidates = 0
    rewrites = 0
    for fname, new_line, keys in added:
        if not any(f"{fname}\x00{k}" in removed_keys for k in keys):
            continue  # pure addition, not a rewrite
        rewrites += 1
        st = STATUS_RE.search(new_line)
        hg = HEDGE_RE.search(new_line)
        if st and hg:
            candidates += 1
            print(f"[JUDGE] {fname}: status '{st.group(0)}' with hedge '{hg.group(0)}' in the rewritten block:")
            print(f"        {new_line.strip()}")

    print(
        f"\ntension-scan: {rewrites} rewritten block(s) since {merge_base[:8]}, "
        f"{candidates} carrying a status+hedge pair to judge."
    )
    if candidates:
        print(
            "tension-scan: read each flagged block END TO END; fix a real "
            "contradiction, leave honest narrative alone (the judgment is not "
            "mechanizable; see the docstring's census)."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
