#!/usr/bin/env python3
"""Directory-scan-scope parity audit (gate 52).

Enforces that the audited-domain scan run has a single source of truth.
The explicit-allow-list content linters (the ones that enumerate scan
roots rather than walking the repository root and subtracting
``DEFAULT_EXEMPT_DIRS``) must derive their domain run from
``lint_common.AUDITED_DOMAIN_DIRS`` (by splatting it) rather than
hardcoding the directory list inline. This guarantees that adding a
future top-level audited directory propagates to every content linter
from one place, closing the recurring "added the directory to the
linters I happened to see" miss (the #336 to #338 Phase-1-migration
sweeps surfaced it twice: gates 31 and 10 silently skipped
``.project-governance`` because the migration enumerated the
explicit-allow-list set incompletely).

This gate is the mechanical backstop for
``governance/specification-project-governance-separation.md`` section 7.4,
which previously stated the completeness obligation only in prose.

Detection (robust to the three declaration styles the prior fragility
turned on, a module-level ``DEFAULT_SCAN_PATHS`` tuple, a module-level
``DOMAINS`` list, and a function-local list literal inside ``main()``):
the gate matches *literals*, not constant names. For each ``tools/*.py``
file it counts the number of DISTINCT audited domain directories that
appear as a standalone string-literal line (``^\\s*"<dir>",?\\s*$``). A
file with at least ``DECLARE_THRESHOLD`` such distinct literals is
"enumerating the domain run". Because a function-local list is still a
run of standalone string literals, this detector sees it even though a
``grep`` for the constant name would not.

A file that enumerates the run is a violation UNLESS it is one of:

  - ``lint_common.py`` itself, which is the canonical
    ``AUDITED_DOMAIN_DIRS`` definition (the single source of truth).
  - a file in ``EXEMPT`` (below), which legitimately enumerates a
    DIFFERENT domain set for a documented reason and carries a one-line
    rationale.

Any other enumerating file fails with the instruction to splat
``lint_common.AUDITED_DOMAIN_DIRS`` instead. Adding a new exempt file is
a deliberate, rationale-bearing edit to this gate, not a silent drift.

The gate also asserts the source of truth is intact:
``lint_common.AUDITED_DOMAIN_DIRS`` must contain exactly the expected
twelve members (the eleven domain directories plus ``.project-governance``).

Usage:
    python3 tools/lint-scan-scope-parity.py [tools-dir]

With no arguments, scans the ``tools/`` directory next to this script. A
path argument overrides the scan directory, which the regression
fixtures rely on to point the gate at a temporary directory. Exits
non-zero if any finding is reported.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from lint_common import AUDITED_DOMAIN_DIRS, read_text_safe

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = Path(__file__).resolve().parent

# A file with at least this many DISTINCT audited-domain-dir literals
# appearing as standalone string-literal lines is treated as enumerating
# the domain run. The real enumerations all carry eleven or twelve; a
# file that incidentally names one or two domain directories (a path
# fragment, a single example) is well below the threshold.
DECLARE_THRESHOLD = 6

# The single canonical location of the domain-dir run: the
# ``AUDITED_DOMAIN_DIRS`` definition itself. This gate's own file is also
# allowed, because its ``EXPECTED_AUDITED`` integrity-reference list (used
# to catch the source of truth drifting) is a deliberate second copy of
# the run that has nowhere else to live.
SOURCE_OF_TRUTH = "lint_common.py"
THIS_GATE = "lint-scan-scope-parity.py"

# Files that legitimately enumerate a DIFFERENT domain set than the
# audited run, each with a rationale. They are NOT content linters that
# implement a section-6.3 / full-corpus-audit-sweep obligation, OR they
# scan the corpus-document set (which excludes ``.project-governance`` by
# the project-governance separation), so they do not splat
# ``AUDITED_DOMAIN_DIRS``. Adding an entry here is a deliberate edit.
EXEMPT: dict[str, str] = {
    "lint-structure.py": (
        "Gate 38 (section-placement) checks the corpus document model and "
        "corpus-index membership; the .project-governance docs are outside "
        "that model (no 13-field metadata block, indexed by their own "
        "README), so adding the directory would demand corpus-index "
        "membership against the separation spec. Corpus-only domain set."
    ),
    "build-taxonomy.py": (
        "Taxonomy generator: .project-governance docs are project-governance, "
        "not adopter taxonomy/portal/scorecard content, so they are "
        "deliberately excluded from the generated artefacts. Corpus-only set."
    ),
    "detect-collection-candidates.py": (
        "Collection-candidate detection helper, not a content linter "
        "implementing a full-corpus-audit-sweep obligation; it suggests "
        "corpus collection candidates in a priority order, not a scan-scope "
        "obligation."
    ),
}

# Standalone string-literal line that is exactly one audited domain dir,
# e.g. ``    "governance",``. Matches a path-fragment string only when the
# whole literal is the bare directory name, so ``"governance" / "x.md"``
# (a path expression) does not match.
_DIR_ALTERNATION = "|".join(re.escape(d) for d in AUDITED_DOMAIN_DIRS)
DOMAIN_LITERAL_LINE = re.compile(rf'^\s*"({_DIR_ALTERNATION})",?\s*$')

EXPECTED_AUDITED = (
    "ai",
    "architecture",
    "compliance",
    "dev-security",
    "governance",
    ".project-governance",
    "operations",
    "privacy",
    "resilience",
    "risk",
    "security",
    "supply-chain",
)


def distinct_domain_literals(text: str) -> set[str]:
    """Return the set of audited domain dirs appearing as standalone literals."""
    found: set[str] = set()
    for line in text.splitlines():
        m = DOMAIN_LITERAL_LINE.match(line)
        if m:
            found.add(m.group(1))
    return found


def main(argv: list[str]) -> int:
    scan_dir = Path(argv[1]).resolve() if len(argv) > 1 else TOOLS_DIR

    findings: list[str] = []

    # Source-of-truth integrity: AUDITED_DOMAIN_DIRS must be exactly the
    # expected twelve members (order-independent membership check).
    if set(AUDITED_DOMAIN_DIRS) != set(EXPECTED_AUDITED):
        missing = set(EXPECTED_AUDITED) - set(AUDITED_DOMAIN_DIRS)
        extra = set(AUDITED_DOMAIN_DIRS) - set(EXPECTED_AUDITED)
        findings.append(
            "lint_common.AUDITED_DOMAIN_DIRS membership drift: "
            f"missing={sorted(missing)} extra={sorted(extra)}"
        )

    for py in sorted(scan_dir.glob("*.py")):
        text = read_text_safe(py)
        if text is None:
            continue
        distinct = distinct_domain_literals(text)
        if len(distinct) < DECLARE_THRESHOLD:
            continue
        name = py.name
        if name in (SOURCE_OF_TRUTH, THIS_GATE):
            continue  # the canonical definition / this gate's integrity reference
        if name in EXEMPT:
            continue  # documented divergent-set file
        try:
            display = py.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            display = py.name
        findings.append(
            f"{display}: enumerates the domain run "
            f"as standalone literals ({len(distinct)} distinct domain dirs), "
            "but is neither the lint_common.AUDITED_DOMAIN_DIRS source nor a "
            "documented EXEMPT divergent-set file. Splat "
            "lint_common.AUDITED_DOMAIN_DIRS instead of hardcoding the run "
            "(or, if this linter legitimately scans a different domain set, "
            "add it to EXEMPT in this gate with a rationale)."
        )

    if not findings:
        print(
            "OK: domain-dir scan run has a single source of truth "
            f"(lint_common.AUDITED_DOMAIN_DIRS); {len(EXEMPT)} documented "
            "divergent-set file(s) exempt."
        )
        return 0

    print("Directory-scan-scope parity audit FAILED:")
    for f in findings:
        print(f"  - {f}")
    print(f"\nFAIL: {len(findings)} finding(s).")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
