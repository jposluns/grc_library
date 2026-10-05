#!/usr/bin/env python3
"""Hooks Python-syntax audit (gate 95).

Every hook in `.claude/hooks/*.py` is executable machinery: the Claude Code harness
invokes each file with the running Python interpreter at hook-fire time. A hook with a
Python syntax error fails at exactly the moment it is supposed to protect, and the
hooks here FAIL OPEN by design (a guard that wedges the session on its own malfunction
gets disabled), so a syntax-broken hook does not announce itself: it silently stops
protecting.

Before this gate, no gate covered that. Gate 71 (stdlib-only imports) AST-parses
`tools/`, `tests/`, `.web/`, and the vendored `vendor/aiqt/tools/` and fails on an unparseable file there, but does not
scan `.claude/hooks/`; gate 94 (static unused-import) scans `.claude/hooks/` but SKIPs
a file it cannot parse, by design (its verdicts are about imports, and its ignorance
refuses to flag). So a `.claude/hooks/*.py` with a syntax error could be committed and
ship gate-green (the r22 guardrail-review coverage finding this gate closes).

Mechanism: `compile(source_bytes, path, "exec")` every `*.py` under `.claude/hooks/`
(recursive, `__pycache__` excluded; the directory is flat today, and recursion keeps a
future helper subdirectory in scope by construction, a property gate 94's scan shares since its
r22-F4 widening). `compile` runs the FULL compile-stage check the interpreter
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
version CI runs, not for every interpreter an adopter might use; and the DEFAULT hooks
directory, when missing or empty, passes with a count of 0 (an adopter fork without the hook
tree stays green), so the gate proves "everything present compiles", never "the hooks are
present". An EXPLICIT --hooks-dir that is empty, not a directory, or holds no hook file is
refused instead (3b50b2d1).

Usage:
    python3 tools/lint-hooks-syntax.py                # scan .claude/hooks/ (gate 95)
    python3 tools/lint-hooks-syntax.py --hooks-dir D  # fixture/regression override
    python3 tools/lint-hooks-syntax.py --launcher-isolation  # gate 105

Exit codes: 0 = every scanned file compiles; 1 = one or more files do not compile;
2 = a refused --hooks-dir (empty value, not a directory, or no hook file in it).

Stdlib-only Python 3.11.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
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


# Gate 105 shares this tracked tool with gate 95; select it explicitly.
class Refusal(Exception):
    """An input that cannot be proved to launch an isolated Python script."""


def _no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Refusal("duplicate JSON key " + repr(key))
        result[key] = value
    return result


def _literal(token, role):
    if not token or any(c in token for c in "$\x60*?[{~<>()}"):
        raise Refusal(role + " must be a literal path or option token: " + repr(token))


def _script(token, raw):
    prefix = '"$CLAUDE_PROJECT_DIR"/.claude/hooks/'
    if raw.startswith(prefix):
        suffix = raw[len(prefix):]
        if (not re.fullmatch(r"[A-Za-z0-9_./-]+\.py", suffix)
                or any(part in {"", ".", ".."} for part in suffix.split("/"))):
            raise Refusal("project-directory anchor needs a literal hook path")
        return
    raise Refusal('script operand must start with "$CLAUDE_PROJECT_DIR"/.claude/hooks/')


def isolation_flags(tokens):
    flags = set()
    args = iter(tokens)
    for token, raw in args:
        if token == "--" or not token.startswith("-"):
            if token == "--":
                token, raw = next(args, ("", ""))
            _script(token, raw)
            if token == "-":
                raise Refusal("stdin is refused; a script operand is required")
            for argument, _raw in args:
                _literal(argument, "script argument")
            return flags
        if token == "-":
            raise Refusal("stdin is refused; a script operand is required")
        _literal(token, "Python option")
        if token.startswith("--"):
            raise Refusal("unmodelled Python long option " + repr(token))
        body = token[1:]
        for position, char in enumerate(body):
            if char in "cm":
                raise Refusal("-c and -m are refused; a script operand is required")
            if char in "WX":
                raise Refusal("-X and -W Python options are refused")
            if char == "Q":
                argument = body[position + 1:] or next(args, ("", ""))[0]
                _literal(argument, "Python option argument")
                break
            if char not in "bBdEIOPqRsSuvx":
                raise Refusal("unmodelled Python option -" + char)
            flags.add(char)
    raise Refusal("a script operand is required")


def classify(command):
    # Check raw syntax even in quoted words; this is deliberately a narrow grammar.
    if any(c in command for c in ";|&\n\r\0<>\x60#()") or "$(" in command:
        raise Refusal("shell control, redirection, comment or substitution syntax")
    try:
        lexer = shlex.shlex(command, posix=True)
        lexer.whitespace_split = True
        lexer.commenters = ""
        tokens = []
        while True:
            start = lexer.instream.tell()
            token = lexer.get_token()
            if token is None:
                break
            raw = command[start:lexer.instream.tell()].strip()
            tokens.append((token, raw))
    except ValueError as exc:
        raise Refusal("command does not tokenize: " + str(exc)) from exc
    i = 0
    while i < len(tokens) and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tokens[i][0]):
        token, raw = tokens[i]
        name, value = token.split("=", 1)
        if not raw.startswith(name + "="):
            raise Refusal("assignment name and equals sign must be unquoted")
        prefix = 'ORCH_LEASE_FILE="$CLAUDE_PROJECT_DIR"'
        if (name != "ORCH_LEASE_FILE" or not raw.startswith(prefix)
                or not re.fullmatch(r"/[A-Za-z0-9_./-]+", raw[len(prefix):])):
            raise Refusal('only ORCH_LEASE_FILE="$CLAUDE_PROJECT_DIR"/literal/path is modelled')
        i += 1
    if i == len(tokens):
        raise Refusal("empty command (no interpreter)")
    program = tokens[i][0]
    _literal(program, "interpreter")
    if not os.path.isabs(program) or not re.fullmatch(r"python3(?:\.\d+)?", os.path.basename(program)):
        raise Refusal("an absolute interpreter path with basename python3 or python3.N is required")
    flags = isolation_flags(tokens[i + 1:])
    return "python-isolated" if "I" in flags or set("PEs") <= flags else "python-bare"


def iter_commands(node, trail="hooks"):
    if isinstance(node, dict):
        if node.get("type") == "command":
            yield trail, node.get("command")
        for key, value in node.items():
            yield from iter_commands(value, trail + "." + key)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from iter_commands(value, trail + "[" + str(i) + "]")


def launcher_main(argv):
    parser = argparse.ArgumentParser(description="Hook-launcher isolation audit (gate 105)")
    parser.add_argument("--settings", default=None)
    args = parser.parse_args(argv)
    try:
        if args.settings is not None and not args.settings.strip():
            raise Refusal("--settings needs a nonempty file path")
        path = Path(args.settings) if args.settings is not None else REPO_ROOT / ".claude/settings.json"
        settings = json.loads(path.read_bytes().decode("utf-8"), object_pairs_hook=_no_duplicate_keys)
        if not isinstance(settings, dict):
            raise Refusal("settings must be a JSON object")
        commands = list(iter_commands(settings.get("hooks")))
        if not commands:
            raise Refusal("settings has no command hooks")
        findings = []
        for trail, command in commands:
            if not isinstance(command, str):
                raise Refusal(trail + ": command must be a string")
            if classify(command) != "python-isolated":
                findings.append(trail + ": " + command)
    except (Refusal, OSError, UnicodeError, ValueError) as exc:
        print("ERROR: settings.json: " + str(exc), file=sys.stderr)
        return 2
    if findings:
        print("FAIL: Python hook launcher(s) without isolation:\n  " + "\n  ".join(findings))
        return 1
    print("OK: hook-launcher isolation audit clean (" + str(len(commands)) +
          " Python launcher(s) isolated).")
    return 0


def main(argv: list[str] | None = None) -> int:
    if argv and argv[0] == "--launcher-isolation":
        return launcher_main(argv[1:])
    ap = argparse.ArgumentParser(
        description="Hooks Python-syntax audit (gate 95): compile every "
                    ".claude/hooks/*.py and fail on any syntax error.")
    ap.add_argument("--hooks-dir", default=None,
                    help="directory to scan (default: .claude/hooks/; regression override)")
    args = ap.parse_args(argv)
    # 3b50: an EXPLICIT --hooks-dir that is missing used to compile zero files and print OK;
    # refuse it (exit 2). The DEFAULT keeps its documented contract: an adopter fork without the
    # hook tree passes with zero files compiled.
    if args.hooks_dir is not None and not args.hooks_dir.strip():
        # 3b50b2d1: an empty value is Path(".") and compiled the whole current directory.
        print("ERROR: --hooks-dir needs a directory argument (an empty value is refused).",
              file=sys.stderr)
        return 2
    if args.hooks_dir is not None and not Path(args.hooks_dir).is_dir():
        print(f"ERROR: --hooks-dir {args.hooks_dir}: not a directory; nothing would be compiled.",
              file=sys.stderr)
        return 2
    if args.hooks_dir is not None and not _scan_files(Path(args.hooks_dir)):
        # 3b50b2d1: an explicit directory with no hook file compiled nothing and printed OK. The
        # predicate is the scan's own file set (recursive, regular files, no __pycache__), so a
        # nested-only tree is scanned and a directory merely named *.py is not a hook.
        print(f"ERROR: --hooks-dir {args.hooks_dir}: holds no *.py hook file; nothing would be "
              f"compiled.", file=sys.stderr)
        return 2
    count, findings = scan(Path(args.hooks_dir) if args.hooks_dir is not None else HOOKS_DIR)
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
