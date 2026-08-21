#!/usr/bin/env python3
"""PreToolUse + Stop guard: HALT and MAINTAINER-ALERT when the orchestrator's OWN running model is Opus 5.

Maintainer-directed 2026-08-21: "add a validation so that if you ever start using OPUS 5, you stop
immediately and MAINTAINER ALERT so I can swap you to a better working model." The maintainer judges
Opus 5 a worse working model for this project than Opus 4.8 and wants a mechanical hard-stop the
moment a session (or a mid-session model swap) lands on Opus 5.

SIGNAL: the running model id, read from the LAST real assistant entry of the transcript
(payload["transcript_path"] -> message.model). This is the same transcript surface
surface-session-facts.py reads; assistant entries carry the model that produced them, so a
PreToolUse fires with the Opus-5 model already recorded when Opus 5 tries to run its first tool.
Entries whose model is not a concrete `claude-*` id (`<synthetic>` injected notifications, interrupts)
are skipped so the guard reads the last GENUINE model.

MATCH: a model id matching `claude-opus-5` or `claude-opus-5-<x>` (covers the bare id, dated
variants, the `-1m` context variant). Does NOT match `claude-opus-4-8`, any 4.x, `claude-opus-50`,
`claude-opus-5x`, or a sonnet/haiku id.

FAIL-OPEN discipline (same as the other block-* guards): this guard BLOCKS (exit 2) ONLY when it
POSITIVELY resolves the running model as Opus 5. On ANY uncertainty (no payload, no transcript_path,
an unreadable/unparseable transcript, no resolvable `claude-*` model) it exits 0 (allow). A
fail-CLOSED guard here would wedge EVERY tool call on EVERY model, the good 4.8 included, whenever it
could not read the model, which is the "a guard that blocks work on its own malfunction gets removed"
failure. RESIDUE, stated not hidden: Opus 5 running while the transcript is momentarily unreadable
would not be caught by this observer; the passive statusline model readout is the backstop for that
narrow window.

On a positive detection it also appends an OPEN MAINTAINER ALERT block to the out-of-band watchdog
channel (grc_library_scratch/MAINTAINER_ALERT.md, read at every /orch resume) if that sibling is
present, deduped by marker-presence so it is written once per open incident. That channel clears by
REMOVAL (the maintainer removes the block and resets the Status line), so marker-presence is exactly
open-ness. Best-effort: a write failure never changes the block verdict.

Exit protocol (Claude Code hooks): exit 0 allows; on a blocking-capable event (PreToolUse) exit 2
blocks and feeds stderr to the model; on Stop the guard is NON-blocking (a turn-end alert must not
force continuation) and surfaces the alert via a stdout `systemMessage`.

Self-test: python3 .claude/hooks/block-opus5-orchestrator-model.py --self-test
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

MARKER = "opus5-orchestrator-model"


def is_opus5(model) -> bool:
    """True only for a positively-resolved Opus-5 id: `claude-opus-5` or `claude-opus-5-<x>`."""
    if not isinstance(model, str):
        return False
    m = model.strip().lower()
    return m == "claude-opus-5" or m.startswith("claude-opus-5-")


def model_from_transcript(tp) -> str | None:
    """The last GENUINE assistant model id (a concrete `claude-*`), or None on any failure."""
    if not tp:
        return None
    try:
        with open(tp, encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return None
    for ln in reversed(lines):
        try:
            obj = json.loads(ln)
        except Exception:
            continue
        if obj.get("type") != "assistant":
            continue
        msg = obj.get("message")
        if not isinstance(msg, dict):
            continue
        mod = msg.get("model")
        if isinstance(mod, str) and mod.startswith("claude-"):
            return mod
    return None


def resolve_model(payload) -> str | None:
    """Best-effort running-model id. Transcript is primary; a payload `model` is a secondary hint."""
    mod = model_from_transcript(payload.get("transcript_path"))
    if mod:
        return mod
    pm = payload.get("model")
    if isinstance(pm, dict):
        return pm.get("id")
    if isinstance(pm, str):
        return pm
    return None


def _alert_file() -> Path | None:
    try:
        scratch = Path(__file__).resolve().parents[2].parent / "grc_library_scratch"
        if scratch.is_dir():
            return scratch / "MAINTAINER_ALERT.md"
    except Exception:
        pass
    return None


def already_open(text: str) -> bool:
    """True if an alert for this marker is already present (dedup).

    This channel clears by REMOVAL: an OPEN alert is a `### ALERT` block PRESENT in the file, and the
    maintainer clears it by removing the block and resetting the Status line. There is no per-block
    resolution line, so marker-presence is exactly open-ness.
    """
    return MARKER in text


def write_alert(model: str) -> None:
    """Append an OPEN alert block (best-effort, deduped by marker-presence). Never raises."""
    try:
        f = _alert_file()
        if f is None:
            return
        text = f.read_text(encoding="utf-8") if f.exists() else ""
        if already_open(text):
            return
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        block = (
            f"\n### ALERT {ts} {MARKER}\n"
            f"The orchestrator session is running on model `{model}` (Opus 5). Per maintainer "
            f"directive (2026-08-21), orchestrator work is HALTED at the first tool call. Swap the "
            f"session to a better working model (e.g. Opus 4.8, `claude-opus-4-8`) and re-resume. "
            f"This channel clears by removal: once the model is swapped, remove this block and reset "
            f"the Status line above.\n"
        )
        with open(f, "a", encoding="utf-8") as fh:
            fh.write(block)
    except Exception:
        return


def _message(model: str) -> str:
    return (
        f"MAINTAINER ALERT (block-opus5): the orchestrator is running on `{model}` (Opus 5). "
        f"Per maintainer directive 2026-08-21, HALT IMMEDIATELY: do not run this tool or any further "
        f"orchestrator work. Tell the maintainer to swap the session to a better working model "
        f"(e.g. Opus 4.8 / claude-opus-4-8), then re-resume. An OPEN alert was written to "
        f"grc_library_scratch/MAINTAINER_ALERT.md if that sibling is present."
    )


def _self_test() -> int:
    checks = [
        ("opus5 bare", is_opus5("claude-opus-5") is True),
        ("opus5 dated", is_opus5("claude-opus-5-20260901") is True),
        ("opus5 1m", is_opus5("claude-opus-5-1m") is True),
        ("opus5 point", is_opus5("claude-opus-5-1") is True),
        ("opus5 upper", is_opus5("Claude-Opus-5") is True),
        ("opus48 no", is_opus5("claude-opus-4-8") is False),
        ("opus41 no", is_opus5("claude-opus-4-1-20250805") is False),
        ("opus50 no", is_opus5("claude-opus-50") is False),
        ("opus5x no", is_opus5("claude-opus-5x") is False),
        ("sonnet5 no", is_opus5("claude-sonnet-5") is False),
        ("none no", is_opus5(None) is False),
        ("empty no", is_opus5("") is False),
        ("synthetic no", is_opus5("<synthetic>") is False),
        ("open-present", already_open("a\n### ALERT x " + MARKER + "\nbody") is True),
        ("open-absent", already_open("nothing here") is False),
    ]
    bad = [n for n, ok in checks if not ok]
    if bad:
        print(f"block-opus5 self-test: FAIL {bad}")
        return 1
    print(f"block-opus5 self-test: OK ({len(checks)} checks)")
    return 0


def main() -> int:
    if "--self-test" in sys.argv:
        return _self_test()
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # no/bad payload -> fail OPEN
    try:
        model = resolve_model(payload)
    except Exception:
        return 0  # any error -> fail OPEN
    if not is_opus5(model):
        return 0  # not positively Opus 5 -> allow (fail OPEN on uncertainty)
    write_alert(model)
    if (payload.get("hook_event_name") or "") == "Stop":
        # Turn-end: surface the alert without forcing continuation.
        print(json.dumps({"systemMessage": _message(model)}))
        return 0
    # PreToolUse (blocking-capable): hard-block the tool.
    print(_message(model), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
