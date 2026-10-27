#!/usr/bin/env python3
"""TODO index<->reference bijection audit (a backlog-integrity gate).

The TODO-rework format (2026-08) splits the public backlog into an INDEX
([`TODO.md`](../TODO.md): one ``| ID | Item | Tags |`` row per open item, under
``## `` bands, e.g. Priority N) and a DETAIL file
(the private `grc_library_private/TODO-REFERENCE.md`, resolved via the private
sibling since PR #1795 removed the public copy: one ``### <id> <title>`` block per
item, under the same bands). The two surfaces are joined by the stable id, and
the format's whole contract is that they stay in one-to-one correspondence.

Nothing else enforces that correspondence: a codex ``/validate-pr`` showed that
adding an index row with no detail block (or the reverse, or drifting a title,
band, or the row order between the two files) leaves the full audit programme
green. This gate closes that gap. It fails, fail-loud, when the index and the
reference are not a bijection with matching id, title, band, and position order:

  - MISSING: an index-row id with no detail block.
  - EXTRA: a detail-block id with no index row.
  - DUPLICATE: an id appearing twice in either file.
  - TITLE DRIFT: a row and its block disagree on the item title.
  - BAND MISMATCH: a row and its block sit under different ``## `` bands.
  - ORDER MISMATCH: the id sequence differs between the two files.
  - INDEX DETAIL LEAK: a ``### id`` detail-block heading appearing in the
    index file ([`TODO.md`](../TODO.md)) instead of only in the reference file.
  - MALFORMED INDEX ROW: a pipe-starting row inside an index table lacks its
    terminal pipe or exactly three cells, or its first cell is not a valid
    backlog id (a row missing its LEADING pipe is documented residue).

Adopter-graceful: if the private ``grc_library_private/TODO-REFERENCE.md`` is
absent (an adopter clone without the private sibling), the gate is a no-op OK,
and it prints a ``DEGRADED:`` line naming the skipped pair. When the default
lookup does resolve the sibling but it holds neither ``P-TODO.md`` nor
``P-TODO-REFERENCE.md``, it used to pass with no notice, so a mis-resolved or
emptied store read as checked (3b648). The sibling is now classified by what it
holds: an empty directory fails with exit 2 naming it, as likely stray, and says
to remove it or pass ``--private-root``; one holding ``TODO-REFERENCE.md`` but no
P-TODO file fails with exit 2 and says to restore the pair; one holding other
content and none of the three backlog files is a private store without a backlog
(the README's transitional fallback store for ``.working/`` records), so it passes
with an ``OK:`` line naming it and saying private parity was not checked, and the
message never advises renaming it (3b648 r4: the tools reading that store would
break). A resolved sibling is the private store, whoever's checkout it is, so no other
signal is consulted (3b648 r3: the repository origin was dropped as unsound).
A recognised legacy ``P-TODO.md`` alone is the accepted pre-split layout: it
passes with an ``OK:`` line saying private parity was not checked. CI and most
adopters have no sibling, so they take the ``DEGRADED:`` path above and never
reach this check.

``--root DIR`` names a fixture repository and ``--private-root DIR`` its private
store. Under ``--root`` the gate never resolves the real private sibling: the
private files come from ``--private-root`` when given and otherwise from the
root itself, as gates 78 and 81 read ``P-TODO.md``, and no ``DEGRADED:`` line
is printed. An explicit ``--private-root`` declares the private input, so a
directory holding neither ``P-TODO.md`` nor ``P-TODO-REFERENCE.md`` fails with
exit 2 naming the path (check-fails-closed-on-unreadable: a declared resource
that is absent is a failure). Otherwise, when ``--root`` names the private
directory and it holds no P-TODO pair, or either flag names one holding a legacy
``### ``-block ``P-TODO.md`` alone, an informational ``OK:`` line says private
parity was not checked, names the flag and directory, and says why, as gate 81
says ``P-TODO.md`` is not present. Those cases pass: ``--root`` names a fixture
repository that the private lookup only defaults to, and a legacy file is the
accepted pre-split layout; a broken or half-converted pair still fails. A private
directory that cannot be listed, or a candidate file in it that cannot be
examined or opened, fails with exit 2 and names the path: an unreadable store is
not one without the pair. Each file is read once and decoded as strict UTF-8;
undecodable bytes fail with exit 2 naming the path. A present ``P-TODO.md`` must
be positively one of the two forms the gate knows, an index (``| ID | Item |
Tags |`` header) or a legacy file with at least one ``### <id> <title>`` block;
an empty file or one in neither form fails with exit 2 naming the path and the
reason, since the gate cannot tell what it holds. Stdlib-only.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

_TOOLS_DIR = str(Path(__file__).resolve().parent)
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from aiqt_corpus import split_row, is_separator_row, is_fence_line  # noqa: E402  # generic core (behaviour-identical to lint_common)
from lint_common import REPO_ROOT, TODO_ID_RE, print_degraded, require_dir, resolve_sibling, has_todo_index_header, strict_kind  # noqa: E402  # grc-config/store, stays local

TODO_REL = "TODO.md"
REFERENCE_REL = "TODO-REFERENCE.md"
INDEX_TABLE_HEADER = ("ID", "Item", "Tags")
PTODO_INDEX_REL = "P-TODO.md"           # private backlog index (in grc_library_private)
PTODO_REFERENCE_REL = "P-TODO-REFERENCE.md"  # private backlog detail (in grc_library_private)

BAND_RE = re.compile(r"^## (.+?)\s*$")  # any H2 section is a band (Priority N, Time-bounded follow-ups, ...)
REF_HEADING_RE = re.compile(
    r"^### (?P<id>P-\d+(?:\.\d+){1,2}[a-z]?|\d+(?:\.\d+)+(?:\.[a-z]|[a-z])?|TF-\d+)"
    r"\s+(?P<title>.*)$"
)


def _non_fence_lines(text: str):
    """Yield ``(line)`` skipping fenced-code-block INTERIORS, so a ``### id`` or
    ``| id |`` example inside a ``` fence is not mistaken for a real item.
    Fence lines are what the shared ``aiqt_corpus.is_fence_line`` recognizes (a
    marker after at most three spaces of indent, the toggle model gate 66
    certifies; 3b83), so a marker indented four or more columns is content and
    cannot hide the rows after it from this gate."""
    in_fence = False
    for line in text.splitlines():
        if is_fence_line(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield line


def _norm_title(t: str) -> str:
    """Normalize a title for comparison. A literal pipe in a title is NOT
    supported by the index-row format (the row would over-split); such a title
    is rejected loudly by gate 81 (missing tag) / gate 90 (title drift), so
    reword it rather than escaping the pipe."""
    return t.strip()


def parse_index(text: str) -> list[tuple[str, str, str]]:
    """Ordered ``(id, normalized-title, band)`` for each index row in TODO.md."""
    out: list[tuple[str, str, str]] = []
    band = ""
    for line in _non_fence_lines(text):
        m = BAND_RE.match(line)
        if m:
            band = m.group(1).strip()
            continue
        s = line.strip()
        if not (s.startswith("|") and s.endswith("|")):
            continue
        cells = split_row(line)
        if len(cells) < 3 or is_separator_row(cells):
            continue
        item_id = cells[0].strip()
        if not TODO_ID_RE.match(item_id):
            continue
        out.append((item_id, _norm_title(cells[1]), band))
    return out


def parse_reference(text: str) -> list[tuple[str, str, str]]:
    """Ordered ``(id, normalized-title, band)`` for each ``### id`` block."""
    out: list[tuple[str, str, str]] = []
    band = ""
    for line in _non_fence_lines(text):
        m = BAND_RE.match(line)
        if m:
            band = m.group(1).strip()
            continue
        h = REF_HEADING_RE.match(line)
        if h:
            out.append((h.group("id"), _norm_title(h.group("title")), band))
    return out


def _dups(ids: list[str]) -> list[str]:
    seen: set[str] = set()
    dup: list[str] = []
    for i in ids:
        if i in seen and i not in dup:
            dup.append(i)
        seen.add(i)
    return dup


def find_findings(index: list[tuple[str, str, str]],
                  reference: list[tuple[str, str, str]],
                  index_label: str = TODO_REL,
                  reference_label: str = REFERENCE_REL) -> list[str]:
    findings: list[str] = []
    idx_ids = [r[0] for r in index]
    ref_ids = [r[0] for r in reference]
    idx_map = {r[0]: r for r in index}
    ref_map = {r[0]: r for r in reference}

    for d in _dups(idx_ids):
        findings.append(f"DUPLICATE: id {d} appears more than once in {index_label}")
    for d in _dups(ref_ids):
        findings.append(f"DUPLICATE: id {d} appears more than once in {reference_label}")

    for i in idx_ids:
        if i not in ref_map:
            findings.append(f"MISSING: index row {i} in {index_label} has no detail block in {reference_label}")
    for i in ref_ids:
        if i not in idx_map:
            findings.append(f"EXTRA: detail block {i} in {reference_label} has no index row in {index_label}")

    for i in idx_ids:
        if i in ref_map:
            _, it, ib = idx_map[i]
            _, rt, rb = ref_map[i]
            if it != rt:
                findings.append(
                    f"TITLE DRIFT: {i} title differs: {index_label} has {it!r}, {reference_label} has {rt!r}")
            if ib != rb:
                findings.append(
                    f"BAND MISMATCH: {i} is under {ib!r} in {index_label} but {rb!r} in {reference_label}")

    # order: the shared-id sequence must be identical in both files
    shared_idx = [i for i in idx_ids if i in ref_map]
    shared_ref = [i for i in ref_ids if i in idx_map]
    if shared_idx != shared_ref:
        findings.append(
            f"ORDER MISMATCH: the id order in {index_label} ({', '.join(shared_idx)}) "
            f"differs from {reference_label} ({', '.join(shared_ref)})")
    return findings


INDEX_DETAIL_LEAK_RE = re.compile(
    r"^### (?:P-\d+(?:\.\d+){1,2}[a-z]?|\d+(?:\.\d+)+(?:\.[a-z]|[a-z])?|TF-\d+)\b"
)


def find_index_detail_leaks(todo_text: str) -> list[str]:
    """A ``### <id>`` detail block in the INDEX file (TODO.md) is a format break:
    detail blocks belong only in TODO-REFERENCE.md. Left unflagged, it silently
    flips a downstream format heuristic (audit-backlog-actionability) to the
    legacy branch. Return the offending heading lines."""
    return [ln for ln in _non_fence_lines(todo_text) if INDEX_DETAIL_LEAK_RE.match(ln)]


def find_malformed_index_rows(todo_text: str) -> list[str]:
    """Malformed rows in an actual ``| ID | Item | Tags |`` index table.

    Once an index header is seen, every contiguous row that STARTS with a pipe
    (a table row) must also end with a pipe and hold exactly three cells;
    non-separator data rows must additionally carry a valid backlog id in cell
    one. The scan ends at the first line that is not a pipe row, so unrelated
    tables under later H2 sections are outside its scope. Return the complete
    offending row strings.

    RESIDUE (dual-family QA of PR #1666, codex): detection is scoped to rows
    that START with a pipe, so a row missing its LEADING pipe (``id | item |
    tags |``) ends the table scan rather than being flagged, the mirror of the
    terminal-pipe direction this catches; and the exact-three-cell rule would
    flag a future row carrying an unescaped ``|`` inside a cell (claude note),
    which ``split_row``/``parse`` tolerate via ``cells[:3]``. Neither occurs on
    the live tree (0 findings); both are routed to close the residual class.

    INDEX-side only: reference-side ``### `` headings are too varied to flag
    without false positives, and catching the index-side defect already breaks
    a vacuous-clean match.
    """
    out: list[str] = []
    in_index_table = False

    for line in _non_fence_lines(todo_text):
        stripped = line.strip()
        starts_with_pipe = stripped.startswith("|")
        ends_with_pipe = stripped.endswith("|")
        cells = split_row(line) if starts_with_pipe else []

        if not in_index_table:
            if (starts_with_pipe
                    and tuple(cells[:3]) == INDEX_TABLE_HEADER):
                in_index_table = True
                if not ends_with_pipe or len(cells) != 3:
                    out.append(stripped)
            continue

        if not starts_with_pipe:
            in_index_table = False
            continue

        exact_shape = ends_with_pipe and len(cells) == 3
        if is_separator_row(cells):
            if not exact_shape:
                out.append(stripped)
            continue

        first = cells[0].strip() if cells else ""
        if (not exact_shape
                or not first
                or first.lower() == "id"
                or not TODO_ID_RE.match(first)):
            out.append(stripped)

    return out


def _check_one(todo_text: str, reference_text: str,
               index_label: str, reference_label: str) -> tuple[list[str], int, int]:
    """Parity + leak + malformed findings for one (index, reference) backlog pair.

    The caller has already read both files (once, strict UTF-8). Labels are the
    human-facing relative names used in finding text (they differ per pair:
    TODO.md/TODO-REFERENCE.md vs P-TODO.md/P-TODO-REFERENCE.md)."""
    index = parse_index(todo_text)
    reference = parse_reference(reference_text)
    findings = find_findings(index, reference, index_label, reference_label)
    for leak in find_index_detail_leaks(todo_text):
        findings.append(f"INDEX DETAIL LEAK: {index_label} contains a detail block heading "
                        f"({leak.strip()!r}); detail blocks belong only in {reference_label}")
    for bad in find_malformed_index_rows(todo_text):
        findings.append(
            f"MALFORMED INDEX ROW: {index_label} row {bad!r} must have both bounding "
            "pipes, exactly three cells (`ID`, `Item`, `Tags`), and a valid backlog "
            "id in its first cell"
        )
    return findings, len(index), len(reference)


def _first_existing(*candidates: Path | None) -> Path | None:
    for c in candidates:
        if c is not None and c.is_file():
            return c
    return None


def _read_strict(path: Path) -> tuple[str | None, str | None]:
    """``(text, None)`` for a file read once and decoded as strict UTF-8, else ``(None, reason)``.

    3b641 r3 (VPR3B641-R2): invalid UTF-8 used to end in a UnicodeDecodeError
    traceback (exit 1); it is now a reason naming the path, refused with exit 2
    like an unreadable file. Every consumer splits with ``str.splitlines``, so
    reading bytes (no newline translation) parses as ``read_text`` did."""
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        return None, f"cannot read {path} ({exc.strerror})"
    try:
        return data.decode("utf-8"), None
    except UnicodeDecodeError as exc:
        return None, f"cannot decode {path} as UTF-8 ({exc.reason} at byte {exc.start})"


def _probe_private(private_dir: Path) -> tuple[dict[str, str | None], list[str]]:
    """The private candidate files' text, telling ABSENT from UNREADABLE.

    3b641 r2 (VPR3B641-R1): ``Path.is_file()`` returns False for a file in a
    directory without search permission, so a mode-000 ``--private-root`` read as
    a directory with no P-TODO pair and passed. The directory is listed and each
    candidate probed with ``strict_kind`` (only ENOENT is absent) and read, so
    any other OSError, or bytes that are not UTF-8 (r3), is an error naming the
    path (check-fails-closed-on-unreadable). Returns ({relative name: text, or
    None when absent}, errors)."""
    try:
        os.listdir(private_dir)
    except OSError as exc:
        return {}, [f"cannot read the private directory {private_dir} ({exc.strerror}); "
                    "private index<->reference parity cannot be checked"]
    texts: dict[str, str | None] = {}
    errors: list[str] = []
    for rel in (REFERENCE_REL, PTODO_INDEX_REL, PTODO_REFERENCE_REL):
        path = private_dir / rel
        try:
            kind = strict_kind(path)
        except OSError as exc:
            errors.append(f"cannot read {path} ({exc.strerror}); "
                          "private index<->reference parity cannot be checked")
            continue
        if kind is None:
            texts[rel] = None
            continue
        if kind != "file":
            errors.append(f"{path} is present but is not a regular file")
            continue
        text, why = _read_strict(path)
        if why is not None:
            errors.append(f"{why}; private index<->reference parity cannot be checked")
            continue
        texts[rel] = text
    return texts, errors


def _classify_ptodo(path: Path, text: str) -> tuple[str | None, str | None]:
    """``("index" | "legacy", None)`` for a P-TODO.md the gate recognises, else ``(None, reason)``.

    3b641 r3 (VPR3B641-R2): any P-TODO.md without an index header used to count
    as legacy, so a file holding only ``garbage`` passed as a legacy ### -block
    backlog. The form is now established positively: an index header
    (``has_todo_index_header``) or at least one ``### <id> <title>`` block that
    ``parse_reference`` recognises. Anything else is a file the gate cannot read
    as a backlog, so it is refused rather than skipped."""
    if not text.strip():
        return None, (f"{path} is empty; it is neither an index-form nor a legacy "
                      f"### -block {PTODO_INDEX_REL}")
    if has_todo_index_header(text):
        return "index", None
    if parse_reference(text):
        return "legacy", None
    return None, (f"{path} is neither an index-form {PTODO_INDEX_REL} (no `| ID | Item | Tags |` "
                  "header) nor a legacy one (no `### <id> <title>` block the gate recognises)")


