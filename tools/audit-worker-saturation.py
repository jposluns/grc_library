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
reads BOTH exchange planes and reports their de-duplicated union: the SIBLING
repository ``grc_library_scratch`` (the worker liveness registry ``workers/<id>.md``
and the work queue ``queue/<id>.md``), AND the same-VM file-drop exchange root
(``$GRC_WORKING``, default ``/home/grc/grc_working``: per-family ``available-work``
and per-worker ``heartbeat`` files). Reading only the git-scratch plane was a real
defect, fixed 2026-07-25: once workers moved to the file-drop transport as primary,
this tool reported ``NO-WORKERS`` while a worker was demonstrably live, and
``NO-WORKERS`` is precisely the verdict that licenses self-running work under the
mandatory-offload discipline, so a false one actively defeated the discipline it
exists to serve. Neither repository's CI can see the other, so no CI gate can check
it; the check is orchestrator-side by design. It is named ``audit-*`` (not ``lint-*``) so the gate machinery (the
four-surface parity gate, the regression suite) does NOT auto-discover it, and it
is NOT wired into ``run_all_audits.sh`` / ``quality.yml`` /
``.pre-commit-config.yaml``. Every REPORTING path exits 0 (its verdict is advisory context
for the orchestrator, never a workflow failure); wiring it as a blocking gate
would be a decorative gate (gate-discipline rule), because the scratch checkout is
not guaranteed present in every environment. It proceeds when EITHER plane resolves, naming
any missing one in a ``note:`` line, and only reports that it has nothing to say
when BOTH are absent (an advisory tool must not manufacture a result from missing
input). An UNREADABLE directory is reported, never counted as empty: the file-drop
subtrees are group-owned, so a permissions failure would otherwise reproduce the
exact silent-zero defect described above. Its self-test lives behind ``--self-test``, which is the ONE non-zero exit path: it returns 1 on a self-test failure, deliberately, because a self-test that passed silently while failing would be worthless. Nothing in the reporting modes can fail the caller.

BOTH LIVENESS DEFINITIONS ARE MIRRORED, NOT INVENTED, and they DIFFER by plane.
Each is copied from the helper that owns its plane, so this tool never disagrees
with either on who is live. On the GIT-SCRATCH plane, per
``grc_library_scratch/tools/credit-offload-queue.py`` and its ``list-workers``
``[LIVE]`` marker: ``status`` is ``active`` AND ``last_seen`` is within
``STALE_MINUTES`` (20). The field-line format (``- **key:** value``), the timestamp
format (``%Y-%m-%dT%H:%M:%SZ``), and the 1e9-minutes-on-unparseable-stamp behaviour
are mirrored from that helper. On the FILE-DROP plane, per
``credit-offload-filedrop.py`` and its own ``list-workers``: liveness is the
heartbeat FILE's mtime age within the same 20-minute window, the file NAME is the
worker id, and there is NO ``status`` field, so there is no "active" half to test.
A worker id present on both planes is counted ONCE. See the two constants blocks
below, each annotated with the helper it mirrors.

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
import collections
import datetime
import os
import re
import sys
import tempfile
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

# Mirrored verbatim from grc_library_scratch/tools/credit-offload-filedrop.py, the
# SAME-VM file-drop transport, so the two tools share one liveness definition on
# that plane too (do not diverge these):
#   STALE_MINUTES = 20                    (same window as the git-scratch plane)
#   FAMILIES = ("opus", "fable", "codex")
#   DEFAULT_ROOT = "/home/grc/grc_working"; $GRC_WORKING overrides
#   layout: <root>/<family>/{available-work,inbox/<worker>,outbox/<worker>,heartbeat}
#   cmd_list_workers LIVE test: the heartbeat FILE's mtime age <= STALE_MINUTES,
#     where the file NAME is the worker id; a missing file reads as +inf minutes.
#     Note the plane difference: file-drop liveness has NO status field, so there
#     is no "active" half to test, and the stamp INSIDE the heartbeat file is not
#     the liveness signal (its mtime is).
FAMILIES = ("opus", "fable", "codex")
DEFAULT_WORKING = "/home/grc/grc_working"


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


