#!/usr/bin/env python3
"""Advisory worker-saturation report for the credit-offload fleet: makes IDLE
CAPACITY observable, so the orchestrator notices when live workers sit idle
with no queued work to claim.

WHY THIS EXISTS. Under credit-offload, workers poll the scratch queue and claim
one order at a time. The failure this surfaces is silent: the pending queue
drains to zero while workers are alive and offloadable work still exists, so the
fleet stops offloading without anything saying so (the class the maintainer alert
2026-07-19-a idle-liveness fix addressed from the worker side; this is the
orchestrator-side observable). This tool answers, from the record, "are the live
workers saturated with work, or is there idle capacity right now?"

WHAT THIS IS (and is NOT). This is an orchestrator dev-aid, not an audit gate. It
reads the SIBLING repository ``grc_library_scratch`` (the worker liveness registry
``workers/<id>.md`` and the work queue ``queue/<id>.md``). Neither repository's CI
can see the other, so no CI gate can check it; the check is orchestrator-side by
design. It is named ``audit-*`` (not ``lint-*``) so the gate machinery (the
four-surface parity gate, the regression suite) does NOT auto-discover it, and it
is NOT wired into ``run_all_audits.sh`` / ``quality.yml`` /
``.pre-commit-config.yaml``. It ALWAYS exits 0 (its verdict is advisory context
for the orchestrator, never a workflow failure); wiring it as a blocking gate
would be a decorative gate (gate-discipline rule), because the scratch checkout is
not guaranteed present in every environment. When the scratch checkout is absent
it says so and exits 0 (an advisory tool must not manufacture a result from
missing input). Its self-test lives behind ``--self-test``.

THE LIVENESS DEFINITION IS MIRRORED, NOT INVENTED. A worker is LIVE on exactly the
same definition ``grc_library_scratch/tools/credit-offload-queue.py`` uses for its
``list-workers`` ``[LIVE]`` marker: ``status`` is ``active`` AND ``last_seen`` is
within the staleness window ``STALE_MINUTES`` (20). The field-line format
(``- **key:** value``), the timestamp format (``%Y-%m-%dT%H:%M:%SZ``), and the
1e9-minutes-on-unparseable-stamp behaviour are mirrored from that helper so the two
tools never disagree on who is live. See the constants below.

VERDICTS.
  NO-WORKERS     : 0 live workers, so there is nothing to offload to.
  SATURATED      : outstanding orders >= live workers, so every live worker has
                   or will have work to claim.
  IDLE-CAPACITY  : live workers > outstanding orders, so at least one live worker
                   has nothing to claim right now (the observable this tool exists
                   to raise).
"outstanding orders" = pending (unclaimed) plus claimed/in-progress (not yet
``done``).

USAGE
  python3 tools/audit-worker-saturation.py [--scratch PATH]
      Multi-line report: live-worker count, pending/claimed/outstanding counts,
      the idle-capacity count, and the verdict.
  python3 tools/audit-worker-saturation.py --oneline [--scratch PATH]
      One-line statusline form, e.g.
      ``workers: 2 live / 1 pending / 0 claimed [IDLE-CAPACITY]``.
  python3 tools/audit-worker-saturation.py --self-test
      In-memory fixture scenarios against the verdict logic; PASS/FAIL per case.

The scratch checkout is located by ``--scratch``, else the ``GRC_SCRATCH_PATH``
environment variable, else the sibling directory ``../grc_library_scratch``
relative to this repository's root.
"""

from __future__ import annotations

import argparse
import datetime
import os
import re
import sys
from pathlib import Path

from lint_common import resolve_sibling, sibling_placeholder_present

REPO_ROOT = Path(__file__).resolve().parent.parent

# Mirrored verbatim from grc_library_scratch/tools/credit-offload-queue.py so the
# two tools share one liveness definition (do not diverge these):
#   STALE_MINUTES = 20
#   FIELD_RE = re.compile(r"^- \*\*(\w+):\*\* (.*)$")
#   a stamp is "%Y-%m-%dT%H:%M:%SZ"; an unparseable stamp reads as 1e9 minutes old
#   list-workers LIVE test: fields["status"] == "active" and age <= STALE_MINUTES
STALE_MINUTES = 20
FIELD_RE = re.compile(r"^- \*\*(\w+):\*\* (.*)$")


