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

1. Adjacent-link class (non-table lines only): a reference with a markdown
   ``.md`` link within the adjacency window on the same line and no intervening
   table pipe. The link names the target; the cited number must be a numbered
   heading or a line-initial inline clause in that target.
2. Binding-declaration class: a line carrying the binding sentinel together with
   a ``.md`` link binds every SUBSEQUENT bare reference in the file to that
   target (the last link ending before the sentinel).

Documented exclusions (recall costs, not gaps): table rows (any line with a
pipe); external-standard context lines; targets with zero numbered headings and
zero inline clauses; bare references with no adjacent link and no active binding;
name-based references and range second endpoints.

Engine/wrapper split (Group-A content-generic lane, Pattern A): this engine
carries the PURE check (``extract_sections``, ``resolve_target``,
``binding_target``, ``adjacent_link``, ``check_file``) with the tool-specific
heading model (``HEADING_RE`` / ``CLAUSE_RE``); it is parameterized by
``repo_root`` and the shared cross-file reference-extraction config
(``ref_patterns`` / ``md_link_re`` / ``binding_sentinel`` /
``external_context_re`` / ``adjacency_window``), so the engine is
repository-root-free and scan-scope-free. The project wrapper
(``tools/lint-cross-file-section-refs.py``) supplies ``REPO_ROOT``, the shared
CROSS_* config from ``lint_common``, the grc scan scope
(``iter_markdown_targets`` / ``EXEMPT_FILES``) and the reporting in ``main``, and
keeps a module-global ``check_file`` shim delegating here so the scan-scope
regression test (which patches ``mod.check_file`` and runs ``main``) observes the
original signature and behaviour.

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

# Same heading model as the intra-document gate: a numbered heading, and the
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

    The nearest link (either side) within ``adjacency_window`` characters wins; a
    table pipe between the reference and the link breaks adjacency.
    """
    best: tuple[int, str] | None = None
    for match in md_link_re.finditer(line):
        if match.end() <= ref_start:
            gap = ref_start - match.end()
            between = line[match.end() : ref_start]
        elif match.start() >= ref_end:
            gap = match.start() - ref_end
            between = line[ref_end : match.start()]
        else:
            continue
        if gap > adjacency_window or "|" in between:
            continue
        if best is None or gap < best[0]:
            best = (gap, match.group(1))
    return best[1] if best else None


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
        if "|" in line:
            continue
        if external_context_re.search(line):
            continue
        for pattern in ref_patterns:
            for match in pattern.finditer(line):
                number = match.group(1).rstrip(".")
                link = adjacent_link(line, match.start(), match.end(), md_link_re, adjacency_window)
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
