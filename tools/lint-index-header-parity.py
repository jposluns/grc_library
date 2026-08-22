#!/usr/bin/env python3
"""Index-header parity audit for the GRC Documentation Library.

The document index register
(``governance/register-document-index-and-classification.md``) mirrors,
per active document, its Owner Role and Review Frequency from that
document's own metadata header, which is the go-forward source of truth.
This gate locks that mirror in place. For every active-index row it:

1. Resolves the row's Repository Path to the linked document and reads
   that document's metadata header.
2. **Review Frequency:** tokenizes both the index cell and the header's
   ``Review Frequency`` value with a cadence recognizer and fails the row
   when the two token sets are DISJOINT (empty intersection). This lets a
   header add a trigger clause on top of the same base cadence
   ("Annual and upon material change" vs index "Annual") while catching a
   genuine base-cadence disagreement (index "Annual" vs header
   "Quarterly"). An unrecognizable cadence on either side is a finding,
   not a silent pass (fail-closed, per the guard-inputs discipline).
3. **Owner Role:** compares the index Owner Role cell to the header
   ``Owner`` value (``.strip()`` then byte equality; Owner values are
   canonical titles, so case drift is real drift). Under ``--strict-owner``
   a mismatch is a finding (exit 1); without it, a mismatch prints as a
   ``WARNING:`` line and does not affect the exit code (a rollback lever
   that does not demote the gate, and headroom for adopter forks whose
   owner cells legitimately diverge).

The Title column is deliberately NOT checked here (a measured 41 index-vs-header
title diffs, most a deliberate systematic shortening, need a content
reconcile first); it is routed as its own backlog item. The per-row check
is structured so a third comparator drops in without reshaping the parse.

Usage:
    python3 tools/lint-index-header-parity.py
    python3 tools/lint-index-header-parity.py --strict-owner
    python3 tools/lint-index-header-parity.py --root /path/to/alt-repo

The ``--root`` flag overrides the repository root (used by the gate-36
regression fixture). Default: the actual repo root, from this file's location.

Exit codes (per the tests/README.md convention):
    0  clean
    1  one or more findings (owner under --strict-owner, cadence, malformed
       row, missing linked file, header missing a needed field)
    2  environmental error (register file missing, or its active-index
       header row not found)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_common import parse_metadata_block, split_row, is_separator_row  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent

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
COL_TITLE = 2
COL_PATH = 3
COL_OWNER = 4
COL_FREQ = 5
NUM_COLS = 8

# Same code-span-link shape gate 4 (lint-structure.py) parses.
LINK_TARGET_RE = re.compile(r"\[`([^`]+)`\]\(([^)]+)\)")

# Cadence recognizer: longest-phrase-first, case-insensitive, CONSUMING
# (a matched phrase is blanked before shorter phrases are tried, so
# "semi-annual" never also yields ANNUAL, and "6 to 12 months" never also
# yields ANNUAL via "12 months"). Mirrors, in token form, the FREQUENCY_MAP
# in tools/check-review-cadence.py (which encodes biannual = 6 months); this
# gate needs only tokens, not month arithmetic, so it keeps its own table.
# Ordered list of (phrase, token); scanned in this order.
CADENCE_PHRASES = [
    ("6 to 12 months", "SIX_TO_TWELVE"),
    ("semi-annual", "SEMIANNUAL"),
    ("semi annual", "SEMIANNUAL"),
    ("biannual", "SEMIANNUAL"),
    ("6 months", "SEMIANNUAL"),
    ("biennial", "BIENNIAL"),
    ("24 months", "BIENNIAL"),
    ("annual", "ANNUAL"),  # substring also covers "annually"
    ("yearly", "ANNUAL"),
    ("12 months", "ANNUAL"),
    ("quarterly", "QUARTERLY"),
    ("3 months", "QUARTERLY"),
    ("monthly", "MONTHLY"),
    ("weekly", "WEEKLY"),
    ("daily", "DAILY"),
    ("continuous", "CONTINUOUS"),
]
# Event-driven / on-demand cadence, matched after the fixed phrases.
CADENCE_EVENT_RE = re.compile(
    r"upon|as required|as needed|following|on material change|"
    r"at every material change|event-driven|updated",
    re.IGNORECASE,
)


def cadence_tokens(value: str) -> set[str]:
    """Tokenize a cadence string (longest-phrase-first, consuming)."""
    work = value.lower()
    tokens: set[str] = set()
    for phrase, token in CADENCE_PHRASES:
        if phrase in work:
            tokens.add(token)
            work = work.replace(phrase, " ")
    if CADENCE_EVENT_RE.search(work):
        tokens.add("EVENT")
    return tokens


def find_index_table(lines: list[str]) -> tuple[int, list[str]] | None:
    """Return (start_lineno, data_row_lines) for the active index table, or None.

    ``start_lineno`` is 1-based, the line of the header row. ``data_row_lines``
    is a list of (lineno, raw_line) for each data row (separator excluded).
    """
    for i, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            continue
        if split_row(line) == INDEX_HEADER_CELLS:
            data: list[tuple[int, str]] = []
            for j in range(i + 1, len(lines)):
                row = lines[j]
                if not row.lstrip().startswith("|"):
                    break
                cells = split_row(row)
                if is_separator_row(cells):
                    continue
                data.append((j + 1, row))
            return (i + 1, data)  # type: ignore[return-value]
    return None


def check_row(cells: list[str], header_fields: dict[str, str], strict_owner: bool) -> list[str]:
    """Return per-row findings (owner/cadence). Warnings are prefixed 'WARNING:'."""
    findings: list[str] = []

    # Review Frequency: empty-intersection rule.
    idx_freq = cells[COL_FREQ]
    hdr_freq = header_fields.get("Review Frequency", "")
    idx_tok = cadence_tokens(idx_freq)
    hdr_tok = cadence_tokens(hdr_freq)
    if not idx_tok and not hdr_tok:
        findings.append(
            f"no recognized cadence token in index cell ({idx_freq!r}) or header ({hdr_freq!r})"
        )
    elif not idx_tok:
        findings.append(f"no recognized cadence token in index cell ({idx_freq!r})")
    elif not hdr_tok:
        findings.append(f"no recognized cadence token in header Review Frequency ({hdr_freq!r})")
    elif not (idx_tok & hdr_tok):
        findings.append(
            f"disjoint cadence tokens (index {sorted(idx_tok)} vs header {sorted(hdr_tok)})"
        )

    # Owner Role: strict equality; gated by --strict-owner.
    idx_owner = cells[COL_OWNER].strip()
    hdr_owner = header_fields.get("Owner", "").strip()
    if idx_owner != hdr_owner:
        msg = f"owner mismatch (index {idx_owner!r} vs header {hdr_owner!r})"
        findings.append(msg if strict_owner else f"WARNING:{msg}")

    return findings


def main(argv: list[str]) -> int:
    global REPO_ROOT
    parser = argparse.ArgumentParser(description="Index-header parity audit.")
    parser.add_argument("--root", type=Path, default=None,
                        help="Override repository root (for isolation testing).")
    parser.add_argument("--strict-owner", action="store_true",
                        help="Treat an Owner Role mismatch as a finding (exit 1) "
                             "instead of a warning.")
    args = parser.parse_args(argv[1:])
    if args.root is not None:
        REPO_ROOT = args.root.resolve()

    index_path = REPO_ROOT / INDEX_REL
    if not index_path.exists():
        print(f"ERROR (environmental): index register not found at {index_path}", file=sys.stderr)
        return 2
    lines = index_path.read_text(encoding="utf-8").splitlines()

    table = find_index_table(lines)
    if table is None:
        print("ERROR (environmental): active-index table header row not found in "
              f"{INDEX_REL}", file=sys.stderr)
        return 2
    _start, data_rows = table

    findings: list[str] = []
    warnings: list[str] = []
    gov_dir = REPO_ROOT / "governance"

    for lineno, raw in data_rows:
        cells = split_row(raw)
        if len(cells) != NUM_COLS:
            findings.append(f"{INDEX_REL}:{lineno}: malformed row: {len(cells)} cells, expected {NUM_COLS}")
            continue
        m = LINK_TARGET_RE.search(cells[COL_PATH])
        if not m:
            findings.append(f"{INDEX_REL}:{lineno}: Repository Path cell has no parseable code-span link: {cells[COL_PATH]!r}")
            continue
        display, target = m.group(1), m.group(2)
        resolved = (gov_dir / target).resolve()
        # Defence in depth: display path (repo-root-relative) must agree with target.
        expected = (REPO_ROOT / display).resolve()
        if resolved != expected:
            findings.append(f"{INDEX_REL}:{lineno}: display path {display!r} disagrees with link target {target!r}")
            continue
        if not resolved.exists():
            findings.append(f"{INDEX_REL}:{lineno}: linked document does not exist: {display}")
            continue
        block = parse_metadata_block(resolved.read_text(encoding="utf-8"))
        if "Owner" not in block.fields:
            findings.append(f"{INDEX_REL}:{lineno}: linked document {display} header has no Owner field")
            continue
        if "Review Frequency" not in block.fields:
            findings.append(f"{INDEX_REL}:{lineno}: linked document {display} header has no Review Frequency field")
            continue
        for f in check_row(cells, block.fields, args.strict_owner):
            if f.startswith("WARNING:"):
                warnings.append(f"{INDEX_REL}:{lineno}: {f[len('WARNING:'):]}")
            else:
                findings.append(f"{INDEX_REL}:{lineno}: {f}")

    for w in warnings:
        print(f"WARNING: {w}")
    for f in findings:
        print(f"FAIL: {f}")
    if findings:
        print(f"\nIndex-header parity: {len(findings)} finding(s).")
        return 1
    print(f"Index-header parity: {len(data_rows)} rows checked, clean"
          + (f" ({len(warnings)} owner warning(s))" if warnings else "") + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
