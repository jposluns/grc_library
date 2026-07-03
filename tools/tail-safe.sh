#!/usr/bin/env bash
#
# tail-safe.sh: the sanctioned display-truncation wrapper for verification
# commands (TODO section 1.9(a); the RM-10 pipe-masking failure class).
#
# THE PROBLEM IT CLOSES. Piping a verification command into a truncating
# filter (`guard | tail`, `run_all_audits.sh | head`) masks the command's
# exit code: the pipeline reports the FILTER's exit, so a failing gate can
# chain into a push as if green. Six RM-10 incidents trace to this shape.
#
# WHAT IT DOES. Runs the wrapped command UNPIPED with its stdout+stderr
# captured to a temp file, prints the last N lines of that capture, prints
# an explicit `EXIT=<code>` line, and exits with the command's REAL exit
# code: display truncation without exit-code loss.
#
# Usage:
#   tools/tail-safe.sh [-n LINES] -- command [args...]
#   tools/tail-safe.sh --self-test
#
# Examples:
#   tools/tail-safe.sh -n 8 -- ./tools/run_all_audits.sh
#   tools/tail-safe.sh -- ./tools/pre-push-guard.sh && git push -u origin BR
#
# The trailing `EXIT=<code>` line is printed to stdout so the truncated
# display always carries the real code visibly; the wrapper's own exit
# status carries it mechanically for `&&` chains.
#
# The PreToolUse hook at .claude/hooks/block-verification-pipes.py points
# rejected pipe invocations here. Self-test is inline (--self-test) rather
# than a tests/ fixture so the gate-36 regression runner does not adopt a
# non-linter tool (the audit-matrix-semantic-fit.py precedent).

set -u

self_test() {
  local out rc
  # 1. success propagation and EXIT line
  out="$("$0" -n 2 -- /bin/sh -c 'echo a; echo b; echo c; exit 0')"; rc=$?
  [ "$rc" -eq 0 ] || { echo "self-test FAIL: success exit not propagated (rc=$rc)"; return 1; }
  printf '%s\n' "$out" | grep -q '^EXIT=0$' || { echo "self-test FAIL: EXIT=0 line missing"; return 1; }
  printf '%s\n' "$out" | grep -q '^c$' || { echo "self-test FAIL: tail lines missing"; return 1; }
  printf '%s\n' "$out" | grep -q '^a$' && { echo "self-test FAIL: truncation did not truncate"; return 1; }
  # 2. failure propagation (the RM-10 case a bare pipe would mask)
  "$0" -n 1 -- /bin/sh -c 'echo failing; exit 7' > /dev/null; rc=$?
  [ "$rc" -eq 7 ] || { echo "self-test FAIL: failure exit not propagated (rc=$rc)"; return 1; }
  # 3. stderr captured into the display
  out="$("$0" -n 2 -- /bin/sh -c 'echo err-line 1>&2; exit 0')"; rc=$?
  printf '%s\n' "$out" | grep -q 'err-line' || { echo "self-test FAIL: stderr not captured"; return 1; }
  echo "tail-safe self-test OK (3 checks)"
  return 0
}

LINES=15
case "${1:-}" in
  --self-test) self_test; exit $?;;
esac
while [ $# -gt 0 ]; do
  case "$1" in
    -n) LINES="$2"; shift 2;;
    --) shift; break;;
    *) echo "tail-safe.sh: unknown argument '$1' (usage: tail-safe.sh [-n LINES] -- command [args...])" >&2; exit 64;;
  esac
done
[ $# -gt 0 ] || { echo "tail-safe.sh: no command given after --" >&2; exit 64; }

CAP="$(mktemp "${TMPDIR:-/tmp}/tail-safe.XXXXXX")" || exit 65
trap 'rm -f "$CAP"' EXIT

"$@" > "$CAP" 2>&1
CODE=$?

tail -n "$LINES" "$CAP"
echo "EXIT=$CODE"
exit "$CODE"
