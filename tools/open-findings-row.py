#!/usr/bin/env python3
"""Write one finding row into the open-findings ledger, checked with the merge guard's own grammar (3b334).

WHY. Ledger rows were written by hand (the Edit tool, a subagent), so a row the merge guard reads
differently from its author's intent surfaced only at merge time: a disposition that looks closed but
fails the 3.126 grammar (`FIXED (d44d9b2b)`, `ROUTED pending-decisions`, `FIXED d44d9b2b`, the forms
recorded in mistakes register 95), an unescaped pipe that shifts the columns, or a FIXED class row with
no attestation. This tool checks one row BEFORE it is written, with the functions of
.claude/hooks/block-on-open-findings.py itself (loaded from this checkout by path, as
merge-when-green.py does), and writes it in place atomically. It defines no disposition, severity,
class or column grammar of its own, so it and the guard cannot disagree.

Usage:
    python3 -I tools/open-findings-row.py --id ID --after ANCHOR_ID [--ledger PATH] [--dry-run] [--open]
        [--delivery PATH [--source-key KEY]] < row
    python3 -I tools/open-findings-row.py --id ID --append [--ledger PATH] [--dry-run] [--open]
        [--delivery PATH [--source-key KEY]] < row
    python3 -I tools/open-findings-row.py --set-disposition --id ID [--ledger PATH] [--dry-run] < cell
    python3 -I tools/open-findings-row.py --self-test

ROW INPUT. Exactly one table line on stdin (UTF-8, at most one trailing LF), never in argv, so the row
text stays out of process listings. The output never carries row text or ids either: every mode,
refusals included, prints line numbers, verdict codes and counts only. The default ledger is
lint_common.resolve_working("open-findings.md", strict=True); --ledger overrides it. A missing ledger
is an error, never a fail-open.

FINDING ID. The leading bracketed token of the Finding cell (`[VPR3B330-PR8-R1] ...`), read with the
hook's own leading_class_token; --id must equal it without the brackets. A duplicate is that token
leading the Finding cell of any row the guard reads in `## Open` or `## Closed today`, or of any
unfenced finding-row-shaped line (the hook's MISFILED_ROW_RE) outside them, which covers the dated
archive below `## Closed today` and a mis-filed row above it. CONSEQUENCE, stated: the hook reads the
same leading token as a CLASS token (P-1.67), so a FIXED row owes a `[class: "<token>" @ <count>]` or
`[class-exempt: <reason>]` clause, and this tool refuses one without it, as D14 does.

PLACEMENT.
  --after ANCHOR_ID  after the one row the guard reads in `## Open` or `## Closed today` whose Finding
                     cell leads with [ANCHOR_ID] and whose severity is in the hook's vocabulary;
                     fenced lines and header rows are never candidates.
  --append           after the newest ISO-dated row the guard reads in `## Open` (the latest Found
                     date; a tie goes to the last in file order), not blindly at end of file.

SET DISPOSITION. --set-disposition --id ID changes one existing row in place instead of adding one,
for example ROUTED <id> to FIXED #N (sha) [class: ...] once the fix merges, which was done by hand.
stdin carries the new Disposition cell text, never a row: one line (UTF-8, at most one trailing LF),
surrounding whitespace dropped as the guard's str.strip drops it. The target is the one row the guard
reads in `## Open` or `## Closed today` whose Finding cell leads with [ID] (any severity; a header
the guard parses as a row is a candidate, so it can make the id ambiguous); fenced lines, the dated
archive and mis-filed rows outside both sections are never targets. Only the text of that row's
last cell, between its last two unescaped pipes (or after the last one when the row has no
trailing border pipe), is replaced, written as one space, the cell, one space; every other line,
the other cells, the line ends and the final line end are kept byte for byte. The changed row is
then held to the same checks as a new row: check_row (columns, Found date, severity, disposition
grammar, class clauses, the id), the splice re-parse (the guard must read the same rows with only
this row's disposition changed, and the mis-filed list must not change), the merge guard's
decide_exit before and after, and the report-only class count over this checkout's git-tracked
set. Its refusals (exit 1) are the stdin ones above plus disposition-empty (an empty or blank cell;
--open is not accepted here, so this mode never writes an undispositioned row), id-invalid,
id-not-found (no row leads with [ID] in those sections), id-ambiguous (more than one; the second's
line is given), malformed-columns (an unescaped pipe in the cell, or a target row that already has
the wrong column count), the row checks above, splice-mismatch, misfiled-grew and
merge-guard-regressed. The output is the ledger line, the target's line number and section, the
row verdict, the class-count line and the merge-guard line: no cell text and no id. --after,
--append, --open, --delivery and --source-key are usage errors with it (exit 2). The write is the
same atomic_replace transaction, and --dry-run runs the same pre-flight. RESIDUES, stated: the
whole changed row is checked, so a row the tool would not have written (a Found date that is not
ISO, a severity outside the vocabulary) cannot be dispositioned with it until it is corrected by
hand; a row with the same id in the archive or mis-filed outside the two sections is neither a
target nor a conflict; the tool does not check that the new disposition is true (that #N merged,
that the sha is on the default branch, that the attested class count is current), only that the
guard reads it as the author intends; and a disposition that was valid before is replaced without
comparison, so a FIXED row can be set back to ROUTED.

REFUSALS (exit 1). not-utf8, multiline, bad-line-char (a CR or another character str.splitlines
treats as a line break), malformed-columns, severity-unknown, disposition-invalid, disposition-empty
(an error or warning row with an empty disposition; --open admits it: an empty error row
makes the merge guard block the merge, while an empty warning row is surfaced without blocking), class-unattested, class-bad-exempt, class-multi (on any row: one clause
per row), found-not-iso, id-invalid, id-not-in-row, duplicate-id, anchor-not-found, anchor-ambiguous,
no-dated-open-row, open-row-in-closed (an --open row may not land in `## Closed today`, which the guard
does not scan), splice-mismatch, misfiled-grew, merge-guard-regressed. A block the ledger already has
is reported, not refused, so dispositioning stays possible. A note row's disposition is not
grammar-checked (the guard does not check it), but its columns and class clauses are.

CLASS COUNT (report only). For a FIXED class row with a `[class: ...]` clause the tool re-runs
check-class-completeness.py's probe over this checkout's git-tracked set and reports the reproduced
count against the attested one, as a WARNING when they differ. It never refuses on it: an in-flight
branch can legitimately differ from this tree (the 2026-10-13 D14 cross-branch seed). D14 stays the
pre-push check that fails on growth.

DELIVERY FINDINGS (report only, 3b544). --delivery PATH names the review delivery the row records
(mistakes register 312: a delivery reported FINDINGS 0E/1W/2N, only some of its findings got rows, and
the gap went unseen for hours). The tool reads the delivery's last `FINDINGS: <n> ERROR, <n> WARN, <n>
NOTE` line and prints one `delivery-findings:` line: the three totals beside the number of ledger rows
whose Source cell leads with the delivery's own review key, `<family> <item> /validate-pr round <n> @
<sha>`, with a WARNING when there are fewer rows than findings. THE KEY comes from the delivery: the
family is the `family=` value of a `WORKER_STATUS:` first line (the wrapper's header), the item and
sha are those of the last `VPR-COMPLETE <item> <sha>` line as written, and the round is that of a
`# /validate-pr round <n> (REFUTE...): <item>, ...` heading whose item field is the item (the
delivery's copy of the brief heading) only when it is the delivery's first heading (3b544 r3): a
round heading after another heading is a quote, never the delivery's round. The round number `<n>` is a
positive integer in ASCII digits with no leading zero, so a heading with `round 0` or `round 03` is not a
round heading. A heading's item field is read exactly so (3b578): after the round number, one or more
spaces or tabs, then `(REFUTE` in uppercase, closed by its first `)`, which a `:` must follow; then
the text up to the first comma or the line end, spaces and tabs stripped, which must be one item
token (ASCII letters, digits, `.`, `_` or `-`, starting and ending with a letter or digit, as in
VPR-COMPLETE). A heading whose item field is another item names no item, even when it mentions the
item later. A heading with no item field
(for example `(refute)`, text before `(REFUTE`, a `)` inside its parentheses, no colon after them,
or a field that is empty, backticked, or holds a space or a no-break space) gives no round, but it
names the item when it holds it as a whole token (not next to an ASCII letter or digit, `_` or `-`), so it
still counts toward round-heading-ambiguous (3b578 r2). Many deliveries carry no such heading (neither
sample delivery staged for 3b544 does), so the orchestrator should pass --source-key when it knows the
round. --source-key KEY gives the whole key explicitly; every part the delivery also carries must
equal the key's, else the count is UNVERIFIABLE (source-key-disagrees), and a key not in that form is
UNVERIFIABLE (source-key-invalid). Without --source-key, a delivery that lacks a part prints the row
count as UNVERIFIABLE (no-vpr-complete-line, no-worker-status-family, no-round-heading), never a
broader count; a part carried in a form that does not parse is UNVERIFIABLE either way
(worker-status-family-unparseable, vpr-complete-line-unparseable, round-heading-ambiguous when
headings naming the item state two rounds). A delivery with no `WORKER_STATUS` first line has no
family; a `WORKER_STATUS` first line without exactly one valid `family=` value (none, two, or an
empty one) is a part that does not parse, and so is one whose envelope,
`WORKER_STATUS: <STATUS> (...)`, does not parse, even with one valid `family=` value: for example
one with no parentheses, or one whose status is not one or more ASCII uppercase letters (A to Z),
such as an empty status or one holding a digit, `_`, or a letter outside A to Z (lowercase,
accented or full-width). A `WORKER_STATUS` first line is a first line that starts with
`WORKER_STATUS:` at column 0, case and colon exact: an indented first line, a lowercase one
(`worker_status:`), and one with no colon or a space before the colon (`WORKER_STATUS PASS`,
`WORKER_STATUS : PASS`) are not `WORKER_STATUS` first lines, whatever follows, so such a delivery
has no family. A byte-order mark before `WORKER_STATUS` makes the first line not a `WORKER_STATUS`
first line, so such a delivery has no family. FINDINGS,
VPR-COMPLETE and heading lines count at column 0 outside code fences: the hook's fence predicates,
except that a backtick run whose remaining text holds a backtick opens no fence (CommonMark reads it
as inline code); delivery lines end at LF only, a CR before it dropped, so a lone CR or U+2028
starts no line. MATCHING RULE: the Source cell starts
with the key exactly (case and spacing included) and the key is not followed by an ASCII letter or
digit, `_` or `-`, so a row of another family, item, round or sha, or with a shorter or longer sha, is
not counted. The rows counted are the duplicate-id scope above, in the ledger text with this row when the
row is accepted, else in the ledger as read. The Source cell is split on unescaped pipes as the guard
splits, and used only when the other four cells equal the guard's parse of the same line; otherwise
the count is UNVERIFIABLE (source-cell-divergence). The option never refuses, never blocks the write
and never changes the exit code. A delivery that is missing, unreadable, not a regular file (it is
opened non-blocking, so a FIFO cannot stall the write) or not UTF-8, that has no FINDINGS line, or
whose last FINDINGS line does not parse prints `delivery-findings: UNVERIFIABLE (<code>)`, never a
zero. Like every other line it carries counts and codes, never the key, its parts or row text.
RESIDUES, stated: a row count shows coverage, not faithfulness (a row that misstates its finding
counts the same); a combined row recording several findings counts once, so fewer rows than findings
is a prompt to look, not proof of a gap; two deliveries with one key (the same family re-run for one
item, round and sha) share their rows, so either can read as covered by the other's; a Source cell
that states the review in another form than the key (other case or spacing, prose before it, a
shorter sha) is not counted, so the count errs low, toward the WARNING; the family is the wrapper's
header, not proof of which model wrote the delivery, and --source-key is trusted for the parts the
delivery lacks; the FINDINGS line is taken as written, so a delivery that miscounts its own findings
is not caught; a delivery whose first heading quotes another round's heading for the same item at
column 0 still takes that round's key, even when its own headings follow the quote (only an
unfenced ATX heading before the quote stops it; a setext, HTML, block-quoted or list-item heading
does not), and with --source-key that case is UNVERIFIABLE (source-key-disagrees) instead; the item
field narrows two checks (3b578): a heading whose item field is another item never counts toward
round-heading-ambiguous, even when it mentions the item later, and a heading with no item field
gives no round, so with --source-key it cannot disagree with the key's round and only counts toward
round-heading-ambiguous; fence reading does not model container blocks or HTML blocks, so a tail
line quoted inside one can still be read, and an unclosed fence runs to the end, so a tail after it
reads as absent (UNVERIFIABLE, not a count).

ENVIRONMENT (exit 2). The hook cannot load or lacks a function used here; the ledger is missing,
unresolvable, unreadable, not UTF-8, a symlink, not a regular file, has more than one hard link, or
belongs to another user (ownership cannot survive the rename); its line ends are not uniformly LF or
uniformly CRLF as str.splitlines (the hook's line model) reads them; the rows the guard parses and the
rows mapped to lines here disagree; the file changed between read and write; the access ACL could not
be read or copied; the group cannot be preserved (ledger-group-unpreservable); the temp file's group,
mode or access ACL differs from the expected values (ledger-metadata-unpreservable); required
directory-fd operations are unavailable (ledger-dir-fd-unavailable); the ledger's immediate
parent is itself a symlink (ledger-parent-symlink, decided by lstat when the parent open
fails); opening the parent, writing,
or renaming fails before the rename succeeds (write-failed); the directory fsync fails
(written-dir-fsync-failed); the read-back after the rename fails (post-write-readback-failed); or the
written file does not read back as written (post-write-mismatch). The rename already happened for
those last three errors. A failed temp-file close or unlink during cleanup never replaces the error
already in flight: the original error line is printed, then a second line "error: temp-cleanup-failed",
still exit 2; the same second line follows "error: internal" when the primary failure was
unexpected. A failed close of the parent directory fd never replaces it either and adds no line,
since it leaves nothing on disk to clean up. With no error in flight that close runs only after the
rename and a verified read-back, so its failure prints "error: internal", still exit 2, while the
ledger already holds the new row; it has no named code, as it checks nothing about the written file.
--dry-run runs the same write pre-flight
(the directory-fd capability check and the O_DIRECTORY|O_NOFOLLOW parent open, then a close), so
it refuses whatever that pre-flight refuses; later write stages (temp creation, group,
ACL and metadata preservation, identity re-check) can still refuse a real write. Outside --self-test an
unexpected failure prints "error: internal" (under --self-test it shows its traceback). A usage error
also exits 2: a --ledger value ending in / or /. is refused that way (ledger-path-directory-suffix)
before pathlib would discard the suffix.

LINE MAPPING. classify() walks the ledger with the hook's own fence and heading predicates
(_fence_run, _fence_closes, _opens_scanned_section) and parses each candidate line with the hook's row
parser; cross_check() then requires the rows so mapped to equal parse_open_rows_full and
parse_dispositioned_rows_full on the whole text, and exits 2 when they differ. A future hook change
that moves a scope rule therefore stops this tool instead of placing a row wrongly.

ATOMIC WRITE. The write transaction opens the parent once with O_DIRECTORY|O_NOFOLLOW. A sibling temp file is created
relative to that directory fd with O_EXCL|O_NOFOLLOW at 0600, written and fsynced, and given the
original group, POSIX access ACL and mode. The target's inode, size, mtime, ctime, mode, uid, gid,
access ACL and sha256 are re-checked relative to the same directory fd before os.replace uses it
for both operands. That directory fd is fsynced and used for read-back and any temp cleanup.
An immediate symlink parent is refused (ledger-parent-symlink); intermediate symlinks and '..'
retain kernel lookup semantics. Writes require directory-fd support; there is no pathname-based fallback.
RESIDUES, stated: there is no shared lock, so a write landing between the re-check and the rename is
lost, as is a write by a writer holding the old inode open; extended attributes other than the access ACL are not carried over; ACLs are read through Linux
xattrs only.

SHA-SHAPED REFS (stated residue). The hook's letter-series and letter-suffixed ref shapes
(`3b108`, `3b50b2e1`, `12b345a`) overlap hex, so a short SHA such as `1b2e3a4` or `12b345a`
reads as a valid ref and `FIXED 1b2e3a4` passes here as it passes the guard. Closing that needs a hook grammar change, which is out of scope here.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime
import errno
import hashlib
import importlib.util
import io
import os
import re
import secrets
import stat
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_common import REPO_ROOT, resolve_working  # noqa: E402

HOOK_REL = Path(".claude") / "hooks" / "block-on-open-findings.py"
MATCHER_REL = Path("tools") / "check-class-completeness.py"
ACL_XATTR = "system.posix_acl_access"
DIR_FD_WRITE_SUPPORTED = (
    all(hasattr(os, name) for name in
        ("O_DIRECTORY", "O_NOFOLLOW", "O_CLOEXEC"))
    and all(func in os.supports_dir_fd
            for func in (os.open, os.unlink, os.rename))
)
# Every hook name this tool reads; a hook that lacks one is an environment error, not a pass.
HOOK_API = (
    "SEVERITIES", "CLASS_ATTEST_RE", "CLASS_EXEMPT_RE", "MISFILED_ROW_RE", "parse_open_rows_full", "parse_dispositioned_rows_full",
    "parse_open_rows", "undispositioned", "leading_class_token", "is_fixed_disposition",
    "class_attestation_state", "extract_class_attestation", "fixed_class_rows_unattested",
    "misfiled_finding_rows", "decide_exit", "_fence_run", "_fence_closes", "_opens_scanned_section",
)
# The Found-date shape --append orders by (a date, not disposition grammar).
ISO_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
# The guard's unescaped-pipe cell split, used for the Source cell only and cross-checked per line.
CELL_SPLIT_RE = re.compile(r"(?<!\\)\|")
# A review delivery's tail (3b544). The FINDINGS labels are compared as strings, not spelled in the
# pattern: they are the delivery contract's words, not the ledger severity vocabulary the hook owns
# (test_tool_defines_no_disposition_grammar holds every pattern here to that).
FINDINGS_LINE_RE = re.compile(
    r"FINDINGS:[ \t]*([0-9]+) ([A-Z]+), ([0-9]+) ([A-Z]+), ([0-9]+) ([A-Z]+)[ \t]*")
FINDINGS_LABELS = ("ERROR", "WARN", "NOTE")
VPR_COMPLETE_RE = re.compile(
    r"VPR-COMPLETE ([A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?) ([0-9A-Fa-f]{7,40})[ \t]*")
# The delivery's own review key (3b544 r2): the wrapper's first-line family, the brief heading's
# round, and the explicit --source-key form the Source cell must lead with.
WORKER_STATUS_RE = re.compile(r"WORKER_STATUS: [A-Z]+ \((.*)\)[ \t]*")
FAMILY_RE = re.compile(r"[a-z][a-z0-9-]*")
ROUND_HEADING_RE = re.compile(r"# /validate-pr round ([1-9][0-9]*)(?![0-9])(.*)")
# A round heading's item field (3b578), matched at the start of the text after the round number: an
# uppercase `(REFUTE` up to its first `)`, a `:`, then one item token up to the first comma or the end,
# never a later mention, so a heading of another item that cites this one gives no round. A heading with
# no item field gives no round either, but its rest is still read for the ambiguity check (3b578 r2).
ROUND_ITEM_RE = re.compile(
    r"[ \t]+\(REFUTE[^)]*\):[ \t]*([A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?)[ \t]*(?:,|$)")
# Any ATX heading line (CommonMark: up to three spaces, one to six #, then a space, a tab or the end):
# a round heading after one is a quote, not the delivery's own (3b544 r3).
ATX_HEADING_RE = re.compile(r" {0,3}#{1,6}(?:[ \t]|$)")
SOURCE_KEY_RE = re.compile(
    r"([a-z][a-z0-9-]*) ([A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?) /validate-pr round ([1-9][0-9]*)"
    r" @ ([0-9A-Fa-f]{7,40})")
# What may not follow the key in a Source cell: a token character would make it another item, round or sha.
KEY_END_RE = re.compile(r"[A-Za-z0-9_-]")
_NO_XATTR = {e for e in (getattr(errno, "ENODATA", None), errno.ENOTSUP, errno.EOPNOTSUPP) if e is not None}


class EnvError(Exception):
    """An environment failure (exit 2). ``code`` is a verdict code; ``line`` an optional line number;
    ``cleanup`` is "temp-cleanup-failed" when the temp-file cleanup also failed, else None."""

    def __init__(self, code: str, line: int | None = None):
        super().__init__(code if line is None else f"{code} (line {line})")
        self.code = code
        self.cleanup: str | None = None


class Refusal(Exception):
    """A placement refusal raised by insertion_point (exit 1)."""

    def __init__(self, code: str, line: int | None = None):
        super().__init__(code if line is None else f"{code} (line {line})")


def load_hook(root: Path):
    """The open-findings hook loaded by file path from ``root`` (the merge-when-green.py pattern). Its
    _load_sibling reuses the lint_common this module imported. Raises EnvError on any load failure."""
    path = Path(root) / HOOK_REL
    try:
        spec = importlib.util.spec_from_file_location("_ofr_open_findings", path)
        if spec is None or spec.loader is None:
            raise EnvError("hook-unloadable")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except EnvError:
        raise
    except Exception as exc:  # noqa: BLE001 - any load failure refuses
        raise EnvError("hook-unloadable") from exc
    if any(not hasattr(mod, name) for name in HOOK_API):
        raise EnvError("hook-api-missing")
    return mod


def decode_row(raw: bytes) -> tuple[str | None, list[str]]:
    """PURE. (row, refusal codes) from the stdin bytes: UTF-8, one line, at most one trailing LF."""
    try:
        row = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, ["not-utf8"]
    if row.endswith("\n"):
        row = row[:-1]
    if "\n" in row:
        return None, ["multiline"]
    if not row:
        return None, ["malformed-columns"]
    if row.splitlines() != [row]:
        return None, ["bad-line-char"]
    return row, []


def decode_cell(raw: bytes) -> tuple[str | None, list[str]]:
    """PURE. (cell, refusal codes) from the --set-disposition stdin bytes: decode_row's checks, then the
    guard's str.strip; an empty or blank cell is disposition-empty."""
    if raw in (b"", b"\n"):
        return None, ["disposition-empty"]
    cell, codes = decode_row(raw)
    if codes:
        return None, codes
    cell = cell.strip()
    return (cell, []) if cell else (None, ["disposition-empty"])


