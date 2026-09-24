#!/bin/sh
# Install the git-native hooks the pre-commit framework does not manage.
#
# Currently: a pre-push dirty-tracked-tree backstop (tools/git-hooks/pre-push), a pre-commit
# refusal of commits on a main/master checkout (tools/git-hooks/pre-commit, P-TODO 3b17), and a
# commit-msg per-commit Version-bump check (tools/git-hooks/commit-msg, P-TODO 3b25), which also runs
# a local unmanaged hook kept as commit-msg-local.
# Run once per clone, alongside `pre-commit install`. Idempotent; refuses rather
# than clobbering an existing foreign hook, and refuses under a set core.hooksPath.
#
# KNOWN LIMITATION (routed hardening, PR #2429): the check-then-link/compare
# publish path has a residual TOCTOU window against a CONCURRENT adversarial
# writer to the shared hooks directory (e.g. a symlink swapped in between the
# existence check and the ln/cmp). This does NOT enable a dirty-push bypass
# (the checker still runs on the real tree); it needs an attacker who can
# already write .git/hooks, which is a stronger position than this race. A
# race-safe redesign (exact-destination link that rejects an existing dest;
# no pathname chmod after validation) is tracked as a follow-up.
set -eu
root="$(git rev-parse --show-toplevel)"

# core.hooksPath: detect PRESENCE by `git config --get` EXIT STATUS. A present-
# but-empty value still redirects git's hook lookup, so a `[ -n "$value" ]` test
# would miss it.
if git -C "$root" config --get core.hooksPath >/dev/null 2>&1; then
  echo "install-git-hooks: core.hooksPath is set; install the hooks" >&2
  echo "  there instead (this installer targets git's default hooks dir)." >&2
  exit 1
fi

