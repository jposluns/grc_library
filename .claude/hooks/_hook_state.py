#!/usr/bin/env python3
"""Shared block-state helper for the PreToolUse self-guard hooks.

Records the recent BLOCK decisions the sibling guard hooks make, to a small local JSONL
state file, so a follow-up hook (`block-repeated-tool-failure.py`) can detect two failure
shapes the sibling guards cannot see on their own:

  (1) a command resubmitted UNCHANGED after a sibling hook just blocked it (the
      intent-vs-artefact loop the orchestrator hit 2026-07-19: it re-submitted the same
      `credit-offload-queue.py`-from-the-wrong-cwd command seven times, editing the command
      DESCRIPTION each time, never the command STRING the block asked it to change); and
  (2) a run of consecutive same-class blocks (the diagnosis circuit-breaker, which forces a
      written mechanism-diagnosis before another retry).

The state file is `.claude/hooks/.state/recent-blocks.jsonl`, machine-local and gitignored
(never committed). It holds at most the last `_MAX_LINES` records, one JSON object per line
(`{"cmd": <normalized command>, "hook": <short hook name>, "ts": <unix int>}`).

Every function is fully failure-tolerant: any IO or parse error is a no-op (`record_*`) or
returns None / 0 (`find_*` / `consecutive_*`), so a broken, partial, or missing state file
NEVER blocks a real command. This is a guardrail helper, not a security boundary; failing
open is the correct posture. Stdlib-only (gate 71).

State-file location is overridable via the `HOOK_STATE_FILE` environment variable (resolved
at call time, not import time), which the self-tests use for deterministic isolation.
"""

import json
import os
import time
from pathlib import Path

_DEFAULT_DIR = Path(__file__).resolve().parent / ".state"
_DEFAULT_FILE = _DEFAULT_DIR / "recent-blocks.jsonl"
_MAX_LINES = 20


def _state_paths() -> tuple[Path, Path]:
    """Return (state_dir, state_file), honouring the HOOK_STATE_FILE override.

    Resolved at call time so a test (or a caller) can redirect the state file by setting the
    environment variable without re-importing the module."""
    override = os.environ.get("HOOK_STATE_FILE")
    if override:
        f = Path(override)
        return f.parent, f
    return _DEFAULT_DIR, _DEFAULT_FILE


def _normalize(command: str) -> str:
    """Normalize a command for byte-equality comparison: strip TRAILING whitespace only.

    Internal spaces are preserved deliberately. A resubmission that only changes trailing
    whitespace is still the same command (it must block again), whereas a real structural fix
    (adding `cd <repo-root> &&`, `git -C <path>`, or an absolute path) changes the
    non-whitespace bytes and so is correctly treated as a different, allowed command."""
    if not isinstance(command, str):
        return ""
    return command.rstrip()


def subject_from_payload(payload: dict) -> str:
    """The canonical BLOCK subject string, uniform across Bash and AskUserQuestion, so a
    record written by one guard is comparable by another.

    Bash -> `tool_input.command`; AskUserQuestion -> the question + header text of every
    question, joined. Both `block-repeated-tool-failure.py` (the reader) and the sibling
    guards (the recorders, via the patch spec) call this same function, so the stored `cmd`
    and the looked-up subject are byte-identical for the same tool call. Returns "" on any
    error (a subject that never matches, so the guard fails open)."""
    try:
        tool_input = payload.get("tool_input") or payload.get("toolInput") or {}
        cmd = tool_input.get("command")
        if isinstance(cmd, str) and cmd.strip():
            return cmd
        parts = []
        for q in tool_input.get("questions", []) or []:
            if isinstance(q, dict):
                parts.append(str(q.get("question", "")))
                parts.append(str(q.get("header", "")))
        return "\n".join(p for p in parts if p).strip()
    except Exception:
        return ""


def _read_records() -> list:
    """Return the parsed records (list of dicts), oldest first. Empty on any error."""
    _, state_file = _state_paths()
    try:
        raw = state_file.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    out = []
    for line in raw:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except ValueError:
            continue  # skip a corrupt line, keep the rest
        if isinstance(rec, dict):
            out.append(rec)
    return out


def record_block(command: str, hook_name: str) -> None:
    """Append a block record and keep only the last `_MAX_LINES`. No-op on any error.

    Called by a guard hook at the exact point it decides to BLOCK, so the record reflects a
    block that actually happened. Wrapped by the caller so an import or call failure here can
    never break the caller's own block (see the patch spec for the existing hooks)."""
    try:
        state_dir, state_file = _state_paths()
        rec = {"cmd": _normalize(command), "hook": str(hook_name), "ts": int(time.time())}
        records = _read_records()
        records.append(rec)
        records = records[-_MAX_LINES:]
        state_dir.mkdir(parents=True, exist_ok=True)
        body = "\n".join(json.dumps(r) for r in records)
        state_file.write_text(body + "\n", encoding="utf-8")
    except Exception:
        return  # fully failure-tolerant: a broken state write never surfaces


def find_recent_block(command: str, window_sec: int = 180):
    """Return the most-recent block record whose normalized `cmd` byte-equals the normalized
    current command within `window_sec`, else None. Returns None on any error."""
    try:
        target = _normalize(command)
        if not target:
            return None
        now = int(time.time())
        for rec in reversed(_read_records()):
            ts = rec.get("ts")
            if not isinstance(ts, int) or now - ts > window_sec:
                continue
            if rec.get("cmd") == target:
                return rec
        return None
    except Exception:
        return None


def consecutive_block_count(hook_name=None, window_sec: int = 300) -> int:
    """Count how many of the most-recent CONSECUTIVE records (within `window_sec`) share a
    hook name. If `hook_name` is None, the target is the hook of the most-recent record (the
    hook currently repeating), so `consecutive_block_count()` answers "how long is the current
    run of same-class blocks". Returns 0 on any error.

    A record older than the window, or one whose hook differs from the target, ends the run."""
    try:
        now = int(time.time())
        count = 0
        target = hook_name
        for rec in reversed(_read_records()):
            ts = rec.get("ts")
            if not isinstance(ts, int) or now - ts > window_sec:
                break
            hook = rec.get("hook")
            if target is None:
                target = hook  # anchor on the tail record's hook
            if hook == target:
                count += 1
            else:
                break
        return count
    except Exception:
        return 0


def record_seen(command: str) -> None:
    """API-symmetry placeholder (the order lists it as optional). Not needed by the current
    two guards, kept as a documented no-op so a future seen-tracking guard has a hook point
    without another state surface. No-op by design."""
    return
