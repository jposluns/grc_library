#!/usr/bin/env python3
"""Merge tool for jposluns/grc_library_new (3b882): the register row check (P1), then the merge.

The grc_library_new squash merge is to go only through this tool, which refuses unless both
QA rows for the PR are in this repository's own registers in the operational store:

* the /validate-pr row in ``validate-pr/history-grc_library_new.md``;
* the /retro row in ``improvement-log-grc_library_new.md``.

A row is a Markdown table line outside any fenced block that begins with ``|`` and has at least
three cells, whose first cell is an ISO date (ASCII digits, ``YYYY-MM-DD``) and whose second cell
starts with the lead ``#N`` (in the improvement log ``#N (/retro)``), the whole lead not followed
by a digit (of any script), and contains the literal tag ``[repo: grc_library_new]``. So ``#3``
and ``#310`` never stand for ``#31``, a ``[repo: grc_library]`` or
untagged row never counts, and a row quoted inside a fence never counts.

Decision D1: the registers are read only from the operational store found by lint_common's strict
store resolver (``_store_dir(root, strict=True)``: ``$GRC_STORE``, else ``<repo-parent>/private``),
never from the private sibling or the in-repo ``.working/`` fallbacks, and never from a store that
resolves inside the repository. A store or register that is absent, is not what it should be, or
cannot be read or decoded as UTF-8 refuses, naming it.

``--check-rows`` is read-only: it never calls gh, writes no file and makes no network call.

Merge mode (``<PR>``, parts P2a and P2b), after the row check passes, every gh call going
through gh():

0. Part 2c, before any gh call: the admin-merge log pre-flight resolves
   ``merge-bypass-log.md`` with lint_common.resolve_working(strict=True), accepts it only inside
   the operational store (decision D1, as for the registers), reads it and refuses unless it is
   a regular file and not a symlink (the append never follows a final symlink) that this user
   may read and write (os.access on the path itself, nothing is opened for writing), its header
   (the first line that begins with ``|``; a title, prose or a list may come before it) equals
   LOG_HEADER, and its last non-blank line is a table line with no blank line after it, so the
   appended row lands inside the table (part 2d). Then plan section 3: the open-findings check
   refuses while the ledger holds an undispositioned ``error`` finding. The ledger
   ``open-findings.md`` is read once from the operational store and that text is judged by the
   open-findings hook's own parse_open_rows() and decide_exit(), loaded by path: the two calls
   merge-when-green.py's open_findings_block() makes, so the two tools agree on a readable
   ledger. It fails closed here: an absent or unloadable hook, no readable ledger inside the
   operational store, or a ledger the hook cannot parse or judge refuses (merge-when-green.py
   itself allows an absent hook, an unreadable ledger and an unparseable one).
1. ``gh pr view`` must report the PR OPEN on base ``main``, its own number and URL in
   grc_library_new, and a 40-character lowercase hex head SHA, which is pinned from here on.
2. Decision D3: the title must end with the ``(CalVer <v>, README <v>)`` suffix and hold no
   control, line-breaking or format character (Unicode category Cc, Zl, Zp or Cf).
3. Decision D5: the Actions runs for the pinned head SHA are read, and the latest
   ``pull_request`` run of every workflow in REQUIRED_WORKFLOWS, from its own file in
   WORKFLOW_PATHS, must be completed with conclusion success; a pending, failed, missing or
   unreadable result refuses, as does a same-named run from any other workflow file.
4. ``--dry-run`` stops here. Otherwise the PR is squash-merged with an explicit subject
   (``<title> (#N)``) and body, pinned with ``--match-head-commit``, with ``--admin``.
5. The merged commit is read back; any trailer line (Co-authored-by, Signed-off-by or any other),
   a message other than the one sent, or other than one parent fails loudly with ``MERGED BUT``.
6. Decision D2: the admin-merge log row, its PR cell in the tagged form
   ``#N [repo: grc_library_new]``, is printed to standard output (everything else goes to
   standard error), then appended to the log found by the pre-flight with one write to a
   descriptor opened in append mode (never created, never through a final symlink), and the
   file is read back: its last line must equal the row. A failed append or read-back exits 3
   and prints the row to standard error, to be added by hand. ``--dry-run`` and
   ``--check-rows`` never write. In each cell every backslash and every pipe is escaped with a
   backslash, and every line-breaking, other control or format character (category Cf, such
   as a bidi override or a zero-width space) becomes a space, so the row is always one line
   of six cells and shows what it holds.

Usage:
    python3 tools/merge-grc-library-new.py <PR> [--dry-run]
    python3 tools/merge-grc-library-new.py --check-rows <PR>
    python3 tools/merge-grc-library-new.py --self-test

Exit codes: 0 both rows present, the dry run passed, the merge read back clean and its log row
was appended, or the self-test passed; 1 refused (a row is missing, the PR state, head, title or CI
does not allow a merge, or an undispositioned error finding is open); 2 usage error, the store, a
register, the admin-merge log or the open-findings ledger cannot be found, read or accepted, the
open-findings check cannot be loaded, or a gh call failed (before the merge, or the merge call
itself, whose state must then be read before any retry); 3 merged but the read-back of the merge
commit, or the append or read-back of the log row, failed.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import os
import re
import shlex
import subprocess
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent

REPO_TAG = "[repo: grc_library_new]"
# (name, store-relative path, the row's QA kind) in report order.
REGISTERS = (
    ("validate-pr", "validate-pr/history-grc_library_new.md", "/validate-pr"),
    ("retro", "improvement-log-grc_library_new.md", "/retro"),
)
_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", re.ASCII)
_PR_ARG = re.compile(r"[1-9][0-9]{0,5}", re.ASCII)
# A CommonMark fence line: up to three spaces, then three or more backticks or tildes.
_FENCE = re.compile(r" {0,3}(`{3,}|~{3,})")

MERGE_REPO = "jposluns/grc_library_new"
PR_URL = "https://github.com/" + MERGE_REPO + "/pull/{pr}"
VIEW_FIELDS = "number,title,state,headRefOid,baseRefName,url"
# Decision D5: the workflows in grc_library_new whose latest run on the pinned head must have
# concluded success: both workflow names a grc_library_new head must pass (3b882 P2b).
REQUIRED_WORKFLOWS = ("Repository quality checks", "Pull request attribution")
# Each required workflow counts only from its own workflow file, as gh api lists them for
# grc_library_new, and only from a pull_request run; a same-named run from another file refuses
# (evaluate_runs in merge-when-green.py binds the same way).
WORKFLOW_PATHS = {"Repository quality checks": ".github/workflows/quality.yml",
                  "Pull request attribution": ".github/workflows/pr-attribution.yml"}
CI_EVENT = "pull_request"
# Decision D2: the admin-merge log's header; the row printed has one cell per column.
LOG_HEADER = "| Date (UTC) | PR | CI state at merge | Mechanism | Justification | Change |"
# Part 2c: the store-relative admin-merge log (gate 50 Check 6 reads the same file), the
# open-findings ledger, and the hook whose decision functions judge it.
LOG_REL = "merge-bypass-log.md"
LEDGER_REL = "open-findings.md"
HOOK_REL = Path(".claude") / "hooks" / "block-on-open-findings.py"
READBACK_ATTEMPTS = 5
READBACK_DELAY = 2
_HEAD = re.compile(r"[0-9a-f]{40}", re.ASCII)
# Decision D3: the suffix used in recent grc_library titles, "(CalVer 2026.11.68, README 1.11.918)".
_TITLE = re.compile(r"[^\n]* \(CalVer [0-9]{4}\.[0-9]{1,2}\.[0-9]{1,4}, "
                    r"README [0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,5}\)", re.ASCII)
_TRAILER = re.compile(r"[A-Za-z][A-Za-z0-9-]*:[ \t]+\S", re.ASCII)


class RegisterError(Exception):
    """The store or a register cannot be found or read; the message names it."""


def _table_rows(text: str):
    """Yield the cells of each table line outside fenced blocks.

    A fence opens on a fence line and closes on a line of the same character, at least as long,
    with nothing after it but spaces or tabs; an unclosed fence runs to the end of the text. A
    table line begins with ``|`` (no indentation) and has at least three cells."""
    fence = None
    for line in text.split("\n"):
        line = line.rstrip("\r")
        match = _FENCE.match(line)
        if fence is not None:
            if (match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence)
                    and not line[match.end():].strip(" \t")):
                fence = None
            continue
        if match:
            fence = match.group(1)
            continue
        if not line.startswith("|"):
            continue
        cells = line.split("|")[1:]
        if line.rstrip(" \t").endswith("|"):
            cells = cells[:-1]
        if len(cells) >= 3:
            yield [c.strip() for c in cells]


def row_present(text: str, pr: int, *, retro: bool) -> bool:
    """Whether ``text`` holds a dated table row for grc_library_new PR ``pr``.

    The second cell must start with the lead, ``#<pr>``, or ``#<pr> (/retro)`` when ``retro``.
    The digit check sits after the whole lead: no digit (of any script) may follow ``#<pr>``, or
    follow ``(/retro)`` when ``retro``. The cell must also contain the
    ``[repo: grc_library_new]`` tag."""
    lead_text = f"#{pr} (/retro)" if retro else f"#{pr}"
    lead = re.compile(re.escape(lead_text) + r"(?!\d)")  # the digit check after the whole lead
    for cells in _table_rows(text):
        if _DATE.fullmatch(cells[0]) and lead.match(cells[1]) and REPO_TAG in cells[1]:
            return True
    return False


def missing_rows(validate_text: str, retro_text: str, pr: int) -> list[str]:
    """The names of the rows absent for PR ``pr``, from ``"validate-pr"`` and ``"retro"`` in that
    order: an empty list means both registers hold the PR's row."""
    missing = []
    if not row_present(validate_text, pr, retro=False):
        missing.append("validate-pr")
    if not row_present(retro_text, pr, retro=True):
        missing.append("retro")
    return missing


