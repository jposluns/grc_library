#!/bin/sh
# Install the git-native hooks the pre-commit framework does not manage.
#
# Currently: a pre-push dirty-tracked-tree backstop (tools/git-hooks/pre-push).
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
  echo "install-git-hooks: core.hooksPath is set; install the pre-push hook" >&2
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
# shim and Python checker therefore still come from the checkout being pushed.
emit_hook() {
  cat <<'HOOK'
#!/bin/sh
# Managed by tools/install-git-hooks.sh: dirty-tree pre-push dispatcher v1.
set -eu
root="$(git rev-parse --show-toplevel)"
exec sh "$root/tools/git-hooks/pre-push" "$@"
HOOK
}

hook="$dest/pre-push"

# Compare the complete managed contents, not just a marker. Never follow or
# overwrite an existing symlink, including a dangling/legacy installation.
if [ ! -L "$hook" ] && [ -f "$hook" ] && emit_hook | cmp -s - "$hook"; then
  chmod 755 "$hook"
  echo "install-git-hooks: already installed ($hook)."
  exit 0
fi
if [ -e "$hook" ] || [ -L "$hook" ]; then
  echo "install-git-hooks: refusing to overwrite the existing hook at $hook." >&2
  echo "  Remove it or integrate the dirty-tree check manually, then re-run." >&2
  exit 1
fi

# Publish a complete, executable file without replacing a concurrently installed
# hook. The temporary file and destination share a filesystem, so ln is atomic.
tmp="$(mktemp "$dest/.pre-push.XXXXXX")"
trap 'rm -f "$tmp"' 0
trap 'exit 1' HUP INT TERM
emit_hook > "$tmp"
chmod 755 "$tmp"
if ! ln "$tmp" "$hook"; then
  echo "install-git-hooks: could not install $hook without overwriting an existing hook." >&2
  exit 1
fi
echo "installed: $hook (resolves the active checkout at push time)"
