#!/usr/bin/env python3
"""Mandatory-near-uncertainty audit (grc gate): pack-owned engine (source of record).

Flag a mandatory-requirement word (``shall`` / ``must`` / ``is required`` and kin) that
appears within a small line window of an uncertainty marker (``TBD``, ``TODO``,
``FIXME``, ``[Unverified]``, ``placeholder`` and kin): a prescriptive requirement sitting
next to an unfinished-content marker is a drafting hazard. Both markers are read outside
fenced code blocks (a marker inside a fence is example syntax, not prose). The uncertainty
marker is also read outside inline code spans (a backticked marker is quoted, not used);
the mandatory word is read on the whole line. A span is recognized on one line only: a run
of backticks closed by the next run of exactly the same length, neither run touching a
further backtick. As in CommonMark, a backslash outside a span escapes the next character,
so a backslash-escaped backtick is literal text and opens no span, while inside a span a
backslash is literal and does not stop the closing run. A run with no such partner on its
line opens no span, and a span broken across lines is not recognized, so a marker after an
unmatched run, between escaped backticks or inside a broken span is still read (fail
closed). Each span is replaced by one NUL character (U+0000), which is neither whitespace
nor a word character: a word beside a span keeps its word boundary, and a marker pattern
can match across a span only by matching that character itself, which no pattern of the
live vocabulary does (each joins its words with whitespace), so the text on the two sides
of a span never forms a marker. A finding reports the marker as written in the source
line, mapped back from the stripped line.

Engine/wrapper split (vocab externalized): this engine carries
the PURE check ALGORITHM (the two-pass window scan, fence exclusion, the code-span strip of
the uncertainty pass, ``check_file``) and takes
the uncertainty + mandatory patterns + the window as an ``UncertaintyVocabulary`` (moved to the
``uncertainty`` reference-vocabulary profile, ``defaults/grc/uncertainty.toml``); a ``run`` groups
+ reports; the
project wrapper (``.claude/skills/corpus-management/tools/lint-shall-near-uncertainty.py``) supplies the grc scan scope and the
grc-specific exempt-file set (filtered out before delegating), so this engine holds no
scan-scope or project-file policy and is repository-root-free.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple

try:
    from aiqt_corpus import is_fence_line, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise ImportError(
        "the aiqt_corpus module is unavailable: run through the project wrapper "
        "(python3 .claude/skills/corpus-management/tools/lint-shall-near-uncertainty.py), which bootstraps the vendored copy, "
        "or put the AIQT pack's tools/ on sys.path (AIQT_PACK_ROOT)."
    ) from exc

# Inline code spans, for the uncertainty pass only, by one exact rule read left to right
# as CommonMark reads it: outside a span a backslash escapes the next character, so a
# backslash-escaped backtick is literal text that opens no span (and an escaped backslash
# escapes nothing further, so a backtick after it is live). A live run of one or more
# backticks opens a span closed by the next run of the SAME length (so ``TODO`` is a span
# as well as `TODO`, and `` a`b `` is one span); inside a span a backslash is literal, so
# it does not stop the closing run. Only exact runs pair: the shared CODE_SPAN_RE can
# backtrack into a longer run and take one backtick of an unmatched ``, which would hide a
# bare marker after it, and a pattern blind to escapes would read \`TODO\` as a span; here
# a run with no equal partner on its line opens no span and stays literal. A span is
# matched within one line (the engine reads line by line), so a span broken across lines
# is not recognized and its marker is read: fail closed. A marker inside a span is quoted,
# not used. Each span is replaced by one NUL character (_SPAN_STAND_IN), not removed and
# not a space: NUL is not a word character, so the text on either side keeps its word
# boundary and never glues into one word, and it is not whitespace, so no pattern that
# joins words with \s can match across it and the text on the two sides of a span never
# joins into a marker. The mandatory pass reads the whole line. The match is found on the
# stripped line but reported from the source line: each stripped character records the
# source range it stands for (a span's stand-in stands for the whole span), so the
# reported marker is the source text the match covers.
_SPAN_STAND_IN = "\x00"


def _closing_run(line: str, start: int, width: int) -> int:
    """Return the index of the next run of exactly ``width`` backticks at or after
    ``start`` (backslashes are literal inside a span), or -1 when the line has none."""
    i = start
    while i < len(line):
        if line[i] != "`":
            i += 1
            continue
        j = i
        while j < len(line) and line[j] == "`":
            j += 1
        if j - i == width:
            return i
        i = j
    return -1


def _strip_code_spans_mapped(line: str) -> tuple[str, list[tuple[int, int]]]:
    """Return ``line`` with each inline code span replaced by one NUL character, and for
    each character of the result the ``(start, end)`` range of ``line`` it stands for."""
    out: list[str] = []
    origin: list[tuple[int, int]] = []
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == "\\" and i + 1 < len(line):
            # escaped character: literal text, opens no span
            out.append(line[i:i + 2])
            origin.extend(((i, i + 1), (i + 1, i + 2)))
            i += 2
            continue
        if ch != "`":
            out.append(ch)
            origin.append((i, i + 1))
            i += 1
            continue
        j = i
        while j < len(line) and line[j] == "`":
            j += 1
        close = _closing_run(line, j, j - i)
        if close < 0:
            out.append(line[i:j])  # no partner of the same length: the run is literal
            origin.extend((k, k + 1) for k in range(i, j))
            i = j
        else:
            end = close + (j - i)
            out.append(_SPAN_STAND_IN)
            origin.append((i, end))  # the stand-in stands for the whole span
            i = end
    return "".join(out), origin


def strip_code_spans(line: str) -> str:
    """Return ``line`` with each inline code span replaced by one NUL character, which is
    neither whitespace nor a word character (uncertainty pass)."""
    return _strip_code_spans_mapped(line)[0]


class UncertaintyVocabulary(NamedTuple):
    """The adopter-overridable mandatory-near-uncertainty vocabulary.

    The check ALGORITHM (the two-pass window scan, fence exclusion) stays in this
    engine; only these DATA move to the ``uncertainty`` reference-vocabulary
    profile and are passed in. ``patterns`` order is policy (check_file reports the
    first matching uncertainty pattern per line).
    """
    patterns: tuple
    mandatory: "re.Pattern[str]"
    window_lines: int


def uncertainty_vocabulary(*, patterns, mandatory, window_lines) -> "UncertaintyVocabulary":
    """Compose the loaded profile (loader-compiled patterns) into the vocabulary;
    fail closed. ``patterns`` and ``mandatory`` are already compiled ``re.Pattern``
    objects (profile_loader compiles the {regex, ignorecase} tables)."""
    if not isinstance(patterns, list) or any(
        not isinstance(pat, re.Pattern) for pat in patterns
    ):
        raise ValueError(
            "uncertainty.patterns: expected an array of {regex, ignorecase} tables")
    if not isinstance(mandatory, re.Pattern):
        raise ValueError(
            "uncertainty.mandatory: expected a {regex, ignorecase} table")
    if (not isinstance(window_lines, int) or isinstance(window_lines, bool)
            or window_lines < 0):
        raise ValueError("uncertainty.window_lines: expected a nonnegative integer")
    return UncertaintyVocabulary(tuple(patterns), mandatory, window_lines)


def check_file(path: Path, *, vocab: UncertaintyVocabulary) -> list[tuple[int, str, str]]:
    """Return list of (lineno, uncertainty_match, line_snippet) findings. PURE (the wrapper filters exempt files)."""
    text = read_text_safe(path)
    if text is None:
        return []
    lines = text.splitlines()
    findings: list[tuple[int, str, str]] = []

    # Pre-compute the set of line indices that fall inside a fenced
    # code block. Both passes consult this set so a mandatory marker
    # inside a code block within window range of an uncertainty marker
    # outside the code block is correctly skipped (and vice versa).
    in_code_lines: set[int] = set()
    in_code_block = False
    for i, line in enumerate(lines):
        if is_fence_line(line):
            in_code_block = not in_code_block
            in_code_lines.add(i)  # the fence line itself is also non-content
            continue
        if in_code_block:
            in_code_lines.add(i)

    # First pass: locate uncertainty markers outside code blocks and outside
    # inline code spans (each span replaced by one NUL character before matching).
    uncertainty_lines: dict[int, str] = {}
    for i, line in enumerate(lines):
        if i in in_code_lines:
            continue
        prose, origin = _strip_code_spans_mapped(line)
        for pat in vocab.patterns:
            m = pat.search(prose)
            if m:
                # Report the marker as written in the source line (span text included).
                if m.end() > m.start():
                    uncertainty_lines[i] = line[origin[m.start()][0]:origin[m.end() - 1][1]]
                else:
                    uncertainty_lines[i] = m.group(0)
                break

    # Second pass: scan a window around each uncertainty marker for
    # mandatory words. Skip mandatory-marker lines that sit inside a
    # code block: they are example syntax, not prescriptive prose.
    for u_line, u_marker in uncertainty_lines.items():
        lo = max(0, u_line - vocab.window_lines)
        hi = min(len(lines), u_line + vocab.window_lines + 1)
        for i in range(lo, hi):
            if i in in_code_lines:
                continue
            if vocab.mandatory.search(lines[i]):
                findings.append((u_line + 1, u_marker, lines[u_line].strip()[:150]))
                break

    return findings


def run(files: list[Path], *, repo_root: Path, vocab: UncertaintyVocabulary) -> int:
    grouped: dict[str, list[tuple[int, str, str]]] = {}
    total = 0
    for f in files:
        rel = f.relative_to(repo_root).as_posix()
        findings = check_file(f, vocab=vocab)
        if findings:
            grouped[rel] = findings
            total += len(findings)

    if not grouped:
        print("OK: no mandatory-near-uncertainty findings.")
        return 0

    for rel, findings in sorted(grouped.items()):
        print(f"=== {rel} ===")
        for lineno, marker, snippet in findings:
            print(f"  L{lineno} [near {marker}] {snippet}")

    print(f"\nFAIL: {total} finding(s) across {len(grouped)} file(s).")
    print("Mandatory shall/must/will requirements should not appear next to uncertainty markers.")
    print("Either complete the requirement (remove the marker) or soften the language (may, recommended).")
    return 1
