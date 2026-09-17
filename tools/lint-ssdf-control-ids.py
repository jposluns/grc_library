#!/usr/bin/env python3
"""NIST SSDF control-identifier validity audit - grc wrapper over the pack engine.

Flag a NIST SSDF (SP 800-218 / 800-218A) control identifier that is not a valid
practice/task id, or a non-SSDF code sitting in an SSDF-labelled column.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan (the
SSDF regexes, _split_cells, _is_sep, _validate_ssdf_id, check_file) is the source of
record in the pack engine (.corpus-management/tools/gate_lint_ssdf_control_ids.py);
it is catalogue-free and takes the SSDF catalogue via configure(ref). This wrapper
supplies the catalogue (valid practices/tasks; the family tuple is engine-fixed), configures the engine,
and keeps EXEMPT_SUFFIXES, a module-global check_file shim, main, and the exit codes.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # own dir on sys.path (matches original; programmatic-load safe)
import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path (engine imports aiqt_corpus)
from lint_common import REPO_ROOT, iter_markdown_targets  # noqa: E402  # grc-config/store, stays local

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

# --- Valid SSDF ids (SP 800-218 v1.1, from the NIST OSCAL catalogue) ---
VALID_PRACTICES = {
    "PO.1", "PO.2", "PO.3", "PO.4", "PO.5",
    "PS.1", "PS.2", "PS.3",
    "PW.1", "PW.2", "PW.3", "PW.4", "PW.5", "PW.6", "PW.7", "PW.8", "PW.9",  # PW.3 is 800-218A
    "RV.1", "RV.2", "RV.3",
}
VALID_TASKS = {
    # Union of SP 800-218 v1.1 (base) and SP 800-218A (Generative AI profile),
    # since the corpus cites both. 800-218A adds PW.3.x, PO.5.3, PS.1.2/1.3.
    # NB: PW.4.3 is NOT valid: a v1.0 task moved for v1.1 whose id was not reused
    # (218A gap-numbering note, lines 579-580); PW.4 has 4.1/4.2/4.4 only.
    "PO.1.1", "PO.1.2", "PO.1.3", "PO.2.1", "PO.2.2", "PO.2.3",
    "PO.3.1", "PO.3.2", "PO.3.3", "PO.4.1", "PO.4.2", "PO.5.1", "PO.5.2", "PO.5.3",
    "PS.1.1", "PS.1.2", "PS.1.3", "PS.2.1", "PS.3.1", "PS.3.2",
    "PW.1.1", "PW.1.2", "PW.1.3", "PW.2.1", "PW.3.1", "PW.3.2", "PW.3.3",
    "PW.4.1", "PW.4.2", "PW.4.4",
    "PW.5.1", "PW.6.1", "PW.6.2", "PW.7.1", "PW.7.2", "PW.8.1", "PW.8.2",
    "PW.9.1", "PW.9.2",
    "RV.1.1", "RV.1.2", "RV.1.3", "RV.2.1", "RV.2.2",
    "RV.3.1", "RV.3.2", "RV.3.3", "RV.3.4",
}

# Files where SSDF-shaped strings are historical description, not live citations.
EXEMPT_SUFFIXES = (
    "CHANGELOG.md",
    "governance/specification-audit-programme.md",  # gate-description prose uses example codes
)


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_ssdf_control_ids  # the pack-owned engine (source of record)
    return gate_lint_ssdf_control_ids


# Configure the engine ONCE with the grc SSDF catalogue.
import types  # noqa: E402
_engine().configure(types.SimpleNamespace(
    valid_practices=VALID_PRACTICES, valid_tasks=VALID_TASKS))


def check_file(path: Path, rel: str) -> list[str]:
    """Thin shim delegating to the pack engine's pure scan (engine already configured);
    kept module-global so the scan-scope regression meta-test can call it."""
    return _engine().check_file(path, rel)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="NIST SSDF control-identifier validity audit.")
    ap.add_argument("paths", nargs="*", default=[str(REPO_ROOT)],
                    help="files or directories to scan (default: the whole repository)")
    args = ap.parse_args(argv[1:])
    findings: list[str] = []
    for path in iter_markdown_targets(args.paths or [str(REPO_ROOT)]):
        rel = path.relative_to(REPO_ROOT).as_posix()
        if rel.endswith(EXEMPT_SUFFIXES):
            continue
        findings.extend(check_file(path, rel))
    if findings:
        print("FAIL: invalid NIST SSDF control identifier(s) found:")
        for f in sorted(set(findings)):
            print(f"  - {f}")
        print(
            "\nSSDF (SP 800-218 v1.1) has exactly four practice groups: PO, PS, PW, RV. "
            "Correct the id to a valid practice/task, or (for a semantic remap) to the "
            "SSDF task that fits."
        )
        return 1
    print("OK: all NIST SSDF control identifiers are valid (SP 800-218 v1.1).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