def find_store(root: Path) -> Path:
    """The operational store by lint_common's strict resolver, or :class:`RegisterError`.

    Only ``_store_dir(root, strict=True)`` is consulted (decision D1): the private sibling and the
    in-repo ``.working/`` fallbacks of ``resolve_working`` are never probed or read."""
    if str(TOOLS_DIR) not in sys.path:
        sys.path.append(str(TOOLS_DIR))
    import lint_common

    try:
        store = lint_common._store_dir(root.resolve(), strict=True)
    except lint_common.InaccessiblePath as exc:
        raise RegisterError(f"operational store {exc.filename}: {exc.strerror}") from exc
    if store is None:
        where = os.environ.get("GRC_STORE") or str(root.resolve().parent / "private")
        raise RegisterError(
            f"operational store {where}: absent, or inside the repository; set GRC_STORE to the "
            "operational store (the sibling and in-repo .working/ fallbacks are never read)")
    return store


def read_register(store: Path, rel: str) -> str:
    """The text of ``<store>/<rel>``, or :class:`RegisterError` naming it."""
    if str(TOOLS_DIR) not in sys.path:
        sys.path.append(str(TOOLS_DIR))
    import lint_common

    path = store / rel
    try:
        kind = lint_common.strict_kind_under(store, rel)
    except lint_common.InaccessiblePath as exc:
        raise RegisterError(f"{path}: {exc.strerror}") from exc
    if kind is None:
        raise RegisterError(f"{path}: absent")
    if kind != "file":
        raise RegisterError(f"{path}: not a regular file ({kind})")
    try:
        if not path.resolve().is_relative_to(store.resolve()):
            raise RegisterError(f"{path}: resolves outside the operational store")
        return path.read_text(encoding="utf-8")
    except (OSError, RuntimeError, UnicodeDecodeError) as exc:
        raise RegisterError(f"{path}: cannot be read: {exc}") from exc


