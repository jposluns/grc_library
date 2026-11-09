#!/usr/bin/env python3
"""Public hooks syntax, self-test, launcher-isolation and registration-parity audit (gate 111).

This one tracked tool carries gate 111, the re-scoped public successor of the retired gates
95 (hooks syntax) and 105 (hook-launcher isolation) under decision D3. With no mode argument
it runs the four gate 111 checks described below, in this order: the compile check, the
self-test run, the launcher-isolation check and the registration-parity check. With
`--launcher-isolation` as its FIRST argument it runs the launcher-isolation check alone.

Every hook in `.claude/hooks/*.py` is executable machinery: the Claude Code harness
invokes each hook that `.claude/settings.json` names at hook-fire time with the absolute
`/usr/bin/python3 -I` launcher given there (the launcher check requires an absolute,
isolated launcher), and helpers those hooks import run in the same interpreter. A hook
with a Python syntax error fails at exactly the moment it is supposed to protect, and the
hooks here FAIL OPEN by design (a guard that wedges the session on its own malfunction
gets disabled), so a syntax-broken hook does not announce itself: it silently stops
protecting.

Before the retired gate 95, no gate covered that. Gate 71 (stdlib-only imports) AST-parses
`.claude/skills/corpus-management/tools/`, `.claude/skills/corpus-management/tests/`, `.web/`, and the vendored `.claude/aiqt/tools/` and fails on an unparseable file there, but does not
scan `.claude/hooks/`; gate 94 (static unused-import) scans `.claude/hooks/` but SKIPs
a file it cannot parse, by design (its verdicts are about imports, and its ignorance
refuses to flag). So a `.claude/hooks/*.py` with a syntax error could be committed and
ship gate-green (the r22 guardrail-review coverage finding this check closes).

Compile check: `compile(source_bytes, path, "exec")` every `*.py` under `.claude/hooks/`
(recursive, `__pycache__` excluded; the directory is flat today, and recursion keeps a
future helper subdirectory in scope by construction, a property gate 94's scan shares since its
r22-F4 widening). `compile` runs the FULL compile-stage check the interpreter
performs (it catches `return` / `break` / `continue` / `yield` / `nonlocal` at module
scope and other errors that a bare `ast.parse` accepts), but it never imports or
executes the module, so no hook side effect can fire during this check. Compiling RAW
BYTES (not a pre-decoded str) honours PEP 263 coding declarations and a leading UTF-8
BOM, so the check matches `python3 hook.py` compilability rather than diverging from it
in the false-positive direction. On SyntaxError (which subsumes IndentationError,
TabError, and an encoding-declaration error) the gate prints `path:line: <message>` and
fails; a file with null bytes fails the same way.

Compile-check residues, stated: a compile under THIS interpreter proves compilability for the
Python version CI runs, not for every interpreter an adopter might use; and the DEFAULT hooks
directory, when missing or empty, compiles 0 files (an adopter fork without the hook
tree compiles nothing), so the compile check proves "everything present compiles", never "the
hooks are present" (the registration-parity check below is what fails a registered hook that is
absent). An EXPLICIT --hooks-dir that is empty, not a directory, or holds no hook file is
refused instead (3b50b2d1).

Self-test run (chunk G): every scanned file that OFFERS `--self-test`, decided statically as a
file that parses and holds the exact string constant `--self-test` somewhere in its syntax
tree, is run as `<this interpreter> -I <hook> --self-test`, one at a time, with the repository
root as the working directory, stdin closed, and the runner's echo token
(`GRC_RUNNER_ECHO_TOKEN`) removed from its environment. Each run is bounded by a timeout
(`--self-test-timeout`, default 120 seconds); on a timeout the run's whole process group is
killed. A nonzero exit, a timeout, or a run that cannot start fails the gate with the hook's
path and the last lines of its output. Residues: the offer is detected by the literal
constant, so a self-test reached by another spelling is not run; a file that does not parse
is not run (the compile check already fails it); and a self-test proves only what its own cases
assert.

Launcher-isolation check (the retired gate 105, folded into gate 111 at chunk CR2B,
orchestrator decision RBQ64): read `.claude/settings.json` (or `--settings F`) as
strict JSON (a duplicate key, and a `NaN`, `Infinity` or `-Infinity` constant, are
refused), collect every `"type": "command"` entry under `hooks`, and require each
command to launch Python isolated: an absolute `python3` or `python3.N` interpreter
given `-I`, or all of `-P`, `-E` and `-s`, then a literal script operand under
`"$CLAUDE_PROJECT_DIR"/.claude/hooks/`. The only modelled prefix is an
`ORCH_LEASE_FILE="$CLAUDE_PROJECT_DIR"/literal/path` assignment. The grammar is narrow on
purpose: anything it does not model (shell control, redirection or expansion syntax, a
wrapper or non-Python program, `-c`, `-m`, stdin, `-W`, `-X`, or any other unmodelled
option, such as the Python 2 `-Q`) is refused rather than guessed at.

Registration-parity check (chunk G): from the same strictly read settings, every command hook
must name a hook file `"$CLAUDE_PROJECT_DIR"/.claude/hooks/<path>.py` that exists in the hooks
directory (a registered-but-absent hook is a silently dead control), and every `*.py` hook in
the hooks directory whose file name does not start with `_` (a `_`-prefixed file is a helper
module the hooks import, never registered) must be registered by at least one command (an
unregistered hook never fires). A mismatch either way fails the gate with the path. Residues:
parity is by path, not by event or matcher, so a hook registered under the wrong event still
passes; and when `--hooks-dir` is given WITHOUT `--settings`, parity is skipped with a NOTE
line, because the live settings register the live hooks, not a fixture directory (the runner
never passes `--hooks-dir`).

The default run exits with the highest exit code of the four checks.

Usage:
    python3 .claude/skills/corpus-management/tools/lint-hooks-syntax.py                # gate 111: compile, self-tests, launcher check, parity
    python3 .claude/skills/corpus-management/tools/lint-hooks-syntax.py --hooks-dir D  # fixture/regression override
    python3 .claude/skills/corpus-management/tools/lint-hooks-syntax.py --settings F   # gate 111 with another settings file
    python3 .claude/skills/corpus-management/tools/lint-hooks-syntax.py --self-test-timeout S  # per-hook self-test bound, seconds
    python3 .claude/skills/corpus-management/tools/lint-hooks-syntax.py --launcher-isolation  # gate 111 launcher check alone
    python3 .claude/skills/corpus-management/tools/lint-hooks-syntax.py --launcher-isolation --settings F  # launcher check alone, override

Exit codes, compile check: 0 = every scanned file compiles; 1 = one or more files do not
compile; 2 = a refused --hooks-dir (empty value, not a directory, or no hook file in it).

Exit codes, self-test run: 0 = every self-test run exited 0 (or no file offers one); 1 = one
or more self-tests exited nonzero, timed out, or could not start.

Exit codes, launcher-isolation check: 0 = settings hold at least one command hook and every one
is an isolated Python launcher; 1 = one or more modelled Python launchers lack isolation
(neither `-I` nor all of `-P`, `-E` and `-s`); 2 = a refused launcher (a command outside
the modelled grammar, or a command value that is not a string) or refused or unreadable
settings (an empty --settings value, a missing or unreadable file, non-UTF-8 bytes,
invalid JSON, a duplicate key, a `NaN`, `Infinity` or `-Infinity` constant, nesting too
deep to parse or walk, a top level that is not an object, or no command hooks).
One refused launcher makes the whole run exit 2, even if other launchers lack isolation.

Exit codes, registration-parity check: 0 = parity holds (or was skipped, see above); 1 = a
registered hook file is absent, a command names no hook file, or a hook is unregistered;
2 = refused or unreadable settings, as for the launcher check.

In both modes an argparse usage error also exits 2.

Stdlib-only Python 3.14.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import shlex
import signal
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
HOOKS_DIR = REPO_ROOT / ".claude" / "hooks"
HOOK_PREFIX = '"$CLAUDE_PROJECT_DIR"/.claude/hooks/'
SELF_TEST_FLAG = "--self-test"
SELF_TEST_TIMEOUT = 120.0  # seconds per hook self-test run
SELF_TEST_TAIL = 8  # output lines quoted from a failed self-test


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


def offers_self_test(path: Path) -> bool:
    """True when the file parses and holds the exact string constant --self-test."""
    try:
        tree = ast.parse(path.read_bytes(), filename=str(path))
    except (OSError, SyntaxError, ValueError, RecursionError, MemoryError):
        return False  # unreadable or unparseable: the compile check reports it
    return any(isinstance(node, ast.Constant) and node.value == SELF_TEST_FLAG
               for node in ast.walk(tree))


def _tail(text: str) -> str:
    lines = [line for line in text.splitlines() if line.strip()][-SELF_TEST_TAIL:]
    return "".join("\n    | " + line for line in lines)


def run_self_tests(files: list[Path], timeout: float) -> tuple[int, list[str]]:
    """Run each file that offers --self-test, one at a time, under a bounded timeout."""
    env = {k: v for k, v in os.environ.items() if k != "GRC_RUNNER_ECHO_TOKEN"}
    ran = 0
    findings: list[str] = []
    for path in files:
        if not offers_self_test(path):
            continue
        ran += 1
        try:
            proc = subprocess.Popen(
                [sys.executable, "-I", str(path), SELF_TEST_FLAG], cwd=str(REPO_ROOT), env=env,
                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, errors="replace", start_new_session=True)
        except OSError as exc:
            findings.append(f"{_rel(path)}: {SELF_TEST_FLAG} could not start: {exc}")
            continue
        try:
            output, _ = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            # Kill the whole session this run started (its child git processes too).
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except (OSError, AttributeError):
                proc.kill()
            output, _ = proc.communicate()
            findings.append(f"{_rel(path)}: {SELF_TEST_FLAG} timed out after {timeout:g} s"
                            + _tail(output or ""))
            continue
        if proc.returncode != 0:
            findings.append(f"{_rel(path)}: {SELF_TEST_FLAG} exited {proc.returncode}"
                            + _tail(output or ""))
    return ran, findings


# The launcher-isolation check (the retired gate 105) and the registration-parity check both
# read the settings; `--launcher-isolation` selects the launcher check alone.
class Refusal(Exception):
    """An input that cannot be proved to launch an isolated Python script."""


def _no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Refusal("duplicate JSON key " + repr(key))
        result[key] = value
    return result


def _no_constants(name):
    # json.loads accepts NaN, Infinity and -Infinity by default; strict JSON does not.
    raise Refusal("non-JSON constant " + name)


def _literal(token, role):
    if not token or any(c in token for c in "$\x60*?[{~<>()}"):
        raise Refusal(role + " must be a literal path or option token: " + repr(token))


def _hook_suffix(raw):
    """The literal hook path after the project anchor, or a Refusal."""
    suffix = raw[len(HOOK_PREFIX):]
    if (not re.fullmatch(r"[A-Za-z0-9_./-]+\.py", suffix)
            or any(part in {"", ".", ".."} for part in suffix.split("/"))):
        raise Refusal("project-directory anchor needs a literal hook path")
    return suffix


def _script(token, raw):
    if raw.startswith(HOOK_PREFIX):
        _hook_suffix(raw)
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
        for char in body:
            if char in "cm":
                raise Refusal("-c and -m are refused; a script operand is required")
            if char in "WX":
                raise Refusal("-X and -W Python options are refused")
            if char not in "bBdEIOPqRsSuvx":
                raise Refusal("unmodelled Python option -" + char)
            flags.add(char)
    raise Refusal("a script operand is required")


def _tokens(command):
    """(token, raw text) pairs of a command, refusing syntax outside the narrow grammar."""
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
    return tokens


def classify(command):
    tokens = _tokens(command)
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


def registered_hook(command):
    """The hook path (relative to .claude/hooks/) a command names, or a Refusal."""
    for _token, raw in _tokens(command):
        if raw.startswith(HOOK_PREFIX):
            return _hook_suffix(raw)
    raise Refusal('names no "$CLAUDE_PROJECT_DIR"/.claude/hooks/ hook file')


def iter_commands(node, trail="hooks"):
    if isinstance(node, dict):
        if node.get("type") == "command":
            yield trail, node.get("command")
        for key, value in node.items():
            yield from iter_commands(value, trail + "." + key)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from iter_commands(value, trail + "[" + str(i) + "]")


def load_commands(settings_arg):
    """Every (trail, command) hook entry of the strictly read settings, or a Refusal."""
    if settings_arg is not None and not settings_arg.strip():
        raise Refusal("--settings needs a nonempty file path")
    path = Path(settings_arg) if settings_arg is not None else REPO_ROOT / ".claude/settings.json"
    settings = json.loads(path.read_bytes().decode("utf-8"), object_pairs_hook=_no_duplicate_keys,
                          parse_constant=_no_constants)
    if not isinstance(settings, dict):
        raise Refusal("settings must be a JSON object")
    commands = list(iter_commands(settings.get("hooks")))
    if not commands:
        raise Refusal("settings has no command hooks")
    return commands


def launcher_main(argv):
    parser = argparse.ArgumentParser(
        description="Hook-launcher isolation check of gate 111 (the retired gate 105), run alone")
    parser.add_argument("--settings", default=None)
    args = parser.parse_args(argv)
    try:
        commands = load_commands(args.settings)
        findings = []
        for trail, command in commands:
            if not isinstance(command, str):
                raise Refusal(trail + ": command must be a string")
            if classify(command) != "python-isolated":
                findings.append(trail + ": " + command)
    except (Refusal, OSError, UnicodeError, ValueError, RecursionError) as exc:
        print("ERROR: settings.json: " + str(exc), file=sys.stderr)
        return 2
    if findings:
        print("FAIL: Python hook launcher(s) without isolation:\n  " + "\n  ".join(findings))
        return 1
    print("OK: hook-launcher isolation audit clean (" + str(len(commands)) +
          " Python launcher(s) isolated).")
    return 0


def parity_check(settings_arg, hooks_dir: Path) -> int:
    """Registration parity: registered hooks exist, and every non-helper hook is registered."""
    try:
        commands = load_commands(settings_arg)
    except (Refusal, OSError, UnicodeError, ValueError, RecursionError) as exc:
        print("ERROR: registration parity: settings.json: " + str(exc), file=sys.stderr)
        return 2
    findings: list[str] = []
    registered: set[str] = set()
    for trail, command in commands:
        if not isinstance(command, str):
            findings.append(f"{trail}: command is not a string, so it names no hook file")
            continue
        try:
            rel = registered_hook(command)
        except Refusal as exc:
            findings.append(f"{trail}: registered command {exc}: {command}")
            continue
        registered.add(rel)
        if not (hooks_dir / rel).is_file():
            findings.append(f"{_rel(hooks_dir / rel)}: registered in settings.json ({trail}) "
                            f"but the hook file is absent")
    hooks = [p for p in _scan_files(hooks_dir) if not p.name.startswith("_")]
    for path in hooks:
        if path.relative_to(hooks_dir).as_posix() not in registered:
            findings.append(f"{_rel(path)}: hook present but not registered in settings.json")
    if findings:
        print("FAIL: hook registration parity (a registered-but-absent hook is a dead control; "
              "an unregistered hook never fires):")
        for line in findings:
            print(f"  {line}")
        return 1
    print(f"OK: hook registration parity clean ({len(registered)} registered hook file(s) "
          f"present; {len(hooks)} non-helper hook file(s) all registered).")
    return 0


def _timeout(value: str) -> float:
    try:
        seconds = float(value)
    except ValueError:
        seconds = float("nan")
    if not 0 < seconds <= 3600:
        raise argparse.ArgumentTypeError("needs a number of seconds above 0 and at most 3600")
    return seconds


def main(argv: list[str] | None = None) -> int:
    if argv and argv[0] == "--launcher-isolation":
        return launcher_main(argv[1:])
    ap = argparse.ArgumentParser(
        description="Public hooks audit (gate 111): compile every .claude/hooks/*.py, run each "
                    "hook's --self-test under a timeout, check the settings launchers are "
                    "isolated, and check hook registration parity with .claude/settings.json.")
    ap.add_argument("--hooks-dir", default=None,
                    help="directory to scan (default: .claude/hooks/; regression override)")
    ap.add_argument("--settings", default=None,
                    help="settings file for the launcher-isolation and registration-parity "
                         "checks (default: .claude/settings.json)")
    ap.add_argument("--self-test-timeout", type=_timeout, default=SELF_TEST_TIMEOUT,
                    help="seconds each hook self-test may run before it fails the gate "
                         f"(default: {SELF_TEST_TIMEOUT:g})")
    args = ap.parse_args(argv)
    # 3b50: an EXPLICIT --hooks-dir that is missing used to compile zero files and print OK;
    # refuse it (exit 2). The DEFAULT keeps its documented contract: an adopter fork without the
    # hook tree compiles zero files.
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
    hooks_dir = Path(args.hooks_dir) if args.hooks_dir is not None else HOOKS_DIR
    count, findings = scan(hooks_dir)
    rc = 0
    if findings:
        print("FAIL: hook file(s) that do not compile as Python (a syntax-broken hook "
              "fails open and silently stops protecting; fix the file, never delete "
              "the hook):")
        for line in findings:
            print(f"  {line}")
        rc = 1
    else:
        print(f"OK: hooks Python-syntax audit clean ({count} hook file(s) compiled).")
    ran, failures = run_self_tests(_scan_files(hooks_dir), args.self_test_timeout)
    if failures:
        print("FAIL: hook self-test(s) that failed (a hook whose own cases fail may no longer "
              "protect):")
        for line in failures:
            print(f"  {line}")
        rc = max(rc, 1)
    else:
        print(f"OK: hook self-tests passed ({ran} hook file(s) offering {SELF_TEST_FLAG} run, "
              f"each bounded by {args.self_test_timeout:g} s).")
    # Gate 111 also runs the launcher-isolation check of the retired gate 105 (D3,
    # RBQ64 coverage parity), so the settings launchers stay checked.
    launcher_args = [] if args.settings is None else ["--settings", args.settings]
    rc = max(rc, launcher_main(launcher_args))
    if args.hooks_dir is not None and args.settings is None:
        print("NOTE: hook registration parity skipped: --hooks-dir was given without "
              "--settings, and the live settings register the live hooks, not that directory.")
        return rc
    return max(rc, parity_check(args.settings, hooks_dir))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
