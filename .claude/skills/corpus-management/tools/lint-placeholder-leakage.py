#!/usr/bin/env python3
"""Placeholder-leakage audit (grc gate 12): project entry point.

The gate ENGINE is pack-owned source of record at
``.claude/skills/corpus-management/src/tools/gate_lint_placeholder_leakage.py`` (Corpus-Management pack, gate register
``core/gates.toml``, id ``lint-placeholder-leakage``, enforcing the pack's ``placeholder-leakage``
clause); this thin wrapper keeps the house ``python3 .claude/skills/corpus-management/tools/lint-placeholder-leakage.py`` shape (gate
35 parses exactly that) and supplies the grc-local scan configuration the pack engine deliberately
does not carry: the AIQT bootstrap, the default scan root (whole repo), the markdown target selector
(``iter_targets``, kept here so the scan-scope regression's ALLOW map observes it unmoved), and the
grc exempt policy (``is_exempt`` with the exempt-file set, the exempt-dir set, and the ``template-`` /
``worklist-`` filename-prefix carve-outs). The wrapper filters exempt files out before delegating, so
the engine holds no project-file policy; it drives the engine's per-file ``scan`` and prints ONE
combined report in the engine's ``run`` shape, with the generated manifest's wrapper-local scan
(``manifest_findings``) counted and grouped alongside. These wrapper bytes are
HAND-MAINTAINED, not compiler-generated, so gate 99 does NOT own them.

Boundary with the shall-near-uncertainty audit (``lint-shall-near-uncertainty.py``): the two share
five marker tokens (TODO, TBD, FIXME, XXX, [Unverified]) plus a sixth in differing forms (this gate
matches the parenthesized ``(placeholder)``; that one matches bare ``placeholder``), and split by
PRESENCE vs CONJUNCTION. Each maintains its own token list; extend both deliberately.

Usage:
    python3 .claude/skills/corpus-management/tools/lint-placeholder-leakage.py
    python3 .claude/skills/corpus-management/tools/lint-placeholder-leakage.py path1 path2 ...
    python3 .claude/skills/corpus-management/tools/lint-placeholder-leakage.py --self-test

``--self-test`` checks the exempt-file matching (``in_exempt_files``) on a temporary tree and
checks that every path-form ``EXEMPT_FILES`` entry names a file in this repository, so an
entry that can never match fails (exit 1) instead of passing silently.

Exit codes are the wrapper's (0 clean, 1 findings, the engine's convention; 2 a refused explicit
path, missing or outside this tree (``guard_explicit_paths_cwd``'s SystemExit(2)), or an argparse
usage error): the wrapper drives the engine's per-file ``scan`` and returns its own combined verdict
in the engine's ``run`` shape; the report-text parity with the engine's ``run`` is pinned by two
regression pins in ``.claude/skills/corpus-management/tests/test_linters.py`` (the FAIL-report and OK-report parity tests), so the
copied report shape cannot drift silently.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import aiqt_bootstrap  # noqa: E402,F401  # single shim: AIQT pack .claude/aiqt/tools/ (aiqt_corpus via sys.modules, not sys.path)
from lint_common import guard_explicit_paths_cwd, is_default_exempt_root, is_adopter_exempt, read_text_safe, DEFAULT_EXEMPT_DIRS, in_exempt_dir, repo_relative_parts, REPO_ROOT  # noqa: E402  # grc-config/store, stays local

# Derive the pack .claude/skills/corpus-management/src/tools/ from this file's location, independent of REPO_ROOT.
PACK_TOOLS = Path(__file__).resolve().parent.parent / "src" / "tools"

DEFAULT_PATHS = [str(REPO_ROOT)]

# Files whose content legitimately mentions these markers. An entry holding a
# ``/`` is a repository-relative POSIX path and exempts that one file only; a
# bare entry is a file name and exempts every file of that name
# (``in_exempt_files``).
EXEMPT_FILES = {
    ".working/CHANGELOG.md",
    ".working/TODO.md",
    "TODO-REFERENCE.md",
    "governance/specification-master-project.md",
    "governance/specification-ingestion.md",
    "specification-citation-verification.md",
    # The Audit Programme Specification discusses the placeholder linter's
    # rule set and references .working/TODO.md by name; both produce false positives.
    "specification-audit-programme.md",
    # The coverage-gaps register uses "TODO backlog: <topic>" planned-target
    # references to .working/TODO.md items; this is by design, not leakage.
    "register-coverage-gaps.md",
    # The decision tree references .working/TODO.md and coverage gaps by name.
    "decision-tree.md",
}

# The generated web-to-corpus link manifest (.web/corpus-link-manifest.md, and that
# exact path only; a file of the same name elsewhere is scanned normally) enumerates
# every GitHub target the site links, .working/TODO.md among them (document pages link
# their sources' related documents). A row naming that file is a link target, not a
# placeholder marker, so the literal .working/TODO.md path token is skipped in a row's
# target and link-text cells ALONE; every other cell, and everything else in those
# cells, stays scanned (the former whole-file EXEMPT_FILES entry blinded the gate to
# template text leaking into the manifest).
MANIFEST_REL = ".web/corpus-link-manifest.md"

# A whitespace-delimited cell token that IS the .working/TODO.md path (bare or
# directory-qualified), and nothing else.
_TODO_PATH_TOKEN_RE = re.compile(r"(?:[\w.-]+/)*TODO\.md\Z")


def _mask_manifest_line(line: str) -> str:
    """The manifest line with the literal .working/TODO.md path token blanked in the
    target (first) and link-text (third) cells of a well-formed manifest row;
    any other line, cell, or token is returned for scanning untouched."""
    parts = line.split("|")
    # A manifest row is "| target | location | link text |": five split parts
    # with empty ends.
    if len(parts) != 5 or parts[0].strip() or parts[4].strip():
        return line
    for cell_index in (1, 3):
        parts[cell_index] = " ".join(
            "" if _TODO_PATH_TOKEN_RE.fullmatch(token) else token
            for token in parts[cell_index].split(" ")
        )
    return "|".join(parts)


def manifest_findings(path: Path, *, patterns) -> list[tuple[int, str, str]]:
    """Findings for the generated manifest: the engine's patterns over EVERY
    line of the file, fenced or not (the manifest is a generated table with
    no legitimate code fences, so the engine's fence-aware line iterator
    would let a fence marker, terminated or not, hide leaked content from
    the scan), each line masked by ``_mask_manifest_line`` first. Reported
    excerpts are the original line, like the engine's."""
    findings: list[tuple[int, str, str]] = []
    text = read_text_safe(path)
    if text is None:
        return findings
    for lineno, line in enumerate(text.splitlines(), 1):
        masked = _mask_manifest_line(line)
        for pattern, label in patterns:
            if pattern.search(masked):
                findings.append((lineno, label, line.strip()[:140]))
                break  # one finding per line is enough, like the engine
    return findings

