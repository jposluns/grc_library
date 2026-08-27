#!/usr/bin/env python3
"""Stop hook: when the assistant's last message discusses 'session' and 'depth' in
proximity, surface the FACTUAL session length and compaction count, not inference.

Maintainer-directed 2026-08-15: "add a hook when you use the term 'session' and 'depth'
within a few words or in the same sentence to include the session length and number of
compactions, so i can see facts, not inference." The orchestrator had repeatedly asserted
"session depth"/"deep session" as an un-instrumented inference (the evidence-grounded-
completion un-observable-state failure); this replaces the felt inference with the two
externally-observable numbers the maintainer actually tracks.

NON-BLOCKING: emits the facts via the hook `systemMessage` field (shown to the maintainer),
never blocks turn-end. FAIL OPEN on any error, a personal instrument must never trap the run.
MAINTAINER-ORCHESTRATOR-ONLY: reads degradation-watch-log.md from the operational store (via lint_common.resolve_working); if that is
absent (adopter, or the operational store not present) it is a silent no-op.

Fact sources (the maintainer's own metric log):
  * session length  = now minus the newest `session-start` ISO timestamp.
  * compaction count = canonical `| <iso> | compaction |` rows with ts >= session-start.
"""
import sys, os, re, json
from pathlib import Path
from datetime import datetime, timezone
ISO = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?Z)"  # seconds OPTIONAL: the degradation log's dominant form is minute-only (handoff-snapshot.py:211)


def _fail_open():
    sys.exit(0)


def _parse(ts):
    # Accept BOTH minute-only (the log's dominant form) and full-seconds ISO stamps.
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%MZ"):
        try:
            return datetime.strptime(ts, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    raise ValueError(f"unparseable timestamp: {ts!r}")


def _last_assistant_text(transcript_path):
    try:
        with open(transcript_path, encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return ""
    for ln in reversed(lines):
        try:
            obj = json.loads(ln)
        except Exception:
            continue
        if obj.get("type") == "assistant":
            parts = obj.get("message", {}).get("content", [])
            return " ".join(
                p.get("text", "")
                for p in parts
                if isinstance(p, dict) and p.get("type") == "text"
            )
    return ""


def _has_pair(text):
    # primary: any sentence containing both 'session' and 'depth' (word-boundary, ci)
    for sent in re.split(r"[.!?\n]+", text):
        low = sent.lower()
        if re.search(r"\bsession", low) and re.search(r"\bdepth", low):
            return True
    # fallback: the two tokens within ~45 chars ("within a few words")
    low = text.lower()
    for m in re.finditer(r"\bsession", low):
        if "depth" in low[m.start(): m.start() + 45]:
            return True
    for m in re.finditer(r"\bdepth", low):
        if "session" in low[max(0, m.start() - 45): m.start()]:
            return True
    return False


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        _fail_open()
    tp = payload.get("transcript_path")
    if not tp or not os.path.exists(tp):
        _fail_open()
    text = _last_assistant_text(tp)
    if not text or not _has_pair(text):
        _fail_open()
    repo = Path(os.environ.get("CLAUDE_PROJECT_DIR", "/home/grc/grc_library")).resolve()
    try:
        sys.path.insert(0, str(repo / "tools"))
        from lint_common import resolve_working
        log_path = resolve_working("degradation-watch-log.md", repo_root=repo)
    except Exception:
        _fail_open()
    if log_path is None or not log_path.exists():
        _fail_open()
    try:
        content = log_path.read_text(encoding="utf-8")
    except Exception:
        _fail_open()
    # STRICT session-start detection: match only the type-token forms, never a prose
    # mention of "session-start" inside another row (e.g. a compaction row's note).
    #   table form: | <iso> | session-start | ...   (iso before the token)
    #   plain form: session-start <iso> ...          (iso after the token)
    starts = []
    for ln in content.splitlines():
        m = re.match(r"\|\s*" + ISO + r"\s*\|\s*session-start\b", ln)
        if not m:
            m = re.match(r"\s*session-start\s+" + ISO, ln)
        if m:
            starts.append(m.group(1))
    if not starts:
        _fail_open()
    start_ts = max(starts, key=_parse)
    start_dt = _parse(start_ts)
    now = datetime.now(timezone.utc)
    secs = (now - start_dt).total_seconds()
    h, mm = int(secs // 3600), int((secs % 3600) // 60)
    comp = 0
    for ln in content.splitlines():
        m = re.match(r"\|\s*" + ISO + r"\s*\|\s*compaction\s*\|", ln)
        if m and _parse(m.group(1)) >= start_dt:
            comp += 1
    facts = (
        f"SESSION FACTS (not inference): length {h}h{mm:02d}m "
        f"(session-start {start_ts} UTC); compactions this session: {comp}. "
        f"Hold any session-depth / length / degradation claim against these numbers."
    )
    print(json.dumps({"systemMessage": facts}))
    sys.exit(0)


def _self_test():
    # Reality fixture (guard-input discipline): the degradation log's dominant form is
    # MINUTE-ONLY; the pre-fix regex/_parse silently missed it. Assert both forms parse and
    # that the minute-only start is selected as newest, mirroring handoff-snapshot.py's fixture.
    assert _parse("2026-08-27T15:30Z").minute == 30          # minute-only parses
    assert _parse("2026-07-29T12:00:00Z").second == 0        # full-seconds still parses
    fixture = (
        "| 2026-07-29T10:00:00Z | session-start | earlier full-seconds |\n"
        "| 2026-07-29T15:30Z | session-start | latest, MINUTES-ONLY (dominant form) |\n"
        "| 2026-07-29T13:00Z | compaction | C1 |\n"
    )
    starts = []
    for ln in fixture.splitlines():
        m = re.match(r"\|\s*" + ISO + r"\s*\|\s*session-start\b", ln)
        if m:
            starts.append(m.group(1))
    assert starts == ["2026-07-29T10:00:00Z", "2026-07-29T15:30Z"], starts
    assert max(starts, key=_parse) == "2026-07-29T15:30Z"    # minute-only selected as newest
    comp = sum(1 for ln in fixture.splitlines()
               if re.match(r"\|\s*" + ISO + r"\s*\|\s*compaction\s*\|", ln))
    assert comp == 1, comp                                    # minute-only compaction row counted
    print("surface-session-facts self-test: 5 assertions PASS (minute-only + full-seconds)")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        _self_test()
        sys.exit(0)
    try:
        main()
    except Exception:
        _fail_open()