def _resolve_pairs(root: Path, private_dir: Path | None) -> tuple[list[tuple[str, str, str, str]], list[str], str | None]:
    """Backlog (index, reference) pairs whose BOTH files currently exist.

    Transitional (2026-08 migration): the public TODO detail file
    (TODO-REFERENCE.md) is moving into the private sibling, and the private
    backlog (P-TODO.md) is being split into an index + P-TODO-REFERENCE.md. This
    resolver handles BOTH the pre-move layout (public TODO-REFERENCE.md, no
    P-TODO-REFERENCE.md) and the post-move layout (references in the private
    sibling), so PR-1 lands green on the old state and stays green after the
    restructure. A pair whose reference file is absent is a no-op (the two-file
    format is not adopted for that backlog yet), matching the original
    adopter-graceful contract. ``private_dir`` is the private sibling root
    (``resolve_sibling('private')`` in production; ``--private-root`` or the
    ``--root`` directory under test); ``None`` means no private sibling (an adopter clone). Returns
    (active_pairs as (index text, reference text, labels), errors, the P-TODO.md form:
    ``"index"``, ``"legacy"`` or None when absent)."""
    pairs: list[tuple[str, str, str, str]] = []
    errors: list[str] = []
    texts: dict[str, str | None] = {}
    if private_dir is not None:
        texts, errors = _probe_private(private_dir)
        if errors:
            return pairs, errors, None

    # Pair 1: public TODO. Index is required; reference resolves private-first
    # (post-move) then public (pre-move). Absent reference -> no-op.
    todo_path = root / TODO_REL
    if not todo_path.is_file():
        errors.append(f"required file missing: {todo_path}")
    else:
        ref_text = texts.get(REFERENCE_REL)
        if ref_text is None and (root / REFERENCE_REL).is_file():
            ref_text, why = _read_strict(root / REFERENCE_REL)
            if why is not None:
                errors.append(f"{why}; index<->reference parity cannot be checked")
        if ref_text is not None:
            todo_text, why = _read_strict(todo_path)
            if why is not None:
                errors.append(f"{why}; index<->reference parity cannot be checked")
            else:
                pairs.append((todo_text, ref_text, TODO_REL, REFERENCE_REL))

    # Pair 2: private P-TODO. Only when the private sibling exists (adopters lack
    # it). Both index and reference must be present; pre-restructure P-TODO.md is
    # a legacy ### -block file with no P-TODO-REFERENCE.md -> no-op (skipped),
    # which correctly avoids running the index-detail-leak check on it. A P-TODO.md
    # in neither form is refused (3b641 r3), with or without its reference.
    ptodo_kind: str | None = None
    if private_dir is not None:
        p_index_text = texts[PTODO_INDEX_REL]
        p_ref_text = texts[PTODO_REFERENCE_REL]
        if p_index_text is not None:
            ptodo_kind, why = _classify_ptodo(private_dir / PTODO_INDEX_REL, p_index_text)
            if why is not None:
                errors.append(f"{why}; private index<->reference parity cannot be checked")
                return pairs, errors, None
        if p_index_text is not None and p_ref_text is not None:
            pairs.append((p_index_text, p_ref_text, PTODO_INDEX_REL, PTODO_REFERENCE_REL))
        elif p_ref_text is not None:
            errors.append(f"{PTODO_REFERENCE_REL} is present but {PTODO_INDEX_REL} is "
                          "missing (broken backlog pair)")
        elif ptodo_kind == "index":
            # F1793-2: a legacy ### -block P-TODO.md with no reference is a no-op
            # (skipped); but a P-TODO.md already in INDEX form with no reference is
            # a half-converted / botched migration -> fail loud rather than skip.
            errors.append(f"{PTODO_INDEX_REL} is in index-row form but "
                          f"{PTODO_REFERENCE_REL} is absent (half-converted backlog; "
                          "every index row would be MISSING its detail block)")

    return pairs, errors, ptodo_kind