def split_lines(text: str) -> tuple[list[str], str, bool]:
    """PURE. (lines, line end, ends-with-line-end) for a ledger whose line ends are uniformly LF or
    uniformly CRLF. Raises EnvError('line-model', n) at the first line where that split and
    str.splitlines (the hook's line model) disagree."""
    eol = "\r\n" if "\r\n" in text else "\n"
    final = text.endswith(eol)
    body = text[: -len(eol)] if final else text
    lines = body.split(eol) if (body or final) else []
    hook_lines = text.splitlines()
    if lines != hook_lines:
        n = next((i for i, (a, b) in enumerate(zip(lines, hook_lines), start=1) if a != b),
                 min(len(lines), len(hook_lines)) + 1)
        raise EnvError("line-model", n)
    return lines, eol, final


def single_row(hook, line: str):
    """The guard's parse of one line as an `## Open` row: its (found, severity, finding, disposition)
    tuple, or None where the guard reads no row (a header, a delimiter, a non-table line)."""
    rows = hook.parse_open_rows_full("## Open\n" + line + "\n")
    return rows[0] if len(rows) == 1 else None


def classify(hook, lines: list[str]) -> list[str | None]:
    """Per line: 'open' or 'closed' for a row the guard reads in that section, 'outside' for an unfenced
    non-heading line outside both, else None (fenced, a heading, or a non-row line in a section). Walks
    the lines with the hook's own predicates; cross_check() confirms the result."""
    kinds: list[str | None] = []
    section = None
    fence = None
    for line in lines:
        stripped = line.strip()
        run = hook._fence_run(line, stripped)
        if fence is not None:
            if hook._fence_closes(run, fence, stripped):
                fence = None
            kinds.append(None)
            continue
        if run is not None:
            fence = run
            kinds.append(None)
            continue
        if line.startswith("## "):
            heading = stripped.lower()
            if hook._opens_scanned_section(heading, ("## open",)):
                section = "open"
            elif hook._opens_scanned_section(heading, ("## closed today",)):
                section = "closed"
            else:
                section = None
            kinds.append(None)
            continue
        if section is None:
            kinds.append("outside")
        else:
            kinds.append(section if single_row(hook, line) is not None else None)
    return kinds


