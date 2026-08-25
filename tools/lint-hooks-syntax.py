#!/usr/bin/env python3
"""Hooks Python-syntax audit (gate 95).

Every hook in `.claude/hooks/*.py` is executable machinery: the Claude Code harness
invokes each file with the running Python interpreter at hook-fire time. A hook with a
Python syntax error fails at exactly the moment it is supposed to protect, and the
hooks here FAIL OPEN by design (a guard that wedges the session on its own malfunction
gets disabled), so a syntax-broken hook does not announce itself: it silently stops
protecting.

Before this gate, no gate covered that. Gate 71 (stdlib-only imports) AST-parses
`tools/`, `tests/`, and `.web/` and fails on an unparseable file there, but does not
scan `.claude/hooks/`; gate 94 (static unused-import) scans `.claude/hooks/` but SKIPs
a file it cannot parse, by design (its verdicts are about imports, and its ignorance
refuses to flag). So a `.claude/hooks/*.py` with a syntax error could be committed and
ship gate-green (the r22 guardrail-review coverage finding this gate closes).

Mechanism: `compile(source_bytes, path, "exec")` every `*.py` under `.claude/hooks/`
(recursive, `__pycache__` excluded; the directory is flat today, and recursion keeps a
future helper subdirectory in scope by construction, unlike gate 94's deliberate
top-level-only hooks scan). `compile` runs the FULL compile-stage check the interpreter
performs (it catches `return` / `break` / `continue` / `yield` / `nonlocal` at module
scope and other errors that a bare `ast.parse` accepts), but it never imports or
executes the module, so no hook side effect can fire during the audit. Compiling RAW
BYTES (not a pre-decoded str) honours PEP 263 coding declarations and a leading UTF-8
BOM, so the gate matches `python3 hook.py` compilability rather than diverging from it
in the false-positive direction. On SyntaxError (which subsumes IndentationError,
TabError, and an encoding-declaration error) the gate prints `path:line: <message>` and
exits 1; a file with null bytes fails the same way. Exit 0 with a scanned-file count
otherwise.

Residues, stated: a compile under THIS interpreter proves compilability for the Python
version CI runs, not for every interpreter an adopter might use; and a missing or empty
hooks directory passes with a count of 0 (an adopter fork without the hook tree stays
green), so the gate proves "everything present compiles", never "the hooks are present".

Usage:
    python3 tools/lint-hooks-syntax.py                # scan .claude/hooks/ (gate 95)
    python3 tools/lint-hooks-syntax.py --hooks-dir D  # fixture/regression override

Exit codes: 0 = every scanned file compiles; 1 = one or more files do not compile.

Stdlib-only Python 3.11.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HOOKS_DIR = REPO_ROOT / ".claude" / "hooks"


def _scan_files(hooks_dir: Path) -> list[Path]:
    if not hooks_dir.is_dir():
        return []
    return [
        p for p in sorted(hooks_dir.rglob("*.py"))
        if p.is_file() and "__pycache__" not in p.relative_to(hooks_dir).parts
    ]


def _rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:  # a --hooks-dir fixture outside the repository
        return str(path)


def scan(hooks_dir: Path) -> tuple[int, list[str]]:
    files = _scan_files(hooks_dir)
    findings: list[str] = []
    for path in files:
        try:
            source = path.read_bytes()
        except OSError as exc:
            findings.append(f"{_rel(path)}:0: unreadable: {exc}")
            continue
        try:
            # compile (never exec/import) runs the full compile-stage check the
            # interpreter runs; compiling RAW BYTES honours PEP 263 + a UTF-8 BOM.
            compile(source, str(path), "exec")
        except SyntaxError as exc:
            findings.append(f"{_rel(path)}:{exc.lineno or 0}: {exc.msg}")
        except ValueError as exc:  # null bytes in source
            findings.append(f"{_rel(path)}:0: {exc}")
    return len(files), findings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Hooks Python-syntax audit (gate 95): compile every "
                    ".claude/hooks/*.py and fail on any syntax error.")
    ap.add_argument("--hooks-dir", default=str(HOOKS_DIR),
                    help="directory to scan (default: .claude/hooks/; regression override)")
    args = ap.parse_args(argv)
    count, findings = scan(Path(args.hooks_dir))
    if findings:
        print("FAIL: hook file(s) that do not compile as Python (a syntax-broken hook "
              "fails open and silently stops protecting; fix the file, never delete "
              "the hook):")
        for line in findings:
            print(f"  {line}")
        return 1
    print(f"OK: hooks Python-syntax audit clean ({count} hook file(s) compiled).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
