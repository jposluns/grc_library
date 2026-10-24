#!/usr/bin/env python3
"""PreToolUse Bash hook: reject pipe-masked verification commands (RM-10).

Shipped PR #620 (RM-10 hardening). Reads the PreToolUse JSON payload on stdin, inspects
`tool_input.command`, and BLOCKS (exit 2, reason on stderr) any command that
pipes a named verification command into a truncating filter, the RM-10
failure shape whose pipeline exit code reports the FILTER, not the gate:

    named commands:  git push (including global options), pre-push-guard.sh, run_all_audits.sh,
                     run-pr-time-checks.sh, unittest, lint-*.py,
                     preflight-changelog.py
    truncating filters: tail, head, grep, sed, awk

The sanctioned alternative is `tools/tail-safe.sh [-n LINES] -- <command>`
(display truncation with the real exit code preserved), or a file-redirect
capture (`cmd > log; CODE=$?`), both of which pass this hook.

Exit protocol (Claude Code hooks): exit 0 allows the tool call; exit 2
blocks it and feeds stderr back to the model as the reason. Any JSON parse
failure allows (fail-open): this hook is a guardrail against one known
mistake shape, not a security boundary, and a hook that could block all
Bash on a malformed payload would be worse than the mistake it prevents.

Acknowledged residuals (guardrail, not a parser): (1) a quoted or heredoc
line whose text itself starts with a verification invocation still blocks
(quote-blind by design; plain mentions as arguments pass via the
command-position anchor); (2) `set -o pipefail` pipes still block even
though pipefail unmasks the exit (uniformity is worth more than the edge);
(3) piping the WRAPPER's own output truncates only display (it prints
EXIT=<code>), allowed; (4) the 2026-07-04 PR #629 widening added
run-linter-regression.py, build-*.py --check invocations, and the tee/wc
sinks to the named sets; a runner outside the widened set is still
uncovered by design (the wrapper and the unpiped habit are the primary
control).

The additional status-read guard covers ALL multi-stage pipelines, including
filters followed by another stage; single-command status reads remain allowed.
It tracks literal set -o/+o pipefail (also short-option clusters ending in o)
within a command list, and reads of $?/${?} in the next command (including double
quotes, assignments and tests). Single quotes, escapes and comments do not
count. The original named-verifier rule remains independent, including its
pipefail policy. Bare background & is refused unless an unconditional,
foreground, argument-free wait in the same shell scope drains all jobs.
With exactly one prior launch in that scope, wait $! and wait -n also collect
that job. Other targeted waits are not certified. Literal coproc launches
are refused. Nesting beyond 64 groups or a RecursionError refuses with a
shell-complexity message, never an allow decision or an uncaught crash.
Heredoc bodies and delimiter words are skipped by these additional guards:
<<WORD, quoted delimiters and <<-WORD (tab stripping) are recognized, including
multiple heredocs on one line. The operator line is still inspected.

Additional residuals: this is a lexical guard, not a Bash interpreter.
Literal parenthesized and brace groups are inspected with local pipefail/job
state; brace-group state sharing and subshell exit-status propagation are
not modeled. Command substitutions, eval, shell strings, functions, aliases
and here-strings are not interpreted; they can produce false positives or
missed indirect commands. Heredoc expansions and executed heredoc scripts
are not inspected; unusual delimiter syntax is not a full Bash grammar.
An unterminated heredoc consumes the remaining input as body text. The legacy
named-verifier regex still scans raw heredoc text as disclosed above.
Conditional lists are conservative; loops/case/if and dynamic shell-option
changes are not modeled. A literal wait is trusted to be the Bash builtin
and to be reached (early exits/signals and overridden builtins are residuals).
No completion is inferred for a child merely because it was launched.

Self-test: `python3 .claude/hooks/block-verification-pipes.py --self-test`.
"""

import json
import re
import sys