def looks_like_exchange_root(root):
    """True when `root` looks like a file-drop exchange root, that is a directory
    holding at least one family subtree. Mirrors the family set the file-drop
    helper routes on; a root with no family subtree has never been `init`ed and
    carries no fleet to report."""
    return root.is_dir() and any((root / fam).is_dir() for fam in FAMILIES)


def find_working(cli_path):
    """Resolve the file-drop exchange root, or None. Same resolution ORDER and
    same no-silent-fallback rule as find_scratch: an explicitly named path
    (--working / GRC_WORKING) that does not resolve is reported rather than
    replaced by the default. GRC_WORKING is the variable the file-drop helper
    itself honours, so the two agree on the root by construction."""
    for label, cand in (("--working", cli_path),
                        ("GRC_WORKING", os.environ.get("GRC_WORKING"))):
        if cand:
            if looks_like_exchange_root(Path(cand)):
                return Path(cand)
            print(f"advisory: {label}={cand} is not a file-drop exchange root "
                  "with at least one family subtree; not falling back to any "
                  "other location; nothing to report.")
            sys.exit(0)
    default = Path(DEFAULT_WORKING)
    if looks_like_exchange_root(default):
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


def mtime_age_minutes(path):
    """Minutes since `path` was last modified; +inf if it does not exist. Mirrored
    from credit-offload-filedrop.py mtime_age_minutes, the file-drop plane's own
    liveness clock."""
    try:
        mtime = path.stat().st_mtime
    except OSError:
        return float("inf")
    delta = datetime.datetime.now(datetime.timezone.utc).timestamp() - mtime
    return delta / 60.0


def worker_is_live(fields, stale_minutes=STALE_MINUTES):
    """The list-workers [LIVE] test: status active AND last_seen within the window."""
    return (fields.get("status") == "active"
            and parse_age_minutes(fields.get("last_seen", "")) <= stale_minutes)


def heartbeat_is_live(hb_path, stale_minutes=STALE_MINUTES):
    """The file-drop cmd_list_workers [LIVE] test: the heartbeat file's mtime age is
    within the window. No status field exists on this plane."""
    return mtime_age_minutes(hb_path) <= stale_minutes


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


def _entries(directory):
    """(sorted entries, readable). An UNREADABLE directory returns ([], False) so
    the caller reports it instead of counting it as empty. This matters on the
    file-drop plane: its subtrees are group-owned (mode 660 / setgid 2770), so an
    account without the exchange group would otherwise read a live fleet as zero,
    which is the exact misleading NO-WORKERS this tool was fixed to stop."""
    try:
        return sorted(directory.iterdir()), True
    except OSError:
        return [], False


def _order_id(path):
    """An order's id: its ``id`` field when present, else the file stem. The
    file-drop dispatch names the dropped file ``<order-id>.md``, so the stem and
    the field agree on both planes; the field is preferred because it is the value
    both helpers key on."""
    try:
        fields = parse_fields(path.read_text(encoding="utf-8", errors="replace"))
    except OSError:
        return path.stem
    return fields.get("id") or path.stem


# The survey result. `shared_live` / `shared_orders` record what de-duplication
# actually removed, so the union is auditable rather than asserted, and
# `unreadable` names any directory that could not be read.
Survey = collections.namedtuple(
    "Survey",
    "live pending claimed other other_statuses scratch_live filedrop_live "
    "shared_live shared_orders unreadable")