# Directories whose content is exempt: the shared default set
# (``lint_common.DEFAULT_EXEMPT_DIRS``).
EXEMPT_DIR_PARTS = DEFAULT_EXEMPT_DIRS


def in_exempt_files(path: Path, *, repo_root: Path = REPO_ROOT) -> bool:
    """True when ``path`` is exempted by an ``EXEMPT_FILES`` entry.

    A bare entry is compared with the file name. An entry with a ``/`` is compared
    with the path relative to ``repo_root`` (path entries such as
    ``governance/specification-master-project.md`` were once compared with the file name
    alone and so never matched). A path outside ``repo_root`` matches bare entries only.
    """
    if path.name in EXEMPT_FILES:
        return True
    parts = repo_relative_parts(path, repo_root=repo_root)
    return bool(parts) and "/".join(parts) in EXEMPT_FILES


def is_exempt(path: Path) -> bool:
    """Return True if the file should be skipped."""
    if is_default_exempt_root(path, repo_root=REPO_ROOT):
        return True
    # Adopter overlay-exemption: honour the adopter's private-overlay dir here too, since
    # this gate builds its own exempt set rather than routing through is_target.
    if is_adopter_exempt(path, repo_root=REPO_ROOT):
        return True
    if in_exempt_files(path):
        return True
    if in_exempt_dir(path, EXEMPT_DIR_PARTS, repo_root=REPO_ROOT):
        return True
    # Template documents legitimately contain placeholders.
    if path.name.startswith("template-"):
        return True
    # Worklist documents contain intentional blank fields for human completion.
    if path.name.startswith("worklist-"):
        return True
    # Only scan markdown documents.
    if path.suffix != ".md":
        return True
    return False


def iter_targets(paths: list[str]) -> list[Path]:
    """Walk supplied paths and return markdown files to scan."""
    targets: list[Path] = []
    for raw in paths:
        p = Path(raw).resolve()
        if p.is_file():
            targets.append(p)
        elif p.is_dir():
            for f in p.rglob("*.md"):
                if not is_exempt(f):
                    targets.append(f)
    # Remove duplicates while preserving order
    seen = set()
    out = []
    for t in targets:
        if t in seen:
            continue
        seen.add(t)
        if not is_exempt(t):
            out.append(t)
    return out


def _engine():
    """Import the pack-owned engine, ensuring its .claude/skills/corpus-management/src/tools/ dir is importable."""
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import gate_lint_placeholder_leakage  # the pack-owned engine (source of record)
    return gate_lint_placeholder_leakage


