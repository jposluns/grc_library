#!/usr/bin/env python3
"""Advisory activity-timing report: session wall-clock split into active vs orchestrator idle/wait.

WHY THIS EXISTS. The maintainer asked (2026-07-31) for the DURATION of every activity recorded
comprehensively and NEVER sampled, because hand-tracking inevitably misses spans. The mechanical,
never-sample source for the ORCHESTRATOR half is the session transcript: every record carries an
ISO `timestamp`, so the wall-clock timeline is measured, not estimated. This tool derives from that
timeline the total session span, the count of assistant turns, and the orchestrator's IDLE/WAIT
spans (the gaps where it dispatched a worker or a CI run and waited on a notification, doing nothing).

WHAT THIS DOES and does NOT cover. This is the mechanical BASELINE: total span, per-turn count, and
idle/wait spans, all measured from timestamps. It deliberately does NOT segment the active time into
per-ACTIVITY buckets (PR build vs edit pass vs dispatch vs consume vs bookkeeping): the transcript
does not label activities, so per-activity segmentation needs either lightweight boundary markers the
orchestrator emits or a classifier, which is a design decision surfaced for the maintainer (P-1.11
follow-up), not guessed here. WORKER durations are measured separately by exec-dispatch (`dur=`),
kept in their own column per the measured-vs-estimated discipline; joining them is a follow-up.

Advisory only: every reporting path exits 0. Only `--self-test` can exit non-zero. Environment
dependent by nature (the transcript lives under the harness's own state directory), so an absent
transcript is reported as absent rather than counted as zero, the same no-op-loudly shape as
`audit-token-spend.py` and `audit-delivery-status.py`.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path

# The harness's per-project transcript directory, derived from the repo path the way the harness
# derives it (absolute path, separators AND underscores to hyphens), never hardcoded, so it follows
# a checkout that moves on disk. Same derivation as audit-token-spend.py's transcript_dir_for.
TRANSCRIPT_HOME = Path.home() / ".claude" / "projects"

# A gap between two consecutive timestamped records longer than this is counted as an orchestrator
# IDLE/WAIT span (waiting on a worker delivery or a CI run), not active work. 120s is chosen so a
# normal think-and-act turn is "active" while a worker/CI wait (minutes) is "idle". Tunable.
DEFAULT_IDLE_THRESHOLD_S = 120


def transcript_dir_for(repo_root: Path) -> Path:
    """The harness transcript directory for a repo path. Observer.

    The harness names it after the absolute repo path with BOTH path separators and underscores
    replaced by hyphens, so `/home/grc/grc_library` becomes `-home-grc-grc-library`.
    """
    return TRANSCRIPT_HOME / str(repo_root.resolve()).replace("/", "-").replace("_", "-")


def parse_iso(ts: str):
    """PURE. An ISO-8601 `...Z` timestamp as an aware datetime, or None when unparseable.

    Returns None rather than raising, so one malformed record cannot abort the whole read (the
    transcript is appended to live, so the last line can be half-written at read time).
    """
    if not isinstance(ts, str) or not ts:
        return None
    s = ts.replace("Z", "+00:00")
    try:
        d = _dt.datetime.fromisoformat(s)
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=_dt.timezone.utc)


def read_timeline(text: str):
    """PURE. The sorted list of (datetime, record_type) for every timestamped record in a transcript.

    Takes the transcript TEXT (not a path) so it is testable on inline fixtures. Tolerates torn or
    non-JSON lines (a live-append artefact) by skipping them; the count of skipped lines is not the
    caller's concern here (this is wall-clock, not a completeness audit).
    """
    events = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except (ValueError, TypeError):
            continue
        if not isinstance(record, dict):
            continue
        when = parse_iso(record.get("timestamp"))
        if when is None:
            continue
        events.append((when, record.get("type", "?")))
    events.sort(key=lambda e: e[0])
    return events


def compute_timing(events, idle_threshold_s: int = DEFAULT_IDLE_THRESHOLD_S) -> dict:
    """PURE. Session span, turn count, and idle/wait spans from a sorted (datetime, type) timeline.

    total_s   = last timestamp minus first (the whole session wall-clock).
    idle_s    = the summed length of every inter-record gap longer than idle_threshold_s (the
                orchestrator waiting on a worker or CI, doing nothing).
    active_s  = total_s minus idle_s (a measured residual, NOT a per-activity sum).
    turns     = the number of `assistant` records (one per orchestrator turn).
    idle_spans = the individual long gaps as (seconds, type_of_the_record_that_FOLLOWED_the_gap),
                sorted longest-first, so the biggest waits are visible.

    Returns zeros for an empty timeline rather than raising, so an absent/empty transcript is a
    clean no-op.
    """
    if not events:
        return {"total_s": 0, "active_s": 0, "idle_s": 0, "turns": 0, "records": 0,
                "idle_spans": [], "first": None, "last": None}
    first, last = events[0][0], events[-1][0]
    total_s = (last - first).total_seconds()
    idle_s = 0.0
    idle_spans = []
    for (t0, _ty0), (t1, ty1) in zip(events, events[1:]):
        gap = (t1 - t0).total_seconds()
        if gap > idle_threshold_s:
            idle_s += gap
            idle_spans.append((round(gap, 1), ty1))
    idle_spans.sort(reverse=True)
    turns = sum(1 for _when, ty in events if ty == "assistant")
    return {"total_s": round(total_s, 1), "active_s": round(total_s - idle_s, 1),
            "idle_s": round(idle_s, 1), "turns": turns, "records": len(events),
            "idle_spans": idle_spans, "first": first, "last": last}


def fmt_dur(seconds) -> str:
    """PURE. Seconds as `HhMMmSSs` / `MMmSSs` / `SSs`, for a human reading the report."""
    s = int(round(seconds or 0))
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if h:
        return f"{h}h{m:02d}m{sec:02d}s"
    if m:
        return f"{m}m{sec:02d}s"
    return f"{sec}s"


def report(repo_root: Path, session: str | None, idle_threshold_s: int, oneline: bool) -> int:
    tdir = transcript_dir_for(repo_root)
    transcripts = []
    if tdir.is_dir():
        transcripts = sorted(tdir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    if session:
        transcripts = [p for p in transcripts if session in p.stem]
    if not transcripts:
        print(f"activity-timing: no transcript found under {tdir}")
        print("  Reported as absent rather than zero (the transcript lives in the harness's own")
        print("  state directory, so a different machine or harness legitimately has none here).")
        return 0
    try:
        text = transcripts[0].read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"activity-timing: could not read {transcripts[0].name}: {exc}")
        return 0
    t = compute_timing(read_timeline(text), idle_threshold_s)

    if oneline:
        print(f"timing: total {fmt_dur(t['total_s'])} | active {fmt_dur(t['active_s'])} | "
              f"idle {fmt_dur(t['idle_s'])} over {t['turns']} turns "
              f"({len(t['idle_spans'])} waits > {idle_threshold_s}s)")
        return 0

    print("activity-timing report (advisory, MEASURED from transcript timestamps, never sampled)")
    print()
    print(f"  transcript:           {transcripts[0].name}")
    if t["first"]:
        print(f"  session span:         {t['first'].isoformat()} .. {t['last'].isoformat()}")
    print(f"  total wall-clock:     {fmt_dur(t['total_s']):>12}")
    print(f"  active (residual):    {fmt_dur(t['active_s']):>12}  (total minus idle; NOT a per-activity sum)")
    print(f"  orchestrator idle:    {fmt_dur(t['idle_s']):>12}  (gaps > {idle_threshold_s}s, i.e. worker/CI waits)")
    print(f"  assistant turns:      {t['turns']:>12,}")
    print(f"  timestamped records:  {t['records']:>12,}")
    if t["idle_spans"]:
        print()
        print(f"  longest idle/wait spans (the record type AFTER each gap):")
        for gap_s, after in t["idle_spans"][:8]:
            print(f"    {fmt_dur(gap_s):>10}  waited, then a {after!r} record")
    print()
    print("  This is the MECHANICAL BASELINE. Per-ACTIVITY segmentation (PR build vs edit vs dispatch")
    print("  vs consume vs bookkeeping) needs boundary markers or a classifier and is a design")
    print("  decision surfaced for the maintainer (P-1.11 follow-up). Worker durations are measured")
    print("  separately by exec-dispatch (dur=) and kept in their own column, never summed with these.")
    return 0


def self_test() -> int:
    failures = []
    total = 0

    def check(name, got, want):
        nonlocal total
        total += 1
        if got != want:
            failures.append(name)
            print(f"  FAIL: {name} -> {got!r}, expected {want!r}")
        else:
            print(f"  PASS: {name}")

    # parse_iso
    check("parse_iso: a Z timestamp parses to aware UTC",
          parse_iso("2026-08-01T02:22:11.818Z").isoformat(), "2026-08-01T02:22:11.818000+00:00")
    check("parse_iso: an empty string is None, not an error", parse_iso(""), None)
    check("parse_iso: a non-timestamp is None", parse_iso("not a time"), None)

    # read_timeline: sorts, skips torn/non-timestamped lines
    fixture = "\n".join([
        json.dumps({"type": "assistant", "timestamp": "2026-08-01T00:00:30Z"}),
        json.dumps({"type": "user", "timestamp": "2026-08-01T00:00:00Z"}),
        '{"type": "assistant", "timestamp": "2026-08-01T00:0',  # torn line
        json.dumps({"type": "system"}),                          # no timestamp
        json.dumps({"type": "assistant", "timestamp": "2026-08-01T00:05:00Z"}),
    ])
    tl = read_timeline(fixture)
    check("read_timeline: keeps only timestamped, well-formed records", len(tl), 3)
    check("read_timeline: sorts ascending by time",
          [ty for _w, ty in tl], ["user", "assistant", "assistant"])

    # compute_timing: total, idle (a gap > threshold), turns
    events = read_timeline(fixture)
    t = compute_timing(events, idle_threshold_s=120)
    check("compute_timing: total span is last minus first", t["total_s"], 300.0)
    # gaps: 30s (user->assistant, not idle), 270s (assistant->assistant, > 120s idle)
    check("compute_timing: idle sums only gaps over the threshold", t["idle_s"], 270.0)
    check("compute_timing: active is total minus idle", t["active_s"], 30.0)
    check("compute_timing: turns counts assistant records", t["turns"], 2)
    check("compute_timing: one idle span recorded, tagged by the following record",
          t["idle_spans"], [(270.0, "assistant")])
    check("compute_timing: an empty timeline is a clean zero, not an error",
          compute_timing([])["total_s"], 0)

    # fmt_dur
    check("fmt_dur: seconds only", fmt_dur(45), "45s")
    check("fmt_dur: minutes and seconds", fmt_dur(125), "2m05s")
    check("fmt_dur: hours, minutes, seconds", fmt_dur(3725), "1h02m05s")

    print()
    print(f"self-test: {total - len(failures)}/{total} passed")
    return 1 if failures else 0


def main(argv) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default=os.environ.get("GRC_REPO", str(Path(__file__).resolve().parents[1])),
                    help="repo root whose transcript directory to read")
    ap.add_argument("--session", help="substring of a session id; defaults to the most recent")
    ap.add_argument("--idle-threshold", type=int, default=DEFAULT_IDLE_THRESHOLD_S,
                    help=f"gap seconds counted as idle/wait (default {DEFAULT_IDLE_THRESHOLD_S})")
    ap.add_argument("--oneline", action="store_true", help="one-line form for a statusline")
    ap.add_argument("--self-test", action="store_true", help="run the fixture set")
    a = ap.parse_args(argv[1:])
    if a.self_test:
        return self_test()
    return report(Path(a.repo), a.session, a.idle_threshold, a.oneline)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
