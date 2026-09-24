#!/usr/bin/env python3
"""Cross-document retention-consistency audit - grc wrapper over the pack-owned engine.

Verify that each procedure document's evidence-retention period matches the canonical
period for the same category in the central data-retention-schedule register.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE check
(normalise, register_value, procedure_value, collect_findings) plus the generic
period-parsing config live in the pack-owned engine
(.corpus-management/tools/gate_lint_retention_consistency.py, source of record).
This wrapper supplies the grc config: the register path, the register-category-to-
procedure check list, the procedure anchor phrase, and the --root handling and
reporting.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from aiqt_corpus import read_text_safe  # noqa: E402  # generic core (behaviour-identical to lint_common)
from lint_common import REPO_ROOT, require_dir  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

REGISTER = "governance/register-data-retention-schedule.md"

# Each check names a register row (matched on its first table cell, case-
# insensitive, exact after trimming) and the procedure document that must cite
# the same retention period.
RETENTION_CHECKS: list[dict[str, str]] = [
    {
        "label": "CAPA records evidence-retention",
        "register_category": "CAPA records",
        "procedure": "compliance/procedure-capa.md",
    },
    {
        "label": "Internal-audit evidence-retention",
        "register_category": "Internal audit reports",
        "procedure": "compliance/standard-internal-audit.md",
    },
    {
        "label": "Control-testing evidence-retention",
        "register_category": "Control testing evidence",
        "procedure": "compliance/procedure-control-testing.md",
    },
    {
        "label": "Privacy-impact-assessment record-retention",
        "register_category": "Privacy impact assessments",
        "procedure": "privacy/procedure-privacy-impact-and-cross-border-transfer.md",
    },
    {
        "label": "Privacy-breach evidence-retention",
        "register_category": "Privacy breach notifications",
        "procedure": "privacy/procedure-data-protection-and-privacy-breach-response.md",
    },
    {
        "label": "AI-impact-assessment record-retention",
        "register_category": "AI Impact Assessments",
        "procedure": "privacy/procedure-privacy-impact-and-cross-border-transfer.md",
    },
    {
        "label": "AI-audit report-retention",
        "register_category": "AI audit reports",
        "procedure": "ai/procedure-ai-audit.md",
    },
    {
        "label": "Supplier-audit report-retention",
        "register_category": "Supplier audit reports",
        "procedure": "supply-chain/procedure-supplier-audit.md",
    },
]

# The procedure's retention statement is anchored on this phrase so the linter
# pins the evidence-retention figure and not an unrelated period elsewhere.
PROCEDURE_ANCHOR_RE = re.compile(
    r"retained for a minimum of[^.\n]*?(\d+)[\s-]*(year|month|day)s?",
    re.IGNORECASE,
)


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_retention_consistency  # the pack-owned engine (source of record)
    return gate_lint_retention_consistency


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Verify cross-document retention-period consistency."
    )
    parser.add_argument(
        "--root",
        default=str(REPO_ROOT),
        help="Repository root to resolve the register and procedures against "
        "(defaults to the live repo; overridden in regression tests).",
    )
    args = parser.parse_args(argv[1:])
    if args.root is not None:  # 3b50b2d1: a missing, empty or non-directory --root is refused
        args.root = require_dir(args.root, "--root")
    root = Path(args.root)

    register_path = root / REGISTER
    register_text = read_text_safe(register_path) if register_path.is_file() else None
    if register_text is None:
        print(f"FAIL: cannot read the retention register at {REGISTER}.")
        return 1

    findings = _engine().collect_findings(
        register_text, root, RETENTION_CHECKS, PROCEDURE_ANCHOR_RE, REGISTER
    )

    if findings:
        for f in findings:
            print(f"  - {f}")
        print(
            f"\nFAIL: {len(findings)} retention-consistency issue(s). A procedure's "
            f"evidence-retention period must match the canonical row in {REGISTER}."
        )
        return 1

    print(
        f"OK: {len(RETENTION_CHECKS)} retention pair(s) consistent; each procedure's "
        f"evidence-retention period matches its canonical row in {REGISTER}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