# The settings.json launcher runs `python3 -I` (SECI-config-is-executable-trust-gate): no
# directory ever enters sys.path, the colocated `_hook_state` recorder executes ONLY from
# its reviewed source bytes, loaded at the recording site through _load_sibling below, and
# no import statement names it anywhere in this file, so nothing planted beside this hook
# (a decoy module, a __pycache__/*.pyc, a seeded sys.modules entry) can run.
# MISSING-HELPER BEHAVIOUR: the decision still blocks; only the recording is skipped.
def _load_sibling(name, _cache={}):
    """Execute a reviewed repository helper's .py SOURCE BYTES and return the module.

    SECI-config-is-executable-trust-gate: the settings.json launcher runs `python3 -I`,
    this function never touches sys.path and never uses import machinery for the
    helper, so nothing planted beside a hook (a stdlib-named decoy module, a
    __pycache__/*.pyc) can execute, and no bytecode cache is ever read or written.
    Containment is decided on the path AS LAUNCHED, before any symlink resolution:
    os.path.abspath(__file__) (unresolved) must sit at <root>/.claude/hooks/<hook>.py,
    and every component from that root down to the hook and down to the helper (the
    root itself, .claude, .claude/hooks, tools, the hook file and the helper file)
    must not be a symlink; only then are real paths compared, requiring the hook's and
    the helper's real locations to sit at exactly their expected places under the real
    repository root (ancestors ABOVE the root may be symlinks: both sides of each
    comparison resolve them identically). Any violation is REFUSED fail-closed: exit 2
    with a clear message, raised as SystemExit so the hooks' fail-open
    `except Exception` guards cannot swallow it. A MISSING helper is different: the
    plain OSError propagates to the caller, which takes this hook's documented
    missing-helper behaviour, never a sys.modules fallback.

    TEST-ONLY SEAM: when this hook is loaded AS A MODULE by the in-repo test harness
    (__name__ != "__main__"), a helper already present in sys.modules is reused, which
    preserves the patch-the-helper-then-load-the-hook test contract. A production launch
    is always a direct execution (__name__ == "__main__"), and neither the environment
    nor any file in the tree can change that, so a production load NEVER consults a
    pre-existing sys.modules entry: it always re-executes the reviewed source and
    overwrites the entry (dependencies included: todo_index_rows reads lint_common from
    the entry this loader has just written).
    """
    import os.path
    import sys
    if name in _cache:
        return _cache[name]
    if __name__ != "__main__" and name in sys.modules:
        _cache[name] = sys.modules[name]
        return _cache[name]

    def _refuse(why):
        print("BLOCKED (hook-helper-isolation): " + why + "; refusing to execute "
              "anything but the reviewed helper sources.", file=sys.stderr)
        sys.exit(2)

    hook_path = os.path.abspath(__file__)  # the path AS LAUNCHED, symlinks unresolved
    hooks_dir = os.path.dirname(hook_path)
    claude_dir = os.path.dirname(hooks_dir)
    root = os.path.dirname(claude_dir)
    if os.path.basename(hooks_dir) != "hooks" or os.path.basename(claude_dir) != ".claude":
        _refuse("this hook's launch path " + hook_path + " is not under "
                "<repo-root>/.claude/hooks, so no repository root can anchor helper "
                "containment")
    parts = (".claude", "hooks") if name.startswith("_") else ("tools",)
    helper_dir = os.path.join(root, *parts)
    helper_path = os.path.join(helper_dir, name + ".py")
    for p in (root, claude_dir, hooks_dir, hook_path, helper_dir, helper_path):
        if os.path.islink(p):
            _refuse(p + " is a symlink on the path as launched (containment is "
                    "decided before any symlink resolution)")
    real_root = os.path.realpath(root)
    if os.path.realpath(hook_path) != os.path.join(real_root, ".claude", "hooks",
                                                   os.path.basename(hook_path)):
        _refuse("this hook's real location " + os.path.realpath(hook_path)
                + " does not sit at its launch-path place under the real repository "
                "root " + real_root)
    if os.path.realpath(helper_path) != os.path.join(real_root, *parts, name + ".py"):
        _refuse("helper " + helper_path + " does not resolve to its expected place "
                "under the real repository root " + real_root)
    for dep in {"todo_index_rows": ("lint_common",)}.get(name, ()):
        _load_sibling(dep)
    with open(helper_path, "rb") as fh:
        source = fh.read()
    module = type(sys)(name)
    module.__file__ = helper_path
    exec(compile(source, helper_path, "exec", dont_inherit=True), module.__dict__)
    sys.modules[name] = module
    _cache[name] = module
    return module


