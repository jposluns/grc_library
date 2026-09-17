#!/usr/bin/env python3
"""Executive-narrative vocabulary - pack engine.

Engine/wrapper split (Group-A content-generic lane, Pattern A): the PURE scan
(the shall/dash/quote/link regexes + matching logic; _has_citation, _strip_link_targets,
_noncode_lines, _shall_is_qualified, scan_page_text, check_file) is the source of record
here in the pack, moved verbatim from the grc gate. The absolutes denylist and the
external-standard citation vocabulary are supplied by the adopter via configure(ref), so
the engine carries no project vocabulary; the grc wrapper (tools/lint-narrative-vocabulary.py)
supplies them, configures the engine, and keeps the narrative scan scope (discover), the
self-test, main, module-global shims (scan_page_text / check_file), and the exit codes.
"""

from __future__ import annotations

import re
from pathlib import Path  # noqa: F401  # used in check_file's annotation (get_type_hints fidelity)

try:
    from aiqt_corpus import CODE_SPAN_RE, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_narrative_vocabulary: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# --- Adopter-supplied vocabulary: populated by configure(ref). ---
# Placeholders until an adopter calls configure(); the grc wrapper does so at import.
ABSOLUTES_SINGLE: tuple = ()
ABSOLUTES_MULTI: tuple = ()
CROSS_EXTERNAL_CONTEXT_RE = None


def configure(ref) -> None:
    """Populate the absolutes denylist (single + multi-word) and the external-standard
    citation vocabulary from the adopter. The scan functions resolve these as module
    globals; call once before scan_page_text()/check_file()."""
    global ABSOLUTES_SINGLE, ABSOLUTES_MULTI, CROSS_EXTERNAL_CONTEXT_RE
    ABSOLUTES_SINGLE = ref.absolutes_single
    ABSOLUTES_MULTI = ref.absolutes_multi
    CROSS_EXTERNAL_CONTEXT_RE = ref.cross_external_context_re


# Bare ``shall``: free-standing, not part of a hyphenated identifier and not
# a substring (``Marshall``). Same boundaries as gate 56.
BARE_SHALL = re.compile(r"(?<![A-Za-z0-9_-])shall(?![A-Za-z0-9_-])", re.IGNORECASE)

# Em / en dash (functional escapes, not literal glyphs, per the tools/ dash ban).
DASH_RE = re.compile("[\u2014\u2013]")

# Inline quotation spans: straight or curly double quotes.
QUOTE_SPAN_RES: tuple[re.Pattern[str], ...] = (
    re.compile(r'"[^"]+"'),
    re.compile("\u201c[^\u201d]+\u201d"),
)

# A visible source citation: a markdown link, or a named external standard
# (the shared external-standard vocabulary from lint_common, e.g. ISO, NIST,
# GDPR). Residue: an unlinked source name outside that vocabulary does not
# qualify; authors cite qualified quotes with a link or a named standard.
MD_LINK_RE = re.compile(r"\[[^\]]*\]\([^)]+\)")

# How close (characters, same line) a citation must sit to the quotation to
# count as "visibly adjacent (inline, immediately before or after)".
ADJACENCY_WINDOW = 120


def _has_citation(segment: str) -> bool:
    return bool(MD_LINK_RE.search(segment) or CROSS_EXTERNAL_CONTEXT_RE.search(segment))


def _strip_link_targets(line: str) -> str:
    """Blank markdown link DESTINATIONS/labels, keeping visible link TEXT, so the
    absolutes denylist scans only VISIBLE prose. A forbidden word inside a URL
    (``[source](.../guarantee)``) is not visible prose and must not be flagged,
    while the link TEXT is preserved and still scanned. Handles inline
    ``[text](dest)`` / ``[text](dest "title")`` / ``[text](<dest>)``, the reference
    USE ``[text][label]``, and a whole reference-DEFINITION line ``[label]: dest``
    (its destination is not visible prose)."""
    # A WELL-FORMED reference DEFINITION is entirely link metadata (label + a single
    # dest token + an optional quoted/paren title, and NOTHING else), none of it
    # visible prose, so blank the whole line. A line that merely RESEMBLES a ref-def
    # but carries trailing bare prose (``[note]: The guarantee applies.``) is NOT a
    # ref-def and is scanned as prose (only its inline links stripped below). This
    # covers a title-carried absolute (``[n]: url "guarantee"``) and a label-carried
    # one (``[guarantee]: url``), both metadata, without hiding real prose.
    if re.match(r'^\s*\[[^\]]+\]:\s*(?:<[^>]*>|\S+)\s*("[^"]*"|\'[^\']*\'|\([^)]*\))?\s*$', line):
        return ""
    line = re.sub(r"\]\([^)]*\)", "]", line)   # ](dest) / ](dest "title") / ](<dest>) -> ]
    line = re.sub(r"\]\[[^\]]*\]", "]", line)  # ][label] -> ]
    return line


