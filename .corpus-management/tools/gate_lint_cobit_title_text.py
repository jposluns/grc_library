#!/usr/bin/env python3
"""COBIT objective-title canonicality - pack engine.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan
(the objective-code/title regexes, _norm, extract_title, scan_text, scan_file) is
the source of record here in the pack, moved verbatim from the grc gate. The COBIT
objective catalogue (code -> canonical title) is supplied by the adopter via
configure(objectives), so the engine carries no project catalogue; the grc wrapper
(tools/lint-cobit-title-text.py) imports the cobit_iso31000_reference catalogue,
configures the engine, and keeps EXEMPT_FILES, a module-global scan_file shim, main,
and the exit codes.
"""

from __future__ import annotations

import re
from pathlib import Path  # noqa: F401  # used in scan_file's annotation (get_type_hints fidelity)

try:
    from aiqt_corpus import is_fence_line
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_cobit_title_text: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# --- COBIT objective catalogue (code -> canonical title): populated by configure(). ---
# Placeholder until an adopter calls configure(); the grc wrapper does so at import.
COBIT_OBJECTIVES: dict = {}


def configure(objectives) -> None:
    """Populate the COBIT objective catalogue (code -> canonical title) from the
    adopter's reference. scan_text resolves it as a module global; call once before
    scan_text()/scan_file()."""
    global COBIT_OBJECTIVES
    COBIT_OBJECTIVES = objectives


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

