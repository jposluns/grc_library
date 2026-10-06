#!/usr/bin/env python3
"""UserPromptSubmit hook: every turn, inject the current UTC timestamp + session duration + a
reminder of the maintainer standing rule into context, so the assistant always has FRESH values and
is re-primed against convention-erosion.

Maintainer-directed 2026-08-21: every message the assistant authors MUST begin with the current UTC
timestamp and end with the session duration. This hook is the anti-forgetting half (supplies the
exact values so the assistant need not guess); block-unstamped-turn-end.py is the enforcing half.

MAINTAINER-SCOPED (no-op for adopters, who lack grc_library_private): the console-format rule is the
maintainer's preference, not portable. FAIL-OPEN on any error: a prompt is never blocked or delayed.
"""
import json
import sys


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


try:
    _session_clock = _load_sibling("_session_clock")
    stamp_and_duration = _session_clock.stamp_and_duration
    maintainer_env = _session_clock.maintainer_env
except Exception:
    def stamp_and_duration(tp, now=None):
        return None, None

    def maintainer_env():
        return False


def _is_worker() -> bool:
    """Dispatched orch-verify worker? Session-discipline hooks are orchestrator-scoped and no-op in a
    worker (WK-HOOK1: the stamp hook made every claude worker re-send its whole deliverable). Fail-safe:
    any detection error -> False (keep orchestrator behaviour, the status quo)."""
    try:
        return _load_sibling("_hookutil").is_verify_worker()
    except Exception:
        return False


def main() -> int:
    if "--self-test" not in sys.argv and _is_worker():
        return 0
    if "--self-test" in sys.argv:
        _clock = _load_sibling("_session_clock")
        ok = (_clock.conforms("[2026-08-21 02:31Z] x (session: 1h 0m)")
              and not _clock.conforms("no stamp"))
        rc = _clock._self_test()
        print(f"{'inject-session-timestamp'} self-test: {'OK' if ok and rc==0 else 'FAIL'}")
        return 0 if (ok and rc == 0) else 1
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if not isinstance(payload, dict):
        return 0
    try:
        if not maintainer_env():
            return 0
        stamp, dur = stamp_and_duration(payload.get("transcript_path"))
    except Exception:
        return 0
    if not stamp:
        return 0
    have_dur = bool(dur)
    msg = (
        "STANDING RULE (maintainer-directed 2026-08-21): BEGIN every message you author with the "
        "current UTC timestamp and END it with the session duration. Use these values now: "
        f"start with `{stamp}` , " + (f"end with `{dur}` ." if have_dur else "and end with `(session: Xh Ym)` (session start not yet determinable this turn).") +
        " Format: `[YYYY-MM-DD HH:MMZ]` ... `(session: Xh Ym)`. This applies to every message, including short ones."
    )
    try:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": msg}}))
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