def cross_check(hook, text: str, lines: list[str], kinds: list[str | None]) -> None:
    """Raise EnvError('row-map-divergence') unless the rows mapped to lines equal the guard's parse of
    the whole text, for `## Open` alone and for `## Open` plus `## Closed today`."""
    opened = [single_row(hook, ln) for ln, k in zip(lines, kinds) if k == "open"]
    both = [single_row(hook, ln) for ln, k in zip(lines, kinds) if k in ("open", "closed")]
    if opened != hook.parse_open_rows_full(text) or both != hook.parse_dispositioned_rows_full(text):
        raise EnvError("row-map-divergence")


def check_row(hook, row: str, finding_id: str, *, allow_open: bool) -> tuple[list[str], tuple | None]:
    """(refusal codes, parsed row) for one row line, judged by the hook's functions only."""
    rows = hook.parse_open_rows_full("## Open\n" + row + "\n")
    if len(rows) != 1 or rows[0][3] is None:
        return ["malformed-columns"], None
    found, sev, finding, disp = rows[0]
    codes = []
    try:
        if not ISO_DATE_RE.fullmatch(found):
            raise ValueError
        datetime.date.fromisoformat(found)
    except ValueError:
        codes.append("found-not-iso")
    if sev not in hook.SEVERITIES:
        codes.append("severity-unknown")
    elif sev != "note" and hook.undispositioned([(sev, finding, disp)], sev):
        if disp:
            codes.append("disposition-invalid")
        elif not allow_open:
            codes.append("disposition-empty")
    state = hook.class_attestation_state(disp)
    class_spans = [m.span() for m in hook.CLASS_ATTEST_RE.finditer(disp)]
    exempt_count = sum(
        not any(a <= m.start() and m.end() <= b for a, b in class_spans)
        for m in hook.CLASS_EXEMPT_RE.finditer(disp)
    )
    if state == "multi" or len(class_spans) + exempt_count > 1:
        codes.append("class-multi")
    elif hook.fixed_class_rows_unattested([(sev, finding, disp)]):
        codes.append("class-bad-exempt" if state == "bad-exempt" else "class-unattested")
    if hook.leading_class_token("[" + finding_id + "]") != finding_id:
        codes.append("id-invalid")
    elif hook.leading_class_token(finding) != finding_id:
        codes.append("id-not-in-row")
    return codes, rows[0]


def id_lines(hook, lines: list[str], kinds: list[str | None], finding_id: str) -> list[int]:
    """1-based lines whose Finding cell leads with [finding_id] (the duplicate scope in the docstring)."""
    hits = []
    for n, (line, kind) in enumerate(zip(lines, kinds), start=1):
        if kind in ("open", "closed") or (kind == "outside" and hook.MISFILED_ROW_RE.match(line)):
            parsed = single_row(hook, line)
            if parsed is not None and hook.leading_class_token(parsed[2]) == finding_id:
                hits.append(n)
    return hits


def insertion_point(hook, lines: list[str], kinds: list[str | None], *,
                    after_id: str | None) -> tuple[int, str]:
    """(0-based index of the line to insert after, its section). Raises Refusal."""
    if after_id is not None:
        hits = []
        for i, (line, k) in enumerate(zip(lines, kinds)):
            if k not in ("open", "closed"):
                continue
            _found, sev, finding, _disp = single_row(hook, line)
            # The severity screen keeps a header the guard parses as a row (`| Date | Level | ...`) out.
            if sev in hook.SEVERITIES and hook.leading_class_token(finding) == after_id:
                hits.append((i, k))
        if not hits:
            raise Refusal("anchor-not-found")
        if len(hits) > 1:
            raise Refusal("anchor-ambiguous", hits[1][0] + 1)
        return hits[0]
    best = None
    for i, (line, k) in enumerate(zip(lines, kinds)):
        if k != "open":
            continue
        found = single_row(hook, line)[0]
        if not ISO_DATE_RE.fullmatch(found):
            continue
        try:
            day = datetime.date.fromisoformat(found)
        except ValueError:
            continue
        if best is None or day >= best[0]:
            best = (day, i)
    if best is None:
        raise Refusal("no-dated-open-row")
    return best[1], "open"


def splice(lines: list[str], eol: str, final: bool, after_index: int, row: str) -> str:
    """PURE. The ledger text with ``row`` inserted after line ``after_index`` (0-based), line ends kept."""
    out = lines[:after_index + 1] + [row] + lines[after_index + 1:]
    return eol.join(out) + (eol if final else "")


def merge_guard_code(hook, text: str) -> int:
    """The guard's decide_exit on ``text`` (0 allow, 2 block). Its stderr carries finding text, so it is
    captured and discarded; this tool reports codes instead."""
    with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
        return hook.decide_exit(hook.parse_open_rows(text), text)


