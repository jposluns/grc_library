#!/usr/bin/env python3
"""exec-dispatch.py - orchestrator-side dispatch for the exec'd worker pool.

Reads the maintainer-maintained account-config (grc_library_private/worker-accounts.json),
selects an eligible worker account for a job per the dispatch rules, and (optionally)
invokes the root-owned wrapper via sudo to run the job as the single worker_agents user.

This is PROJECT-ONLY operational machinery (it references the host wrappers at
/usr/local/sbin and the _private account-config), not portable pack material, in the same
class as manage-workers.py / audit-worker-saturation.py / collect-deliveries.py.

Design of record: grc_library_private/codex-exec-serve-loop-decision.md. The account-config
schema and the dispatch rules (A1 per-account caps, A3 exhaust-a-set-then-next, personal-last,
usage-limit handling) are specified there.

Decision logic is PURE and injects `now` so --self-test can pin time (no wall-clock in the
decision path). The dispatch/invoke path is a thin shell around it.

Modes:
  --self-test                         run the decision-logic fixtures (exit non-zero on fail)
  --dry-run --family F --model M      show eligible accounts (ordered) + the pick, no dispatch
  --dispatch --family F --model M --order-id ID --prompt-file P   actually run the job

Stdlib-only (project convention).
"""
from __future__ import annotations

import argparse
import datetime as _dt
import fcntl
import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

# --- host constants (project-only) -------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]                 # /home/grc/grc_library
DEFAULT_CONFIG = REPO_ROOT.parent / "grc_library_private" / "worker-accounts.json"
JOB_DIR = Path("/var/lib/grc-worker-jobs")
WRAPPER = {
    "claude": "/usr/local/sbin/run-claude-worker",
    "codex": "/usr/local/sbin/run-codex-worker",
}
WORKER_USER = "worker_agents"

# --- in-flight registry (per-account concurrency; TODO 3.141) ----------------------
INFLIGHT_NAME = "inflight.json"
INFLIGHT_LOCK_NAME = "inflight.lock"       # flock target only; its CONTENT is never rewritten
STALE_STARTED_AGE_S = 24 * 3600            # absolute backstop against pid reuse (NOT mtime staleness)

# Tier -> distribution weight (higher = takes more within a priority set). The per-account
# flock currently caps same-account concurrency at 1, so weight is a tie-break today; it
# becomes load-bearing once per-job config-dir snapshots enable concurrency > 1 (WIRE-IN).
TIER_WEIGHT = {
    "pro-20x": 20.0,
    "20x": 20.0,
    "teams-6.5x": 6.5,
    "pro-team": 2.0,
    "pro": 2.0,
    "normal": 1.0,
    "personal": 1.0,
}


# --- config ------------------------------------------------------------------------
def load_config(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _parse_iso(s: str) -> _dt.datetime:
    """Parse an ISO-8601 datetime (with or without tz) to an aware UTC datetime."""
    dt = _dt.datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_dt.timezone.utc)
    return dt.astimezone(_dt.timezone.utc)


# --- pure decision logic (now is injected) -----------------------------------------
def account_available(acct: dict, now: _dt.datetime) -> tuple[bool, str]:
    """Is this account dispatchable at `now`? Returns (ok, reason)."""
    state = acct.get("usage_state", "available")
    if state == "limited":
        until = acct.get("limited_until")
        if not until:
            return False, "limited (no limited_until; treated as unavailable)"
        try:
            until_dt = _parse_iso(until)
        except ValueError:
            return False, f"limited (unparseable limited_until={until!r})"
        if now < until_dt:
            return False, f"limited until {until}"
        return True, f"limited window passed ({until})"
    if state != "available":
        return False, f"usage_state={state!r}"
    return True, "available"


def eligible_accounts(config: dict, family: str, model: str, now: _dt.datetime) -> list[dict]:
    """Accounts that can serve a (family, model) job at `now`, in dispatch-preference order.

    Order: non-personal before personal (personal_accounts_last), then priority_set ascending
    (exhaust a set before the next), then tier-weight descending, then account id. Each entry
    is annotated with `_reason` and `_weight` for transparency.
    """
    out = []
    for acct in config.get("accounts", []):
        if acct.get("family") != family:
            continue
        if model not in acct.get("models", []):
            continue
        ok, reason = account_available(acct, now)
        if not ok:
            continue
        a = dict(acct)
        a["_reason"] = reason
        a["_weight"] = TIER_WEIGHT.get(acct.get("tier", ""), 1.0)
        out.append(a)
    out.sort(key=lambda a: (
        1 if a.get("personal") else 0,      # non-personal first
        a.get("priority_set", 9999),         # lower set first (exhaust-then-next)
        -a["_weight"],                       # higher tier weight first
        a.get("id", a.get("account", "")),
    ))
    return out