def survey_scratch(scratch):
    """The git-scratch plane. Returns (live_worker_ids, {order_id: state}, other,
    other_statuses), where state is 'pending' or 'claimed' and `other` counts order
    files whose status is neither pending/claimed nor done (surfaced rather than
    silently dropped)."""
    live_ids = set()
    workers_dir = scratch / "workers"
    for p in sorted(workers_dir.glob("*.md")):
        if p.name == "README.md":
            continue
        fields = parse_fields(p.read_text(encoding="utf-8", errors="replace"))
        if worker_is_live(fields):
            live_ids.add(fields.get("worker_id") or p.stem)

    orders = {}
    other = 0
    other_statuses = {}
    queue_dir = scratch / "queue"
    if queue_dir.is_dir():
        for p in sorted(queue_dir.glob("*.md")):
            if p.name == "README.md":
                continue
            fields = parse_fields(p.read_text(encoding="utf-8", errors="replace"))
            status = fields.get("status", "")
            oid = fields.get("id") or p.stem
            if status == "pending":
                orders[oid] = "pending"
            elif status == "claimed":
                orders[oid] = "claimed"
            elif status == "done":
                pass  # consumed, not outstanding
            else:
                other += 1
                other_statuses[status] = other_statuses.get(status, 0) + 1
    return live_ids, orders, other, other_statuses


def survey_filedrop(root):
    """The same-VM file-drop plane. Returns (live_worker_ids, {order_id: state},
    unreadable_paths). A worker is live on the file-drop heartbeat test; an order
    is 'pending' while it sits unclaimed in a family's available-work/ and
    'claimed' once a worker has mv-ed it into inbox/<worker>/. Every family is
    scanned, because the fleet is one fleet however its orders are routed."""
    live_ids = set()
    orders = {}
    unreadable = []
    delivered = set()
    for fam in FAMILIES:
        fam_dir = root / fam
        if not fam_dir.is_dir():
            continue

        hb_dir = fam_dir / "heartbeat"
        if hb_dir.is_dir():
            entries, readable = _entries(hb_dir)
            if not readable:
                unreadable.append(hb_dir)
            for hb in entries:
                # The heartbeat FILE NAME is the worker id (file-drop convention).
                if hb.is_file() and heartbeat_is_live(hb):
                    live_ids.add(hb.name)

        avail_dir = fam_dir / "available-work"
        if avail_dir.is_dir():
            entries, readable = _entries(avail_dir)
            if not readable:
                unreadable.append(avail_dir)
            for p in entries:
                if p.is_file() and p.suffix == ".md" and p.name != "README.md":
                    orders[_order_id(p)] = "pending"

        inbox_root = fam_dir / "inbox"
        if inbox_root.is_dir():
            worker_dirs, readable = _entries(inbox_root)
            if not readable:
                unreadable.append(inbox_root)
            for wdir in worker_dirs:
                if not wdir.is_dir():
                    continue
                entries, readable = _entries(wdir)
                if not readable:
                    unreadable.append(wdir)
                for p in entries:
                    # Count order FILES, not holders: an inbox may legitimately be
                    # read mid-claim, and a worker holding two orders is an anomaly
                    # to reflect in the count, not to collapse to one.
                    if p.is_file() and p.suffix == ".md" and p.name != "README.md":
                        orders[_order_id(p)] = "claimed"

        # DELIVERED ids. A file-drop delivery writes the result into
        # outbox/<worker>/<id>.md and UNLINKS the inbox copy, but it does not touch
        # the git-scratch queue/ row, which keeps reading `pending`. That phantom
        # pending inflates `outstanding` and can flip the verdict to SATURATED when
        # the truth is IDLE-CAPACITY, suppressing the very fan-out this tool exists
        # to prompt (the mirror of the NO-WORKERS defect, found by the #1157
        # pre-push verifier and firing live at the time). Collecting delivered ids
        # here lets merge_orders retire the phantom without depending on whether
        # `reconcile-queue` has been run.
        outbox_root = fam_dir / "outbox"
        if outbox_root.is_dir():
            worker_dirs, readable = _entries(outbox_root)
            if not readable:
                unreadable.append(outbox_root)
            for wdir in worker_dirs:
                if not wdir.is_dir():
                    continue
                entries, readable = _entries(wdir)
                if not readable:
                    unreadable.append(wdir)
                for p in entries:
                    if p.is_file() and p.suffix == ".md" and p.name != "README.md":
                        delivered.add(_order_id(p))
    return live_ids, orders, unreadable, delivered