def find_scratch(cli_path):
    """Resolve the scratch checkout, or None. An EXPLICITLY named path
    (--scratch / GRC_SCRATCH_PATH) that does not resolve is reported and NOT
    silently replaced by the sibling default (an explicit wrong path is a mistake
    to surface, not to paper over), matching the two sibling advisory tools."""
    for label, cand in (("--scratch", cli_path),
                        ("GRC_SCRATCH_PATH", os.environ.get("GRC_SCRATCH_PATH"))):
        if cand:
            if Path(cand).is_dir() and (Path(cand) / "workers").is_dir():
                return Path(cand)
            print(f"advisory: {label}={cand} is not a scratch checkout with a "
                  "workers/ registry; not falling back to any other location; "
                  "nothing to report.")
            sys.exit(0)
    # Default: the real grc_library_scratch sibling, via the shared resolver.
    # None on a portable clone with no scratch sibling.
    default = resolve_sibling("scratch")
    if default is not None and (default / "workers").is_dir():
        return default
    return None


def parse_fields(text):
    """Parse the ``- **key:** value`` field lines from a worker/order file's TEXT
    (mirrors credit-offload-queue.py read_fields_text)."""
    fields = {}
    for line in text.splitlines():
        m = FIELD_RE.match(line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields


def parse_age_minutes(stamp):
    """Age of a UTC stamp in minutes; 1e9 when the stamp is missing or malformed
    (so an unparseable stamp reads as very old, i.e. NOT live), mirroring the queue
    helper exactly."""
    try:
        t = datetime.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=datetime.timezone.utc)
    except ValueError:
        return 1e9
    delta = datetime.datetime.now(datetime.timezone.utc) - t
    return delta.total_seconds() / 60.0


def worker_is_live(fields, stale_minutes=STALE_MINUTES):
    """The list-workers [LIVE] test: status active AND last_seen within the window."""
    return (fields.get("status") == "active"
            and parse_age_minutes(fields.get("last_seen", "")) <= stale_minutes)


def verdict(live, pending, claimed):
    """The saturation verdict. outstanding = pending + claimed.
    NO-WORKERS when no live worker; SATURATED when outstanding >= live (every live
    worker has or will have work); else IDLE-CAPACITY (live > outstanding)."""
    outstanding = pending + claimed
    if live == 0:
        return "NO-WORKERS"
    if outstanding >= live:
        return "SATURATED"
    return "IDLE-CAPACITY"


def survey(scratch):
    """Count live workers and outstanding orders from the scratch checkout.

    Returns (live, pending, claimed, other, other_statuses) where `other` counts
    order files whose status is neither pending/claimed nor done (surfaced rather
    than silently dropped), and `other_statuses` maps each such status to its
    count."""
    live = 0
    workers_dir = scratch / "workers"
    for p in sorted(workers_dir.glob("*.md")):
        if p.name == "README.md":
            continue
        if worker_is_live(parse_fields(p.read_text(encoding="utf-8", errors="replace"))):
            live += 1

    pending = claimed = other = 0
    other_statuses = {}
    queue_dir = scratch / "queue"
    if queue_dir.is_dir():
        for p in sorted(queue_dir.glob("*.md")):
            if p.name == "README.md":
                continue
            status = parse_fields(
                p.read_text(encoding="utf-8", errors="replace")).get("status", "")
            if status == "pending":
                pending += 1
            elif status == "claimed":
                claimed += 1
            elif status == "done":
                pass  # consumed, not outstanding
            else:
                other += 1
                other_statuses[status] = other_statuses.get(status, 0) + 1
    return live, pending, claimed, other, other_statuses


def oneline(live, pending, claimed):
    """The statusline form."""
    v = verdict(live, pending, claimed)
    return (f"workers: {live} live / {pending} pending / {claimed} claimed "
            f"[{v}]")


def run_report(scratch, one):
    live, pending, claimed, other, other_statuses = survey(scratch)
    if one:
        print(oneline(live, pending, claimed))
        return
    outstanding = pending + claimed
    v = verdict(live, pending, claimed)
    idle = max(0, live - outstanding)
    print(oneline(live, pending, claimed))
    print(f"live workers:      {live}")
    print(f"outstanding orders: {outstanding} ({pending} pending + {claimed} claimed)")
    print(f"idle capacity:     {idle} live worker(s) with nothing to claim")
    print(f"verdict:           {v}")
    if v == "IDLE-CAPACITY":
        print("  IDLE-CAPACITY: at least one live worker has no order to claim. "
              "If offloadable backlog exists, enqueue it so the idle worker(s) "
              "pick it up; otherwise the fleet is idle by design.")
    elif v == "NO-WORKERS":
        print("  NO-WORKERS: no live worker to offload to (register or wake a "
              "worker before enqueuing offload work).")
    if other:
        shown = ", ".join(f"{k or '(blank)'}={n}" for k, n in sorted(other_statuses.items()))
        print(f"note: {other} order file(s) carry a status that is neither "
              f"pending/claimed nor done ({shown}); not counted as outstanding, "
              "surfaced for triage.")