def resolve_in_store(root: Path, rel: str, what: str) -> Path:
    """``rel`` by lint_common.resolve_working(strict=True), accepted only as ``<store>/<rel>``
    resolving inside the operational store (decision D1), or :class:`RegisterError` naming it."""
    if str(TOOLS_DIR) not in sys.path:
        sys.path.append(str(TOOLS_DIR))
    import lint_common

    store = find_store(root)
    try:
        path = lint_common.resolve_working(rel, repo_root=root.resolve(), strict=True)
    except lint_common.InaccessiblePath as exc:
        raise RegisterError(f"{what} ({rel}) {exc.filename}: {exc.strerror}") from exc
    if path is None:
        raise RegisterError(f"{what} {store / rel}: absent from the operational store")
    try:
        inside = path == store / rel and path.resolve().is_relative_to(store.resolve())
    except (OSError, RuntimeError) as exc:
        raise RegisterError(f"{what} {path}: cannot be resolved: {exc}") from exc
    if not inside:
        raise RegisterError(f"{what} {path}: outside the operational store {store} (the sibling "
                            "and in-repo .working/ fallbacks are never used)")
    return path


def read_in_store(path: Path, what: str) -> str:
    """The UTF-8 text of the regular file ``path``, or :class:`RegisterError` naming it."""
    try:
        if not path.is_file():
            raise RegisterError(f"{what} {path}: not a regular file")
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise RegisterError(f"{what} {path}: cannot be read: {exc}") from exc


def log_shape_problem(text: str) -> str:
    """Part 2d items 1 and 2: "" when ``text`` has the admin-merge log's shape, else the problem.

    The header is the first line that begins with ``|`` (a title, a licence line, prose or a list
    may come before it) and must equal LOG_HEADER. The last non-blank line must be a table line
    with no blank line after it, so a row appended to the file lands inside the table."""
    lines = text.split("\n")
    header = next((line for line in lines if line.startswith("|")), None)
    if header is None:
        return "no table header line (no line begins with |)"
    if header != LOG_HEADER:
        return f"header line {header!r} is not {LOG_HEADER!r}"
    body = lines[:-1] if lines[-1] == "" else lines
    filled = [i for i, line in enumerate(body) if line.strip()]
    last = body[filled[-1]]
    if not last.startswith("|"):
        return (f"last non-blank line {last!r} is not a table line, so an appended row would "
                "land outside the table")
    if filled[-1] != len(body) - 1:
        return ("a blank line follows the last table line, so an appended row would land "
                "outside the table")
    return ""


def log_preflight(root: Path) -> Path:
    """Parts 2c and 2d: the admin-merge log inside the operational store (D1), a regular file and
    not a symlink, that this user may read and write, with the shape log_shape_problem() accepts;
    or :class:`RegisterError` naming it. append_log_row() opens the log for reading and writing
    with O_NOFOLLOW, so a final-component symlink (even to a file inside the store) or a file
    this user cannot read and write would be refused only after the merge: both refuse here.
    os.access runs on the path itself, and nothing is opened for writing."""
    import stat

    path = resolve_in_store(root, LOG_REL, "admin-merge log")
    try:
        info = os.lstat(path)
    except OSError as exc:
        raise RegisterError(f"admin-merge log {path}: cannot be examined: {exc}") from exc
    if stat.S_ISLNK(info.st_mode):
        raise RegisterError(f"admin-merge log {path}: a symlink, which the append never follows "
                            "(O_NOFOLLOW), so the row could not be appended after the merge")
    text = read_in_store(path, "admin-merge log")
    try:
        writable = os.access(path, os.R_OK | os.W_OK)
    except OSError as exc:
        raise RegisterError(f"admin-merge log {path}: cannot be examined: {exc}") from exc
    if not writable:
        raise RegisterError(f"admin-merge log {path}: not writable by this user (the append opens "
                            "it for reading and writing), so the row could not be appended after "
                            "the merge")
    problem = log_shape_problem(text)
    if problem:
        raise RegisterError(f"admin-merge log {path}: {problem}")
    return path


def _log_last_line(path: Path) -> str | None:
    """The last line of the log as read back from disk."""
    lines = path.read_bytes().decode("utf-8").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return lines[-1] if lines else None


def append_log_row(path: Path, row: str) -> str:
    """Part 2c item 2: append ``row`` to the log with one write to a descriptor opened in append
    mode (never created, never through a final symlink), then read the file back. Returns "" when
    the last line equals ``row``, else the problem. A newline goes first when the file lacks one."""
    import stat

    data = row.encode("utf-8") + b"\n"
    try:
        fd = os.open(path, os.O_RDWR | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0))
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode):
                return f"append to {path} refused: not a regular file"
            if info.st_size:
                os.lseek(fd, -1, os.SEEK_END)
                if os.read(fd, 1) != b"\n":
                    data = b"\n" + data
            written = os.write(fd, data)
        finally:
            os.close(fd)
    except OSError as exc:
        return f"append to {path} failed: {exc}"
    if written != len(data):
        return f"append to {path} wrote {written} of {len(data)} bytes"
    try:
        last = _log_last_line(path)
    except (OSError, UnicodeDecodeError) as exc:
        return f"read-back of {path} failed: {exc}"
    if last != row:
        return f"read-back of {path}: its last line is {last!r}, not the row"
    return ""


