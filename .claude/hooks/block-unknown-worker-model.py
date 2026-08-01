#!/usr/bin/env python3
"""PreToolUse (Bash) guard: block an exec-dispatch `--model X` that names an UNKNOWN model.

The 3.194 failure mode (2026-07-30 `gpt-5-codex` recurrence): an unknown `--model` filters every
account to zero in exec-dispatch, and the resulting "no eligible account" message is
indistinguishable from a genuine no-capacity state, costing several failed dispatch attempts and
orchestrator time. exec-dispatch now fails loud itself (the `known_model_error` guard), and this
hook is the defence-in-depth layer that catches the typo BEFORE the tool runs, printing the valid
model list and the one-line update method.

Single source of truth: the top-level `known_models` map in `grc_library_private/worker-accounts.json`
(the same the tool reads). Updated in ONE place when a model releases.

FAIL-OPEN discipline: this guard can only ever be RIGHT to block a provably-unknown model. On ANY
uncertainty (no `--model`, no config, no `known_models`, an unparseable command, a read error) it
exits 0 (allow), because a guard that blocks work on its own malfunction gets removed, and a removed
guard protects nothing. It blocks (exit 2) ONLY when it positively resolves a family + a model and
the model is provably absent from that family's known set.
"""
import json
import shlex
import sys
from pathlib import Path


def _known_models():
    """The known_models map, or None on any failure (fail-open)."""
    try:
        repo_root = Path(__file__).resolve().parents[2]
        cfg = repo_root.parent / "grc_library_private" / "worker-accounts.json"
        if not cfg.is_file():
            return None
        km = json.loads(cfg.read_text(encoding="utf-8")).get("known_models")
        return km if isinstance(km, dict) else None
    except Exception:
        return None


def _flag(tokens, name):
    """Value of `--name V` (or `--name=V`) in a token list, else None. Last wins."""
    val = None
    for i, t in enumerate(tokens):
        if t == name and i + 1 < len(tokens):
            val = tokens[i + 1]
        elif t.startswith(name + "="):
            val = t.split("=", 1)[1]
    return val


def evaluate(command: str):
    """PURE decision. Return a block-message string, or None to allow. Fail-open on any doubt."""
    if not command or "exec-dispatch.py" not in command:
        return None
    try:
        tokens = shlex.split(command)
    except Exception:
        return None  # unparseable -> allow
    if not any("exec-dispatch.py" in t for t in tokens):
        return None
    family = _flag(tokens, "--family")
    model = _flag(tokens, "--model")
    if not family or not model:
        return None  # can't resolve both -> allow
    km = _known_models()
    if not isinstance(km, dict) or family not in km:
        return None  # no source of truth for this family -> allow (fail OPEN)
    valid = km.get(family)
    if not isinstance(valid, (list, tuple, set)):
        return None  # malformed family value -> allow (fail OPEN)
    if model in valid:
        return None
    return (f"BLOCKED (3.194 model-validity guard): --model {model!r} is not a known {family} "
            f"model, so exec-dispatch would filter every account to zero and report a misleading "
            f"'no eligible account'. Valid {family} models: {sorted(valid)}. If this is a "
            f"newly-released model, add it to known_models[{family!r}] in "
            f"grc_library_private/worker-accounts.json (the single source of truth), then retry.")


def _self_test():
    fixture = {"known_models": {"claude": ["opus", "sonnet"], "codex": ["gpt-5.6-sol"]}}
    global _known_models
    orig = _known_models
    _known_models = lambda: fixture["known_models"]  # noqa: E731
    checks = []
    def c(name, cond):
        checks.append((name, cond))
    try:
        c("blocks-unknown-codex", evaluate("python3 tools/exec-dispatch.py --dispatch --family codex --model gpt-5-codex") is not None)
        c("allows-known-codex", evaluate("python3 tools/exec-dispatch.py --dispatch --family codex --model gpt-5.6-sol") is None)
        c("blocks-unknown-claude", evaluate("exec-dispatch.py --family claude --model opus-9 --dispatch") is not None)
        c("allows-known-claude", evaluate("exec-dispatch.py --family claude --model opus") is None)
        c("allows-eq-form", evaluate("exec-dispatch.py --family=codex --model=gpt-5.6-sol") is None)
        c("blocks-eq-form-unknown", evaluate("exec-dispatch.py --family=codex --model=nope") is not None)
        c("allows-no-model", evaluate("exec-dispatch.py --family codex --dispatch") is None)
        c("allows-no-family", evaluate("exec-dispatch.py --model gpt-5-codex") is None)
        c("allows-non-execdispatch", evaluate("echo --model gpt-5-codex") is None)
        c("allows-empty", evaluate("") is None)
        # fail-open when no config
        _known_models = lambda: None  # noqa: E731
        c("failopen-no-config", evaluate("exec-dispatch.py --family codex --model nope") is None)
        _known_models = lambda: {"codex": ["x"]}  # noqa: E731  (claude family absent)
        c("failopen-family-absent", evaluate("exec-dispatch.py --family claude --model opus") is None)
        _known_models = lambda: {"claude": None}  # noqa: E731  (malformed family value)
        c("failopen-malformed-value", evaluate("exec-dispatch.py --family claude --model opus") is None)
        _known_models = lambda: "oops"  # noqa: E731  (non-dict km)
        c("failopen-nondict-km", evaluate("exec-dispatch.py --family claude --model opus") is None)
    finally:
        _known_models = orig
    bad = [n for n, ok in checks if not ok]
    if bad:
        print(f"block-unknown-worker-model self-test: FAIL {bad}")
        return 1
    print(f"block-unknown-worker-model self-test: OK ({len(checks)} checks)")
    return 0


def main():
    if "--self-test" in sys.argv:
        return _self_test()
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # no/'bad payload -> allow
    if payload.get("tool_name") != "Bash":
        return 0
    command = (payload.get("tool_input") or {}).get("command", "")
    try:
        msg = evaluate(command)
    except Exception:
        return 0  # any unexpected error -> fail OPEN (never wedge a Bash command)
    if msg:
        print(msg, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