def verify_splice(hook, before: str, after: str, parsed: tuple, at: int, section: str,
                  kinds: list[str | None]) -> list[str]:
    """Refusal codes from re-parsing the spliced text: the guard must read exactly the earlier rows plus
    this one at the expected index, and the mis-filed list must not change."""
    out = []
    a_lines, _eol, _final = split_lines(after)
    a_kinds = classify(hook, a_lines)
    cross_check(hook, after, a_lines, a_kinds)
    k_open = kinds[:at + 1].count("open")
    k_both = k_open + kinds[:at + 1].count("closed")
    open_b = hook.parse_open_rows_full(before)
    both_b = hook.parse_dispositioned_rows_full(before)
    want_open = open_b[:k_open] + [parsed] + open_b[k_open:] if section == "open" else open_b
    want_both = both_b[:k_both] + [parsed] + both_b[k_both:]
    if (a_kinds[at + 1] != section or single_row(hook, a_lines[at + 1]) != parsed
            or hook.parse_open_rows_full(after) != want_open
            or hook.parse_dispositioned_rows_full(after) != want_both):
        out.append("splice-mismatch")
    if ([(s, ln) for (_n, s, ln) in hook.misfiled_finding_rows(after)]
            != [(s, ln) for (_n, s, ln) in hook.misfiled_finding_rows(before)]):
        out.append("misfiled-grew")
    return out


def class_count_report(hook, finding: str, disposition: str, probe) -> str:
    """The report-only class-count line. ``probe(token) -> (count, unreadable)``, or None to skip."""
    if not (hook.is_fixed_disposition(disposition) and hook.leading_class_token(finding)
            and hook.class_attestation_state(disposition) == "class"):
        return "class-count: not applicable"
    if probe is None:
        return "class-count: not checked"
    token, attested = hook.extract_class_attestation(disposition)
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            count, unreadable = probe(token)
    except Exception:  # noqa: BLE001 - report only: an unrunnable probe is said, never a refusal
        return "class-count: WARNING unverified (the probe could not run on this checkout)"
    if unreadable:
        return f"class-count: WARNING unverified ({unreadable} corpus file(s) unreadable)"
    if count > attested:
        return (f"class-count: WARNING reproduced {count} > attested {attested} on this checkout "
                "(D14 fails on growth; report only)")
    if count < attested:
        return f"class-count: WARNING reproduced {count} < attested {attested} on this checkout (report only)"
    return f"class-count: reproduced {count} = attested {attested}"


def read_delivery(path) -> tuple[str | None, str | None]:
    """(text, None), or (None, code) for a delivery the report cannot read: delivery-missing,
    delivery-unreadable, delivery-not-regular or delivery-not-utf8. The open is non-blocking, so a
    FIFO is refused as not regular instead of stalling the write."""
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | os.O_CLOEXEC)
    except FileNotFoundError:
        return None, "delivery-missing"
    except (OSError, ValueError):
        return None, "delivery-unreadable"
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            return None, "delivery-not-regular"
        chunks = []
        while chunk := os.read(fd, 1 << 16):
            chunks.append(chunk)
    except OSError:
        return None, "delivery-unreadable"
    finally:
        os.close(fd)
    try:
        return b"".join(chunks).decode("utf-8"), None
    except UnicodeDecodeError:
        return None, "delivery-not-utf8"


def delivery_lines(text: str) -> list[str]:
    """PURE. A delivery's lines, ended at LF only with a CR before it dropped, so a lone CR, U+2028 or
    another character str.splitlines breaks on never starts a column-0 line mid-line (3b544 r2)."""
    lines = text.split("\n")
    if lines[-1] == "":
        lines.pop()
    return [ln[:-1] if ln.endswith("\r") else ln for ln in lines]


def parse_delivery(hook, text: str) -> tuple[tuple[int, int, int] | str, dict]:
    """PURE. (totals, parts) from a delivery. totals is (errors, warns, notes) from the last FINDINGS
    line, or a code: no-findings-line, findings-line-unparseable. parts holds the review key's parts
    the delivery carries, None where it carries none: family (the `family=` value of a WORKER_STATUS
    first line), item and sha (the last VPR-COMPLETE line, as written), rounds (the round, the item
    field (the item token ROUND_ITEM_RE reads) or None, the text after the round number, and
    whether it is the delivery's first heading, of each `# /validate-pr round <n>` heading); bad is the
    code of a part carried in a form that does not parse (worker-status-family-unparseable,
    vpr-complete-line-unparseable), else None. FINDINGS, VPR-COMPLETE and heading lines count at
    column 0 outside code fences: the hook's fence predicates, except that a backtick run whose
    remaining text holds a backtick opens no fence (CommonMark reads that line as inline code). Any
    unfenced ATX heading, indented up to three spaces, counts as a heading for the first-heading test."""
    findings = complete = None
    rounds = []
    headed = False
    fence = None
    lines = delivery_lines(text)
    for line in lines:
        stripped = line.strip()
        run = hook._fence_run(line, stripped)
        if fence is not None:
            if hook._fence_closes(run, fence, stripped):
                fence = None
            continue
        if run is not None and not (run[0] == "`" and "`" in stripped[run[1]:]):
            fence = run
            continue
        if line.startswith("FINDINGS:"):
            findings = line
        elif line.startswith("VPR-COMPLETE"):
            complete = line
        elif (m := ROUND_HEADING_RE.fullmatch(line)) is not None or ATX_HEADING_RE.match(line):
            if m is not None:
                named = ROUND_ITEM_RE.match(m[2])
                rounds.append((m[1], None if named is None else named[1], m[2], not headed))
            headed = True
    totals: tuple[int, int, int] | str = "no-findings-line"
    if findings is not None:
        m = FINDINGS_LINE_RE.fullmatch(findings)
        if m is None or (m[2], m[4], m[6]) != FINDINGS_LABELS:
            totals = "findings-line-unparseable"
        else:
            totals = (int(m[1]), int(m[3]), int(m[5]))
    parts = {"family": None, "item": None, "sha": None, "rounds": rounds, "bad": None}
    if lines and lines[0].startswith("WORKER_STATUS:"):
        m = WORKER_STATUS_RE.fullmatch(lines[0])
        values = [] if m is None else [f.strip()[len("family="):] for f in m[1].split(",")
                                       if f.strip().startswith("family=")]
        if len(values) == 1 and FAMILY_RE.fullmatch(values[0]):
            parts["family"] = values[0]
        else:
            parts["bad"] = "worker-status-family-unparseable"
    if complete is not None:
        m = VPR_COMPLETE_RE.fullmatch(complete)
        if m is None:
            parts["bad"] = parts["bad"] or "vpr-complete-line-unparseable"
        else:
            parts["item"], parts["sha"] = m[1], m[2]
    return totals, parts


def review_key(parts: dict, source_key: str | None) -> tuple[str | None, str | None]:
    """PURE. (key, None) for the delivery's own review key `<family> <item> /validate-pr round <n> @
    <sha>`, or (None, code), the first that applies in this order: a part the delivery carries but
    cannot parse (its code); a --source-key that does not parse (source-key-invalid); headings naming
    the item (the key's with --source-key, else the VPR-COMPLETE line's) with two rounds, wherever they
    stand (round-heading-ambiguous), so without --source-key a delivery with no VPR-COMPLETE line names
    no item and gets no-vpr-complete-line; with --source-key, a carried part that differs from the
    key's (source-key-disagrees); without it, the first part the delivery lacks (no-vpr-complete-line,
    no-worker-status-family, no-round-heading). A heading names the item when its item field is the
    item, or when it has no item field but holds the item as a whole token (3b578 r2); the round is
    only ever that of the delivery's first heading, when its item field is the item (3b544 r3, 3b578)."""
    if parts["bad"] is not None:
        return None, parts["bad"]
    given = None
    if source_key is not None:
        given = SOURCE_KEY_RE.fullmatch(source_key)
        if given is None:
            return None, "source-key-invalid"
    item = parts["item"] if given is None else given[2]
    rounds, own = set(), None
    if item is not None:
        token = re.compile(r"(?<![A-Za-z0-9_-])" + re.escape(item) + r"(?![A-Za-z0-9_-])")
        for rnd, named, rest, leads in parts["rounds"]:
            if named == item:
                rounds.add(rnd)
                if leads:
                    own = rnd
            elif named is None and token.search(rest):
                # The ambiguity backstop (3b578 r2): a heading with no item field gives no round, but one
                # holding the item still states a round for it, so a quote first cannot hide a later own round.
                rounds.add(rnd)
    if len(rounds) > 1:
        return None, "round-heading-ambiguous"
    carried = (parts["family"], parts["item"], own, parts["sha"])
    if given is not None:
        if any(c is not None and c != k for c, k in zip(carried, given.groups())):
            return None, "source-key-disagrees"
        return source_key, None
    for value, code in ((parts["item"], "no-vpr-complete-line"), (parts["family"], "no-worker-status-family"),
                        (carried[2], "no-round-heading")):
        if value is None:
            return None, code
    family, item, rnd, sha = carried
    return f"{family} {item} /validate-pr round {rnd} @ {sha}", None


def source_cell(hook, line: str) -> str | None:
    """The Source cell of one row line, or None where the guard reads no well-formed row. Raises
    EnvError('source-cell-divergence') when the split's other four cells differ from the guard's parse
    of the same line, so a hook change to the split stops the count instead of skewing it."""
    parsed = single_row(hook, line)
    if parsed is None or parsed[3] is None:
        return None
    cells = [c.strip() for c in CELL_SPLIT_RE.split(line.strip())]
    if cells and cells[0] == "":
        cells = cells[1:]
    if cells and cells[-1] == "":
        cells = cells[:-1]
    if len(cells) != 5 or (cells[0], cells[1].lower(), cells[2], cells[4]) != parsed:
        raise EnvError("source-cell-divergence")
    return cells[3]


