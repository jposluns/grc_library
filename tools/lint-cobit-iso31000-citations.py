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

import re
import sys
from dataclasses import dataclass
from pathlib import Path

from lint_common import (
    DEFAULT_EXEMPT_DIRS,
    REPO_ROOT,
    iter_markdown_targets,
)

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
})

# A COBIT code token: objective (APO12) with optional practice (.06),
# not preceded by a letter/digit/hyphen (so identifiers embedding the
# prefixes do not match) and not followed by a further digit.
COBIT_CODE_RE = re.compile(
    r"(?<![A-Za-z0-9-])(EDM|APO|BAI|DSS|MEA)(\d{2})(\.\d{2})?(?![0-9])")

# ISO 31000 clause attribution is deliberately narrow (precision-first):
# a clause token is checked only where its attribution to ISO 31000 is
# unambiguous. Four shapes are recognized: (S1/S2) the standard name
# immediately followed by the clause token ("ISO 31000:2018 §6.7",
# "ISO 31000, Clause 6"); (S3) a table cell naming only ISO 31000 whose
# next cell opens with clause tokens ("| ISO 31000:2018 | §6.7 ... |");
# (S4) a cell whose clause tokens are followed by "(ISO 31000" in the
# same cell. Clause tokens on multi-standard prose lines or in cells
# attributable to other standards are not checked (they belong to ISO
# 27001/37301 and friends); a matrix column whose header names ISO
# 31000 but whose cells never mention it is likewise out of scope, per
# the audit-programme spec's conservative-scope principle.
ADJACENT_CLAUSE_RE = re.compile(
    r"ISO\s*31000(?::2018)?\s*[,;]?\s*(?:§\s*|[Cc]lause\s+)"
    r"(\d(?:\.\d+){0,2})\b")
CLAUSE_TOKEN_RE = re.compile(r"(?:§\s*|[Cc]lause\s+)(\d(?:\.\d+){0,2})\b")
ISO31000_NAME_RE = re.compile(r"ISO(?:/IEC)?\s*31000(?::2018)?")
OTHER_ISO_RE = re.compile(r"ISO(?:/IEC)?\s*(?!31000)\d{4,5}")
CELL_TRAILING_PAREN_RE = re.compile(r"\(ISO\s*31000")
WRONG_DESIGNATION_RE = re.compile(r"ISO/IEC\s*31000")


def _iso31000_clauses_on_line(line: str) -> list[str]:
    """Clause tokens unambiguously attributable to ISO 31000."""
    clauses = [m.group(1) for m in ADJACENT_CLAUSE_RE.finditer(line)]  # S1/S2
    cells = line.split("|")
    for idx, cell in enumerate(cells):
        # S4: clause tokens in a cell that closes with "(ISO 31000...".
        if CELL_TRAILING_PAREN_RE.search(cell) and not OTHER_ISO_RE.search(cell):
            clauses.extend(
                m.group(1) for m in CLAUSE_TOKEN_RE.finditer(cell))
        # S3: a cell naming only ISO 31000, next cell opening with clauses.
        if (ISO31000_NAME_RE.search(cell)
                and not OTHER_ISO_RE.search(cell)
                and not CLAUSE_TOKEN_RE.search(cell)
                and idx + 1 < len(cells)):
            nxt = cells[idx + 1]
            if not OTHER_ISO_RE.search(nxt):
                clauses.extend(
                    m.group(1) for m in CLAUSE_TOKEN_RE.finditer(nxt))
    return clauses


@dataclass
class Finding:
    path: Path
    line: int
    rule: str
    message: str
    text: str


def scan_file(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    findings: list[Finding] = []
    in_fence = False
    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        # Check 1: COBIT code existence.
        for m in COBIT_CODE_RE.finditer(line):
            obj = m.group(1) + m.group(2)
            prac = m.group(3)
            if obj not in COBIT_OBJECTIVES:
                findings.append(Finding(
                    path, i, "cobit-objective-unknown",
                    f"'{m.group(0)}' cites '{obj}', not one of the 40 "
                    f"COBIT {'2019'} objectives",
                    line.strip()[:140]))
                continue
            if prac is not None:
                num = int(prac[1:])
                limit = COBIT_PRACTICE_COUNTS[obj]
                if not 1 <= num <= limit:
                    findings.append(Finding(
                        path, i, "cobit-practice-out-of-range",
                        f"'{m.group(0)}' exceeds {obj}'s practice range "
                        f"({obj}.01..{obj}.{limit:02d}; "
                        f"{obj} is '{COBIT_OBJECTIVES[obj]}')",
                        line.strip()[:140]))

        # Check 2: ISO 31000 designation.
        if WRONG_DESIGNATION_RE.search(line):
            findings.append(Finding(
                path, i, "iso31000-wrong-designation",
                "'ISO/IEC 31000' is not the standard's designation; "
                "ISO 31000 is an ISO (TC 262) standard",
                line.strip()[:140]))

        # Check 3: ISO 31000 clause existence (unambiguous shapes only).
        for clause in _iso31000_clauses_on_line(line):
            if clause not in ISO31000_CLAUSES:
                findings.append(Finding(
                    path, i, "iso31000-clause-unknown",
                    f"clause '{clause}' is not in the ISO 31000:2018 "
                    f"clause tree (clauses 1-6; deepest level x.y.z)",
                    line.strip()[:140]))
    return findings


def main(argv: list[str]) -> int:
    paths = argv[1:] or [str(REPO_ROOT)]
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
        print(f"=== {path.relative_to(REPO_ROOT).as_posix()} ===")
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
