#!/usr/bin/env python3
"""Index-header parity audit - grc wrapper over the pack-owned engine.

The document index register
(``governance/register-document-index-and-classification.md``) mirrors, per
active document, its Owner Role and Review Frequency from that document's own
metadata header, the go-forward source of truth. This gate locks that mirror.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE check
(cadence_tokens, find_index_table, check_row, collect_findings) plus the generic
review-cadence recognizer + code-span-link regex live in the pack-owned engine
(.corpus-management/tools/gate_lint_index_header_parity.py, source of record).
This wrapper supplies the grc index register schema (the index relative path, the
8-column header row, the column indices, the Owner/Review Frequency metadata
field names) + the per-document base-cadence allow-list + the --root and
--strict-owner handling + the register-missing/unreadable/table-not-found
environmental exits + the WARNING/FAIL/summary reporting.

The Title column is deliberately NOT checked here (a measured 41 index-vs-header
title diffs, most a deliberate systematic shortening, need a content reconcile
first); it is routed as its own backlog item. The per-row check is structured so
a third comparator drops in without reshaping the parse.

Usage:
    python3 tools/lint-index-header-parity.py
    python3 tools/lint-index-header-parity.py --strict-owner
    python3 tools/lint-index-header-parity.py --root /path/to/alt-repo

Exit codes (per the tests/README.md convention):
    0  clean
    1  one or more findings (owner under --strict-owner, cadence, malformed row,
       missing linked file, header missing a needed field)
    2  environmental error (register file missing or unreadable, or its
       active-index header row not found)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # own-dir (original had one; preserved)
import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path (engine imports aiqt_corpus)
from lint_common import REPO_ROOT, require_dir  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

INDEX_REL = "governance/register-document-index-and-classification.md"

# The active-index table's exact 8-column header row. The scan arms on this
# literal cell set and consumes the pipe-prefixed rows that follow.
INDEX_HEADER_CELLS = [
    "Domain",
    "Type",
    "Title",
    "Repository Path",
    "Owner Role",
    "Review Frequency",
    "Primary Alignment Families",
    "Adoption Disposition",
]
COL_TITLE = 2   # currently unused; retained to document the 8-column schema and the third-comparator extension point
COL_PATH = 3
COL_OWNER = 4
COL_FREQ = 5
NUM_COLS = 8

# The metadata field names the index columns are mirrored FROM (grc metadata schema).
OWNER_FIELD = "Owner"
FREQ_FIELD = "Review Frequency"

# Semantic exceptions to base-set equality. Each entry is pinned to the document
# path AND the expected (index base set, header base set), so a later cadence
# change fails closed instead of inheriting a blanket exemption.
# Tuple shape: (index base tokens, header base tokens, one-line rationale).
BASE_CADENCE_EQUALITY_ALLOWLIST: dict[
    str, tuple[frozenset[str], frozenset[str], str]
] = {
    "operations/register-it-security-operations.md": (
        frozenset({"CONTINUOUS", "MONTHLY"}),
        frozenset({"ANNUAL", "CONTINUOUS", "MONTHLY"}),
        "Legitimate multi-cadence: index records continuous/monthly operating cadence; "
        "header additionally requires annual full review.",
    ),
    "ai/register-mcp-server.md": (
        frozenset({"QUARTERLY"}),
        frozenset({"CONTINUOUS", "QUARTERLY"}),
        "Legitimate multi-cadence wording: index records quarterly review; the header's "
        "continuous-update clause is event-driven registration/change/retirement maintenance.",
    ),
    "risk/template-enterprise-risk-register.md": (
        frozenset({"ANNUAL"}),
        frozenset({"ANNUAL", "QUARTERLY"}),
        "Template: index records annual template review; header additionally requires "
        "quarterly review of register entries.",
    ),
    "supply-chain/register-supplier-risk-template.md": (
        frozenset({"QUARTERLY"}),
        frozenset({"ANNUAL", "QUARTERLY"}),
        "Template: index records quarterly active-entry review; header additionally requires "
        "annual template review.",
    ),
    "supply-chain/register-sbom.md": (
        frozenset({"QUARTERLY"}),
        frozenset({"CONTINUOUS", "QUARTERLY"}),
        "Legitimate multi-cadence wording: index records quarterly review; the header's "
        "continuous-update clause is build/supplier-refresh driven.",
    ),
}


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_index_header_parity  # the pack-owned engine (source of record)
    return gate_lint_index_header_parity


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Index-header parity audit.")
    parser.add_argument("--root", type=str, default=None,
                        help="Override repository root (for isolation testing).")
    parser.add_argument("--strict-owner", action="store_true",
                        help="Treat an Owner Role mismatch as a finding (exit 1) "
                             "instead of a warning.")
    args = parser.parse_args(argv[1:])
    if args.root is not None:  # 3b50b2d1: a missing, empty or non-directory --root is refused
        args.root = require_dir(args.root, "--root")
    root = args.root.resolve() if args.root is not None else REPO_ROOT

    index_path = root / INDEX_REL
    if not index_path.exists():
        print(f"ERROR (environmental): index register not found at {index_path}", file=sys.stderr)
        return 2
    try:
        text = index_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR (environmental): cannot read index register {index_path}: {exc}", file=sys.stderr)
        return 2

    result = _engine().collect_findings(
        text, root,
        index_rel=INDEX_REL,
        header_cells=INDEX_HEADER_CELLS,
        num_cols=NUM_COLS,
        col_path=COL_PATH,
        col_owner=COL_OWNER,
        col_freq=COL_FREQ,
        owner_field=OWNER_FIELD,
        freq_field=FREQ_FIELD,
        strict_owner=args.strict_owner,
        base_cadence_allowlist=BASE_CADENCE_EQUALITY_ALLOWLIST,
    )
    if result is None:
        print("ERROR (environmental): active-index table header row not found in "
              f"{INDEX_REL}", file=sys.stderr)
        return 2
    findings, warnings, rows_checked = result

    for w in warnings:
        print(f"WARNING: {w}")
    for f in findings:
        print(f"FAIL: {f}")
    if findings:
        print(f"\nIndex-header parity: {len(findings)} finding(s).")
        return 1
    print(f"Index-header parity: {rows_checked} rows checked, clean"
          + (f" ({len(warnings)} owner warning(s))" if warnings else "") + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