def _noncode_lines(text: str) -> list[tuple[int, str | None]]:
    """Non-code (lineno, raw) lines, fence-MARKER-aware: a fenced block opened by
    ``` closes only on ```, and one opened by ~~~ only on ~~~, so a mismatched
    marker inside a block (``` inside a ~~~ fence) is content, not a toggle.

    Each elided fenced block is represented by a single sentinel ``(lineno, None)``
    at its opening line, so an adjacency walk STOPS at the fence boundary instead
    of treating the non-code lines flanking an elided block as adjacent (the
    across-the-fence false-qualification of a blockquoted ``shall``)."""
    out: list[tuple[int, str | None]] = []
    fence: str | None = None  # the 3-char marker (``` or ~~~) that opened the block
    for lineno, raw in enumerate(text.splitlines(), 1):
        stripped = raw.lstrip()
        marker = stripped[:3] if (stripped.startswith("```") or stripped.startswith("~~~")) else None
        if fence is None:
            if marker is not None:
                fence = marker
                out.append((lineno, None))  # fence-boundary sentinel
                continue
            out.append((lineno, raw))
        else:
            if marker == fence:
                fence = None
            # any line while inside a fence (matching-close included) is code: skip
    return out


def _shall_is_qualified(line: str, match: re.Match[str], idx: int,
                        noncode: list[tuple[int, str | None]]) -> bool:
    """The qualified-shall test (see module docstring). ``line`` is the
    code-span-stripped line; ``idx`` indexes ``noncode`` for blockquote
    adjacency."""
    if line.lstrip().startswith(">"):
        # Blockquote quotation: citation on the line or an adjacent non-blank line.
        if _has_citation(line):
            return True
        for step in (-1, 1):
            j = idx + step
            # Skip blank lines, but STOP at a fence boundary (None sentinel): an
            # elided fenced block between the shall and a citation means they are
            # NOT visibly adjacent, so the citation does not qualify the shall.
            while 0 <= j < len(noncode) and noncode[j][1] is not None and not noncode[j][1].strip():
                j += step
            if 0 <= j < len(noncode) and noncode[j][1] is not None and _has_citation(noncode[j][1]):
                return True
        return False
    for qre in QUOTE_SPAN_RES:
        for qm in qre.finditer(line):
            if qm.start() < match.start() and match.end() <= qm.end():
                before = line[max(0, qm.start() - ADJACENCY_WINDOW):qm.start()]
                after = line[qm.end():qm.end() + ADJACENCY_WINDOW]
                if _has_citation(before) or _has_citation(after):
                    return True
    return False


def scan_page_text(text: str) -> list[tuple[int, str, str]]:
    """(lineno, class, message) findings for one page. PURE.

    Classes: ``absolute``, ``shall``, ``dash``."""
    findings: list[tuple[int, str, str]] = []
    noncode = _noncode_lines(text)
    for idx, (lineno, raw) in enumerate(noncode):
        if raw is None:  # fence-boundary sentinel: a boundary, not a scannable line
            continue
        stripped = CODE_SPAN_RE.sub("", raw)  # backticked word-references never match
        prose = _strip_link_targets(stripped)  # absolutes scan VISIBLE prose only (F3)
        if DASH_RE.search(stripped):
            findings.append((lineno, "dash",
                             "em/en dash in narrative prose (the dash ban applies to the "
                             "narrative layer; rewrite with commas, colons, or parentheses)"))
        for name, pat in ABSOLUTES_SINGLE:
            if pat.search(prose):
                findings.append((lineno, "absolute",
                                 f"absolute {name!r} in narrative prose (page-wide denylist; a "
                                 f"narrative page states contribution, dependency, prevention, "
                                 f"or evidence, never an absolute)"))
        for m in BARE_SHALL.finditer(stripped):
            if _shall_is_qualified(stripped, m, idx, noncode):
                continue
            findings.append((lineno, "shall",
                             "unqualified 'shall' (narrative prose harmonizes on 'must'; a "
                             "'shall' is permitted only inside a verbatim quotation with a "
                             "visibly adjacent source citation)"))
    # Multi-word absolutes: scan each PARAGRAPH (consecutive non-code, non-blank
    # lines) joined with a space, so a phrase wrapped across a soft line break
    # cannot escape; report at the paragraph's first line. Paragraph-bounded (not
    # whole-page) so two unrelated sentences are not falsely joined into a match.
    para: list[tuple[int, str]] = []
    def _flush_para() -> None:
        if not para:
            return
        joined = " ".join(t for _, t in para)
        for name, pat in ABSOLUTES_MULTI:
            if pat.search(joined):
                findings.append((para[0][0], "absolute",
                                 f"absolute {name!r} in narrative prose (page-wide denylist; a "
                                 f"narrative page states contribution, dependency, prevention, "
                                 f"or evidence, never an absolute)"))
    for lineno, raw in noncode:
        if raw is None:  # F2: a fence boundary never joins two paragraphs across it
            _flush_para(); para = []
            continue
        stripped = CODE_SPAN_RE.sub("", raw)
        if stripped.strip():
            para.append((lineno, _strip_link_targets(stripped)))  # F3: multi-word absolutes ignore URLs
        else:
            _flush_para(); para = []
    _flush_para()
    return findings


def check_file(path: Path, rel: str) -> list[str]:
    text = read_text_safe(path)
    if text is None:
        # Fail LOUD, not open: an executive/ page that cannot be read cannot be
        # cleared of the vocabulary rules (the 1.3a fail-loud lesson).
        return [f"{rel}: not readable / not utf-8 (cannot be checked for the narrative vocabulary rules; fail loud)"]
    return [f"{rel}:L{lineno}: {msg}" for lineno, _cls, msg in scan_page_text(text)]
