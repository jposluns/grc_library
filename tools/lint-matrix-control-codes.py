#!/usr/bin/env python3
"""Central compliance-matrix framework-control-code validity - grc wrapper over the pack engine.

Validate every framework-control code in the central compliance matrix
(compliance/matrix-grc-compliance-alignment.md): CSA CCM v4.1 / AICM v1.1 column
membership, ISO/IEC 27001:2022 Annex A membership + clause format, and NIST CSF 2.0
well-formedness + Category membership. The optional AICPA TSC 2017 column (backlog 3.57)
is validated for 2017 Trust Services Criteria criterion membership (the 61-criterion
closed set in tools/tsc_reference.py).

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan
(Finding, the header/regex constants, the row helpers, the per-framework checks, and
scan_matrix) is the source of record in the pack engine
(.corpus-management/tools/gate_lint_matrix_control_codes.py); it is catalogue-free and
takes the five framework-reference predicates, plus the two optional TSC predicates,
via configure(ref). This wrapper imports
the shared grc reference modules, configures the engine, and keeps the matrix scan
scope (MATRIX_PATH), a module-global scan_matrix(path) shim, lint_target, main, and
the exit codes: 0 clean, 1 on findings, 2 when a target is missing, cannot be read as UTF-8, or
holds no matrix table (a header row naming both the ISO/IEC 27001:2022 and NIST CSF 2.0 columns),
since such a target selects nothing to check (P-TODO 3b57; no caller passes arbitrary filenames:
pre-commit sets pass_filenames false, and quick-guard, run_all_audits.sh and CI run it with no
arguments).
"""

from __future__ import annotations

import argparse
import re
import sys
import types
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from ccm_aicm_reference import is_aicm_only, is_ccm_v41  # noqa: E402  # grc reference catalogue
from iso_27001_reference import check_iso_token  # noqa: E402  # shared with gate 58
from nist_csf_reference import is_valid_category, relocation_note  # noqa: E402  # shared with gate 54
from tsc_reference import is_tsc_group_heading, is_valid_tsc_criterion  # noqa: E402  # grc reference catalogue (3.57)
from lint_common import REPO_ROOT  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"


MATRIX_REL = "compliance/matrix-grc-compliance-alignment.md"
MATRIX_PATH = REPO_ROOT / MATRIX_REL


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_matrix_control_codes  # the pack-owned engine (source of record)
    return gate_lint_matrix_control_codes


# Configure the engine ONCE with the grc framework-reference predicates.
_engine().configure(types.SimpleNamespace(
    is_valid_category=is_valid_category,
    relocation_note=relocation_note,
    is_ccm_v41=is_ccm_v41,
    is_aicm_only=is_aicm_only,
    check_iso_token=check_iso_token,
    is_valid_tsc_criterion=is_valid_tsc_criterion,
    is_tsc_group_heading=is_tsc_group_heading,
))


def scan_matrix(path: Path) -> list:
    """Thin shim delegating to the pack engine's pure scan (engine already configured)."""
    return _engine().scan_matrix(path)


def has_matrix_table(text: str) -> bool:
    """True when `text` holds a table header row naming both the ISO and NIST columns, the row
    the engine's scan keys on (same split_row and header constants)."""
    eng = _engine()
    for line in text.splitlines():
        if line.lstrip().startswith("|"):
            cells = eng.split_row(line)
            if eng.ISO_HEADER in cells and eng.NIST_HEADER in cells:
                return True
    return False


# The canonical matrix's exact table model (3.57): the only pipe lines it may carry are
# its mapping tables (this exact header), the framework-key table and the coverage-summary
# table, each a header, a separator of the same width, then rows of that width. Any other
# pipe line (a misspelt or dropped label in any header, a row cut off from its table by a
# blank line, a row without its leading pipe, a mapping row inside an auxiliary table, a
# surplus or missing cell) is a finding, so the engine can never silently skip a table,
# a column or a row of the canonical matrix. Grc configuration, not engine behaviour.
CANONICAL_TABLE_HEADERS = {
    "| Domain | Document Title | Path | CSA CCM v4.1 | CSA AICM v1.1 | ISO/IEC 27001:2022 "
    "| NIST CSF 2.0 | CTPAT | PIP | BASC v6 | WCO SAFE | AEO/AEO-S | AICPA TSC 2017 |": "mapping",
    "| Column | Framework | Reference Basis |": "framework key",
    "| Framework | Coverage emphasis |": "coverage summary",
}


