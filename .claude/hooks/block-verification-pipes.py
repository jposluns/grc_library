#!/usr/bin/env python3
"""PreToolUse Bash hook: reject pipe-masked verification commands (RM-10).

Shipped PR #620 (RM-10 hardening). Reads the PreToolUse JSON payload on stdin, inspects
`tool_input.command`, and BLOCKS (exit 2, reason on stderr) any command that
pipes a named verification command into a truncating filter, the RM-10
failure shape whose pipeline exit code reports the FILTER, not the gate:

    named commands:  pre-push-guard.sh, run_all_audits.sh,
                     run-pr-time-checks.sh, unittest, lint-*.py,
                     preflight-changelog.py
    truncating filters: tail, head, grep, sed, awk

The sanctioned alternative is `tools/tail-safe.sh [-n LINES] -- <command>`
(display truncation with the real exit code preserved), or a file-redirect
capture (`cmd > log; CODE=$?`), both of which pass this hook.

Exit protocol (Claude Code hooks): exit 0 allows the tool call; exit 2
blocks it and feeds stderr back to the model as the reason. Any parse
failure allows (fail-open): this hook is a guardrail against one known
mistake shape, not a security boundary, and a hook that could block all
Bash on a malformed payload would be worse than the mistake it prevents.

Acknowledged residuals (guardrail, not a parser): (1) a quoted or heredoc
line whose text itself starts with a verification invocation still blocks
(quote-blind by design; plain mentions as arguments pass via the
command-position anchor); (2) `set -o pipefail` pipes still block even
though pipefail unmasks the exit (uniformity is worth more than the edge);
(3) piping the WRAPPER's own output truncates only display (it prints
EXIT=<code>), allowed; (4) the 2026-07-04 section-1.9(c) widening added
run-linter-regression.py, build-*.py --check invocations, and the tee/wc
sinks to the named sets; a runner outside the widened set is still
uncovered by design (the wrapper and the unpiped habit are the primary
control).

Self-test: `python3 .claude/hooks/block-verification-pipes.py --self-test`.
"""

import json
import re
import sys

VERIFICATION = (
    r'(?:pre-push-guard\.sh|run_all_audits\.sh|run-pr-time-checks\.sh'
    r'|unittest\b|lint-[A-Za-z0-9_-]+\.py|preflight-changelog\.py'
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
    r'(?:python3?\s+(?:-m\s+)?|bash\s+|sh\s+)?'    # interpreter
    r'(?:[\w.~-]*/)*'                              # path prefix (tools/, ./)
)
# Then anything within the same pipeline segment (no |, ;, or newline; &
# only as part of an fd redirect like 2>&1), then a pipe straight into a
# truncating filter.
SEGMENT = r'(?:[^|;&\n]|\d?>&\d?)*'
PIPED = re.compile(COMMAND_POS + VERIFICATION + SEGMENT + r'\|[|&]?\s*' + FILTERS,
                   re.MULTILINE)


def command_is_blocked(command: str) -> bool:
    # No whole-command exemption for tail-safe.sh: under the wrapper the
    # verification name sits mid-segment (after `--`), not at command
    # position, so wrapper invocations pass this regex naturally, and a
    # wrapper mention elsewhere in a compound cannot whitelist a masked
    # pipe in another segment.
    return bool(PIPED.search(command))


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        command = payload.get('tool_input', {}).get('command', '')
    except Exception:
        return 0  # fail-open on malformed payload (see docstring)
    if not isinstance(command, str) or not command_is_blocked(command):
        return 0
    sys.stderr.write(
        "BLOCKED (RM-10 guardrail): this command pipes a verification "
        "command into a truncating filter, which masks its exit code (the "
        "pipeline reports the filter's exit, not the gate's). Run it "
        "standalone, use a file-redirect capture (cmd > log; CODE=$?), or "
        "use the sanctioned wrapper: tools/tail-safe.sh [-n LINES] -- "
        "<command> (prints the last N lines plus EXIT=<code> and exits "
        "with the real code).\n")
    return 2


def self_test() -> int:
    blocked = [
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
        # the 2026-07-04 1.9(c) widening: new runners and new sinks
        'python3 tools/run-linter-regression.py | tail -5',
        'python3 tools/build-taxonomy.py --check | head -2',
        './tools/run_all_audits.sh | wc -l',
        './tools/pre-push-guard.sh | tee /tmp/guard.log',
    ]
    allowed = [
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
