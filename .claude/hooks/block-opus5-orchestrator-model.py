#!/usr/bin/env python3
"""PreToolUse + Stop guard: HALT and MAINTAINER-ALERT when the orchestrator's OWN running model is Opus 5.

Maintainer-directed 2026-08-21: "add a validation so that if you ever start using OPUS 5, you stop
immediately and MAINTAINER ALERT so I can swap you to a better working model." The maintainer judges
Opus 5 a worse working model for this project than Opus 4.8 and wants a mechanical hard-stop the
moment a session (or a mid-session model swap) lands on Opus 5.

MAINTAINER-SCOPED: the Opus-5 ban is the maintainer's preference for THIS project, NOT a portable
adopter guard. The guard NO-OPS for an adopter (signal: the `grc_library_private` sibling is absent),
so an adopter who legitimately runs Opus 5 with Claude Code is never blocked by it.

SIGNAL: the running model id, read from the transcript's LAST real assistant entry
(payload["transcript_path"] -> message.model), the same surface surface-session-facts.py reads.
Injected `<synthetic>` entries (notifications, interrupts) are skipped so the guard reads the last
GENUINE model, WHATEVER it is (claude or not); is_opus5() then decides. A non-Opus-5 last model
(4.8, a differently-cased id, a non-claude id) yields ALLOW, never a search back to an older entry.

MATCH: a model id matching `claude-opus-5` or `claude-opus-5-<x>` (bare id, dated variants, the
`-1m` context variant). Does NOT match `claude-opus-4-8`, any 4.x, `claude-opus-50`, `claude-opus-5x`,
or a sonnet/haiku id.

FAIL-OPEN discipline (the contract, and the four fail-CLOSED gaps a codex verifier caught in the
first version, all closed here): the guard BLOCKS (exit 2) ONLY when it POSITIVELY resolves the
running model as Opus 5 in the maintainer environment. On ANY uncertainty it exits 0 (allow):
  * no payload / bad payload / any internal error;
  * no transcript_path, or an unreadable transcript;
  * a MALFORMED (unparseable) line at the tail of the transcript: the guard fails OPEN rather than
    searching PAST it to an older entry, because a partially-written current record after an
    Opus-5 -> good-model switch must never resurrect the stale Opus-5 and block the good session;
  * a last genuine model that is not a positive Opus-5 match (this is the whole point);
  * NO `payload.model` fallback: the transcript is the sole authority, so a missing transcript
    fails open instead of blocking on an unverified payload hint.
A fail-CLOSED path here would wedge a GOOD-model session, which is the worst outcome and the reason
the contract is fail-open. RESIDUE, stated not hidden: Opus 5 running while the transcript is
momentarily unreadable is not caught (backstopped by the passive statusline model readout); and the
alert-write dedup is a non-atomic read-then-append, so two concurrent Opus-5 sessions could each
append one alert block (a duplicate alert, harmless, accepted).

On a positive detection it also appends an OPEN MAINTAINER ALERT block to the out-of-band watchdog
channel (grc_library_scratch/MAINTAINER_ALERT.md, read at every /orch resume) if that sibling is
present, deduped by marker-presence (the channel clears by REMOVAL). Best-effort: a write failure
never changes the block verdict.

Exit protocol: exit 0 allows. Only a PreToolUse event blocks (exit 2, reason on stderr). Every other
event, Stop or an unknown/malformed label, is NON-blocking (a stdout `systemMessage`), so a turn-end
(or a mislabelled event) never forces continuation.

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
    """The LAST genuine assistant model id (any non-`<synthetic>` model string), or None.

    Returns None (fail OPEN) on: no path, an unreadable file, OR a MALFORMED line reached before any
    genuine model (never search PAST an unparseable tail record to an older model, which would risk
    resurrecting a stale Opus-5 after a good-model switch). Skips injected `<synthetic>`/empty models.
    Returns the model string AS-IS (claude or not); is_opus5() does the classification, so a
    non-claude or differently-cased current model naturally yields ALLOW rather than a fail-closed
    fallback.
    """
    if not tp:
        return None
    try:
        with open(tp, encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return None
    for ln in reversed(lines):
        s = ln.strip()
        if not s:
            continue
        try:
            obj = json.loads(s)
        except Exception:
            # A non-empty, unparseable line (e.g. a partially-written current record): fail OPEN
            # rather than falling back to an older entry.
            return None
        if obj.get("type") != "assistant":
            continue
        msg = obj.get("message")
        if not isinstance(msg, dict):
            continue
        mod = msg.get("model")
        if not isinstance(mod, str) or not mod or mod == "<synthetic>":
            continue  # injected/synthetic: skip to the previous genuine entry
        return mod  # the current real model, whatever it is
    return None


def resolve_model(payload) -> str | None:
    """Running-model id from the transcript ONLY (the authoritative source). No payload fallback:
    a missing/unreadable transcript fails OPEN (returns None), per the fail-open contract."""
    return model_from_transcript(payload.get("transcript_path"))


def _maintainer_env() -> bool:
    """True only in the maintainer's environment (the `grc_library_private` sibling is present).
    Adopters lack `_private`, so the maintainer-specific Opus-5 ban no-ops for them."""
    try:
        return (Path(__file__).resolve().parents[2].parent / "grc_library_private").is_dir()
    except Exception:
        return False


def _alert_file() -> "Path | None":
    try:
        scratch = Path(__file__).resolve().parents[2].parent / "grc_library_scratch"
        if scratch.is_dir():
            return scratch / "MAINTAINER_ALERT.md"
    except Exception:
        pass
    return None


def already_open(text: str) -> bool:
    """True if an alert for this marker is already present (dedup by marker-presence; the channel
    clears by REMOVAL, so marker-presence is exactly open-ness)."""
    return MARKER in text


def write_alert(model: str) -> None:
    """Append an OPEN alert block (best-effort, deduped by marker-presence). Never raises.

    The read-then-append is deliberately non-atomic: two concurrent Opus-5 sessions could each see no
    marker and append, yielding a duplicate alert block. That is harmless (the maintainer still sees
    the alert) and concurrent Opus-5 orchestrator sessions are near-impossible, so it is accepted."""
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
        ("opus48 cased no", is_opus5("Claude-Opus-4-8") is False),
        ("opus41 no", is_opus5("claude-opus-4-1-20250805") is False),
        ("opus50 no", is_opus5("claude-opus-50") is False),
        ("opus5x no", is_opus5("claude-opus-5x") is False),
        ("sonnet5 no", is_opus5("claude-sonnet-5") is False),
        ("gpt no", is_opus5("gpt-5") is False),
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
    if not _maintainer_env():
        return 0  # adopter: the Opus-5 ban is the maintainer's preference, not portable -> allow
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
    if (payload.get("hook_event_name") or "") == "PreToolUse":
        # PreToolUse (blocking-capable): hard-block the tool.
        print(_message(model), file=sys.stderr)
        return 2
    # Stop, or any other/unknown/malformed event label: non-blocking, surface the alert only.
    print(json.dumps({"systemMessage": _message(model)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
