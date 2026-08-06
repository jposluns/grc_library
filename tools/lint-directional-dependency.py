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
``guardrails/``, the repository backlog
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

The pack subtree ``guardrails/`` is a root-level non-deliverable
surface per section 4. It is absent from the derived scan roots, so the
default run never reaches it; the ``EXEMPT_PREFIXES`` entry below is
retained as defence-in-depth for an explicit-path invocation.

Link detection is the hardened form ported from gate 87 (#1426), NOT gate 3's: the LINK_RE handles titled and angle-bracket links, a REF_DEF_RE catches reference-style link definitions, and a marker-aware fence parser tracks the fence type. Fenced code blocks
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

from lint_common import AUDITED_DOMAIN_DIRS, REPO_ROOT


# The project-governance directory: the target the direction rule forbids
# corpus documents from linking into.
PROJECT_GOV_DIR = ".project-governance"

# Match markdown links; titled ``](dest "title")`` and angle ``](<dest>)`` forms
# cannot fail open (the #1426 gate-87 hardening, ported: the prior
# ``\]\(([^)\s]+)\)`` required a closing ")" and rejected a space).
LINK_RE = re.compile(r"\]\(\s*<?([^\s)>]+)")
EXTERNAL = re.compile(r"^(https?:|mailto:|tel:|ftp:|#)")

# Reference-style link DEFINITION ``[label]: dest`` at line start: 0-3 leading
# spaces (4+ is an indented code block), an optional blockquote prefix, then the
# label. A corpus doc that references .project-governance/ via a ref-def renders a
# link but is not an inline ``](dest)`` match, so LINK_RE alone fails open. Ported
# from gate 87 (#1426); the marker-aware fence tracking (below) excludes fenced defs.
REF_DEF_RE = re.compile(r"^ {0,3}(?:>[ \t]?)*\[[^\]]+\]:\s*<?([^\s>]+)")

# Marker-aware fence parser (CommonMark): a block closes only on the same marker
# char and a run length >= the opener, no info string; the shared ``is_fence_line``
# toggle is marker-blind, so a ``` inside a ~~~ example would wrongly flip the scan.
# Local to gate 53, ported from gate 87 (#1426).
_FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")


def _fence_marker(line: str):
    m = _FENCE_RE.match(line)
    if not m:
        return None
    run = m.group(1)
    return run[0], len(run), m.group(2).strip()


def _closes(marker, opener) -> bool:
    return (marker is not None and marker[0] == opener[0]
            and marker[1] >= opener[1] and not marker[2])

# Non-deliverable subtrees that are absent from the derived scan roots, kept
# as an explicit exemption (defence-in-depth) for an explicit-path invocation;
# they MAY link into .project-governance/ per separation-spec section 4. Path
# prefixes are relative to REPO_ROOT, POSIX form. The pack (``guardrails/``) is
# the root-level non-deliverable subtree; TODO.md / CHANGELOG.md / docs/
# / .working/ / .claude/ are likewise absent from the scan roots below.
EXEMPT_PREFIXES: tuple[str, ...] = ("guardrails/",)

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
    open_fence = None  # marker-aware: (char, run-length); ``` inside ~~~ is content
    with path.open("r", encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.rstrip("\n")
            marker = _fence_marker(line)
            if open_fence is not None:
                if _closes(marker, open_fence):
                    open_fence = None
                continue
            if marker is not None:
                open_fence = (marker[0], marker[1])
                continue
            for m in LINK_RE.finditer(line):
                target = m.group(1)
                if EXTERNAL.match(target):
                    continue
                if links_into_project_gov(path, target):
                    findings.append((lineno, target))
            rd = REF_DEF_RE.match(line)
            if rd:
                target = rd.group(1)
                if not EXTERNAL.match(target) and links_into_project_gov(path, target):
                    findings.append((lineno, target))
    return findings


def _self_test() -> int:
    import tempfile
    failures: list[str] = []

    def expect(name: str, findings, should_flag: bool) -> None:
        flagged = bool(findings)
        if should_flag and not flagged:
            failures.append(f"{name}: expected a corpus-to-project finding, got none")
        elif not should_flag and flagged:
            failures.append(f"{name}: expected PASS, got {findings}")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)

        def write(rel: str, content: str) -> Path:
            fp = root / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content, encoding="utf-8")
            return fp

        expect("inline-link-flagged", check_file(write("note.md", "# N\n\nSee [reg](.project-governance/register.md).\n")), True)
        expect("titled-link-flagged", check_file(write("titled.md", "# T\n\nSee [reg](.project-governance/register.md \"Reg\").\n")), True)
        expect("angle-link-flagged", check_file(write("angle.md", "# A\n\nSee [reg](<.project-governance/register.md>).\n")), True)
        expect("ref-def-flagged", check_file(write("ref.md", "# R\n\nSee [reg][n].\n\n[n]: .project-governance/register.md\n")), True)
        expect("blockquote-ref-def-flagged", check_file(write("bqref.md", "# R\n\n> See [reg][n].\n> [n]: .project-governance/register.md\n")), True)
        expect("indented-ref-def-pass", check_file(write("indent.md", "# R\n\n    [n]: .project-governance/register.md\n")), False)
        expect("fenced-ref-def-pass", check_file(write("fencedref.md", "# R\n\n~~~\n```\n[n]: .project-governance/register.md\n~~~\n")), False)
        expect("non-project-gov-link-pass", check_file(write("clean.md", "# C\n\nSee [spec](../governance/specification-master-project.md).\n")), False)
        expect("fenced-inline-link-pass", check_file(write("fenced.md", "# F\n\n```\n[reg](.project-governance/register.md)\n```\n")), False)

    if failures:
        for fl in failures:
            print(f"  SELF-TEST FAIL: {fl}")
        print(f"self-test: {len(failures)} case(s) failed.")
        return 1
    print("self-test: all directional-dependency cases passed (inline/titled/angle "
          "links and reference-style defs into .project-governance/ flagged; blockquoted "
          "ref-def flagged; indented and fenced ref-defs and fenced inline link, plus a "
          "non-project-gov link, not flagged).")
    return 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv[1:]:
        return _self_test()
    paths = [a for a in argv[1:] if not a.startswith("-")] or DEFAULT_CORPUS_ROOTS

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
