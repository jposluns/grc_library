#!/usr/bin/env python3
"""Cross-file section-reference audit (grc gate): pack-owned engine (source of record).

Validate that a corpus document citing a section of ANOTHER corpus document by
number cites a section that actually exists in the resolved target. Library
documents cite by number, e.g. "see [the mobile standard](standard-mobile.md)
Section 5.4" or, via a binding declaration, a file-wide "Section numbers below
refer to that standard." sentinel after which bare references bind to the
declared target. When the target is renumbered, such references silently go
stale; the intra-document gate deliberately filters cross-document context out,
so this class is otherwise gate-blind.

The engine fires ONLY on two high-confidence resolvable-target classes:

1. Adjacent-link class: a reference with a markdown ``.md`` link within the
   adjacency window in the same prose line or table cell. The link names the
   target; the cited number must be a numbered heading or a line-initial
   inline clause in that target.
2. Binding-declaration class: a line carrying the binding sentinel together with
   a ``.md`` link binds every SUBSEQUENT bare reference in the file to that
   target (the last link ending before the sentinel).

Every line is split into cells on unescaped pipes outside matched code spans,
and every cell is checked; an unmatched backtick is literal and backslashes
inside code are literal. A local heading
reference in a table cell is excluded when no link precedes it in the cell and
the text between it and a nearby following link, which begins with a space, is
an exception path. A parenthesis is bare when it is outside any code span and
not escaped with a backslash; an escaped or code-span parenthesis is ignored.
The text is an exception path only when it holds at least one character that is
neither a space nor a bare parenthesis, holds no bare closing parenthesis
without a bare opening parenthesis before it in that text, and ends, ignoring
spaces, with a bare opening parenthesis. The path is closed when the text after
the link closes every bare opening parenthesis the text before the link leaves
unmatched. A cell of that shape whose path is not closed is refused as
malformed, whether or not the target holds the cited number, instead of being
checked as a citation of the target. "Of the target" describes the
target, so it is checked. Prose remains subject to the adjacent-link check.
Only explicit "of [the] target" wording is treated as a target citation in
this table-cell exception; "of the policy" remains a documented residual.
The exception applies only to a line whose first non-whitespace character is
a pipe, as the corpus writes table rows; a valid row written without a leading
pipe, any cell of which holds a local section, then descriptive text, then a
parenthesized link to the target, is treated as prose for this exception, so
its local section is checked against the adjacent link (a documented residual).
Headings and cited references are cut to four levels; inline
clauses are recognized only at two to four levels, so a deeper clause line is
not a target section and a five-level citation to it is checked against its
four-level prefix (a documented residual).

Documented exclusions (recall costs, not gaps): external-standard context lines;
targets with zero numbered headings and
zero inline clauses; bare references with no adjacent link and no active binding;
name-based references and range second endpoints.

Engine/wrapper split: this engine carries the PURE check (``extract_sections``,
``resolve_target``, ``binding_target``, ``adjacent_link``, ``check_file``) with
the tool-specific heading model (``HEADING_RE`` / ``CLAUSE_RE``); it is
parameterized by ``repo_root`` and the shared cross-file reference-extraction
config (``ref_patterns`` / ``md_link_re`` / ``binding_sentinel`` /
``external_context_re`` / ``adjacency_window``), so the engine is
repository-root-free and scan-scope-free. The project wrapper
(``.claude/skills/corpus-management/tools/lint-cross-file-section-refs.py``)
supplies ``REPO_ROOT``, the shared CROSS_* config from ``lint_common``, the grc
scan scope (``iter_markdown_targets`` / ``EXEMPT_FILES``) and the reporting in
``main``, and keeps a module-global ``check_file`` shim delegating here so the
scan-scope regression test (which patches ``mod.check_file`` and runs ``main``)
observes the original signature and behaviour.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    from aiqt_corpus import iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_cross_file_section_refs: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# Same heading shape as the intra-document gate, cut to four levels (the
# intra-document gate compares full depth): a numbered heading, and the
# canonical section model's line-initial inline clauses ("4.7.1 All audit ...")
# that citers reference (at least two levels, keeping single-level ordered-list
# items out of the set). Tool-specific to this gate; travels with the engine.
HEADING_RE = re.compile(r"^(#{2,6})\s+(?:Section\s+)?(\d+(?:\.\d+){0,3})[.\s:]")
CLAUSE_RE = re.compile(r"^(\d+(?:\.\d+){1,3})\s")


def extract_sections(text: str) -> set[str]:
    """Return the numeric heading and inline-clause identifiers of a document."""
    sections: set[str] = set()
    for _lineno, line in iter_non_code_lines(text):
        match = HEADING_RE.match(line)
        if match:
            sections.add(match.group(2).rstrip("."))
            continue
        clause = CLAUSE_RE.match(line)
        if clause:
            sections.add(clause.group(1))
    return sections


def resolve_target(source: Path, target_rel: str, repo_root: Path) -> Path | None:
    """Resolve a markdown link target relative to the citing file, inside the repo."""
    try:
        candidate = (source.parent / target_rel).resolve()
    except (OSError, ValueError):
        return None
    if not candidate.is_file():
        return None
    try:
        candidate.relative_to(repo_root)
    except ValueError:
        return None
    return candidate


def binding_target(line: str, source: Path, repo_root: Path, md_link_re, binding_sentinel: str) -> Path | None:
    """Return the binding target for a sentinel line (last link before it)."""
    sentinel_at = line.find(binding_sentinel)
    if sentinel_at < 0:
        return None
    best: str | None = None
    for match in md_link_re.finditer(line):
        if match.end() <= sentinel_at:
            best = match.group(1)
    if best is None:
        return None
    return resolve_target(source, best, repo_root)


def adjacent_link(line: str, ref_start: int, ref_end: int, md_link_re, adjacency_window: int) -> str | None:
    """Return the .md link within the adjacency window of a reference.

    The nearest link (either side) within ``adjacency_window`` characters wins.
    The caller supplies one table cell or one prose line at a time.
    """
    best: tuple[int, str] | None = None
    for match in md_link_re.finditer(line):
        if match.end() <= ref_start:
            gap = ref_start - match.end()
        elif match.start() >= ref_end:
            gap = match.start() - ref_end
        else:
            continue
        if gap > adjacency_window:
            continue
        if best is None or gap < best[0]:
            best = (gap, match.group(1))
    return best[1] if best else None


def reference_cells(line: str) -> list[str]:
    """Split on table delimiters, preserving escaped pipes and code-span pipes.

    A backtick run opens code only when an equal-length closing run exists.
    Outside code, backslashes escape a pipe only when the immediately preceding
    backslash run has odd length. Inside code, backslashes are literal.
    """
    cells: list[str] = []
    start = 0
    backslashes = 0
    code_run = 0
    i = 0
    while i < len(line):
        char = line[i]
        if char == "\\" and code_run == 0:
            backslashes += 1
            i += 1
            continue
        escaped = backslashes % 2 == 1
        backslashes = 0
        if char == "`" and (code_run or not escaped):
            end = i + 1
            while end < len(line) and line[end] == "`":
                end += 1
            run = end - i
            if code_run == 0:
                closing = re.search(r"(?<!`)`{%d}(?!`)" % run, line[end:])
                if closing:
                    code_run = run
            elif code_run == run:
                code_run = 0
            i = end
            continue
        if char == "|" and not escaped and code_run == 0:
            cells.append(line[start:i])
            start = i + 1
        i += 1
    cells.append(line[start:])
    return cells


def _bare_characters(cell: str):
    """Yield ``(index, char)`` for each character of ``cell`` that is structure.

    The scan begins at the start of the cell. A character is skipped when it is
    inside a code span, is a backslash, follows an odd run of backslashes, or is
    a backtick: a backtick run not escaped is never yielded, whether or not an
    equal-length closing run makes it open a code span.
    Code spans follow the rule ``reference_cells`` uses: a backtick run not
    escaped opens code only when an equal-length closing run exists, and inside
    code backslashes are literal.
    """
    backslashes = 0
    i = 0
    while i < len(cell):
        char = cell[i]
        if char == "\\":
            backslashes += 1
            i += 1
            continue
        escaped = backslashes % 2 == 1
        backslashes = 0
        if char == "`" and not escaped:
            end = i + 1
            while end < len(cell) and cell[end] == "`":
                end += 1
            closing = re.search(r"(?<!`)`{%d}(?!`)" % (end - i), cell[end:])
            i = end + closing.end() if closing else end
            continue
        if not escaped:
            yield i, char
        i += 1


def _exception_path_depth(cell: str, start: int, end: int) -> int:
    """Count the bare opening parentheses ``cell[start:end]`` leaves unmatched.

    Return 0 when that text is not an exception path. A parenthesis is bare
    when ``_bare_characters`` yields it, scanning the cell from its start, so a
    parenthesis inside a code span or escaped with a backslash is ignored. The
    text is an exception path only when it holds at least one character that
    is neither a space nor a bare parenthesis, holds no bare closing
    parenthesis without a bare opening parenthesis before it in the text, and
    ends, ignoring spaces, with a bare opening parenthesis.
    """
    bare = {i: char for i, char in _bare_characters(cell) if start <= i < end}
    if not any(
        not cell[i].isspace() and bare.get(i) not in ("(", ")")
        for i in range(start, end)
    ):
        return 0
    depth = 0
    for char in bare.values():
        if char == "(":
            depth += 1
        elif char == ")":
            if depth == 0:
                return 0
            depth -= 1
    last = start + len(cell[start:end].rstrip()) - 1
    if bare.get(last) != "(":
        return 0
    return depth


def _closes_open_parenthesis(cell: str, start: int, depth: int = 1) -> bool:
    """Whether ``cell[start:]`` closes ``depth`` parentheses already open before ``start``.

    Parentheses are counted with nesting, so a nested parenthetical does not
    close an open one. Only a parenthesis at or after ``start`` is counted. A
    parenthesis is ignored only inside a code span, or after an odd run of
    backslashes, that the scanned text itself opens. The scan begins at the
    start of the cell, so a code span opened before ``start`` is part of the
    scanned text: a parenthesis it encloses after ``start`` is ignored, and a
    span or escape opened outside the cell is not seen. Code spans follow the
    rule ``reference_cells`` uses: a backtick run not escaped opens code only
    when an equal-length closing run exists, and inside code backslashes are
    literal.
    """
    for i, char in _bare_characters(cell):
        if i < start:
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return True
    return False


def check_file(
    path: Path,
    repo_root: Path,
    ref_patterns,
    md_link_re,
    binding_sentinel: str,
    external_context_re,
    adjacency_window: int,
) -> list[str]:
    """Return finding strings for one markdown file."""
    text = read_text_safe(path)
    if text is None:
        return []
    findings: list[str] = []
    section_cache: dict[Path, set[str]] = {}
    bound_target: Path | None = None
    own_sections = extract_sections(text)

    def target_sections(target: Path) -> set[str]:
        if target not in section_cache:
            target_text = read_text_safe(target)
            section_cache[target] = (
                extract_sections(target_text) if target_text is not None else set()
            )
        return section_cache[target]

    for lineno, line in iter_non_code_lines(text):
        candidate_binding = binding_target(line, path, repo_root, md_link_re, binding_sentinel)
        if candidate_binding is not None:
            bound_target = candidate_binding
            continue
        if external_context_re.search(line):
            continue
        for cell in reference_cells(line):
            for pattern in ref_patterns:
                for match in pattern.finditer(cell):
                    number = match.group(1).rstrip(".")
                    link = adjacent_link(cell, match.start(), match.end(), md_link_re, adjacency_window)
                    # A parenthesized link can elaborate a local heading only
                    # after descriptive text and with a closing parenthesis.
                    following = next(
                        (m for m in md_link_re.finditer(cell)
                         if m.start() >= match.end()
                         and m.start() - match.end() <= adjacency_window),
                        None,
                    )
                    intervening = cell[match.end():following.start()] if following else ""
                    # Bare opening parentheses the text before the link leaves
                    # unmatched; 0 when that text is not an exception path.
                    open_count = (
                        _exception_path_depth(cell, match.end(), following.start())
                        if following else 0
                    )
                    if (line.lstrip().startswith("|") and link is not None
                            and number in own_sections and following is not None
                            and not any(m.end() <= match.start() for m in md_link_re.finditer(cell))
                            # The text before the link begins with a space and
                            # is an exception path: descriptive, with no stray
                            # bare closing parenthesis, and ending with a bare
                            # opening parenthesis. Otherwise the cell is
                            # checked as a citation of the target.
                            and re.match(r"\s", intervening)
                            and open_count > 0
                            and not re.match(r"\s+of\s+(?:the\s+)?target\b", intervening, re.I)):
                        # Scan with balanced parentheses: the text after the
                        # link must close every parenthesis the text before it
                        # left open, a nested parenthetical does not close an
                        # open one, and a parenthesis in a code span or
                        # escaped is not counted. The scan starts at the
                        # cell's start, so a code span opened before the link
                        # is known.
                        if _closes_open_parenthesis(cell, following.end(), open_count):
                            continue
                        # Without its closing parenthesis the row would fall
                        # through to the target check and pass whenever the
                        # target holds the same number, so refuse it here.
                        findings.append(
                            f"{path.relative_to(repo_root)}:{lineno}: local section "
                            f"§{number} is followed by descriptive text and a "
                            f"parenthesized link with no closing parenthesis in "
                            f"its table cell"
                        )
                        continue
                    if link is not None:
                        target = resolve_target(path, link, repo_root)
                    elif bound_target is not None:
                        target = bound_target
                    else:
                        continue
                    if target is None or target == path:
                        continue
                    sections = target_sections(target)
                    if not sections:
                        continue
                    if number not in sections:
                        findings.append(
                            f"{path.relative_to(repo_root)}:{lineno}: cross-file reference "
                            f"§{number} does not resolve to a numbered heading or "
                            f"inline clause in {target.relative_to(repo_root)}"
                        )
    return findings
