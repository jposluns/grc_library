#!/usr/bin/env python3
"""COBIT objective-title canonicality audit - grc wrapper over the pack engine.

Flag a COBIT objective code whose paired title in the corpus is not the canonical
COBIT 2019 objective title (a wrong-title citation the existence gate cannot see).

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan (the
objective-code/title regexes, _norm, extract_title, scan_text, scan_file) is the
source of record in the pack engine
(.corpus-management/tools/gate_lint_cobit_title_text.py); it is catalogue-free and
takes the COBIT objective catalogue via configure(). This wrapper imports the
cobit_iso31000_reference catalogue (shared with gate 61), configures the engine, and
keeps EXEMPT_FILES, a module-global scan_file shim, main, and the exit codes.
"""

from __future__ import annotations

import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack tools/ on sys.path (engine imports aiqt_corpus)
from lint_common import DEFAULT_EXEMPT_DIRS, REPO_ROOT, iter_markdown_targets  # noqa: E402  # grc-config/store, stays local

try:
    from cobit_iso31000_reference import COBIT_OBJECTIVES  # noqa: E402  # grc reference catalogue (shared with gate 61)
except ImportError as exc:  # pragma: no cover - environment guard
    print(f"ERROR: cannot import the COBIT reference module: {exc}", file=sys.stderr)
    raise SystemExit(2)

PACK_TOOLS = Path(__file__).resolve().parent.parent / ".corpus-management" / "tools"

# Files whose COBIT code tokens are illustrative or meta, not corpus
# citations. Same set gate 61 exempts (the audit-programme spec, the
# citation-verification spec, TODO, and CHANGELOG all discuss codes as
# examples), so the two COBIT gates share one scope.
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
    import gate_lint_cobit_title_text  # the pack-owned engine (source of record)
    return gate_lint_cobit_title_text


# Configure the engine ONCE with the grc COBIT objective catalogue.
_engine().configure(COBIT_OBJECTIVES)


def scan_file(path: Path) -> list[tuple[Path, int, str, str, str]]:
    """Thin shim delegating to the pack engine's pure scan (engine already configured);
    kept module-global so the scan-scope regression meta-test can call it."""
    return _engine().scan_file(path)


def main(argv: list[str]) -> int:
    paths = argv[1:] or [str(REPO_ROOT)]
    targets = iter_markdown_targets(
        paths, exempt_dirs=DEFAULT_EXEMPT_DIRS, exempt_files=EXEMPT_FILES)
    findings: list[tuple[Path, int, str, str, str]] = []
    for path in targets:
        findings.extend(scan_file(path))

    if not findings:
        print(f"OK: COBIT objective titles canonical across {len(targets)} "
              f"files ({len(COBIT_OBJECTIVES)} objective titles in the "
              f"reference).")
        return 0

    by_file: dict[Path, list[tuple[Path, int, str, str, str]]] = {}
    for f in findings:
        by_file.setdefault(f[0], []).append(f)
    for path in sorted(by_file):
        rel = path.relative_to(REPO_ROOT).as_posix()
        print(f"=== {rel} ===")
        for _, ln, code, found, canon in by_file[path]:
            print(f"  L{ln} [cobit-title] {code}: found \"{found}\", "
                  f"canonical \"{canon}\"")
    print(f"\nFAIL: {len(findings)} non-canonical COBIT objective title(s) "
          f"across {len(by_file)} file(s). The authoritative reference is "
          f"tools/cobit_iso31000_reference.py (COBIT_OBJECTIVES).",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