def review_rows(hook, lines: list[str], kinds: list[str | None], key: str) -> int:
    """The rows of the duplicate-id scope (id_lines) whose Source cell leads with ``key`` by the
    docstring's matching rule."""
    count = 0
    for line, kind in zip(lines, kinds):
        if kind in ("open", "closed") or (kind == "outside" and hook.MISFILED_ROW_RE.match(line)):
            cell = source_cell(hook, line)
            if cell is not None and cell.startswith(key) and not KEY_END_RE.match(cell, len(key)):
                count += 1
    return count


def delivery_report(hook, ledger_text: str, path, *, with_row: bool, source_key: str | None = None) -> str:
    """The report-only delivery-findings line (3b544). It never raises: what cannot be read, parsed or
    counted is said as UNVERIFIABLE, never as a zero."""
    try:
        text, code = read_delivery(path)
        totals, parts = (code, None) if text is None else parse_delivery(hook, text)
        key, why = (None, None) if parts is None else review_key(parts, source_key)
    except Exception:  # noqa: BLE001 - report only: never a refusal
        totals, key, why = "delivery-report-failed", None, None
    if isinstance(totals, str):
        return f"delivery-findings: UNVERIFIABLE ({totals}); nothing compared (report only)"
    errors, warns, notes = totals
    total = errors + warns + notes
    head = f"delivery-findings: reported {errors} ERROR, {warns} WARN, {notes} NOTE ({total} in all)"
    if key is None:
        return f"{head}; ledger rows UNVERIFIABLE ({why}) (report only)"
    try:
        lines, _eol, _final = split_lines(ledger_text)
        rows = review_rows(hook, lines, classify(hook, lines), key)
    except EnvError as exc:
        return f"{head}; ledger rows UNVERIFIABLE ({exc.code}) (report only)"
    except Exception:  # noqa: BLE001 - report only: never a refusal
        return f"{head}; ledger rows UNVERIFIABLE (row-count-failed) (report only)"
    if rows < total:
        verdict = "WARNING fewer rows than reported findings (a combined row counts once)"
    elif rows > total:
        verdict = "more rows than reported findings"
    else:
        verdict = "rows equal the reported total (coverage, not faithfulness)"
    where = "ledger with this row" if with_row else "ledger as read, nothing written"
    origin = "the delivery" if source_key is None else "--source-key"
    return (f"{head}; {rows} ledger row(s) lead with its review key (key from {origin}; {where}); "
            f"{verdict} (report only)")


def make_probe(root: Path):
    """The class-count observer over ``root``'s git-tracked corpus set (check-class-completeness.py)."""
    def probe(token: str) -> tuple[int, int]:
        spec = importlib.util.spec_from_file_location("_ofr_class_completeness", Path(root) / MATCHER_REL)
        matcher = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(matcher)
        files = matcher.attest_file_set(Path(root))
        occ, skipped = matcher.find_occurrences([token], files, root=Path(root))
        return len(occ[token]), len(skipped)
    return probe


def evaluate(hook, text: str, row: str, finding_id: str, *, after_id: str | None,
             allow_open: bool, probe=None) -> tuple[list[str], list[str], str | None]:
    """The whole decision for one row against one ledger text: (refusals, report lines, new text or
    None). Pure apart from ``probe``. Raises EnvError when the line model or row map cannot be
    trusted. Refusals and report lines carry codes, counts and line numbers only."""
    lines, eol, final = split_lines(text)
    kinds = classify(hook, lines)
    cross_check(hook, text, lines, kinds)
    report = [ledger_report(eol, kinds)]
    codes, parsed = check_row(hook, row, finding_id, allow_open=allow_open)
    if codes:
        return codes, report, None
    _found, sev, finding, disp = parsed
    refusals = [f"duplicate-id (line {n})" for n in id_lines(hook, lines, kinds, finding_id)]
    try:
        at, section = insertion_point(hook, lines, kinds, after_id=after_id)
    except Refusal as exc:
        return refusals + [str(exc)], report, None
    if section == "closed" and sev != "note" and not disp:
        refusals.append("open-row-in-closed")
    report.append(f"anchor: line {at + 1} ({section})")
    report.append(f"insert: line {at + 2} ({section})")
    new_text = splice(lines, eol, final, at, row)
    refusals += verify_splice(hook, text, new_text, parsed, at, section, kinds)
    owed = hook.is_fixed_disposition(disp) and hook.leading_class_token(finding)
    state = hook.class_attestation_state(disp)
    report.append(
        "row: columns ok; severity ok; disposition "
        + ("not checked (note)" if sev == "note" else "ok" if disp else "empty (admitted by --open)")
        + "; class-attestation " + (state if owed else "not owed")
        + "; id " + ("duplicate" if any(r.startswith("duplicate-id") for r in refusals) else "unique"))
    report.append(class_count_report(hook, finding, disp, probe))
    code_b, code_a = merge_guard_code(hook, text), merge_guard_code(hook, new_text)
    expected_block = allow_open and sev == "error" and not disp
    note = ""
    if code_a and not code_b and expected_block:
        note = " (this row, admitted by --open)"
    elif code_b:
        note = " (existing block, reported only)"
    report.append(f"merge-guard: before {'block' if code_b else 'allow'}, "
                  f"after {'block' if code_a else 'allow'}{note}")
    if code_a and not code_b and not expected_block:
        refusals.append("merge-guard-regressed")
    return refusals, report, (None if refusals else new_text)


def ledger_report(eol: str, kinds: list[str | None]) -> str:
    """The report's first line: the line model and the row counts per section."""
    return (f"ledger: line-model ok ({'CRLF' if eol == chr(13) + chr(10) else 'LF'}); "
            f"{kinds.count('open')} open row(s), {kinds.count('closed')} closed-today row(s)")


def target_line(hook, lines: list[str], kinds: list[str | None], finding_id: str) -> tuple[int, str]:
    """(0-based index, section) of the one row the guard reads in `## Open` or `## Closed today` whose
    Finding cell leads with [finding_id]; no severity screen, so a parsed header can make it ambiguous.
    Raises Refusal."""
    hits = [(i, k) for i, (line, k) in enumerate(zip(lines, kinds))
            if k in ("open", "closed") and hook.leading_class_token(single_row(hook, line)[2]) == finding_id]
    if not hits:
        raise Refusal("id-not-found")
    if len(hits) > 1:
        raise Refusal("id-ambiguous", hits[1][0] + 1)
    return hits[0]


def replace_last_cell(line: str, cell: str) -> str:
    """PURE. ``line`` with the text of its last cell, by the guard's unescaped-pipe split, replaced by one
    space, ``cell`` and (before a trailing border pipe) one space; all else is kept as it was."""
    body = line.rstrip()
    pipes = [m.start() for m in CELL_SPLIT_RE.finditer(body)]
    if len(pipes) >= 2 and pipes[-1] == len(body) - 1:
        return line[:pipes[-2] + 1] + " " + cell + " " + line[pipes[-1]:]
    return line[:pipes[-1] + 1] + " " + cell + line[len(body):]


def verify_replace(hook, before: str, after: str, lines: list[str], kinds: list[str | None],
                   old: tuple, parsed: tuple, at: int, section: str) -> list[str]:
    """Refusal codes from re-parsing the changed text: every other line is unchanged, every line keeps
    its kind, the guard reads exactly the earlier rows with only this row's disposition changed, and the
    mis-filed list does not change."""
    out = []
    a_lines, _eol, _final = split_lines(after)
    a_kinds = classify(hook, a_lines)
    cross_check(hook, after, a_lines, a_kinds)
    k_open = kinds[:at].count("open")
    k_both = k_open + kinds[:at].count("closed")
    open_b = hook.parse_open_rows_full(before)
    both_b = hook.parse_dispositioned_rows_full(before)
    want_open = open_b[:k_open] + [parsed] + open_b[k_open + 1:] if section == "open" else open_b
    want_both = both_b[:k_both] + [parsed] + both_b[k_both + 1:]
    if (len(a_lines) != len(lines) or a_lines[:at] + a_lines[at + 1:] != lines[:at] + lines[at + 1:]
            or a_kinds != kinds or parsed[:3] != old[:3] or single_row(hook, a_lines[at]) != parsed
            or hook.parse_open_rows_full(after) != want_open
            or hook.parse_dispositioned_rows_full(after) != want_both):
        out.append("splice-mismatch")
    if ([(s, ln) for (_n, s, ln) in hook.misfiled_finding_rows(after)]
            != [(s, ln) for (_n, s, ln) in hook.misfiled_finding_rows(before)]):
        out.append("misfiled-grew")
    return out


def evaluate_disposition(hook, text: str, cell: str, finding_id: str, *,
                         probe=None) -> tuple[list[str], list[str], str | None]:
    """--set-disposition: the whole decision for one Disposition cell against one ledger text, held to
    evaluate()'s row checks: (refusals, report lines, new text or None). Pure apart from ``probe``.
    Raises EnvError when the line model or row map cannot be trusted."""
    lines, eol, final = split_lines(text)
    kinds = classify(hook, lines)
    cross_check(hook, text, lines, kinds)
    report = [ledger_report(eol, kinds)]
    if hook.leading_class_token("[" + finding_id + "]") != finding_id:
        return ["id-invalid"], report, None
    try:
        at, section = target_line(hook, lines, kinds, finding_id)
    except Refusal as exc:
        return [str(exc)], report, None
    report.append(f"target: line {at + 1} ({section})")
    row = replace_last_cell(lines[at], cell)
    codes, parsed = check_row(hook, row, finding_id, allow_open=False)
    if codes:
        return codes, report, None
    _found, sev, finding, disp = parsed
    new_text = eol.join(lines[:at] + [row] + lines[at + 1:]) + (eol if final else "")
    refusals = [] if disp == cell else ["splice-mismatch"]
    refusals += verify_replace(hook, text, new_text, lines, kinds, single_row(hook, lines[at]), parsed,
                               at, section)
    owed = hook.is_fixed_disposition(disp) and hook.leading_class_token(finding)
    report.append(
        "row: columns ok; severity ok; disposition " + ("not checked (note)" if sev == "note" else "ok")
        + "; class-attestation " + (hook.class_attestation_state(disp) if owed else "not owed"))
    report.append(class_count_report(hook, finding, disp, probe))
    code_b, code_a = merge_guard_code(hook, text), merge_guard_code(hook, new_text)
    report.append(f"merge-guard: before {'block' if code_b else 'allow'}, "
                  f"after {'block' if code_a else 'allow'}{' (existing block, reported only)' if code_b else ''}")
    if code_a and not code_b:
        refusals.append("merge-guard-regressed")
    return refusals, report, (None if refusals else new_text)


