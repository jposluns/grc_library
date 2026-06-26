#!/usr/bin/env python3
"""Corpus-to-project directional-dependency audit (gate 53).

Enforces the one-way dependency rule of
``governance/specification-project-governance-separation.md`` section 4:
no corpus (deliverable) document may contain a markdown link whose
resolved target is inside the ``.project-governance/`` directory.
Project governance depends on the corpus, never the reverse; a
corpus-to-project link would invert that dependency. This gate is the
mechanical backstop for section 7.3, which previously recorded the gate
as queued and relied on the migration discipline (section 8.2) plus the
broken-link gate (gate 3) until it existed.

Per section 4, the NON-deliverable surfaces MAY link into
``.project-governance/`` and are therefore out of scope: the pack under
``dev-security/claude-rules/``, the repository backlog
[`TODO.md`](../TODO.md), the root [`CHANGELOG.md`](../CHANGELOG.md), the
generated indexes under ``docs/``, and ``.working/`` / ``.claude/``.
``.project-governance/`` itself is also out of scope (links *within* it
are allowed). Only the published deliverable corpus is policed; the
direction rule, not link-resolvability, is what the separation turns on
(the broken-link gate already guarantees these links resolve, because
``.project-governance/`` is audited, not exempt).

The deliverable-corpus scan set is DERIVED from the single source of
truth ``lint_common.AUDITED_DOMAIN_DIRS`` (minus ``.project-governance``,
which is the project-governance directory, not deliverable corpus) plus
the root deliverable documents, so adding a future audited domain
directory propagates here from one place. Deriving the run (rather than
hardcoding the eleven domain names as standalone literals) also keeps
this gate clear of the directory-scan-scope parity gate (gate 52), which
forbids content linters from hardcoding the audited-domain run.

The pack subtree ``dev-security/claude-rules/`` lives inside the
``dev-security`` domain directory but is a non-deliverable surface per
section 4, so it is excluded by path prefix.

Detection mirrors the broken-link checker (gate 3): fenced code blocks
are skipped (link-like text inside ``` ``` ``` is documentation, not a
real link), external-scheme targets are skipped, and a link target is
resolved relative to the directory containing the source file. A
resolved target is "into project governance" when ``.project-governance``
is one of its path components, which catches every relative shape
(``.project-governance/x.md``, ``../.project-governance/x.md``) and the
bare directory link itself.

Usage:
    python3 tools/lint-directional-dependency.py [paths...]

With no arguments, scans the deliverable corpus. A path argument
overrides the scan set, which the regression fixtures rely on to point
the gate at a temporary directory. Exits non-zero if any corpus-to-project
link is found.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

from lint_common import AUDITED_DOMAIN_DIRS

REPO_ROOT = Path(__file__).resolve().parent.parent

# The project-governance directory: the target the direction rule forbids
# corpus documents from linking into.
PROJECT_GOV_DIR = ".project-governance"

# Match markdown links ``[text](target)`` where target is not external.
# Same patterns as the broken-link checker (gate 3).
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
EXTERNAL = re.compile(r"^(https?:|mailto:|tel:|ftp:|#)")

# Non-deliverable subtrees that live inside a scanned domain directory and
# MAY link into .project-governance/ per separation-spec section 4. Path
# prefixes are relative to REPO_ROOT, POSIX form. The pack is the only
# such subtree nested under a domain dir; TODO.md / CHANGELOG.md / docs/
# / .working/ / .claude/ are simply absent from the scan roots below.
EXEMPT_PREFIXES: tuple[str, ...] = ("dev-security/claude-rules/",)

# Root-level deliverable documents (the published library specifications
# and front matter), matching the broken-link checker's root set minus
# the tooling/generated surfaces it additionally scans.
ROOT_DELIVERABLE_DOCS: tuple[str, ...] = (
    "README.md",
    "NOTICE.md",
    "specification-master-project.md",
    "specification-ingestion.md",
    "instruction-ai-document-ingestion.md",
)

# Deliverable-corpus scan roots: the audited domain directories minus the
# project-governance directory (derived from the single source of truth so
# a future audited domain propagates here, and so this gate does not
# itself hardcode the domain run), plus the root deliverable documents.
DEFAULT_CORPUS_ROOTS: list[str] = [
    *(d for d in AUDITED_DOMAIN_DIRS if d != PROJECT_GOV_DIR),
    *ROOT_DELIVERABLE_DOCS,
]


def _is_exempt(path: Path) -> bool:
    """True if ``path`` is under a non-deliverable exempt subtree."""
    try:
        rel = path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return False  # outside the repo (a temp-dir fixture): not exempt
    return any(rel.startswith(prefix) for prefix in EXEMPT_PREFIXES)


def iter_markdown_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        path = (REPO_ROOT / p) if not Path(p).is_absolute() else Path(p)
        if path.is_file() and path.suffix == ".md":
            files.append(path)
        elif path.is_dir():
            for f in path.rglob("*.md"):
                files.append(f)
    # Exclude the project-governance tree itself (links within it are
    # allowed) and the non-deliverable exempt subtrees (the pack).
    kept = [
        f
        for f in files
        if PROJECT_GOV_DIR not in f.resolve().parts and not _is_exempt(f)
    ]
    return sorted(set(kept))


def links_into_project_gov(source: Path, target: str) -> bool:
    """True if ``target`` (a link in ``source``) resolves into project governance."""
    target_no_anchor = target.split("#", 1)[0]
    if not target_no_anchor:
        return False  # pure-anchor link
    resolved = (source.parent / target_no_anchor).resolve()
    return PROJECT_GOV_DIR in resolved.parts


def check_file(path: Path) -> list[tuple[int, str]]:
    findings: list[tuple[int, str]] = []
    in_code = False
    with path.open("r", encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.rstrip("\n")
            if line.lstrip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            for m in LINK_RE.finditer(line):
                target = m.group(1)
                if EXTERNAL.match(target):
                    continue
                if links_into_project_gov(path, target):
                    findings.append((lineno, target))
    return findings


def main(argv: list[str]) -> int:
    paths = argv[1:] or DEFAULT_CORPUS_ROOTS

    files = iter_markdown_files(paths)
    grouped: dict[str, list[tuple[int, str]]] = defaultdict(list)
    total = 0
    for f in files:
        for finding in check_file(f):
            try:
                display = f.relative_to(REPO_ROOT).as_posix()
            except ValueError:
                display = f.as_posix()
            grouped[display].append(finding)
            total += 1

    if not grouped:
        print(
            "OK: no corpus-to-project link "
            f"(no deliverable-corpus document links into {PROJECT_GOV_DIR}/)."
        )
        return 0

    print("Corpus-to-project directional-dependency audit FAILED:")
    for relpath in sorted(grouped):
        print(f"=== {relpath} ===")
        for lineno, target in grouped[relpath]:
            print(f"  L{lineno} -> {target}  (corpus-to-project link)")
    print(
        f"\nFAIL: {total} corpus-to-project link(s) across {len(grouped)} file(s). "
        f"The one-way dependency rule (separation spec section 4) forbids a "
        f"deliverable-corpus document from linking into {PROJECT_GOV_DIR}/; "
        "sever the link to a plain-text mention, or move the citing document "
        "to a non-deliverable surface."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
