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
and per-worker ``heartbeat`` files, PLUS the central month-partitioned ``done/`` archive of
consumed deliveries and orders). Reading only the git-scratch plane was a real
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
import time
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


STALL_MINUTES = 15

# One row per live worker, for the stall read. A namedtuple so the pure predicate below cannot
# accidentally reach the filesystem through it.
WorkerFacts = collections.namedtuple(
    "WorkerFacts", "family worker hb_age holds session_age since_delivery oldest_claimable")
Suspect = collections.namedtuple(
    "Suspect", "family worker hb_age session_age since_delivery oldest_claimable evidence")


def stall_evidence_minutes(session_age, since_delivery, oldest_claimable):
    """PURE. The weakest of the three spans, because the finding is only as strong as its weakest leg.

    A worker cannot be judged stalled on a long-waiting order if it only started a minute ago, nor on
    a long session if it delivered seconds ago. Taking the MINIMUM makes every span a veto, which is
    what keeps the healthy cycle boundary out of the report.
    """
    return min(session_age, since_delivery, oldest_claimable)


def stall_suspects(facts, stall_minutes=STALL_MINUTES, stale_minutes=STALE_MINUTES):
    """PURE: WorkerFacts in, Suspect out. No filesystem, no clock.

    A STALL SUSPECT is live, holds nothing, and has had CLAIMABLE work in its own family for longer
    than `stall_minutes` on all three evidence spans.

    IT IS CALLED SUSPECT AND NOT STALLED ON PURPOSE, and it deliberately does NOT feed `verdict()`.
    The exchange records no claim event, so the finding is circumstantial by construction. More
    importantly the asymmetry runs one way: a false `STALLED-CAPACITY` verdict would read as "this
    capacity is unusable" and license self-running work the mandatory-offload discipline requires be
    offloaded, which is the same false reassurance as the NO-WORKERS-while-live defect fixed in #1157,
    in the more expensive direction. Whereas IDLE-CAPACITY on a genuinely stalled worker merely wastes
    an enqueue, which is nearly free and self-correcting. So this reports a condition and names its
    evidence; it never moves a verdict.
    """
    out = []
    for f in facts:
        if f.hb_age > stale_minutes:
            continue   # not live: a dead worker is `reclaim`'s job, not a stall report
        if f.holds:
            continue   # holding work is the opposite of failing to claim
        evidence = stall_evidence_minutes(f.session_age, f.since_delivery, f.oldest_claimable)
        if evidence > stall_minutes:
            out.append(Suspect(f.family, f.worker, f.hb_age, f.session_age,
                               f.since_delivery, f.oldest_claimable, evidence))
    return out


def claimable_by(worker, order_fields):
    """PURE. May this worker claim an order carrying these fields?

    THE AMENDMENT THE CANDIDATE REQUIRED (resume-consume-3115-3116-verify F-1). The candidate measured
    the age of the oldest AVAILABLE order, with no test of whether the worker may claim it. Since the
    transport began enforcing per-order exclusions at claim time, a BARRED order sits in
    available-work ageing indefinitely while the excluded worker correctly declines it every cycle, so
    availability alone would report a blameless worker as a stall suspect. Demonstrated against the
    candidate's own predicate before this fix, so it is a measured interaction rather than a guess.
    """
    barred = {w.strip() for w in (order_fields.get("not_worker") or "").split(",") if w.strip()}
    return worker not in barred


def ctime_age_minutes(path):
    """Minutes since the path's inode last changed. Observer.

    Distinct from mtime age because os.rename preserves mtime but advances ctime, which is exactly
    the difference the availability clock turns on (see collect_stall_facts).
    """
    try:
        return max(0.0, (time.time() - path.stat().st_ctime) / 60.0)
    except OSError:
        return 0.0


