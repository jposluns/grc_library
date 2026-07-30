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

The five checks:

**Check 1, QA-cadence parity (the former §4.6 surface).** Derive the merged-PR
list from the ``CHANGELOG.md`` per-entry headers, matched in BOTH the compact
``**date | version | PR #N**`` form (the TODO 3.16 root-reformat default) and
the legacy ``## YYYY-MM-DD, Library Version X, PR #N`` form. For each PR N with ``max(INCEPTION, oldest surviving row) <= N < max(PR)``, require a row in
the PR-scoped validation history register AND (for substantive PRs) a row in
the improvement log, with these exemptions:

- EVERY merged PR, INCLUDING the single highest-numbered one, needs its own
  rows (PR #1248, the synchronous-``/validate-pr`` cutover): the QA now
  runs before the PR is finalized and its rows land in the SAME PR, so the
  window is inclusive of ``max_pr``. (The former highest-PR-in-flight exemption
  went with the retired recursion-avoidance batching.)
- A session-closing handoff PR is exempt from BOTH the validate-pr and the
  retro requirement (the loop-break: a handoff PR skips its own trailing
  QA). Handoff PRs are detected by their explicit validate-pr exemption row
  (the Findings cell contains ``SKIPPED`` together with ``handoff``, or the
  phrase ``handoff-PR exception``).
- A subsumption / maintainer-exception row (Findings cell contains
  ``SUBSUMED``, ``NOT run``, or a maintainer-authorised exception, in either
  the ``-ised`` or ``-ized`` spelling) satisfies
  the validate-pr requirement and does NOT require a retro row (#328 is the
  canonical instance: its QA was force-stopped and subsumed by Sweep 42).
- A THIRD row state, ``pending`` (TODO 3.120): a validate-pr row that is
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
  mirroring gate 59): the dated-archive sweep (TODO section 1.19.9) moves AGED
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