VERIFICATION = (
    r'(?:pre-push-guard\.sh|run_all_audits\.sh|run-pr-time-checks\.sh'
    r'''|git\s+(?:(?:(?:-[Cc]|--git-dir|--work-tree|--namespace)\s+(?:"[^"\n]*"|'[^'\n]*'|[^\s|;&]+)|-[pP]|--[^\s|;&]+)\s+)*push\b|unittest\b|lint-[A-Za-z0-9_-]+\.py|preflight-changelog\.py'''
    r'|run-linter-regression\.py|build-[A-Za-z0-9_-]+\.py(?=[^|]*--check(?![\w-])))'
)
FILTERS = r'(?:tail|head|grep|sed|awk|tee|wc)\b'
# The verification command must sit at COMMAND POSITION in its pipeline
# segment: at segment start (or after && / || / ; / & / newline / an
# opening subshell or brace), optionally preceded by env assignments, an
# interpreter (python3 [-m] / bash / sh / env), and a path prefix. This is
# what distinguishes EXECUTING a verification command from merely
# mentioning its filename as an argument (`grep -n X tools/lint-foo.py |
# head` inspects a file and masks nothing; it must pass).
COMMAND_POS = (
    r'(?:^|[;&\n(]\s*|&&\s*|\|\|\s*|\{\s+)'
    r'(?:[A-Za-z_][A-Za-z0-9_]*=\S*\s+)*'          # env assignments
    r'(?:timeout\s+[\w.]+\s+|env\s+)?'             # common runners
    r'(?:[A-Za-z_][A-Za-z0-9_]*=\S*\s+)*'          # assignments after env
    r'(?:python3?\s+(?:-m\s+)?|bash\s+|sh\s+)?'    # interpreter
    r'(?:[\w.~-]*/)*'                              # path prefix (tools/, ./)
)
# Then anything within the same pipeline segment (no |, ;, or newline; &
# only as part of an fd redirect like 2>&1), then a pipe straight into a
# truncating filter.
SEGMENT = r'(?:[^|;&\n]|\d?>&\d?)*'
PIPED = re.compile(COMMAND_POS + VERIFICATION + SEGMENT + r'\|[|&]?\s*' + FILTERS,
                   re.MULTILINE)


MAX_SHELL_NESTING = 64
OPERATORS = re.compile(r"&&|\|\||\|&|&>>|&>|>>|<<-|<<<?|>&|<&|[;\n|&()<>{}]")


def shell_tokens(command):
    """Yield (kind, decoded word, start, end, expands_status), without execution."""
    i = 0
    heredocs, delimiter = [], None
    while i < len(command):
        if command[i].isspace() and command[i] != "\n":
            i += 1
            continue
        if command[i] == "#":
            end = command.find("\n", i)
            i = len(command) if end < 0 else end
            continue
        op = OPERATORS.match(command, i)
        if op:
            yield ("op", op[0], i, op.end(), False)
            i = op.end()
            if op[0] in ("<<", "<<-"):
                delimiter = op[0] == "<<-"
            elif op[0] == "\n":
                for terminator, strip_tabs in heredocs:
                    while i < len(command):
                        end = command.find("\n", i)
                        end = len(command) if end < 0 else end
                        line = command[i:end]
                        i = min(end + 1, len(command))
                        if (line.lstrip("\t") if strip_tabs else line) == terminator:
                            break
                heredocs.clear()
                delimiter = None
            continue
        start, word, status, quote = i, [], False, None
        parameter_depth = 0
        while i < len(command):
            c = command[i]
            if quote != "'" and c == "\\":
                if i + 1 < len(command):
                    nxt = command[i + 1]
                    if quote is None or nxt in '$`"\\\n':
                        if nxt != "\n":
                            word.append(nxt)
                        i += 2
                        continue
            if c in "\"'" and (quote is None or quote == c):
                quote = c if quote is None else None
                i += 1
                continue
            if quote != "'" and (command.startswith("$?", i)
                                  or command.startswith("${?}", i)):
                status = True
            # Keep parameter expansions in a word, but still notice nested $?.
            if quote != "'" and command.startswith("${", i):
                parameter_depth += 1
                word.append("${")
                i += 2
                continue
            if parameter_depth and c == "}":
                parameter_depth -= 1
                word.append(c)
                i += 1
                continue
            if (quote is None and not parameter_depth
                    and (c.isspace() or OPERATORS.match(command, i))):
                break
            word.append(c)
            i += 1
        decoded = "".join(word)
        if delimiter is not None:
            heredocs.append((decoded, delimiter))
            delimiter = None
            status = False  # heredoc delimiter words do not expand $?
        yield ("word", decoded, start, i, status)