def self_test():
    """In-memory fixture scenarios against the verdict logic; PASS/FAIL per case,
    exit non-zero only if a case fails."""
    # (name, live, pending, claimed, expected verdict)
    cases = [
        ("IDLE-CAPACITY: 3 live, 1 pending, 0 claimed", 3, 1, 0, "IDLE-CAPACITY"),
        ("IDLE-CAPACITY: 2 live, 0 pending, 0 claimed", 2, 0, 0, "IDLE-CAPACITY"),
        ("SATURATED: 2 live, 2 pending, 0 claimed", 2, 2, 0, "SATURATED"),
        ("SATURATED: 2 live, 0 pending, 3 claimed", 2, 0, 3, "SATURATED"),
        ("NO-WORKERS: 0 live, 5 pending, 0 claimed", 0, 5, 0, "NO-WORKERS"),
        ("BOUNDARY SATURATED: 2 live, 1 pending, 1 claimed (outstanding 2 == live 2)",
         2, 1, 1, "SATURATED"),
        # extra guards on the boundary and the NO-WORKERS-wins precedence:
        ("IDLE boundary: 3 live, 1 pending, 1 claimed (outstanding 2 < live 3)",
         3, 1, 1, "IDLE-CAPACITY"),
        ("NO-WORKERS wins even with 0 outstanding: 0 live, 0 pending, 0 claimed",
         0, 0, 0, "NO-WORKERS"),
    ]
    failures = 0
    for name, live, pending, claimed, expected in cases:
        got = verdict(live, pending, claimed)
        ok = got == expected
        failures += 0 if ok else 1
        print(f"  {'PASS' if ok else 'FAIL'}: {name} -> {got}"
              + ("" if ok else f" (expected {expected})"))

    # liveness-parse guards (the [LIVE] definition), using an in-memory recent and
    # old stamp so the test is deterministic without touching the clock directly.
    now = datetime.datetime.now(datetime.timezone.utc)
    recent = (now - datetime.timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    old = (now - datetime.timedelta(minutes=STALE_MINUTES + 5)).strftime("%Y-%m-%dT%H:%M:%SZ")
    live_cases = [
        ("active + recent = live", {"status": "active", "last_seen": recent}, True),
        ("active + old = not live", {"status": "active", "last_seen": old}, False),
        ("checked-out + recent = not live",
         {"status": "checked-out", "last_seen": recent}, False),
        ("active + malformed stamp = not live",
         {"status": "active", "last_seen": "not-a-timestamp"}, False),
    ]
    for name, fields, expected in live_cases:
        got = worker_is_live(fields)
        ok = got == expected
        failures += 0 if ok else 1
        print(f"  {'PASS' if ok else 'FAIL'}: liveness, {name} -> {got}"
              + ("" if ok else f" (expected {expected})"))

    total = len(cases) + len(live_cases)
    print(f"\nself-test: {total - failures}/{total} passed")
    return 0 if failures == 0 else 1


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--scratch", help="path to the grc_library_scratch checkout")
    ap.add_argument("--oneline", action="store_true",
                    help="print the one-line statusline form only")
    ap.add_argument("--self-test", action="store_true",
                    help="run the inline verdict/liveness self-test and exit")
    args = ap.parse_args(argv[1:])

    if args.self_test:
        return self_test()

    scratch = find_scratch(args.scratch)
    if scratch is None:
        if sibling_placeholder_present("scratch"):
            print("advisory: grc_library_scratch sibling absent (portable clone; "
                  ".scratch placeholder present); maintainer-only advisory, "
                  "nothing to report.")
        else:
            print("advisory: no scratch checkout found (no --scratch or "
                  "GRC_SCRATCH_PATH given, and no sibling grc_library_scratch "
                  "directory with a workers/ registry); nothing to report.")
        return 0

    run_report(scratch, args.oneline)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
