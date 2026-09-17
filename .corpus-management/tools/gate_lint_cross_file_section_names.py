#!/usr/bin/env python3
"""Cross-file section-NAME audit (grc gate): pack-owned engine (source of record).

The names phase layers title-fit checking on top of the numbers phase (gate 62,
cross-file-section-refs): a reference that pairs a section NUMBER with a heading
TITLE must cite the title's actual number in the resolved target. It fires on the
same two resolvable-target classes (adjacent-link and binding-declaration), plus
the table-row seam gate 62 excludes: an anchored-title reference to a number that
is not a numbered heading in the target, on a table row, is this gate's to fail.

Engine/wrapper split (Group-A content-generic lane, Pattern A): this engine
carries the PURE check (``normalize_title``, ``extract_titles``,
``resolve_target``, ``binding_target``, ``adjacent_link``, ``title_candidate``,
``check_file``) with the tool-specific title regexes (``TITLE_HEADING_RE`` /
``PAREN_TITLE_RE`` / ``QUOTE_TITLE_RE``); it is parameterized by ``repo_root`` and
the shared cross-file reference-extraction config (``ref_patterns`` /
``md_link_re`` / ``binding_sentinel`` / ``external_context_re`` /
``adjacency_window``), so the engine is repository-root-free and scan-scope-free.
The project wrapper (``tools/lint-cross-file-section-names.py``) supplies
``REPO_ROOT``, that CROSS_* config from ``lint_common`` (shared with the
numbers-phase sibling gate 62 so the two cannot drift), the grc scan scope
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
        "gate_lint_cross_file_section_names: cannot import the AIQT generic core "
        f"(aiqt_corpus); the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

# Gate 62's heading model with a title capture group: markdown headings only
# (inline clauses carry no title, so the names phase skips them). Tool-specific
# to this gate; travels with the engine.
TITLE_HEADING_RE = re.compile(
    r"^(#{2,6})\s+(?:Section\s+)?(\d+(?:\.\d+){0,3})[.\s:]\s*(.*)$"
)

# Title-candidate shapes immediately after a reference: a parenthetical or a
# (optionally comma-led) double-quoted run.
PAREN_TITLE_RE = re.compile(r"^\s*\(([^)]{2,120})\)")
QUOTE_TITLE_RE = re.compile(r'^\s*,?\s*["“]([^"”]{2,120})["”]')


def normalize_title(raw: str) -> str:
    collapsed = " ".join(raw.split())
    return collapsed.rstrip(".:").strip().lower()


def extract_titles(text: str) -> dict[str, str]:
    """Map heading number to normalized title (markdown headings only)."""
    titles: dict[str, str] = {}
    for _lineno, line in iter_non_code_lines(text):
        match = TITLE_HEADING_RE.match(line)
        if match:
            number = match.group(2).rstrip(".")
            title = normalize_title(match.group(3))
            if title:
                titles.setdefault(number, title)
    return titles


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
    """Return the .md link within the adjacency window of a reference."""
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


def title_candidate(line: str, ref_end: int) -> str | None:
    """Return the raw title candidate immediately after a reference."""
    tail = line[ref_end:]
    for pattern in (PAREN_TITLE_RE, QUOTE_TITLE_RE):
        match = pattern.match(tail)
        if match:
            return match.group(1)
    return None


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
    title_cache: dict[Path, dict[str, str]] = {}
    bound_target: Path | None = None

    def target_titles(target: Path) -> dict[str, str]:
        if target not in title_cache:
            target_text = read_text_safe(target)
            title_cache[target] = (
                extract_titles(target_text) if target_text is not None else {}
            )
        return title_cache[target]

    for lineno, line in iter_non_code_lines(text):
        candidate_binding = binding_target(line, path, repo_root, md_link_re, binding_sentinel)
        if candidate_binding is not None:
            bound_target = candidate_binding
            continue
        if external_context_re.search(line):
            continue
        for pattern in ref_patterns:
            for match in pattern.finditer(line):
                number = match.group(1).rstrip(".")
                raw_title = title_candidate(line, match.end())
                if raw_title is None:
                    continue
                link = adjacent_link(line, match.start(), match.end(), md_link_re, adjacency_window)
                if link is not None:
                    target = resolve_target(path, link, repo_root)
                elif bound_target is not None:
                    target = bound_target
                else:
                    continue
                if target is None or target == path:
                    continue
                titles = target_titles(target)
                if not titles:
                    continue
                claimed = normalize_title(raw_title)
                if not claimed:
                    continue
                # The anchoring rule: only a candidate that IS some heading
                # title in the target is a title claim.
                anchor_numbers = [n for n, t in titles.items() if t == claimed]
                if not anchor_numbers:
                    continue
                own_title = titles.get(number)
                if own_title is None:
                    if "|" in line:
                        # Table row: gate 62 excludes it, so the anchored-title
                        # + absent-number shape is this gate's to fail.
                        anchors = ", ".join(sorted(anchor_numbers))
                        findings.append(
                            f"{path.relative_to(repo_root)}:{lineno}: "
                            f"cross-file reference §{number} ({raw_title}) "
                            f"names the title of heading §{anchors} of "
                            f"{target.relative_to(repo_root)}, but §{number} "
                            f"is not a numbered heading there"
                        )
                    # Non-table: gate 62 owns existence; an inline clause has
                    # no title to verify.
                    continue
                if own_title != claimed:
                    anchors = ", ".join(sorted(anchor_numbers))
                    findings.append(
                        f"{path.relative_to(repo_root)}:{lineno}: cross-file "
                        f"reference §{number} ({raw_title}) names a title "
                        f"that is heading §{anchors}, not §{number}, of "
                        f"{target.relative_to(repo_root)}"
                    )
    return findings
