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
    python3 -I tools/open-findings-row.py --id ID --after ANCHOR_ID [--ledger PATH] [--dry-run] [--open] < row
    python3 -I tools/open-findings-row.py --id ID --append [--ledger PATH] [--dry-run] [--open] < row
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
    report = [f"ledger: line-model ok ({'CRLF' if eol == chr(13) + chr(10) else 'LF'}); "
              f"{kinds.count('open')} open row(s), {kinds.count('closed')} closed-today row(s)"]
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
    row, codes = decode_row(raw)
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
    refusals, report, new_text = evaluate(hook, text, row, args.id, after_id=args.after,
                                          allow_open=args.allow_open, probe=make_probe(root))
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
    ap.add_argument("--ledger", type=ledger_path,
                    help="ledger path (default: resolve_working, strict); a value ending in / or /. "
                         "is refused (ledger-path-directory-suffix)")
    ap.add_argument("--dry-run", action="store_true",
                    help="check and report, running the write pre-flight; write nothing")
    ap.add_argument("--open", dest="allow_open", action="store_true",
                    help="admit an error or warning row with an empty disposition")
    ap.add_argument("--self-test", action="store_true", help="run the built-in self-test and exit")
    args = ap.parse_args(argv)
    if not args.self_test and (args.id is None or (args.after is None and not args.append)):
        ap.error("--id and one of --after or --append are required")
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

    with tempfile.TemporaryDirectory() as d:
        base = Path(d)
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