# Canonical table lines use a character allowlist rather than per-shape checks: printable
# ASCII plus the section sign, minus "<" (raw HTML) and "\\" (escapes that renderers split
# differently). Anything else (a non-breaking or other Unicode space, a control character,
# a Unicode line or paragraph separator) is refused, so no invisible character can change
# how a renderer splits the line into cells or rows.
TABLE_LINE_ALLOWED = frozenset(chr(c) for c in range(0x20, 0x7F)) - {"<", "\\"} | {"\u00a7"}
# Characters Python's str.splitlines treats as line breaks but CommonMark does not: refused
# anywhere in the file, since the checker and a renderer would disagree about the lines.
NON_COMMONMARK_BREAKS = frozenset("\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029")
FENCE_OR_HTML_RE = re.compile(r"^\s*(?:```|~~~|<[A-Za-z/!?])")
DELIM_CELL_RE = re.compile(r"^:?-+:?$")


def canonical_structure_findings(text: str) -> list:
    """Findings for any line of the canonical matrix outside its exact table model.

    Each table is a recognized header preceded by a blank line (or the file start), its
    separator, then rows of its width, followed by a blank line (or the file end); every
    table line starts at column 1 with a pipe and ends with a pipe, and carries no
    backslash. A non-blank line directly after a table would render as a row of it, and an
    indented line would render as a code block, so both are refused.
    """
    eng = _engine()
    out = []
    # Split only where CommonMark breaks a line (LF, CRLF, CR), never on the extra
    # separators str.splitlines honours.
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")

    def refuse(lineno: int, problem: str) -> None:
        out.append(eng.Finding(lineno, "matrix-structure", problem + "; the canonical "
                               "matrix admits only its exact table model."))

    width = None     # the current recognized table's width, or None outside one
    expect_sep = False
    for lineno, raw in enumerate(lines, start=1):
        line = raw.rstrip(" \t")
        if any(ch in NON_COMMONMARK_BREAKS for ch in raw):
            refuse(lineno, "a line or paragraph separator that Markdown renderers do not "
                           "treat as a line break")
            width, expect_sep = None, False
            continue
        # The canonical matrix carries no code fences and no HTML: a table inside either
        # does not render as a table, and inline or container-prefixed HTML (a blockquoted
        # tag, an unclosed <div hidden>) can hide the tables after it, so a fence opener and
        # any "<" anywhere in the file are refused outright.
        if FENCE_OR_HTML_RE.match(line) or "<" in line:
            refuse(lineno, "a code fence or an HTML block (a table inside one does not render)")
            width, expect_sep = None, False
            continue
        # Blank means spaces and tabs only, as in CommonMark (Python's strip() would also
        # drop a non-breaking space, which a renderer treats as text).
        prev = lines[lineno - 2].strip(" \t") if lineno > 1 else ""
        if width is not None and "|" not in line:
            if line.strip(" \t"):
                refuse(lineno, "a non-blank line directly after a table renders as a row of it")
            width, expect_sep = None, False
            continue
        if "|" not in line:
            continue
        cells = eng.split_row(line)
        if line in CANONICAL_TABLE_HEADERS:
            if width is not None or prev:
                refuse(lineno, "a table header must follow a blank line (otherwise it renders "
                               "inside the table or paragraph above it)")
            width, expect_sep = len(cells), True
            continue
        bad = sorted({ch for ch in line if ch not in TABLE_LINE_ALLOWED})
        if bad:
            refuse(lineno, "a character outside the canonical table character set "
                           f"({', '.join(repr(c) for c in bad)}): raw HTML, escapes, and "
                           "invisible characters can change how the row renders")
        elif eng.ISO_HEADER in cells and eng.NIST_HEADER in cells:
            refuse(lineno, "a header-shaped row that is not the exact mapping header")
        elif width is None:
            refuse(lineno, "a pipe line outside any recognized table (an unrecognized header, "
                           "or a row cut off from its table)")
        elif not (line.startswith("|") and line.endswith("|")):
            refuse(lineno, "a table row must start at column 1 with a pipe and end with one")
        elif len(cells) != width:
            refuse(lineno, f"row has {len(cells)} cells but its table has {width}")
        elif expect_sep and not all(DELIM_CELL_RE.match(c) for c in cells):
            refuse(lineno, "the row under a table header must be a GFM delimiter row "
                           "(every cell :?-+:?)")
        elif not expect_sep and eng.is_separator_row(cells):
            refuse(lineno, "a separator row inside a table body")
        expect_sep = False
    return out


