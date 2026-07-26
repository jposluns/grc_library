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


# --- dispatch (the thin shell) -----------------------------------------------------
def dispatch(config: dict, family: str, model: str, order_id: str, prompt_file: str,
             effort: str | None = None, now: _dt.datetime | None = None) -> dict:
    now = now or _dt.datetime.now(_dt.timezone.utc)
    acct = select_account(config, family, model, now)
    if acct is None:
        return {"ok": False, "error": "no eligible account", "family": family, "model": model}
    wrapper = WRAPPER[family]
    worker_id = mint_worker_id(acct["account"], family, now)
    cmd = ["sudo", "-n", "-u", WORKER_USER, wrapper, prompt_file,
           "--account", acct["account"], "--model", model]
    if effort:
        cmd += ["--effort", effort]
    started = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    dur = time.time() - started
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
        {"id": "jposluns-work-claude", "account": "jposluns-work", "family": "claude",
         "tier": "pro-team", "priority_set": 1, "personal": False,
         "models": ["opus", "sonnet", "haiku"], "usage_state": "available", "limited_until": None},
        {"id": "security-work-claude", "account": "security-work", "family": "claude",
         "tier": "pro-team", "priority_set": 1, "personal": False,
         "models": ["opus", "sonnet", "haiku"], "usage_state": "available", "limited_until": None},
        {"id": "jeff-posluns-claude", "account": "jeff-posluns", "family": "claude",
         "tier": "personal", "priority_set": 2, "personal": True,
         "models": ["opus", "sonnet", "haiku"], "usage_state": "limited",
         "limited_until": "2026-07-29T04:59:00-04:00"},
        {"id": "jeff-mailz-claude", "account": "jeff-mailz", "family": "claude",
         "tier": "pro-20x", "priority_set": 3, "personal": True,
         "models": ["opus", "sonnet", "haiku"], "usage_state": "available", "limited_until": None},
        {"id": "jeff-mailz-codex", "account": "jeff-mailz", "family": "codex",
         "tier": "pro-20x", "priority_set": 1, "personal": False,
         "models": ["gpt-5.6-terra"], "usage_state": "available", "limited_until": None},
        {"id": "jeff-posluns-codex", "account": "jeff-posluns", "family": "codex",
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

    # 1. jeff-posluns claude is EXCLUDED while limited (the maintainer's core case).
    elig = eligible_accounts(_FIXTURE, "claude", "opus", sunday)
    ids = [a["id"] for a in elig]
    check("posluns-excluded-while-limited", "jeff-posluns-claude" not in ids)

    # 2. A work (non-personal, set 1) account is picked first, never the orchestrator's own.
    pick = select_account(_FIXTURE, "claude", "opus", sunday)
    check("work-account-picked-first", pick["id"] in ("jposluns-work-claude", "security-work-claude"))
    check("orchestrator-not-first", pick["id"] != "jeff-mailz-claude")

    # 3. Orchestrator's own account (personal, set 3) is LAST among eligible.
    check("orchestrator-last", ids[-1] == "jeff-mailz-claude")

    # 4. Past the reset window, jeff-posluns becomes eligible again.
    ids_thu = [a["id"] for a in eligible_accounts(_FIXTURE, "claude", "opus", thursday)]
    check("posluns-eligible-after-reset", "jeff-posluns-claude" in ids_thu)

    # 5. Model filter actually discriminates: a real model offered only by the OTHER family (a codex
    #    model requested for the claude family) is filtered out because no claude account lists it.
    #    (This exercises the `model not in acct.models` branch, unlike the family invariant.)
    check("model-filter-excludes-wrong-family-model",
          eligible_accounts(_FIXTURE, "claude", "gpt-5.6-terra", sunday) == [])

    # 6. Codex: primary (jeff-mailz, set 1) before secondary (jeff-posluns, set 2).
    cod = [a["id"] for a in eligible_accounts(_FIXTURE, "codex", "gpt-5.6-terra", sunday)]
    check("codex-primary-first", cod == ["jeff-mailz-codex", "jeff-posluns-codex"])

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
    args = ap.parse_args()

    if args.self_test:
        return _self_test()

    config = load_config(Path(args.config))
    now = _dt.datetime.now(_dt.timezone.utc)

    if args.dry_run:
        if not (args.family and args.model):
            ap.error("--dry-run needs --family and --model")
        elig = eligible_accounts(config, args.family, args.model, now)
        print(f"[{now.astimezone().strftime('%H:%M:%S')}] eligible {args.family}/{args.model} "
              f"(now={now.isoformat()}):")
        for i, a in enumerate(elig):
            tag = "  <-- PICK" if i == 0 else ""
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
                       effort=args.effort, now=now)
        # print a compact status line, then the worker output
        print(f"[{_dt.datetime.now().strftime('%H:%M:%S')}] dispatch order={res.get('order_id')} "
              f"worker={res.get('worker_id')} model={args.model} effort={args.effort or 'default'} "
              f"rc={res.get('rc')} dur={res.get('duration_s')}s limited={res.get('usage_limited')}")
        if res.get("stdout"):
            sys.stdout.write(res["stdout"])
        if not res["ok"] and res.get("stderr"):
            sys.stderr.write(res["stderr"])
        return 0 if res["ok"] else 1

    ap.error("choose one of --self-test / --dry-run / --dispatch")
    return 2


if __name__ == "__main__":
    sys.exit(main())
