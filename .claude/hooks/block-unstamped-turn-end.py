#!/usr/bin/env python3
"""Stop hook: block turn-end if the assistant's FINAL authored message lacks the required leading
UTC timestamp or trailing session duration (maintainer standing rule 2026-08-21). Supplies the
correct current values in the block reason so the re-emit is trivially correct.

FINAL MESSAGE SOURCE: the Stop payload's `last_assistant_message` (a string, or an object with
`content`) is preferred over the transcript, because the transcript can lag; the transcript's last
assistant entry (content as a list of blocks OR a plain string) is the fallback.

LOOP-SAFE: on `stop_hook_active` returns 0, so it blocks AT MOST ONCE per turn-end sequence.
FAIL-OPEN: any error, a non-dict payload, a missing/unreadable transcript, empty prose, OR an
UNCOMPUTABLE duration (no parseable session start) returns 0 (allow) - it never blocks demanding a
value it cannot supply, and never wedges the session.
MAINTAINER-SCOPED: no-op for adopters (no grc_library_private).

RESIDUE: hooks cannot rewrite assistant text, so this FORCES a correction rather than performing it,
and gates only the FINAL message of a turn (intermediate narration relies on the re-prime +
discipline).
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
    conforms = _session_clock.conforms
    values_current = _session_clock.values_current
    maintainer_env = _session_clock.maintainer_env
except Exception:
    def stamp_and_duration(tp, now=None):
        return None, None

    def conforms(t):
        return True  # fail-open

    def values_current(t, tp, now=None):
        return True  # fail-open

    def maintainer_env():
        return False


def _text_from_content(parts) -> str:
    if isinstance(parts, str):
        return parts.strip()
    if isinstance(parts, list):
        return " ".join(
            p.get("text", "") for p in parts if isinstance(p, dict) and p.get("type") == "text"
        ).strip()
    return ""


def _last_assistant_text(tp) -> str:
    try:
        lines = open(tp, encoding="utf-8").readlines()
    except Exception:
        return ""
    for ln in reversed(lines):
        try:
            obj = json.loads(ln)
        except Exception:
            continue
        if not isinstance(obj, dict):
            continue
        if obj.get("type") != "assistant":
            continue
        msg = obj.get("message")
        if not isinstance(msg, dict):
            return ""
        return _text_from_content(msg.get("content", []))
    return ""


def final_message(payload) -> str:
    """The final assistant message text. If the payload PROVIDES `last_assistant_message`, use it
    AUTHORITATIVELY (even when empty -> ""), never falling through to the lagging transcript; only
    when the key is ABSENT do we read the transcript (codex ERR1 + gemini WARN)."""
    if "last_assistant_message" in payload:
        lam = payload.get("last_assistant_message")
        if isinstance(lam, str):
            return lam.strip()
        if isinstance(lam, dict):
            return _text_from_content(lam.get("content", []))
        return ""  # present but null/other -> treat as empty, do NOT fall back
    return _last_assistant_text(payload.get("transcript_path"))


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
        clock_test = _load_sibling("_session_clock")._self_test
        ok = conforms("[2026-08-21 02:31Z] x (session: 1h 0m)") and not conforms("no stamp")
        rc = clock_test()
        print(f"block-unstamped-turn-end self-test: {'OK' if ok and rc == 0 else 'FAIL'}")
        return 0 if (ok and rc == 0) else 1
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if not isinstance(payload, dict):
        return 0  # a non-dict JSON root (null / list): fail OPEN, do not crash
    if payload.get("stop_hook_active"):
        return 0  # continuation under way: block at most once (loop-safe)
    try:
        if not maintainer_env():
            return 0
        text = final_message(payload)
        if not text:
            return 0  # no prose to stamp (pure tool-use turn)
        tp = payload.get("transcript_path")
        if conforms(text) and values_current(text, tp):
            return 0
        stamp, dur = stamp_and_duration(tp)
        if dur is None:
            return 0  # cannot compute the duration -> cannot enforce it -> fail OPEN
    except Exception:
        return 0
    print(
        "BLOCKED (unstamped-turn-end): your final message lacks the required leading UTC timestamp "
        "or trailing session duration (maintainer standing rule 2026-08-21).\n"
        "WHY: every authored message must carry both so the maintainer can place it in time; the "
        "turn-end is where the final message is checked.\n"
        f"CONSIDER INSTEAD: re-send the same message starting with `{stamp}` and ending with `{dur}`.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