def session_age_from_id(worker_id):
    """Minutes since this worker's session STARTED, parsed from its minted id. Pure.

    The id is `<family>-<YYYYMMDD>T<HHMMSS>Z-<4 hex>` and the heartbeat FILE NAME is the id, so the
    timestamp is available without reading anything.

    THIS IS THE DEFECT THIS FUNCTION EXISTS TO FIX (found by a worker 2026-07-25, after TODO 3.116
    had already closed). The shipped version used the heartbeat marker's mtime as the session age.
    A heartbeat marker is REWRITTEN on every check-in, so its mtime is the LAST CHECK-IN, never the
    session start, and neither does its ctime. Because the stall evidence is a min() of three spans
    and the heartbeat age also caps liveness at STALE_MINUTES, an mtime-derived session age made the
    evidence unable to exceed STALE_MINUTES: the signal could fire only in the narrow band between
    STALL_MINUTES and STALE_MINUTES, minutes before the worker would be called stale anyway. A
    worker heartbeating on its documented cycle, which is the ENTIRE subject of the check ("the
    worker keeps heartbeating but stops claiming"), could never be flagged. The guard's logic was
    correct throughout; it was fed an input that cannot answer the question asked of it.

    Returns +inf for an id that does not carry a conforming timestamp. +inf and not 0.0: the value
    feeds a min() of vetoes, so an unparseable id must contribute NO veto rather than a permanent
    one. A legacy or hand-made id therefore neither suppresses a real suspect nor invents one.
    """
    match = re.search(r"(\d{8}T\d{6}Z)", worker_id or "")
    if not match:
        return float("inf")
    try:
        started = datetime.datetime.strptime(
            match.group(1), "%Y%m%dT%H%M%SZ").replace(tzinfo=datetime.timezone.utc)
    except ValueError:
        return float("inf")
    return max(0.0, (datetime.datetime.now(datetime.timezone.utc) - started).total_seconds() / 60.0)


def collect_stall_facts(root):
    """The file-drop walk: one WorkerFacts row per heartbeat marker. Observer; decides nothing.

    FAMILY-SCOPED by design. The transport routes orders by family and a worker only ever sees its own
    family's available-work, so an order waiting in another family is no evidence at all about this
    worker. The fleet-wide counts elsewhere in this tool are deliberately not reused here.

    The oldest-claimable span EXCLUDES orders this worker is barred from, which is the amendment the
    candidate required: a barred order ages in available-work indefinitely while the excluded worker
    correctly declines it every cycle, so counting it would report a blameless worker as a suspect.
    """
    facts = []
    if root is None:
        return facts
    for fam in FAMILIES:
        fam_dir = root / fam
        if not fam_dir.is_dir():
            continue
        hb_dir = fam_dir / "heartbeat"
        if not hb_dir.is_dir():
            continue
        avail = fam_dir / "available-work"
        for hb in sorted(p for p in hb_dir.iterdir() if p.is_file()):
            worker = hb.name
            inbox = fam_dir / "inbox" / worker
            holds = None
            if inbox.is_dir():
                held = sorted(q.stem for q in inbox.glob("*.md") if q.name != "README.md")
                holds = held[0] if held else None
            outbox = fam_dir / "outbox" / worker
            # Since its LAST delivery, or +inf when it has never delivered. The +inf is deliberate
            # and was WRONG here before: this fell back to heartbeat age, which made the span a
            # permanent veto (see session_age_from_id for why any heartbeat-derived span cannot
            # answer this question). A never-delivered worker gives NO evidence about quiet time,
            # and since evidence is a min() of vetoes, "no evidence" must be +inf, not a small
            # number that silently vetoes. The compounding factor: collect-deliveries.py sweeps
            # outboxes empty, so `ages` is now routinely empty for a worker whose results were
            # collected, which made the bad fallback the COMMON path rather than the rare one.
            since_delivery = float("inf")
            if outbox.is_dir():
                ages = [mtime_age_minutes(q) for q in outbox.glob("*.md") if q.name != "README.md"]
                if ages:
                    since_delivery = min(ages)
            oldest_claimable = 0.0
            if avail.is_dir():
                for order in avail.glob("*.md"):
                    if order.name == "README.md":
                        continue
                    try:
                        fields = parse_fields(order.read_text(encoding="utf-8", errors="replace"))
                    except OSError:
                        continue
                    if not claimable_by(worker, fields):
                        continue
                    # ctime, NOT mtime: `reclaim` returns an order to available-work with
                    # os.rename, which PRESERVES mtime, so a reclaimed order's mtime age includes
                    # the span a now-dead worker held it. That inflated span would fire against a
                    # healthy worker that has only had the chance to claim it since the rename.
                    # ctime advances on the rename, so it dates the order's availability.
                    oldest_claimable = max(oldest_claimable, ctime_age_minutes(order))
            facts.append(WorkerFacts(
                family=fam, worker=worker, hb_age=mtime_age_minutes(hb), holds=holds,
                session_age=session_age_from_id(worker), since_delivery=since_delivery,
                oldest_claimable=oldest_claimable))
    return facts


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


