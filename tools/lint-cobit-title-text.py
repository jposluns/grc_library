#!/usr/bin/env python3
"""COBIT 2019 objective TITLE-TEXT validation audit (TODO section 1.16).

Gate 61 (``lint-cobit-iso31000-citations.py``) validates COBIT code
EXISTENCE (a code is one of the 40 objectives / inside its practice range)
and the ISO 31000 designation, but deliberately does NOT check citation
TITLES. This gate closes the OBJECTIVE-title half of that gap (the 40
objective titles extract cleanly from the held source, unlike the
line-wrapped practice titles, which stay unchecked): where the corpus
pairs an objective code with a title, the title must be the canonical
COBIT 2019 objective title.

The motivating defect class (validate-pr-987 note N1): the corpus writes
the IMPERATIVE verb form ``DSS05 Manage Security Services`` where the
canonical COBIT 2019 title is the PAST PARTICIPLE ``Managed Security
Services`` (and the EDM domain uses ``Ensured``). A truncated title
(``DSS02 Manage Service Requests`` for the canonical ``Managed Service
Requests and Incidents``) is the same finding.

Scope and precision (precision-first, per the audit-programme spec):

  * Corpus-wide over the same target set as gate 61: ``iter_markdown_targets``
    with ``DEFAULT_EXEMPT_DIRS`` (so ``.working``/``.claude`` are out and
    ``.project-governance`` is in) and the shared ``EXEMPT_FILES``.
  * A code is checked for a title ONLY when a canonical-title-SHAPED phrase
    immediately follows it: after the code and an optional separator
    (``:`` ``-`` ``|`` ``"`` ``'`` ``(`` ``,``), the next word is a COBIT
    title verb form (``Managed`` / ``Manage`` / ``Ensured`` / ``Ensure``,
    case-insensitive). A code with NO following title (cited alone, or next
    to a crosswalk cell such as a CCM control code) is ALLOWED, never
    flagged (matching the many no-title carriers).
  * The candidate title runs from that verb word to the field boundary
    (a ``|`` table-cell edge, a quote/paren close, a sentence period,
    comma, semicolon, colon, tab, two-or-more spaces, or end of line),
    capped at 8 words (the longest canonical title is 6). It is compared
    case-insensitively (after whitespace normalization) to the canonical
    title; any difference is a finding, with the code, the found title,
    and the canonical title reported.

Recall cost (precision-first, the same documented-recall-cost discipline gate
62 carries): a code is checked only when a COBIT title verb form opens the
phrase after it, so a title paraphrase that drops the verb entirely (a bare
noun phrase such as ``DSS05 (security services)``) is read as "no title" and
passes unchecked. This is a deliberate false-positive-free boundary; the
imperative-vs-participle defect class the gate targets is fully covered
because every one of the 40 canonical objective titles is participle-led. A
future widening to noun-phrase paraphrases would need a corpus census first
(the discipline gate 61 followed).

Exit codes: 0 all objective titles canonical (or no titled carriers);
1 findings; 2 environment error (reference module missing).

Stdlib-only (gate 71). Python 3.11.

Usage:
    python3 tools/lint-cobit-title-text.py [paths...]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from lint_common import (
    DEFAULT_EXEMPT_DIRS,
    REPO_ROOT,
    is_fence_line,
    iter_markdown_targets,
)

try:
    from cobit_iso31000_reference import COBIT_OBJECTIVES
except ImportError as exc:  # pragma: no cover - environment guard
    print(f"ERROR: cannot import the COBIT reference module: {exc}",
          file=sys.stderr)
    raise SystemExit(2)

# Files whose COBIT code tokens are illustrative or meta, not corpus
# citations. Same set gate 61 exempts (the audit-programme spec, the
# citation-verification spec, TODO, and CHANGELOG all discuss codes as
# examples), so the two COBIT gates share one scope.
EXEMPT_FILES = frozenset({
    "CHANGELOG.md",
    "specification-audit-programme.md",
    "specification-citation-verification.md",
    "TODO.md",
})

# A COBIT objective code token. Reused verbatim from gate 61 EXCEPT this
# gate cares only about OBJECTIVE codes (no practice suffix): an objective
# title attaches to APO12, never to APO12.06. A trailing ``.dd`` practice
# suffix is tolerated in the match and simply means "not an objective-title
# carrier" (a practice code is not followed by an objective title).
OBJECTIVE_CODE_RE = re.compile(
    r"(?<![A-Za-z0-9-])(EDM|APO|BAI|DSS|MEA)(\d{2})(?![0-9])")

# The separator that may sit between a code and its title.
_SEP_RE = re.compile(r"\s*[:\-|\"'(,]?\s*")

# A COBIT title verb form opening the candidate title (case-insensitive).
_TITLE_STEM_RE = re.compile(r"(?i)(?:Managed|Manage|Ensured|Ensure)\b")

# Field boundary that ends a candidate title.
_BOUNDARY_RE = re.compile(r"\s{2,}|[|\")]|[.,;:\t]|\s*$")

_TITLE_MAX_WORDS = 8


def _norm(s: str) -> str:
    """Collapse whitespace and strip, for case-insensitive comparison."""
    return re.sub(r"\s+", " ", s).strip()


def extract_title(rest: str) -> str | None:
    """Given the line text immediately AFTER an objective code, return the
    candidate title if a canonical-title-shaped phrase follows, else None.

    ``rest`` starts right after the code token. A separator run is consumed
    first; then the next word must be a COBIT title verb form for a title to
    be considered present. The title is captured to the field boundary and
    capped at ``_TITLE_MAX_WORDS`` words.
    """
    sep = _SEP_RE.match(rest)
    body = rest[sep.end():] if sep else rest
    if not _TITLE_STEM_RE.match(body):
        return None
    boundary = _BOUNDARY_RE.search(body)
    raw = body[:boundary.start()] if boundary and boundary.start() > 0 else body
    words = _norm(raw).split()
    if not words:
        return None
    return " ".join(words[:_TITLE_MAX_WORDS])


def scan_text(text: str) -> list[tuple[int, str, str, str]]:
    """Return (lineno, code, found_title, canonical_title) for each carrier
    whose paired objective title is not the canonical COBIT 2019 title."""
    findings: list[tuple[int, str, str, str]] = []
    in_code = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if is_fence_line(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        for m in OBJECTIVE_CODE_RE.finditer(line):
            # A practice code (APO12.06) is not an objective-title carrier.
            if line[m.end():m.end() + 1] == ".":
                continue
            code = f"{m.group(1)}{m.group(2)}"
            if code not in COBIT_OBJECTIVES:
                continue  # a non-objective token (existence is gate 61's job)
            found = extract_title(line[m.end():])
            if found is None:
                continue  # no title paired with this code: allowed
            canonical = COBIT_OBJECTIVES[code]
            if _norm(found).lower() != _norm(canonical).lower():
                findings.append((lineno, code, found, canonical))
    return findings


def scan_file(path: Path) -> list[tuple[Path, int, str, str, str]]:
    text = path.read_text(encoding="utf-8")
    return [(path, ln, code, found, canon)
            for ln, code, found, canon in scan_text(text)]


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
