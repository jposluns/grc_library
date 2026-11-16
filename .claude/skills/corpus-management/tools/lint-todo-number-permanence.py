#!/usr/bin/env python3
"""Detect a recycled TODO item number or a stale item-number counter (gate 78).

``.working/TODO.md`` states the permanent-id rule at the bottom of the file: "TODO
numbers are permanent and never recycled (2026-07-15) ... the ``## Number allocation`` block centralizes the ``Next item number:`` counters
(series 5/6/7 frozen; series 3 draws a counter like the other active series), maintained on every TODO
edit; new and split-out items each draw the next number and advance the
counter, closed numbers retire with their item, and existing items are not
renumbered when the file is reorganized (so a number maps to exactly one
item across the file's whole history and lookups by number stay
unambiguous)."

Nothing enforced it, and in the earlier repository it was broken twice:
one change created an item heading whose number had already been retired
to ``.working/DONE.md``, and left a section counter at a number whose
heading was still live; a pre-push verifier caught both. A class-width
check then found a further, older live violation. This gate is the
mechanical backstop.

Four checks, spanning ``.working/TODO.md``, the private backlog list,
the operational store's ``DONE.md`` (logical ``.working/DONE.md``), and the public ``.claude/skills/corpus-management/tools/todo-number-floor.json``:

  A. RECYCLE. A live id from ``.working/TODO.md`` OR the private list
     whose number is also recorded as retired in the operational store's ``DONE.md`` (logical ``.working/DONE.md``)
     heading. Such a number denotes two items, which is exactly what the
     rule forbids. A live id is an item the audit tool counts, read the
     same way in both lists (design note 5): an index row or a ``### <id>``
     heading, read through the shared ``.claude/skills/corpus-management/tools/todo_index_rows.py`` grammar,
     or a top-level bold bullet in the audit tool's closed grammar, read by
     that tool's own parser. The two lists are unioned into the live set.

  B. COUNTER. A ``**Next item number: X.**`` counter pointing at a number
     already used in its section, live in ``.working/TODO.md`` or the private
     list, retired in ``DONE.md``, or at or below the highest ordinal EVER
     allocated for the section per the public floor (``.claude/skills/corpus-management/tools/todo-number-floor.json``).
     A counter at or below any of these hands the next author a colliding id.

  C. CROSS-LIST-COLLISION. A number that is LIVE in BOTH ``.working/TODO.md`` and
     the private list at once: a botched migration that COPIED an item
     into the private list instead of MOVING it, leaving a stale
     duplicate. Because A and B read the DEDUPLICATED union (an id in both
     lists collapses to a single live entry), only this check, comparing
     the two lists as separate sets, catches a copied-not-moved duplicate.

  D. UNCLOSED BLOCK. A code fence or line-starting HTML comment left
     open at the end of ``.working/TODO.md`` or the private list: it hides every
     later bullet item from the live set, so checks A and C would pass
     over a recycled or duplicated id there (design note 1c).

Design decisions, stated because each has a false-positive or
false-negative cost:

  1. RETIRED-ID PARSE. ``DONE.md`` entry headings carry the retired id as a
     ``§N.M`` token, but in several shapes: ``### §N.M <title> ...``,
     ``### TODO §N.M: ...``, ``### PR #N: §N.M <label>: ...``, and multi-id
     ``### §N.M + §N.M + §N.M: ...``. Some entries legitimately carry no id
     at all. This gate takes the ``§``-prefixed ids that appear BEFORE THE
     LAST COLON of the heading, or, when the heading has no colon, every
     ``§``-prefixed id outside parentheses. Rationale: the convention places
     the retired id ahead of the title, while a LATER ``§`` mention is
     usually a destination or a cross-reference (``### TODO §N.M (...
     re-homed to §N.K-§N.J): ...`` retires N.M, not N.K through N.J).

     FALSE-NEGATIVE RISK, and it is large: a ``DONE.md`` entry with no
     ``§N.M`` in its heading is invisible to this gate. In the earlier
     repository, 539 ``DONE.md`` headings carried 140 distinct ids, so
     most entries stated no id. The gate therefore catches recycling of a
     number whose retirement was RECORDED, and cannot catch recycling of a
     number whose retirement was not. Closing that gap needs a ``DONE.md``
     heading convention (always carry the retired id), which is a separate
     change; this gate is deliberately the recorded-retirement half rather
     than nothing.

     1a. PRIVATE BACKLOG (P-N.M) ids use a DIFFERENT convention, so a SECOND
     pass (P_RETIRED_RE) handles them. They carry no ``§`` marker, and the
     DONE heading places the id AFTER the ``PR #N:`` prefix (``### PR
     #N: P-N.M ...``), where the before-last-colon scope of the § pass
     would exclude it. So the P-pass scans the WHOLE paren-stripped heading.
     To keep that wide scope false-positive-free it (a) rejects a compound
     token whole rather than truncating it (``P-N.Mb-ii`` and ``P-N.M-K``
     yield nothing, not the parent ``P-N.M``), (b) skips an id preceded by
     a destination cue (``absorbed into P-N.M``) or followed by a creation
     participle (``P-N.M created``), both naming a LIVE id, and (c) relies
     on the EXEMPT rows for live-umbrella partial closes (the P-id rows,
     including two same-id FAMILY rows, are read from the private sibling's
     ``todo-number-exempt.json``, so this public file names no private
     id; with no sibling there is no private list to check either). Series P-1 has NO public
     floor backstop, so this pass is its ONLY recycle protection.

     ACCEPTED LIMITATION (bare in-paren ids). The P-pass strips parentheticals
     before scanning, because a paren usually holds a DESTINATION or a live
     cross-reference (``(...; advances P-x.z)`` names the LIVE P-x.z). So a
     BARE in-paren id with no retirement verb is NOT detected: this is
     deliberate FP-safety, since catching it would also flag that live P-x.z.
     RETIRE_CUE_PID_RE recovers the sub-case that IS unambiguous (``closes
     P-x.y`` inside a paren). What remains undetected is a completed SUB-ITEM
     referenced bare-in-paren, e.g. website-build sub-items (``(P-x.y.z)``)
     of their P-x.y umbrella (a sub-item governed by its umbrella, ~nil
     top-level recycle risk). Safely closing this needs the live-set-aware
     or structured-DONE-id-field durable fix, not a wider paren scan that
     would reintroduce the destination false positive.

     1b. QUEUE ids (``3bNN``) are read from TWO STRUCTURED POSITIONS only:
     the id list right after the heading's ``PR #N:`` or date prefix (``###
     PR #N: 3bN: ...``, ``### PR #N: 3bN/3bM residue``), and a parenthetical
     holding only ids just before the trailing date (``... guard (3bN)
     (YYYY-MM-DD)``, ``... (3bN, 3bM) (YYYY-MM-DD)``). A queue id anywhere
     else in a heading is a MENTION and retires nothing, however it is
     worded. Scanning the whole heading with guard lists for partial-close
     words and source or destination verbs is unsound: in the earlier
     repository any such list proved to be a sample (``blocks 3bN``,
     ``closure of 3bN``, ``routed to 3bM, 3bN``), so the pass reads
     positions instead of words. In the lead position the item stays open
     when any parenthetical follows the ids, with or without a space or a
     ``:``, ``,`` or ``-`` separator and whatever it holds (``3bN(b)``,
     ``3bN (part d)``, ``3bN: (b)``, ``3bN (closed)``), or a partial word
     follows after an optional ``:``, ``,`` or ``-`` (``3bN part d``, ``3bN:
     part d``, ``3bN partial``, ``3bN phase 1``, ``3bN slice 1``, ``3bN
     split``); a compound token yields nothing (``3bN-ii``, ``3bNb2e1``,
     ``3bN.1``). Other partial wording in the lead position retires the id:
     that failure is loud (the gate goes red on a live item) and an EXEMPT
     row clears it, as for the other series. Measured at adoption in the
     earlier repository: the same 71 retired queue ids as the whole-heading
     scan, none live. The queue series has no counter and no public floor,
     so only checks A and C apply to it.
     FALSE-NEGATIVE RISK (silent, unlike a false retirement, which is loud by
     construction because it only matters when the id is live): a closure is
     not read when it is written only as a mention (``closure of 3bN``), with
     a lead parenthetical (``3bN (closed)``), in a heading that omits the id
     (several 2026-09 closures in the earlier repository), or in a shape
     outside the two positions: a multi-PR prefix (``PR #N + #M:``), an
     id-first heading (``### 3bN closed:``), ``PR #N QA:``, a lead list joined
     by ``and``, ``+`` or ``&``, a backticked or bold lead id, a tail joined
     by ``and`` or ``;``, a tail whose date carries a suffix, or no tail date.
     These are examples, not a complete list: any shape outside the two
     positions is not read. Others seen in probes: ``PR #N:3bN`` (no space
     after the colon), ``PR #N (repo): 3bN``, ``3bN. Title`` (a period reads
     as a compound token), ``(3bN )`` (a space inside the tail), and an
     upper-case ``3BN``. The durable fix is for the finalize tool to write
     the closed id in the lead position.

     1c. An UNCLOSED code fence or line-starting HTML comment in .working/TODO.md or
     the private list hides every later bullet from the audit tool's parser,
     so a recycled id there would pass. Gate 78 therefore reports the tool's
     unclosed_blocks for both files as a finding.

     Sub-bullet ids (``§N.M-R1``, ``§N.M-R3``) are NOT retired item
     numbers, so the id pattern requires a bare dotted number and rejects
     a ``-R<n>`` suffix. Otherwise closing a sub-bullet would read as
     retiring its parent.

  2. REDIRECT STUBS ARE NOT EXEMPT, deliberately. The rule's one exception
     is the series-consolidation move, where "the content moves to a new
     series child X.Y.Z and a forward redirect stub is left at the original
     number (both close together)". A stub (for example ``### N.M ... MOVED
     to N.M.K (Series A)``, now in TODO-REFERENCE.md) is a LIVE heading
     holding its number on purpose, so it is correctly part of the live set:
     the number is alive, not retired. Exempting stubs would be wrong,
     because a number that is simultaneously stub-alive in
     ``.working/TODO.md`` and retired in ``DONE.md`` is a genuine
     inconsistency the gate should report. In the earlier repository no stub
     collided, so this cost nothing there, and it keeps the check honest if
     the convention is applied loosely later.

  3. NON-``N.M`` SERIES. The ``TF-`` series has its own
     ``Next item number: TF-N.`` counter, so it is checked, with its
     integer as the ordinal. The reference-base ids (``SR-1``, ``RB-R6``,
     ``Group ...``, ``Reference-base ...``) have NO counter and no
     retirement convention in ``DONE.md``, so they are skipped for checks
     A and B rather than half-checked. A coded id is still live wherever
     the audit tool counts it as an item: as a TAGGED coded bullet
     (``- **RB-N [private] ...**``) or as a ``### RB-N`` heading (in
     either list; design note 5), so check C does see a coded id live in
     both lists. A coded id has no ordinal, so it takes part in check C
     only; a ``TF-`` token that is not ``TF-<digits>`` (``### TF-NA``) is
     read as a coded id and is unordered too. Stated so a later reader
     does not mistake the silence for a clean result.

  4. EXEMPTIONS. A ``DONE.md`` entry that records a PARTIAL close against a
     still-open umbrella item legitimately names a live number (for example
     ``### TODO §N.M (apply wave complete; item stays open for the matrix
     TSC-column residual): ...``). Those are listed in ``EXEMPT`` keyed by
     ``(id, distinctive_heading_substring)`` with the entry's date (a row
     keyed by a private backlog id goes in the private sibling's
     ``todo-number-exempt.json`` instead, read into ``PRIVATE_EXEMPT``), so an
     exemption cannot silently widen to a different entry. In the earlier
     repository, a line-number key was tried first and REJECTED on
     measurement: one unrelated PR shifted both entries by 4 lines and both
     exemptions lapsed, which would make the gate re-fire on ordinary edits.
     A substring survives line drift while still binding to one entry.

  5. LIVE-ITEM GRAMMAR. This gate, the audit tool and the decision-log hook
     read the same items with the same ids, so a number the stop guard counts
     is a number this gate checks. Index rows and ``### <id>`` headings are
     read through ``.claude/skills/corpus-management/tools/todo_index_rows.py``
     (``index_rows``, ``item_headings``), in ``.working/TODO.md`` and the
     private list alike, and bullets through the audit tool's parser. In the
     earlier repository, a version of this gate read rows through
     ``lint_common.parse_todo_index`` and headings through its own regex, in
     the private list only. What that changes:

     - Rows are read only under a ``| ID | Item | Tags |`` header, as the
       tool and the hook read them; a header-less ``| N.M | ... |`` row is
       not live. RESIDUE: deleting a list's header hides every row of that
       list from all three readers, and no gate reports that today.
     - A row indented by one to three spaces is read (Markdown renders it
       as a table row); four spaces or a tab make it code, and it is not.
     - An UNREADABLE row (``| N.M | two cells |``, or one without its
       closing pipe) fails closed: its id is live, so a recycled or
       duplicated number there is caught and a counter at or below that
       number is stale, and the gate prints a NOTE naming the row. The
       audit tool counts it ACTIONABLE, and gate 90 reports it as
       malformed when it sits inside the index table.
     - A heading id ends at a word boundary: ``### RB-N. title`` is
       ``RB-N``, ``### N.M.a child`` is ``N.M``, and a four-part numeric
       heading keeps only its first three parts. Headings are read in ``.working/TODO.md`` too.
     - A heading outside the shared grammar is not live here, as in the
       tool and the hook: a ``§`` marker (``### §N.M``), or a tab or a
       second space after ``###``. In the earlier repository, the previous
       regex took these, though neither list used them (the live lists
       held none when the shared grammar was adopted); the audit tool
       lists such a heading among its ITEM-LIKE lines when its lead word
       looks like an id.

Exit codes:

  0   no recycled number, no stale counter, no cross-list duplicate and no
      unclosed block.
  1   one or more findings.
  2   a required file is missing or unparseable. `.working/DONE.md` counts as
      "required" only under an EXPLICIT ``--root``; on the DEFAULT lookup it
      resolves via ``lint_common.resolve_working`` (operational store preferred)
      and an ABSENT ledger downgrades the recycled-number check to a reported
      skip, exit 0. A default-lookup private sibling that is present but
      unusable (not a directory, a dangling link, or one that cannot be
      examined) is not absent: it fails with exit 2 naming it. So does a
      sibling whose contents cannot be listed, or whose private list cannot
      be examined or is not a regular file; and so does a ``DONE.md`` lookup
      that meets a store, sibling, ``.working`` directory or ledger that is
      present but cannot be examined (a dangling link, an unsearchable
      directory), a ``GRC_STORE`` path with a missing intermediate component
      (its message names the component), or a ledger that is not a regular
      file. A private list, ``DONE.md`` or ``.working/TODO.md`` that is not
      valid UTF-8 exits 2 naming it. Only a sibling, private list or ledger
      that is genuinely absent (no entry at the path) is skipped. The lookups
      probe with ``os.lstat``/``os.stat``, so the verdict is the same on
      Python 3.11 and 3.12+.

Usage:

    python3 .claude/skills/corpus-management/tools/lint-todo-number-permanence.py
    python3 .claude/skills/corpus-management/tools/lint-todo-number-permanence.py --root <dir>

Stdlib-only Python 3.14.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

from lint_common import InaccessiblePath, print_degraded, resolve_working, resolve_sibling, require_dir, strict_kind
# The one index-row and item-heading grammar the audit tool and the decision-log hook read.
from todo_index_rows import ITEM_HEADING_RE, index_rows, item_headings

REPO_ROOT: Path = Path(__file__).resolve().parents[4]

TODO_REL = ".working/TODO.md"
DONE_REL = ".working/DONE.md"
# The private backlog list lives ONLY in the private sibling (no in-repo
# fallback, unlike .working/); absent for public CI / adopter clones.
PTODO_REL = "P-TODO.md"
# The partial-close exemption rows keyed by a private backlog id live beside the private list,
# in the same sibling, so the public tool names no private id. Format: a JSON object
# {"rows": [[id, distinctive heading substring, "<date>; heading: <substring>"], ...]}.
PEXEMPT_REL = "todo-number-exempt.json"

# Live index rows and '### <id>' headings are read through .claude/skills/corpus-management/tools/todo_index_rows.py (index_rows, item_headings),
# the grammar the audit tool and the decision-log hook count with (design note 5). The gate keeps no
# heading regex or lint_common.parse_todo_index row reader of its own: in the earlier repository, those
# read an unreadable row, a header-less row and a '### RB-N. title' heading differently from the tool.

# A retired id inside a DONE.md heading, always section-marked. Rejects a
# '-R<n>' sub-bullet suffix (see design note 1).
RETIRED_ID_RE = re.compile(r"§\s*((?:\d+(?:\.\d+)+[a-z]?)|TF-\d+)(?!-R\d)(?![\d.])")

# A retired private backlog id (P-N.M / P-N.M.K, optional trailing letter) in a
# DONE.md heading (design note 1a). Differs from the § convention in marker AND
# placement: no '§', and the id usually follows the 'PR #N:' prefix, where the
# before-last-colon scope would exclude it. The token grammar mirrors
# lint_common.TODO_ID_RE's P-branch (parity pinned by a regression test) so live
# and retired ids compare as equal strings. The trailing lookaheads make a
# compound token a NON-match, never a truncated prefix: 'P-N.Mb-ii' (a sub-slice
# label) and 'P-N.M-K' (a creation range) yield nothing, not their parent id;
# 'P-NNN' (undotted) never matches.
P_RETIRED_RE = re.compile(r"\bP-\d+(?:\.\d+){1,2}[a-z]?(?!\.\d)(?![-\w])")

# A P-id immediately preceded by a destination/relocation cue names a LIVE id
# pointed AT ('absorbed into P-N.M', 're-homed to P-N.M', '-> P-N.M'); one
# immediately followed by a creation participle names a LIVE id being opened
# ('P-N.M created'). Measured 2026-08-29 in the earlier repository: zero
# activations across the ledger (real destination mentions sat inside
# parentheses, already stripped), so both guards are prophylactic at zero
# measured false-negative cost.
P_DEST_CUE_RE = re.compile(
    r"(?:\b(?:to|into|as|by|of)|->|\u2192|\badvances|\bnow)\s*$", re.IGNORECASE)
P_CREATE_CUE_RE = re.compile(r"^\s*(?:created|opened|spawned|filed)\b", re.IGNORECASE)

# An explicit retirement verb immediately before a P-id names a RETIRED id even
# INSIDE a parenthetical (which the whole-heading P-pass strips for FP-safety),
# e.g. a ledger heading '(...; closes P-x.y, advances P-x.z)': 'closes P-x.y' is a
# retirement the paren-strip would otherwise hide, while 'advances P-x.z' is
# NOT a retirement verb so the live P-x.z is untouched. Only unambiguous
# retirement verbs (closes/closed/retires/retired); 'superseded' is omitted
# because 'superseded BY P-x' points at a live id.
RETIRE_CUE_PID_RE = re.compile(
    r"\b(?:closes|closed|retires|retired)\s+(P-\d+(?:\.\d+){1,2}[a-z]?)(?!\.\d)(?![-\w])",
    re.IGNORECASE)

# '**Next item number: N.M.**' / '**Next item number: TF-N.**'
COUNTER_RE = re.compile(
    r"^\s*-?\s*\*\*Next item number:\s*((?:\d+\.\d+)|TF-\d+)\.\*\*"
)

PAREN_RE = re.compile(r"\([^()]*\)")

# Retired queue ids (3bNN) in a DONE.md heading are read ONLY from two structured positions (design note 1b): the
# id list right after the heading's ``PR #N:`` (or date) prefix, and a parenthetical holding only ids just before
# the trailing date. A queue id anywhere else in a heading is a mention and retires nothing.
_THREEB_ID = r"3b\d+[a-z]?"
THREEB_LEAD_RE = re.compile(
    r"^### (?:[\w-]+ )?(?:PR #\d+|\d{4}-\d\d-\d\d):\s+(?P<ids>" + _THREEB_ID
    + r"(?:\s*[/,]\s*" + _THREEB_ID + r")*)(?P<after>.*)$")
THREEB_TAIL_RE = re.compile(
    r"\((?P<ids>" + _THREEB_ID + r"(?:\s*[/,]\s*" + _THREEB_ID + r")*)\)\s*\(\d{4}-\d\d-\d\d\)\s*$")
THREEB_ID_RE = re.compile(_THREEB_ID)
# After a lead id list the item stays open when: a word character, dot or hyphen follows at once (a compound
# token: ``3bN-ii``, ``3bNb2e1``, ``3bN.1``); ANY parenthetical follows, with or without a space (``3bN(b)``,
# ``3bN (part d)``, ``3bN: (b)``, ``3bN (closed)``: read structurally, whatever it holds, after an optional ``:``,
# ``,`` or ``-``); or a partial word follows after an optional ``:``, ``,`` or ``-`` separator (``3bN part d``,
# ``3bN: part d``, ``3bN - part d``, ``3bN partial``, ``3bN phase 1``, ``3bN slice 1``, ``3bN split``). Any other
# partial wording retires the id loudly (the gate goes red on a live item) and is cleared by an EXEMPT row, as for
# the other series.
THREEB_LEAD_PARTIAL_RE = re.compile(
    r"^(?:[\w.-]|\s*[:,-]?\s*\(|\s*[:,-]?\s*(?:parts?|partial(?:ly)?|phase|slice|split)\b)", re.IGNORECASE)

# (id, distinctive DONE.md heading substring) -> the exempted entry's date and
# that heading (no code reads the values; _exempt matches the keys). A value's
# heading text leaves out finding ids, so it can be shorter than its key's
# substring (the key keeps them, since it must match the entry). Each row is a
# pre-rule grandfather (a number reassigned before the permanent-id rule) or a
# partial close recorded against a still-open umbrella item; both classes are
# described below. Keyed by a heading SUBSTRING, not
# by line number: a line key looked tighter but re-fired on any unrelated edit
# that shifted DONE.md (measured in the earlier repository: one PR moved two
# entries by 4 lines and both exemptions lapsed), which would make the gate
# unusable per-commit. Each § substring below was checked to match exactly ONE of
# DONE.md's entry headings, so an exemption cannot widen to another entry. The
# P-id partial-close rows (read from the private sibling, see PEXEMPT_REL) add two FAMILY rows (a distinctive id-prefixed
# substring matching a batch of the SAME id's headings, e.g. 'P-N.M Phase'):
# these are id-scoped by _exempt so they still cannot widen to a DIFFERENT item,
# only to more of the same live id's own partial closes.
# The DONE.md entries these rows name live in the private operational store;
# with --root, the entries are read from that root's .working/DONE.md instead.
#
# THIS DICT'S COMPLETENESS, NOT THE PARSE, IS THIS GATE'S FALSE-POSITIVE SURFACE:
# the parse cannot tell a partial or sub-item close from a full retirement, so
# every legitimate live-and-retired coexistence must be covered by a row here:
# its own row, or a FAMILY row (above) whose substring matches several partial
# closes of the same live id. Any future partial close against a still-open
# umbrella must add a row in the same PR that records the close, unless a family
# row for that id already matches its heading.
#
# Two classes, both audited in the earlier repository:
#   PRE-RULE GRANDFATHER: the number was reassigned to different work BEFORE the
#     permanent-id rule (stated in .working/TODO.md) took effect. Closed set: it
#     cannot grow, because a reassignment after the rule is the violation this gate
#     reports. Unfixable forward by design: the same rule forbids renumbering an
#     existing item, so renumbering these to clear the gate would break the rule it
#     enforces.
#   PARTIAL CLOSE: the DONE entry closed part of an item, or one sub-item of it,
#     and the SAME item is legitimately still live. Open-ended: this class stays
#     live maintenance (the NYC-LL144 row below is dated 2026-07-24, after the rule).
EXEMPT: dict[tuple[str, str], str] = {
    # --- pre-rule grandfathers (7 ids, 8 rows: one id collides on two DONE lines) ---
    ("3.2", "CHANGELOG detailed-mirror per-PR-header parity check"): (
        "2026-07-01; heading: CHANGELOG detailed-mirror per-PR-header parity check"
    ),
    ("3.3", "Citation-verification consistency cross-check"): (
        "2026-07-01; heading: Citation-verification consistency cross-check"
    ),
    ("3.9", "document the scratch `ref/` base as the standing citation"): (
        "2026-07-01; heading: document the scratch `ref/` base as the standing citation"
    ),
    ("3.13", "protected `.claude/CLAUDE.md` wind-down"): (
        "2026-07-01; heading: protected `.claude/CLAUDE.md` wind-down"
    ),
    ("3.14", "protected `.claude/CLAUDE.md` wind-down"): (
        "2026-07-01; heading: protected `.claude/CLAUDE.md` wind-down"
    ),
    ("3.14", "tooling half"): (
        "2026-07-01; heading: tooling half"
    ),
    ("4.5", "gate 56 bare-normative-shall audit"): (
        "2026-06-29; heading: gate 56 bare-normative-shall audit"
    ),
    ("4.6", "QA-cadence mechanical enforcement closed as satisfied"): (
        "2026-06-29; heading: QA-cadence mechanical enforcement closed as satisfied"
    ),
    # --- partial closes against a still-open umbrella (open-ended class) ---
    ("3.57", "apply wave complete"): (
        "date not recorded; heading: apply wave complete"
    ),
    ("5.9", "NYC-LL144"): (
        "2026-07-24; heading: NYC-LL144"
    ),
    # Rows keyed by a private backlog id (P-N.M) are not kept in this public file: they live in
    # the private sibling's todo-number-exempt.json and are read into PRIVATE_EXEMPT at run time
    # (see _load_private_exempt).
}


def _ordinal(item_id: str) -> tuple[str, int] | None:
    """Map an id to (section, ordinal) for counter comparison.

    'N.M' -> ('N', M); 'N.M.K' -> ('N', M) (a series child occupies its
    parent's ordinal); 'TF-N' -> ('TF', N). Returns None for an id this gate
    does not order, including a coded id ('RB-N') and a TF- token that is not
    'TF-<digits>' ('TF-NA', read as a coded id).
    """
    if item_id.startswith("TF-"):
        m = re.fullmatch(r"TF-(\d+)", item_id)
        return ("TF", int(m.group(1))) if m else None
    parts = item_id.split(".")
    if len(parts) < 2:
        return None
    m = re.match(r"(\d+)", parts[1])
    if not m:
        return None
    return (parts[0], int(m.group(1)))


def parse_live_index(text: str) -> dict[str, list[int]]:
    """Live index-row ids in one backlog file -> their line numbers.

    Rows are read through ``todo_index_rows.index_rows`` (design note 5):
    only under a ``| ID | Item | Tags |`` header, and an UNREADABLE
    ``| <id> |`` row (no title or tags cell, or no closing pipe) is live too,
    failing closed as it does in the audit tool.
    """
    live: dict[str, list[int]] = {}
    for row in index_rows(text):
        live.setdefault(row.item_id, []).append(row.line)
    return live


def parse_live(text: str) -> dict[str, list[int]]:
    """Live ``### <id>`` heading ids in one backlog file -> their line numbers, read through
    ``todo_index_rows.item_headings``, the heading grammar the audit tool counts (design note 5)."""
    live: dict[str, list[int]] = {}
    for heading in item_headings(text):
        live.setdefault(heading.item_id, []).append(heading.line)
    return live


# Bullet-item grammar. In the earlier repository, gate 78 loaded these from the
# maintainer's audit-backlog-actionability.py, which does not ship; they are carried here
# unchanged (TOP_BULLET_ITEM_RE, the fence and line-starting comment mask, unclosed_blocks
# and the block-containment walk of its parse_items), so the gate reads bullets exactly as
# that tool did.
# An open item written as a top-level bold bullet: ``- **<id>`` at column 0, where <id> is a
# ``3bNN`` queue id or a private ``P-n.m`` id, or a coded id or section number followed by a
# `` [private]`` / `` [public]`` tag. It is an item only outside a ``### <id>`` item block and
# outside a code fence or a line-starting HTML comment.
TOP_BULLET_ITEM_RE = re.compile(
    r"^- \*\*(?P<id>P-\d+(?:\.\d+){1,2}[a-z]?"
    r"|3b\d+[a-z]?"
    r"|(?:[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+|\d+(?:\.\d+){1,2}[a-z]?)(?=(?:\*\*)? \[(?:private|public)\]))"
    r"(?=[ \t*:])(?P<title>.*)$"
)
# A fence opens at 0 to 3 spaces of indentation (deeper indentation is list or code content).
_FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_COMMENT_TOKEN_RE = re.compile(r"<!--|-->")


def _comment_open_after(s: str, open_: bool) -> bool:
    """Whether an HTML comment is still open after ``s``, reading its delimiters in order."""
    for tok in _COMMENT_TOKEN_RE.findall(s):
        if tok == "<!--" and not open_:
            open_ = True
        elif tok == "-->" and open_:
            open_ = False
    return open_


def _mask_scan(lines: "list[str]") -> "tuple[list[bool], int | None]":
    """True for each line inside (or opening/closing) a code fence, or inside an HTML comment that STARTS
    a line, plus the 0-based index of a fence or comment still open at end of file (or None)."""
    mask: list[bool] = []
    fence: "str | None" = None
    in_comment = False
    open_at: "int | None" = None
    for i, ln in enumerate(lines):
        if fence is not None:
            mask.append(True)
            m = _FENCE_OPEN_RE.match(ln)
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not ln.strip()[len(m.group(1)):].strip():
                fence = None
                open_at = None
            continue
        if in_comment:
            mask.append(True)
            in_comment = _comment_open_after(ln, True)
            if not in_comment:
                open_at = None
            elif "-->" in ln:
                open_at = i  # closed and reopened on this line: the open comment starts here
            continue
        m = _FENCE_OPEN_RE.match(ln)
        if m and not (m.group(1)[0] == "`" and "`" in ln[m.end():]):  # ```x``` is inline code
            fence = m.group(1)
            open_at = i
            mask.append(True)
            continue
        stripped = ln.lstrip(" ")
        if stripped.startswith("<!--") and len(ln) - len(stripped) <= 3:
            mask.append(True)
            in_comment = _comment_open_after(ln, False)
            if in_comment:
                open_at = i
            continue
        mask.append(False)
    return mask, open_at


def unclosed_blocks(text: str) -> "list[tuple[int, str]]":
    """A code fence or line-starting HTML comment still open at end of file: everything after its
    opening line is masked, so it is reported rather than left to hide items silently."""
    lines = text.splitlines()
    open_at = _mask_scan(lines)[1]
    if open_at is None:
        return []
    return [(open_at + 1, "unclosed fence or comment opened here: " + lines[open_at].strip()[:60])]


def _bullet_heads(text: str) -> "list[int]":
    """1-based line numbers of the top-level bold-bullet item heads, by the containment walk the audit
    tool's parse_items used: a ``### <id>`` heading opens an item (its body holds no bullet items); a
    ``## `` header, or a non-item ``### `` heading outside a ``### <id>`` item, closes the open block; a
    bullet item's block is its line plus indented, non-blank continuation lines; a masked line never
    starts an item or changes containment."""
    lines = text.splitlines()
    masked = _mask_scan(lines)[0]
    heads: list[int] = []
    in_item = False  # a block is open
    in_bullet = False  # the open block is a bold-bullet item, not a ``### <id>`` item
    for ln_no, line in enumerate(lines):
        is_heading = bool(ITEM_HEADING_RE.match(line))
        if masked[ln_no]:
            continue  # a masked line (a masked ``### <id>`` too) never changes containment
        if is_heading:
            in_item, in_bullet = True, False
            continue
        if line.startswith("## ") or (line.startswith("### ") and (not in_item or in_bullet)):
            in_item = in_bullet = False
            continue
        if not in_item or in_bullet:
            if TOP_BULLET_ITEM_RE.match(line):
                heads.append(ln_no + 1)
                in_item = in_bullet = True
                continue
            if in_bullet:
                if line.strip() and (line.startswith("  ") or line.startswith("\t")):
                    continue
                in_item = in_bullet = False
    return heads


def parse_live_bullets(text: str) -> dict[str, list[int]]:
    """Live bullet-form item ids (the closed bullet grammar: ``- **3bNN``, ``- **P-n.m``, or a tagged coded or
    section id, outside a ``### <id>`` item, a fence or a line-starting comment) -> their line numbers."""
    lines = text.splitlines()
    live: dict[str, list[int]] = {}
    for n in _bullet_heads(text):
        m = TOP_BULLET_ITEM_RE.match(lines[n - 1])
        if m:
            live.setdefault(m.group("id"), []).append(n)
    return live


def parse_live_list(text: str) -> dict[str, list[int]]:
    """One backlog file's live ids -> their line numbers, in order: its index rows and ``### <id>`` headings
    (.claude/skills/corpus-management/tools/todo_index_rows.py) and its bullet items (the carried bullet grammar above). These are the items the audit tool
    counts, read the same way in ``.working/TODO.md`` and the private list (design note 5); in the earlier
    repository, a version of this gate read ``.working/TODO.md`` for rows and bullets only, so a public
    ``### RB-N`` heading was not live."""
    live: dict[str, list[int]] = {}
    for part in (parse_live_index(text), parse_live(text), parse_live_bullets(text)):
        for item_id, lines in part.items():
            live.setdefault(item_id, []).extend(lines)
    for lines in live.values():
        lines.sort()
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
        # this, '### TODO §N.M (... re-homed to §N.K-§N.J): ...' reads as
        # retiring N.K through N.J, which was a measured false positive in
        # the earlier repository.
        scope = PAREN_RE.sub(" ", scope)
        for m in RETIRED_ID_RE.finditer(scope):
            retired.setdefault(m.group(1), []).append(lineno)
        # P-id pass (design note 1a): the WHOLE paren-stripped heading, not the
        # before-last-colon scope: the private backlog's P-id convention places the
        # id AFTER the 'PR #N:' prefix. Cue-guarded against destination/creation
        # mentions of a LIVE id (P_DEST_CUE_RE / P_CREATE_CUE_RE).
        p_scope = PAREN_RE.sub(" ", head)
        for m in P_RETIRED_RE.finditer(p_scope):
            if P_DEST_CUE_RE.search(p_scope[max(0, m.start() - 40):m.start()]):
                continue
            if P_CREATE_CUE_RE.match(p_scope[m.end():]):
                continue
            retired.setdefault(m.group(0), []).append(lineno)
        # Retirement-cue pass: an explicit 'closes/closed/retires/retired P-x.y'
        # names a RETIRED id even inside a parenthetical, which the P-pass strips
        # for FP-safety (in the earlier repository, the ledger held a single real
        # case). Scans the RAW head; a live destination like 'advances P-x.z' is
        # not a cue and stays untouched.
        for m in RETIRE_CUE_PID_RE.finditer(head):
            retired.setdefault(m.group(1), []).append(lineno)
        # Queue-id pass (design note 1b): two structured positions only.
        lead = THREEB_LEAD_RE.match(line)
        if lead and not THREEB_LEAD_PARTIAL_RE.match(lead.group("after")):
            for tid in THREEB_ID_RE.findall(lead.group("ids")):
                retired.setdefault(tid, []).append(lineno)
        tail = THREEB_TAIL_RE.search(line)
        if tail:
            for tid in THREEB_ID_RE.findall(tail.group("ids")):
                retired.setdefault(tid, []).append(lineno)
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


# The private-id rows read from the private sibling's PEXEMPT_REL by main(); empty when the
# sibling or the file is absent, so a private-id partial close then has no exemption.
PRIVATE_EXEMPT: dict[tuple[str, str], str] = {}


def _load_private_exempt(text: str) -> dict[tuple[str, str], str]:
    """Parse the private exemption file: a JSON object whose ``rows`` member is a list of
    ``[id, distinctive heading substring, value]`` string triples. Raises ``ValueError``
    naming the first malformed part (guards against a malformed row silently exempting
    nothing, or everything). A field that is empty or only whitespace is malformed: a
    whitespace-only heading substring occurs in ordinary headings, so it would exempt
    every retirement of its id."""
    import json
    data = json.loads(text)
    if not isinstance(data, dict) or not isinstance(data.get("rows"), list):
        raise ValueError("the file is not a JSON object with a 'rows' list")
    rows: dict[tuple[str, str], str] = {}
    for n, row in enumerate(data["rows"], 1):
        if (not isinstance(row, list) or len(row) != 3
                or not all(isinstance(part, str) for part in row)):
            raise ValueError(f"row {n} is not three strings")
        for field, part in zip(("id", "heading marker", "value"), row):
            if not part.strip():
                raise ValueError(f"row {n} has an empty or whitespace-only {field} field")
        rows[(row[0], row[1])] = row[2]
    return rows


def _exempt(item_id: str, heading: str) -> bool:
    """True if (id, heading) matches a recorded partial-close exemption."""
    for (exempt_id, marker) in (*EXEMPT, *PRIVATE_EXEMPT):
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
    for item_id in sorted(set(live) & set(retired), key=lambda s: (_ordinal(s) or ("", 0), s)):
        done_lines = [
            ln for ln in retired[item_id]
            if not _exempt(item_id, done_lines_text.get(ln, ""))
        ]
        if done_lines:
            findings.append((item_id, live[item_id], done_lines))
    return findings


def _load_number_floor() -> dict[str, int]:
    """The PUBLIC number floor (``.claude/skills/corpus-management/tools/todo-number-floor.json``), keyed by section
    (``1``/``2``/.../``TF``) -> highest ordinal ever allocated. Absent -> {} (no-op)."""
    import json
    fp = REPO_ROOT / ".claude" / "skills" / "corpus-management" / "tools" / "todo-number-floor.json"
    if not fp.is_file():
        return {}
    return {k: int(v) for k, v in json.loads(fp.read_text()).items()
            if not k.startswith("_")}


def find_stale_counters(
    live: dict[str, list[int]],
    retired: dict[str, list[int]],
    counters: dict[str, tuple[str, int]],
    floor: dict[str, int] | None = None,
) -> list[tuple[str, str, int, int, list[str]]]:
    """Counters pointing at an already-used ordinal in their section. ``floor`` (the
    PUBLIC ``.claude/skills/corpus-management/tools/todo-number-floor.json``, keyed by section) supplies the highest
    ordinal EVER allocated, so the counter-recycle check catches a counter at or below a
    RETIRED number even where ``DONE.md`` is absent (CI / adopter clone). This is the
    recycle backstop the full suite enforces, which the private DONE archive could not
    provide."""
    floor = floor or {}
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
        if section in floor:
            used.setdefault(floor[section], []).append(f"floor {section}.{floor[section]}")
        blocking = sorted(n for n in used if n >= target[1])
        if blocking:
            names = sorted({name for n in blocking for name in used[n]})
            findings.append((section, raw, lineno, max(used), names))
    return findings


def _mark(item_id: str) -> str:
    """The section marker a finding prints before an id: ``§`` for a section or TF id, none for a P- or queue id."""
    return "" if item_id.startswith(("P-", "3b")) else "\u00a7"


def find_cross_list_collisions(
    todo_live: dict[str, list[int]],
    ptodo_live: dict[str, list[int]],
) -> list[str]:
    """A number LIVE in BOTH lists at once: a botched migration that COPIED an
    item into the private list instead of MOVING it, leaving a stale duplicate.
    The two single-source checks (recycle, counter) each assumed exactly one
    live source, so this is the only check that catches it."""
    return sorted(set(todo_live) & set(ptodo_live), key=lambda s: (_ordinal(s) or ("", 0), s))


def main(argv: list[str]) -> int:
    global REPO_ROOT, PRIVATE_EXEMPT
    parser = argparse.ArgumentParser(
        description="Detect a recycled TODO item number or a stale item-number counter."
    )
    parser.add_argument(
        "--root",
        type=str,
        default=None,
        help="Override the repository root .working/TODO.md and .working/DONE.md are read "
             "from (used by the regression fixtures for synthetic isolation).",
    )
    args = parser.parse_args(argv[1:])
    if args.root is not None:  # A missing, empty or non-directory --root is refused
        args.root = require_dir(args.root, "--root")
    if args.root is not None:
        REPO_ROOT = args.root.resolve()

    todo_path = REPO_ROOT / TODO_REL
    if not todo_path.is_file():
        print(f"ERROR: required file missing: {todo_path}", file=sys.stderr)
        return 2

    done_path: Path | None
    if args.root is not None:
        # EXPLICIT --root stays VERBATIM, including its missing-file exit 2: the
        # regression fixtures build a synthetic {.working/TODO.md, .working/DONE.md} root
        # and one asserts a fixture with no DONE.md exits 2. It must NOT soften
        # to a skip, and must NOT route through resolve_working, which reads
        # lint_common's REPO_ROOT, not this module's mutated one, so a --root
        # fixture would otherwise silently read the LIVE tree's DONE.md.
        done_path = REPO_ROOT / DONE_REL
        if not done_path.is_file():
            print(f"ERROR: required file missing: {done_path}", file=sys.stderr)
            return 2
    else:
        # Strict: only an ABSENT ledger takes the skip below. A store, sibling, .working
        # directory or DONE.md that is present but cannot be examined (a dangling link, an
        # unsearchable directory, a non-directory where a directory belongs) refuses, under 3.11,
        # whose pathlib raises PermissionError there, as under 3.12+, whose pathlib reads absent.
        try:
            done_path = resolve_working("DONE.md", strict=True)
            done_kind = strict_kind(done_path) if done_path is not None else None
        except InaccessiblePath as exc:
            # The exception names the cause (a missing component is not "present").
            print(f"ERROR: cannot look up DONE.md in the private store ({exc}); "
                  f"refusing the skip an absent ledger takes.", file=sys.stderr)
            return 2
        if done_path is not None and done_kind != "file":
            print(f"ERROR: the private store holding DONE.md is present but unusable: {done_path} "
                  f"is present but is not a regular file.", file=sys.stderr)
            return 2
        if done_path is None:
            # `.working/DONE.md` is the maintainer-only retirement ledger. When
            # the operational store is absent, the ledger is absent in public CI
            # and adopter clones, so check A (RECYCLE, a LIVE id equal to a specific
            # retired id) no-ops there: without the full retired-id set there is
            # nothing a live number can be compared against. Check B (COUNTER) is
            # UNAFFECTED: it reads the PUBLIC floor (.claude/skills/corpus-management/tools/todo-number-floor.json,
            # the highest ordinal EVER allocated per series), so it still catches a
            # counter at or below a retired-ONLY number even here (the floor coupling
            # is the recycle backstop the full suite enforces; only the exact-live-id-vs-retired
            # comparison of check A remains maintainer-local).
            print(
                f"OK: DONE.md not present (maintainer-only working state; "
                f"skipping the recycled-number check in public CI / adopter "
                f"clone). The .working/TODO.md counter check still ran against the live "
                f"item ids."
            )

    # The private list is unioned into the live set so backlog numbers stay permanent ACROSS
    # both lists (a migrated item keeps its N.M id in the private list; gate 78 must still
    # see it). Adopter-graceful: absent private sibling / absent private list -> "" -> no-op.
    ptodo_path: Path | None
    private: Path | None = None
    if args.root is not None:
        cand = REPO_ROOT / PTODO_REL   # verbatim under an explicit synthetic root
        ptodo_path = cand if cand.is_file() else None
        pexempt = REPO_ROOT / PEXEMPT_REL
        pexempt_path = pexempt if pexempt.is_file() else None
    else:
        # Strict: an ABSENT sibling still takes the degraded path below, but one that is
        # present and unusable (a file, a FIFO, a dangling link, an unsearchable parent) refuses.
        try:
            private = resolve_sibling("private", strict=True)
        except InaccessiblePath as exc:
            print(f"ERROR: the private sibling is present but unusable ({exc}); refusing "
                  f"the degraded path it would silently select.", file=sys.stderr)
            return 2
        cand = (private / PTODO_REL) if private is not None else None
        ptodo_path = None
        pexempt_path = None
        if cand is not None:
            # Probe as gate 90 does (list the sibling, then strict_kind), not with
            # Path.is_file, which reads a file in an unsearchable sibling as absent (3.12+) or
            # raises PermissionError (3.11). Only ENOENT in a readable sibling is absent.
            try:
                os.listdir(private)
                kind = strict_kind(cand)
                pexempt = private / PEXEMPT_REL
                pexempt_kind = strict_kind(pexempt)
            except OSError as exc:
                print(f"ERROR: the private sibling is present but unusable: cannot examine "
                      f"{exc.filename or cand} ({exc.strerror}).", file=sys.stderr)
                return 2
            if kind not in (None, "file"):
                print(f"ERROR: the private sibling is present but unusable: {cand} is present "
                      f"but is not a regular file.", file=sys.stderr)
                return 2
            ptodo_path = cand if kind == "file" else None
            if pexempt_kind not in (None, "file"):
                print(f"ERROR: the private sibling is present but unusable: {pexempt} is present "
                      f"but is not a regular file.", file=sys.stderr)
                return 2
            pexempt_path = pexempt if pexempt_kind == "file" else None
        # The DEFAULT lookup's skips exit 0, so a green full-suite run must not read as a pass.
        # Each skip names its own cause; the private list is skipped for an absent sibling AND
        # for a usable sibling with no private list in it, so the notice says which.
        degraded = []
        if done_path is None:
            degraded.append("the recycled-number check (DONE.md: no private store supplies it)")
        if ptodo_path is None:
            why = ("no private sibling supplies it" if private is None
                   else f"the private sibling has no {PTODO_REL}")
            degraded.append(f"the {PTODO_REL} live ids and cross-list duplicate check ({why})")
        if degraded:
            print_degraded(
                "gate 78",
                f"gate 78 skipped {' and '.join(degraded)}; this pass attests nothing about them."
            )

    # A file that is not valid UTF-8 exits 2 naming it, as gate 90 does, not a traceback.
    reading = todo_path
    try:
        todo_text = todo_path.read_text(encoding="utf-8")
        reading = done_path
        done_text = (
            done_path.read_text(encoding="utf-8") if done_path is not None else ""
        )
        reading = ptodo_path
        ptodo_text = ptodo_path.read_text(encoding="utf-8") if ptodo_path is not None else ""
        reading = pexempt_path
        pexempt_text = (
            pexempt_path.read_text(encoding="utf-8") if pexempt_path is not None else None
        )
    except OSError as exc:
        print(f"ERROR: cannot read a required file: {exc}", file=sys.stderr)
        return 2
    except UnicodeDecodeError as exc:
        print(f"ERROR: cannot decode {reading} as UTF-8 ({exc.reason} at byte {exc.start}).",
              file=sys.stderr)
        return 2
    # An absent sibling or file leaves no private-id row (the private list is skipped with the
    # sibling); a present but malformed file exits 2 naming it rather than exempting nothing.
    PRIVATE_EXEMPT = {}
    if pexempt_text is not None:
        try:
            PRIVATE_EXEMPT = _load_private_exempt(pexempt_text)
        except ValueError as exc:
            print(f"ERROR: cannot parse {pexempt_path}: {exc}.", file=sys.stderr)
            return 2
    # Name only the lists actually read, and say so explicitly when the private list is absent (gate 81's style).
    lists_read = f"{TODO_REL} + {PTODO_REL}" if ptodo_path is not None else TODO_REL
    if ptodo_path is None:
        where = ("not in the --root directory" if args.root is not None
                 else "no private sibling; public-only clone / adopter checkout" if private is None
                 else f"the private sibling {private} has no {PTODO_REL}")
        print(f"OK: {PTODO_REL} not present ({where}). Scanning {TODO_REL} only.")

    # Each list is read for all three item forms the audit tool counts (design note 5): index rows
    # and '### <id>' headings through .claude/skills/corpus-management/tools/todo_index_rows.py, bullets through the tool's own parser. A
    # half-converted list therefore keeps every item, whichever form it is written in.
    todo_live = parse_live_list(todo_text)
    ptodo_live = parse_live_list(ptodo_text)
    live = {**todo_live, **ptodo_live}   # union of ids across both lists
    retired = parse_retired(done_text)
    counters = parse_counters(todo_text)

    recycled = find_recycled(live, retired, done_headings(done_text))
    floor = _load_number_floor()
    stale = find_stale_counters(live, retired, counters, floor)
    cross = find_cross_list_collisions(todo_live, ptodo_live)
    # Design note 1c: an unclosed fence or comment hides later bullets from the live set.
    unclosed = [(name, n, msg) for name, txt in ((".working/TODO.md", todo_text), ("P-TODO.md", ptodo_text))
                for n, msg in unclosed_blocks(txt)]
    # Design note 5: an unreadable index row fails closed (its id is live above); the gate names it for a rewrite.
    unreadable = [(name, row.line) for name, txt in ((".working/TODO.md", todo_text), ("P-TODO.md", ptodo_text))
                  for row in index_rows(txt) if not row.readable]
    for name, n in unreadable:
        print(f"NOTE: {name}:{n}: unreadable index row, read as live (fail closed); "
              f"rewrite it as `| <id> | <title> | <tags> |`.")

    if not recycled and not stale and not cross and not unclosed:
        print(
            f"OK: {len(live)} live backlog item(s) ({lists_read}), "
            f"{len(retired)} recorded retired number(s), {len(counters)} counter(s); "
            f"no recycled number, no cross-list duplicate, no stale counter."
        )
        return 0

    if unclosed:
        print("=== unclosed code fence or HTML comment (it hides every later bullet item from this gate) ===")
        for name, n, msg in unclosed:
            print(f"  {name}:{n}: {msg}")

    if recycled:
        print("=== recycled item numbers (a number denoting two items) ===")
        for item_id, _live_lines, done_lines in recycled:
            srcs = []
            if item_id in todo_live:
                srcs.append(".working/TODO.md:" + ",".join(str(n) for n in todo_live[item_id]))
            if item_id in ptodo_live:
                srcs.append("P-TODO.md:" + ",".join(str(n) for n in ptodo_live[item_id]))
            dl = ", ".join(f"{done_path}:{n}" for n in done_lines)
            print(f"  {_mark(item_id)}{item_id}: live at {'; '.join(srcs)}; recorded retired at {dl}")

    if cross:
        print("=== numbers live in BOTH lists (a copy-not-move migration bug) ===")
        for item_id in cross:
            tl = ",".join(str(n) for n in todo_live[item_id])
            pl = ",".join(str(n) for n in ptodo_live[item_id])
            print(f"  {_mark(item_id)}{item_id}: .working/TODO.md:{tl} AND P-TODO.md:{pl}")

    if stale:
        print("=== counters pointing at an already-used number ===")
        for section, raw, lineno, highest, names in stale:
            print(
                f"  .working/TODO.md:{lineno}: section {section} counter is '{raw}' but "
                f"{', '.join(('' if n.startswith('P-') else '§') + n for n in names)} already exist(s) "
                f"(highest used ordinal {highest}); advance it past {highest}"
            )

    total = len(recycled) + len(stale) + len(cross) + len(unclosed)
    print(f"\nFAIL: {total} item-number permanence finding(s).")
    print("TODO numbers are permanent and never recycled: a closed number retires with")
    print("its item, and every edit advances its section's 'Next item number' counter.")
    print("Fix the artefact (renumber the new item, or advance the counter); do not")
    print("weaken this gate. A legitimate partial-close entry against a still-open")
    print("umbrella item goes in EXEMPT (a private backlog id's row goes in the private")
    print(f"sibling's {PEXEMPT_REL} instead), keyed by its id and a distinctive heading")
    print("substring, valued '<date>; heading: <substring>' with the entry's date, or")
    print("'date not recorded; heading: <substring>' when it has none, the value's")
    print("heading text leaving out finding ids that the key keeps; a family row's")
    print("substring may match several of that same id's partial-close headings.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
