#!/usr/bin/env python3
"""Per-document ISO/IEC 27001:2022 Annex A validity audit - grc wrapper over the pack engine.

Validate ISO/IEC 27001:2022 Annex A codes wherever they appear in per-document
framework tables (the central compliance matrix is gate 49's target and is excluded
here). The authoritative Annex A structure lives in the shared ``iso_27001_reference``
module, also used by gate 49.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan
(_check_theme, _check_range, findings_in, scan_file) plus the ISO parsing patterns
live in the pack-owned engine (.corpus-management/tools/gate_lint_document_iso_annex_a.py,
source of record); the engine takes the reference as a predicate (check_iso_token) +
the theme set (ISO_ANNEX_A_RANGES) + repo_root as params. This wrapper imports the
shared reference, supplies those, and keeps the grc scan scope (collect_targets, with
the matrix exclusion), the module-global scan_file(path) shim (call-time REPO_ROOT,
for the regression tests that call it directly), the reporting, and the exit codes.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import is_default_exempt_root, AUDITED_DOMAIN_DIRS, REPO_ROOT, iter_markdown_targets  # noqa: E402  # grc-config/store, stays local
from iso_27001_reference import ISO_ANNEX_A_RANGES, check_iso_token  # noqa: E402  # grc reference catalogue, shared with gate 49

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

# The central matrix is gate 49's exact target; exclude it here to avoid
# duplicate coverage. Path is relative to REPO_ROOT, posix form.
MATRIX_REL = "compliance/matrix-grc-compliance-alignment.md"


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_document_iso_annex_a  # the pack-owned engine (source of record)
    return gate_lint_document_iso_annex_a


def collect_targets(paths: list[str] | None) -> list[Path]:
    """Resolve the scan targets: explicit paths, or the audited corpus."""
    if paths:
        return [
            Path(p).resolve() for p in paths
            if not is_default_exempt_root(Path(p).resolve(), repo_root=REPO_ROOT)
        ]
    roots = [REPO_ROOT / d for d in (*AUDITED_DOMAIN_DIRS, "guardrails")]
    out: list[Path] = []
    for p in iter_markdown_targets(roots):
        rel = p.relative_to(REPO_ROOT).as_posix() if p.is_relative_to(REPO_ROOT) else str(p)
        if rel == MATRIX_REL:
            continue
        out.append(p)
    return out


def scan_file(path: Path) -> list:
    """Thin shim delegating to the pack engine's pure scan.

    Kept as a module-global because the regression tests call ``mod.scan_file(path)``
    directly (and mutate ``mod.REPO_ROOT``); the shim reads ``REPO_ROOT`` at call time
    so a test override is honoured, and supplies the shared ISO reference.
    """
    return _engine().scan_file(path, REPO_ROOT, check_iso_token, ISO_ANNEX_A_RANGES)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Audit ISO/IEC 27001:2022 Annex A codes in per-document framework tables."
    )
    parser.add_argument(
        "paths", nargs="*", default=None,
        help="Documents to scan (default: the audited corpus).",
    )
    args = parser.parse_args(argv[1:])
    explicit = bool(args.paths)
    targets = collect_targets(args.paths)
    if explicit:
        missing = [t for t in targets if not t.is_file()]
        if missing:
            print(f"ERROR: target not found: {missing[0]}", file=sys.stderr)
            return 2

    findings = []
    for path in targets:
        findings.extend(scan_file(path))

    if not findings:
        scope = (
            f"{len(targets)} explicit document(s)" if explicit
            else f"{len(targets)} corpus document(s)"
        )
        print(
            f"OK: ISO/IEC 27001:2022 Annex A codes in per-document framework tables are valid "
            f"({scope}; Annex A theme/control ranges and clause range; matrix excluded)."
        )
        return 0

    by_file: dict[str, list] = {}
    for f in findings:
        by_file.setdefault(f.path, []).append(f)
    for rel in sorted(by_file):
        print(f"=== {rel} ===")
        for f in by_file[rel]:
            print(f"  L{f.line} [{f.rule}] {f.message}")
    print(
        f"\nFAIL: {len(findings)} per-document ISO/IEC 27001:2022 Annex A control-code "
        f"issue(s) across {len(by_file)} file(s). Codes are validated against the "
        f"authoritative 2022 Annex A theme/control ranges (A.5-A.8) and clause range "
        f"(§4-§10); only cells governed by an ISO 27001:2022 label are scanned.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
