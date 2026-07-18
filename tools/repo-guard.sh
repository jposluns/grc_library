#!/usr/bin/env bash
#
# Cross-repo write-safety guard (TODO section 1.15a).
#
# The maintainer-orchestrator works across three colocated repositories under
# /home/jposluns/ (grc_library, grc_library_ref, grc_library_scratch, plus
# grc_library_private), and the Bash tool's working directory persists a `cd` across
# calls. So a cwd-dependent repo-mutating git command can silently target the WRONG
# repository (observed 2026-07-15: a grc_library-intended `git checkout main && git pull`
# ran in grc_library_scratch because the cwd had persisted an earlier `cd` into scratch).
#
# This wrapper is the mechanical half of the guardrail: route a repo-mutating command
# through it with an explicit --repo assertion, and it refuses (non-zero) unless the
# current git repository's top-level directory basename matches the asserted repo. On a
# match it execs the command, so the command's own exit code passes through unchanged.
#
# Usage:
#   tools/repo-guard.sh <expected-repo-basename> -- <command> [args...]
#
# Examples:
#   tools/repo-guard.sh grc_library -- git checkout main
#   tools/repo-guard.sh grc_library_scratch -- git reset --hard origin/main
#
# Exit codes:
#   0            the command ran (its own exit code is passed through on success)
#   <cmd's rc>   the command ran and returned non-zero (passed through)
#   2            usage error (missing --repo assertion, missing `--`, or empty command)
#   3            REFUSED: the current repo's toplevel basename does not match --repo, or
#                the cwd is not inside a git work tree (fail-loud, the command did NOT run)
#
# It is a utility wrapper, not an audit gate: it is NOT wired into run_all_audits.sh and
# never runs in CI. It is defence-in-depth for interactive cross-repo work; the paired
# convention (confirm the target repo before every mutating command) lives in the project
# CLAUDE.md.

set -uo pipefail

die_usage() {
  echo "repo-guard: usage: tools/repo-guard.sh <expected-repo-basename> -- <command> [args...]" >&2
  echo "repo-guard: $1" >&2
  exit 2
}

[ "$#" -ge 1 ] || die_usage "missing the expected-repo-basename assertion"
EXPECTED="$1"
shift

[ "${1:-}" = "--" ] || die_usage "missing the '--' separator before the command"
shift

[ "$#" -ge 1 ] || die_usage "no command given after '--'"

# Resolve the current git work tree's top-level basename. Fail loud if not in a work tree.
TOPLEVEL="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  echo "repo-guard: REFUSED -- current directory is not inside a git work tree (expected repo '$EXPECTED')." >&2
  exit 3
}
ACTUAL="$(basename "$TOPLEVEL")"

if [ "$ACTUAL" != "$EXPECTED" ]; then
  echo "repo-guard: REFUSED -- asserted repo '$EXPECTED' but the current work tree is '$ACTUAL' ($TOPLEVEL)." >&2
  echo "repo-guard: the command was NOT run. cd to the intended repo, or correct the --repo assertion." >&2
  exit 3
fi

# Match: run the command; its exit code passes through.
exec "$@"
