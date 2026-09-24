#!/usr/bin/env python3
"""COBIT 2019 / ISO 31000 citation-existence audit.

The corpus cites COBIT 2019 objective and management-practice codes
(``APO12``, ``DSS05.03``) and ISO 31000:2018 clause numbers (``§6.7``,
``Clause 6.4.2``) throughout its framework-alignment tables and prose.
Gates 48/49/54/58 validate CCM/AICM, NIST, and ISO/IEC 27001 Annex A
identifiers but neither framework family here, so a fabricated COBIT
practice code or a swapped ISO 31000 clause number was gate-blind (the
motivating catches: a cited ``APO12.07`` where APO12 ends at .06, and
an ISO 31000 clause swap, both found by the 2026-07-02 audit and fixed
manually; two further live fabrications, ``MEA01.06`` and ``DSS01.06``,
were found while building this gate and fixed in the same PR).

Checks:

  * **COBIT code existence** (corpus-wide): every ``EDM|APO|BAI|DSS|MEA``
    objective token (``APO12``) must be one of the 40 COBIT 2019
    objectives, and every practice token (``APO12.06``) must fall inside
    its objective's contiguous practice range (the per-objective counts
    in :mod:`cobit_iso31000_reference`; the 231-practice set is closed).
  * **ISO 31000 clause existence** (unambiguous-adjacency scope): a
    ``§N[.N[.N]]`` / ``Clause N[.N[.N]]`` token is validated against the
    ISO 31000:2018 tree (clauses 1-6 only; the numbered term definitions
    3.1-3.8 are accepted) only where its attribution to ISO 31000 is
    unambiguous (the standard name immediately precedes it, the
    preceding table cell names only ISO 31000, or the same cell closes
    with an "(ISO 31000" attribution); clause tokens adjacent to other
    standards are never mis-attributed.
  * **Designation**: ISO 31000 is an ISO (TC 262) standard, never
    "ISO/IEC 31000"; the wrong designation is flagged anywhere.

Deliberately NOT checked (precision-first, per the audit-programme
spec's design principle 4): citation TITLES and semantic FIT. Practice
titles are not embedded in the reference module (the held extract
line-wraps them; see its provenance note), and title/fit judgment is
the ``/matrix-fit`` layer's job (``audit-matrix-semantic-fit.py``
builds the COBIT-aware worklist).

Exit codes: 0 all citations valid; 1 findings; 2 environment error
(reference module missing).
"""

from __future__ import annotations

import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path
from lint_common import DEFAULT_EXEMPT_DIRS, REPO_ROOT, guard_explicit_paths_cwd, iter_markdown_targets  # noqa: E402  # grc-config/scope

try:
    from cobit_iso31000_reference import (
        COBIT_OBJECTIVES,
        COBIT_PRACTICE_COUNTS,
        ISO31000_CLAUSES,
    )
except ImportError as exc:  # pragma: no cover - import guard
    print(f"ERROR: cannot load cobit_iso31000_reference: {exc}",
          file=sys.stderr)
    sys.exit(2)

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

# Meta-documents that describe this gate's rule set (or narrate the
# fabrication catches historically) inevitably contain the codes the
# gate searches for; per the audit-programme spec's meta-document
# exception they are exempted by name. CHANGELOG.md and TODO.md carry
# the APO12.07 catch narrative; the two specifications document the
# gate itself.
EXEMPT_FILES = frozenset({
    "CHANGELOG.md",
    "specification-audit-programme.md",
    "specification-citation-verification.md",
    "TODO.md",
    "TODO-REFERENCE.md",
})


def _engine():
    """Import the pack-owned engine, ensuring its tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_cobit_iso31000_citations  # the pack-owned engine (source of record)
    return gate_lint_cobit_iso31000_citations


def scan_file(path: Path) -> list:
    """Thin shim delegating to the pack engine's pure per-file check.

    Kept in the wrapper as a module-global because the scan-scope regression
    test patches ``mod.scan_file`` and runs ``main``; the citation regexes and
    the ``Finding`` dataclass live in the engine, and the COBIT/ISO reference
    data is threaded in from the wrapper's own import of
    ``cobit_iso31000_reference``.
    """
    return _engine().scan_file(
        path,
        cobit_objectives=COBIT_OBJECTIVES,
        cobit_practice_counts=COBIT_PRACTICE_COUNTS,
        iso31000_clauses=ISO31000_CLAUSES,
    )


def _display_path(path: Path) -> str:
    """Repo-relative POSIX path for display, falling back to the absolute path for a
    target outside REPO_ROOT (a hand-invocation on an external file), so the findings
    loop never raises ValueError from ``relative_to`` (deep-assessment r5 Low-3 / 3.98 (closing PR #1010))."""
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main(argv: list[str]) -> int:
    # 3b48: explicit paths are refused when missing (a content check on the held COBIT and ISO 31000 catalogues; #1010 made out-of-tree reporting sound), else normalized.
    paths = guard_explicit_paths_cwd(argv[1:], repo_root=REPO_ROOT, allow_outside=True) if argv[1:] else [str(REPO_ROOT)]
    targets = iter_markdown_targets(
        paths, exempt_dirs=DEFAULT_EXEMPT_DIRS, exempt_files=EXEMPT_FILES)
    all_findings: list[Finding] = []
    for path in targets:
        all_findings.extend(scan_file(path))

    if not all_findings:
        print(
            f"OK: COBIT/ISO 31000 citations valid across {len(targets)} "
            f"files ({len(COBIT_OBJECTIVES)} objectives, "
            f"{sum(COBIT_PRACTICE_COUNTS.values())} practices, "
            f"{len(ISO31000_CLAUSES)} ISO 31000 clause numbers in the "
            f"reference).")
        return 0

    by_file: dict[Path, list[Finding]] = {}
    for f in all_findings:
        by_file.setdefault(f.path, []).append(f)
    for path in sorted(by_file):
        print(f"=== {_display_path(path)} ===")
        for f in by_file[path]:
            print(f"  L{f.line} [{f.rule}] {f.message}")
    print(
        f"\nFAIL: {len(all_findings)} COBIT/ISO 31000 citation issue(s) "
        f"across {len(by_file)} file(s). The authoritative reference is "
        f"tools/cobit_iso31000_reference.py (COBIT 2019 / ISO 31000:2018).",
        file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