def _tray_order_id(stem: str) -> str:
    """PURE. Recover an order id from a delivery-tray filename.

    The tray names a collected delivery ``<worker-id>__<order-id>.md`` so both ids survive without
    parsing the body. A RESULT file carries no ``id:`` field, so ``_order_id`` would fall back to the
    whole stem and yield an id that matches no queue row, which would silently defeat the
    phantom-pending retirement below. Splitting on the FIRST join is correct because a worker id never
    contains it while an order id may contain hyphens.
    """
    return stem.split("__", 1)[1] if "__" in stem else stem


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

    # The CENTRAL, worker-id-independent archive (2026-07-25). A consumed delivery is MOVED
    # out of its worker's outbox into done/, so without scanning here every archived order id
    # would stop counting as delivered, its phantom `pending` git-scratch row would come back,
    # `outstanding` would inflate, and the verdict could flip to a false SATURATED. That is
    # precisely the defect fixed in grc_library #1158, and the archive would have reintroduced
    # it. Both partitions are scanned because an order and its result archive separately.
    # THE DELIVERY TRAY (grc_library #1171, and the regression it caused). A delivery is now swept out
    # of its worker's outbox into inbox/deliveries/ as soon as the orchestrator notices it, so between
    # that sweep and its eventual archive an order sits in a THIRD location this scan did not know
    # about. Without it the order stops counting as delivered, its phantom `pending` git-scratch row
    # comes back, `outstanding` inflates, and the verdict flips to a false SATURATED, which is the very
    # defect the delivered-set logic below was written to prevent, reintroduced by a tool built the same
    # day. It fired live: SATURATED reported while a worker sat idle, found because the maintainer asked
    # whether the fleet was being kept fed. The composed filename also has to be split, or the recovered
    # id matches no queue row and the scan is inert even when it runs.
    tray = root / "inbox" / "deliveries"
    if tray.is_dir():
        entries, readable = _entries(tray)
        if not readable:
            unreadable.append(tray)
        for p in entries:
            if p.is_file() and p.suffix == ".md" and p.name != "README.md":
                delivered.add(_tray_order_id(p.stem))

    for kind in ("deliveries", "orders"):
        kind_root = root / "done" / kind
        if not kind_root.is_dir():
            continue
        month_dirs, readable = _entries(kind_root)
        if not readable:
            unreadable.append(kind_root)
        for mdir in month_dirs:
            if not mdir.is_dir():
                continue
            entries, readable = _entries(mdir)
            if not readable:
                unreadable.append(mdir)
            for p in entries:
                if p.is_file() and p.suffix == ".md" and p.name != "README.md":
                    # done/deliveries/ holds files filed FROM the tray, so they carry the same
                    # composed name and need the same split; done/orders/ holds plain order ids,
                    # which the split leaves untouched.
                    delivered.add(_tray_order_id(p.stem))
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
    # STALL SUSPECTS, reported beside the verdict and never folded into it (TODO 3.116).
    for _s in stall_suspects(collect_stall_facts(working)):
        print(f"STALL-SUSPECT  {_s.worker} ({_s.family}): live at {_s.hb_age:.1f}m, holds "
              f"nothing, and claimable work has waited {_s.oldest_claimable:.1f}m "
              f"(session {_s.session_age:.1f}m, since delivery {_s.since_delivery:.1f}m; "
              f"weakest span {_s.evidence:.1f}m). CIRCUMSTANTIAL: the exchange records no claim "
              f"event, so this is not proof. Check in on it before assuming the capacity is real.")

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


