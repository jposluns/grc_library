#!/usr/bin/env python3
"""COBIT objective-title canonicality - pack engine.

Recognize verb-led title-shaped phrases after an optional code wrapper
(**, __ or backtick), whitespace and one optional separator (colon, hyphen,
en dash, em dash, pipe, quote, opening parenthesis, comma, semicolon, slash
or opening bracket). The listed opening forms are:
Manage/Managed/Managing, Ensure/Ensured/Ensuring, Monitor/Monitored/Monitoring,
Evaluate/Evaluated/Evaluating, Assess/Assessed/Assessing,
Deliver/Delivered/Delivering, Align/Aligned/Aligning, Build/Built/Building,
and Direct/Directed/Directing.
Only Manage/Managed/Ensure/Ensured match case-insensitively; all added forms
must have the capitalization listed above. A candidate needs at least two
words before a field boundary. Closing wrappers (**, __, backtick, * or _)
and every accepted punctuation separator end the capture, except word-internal
hyphens, slashes, en/em dashes, parentheses, brackets, asterisks,
underscores, backticks and apostrophes. Compounds joined by any word-internal mark count by their parts for the two-word minimum, preserving their spelling.
For a single-quoted candidate, the last closing quote before the next non-quote
field boundary closes the title. A double-quoted candidate ends at the first
closing double quote; apostrophes inside double quotes remain part of the title. In an unquoted candidate, a plural
possessive (s' or S' followed by whitespace and a capitalized word) also
continues the title.
Residual: a wrong title opening with a word outside the listed forms, or
with no verb at all, is not detected (for example, MEA03, External Compliance).
Separators or wrappers outside the accepted set are also not detected:
for example **MEA03:** Title, italic or curly-quoted titles, a linked code,
or stacked separators. Added forms in other cases and single-word candidates
are intentionally outside this precision-first check.

Known false positives include sentence-case prose after a code
(for example, APO12: Assessing risk is required annually), a canonical title
used as a plural possessive before a capitalized word (for example,
APO10 Managed Vendors' SLAs), BAI03 Built-in controls apply, and
per APO12 - Managed risk-based approach. An unspaced em dash followed by a
word continues a title, so MEA03 with its canonical title followed by
an unspaced em dash and anchors this is flagged; prose em and en dashes are
both forbidden by the language gate. An unspaced en dash after a spaced en-dash
separator also continues the title, so the code APO12, a spaced en dash, then
its canonical title joined to further words by an unspaced en dash (for
example, ISO 31000 crosswalk) is a known false positive.

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
_SEP_RE = re.compile(r"\s*(?:\*\*|__|`)?\s*(?:[:\-\u2013\u2014|\"'(,;/\[])?\s*")

# Legacy stems ignore case; added opening forms require the listed capitalization.
_TITLE_STEM_RE = re.compile(
    r"(?:(?i:Managed|Manage|Ensured|Ensure)|Managing|Ensuring|Monitored|Monitor|Monitoring|"
    r"Evaluated|Evaluate|Evaluating|Assessed|Assess|Assessing|Delivered|Deliver|Delivering|"
    r"Aligned|Align|Aligning|Built|Build|Building|Directed|Direct|Directing)\b")

# Field boundary that ends a candidate title.
# Soft marks end fields unless flanked by word characters.
_INTERNAL_MARKS = r"\-/\u2013\u2014()[\]*_\x60"
_BOUNDARY_RE = re.compile(
    rf"\s{{2,}}|(?<![^\W_])[{_INTERNAL_MARKS}']|[{_INTERNAL_MARKS}](?![^\W_])"
    r"|'(?!\w)|[|\".,;:\t]|\s*$")

_TITLE_MAX_WORDS = 8


def _norm(s: str) -> str:
    """Collapse whitespace and strip, for case-insensitive comparison."""
    return re.sub(r"\s+", " ", s).strip()


def extract_title(rest: str, *, quote: str = "") -> str | None:
    """Given the line text immediately AFTER an objective code, return the
    candidate title if a canonical-title-shaped phrase follows, else None.

    ``rest`` starts right after the code token. A separator run is consumed
    first; then the next word must be a COBIT title verb form for a title to
    be considered present. The title is captured to the field boundary and
    capped at ``_TITLE_MAX_WORDS`` whitespace words; fewer than two parts is not a title.
    Legacy stems ignore case; added forms require the listed capitalization.
    Closing wrappers and punctuation end the capture except word-internal marks
    and unquoted plural possessives followed by a capitalized word.
    """
    sep = _SEP_RE.match(rest)
    body = rest[sep.end():] if sep else rest
    if not _TITLE_STEM_RE.match(body):
        return None
    boundary = None
    opening = rest[:sep.end()] if sep else ""
    quote = quote or next((c for c in opening if c in "'\""), "")
    marks = list(_BOUNDARY_RE.finditer(body))
    if quote:
        # For single quotes, the last closing quote before a field boundary wins.
        # Earlier apostrophes can belong to plural possessives in the title.
        closing = None
        for mark in marks:
            if quote == '"' and mark.group() == "'":
                continue  # An apostrophe inside double quotes is title text.
            if mark.group() == quote:
                closing = mark
                if quote == '"':
                    boundary = mark  # A double quote has no possessive reading.
                    break
            else:
                boundary = closing if closing is not None else mark
                break
    else:
        for mark in marks:
            # Keep unquoted plural possessives with a following title word.
            if (mark.group() == "'" and mark.start() > 0
                    and re.match(r"[sS]'\s+[A-Z]\w*", body[mark.start() - 1:])):
                continue
            boundary = mark
            break
    raw = body[:boundary.start()] if boundary and boundary.start() > 0 else body
    words = _norm(raw).split()
    # Compounds count by their parts for eligibility; preserve spelling
    # and the existing whitespace-word cap in the returned candidate.
    if len(re.findall(rf"[^\s{_INTERNAL_MARKS}]+", raw)) < 2:
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
            found = extract_title(
                line[m.end():],
                quote=(line[m.start() - 1] if m.start() > 0
                       and line[m.start() - 1] in "'\"" else ""))
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