def merge_orders(scratch_orders, filedrop_orders, delivered=frozenset()):
    """Union the two planes' orders BY ORDER ID so one logical order counts once.
    'claimed' wins over 'pending' whichever plane it came from, because the
    orchestrator authors an order into the git-scratch queue/ AND dispatches the
    same id to file-drop, where a worker then claims it: the claimed state is the
    later, more accurate one.

    ``delivered`` is the set of order ids with a file in a file-drop outbox. Read it as
    "a worker wrote something back", NOT as "the work is complete": a NOT-RUN notice and
    a declined order are indistinguishable from a finished result here, and that is
    deliberate, because in every case the git-scratch row should stop sitting ``pending``
    once a worker has responded. Such an order is dropped from the outstanding count
    UNLESS file-drop currently shows it outstanding (see the retirement rule below). This is what keeps a delivered-but-still-
    ``pending`` git-scratch row (a file-drop delivery never updates that row) from
    inflating ``outstanding`` and flipping the verdict to SATURATED when the truth is
    IDLE-CAPACITY. Evidence is DELIVERY, not a status field, so the count does not
    depend on whether ``reconcile-queue`` has been run.

    Returns {order_id: state}."""
    merged = dict(scratch_orders)
    for oid, state in filedrop_orders.items():
        if merged.get(oid) == "claimed":
            continue
        merged[oid] = state
    # Retire only ids file-drop does NOT currently show. A historical outbox file must
    # not erase an order that is outstanding RIGHT NOW: an id can be re-dispatched
    # (the natural move, since the id names the work) while an older outbox file for it
    # survives, and popping it then makes a genuinely outstanding order invisible to
    # the observable, which is the under-count direction and how an order gets
    # forgotten. Current file-drop presence outranks a historical outbox file, the same
    # "later state wins" logic already applied for claimed-over-pending above. Found by
    # the #1157 post-merge sweep (F1), whose precondition was live at the time: a
    # NOT-RUN notice sat in an outbox for work that still needed doing.
    for oid in delivered - set(filedrop_orders):
        merged.pop(oid, None)
    return merged


def survey(scratch, working):
    """Count live workers and outstanding orders as the de-duplicated UNION of both
    exchange planes (the git-scratch registry/queue and the same-VM file-drop
    heartbeats/available-work/inboxes). Either plane may be None (absent)."""
    if scratch is None:
        s_live, s_orders, other, other_statuses = set(), {}, 0, {}
    else:
        s_live, s_orders, other, other_statuses = survey_scratch(scratch)
    if working is None:
        f_live, f_orders, unreadable, delivered = set(), {}, [], set()
    else:
        f_live, f_orders, unreadable, delivered = survey_filedrop(working)

    orders = merge_orders(s_orders, f_orders, delivered)
    return Survey(
        live=len(s_live | f_live),
        pending=sum(1 for st in orders.values() if st == "pending"),
        claimed=sum(1 for st in orders.values() if st == "claimed"),
        other=other,
        other_statuses=other_statuses,
        scratch_live=len(s_live),
        filedrop_live=len(f_live),
        shared_live=len(s_live & f_live),
        shared_orders=len(set(s_orders) & set(f_orders)),
        unreadable=unreadable,
    )


def oneline(live, pending, claimed):
    """The statusline form."""
    v = verdict(live, pending, claimed)
    return (f"workers: {live} live / {pending} pending / {claimed} claimed "
            f"[{v}]")


