#!/usr/bin/env python3
"""COBIT 2019 / ISO 31000 citation-existence audit (grc gate): pack-owned engine (source of record).

Detect fabricated COBIT 2019 governance/management-objective codes and invalid
ISO 31000 clause citations in corpus documents: a code matching the COBIT shape
that is not a real objective, an objective cited with a practice number beyond
its catalogue count, and an ISO 31000 clause number outside the standard's clause
set. ``scan_file`` returns a per-file list of ``Finding`` records; the wrapper's
``main`` aggregates them across the corpus.

Engine/wrapper split (SHARED/SAFETY lane PR-43, Pattern A + keyword-parameter
variant): this engine carries the citation regexes, the ISO-clause helper, the
``Finding`` dataclass, and the per-file ``scan_file``. The COBIT/ISO reference
data (``COBIT_OBJECTIVES``, ``COBIT_PRACTICE_COUNTS``, ``ISO31000_CLAUSES``) is grc
reference data shared with the COBIT title-text gate, so it stays wrapper-side in
``tools/cobit_iso31000_reference.py`` and is threaded in as the three keyword
parameters ``cobit_objectives`` / ``cobit_practice_counts`` / ``iso31000_clauses``.
The project wrapper (``tools/lint-cobit-iso31000-citations.py``) supplies the grc
scan scope, the exempt-file set, and those constants, and keeps a thin module-global
``scan_file`` shim delegating here so the scan-scope regression test (which patches
``mod.scan_file`` and runs ``main``) observes the original signature and behaviour.
The engine's ``scan_file`` is scope-free and repository-root-free.

Exit codes (the wrapper returns these): 0 clean; 1 one or more fabricated citations.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

try:
    from aiqt_corpus import is_fence_line
except ImportError as exc:  # pragma: no cover - import guard
    raise SystemExit(
        "gate_lint_cobit_iso31000_citations: cannot import the AIQT generic core "
        "(aiqt_corpus). The engine requires the pack tools/ directory on sys.path "
        "(the wrapper adds it via aiqt_bootstrap and _engine()).\n"
        f"  {exc}"
    )


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


def scan_file(
    path: Path,
    *,
    cobit_objectives: dict,
    cobit_practice_counts: dict,
    iso31000_clauses: dict,
) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    findings: list[Finding] = []
    in_fence = False
    for i, line in enumerate(text.splitlines(), start=1):
        if is_fence_line(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        # Check 1: COBIT code existence.
        for m in COBIT_CODE_RE.finditer(line):
            obj = m.group(1) + m.group(2)
            prac = m.group(3)
            if obj not in cobit_objectives:
                findings.append(Finding(
                    path, i, "cobit-objective-unknown",
                    f"'{m.group(0)}' cites '{obj}', not one of the 40 "
                    f"COBIT {'2019'} objectives",
                    line.strip()[:140]))
                continue
            if prac is not None:
                num = int(prac[1:])
                limit = cobit_practice_counts[obj]
                if not 1 <= num <= limit:
                    findings.append(Finding(
                        path, i, "cobit-practice-out-of-range",
                        f"'{m.group(0)}' exceeds {obj}'s practice range "
                        f"({obj}.01..{obj}.{limit:02d}; "
                        f"{obj} is '{cobit_objectives[obj]}')",
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
            if clause not in iso31000_clauses:
                findings.append(Finding(
                    path, i, "iso31000-clause-unknown",
                    f"clause '{clause}' is not in the ISO 31000:2018 "
                    f"clause tree (clauses 1-6; deepest level x.y.z)",
                    line.strip()[:140]))
    return findings