def select_account(config: dict, family: str, model: str, now: _dt.datetime):
    """Top eligible account, or None. (max_concurrent enforcement is WIRE-IN: today the
    per-account flock in the wrapper serializes same-account jobs at 1.)"""
    elig = eligible_accounts(config, family, model, now)
    return elig[0] if elig else None


def pick_account(config: dict, family: str, model: str, now: _dt.datetime,
                 account: str | None = None):
    """Resolve WHICH account to dispatch to. PURE. Returns (acct_dict_or_None, reason).

    Without `account`, the top eligible (select_account's pick). With `account`, that EXACT
    account IF it is eligible for (family, model) at `now`, else None with a reason that
    distinguishes an unknown account from a known-but-ineligible one.

    The override is what lets the orchestrator SPREAD concurrent jobs across distinct accounts:
    the wrapper's per-account flock serializes same-account jobs at 1, so without targeting, N
    concurrent auto-dispatches all pick the top account and run SERIALLY. Targeting a different
    eligible account per concurrent job gives real parallelism (each account's flock serializes
    only its own one job). It does NOT bypass a flock, so it is safe today, before same-account
    config-dir snapshotting exists."""
    elig = eligible_accounts(config, family, model, now)
    if account is None:
        return (elig[0], "auto: top eligible") if elig else (None, "no eligible account")
    for a in elig:
        if a.get("account") == account:
            return a, f"targeted: {account}"
    known = any(x.get("account") == account and x.get("family") == family
                for x in config.get("accounts", []))
    if known:
        return None, (f"account '{account}' is known for family '{family}' but NOT eligible for "
                      f"model '{model}' at this time (unavailable, limited, or model not offered)")
    return None, f"account '{account}' is not in the config for family '{family}'"


# --- usage-limit parsing (best-effort; CLI formats need calibration = WIRE-IN) ------
import re as _re

# Only HIGH-CONFIDENCE limit-notice shapes: a "limit(s) reached/exceeded ... reset(s) at <time>"
# or "usage limit ... until/at <time>". A loose "you've reached ... limit" pattern was REMOVED
# (verifier #1185 Finding 3) because it false-fired on benign prose that merely quotes the word
# "limit" (e.g. a worker report summarising text about a "monthly limit of free views").
_LIMIT_PATTERNS = [
    _re.compile(r"limit\s+(?:reached|exceeded).*?reset[s]?\s+(?:at\s+)?(?P<when>[0-9T:\-\+ ]{5,40})", _re.I),
    _re.compile(r"usage\s+limit.*?(?:until|at)\s+(?P<when>[0-9T:\-\+ ]{5,40})", _re.I),
]


def parse_usage_limit(text: str) -> tuple[bool, str | None]:
    """Detect a usage-limit notice in worker output. Returns (is_limited, reset_iso_or_None).

    Best-effort and DELIBERATELY CONSERVATIVE (errs toward NOT flagging): a false 'limited' would
    strand a healthy account, so this matches only high-confidence "limit reached/exceeded ... reset
    at <time>" / "usage limit ... until <time>" shapes and WILL MISS looser phrasings (e.g. a bare
    "rate limit exceeded" with no reset time). The exact claude / codex limit-notice wording still
    needs calibration against real captures (WIRE-IN); a missed limit is cheap (the dispatch just
    fails and the account is retried), whereas a false limit wrongly cools an account off, so the
    conservative bias is intentional. A detected limit with no parseable time returns reset=None so
    the caller picks a cool-off.
    """
    for pat in _LIMIT_PATTERNS:
        m = pat.search(text or "")
        if m:
            when = m.groupdict().get("when")
            if when:
                try:
                    return True, _parse_iso(when.strip().replace(" ", "T", 1))
                except ValueError:
                    return True, None
            return True, None
    return False, None