def lint_target(target: Path) -> int:
    if not target.is_file():
        print(f"ERROR: target not found: {target}", file=sys.stderr)
        return 2
    # 3b50b2d2: an unreadable (or non-UTF-8) file used to print OK after checking nothing.
    # 3b57: so did a readable file with no matrix table; it is now refused too, because it
    # selects nothing to check (quick-guard runs this gate fixed-target, with no arguments,
    # since #1246, so it no longer needs the table-less-input pass NormalizedPositionalArgsTests
    # required).
    try:
        text = target.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"ERROR: cannot read {target}: {exc}", file=sys.stderr)
        return 2
    if not has_matrix_table(text):
        print(f"ERROR: {target} holds no matrix table (no header row naming both the "
              f"ISO/IEC 27001:2022 and NIST CSF 2.0 columns); nothing to check", file=sys.stderr)
        return 2
    findings = scan_matrix(target)
    if target.resolve() == MATRIX_PATH.resolve():
        findings = sorted(findings + canonical_structure_findings(text), key=lambda f: f.line)
    rel = target.relative_to(REPO_ROOT).as_posix() if target.is_relative_to(REPO_ROOT) else str(target)
    if not findings:
        print(
            f"OK: matrix framework-control codes valid in {rel} "
            f"(CSA CCM v4.1 column membership, no AICM-only codes; "
            f"CSA AICM v1.1 column membership, AICM-only codes only, no CCM-base codes; "
            f"ISO/IEC 27001:2022 Annex A membership + clause format; "
            f"NIST CSF 2.0 well-formedness + Category membership; "
            f"AICPA TSC 2017 criterion membership where the column is present; "
            f"CCM/AICM title accuracy covered by the CSA citation gate)."
        )
        return 0
    print(f"=== {rel} ===")
    for f in findings:
        print(f"  L{f.line} [{f.rule}] {f.message}")
    print(
        f"\nFAIL: {len(findings)} matrix control-code issue(s). CSA CCM v4.1 "
        f"column tokens are validated for CCM v4.1.0 catalogue membership "
        f"(AICM-only codes rejected); CSA AICM v1.1 column tokens for AICM-only "
        f"(AI-specific) membership (CCM-base codes rejected); ISO codes against "
        f"the ISO/IEC 27001:2022 Annex A control set and clause range; NIST tokens "
        f"against the CSF 2.0 Core Function prefixes and the authoritative 22-Category set; "
        f"AICPA TSC 2017 tokens against the closed 61-criterion 2017 Trust Services Criteria set.",
        file=sys.stderr,
    )
    return 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Audit matrix framework-control codes."
    )
    parser.add_argument(
        "paths", nargs="*", default=None,
        help="Files to scan (default: the compliance matrix).",
    )
    args = parser.parse_args(argv[1:])
    targets = (
        [Path(p).resolve() for p in args.paths] if args.paths else [MATRIX_PATH]
    )
    worst = 0
    for target in targets:
        worst = max(worst, lint_target(target))
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv))