def check_rows(pr: int, *, root: Path = REPO_ROOT) -> tuple[int, list[str]]:
    """Read both registers from the operational store and check PR ``pr``'s rows.

    Returns ``(exit code, report lines)``: 0 with both matched paths; 2 naming the store, or each
    register that cannot be read; 1 naming each register whose row is missing."""
    try:
        store = find_store(root)
    except RegisterError as exc:
        return 2, [f"REFUSED: {exc}"]
    texts, errors = {}, []
    for name, rel, _kind in REGISTERS:
        try:
            texts[name] = read_register(store, rel)
        except RegisterError as exc:
            errors.append(f"REFUSED: {name} register unreadable: {exc}")
    if errors:
        return 2, errors
    missing = missing_rows(texts["validate-pr"], texts["retro"], pr)
    lines = [f"REFUSED: missing {kind} row for #{pr} {REPO_TAG} in {store / rel}"
             for name, rel, kind in REGISTERS if name in missing]
    if lines:
        return 1, lines
    return 0, [f"rows present for #{pr} {REPO_TAG}: {kind} in {store / rel}"
               for _name, rel, kind in REGISTERS]


def gh(*args: str) -> str:
    """Run gh and return its stdout; the one seam for every gh call (stubbed in tests).

    As in merge-when-green.py: stderr is captured, so a failure carries it in the raised
    CalledProcessError; after a success it is passed through."""
    done = subprocess.run(["gh", *args], text=True, capture_output=True)
    if done.returncode != 0:
        raise subprocess.CalledProcessError(done.returncode, done.args, done.stdout, done.stderr)
    if done.stderr:
        sys.stderr.write(done.stderr)
    return done.stdout


def _describe(exc: BaseException) -> str:
    detail = getattr(exc, "stderr", None)
    if isinstance(detail, str) and detail.strip():
        return f"{exc}: {detail.strip()}"
    return str(exc)


def title_has_suffix(title: str) -> bool:
    """Decision D3: the title ends with " (CalVer <v>, README <v>)" (ASCII digits, one line). A
    title holding any control, line-breaking or format character (Unicode category Cc, Zl, Zp
    or Cf: a newline, carriage return, vertical tab, form feed, NEL, U+2028 or U+2029 (3b882 fix
    round 7), and a bidi override or isolate such as U+202E or U+2066, a zero-width space
    U+200B, a byte order mark U+FEFF or a soft hyphen U+00AD (3b882 fix round 8) among them) is
    refused, so the squash subject and the admin-merge log row show what they hold."""
    return (isinstance(title, str) and _TITLE.fullmatch(title) is not None
            and not any(unicodedata.category(c) in ("Cc", "Zl", "Zp", "Cf") for c in title))


def message_trailers(message: str) -> list[str]:
    """The lines after the subject shaped like a trailer, or naming Co-authored-by in any case."""
    found = []
    for line in message.split("\n")[1:]:
        line = line.rstrip("\r")
        if _TRAILER.match(line) or "co-authored-by" in line.casefold():
            found.append(line)
    return found


RUNS_PER_PAGE = 100
RUNS_MAX_PAGES = 50


def read_runs(head: str, gh) -> tuple[int, list[str], str]:
    """Decision D5: every page of ``actions/runs?head_sha=<head>``, RUNS_PER_PAGE runs a page
    (3b882 fix round 5: a head with more runs than one page holds is read in full), joined into
    one ``{"total_count", "workflow_runs"}`` JSON text for ci_check(). ``(0, [], text)`` once
    the runs read reach total_count; ``(2, [problem], "")`` when a page cannot be read, is not a
    list of run objects with a non-negative integer total_count, holds more than RUNS_PER_PAGE
    runs, reports a total_count other than page 1's, repeats a run id, brings the runs read past
    total_count, ends early (fewer than RUNS_PER_PAGE runs before total_count is reached) or
    when RUNS_MAX_PAGES pages do not reach total_count. A short or inconsistent read refuses;
    part of the list is never judged."""
    runs, ids, total = [], set(), None
    for page in range(1, RUNS_MAX_PAGES + 1):
        where = f"Actions runs for {head} page {page}"
        try:
            text = gh("api", f"repos/{MERGE_REPO}/actions/runs?head_sha={head}"
                             f"&per_page={RUNS_PER_PAGE}&page={page}")
        except (subprocess.CalledProcessError, OSError) as exc:
            return 2, [f"{where} unreadable: {_describe(exc)}"], ""
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            return 2, [f"{where} unreadable: {exc}"], ""
        listed = data.get("workflow_runs") if isinstance(data, dict) else None
        if not isinstance(listed, list) or not all(isinstance(r, dict) for r in listed):
            return 2, [f"{where} unreadable: no list of run objects"], ""
        count = data.get("total_count")
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            return 2, [f"{where} unreadable: total_count {count!r}"], ""
        if total is None:
            total = count
        elif count != total:
            return 2, [f"{where} inconsistent: total_count {count}, page 1 gave {total}"], ""
        if len(listed) > RUNS_PER_PAGE:
            return 2, [f"{where} malformed: {len(listed)} runs, more than {RUNS_PER_PAGE}"], ""
        for r in listed:
            run_id = r.get("id")
            if isinstance(run_id, int) and not isinstance(run_id, bool):
                if run_id in ids:
                    return 2, [f"{where} inconsistent: run {run_id} listed twice"], ""
                ids.add(run_id)
        runs.extend(listed)
        if len(runs) > total:
            return 2, [f"{where} inconsistent: {len(runs)} runs read, total_count {total}"], ""
        if len(runs) == total:
            return 0, [], json.dumps({"total_count": total, "workflow_runs": runs})
        if len(listed) < RUNS_PER_PAGE:
            return 2, [f"{where} incomplete: the page ended after {len(listed)} runs with "
                       f"{len(runs)} of total_count {total} read"], ""
    return 2, [f"Actions runs for {head} incomplete: {len(runs)} of total_count {total} read "
               f"in {RUNS_MAX_PAGES} pages"], ""


