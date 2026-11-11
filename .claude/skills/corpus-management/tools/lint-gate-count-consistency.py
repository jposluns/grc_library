#!/usr/bin/env python3
"""Cross-file gate-count consistency audit (grc gate 39): project entry point.

The gate ENGINE is pack-owned source of record at
``.claude/skills/corpus-management/src/tools/gate_lint_gate_count_consistency.py`` (Corpus-Management pack, gate
register ``core/gates.toml``, id ``lint-gate-count-consistency``, enforcing the pack's
``gate-count-consistency`` clause); this thin wrapper keeps the house
``python3 .claude/skills/corpus-management/tools/lint-gate-count-consistency.py`` shape (gate 35 parses exactly that) and supplies
the grc-local configuration the pack engine deliberately does not carry: the AIQT bootstrap; the
canonical-count sources (the audit-programme spec path, parsed for the §6 gate-inventory row count
by ``parse_canonical_count``, and the rule / skill collection directories); the scan scope (the
scanned suffixes, the exempt-file / exempt-dir sets, the ``iter_targets`` selector kept here so the
scan-scope regression's ALLOW map observes it unmoved); and a ``scan_file`` shim (so a
direct-module-load test observes ``scan_file`` on the wrapper). The wrapper builds the
canonical-count map and delegates the scan + report to the engine. These wrapper bytes are
HAND-MAINTAINED, not compiler-generated, so gate 99 does NOT own them.

Usage:
    python3 .claude/skills/corpus-management/tools/lint-gate-count-consistency.py
    python3 .claude/skills/corpus-management/tools/lint-gate-count-consistency.py path1 path2 ...

Exit codes:
    0   no findings.
    1   one or more stale-count findings.
    2   the canonical gate count could not be parsed (a prerequisite failure).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: verifies the vendored AIQT pack .claude/aiqt/ and publishes aiqt_corpus in sys.modules
from aiqt_corpus import read_text_safe  # noqa: E402  # generic core (behaviour-identical to lint_common)
from lint_common import guard_explicit_paths_cwd, has_exempt_part, is_default_exempt_root, CORPUS_MANAGEMENT_DIR, DEFAULT_EXEMPT_DIRS, PROJECT_DOCUMENT_DIRS, PROJECT_DOCUMENT_FILES, REPO_ROOT  # noqa: E402  # grc-config/store, stays local

# Derive the pack .claude/skills/corpus-management/src/tools/ from this file's location, independent of REPO_ROOT.
PACK_TOOLS = Path(__file__).resolve().parent.parent / "src" / "tools"

SPEC_PATH = (REPO_ROOT / ".claude" / "skills" / "corpus-management" / "specs"
             / "specification-audit-programme.md")

# A retired gate keeps its number as a tombstone row: the Gate cell is "*(retired
# YYYY-MM-DD: reason)*" and the Script cell is "n/a", the shape gate 35 accepts. A
# tombstone is a recorded gap, not a gate, so it is not counted.
TOMBSTONE_ROW_RE = re.compile(
    r"^\|\s*\d+\s*\|\s*\*\(retired \d{4}-\d{2}-\d{2}: [^|]+\)\*\s*\|\s*n/a\s*\|$")

# The rule and skill collections this audit once counted (a top-level
# guardrails/ tree) no longer ship, and gate 41 now checks the pinned AIQT
# families instead, so neither has a canonical source here. Their counts stay
# 0, the value the missing directories already gave (gates come from the §6
# inventory row count, parsed separately).
UNSHIPPED_COLLECTION_COUNT = 0


EXEMPT_FILES: frozenset[str] = frozenset(
    {
        ".working/CHANGELOG.md",
        ".claude/skills/corpus-management/data/taxonomy.yml",
        ".claude/skills/corpus-management/data/narrative.yml",
        "governance/portal.md",
        "governance/maturity-scorecard.md",
        ".claude/skills/corpus-management/tests/test_linters.py",
    }
)

# Note: the validation-sweep history file (now at
# `.working/validate-sweeps/history.md`, relocated within
# `.working/`) is a historical-record artefact by purpose; the file
# is in `.working/` which is in `DEFAULT_EXEMPT_DIRS`, so a per-file
# exemption here is not needed.

# Directory names that are out of scope for this audit, matched against single
# path components.
EXEMPT_DIRS: frozenset[str] = DEFAULT_EXEMPT_DIRS

# Repository-relative directories that are out of scope for this audit, matched
# as a path prefix: the pack's test fixtures may embed sample counts. This entry
# was once in EXEMPT_DIRS, where its slashes could never match a single path
# component, so it exempted nothing.
EXEMPT_REL_DIRS: tuple[str, ...] = (f"{CORPUS_MANAGEMENT_DIR}/tests/fixtures",)

# Moved trees this audit scanned before the move (``tools/``, ``tests/``, the
# project documents and the vendored AIQT pack), admitted ahead of the
# ``.claude`` component exemption; the rest of ``.claude/`` stays exempt.
ADMITTED_ROOTS: tuple[str, ...] = (
    *PROJECT_DOCUMENT_DIRS,
    *PROJECT_DOCUMENT_FILES,
    f"{CORPUS_MANAGEMENT_DIR}/tools",
    f"{CORPUS_MANAGEMENT_DIR}/tests",
    ".claude/aiqt",
)

# File suffixes the linter scans. Markdown is the primary surface;
# Python and shell scripts are included because their docstrings and
# top-of-file comments frequently cite the gate count.
SCAN_SUFFIXES: frozenset[str] = frozenset({".md", ".py", ".sh"})


def parse_canonical_count() -> int:
    """Parse §6 inventory of the audit-programme spec and return the
    live-gate row count (tombstone rows for retired numbers are not counted).

    The §6 inventory is a markdown table with one row per gate number.
    The header row is ``| # | Gate | Script |`` followed by a
    separator row of dashes. Data rows have numeric first cells.

    Raises ``RuntimeError`` if the inventory cannot be located or
    parsed.
    """
    text = read_text_safe(SPEC_PATH)
    if text is None:
        raise RuntimeError(f"cannot read {SPEC_PATH}")
    lines = text.splitlines()

    # Locate the §6 inventory header.
    inventory_start = None
    for lineno, line in enumerate(lines):
        if line.strip().startswith("## 6.") and "inventory" in line.lower():
            inventory_start = lineno
            break
    if inventory_start is None:
        raise RuntimeError("§6 inventory header not found in spec")

    # Find the table header row after the §6 header. The header row
    # starts with ``| #`` and contains the column ``Gate``.
    table_start = None
    for lineno in range(inventory_start, len(lines)):
        line = lines[lineno].strip()
        if line.startswith("| #") and "Gate" in line:
            table_start = lineno
            break
    if table_start is None:
        raise RuntimeError("§6 inventory table header not found")

    # Count data rows: after the header and the separator row, each
    # subsequent line beginning with ``|`` and a digit is a data row.
    # Stop at the first non-table line.
    count = 0
    for lineno in range(table_start + 2, len(lines)):
        line = lines[lineno].strip()
        if not line.startswith("|"):
            break
        # First cell is the gate number. Strip the leading ``|`` and
        # whitespace, then check the cell is numeric.
        first_cell = line.split("|", 2)[1].strip() if line.count("|") >= 2 else ""
        if first_cell.isdigit():
            if not TOMBSTONE_ROW_RE.match(line):
                count += 1
        else:
            break
    if count == 0:
        raise RuntimeError("§6 inventory has zero data rows")
    return count



def iter_targets(paths: list[str]) -> list[Path]:
    """Yield scannable files. ``paths`` is a list of repo-relative or
    absolute paths; if a path is a directory, it is walked recursively.
    If ``paths`` is empty, the entire repository root is walked. Exempt
    files and directories are skipped in either mode."""
    targets: list[Path] = []
    seen: set[Path] = set()

    def consider(path: Path) -> None:
        if is_default_exempt_root(path, repo_root=REPO_ROOT):
            return
        if not path.is_file():
            return
        if path.suffix not in SCAN_SUFFIXES:
            return
        try:
            rel = path.resolve().relative_to(REPO_ROOT).as_posix()
            parts = path.resolve().relative_to(REPO_ROOT).parts
        except ValueError:
            # Path is outside the repo (e.g. a temporary fixture).
            rel = path.as_posix()
            parts = path.parts
        if has_exempt_part(parts, EXEMPT_DIRS, admitted_roots=ADMITTED_ROOTS):
            return
        if rel in EXEMPT_FILES:
            return
        if any(rel == d or rel.startswith(d + "/") for d in EXEMPT_REL_DIRS):
            return
        if path.resolve() in seen:
            return
        targets.append(path.resolve())
        seen.add(path.resolve())

    roots = [Path(p) for p in paths] if paths else [REPO_ROOT]
    for root in roots:
        root = root.resolve() if root.exists() else root
        if root.is_file():
            consider(root)
        elif root.is_dir():
            for path in root.rglob("*"):
                consider(path)
    return sorted(targets)



def _engine():
    """Import the pack-owned engine, ensuring its .claude/skills/corpus-management/src/tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_gate_count_consistency  # the pack-owned engine (source of record)
    return gate_lint_gate_count_consistency


def scan_file(path: Path, counts: dict[str, int]):
    """Compatibility shim: a direct-module-load test loads this wrapper via importlib and calls
    ``scan_file(path, counts)`` on it. Delegate to the pack engine's ``scan_file`` (source of
    record for the check logic)."""
    return _engine().scan_file(path, counts)


def main(argv: list[str]) -> int:
    try:
        gate_count = parse_canonical_count()
    except RuntimeError as exc:
        print(f"ERROR: cannot determine canonical gate count: {exc}", file=sys.stderr)
        return 2

    engine = _engine()
    counts = {
        "gate": gate_count,
        "rule": UNSHIPPED_COLLECTION_COUNT,
        "skill": UNSHIPPED_COLLECTION_COUNT,
    }

    # Explicit paths are refused when missing or outside this tree (the counts are this
    # tree's inventory), else normalized.
    paths = guard_explicit_paths_cwd(argv[1:], repo_root=REPO_ROOT) if argv[1:] else []
    targets = iter_targets(paths)
    return engine.run(
        targets,
        counts=counts,
        repo_root=REPO_ROOT,
        spec_rel=SPEC_PATH.relative_to(REPO_ROOT),
    )


if __name__ == "__main__":
    sys.exit(main(sys.argv))