def metadata(st: os.stat_result) -> tuple[int, ...]:
    """Fields whose change invalidates the initial ledger snapshot."""
    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns,
            st.st_mode, st.st_uid, st.st_gid)


def read_ledger(path: Path | str, *, dir_fd: int | None = None
                ) -> tuple[bytes, os.stat_result, bytes | None]:
    """Read the ledger, refusing a symlink (ledger-symlink), a non-regular file
    (ledger-not-regular) and a hard-linked file (ledger-hardlinked). When dir_fd is supplied,
    ``path`` is opened relative to that directory fd (the write-side re-check and read-back)."""
    try:
        fd = os.open(
            path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC,
            dir_fd=dir_fd)
    except FileNotFoundError as exc:
        raise EnvError("ledger-missing") from exc
    except OSError as exc:
        raise EnvError("ledger-symlink" if exc.errno == errno.ELOOP else "ledger-unreadable") from exc
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            raise EnvError("ledger-not-regular")
        if st.st_nlink != 1:
            raise EnvError("ledger-hardlinked")
        acl = read_acl(fd)
        chunks = []
        while chunk := os.read(fd, 1 << 16):
            chunks.append(chunk)
        if metadata(os.fstat(fd)) != metadata(st) or read_acl(fd) != acl:
            raise EnvError("ledger-changed")
    except OSError as exc:
        raise EnvError("ledger-unreadable") from exc
    finally:
        os.close(fd)
    return b"".join(chunks), st, acl


def read_acl(target) -> bytes | None:
    """The POSIX access ACL xattr of a path (not followed) or an open fd, or None when there is none."""
    if not hasattr(os, "getxattr"):
        return None
    try:
        if isinstance(target, int):
            return os.getxattr(target, ACL_XATTR)
        return os.getxattr(target, ACL_XATTR, follow_symlinks=False)
    except OSError as exc:
        if exc.errno in _NO_XATTR:
            return None
        raise EnvError("acl-unreadable") from exc


def _copy_acl(fd: int, acl: bytes | None) -> None:
    """Give the temp file exactly the original's access ACL, removing one a default ACL gave it."""
    try:
        if acl is not None:
            os.setxattr(fd, ACL_XATTR, acl)
        elif read_acl(fd) is not None:
            os.removexattr(fd, ACL_XATTR)
    except OSError as exc:
        raise EnvError("acl-copy-failed") from exc


def check_owner(st: os.stat_result) -> None:
    """Refuse a ledger owned by another user: a rename cannot keep its ownership."""
    if st.st_uid != os.geteuid():
        raise EnvError("ledger-owner-differs")


