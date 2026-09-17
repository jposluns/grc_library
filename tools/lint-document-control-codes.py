#!/usr/bin/env python3
"""Per-document NIST CSF 2.0 control-code validity audit - grc wrapper over the pack engine.

Validate NIST CSF 2.0 codes wherever they appear in per-document framework tables
(the central compliance matrix is gate 49's target and is excluded here). The
authoritative 22-Category CSF 2.0 set and the CSF-1.1 relocation map live in
``nist_csf_reference.py`` (transcribed from NIST CSWP 29 Table 1), shared with gate 49.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan
(check_code, codes_in, scan_file) plus the NIST-CSF parsing patterns live in the
pack-owned engine (.corpus-management/tools/gate_lint_document_control_codes.py,
source of record); the engine takes the catalogue as two predicates
(is_valid_category, relocation_note) and repo_root as params. This wrapper imports
the shared reference, supplies those predicates, and keeps the grc scan scope
(collect_targets, with the matrix exclusion) and the grouped reporting + exit codes.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import is_default_exempt_root, AUDITED_DOMAIN_DIRS, REPO_ROOT, iter_markdown_targets  # noqa: E402  # grc-config/store, stays local
from nist_csf_reference import is_valid_category, relocation_note  # noqa: E402  # grc reference catalogue, shared with gate 49

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

# The central matrix is gate 49's exact target; exclude it here to avoid
# duplicate coverage. Path is relative to REPO_ROOT, posix form.
MATRIX_REL = "compliance/matrix-grc-compliance-alignment.md"


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_document_control_codes  # the pack-owned engine (source of record)
    return gate_lint_document_control_codes


def collect_targets(paths: list[str] | None) -> list[Path]:
    """Resolve the scan targets: explicit paths, or the audited corpus."""
    if paths:
        return [
            Path(p).resolve() for p in paths
            if not is_default_exempt_root(Path(p).resolve(), repo_root=REPO_ROOT)
        ]
    roots = [REPO_ROOT / d for d in (*AUDITED_DOMAIN_DIRS, "guardrails")]
    targets = iter_markdown_targets(roots)
    out: list[Path] = []
    for p in targets:
        rel = p.relative_to(REPO_ROOT).as_posix() if p.is_relative_to(REPO_ROOT) else str(p)
        if rel == MATRIX_REL:
            continue
        out.append(p)
    return out


def scan_file(path: Path) -> list:
    """Thin shim delegating to the pack engine's pure scan.

    Kept as a module-global because the regression tests call ``mod.scan_file(path)``
    directly (and mutate ``mod.REPO_ROOT``); the shim reads ``REPO_ROOT`` at call time
    so a test override is honoured, and supplies the shared CSF reference predicates.
    """
    return _engine().scan_file(path, REPO_ROOT, is_valid_category, relocation_note)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Audit NIST CSF 2.0 codes in per-document framework tables."
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
            f"OK: NIST CSF 2.0 codes in per-document framework tables are valid "
            f"({scope}; CSF 2.0 Category membership; matrix excluded)."
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
        f"\nFAIL: {len(findings)} per-document NIST CSF 2.0 control-code issue(s) "
        f"across {len(by_file)} file(s). Codes are validated at the Category level "
        f"against the authoritative CSF 2.0 22-Category set; CSF-1.1-era codes are "
        f"flagged with a relocation note.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
