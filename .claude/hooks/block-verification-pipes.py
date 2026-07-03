#!/usr/bin/env python3
"""PreToolUse Bash hook: reject pipe-masked verification commands (RM-10).

TODO section 1.9(a). Reads the PreToolUse JSON payload on stdin, inspects
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

Self-test: `python3 .claude/hooks/block-verification-pipes.py --self-test`.
"""

import json
import re
import sys

VERIFICATION = (
    r'(?:pre-push-guard\.sh|run_all_audits\.sh|run-pr-time-checks\.sh'
    r'|unittest\b|lint-[A-Za-z0-9_-]+\.py|preflight-changelog\.py)'
)
FILTERS = r'(?:tail|head|grep|sed|awk)\b'
# The verification command, then anything within the same pipeline segment
# (no |, ;, or newline; & only as part of an fd redirect like 2>&1), then a
# pipe straight into a truncating filter.
SEGMENT = r'(?:[^|;&\n]|\d?>&\d?)*'
PIPED = re.compile(VERIFICATION + SEGMENT + r'\|[|&]?\s*' + FILTERS)


def command_is_blocked(command: str) -> bool:
    if 'tail-safe.sh' in command:
        return False  # the sanctioned wrapper is the fix, never the trigger
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
    ]
    allowed = [
        './tools/run_all_audits.sh',
        './tools/pre-push-guard.sh && git push -u origin br',
        './tools/run_all_audits.sh > /tmp/a.log; echo $?',
        'tools/tail-safe.sh -n 8 -- ./tools/run_all_audits.sh',
        'echo run_all_audits.sh is green',  # no pipe at all
        'git log --oneline | head -5',      # not a verification command
        './tools/run_all_audits.sh; grep -c OK /tmp/a.log',  # ; ends the segment
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