**Check 3, worker-provenance (ACTIVE since the section-3.6 codification).**
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
which is past the point where a convention is the right control. Same window as
Check 1 (highest PR exempt as in flight, floor at the register's own oldest row); a row
counts by PRESENCE whatever its Mechanism cell says, so a future protection change that
permits a plain merge is recorded honestly rather than forced to keep reading
`--admin`. An empty or absent log no-ops rather than flagging the whole history.

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

import re
import sys
from pathlib import Path

from lint_common import DEFAULT_EXEMPT_DIRS, read_text_safe, resolve_working

REPO_ROOT = Path(__file__).resolve().parent.parent

CHANGELOG_PATH = "CHANGELOG.md"
DETAILED_CHANGELOG_PATH = ".working/changelog-details/CHANGELOG-detailed.md"
VALIDATE_PR_HISTORY = ".working/validate-pr/history.md"
IMPROVEMENT_LOG = ".working/improvement-log.md"
TODO_PATH = "TODO.md"
DEEP_ASSESSMENT_REGISTER = ".working/deep-assessment/register.md"

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
KNOWN_HANDOFF_NO_ROW: frozenset[int] = frozenset({300, 322, 334})

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
SUBSUMPTION_FINDINGS = re.compile(
    r"SUBSUMED|NOT\s+run|maintainer[-\s]authori[sz]\w*",
    re.IGNORECASE,
)

# A row whose QA was DISPATCHED / offloaded but has NOT yet RETURNED, so the row is
# present-but-UNRESOLVED (TODO 3.120). Check 1 was satisfied by row PRESENCE, so an
# honest `DISPATCHED, RESULT PENDING` row read GREEN while the PR's QA had in fact never
# run: this is the stranded-QA hole that let validate-pr-1173 (`PENDING, offloaded`) and
# validate-pr-1180 (`DISPATCHED`) sit unconsumed across sessions. It is a THIRD state,
# between resolved-present and absent, and Check 1 FAILS on it once a later PR exists. A
# row that also carries RETURNED is NOT pending (it returned; the word may appear in its
# prose, e.g. "the order was dispatched at #1180 and never returned, now RETURNED").
PENDING_FINDINGS = re.compile(r"\bDISPATCHED\b|\bRESULT\s+PENDING\b|^\**\s*PENDING\b", re.IGNORECASE)
RETURNED_MARK = re.compile(r"\bRETURNED\b", re.IGNORECASE)

# A markdown table data row: leading pipe, an ISO date cell, then the rest.
TABLE_ROW = re.compile(r"^\|\s*\d{4}-\d{2}-\d{2}\s*\|")

# CHANGELOG entry header: `## YYYY-MM-DD, Library Version X.Y.Z, PR #N`,
# plus the compact form the TODO 3.16 root-reformat introduced
# (``**date | version | PR #N**``, optional ``- summary`` tail).
CHANGELOG_HEADER = re.compile(
    r"^##\s+\d{4}-\d{2}-\d{2},\s+Library Version\s+[0-9.]+,\s+PR\s+#(\d+)"
    r"|^\*\*\d{4}-\d{2}-\d{2} \| [0-9.]+ \| PR #(\d+)\*\*",
    re.MULTILINE,
)

# improvement-log PR column tolerates an optional leading `#` (mixed format:
# some rows `338`, others `#333`).
RETRO_ROW_PR = re.compile(r"^\|\s*\d{4}-\d{2}-\d{2}\s*\|\s*#?(\d+)")

# TODO/DONE rotation-failure markers on a backlog bullet (precision-first).
# Two precision levers keep this FP-free on the live TODO: (1) the
# strikethrough and checkbox markers must begin the bullet's CONTENT (a whole
# item struck through / checked off as done), so inline strikethrough used to
# mark completed sub-steps within a still-open item, e.g. FR-167's
# "~~risk 15~~ -> ~~dev-security 17~~" batch sequence, is not flagged; (2) the
# suffix / status / uppercase-SHIPPED markers are matched against the line
# with code-span (backtick) content removed, so the maintenance note that
# describes the convention ("no `[done]` suffixes") is not flagged.
CODE_SPAN = re.compile(r"`[^`]*`")

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


def cells(line: str) -> list[str]:
    """Split a markdown table row into stripped cells."""
    return [c.strip() for c in line.split("|")]


def parse_changelog_prs(text: str) -> set[int]:
    """The set of PR numbers that have a CHANGELOG entry header."""
    return {int(a or b) for a, b in CHANGELOG_HEADER.findall(text)}


def parse_validate_pr_status(text: str) -> dict[int, str]:
    """Map each PR with a validate-pr row to its status.

    Status is one of 'handoff', 'subsumption', or 'normal', classified from
    the row's Findings cell (field index 4). A PR cell may name more than one
    PR (a combined row such as `248, 249`); each named PR inherits the row's
    status.
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
        elif SUBSUMPTION_FINDINGS.search(findings):
            row_status = "subsumption"
        elif PENDING_FINDINGS.search(findings) and not RETURNED_MARK.search(findings):
            row_status = "pending"
        else:
            row_status = "normal"
        for pr in (int(x) for x in re.findall(r"\d+", c[2])):
            status[pr] = row_status
    return status


def parse_retro_prs(text: str) -> set[int]:
    """The set of PR numbers with an improvement-log (/retro) row."""
    prs: set[int] = set()
    for line in text.splitlines():
        m = RETRO_ROW_PR.match(line)
        if m:
            prs.add(int(m.group(1)))
    return prs


BYPASS_ROW_PR = re.compile(r"^\|[^|]*\|\s*#(\d+)\s*\|")
BYPASS_LOG_REL = ".working/merge-bypass-log.md"


def parse_bypass_prs(text: str) -> set[int]:
    """The set of PR numbers carrying a merge-bypass-log row."""
    prs: set[int] = set()
    for line in text.splitlines():
        m = BYPASS_ROW_PR.match(line)
        if m:
            prs.add(int(m.group(1)))
    return prs


def bypass_log_findings(
    changelog_prs: set[int],
    bypass_prs: set[int],
    *,
    inception: int = INCEPTION,
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
    for pr in sorted(p for p in changelog_prs if floor <= p < max_pr):
        if pr not in bypass_prs:
            findings.append(
                f"  [bypass-log] PR #{pr}: no row in {BYPASS_LOG_REL}. Every merged PR in "
                f"[{floor}, {max_pr}) needs one, because protection requires an approval a "
                f"solo-authored PR never gets, so the merge went through the always-on `--admin` "
                f"bypass and the row is the only record that it did. Add the row from the OBSERVED "
                f"pre-merge CI state, never in anticipation of a merge.")
    return findings


def effective_floor(present_prs: set[int], *, floor: int = INCEPTION) -> int:
    """The dynamic Check-1 floor: ``max(INCEPTION, oldest surviving row)``.

    The dated-archive sweep (TODO section 1.19.9) moves AGED roll-up rows out
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
    return max(floor, min(present_prs)) if present_prs else floor


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
    # Dynamic per-register floors (TODO section 1.19.9): a row swept to
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
                # swept to grc_library_private (section 1.19.9), so out of scope.
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
            # Third state (TODO 3.120): the row is PRESENT but marks the QA as
            # DISPATCHED / RESULT-PENDING and never RETURNED. Row presence alone used
            # to read GREEN here, so a stranded QA order (validate-pr-1173/1180) passed
            # while the PR's QA had never run. This PR is in-window (a later PR exists),
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
                f"DELETED from TODO and rotated to the DONE ledger in the "
                f"same PR, not annotated in place. Line: {line.strip()[:100]}"
            )
    return findings


