#!/usr/bin/env python3
"""TODO index<->reference bijection audit (a backlog-integrity gate).

The TODO-rework format (2026-08) splits the public backlog into an INDEX
([`TODO.md`](../TODO.md): one ``| ID | Item | Tags |`` row per open item, under
``## `` bands, e.g. Priority N) and a DETAIL file
([`TODO-REFERENCE.md`](../TODO-REFERENCE.md): one ``### <id> <title>`` block per
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

Adopter-graceful: if ``TODO-REFERENCE.md`` is absent (a clone that has not
adopted the two-file format), the gate is a no-op OK. Stdlib-only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_TOOLS_DIR = str(Path(__file__).resolve().parent)
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

from lint_common import (  # noqa: E402
    REPO_ROOT,
    TODO_ID_RE,
    parse_todo_index,
    split_row,
    is_separator_row,
)

TODO_REL = "TODO.md"
REFERENCE_REL = "TODO-REFERENCE.md"

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
                  reference: list[tuple[str, str, str]]) -> list[str]:
    findings: list[str] = []
    idx_ids = [r[0] for r in index]
    ref_ids = [r[0] for r in reference]
    idx_map = {r[0]: r for r in index}
    ref_map = {r[0]: r for r in reference}

    for d in _dups(idx_ids):
        findings.append(f"DUPLICATE: id {d} appears more than once in {TODO_REL}")
    for d in _dups(ref_ids):
        findings.append(f"DUPLICATE: id {d} appears more than once in {REFERENCE_REL}")

    for i in idx_ids:
        if i not in ref_map:
            findings.append(f"MISSING: index row {i} in {TODO_REL} has no detail block in {REFERENCE_REL}")
    for i in ref_ids:
        if i not in idx_map:
            findings.append(f"EXTRA: detail block {i} in {REFERENCE_REL} has no index row in {TODO_REL}")

    for i in idx_ids:
        if i in ref_map:
            _, it, ib = idx_map[i]
            _, rt, rb = ref_map[i]
            if it != rt:
                findings.append(
                    f"TITLE DRIFT: {i} title differs: {TODO_REL} has {it!r}, {REFERENCE_REL} has {rt!r}")
            if ib != rb:
                findings.append(
                    f"BAND MISMATCH: {i} is under {ib!r} in {TODO_REL} but {rb!r} in {REFERENCE_REL}")

    # order: the shared-id sequence must be identical in both files
    shared_idx = [i for i in idx_ids if i in ref_map]
    shared_ref = [i for i in ref_ids if i in idx_map]
    if shared_idx != shared_ref:
        findings.append(
            f"ORDER MISMATCH: the id order in {TODO_REL} ({', '.join(shared_idx)}) "
            f"differs from {REFERENCE_REL} ({', '.join(shared_ref)})")
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


def run(root: Path) -> int:
    todo_path = root / TODO_REL
    ref_path = root / REFERENCE_REL
    if not todo_path.is_file():
        print(f"ERROR: required file missing: {todo_path}", file=sys.stderr)
        return 2
    if not ref_path.is_file():
        print(f"OK: {REFERENCE_REL} not present (two-file backlog format not adopted); no-op.")
        return 0
    todo_text = todo_path.read_text(encoding="utf-8")
    index = parse_index(todo_text)
    reference = parse_reference(ref_path.read_text(encoding="utf-8"))
    findings = find_findings(index, reference)
    for leak in find_index_detail_leaks(todo_text):
        findings.append(f"INDEX DETAIL LEAK: {TODO_REL} contains a detail block heading "
                        f"({leak.strip()!r}); detail blocks belong only in {REFERENCE_REL}")
    if not findings:
        print(
            f"OK: {len(index)} index row(s) and {len(reference)} detail block(s) are a "
            f"one-to-one match (id, title, band, and order all agree)."
        )
        return 0
    print("=== TODO index<->reference parity findings ===", file=sys.stderr)
    for f in findings:
        print(f"  {f}", file=sys.stderr)
    print(
        f"\nFAIL: {len(findings)} index<->reference parity finding(s). Every open item "
        f"is exactly one {TODO_REL} index row plus one {REFERENCE_REL} detail block, "
        f"with matching id, title, band, and position order. Fix the mismatch; do not "
        f"weaken this gate.",
        file=sys.stderr,
    )
    return 1


def main(argv: list[str]) -> int:
    root = REPO_ROOT
    args = argv[1:]
    if len(args) == 2 and args[0] == "--root":
        root = Path(args[1]).resolve()
    return run(root)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
