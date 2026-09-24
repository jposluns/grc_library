#!/usr/bin/env python3
"""Central compliance-matrix framework-control-code validity - grc wrapper over the pack engine.

Validate every framework-control code in the central compliance matrix
(compliance/matrix-grc-compliance-alignment.md): CSA CCM v4.1 / AICM v1.1 column
membership, ISO/IEC 27001:2022 Annex A membership + clause format, and NIST CSF 2.0
well-formedness + Category membership.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan
(Finding, the header/regex constants, the row helpers, the per-framework checks, and
scan_matrix) is the source of record in the pack engine
(.corpus-management/tools/gate_lint_matrix_control_codes.py); it is catalogue-free and
takes the five framework-reference predicates via configure(ref). This wrapper imports
the shared grc reference modules, configures the engine, and keeps the matrix scan
scope (MATRIX_PATH), a module-global scan_matrix(path) shim, lint_target, main, and
the exit codes: 0 clean (a readable file with no matrix table is clean, as the #1245
positional-multifile contract requires), 1 on findings, 2 when a target is missing or cannot be
read as UTF-8.
"""

from __future__ import annotations

import argparse
import sys
import types
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from ccm_aicm_reference import is_aicm_only, is_ccm_v41  # noqa: E402  # grc reference catalogue
from iso_27001_reference import check_iso_token  # noqa: E402  # shared with gate 58
from nist_csf_reference import is_valid_category, relocation_note  # noqa: E402  # shared with gate 54
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
))


def scan_matrix(path: Path) -> list:
    """Thin shim delegating to the pack engine's pure scan (engine already configured)."""
    return _engine().scan_matrix(path)


def lint_target(target: Path) -> int:
    if not target.is_file():
        print(f"ERROR: target not found: {target}", file=sys.stderr)
        return 2
    # 3b50b2d2: an unreadable (or non-UTF-8) file used to print OK after checking nothing. A
    # readable file with no matrix table stays a clean pass: NormalizedPositionalArgsTests (#1245)
    # requires table-less .md input to exit 0. quick-guard itself runs this gate fixed-target, with
    # no arguments, since #1246.
    try:
        target.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"ERROR: cannot read {target}: {exc}", file=sys.stderr)
        return 2
    findings = scan_matrix(target)
    rel = target.relative_to(REPO_ROOT).as_posix() if target.is_relative_to(REPO_ROOT) else str(target)
    if not findings:
        print(
            f"OK: matrix framework-control codes valid in {rel} "
            f"(CSA CCM v4.1 column membership, no AICM-only codes; "
            f"CSA AICM v1.1 column membership, AICM-only codes only, no CCM-base codes; "
            f"ISO/IEC 27001:2022 Annex A membership + clause format; "
            f"NIST CSF 2.0 well-formedness + Category membership; "
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
        f"against the CSF 2.0 Core Function prefixes and the authoritative 22-Category set.",
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