def _build_filedrop(root, heartbeats, available, claimed, delivered=None, archived=None,
                    trayed=None):
    """heartbeats: {family: {worker_id: age_minutes}};
    available: {family: [order_id]}; claimed: {family: {worker_id: [order_id]}};
    delivered: {family: {worker_id: [order_id]}} written into outbox/<worker>/;
    archived: [order_id] written into done/deliveries/<month>/ (family-independent);
    trayed: [(worker_id, order_id)] written into inbox/deliveries/ under the tray's composed
    <worker-id>__<order-id>.md name, the location a swept delivery occupies before archive."""
    for wid, oid in (trayed or []):
        tray = root / "inbox" / "deliveries"
        tray.mkdir(parents=True, exist_ok=True)
        # A RESULT file, deliberately WITHOUT an `id:` field, because that absence is what makes the
        # composed-filename split load-bearing rather than incidental.
        (tray / f"{wid}__{oid}.md").write_text("# result\n\n<!-- END OF DELIVERY -->\n", encoding="utf-8")
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
    for oid in (archived or []):
        d = root / "done" / "deliveries" / "2026-07"
        d.mkdir(parents=True, exist_ok=True)
        _write(d / f"{oid}.md", f"# archived result {oid}\n")
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

    # 12. THE ARCHIVE MUST STILL COUNT AS DELIVERED (2026-07-25). A consumed delivery is MOVED
    #     out of its worker's outbox into the central done/ archive, so if done/ were not
    #     scanned its order id would stop counting as delivered, the phantom `pending`
    #     git-scratch row would return, and outstanding would inflate. Here the ONLY evidence
    #     of delivery is the archive: no outbox copy exists at all. Mutation-check: removing
    #     the done/ scan makes this case report 1 pending instead of 0.
    ar_s = _build_scratch(tmp / "c12-scratch",
                          workers={"w-a": ("active", 1)},
                          orders={"o-archived": "pending"})
    ar_f = _build_filedrop(tmp / "c12-working",
                           heartbeats={"opus": {"w-a": 1}},
                           available={}, claimed={},
                           archived=["o-archived"])
    cases.append(("an archived delivery in done/ still counts as delivered",
                  ar_s, ar_f, (1, 0, 0, "IDLE-CAPACITY")))

    # THE #1171 REGRESSION, pinned. A delivery swept into the tray must still retire its phantom
    # `pending` scratch row; before the tray was scanned this returned SATURATED with a worker idle.
    tr_s = _build_scratch(tmp / "c13-scratch",
                          workers={"w-a": ("active", 1)},
                          orders={"o-trayed": "pending"})
    tr_f = _build_filedrop(tmp / "c13-working",
                           heartbeats={"opus": {"w-a": 1}},
                           available={}, claimed={},
                           trayed=[("opus-20260725T122030Z-6443", "o-trayed")])
    cases.append(("a delivery swept into the tray retires its phantom pending row",
                  tr_s, tr_f, (1, 0, 0, "IDLE-CAPACITY")))

    # And the SPLIT is what makes that work: an unsplit stem yields an id matching no queue row, so
    # the scan would run and be inert. Two live workers with one phantom row would read SATURATED.
    sp_s = _build_scratch(tmp / "c14-scratch",
                          workers={"w-a": ("active", 1), "w-b": ("active", 1)},
                          orders={"o-split": "pending"})
    sp_f = _build_filedrop(tmp / "c14-working",
                           heartbeats={"opus": {"w-a": 1, "w-b": 1}},
                           available={}, claimed={},
                           trayed=[("opus-worker-with-a-long-id", "o-split")])
    cases.append(("the composed-filename split is load-bearing, not incidental",
                  sp_s, sp_f, (2, 0, 0, "IDLE-CAPACITY")))

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
    # The stall read (TODO 3.116). PURE predicate, so every guard is pinned with constructed facts.
    def _wf(**kw):
        base = dict(family="opus", worker="opus-a", hb_age=1.0, holds=None,
                    session_age=600.0, since_delivery=600.0, oldest_claimable=600.0)
        base.update(kw)
        return WorkerFacts(**base)
    for _n, _facts, _want in (
            ("a live idle worker with long-waiting claimable work is a suspect", [_wf()], 1),
            ("a worker HOLDING an order is never a suspect", [_wf(holds="o-1")], 0),
            ("a STALE worker is reclaim's job, not a stall report", [_wf(hb_age=99.0)], 0),
            ("a JUST-STARTED worker is not a suspect", [_wf(session_age=2.0)], 0),
            ("a worker that delivered SECONDS ago is not a suspect", [_wf(since_delivery=0.5)], 0),
            ("a RECENT order is not evidence yet", [_wf(oldest_claimable=1.0)], 0),
            ("no claimable work at all is not a stall", [_wf(oldest_claimable=0.0)], 0),
    ):
        total += 1
        _got = len(stall_suspects(_facts))
        if _got != _want:
            failures.append(_n)
            print(f"  FAIL: {_n} -> {_got} suspect(s), expected {_want}")
        else:
            print(f"  PASS: {_n}")
    # COLLECTOR-level cases (added 2026-07-25 after a worker found the shipped stall signal could
    # not fire). The seven PURE cases above were all correct and all passed, which is precisely why
    # they missed the defect: the predicate was right and the INPUT could not answer the question.
    # Every case below is DISCRIMINATING against the shipped code, i.e. it fails if the input
    # reverts. A pure-predicate suite alone cannot catch a guard-input defect, so the collector's
    # derivation of each span needs its own pinning.
    for _n, _id, _want in (
            ("a conforming worker id yields a finite session age", "opus-20260101T000000Z-aaaa", True),
            ("an unparseable id yields +inf, contributing NO veto", "legacy-worker-a", False),
            ("an impossible date yields +inf rather than raising", "opus-20261399T999999Z-bb", False),
    ):
        total += 1
        _age = session_age_from_id(_id)
        _finite = _age != float("inf")
        if _finite != _want:
            failures.append(_n)
            print(f"  FAIL: {_n} -> {_age}")
        else:
            print(f"  PASS: {_n}")
    with tempfile.TemporaryDirectory() as _td:
        _r = Path(_td)
        # (1) The availability clock is ctime, not mtime. Setting mtime 45m into the past leaves
        # ctime at now, so a ctime-based read stays ~0 while an mtime-based read returns ~45. This
        # is the only way to pin fix 3: ctime CANNOT be aged with os.utime (the kernel owns it), so
        # a genuinely-old availability span is not constructible here. The discrimination runs the
        # other way instead, and it is enough to catch a revert to mtime.
        _o = _r / "order.md"
        _o.write_text("- **id:** o\n", encoding="utf-8")
        os.utime(_o, (time.time() - 45 * 60,) * 2)
        total += 1
        _av = ctime_age_minutes(_o)
        if _av > 5.0:
            failures.append("the availability clock ignores a back-dated mtime")
            print(f"  FAIL: the availability clock ignores a back-dated mtime -> {_av:.1f}m "
                  "(reverted to mtime)")
        else:
            print("  PASS: the availability clock ignores a back-dated mtime")
        # (2) THE DEFECT ITSELF. A worker minted long ago that is heartbeating on its normal cycle
        # must report its SESSION age, not its heartbeat age. Under the shipped code this reported
        # ~1 minute, which capped the evidence below STALL_MINUTES and made the whole check inert.
        _fam = _r / "opus"
        for _sub in ("heartbeat", "available-work", "inbox", "outbox"):
            (_fam / _sub).mkdir(parents=True, exist_ok=True)
        _old = (datetime.datetime.now(datetime.timezone.utc)
                - datetime.timedelta(minutes=600)).strftime("%Y%m%dT%H%M%SZ")
        _wid = f"opus-{_old}-cccc"
        _hb = _fam / "heartbeat" / _wid
        _hb.write_text("x\n", encoding="utf-8")
        os.utime(_hb, (time.time() - 60,) * 2)  # heartbeating one minute ago: healthy cycle
        total += 1
        _f = [f for f in collect_stall_facts(_r) if f.worker == _wid]
        _sa = _f[0].session_age if _f else -1.0
        if not _f or _sa < 500.0:
            failures.append("session age comes from the minted id, not the heartbeat mtime")
            print("  FAIL: session age comes from the minted id, not the heartbeat mtime -> "
                  f"{_sa:.1f}m (heartbeat is 1m old; a heartbeat-derived value cannot exceed it)")
        else:
            print("  PASS: session age comes from the minted id, not the heartbeat mtime")
        # (3) A never-delivered worker gives +inf, not its heartbeat age. collect-deliveries.py
        # sweeps outboxes empty, so this fallback is the common path, not the rare one.
        # (3b) The availability clock at its CALL SITE, not just in the helper. Testing
        # ctime_age_minutes directly is NOT sufficient: reverting only the call site to
        # mtime_age_minutes leaves the helper's own test passing, which is how the first version of
        # this case let the revert through. A back-dated-mtime order must age ~0, not ~45.
        _ord = _fam / "available-work" / "back-dated.md"
        _ord.write_text("- **id:** back-dated\n", encoding="utf-8")
        os.utime(_ord, (time.time() - 45 * 60,) * 2)
        total += 1
        _f = [f for f in collect_stall_facts(_r) if f.worker == _wid]
        _oc = _f[0].oldest_claimable if _f else -1.0
        if not _f or _oc > 5.0:
            failures.append("the collector's availability span uses ctime at the call site")
            print("  FAIL: the collector's availability span uses ctime at the call site -> "
                  f"{_oc:.1f}m (call site reverted to mtime)")
        else:
            print("  PASS: the collector's availability span uses ctime at the call site")
        total += 1
        _sd = _f[0].since_delivery if _f else 0.0
        if _sd != float("inf"):
            failures.append("an empty outbox yields +inf for since-delivery")
            print(f"  FAIL: an empty outbox yields +inf for since-delivery -> {_sd}")
        else:
            print("  PASS: an empty outbox yields +inf for since-delivery")
    # The claimability amendment: a BARRED order must not make its excluded worker a suspect.
    for _n, _worker, _fields, _want in (
            ("an unbarred worker may claim", "opus-a", {}, True),
            ("the barred worker may NOT claim", "opus-a", {"not_worker": "opus-a"}, False),
            ("a different worker may still claim a barred order", "opus-b", {"not_worker": "opus-a"}, True),
            ("whitespace and multiples are handled", "opus-b", {"not_worker": " opus-a , opus-b "}, False),
    ):
        total += 1
        _got = claimable_by(_worker, _fields)
        if _got != _want:
            failures.append(_n)
            print(f"  FAIL: {_n} -> {_got}, expected {_want}")
        else:
            print(f"  PASS: {_n}")

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
