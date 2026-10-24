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
control); (5) because the named-verifier rule judges the raw text too,
a pipe inside a comment on a verifier line may block (accepted false
block, safe direction).

The additional status-read guard covers multi-stage pipelines, including
filters followed by another stage, EXCEPT the two round-10 narrowings
documented below (a plain data-emitter first stage, and an executed &&
continuation); single-command status reads remain allowed.
After a | or |& the pipeline continues across ANY run of whitespace,
comments, blank lines and backslash-newline line continuations (round 6:
a bare backslash-newline yields no word at all, exactly as in bash, so a
blank or comment line after a continued pipe no longer splits the
pipeline), and a backslash-newline elsewhere joins its line onto the
next, so a split pipeline is judged as one pipeline. It tracks literal set -o/+o pipefail
(also short-option clusters ending in o) within a command list, and reads of
the status parameter in the next command: $? and every parameter expansion
of ? (${?}, ${?:-x}, ${?#0}, ${?%x}, ${?:+x}, ${#?} and similar), including
inside double quotes, assignments and tests. Single quotes, escapes and
comments do not count. The original named-verifier rule remains independent,
including its pipefail policy, and blocks when PIPED matches EITHER the
raw command text OR a view in which only backslash-newline line
continuations are removed (legacy_view; no comment stripping at all,
quotes untouched), so a continuation-split verifier pipeline blocks and
no misread quote or comment boundary can delete a real pipe before the
rule sees it.
Bare background & is refused unless an unconditional,
foreground, argument-free wait in the same shell scope drains all jobs.
Round 7: an unquoted $(( or a (( at a word boundary is one arithmetic word
ONLY when its interior contains identifiers, digits, whitespace other than
newline, arithmetic/bitwise operators, ? : comma, and simple $name or ${name}
references. Parentheses, quotes, backslashes, substitutions, backticks,
semicolons, newlines and all other characters reject that recognition.
Rejected spans use round-5 shell tokenization, including their nested
parentheses: an ampersand can then block valid complex arithmetic (accepted
false block, safe direction), and shell syntax is not hidden in one word.
This allowlist is lexical, not validation of an arithmetic expression.
Round 8: a << or <<- inside a rejected span is refused (arithmetic-shift):
a shift cannot be told from a heredoc there, and a heredoc reading would
skip the commands after it. Complex arithmetic that shifts, or a real
heredoc inside it, is a false block (safe direction).
Round 9: a rejected arithmetic span closes only at the adjacent )) that
always ends (( ... )) and $(( ... )); a lone ) (a case pattern arm) only
decrements its depth and never ends the span. Only space and tab (not
\\r) separate words, so a CRLF heredoc delimiter keeps its \\r and matches
its \\r terminator line instead of silently diverging.
Round 10: that close is no longer trusted to bound heredoc operators,
because a nested adjacent )) inside the span (round-9 reviews, nested-pair)
ends the tracking early while the outer arithmetic is still open. Any
command that enters the rejected-arithmetic fallback and also contains <<
anywhere now refuses (arithmetic-shift), even where the fallback seems
closed; complex arithmetic in the same command as an unrelated heredoc,
shift or here-string is a false block (safe direction). Heredoc skipping
refuses (heredoc-divergence) when the delimiter is not one plain
[A-Za-z0-9_-] word after quote removal, or when any skipped body line ends
in a backslash or holds a carriage return: bash can join, continue or
terminate such lines differently from this guard's physical-line reading,
so a LATER physically matching line could satisfy the round-9 unterminated
check while bash had already ended the heredoc and run the lines in between
(round-9 reviews, later-delimiter). A quoted-delimiter heredoc whose body
line ends in a backslash also refuses (false block, safe direction).
Round 10 also narrows the pipeline-status guard in two reviewed ways: a
two-stage pipeline whose first stage is a plain echo or printf data emitter
(round 11: "plain" is an allow-list judged after backslash-newline
continuations are removed, so only literal text, quoted literals and simple
$name/${name} references pass; any command substitution, backquote, bash-5.3
${ cmd; } / ${| cmd; } brace substitution or ${name@OP} parameter operator
disqualifies it; leading do, then, else and assignment words are skipped)
feeds data into its consumer, whose
status is exactly what $? then reads, so it sets no pending warning; and an
executed single-command && continuation replaces the guarded pipeline's
status (a skipped one leaves the pipeline's own nonzero status), so it
clears the pending warning, while a || continuation keeps it because a
skipped || branch leaves the masking filter's zero status readable.
With exactly one prior launch in that scope, wait $! and wait -n also collect
that job. Other targeted waits are not certified. Literal coproc launches
are refused. Nesting beyond 64 groups or a RecursionError refuses with a
shell-complexity message, never an allow decision or an uncaught crash.
Heredoc bodies and delimiter words are skipped by these additional guards:
<<WORD, quoted delimiters and <<-WORD (tab stripping) are recognized, including
multiple heredocs on one line. The operator line is still inspected.

Additional residuals: this is a lexical guard, not a Bash interpreter.
Literal parenthesized and brace groups are inspected with local pipefail/job
state; brace-group state sharing is not modeled, and exit-status propagation
out of subshells, brace groups and command substitutions is not modeled: a
status read after `(cmd | tail)`, `{ cmd | tail; }` or `x=$(cmd | tail)` is
not flagged. Command substitutions, eval, shell strings, functions, aliases
and here-strings are not interpreted; they can produce false positives or
missed indirect commands. Heredoc expansions and executed heredoc scripts
are not inspected; unusual delimiter syntax is not a full Bash grammar.
A heredoc whose terminator is never matched before the end of the command is
refused (heredoc-unterminated, round 9), never read as body that would hide
later commands; a divergent delimiter or skipped body line (a non-plain
delimiter word, a CR-bearing line, or a backslash-continued line) refuses
(heredoc-divergence, round 10) even when a later physical line would match,
rather than swallowing the commands in between. The legacy
named-verifier regex still scans raw heredoc, comment and quoted text as
disclosed above, both verbatim and with backslash-newline continuations
removed; either match blocks.
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
# truncating filter. The filter may sit on a following line: \s* spans the
# newline after a trailing | or |&, because bash continues the pipeline
# across that newline. PIPED matches BOTH the raw command text AND
# legacy_view(command), which only joins backslash-newline continuations
# (comment text is never removed, so a quoted # misread as a comment can
# never delete a real pipe; a pipe inside a comment on a verifier line may
# block, an accepted false block in the safe direction).
SEGMENT = r'(?:[^|;&\n]|\d?>&\d?)*'
PIPE_JOINT = r'\|[|&]?\s*(?:#[^\n]*\n\s*)*'
PIPED = re.compile(COMMAND_POS + VERIFICATION + SEGMENT + PIPE_JOINT + FILTERS,
                   re.MULTILINE)


MAX_SHELL_NESTING = 64
OPERATORS = re.compile(r"&&|\|\||\|&|&>>|&>|>>|<<-|<<<?|>&|<&|[;\n|&()<>{}]")
# $? and every parameter expansion of the ? status parameter: ${?}, ${?:-x},
# ${?#0}, ${?%x}, ${?:+x}, ${#?} (length), ${!?} and similar all read it.
STATUS_READ = re.compile(r"\$(?:\?|\{[#!]?\?)")


ARITHMETIC_CHAR = re.compile(r"[A-Za-z_0-9+*/%<>=!~&|^?:,\-]|[^\S\n]")
ARITHMETIC_VARIABLE = re.compile(r"\$(?:[A-Za-z_][A-Za-z_0-9]*|\{[A-Za-z_][A-Za-z_0-9]*\})")


def _arithmetic_end(command, i):
    """End index just past the )) closing the (( at command[i], or None.

    Accept only the strict lexical interior above, stopping at the first
    disallowed character. In particular, never count parentheses through
    quotes or shell substitutions to find a later closing delimiter.
    """
    j = i + 2
    while j < len(command):
        if command.startswith("))", j):
            return j + 2
        if ARITHMETIC_CHAR.fullmatch(command[j]):
            j += 1
            continue
        variable = ARITHMETIC_VARIABLE.match(command, j)
        if variable is None:
            return None
        j = variable.end()
    return None


def shell_tokens(command, cuts=None):
    """Yield (kind, decoded word, start, end, expands_status), without execution.

    When ``cuts`` is a list, the (start, end) spans of backslash-newline
    line continuations (which the word loop below already consumes) are
    appended to it in source order. legacy_view splices them out. Comment
    spans are NOT recorded: 3b513 round 5 removed comment cutting entirely,
    because a quoted # misread as a comment deleted real pipeline text.
    """
    i = 0
    heredocs, delimiter = [], None
    arithmetic_fallback = None
    while i < len(command):
        if command[i] in " \t":
            # Round 9: only space and tab (not \r, \f, \v) separate words,
            # matching bash's blank metacharacters; a newline is an operator.
            i += 1
            continue
        if command[i] == "#":
            end = command.find("\n", i)
            end = len(command) if end < 0 else end
            i = end
            continue
        if arithmetic_fallback is None and command.startswith("((", i):
            # Only a strict interior can hide arithmetic & and | in a word.
            end = _arithmetic_end(command, i)
            if end is not None:
                yield ("word", command[i:end], i, end,
                       bool(STATUS_READ.search(command, i, end)))
                i = end
                continue
            arithmetic_fallback = 0
            # Round 10: the adjacency close below cannot be trusted to bound
            # heredoc operators (a nested adjacent )) inside the span ends
            # the tracking early), so a command that enters the fallback and
            # contains << anywhere is refused outright.
            if "<<" in command:
                shift = command.find("<<")
                yield ("ambiguous-shift", "<<", shift, shift + 2, False)
        op = OPERATORS.match(command, i)
        if op:
            # Once recognition fails, tokenize the entire parenthesized span
            # as in round 5; do not recognize an inner (( as arithmetic.
            if arithmetic_fallback is not None:
                if op[0] == "(":
                    arithmetic_fallback += 1
                elif op[0] == ")":
                    arithmetic_fallback -= 1
                    # Round 9: a rejected arithmetic span closes only at the
                    # adjacent )) that always ends a (( ... )) or $(( ... )),
                    # i.e. a ) immediately preceded by another ). A lone )
                    # (a case pattern arm like `1)`) only decrements and can
                    # never end the span, so it cannot drop tracking early and
                    # let a later << start heredoc skipping.
                    if (arithmetic_fallback <= 0 and i > 0
                            and command[i - 1] == ")"):
                        arithmetic_fallback = None
            if arithmetic_fallback is not None and op[0] in ("<<", "<<-"):
                # Round 8: never let a shift start heredoc skipping; refuse.
                yield ("ambiguous-shift", op[0], i, op.end(), False)
                i = op.end()
                continue
            yield ("op", op[0], i, op.end(), False)
            i = op.end()
            if op[0] in ("<<", "<<-"):
                delimiter = op[0] == "<<-"
            elif op[0] == "\n":
                for terminator, strip_tabs in heredocs:
                    if not re.fullmatch(r"[A-Za-z0-9_-]+", terminator):
                        # Round 10: only one plain word, after quote removal,
                        # is matched exactly as bash matches it; any other
                        # delimiter (CR, $'...', empty, operators) can end
                        # the heredoc somewhere this guard does not look.
                        yield ("heredoc-divergence", terminator, op.start(),
                               i, False)
                    matched = False
                    while i < len(command):
                        end = command.find("\n", i)
                        end = len(command) if end < 0 else end
                        line = command[i:end]
                        i = min(end + 1, len(command))
                        if (line.lstrip("\t") if strip_tabs else line) == terminator:
                            matched = True
                            break
                        if line.endswith("\\") or "\r" in line:
                            # Round 10: bash joins a backslash-continued body
                            # line (unquoted delimiter) and treats a CR line
                            # differently from this physical-line reading, so
                            # it can terminate the heredoc EARLIER and run
                            # the skipped lines; a later physical match would
                            # defeat the round-9 unterminated refusal. Refuse.
                            yield ("heredoc-divergence", line, op.start(), i,
                                   False)
                    if not matched:
                        # Round 9: a terminator that is never matched before the
                        # end of the command (a CRLF or backslash-continued or
                        # otherwise divergent delimiter) would otherwise swallow
                        # every later command as body. Refuse, fail closed.
                        yield ("heredoc-unterminated", terminator, op.start(), i,
                               False)
                heredocs.clear()
                delimiter = None
            continue
        start, word, status, quote = i, [], False, None
        parameter_depth = 0
        quoted = False
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
                        if cuts is not None:
                            cuts.append((i, i + 2))
                        i += 2
                        if word or quoted:
                            continue
                        break  # bare continuation: no word yet; bash removes
                               # it, so re-dispatch (comment, operator, space)
            if c in "\"'" and (quote is None or quote == c):
                quote = c if quote is None else None
                quoted = True
                i += 1
                continue
            if quote != "'" and STATUS_READ.match(command, i):
                status = True
            if (quote is None and arithmetic_fallback is None
                    and command.startswith("$((", i)):
                # Apply the same strict interior to arithmetic expansions.
                end = _arithmetic_end(command, i + 1)
                if end is not None:
                    if STATUS_READ.search(command, i, end):
                        status = True
                    word.append(command[i:end])
                    i = end
                    continue
                if not parameter_depth:
                    arithmetic_fallback = 0
                    # Round 10: same outright refusal as the (( entry above.
                    if "<<" in command:
                        shift = command.find("<<")
                        yield ("ambiguous-shift", "<<", shift, shift + 2,
                               False)
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
                    and (c in " \t" or OPERATORS.match(command, i))):
                # Round 9: a word ends at space, tab, or an operator (newline
                # included via OPERATORS); \r stays in the word, so a CRLF
                # heredoc delimiter keeps its \r and matches its \r body line.
                break
            word.append(c)
            i += 1
        decoded = "".join(word)
        if not decoded and not quoted:
            # Only bare backslash-newline continuations reach here: bash
            # removes them outright, so no word existed. An empty word would
            # otherwise split a pipeline continued across a blank line.
            continue
        if delimiter is not None:
            heredocs.append((decoded, delimiter))
            delimiter = None
            status = False  # heredoc delimiter words do not expand $?
        yield ("word", decoded, start, i, status)


def legacy_view(command):
    """The continuation-joined text the legacy PIPED regex ALSO judges.

    Only backslash-newline line continuations are spliced out, exactly
    where the tokenizer consumes them; everything else, including quotes,
    comment text and raw heredoc text, stays byte-for-byte, so the
    quote-blind and raw-heredoc residuals disclosed above are unchanged
    and no comment stripping can delete a real pipe (3b513 round 5: a
    quoted # inside $( ) was misread as a comment, cutting the | tail
    that followed it). PIPED judges the raw text too; either match blocks.
    """
    cuts = []
    for _token in shell_tokens(command, cuts):
        pass
    if not cuts:
        return command
    pieces, previous = [], 0
    for start, end in cuts:
        pieces.append(command[previous:start])
        previous = end
    pieces.append(command[previous:])
    return "".join(pieces)


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


def _strip_line_continuations(raw):
    """Remove backslash-newline continuations wherever bash removes them
    before tokenizing: in unquoted and double-quoted text, but NOT inside
    single quotes (there a backslash-newline is literal). This rejoins a
    substitution opener that a line continuation split apart, e.g. a "$"
    then backslash-newline then "(", so the plain-emitter check sees the
    real opener. Single-quote regions are only entered outside double
    quotes, so an apostrophe inside double quotes stays literal."""
    out, i, n, in_dquote = [], 0, len(raw), False
    while i < n:
        c = raw[i]
        if not in_dquote and c == "'":
            end = raw.find("'", i + 1)
            if end < 0:
                out.append(raw[i:])
                break
            out.append(raw[i:end + 1])
            i = end + 1
            continue
        if c == "\\" and i + 1 < n and raw[i + 1] == "\n":
            i += 2  # line continuation: removed in bash before tokenizing
            continue
        if c == "\\" and i + 1 < n:
            out.append(raw[i:i + 2])  # keep an escaped pair (e.g. \" \$ \\)
            i += 2
            continue
        if c == '"':
            in_dquote = not in_dquote
        out.append(c)
        i += 1
    return "".join(out)


def emitter_is_plain(raw):
    """True when an echo/printf stage text can only emit data, never run code.

    Judged after _strip_line_continuations, because bash removes a
    backslash-newline before it recognizes a substitution, so an opener a
    continuation split apart is a real opener. An ALLOW-LIST: only literal
    text, single- and double-quoted literals and simple $name / ${name}
    parameter references may appear. Anything that can run code or transform
    disqualifies the stage: a $( command or arithmetic substitution, a
    backquote substitution, a bash-5.3 ${ cmd; } or ${| cmd; } brace
    substitution, and every ${name OP ...} parameter operator (including the
    @P prompt transformation). Quote context matters: inside single quotes
    nothing expands (an apostrophe in a double-quoted word is literal, not a
    delimiter); inside double quotes $(, backquote and ${...} still expand.
    An unbalanced single quote is not judged plain.
    """
    joined = _strip_line_continuations(raw)
    i, n, in_dquote = 0, len(joined), False

    def expansion_runs_code():
        # Called with joined[i] == "$"; return (disqualified, next_index).
        nxt = joined[i + 1:i + 2]
        if nxt == "(":
            return True, i + 1  # $( command or $(( arithmetic substitution
        if nxt == "{":
            m = re.match(r"\$\{[A-Za-z_][A-Za-z0-9_]*\}", joined[i:])
            if not m:
                return True, i + 1  # ${ cmd; }, ${| cmd; } or ${name OP ...}
            return False, i + m.end()  # a simple ${name} only emits data
        return False, i + 1  # a bare $name / $1 / $? only emits data

    while i < n:
        c = joined[i]
        if not in_dquote and c == "'":
            end = joined.find("'", i + 1)
            if end < 0:
                return False
            i = end + 1
            continue
        if c == "\\":
            i += 2  # the next character is an escaped literal
            continue
        if c == '"':
            in_dquote = not in_dquote
            i += 1
            continue
        if c == "`":
            return False  # backquote command substitution
        if c == "$":
            disqualified, i = expansion_runs_code()
            if disqualified:
                return False
            continue
        i += 1
    return True


def shell_violation(command):
    """Return (guard, offending source span), or None; never run shell text."""
    try:
        return _shell_violation(command)
    except RecursionError:
        return ("shell-complexity", "recursion limit")


def _shell_violation(command):
    tokens = list(shell_tokens(command))
    for kind, text, start, end, _status in tokens:
        if kind == "ambiguous-shift":
            line_start = command.rfind("\n", 0, start) + 1
            line_end = command.find("\n", end)
            line_end = len(command) if line_end < 0 else line_end
            return ("arithmetic-shift", command[line_start:line_end])
        if kind == "heredoc-unterminated":
            return ("heredoc-unterminated", text)
        if kind == "heredoc-divergence":
            return ("heredoc-divergence", text)

    def inspect(items, pipefail=False, pending=None, nesting=0):
        if nesting > MAX_SHELL_NESTING:
            return ("shell-complexity", "nesting limit")
        segment, jobs, conditional = [], [], None
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

            def emits_data(stage):
                # Round 10 (F1), hardened round 11: a plain echo or printf
                # first stage only feeds data in, so its consumer's status is
                # exactly what $? reads and nothing is masked. "Plain" is an
                # allow-list (emitter_is_plain) judged on the stage text with
                # backslash-newline continuations removed first, so a
                # substitution opener split by a continuation can no longer
                # slip through a raw-text search. Leading loop/branch words and
                # assignments sit before the emitter in command position.
                stage_words = argv(stage)
                while stage_words and (
                        stage_words[0] in ("do", "then", "else")
                        or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*",
                                        stage_words[0], re.DOTALL)):
                    stage_words.pop(0)
                if not stage_words or stage_words[0] not in ("echo", "printf"):
                    return False
                if any(t[0] != "word" and t[0] != "op" for t in stage):
                    return False  # a compound group is not a plain emitter
                raw = command[stage[0][2]:stage[-1][3]]
                return emitter_is_plain(raw)
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
            new_pending = (span if len(stages) > 1 and not pipefail
                           and not (len(stages) == 2 and emits_data(stages[0]))
                           else None)
            if conditional == "&&" and len(stages) == 1:
                # Round 10 (F2): an executed && continuation replaces the
                # guarded pipeline's status; a skipped one leaves the
                # pipeline's own nonzero status. Either way $? no longer
                # reads the masking filter. A || continuation keeps the
                # warning: a skipped || branch leaves the filter's zero.
                pending = new_pending
            else:
                pending = new_pending or (pending if conditional else None)
            if separator == "&":
                jobs.append(span)
                launched += 1
                pending = None  # an asynchronous list itself returns zero
            conditional = separator if separator in ("&&", "||") else None
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
                # A newline directly after | or |& continues the pipeline, as
                # in bash (the tokenizer already drops the whitespace and any
                # comment between the pipe and the newline).
                if (token[1] == "\n" and segment and segment[-1][0] == "op"
                        and segment[-1][1] in ("|", "|&")):
                    i += 1
                    continue
                found = finish(token[1])
                if found:
                    return found
            else:
                segment.append(token)
            i += 1
        found = finish("")
        return found or (("untracked-background", jobs[0]) if jobs else None)

    return inspect(tokens)