def run_record_problem(r: dict) -> str:
    """3b882 fix round 6: "" when the run ``r`` has a positive integer id and a created_at that
    parses as a time with a zone, else the problem. ci_check() orders a workflow's runs by these
    two, so a record missing either cannot be placed and refuses."""
    run_id = r.get("id")
    if not isinstance(run_id, int) or isinstance(run_id, bool) or run_id < 1:
        return f"id {run_id!r} is not a positive integer"
    created = r.get("created_at")
    try:
        when = datetime.fromisoformat(created[:-1] + "+00:00" if created.endswith("Z")
                                      else created)
    except (AttributeError, TypeError, ValueError):
        return f"created_at {created!r} is not a parseable timestamp"
    if when.tzinfo is None:
        return f"created_at {created!r} has no time zone"
    return ""


def _run_order(r: dict) -> tuple[datetime, int]:
    """The ordering key of a run that run_record_problem() accepted."""
    created = r["created_at"]
    when = datetime.fromisoformat(created[:-1] + "+00:00" if created.endswith("Z") else created)
    return when, r["id"]


def ci_check(text: str, head: str) -> tuple[int, list[str], dict]:
    """Decision D5 on the ``actions/runs?head_sha=`` JSON: ``(0, [], {name: run id})`` when the
    latest ``pull_request`` run on ``head`` of every required workflow, from its own file in
    WORKFLOW_PATHS, completed with success; 1 naming each workflow whose run is missing, pending
    or not successful, or that is also reported from another workflow file (a name collision:
    only its own file may satisfy it, as in merge-when-green.py's evaluate_runs); 2 when the list
    cannot be read or is incomplete, or (3b882 fix round 6) when a ``pull_request`` run of a
    required workflow on ``head`` lacks a positive integer id or a parseable created_at with a
    zone: such a run cannot be ordered, so it refuses instead of sorting as oldest."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return 2, [f"Actions runs for {head} unreadable: {exc}"], {}
    runs = data.get("workflow_runs") if isinstance(data, dict) else None
    if not isinstance(runs, list) or not all(isinstance(r, dict) for r in runs):
        return 2, [f"Actions runs for {head} unreadable: no list of run objects"], {}
    total = data.get("total_count")
    if not isinstance(total, int) or isinstance(total, bool) or total > len(runs):
        return 2, [f"Actions runs for {head} incomplete: total_count {total!r}, "
                   f"{len(runs)} listed"], {}
    problems, green, malformed_seen = [], {}, False
    for name in REQUIRED_WORKFLOWS:
        path = WORKFLOW_PATHS[name]
        named = [r for r in runs if r.get("name") == name]
        foreign = [r for r in named if r.get("path") != path]
        if foreign:
            problems.append(f"required workflow {name!r} is also reported from "
                            f"{foreign[0].get('path')!r}, not only {path!r} (a name collision); "
                            "only its own file may satisfy it")
            continue
        mine = [r for r in named if r.get("head_sha") == head and r.get("event") == CI_EVENT]
        if not mine:
            problems.append(f"required workflow {name!r}: no {CI_EVENT} run from {path} on {head}")
            continue
        malformed = [(r, run_record_problem(r)) for r in mine if run_record_problem(r)]
        if malformed:
            for r, why in malformed:
                problems.append(f"required workflow {name!r}: run record on {head} is malformed "
                                f"({why}); it cannot be ordered, so the merge is refused")
            malformed_seen = True
            continue
        latest = max(mine, key=_run_order)
        if latest.get("status") != "completed" or latest.get("conclusion") != "success":
            problems.append(f"required workflow {name!r}: latest run {latest.get('id')} on {head} "
                            f"is {latest.get('status')}/{latest.get('conclusion')}")
        else:
            green[name] = latest.get("id")
    if malformed_seen:
        return 2, problems, {}
    return (1 if problems else 0), problems, green


def open_findings(root: Path, ledger=None) -> tuple[int, str]:
    """Plan section 3: ``(exit code, message)`` from the open-findings hook's own decision.

    The ledger is read once and that text is judged by the hook's parse_open_rows() and
    decide_exit(), loaded by path: the two calls merge-when-green.py's open_findings_block()
    makes, so the two merge tools agree on a readable ledger. The ledger is never read a second
    time (open_findings_block rereads it and allows on any read or parse error). 1 means an
    undispositioned ``error`` finding (or a mis-filed finding row) is open. Part 2c item 3: the
    check fails closed with 2: the hook absent or not loadable, no readable ledger (``ledger``
    when given, else ``open-findings.md`` inside the operational store, decision D1), or a
    ledger the hook cannot parse or judge."""
    hook = Path(root) / HOOK_REL
    if not hook.is_file():
        return 2, f"the open-findings hook {hook} is absent; refusing to merge unchecked"
    try:
        spec = importlib.util.spec_from_file_location("_mgln_open_findings_hook", hook)
        hook_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(hook_mod)
        hook_mod.parse_open_rows, hook_mod.decide_exit  # noqa: B018 - both must exist
    except Exception as exc:  # noqa: BLE001 - any load failure refuses
        return 2, (f"the open-findings hook {hook} could not be loaded ({exc}); refusing to merge "
                   "unchecked")
    try:
        if ledger is None:
            ledger = resolve_in_store(Path(root), LEDGER_REL, "open-findings ledger")
        text = read_in_store(Path(ledger), "open-findings ledger")
    except RegisterError as exc:
        return 2, f"{exc}; refusing to merge unchecked"
    err = io.StringIO()
    try:
        rows = hook_mod.parse_open_rows(text)
        with contextlib.redirect_stderr(err):
            code = hook_mod.decide_exit(rows, text)
    except Exception as exc:  # noqa: BLE001 - any parse or decision failure refuses
        return 2, (f"the open-findings ledger {ledger} could not be parsed or judged ({exc}); "
                   "refusing to merge unchecked")
    return (1 if code else 0), err.getvalue().strip()


def _cell(text: str) -> str:
    """One log-row cell: a backslash or pipe is escaped (GFM reads only an unescaped pipe as a
    cell boundary, so a bare backslash before a pipe would otherwise unescape it), and every
    control or line-separator character, all that str.splitlines() breaks on included, and
    every format character (category Cf, such as U+202E or U+200B; 3b882 fix round 8) becomes
    a space."""
    out = []
    for char in str(text):
        if char in "\\|":
            out.append("\\" + char)
        elif unicodedata.category(char) in ("Cc", "Zl", "Zp", "Cf"):
            out.append(" ")
        else:
            out.append(char)
    return "".join(out)


def _read_merge_commit(pr: int, gh, sleep) -> tuple[str | None, str]:
    """Poll for the merge commit OID: ``(oid, "")`` or ``(None, last problem)``."""
    last = "not read"
    for attempt in range(READBACK_ATTEMPTS):
        if attempt:
            sleep(READBACK_DELAY)
        try:
            state = json.loads(gh("pr", "view", str(pr), "--repo", MERGE_REPO, "--json",
                                  "state,mergeCommit"))
        except (subprocess.CalledProcessError, OSError, json.JSONDecodeError) as exc:
            last = f"gh pr view failed: {_describe(exc)}"
            continue
        if not isinstance(state, dict):
            last = f"gh pr view gave {state!r}"
            continue
        commit = state.get("mergeCommit")
        oid = commit.get("oid") if isinstance(commit, dict) else None
        if state.get("state") == "MERGED" and isinstance(oid, str) and _HEAD.fullmatch(oid):
            return oid, ""
        last = f"state {state.get('state')!r}, mergeCommit {commit!r}"
    return None, f"no merge commit after {READBACK_ATTEMPTS} reads ({last})"


def run_merge(pr: int, *, root: Path, gh, dry_run: bool = False, sleep=time.sleep,
              now: datetime | None = None) -> int:
    """Merge mode: the row check, then items (a) to (e) of 3b882 P2a; see the module docstring."""
    def err(line: str) -> None:
        print(line, file=sys.stderr)

    code, lines = check_rows(pr, root=root)
    for line in lines:
        err(line)
    if code:
        return code
    try:
        log_path = log_preflight(root)
    except RegisterError as exc:
        err(f"REFUSED: {exc}")
        return 2
    blocked, why = open_findings(root)
    if blocked:
        err(f"REFUSED: open-findings check: {why}")
        return blocked
    try:
        view = json.loads(gh("pr", "view", str(pr), "--repo", MERGE_REPO, "--json", VIEW_FIELDS))
    except (subprocess.CalledProcessError, OSError, json.JSONDecodeError) as exc:
        err(f"REFUSED: gh pr view {pr} --repo {MERGE_REPO} failed: {_describe(exc)}")
        return 2
    if not isinstance(view, dict):
        err(f"REFUSED: gh pr view {pr} gave {view!r}")
        return 2
    head, title = view.get("headRefOid"), view.get("title")
    problems = []
    if view.get("number") != pr:
        problems.append(f"gh reports PR number {view.get('number')!r}, not {pr}")
    if view.get("state") != "OPEN":
        problems.append(f"PR #{pr} is {view.get('state')!r}, not OPEN")
    if view.get("baseRefName") != "main":
        problems.append(f"PR #{pr} base is {view.get('baseRefName')!r}, not main")
    if view.get("url") != PR_URL.format(pr=pr):
        problems.append(f"PR URL {view.get('url')!r} is not {PR_URL.format(pr=pr)}")
    if not (isinstance(head, str) and _HEAD.fullmatch(head)):
        problems.append(f"head {head!r} is not a 40-character lowercase hex SHA")
    if not title_has_suffix(title):
        problems.append(f"title {title!r} lacks the (CalVer <v>, README <v>) suffix or holds a "
                        "control, line-breaking or format character (decision D3)")
    if problems:
        for line in problems:
            err(f"REFUSED: {line}")
        return 1
    read_code, read_lines, runs_text = read_runs(head, gh)
    if read_code:
        for line in read_lines:
            err(f"REFUSED: {line} (decision D5)")
        return read_code
    ci_code, ci_lines, green = ci_check(runs_text, head)
    if ci_code:
        for line in ci_lines:
            err(f"REFUSED: {line} (decision D5)")
        return ci_code
    subject = f"{title} (#{pr})"
    body = f"Squash merge of #{pr} at {head[:12]}."
    argv = ["pr", "merge", str(pr), "--repo", MERGE_REPO, "--squash", "--subject", subject,
            "--body", body, "--match-head-commit", head, "--admin"]
    command = shlex.join(["gh", *argv])
    if dry_run:
        err(f"DRY RUN: every check passed for #{pr} at {head}; would run: {command}")
        return 0
    try:
        gh(*argv)
    except (subprocess.CalledProcessError, OSError) as exc:
        err(f"MERGE CALL FAILED, merge state unknown: {command}: {_describe(exc)}; read the PR "
            "state before any retry")
        return 2
    oid, missing = _read_merge_commit(pr, gh, sleep)
    failures = [missing] if oid is None else []
    if oid is not None:
        try:
            data = json.loads(gh("api", f"repos/{MERGE_REPO}/commits/{oid}"))
            message, parents = data["commit"]["message"], data["parents"]
            if not isinstance(message, str) or not isinstance(parents, list):
                raise TypeError("commit message or parents of the wrong type")
        except (subprocess.CalledProcessError, OSError, json.JSONDecodeError, KeyError,
                TypeError) as exc:
            failures.append(f"merge commit {oid} unreadable: {_describe(exc)}")
        else:
            trailers = message_trailers(message)
            if trailers:
                failures.append(f"merge commit {oid} carries trailer(s): {'; '.join(trailers)}")
            if message.rstrip("\n") != subject + "\n\n" + body:
                failures.append(f"merge commit {oid} message differs from what was sent: "
                                f"{message!r}")
            if len(parents) != 1:
                failures.append(f"merge commit {oid} has {len(parents)} parents, not 1")
    when = (now or datetime.now(timezone.utc)).strftime("%Y-%m-%d")
    readback = ("clean, no trailer" if not failures else "FAILED: " + "; ".join(failures))
    cells = [
        when,
        f"#{pr} {REPO_TAG}",
        "; ".join(f"{name} completed/success on {head} (run {green[name]})"
                  for name in REQUIRED_WORKFLOWS) + " (merge-grc-library-new.py fail-closed)",
        f"admin squash (merge-grc-library-new.py --admin), head pinned to {head}",
        f"branch protection requires PR review; /validate-pr and /retro rows present for "
        f"#{pr} {REPO_TAG}; no undispositioned error finding; title carries the CalVer and "
        "README suffix",
        f"{title}; merge commit {oid or 'not read'}; read-back {readback}; command: {command}",
    ]
    row = "| " + " | ".join(_cell(c) for c in cells) + " |"
    print(row, flush=True)
    log_problem = append_log_row(log_path, row)
    if failures:
        for line in failures:
            err(f"MERGED BUT {line}")
        err(f"MERGED BUT the read-back of #{pr} failed: a finding row is required; the merge "
            "cannot be undone. The log row above records the failure.")
    if log_problem:
        err(f"MERGED BUT the log row was not written: {log_problem}; add this row to {log_path} "
            "by hand:")
        err(row)
    if failures or log_problem:
        return 3
    err(f"merged #{pr} as {oid}; read-back clean (no trailer, message as sent, one parent); "
        f"log row appended to {log_path} and read back")
    return 0


def self_test() -> int:
    """Exercise the pure row check and the store reads against temporary fixtures only."""
    import tempfile

    v_row = "| 2026-11-14 | #31 [repo: grc_library_new] | train 1 | claude | IDS | done |"
    r_row = "| 2026-11-14 | #31 (/retro) [NEW31-RETRO] [repo: grc_library_new] | t | a | b | c |"
    log_shape = ("# Merge-bypass log\n\n**License:** CC BY-SA 4.0\n\nProse.\n\n- a list item\n\n"
                 + LOG_HEADER + "\n| 2026-11-14 | #3132 | ci | admin squash | why | change |\n")
    cases = [
        ("both rows", missing_rows(v_row, r_row, 31), []),
        ("validate-pr missing", missing_rows("", r_row, 31), ["validate-pr"]),
        ("retro missing", missing_rows(v_row, "", 31), ["retro"]),
        ("#3 is not #31", missing_rows(v_row.replace("#31", "#3"), r_row.replace("#31", "#3"), 31),
         ["validate-pr", "retro"]),
        ("#310 is not #31", missing_rows(v_row.replace("#31", "#310"), r_row.replace("#31", "#310"), 31),
         ["validate-pr", "retro"]),
        ("#31 is not #3", missing_rows(v_row, r_row, 3), ["validate-pr", "retro"]),
        ("fullwidth digits", missing_rows(v_row.replace("#31", "#３１"), r_row, 31),
         ["validate-pr"]),
        ("grc_library tag", missing_rows(v_row.replace(REPO_TAG, "[repo: grc_library]"), r_row, 31),
         ["validate-pr"]),
        ("untagged", missing_rows(v_row.replace(" " + REPO_TAG, ""), r_row, 31), ["validate-pr"]),
        ("retro marker absent", missing_rows(v_row, r_row.replace(" (/retro)", ""), 31), ["retro"]),
        ("fenced rows", missing_rows("```\n" + v_row + "\n```", "~~~\n" + r_row + "\n~~~", 31),
         ["validate-pr", "retro"]),
        ("closed fence", missing_rows("```\nx\n```\n" + v_row, r_row, 31), []),
        ("prose line", missing_rows("Moved #31 " + REPO_TAG + " on 2026-11-14.", r_row, 31),
         ["validate-pr"]),
        ("undated row", missing_rows(v_row.replace("2026-11-14", "PR"), r_row, 31), ["validate-pr"]),
        ("title suffix", title_has_suffix("x (CalVer 2026.11.69, README 1.11.919)"), True),
        ("title without suffix", title_has_suffix("x (CalVer 2026.11.69)"), False),
        ("title with a carriage return", title_has_suffix("x\ry (CalVer 2026.11.69, README 1.11.919)"),
         False),
        ("title with a right-to-left override",
         title_has_suffix("x\u202ey (CalVer 2026.11.69, README 1.11.919)"), False),
        ("title with a zero-width space",
         title_has_suffix("x\u200by (CalVer 2026.11.69, README 1.11.919)"), False),
        ("co-authored trailer", message_trailers("s\n\nb\n\nCo-authored-by: a <b>"),
         ["Co-authored-by: a <b>"]),
        ("clean message", message_trailers("content: s\n\nSquash merge of #31 at abc."), []),
        ("cell escapes backslash and pipe", _cell("a \\| b"), "a \\\\\\| b"),
        ("cell blanks line separators", _cell("a\u2028b\x85c\vd\re"), "a b c d e"),
        ("cell blanks format characters", _cell("a\u202eb\u200bc\ufeffd\u00ade"), "a b c d e"),
        ("log: real shape", log_shape_problem(log_shape), ""),
        ("log: header only", log_shape_problem(LOG_HEADER + "\n"), ""),
        ("log: no table header", "no table header" in log_shape_problem("# t\n\nprose\n"), True),
        # 3b882 fix round 8 (round 7 agy-A F2): a title and a table header, then no table line.
        # The header is the last non-blank line and a table line with no blank line after it, so
        # log_shape_problem accepts it (no problem), as it accepts a header-only log.
        ("log: no table line", log_shape_problem("# t\n\n" + LOG_HEADER + "\n"), ""),
        # 3b882 fix round 6 (round 5 agy-A F3): prose after the header is not a table line.
        ("log: prose after the header",
         "is not a table line" in log_shape_problem("# t\n\n" + LOG_HEADER + "\n\nprose\n"), True),
        ("log: first table line differs",
         "is not" in log_shape_problem("| a | b | c |\n" + log_shape), True),
        ("log: prose after the table",
         "outside the table" in log_shape_problem(log_shape + "prose\n"), True),
        ("log: blank line after the table",
         "outside the table" in log_shape_problem(log_shape + "\n"), True),
    ]
    failures = [f"{name}: got {got}, want {want}" for name, got, want in cases if got != want]
    saved = os.environ.get("GRC_STORE")
    try:
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            root = parent / "repo"
            root.mkdir()
            store = parent / "store"
            (store / "validate-pr").mkdir(parents=True)
            os.environ["GRC_STORE"] = str(store)
            (store / REGISTERS[1][1]).write_text(r_row + "\n", encoding="utf-8")
            store_cases = [("validate-pr register absent", 2)]
            got = [check_rows(31, root=root)[0]]
            (store / REGISTERS[0][1]).write_bytes(b"\xff" + v_row.encode() + b"\n")
            store_cases.append(("invalid UTF-8", 2))
            got.append(check_rows(31, root=root)[0])
            (store / REGISTERS[0][1]).write_text(v_row.replace("#31", "#310") + "\n", encoding="utf-8")
            store_cases.append(("row missing", 1))
            got.append(check_rows(31, root=root)[0])
            (store / REGISTERS[0][1]).write_text(v_row + "\n", encoding="utf-8")
            store_cases.append(("both rows", 0))
            got.append(check_rows(31, root=root)[0])
            os.environ["GRC_STORE"] = str(parent / "absent")
            store_cases.append(("store absent", 2))
            got.append(check_rows(31, root=root)[0])
            os.environ["GRC_STORE"] = str(root)
            store_cases.append(("store inside the repository", 2))
            got.append(check_rows(31, root=root)[0])
            failures += [f"{name}: exit {code}, want {want}"
                         for (name, want), code in zip(store_cases, got) if code != want]
            count = len(cases) + len(store_cases)
    finally:
        if saved is None:
            os.environ.pop("GRC_STORE", None)
        else:
            os.environ["GRC_STORE"] = saved
    if failures:
        for line in failures:
            print("FAIL:", line, file=sys.stderr)
        return 1
    print(f"merge-grc-library-new.py self-test OK ({count} cases)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Merge a grc_library_new PR after its QA rows, title and CI are checked, or "
                    "check its QA register rows only (read-only).")
    parser.add_argument("pr", nargs="?", metavar="PR",
                        help="merge this PR (rows, title, CI, squash merge, read-back, log row)")
    parser.add_argument("--dry-run", action="store_true",
                        help="with PR: run every check and stop before the merge")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check-rows", metavar="PR",
                      help="exit 0 only when both the /validate-pr and /retro rows are present")
    mode.add_argument("--self-test", action="store_true", help="run the built-in self-test")
    args = parser.parse_args(argv)
    chosen = (args.pr is not None) + (args.check_rows is not None) + bool(args.self_test)
    if chosen != 1 or (args.dry_run and args.pr is None):
        print("usage error: give exactly one of PR, --check-rows PR or --self-test; --dry-run "
              "goes only with PR", file=sys.stderr)
        return 2
    if args.self_test:
        return self_test()
    given = args.pr if args.pr is not None else args.check_rows
    if not _PR_ARG.fullmatch(given):
        print(f"usage error: a PR number is 1 to 999999 with no leading zero, got {given!r}",
              file=sys.stderr)
        return 2
    if args.pr is not None:
        return run_merge(int(given), root=REPO_ROOT, gh=gh, dry_run=args.dry_run, sleep=time.sleep)
    code, lines = check_rows(int(args.check_rows))
    for line in lines:
        print(line, file=sys.stderr if code else sys.stdout)
    return code


if __name__ == "__main__":
    sys.exit(main())
