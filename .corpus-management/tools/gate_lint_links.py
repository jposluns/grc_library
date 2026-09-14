#!/usr/bin/env python3
"""Broken-internal-link audit (grc gate 3): pack-owned engine (source of record).

Detect an internal markdown link whose target does not resolve to an existing file
inside the repository. External targets (http/https/mailto/tel/ftp, or a pure
``#`` fragment) are not checked; a trailing ``#anchor`` is stripped before
resolution; a link inside a fenced code block is illustrative content and is
skipped (the shared fence-aware scan toggles on each fence line).

Engine/wrapper split (compile PR-10): this engine carries the PURE check
(``LINK_RE``, ``EXTERNAL``, ``resolve_link``, ``check_file``) and a ``run`` that
groups + reports; the project wrapper (``tools/lint-links.py``) supplies the grc
scan scope (the default roots, the markdown selector) and the repository root, so
this engine holds no scan-scope or project-path policy and is repository-root-free
(``repo_root`` is a parameter, never a module global).

Exit codes (the wrapper returns these): 0 clean; 1 one or more broken links.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

try:
    from aiqt_corpus import is_fence_line
except ImportError as exc:  # fail loud: broken setup, never silently worked around
    raise ImportError(
        "the aiqt_corpus module is unavailable: run through the project wrapper "
        "(python3 tools/lint-links.py), which bootstraps the vendored copy, or put "
        "the AIQT pack's tools/ on sys.path (AIQT_PACK_ROOT)."
    ) from exc

# Match a markdown link target: ``](target)`` where target has no whitespace.
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
# Targets that are not internal file references (left unchecked).
EXTERNAL = re.compile(r"^(https?:|mailto:|tel:|ftp:|#)")


def resolve_link(source: Path, target: str) -> Path:
    """Resolve ``target`` relative to the directory containing ``source``."""
    # Strip fragment (#anchor) from the end of the target.
    target_no_anchor = target.split("#", 1)[0]
    if not target_no_anchor:
        return source  # pure-anchor link
    return (source.parent / target_no_anchor).resolve()


def check_file(path: Path, *, repo_root: Path) -> list[tuple[int, str, str]]:
    """Return ``(lineno, target, reason)`` for each broken internal link in ``path``."""
    findings: list[tuple[int, str, str]] = []
    in_code = False
    with path.open("r", encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.rstrip("\n")
            if is_fence_line(line):
                in_code = not in_code
                continue
            if in_code:
                continue
            for m in LINK_RE.finditer(line):
                target = m.group(1)
                if EXTERNAL.match(target):
                    continue
                resolved = resolve_link(path, target)
                # The resolved path must exist and be inside repo_root.
                try:
                    resolved.relative_to(repo_root)
                except ValueError:
                    findings.append((lineno, target, "resolves outside repo"))
                    continue
                if not resolved.exists():
                    findings.append((lineno, target, "target does not exist"))
    return findings


def run(files: list[Path], *, repo_root: Path) -> int:
    grouped: dict[str, list[tuple[int, str, str]]] = defaultdict(list)
    total = 0
    for f in files:
        for finding in check_file(f, repo_root=repo_root):
            try:
                rel = f.relative_to(repo_root).as_posix()
            except ValueError:  # explicit path outside repo_root
                rel = f.as_posix()
            grouped[rel].append(finding)
            total += 1

    if not grouped:
        print("OK: no broken links.")
        return 0

    for relpath in sorted(grouped):
        print(f"=== {relpath} ===")
        for lineno, target, reason in grouped[relpath]:
            print(f"  L{lineno} -> {target}  ({reason})")

    print(f"\nFAIL: {total} broken link(s) across {len(grouped)} file(s).")
    return 1
