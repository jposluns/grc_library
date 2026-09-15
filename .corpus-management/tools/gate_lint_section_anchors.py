#!/usr/bin/env python3
"""Section-anchor audit (grc gate): pack-owned engine (source of record).

Validate that every cross-document (or same-document) markdown link of the form
``[text](path#anchor)`` resolves its ``#anchor`` to a real heading in the target
file. Headings are extracted outside fenced code blocks and slugified per the
GitHub flavour rules (lowercase; drop characters that are not alphanumeric,
space, hyphen, or underscore; spaces to hyphens; collapse consecutive hyphens);
an anchor matching no heading slug in its resolved target is a finding. External
scheme URLs (``http://``, ``https://``, ``mailto:``) and links whose target file
does not exist (handled by the separate link-existence gate) are skipped.

Engine/wrapper split (SHARED/SAFETY lane PR-35, Pattern A): this engine carries
the pure check (``LINK_RE``, ``HEADING_RE``, ``slugify``, ``extract_anchors``,
``scan``); the project wrapper (``tools/lint-section-anchors.py``) supplies the grc
scan scope (``iter_markdown_targets``) and the grouped reporting in ``main``, and
keeps a thin module-global ``scan`` shim delegating here so the scan-scope
regression test (which patches ``mod.scan`` and runs ``main``) observes the
original signature and behaviour. ``scan`` takes ``repo_root`` as a keyword so the
engine is repository-root-free; the wrapper supplies the grc root.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    from aiqt_corpus import iter_non_code_lines, read_text_safe
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise SystemExit(
        "gate_lint_section_anchors: cannot import the AIQT generic core (aiqt_corpus); "
        f"the pack tools/ dir must be on sys.path. Underlying error: {exc}"
    )

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)#]*)#([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def slugify(heading: str) -> str:
    """Slugify a markdown heading per GitHub's rules (best-effort)."""
    # Remove trailing markdown formatting and code backticks
    s = heading.strip().lower()
    # Drop characters that aren't alphanumeric, space, hyphen, or underscore
    s = re.sub(r"[^a-z0-9\s\-_]+", "", s)
    # Spaces → hyphens
    s = re.sub(r"\s+", "-", s)
    # Collapse consecutive hyphens
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def extract_anchors(text: str) -> set[str]:
    """Return set of anchor slugs derivable from headings in `text`."""
    anchors: set[str] = set()
    for _lineno, line in iter_non_code_lines(text):
        m = HEADING_RE.match(line)
        if m:
            heading = m.group(2)
            # Strip markdown formatting from heading text
            heading_clean = re.sub(r"[`*_]+", "", heading)
            anchors.add(slugify(heading_clean))
    return anchors


def scan(path: Path, *, repo_root: Path) -> list[tuple[int, str, str, str]]:
    """Return list of (line, target_rel, anchor, reason) findings."""
    findings: list[tuple[int, str, str, str]] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    base_dir = path.parent
    for lineno, line in iter_non_code_lines(text):
        for m in LINK_RE.finditer(line):
            link_text, target_rel, anchor = m.group(1), m.group(2).strip(), m.group(3).strip()
            # Strip inline-code backticks from link text
            anchor = anchor.split(" ")[0]  # ignore link-title text
            if not target_rel:
                # Same-document anchor: target is the current file
                target_path = path
            else:
                # Skip external links (http/https/etc.)
                if target_rel.startswith(("http://", "https://", "mailto:")):
                    continue
                target_path = (base_dir / target_rel).resolve()
            if not target_path.exists():
                continue  # lint-links handles this
            try:
                target_text = target_path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            anchors_available = extract_anchors(target_text)
            if anchor not in anchors_available:
                try:
                    target_rel_disp = target_path.relative_to(repo_root).as_posix()
                except ValueError:
                    target_rel_disp = str(target_path)
                findings.append(
                    (lineno, target_rel_disp, anchor, f"no heading slugifies to #{anchor}")
                )
    return findings
