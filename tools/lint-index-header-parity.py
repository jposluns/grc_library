#!/usr/bin/env python3
"""Index-header parity audit - grc wrapper over the pack-owned engine.

The document index register
(``governance/register-document-index-and-classification.md``) mirrors, per
active document, its Owner Role, Review Frequency and Title from that document's
own metadata header, the go-forward source of truth. This gate locks that mirror;
the Title comparison is a ratchet against a pinned baseline of known diffs.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE check
(cadence_tokens, find_index_table, check_row with its three comparators,
collect_findings) plus the generic review-cadence recognizer + code-span-link
regex live in the pack-owned engine
(.corpus-management/tools/gate_lint_index_header_parity.py, source of record).
This wrapper supplies the grc index register schema (the index relative path, the
8-column header row, the column indices, the Owner/Review Frequency/Document Title
metadata field names) + the per-document base-cadence allow-list + the title
baseline and its classes + the --root and --strict-owner handling + the
register-missing/unreadable/table-not-found environmental exits + the
WARNING/DRIFT/FAIL/summary reporting.

Title ratchet (3b150): titles are compared by stripped equality. The frozen
2026-10-01 baseline pins 44 exact index/header pairs: 29 deliberate-shortening
privacy jurisdiction annexes and 15 real-drift rows. A pinned pair passes; a
real-drift pair also prints a DRIFT work item. A NEW or CHANGED difference, a
stale entry whose titles now agree, an empty title, a missing or repeated
Document Title field and a malformed baseline entry are findings. A baseline path
that matches no readable row fails on a default-root run and warns under an
explicit --root, so partial fixture trees keep working.

Usage:
    python3 tools/lint-index-header-parity.py
    python3 tools/lint-index-header-parity.py --strict-owner
    python3 tools/lint-index-header-parity.py --root /path/to/alt-repo

Exit codes (per the tests/README.md convention):
    0  clean (warnings and DRIFT work items may be present)
    1  one or more findings (owner under --strict-owner, cadence, title or
       title baseline, malformed row, missing or unreadable linked file, header
       missing a needed field)
    2  environmental error (register file missing, unreadable or not valid
       UTF-8, or its active-index header row not found)
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
COL_TITLE = 2   # the engine's third comparator (the 3b150 title ratchet)
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


# Frozen 2026-10-01 title evidence: 44 exact pairs, classified as 29
# deliberate-shortening privacy annexes and 15 real-drift rows. All 29 privacy
# jurisdiction annexes drop Regulatory; EU, UK, US and UAE also abbreviate the
# jurisdiction. Drift: 8 index doctype omissions, 2 header doctype omissions,
# 1 CAPA omission, 1 IT scope omission, 1 DPIA acronym omission, 1 OT expansion
# mismatch and 1 FAIR annotation. No family-wide convention supports those 15.
# Every drift pair is a work item; every pair remains pinned until reconciled.
# Re-checked against main 0375cb3a6 on 2026-10-22: 44 of 44 pairs still exact.
# Tuple shape: (index title, header title, class, one-line rationale).
TITLE_FIELD = "Document Title"
TITLE_DIFF_CLASSES = ("deliberate-shortening", "real-drift")
TITLE_WORKLIST_CLASSES = frozenset({"real-drift"})  # pinned pairs printed as DRIFT work items
_WHY_DOCTYPE = ("Real drift: 124 of 136 Standard/Procedure index titles retain their "
                "doctype (71/78 Standards, 53/58 Procedures); this omission is not a family rule.")
_WHY_JURISDICTION = ("Privacy-family shortening: all 30 jurisdiction annexes drop Regulatory; "
                     "EU, UK, US and UAE also abbreviate the jurisdiction name.")
TITLE_DIFF_BASELINE: dict[str, tuple[str, str, str, str]] = {
    "compliance/policy-compliance-and-audit-management.md": (
        "Compliance and Audit Management Policy",
        "Compliance, Audit, and CAPA Management Policy",
        "real-drift",
        "Real drift: the index omits CAPA management, while the compliance CAPA "
        "procedure retains CAPA on both sides; this is not a family shortening rule.",
    ),
    "security/procedure-onboarding-and-offboarding.md": (
        "Onboarding and Offboarding Procedure",
        "IT Onboarding and Offboarding Procedure",
        "real-drift",
        "Real drift: the index drops the header scope qualifier IT; other indexed "
        "IT titles retain that qualifier. Scope removal is not an index-wide convention.",
    ),
    "operations/standard-network-security-and-segmentation.md": (
        "Network Security and Segmentation",
        "Network Security and Segmentation Standard",
        "real-drift",
        _WHY_DOCTYPE,
    ),
    "operations/standard-physical-security-of-it-infrastructure.md": (
        "Physical Security of IT Infrastructure",
        "Physical Security of IT Infrastructure Standard",
        "real-drift",
        _WHY_DOCTYPE,
    ),
    "operations/standard-certificate-authority-management.md": (
        "Certificate Authority Management",
        "Certificate Authority Management Standard",
        "real-drift",
        _WHY_DOCTYPE,
    ),
    "operations/procedure-change-management-and-configuration-control.md": (
        "Change Management and Configuration Control",
        "Change Management and Configuration Control Procedure",
        "real-drift",
        _WHY_DOCTYPE,
    ),
    "operations/procedure-endpoint-management-and-device-compliance.md": (
        "Endpoint Management and Device Compliance",
        "Endpoint Management and Device Compliance Procedure",
        "real-drift",
        _WHY_DOCTYPE,
    ),
    "operations/procedure-media-handling-and-transport.md": (
        "Media Handling and Transport",
        "Media Handling and Transport Procedure",
        "real-drift",
        _WHY_DOCTYPE,
    ),
    "operations/procedure-security-monitoring-and-alert-management.md": (
        "Security Monitoring and Alert Management",
        "Security Monitoring and Alert Management Procedure",
        "real-drift",
        _WHY_DOCTYPE,
    ),
    "operations/procedure-threat-intelligence-and-siem-operations.md": (
        "Threat Intelligence and SIEM Operations",
        "Threat Intelligence and SIEM Operations Procedure",
        "real-drift",
        _WHY_DOCTYPE,
    ),
    "privacy/template-dpia.md": (
        "Data Protection Impact Assessment Template",
        "DPIA (Data Protection Impact Assessment) Template",
        "real-drift",
        "Real drift: the index drops DPIA, while sibling privacy templates retain "
        "LIA and TIA on both sides; acronym removal is not a family convention.",
    ),
    "privacy/jurisdictions/annex-privacy-european-union.md": (
        "EU Privacy Requirements",
        "European Union Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-united-kingdom.md": (
        "UK Privacy Requirements",
        "United Kingdom Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-switzerland.md": (
        "Switzerland Privacy Requirements",
        "Switzerland Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-canada.md": (
        "Canada Privacy Requirements",
        "Canada Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-united-states.md": (
        "US Privacy Requirements",
        "United States Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-brazil.md": (
        "Brazil Privacy Requirements",
        "Brazil Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-latin-america.md": (
        "Latin America Privacy Requirements",
        "Latin America Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-mexico.md": (
        "Mexico Privacy Requirements",
        "Mexico Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-chile.md": (
        "Chile Privacy Requirements",
        "Chile Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-peru.md": (
        "Peru Privacy Requirements",
        "Peru Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-colombia.md": (
        "Colombia Privacy Requirements",
        "Colombia Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-ecuador.md": (
        "Ecuador Privacy Requirements",
        "Ecuador Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-singapore.md": (
        "Singapore Privacy Requirements",
        "Singapore Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-australia.md": (
        "Australia Privacy Requirements",
        "Australia Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-japan.md": (
        "Japan Privacy Requirements",
        "Japan Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-south-korea.md": (
        "South Korea Privacy Requirements",
        "South Korea Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-new-zealand.md": (
        "New Zealand Privacy Requirements",
        "New Zealand Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-uae.md": (
        "UAE Privacy Requirements",
        "United Arab Emirates Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-saudi-arabia.md": (
        "Saudi Arabia Privacy Requirements",
        "Saudi Arabia Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-south-africa.md": (
        "South Africa Privacy Requirements",
        "South Africa Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-turkey.md": (
        "Turkey Privacy Requirements",
        "Turkey Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-nigeria.md": (
        "Nigeria Privacy Requirements",
        "Nigeria Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-kenya.md": (
        "Kenya Privacy Requirements",
        "Kenya Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-china.md": (
        "China Privacy Requirements",
        "China Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-india.md": (
        "India Privacy Requirements",
        "India Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-thailand.md": (
        "Thailand Privacy Requirements",
        "Thailand Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-indonesia.md": (
        "Indonesia Privacy Requirements",
        "Indonesia Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-philippines.md": (
        "Philippines Privacy Requirements",
        "Philippines Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-vietnam.md": (
        "Vietnam Privacy Requirements",
        "Vietnam Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "privacy/jurisdictions/annex-privacy-malaysia.md": (
        "Malaysia Privacy Requirements",
        "Malaysia Privacy Regulatory Requirements",
        "deliberate-shortening",
        _WHY_JURISDICTION,
    ),
    "dev-security/standard-developer-security-requirements.md": (
        "Developer Security Requirements Standard",
        "Developer Security Requirements",
        "real-drift",
        "Real drift: the index retains Standard, as 71 of 78 Standard rows do; "
        "the header omits it. Reconcile the pair without inventing an inverse convention.",
    ),
    "dev-security/standard-devops-security-requirements.md": (
        "DevOps Security Requirements Standard",
        "DevOps Security Requirements",
        "real-drift",
        "Real drift: the index retains Standard, as 71 of 78 Standard rows do; "
        "the header omits it. Reconcile the pair without inventing an inverse convention.",
    ),
    "operations/ot/annex-ot-security-overview.md": (
        "OT Security Overview Annex",
        "Operational Technology Security Overview Annex",
        "real-drift",
        "Real drift: four OT-named siblings use OT on both sides; only this "
        "header expands Operational Technology. No family-wide title difference exists.",
    ),
    "risk/guideline-quantitative-risk-analysis.md": (
        "Quantitative Risk Analysis Guideline (FAIR-aligned)",
        "Quantitative Risk Analysis Guideline",
        "real-drift",
        "Real drift: the index adds a (FAIR-aligned) annotation absent from the "
        "header; reconcile where the annotation belongs.",
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
                        help="Override repository root; unmatched title-baseline paths warn.")
    parser.add_argument("--strict-owner", action="store_true",
                        help="Treat an Owner Role mismatch as a finding instead of a warning.")
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
    except (OSError, UnicodeError) as exc:
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
        col_title=COL_TITLE,
        title_field=TITLE_FIELD,
        title_baseline=TITLE_DIFF_BASELINE,  # looked up per call, so tests can patch it
        title_classes=frozenset(TITLE_DIFF_CLASSES),
        title_worklist_classes=TITLE_WORKLIST_CLASSES,
        title_baseline_partial=args.root is not None,
    )
    if result is None:
        print("ERROR (environmental): active-index table header row not found in "
              f"{INDEX_REL}", file=sys.stderr)
        return 2
    findings, warnings, rows_checked, drift_rows = result

    for w in warnings:
        print(f"WARNING: {w}")
    for d in drift_rows:
        print(f"DRIFT (baselined real drift, awaiting the corpus title reconcile): {d}")
    for f in findings:
        print(f"FAIL: {f}")
    if findings:
        print(f"\nIndex-header parity: {len(findings)} finding(s).")
        return 1
    # The engine reports every row that skips the title comparison as a finding,
    # so a clean run compared the title cell of every row checked.
    print(f"Index-header parity: {rows_checked} rows checked ({rows_checked} title cells ratcheted), clean"
          + (f" ({len(warnings)} warning(s))" if warnings else "")
          + (f"; {len(drift_rows)} baselined real-drift title row(s) await the corpus reconcile"
             if drift_rows else "")
          + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
