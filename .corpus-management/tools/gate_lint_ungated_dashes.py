#!/usr/bin/env python3
"""Ungated-surface dash audit (grc gate 82): pack-owned engine (source of record).

No Unicode em-dash (U+2014) or en-dash (U+2013) may appear as a dash in prose on the
surfaces scanned. This is the SAME house-style ban the ``language-convention`` clause
already states (and that the language-and-style gate enforces on the corpus); this gate
extends that one clause to the OPERATIONAL surfaces the corpus language gate does not walk.
Because it reuses an existing clause, the transfer adds no new clause, rule, or generated
rule file: only this engine, its project wrapper, a gate-register row, and an id-history
event.

Detection (the PURE check): a glyph inside a markdown INLINE-CODE backtick span or inside a
fenced code block is exempt (the deliberate illustration / code-example form, exactly how the
language-convention rule DEFINES the ban, by quoting the forbidden glyphs in backticks). A
glyph used AS a dash in prose, outside code, is what re-drift looks like, and is what this
gate flags. For a non-markdown file (a ``.py`` comment or docstring) there are no backtick
spans, so a literal glyph is prose and stays flagged; the FUNCTIONAL dash literals in the
linters themselves are written as Unicode escapes, so they are not literal glyphs and never
match.

Engine/wrapper split (compile PR-8): this engine carries the PURE check (``DASH``,
``INLINE_CODE`` = the shared ``aiqt_corpus.CODE_SPAN_RE``, ``FENCE``, ``strip_code``,
``scan_text``, ``scan_file``), the ``pure_self_test_checks`` that exercise that check, and a
``run`` that iterates the given files and reports. The project wrapper
(``tools/lint-ungated-dashes.py``) supplies the grc operational scan SCOPE and the AIQT
bootstrap; ``run`` takes the target list and the repo root from the wrapper and holds no
scan-scope policy.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    from aiqt_corpus import CODE_SPAN_RE  # generic core (behaviour-identical to lint_common)
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise ImportError(
        "the aiqt_corpus module is unavailable: run through the project wrapper "
        "(python3 tools/lint-ungated-dashes.py), which bootstraps the vendored copy, "
        "or put the AIQT pack's tools/ on sys.path (AIQT_PACK_ROOT)."
    ) from exc

DASH = re.compile("[\u2014\u2013]")
# Inline-code span: a run of N backticks, shortest content, closing run of N backticks.
INLINE_CODE = CODE_SPAN_RE
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")


def strip_code(line: str) -> str:
    """Blank out inline-code backtick spans so a glyph INSIDE one is not flagged (the
    illustration / code-example form)."""
    return INLINE_CODE.sub(lambda m: "`" + " " * len(m.group(2)) + "`", line)


def scan_text(text: str, is_md: bool):
    """Yield (lineno, stripped_line) for each line carrying a dash outside code. PURE.

    For markdown, inline-code backtick spans and fenced code blocks are exempt (a glyph there
    is an illustration or a code example). For non-markdown (a `.py` comment or docstring),
    there are no backtick code spans, so a literal glyph is prose and stays flagged; the
    functional dash literals are Unicode-escaped and so are not literal glyphs."""
    in_fence = False
    for lineno, raw in enumerate(text.splitlines(), 1):
        if is_md and FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        probe = strip_code(raw) if is_md else raw
        if DASH.search(probe):
            yield lineno, raw.strip()


def scan_file(path: Path):
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    return list(scan_text(text, path.suffix.lower() == ".md"))


def pure_self_test_checks():
    """Return [(name, passed_bool), ...] for the PURE scan_text/strip_code logic.

    These test the engine's own behaviour (source of record), so they live with the engine;
    the project wrapper appends its scan-scope checks and reports the combined result."""
    checks = []

    def c(name, cond):
        checks.append((name, cond))

    c("md-prose-dash-flagged", list(scan_text("a \u2014 b\n", True)) == [(1, "a \u2014 b")])
    c("md-inline-code-exempt", list(scan_text("Em-dashes (`\u2014`) are forbidden.\n", True)) == [])
    c("md-en-dash-flagged", list(scan_text("range 1\u20132\n", True)) == [(1, "range 1\u20132")])
    c("md-fence-exempt", list(scan_text("```\nx \u2014 y\n```\n", True)) == [])
    c("md-clean", list(scan_text("no dashes here, just commas.\n", True)) == [])
    c("py-comment-dash-flagged", list(scan_text("# a \u2014 b\n", False)) == [(1, "# a \u2014 b")])
    c("py-escaped-literal-clean", list(scan_text('P = "[\\\\u2014\\\\u2013]"\n', False)) == [])
    c("py-inline-code-not-stripped", len(list(scan_text("x = `\u2014`\n", False))) == 1)
    return checks


def run(files: list[Path], *, repo_root: Path) -> int:
    findings = []
    for path in files:
        for lineno, line in scan_file(path):
            try:
                rel = path.relative_to(repo_root).as_posix()
            except ValueError:  # explicit path outside repo_root
                rel = path.as_posix()
            findings.append((rel, lineno, line))
    if findings:
        print(
            f"FAIL: {len(findings)} Unicode em/en dash(es) on the scanned surfaces. "
            f"Replace each with a comma, colon, or parentheses; a glyph that must appear "
            f"(an illustration, a code example) belongs inside a backtick code span, which "
            f"is exempt."
        )
        for rel, lineno, line in findings:
            print(f"  {rel}:{lineno}: {line[:110]}")
        return 1
    print(
        "OK: no Unicode em/en dashes on the scanned surfaces; backtick-quoted glyphs are exempt."
    )
    return 0
