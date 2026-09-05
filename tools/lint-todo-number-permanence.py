#!/usr/bin/env python3
"""Detect a recycled TODO item number or a stale item-number counter (gate 78).

``TODO.md`` states the permanent-id rule at the bottom of the file: "TODO
numbers are permanent and never recycled (2026-07-15) ... the ``## Number allocation`` block centralizes the ``Next item number:`` counters
(series 5/6/7 frozen; series 3 draws a counter like the other active series), maintained on every TODO
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
mechanical backstop (built in PR #1173).

Three checks, spanning ``TODO.md``, the private ``P-TODO.md``,
``.working/DONE.md``, and the public ``tools/todo-number-floor.json``:

  A. RECYCLE. A live index-row id from ``TODO.md`` OR the private
     ``P-TODO.md`` (the two are unioned into the live set) whose number is
     also recorded as retired in a ``.working/DONE.md`` heading. Such a
     number denotes two items, which is exactly what the rule forbids.

  B. COUNTER. A ``**Next item number: X.**`` counter pointing at a number
     already used in its section, live in ``TODO.md`` or ``P-TODO.md``,
     retired in ``DONE.md``, or at or below the highest ordinal EVER
     allocated for the
     section per the public floor (``tools/todo-number-floor.json``). A
     counter at or below any of these hands the next author a colliding id.

  C. CROSS-LIST-COLLISION. A number that is LIVE in BOTH ``TODO.md`` and
     the private ``P-TODO.md`` at once: a botched migration that COPIED an
     item into ``P-TODO.md`` instead of MOVING it, leaving a stale
     duplicate. Because A and B read the DEDUPLICATED union (an id in both
     lists collapses to a single live entry), only this check, comparing
     the two lists as separate sets, catches a copied-not-moved duplicate.

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

     1a. PRIVATE-LIST (P-N.M) ids use a DIFFERENT convention, so a SECOND
     pass (P_RETIRED_RE) handles them. They carry no ``§`` marker, and the
     DONE heading places the id AFTER the ``PR #N:`` prefix (``### PR
     #1487: P-3.247 ...``), where the before-last-colon scope of the § pass
     would exclude it. So the P-pass scans the WHOLE paren-stripped heading.
     To keep that wide scope false-positive-free it (a) rejects a compound
     token whole rather than truncating it (``P-1.51b-ii`` and ``P-1.33-35``
     yield nothing, not a parent ``P-1.51`` / ``P-1.33``), (b) skips an id
     preceded by a destination cue (``absorbed into P-1.55``) or followed by
     a creation participle (``P-1.52 created``), both naming a LIVE id, and
     (c) relies on the same EXEMPT dict for live-umbrella partial closes
     (the P-id section, including two same-id FAMILY rows). Series P-1 has
     NO public floor backstop, so this pass is its ONLY recycle protection.

     ACCEPTED LIMITATION (bare in-paren ids). The P-pass strips parentheticals
     before scanning, because a paren usually holds a DESTINATION or a live
     cross-reference (``(...; advances P-3.210)`` names the LIVE P-3.210). So a
     BARE in-paren id with no retirement verb is NOT detected: this is
     deliberate FP-safety, since catching it would also flag the live P-3.210.
     RETIRE_CUE_PID_RE recovers the sub-case that IS unambiguous (``closes
     P-x.y`` inside a paren). What remains undetected is a completed SUB-ITEM
     referenced bare-in-paren, e.g. the ``(P-1.25.26)`` website-build sub-items
     of the P-1.25 umbrella (a sub-item governed by its umbrella, ~nil top-level
     recycle risk). Safely closing this needs the live-set-aware or
     structured-DONE-id-field durable fix (guardrail seed
     gate78-parse-retired-misses-pr-prefixed-P3-ids, part 2), not a wider paren
     scan that would reintroduce the destination false positive.

     Sub-bullet ids (``§5.9-R1``, ``§6.3-R3``) are NOT retired item
     numbers, so the id pattern requires a bare dotted number and rejects
     a ``-R<n>`` suffix. Otherwise closing a sub-bullet would read as
     retiring its parent.

  2. REDIRECT STUBS ARE NOT EXEMPT, deliberately. The rule's one exception
     is the series-consolidation move, where "the content moves to a new
     series child X.Y.Z and a forward redirect stub is left at the
     original number (both close together)". A stub (for example
     ``### 2.24 ... MOVED to 2.25.1 (Series A)``, now in TODO-REFERENCE.md) is a LIVE heading holding
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
  2   a required file is missing or unparseable. `.working/DONE.md` counts as
      "required" only under an EXPLICIT ``--root``; on the DEFAULT lookup it
      resolves via ``lint_common.resolve_working`` (private sibling preferred)
      and an ABSENT ledger downgrades the recycled-number check to a reported
      skip, exit 0.

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

from lint_common import resolve_working, resolve_sibling, parse_todo_index

REPO_ROOT: Path = Path(__file__).resolve().parent.parent

TODO_REL = "TODO.md"
DONE_REL = ".working/DONE.md"
# The private backlog list lives ONLY in the grc_library_private sibling (no
# in-repo fallback, unlike .working/); absent for public CI / adopter clones.
PTODO_REL = "P-TODO.md"

# A live backlog heading: '### 3.109 <title>' or '### 2.25.1 <title>' or
# '### 1.19.10a <title>', '### TF-2 <title>', or '### P-1.1 <title>' (the private
# P-TODO.md list). A leading section marker is
# tolerated ('### §3.109 ...') though TODO does not currently use one.
LIVE_HEADING_RE = re.compile(
    r"^###\s+(?:§\s*)?((?:P-\d+(?:\.\d+){1,2}[a-z]?)|(?:\d+(?:\.\d+)+[a-z]?)|TF-\d+)(?=[\s:]|$)"
)

# A retired id inside a DONE.md heading, always section-marked. Rejects a
# '-R<n>' sub-bullet suffix (see design note 1).
RETIRED_ID_RE = re.compile(r"§\s*((?:\d+(?:\.\d+)+[a-z]?)|TF-\d+)(?!-R\d)(?![\d.])")

# A retired PRIVATE-list id (P-N.M / P-N.M.K, optional trailing letter) in a
# DONE.md heading (design note 1a). Differs from the § convention in marker AND
# placement: no '§', and the id usually follows the 'PR #N:' prefix, where the
# before-last-colon scope would exclude it. The token grammar mirrors
# lint_common.TODO_ID_RE's P-branch (parity pinned by a regression test) so live
# and retired ids compare as equal strings. The trailing lookaheads make a
# compound token a NON-match, never a truncated prefix: 'P-1.51b-ii' (a sub-slice
# label) and 'P-1.33-35' (a creation range) yield nothing, not their parent id;
# 'P-384' (undotted) never matches.
P_RETIRED_RE = re.compile(r"\bP-\d+(?:\.\d+){1,2}[a-z]?(?!\.\d)(?![-\w])")

# A P-id immediately preceded by a destination/relocation cue names a LIVE id
# pointed AT ('absorbed into P-1.55', 're-homed to P-1.9', '-> P-3.250'); one
# immediately followed by a creation participle names a LIVE id being opened
# ('P-1.52 created'). Measured 2026-08-29: zero activations across the ledger
# (real destination mentions sit inside parentheses, already stripped), so both
# guards are prophylactic at zero measured false-negative cost.
P_DEST_CUE_RE = re.compile(
    r"(?:\b(?:to|into|as|by|of)|->|\u2192|\badvances|\bnow)\s*$", re.IGNORECASE)
P_CREATE_CUE_RE = re.compile(r"^\s*(?:created|opened|spawned|filed)\b", re.IGNORECASE)

# An explicit retirement verb immediately before a P-id names a RETIRED id even
# INSIDE a parenthetical (which the whole-heading P-pass strips for FP-safety),
# e.g. DONE:3315 '(...; closes P-3.216, advances P-3.210)': 'closes P-3.216' is a
# retirement the paren-strip would otherwise hide, while 'advances P-3.210' is
# NOT a retirement verb so the live P-3.210 is untouched. Only unambiguous
# retirement verbs (closes/closed/retires/retired); 'superseded' is omitted
# because 'superseded BY P-x' points at a live id.
RETIRE_CUE_PID_RE = re.compile(
    r"\b(?:closes|closed|retires|retired)\s+(P-\d+(?:\.\d+){1,2}[a-z]?)(?!\.\d)(?![-\w])",
    re.IGNORECASE)

# '**Next item number: 3.110.**' / '**Next item number: TF-3.**'
COUNTER_RE = re.compile(
    r"^\s*-?\s*\*\*Next item number:\s*((?:\d+\.\d+)|TF-\d+)\.\*\*"
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
# per-commit. Each § substring below was checked to match exactly ONE of
# DONE.md's entry headings, so an exemption cannot widen to another entry. The
# P-id partial-close section adds two FAMILY rows (a distinctive id-prefixed
# substring matching a batch of the SAME id's headings, e.g. 'P-1.25 Phase'):
# these are id-scoped by _exempt so they still cannot widen to a DIFFERENT item,
# only to more of the same live id's own partial closes.
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
    # --- P-id partial closes (2026-08-29, PR ####; P-1.55). The private-list
    #     ids (P-N.M) newly detected by P_RETIRED_RE. Each is a live P-TODO
    #     umbrella whose DONE headings closed one phase/batch/sub-item. Two are
    #     FAMILY rows (a distinctive id-prefixed substring matching a batch of
    #     same-id headings): scoped to the id by _exempt, so a family row cannot
    #     widen to a different item, only to more of the SAME live id's own
    #     partial closes -- acceptable because recycling that id is forbidden
    #     anyway. ---
    ("P-1.25", "P-1.25 Phase"): (
        "PARTIAL CLOSE family (5 headings, DONE:581/586/591/3210/3214). The "
        "'Executive narrative + executive-experience layer' umbrella (P-1.25) is "
        "live at P-TODO; each 'Phase N' entry closed one build phase of it."
    ),
    ("P-3.202", "P-3.202 synchronous-model cutover-leftover"): (
        "PARTIAL CLOSE (provisional; DONE:3186, #1361). P-3.202 is live at P-TODO "
        "and its detail says the comprehensive sweep is INCOMPLETE, so #1361 is "
        "read as a slice, not a full close. The DONE heading itself does not say "
        "'partial', so the substantiation rests on the live P-TODO detail, not "
        "the heading; the disposition (was #1361 a partial advance, or should "
        "P-3.202 be closed?) is ROUTED to the maintainer (pending-decisions "
        "2026-08-29). Provisionally EXEMPT to keep the gate green; revisit on the "
        "maintainer's call."
    ),
    ("P-3.209", "P-3.209 batch"): (
        "PARTIAL CLOSE family (9 headings, DONE:596-628). The security/risk/"
        "resilience defect-hunt umbrella (P-3.209) is live at P-TODO; each "
        "'batch N' entry closed one batch of it."
    ),
    ("P-3.209", "P-3.209 cadence-consistency findings"): (
        "PARTIAL CLOSE (DONE:216, #1677; findings F45/F47/F41-42 of the live "
        "P-3.209 defect-hunt umbrella)."
    ),
    ("P-1.31", "P-1.31 item"): (
        "PARTIAL CLOSE FAMILY of the still-live P-1.31 umbrella (external "
        "AI-review advisory). The five governance-coverage documents the "
        "maintainer selected (items 6/1/10/2/7) landed as PRs #1821-#1825. "
        "Their five 'PR #NNNN: P-1.31 item N' DONE headings are partial closes; "
        "P-1.31 remains live for held items 3/4/5/8/9. The exemption is "
        "id-scoped, so it cannot widen to a different item."
    ),
    ("P-3.214", "P-3.214 ISO 19011:2018"): (
        "PARTIAL CLOSE (DONE:632, #1392) of the live P-3.214 reference-currency "
        "umbrella (ISO 19011 edition migration)."
    ),
    ("P-3.214", "P-3.214 currency"): (
        "PARTIAL CLOSE (DONE:636, #1391) of the live P-3.214 reference-currency "
        "umbrella (CRA staging + ISO 27017 edition)."
    ),
    ("P-3.214", "P-3.214 B-3"): (
        "PARTIAL CLOSE (DONE:640, #1390) of the live P-3.214 reference-currency "
        "umbrella (ISO 19011 clause-structure)."
    ),
    ("P-3.214", "P-3.214 confirmed errors"): (
        "PARTIAL CLOSE (DONE:648, #1388) of the live P-3.214 reference-currency "
        "umbrella (Bill C-27 lapsed + NIST 800-61 Rev.3 inversion)."
    ),
    ("P-3.217", "P-3.217 HIGH citation defects"): (
        "PARTIAL CLOSE (DONE:3318, #1507) of the live P-3.217 orphaned-finding-set "
        "umbrella (MED/LOW tier stays open)."
    ),
    ("P-3.217", "P-3.217 residue M16/M17"): (
        "PARTIAL CLOSE (DONE:3321, #1508) of the live P-3.217 umbrella (MED/LOW "
        "tier stays open)."
    ),
    ("P-3.217", "P-3.217 HIGH-tier disposition"): (
        "PARTIAL CLOSE (DONE:3563, #1797; the HIGH-tier disposition) of the live "
        "P-3.217 umbrella (MED/LOW tier stays open)."
    ),
    ("P-1.70", "P-1.70 part 3"): (
        "PARTIAL CLOSE. PR #1994 closed part 3 (overlap-aware class-attestation clause "
        "counting) of the still-open P-1.70 umbrella; parts 1-2 (repair the legacy "
        "malformed Closed-today rows; structural fail-closed on any in-window malformed "
        "row) remain live in P-TODO.md. Dated 2026-09-05, after the 2026-07-15 rule."
    ),
    ("P-1.70", "P-1.70 part-2b"): (
        "PARTIAL CLOSE. PR #1996 closed part-2b (the mis-filed finding-row detector: D14 "
        "fail-closed + hook warning) of the still-open P-1.70 umbrella; the L250 archive-row "
        "reword and the warn-to-block posture decision remain. Dated 2026-09-05, after the "
        "2026-07-15 rule."
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


def parse_live_index(text: str) -> dict[str, list[int]]:
    """Live item ids in a NEW-format TODO.md (index rows) -> their line numbers.

    TODO.md is now an index of ``| <id> | <title> | <tags> |`` rows; the ids
    are in cell 1. During the 2026-08 migration P-TODO.md also moves to this
    index-row shape; the caller unions this with ``parse_live`` so BOTH the
    legacy ``### <id>`` layout and the new index layout are covered.
    """
    live: dict[str, list[int]] = {}
    for it in parse_todo_index(text):
        live.setdefault(it["id"], []).append(it["line"])
    return live


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
        # P-id pass (design note 1a): the WHOLE paren-stripped heading, not the
        # before-last-colon scope -- the private-list P-id convention places the
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
        # for FP-safety (the single real case: DONE 'closes P-3.216'). Scans the
        # RAW head; a live destination like 'advances P-3.210' is not a cue and
        # stays untouched.
        for m in RETIRE_CUE_PID_RE.finditer(head):
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


def _load_number_floor() -> dict[str, int]:
    """The PUBLIC number floor (``tools/todo-number-floor.json``), keyed by section
    (``1``/``2``/.../``TF``) -> highest ordinal ever allocated. Absent -> {} (no-op)."""
    import json
    fp = REPO_ROOT / "tools" / "todo-number-floor.json"
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
    PUBLIC ``tools/todo-number-floor.json``, keyed by section) supplies the highest
    ordinal EVER allocated, so the counter-recycle check catches a counter at or below a
    RETIRED number even where ``DONE.md`` is absent (CI / adopter clone). This is the
    CI-enforceable recycle backstop the private DONE archive could not provide."""
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