def run(root: Path, private_dir: Path | None = None, private_flag: str | None = None) -> int:
    """``private_flag`` is the CLI flag that named ``private_dir`` (``--private-root``
    or ``--root``), or None on the default sibling lookup."""
    pairs, errors, ptodo_kind = _resolve_pairs(root, private_dir)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 2
    if private_dir is not None and not any(p[2] == PTODO_INDEX_REL for p in pairs):
        # 3b648 (VPR3B641-R4 note 4): the default lookup resolved a sibling with no P-TODO pair
        # and used to pass with no notice. A resolved sibling is the private store, so one
        # holding neither P-TODO file fails (exit 2, as --private-root does). r3: rounds 1-2 read
        # the repository origin to excuse adopters; that signal was unsound and is removed. CI
        # and most adopters have no sibling, so they take the DEGRADED path in main instead.
        # r4 (VPR3B648-R3): a sibling holding other content and no backlog file is the README's
        # transitional fallback store for .working/ records, which other tools read; it passes
        # with the not-checked line below. Only an empty sibling (likely stray) or one holding
        # TODO-REFERENCE.md without the P-TODO pair fails, and neither message says to rename it.
        if private_flag is None and ptodo_kind is None:
            try:
                entries = os.listdir(private_dir)
            except OSError as exc:
                print(f"ERROR: cannot read the private directory {private_dir} ({exc.strerror}); "
                      "private index<->reference parity cannot be checked", file=sys.stderr)
                return 2
            if not entries:
                print(f"ERROR: the private sibling {private_dir} is an empty directory, so no private "
                      f"store supplies {PTODO_INDEX_REL} and {PTODO_REFERENCE_REL}; it is likely "
                      "stray: remove it, or pass --private-root naming the private store; private "
                      "index<->reference parity cannot be checked", file=sys.stderr)
                return 2
            if REFERENCE_REL in entries:
                print(f"ERROR: no private P-TODO pair was found in the private sibling {private_dir} "
                      f"(it holds {REFERENCE_REL} but neither {PTODO_INDEX_REL} nor "
                      f"{PTODO_REFERENCE_REL}); restore the pair there; private index<->reference "
                      "parity cannot be checked", file=sys.stderr)
                return 2
        # 3b641 r4 (VPR3B641-R3): --private-root declares the private input, so a directory
        # holding neither P-TODO file is an absent declared resource and fails with exit 2
        # (check-fails-closed-on-unreadable). A recognised legacy P-TODO.md is not absent: it
        # keeps the not-checked line below. --root only names a fixture repository that the
        # private lookup defaults to, so it keeps the line too.
        if private_flag == "--private-root" and ptodo_kind is None:
            print(f"ERROR: no private P-TODO pair was found in the --private-root directory "
                  f"{private_dir} (it holds neither {PTODO_INDEX_REL} nor {PTODO_REFERENCE_REL}); "
                  "private index<->reference parity cannot be checked", file=sys.stderr)
            return 2
        # 3b635 r4 / 3b641: otherwise a named private directory with no P-TODO pair says so, as
        # gate 81 says P-TODO.md is not present; informational, not DEGRADED, and exit 0 (the
        # explicit-path fixture contract; a broken or half-converted pair already failed above).
        # It keeps the OK: prefix of the gate's other pass lines: the directory was read and
        # holds no pair, so nothing was skipped; an unreadable one failed above (3b641 r2), as did
        # a P-TODO.md in neither form (r3), so a present one here is a recognised legacy file.
        if ptodo_kind == "legacy":
            why = (f"holds a legacy ### -block {PTODO_INDEX_REL} and no "
                   f"{PTODO_REFERENCE_REL} (backlog not yet split)")
        elif private_flag is None:
            why = (f"holds none of {REFERENCE_REL}, {PTODO_INDEX_REL} or {PTODO_REFERENCE_REL} "
                   "(a private store without a backlog)")
        else:
            why = f"holds neither {PTODO_INDEX_REL} nor {PTODO_REFERENCE_REL}"
        where = f"the {private_flag} directory" if private_flag else "the private sibling"
        print(f"OK: private index<->reference parity not checked: {where} {private_dir} {why}.")
    if not pairs:
        print("OK: no two-file backlog pair present (reference file(s) absent); no-op.")
        return 0

    all_findings: list[str] = []
    summary: list[str] = []
    for index_text, reference_text, index_label, reference_label in pairs:
        findings, n_index, n_ref = _check_one(
            index_text, reference_text, index_label, reference_label)
        all_findings.extend(findings)
        summary.append(f"{index_label}: {n_index} index row(s) / {n_ref} detail block(s)")

    if not all_findings:
        print("OK: index<->reference parity holds for " + "; ".join(summary)
              + " (id, title, band, and order all agree).")
        return 0
    print("=== TODO index<->reference parity findings ===", file=sys.stderr)
    for f in all_findings:
        print(f"  {f}", file=sys.stderr)
    print(
        f"\nFAIL: {len(all_findings)} index<->reference parity finding(s). Every open item "
        f"is exactly one index row plus one detail block, with matching id, title, band, "
        f"and position order. Fix the mismatch; do not weaken this gate.",
        file=sys.stderr,
    )
    return 1


