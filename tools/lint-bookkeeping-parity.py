#!/usr/bin/env python3
"""Bookkeeping-parity audit (gate 50).

The honest backstop for the per-PR QA cadence and the TODO/DONE rotation
discipline. It enforces the PRESENCE of the bookkeeping records the
project's process mandates, not their semantic correctness: a gate cannot
tell whether a `/validate-pr` row's prose is accurate, only whether the row
exists. That presence check is exactly the failure mode the mechanical
layer did not previously catch (Sweep 22, 2026-06-22: eleven PRs recorded
with an informal substitute for the formal QA record).

This is the §4.11 "bookkeeping-parity" gate family member co-designed with
the §4.6 (QA-cadence) and §4.10 (TODO/DONE rotation) items, both since closed
(§4.6 as this gate's Check 1, satisfied in #471; §4.10 closed via gate 57 plus
the D5 PR-time check); the separate pre-push-runner gate (folding gates 40/31 into
``run-pr-time-checks.sh``) was built first in PR #333, so this gate extends
rather than duplicates it. It is modelled on
``tools/lint-todo-staleness.py`` (gate 45), the closest analogue: that gate
also reads ``CHANGELOG.md`` plus the working-state history files. Unlike
gate 45, this gate parses committed file *content* (not the commit graph),
so it is a regular corpus gate that runs in ``run_all_audits.sh`` and the
three other audit surfaces; it is deliberately NOT added to the pre-push
history-aware runner (which is for delta and commit-graph gates), because
the post-commit ``run_all_audits.sh`` already runs it before any push.

The six checks (plus the per-PR row-integrity pass, GATE50-UNIQUE, documented at
``row_integrity_findings``: one canonical row per PR per register; explicit ``iteration`` /
``addendum`` companions; no pending/IN-PROGRESS row beside another row for the same PR):

**Check 1, QA-cadence parity (the former §4.6 surface).** Derive the merged-PR
list from the ``CHANGELOG.md`` per-entry headers, matched in BOTH the compact
``**date | version | PR #N**`` form (the 3.16 (PR #855) root-reformat default), the
legacy ``## YYYY-MM-DD, Library Version X, PR #N`` form, AND the rolled-up forms
that condensation produces (``| PRs #A-#B (N PRs) |``, its multi-range variant,
and three ``**Week of ... (PRs ...)**`` shapes), whose ranges are expanded. Before
2026-08-10 only the singular forms were read, so once roll-ups landed this universe
collapsed to the single un-condensed entry and both checks narrowed with it. For each PR N with ``max(INCEPTION, oldest surviving row) <= N <= max(PR)``, require a row in
the PR-scoped validation history register AND (for substantive PRs) a row in
the improvement log, with these exemptions:

- EVERY merged PR, INCLUDING the single highest-numbered one, needs its own
  rows (PR #1248, the synchronous-``/validate-pr`` cutover): the QA now
  runs before the PR is finalized and its rows land in the SAME PR, so the
  window is inclusive of ``max_pr``. (The former highest-PR-in-flight exemption
  went with the retired recursion-avoidance batching.)
- A session-closing handoff PR normally runs its own validate-pr and retro
  like any PR; ONLY when its own QA cannot be made self-contained at the
  session boundary may it take the documented loop-termination fallback and
  skip both (the loop-break). A fallback-taking handoff PR is detected by its explicit validate-pr exemption row
  (the Findings cell contains ``SKIPPED`` together with ``handoff``, or the
  phrase ``handoff-PR exception``).
- A subsumption / maintainer-exception row (Findings cell carries a deliberate
  marker: ``SUBSUMED`` as an all-caps token, ``NOT RUN`` as an all-caps
  disposition at the cell start, or a maintainer-authorised exception in either
  the ``-ised`` or ``-ized`` spelling) satisfies
  the validate-pr requirement and does NOT require a retro row (#328 is the
  canonical instance: its QA was force-stopped and subsumed by Sweep 42).
- A THIRD row state, ``pending`` (3.120 (closing PR #1210)): a validate-pr row that is
  PRESENT but records the QA as ``DISPATCHED`` / ``RESULT PENDING`` and never
  ``RETURNED``. Row presence alone used to read GREEN on it, the hole that let
  validate-pr-1173 / validate-pr-1180 sit unconsumed across sessions. A pending
  row on ANY in-window PR (now including the highest, per the sync cutover)
  FAILS Check 1 as a stranded QA order: the result must have RETURNED before the
  PR is finalized. A row that ALSO carries
  ``RETURNED`` is not pending: the word ``dispatched`` may legitimately appear
  in a returned row's prose, so the classifier requires ``RETURNED`` absent.
- A handful of pre-INCEPTION-era handoff PRs were merged before the
  exemption-row convention existed, so they carry no validate-pr row at all;
  they are listed in ``KNOWN_HANDOFF_NO_ROW`` so the gate does not
  false-positive on a legitimately-absent row.
- The window's lower bound is a DYNAMIC per-register floor,
  ``max(INCEPTION, oldest surviving row in that register)`` (``effective_floor``,
  mirroring gate 59): the dated-archive sweep (1.19.9 (closing PR #1034)) moves AGED
  validate-pr / retro rows out to ``grc_library_private``, keeping each register
  to a recent window, so a swept-out PR falls below its register's floor and is
  out of scope, not flagged missing. The two registers sweep independently, so
  each gets its own floor. Before any sweep both floors equal ``INCEPTION`` and
  behaviour is identical to the fixed-constant gate.

**Check 2, TODO/DONE rotation parity (the former §4.10 surface).** Precision-first
and FP-free (the gate-48 S5 precedent): flag only the unambiguous
rotation-failure shapes the change-tracking rule explicitly prohibits on a
backlog bullet, a self-completion marker. A descriptive mention such as
"batch 1 shipped in #275" inside a still-open item's prose carries no marker
and is NOT flagged; the markers are the uppercase ``SHIPPED in #N`` /
``DONE in #N`` resolution form, a ``Status: completed|done|shipped`` line, a
``[done]`` / ``[shipped]`` / ``[x]`` checkbox/suffix marker, or a
strikethrough ``~~...~~`` on a list item.

**Check 3, worker-provenance (ACTIVE since the PR #612 codification).**
Both activation conditions now hold: the external-collaborator worker
primitive exists (a Model-B worker session delivers research to the scratch
repository's ``inbox/<worker-id>/`` with a ``MANIFEST.md``, per the scratch
``WORKER-ONBOARDING.md`` and the multi-session runbook), and the marking
convention is: a PR that applies a scratch-inbox delivery carries a
``**Worker provenance:**`` line in its detailed-mirror CHANGELOG entry
naming the delivery path. This check validates every such marker line in
the maintainer-grade detailed mirror:
the line must reference an ``inbox/<worker-id>/`` path (the attestation
names WHERE the delivery lives so the orchestrator's apply-time
verification is traceable to it). Presence-not-correctness, per the gate's
framing: a well-formed marker attests that provenance was recorded, not
that the apply-time verification was sound; and an UNMARKED worker
application is free prose no gate can detect, guarded instead by the
CLAUDE.md close-out checklist (the same convention-level residual as the
QA-abbreviation half of Check 1).

**Check 4, version-history parity (the former §4.6 #376 surface).** For every
tracked file that carries BOTH a metadata ``**Version:**`` field AND a
``## Version history`` table, the metadata ``Version`` value must appear as
a row in that table (the #372 paired-surface miss: the pack README metadata
``Version`` moved with no matching history row). Precision-first and FP-free
(the gate-48 S5 / check-2 precedent): flag ONLY a metadata ``Version`` with
no matching history row; tolerate history rows with no current metadata match
(the normal historical rows). This is the mechanizable half of the #376
"update-one-of-a-pair" design; the semantic half (a coded-value migration
leaving a stale description) is not mechanizable and stays the close-out
checklist convention. Adding this as a fourth internal check of gate 50 (not
a new numbered gate) follows the gate-48 "two checks to four" precedent: no
gate-count change, no four-surface re-wiring.

**Check 5, deep-assessment register row-order (the r3 guardrail-review G3
surface).** The deep-assessment run register lists its runs in strictly
ascending run-number order (r1, r2, r3 ...), but had no ordering check while
its sibling structured-bookkeeping files ARE gated (the detailed mirror by
gate 59, the concurrency lease by gate 63). This closes that one-of-a-pair
gap: flag ONLY a run row whose number is not greater than the previous run
row's (precision-first / FP-free; #888 mis-ordered a row and it reached main,
caught by /validate-pr). A register-less fork yields no findings.
Added as a fifth internal check of gate 50 (not a new numbered gate), the same
no-count-ripple precedent as Check 4.

**Check 6, merge-bypass-log parity (added after five same-day recurrences).** Every
in-window merged PR needs a row in the merge-bypass log. Branch protection
here requires an approval a solo-authored PR never receives, so every merge goes
through the maintainer's always-on `--admin` bypass, which is invisible when used; the
log is the only thing that makes it auditable. CLAUDE.md already called an unlogged
bypass a discipline failure, and it recurred five times in one day (#1170 to #1174),
which is past the point where a convention is the right control. Same DYNAMIC-FLOOR model as Check 1
(floor at the register's own oldest row), but NOT the same window: Check 1 includes the
highest PR, because after the synchronous cutover its QA rows are written pre-merge in its
own PR, while Check 6 EXCLUDES it, because a bypass row records a post-merge fact. A row
counts by PRESENCE whatever its Mechanism cell says, so a future protection change that
permits a plain merge is recorded honestly rather than forced to keep reading
`--admin`. An empty or absent log no-ops rather than flagging the whole history. One
exemption (3b145, VERIFY ONLINE / FAIL CLOSED, maintainer ruling 2026-10-01 12:49Z): the
branch's DECLARED OWN PR (the store-scope declaration below) is skipped even when it is
not the highest number, because a rebased branch carries the headers of PRs that merged
after its own was opened, so its own unmerged PR falls below ``max_pr`` while its bypass
row records a post-merge fact the branch cannot have yet. Exactly that one PR, and only
when ALL of the following hold: the offline declaration is certain; its declaring root
header is the SINGULAR form (``own_pr_singular_header``: the compact
``**date | version | PR #N**`` or legacy ``## date, Library Version X, PR #N`` shape; a
weekly roll-up or a range that happens to parse to one PR never qualifies); the origin
remote parses as a github.com remote (the one host this repository's gh is configured
for), with gh pointed at that host THREE ways (round-3 codex R3-01 / claude F1: a
hostless ``--repo owner/repo`` resolves against gh's DEFAULT host, which ``GH_HOST``
can repoint at an enterprise server carrying a same-named repository, and no identity
field below names a host): the explicit host-carrying ``--repo
github.com/<owner>/<repo>`` (gh's HOST/OWNER/REPO form), ``GH_HOST=github.com`` pinned
in the gh subprocess environment over a copy of this process's environment, and the
answer's ``url`` required to begin ``https://github.com/<owner>/<repo>/pull/<N>`` (the
one returned field that names a host); and ``gh pr view <N> --repo
github.com/<owner>/<repo> --json
state,headRefName,isCrossRepository,headRepositoryOwner,headRepository,url``
(``verify_own_pr_open``, bounded by a short timeout) reports the PR OPEN, with its head
branch equal to the current branch, AND with the origin repository itself as its head
repository (``isCrossRepository`` exactly false, ``headRepositoryOwner.login`` and
``headRepository.name`` equal to origin's owner and name): a branch name alone
identifies no repository, so a fork PR with the same branch name keeps the demand
(round-2 codex R2-01 / claude F1). Anything else -- no declaration, a roll-up or range
header, a non-github.com or unparsable origin (round-2 codex R2-02 / claude F2), no gh,
a network or API error, a timeout, unparsable output, duplicate or conflicting JSON keys
(refused by a duplicate-raising ``object_pairs_hook``, round-2 codex R2-03), a CLOSED or
MERGED state, a cross-repository flag, a head-repository mismatch, a PR url under any
other host, repository or number (round-3 codex R3-01), a head-branch mismatch, an
exception raised by the check itself (converted to a printed refusal, never a crash;
round-3 claude F4), any other uncertainty -- keeps the demand and prints why. The online
call is lazy (it runs only when the exemption would actually bite: the own PR is
in-window with no row) and injectable (``_gh_runner``): the in-process tests replace
that seam, the corpus smoke test substitutes it inside its own subprocess before
calling ``main`` (round-3 claude F2), and the remaining live-CLI fixture keeps its
declared own PR at the window ceiling, excluded before the lazy call, so tests never
touch the network. Gate 50
itself DOES run in public CI; it is Check 6, and with it any online call, that never
runs there, because this check reads the maintainer-only merge-bypass log, which public
CI and adopter clones do not have, so they skip the whole check. That store-local
design is deliberate and unchanged.

**Store scope (rows and Check 3; maintainer ruling 2026-09-30 17:07Z, option B,
simplified 21:03Z).** The operational store is shared by every open branch, so the
per-PR row-integrity pass and Check 3 can see another open PR's in-flight rows and
mirror entry. Those two passes defer an entry only after this branch DECLARES its own
PR: the single new singular root ``CHANGELOG.md`` header naming a PR absent from the
merge-base root headers, from origin/main's root headers and from origin/main's
``(#N)`` and ``Merge pull request #N`` commit subjects
(``lint_common.own_pr_declaration``). No other ref is consulted. Historical header
edits, roll-ups, a merged PR's header, a second new identity, a combined identity,
an unparseable or unrecognized new header, and any fence or HTML-comment delimiter
at or above the candidate declare nothing. No declaration, or an unreadable
merge-base changelog, origin/main changelog or origin/main log, means no deferral
and a printed note.

The shared ``StoreScope`` always protects the own PR and every PR covered by this
branch's root headers, origin/main's root headers or origin/main's merge subjects,
range interiors included, so a missing or wrong record for a merged PR or for the
own PR is never deferred (a merged PR that took a D1 ``Changelog:`` trailer instead
of a root entry is protected by its merge subject). Another entry can defer when
every PR it names exceeds the ceiling ``max(declared own PR, highest root header
PR)``, or when every named PR is another open PR absent from all of that evidence.
origin/main is read offline, from the local remote-tracking ref, so merged means
reachable from that ref: a PR merged after the last fetch reads as open, and its
deferral is printed like every other.

Every reader takes its text raw; nothing is masked. One shared, case-insensitive
grammar (``lint_common.STORE_PR_IDENTITY_RE``) reads every PR identity and every
range, so identity and range extraction cannot disagree and a range written with a
lowercase ``pr`` label protects its interior like any other. Register rows defer
only on a complete, certain identity (``store_row_prs`` for retro rows,
``store_history_prs`` for history rows, both carrying range interiors); an identity
with a prose tail is evaluated. In the mirror, an unknown or ambiguous boundary, a
header-shaped line the boundary grammar cannot read, and a fence or comment
delimiter disable deferral for the rest of the file, so an example cannot hide a
later marker and an unrecognized header is never swallowed into the deferred entry
above it. Open-PR deferral also reaches entries below the own entry. A plain,
unmarked header lookalike is indistinguishable from a real entry, including inside
the own entry, where it can defer the lines below it. Likewise, an open PR's header
carried onto a stacked branch that has not yet written its own entry reads offline
as the own entry and declares, so that branch's own records can defer until it
writes one. Both residues are loud, because every deferral prints its location,
named PRs, reason and the declared own PR. Checks 1, 2, 4 and 5 are not scoped and
keep their existing windows without filtering. Check 6 keeps its window and filters
nothing from it either; its one scope input is the declared own PR itself, exempted
from the row demand only when the declaration is certain, its declaring header is the
singular form, and the online check verifies the PR OPEN on this branch with the
github.com origin repository itself as its head repository (3b145, ruling 2026-10-01
12:49Z; see ``bypass_log_findings`` and ``check6_own_pr_exemption``), never any other PR.

The `.working/` inputs and graceful degradation. Five of the six checks read
maintainer-only working state (the validate-pr and improvement-log registers,
the merge-bypass log, the detailed CHANGELOG mirror, the deep-assessment
register). Those reads route through ``lint_common.resolve_working``, which
prefers ``grc_library_private/.working/`` and returns None when neither the
private sibling nor the in-repo ``.working/`` supplies the file. Each dependent
check then no-ops INDIVIDUALLY and the run reports which checks it skipped, so
the closing OK line never asserts a check passed that never ran. Checks 2
(TODO/DONE rotation) and 4 (version-history parity) read PUBLIC files and always
run, so a public-CI or adopter-clone invocation is a partial audit, not a no-op.
Check 1 is all-or-nothing across its TWO registers: with either absent its
per-register floor collapses to INCEPTION and every in-window PR reads as
missing a row, so it skips unless both are present.

Exit codes:
    0 - All present-and-rotated checks pass.
    1 - At least one missing record or rotation-failure marker detected.
    2 - Invocation or environment error (a PUBLIC input, or a private-tree input
        that is PRESENT but unreadable; a simply-ABSENT private input is a skip).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from collections.abc import Callable

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from aiqt_corpus import SIMPLE_CODE_SPAN_RE, read_text_safe  # noqa: E402  # generic core (behaviour-identical to lint_common)
from lint_common import is_default_exempt_root, DEFAULT_EXEMPT_DIRS, REPO_ROOT, StoreScope, STORE_PR_IDENTITY_RE, changelog_entry_boundary, above_store_ceiling, store_deferral_note, store_history_prs, store_row_prs, dynamic_floor, resolve_working, store_deferral_flags, store_scope  # noqa: E402  # grc-config/store, stays local


CHANGELOG_PATH = "CHANGELOG.md"
# Display relpaths for error messages: resolve_working keys (working-root-relative; the
# operational store has no working/ subdir, so no leading dot-working prefix). Reads route
# through resolve_working() with these same keys; see the resolved reads in main().
VALIDATE_PR_HISTORY = "validate-pr/history.md"
IMPROVEMENT_LOG = "improvement-log.md"
TODO_PATH = "TODO.md"
DEEP_ASSESSMENT_REGISTER = "deep-assessment/register.md"

# The PR number from which the QA-cadence parity check applies. Set to a
# recent known-clean frontier rather than the earliest row, because the
# pre-frontier history predates the current exemption-row conventions and
# carries the irregularities mapped below. validate-pr rows start at #183
# and improvement-log rows at #213; with the KNOWN_HANDOFF_NO_ROW handling
# the frontier #329 is clean for both files (verified by a coverage pass
# 2026-06-25, re-confirmed at build time).
INCEPTION = 329

# Session-closing handoff PRs merged before (or without) the validate-pr
# exemption-row convention, so they carry no validate-pr row to auto-detect
# as a handoff. A real, pre-existing bookkeeping gap, not a defect to chase:
# listed here so the gate recognizes them as handoff-exempt. #300 and #322
# are below INCEPTION (harmless either way); #334 is in range and needs this
# allowlist.
# #1054 was added 2026-08-10, when the restored CHANGELOG range parsing first made it visible.
# Its first-parent subject is "Session-closing handoff #1054: Sweep 115 pre-close /validate
# (PASS 0/0 over #1044..#1053) ... + lease RELEASE (#1054)", so it is genuinely the documented
# loop-break class rather than a failing item dropped into an allowlist. It carries no Findings-cell
# marker; an earlier version of this comment claimed that was because #1054 predates the marker
# convention, which the register REFUTES (history.md:509 uses the marker at #886, and :352 at #1043
# the same day). The honest reason is simply that the row was never written, and the omission stayed
# invisible while this check's window was empty.
KNOWN_HANDOFF_NO_ROW: frozenset[int] = frozenset({300, 322, 334, 1054})

# Never-merged PR numbers that fall INSIDE a contiguous weekly range in the root
# CHANGELOG. The weekly headers cite gap-free PR ranges by convention (a skipped
# number is shown in-range rather than as a visible gap), but this gate builds its
# "every merged PR needs a QA row" universe by expanding those ranges, so a skipped
# number would otherwise be demanded a validate-pr and a bypass-log row it can never
# have. These PRs were opened-and-closed-without-merge (verified: no `(#N)` merge
# commit on `main`), so excluding them is a false-positive fix, not a gate weakening.
KNOWN_SKIPPED_PRS: frozenset[int] = frozenset({1092, 1093, 1221, 1400, 1471, 1493, 1648, 2083, 2653})

# A row whose Findings cell marks the PR as a session-closing handoff
# (validate-pr + retro both legitimately skipped, the loop-break).
HANDOFF_FINDINGS = re.compile(
    r"handoff-?PR\s+exception|SKIPPED.*handoff|handoff.*SKIPPED",
    re.IGNORECASE,
)

# A row whose Findings cell marks the PR's QA as subsumed by a later sweep
# or carried under an explicit maintainer-authorised exception (both the
# -ised and -ized spellings are recognized: the history predates the
# Canadian-spelling harmonization, so old rows carry -ised while new rows
# follow the house -ized convention). Satisfies the validate-pr requirement;
# no retro row required.
# Deliberate subsumption / maintainer-exception markers. 3.158: the earlier
# single case-insensitive pattern matched ``NOT run`` ANYWHERE in a Findings
# cell, so incidental prose ("did not run the grep", "do not run --prune")
# mis-classified an ordinary row as exempt, a fail-open (a genuinely-pending
# row carrying such prose would have escaped Check 1). Each marker must now be
# an UNAMBIGUOUS, deliberately-authored disposition:
#   * ``SUBSUMED`` as an all-caps token (case-sensitive), never lowercase prose;
#   * ``NOT RUN`` as an all-caps disposition ANCHORED at the cell start (after
#     optional bold), where a real exemption states it (e.g.
#     ``**NOT RUN (no independent party available).**``), never mid-prose; and
#   * ``maintainer-authorised/-authorized exception`` (a deliberate phrase):
#     the regex REQUIRES the ``exception`` qualifier as an ADJACENT word (up to
#     three intervening words, no clause separator), so neither incidental
#     ``maintainer-authorized the reviewer; RESULT PENDING`` prose NOR a
#     cross-clause ``...the reviewer; exception request pending`` in a
#     genuinely-pending row pre-empts the pending check (the 3.158 residual the
#     Sweep-142 dual-family /validate + its codex /validate-pr caught: the earlier
#     bare ``.search`` matched anywhere, and a ``[^.|]{0,40}`` bridge still let a
#     semicolon-separated ``exception`` word through).
_SUBSUMED_MARK = re.compile(r"\bSUBSUMED\b")
_NOT_RUN_MARK = re.compile(r"^\s*\*{0,2}\s*NOT\s+RUN\b")
_MAINT_AUTH_MARK = re.compile(r"maintainer[-\s]authori[sz]\w*(?:\s+\w+){0,3}\s+exception\b", re.IGNORECASE)


def is_subsumption_findings(findings: str) -> bool:
    """True when the Findings cell carries a deliberate subsumption /
    maintainer-exception marker (3.158: incidental "not run" prose in an
    ordinary row does not qualify)."""
    return bool(
        _SUBSUMED_MARK.search(findings)
        or _NOT_RUN_MARK.match(findings)
        or _MAINT_AUTH_MARK.search(findings)
    )

# A row whose QA was DISPATCHED / offloaded but has NOT yet RETURNED, so the row is
# present-but-UNRESOLVED (3.120 (closing PR #1210)). Check 1 was satisfied by row PRESENCE, so an
# honest `DISPATCHED, RESULT PENDING` row read GREEN while the PR's QA had in fact never
# run: this is the stranded-QA hole that let validate-pr-1173 (`PENDING, offloaded`) and
# validate-pr-1180 (`DISPATCHED`) sit unconsumed across sessions. It is a THIRD state,
# between resolved-present and absent, and Check 1 FAILS on it in its own PR (the window includes the current highest PR). A
# row that also carries RETURNED is NOT pending (it returned; the word may appear in its
# prose, e.g. "the order was dispatched at #1180 and never returned, now RETURNED").
PENDING_FINDINGS = re.compile(r"\bDISPATCHED\b|\bRESULT\s+PENDING\b|^\**\s*PENDING\b", re.IGNORECASE)
RETURNED_MARK = re.compile(r"\bRETURNED\b", re.IGNORECASE)

# A markdown table data row: leading pipe, an ISO date cell, then the rest.
TABLE_ROW = re.compile(r"^\|\s*\d{4}-\d{2}-\d{2}\s*\|")


# The right-hand boundary of a PR-number token (P-3.245): the digit run must
# not CONTINUE into a word character (`resume-0825b`), a dotted-id segment
# (`3.245`, `1.17.118`, `2026.08.415`), or a hyphenated identifier tail
# (`338-x`) -- while a `-#` continuation stays allowed, so a combined
# `#1699-#1710` cell keeps contributing both endpoints exactly as the old
# extraction did. A sentence-final `.` with no digit after it is not a
# continuation (`#1709.` still parses).
PR_NUM_BOUNDARY = r"(?!\w|\.\d|-(?!#))"

# A PR token inside a register PR cell (the validate-pr history's c[2]). Two
# shapes: a `#`-anchored `#N` in any adjacent context (`#1709`, `PR #2000`,
# `#1699-#1710`), or a STANDALONE bare digit run (the documented mixed and
# combined formats: `500`, `248, 249`), left-bounded so a digit run inside a
# dotted or hyphenated identifier (`3.245`, `P-3.150`, `2026.08.415`,
# `§7.1.1`, `resume-0825b`) is never read as a PR. P-3.245: the earlier
# greedy `re.findall(r"\d+", ...)` matched those interior digit runs,
# injected phantom low PR numbers into the status map, and collapsed the
# dynamic floor (`max(INCEPTION, min(rows))`) toward INCEPTION, demanding
# rows for every swept-out PR (the #1709-window storm).
PR_CELL_TOKEN = re.compile(r"#(\d+)" + PR_NUM_BOUNDARY + r"|(?<![\w.#-])(\d+)" + PR_NUM_BOUNDARY)

# improvement-log PR column tolerates an optional leading `#` (mixed format:
# some rows `338`, others `#333`). P-3.245: the trailing PR_NUM_BOUNDARY
# refuses a digit run that continues into a larger token, so a dotted
# backlog id or version at the cell start (`3.245`, `1.17.118`,
# `2026.08.415`) no longer reads as a PR number.
RETRO_ROW_PR = re.compile(r"^\|\s*\d{4}-\d{2}-\d{2}\s*\|\s*#?(\d+)" + PR_NUM_BOUNDARY)

# TODO/DONE rotation-failure markers on a backlog bullet (precision-first).
# Two precision levers keep this FP-free on the live TODO: (1) the
# strikethrough and checkbox markers must begin the bullet's CONTENT (a whole
# item struck through / checked off as done), so inline strikethrough used to
# mark completed sub-steps within a still-open item, e.g. FR-167's
# "~~risk 15~~ -> ~~dev-security 17~~" batch sequence, is not flagged; (2) the
# suffix / status / uppercase-SHIPPED markers are matched against the line
# with code-span (backtick) content removed, so the maintenance note that
# describes the convention ("no `[done]` suffixes") is not flagged.
CODE_SPAN = SIMPLE_CODE_SPAN_RE

# Markers that must begin the bullet content (checked against the raw line).
TODO_BULLET_START_MARKERS: list[tuple[str, re.Pattern[str]]] = [
    # A list item whose content begins with a strikethrough: `- ~~PR #99~~`.
    ("strikethrough-on-bullet", re.compile(r"^\s*[-*+]\s+~~")),
    # A checked task box opening a bullet: `- [x] ...`.
    ("checkbox-done", re.compile(r"^\s*[-*+]\s+\[[xX]\]")),
]

# Markers checked against the line with code spans stripped (so a backticked
# reference to the convention is not a marker).
TODO_DESPANNED_MARKERS: list[tuple[str, re.Pattern[str]]] = [
    # `[done]` / `[shipped]` suffix marker.
    ("done-suffix-marker", re.compile(r"\[(?:done|shipped)\]", re.IGNORECASE)),
    # `Status: completed|done|shipped` annotation.
    ("status-completed", re.compile(r"Status:\s*(?:completed|done|shipped)", re.IGNORECASE)),
    # Uppercase resolution marker `SHIPPED in #N` / `DONE in #N`. Uppercase is
    # the precision lever: descriptive lowercase "shipped in #275" inside an
    # open item is not a marker and is not flagged.
    ("uppercase-shipped-marker", re.compile(r"\b(?:SHIPPED|DONE)\s+in\s+#?\d+\b")),
]


# Check 4 (version-history parity) patterns.
# Metadata Version field: the first `**Version:** X.Y.Z` line in a file.
METADATA_VERSION = re.compile(r"^\*\*Version:\*\*\s*([0-9]+(?:\.[0-9]+)+)", re.MULTILINE)
# The `## Version history` section heading.
VERSION_HISTORY_HEADING = re.compile(r"^##\s+Version history\s*$", re.MULTILINE)
# A whole table cell that is a dotted version token (2+ parts).
VERSION_TOKEN = re.compile(r"^[0-9]+(?:\.[0-9]+)+$")

# Check 5 (deep-assessment register row-order): a run-table data row whose
# first (Run) column is an `rN` run identifier. The register lists runs in
# strictly ascending run-number order (r1, r2, r3 ...); a row out of order is
# the #888 mis-order the r3 guardrail-review G3 finding flagged.
REGISTER_RUN_ROW = re.compile(r"^\|\s*r(\d+)\s*\|")


def read(rel: str) -> str:
    path = REPO_ROOT / rel
    return path.read_text(encoding="utf-8")


_CODE_SPAN_RE = re.compile(r"(`+)(?:.+?)\1")


def split_markdown_row(line: str) -> list[str]:
    """Split a markdown table row on pipes OUTSIDE inline code spans.

    3.159: a naive ``line.split("|")`` treats a pipe inside an inline code span
    (e.g. a Findings cell mentioning a backtick-wrapped pipe) as a column
    delimiter, shifting every cell after it. Because the row classifiers read a
    FIXED column index (the Findings cell at index 4), a shifted row is read
    from the wrong column, a fail-open in a QA-cadence gate. This masks each
    code span, splits on the surviving (unfenced) pipes, then restores the
    spans, so a pipe inside a span stays within its cell. A code span is a run
    of one-or-more backticks, content, and a MATCHING run of equal length
    (CommonMark); the ``\1`` backreference matches the run length, so
    multi-backtick spans (``a|b`` wrapped in double backticks) are handled, not
    only single-backtick ones. An UNMATCHED backtick run is literal text, so its
    pipes split normally; a backslash-escaped pipe outside a span stays a
    delimiter (out of scope here, it would change the census).
    """
    spans: list[str] = []

    def _mask(match: "re.Match[str]") -> str:
        spans.append(match.group(0))
        return f"\x00{len(spans) - 1}\x00"

    masked = _CODE_SPAN_RE.sub(_mask, line)

    def _restore(cell: str) -> str:
        return re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], cell)

    return [_restore(cell) for cell in masked.split("|")]


def cells(line: str) -> list[str]:
    """Split a markdown table row into stripped cells (code-span-aware, 3.159)."""
    return [c.strip() for c in split_markdown_row(line)]


# An entry header that carries a PR token, in any of the six shapes the live file uses: the
# singular `| PR #N |`, the daily roll-up `| PRs #A-#B (N PRs) |`, its multi-range variant, and
# three `Week of ... (PRs ...)` weekly forms that carry no declared count.
CHANGELOG_PR_HEADER = re.compile(
    r"^(?:##\s+\d{4}-\d{2}-\d{2},\s+Library Version\s+[0-9.]+,\s+PRs?\s+(?P<a>#[\d\s,#and-]*)"
    r"|\*\*\d{4}-\d{2}-\d{2} \| [0-9.]+ \| PRs? (?P<b>#\d[^*]*)\*\*"
    r"|\*\*Week of \d{4}-\d{2}-\d{2} \(PRs? (?P<c>#\d[^)]*)\)\*\*)",
    re.MULTILINE,
)
# P-3.245 belt-and-braces: `(?!\.\d)` refuses a dotted continuation, so a
# literal `#3.245` in a header body reads as no PR rather than as `#3`.
PR_RANGE_TOKEN = re.compile(r"#(\d+)(?!\d|\.\d)(?:\s*-\s*#(\d+)(?!\d|\.\d))?")
# A single header cannot legitimately span more than this many PRs. Enforced across the WHOLE
# header, not per range token: `#1-#5000 and #5001-#10000 and #10001-#15000` is three in-bound
# tokens and 15000 PRs, which a per-token check would wave through. Checked BEFORE the set is
# built, because it is `prs.update(range(...))` that materializes (the `range` itself is lazy), so
# a mistyped bound would otherwise exhaust memory instead of producing a finding.
MAX_HEADER_SPAN = 5000
# NO example strip anywhere in this gate (orchestrator decision 2026-09-30 14:51Z, superseding
# the W5-era FENCED_BLOCK / HTML_COMMENT strip this gate used to apply to its audit universe and
# its register records): every reader takes the text RAW. A fenced or commented header lookalike
# now counts toward the audit universe, and a row lookalike counts as a row, which can only ADD
# loud demands or findings (the safe direction); a mask, by contrast, was shown to HIDE real rows
# (r4 QA: literal `<!--` / `-->` tokens in two rows' prose swallowed every row between them).


def parse_changelog_prs(text: str) -> set[int]:
    """Every PR number a CHANGELOG entry header covers, ranges expanded.

    The roll-up condensation replaced per-PR headers with ranged ones (`PRs #1465-#1470 (6 PRs)`).
    The numbers stayed in the file; this parser is what had never been taught the new shape, so
    the checks built on it silently narrowed to the one remaining singular entry.

    A range is expanded inclusively. Roll-up headers keep ranges contiguous (the change-tracking
    rule shows a never-merged number inside the range, not as a split), so a never-merged number
    is excluded by listing it in KNOWN_SKIPPED_PRS, which the caller subtracts: #1221, #1400,
    #1471 and #2083 sit inside unbroken weekly ranges for exactly that reason. Where a range spans
    a never-merged number that is not listed, the surplus surfaces as a DEMAND for
    a bypass row on a PR that has none. Nothing removes that demand, which is deliberate: it is
    the LOUD direction, and a guard that removed it was built and deleted on 2026-08-10 because it
    could not distinguish a never-merged PR from one its input simply had not seen. (Checked
    2026-09-28 for #1826-#2639: every number there with no merge commit is in KNOWN_SKIPPED_PRS;
    the older part of the window was not re-measured then.) The declared `(N PRs)` count, where a form carries one, is not relied on here; the
    weekly forms carry none.

    RAW read, no example strip (orchestrator decision 2026-09-30 14:51Z, superseding the W5
    strip): a fenced or HTML-commented header lookalike counts toward the universe like any
    other header, so an example can only ADD loud row demands, never remove one; and because
    the store-scope ceiling reads the SAME raw text with the same cell grammar,
    ``max(changelog)`` still never exceeds the ceiling.
    """
    prs: set[int] = set()
    for match in CHANGELOG_PR_HEADER.finditer(text):
        body = match.group("a") or match.group("b") or match.group("c") or ""
        spans: list[tuple[int, int]] = []
        for lo_s, hi_s in PR_RANGE_TOKEN.findall(body):
            lo = int(lo_s)
            hi = int(hi_s) if hi_s else lo
            if hi < lo:
                # An inverted range is malformed. Take the two endpoints, which are real PR
                # numbers the header names, rather than dropping the header's PRs silently.
                spans.append((lo, lo))
                spans.append((hi, hi))
                continue
            spans.append((lo, hi))
        if sum(hi - lo + 1 for lo, hi in spans) > MAX_HEADER_SPAN:
            # Over the whole-header bound: keep only the endpoints each token names, so the audit
            # narrows rather than losing the header entirely, and never materializes the interior.
            prs.update(n for lo, hi in spans for n in (lo, hi))
            continue
        for lo, hi in spans:
            prs.update(range(lo, hi + 1))
    return prs


def parse_validate_pr_status(text: str) -> dict[int, str]:
    """Map each PR with a validate-pr row to its status.

    Status is one of 'handoff', 'subsumption', 'pending', or 'normal', classified from
    the row's Findings cell (field index 4). A PR cell may name more than one
    PR (a combined row such as `248, 249`); each named PR inherits the row's
    status. PR tokens are boundary-checked (P-3.245): a digit run inside a
    dotted or hyphenated identifier (`3.245`, a version, `resume-0825b`) is
    not read as a PR.
    """
    status: dict[int, str] = {}
    for line in text.splitlines():
        if not TABLE_ROW.match(line):
            continue
        c = cells(line)
        # c[0]='' c[1]=date c[2]=PR c[3]=touched c[4]=findings ...
        if len(c) < 5:
            continue
        findings = c[4]
        if HANDOFF_FINDINGS.search(findings):
            row_status = "handoff"
        elif is_subsumption_findings(findings):
            row_status = "subsumption"
        elif PENDING_FINDINGS.search(findings) and not RETURNED_MARK.search(findings):
            row_status = "pending"
        else:
            row_status = "normal"
        for pr in (int(m.group(1) or m.group(2)) for m in PR_CELL_TOKEN.finditer(c[2])):
            # 3.150 item 3: the ledger is newest-first, so the FIRST parsed row for a PR is the
            # newest; keep it (setdefault) rather than letting a later (older) row overwrite. This
            # forecloses a latent false-BLOCK where a newer RETURNED row above an older DISPATCHED
            # row would classify `pending`. (Zero live effect today: one row per PR by convention.)
            status.setdefault(pr, row_status)
    return status


def parse_retro_prs(text: str) -> set[int]:
    """The set of PR numbers with an improvement-log (/retro) row (boundary-checked, P-3.245)."""
    prs: set[int] = set()
    for line in text.splitlines():
        m = RETRO_ROW_PR.match(line)
        if m:
            prs.add(int(m.group(1)))
    return prs


# GATE50-UNIQUE (row integrity, 2026-09-24): Check 1 above tests PRESENCE and reduces each
# register to one status per PR (``setdefault`` / a set), so a stale IN-PROGRESS row left beside a
# final row, or two retro rows for one PR, read green. Observed: after a context compaction the
# orchestrator appended final rows beside its own pre-compaction IN-PROGRESS rows for PR #2490.
# This check keeps every row occurrence and enforces ONE canonical row per PR per register.
# A row is a COMPANION (allowed alongside the canonical row) only when its PR cell says so with an
# explicit ``iteration`` or ``addendum`` keyword (``#2429 iteration``, ``#2398 addendum``);
# a companion never stands alone. One ordinary row plus one handoff/subsumption exemption row is
# the documented legitimate pair. A row whose disposition cell BEGINS with a pending marker
# (IN PROGRESS / DISPATCHED / RESULT PENDING / PENDING) may not coexist with any other row for the
# same PR. The marker is matched at the start of c[4] or c[5] (see below), because the history
# has two layouts (Findings at c[4] in the legacy layout, the disposition at c[5] in the newer
# one), which the fixed-index classifier above cannot see. A lone IN-PROGRESS row is allowed (it
# is the normal state between opening a PR and its close-out upsert).
# The companion keyword must sit IMMEDIATELY after the PR token(s) at the start of the PR cell
# (``#2429 iteration``, ``1329 addendum``, ``#10, #11 addendum``), so a PR cell that merely
# describes an addendum (``#10 (addendum detector fix)``) is not a companion.
COMPANION_PR_CELL = re.compile(
    STORE_PR_IDENTITY_RE.pattern + r"\s+(?:iteration|addendum)\b", re.IGNORECASE
)
ROW_PENDING_CELL = re.compile(
    r"^\**\s*(?:IN[\s-]PROGRESS|DISPATCHED|RESULT\s+PENDING|PENDING)\b", re.IGNORECASE
)
# EXEMPTION is read from c[4] only, the same Findings cell Check 1 classifies, because the
# history's layouts vary too much for a reliable disposition-column guess (a strict tier-cell
# test left 520 live rows with no recognizable disposition in the guessed cell). A newer-layout
# row pair that is legitimately ordinary + exemption therefore needs an explicit companion marker.
# PENDING is a start-anchored marker in c[4] or c[5] (the newer layout's disposition cell), and is
# suppressed when RETURNED appears in any cell from c[4] on (not the Touched/Families cell c[3]) (a legacy row can carry RETURNED in Findings
# and stale pending prose in Hot-fix, e.g. history.md:653). Residue: a pending-worded Hot-fix cell
# on a row with no RETURNED anywhere reads pending; it only matters when the PR has another row.


def _disposition_candidates(c: list[str]) -> list[str]:
    return [c[4]] + ([c[5]] if len(c) > 5 else [])


def _history_row_records(text: str) -> list[tuple[int, list[int], str, bool, bool]]:
    """(line, prs, exemption_kind or '', is_companion, is_pending) for each history data row.

    RAW read, no example masking (orchestrator decision 2026-09-30 14:51Z): a fenced or
    commented row lookalike is a record like any other (a loud duplicate at worst), because the
    old blanking pass was shown to do the opposite of documentation-hygiene: a literal ``<!--``
    in one row's prose and a ``-->`` in a later row's swallowed every REAL row between them.

    The keys stay this register's own PR tokens; they travel as a ``StorePRs`` carrying the
    cell's complete identity, its certainty and its range interiors, so a combined or ranged
    row that names the own PR or a merged PR (``#2660-#2662`` around own #2661) is evaluated,
    never deferred on its endpoints alone.
    """
    out: list[tuple[int, list[int], str, bool, bool]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if not TABLE_ROW.match(line):
            continue
        c = cells(line)
        if len(c) < 5:
            continue
        keys = sorted({int(m.group(1) or m.group(2)) for m in PR_CELL_TOKEN.finditer(c[2])})
        if not keys:
            continue
        prs = store_history_prs(c[2], keys)
        if HANDOFF_FINDINGS.search(c[4]):
            kind = "handoff"
        elif is_subsumption_findings(c[4]):
            kind = "subsumption"
        else:
            kind = ""
        returned_anywhere = any(RETURNED_MARK.search(x) for x in c[4:])
        pending = not returned_anywhere and any(ROW_PENDING_CELL.match(d) for d in _disposition_candidates(c))
        out.append((lineno, prs, kind, bool(COMPANION_PR_CELL.match(c[2])), pending))
    return out


def _retro_row_records(text: str) -> list[tuple[int, list[int], str, bool, bool]]:
    """Every raw retro data row whose PR cell opens with a PR identity.

    The complete leading identity is the row's key set (``#10, #11 addendum (/retro)``,
    ``#2652 and #2650`` and ``#2650-2652`` name both PRs); later mentions in the cell are prose,
    not the identity, and a prose tail makes the identity uncertain, so it cannot defer.
    """
    out: list[tuple[int, list[int], str, bool, bool]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if not TABLE_ROW.match(line):
            continue
        c = cells(line)
        if len(c) < 3:
            continue
        prs = store_row_prs(c[2])
        if not prs:
            continue
        out.append((lineno, prs, "", bool(COMPANION_PR_CELL.match(c[2])), False))
    return out


def row_integrity_findings(
    records: list[tuple[int, list[int], str, bool, bool]], register: str, *, ceiling: int | StoreScope | None = None
) -> list[str]:
    """One grouped finding per PR whose rows in ``register`` break the one-canonical-row rule.

    With a ``ceiling`` (an integer or the shared ``StoreScope``), a row the shared decision
    defers is set aside WHOLE, before grouping; a row naming any protected PR is kept whole and
    counts under every key it names.
    """
    by_pr: dict[int, list[tuple[int, str, bool, bool]]] = {}
    for lineno, prs, kind, companion, pending in records:
        if above_store_ceiling(prs, ceiling):
            continue
        for pr in prs:
            by_pr.setdefault(pr, []).append((lineno, kind, companion, pending))
    findings: list[str] = []
    for pr in sorted(by_pr):
        rows = by_pr[pr]
        if len(rows) == 1:
            if rows[0][2]:
                findings.append(
                    f"  [row-integrity] PR #{pr}: {register} line {rows[0][0]} is a companion "
                    f"(iteration/addendum) row with no canonical row for the PR."
                )
            continue
        lines = ", ".join(str(r[0]) for r in rows)
        canonical = [r for r in rows if not r[2]]
        ordinary = [r for r in canonical if not r[1]]
        exempt = [r for r in canonical if r[1]]
        reasons: list[str] = []
        if any(r[3] for r in rows):
            reasons.append("a pending/IN-PROGRESS row coexists with another row (upsert it instead)")
        if len(ordinary) > 1:
            reasons.append(f"{len(ordinary)} canonical rows (keep one; mark earlier rounds 'iteration' or 'addendum')")
        if len(exempt) > 1:
            reasons.append(f"{len(exempt)} exemption rows (consolidate into one disposition)")
        if not canonical:
            reasons.append("only companion rows, no canonical row")
        if reasons:
            findings.append(f"  [row-integrity] PR #{pr}: {register} lines {lines}: " + "; ".join(reasons) + ".")
    return findings


def _deferred_prs(records: list[tuple[int, list[int], str, bool, bool]], ceiling: int | StoreScope | None) -> set[int]:
    """PRs named by rows eligible for deferral under the shared scope."""
    return {pr for _lineno, prs, *_rest in records if above_store_ceiling(prs, ceiling) for pr in prs}


def _deferred_mirror_prs(detailed_text: str, ceiling: int | StoreScope | None) -> set[int]:
    """PRs deferred by the same mirror flags as the provenance check."""
    out: set[int] = set()
    for deferred, prs in store_deferral_flags(detailed_text.split("\n"), ceiling):
        if deferred:
            out.update(prs)
    return out


BYPASS_ROW_PR = re.compile(r"^\|[^|]*\|\s*#(\d+)\s*\|")
BYPASS_LOG_REL = "merge-bypass-log.md"


def parse_bypass_prs(text: str) -> set[int]:
    """The set of PR numbers carrying a merge-bypass-log row."""
    prs: set[int] = set()
    for line in text.splitlines():
        m = BYPASS_ROW_PR.match(line)
        if m:
            prs.add(int(m.group(1)))
    return prs



# --- 3b145 online own-PR verification (maintainer ruling 2026-10-01 12:49Z) ---------------
# VERIFY ONLINE, FAIL CLOSED. The Check 6 own-PR exemption is the one place this gate drops a
# row demand, and offline evidence can prove a declaration NEW but never that the PR is still
# UNMERGED: a stale origin/main lets an already-merged PR declare (round-1 codex R1 / claude
# F1), which is the 2026-08-10 failure shape again. So the exemption is granted only after
# `gh pr view` confirms, live, that the declared PR is OPEN and that its head branch is THIS
# branch. The project has no shared gh helper (detect-env.py, audit-validation-coverage.py and
# check-clean-language-upstream.py each carry a tool-local subprocess seam), so this follows
# the same per-tool pattern with one injectable runner, `_gh_runner`.
GH_PR_VIEW_TIMEOUT = 10  # seconds; the ruling's "short bounded timeout"

# Host AND owner/repo from the origin remote URL (round-2 codex R2-02 / claude F2: the old
# last-two-segments parse, the audit-validation-coverage.py `owner_repo` pattern, dropped
# the host, so a GHE, GitLab or local-path origin mapped to the SAME-NAMED github.com
# repository and gh verified the wrong repository's PR). Only a github.com remote
# qualifies -- the one host this repository's gh is configured for -- in the two shapes
# git uses for it: a scheme URL (https/ssh/git, optional userinfo, NO port: a port names
# a different endpoint) and the scp-like `[user@]github.com:owner/repo`. `.git` is
# tolerated. Anything else (another host, a port, a path or file: remote, an unparsable
# URL) fails closed: the demand is kept and the reason printed.
_ORIGIN_GITHUB_RE = re.compile(
    r"^(?:(?:https|ssh|git)://(?:[^/@\s]+@)?github\.com/"
    r"|(?:[^@/\s:]+@)?github\.com:)"
    r"(?P<owner>[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)/"
    r"(?P<repo>[A-Za-z0-9._-]+?)(?:\.git)?/?$",
    re.IGNORECASE,
)


class _DuplicateJSONKey(ValueError):
    """A gh JSON document carried the same key twice (round-2 codex R2-03): plain
    ``json.loads`` silently keeps the LAST value, so a document saying both MERGED and
    OPEN reads OPEN. Under the ruling's any-uncertainty contract a conflicting document
    is refused, keeping the demand."""


def _refuse_duplicate_json_keys(pairs):
    """``object_pairs_hook`` building each JSON object while refusing duplicate keys,
    at every nesting depth (round-2 codex R2-03)."""
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise _DuplicateJSONKey(f"duplicate JSON key {key!r}")
        obj[key] = value
    return obj

# The SINGULAR root header forms (round-1 codex R2): the compact `**date | version | PR #N**`
# cell and the legacy `## date, Library Version X, PR #N` line, each labelled singular `PR`
# (never `PRs`) and naming exactly one number with nothing else in the cell. A weekly roll-up
# (`**Week of ... (PRs #N)**`) or a range (`PRs #N-#N (1 PRs)`) can parse to a single PR, and
# `own_pr_declaration` accepts either, but neither is the singular form the declaration
# contract states, so neither ever carries the Check 6 exemption. The legacy alternative is
# strict to end-of-line (any tail fails closed); the live declaring form is the compact one.
SINGULAR_OWN_HEADER_RE = re.compile(
    r"^(?:##[ \t]+\d{4}-\d{2}-\d{2},\s+Library Version\s+[0-9.]+,\s+(?i:PR)[ \t]+#(?P<a>\d+)\s*$"
    r"|\*\*\d{4}-\d{2}-\d{2} \| [0-9.]+ \| (?i:PR) #(?P<b>\d+)\*\*)"
)


def own_pr_singular_header(changelog_text: str, own_pr: int) -> bool:
    """True when ``own_pr``'s root header uses a SINGULAR form (codex R2, fail closed).

    When a declaration exists, exactly one root header names the own PR (a second new header
    naming it would have made the declaration ambiguous, and a merge-base or origin/main
    header naming it would have blocked it), so finding any singular header naming ``own_pr``
    tests exactly the declaring line.
    """
    for line in changelog_text.splitlines():
        match = SINGULAR_OWN_HEADER_RE.match(line)
        if match and int(match.group("a") or match.group("b")) == own_pr:
            return True
    return False


def _gh_runner(argv: list[str], *, timeout: float, env: dict[str, str] | None = None):
    """The injectable process seam for the online verification and its two local git reads.

    Tests replace this module attribute (or pass ``runner=``) with a scripted stand-in, so
    they never run git or gh and never touch the network; the live gate uses the real
    subprocess. Resolved at call time, so a patched module attribute takes effect. ``env``
    is handed to the subprocess unchanged (``None`` inherits); the gh call passes a copy
    of this process's environment with ``GH_HOST`` pinned to github.com (round-3 codex
    R3-01 / claude F1).
    """
    return subprocess.run(argv, capture_output=True, text=True, timeout=timeout, env=env)


def verify_own_pr_open(own_pr: int, *, runner=None) -> tuple[bool, str]:
    """(True, "") only when gh confirms ``own_pr`` OPEN, headed by THIS branch of THIS repo.

    The ruling's online check: ``gh pr view <N> --repo github.com/<owner>/<repo> --json
    state,headRefName,isCrossRepository,headRepositoryOwner,headRepository,url``, bounded
    by ``GH_PR_VIEW_TIMEOUT`` and pointed at the github.com origin repository THREE ways
    (round-3 codex R3-01 / claude F1: a hostless ``--repo owner/repo`` resolves against
    gh's DEFAULT host, which ``GH_HOST`` can repoint at an enterprise server carrying a
    same-named repository, and none of the identity fields names a host): the ``--repo``
    argument carries the host explicitly (gh's HOST/OWNER/REPO form), the gh subprocess
    runs with ``GH_HOST=github.com`` set over a copy of this process's environment, and
    the answer's ``url`` must begin ``https://github.com/<owner>/<repo>/pull/<N>``, the
    one returned field that names a host. FAIL CLOSED, exhaustively: an unreadable
    current branch, a detached HEAD, an unreadable origin URL, an origin that is not a
    parsable github.com remote (round-2 codex R2-02 / claude F2), a missing gh binary, a
    gh non-zero exit (auth, network, API, unknown PR), a timeout, unparsable or
    incomplete JSON, duplicate or conflicting JSON keys (round-2 codex R2-03), a state
    other than OPEN, a cross-repository (fork) PR or a head repository other than the
    origin repository itself (round-2 codex R2-01 / claude F1: ``headRefName`` is a bare
    branch name naming no repository, so a fork PR with the same branch name must keep
    the demand), a PR url under any other host, repository or number (round-3 codex
    R3-01), and a head branch other than the current branch each return ``(False, why)``,
    and the caller keeps the row demand and prints why. So does ANY exception the checks
    raise (round-3 claude F4: a RecursionError from hostile JSON nesting, a
    UnicodeDecodeError or ValueError from the runner): the backstop here converts it to
    the same printed refusal instead of a crash. Nothing is cached: the answer is only as
    good as the moment it was given, which is why the caller runs this lazily, at the
    moment the exemption would bite.
    """
    try:
        return _verify_own_pr_open(own_pr, runner=runner)
    except Exception as exc:  # the any-uncertainty contract: a crash never answers
        detail = " ".join(str(exc).split())[:160]
        return False, (f"the online check raised {exc.__class__.__name__}"
                       + (f" ({detail})" if detail else "")
                       + "; an exception is uncertainty, so it is refused like any "
                         "other online failure (round-3 claude F4)")


def _verify_own_pr_open(own_pr: int, *, runner=None) -> tuple[bool, str]:
    """The checks behind ``verify_own_pr_open``, whose backstop turns any exception
    raised here into a kept demand with a printed reason (round-3 claude F4)."""
    if runner is None:
        runner = _gh_runner
    try:
        branch_proc = runner(["git", "-C", str(REPO_ROOT), "rev-parse", "--abbrev-ref", "HEAD"],
                             timeout=GH_PR_VIEW_TIMEOUT)
        url_proc = runner(["git", "-C", str(REPO_ROOT), "remote", "get-url", "origin"],
                          timeout=GH_PR_VIEW_TIMEOUT)
    except subprocess.TimeoutExpired:
        return False, "a local git read (current branch / origin URL) did not answer in time"
    except OSError as exc:
        return False, f"a local git read could not run ({exc.__class__.__name__})"
    if branch_proc.returncode != 0:
        return False, "the current branch could not be read (git rev-parse failed)"
    branch = branch_proc.stdout.strip()
    if not branch or branch == "HEAD":
        return False, "HEAD is detached, so no current branch can match the PR's head branch"
    if url_proc.returncode != 0:
        return False, "the origin remote URL could not be read (git remote get-url failed)"
    url = url_proc.stdout.strip()
    match = _ORIGIN_GITHUB_RE.match(url)
    if not match:
        return False, (f"the origin remote URL {url!r} is not a parsable github.com "
                       f"<owner>/<repo> remote, the only host gh is configured for here; "
                       f"any other or unparsable host fails closed")
    owner, repo_name = match.group("owner"), match.group("repo")
    repo = f"{owner}/{repo_name}"
    # Round-3 codex R3-01 / claude F1: the destination host is pinned in the --repo
    # argument AND in the subprocess environment, because a hostless --repo falls back
    # to gh's default host and GH_HOST can repoint that default at another server
    # carrying a same-named repository, whose same-numbered OPEN PR would then pass
    # every identity check below (none of those fields names a host).
    gh_env = dict(os.environ)
    gh_env["GH_HOST"] = "github.com"
    try:
        gh_proc = runner(["gh", "pr", "view", str(own_pr), "--repo",
                          f"github.com/{repo}", "--json",
                          "state,headRefName,isCrossRepository,headRepositoryOwner,"
                          "headRepository,url"], timeout=GH_PR_VIEW_TIMEOUT, env=gh_env)
    except FileNotFoundError:
        return False, "gh is not available (not installed or not on PATH)"
    except subprocess.TimeoutExpired:
        return False, f"gh pr view #{own_pr} did not answer within {GH_PR_VIEW_TIMEOUT}s"
    except OSError as exc:
        return False, f"gh pr view #{own_pr} could not run ({exc.__class__.__name__})"
    if gh_proc.returncode != 0:
        detail = " ".join((gh_proc.stderr or "").split())[:160] or "no detail"
        return False, f"gh pr view #{own_pr} failed (exit {gh_proc.returncode}: {detail})"
    try:
        data = json.loads(gh_proc.stdout, object_pairs_hook=_refuse_duplicate_json_keys)
    except _DuplicateJSONKey as exc:
        return False, (f"gh pr view #{own_pr} returned JSON carrying a {exc} "
                       f"(conflicting answers are refused, round-2 codex R2-03)")
    except json.JSONDecodeError:
        return False, f"gh pr view #{own_pr} returned unparsable output"
    try:
        state, head = data["state"], data["headRefName"]
        cross = data["isCrossRepository"]
        head_owner, head_repo = data["headRepositoryOwner"], data["headRepository"]
        pr_url = data["url"]
    except (KeyError, TypeError):
        return False, f"gh pr view #{own_pr} returned unparsable output"
    if not isinstance(state, str) or not isinstance(head, str) or not isinstance(pr_url, str):
        return False, f"gh pr view #{own_pr} returned unparsable output"
    if state != "OPEN":
        return False, f"gh reports PR #{own_pr} state {state}, not OPEN"
    if cross is not False:
        return False, (f"gh does not certainly deny that PR #{own_pr} is a cross-repository "
                       f"(fork) PR (isCrossRepository must be exactly false); a fork's branch "
                       f"can share this branch's name, so it never carries the exemption")
    login = head_owner.get("login") if isinstance(head_owner, dict) else None
    name = head_repo.get("name") if isinstance(head_repo, dict) else None
    if not isinstance(login, str) or not isinstance(name, str):
        return False, f"gh pr view #{own_pr} returned unparsable output"
    # GitHub owner and repository names are case-insensitive identifiers, so the fold
    # tolerates a differently-cased clone URL without admitting any other repository.
    if login.lower() != owner.lower() or name.lower() != repo_name.lower():
        return False, (f"gh reports PR #{own_pr} head repository {login}/{name}, not the "
                       f"origin repository {repo} itself; a same-name fork branch never "
                       f"carries the exemption")
    # The one returned field that names a HOST (round-3 codex R3-01): the identity
    # fields above pin owner, name and branch, but would match a same-named repository
    # on whichever server gh answered from. The case fold mirrors the identity fold;
    # the digit boundary stops a PR number sharing these digits as a prefix (#26510
    # for #2651) from matching.
    expected = f"https://github.com/{repo}/pull/{own_pr}"
    if (not pr_url.lower().startswith(expected.lower())
            or pr_url[len(expected):len(expected) + 1].isdigit()):
        return False, (f"gh reports PR #{own_pr} url {pr_url!r}, not {expected} on "
                       f"github.com itself; an answer about any other host, repository "
                       f"or PR never carries the exemption (round-3 codex R3-01)")
    if head != branch:
        return False, f"gh reports PR #{own_pr} head branch {head!r}, not this branch {branch!r}"
    return True, ""


def check6_own_pr_exemption(changelog_text: str, own_pr: int, *, runner=None) -> tuple[bool, str]:
    """The complete 3b145 exemption test: singular header form first (offline, codex R2),
    then the online OPEN-on-this-branch-of-this-repo verification. ``main`` passes this
    to ``bypass_log_findings`` as ``verify``; any ``(False, why)`` keeps the row demand."""
    if not own_pr_singular_header(changelog_text, own_pr):
        return False, ("its declaring root header is not the SINGULAR form (a weekly roll-up "
                       "or a range header can parse to one PR but never carries the exemption)")
    return verify_own_pr_open(own_pr, runner=runner)


def bypass_log_findings(
    changelog_prs: set[int],
    bypass_prs: set[int],
    *,
    inception: int = INCEPTION,
    own_pr: int | None = None,
    verify: Callable[[int], tuple[bool, str]] | None = None,
) -> list[str]:
    """Check 6: every in-window merged PR has a merge-bypass-log row.

    WHY THIS IS A GATE AND NOT A CONVENTION. The project CLAUDE.md already states that an unlogged
    bypass merge is a discipline failure, because branch protection here requires an approval that a
    solo-authored PR never receives, so every merge goes through the maintainer's always-on
    `--admin` bypass. That bypass is invisible when used, and the log is the only thing converting
    it from an unaudited hole into a recorded exception. The convention alone did not hold: on
    2026-07-25 FIVE consecutive merges (#1170 to #1174) shipped with no row, unnoticed until the log
    was read for an unrelated reason. Five recurrences in one day is past the point where a
    convention is the right control.

    Check 6 EXCLUDES the highest-numbered PR as in-flight: its bypass-log row records a POST-merge
    fact (whether the merge used `--admin`), unknowable before merge, so demanding it here would make
    every PR fail its own gate. This differs from Check 1, which after the 3.137b synchronous cutover
    INCLUDES the highest PR (its QA rows are written pre-merge in its own PR). And the
    floor is the register's own oldest row, so a log that starts partway through history is not
    retroactively in breach.

    The same post-merge-fact logic exempts the branch's DECLARED OWN PR (``own_pr``) even when it
    is NOT the highest number (3b145): a rebased branch carries the headers of PRs that merged
    after its own was opened, so its own unmerged PR falls below ``max_pr`` and this check would
    demand a row its own text forbids writing before the merge is observed (PR #2653 under merged
    #2654-#2665, superseded by #2666 just to get past this gate). The caller passes ``own_pr``
    ONLY when ``lint_common.own_pr_declaration`` is certain; and since the VERIFY ONLINE / FAIL
    CLOSED ruling (2026-10-01 12:49Z) the demand is dropped only after ``verify`` -- the complete
    3b145 exemption test, ``check6_own_pr_exemption`` in ``main`` -- returns ``(True, "")`` for
    that PR: the declaring root header is the SINGULAR form (never a roll-up or range, codex R2)
    and ``gh pr view`` reports the PR OPEN with THIS branch as its head and the github.com
    origin repository itself as its head repository, never a fork (round-2 codex R2-01 /
    claude F1). ``verify`` runs lazily,
    exactly when the exemption would bite (the own PR is in-window with no row), so a run that
    needs no exemption makes no online call; any ``(False, why)`` keeps the demand and prints
    why. ``verify=None`` means the caller attests the verification already happened (the
    direct-call test seam); ``main`` always passes the real verifier. Exactly one PR is ever
    exemptable, and both the skip and a refusal print a note, so the residue is LOUD, never
    silent. That is deliberately NOT a claim that the 2026-08-10 failure class (an
    origin/main-keyed guard whose stale offline evidence silently deleted the row demand for
    eight recently-merged PRs, removed for it) is impossible here, only that it is now bounded
    and visible: one PR at most, verified against the live PR state, and demanded again the
    moment the online check cannot positively confirm it OPEN on this branch.

    A row is satisfied by its PRESENCE, whatever its Mechanism cell says. That is deliberate: if a
    future protection change makes a plain merge succeed, the honest record is a row saying so, and
    this check must not force the mechanism to keep reading `--admin` to stay green.
    """
    findings: list[str] = []
    if not changelog_prs:
        return findings
    if not bypass_prs:
        # NO-OP, not a storm. An empty or absent log has no oldest row to anchor a floor on, so the
        # window would open at INCEPTION and flag every PR in the corpus's history. That is useless
        # as a signal and actively hostile to an adopter fork, which the project CLAUDE.md says may
        # delete `.working/` outright. Silence here is the honest answer: with no rows there is
        # nothing to be in parity WITH.
        return findings
    max_pr = max(changelog_prs)
    floor = effective_floor(bypass_prs, floor=inception)
    # The out-of-order residue, scoped to what the own-PR exemption cannot cover. A PR below
    # max_pr is ASSUMED merged, and PRs do not merge in number order. On `main` this is inert: an
    # unmerged PR has no CHANGELOG entry there, so it never enters this universe. It bites on a
    # PR's OWN BRANCH, where its entry does exist (#1471 under merged #1472; #2653 under merged
    # #2654-#2665): the branch's own declared PR is exempted below, but ONLY once `verify`
    # confirms the exemption (3b145, ruling 2026-10-01 12:49Z). Any OTHER unmerged PR's entry
    # carried here (a stacked branch's second open entry, a never-merged number inside an
    # unbroken weekly range that KNOWN_SKIPPED_PRS has not recorded) still false-positives
    # LOUDLY, deliberately: a guard keyed on `origin/main` was built for this and REMOVED on
    # 2026-08-10, because a stale remote-tracking ref passed every precondition it could check
    # locally and silently deleted the row demand for eight recently-merged PRs. Dropping a
    # demand is the exact failure this check exists to catch, so beyond the one ONLINE-VERIFIED
    # PR the branch itself declares, the loud false positive stays the better trade.
    for pr in sorted(p for p in changelog_prs if floor <= p < max_pr):
        if pr in bypass_prs:
            continue
        if pr == own_pr:
            ok, why = (True, "") if verify is None else verify(pr)
            if ok:
                print(
                    f"note: [bypass-log] PR #{pr} is this branch's declared own PR, below the "
                    f"window ceiling #{max_pr} because later-merged PRs' headers sit above it; "
                    f"its row records a post-merge fact, so the demand is exempt here (3b145"
                    + (", verified OPEN on this branch via gh" if verify is not None else "")
                    + ") and falls due the moment the merge is observed."
                )
                continue
            print(
                f"note: [bypass-log] PR #{pr} is this branch's declared own PR, but the 3b145 "
                f"exemption is withheld: {why}. Fail closed (VERIFY ONLINE ruling 2026-10-01 "
                f"12:49Z): the row demand stands and the finding below is deliberate."
            )
        findings.append(
            f"  [bypass-log] PR #{pr}: no row in {BYPASS_LOG_REL}. Every merged PR in "
            f"[{floor}, {max_pr}) needs one, because protection requires an approval a "
            f"solo-authored PR never gets, so the merge went through the always-on `--admin` "
            f"bypass and the row is the only record that it did. Add the row from the OBSERVED "
            f"pre-merge CI state, never in anticipation of a merge.")
    return findings


def effective_floor(present_prs: set[int], *, floor: int = INCEPTION) -> int:
    """The dynamic Check-1 floor: ``max(INCEPTION, oldest surviving row)``.

    The dated-archive sweep (1.19.9 (closing PR #1034)) moves AGED roll-up rows out
    of the in-repo history registers (``validate-pr/history.md`` and
    ``improvement-log.md``) to ``grc_library_private``, keeping each register
    to a recent window (the gate-59 current-week model applied to the
    registers). The root ``CHANGELOG.md`` (the universe set Check 1 iterates)
    keeps EVERY PR, so once a register's old rows are swept this floor rises to
    that register's oldest SURVIVING row and a swept-out PR falls below it,
    correctly out of scope rather than flagged as a missing row. The floor
    never drops below ``INCEPTION``; before any sweep the oldest surviving row
    is far below it (validate-pr rows begin #183, retro rows #213), so the
    floor is ``INCEPTION`` and behaviour is identical to the pre-sweep
    fixed-constant gate. Per-register (not one combined floor): the two
    registers sweep independently, so their oldest surviving rows can differ;
    a combined floor would keep the higher-floored register in scope below its
    own oldest row and re-introduce false missing-row findings.
    """
    return dynamic_floor(present_prs, floor)


def qa_cadence_findings(
    changelog_prs: set[int],
    vp_status: dict[int, str],
    retro_prs: set[int],
    *,
    inception: int = INCEPTION,
    known_handoff: frozenset[int] = KNOWN_HANDOFF_NO_ROW,
) -> list[str]:
    """Check 1: every in-window substantive PR has its validate-pr + retro rows."""
    findings: list[str] = []
    if not changelog_prs:
        return ["  [qa-cadence] CHANGELOG.md has no parseable PR headers."]
    max_pr = max(changelog_prs)
    # Dynamic per-register floors (1.19.9 (closing PR #1034)): a row swept to
    # grc_library_private drops below its register's floor and is out of scope,
    # not flagged missing. Before any sweep both floors equal INCEPTION.
    vp_floor = effective_floor(set(vp_status), floor=inception)
    retro_floor = effective_floor(retro_prs, floor=inception)

    for pr in sorted(p for p in changelog_prs if inception <= p <= max_pr):
        if pr in known_handoff:
            continue
        st = vp_status.get(pr)
        if st is None:
            if pr < vp_floor:
                # Older than the oldest surviving validate-pr row: its row was
                # swept to grc_library_private (PR #1034), so out of scope.
                continue
            findings.append(
                f"  [qa-cadence] PR #{pr}: no row in {VALIDATE_PR_HISTORY}. "
                f"Every merged PR in [{inception}, {max_pr}] needs a "
                f"/validate-pr row (or a handoff/subsumption exemption row). "
                f"If this is a session-closing handoff PR predating the "
                f"exemption-row convention, add it to KNOWN_HANDOFF_NO_ROW."
            )
            continue
        if st in ("handoff", "subsumption"):
            # Handoff: both rows legitimately absent. Subsumption: validate-pr
            # satisfied by the note row, no retro required.
            continue
        if st == "pending":
            # Third state (3.120 (closing PR #1210)): the row is PRESENT but marks the QA as
            # DISPATCHED / RESULT-PENDING and never RETURNED. Row presence alone used
            # to read GREEN here, so a stranded QA order (validate-pr-1173/1180) passed
            # while the PR's QA had never run. This PR is in-window (the window includes the current highest PR),
            # so the order is stranded: FAIL until the result RETURNS.
            findings.append(
                f"  [qa-cadence] PR #{pr}: its /validate-pr row is PRESENT but marks the "
                f"QA as DISPATCHED / RESULT-PENDING and it never RETURNED (window through "
                f"#{max_pr}), so the QA order is stranded. Consume "
                f"the result, update the row to RETURNED with its findings dispositioned, "
                f"or re-issue the order (per the undelivered-validate-pr-is-blocking rule)."
            )
            continue
        # Normal substantive PR: validate-pr row present; require the retro row
        # unless it is older than the oldest surviving retro row (swept out).
        if pr not in retro_prs and pr >= retro_floor:
            findings.append(
                f"  [qa-cadence] PR #{pr}: has a /validate-pr row but no "
                f"/retro row in {IMPROVEMENT_LOG}. A substantive PR records "
                f"its /retro row in the same PR; it "
                f"is missing here."
            )
    return findings


def todo_rotation_findings(todo_text: str) -> list[str]:
    """Check 2: no self-completion marker on a TODO backlog bullet."""
    findings: list[str] = []
    for lineno, line in enumerate(todo_text.splitlines(), 1):
        despanned = CODE_SPAN.sub("", line)
        hit: str | None = None
        for label, pattern in TODO_BULLET_START_MARKERS:
            if pattern.search(line):
                hit = label
                break
        if hit is None:
            for label, pattern in TODO_DESPANNED_MARKERS:
                if pattern.search(despanned):
                    hit = label
                    break
        if hit is not None:
            findings.append(
                f"  [todo-rotation] {TODO_PATH}:{lineno} carries a "
                f"self-completion marker ({hit}): a closed item must be "
                f"DELETED from TODO in this PR and rotated to the private-sibling "
                f"DONE ledger (cross-repo), not annotated in place. Line: {line.strip()[:100]}"
            )
    return findings


def discover_version_history_files() -> list[tuple[str, str]]:
    """Every tracked .md file carrying BOTH a metadata Version field and a
    ``## Version history`` table, skipping the standard exempt dirs.

    The discovery is repo-wide (not the audited-domain run) because the
    files that carry a ``## Version history`` table live in the pack dir,
    outside the corpus domains; it skips ``DEFAULT_EXEMPT_DIRS`` (``.git``,
    ``node_modules``, ``__pycache__``, ``.claude``, ``.working``, ``references``) rather than
    enumerating the audited domains, so it does not duplicate the
    ``AUDITED_DOMAIN_DIRS`` run (gate 52).
    """
    out: list[tuple[str, str]] = []
    for path in sorted(REPO_ROOT.rglob("*.md")):
        if is_default_exempt_root(path, repo_root=REPO_ROOT):
            continue
        rel = path.relative_to(REPO_ROOT)
        # Test scratch (tests/tmp) holds transient fixtures, not corpus; a
        # chmod-0 fixture .md there (e.g. the claude-rules-sync synthetic tree)
        # would crash the raw rglob read (gate-37 defence-in-depth fix 2).
        if rel.parts[:2] == ("tests", "tmp"):
            continue
        if any(part in DEFAULT_EXEMPT_DIRS for part in rel.parts):
            continue
        text = read_text_safe(path)
        if text is None:
            continue
        if METADATA_VERSION.search(text) and VERSION_HISTORY_HEADING.search(text):
            out.append((str(rel), text))
    return out


def version_history_parity_findings(files: list[tuple[str, str]]) -> list[str]:
    """Check 4: a file's metadata Version must appear as a row in its own
    ``## Version history`` table.

    Precision-first / FP-free: flag ONLY a metadata Version with no matching
    history row. History rows with no current metadata match (the normal
    historical rows) are tolerated.
    """
    findings: list[str] = []
    for rel, text in files:
        mv = METADATA_VERSION.search(text)
        vh = VERSION_HISTORY_HEADING.search(text)
        if not (mv and vh):
            continue
        meta_version = mv.group(1)
        # Restrict to the Version history section (heading to the next H2 / EOF).
        section = text[vh.end():]
        nxt = re.search(r"^##\s+", section, re.MULTILINE)
        if nxt:
            section = section[: nxt.start()]
        history_versions: set[str] = set()
        for line in section.splitlines():
            if not line.lstrip().startswith("|"):
                continue
            for cell in (c.strip() for c in split_markdown_row(line)):
                if VERSION_TOKEN.match(cell):
                    history_versions.add(cell)
        if meta_version not in history_versions:
            findings.append(
                f"  [version-history-parity] {rel}: metadata Version "
                f"{meta_version} has no matching row in the file's "
                f"## Version history table. When the metadata Version is "
                f"bumped, add the paired version-history row in the same "
                f"commit (the #372 paired-surface miss)."
            )
    return findings


def register_row_order_findings(register_text: str) -> list[str]:
    """Check 5: the deep-assessment run register's run-table rows must appear in
    strictly ascending run-number order (r1, r2, r3 ...).

    Precision-first / FP-free: flag ONLY a run row whose number is not greater
    than the previous run row's. The register is a low-churn ledger whose
    sibling structured-bookkeeping files ARE gated (the detailed mirror by gate
    59, the lease by gate 63) while it was not; this closes that one-of-a-pair
    gap (the r3 guardrail-review G3 finding; #888 mis-ordered a row and it
    reached main, caught by /validate-pr). An empty or register-less
    input yields no findings (a fork without the register is not a defect).
    """
    findings: list[str] = []
    prev_n: int | None = None
    for line in register_text.splitlines():
        m = REGISTER_RUN_ROW.match(line)
        if not m:
            continue
        n = int(m.group(1))
        if prev_n is not None and n <= prev_n:
            findings.append(
                f"  [register-row-order] {DEEP_ASSESSMENT_REGISTER}: run r{n} "
                f"row appears after r{prev_n}; the run-table must be in strictly "
                f"ascending run-number order (the #888 mis-order class)."
            )
        prev_n = n
    return findings


WORKER_PROVENANCE_RE = re.compile(
    r"^(?:[-*][ \t]+)?\*\*Worker provenance:\*\*(.*)$", re.MULTILINE
)

INBOX_PATH_RE = re.compile(r"\binbox/[A-Za-z0-9._-]+/\S*")


def worker_provenance_findings(detailed_text: str, *, ceiling: int | StoreScope | None = None) -> list[str]:
    """Check 3 (active): worker-delivered-diff provenance attestation.

    A PR that applies a scratch-inbox worker delivery marks its
    detailed-mirror CHANGELOG entry with a ``**Worker provenance:**`` line
    naming the delivery path (``inbox/<worker-id>/...``, normally the
    ``MANIFEST.md``). This check validates each marker line's shape,
    whether written standalone or as a list bullet (``- **Worker
    provenance:** ...``, the mirror's natural authoring form): the
    same-line remainder must reference an ``inbox/<worker-id>/`` path so
    the attestation is traceable to the delivery (a value on a FOLLOWING
    line does not count; an empty remainder is a finding). It enforces presence and well-formedness,
    never the apply-time verification's semantic soundness; an unmarked
    worker application is free prose, guarded by the CLAUDE.md close-out
    checklist. Formerly a dormant stub; activated by the PR #612
    codification once the external-collaborator primitive (the scratch
    WORKER-ONBOARDING flow) and this marking convention both existed. See
    the "Bookkeeping-parity gate, pinned design" entry in
    the design-decisions record.

    Store scope: a marker is skipped only inside an entry the shared ``store_deferral_flags``
    defer (another open PR's in-flight entry, printed as a note by ``main``). Every other raw
    marker is checked, including markers in the preamble, the own entry, merged entries, and
    everything after an example delimiter or an unrecognized header.
    """
    findings: list[str] = []
    lines = detailed_text.split("\n")
    flags = store_deferral_flags(lines, ceiling)
    for line, (deferred, _scope_prs) in zip(lines, flags):
        match = WORKER_PROVENANCE_RE.match(line)
        if match is None:
            continue
        if deferred:
            continue
        value = match.group(1).strip()
        if not INBOX_PATH_RE.search(value):
            findings.append(
                f"worker-provenance marker does not name an "
                f"inbox/<worker-id>/ delivery path: `{value}`"
            )
    return findings


def main() -> int:
    # The five `.working/`-tree inputs route through resolve_working: it prefers
    # grc_library_private/.working/, falls back to the in-repo `.working/`, and
    # returns None when neither supplies the file (public CI / adopter clone).
    # Each private-dependent check then no-ops INDIVIDUALLY, so the two PUBLIC
    # checks (TODO/DONE rotation, version-history parity) run either way and the
    # gate keeps its full strength on the maintainer's machine.
    vp_path = resolve_working("validate-pr/history.md")
    retro_path = resolve_working("improvement-log.md")
    detailed_path = resolve_working("changelog-details/CHANGELOG-detailed.md")
    register_path = resolve_working("deep-assessment/register.md")
    bypass_path = resolve_working("merge-bypass-log.md")

    try:
        changelog_text = read(CHANGELOG_PATH)
        changelog = parse_changelog_prs(changelog_text) - KNOWN_SKIPPED_PRS
        todo_text = read(TODO_PATH)
        vp_text = vp_path.read_text(encoding="utf-8") if vp_path else None
        retro_text = retro_path.read_text(encoding="utf-8") if retro_path else None
        detailed_text = detailed_path.read_text(encoding="utf-8") if detailed_path else None
        register_text = register_path.read_text(encoding="utf-8") if register_path else None
        bypass_text = bypass_path.read_text(encoding="utf-8") if bypass_path else None
    except FileNotFoundError as exc:
        print(f"ERROR: required file missing: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"ERROR: file read failure: {exc}", file=sys.stderr)
        return 2

    all_findings: list[str] = []
    skipped: list[str] = []
    scope = store_scope(changelog_text)
    ceiling = scope
    if scope.note:
        print(f"note: {scope.note}")

    # Check 1 needs BOTH registers. With either absent, that register's
    # effective floor collapses to INCEPTION and EVERY in-window PR is flagged
    # as missing its row, so a half-run is a false-positive storm, not a weaker
    # check. Skip unless both are present.
    # GATE50-UNIQUE: row integrity runs on EACH register that is available (independently of
    # Check 1's both-registers requirement, so one absent register never hides duplicates in the
    # other), before the presence check.
    if vp_text is None and retro_text is None:
        skipped.append("per-PR row integrity")
    if vp_text is not None:
        vp_records = _history_row_records(vp_text)
        for lineno, prs, *_ in vp_records:
            if above_store_ceiling(prs, scope):
                print(store_deferral_note(prs, scope, "validate-pr/history.md", lineno))
        all_findings.extend(row_integrity_findings(vp_records, "validate-pr/history.md", ceiling=ceiling))
    if retro_text is not None:
        retro_records = _retro_row_records(retro_text)
        for lineno, prs, *_ in retro_records:
            if above_store_ceiling(prs, scope):
                print(store_deferral_note(prs, scope, "improvement-log.md", lineno))
        all_findings.extend(row_integrity_findings(retro_records, "improvement-log.md", ceiling=ceiling))

    if vp_text is None or retro_text is None:
        skipped.append(f"QA-cadence parity (from PR #{INCEPTION})")
    else:
        all_findings.extend(
            qa_cadence_findings(
                changelog,
                parse_validate_pr_status(vp_text),
                parse_retro_prs(retro_text),
            )
        )

    # Checks 2 and 4 read PUBLIC files only (TODO.md; the repo-wide
    # metadata/version-history pair), so they always run. Check 2 scans the
    # TODO.md index rows; per-item DETAIL now lives in the private
    # grc_library_private/TODO-REFERENCE.md (cross-repo, PR #1795), governed there.
    # gate 57 (lint-todo-marked-done.py) defaults to the public TODO.md only, so
    # this check is not widened.
    all_findings.extend(todo_rotation_findings(todo_text))
    vh_files = discover_version_history_files()
    all_findings.extend(version_history_parity_findings(vh_files))

    if detailed_text is None:
        skipped.append("worker-provenance attestation")
    else:
        lines = detailed_text.split("\n")
        flags = store_deferral_flags(lines, scope)
        for lineno, ((deferred, prs), line) in enumerate(zip(flags, lines), 1):
            if deferred and changelog_entry_boundary(line):
                print(store_deferral_note(prs, scope, "changelog-details/CHANGELOG-detailed.md", lineno))
        all_findings.extend(worker_provenance_findings(detailed_text, ceiling=ceiling))

    if register_text is None:
        skipped.append("deep-assessment register row-order")
    else:
        all_findings.extend(register_row_order_findings(register_text))

    if bypass_text is None:
        skipped.append("merge-bypass-log parity")
    else:
        # Check 6's one scope input (3b145; VERIFY ONLINE / FAIL CLOSED ruling 2026-10-01
        # 12:49Z): the declared own PR, passed only under the explicit open_rule guard.
        # store_scope sets own_pr only together with open_rule, so that guard is redundant by
        # construction; it stays explicit because the 2026-08-10 precedent (a stale input
        # silently deleting row demands) is exactly the failure an uncertain input reopens.
        # The demand is then dropped only after check6_own_pr_exemption passes for that PR:
        # the declaring root header is the SINGULAR form and gh verifies the PR OPEN on this
        # branch with the github.com origin repository itself as its head (never a fork),
        # called lazily at the moment the exemption would bite. Every failure keeps the
        # demand and prints why.
        all_findings.extend(bypass_log_findings(
            changelog, parse_bypass_prs(bypass_text),
            own_pr=scope.own_pr if scope.open_rule else None,
            verify=lambda pr: check6_own_pr_exemption(changelog_text, pr)))

    if skipped:
        print(
            f"OK: {len(skipped)} check(s) skipped, their input being maintainer-only "
            f"working state not present here ({'; '.join(skipped)}); public CI / "
            f"adopter clone."
        )

    if not all_findings:
        ran = [
            name
            for name in (
                "per-PR row integrity",
                f"QA-cadence parity (from PR #{INCEPTION})",
                "TODO/DONE rotation",
                "version-history parity",
                "worker-provenance attestation",
                "deep-assessment register row-order",
                "merge-bypass-log parity",
            )
            if name not in skipped
            and not (name == "version-history parity" and not vh_files)
        ]
        if not vh_files:
            print(
                "note: version-history parity scanned 0 files (no repo file pairs a "
                "**Version:** field with a ## Version history table); the check is "
                "vacuous here and is not asserted as a pass."
            )
        print(f"OK: bookkeeping-parity audit clean ({'; '.join(ran)}).")
        return 0

    print("=== bookkeeping-parity audit ===", file=sys.stderr)
    for f in all_findings:
        print(f, file=sys.stderr)
    print("", file=sys.stderr)
    print(
        f"FAIL: {len(all_findings)} bookkeeping-parity finding(s). "
        "The gate enforces the PRESENCE of the per-PR QA records and the "
        "TODO/DONE rotation the process mandates; see "
        "guardrails/governance/ai-assistant-workflow-disciplines.md "
        "and change-tracking.md for the conventions.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    # 3b50b2g: this tool takes no argument; an unknown or surplus one
    # used to be ignored with exit 0, so it is refused (exit 2) before the check runs.
    import os as _os
    sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    from lint_common import strict_flags as _strict_flags
    _strict_flags(sys.argv[1:], ())
    sys.exit(main())