def _placeholders_config():
    """Load the gate-12 placeholder patterns from the pack profile.

    Returns ordered (compiled-pattern, label) pairs composed from the
    ``placeholders`` reference-vocabulary profile (``defaults/grc/placeholders.toml``,
    loaded lazily via ``profile_loader.load('placeholders')``, patterns compiled by
    the loader). Fail-closed on a malformed profile.
    """
    pack_tools = str(PACK_TOOLS)
    if pack_tools not in sys.path:
        sys.path.insert(0, pack_tools)
    import profile_loader  # the pack-owned reference-vocabulary loader

    return _engine().placeholder_patterns(profile_loader.load("placeholders")["patterns"])


def _self_test() -> int:
    """Check exempt-file matching on a temporary tree, and that every path-form
    ``EXEMPT_FILES`` entry names a file in this repository (so it can match)."""
    import tempfile

    failures: list[str] = []
    path_entries = sorted(e for e in EXEMPT_FILES if "/" in e)
    bare_entries = sorted(e for e in EXEMPT_FILES if "/" not in e)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        for entry in path_entries:
            exact = root / entry
            elsewhere = root / "elsewhere" / Path(entry).name
            if not in_exempt_files(exact, repo_root=root):
                failures.append(f"path entry {entry}: does not match its own path")
            if in_exempt_files(elsewhere, repo_root=root):
                failures.append(f"path entry {entry}: also matches "
                                f"elsewhere/{Path(entry).name}")
        for entry in bare_entries:
            if not in_exempt_files(root / "any" / "dir" / entry, repo_root=root):
                failures.append(f"bare entry {entry}: does not match by file name")
        if in_exempt_files(root / "governance" / "policy-unlisted.md", repo_root=root):
            failures.append("an unlisted file matched an exemption")
    for entry in path_entries:
        target = REPO_ROOT / entry
        if not target.is_file():
            failures.append(f"path entry {entry}: no such file in this repository, "
                            "so the exemption can never match")
        elif not in_exempt_files(target):
            failures.append(f"path entry {entry}: the repository file is not exempted")
    if failures:
        for failure in failures:
            print(f"  SELF-TEST FAIL: {failure}")
        print(f"self-test: {len(failures)} case(s) failed.")
        return 1
    print(f"self-test: exempt-file matching passed ({len(path_entries)} path entries "
          f"matched their repository files only, {len(bare_entries)} bare entries "
          "matched by file name).")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Detect placeholder leakage in production library documents."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=None,
        help="Files or directories to scan (default: whole repo).",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Check the exempt-file matching and that each path entry names a file.",
    )
    args = parser.parse_args(argv[1:])
    if args.self_test:
        if args.paths:
            parser.error("--self-test takes no paths")
        return _self_test()
    # Explicit paths are refused when missing or outside this tree, else normalized.
    args.paths = guard_explicit_paths_cwd(args.paths, repo_root=REPO_ROOT) if args.paths else DEFAULT_PATHS
    targets = iter_targets(args.paths)
    # The generated manifest takes the narrow TODO.md-token carve-out here in
    # the wrapper (project-file policy); every other target goes to the
    # engine's per-file ``scan`` whole. Only the real manifest path qualifies.
    # The wrapper groups and reports BOTH scans itself in ONE summary,
    # mirroring the engine's ``run`` report shape (the former engine ``run``
    # call printed its own OK line before the wrapper's manifest FAIL block, a
    # pass-then-fail contradiction, and its OK file count omitted the
    # manifest).
    manifest_path = (REPO_ROOT / MANIFEST_REL).resolve()
    patterns = _placeholders_config()
    engine = _engine()
    grouped: dict[Path, list[tuple[int, str, str]]] = {}
    for target in targets:
        findings = (manifest_findings(target, patterns=patterns)
                    if target == manifest_path
                    else engine.scan(target, patterns=patterns))
        if findings:
            grouped[target] = findings
    if not grouped:
        print(f"OK: no placeholder leakage (scanned {len(targets)} files).")
        return 0
    total = 0
    for path, findings in sorted(grouped.items()):
        try:
            rel = path.relative_to(REPO_ROOT)
        except ValueError:
            rel = path
        print(f"=== {rel} ===")
        for lineno, label, excerpt in findings:
            print(f"  L{lineno} [{label}] {excerpt}")
        total += len(findings)
    print(
        f"\nFAIL: {total} placeholder finding(s) across {len(grouped)} file(s)."
    )
    print(
        "Placeholders such as TODO, TBD, FIXME, XXX, or "
        "<YYYY-MM-DD>-style markers should not appear in production library "
        "documents. Either complete the content or move the document to the "
        "template directory (filename prefix `template-`)."
    )
    if manifest_path in grouped:
        print(
            f"{MANIFEST_REL} is generated: the .working/TODO.md link-target token is "
            "the only exempt cell content; regenerate the manifest from "
            "clean sources instead of editing it."
        )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
