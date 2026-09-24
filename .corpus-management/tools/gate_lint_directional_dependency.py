#!/usr/bin/env python3
"""Directional-dependency audit (grc gate): pack-owned engine (source of record).

Flag a deliverable-corpus document that links INTO a project-internal governance
directory: a link (inline ``](dest)``, titled, angle-bracketed, or a reference-style
definition) whose target resolves into the ``project_gov_dir`` subtree violates the
one-way dependency rule (a deliverable document must not depend on project-internal
governance). External targets (http/https/mailto/tel/ftp/#) are ignored. Fenced code
blocks are scanned too (fail closed, 3b54): no block structure can hide such a link, so an
example drops the link syntax and keeps a plain path mention (backticked or not).

Engine/wrapper split (compile PR-20): this engine carries the PURE check (the link and
ref-def patterns, ``links_into_project_gov``,
``check_file``, a ``_self_test``) and a ``run`` that groups + reports, taking the
project-governance directory name and the repository root in. The project wrapper
(``tools/lint-directional-dependency.py``) supplies the scan scope (the derived corpus
roots, the exempt prefixes) and the grc ``PROJECT_GOV_DIR`` name. This engine holds no
scan-scope or project-path policy.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path

LINK_RE = re.compile(r"\]\(\s*<?([^\s)>]+)")
EXTERNAL = re.compile(r"^(https?:|mailto:|tel:|ftp:|#)")
# A reference-style link definition line (optionally blockquoted): [label]: dest
REF_DEF_RE = re.compile(r"^ {0,3}(?:>[ \t]?)*\[[^\]]+\]:\s*<?([^\s>]+)")

def links_into_project_gov(source: Path, target: str, project_gov_dir: str) -> bool:
    """True if ``target`` (a link in ``source``) resolves into project governance."""
    target_no_anchor = target.split("#", 1)[0]
    if not target_no_anchor:
        return False
    resolved = (source.parent / target_no_anchor).resolve()
    return project_gov_dir in resolved.parts


def check_file(path: Path, *, project_gov_dir: str) -> list[tuple[int, str]]:
    findings: list[tuple[int, str]] = []
    # FAIL CLOSED (3b54, the gate-100 precedent): fenced code blocks are scanned too, so no block
    # structure can hide a link into project governance; an example drops the link syntax and
    # keeps a plain path mention. Measured cost on the live corpus: zero findings.
    with path.open("r", encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.rstrip("\n")
            for m in LINK_RE.finditer(line):
                target = m.group(1)
                if EXTERNAL.match(target):
                    continue
                if links_into_project_gov(path, target, project_gov_dir):
                    findings.append((lineno, target))
            rd = REF_DEF_RE.match(line)
            if rd:
                target = rd.group(1)
                if not EXTERNAL.match(target) and links_into_project_gov(path, target, project_gov_dir):
                    findings.append((lineno, target))
    return findings


def _self_test() -> int:
    import tempfile
    failures: list[str] = []
    pg = ".project-governance"

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

        def cf(fp):
            return check_file(fp, project_gov_dir=pg)

        expect("inline-link-flagged", cf(write("note.md", "# N\n\nSee [reg](.project-governance/register.md).\n")), True)
        expect("titled-link-flagged", cf(write("titled.md", "# T\n\nSee [reg](.project-governance/register.md \"Reg\").\n")), True)
        expect("angle-link-flagged", cf(write("angle.md", "# A\n\nSee [reg](<.project-governance/register.md>).\n")), True)
        expect("ref-def-flagged", cf(write("ref.md", "# R\n\nSee [reg][n].\n\n[n]: .project-governance/register.md\n")), True)
        expect("blockquote-ref-def-flagged", cf(write("bqref.md", "# R\n\n> See [reg][n].\n> [n]: .project-governance/register.md\n")), True)
        expect("indented-ref-def-pass", cf(write("indent.md", "# R\n\n    [n]: .project-governance/register.md\n")), False)
        expect("fenced-ref-def-flagged", cf(write("fencedref.md", "# R\n\n~~~\n```\n[n]: .project-governance/register.md\n~~~\n")), True)
        expect("non-project-gov-link-pass", cf(write("clean.md", "# C\n\nSee [spec](../governance/specification-master-project.md).\n")), False)
        expect("fenced-inline-link-flagged", cf(write("fenced.md", "# F\n\n```\n[reg](.project-governance/register.md)\n```\n")), True)

    if failures:
        for fl in failures:
            print(f"  SELF-TEST FAIL: {fl}")
        print(f"self-test: {len(failures)} case(s) failed.")
        return 1
    print("self-test: all directional-dependency cases passed (inline/titled/angle "
          "links and reference-style defs into .project-governance/ flagged; blockquoted "
          "ref-def flagged; fenced ref-defs and fenced inline links flagged (fail closed); "
          "an indented ref-def and a non-project-gov link not flagged).")
    return 0


def run(files: list[Path], *, project_gov_dir: str, repo_root: Path) -> int:
    from collections import defaultdict
    grouped: dict[str, list[tuple[int, str]]] = defaultdict(list)
    total = 0
    for f in files:
        for finding in check_file(f, project_gov_dir=project_gov_dir):
            try:
                display = f.relative_to(repo_root).as_posix()
            except ValueError:
                display = f.as_posix()
            grouped[display].append(finding)
            total += 1

    if not grouped:
        print(
            "OK: no corpus-to-project link "
            f"(no deliverable-corpus document links into {project_gov_dir}/)."
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
        f"deliverable-corpus document from linking into {project_gov_dir}/; "
        "sever the link to a plain-text mention, or move the citing document "
        "to a non-deliverable surface."
    )
    return 1
