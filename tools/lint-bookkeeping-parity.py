#!/usr/bin/env python3
"""Post-merge bookkeeping-parity audit (gate 50).

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
also reads ``CHANGELOG.md`` plus the ``.working/`` history files. Unlike
gate 45, this gate parses committed file *content* (not the commit graph),
so it is a regular corpus gate that runs in ``run_all_audits.sh`` and the
three other audit surfaces; it is deliberately NOT added to the pre-push
history-aware runner (which is for delta and commit-graph gates), because
the post-commit ``run_all_audits.sh`` already runs it before any push.

The four checks:

**Check 1, QA-cadence parity (the former §4.6 surface).** Derive the merged-PR
list from the ``CHANGELOG.md`` per-entry headers, matched in BOTH the compact
``**date | version | PR #N**`` form (the TODO 3.16 root-reformat default) and
the legacy ``## YYYY-MM-DD, Library Version X, PR #N`` form. For each PR N with ``INCEPTION <= N < max(PR)``, require a row in
``.working/validate-pr/history.md`` AND (for substantive PRs) a row in
``.working/improvement-log.md``, with these exemptions:

- The single highest-numbered PR is exempt: its ``/validate-pr`` + ``/retro``
  rows legitimately batch into the *next* PR per the recursion-avoidance
  rule, which does not exist yet.
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
- A handful of pre-INCEPTION-era handoff PRs were merged before the
  exemption-row convention existed, so they carry no validate-pr row at all;
  they are listed in ``KNOWN_HANDOFF_NO_ROW`` so the gate does not
  false-positive on a legitimately-absent row.

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
[`.working/changelog-details/CHANGELOG-detailed.md`](../.working/changelog-details/CHANGELOG-detailed.md):
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
surface).** The deep-assessment run register
(``.working/deep-assessment/register.md``) lists its runs in strictly
ascending run-number order (r1, r2, r3 ...), but had no ordering check while
its sibling structured-bookkeeping files ARE gated (the detailed mirror by
gate 59, the concurrency lease by gate 63). This closes that one-of-a-pair
gap: flag ONLY a run row whose number is not greater than the previous run
row's (precision-first / FP-free; #888 mis-ordered a row and it reached main,
caught post-merge by /validate-pr). A register-less fork yields no findings.
Added as a fifth internal check of gate 50 (not a new numbered gate), the same
no-count-ripple precedent as Check 4.

Exit codes:
    0 - All present-and-rotated checks pass.
    1 - At least one missing record or rotation-failure marker detected.
    2 - Invocation or environment error (file read failure).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from lint_common import DEFAULT_EXEMPT_DIRS, read_text_safe

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

    for pr in sorted(p for p in changelog_prs if inception <= p < max_pr):
        if pr in known_handoff:
            continue
        st = vp_status.get(pr)
        if st is None:
            findings.append(
                f"  [qa-cadence] PR #{pr}: no row in {VALIDATE_PR_HISTORY}. "
                f"Every merged PR in [{inception}, {max_pr}) needs a "
                f"/validate-pr row (or a handoff/subsumption exemption row). "
                f"If this is a session-closing handoff PR predating the "
                f"exemption-row convention, add it to KNOWN_HANDOFF_NO_ROW."
            )
            continue
        if st in ("handoff", "subsumption"):
            # Handoff: both rows legitimately absent. Subsumption: validate-pr
            # satisfied by the note row, no retro required.
            continue
        # Normal substantive PR: validate-pr row present; require the retro row.
        if pr not in retro_prs:
            findings.append(
                f"  [qa-cadence] PR #{pr}: has a /validate-pr row but no "
                f"/retro row in {IMPROVEMENT_LOG}. A substantive PR's "
                f"post-merge retrospective row batches into the next PR; it "
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
                f"DELETED from TODO and rotated to .working/DONE.md in the "
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
    reached main, caught post-merge by /validate-pr). An empty or register-less
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
    .working/design-decisions.md.
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
    try:
        changelog = parse_changelog_prs(read(CHANGELOG_PATH))
        vp_status = parse_validate_pr_status(read(VALIDATE_PR_HISTORY))
        retros = parse_retro_prs(read(IMPROVEMENT_LOG))
        todo_text = read(TODO_PATH)
        detailed_text = read(DETAILED_CHANGELOG_PATH)
    except FileNotFoundError as exc:
        print(f"ERROR: required file missing: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"ERROR: file read failure: {exc}", file=sys.stderr)
        return 2

    all_findings: list[str] = []
    all_findings.extend(qa_cadence_findings(changelog, vp_status, retros))
    all_findings.extend(todo_rotation_findings(todo_text))
    all_findings.extend(version_history_parity_findings(discover_version_history_files()))
    all_findings.extend(worker_provenance_findings(detailed_text))
    # Fork-safe: a fork that keeps `.working/` but has never run /deep-assessment
    # may lack the register. read_text_safe re-raises FileNotFoundError (it catches
    # only decode errors), and this read is outside main()'s FileNotFoundError
    # guard, so guard the missing-file case explicitly -> no findings, no crash.
    register_path = REPO_ROOT / DEEP_ASSESSMENT_REGISTER
    register_text = read_text_safe(register_path) if register_path.is_file() else ""
    all_findings.extend(register_row_order_findings(register_text))

    if not all_findings:
        print(
            "OK: bookkeeping-parity audit clean "
            f"(QA-cadence parity from PR #{INCEPTION}; TODO/DONE rotation; "
            "version-history parity; worker-provenance attestation; "
            "deep-assessment register row-order)."
        )
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