def pipefail_changes(words):
    """Yield literal set option changes, stopping at positional arguments."""
    if not words or words[0] != "set":
        return
    i = 1
    while i < len(words):
        option = words[i]
        if not re.fullmatch(r"[-+][A-Za-z]+", option):
            break
        if "o" in option[1:]:
            # -o consumes the following option name; o must end its cluster.
            if option.count("o") != 1 or not option.endswith("o"):
                break
            i += 1
            if i >= len(words):
                break
            if words[i] == "pipefail":
                yield option[0] == "-"
        i += 1


def shell_violation(command):
    """Return (guard, offending source span), or None; never run shell text."""
    try:
        return _shell_violation(command)
    except RecursionError:
        return ("shell-complexity", "recursion limit")


def _shell_violation(command):
    tokens = list(shell_tokens(command))

    def inspect(items, pipefail=False, pending=None, nesting=0):
        if nesting > MAX_SHELL_NESTING:
            return ("shell-complexity", "nesting limit")
        segment, jobs, conditional = [], [], False
        launched = 0

        def finish(separator):
            nonlocal pipefail, pending, segment, conditional, launched
            if not segment:
                return None
            stages = [[]]
            for token in segment:
                if token[0] == "op" and token[1] in ("|", "|&"):
                    stages.append([])
                else:
                    stages[-1].append(token)
            if pending and any(t[4] for t in segment):
                return ("pipeline-status", pending)

            def argv(stage, raw=False):
                words, skip = [], False
                for n, t in enumerate(stage):
                    if skip:
                        skip = False
                        continue
                    if t[0] == "op" and t[1] in (
                            ">", "<", ">>", "<<", "<<-", "<<<", ">&", "<&", "&>", "&>>"):
                        if (n and stage[n - 1][0] == "word"
                                and stage[n - 1][1].isdigit()
                                and stage[n - 1][3] == t[2] and words):
                            words.pop()  # adjacent IO number, not an argument
                        skip = True
                    elif t[0] == "word":
                        words.append(command[t[2]:t[3]] if raw else t[1])
                    else:
                        words.append("<compound>")
                return words

            words = argv(segment)
            span = command[segment[0][2]:segment[-1][3]]
            for stage in stages:
                stage_words = argv(stage)
                if stage_words and stage_words[0] == "coproc":
                    return ("coproc-background", span)
            # Only a standalone builtin in this shell can change its options
            # or collect its children. Conditional waits cannot prove collection.
            standalone = len(stages) == 1 and separator != "&" and not conditional
            if len(stages) == 1 and separator != "&":
                for enabled in pipefail_changes(words):
                    if not enabled or standalone:
                        pipefail = enabled  # even a conditional disable may execute
            if standalone:
                last_pid = (words == ["wait", "$!"]
                            and argv(segment, raw=True)[1] in ("$!", '"$!"'))
                if (words == ["wait"] or (launched == 1 and len(jobs) == 1
                        and (words == ["wait", "-n"] or last_pid))):
                    jobs.clear()
            new_pending = span if len(stages) > 1 and not pipefail else None
            pending = new_pending or (pending if conditional else None)
            if separator == "&":
                jobs.append(span)
                launched += 1
                pending = None  # an asynchronous list itself returns zero
            conditional = separator in ("&&", "||")
            segment = []
            return None

        i = 0
        while i < len(items):
            token = items[i]
            if token[0] == "op" and token[1] in ("(", "{"):
                closing = ")" if token[1] == "(" else "}"
                depth, end = 1, i + 1
                while end < len(items):
                    if items[end][:2] == token[:2]:
                        depth += 1
                    elif items[end][:2] == ("op", closing):
                        depth -= 1
                        if depth == 0:
                            break
                    end += 1
                found = inspect(items[i + 1:end], pipefail, pending, nesting + 1)
                if found:
                    return found
                stop = items[end][3] if end < len(items) else items[-1][3]
                segment.append(("group", command[token[2]:stop], token[2], stop, False))
                i = end + 1
                continue
            if token[0] == "op" and token[1] in (";", "\n", "&&", "||", "&"):
                found = finish(token[1])
                if found:
                    return found
            else:
                segment.append(token)
            i += 1
        found = finish("")
        return found or (("untracked-background", jobs[0]) if jobs else None)

    return inspect(tokens)