# --- id minting --------------------------------------------------------------------
def mint_worker_id(account: str, family: str, now: _dt.datetime) -> str:
    """Fresh id per exec (decided 2026-07-26). Independence routing keys on (account, family),
    NOT this ephemeral id; the trust window keys on (account, model)."""
    stamp = now.astimezone(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{family}-{account}-{stamp}-{uuid.uuid4().hex[:4]}"


# --- in-flight registry helpers (reserve-under-lock; TODO 3.141) -------------------
def _pid_alive(pid: int) -> bool:
    """True if `pid` names a live process. os.kill(pid, 0) is the liveness probe: the
    dispatcher's OWN pid (os.getpid()) is the liveness token for its entry, since dispatch()
    blocks on subprocess.run for the whole job (so a live entry == a live dispatcher)."""
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False            # no such process -> dead
    except PermissionError:
        return True             # exists, owned by another uid
    except OSError:
        return False
    return True


class InflightCorruptError(Exception):
    """The registry FILE exists but is unreadable or malformed (unparseable JSON, non-list
    content, or a non-FileNotFound OSError) -- as distinct from simply ABSENT. Its message names
    the offending file. RESERVE must FAIL CLOSED on it (refuse the dispatch; a corrupt file read
    as empty would UNDER-COUNT in-flight jobs, a fail-open on the now-sole per-account concurrency
    cap -- TODO 3.145). RELEASE may ignore it (best-effort: pid-liveness reaping / operator
    cleanup handles the stale file, and a finished job must not crash on release)."""


def _read_inflight(job_dir: Path) -> list:
    """Load the registry list. A MISSING file -> [] (no registry yet == no in-flight jobs, the
    correct empty state; the very first dispatch depends on this). A present-but-CORRUPT file
    raises InflightCorruptError so callers can FAIL CLOSED rather than silently read it as empty
    and under-count in-flight jobs (TODO 3.145). Only ever called while holding the exclusive
    flock on INFLIGHT_LOCK_NAME."""
    path = job_dir / INFLIGHT_NAME
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        return []                                   # no registry yet -> no in-flight jobs
    except (ValueError, OSError) as exc:
        # ValueError covers json.JSONDecodeError (unparseable); OSError covers a non-FileNotFound
        # read failure (permissions, I/O error). FileNotFoundError is a subclass of OSError, so it
        # MUST be (and is) caught above first.
        raise InflightCorruptError(
            f"in-flight registry {path} is unreadable/corrupt "
            f"({exc.__class__.__name__}: {exc})") from exc
    if not isinstance(data, list) or not all(isinstance(e, dict) for e in data):
        # A JSON scalar/object is not a list; a list whose ELEMENTS are not objects (e.g. [1,2,3])
        # would pass the list check but then crash _reap with AttributeError on `e.get(...)`. Both
        # are corrupt: fail CLOSED (clean refuse) rather than crash. A well-formed entry is an object;
        # an object missing fields (e.g. no pid) still passes here and is dropped by _reap (benign).
        raise InflightCorruptError(
            f"in-flight registry {path} is malformed (expected a JSON list of objects, got "
            f"{type(data).__name__})")
    return data


def _write_inflight(job_dir: Path, entries: list) -> None:
    """Atomically replace the registry (write tmp + os.replace). Only ever called while
    holding the exclusive flock on INFLIGHT_LOCK_NAME (which is itself never rewritten)."""
    tmp = job_dir / (INFLIGHT_NAME + ".tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(entries, fh)
    os.replace(tmp, job_dir / INFLIGHT_NAME)


def _reap(entries: list, now_epoch: float) -> list:
    """Return only the live entries. Liveness = os.kill(pid, 0). The ONLY time-based rule is a
    24h absolute `started`-age ceiling (backstop against pid reuse) -- deliberately NOT mtime
    staleness, since a long healthy job never touches the registry and would be falsely reaped."""
    live = []
    for e in entries:
        try:
            pid = int(e.get("pid"))
            started = float(e.get("started", 0))
        except (TypeError, ValueError):
            continue                        # malformed -> drop
        if now_epoch - started > STALE_STARTED_AGE_S:
            continue                        # 24h ceiling backstop (pid-reuse guard)
        if not _pid_alive(pid):
            continue                        # dead dispatcher -> reap, freeing its slot
        live.append(e)
    return live


def _reserve_slot(job_dir: Path, key: str, max_concurrent: int, worker_id: str,
                  pid: int, now_epoch: float) -> tuple[bool, object]:
    """RESERVE a per-key concurrency slot in ONE exclusive flock critical section (no
    check-then-act TOCTOU): reap stale/dead entries -> count live for `key` -> if at/over
    max_concurrent REFUSE (return (False, message)); else append this job's entry, persist,
    and return (True, entry). The lock is held ONLY for this critical section, NEVER across
    the job's subprocess.run, so concurrent dispatchers do not serialize on the registry.

    FAILS CLOSED (TODO 3.145): if the registry file is present-but-CORRUPT, refuse the dispatch
    with an operator message naming the file to remove -- a corrupt file must NEVER read as empty
    and let a dispatch under-count in-flight jobs. The file is left in place (NOT overwritten) so
    the operator can inspect it; the next valid reserve recreates it once removed."""
    job_dir.mkdir(parents=True, exist_ok=True)
    with open(job_dir / INFLIGHT_LOCK_NAME, "a+") as lock_fh:
        fcntl.flock(lock_fh, fcntl.LOCK_EX)
        try:
            try:
                raw = _read_inflight(job_dir)
            except InflightCorruptError as exc:
                return False, (f"{exc}; refusing dispatch (fail-closed). Inspect and remove "
                               f"{job_dir / INFLIGHT_NAME} to clear -- a valid reserve recreates "
                               f"it.")
            entries = _reap(raw, now_epoch)
            live_for_key = sum(1 for e in entries if e.get("key") == key)
            if live_for_key >= max_concurrent:
                _write_inflight(job_dir, entries)          # persist the reap
                return False, (f"at capacity for '{key}': {live_for_key}/{max_concurrent} "
                               f"in-flight (refusing dispatch)")
            entry = {"key": key, "pid": pid, "worker_id": worker_id, "started": now_epoch}
            entries.append(entry)
            _write_inflight(job_dir, entries)
            return True, entry
        finally:
            fcntl.flock(lock_fh, fcntl.LOCK_UN)


def _release_slot(job_dir: Path, worker_id: str) -> None:
    """Remove this job's entry (matched by worker_id) under the same exclusive lock, so a
    normal completion frees the slot immediately. Best-effort: a leaked entry (e.g. hard kill
    before release) is backstopped by pid-liveness reaping on the next reserve.

    Tolerates a CORRUPT registry (TODO 3.145): a finished job must not crash on release, and a
    corrupt file cannot be safely rewritten (we'd clobber live entries we could not parse), so
    on corruption release is a no-op -- the operator-facing refusal from the next RESERVE, plus
    pid-liveness reaping once the file is restored, handle cleanup."""
    try:
        with open(job_dir / INFLIGHT_LOCK_NAME, "a+") as lock_fh:
            fcntl.flock(lock_fh, fcntl.LOCK_EX)
            try:
                try:
                    entries = _read_inflight(job_dir)
                except InflightCorruptError:
                    return                          # best-effort: leave the file for the operator
                _write_inflight(job_dir, [e for e in entries
                                          if e.get("worker_id") != worker_id])
            finally:
                fcntl.flock(lock_fh, fcntl.LOCK_UN)
    except OSError:
        pass


def _max_concurrent(acct: dict) -> int:
    """Per-key concurrency cap. ABSENT -> 1 (byte-equivalent to today's single-slot behavior);
    a present but non-positive/unparseable value also floors at 1."""
    try:
        mc = int(acct.get("max_concurrent", 1))
    except (TypeError, ValueError):
        mc = 1
    return mc if mc >= 1 else 1


def _inflight_key(acct: dict) -> str:
    """Registry key = the config-dir unit `id` (unique per account+family, so a claude job and
    a codex job for the same subscription have DISTINCT keys/caps), NOT the bare account name;
    fall back to `account` only if `id` is absent."""
    return acct.get("id") or acct.get("account")


def build_dispatch_cmd(wrapper: str, prompt_file: str, account: str, model: str,
                       worker_id: str, effort: str | None = None) -> list:
    """Build the sudo wrapper argv. --worker-id is now passed through to the (already
    backward-compatible) root-owned wrapper, whose charset requirement [A-Za-z0-9_-] the
    minted worker ids satisfy."""
    cmd = ["sudo", "-n", "-u", WORKER_USER, wrapper, prompt_file,
           "--account", account, "--model", model, "--worker-id", worker_id]
    if effort:
        cmd += ["--effort", effort]
    return cmd


# --- dispatch (the thin shell) -----------------------------------------------------
def dispatch(config: dict, family: str, model: str, order_id: str, prompt_file: str,
             effort: str | None = None, now: _dt.datetime | None = None,
             account: str | None = None, job_dir: Path = JOB_DIR) -> dict:
    now = now or _dt.datetime.now(_dt.timezone.utc)
    acct, reason = pick_account(config, family, model, now, account)
    if acct is None:
        return {"ok": False, "error": reason, "family": family, "model": model,
                "requested_account": account}
    wrapper = WRAPPER[family]
    worker_id = mint_worker_id(acct["account"], family, now)
    cmd = build_dispatch_cmd(wrapper, prompt_file, acct["account"], model, worker_id, effort)

    # RESERVE a per-key concurrency slot under the in-flight lock BEFORE running (no TOCTOU).
    # A refusal returns WITHOUT a worker_id so the CLI surfaces it via the existing
    # "NOT DISPATCHED" path (loud, non-zero exit) rather than as a completed-job status line.
    # This path ALSO carries the TODO 3.145 fail-closed refusal on a corrupt registry.
    key = _inflight_key(acct)
    max_conc = _max_concurrent(acct)
    ok, slot = _reserve_slot(job_dir, key, max_conc, worker_id, os.getpid(), now.timestamp())
    if not ok:
        return {"ok": False, "error": slot, "family": family, "model": model,
                "requested_account": account, "refused": True,
                "key": key, "max_concurrent": max_conc}

    try:
        started = time.time()
        proc = subprocess.run(cmd, capture_output=True, text=True)
        dur = time.time() - started
    finally:
        _release_slot(job_dir, worker_id)       # free the slot on the EXIT path
    limited, reset = parse_usage_limit(proc.stdout + proc.stderr)
    return {
        "ok": proc.returncode == 0,
        "worker_id": worker_id,
        "account": acct["account"],
        "family": family,
        "model": model,
        "order_id": order_id,
        "rc": proc.returncode,
        "duration_s": round(dur, 1),
        "usage_limited": limited,
        "usage_reset": reset.isoformat() if reset else None,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


# --- self-test ---------------------------------------------------------------------
_FIXTURE = {
    "accounts": [
        {"id": "work-a-claude", "account": "work-a", "family": "claude",
         "tier": "pro-team", "priority_set": 1, "personal": False,
         "models": ["opus", "sonnet", "haiku"], "usage_state": "available", "limited_until": None},
        {"id": "work-b-claude", "account": "work-b", "family": "claude",
         "tier": "pro-team", "priority_set": 1, "personal": False,
         "models": ["opus", "sonnet", "haiku"], "usage_state": "available", "limited_until": None},
        {"id": "personal-a-claude", "account": "personal-a", "family": "claude",
         "tier": "personal", "priority_set": 2, "personal": True,
         "models": ["opus", "sonnet", "haiku"], "usage_state": "limited",
         "limited_until": "2026-07-29T04:59:00-04:00"},
        {"id": "personal-b-claude", "account": "personal-b", "family": "claude",
         "tier": "pro-20x", "priority_set": 3, "personal": True,
         "models": ["opus", "sonnet", "haiku"], "usage_state": "available", "limited_until": None},
        {"id": "personal-b-codex", "account": "personal-b", "family": "codex",
         "tier": "pro-20x", "priority_set": 1, "personal": False,
         "models": ["gpt-5.6-terra"], "usage_state": "available", "limited_until": None},
        {"id": "personal-a-codex", "account": "personal-a", "family": "codex",
         "tier": "teams-6.5x", "priority_set": 2, "personal": False,
         "models": ["gpt-5.6-terra"], "usage_state": "available", "limited_until": None},
    ]
}


def _self_test() -> int:
    fails = []
    ran = []

    def check(name, cond):
        ran.append(name)
        if not cond:
            fails.append(name)

    sunday = _parse_iso("2026-07-26T18:00:00+00:00")   # before Wed reset
    thursday = _parse_iso("2026-07-30T18:00:00+00:00")  # after Wed reset

    # 1. personal-a claude is EXCLUDED while limited (the maintainer's core case).
    elig = eligible_accounts(_FIXTURE, "claude", "opus", sunday)
    ids = [a["id"] for a in elig]
    check("worklimited-excluded-while-limited", "personal-a-claude" not in ids)

    # 2. A work (non-personal, set 1) account is picked first, never the orchestrator's own.
    pick = select_account(_FIXTURE, "claude", "opus", sunday)
    check("work-account-picked-first", pick["id"] in ("work-a-claude", "work-b-claude"))
    check("orchestrator-not-first", pick["id"] != "personal-b-claude")

    # 3. Orchestrator's own account (personal, set 3) is LAST among eligible.
    check("orchestrator-last", ids[-1] == "personal-b-claude")

    # 4. Past the reset window, personal-a becomes eligible again.
    ids_thu = [a["id"] for a in eligible_accounts(_FIXTURE, "claude", "opus", thursday)]
    check("worklimited-eligible-after-reset", "personal-a-claude" in ids_thu)

    # 5. Model filter actually discriminates: a real model offered only by the OTHER family (a codex
    #    model requested for the claude family) is filtered out because no claude account lists it.
    #    (This exercises the `model not in acct.models` branch, unlike the family invariant.)
    check("model-filter-excludes-wrong-family-model",
          eligible_accounts(_FIXTURE, "claude", "gpt-5.6-terra", sunday) == [])

    # 6. Codex: primary (personal-b, set 1) before secondary (personal-a, set 2).
    cod = [a["id"] for a in eligible_accounts(_FIXTURE, "codex", "gpt-5.6-terra", sunday)]
    check("codex-primary-first", cod == ["personal-b-codex", "personal-a-codex"])

    # 7. A model no account offers -> empty.
    check("unknown-model-empty", select_account(_FIXTURE, "claude", "no-such-model", sunday) is None)

    # 8. Usage-limit parser: detects a notice, and no-notice text is clean.
    lim, _ = parse_usage_limit("Error: usage limit reached, resets at 2026-07-29T04:59:00")
    check("limit-detected", lim is True)
    lim2, _ = parse_usage_limit("PONG")
    check("no-false-limit", lim2 is False)
    # 9. Regression (verifier #1185 Finding 3): benign prose that merely quotes "limit" is NOT flagged.
    lim3, _ = parse_usage_limit("the article notes you've reached your monthly limit of free views")
    check("no-false-limit-benign-prose", lim3 is False)

    # 10. Account override: no override picks the top eligible (same as select_account).
    a_auto, _ = pick_account(_FIXTURE, "claude", "opus", sunday)
    check("override-none-picks-top", a_auto is not None and a_auto["id"] == "work-a-claude")
    # 11. Targeting an eligible NON-top account returns exactly it (the parallelism case).
    a_sec, r_sec = pick_account(_FIXTURE, "claude", "opus", sunday, account="work-b")
    check("override-targets-eligible", a_sec is not None and a_sec["id"] == "work-b-claude")
    # 12. Targeting the personal account (eligible but auto-picked LAST) still works when named.
    a_mz, _ = pick_account(_FIXTURE, "claude", "opus", sunday, account="personal-b")
    check("override-targets-personal", a_mz is not None and a_mz["id"] == "personal-b-claude")
    # 13. Targeting a KNOWN-but-ineligible account (limited personal-a) is REJECTED with a reason.
    a_lim, r_lim = pick_account(_FIXTURE, "claude", "opus", sunday, account="personal-a")
    check("override-rejects-ineligible", a_lim is None and "NOT eligible" in r_lim)
    # 14. Targeting an UNKNOWN account is rejected and distinguished from ineligible.
    a_unk, r_unk = pick_account(_FIXTURE, "claude", "opus", sunday, account="no-such-acct")
    check("override-rejects-unknown", a_unk is None and "not in the config" in r_unk)
    # 15. The same account name across families resolves by FAMILY (personal-b has claude AND codex).
    a_cod, _ = pick_account(_FIXTURE, "codex", "gpt-5.6-terra", sunday, account="personal-b")
    check("override-resolves-by-family", a_cod is not None and a_cod["id"] == "personal-b-codex")

    # --- in-flight registry (TODO 3.141): reserve-under-lock, reaping, --worker-id ------
    import tempfile as _tempfile

    def _dead_pid():
        # A pid guaranteed absent: probe downward from an out-of-range value until os.kill
        # reports it dead. Deterministic and side-effect-free (never signals a live process).
        p = 2 ** 22
        while p > 1:
            if not _pid_alive(p):
                return p
            p -= 1
        return 999999

    now_epoch = sunday.timestamp()
    me = os.getpid()

    with _tempfile.TemporaryDirectory() as _td:
        jd = Path(_td)
        # 16. Below cap -> ALLOWED (slot reserved), returns the entry dict.
        ok1, e1 = _reserve_slot(jd, "work-a-claude", 2, "wid-1", me, now_epoch)
        check("inflight-allow-below-cap", ok1 is True and isinstance(e1, dict))
        # 17. Second reserve for the SAME key at cap=2 -> still allowed (now 2/2).
        ok2, _ = _reserve_slot(jd, "work-a-claude", 2, "wid-2", me, now_epoch)
        check("inflight-allow-to-cap", ok2 is True)
        # 18. Third reserve for the same key -> REFUSED (2/2 in-flight, cap=2), clear message.
        ok3, msg3 = _reserve_slot(jd, "work-a-claude", 2, "wid-3", me, now_epoch)
        check("inflight-refuse-at-cap", ok3 is False and "at capacity" in str(msg3))
        # 19. A DIFFERENT key (distinct config-dir unit) is unaffected -> allowed.
        okX, _ = _reserve_slot(jd, "work-b-claude", 1, "wid-x", me, now_epoch)
        check("inflight-key-isolation", okX is True)
        # 20. Releasing an entry frees a slot for that key -> a new reserve is allowed.
        _release_slot(jd, "wid-1")
        ok4, _ = _reserve_slot(jd, "work-a-claude", 2, "wid-4", me, now_epoch)
        check("inflight-release-frees-slot", ok4 is True)

    # 21. A dead-pid entry is REAPED, freeing the slot; only the live reservation remains.
    with _tempfile.TemporaryDirectory() as _td:
        jd = Path(_td)
        _write_inflight(jd, [{"key": "k", "pid": _dead_pid(), "worker_id": "old",
                              "started": now_epoch}])
        okd, _ = _reserve_slot(jd, "k", 1, "new", me, now_epoch)
        check("inflight-reaps-dead-pid", okd is True)
        check("inflight-dead-entry-removed",
              [e["worker_id"] for e in _read_inflight(jd)] == ["new"])

    # 22. The 24h started-age ceiling reaps even a LIVE-pid entry (pid-reuse backstop).
    with _tempfile.TemporaryDirectory() as _td:
        jd = Path(_td)
        _write_inflight(jd, [{"key": "k", "pid": me, "worker_id": "ancient",
                              "started": now_epoch - (STALE_STARTED_AGE_S + 60)}])
        oka, _ = _reserve_slot(jd, "k", 1, "fresh", me, now_epoch)
        check("inflight-24h-ceiling-reaps", oka is True)

    # 23. A healthy long-running entry (live pid, recent start) is NOT reaped -> still refused.
    with _tempfile.TemporaryDirectory() as _td:
        jd = Path(_td)
        _write_inflight(jd, [{"key": "k", "pid": me, "worker_id": "healthy",
                              "started": now_epoch}])
        okh, msgh = _reserve_slot(jd, "k", 1, "intruder", me, now_epoch)
        check("inflight-healthy-not-reaped", okh is False and "at capacity" in str(msgh))

    # --- 3.145: registry read fails CLOSED on a CORRUPT file, but a MISSING file still allows ---
    with _tempfile.TemporaryDirectory() as _td:
        jd = Path(_td)
        # 24. A MISSING registry reads as [] (no registry yet == no in-flight jobs) and RESERVE
        #     ALLOWS -- the first-ever dispatch MUST NOT refuse (regression guard for the fix).
        check("inflight-missing-reads-empty", _read_inflight(jd) == [])
        okm, _ = _reserve_slot(jd, "k", 1, "wid-m", me, now_epoch)
        check("inflight-missing-allows-reserve", okm is True)

    with _tempfile.TemporaryDirectory() as _td:
        jd = Path(_td)
        # 25. A present-but-CORRUPT registry (unparseable JSON) makes _read_inflight RAISE
        #     (fail-closed signal), NOT silently read as empty.
        (jd / INFLIGHT_NAME).write_text("{not valid json", encoding="utf-8")
        raised = False
        try:
            _read_inflight(jd)
        except InflightCorruptError:
            raised = True
        check("inflight-corrupt-raises", raised is True)
        # 26. RESERVE FAILS CLOSED on the corrupt file: REFUSE (not allow), message names the file.
        okc, msgc = _reserve_slot(jd, "k", 1, "wid-c", me, now_epoch)
        check("inflight-corrupt-refuses-reserve",
              okc is False and INFLIGHT_NAME in str(msgc))
        # 27. RELEASE tolerates the corrupt file (best-effort): no crash, file LEFT for the operator.
        _release_slot(jd, "wid-c")      # must not raise
        check("inflight-corrupt-release-tolerated", (jd / INFLIGHT_NAME).exists())

    with _tempfile.TemporaryDirectory() as _td:
        jd = Path(_td)
        # 28. Non-list content (valid JSON, wrong shape) is ALSO corrupt -> RESERVE refuses.
        (jd / INFLIGHT_NAME).write_text('{"pid": 1}', encoding="utf-8")
        okn, msgn = _reserve_slot(jd, "k", 1, "wid-n", me, now_epoch)
        check("inflight-nonlist-refuses-reserve", okn is False and "malformed" in str(msgn))

    with _tempfile.TemporaryDirectory() as _td:
        jd = Path(_td)
        # 29. A JSON LIST whose ELEMENTS are not objects ([1,2,3]) is corrupt -> RESERVE refuses,
        # rather than crashing _reap with AttributeError on `e.get(...)`. Reality fixture for the
        # scalar-list gap the codex adversarial verifier caught (2026-07-27).
        (jd / INFLIGHT_NAME).write_text('[1, 2, 3]', encoding="utf-8")
        oks, msgs = _reserve_slot(jd, "k", 1, "wid-s", me, now_epoch)
        check("inflight-scalar-list-refuses-reserve", oks is False and "malformed" in str(msgs))
        _release_slot(jd, "wid-s")      # RELEASE tolerates it too (no crash)
        check("inflight-scalar-list-release-tolerated", (jd / INFLIGHT_NAME).exists())

    # 30. build_dispatch_cmd passes --worker-id with the minted id (the wrapper wire-in).
    wid = mint_worker_id("work-a", "claude", sunday)
    cmd = build_dispatch_cmd(WRAPPER["claude"], "/tmp/p.txt", "work-a", "opus", wid)
    check("worker-id-in-cmd",
          "--worker-id" in cmd and cmd[cmd.index("--worker-id") + 1] == wid)
    # 30. --effort is still appended (existing behavior preserved), after --worker-id.
    cmd2 = build_dispatch_cmd(WRAPPER["claude"], "/tmp/p.txt", "work-a", "opus", wid, effort="high")
    check("effort-still-passed", cmd2[-2:] == ["--effort", "high"])
    # 31. The minted worker id satisfies the wrapper charset [A-Za-z0-9_-].
    check("worker-id-charset", _re.fullmatch(r"[A-Za-z0-9_-]+", wid) is not None)
    # 32. max_concurrent ABSENT -> default 1 (byte-equivalent to today); present value honored.
    check("max-concurrent-default-1", _max_concurrent({"id": "x"}) == 1)
    check("max-concurrent-explicit", _max_concurrent({"id": "x", "max_concurrent": 3}) == 3)

    if fails:
        print("SELF-TEST FAIL:", ", ".join(fails))
        return 1
    print(f"exec-dispatch self-test: OK ({len(ran)} checks)")
    return 0


# --- cli ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description="exec'd worker dispatch")
    ap.add_argument("--config", default=str(DEFAULT_CONFIG))
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="show eligible accounts + pick, no dispatch")
    ap.add_argument("--dispatch", action="store_true", help="actually run the job via the wrapper")
    ap.add_argument("--family", choices=["claude", "codex"])
    ap.add_argument("--model")
    ap.add_argument("--effort", choices=["low", "medium", "high", "xhigh"],
                    help="claude: --effort; codex: mapped to model_reasoning_effort (wrapper WIRE-IN)")
    ap.add_argument("--order-id")
    ap.add_argument("--prompt-file")
    ap.add_argument("--account", help="target a SPECIFIC account (must be eligible), instead of the "
                    "auto-pick; use distinct accounts across concurrent dispatches for real "
                    "parallelism (same-account jobs serialize on the wrapper flock)")
    args = ap.parse_args()

    if args.self_test:
        return _self_test()

    config = load_config(Path(args.config))
    now = _dt.datetime.now(_dt.timezone.utc)

    if args.dry_run:
        if not (args.family and args.model):
            ap.error("--dry-run needs --family and --model")
        elig = eligible_accounts(config, args.family, args.model, now)
        if args.account:
            acct, reason = pick_account(config, args.family, args.model, now, args.account)
            print(f"[{now.astimezone().strftime('%H:%M:%S')}] --account {args.account}: "
                  f"{'PICK ' + acct['id'] if acct else 'REJECTED'} ({reason})")
        print(f"[{now.astimezone().strftime('%H:%M:%S')}] eligible {args.family}/{args.model} "
              f"(now={now.isoformat()}):")
        for i, a in enumerate(elig):
            # With --account, the PICK marker belongs on the TARGETED row, not the auto-pick top row
            # (verify-1187 F-1: a hard-coded i==0 marker contradicted an eligible non-top target).
            is_pick = (a.get("account") == args.account) if args.account else (i == 0)
            tag = "  <-- PICK" if is_pick else ""
            print(f"  {i+1}. {a['id']:24s} set={a.get('priority_set')} "
                  f"tier={a.get('tier')} personal={a.get('personal')}{tag}")
        # show who was excluded and why
        for a in config.get("accounts", []):
            if a.get("family") != args.family or args.model not in a.get("models", []):
                continue
            ok, reason = account_available(a, now)
            if not ok:
                print(f"  --  EXCLUDED {a.get('id'):24s} {reason}")
        if not elig:
            print("  (no eligible account)")
        return 0

    if args.dispatch:
        for req in ("family", "model", "order_id", "prompt_file"):
            if not getattr(args, req):
                ap.error(f"--dispatch needs --{req.replace('_','-')}")
        res = dispatch(config, args.family, args.model, args.order_id, args.prompt_file,
                       effort=args.effort, now=now, account=args.account)
        if not res["ok"] and res.get("worker_id") is None:
            # account resolution failed before any worker ran: surface the reason loudly.
            print(f"[{_dt.datetime.now().strftime('%H:%M:%S')}] dispatch order={args.order_id} "
                  f"NOT DISPATCHED: {res.get('error')}", file=sys.stderr)
            return 1
        # print a compact status line, then the worker output
        print(f"[{_dt.datetime.now().strftime('%H:%M:%S')}] dispatch order={res.get('order_id')} "
              f"worker={res.get('worker_id')} account={res.get('account')} model={args.model} "
              f"effort={args.effort or 'default'} rc={res.get('rc')} dur={res.get('duration_s')}s "
              f"limited={res.get('usage_limited')}")
        if res.get("stdout"):
            sys.stdout.write(res["stdout"])
        if not res["ok"] and res.get("stderr"):
            sys.stderr.write(res["stderr"])
        return 0 if res["ok"] else 1

    ap.error("choose one of --self-test / --dry-run / --dispatch")
    return 2


if __name__ == "__main__":
    sys.exit(main())