def main(argv: list[str]) -> int:
    root = REPO_ROOT
    private_override: Path | None = None
    have_private_override = False
    args = argv[1:]
    seen: set[str] = set()
    i = 0
    while i < len(args):
        flag, eq, inline = args[i].partition("=")
        if flag in ("--root", "--private-root"):
            if flag in seen:
                print(f"ERROR: {flag} given more than once.", file=sys.stderr)
                return 2
            seen.add(flag)
            # 3b50b1: a flag with no value, or with a value that is not a directory, is refused
            # (a trailing flag used to be skipped and a --flag=value form ignored).
            if eq:
                value, step = inline, 1
            elif i + 1 < len(args) and not args[i + 1].startswith("-"):
                value, step = args[i + 1], 2
            else:
                print(f"ERROR: {flag} needs a directory argument.", file=sys.stderr)
                return 2
            if flag == "--root":
                root = require_dir(value, "--root")
            else:
                private_override = require_dir(value, "--private-root")
                have_private_override = True
            i += step
        else:
            # 3b50b1 r3: an unknown argument (a typo such as --roott) is refused; it used to be
            # skipped, so the gate scanned the default roots and exited 0.
            print(f"ERROR: unrecognized argument {args[i]!r} "
                  f"(usage: [--root DIR] [--private-root DIR]).", file=sys.stderr)
            return 2
    # The private pair comes from --private-root when given; under --root it otherwise comes
    # from the root itself, as gates 78 and 81 read P-TODO.md, so a fixture run never reads
    # the real sibling (3b635 r3). Only the DEFAULT lookup resolves the private sibling.
    private_flag: str | None = None
    if have_private_override:
        private_dir, private_flag = private_override, "--private-root"
    elif "--root" in seen:
        private_dir, private_flag = root, "--root"
    else:
        private_dir = resolve_sibling("private")
    if private_dir is None:
        # 3b635: without the private sibling the private pair (and, once TODO-REFERENCE.md
        # has moved there, the public pair) is skipped with exit 0; say so. Only on the
        # DEFAULT lookup, as gates 78 and 81: a --root run is a fixture run, not CI.
        skipped = [f"the {PTODO_INDEX_REL} pair"]
        if _first_existing(root / REFERENCE_REL) is None:
            skipped.insert(0, f"the {TODO_REL} pair")
        print_degraded("gate 90",
                       f"gate 90 skipped the index<->reference parity check of "
                       f"{' and '.join(skipped)} (no private store supplies the reference); "
                       f"this pass attests nothing about it.")
    return run(root, private_dir, private_flag)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