def run_report(scratch, working, one):
    s = survey(scratch, working)
    if one:
        print(oneline(s.live, s.pending, s.claimed))
        return
    outstanding = s.pending + s.claimed
    v = verdict(s.live, s.pending, s.claimed)
    idle = max(0, s.live - outstanding)
    print(oneline(s.live, s.pending, s.claimed))
    print(f"live workers:      {s.live}")
    print(f"outstanding orders: {outstanding} ({s.pending} pending + {s.claimed} claimed)")
    print(f"idle capacity:     {idle} live worker(s) with nothing to claim")
    print(f"verdict:           {v}")
    # Plane transparency: which plane the fleet is actually on, and what the
    # de-duplication removed. Without this the union is unauditable.
    print(f"planes:            git-scratch {s.scratch_live} live, "
          f"file-drop {s.filedrop_live} live")
    if s.shared_live or s.shared_orders:
        print(f"  de-duplicated:   {s.shared_live} worker id(s) and "
              f"{s.shared_orders} order id(s) present on both planes, counted once")
    if scratch is None:
        print("  note: no git-scratch checkout resolved; reporting from the "
              "file-drop plane alone.")
    if working is None:
        print("  note: no file-drop exchange root resolved; reporting from the "
              "git-scratch plane alone.")
    if v == "IDLE-CAPACITY":
        print("  IDLE-CAPACITY: at least one live worker has no order to claim. "
              "If offloadable backlog exists, enqueue it so the idle worker(s) "
              "pick it up; otherwise the fleet is idle by design.")
    elif v == "NO-WORKERS":
        print("  NO-WORKERS: no live worker to offload to (register or wake a "
              "worker before enqueuing offload work).")
    if s.unreadable:
        shown = ", ".join(str(p) for p in s.unreadable)
        print(f"note: {len(s.unreadable)} exchange director(ies) could not be read "
              f"({shown}); workers or orders under them are NOT counted, so treat "
              "the counts above as a floor (check the exchange group credential).")
    if s.other:
        shown = ", ".join(f"{k or '(blank)'}={n}" for k, n in sorted(s.other_statuses.items()))
        print(f"note: {s.other} order file(s) carry a status that is neither "
              f"pending/claimed nor done ({shown}); not counted as outstanding, "
              "surfaced for triage.")