def command_is_blocked(command: str) -> bool:
    # Keep the legacy command-position matcher and its existing exemptions.
    return bool(shell_violation(command) or PIPED.search(command))


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        command = payload.get('tool_input', {}).get('command', '')
    except Exception:
        return 0  # fail-open on malformed payload (see docstring)
    if not isinstance(command, str):
        return 0
    violation = shell_violation(command)
    if not violation and not PIPED.search(command):
        return 0
    try:
        _load_sibling("_hook_state").record_block(command, "verification-pipes")
    except Exception:
        pass
    if violation:
        guard, span = violation
        # repr keeps source newlines from impersonating message-contract sections.
        if guard == "pipeline-status":
            sys.stderr.write(
                "BLOCKED (pipeline-status): status read after pipeline " + repr(span) + ".\n"
                "WHY: $? is the last stage's status, so an earlier failure can read as rc=0.\n"
                "CONSIDER INSTEAD: redirect the command to a file, read $? immediately, "
                "then read the file (cmd > log 2>&1; rc=$?; tail log); or use "
                "tools/tail-safe.sh, ${PIPESTATUS[0]}/${PIPESTATUS[@]}, or set -o pipefail.\n")
        elif guard == "untracked-background":
            sys.stderr.write(
                "BLOCKED (untracked-background): bare & detaches " + repr(span) + ".\n"
                "WHY: the child's completion is untracked.\n"
                "CONSIDER INSTEAD: use run_in_background for harness-tracked completion, "
                "or wait for every launched job in this command (a & b & wait).\n")
        elif guard == "coproc-background":
            sys.stderr.write(
                "BLOCKED (coproc-background): coproc launches a child in " + repr(span) + ".\n"
                "WHY: coprocess completion is not tracked by this guard.\n"
                "CONSIDER INSTEAD: use run_in_background for harness-tracked completion, "
                "or run the command in the foreground.\n")
        else:
            sys.stderr.write(
                "BLOCKED (shell-complexity): shell nesting exceeds the inspection limit.\n"
                "WHY: the guard cannot safely inspect this command; refusing it.\n"
                "CONSIDER INSTEAD: run simpler commands with fewer nested groups.\n")
        return 2
    sys.stderr.write(
        "BLOCKED (verification-pipes): (RM-10) this command pipes a "
        "verification command into a truncating filter "
        "(tail/head/grep/sed/awk/tee/wc).\n"
        "WHY: the pipeline reports the filter's exit code, not the gate's, "
        "so a real failure is masked and reads as a pass.\n"
        "CONSIDER INSTEAD: run the verification command standalone, use a file-redirect capture "
        "(cmd > log; CODE=$?), or use the sanctioned wrapper "
        "tools/tail-safe.sh [-n LINES] -- <command> (prints the last N "
        "lines plus EXIT=<code> and exits with the real code).\n")
    return 2