def open_parent(path: Path) -> int:
    """The ledger's immediate parent as an O_DIRECTORY|O_NOFOLLOW fd: the write anchor, and the
    pre-flight --dry-run shares, so both refuse the same parent and capability problems. Raises
    ledger-dir-fd-unavailable without directory-fd support, ledger-parent-symlink when the open
    fails and the immediate parent lstats as a symlink, and write-failed for any other failed
    open."""
    if not DIR_FD_WRITE_SUPPORTED:
        raise EnvError("ledger-dir-fd-unavailable")
    try:
        return os.open(
            path.parent,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
    except OSError as exc:
        with contextlib.suppress(OSError):
            if stat.S_ISLNK(os.lstat(path.parent).st_mode):
                raise EnvError("ledger-parent-symlink") from exc
        raise EnvError("write-failed") from exc


def atomic_replace(path: Path, data: bytes, expect: os.stat_result, expect_sha256: str,
                   expect_acl: bytes | None) -> None:
    """Replace the ledger through one parent fd, preserving its checked metadata."""
    path = Path(path)
    check_owner(expect)
    name = path.name
    tmp = f".{name}.{os.getpid()}.{secrets.token_hex(8)}.tmp"
    fd = dfd = None
    created = replaced = False
    primary: BaseException | None = None
    try:
        try:
            dfd = open_parent(path)
            fd = os.open(
                tmp,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL
                | os.O_NOFOLLOW | os.O_CLOEXEC,
                0o600,
                dir_fd=dfd)
            created = True
            view = memoryview(data)
            while view:
                view = view[os.write(fd, view):]
            try:
                os.fchown(fd, -1, expect.st_gid)
            except OSError as exc:
                raise EnvError("ledger-group-unpreservable") from exc
            _copy_acl(fd, expect_acl)
            os.fchmod(fd, stat.S_IMODE(expect.st_mode))
            temp_st = os.fstat(fd)
            if (temp_st.st_gid != expect.st_gid
                    or stat.S_IMODE(temp_st.st_mode)
                    != stat.S_IMODE(expect.st_mode)
                    or read_acl(fd) != expect_acl):
                raise EnvError("ledger-metadata-unpreservable")
            os.fsync(fd)
            f, fd = fd, None
            os.close(f)

            now_data, now, now_acl = read_ledger(name, dir_fd=dfd)
            if (metadata(now) != metadata(expect) or now_acl != expect_acl
                    or hashlib.sha256(now_data).hexdigest() != expect_sha256):
                raise EnvError("ledger-changed")

            os.replace(tmp, name, src_dir_fd=dfd, dst_dir_fd=dfd)
            replaced = True
            os.fsync(dfd)
        except NotImplementedError as exc:
            raise EnvError("ledger-dir-fd-unavailable") from exc
        except OSError as exc:
            raise EnvError(
                "written-dir-fsync-failed" if replaced else "write-failed"
            ) from exc

        try:
            got, st, got_acl = read_ledger(name, dir_fd=dfd)
        except Exception as exc:  # noqa: BLE001 - the rename already happened; report that state
            raise EnvError("post-write-readback-failed") from exc
        if (hashlib.sha256(got).digest() != hashlib.sha256(data).digest()
                or stat.S_IMODE(st.st_mode) != stat.S_IMODE(expect.st_mode)
                or (st.st_uid, st.st_gid) != (expect.st_uid, expect.st_gid)
                or got_acl != expect_acl):
            raise EnvError("post-write-mismatch")
    except BaseException as exc:
        # Captured explicitly, so only this function's own error can carry the flag.
        primary = exc
        raise
    finally:
        # A failed temp close or unlink must not replace the error in flight.
        try:
            try:
                if fd is not None:
                    os.close(fd)
            finally:
                if created and not replaced:
                    with contextlib.suppress(FileNotFoundError):
                        os.unlink(tmp, dir_fd=dfd)
        except OSError as exc:
            if primary is None:
                raise EnvError("temp-cleanup-failed") from exc
            primary.cleanup = "temp-cleanup-failed"
        finally:
            if dfd is not None:
                # The read-only directory fd leaves nothing to clean up, so a failed close is
                # suppressed under an error in flight rather than reported as a second line.
                try:
                    os.close(dfd)
                except OSError:
                    if primary is None:
                        raise


def _refuse(codes: list[str]) -> int:
    for code in codes:
        print(f"refused: {code}", file=sys.stderr)
    print("result: REFUSED")
    return 1


def _run(args, root: Path, raw: bytes) -> int:
    hook = load_hook(root)
    # stdin is the Disposition cell under --set-disposition, else the whole row.
    value, codes = decode_cell(raw) if args.set_disposition else decode_row(raw)
    if codes:
        return _refuse(codes)
    path = args.ledger
    if path is None:
        try:
            path = resolve_working("open-findings.md", repo_root=root, strict=True)
        except Exception as exc:  # noqa: BLE001 - an unexaminable store is an environment error
            raise EnvError("ledger-unresolvable") from exc
        if path is None:
            raise EnvError("ledger-missing")
    if not path.is_absolute():
        path = Path.cwd() / path
    data, st, acl = read_ledger(path)
    check_owner(st)
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise EnvError("ledger-not-utf8") from exc
    if args.set_disposition:
        refusals, report, new_text = evaluate_disposition(hook, text, value, args.id, probe=make_probe(root))
    else:
        refusals, report, new_text = evaluate(hook, text, value, args.id, after_id=args.after,
                                              allow_open=args.allow_open, probe=make_probe(root))
    if args.delivery is not None:
        # Report only (3b544): the line never refuses and never changes the exit code.
        report.append(delivery_report(hook, text if new_text is None else new_text, args.delivery,
                                      with_row=new_text is not None, source_key=args.source_key))
    for line in report:
        print(line)
    if refusals:
        return _refuse(refusals)
    # The write pre-flight, shared with atomic_replace: --dry-run refuses what a write refuses.
    os.close(open_parent(path))
    if args.dry_run:
        print("result: WOULD-WRITE")
        return 0
    atomic_replace(path, new_text.encode("utf-8"), st, hashlib.sha256(data).hexdigest(), acl)
    print("result: WROTE")
    return 0


def ledger_path(value: str) -> Path:
    """Reject directory-only suffixes before pathlib discards them."""
    if value.endswith(("/", "/.")):
        raise argparse.ArgumentTypeError("ledger-path-directory-suffix")
    return Path(value)


def main(argv: list[str] | None = None, *, root: Path | None = None, stdin: bytes | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--id", help="the finding id: the Finding cell's leading bracketed token, no brackets")
    where = ap.add_mutually_exclusive_group()
    where.add_argument("--after", metavar="ANCHOR_ID",
                       help="insert after the one Open or Closed-today row led by [ANCHOR_ID]")
    where.add_argument("--append", action="store_true",
                       help="insert after the newest dated row the guard reads as Open")
    where.add_argument("--set-disposition", action="store_true",
                       help="replace only the Disposition cell of the one Open or Closed-today row led by "
                            "[ID] with the cell text on stdin")
    ap.add_argument("--ledger", type=ledger_path,
                    help="ledger path (default: resolve_working, strict); a value ending in / or /. "
                         "is refused (ledger-path-directory-suffix)")
    ap.add_argument("--dry-run", action="store_true",
                    help="check and report, running the write pre-flight; write nothing")
    ap.add_argument("--open", dest="allow_open", action="store_true",
                    help="admit an error or warning row with an empty disposition")
    ap.add_argument("--delivery", metavar="PATH",
                    help="report only: print this review delivery's FINDINGS totals beside the ledger "
                         "rows whose Source cell leads with its own review key; never refuses")
    ap.add_argument("--source-key", metavar="KEY",
                    help='with --delivery: the review key "<family> <item> /validate-pr round <n> @ <sha>" '
                         "for the parts the delivery does not carry; parts it carries must agree")
    ap.add_argument("--self-test", action="store_true", help="run the built-in self-test and exit")
    args = ap.parse_args(argv)
    if not args.self_test and (args.id is None
                               or (args.after is None and not args.append and not args.set_disposition)):
        ap.error("--id and one of --after, --append or --set-disposition are required")
    if args.set_disposition and (args.allow_open or args.delivery is not None or args.source_key is not None):
        ap.error("--set-disposition takes no --open, --delivery or --source-key")
    if args.source_key is not None and args.delivery is None:
        ap.error("--source-key needs --delivery")
    if args.self_test:
        return self_test()
    try:
        raw = stdin if stdin is not None else sys.stdin.buffer.read()
        return _run(args, Path(root) if root is not None else REPO_ROOT, raw)
    except EnvError as exc:
        print(f"error: {exc}", file=sys.stderr)
        if exc.cleanup == "temp-cleanup-failed":
            print("error: temp-cleanup-failed", file=sys.stderr)
        print("result: ERROR")
        return 2
    except Exception as exc:  # noqa: BLE001 - never disclose row text through an unexpected exception
        print("error: internal", file=sys.stderr)
        if getattr(exc, "cleanup", None) == "temp-cleanup-failed":
            print("error: temp-cleanup-failed", file=sys.stderr)
        print("result: ERROR")
        return 2


SELF_TEST_LEDGER = (
    "# Open findings\n"
    "\n"
    "## Disposition values\n"
    "```\n"
    "| 2026-10-01 | error | [FENCED-1] a fenced example | probe |  |\n"
    "```\n"
    "\n"
    "## Open\n"
    "\n"
    "| Found | Severity | Finding | Source | Disposition |\n"
    "| --- | --- | --- | --- | --- |\n"
    "| 2026-10-02 | warning | [OPEN-A] first open | probe | ROUTED 3b330 |\n"
    "| 2026-10-05 | error | [OPEN-B] newest open | probe | ROUTED TODO 3.73 |\n"
    "| 2026-10-03 | note | [OPEN-C] an older note after it | probe |  |\n"
    "\n"
    "## Closed today\n"
    "\n"
    "| Found | Severity | Finding | Source | Disposition |\n"
    "| --- | --- | --- | --- | --- |\n"
    "| 2026-10-04 | error | [CLOSED-A] closed row | probe | FIXED #2700 [class-exempt: singleton] |\n"
    "\n"
    "## 2026-09-30 archive\n"
    "\n"
    "| 2026-09-30 | warning | [ARCH-A] archived row | probe | FIXED #2600 [class-exempt: singleton] |\n"
)


def self_test() -> int:
    import tempfile

    cases, fails = 0, []

    def ck(name, got, want):
        nonlocal cases
        cases += 1
        if got != want:
            fails.append(f"{name}: {got!r} != {want!r}")
        print(f"  {'PASS' if got == want else 'FAIL'}: {name}")

    hook = load_hook(REPO_ROOT)

    def row(disp, sev="error", fid="NEW-1", finding="a finding"):
        return f"| 2026-10-13 | {sev} | [{fid}] {finding} | probe | {disp} |"

    def codes(disp, sev="error", allow_open=False, fid="NEW-1", finding="a finding", want_id="NEW-1"):
        return check_row(hook, row(disp, sev, fid, finding), want_id, allow_open=allow_open)[0]

    # mistakes register 95 forms and the d44d9b2b short SHA: the guard rejects each, so the tool does.
    for bad in ("FIXED (d44d9b2b)", "FIXED (pending merge)", "ROUTED pending-decisions", "FIXED d44d9b2b"):
        ck(f"rejected form: {bad}", codes(bad), ["disposition-invalid"])
    ck("FIXED (#1178) with a clause is accepted (control)", codes("FIXED (#1178) [class-exempt: singleton]"), [])
    ck("stated residue: a letter-series-shaped short SHA passes", codes("FIXED 1b2e3a4 [class-exempt: singleton]"), [])
    ck("an empty error disposition needs --open", codes(""), ["disposition-empty"])
    ck("--open admits an empty error disposition", codes("", allow_open=True), [])
    ck("--open admits an empty warning disposition", codes("", sev="warning", allow_open=True), [])
    ck("--open does not admit an invalid disposition", codes("pending", allow_open=True), ["disposition-invalid"])
    ck("a note disposition is not grammar-checked", codes("pending", sev="note"), [])
    ck("a note row's columns are still checked", codes("a | b", sev="note"), ["malformed-columns"])
    ck("a note row's clause count is still checked",
       codes("FIXED #1 [class-exempt: singleton] [class-exempt: cross-repo]", sev="note"), ["class-multi"])
    ck("a FIXED class row with no clause", codes("FIXED #1"), ["class-unattested"])
    ck("an off-set exemption reason", codes("FIXED #1 [class-exempt: too-hard]"), ["class-bad-exempt"])
    ck("two clauses on a FIXED row", codes('FIXED #1 [class: "x" @ 1] [class-exempt: singleton]'), ["class-multi"])
    ck("two clauses on a ROUTED row (one clause per row)",
       codes("ROUTED 3b330 [class-exempt: singleton] [class-exempt: cross-repo]"), ["class-multi"])
    ck("an invalid exempt does not hide multiple clauses",
       codes("ROUTED 3b330 [class-exempt: bad] [class-exempt: singleton]"), ["class-multi"])
    ck("an attested FIXED class row", codes('FIXED #1 [class: "x" @ 1]'), [])
    ck("an unescaped pipe shifts the columns", codes("ROUTED 3b330", finding="a | b"), ["malformed-columns"])
    ck("an escaped pipe keeps the columns", codes("ROUTED 3b330", finding="a \\| b"), [])
    ck("a severity outside the vocabulary", codes("ROUTED 3b330", sev="eror"), ["severity-unknown"])
    ck("an id that is not the leading token", codes("ROUTED 3b330", want_id="OTHER"), ["id-not-in-row"])
    ck("an id that is not token-shaped", codes("ROUTED 3b330", want_id="a b"), ["id-invalid"])
    ck("a header row is not a row", check_row(hook, "| Found | Severity | Finding | Source | Disposition |",
                                              "NEW-1", allow_open=False)[0], ["malformed-columns"])
    ck("stdin: two lines", decode_row(b"| a |\n| b |\n")[1], ["multiline"])
    ck("stdin: a CR", decode_row(b"| a \r b |\n")[1], ["bad-line-char"])
    ck("stdin: U+2028", decode_row("| a \u2028 b |".encode())[1], ["bad-line-char"])
    ck("stdin: not UTF-8", decode_row(b"| \xff |")[1], ["not-utf8"])
    ck("stdin: one line, one LF", decode_row(b"| a |\n"), ("| a |", []))

    def ev(text, disp="ROUTED 3b330", after=None, allow_open=False, fid="NEW-1", sev="error", probe=None):
        return evaluate(hook, text, row(disp, sev, fid), fid, after_id=after, allow_open=allow_open, probe=probe)

    led = SELF_TEST_LEDGER
    refusals, report, new = ev(led)
    ck("append: no refusal", refusals, [])
    ck("append: after the newest dated Open row, not the last one", "insert: line 14 (open)" in report, True)
    ck("append: the row lands on line 14", new.splitlines()[13], row("ROUTED 3b330"))
    ck("append: merge guard stays allow", "merge-guard: before allow, after allow" in report, True)
    tie = led.replace("| 2026-10-03 | note |", "| 2026-10-05 | note |")
    ck("append: a date tie goes to the last in file order", "insert: line 15 (open)" in ev(tie)[1], True)
    refusals, report, _ = ev(led, after="CLOSED-A")
    ck("--after a Closed-today row", (refusals, "insert: line 21 (closed)" in report), ([], True))
    ck("--open row may not land in Closed today",
       ev(led, disp="", after="CLOSED-A", allow_open=True)[0], ["open-row-in-closed"])
    ck("a fenced line is never an anchor", ev(led, after="FENCED-1")[0], ["anchor-not-found"])
    hdr = led.replace("| Found | Severity | Finding |", "| Date | Level | [Finding] |")
    ck("a header row the guard parses is never an anchor", ev(hdr, after="Finding")[0], ["anchor-not-found"])
    twice = led.replace("[OPEN-C]", "[OPEN-A]")
    ck("an anchor on two rows", ev(twice, after="OPEN-A")[0], ["anchor-ambiguous (line 14)"])
    for fid, n in (("OPEN-A", 12), ("CLOSED-A", 20), ("ARCH-A", 24)):
        ck(f"duplicate id {fid}", ev(led, fid=fid)[0], [f"duplicate-id (line {n})"])
    ck("a fenced id is not a duplicate", ev(led, fid="FENCED-1")[0], [])
    empty = led.split("| 2026-10-02")[0] + "\n## Closed today\n"
    ck("append with no dated Open row", ev(empty)[0], ["no-dated-open-row"])
    refusals, report, _ = ev(led, disp="", allow_open=True)
    ck("--open: written, the block is reported",
       (refusals, "merge-guard: before allow, after block (this row, admitted by --open)" in report), ([], True))
    refusals, report, _ = ev(led, disp="", sev="warning", allow_open=True)
    ck("--open warning surfaces without blocking",
       (refusals, "merge-guard: before allow, after allow" in report), ([], True))
    blocked = led.replace("ROUTED TODO 3.73", "")
    refusals, report, _ = ev(blocked)
    ck("an existing block is reported, not refused",
       (refusals, "merge-guard: before block, after block (existing block, reported only)" in report), ([], True))
    for name, bad in (("U+2028", led.replace("first open", "first\u2028open")),
                      ("mixed CRLF", led.replace("\n", "\r\n", 3))):
        try:
            ev(bad)
            got = None
        except EnvError as exc:
            got = exc.code
        ck(f"line model diverges: {name}", got, "line-model")
    crlf = led.replace("\n", "\r\n")
    refusals, report, new = ev(crlf)
    ck("a uniform CRLF ledger keeps CRLF", (refusals, new.count("\r\n"), "\n" in new.replace("\r\n", "")),
       ([], crlf.count("\r\n") + 1, False))
    sentinel = "SENTINEL-ROW-TEXT"
    for disp in ("FIXED (pending merge)", "ROUTED 3b330"):
        srow = f"| 2026-10-13 | error | [NEW-1] {sentinel} | {sentinel} | {disp} |"
        refusals, report, _ = evaluate(hook, led, srow, "NEW-1", after_id=None, allow_open=False)
        ck(f"output carries no row text or id ({disp.split()[0]})",
           any(sentinel in s or "NEW-1" in s for s in refusals + report), False)
    ck("class count: grew", class_count_report(hook, "[X] f", 'FIXED #1 [class: "t" @ 2]', lambda _t: (3, 0)),
       "class-count: WARNING reproduced 3 > attested 2 on this checkout (D14 fails on growth; report only)")
    ck("class count: equal", class_count_report(hook, "[X] f", 'FIXED #1 [class: "t" @ 2]', lambda _t: (2, 0)),
       "class-count: reproduced 2 = attested 2")

    def broken(_t):
        raise OSError("no git")
    ck("class count: probe failure is a warning", class_count_report(hook, "[X] f", 'FIXED #1 [class: "t" @ 2]',
                                                                     broken).startswith("class-count: WARNING"), True)

    def sd(text, cell, fid="OPEN-A"):
        return evaluate_disposition(hook, text, cell, fid)

    fixed = "FIXED #2800 [class-exempt: singleton]"
    refusals, report, new = sd(led, fixed)
    ck("set-disposition: no refusal", (refusals, "target: line 12 (open)" in report), ([], True))
    want = led.splitlines()
    want[11] = "| 2026-10-02 | warning | [OPEN-A] first open | probe | " + fixed + " |"
    ck("set-disposition: only the last cell of the target changes", new, "\n".join(want) + "\n")
    ck("set-disposition: a Closed-today row", sd(led, fixed, fid="CLOSED-A")[1][1], "target: line 20 (closed)")
    bare = led.replace("| probe | ROUTED 3b330 |", "| probe | ROUTED 3b330")
    ck("set-disposition: a row with no trailing border pipe", sd(bare, fixed)[2].splitlines()[11],
       "| 2026-10-02 | warning | [OPEN-A] first open | probe | " + fixed)
    for fid in ("NOPE-1", "FENCED-1", "ARCH-A"):
        ck(f"set-disposition: no target row ({fid})", sd(led, fixed, fid=fid)[0], ["id-not-found"])
    ck("set-disposition: two target rows", sd(twice, fixed)[0], ["id-ambiguous (line 14)"])
    ck("set-disposition: an id that is not token-shaped", sd(led, fixed, fid="a b")[0], ["id-invalid"])
    ck("set-disposition: an invalid disposition", sd(led, "FIXED d44d9b2b")[0], ["disposition-invalid"])
    ck("set-disposition: a FIXED class row with no clause", sd(led, "FIXED #2800")[0], ["class-unattested"])
    ck("set-disposition: an unescaped pipe in the cell", sd(led, "ROUTED 3b330 | x")[0], ["malformed-columns"])
    ck("set-disposition: an escaped pipe in the cell", sd(led, "ROUTED 3b330 \\| x")[0], [])
    refusals, _report, new = sd(crlf, fixed)
    ck("set-disposition: a CRLF ledger keeps CRLF", (refusals, new.count("\r\n")), ([], crlf.count("\r\n")))
    for cell in ("FIXED (" + sentinel + ")", "ROUTED 3b330 " + sentinel):
        refusals, report, _ = sd(led, cell)
        ck(f"set-disposition: output carries no cell text or id ({len(refusals)} refusal(s))",
           any(sentinel in s or "OPEN-A" in s for s in refusals + report), False)
    ck("set-disposition stdin: empty", decode_cell(b"\n"), (None, ["disposition-empty"]))
    ck("set-disposition stdin: blank", decode_cell(b" \t\n"), (None, ["disposition-empty"]))
    ck("set-disposition stdin: two lines", decode_cell(b"ROUTED 3b330\nx\n"), (None, ["multiline"]))
    ck("set-disposition stdin: stripped", decode_cell(b" ROUTED 3b330 \n"), ("ROUTED 3b330", []))

    tail = "FINDINGS: 0 ERROR, 1 WARN, 2 NOTE\nVERDICT: SHIP\nVPR-COMPLETE 3b540 f2a53df9f\n"
    totals, parts = parse_delivery(
        hook, "WORKER_STATUS: PASS (rc=0, family=claude)\n# /validate-pr round 2 (REFUTE): 3b540, commit x\n"
        "FINDINGS: 1 ERROR, 0 WARN, 0 NOTE\n" + tail + "```\nFINDINGS: 9 ERROR, 9 WARN, 9 NOTE\n```\n")
    ck("delivery: the last FINDINGS line outside a fence", totals, (0, 1, 2))
    ck("delivery: the key from the delivery", review_key(parts, None),
       ("claude 3b540 /validate-pr round 2 @ f2a53df9f", None))
    ck("delivery: no round heading and no --source-key", review_key(parse_delivery(
        hook, "WORKER_STATUS: PASS (family=claude)\n" + tail)[1], None), (None, "no-round-heading"))
    ck("delivery: a round heading after another heading is a quote", review_key(parse_delivery(
        hook, "WORKER_STATUS: PASS (family=claude)\n## Probes\n# /validate-pr round 1 (REFUTE): 3b540\n"
        + tail)[1], None), (None, "no-round-heading"))
    ck("delivery: a placeholder FINDINGS line does not parse",
       parse_delivery(hook, "FINDINGS: <n> ERROR, <n> WARN, <n> NOTE\n")[0], "findings-line-unparseable")
    totals, parts = parse_delivery(hook, "DRAFT-COMPLETE 3b544\n")
    ck("delivery: no FINDINGS line", (totals, review_key(parts, None)),
       ("no-findings-line", (None, "no-vpr-complete-line")))
    src = led.replace("first open | probe |", "first open | claude 3b540 /validate-pr round 2 @ f2a53df9f |")
    src = src.replace("an older note after it | probe |", "x | gemini 3b540 /validate-pr round 2 @ f2a53df9f |")
    ck("delivery: rows leading with the key", review_rows(hook, src.splitlines(), classify(hook, src.splitlines()),
                                                          "claude 3b540 /validate-pr round 2 @ f2a53df9f"), 1)

    with tempfile.TemporaryDirectory() as d:
        base = Path(d)
        ck("delivery: a missing delivery is UNVERIFIABLE, not a zero",
           delivery_report(hook, led, base / "absent.md", with_row=False),
           "delivery-findings: UNVERIFIABLE (delivery-missing); nothing compared (report only)")
        path = base / "open-findings.md"
        path.write_text(led, encoding="utf-8")
        os.chmod(path, 0o640)
        data, st, acl = read_ledger(path)
        new = ev(led)[2]
        atomic_replace(path, new.encode("utf-8"), st, hashlib.sha256(data).hexdigest(), acl)
        ck("write: content", path.read_text(encoding="utf-8"), new)
        ck("write: gid kept", os.lstat(path).st_gid, st.st_gid)
        ck("write: mode 0640 kept", stat.S_IMODE(os.lstat(path).st_mode), 0o640)
        ck("write: no temp file left", sorted(os.listdir(base)), ["open-findings.md"])
        data, st, acl = read_ledger(path)
        with open(path, "a", encoding="utf-8") as fh:
            fh.write("| 2026-10-13 | note | [RACE] a concurrent row | probe |  |\n")
        raced = path.read_bytes()
        try:
            atomic_replace(path, b"x\n", st, hashlib.sha256(data).hexdigest(), acl)
            got = None
        except EnvError as exc:
            got = exc.code
        ck("write: a change between read and write refuses", got, "ledger-changed")
        ck("write: the raced file is untouched", path.read_bytes(), raced)
        ck("write: no temp file left on refusal", sorted(os.listdir(base)), ["open-findings.md"])
        link = base / "link.md"
        os.symlink(path, link)
        try:
            read_ledger(link)
            got = None
        except EnvError as exc:
            got = exc.code
        ck("a symlinked ledger refuses", got, "ledger-symlink")
        os.unlink(link)
        os.link(path, base / "hard.md")
        try:
            read_ledger(path)
            got = None
        except EnvError as exc:
            got = exc.code
        ck("a hard-linked ledger refuses", got, "ledger-hardlinked")

    if fails:
        print(f"\nopen-findings-row self-test: FAILED ({len(fails)} of {cases})")
        for f in fails:
            print(f"  {f}")
        return 1
    print(f"\nopen-findings-row self-test: OK ({cases}/{cases} passed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