def find_cross_list_collisions(
    todo_live: dict[str, list[int]],
    ptodo_live: dict[str, list[int]],
) -> list[str]:
    """A number LIVE in BOTH lists at once: a botched migration that COPIED an
    item into P-TODO.md instead of MOVING it, leaving a stale duplicate. The two
    single-source checks (recycle, counter) each assumed exactly one live source,
    so this is the only check that catches it."""
    return sorted(set(todo_live) & set(ptodo_live), key=lambda s: (_ordinal(s) or ("", 0)))


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
    if not todo_path.is_file():
        print(f"ERROR: required file missing: {todo_path}", file=sys.stderr)
        return 2

    done_path: Path | None
    if args.root is not None:
        # EXPLICIT --root stays VERBATIM, including its missing-file exit 2: the
        # regression fixtures build a synthetic {TODO.md, .working/DONE.md} root
        # and one asserts a fixture with no DONE.md exits 2. It must NOT soften
        # to a skip, and must NOT route through resolve_working -- which reads
        # lint_common's REPO_ROOT, not this module's mutated one, so a --root
        # fixture would otherwise silently read the LIVE tree's DONE.md.
        done_path = REPO_ROOT / DONE_REL
        if not done_path.is_file():
            print(f"ERROR: required file missing: {done_path}", file=sys.stderr)
            return 2
    else:
        done_path = resolve_working("DONE.md")
        if done_path is None:
            # `.working/DONE.md` is the maintainer-only retirement ledger. Once
            # `.working/` moves to grc_library_private it is absent in public CI
            # and adopter clones, so check A (RECYCLE, a LIVE id equal to a specific
            # retired id) no-ops there: without the full retired-id set there is
            # nothing a live number can be compared against. Check B (COUNTER) is
            # UNAFFECTED: it reads the PUBLIC floor (tools/todo-number-floor.json,
            # the highest ordinal EVER allocated per series), so it still catches a
            # counter at or below a retired-ONLY number even here (the floor coupling
            # is the CI-enforceable recycle backstop; only the exact-live-id-vs-retired
            # comparison of check A remains maintainer-local).
            print(
                f"OK: {DONE_REL} not present (maintainer-only working state; "
                f"skipping the recycled-number check in public CI / adopter "
                f"clone). The TODO.md counter check still ran against the live "
                f"item ids."
            )

    # P-TODO.md is unioned into the live set so backlog numbers stay permanent ACROSS
    # both lists (a migrated item keeps its N.M id in P-TODO.md; gate 78 must still see
    # it). Adopter-graceful: absent private sibling / absent P-TODO.md -> "" -> no-op.
    ptodo_path: Path | None
    if args.root is not None:
        cand = REPO_ROOT / PTODO_REL   # verbatim under an explicit synthetic root
        ptodo_path = cand if cand.is_file() else None
    else:
        private = resolve_sibling("private")
        cand = (private / PTODO_REL) if private is not None else None
        ptodo_path = cand if (cand is not None and cand.is_file()) else None

    try:
        todo_text = todo_path.read_text(encoding="utf-8")
        done_text = (
            done_path.read_text(encoding="utf-8") if done_path is not None else ""
        )
        ptodo_text = ptodo_path.read_text(encoding="utf-8") if ptodo_path is not None else ""
    except OSError as exc:
        print(f"ERROR: cannot read a required file: {exc}", file=sys.stderr)
        return 2

    todo_live = parse_live_index(todo_text)
    # Transitional (2026-08 migration): P-TODO.md is moving from the legacy
    # ``### <id>`` block shape to the index-row shape (its detail splits into
    # P-TODO-REFERENCE.md). Union both parsers so gate 78 sees every live
    # P-TODO id in EITHER layout; a backlog file is one format at a time, so
    # the two id sets do not overlap in practice.
    ptodo_live = parse_live(ptodo_text)
    for _pid, _plines in parse_live_index(ptodo_text).items():
        ptodo_live.setdefault(_pid, []).extend(_plines)
    live = {**todo_live, **ptodo_live}   # union of ids across both lists
    retired = parse_retired(done_text)
    counters = parse_counters(todo_text)

    recycled = find_recycled(live, retired, done_headings(done_text))
    floor = _load_number_floor()
    stale = find_stale_counters(live, retired, counters, floor)
    cross = find_cross_list_collisions(todo_live, ptodo_live)

    if not recycled and not stale and not cross:
        print(
            f"OK: {len(live)} live backlog item(s) (TODO.md + P-TODO.md), "
            f"{len(retired)} recorded retired number(s), {len(counters)} counter(s); "
            f"no recycled number, no cross-list duplicate, no stale counter."
        )
        return 0

    if recycled:
        print("=== recycled item numbers (a number denoting two items) ===")
        for item_id, _live_lines, done_lines in recycled:
            srcs = []
            if item_id in todo_live:
                srcs.append("TODO.md:" + ",".join(str(n) for n in todo_live[item_id]))
            if item_id in ptodo_live:
                srcs.append("P-TODO.md:" + ",".join(str(n) for n in ptodo_live[item_id]))
            dl = ", ".join(f".working/DONE.md:{n}" for n in done_lines)
            print(f"  {'' if item_id.startswith('P-') else '§'}{item_id}: live at {'; '.join(srcs)}; recorded retired at {dl}")

    if cross:
        print("=== numbers live in BOTH lists (a copy-not-move migration bug) ===")
        for item_id in cross:
            tl = ",".join(str(n) for n in todo_live[item_id])
            pl = ",".join(str(n) for n in ptodo_live[item_id])
            print(f"  {'' if item_id.startswith('P-') else '§'}{item_id}: TODO.md:{tl} AND P-TODO.md:{pl}")

    if stale:
        print("=== counters pointing at an already-used number ===")
        for section, raw, lineno, highest, names in stale:
            print(
                f"  TODO.md:{lineno}: section {section} counter is '{raw}' but "
                f"{', '.join(('' if n.startswith('P-') else '§') + n for n in names)} already exist(s) "
                f"(highest used ordinal {highest}); advance it past {highest}"
            )

    total = len(recycled) + len(stale) + len(cross)
    print(f"\nFAIL: {total} item-number permanence finding(s).")
    print("TODO numbers are permanent and never recycled: a closed number retires with")
    print("its item, and every edit advances its section's 'Next item number' counter.")
    print("Fix the artefact (renumber the new item, or advance the counter); do not")
    print("weaken this gate. A legitimate partial-close entry against a still-open")
    print("umbrella item goes in EXEMPT with its rationale and its DONE.md line.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