def discover_version_history_files() -> list[tuple[str, str]]:
    """Every tracked .md file carrying BOTH a metadata Version field and a
    ``## Version history`` table, skipping the standard exempt dirs.

    The discovery is repo-wide (not the audited-domain run) because the
    files that carry a ``## Version history`` table live in the pack dir,
    outside the corpus domains; it skips ``DEFAULT_EXEMPT_DIRS`` (``.git``,
    ``node_modules``, ``__pycache__``, ``.claude``, ``.working``) rather than
    enumerating the audited domains, so it does not duplicate the
    ``AUDITED_DOMAIN_DIRS`` run (gate 52).
    """
    out: list[tuple[str, str]] = []
    for path in sorted(REPO_ROOT.rglob("*.md")):
        rel = path.relative_to(REPO_ROOT)
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
            for cell in (c.strip() for c in line.split("|")):
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


def worker_provenance_findings(detailed_text: str) -> list[str]:
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
    checklist. Formerly a dormant stub; activated by the section-3.6
    codification once the external-collaborator primitive (the scratch
    WORKER-ONBOARDING flow) and this marking convention both existed. See
    the "Bookkeeping-parity gate, pinned design" entry in
    the design-decisions record.
    """
    findings: list[str] = []
    for match in WORKER_PROVENANCE_RE.finditer(detailed_text):
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
        changelog = parse_changelog_prs(read(CHANGELOG_PATH))
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

    # Check 1 needs BOTH registers. With either absent, that register's
    # effective floor collapses to INCEPTION and EVERY in-window PR is flagged
    # as missing its row, so a half-run is a false-positive storm, not a weaker
    # check. Skip unless both are present.
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
    # metadata/version-history pair), so they always run.
    all_findings.extend(todo_rotation_findings(todo_text))
    all_findings.extend(version_history_parity_findings(discover_version_history_files()))

    if detailed_text is None:
        skipped.append("worker-provenance attestation")
    else:
        all_findings.extend(worker_provenance_findings(detailed_text))

    if register_text is None:
        skipped.append("deep-assessment register row-order")
    else:
        all_findings.extend(register_row_order_findings(register_text))

    if bypass_text is None:
        skipped.append("merge-bypass-log parity")
    else:
        all_findings.extend(bypass_log_findings(changelog, parse_bypass_prs(bypass_text)))

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
                f"QA-cadence parity (from PR #{INCEPTION})",
                "TODO/DONE rotation",
                "version-history parity",
                "worker-provenance attestation",
                "deep-assessment register row-order",
                "merge-bypass-log parity",
            )
            if name not in skipped
        ]
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
        "dev-security/claude-rules/governance/ai-assistant-workflow-disciplines.md "
        "and change-tracking.md for the conventions.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