def _write(path, text):
    """Fixture helper: write `text` to `path`, creating parents."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _fixture_worker_row(worker_id, status, age_minutes):
    stamp = (datetime.datetime.now(datetime.timezone.utc)
             - datetime.timedelta(minutes=age_minutes)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return (f"# Worker {worker_id}\n\n"
            f"- **worker_id:** {worker_id}\n"
            f"- **status:** {status}\n"
            f"- **last_seen:** {stamp}\n")


def _fixture_order(order_id, status):
    return f"# Order {order_id}\n\n- **id:** {order_id}\n- **status:** {status}\n"


def _build_scratch(root, workers, orders):
    """workers: {worker_id: (status, age_minutes)}; orders: {order_id: status}."""
    (root / "workers").mkdir(parents=True, exist_ok=True)
    for wid, (status, age) in workers.items():
        _write(root / "workers" / f"{wid}.md", _fixture_worker_row(wid, status, age))
    (root / "queue").mkdir(parents=True, exist_ok=True)
    for oid, status in orders.items():
        _write(root / "queue" / f"{oid}.md", _fixture_order(oid, status))
    return root


def _build_filedrop(root, heartbeats, available, claimed, delivered=None):
    """heartbeats: {family: {worker_id: age_minutes}};
    available: {family: [order_id]}; claimed: {family: {worker_id: [order_id]}};
    delivered: {family: {worker_id: [order_id]}} written into outbox/<worker>/."""
    for fam, workers in heartbeats.items():
        hb_dir = root / fam / "heartbeat"
        hb_dir.mkdir(parents=True, exist_ok=True)
        for wid, age in workers.items():
            hb = hb_dir / wid
            hb.write_text("stamp\n", encoding="utf-8")
            past = datetime.datetime.now(datetime.timezone.utc).timestamp() - age * 60.0
            os.utime(hb, (past, past))
    for fam, oids in available.items():
        d = root / fam / "available-work"
        d.mkdir(parents=True, exist_ok=True)
        for oid in oids:
            _write(d / f"{oid}.md", _fixture_order(oid, "pending"))
    for fam, per_worker in claimed.items():
        for wid, oids in per_worker.items():
            d = root / fam / "inbox" / wid
            d.mkdir(parents=True, exist_ok=True)
            for oid in oids:
                _write(d / f"{oid}.md", _fixture_order(oid, "claimed"))
    for fam, per_worker in (delivered or {}).items():
        for wid, oids in per_worker.items():
            d = root / fam / "outbox" / wid
            d.mkdir(parents=True, exist_ok=True)
            for oid in oids:
                _write(d / f"{oid}.md", f"# result {oid}\n")
    return root


def _plane_cases(tmp):
    """Fixture scenarios for the two-plane union. Each case is
    (name, scratch_or_None, working_or_None, expected (live, pending, claimed, verdict))."""
    cases = []

    # 1. FILE-DROP ONLY: the live regression. Three workers heartbeating on
    #    file-drop with no git-scratch plane at all must NOT read as NO-WORKERS.
    fd_only = _build_filedrop(
        tmp / "c1-working",
        heartbeats={"opus": {"w-a": 1, "w-b": 2}, "codex": {"c-a": 1}},
        available={"opus": ["o-1", "o-2"]},
        claimed={"opus": {"w-a": ["o-3"]}, "codex": {"c-a": ["o-4"]}})
    cases.append(("file-drop-only fleet is seen (was NO-WORKERS)",
                  None, fd_only, (3, 2, 2, "SATURATED")))

    # 2. FILE-DROP ONLY with idle capacity: 3 live, 1 outstanding.
    fd_idle = _build_filedrop(
        tmp / "c2-working",
        heartbeats={"opus": {"w-a": 1, "w-b": 1, "w-c": 1}},
        available={"opus": ["o-1"]}, claimed={})
    cases.append(("file-drop-only fleet with idle capacity",
                  None, fd_idle, (3, 1, 0, "IDLE-CAPACITY")))

    # 3. BOTH PLANES, a worker id on both: counted ONCE. w-shared is live in the
    #    registry AND heartbeating on file-drop, so live is 2, not 3.
    both_s = _build_scratch(tmp / "c3-scratch",
                            workers={"w-shared": ("active", 1)},
                            orders={"o-1": "pending"})
    both_f = _build_filedrop(tmp / "c3-working",
                             heartbeats={"opus": {"w-shared": 1, "w-only-fd": 1}},
                             available={}, claimed={})
    cases.append(("both planes, worker id on both counted once",
                  both_s, both_f, (2, 1, 0, "IDLE-CAPACITY")))

    # 4. BOTH PLANES, an ORDER id on both: counted ONCE, and the file-drop
    #    'claimed' state wins over the stale git-scratch 'pending' row. This is
    #    the live dispatch shape (authored into queue/, dispatched to file-drop).
    sat_s = _build_scratch(tmp / "c4-scratch",
                           workers={"w-a": ("active", 1)},
                           orders={"o-dual": "pending", "o-gs-only": "pending"})
    sat_f = _build_filedrop(tmp / "c4-working",
                            heartbeats={"opus": {"w-a": 1}},
                            available={}, claimed={"opus": {"w-a": ["o-dual"]}})
    cases.append(("both planes, order id on both counted once as claimed",
                  sat_s, sat_f, (1, 1, 1, "SATURATED")))

    # 5. ABSENT file-drop root: the git-scratch plane still reports correctly.
    gs_only = _build_scratch(tmp / "c5-scratch",
                             workers={"w-a": ("active", 1), "w-stale": ("active", 90)},
                             orders={"o-1": "pending", "o-done": "done"})
    cases.append(("absent file-drop root, git-scratch alone still reports",
                  gs_only, None, (1, 1, 0, "SATURATED")))

    # 6. Staleness on the file-drop plane uses the heartbeat mtime window.
    fd_stale = _build_filedrop(
        tmp / "c6-working",
        heartbeats={"opus": {"w-fresh": 1, "w-stale": STALE_MINUTES + 5}},
        available={}, claimed={})
    cases.append(("file-drop stale heartbeat is not live",
                  None, fd_stale, (1, 0, 0, "IDLE-CAPACITY")))

    # 7. THE PHANTOM-PENDING VECTOR (the #1157 pre-push verifier's W1, which was
    #    firing live when found). A file-drop delivery writes outbox/<worker>/<id>.md
    #    and unlinks the inbox copy, but never updates the git-scratch queue/ row, so
    #    that row still reads 'pending'. Without retiring delivered ids the count
    #    would read (3 live, 1 pending, 0 claimed) and verdict SATURATED (1 >= 3 is
    #    false, so actually IDLE-CAPACITY, but with the phantom the arithmetic tips on
    #    a larger queue); here the delivered order must vanish from the count entirely,
    #    leaving genuine idle capacity visible so the fan-out prompt still fires.
    ph_s = _build_scratch(tmp / "c7-scratch",
                          workers={"w-a": ("active", 1)},
                          orders={"o-delivered": "pending"})
    ph_f = _build_filedrop(tmp / "c7-working",
                           heartbeats={"opus": {"w-a": 1, "w-b": 1, "w-c": 1}},
                           available={}, claimed={},
                           delivered={"opus": {"w-a": ["o-delivered"]}})
    cases.append(("delivered order retires a phantom pending scratch row",
                  ph_s, ph_f, (3, 0, 0, "IDLE-CAPACITY")))

    # 8. The verdict-flipping counterfactual, stated as its own case: three live
    #    workers, TWO genuine outstanding orders and ONE phantom. Truth is 2 < 3, so
    #    IDLE-CAPACITY and fan out. With the phantom counted it would be 3 >= 3 and
    #    SATURATED, suppressing the very prompt this tool exists to produce.
    cf_s = _build_scratch(tmp / "c8-scratch",
                          workers={"w-a": ("active", 1)},
                          orders={"o-phantom": "pending", "o-real": "pending"})
    cf_f = _build_filedrop(tmp / "c8-working",
                           heartbeats={"opus": {"w-a": 1, "w-b": 1, "w-c": 1}},
                           available={"opus": ["o-real"]},
                           claimed={"opus": {"w-b": ["o-claimed"]}},
                           delivered={"opus": {"w-a": ["o-phantom"]}})
    cases.append(("phantom does not flip IDLE-CAPACITY to SATURATED",
                  cf_s, cf_f, (3, 1, 1, "IDLE-CAPACITY")))

    # 9. A delivered order retires when the SCRATCH row is the only thing still calling
    #    it outstanding. This is the W1 phantom in its pure form: git-scratch says
    #    'pending', file-drop has no entry at all (delivery unlinked the inbox copy), and
    #    an outbox file exists. It retires.
    #    NOTE: an earlier version of this case asserted that delivery also outranks a
    #    LIVE claimed inbox copy, and expected (1, 0, 0, IDLE-CAPACITY). That expectation
    #    was WRONG and encoded the under-count the #1157 post-merge sweep found as F1: a
    #    historical outbox file must not erase an order that is outstanding right now.
    #    Cases 10 and 11 now cover that shape with the correct expectation.
    dd_s = _build_scratch(tmp / "c9-scratch",
                          workers={"w-a": ("active", 1)},
                          orders={"o-both": "pending"})
    dd_f = _build_filedrop(tmp / "c9-working",
                           heartbeats={"opus": {"w-a": 1}},
                           available={}, claimed={},
                           delivered={"opus": {"w-a": ["o-both"]}})
    cases.append(("delivery retires a scratch-only phantom",
                  dd_s, dd_f, (1, 0, 0, "IDLE-CAPACITY")))

    # 10. THE UNDER-COUNT GUARD (the #1157 post-merge sweep's F1). A historical outbox
    #     file must NOT erase an order that is outstanding right now. An id can be
    #     re-dispatched while an older outbox file for it survives (a NOT-RUN notice was
    #     sitting in an outbox for real work when this was found), and retiring it then
    #     makes a genuinely outstanding order invisible, which is how an order gets
    #     forgotten. Here o-redispatched is BOTH in available-work and in an outbox: it
    #     must still count as pending.
    rd_f = _build_filedrop(tmp / "c10-working",
                           heartbeats={"opus": {"w-a": 1}},
                           available={"opus": ["o-redispatched"]}, claimed={},
                           delivered={"opus": {"w-a": ["o-redispatched"]}})
    cases.append(("a re-dispatched id is not retired by an old outbox file",
                  None, rd_f, (1, 1, 0, "SATURATED")))

    # 11. Same guard on the CLAIMED side: an id claimed on file-drop with an older
    #     outbox file must stay claimed, not vanish.
    rc_f = _build_filedrop(tmp / "c11-working",
                           heartbeats={"opus": {"w-a": 1}},
                           available={}, claimed={"opus": {"w-a": ["o-again"]}},
                           delivered={"opus": {"w-a": ["o-again"]}})
    cases.append(("a claimed id is not retired by an old outbox file",
                  None, rc_f, (1, 0, 1, "SATURATED")))

    return cases


def self_test():
    """In-memory fixture scenarios against the verdict logic, plus tempdir fixture
    scenarios against the two-plane survey; PASS/FAIL per case, exit non-zero only
    if a case fails."""
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

    # two-plane survey guards, on throwaway fixture trees (never the real
    # exchange): the union, the de-duplication, and each plane alone.
    plane_total = 0
    with tempfile.TemporaryDirectory(prefix="saturation-selftest-") as td:
        tmp = Path(td)
        for name, scratch, working, expected in _plane_cases(tmp):
            s = survey(scratch, working)
            got = (s.live, s.pending, s.claimed,
                   verdict(s.live, s.pending, s.claimed))
            ok = got == expected
            plane_total += 1
            failures += 0 if ok else 1
            print(f"  {'PASS' if ok else 'FAIL'}: planes, {name} -> {got}"
                  + ("" if ok else f" (expected {expected})"))

    total = len(cases) + len(live_cases) + plane_total
    print(f"\nself-test: {total - failures}/{total} passed")
    return 0 if failures == 0 else 1


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--scratch", help="path to the grc_library_scratch checkout")
    ap.add_argument("--working",
                    help="path to the same-VM file-drop exchange root "
                         "(else $GRC_WORKING, else " + DEFAULT_WORKING + ")")
    ap.add_argument("--oneline", action="store_true",
                    help="print the one-line statusline form only")
    ap.add_argument("--self-test", action="store_true",
                    help="run the inline verdict/liveness self-test and exit")
    args = ap.parse_args(argv[1:])

    if args.self_test:
        return self_test()

    scratch = find_scratch(args.scratch)
    working = find_working(args.working)
    if scratch is None and working is None:
        if sibling_placeholder_present("scratch"):
            print("advisory: grc_library_scratch sibling absent (portable clone; "
                  ".scratch placeholder present) and no file-drop exchange root; "
                  "maintainer-only advisory, nothing to report.")
        else:
            print("advisory: no exchange plane found (no --scratch or "
                  "GRC_SCRATCH_PATH given and no sibling grc_library_scratch "
                  "directory with a workers/ registry; no --working or "
                  "GRC_WORKING given and no default file-drop exchange root); "
                  "nothing to report.")
        return 0

    run_report(scratch, working, args.oneline)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