def piped_verifier(command):
    """The legacy named-verifier rule, conservative: a PIPED match on the
    raw text OR on the continuation-joined view (legacy_view) blocks."""
    return PIPED.search(command) or PIPED.search(legacy_view(command))


def command_is_blocked(command: str) -> bool:
    # Keep the legacy command-position matcher and its existing exemptions,
    # judged on the raw text and on the continuation-joined view.
    return bool(shell_violation(command) or piped_verifier(command))


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        command = payload.get('tool_input', {}).get('command', '')
    except Exception:
        return 0  # fail-open on malformed payload (see docstring)
    if not isinstance(command, str):
        return 0
    violation = shell_violation(command)
    if not violation and not piped_verifier(command):
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
        elif guard == "arithmetic-shift":
            sys.stderr.write(
                "BLOCKED (arithmetic-shift): << inside complex arithmetic in " + repr(span) + ".\n"
                "WHY: the guard cannot tell this shift from a heredoc, which would hide "
                "the commands after it.\n"
                "CONSIDER INSTEAD: compute the value in simple arithmetic, e.g. "
                "$((1 << n)) with n set first, or split the command.\n")
        elif guard == "heredoc-unterminated":
            sys.stderr.write(
                "BLOCKED (heredoc-unterminated): heredoc terminator " + repr(span)
                + " is never matched before the end of the command.\n"
                "WHY: the rest of the command would be read as heredoc body, hiding "
                "any commands after a terminator bash would have matched (a CRLF or "
                "backslash-continued delimiter diverges from the registered word).\n"
                "CONSIDER INSTEAD: close the heredoc with its exact terminator alone "
                "on a line with no trailing carriage return or line continuation, or "
                "split the command.\n")
        elif guard == "heredoc-divergence":
            sys.stderr.write(
                "BLOCKED (heredoc-divergence): heredoc delimiter or body line "
                + repr(span) + " diverges from plain line reading.\n"
                "WHY: bash can join, continue or terminate a backslash-continued or "
                "CR-bearing line, or a non-plain delimiter, differently from this "
                "guard, hiding the commands between bash's real terminator and a "
                "later matching line.\n"
                "CONSIDER INSTEAD: use one plain [A-Za-z0-9_-] delimiter word, keep "
                "skipped body lines free of trailing backslashes and carriage "
                "returns, or split the command.\n")
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
        # round 3: a pipeline continued after a trailing | or |& is ONE pipeline
        './tools/run_all_audits.sh 2>&1 |\ncat; echo $?',
        'cmd |\ncat; echo $?',
        'cmd |&\ncat; echo $?',
        'cmd | # filtered below\ncat; echo $?',
        'tools/run_all_audits.sh 2>&1 |\ntail -8',
        './tools/run_all_audits.sh | # note\ntail -3',
        # round 3: every parameter expansion of ? is a status read
        'cmd | cat; echo ${?:-x}',
        'cmd | cat; rc=${?#0}',
        'cmd | cat; test ${#?} -eq 1',
        # round 4: a backslash-newline continuation is the same pipeline
        './tools/run_all_audits.sh 2>&1 | \\\ntail -8',
        './tools/run_all_audits.sh 2>&1 |\\\ntail -8',
        './tools/run_all_audits.sh 2>&1 \\\n| tail -8',
        'git push -u origin br 2>&1 | \\\ntail -3',
        # round 5: the raw text is judged too, so a quoted # misread as a
        # comment can no longer delete the real pipe (round-4 A1/A2)
        'echo "$(./tools/run_all_audits.sh "a # b" | tail -8)"',
        'x="$(git push "a # b" | tail -8)"',
        # round 5 accepted residual: a pipe inside a comment on a verifier
        # line may block (accepted false block, safe direction)
        './tools/run_all_audits.sh # | tail',
        './tools/run_all_audits.sh # keep |\ntail -f log',
        # round 6: blank and comment lines after a continued pipe are still
        # the same pipeline (R5-1)
        'cmd | \\\n\ncat; echo $?',
        'cmd | \\\n\n\ncat; echo $?',
        'cmd | \\\n# note\ncat; echo $?',
        # round 6: a real background launch next to arithmetic still blocks
        'echo $((1 & 2)) &',
        '(( flags & 1 )) &',
        'cmd | cat; echo $(( $? + 1 ))',
        # round 7: rejected arithmetic spans retain shell syntax (R6 reviews)
        'echo $(( $(cmd | tail; echo $?) ))',
        'echo $(( $(cmd &) ))',
        '(( $(cmd &) ))',
        '((printf background) & (true))',
        '((false |\ncat; echo $?) | (cat))',
        'declare -A a; a[\'((\']=1; (( a["(("] )); '
        "printf 'launched\\n' & # ))",
        'declare -A a; a[\'((\']=1; (( a["(("] )); '
        'false | cat; echo $? # ))',
        'echo $(( (1 & 2) | 4 ))',
        'echo $(( $((1 & 2)) ))',
        # round 9: a divergent heredoc terminator refuses rather than
        # swallowing the commands after it (CRLF and backslash-continued)
        'cat <<EOF\r\nbody\r\nEOF\r\n: &\r\n',
        'cat <<EOF\r\nbody\r\nEOF\r\nfalse | cat; echo $?\r\n',
        'cat <<EOF\nE\\\nOF\n: &',
        # round 9: a case pattern arm's ) no longer drops arithmetic tracking
        # early, so a later << inside the span still refuses (arithmetic-shift)
        'echo $(( $(case 1 in 1) echo 1;; 2) echo 2;; esac) + (1 << (2)) ))\n: &',
        'echo $(( $(case 1 in 1) echo 1;; 2) echo 2;; esac) + (1 << (2)) ))\n'
        'false | cat; echo $?',
        # round 10 (later-delimiter): a later physically matching delimiter
        # no longer rescues a divergent heredoc; bash terminates these
        # earlier and runs the hidden launch or status read
        'cat <<EOF\nE\\\nOF\n: &\n: <<EOF\nEOF',
        'cat <<EOF\nE\\\nOF\nfalse |\ncat; echo $?\n: <<EOF\nEOF',
        'cat <<-EOF\n\tE\\\nOF\n: &\n: <<EOF\nEOF',
        "cat <<$'EOF'\nEOF\n: &\n: <<'X'\n$EOF\nX",
        # round 10 (nested-pair): a nested adjacent )) ends fallback tracking
        # early; any << in a command entering the fallback refuses
        '(( $(case 1 in 1) echo 0;; 2) echo 0;; esac) + ((1)) + (1 << EOF) ))'
        '\n: &\nEOF',
        '(( 1 + $(case x in x) printf 1;; y) :;; z) :;; esac) + ((2)) << (2) ))'
        '\n: &\n((\n2\n))',
        '(( 1 + $(case x in x) printf 1;; y) :;; z) :;; esac) + ((2)) << (2) ))'
        '\nfalse |\ncat; echo $?\n((\n2\n))',
        # round 10 accepted false block (safe direction): completed complex
        # arithmetic no longer certifies a later heredoc in the same command
        '(( (1) )); cat <<E\nz &\nE',
        # round 10 F1/F2 boundaries that must keep refusing: a third stage,
        # a substituting emitter, and a || continuation
        "echo '{\"x\":1}' | python3 -I .claude/hooks/block-on-open-findings.py"
        ' | cut -c1-160; echo "guard rc=$?"',
        'echo "$(cmd)" | python3 tools/open-findings-row.py; echo rc=$?',
        'git -C w status --short | wc -l || true; echo rc=$?',
    ]
    allowed = [
        # round 9: heredocs whose terminator IS matched keep allowing
        'cat <<EOF\nx & y\nEOF',
        'cat <<-EOF\n\tx & y\n\tEOF',
        "cat <<'EOF'\nx & y\nEOF",
        '(( 1 + 2 )); cat <<E\nz &\nE',
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
        # round 3: a split pipeline with no status read stays allowed
        'a |\nb',
        # round 3: heredoc body text ending a line with | is data, not shell
        "cat <<'EOF'\nfoo |\necho $?\nEOF\n",
        # round 3: a single-command status read via a modified expansion
        'grep -q pat file; echo ${?:-x}',
        'set -o pipefail; cmd |\ncat; echo $?',
        # round 5: a comment line BEFORE an unpiped verifier still allows
        # (the accepted comment-pipe false block needs the verifier's line)
        '# | tail\n./tools/run_all_audits.sh',
        "echo 'a | \\\ntail'",
        # round 7: simple arithmetic AND/OR in either form stays allowed
        'echo $(( 1 & 2 ))',
        '(( flags & 1 ))',
        'echo $(( 1 | 2 ))',
        '(( flags | 1 ))',
        'echo $(( $flags & ${mask} ))',
        '(( $flags | ${mask} ))',
        'x=$((a & b)); echo $x',
        # round 10 (F1): a plain data emitter feeding one consumer does not
        # mask a status; $? reads the consumer (a writer or a hook under test)
        'echo \'{"tool_name":"Bash"}\' | python3 -I '
        '.claude/hooks/block-on-open-findings.py; echo rc=$?',
        'printf \'%s\\n\' "$line" | python3 tools/open-findings-row.py; echo $?',
        'for f in a b; do printf \'%s\\n\' "$f" | python3 -I "$H"; done; rc=$?',
        # round 10 (F2): an executed && continuation replaces the pipeline's
        # status, so the later read is the continuation's, not the filter's
        'git -C w status --short | wc -l && python3 '
        'tools/lint-version-bump-recency.py >/dev/null 2>&1; echo recency=$?',
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
