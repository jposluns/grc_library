#!/usr/bin/env python3
"""Directional-dependency audit (grc gate): pack-owned engine (source of record).

Flag a deliverable-corpus document that links INTO a project-internal governance
directory: a link (inline ``](dest)``, titled, angle-bracketed, or a reference-style
definition) whose target resolves into the ``project_gov_dir`` subtree violates the
one-way dependency rule (a deliverable document must not depend on project-internal
governance). External targets (http/https/mailto/tel/ftp/#) are ignored. Fenced code
blocks are scanned too (fail closed): no block structure can hide such a link, so an
example drops the link syntax and keeps a plain path mention (backticked or not).

``project_gov_dir`` is a POSIX directory path of one or more parts (for example
``.claude/skills/corpus-management/registers``); a resolved target is inside it when that
run of parts occurs contiguously in the target's resolved path parts.

Engine/wrapper split: this engine carries the PURE check (the link and
ref-def patterns, ``path_in_project_gov``, ``links_into_project_gov``,
``check_file``, a ``_self_test``) and a ``run`` that groups + reports, taking the
project-governance directory path and the repository root in. The project wrapper
(``.claude/skills/corpus-management/tools/lint-directional-dependency.py``) supplies the scan scope (the derived corpus
roots, the exempt prefixes) and the grc ``PROJECT_GOV_DIR`` path. This engine holds no
scan-scope or project-path policy.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

LINK_RE = re.compile(r"\]\(\s*<?([^\s)>]+)")
EXTERNAL = re.compile(r"^(https?:|mailto:|tel:|ftp:|#)")
# A reference-style link definition line (optionally blockquoted): [label]: dest
REF_DEF_RE = re.compile(r"^ {0,3}(?:>[ \t]?)*\[[^\]]+\]:\s*<?([^\s>]+)")


def path_in_project_gov(resolved: Path, project_gov_dir: str) -> bool:
    """True if the parts of ``project_gov_dir`` occur as a contiguous run in ``resolved``'s parts."""
    gov = PurePosixPath(project_gov_dir).parts
    if not gov:
        raise ValueError("project_gov_dir must name at least one path part")
    parts = resolved.parts
    n = len(gov)
    return any(parts[i:i + n] == gov for i in range(len(parts) - n + 1))


def links_into_project_gov(source: Path, target: str, project_gov_dir: str) -> bool:
    """True if ``target`` (a link in ``source``) resolves into project governance."""
    target_no_anchor = target.split("#", 1)[0]
    if not target_no_anchor:
        return False
    resolved = (source.parent / target_no_anchor).resolve()
    return path_in_project_gov(resolved, project_gov_dir)


def check_file(path: Path, *, project_gov_dir: str) -> list[tuple[int, str]]:
    findings: list[tuple[int, str]] = []
    # FAIL CLOSED (the gate-100 precedent): fenced code blocks are scanned
    # too, so no block structure can hide a link into project governance;
    # an example drops the link syntax and keeps a plain path mention.
    # Measured cost on the earlier repository's corpus: zero findings.
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
    pg = ".claude/skills/corpus-management/registers"
    reg = pg + "/register.md"

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

        def cf(fp, gov: str = pg):
            return check_file(fp, project_gov_dir=gov)

        expect("inline-link-flagged", cf(write("note.md", f"# N\n\nSee [reg]({reg}).\n")), True)
        expect("titled-link-flagged", cf(write("titled.md", f"# T\n\nSee [reg]({reg} \"Reg\").\n")), True)
        expect("angle-link-flagged", cf(write("angle.md", f"# A\n\nSee [reg](<{reg}>).\n")), True)
        expect("ref-def-flagged", cf(write("ref.md", f"# R\n\nSee [reg][n].\n\n[n]: {reg}\n")), True)
        expect("blockquote-ref-def-flagged", cf(write("bqref.md", f"# R\n\n> See [reg][n].\n> [n]: {reg}\n")), True)
        expect("indented-ref-def-pass", cf(write("indent.md", f"# R\n\n    [n]: {reg}\n")), False)
        expect("fenced-ref-def-flagged", cf(write("fencedref.md", f"# R\n\n~~~\n```\n[n]: {reg}\n~~~\n")), True)
        expect("non-project-gov-link-pass", cf(write("clean.md", "# C\n\nSee [spec](../governance/specification-master-project.md).\n")), False)
        expect("fenced-inline-link-flagged", cf(write("fenced.md", f"# F\n\n```\n[reg]({reg})\n```\n")), True)
        expect("relative-climb-link-flagged", cf(write("governance/doc.md", f"# D\n\nSee [reg](../{reg}).\n")), True)
        expect("sibling-registers-dir-pass", cf(write("other.md", "# O\n\nSee [reg](registers/register.md).\n")), False)
        expect("skill-docs-link-pass", cf(write("docs.md", "# D\n\nSee [g](.claude/skills/corpus-management/docs/guide.md).\n")), False)
        expect("single-part-dir-flagged", cf(write("legacy.md", "# L\n\nSee [reg](registers/register.md).\n"), "registers"), True)

    if failures:
        for fl in failures:
            print(f"  SELF-TEST FAIL: {fl}")
        print(f"self-test: {len(failures)} case(s) failed.")
        return 1
    print("self-test: all directional-dependency cases passed (inline/titled/angle "
          "links, relative climbs and reference-style defs into the project-governance "
          "directory flagged; blockquoted ref-def flagged; fenced ref-defs and fenced "
          "inline links flagged (fail closed); an indented ref-def, a non-project-gov link, "
          "a partial path match and a sibling skill directory not flagged; a single-part "
          "directory name still flagged).")
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