def self_test() -> int:
    blocked = [
        'cmd | tail | cat; echo $?',
        'cmd | cat; echo $?',
        'set -euo pipefail; set +o pipefail; cmd | cat; echo $?',
        'coproc cmd',
        '(' * 65 + 'true' + ')' * 65,
        'timeout 60 tools/ci-status.sh --sha X 2>&1 | tail -8; echo rc=$?',
        'python3 tools/lint-version-bump-recency.py ... 2>&1 | tail -3; echo rc=$?',
        '... | cut -c1-160; echo "guard rc=$?"',
        '(orch-verify ... ) > /dev/null 2>&1 &',
        'git push -u origin br | tail -3',
        'git -C repo -c color.ui=false push origin br | tail -3',
        'git --git-dir=repo/.git push origin br | head -1',
        'git --git-dir repo/.git push origin br | tail -1',
        'git --work-tree "some tree" --git-dir g push origin br | tail -1',
        'git --namespace space -c "color.ui=false" push origin br | tail -1',
        'git -p push origin br | tail -1',
        'git -P push origin br | tail -1',
        'env GIT_DIR=x git push origin br | tail -1',
        './tools/pre-push-guard.sh | tail -3',
        'tools/run_all_audits.sh 2>&1 | tail -8',
        './tools/run-pr-time-checks.sh | head -20',
        'python3 tools/lint-language.py | grep FAIL',
        'python3 -m unittest | tail -2',
        'python3 tools/preflight-changelog.py | sed -n 1p',
        'cd /x && ./tools/run_all_audits.sh | awk "END{print}"',
        'bash tools/run_all_audits.sh | tail -3',
        'FOO=1 ./tools/pre-push-guard.sh 2>&1 | tail -1',
        './tools/run_all_audits.sh |& tail -3',
        # the 2026-07-04 PR #629 widening: new runners and new sinks
        'python3 tools/run-linter-regression.py | tail -5',
        'python3 tools/build-taxonomy.py --check | head -2',
        './tools/run_all_audits.sh | wc -l',
        './tools/pre-push-guard.sh | tee /tmp/guard.log',
    ]
    allowed = [
        'set -euo pipefail; cmd | cat; echo $?',
        "python3 <<'PY'\nprint(1 & 2)\nPY\n",
        'a & wait $!',
        'a & wait -n',
        'cmd | tail & wait; echo $?',
        'grep -q pat file; echo $?',
        'cmd > f 2>&1; echo rc=$?',
        'set -o pipefail; cmd | tail; echo $?',
        'cmd | tail; echo ${PIPESTATUS[0]}',
        "cmd | tail; echo '$?'",
        'cmd | tail',
        'a & b & wait',
        'a && b',
        'x 2>&1',
        "echo '&'",
        'git push -u origin br',
        './tools/run_all_audits.sh',
        './tools/pre-push-guard.sh && git push -u origin br',
        './tools/run_all_audits.sh > /tmp/a.log; echo $?',
        'tools/tail-safe.sh -n 8 -- ./tools/run_all_audits.sh',
        'echo run_all_audits.sh is green',  # no pipe at all
        'git log --oneline | head -5',      # not a verification command
        './tools/run_all_audits.sh; grep -c OK /tmp/a.log',  # ; ends the segment
        # mention-not-execution: the name is an ARGUMENT, not the command
        "grep -n 'P7' tools/lint-gate-count-consistency.py | head -5",
        'wc -l tools/lint-citations.py | tail -1',
        'cat tools/lint-language.py | head -40',
        'git log --oneline -- tools/lint-language.py | head -3',
        'grep -rn unittest tests/ | head -5',
        'echo "run_all_audits.sh | tail is forbidden"',
        'git commit -m "block the run_all_audits.sh | tail shape"',
        # widening boundaries: a generator WITHOUT --check is not a verification
        'python3 tools/build-taxonomy.py | head -3',
        # regen-then-pipe of a non-check build is display truncation, allowed
        'python3 tools/build-portal.py | tail -2',
        # flag boundary: --checkout is not --check (the lookahead requires a
        # non-word, non-hyphen character after the flag)
        'python3 tools/build-taxonomy.py --checkout main | head -2',
    ]
    ok = True
    for c in blocked:
        if not command_is_blocked(c):
            print(f"self-test FAIL: should block: {c}")
            ok = False
    for c in allowed:
        if command_is_blocked(c):
            print(f"self-test FAIL: should allow: {c}")
            ok = False
    print("hook self-test OK (%d blocked, %d allowed)"
          % (len(blocked), len(allowed)) if ok else "hook self-test FAILED")
    return 0 if ok else 1


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--self-test':
        sys.exit(self_test())
    sys.exit(main())
