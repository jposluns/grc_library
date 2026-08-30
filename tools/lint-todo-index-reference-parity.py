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
absent (an adopter clone without the private sibling), the gate is a no-op OK.
Stdlib-only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_TOOLS_DIR = str(Path(__file__).resolve().parent)
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

from lint_common import (REPO_ROOT, TODO_ID_RE, split_row, is_separator_row,  # noqa: E402
                         resolve_sibling, has_todo_index_header)

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
    ``| id |`` example inside a ``` fence is not mistaken for a real item."""
    in_fence = False
    for line in text.splitlines():
        st = line.lstrip()
        if st.startswith("```") or st.startswith("~~~"):
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


def _check_one(index_path: Path, reference_path: Path,
               index_label: str, reference_label: str) -> tuple[list[str], int, int]:
    """Parity + leak + malformed findings for one (index, reference) backlog pair.

    Caller guarantees both files exist. Labels are the human-facing relative
    names used in finding text (they differ per pair: TODO.md/TODO-REFERENCE.md
    vs P-TODO.md/P-TODO-REFERENCE.md)."""
    todo_text = index_path.read_text(encoding="utf-8")
    index = parse_index(todo_text)
    reference = parse_reference(reference_path.read_text(encoding="utf-8"))
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


def _resolve_pairs(root: Path, private_dir: Path | None) -> tuple[list[tuple[Path, Path, str, str]], list[str]]:
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
    (``resolve_sibling('private')`` in production, or a fixture root under
    test); ``None`` means no private sibling (an adopter clone). Returns
    (active_pairs, errors)."""
    pairs: list[tuple[Path, Path, str, str]] = []
    errors: list[str] = []

    # Pair 1: public TODO. Index is required; reference resolves private-first
    # (post-move) then public (pre-move). Absent reference -> no-op.
    todo_path = root / TODO_REL
    if not todo_path.is_file():
        errors.append(f"required file missing: {todo_path}")
    else:
        ref = _first_existing(
            (private_dir / REFERENCE_REL) if private_dir else None,
            root / REFERENCE_REL,
        )
        if ref is not None:
            pairs.append((todo_path, ref, TODO_REL, REFERENCE_REL))

    # Pair 2: private P-TODO. Only when the private sibling exists (adopters lack
    # it). Both index and reference must be present; pre-restructure P-TODO.md is
    # a legacy ### -block file with no P-TODO-REFERENCE.md -> no-op (skipped),
    # which correctly avoids running the index-detail-leak check on it.
    if private_dir is not None:
        p_index = private_dir / PTODO_INDEX_REL
        p_ref = private_dir / PTODO_REFERENCE_REL
        if p_index.is_file() and p_ref.is_file():
            pairs.append((p_index, p_ref, PTODO_INDEX_REL, PTODO_REFERENCE_REL))
        elif p_ref.is_file() and not p_index.is_file():
            errors.append(f"{PTODO_REFERENCE_REL} is present but {PTODO_INDEX_REL} is "
                          "missing (broken backlog pair)")
        elif p_index.is_file() and not p_ref.is_file():
            # F1793-2: a legacy ### -block P-TODO.md with no reference is a no-op
            # (skipped); but a P-TODO.md already in INDEX form with no reference is
            # a half-converted / botched migration -> fail loud rather than skip.
            if has_todo_index_header(p_index.read_text(encoding="utf-8")):
                errors.append(f"{PTODO_INDEX_REL} is in index-row form but "
                              f"{PTODO_REFERENCE_REL} is absent (half-converted backlog; "
                              "every index row would be MISSING its detail block)")

    return pairs, errors


def run(root: Path, private_dir: Path | None = None) -> int:
    pairs, errors = _resolve_pairs(root, private_dir)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 2
    if not pairs:
        print("OK: no two-file backlog pair present (reference file(s) absent); no-op.")
        return 0

    all_findings: list[str] = []
    summary: list[str] = []
    for index_path, reference_path, index_label, reference_label in pairs:
        findings, n_index, n_ref = _check_one(
            index_path, reference_path, index_label, reference_label)
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
    i = 0
    while i < len(args):
        if args[i] == "--root" and i + 1 < len(args):
            root = Path(args[i + 1]).resolve()
            i += 2
        elif args[i] == "--private-root" and i + 1 < len(args):
            private_override = Path(args[i + 1]).resolve()
            have_private_override = True
            i += 2
        else:
            i += 1
    # Default the private sibling to the real one; --private-root scopes it to a
    # fixture so `--root` regression tests stay hermetic.
    private_dir = private_override if have_private_override else resolve_sibling("private")
    return run(root, private_dir)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