# Worktree-safe hooks dir: in a linked worktree, .git is a FILE, not a dir, so
# do not assume "$root/.git/hooks". Resolve it via git.
hooks_rel="$(git -C "$root" rev-parse --git-path hooks)"
case "$hooks_rel" in
  /*) dest="$hooks_rel" ;;
  *)  dest="$root/$hooks_rel" ;;
esac
mkdir -p "$dest"

# A persistent file in the shared hooks dir survives removal of the worktree
# that installed it. Resolve the active checkout on EACH invocation; the tracked
# shim and Python checker therefore still come from the checkout in use.
emit_pre_push() {
  cat <<'HOOK'
#!/bin/sh
# Managed by tools/install-git-hooks.sh: dirty-tree pre-push dispatcher v1.
set -eu
root="$(git rev-parse --show-toplevel)"
exec sh "$root/tools/git-hooks/pre-push" "$@"
HOOK
}

# The pre-commit dispatcher FAILS OPEN when the active checkout has no tracked
# pre-commit file (a branch older than the hook), so it never breaks a commit there.
emit_pre_commit() {
  cat <<'HOOK'
#!/bin/sh
# Managed by tools/install-git-hooks.sh: commit-on-main pre-commit dispatcher v1.
set -eu
root="$(git rev-parse --show-toplevel)"
[ -f "$root/tools/git-hooks/pre-commit" ] || exit 0
exec sh "$root/tools/git-hooks/pre-commit" "$@"
HOOK
}

# The temp file in flight ($tmp) and any whose removal failed ($leftover) are retried
# by the EXIT trap, so an interrupted or partly failed run leaves nothing behind it can clean.
# $leftover is a NEWLINE-separated list, read back one quoted path per line, so a clone path with
# spaces or glob characters survives intact; each removal failure is tolerated so the rest still run.
tmp=""; leftover=""
cleanup() {
  if [ -n "$tmp" ]; then rm -f -- "$tmp" || :; fi
  printf '%s\n' "$leftover" | while IFS= read -r f; do
    if [ -n "$f" ]; then rm -f -- "$f" || :; fi
  done
}
trap cleanup 0
trap 'exit 1' HUP INT TERM

# The commit-msg dispatcher runs a LOCAL (unmanaged) hook kept as commit-msg-local FIRST, in every
# checkout (so a branch older than the tracked dispatcher still runs it), then FAILS OPEN for the
# tracked check when the active checkout predates it.
emit_commit_msg() {
  cat <<'HOOK'
#!/bin/sh
# Managed by tools/install-git-hooks.sh: version-bump commit-msg dispatcher v1.
set -eu
hooks="$(git rev-parse --git-path hooks)"
if [ -x "$hooks/commit-msg-local" ]; then "$hooks/commit-msg-local" "$@"; fi
root="$(git rev-parse --show-toplevel)"
[ -f "$root/tools/git-hooks/commit-msg" ] || exit 0
exec sh "$root/tools/git-hooks/commit-msg" "$@"
HOOK
}

# install_one NAME EMITTER: idempotent; refuses rather than clobbering a foreign
# hook. Every step is checked explicitly, because a function called as
# `install_one ... || status=1` runs with `set -e` disabled. Returns 1 on any
# refusal or failure so the caller can report it after trying every hook.
install_one() {
  name="$1"; emit="$2"; hook="$dest/$name"; legacy="$hook.legacy"
  # Compare the complete managed contents, not just a marker. Never follow or
  # overwrite an existing symlink, including a dangling/legacy installation.
  if [ ! -L "$hook" ] && [ -f "$hook" ] && "$emit" | cmp -s - "$hook"; then
    if ! chmod 755 "$hook"; then
      echo "install-git-hooks: could not make $hook executable." >&2
      return 1
    fi
    echo "install-git-hooks: already installed ($hook)."
    return 0
  fi
  if [ -e "$hook" ] || [ -L "$hook" ]; then
    echo "install-git-hooks: refusing to overwrite the existing hook at $hook." >&2
    echo "  Remove it or integrate the managed $name check manually, then re-run." >&2
    if [ "$name" = "commit-msg" ]; then
      echo "  To keep a local commit-msg hook, rename it to commit-msg-local (the managed hook runs" >&2
      echo "  it first), then re-run this installer." >&2
    fi
    if [ "$name" = "pre-commit" ]; then
      echo "  If it is the pre-commit framework's hook: run 'pre-commit uninstall', re-run this" >&2
      echo "  installer, then 'pre-commit install' (the framework chains the managed hook as" >&2
      echo "  pre-commit.legacy)." >&2
      if [ -f "$legacy" ] && "$emit" | cmp -s - "$legacy"; then
        # File contents cannot prove the active hook RUNS .legacy (a comment is not
        # behaviour), so the chain is never reported as installed. Verify it by behaviour.
        echo "  NOTE: a managed hook is present at $legacy, but whether the active hook runs it" >&2
        echo "  cannot be verified from file contents. Check by behaviour: on a main checkout," >&2
        echo "  'git commit --allow-empty -m probe' must be REFUSED by check-commit-on-main." >&2
      fi
    fi
    return 1
  fi
  # Publish a complete, executable file without replacing a concurrently installed
  # hook. The temporary file and destination share a filesystem, so ln is atomic.
  if ! tmp="$(mktemp "$dest/.$name.XXXXXX")"; then
    echo "install-git-hooks: could not create a temporary file in $dest." >&2
    tmp=""; return 1
  fi
  if ! "$emit" > "$tmp" || ! chmod 755 "$tmp"; then
    echo "install-git-hooks: could not prepare the $name hook." >&2
    rm -f -- "$tmp" || leftover="$leftover
$tmp"; tmp=""; return 1
  fi
  if ! ln "$tmp" "$hook"; then
    echo "install-git-hooks: could not install $hook without overwriting an existing hook." >&2
    rm -f -- "$tmp" || leftover="$leftover
$tmp"; tmp=""; return 1
  fi
  echo "installed: $hook (resolves the active checkout at run time)"
  # A failed temp removal is recorded for the EXIT trap and makes this hook's result a failure.
  if ! rm -f -- "$tmp"; then
    echo "install-git-hooks: could not remove the temporary file $tmp (retried at exit)." >&2
    leftover="$leftover
$tmp"; tmp=""; return 1
  fi
  tmp=""
  return 0
}

status=0
install_one pre-push emit_pre_push || status=1
install_one pre-commit emit_pre_commit || status=1
install_one commit-msg emit_commit_msg || status=1
exit "$status"
