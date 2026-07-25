#!/usr/bin/env python3
"""Send one of a CLOSED SET of prompts to a worker's tmux session, gated and logged.

WHY TMUX AND NOT A SOCKET. A worker's agent CLI reads its TTY. A unix socket would move
bytes that nothing reads, which is why the file-drop control plane can signal a reload but
cannot wake an idle turn (the codex continuation brief, 2026-07-25). ``tmux send-keys`` writes
the pane's TTY, so it is indistinguishable from typing. The panes were created on the
ORCHESTRATOR'S OWN account and each then ran ``su - <worker-user>`` inside, so the su'd shell is
the pane's FOREGROUND PROCESS while the pane and its TTY belong to the tmux SERVER, which runs
as the orchestrator's own account. No privilege escalation is involved or possible here.

WHY A CLOSED SET. Every prompt is a CONSTANT in this file. Nothing is ever parameterised from
worker output, so a worker cannot steer what is sent to it: prompt-injection is structurally
impossible rather than policy-dependent. Adding a verb is a code change, reviewable as such.

WHY LOGGED. Keystroke injection into a session running as another user is an invisible action
unless recorded. The project has one such class already fixed (an unlogged branch-protection
bypass, 2026-07-25); this does not create a second.

OBSERVED BEHAVIOUR, from the first live send (2026-07-25T14:05Z, `wake` to a Claude worker):

- **Claude QUEUES a message injected mid-turn** rather than corrupting the running turn: the pane
  showed "Press up to edit queued messages" and the worker went from stale to LIVE once its turn
  finished. So a NON-DESTRUCTIVE verb is safe to send regardless of pane state, which is why this
  tool does not gate `wake`, `reload` or `stand-down` on idleness.
- **A visible prompt marker does NOT mean idle.** The pane showed the `❯` prompt while a turn was
  in flight. The reliable busy tell is ``esc to interrupt`` appearing in the status line; the
  prompt marker appears in both states. This is why the maintainer's instruction not to poll for
  prompt markers was right, and why the Codex wake text is self-deferring instead.
- A DESTRUCTIVE verb is still gated, because a queued ``/clear`` would execute after the current
  turn and destroy whatever context that turn produced.

PER-RUNTIME, AND NEVER GUESSED. Claude has a ``/credit-offload`` command file carrying its whole
serve loop, so its wake is a single token. Codex has NO such command: per its own recommendation
its workflow is an on-disk contract plus a normal task prompt, so its wake is prose. The Codex
wake text is deliberately SELF-DEFERRING ("at your next opportunity"), which is what makes it
safe to send without pane-state detection: an instruction that defers itself cannot corrupt work
in progress the way an imperative injected mid-turn could.
"""
from __future__ import annotations

import argparse
import datetime
import getpass
import os
import re
import subprocess
import sys
from pathlib import Path

LOG_REL = ".working/worker-prompt-log.md"

# The orchestrator's OWN session. Sending here would be the orchestrator prompting itself,
# which is a footgun with no legitimate use, so it is refused unconditionally.
ORCHESTRATOR_SESSIONS = {"grc"}

# session name -> runtime. Explicit rather than sniffed from the pane: pane markers appear in
# scrollback and output too, so sniffing has a false-positive mode a static map does not.
RUNTIME_MAP = {"worker": "claude", "worker1": "claude", "mailz": "codex"}

# The closed set. Values are literal keystroke sequences; a tuple sends in order, and a float
# member is a delay in seconds between sends.
VERBS = {
    "wake": {
        "claude": ("/credit-offload",),
        # Maintainer-specified 2026-07-25. Self-deferring by design, so it is safe mid-turn.
        "codex": ("At your next opportunity, resync your grc_library_scratch clone and check in: "
                  "claim the next waiting order in your family if you are not already working.",),
    },
    "reload": {
        "claude": ("When you finish your current task, re-read your worker contract at "
                   "grc_library_scratch/AGENTS.md and your skills, then continue.",),
        "codex": ("When you finish your current task, re-read your worker contract at "
                  "grc_library_scratch/AGENTS.md and your skills, then continue.",),
    },
    "restart": {
        # /clear is fast and local; a fixed generous delay beats polling for a prompt marker,
        # because a marker can appear inside captured output and produce a false ready.
        "claude": ("/clear", 10.0, "/credit-offload"),
        "codex": ("/clear", 10.0,
                  "Resync your grc_library_scratch clone, re-read AGENTS.md, then claim the "
                  "next waiting order in your family."),
    },
    "stand-down": {
        "claude": ("Finish your current task and deliver it, then claim nothing further until "
                   "told otherwise.",),
        "codex": ("Finish your current task and deliver it, then claim nothing further until "
                  "told otherwise.",),
    },
}

# Verbs that destroy context, so they require the worker to hold NO order.
DESTRUCTIVE = {"restart"}


def sh(*args) -> tuple:
    r = subprocess.run(args, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def tmux_sessions() -> list:
    rc, out, _ = sh("tmux", "list-sessions", "-F", "#{session_name}")
    return sorted(out.split()) if rc == 0 else []


def pane_tail(session: str, lines: int = 4) -> str:
    rc, out, _ = sh("tmux", "capture-pane", "-p", "-t", session)
    if rc != 0:
        return ""
    return "\n".join(out.rstrip().splitlines()[-lines:])


def held_orders(root: Path | None) -> dict:
    """worker-id -> held order id, read from the file-drop inboxes.

    The AUTHORITATIVE half of the gate. A pane can look idle while an order is held (that is
    exactly the stalled-mid-task case), so held-state must come from the exchange, never from
    the pane and never from the worker's self-report.
    """
    held = {}
    if root is None:
        return held
    for fam in ("opus", "codex", "fable"):
        base = root / fam / "inbox"
        if not base.is_dir():
            continue
        for wdir in base.iterdir():
            if not wdir.is_dir():
                continue
            for p in wdir.glob("*.md"):
                held[wdir.name] = p.stem
    return held


def working_root(explicit: str | None) -> Path | None:
    for cand in (explicit, os.environ.get("GRC_WORKING"), "/home/grc/grc_working"):
        if cand and Path(cand).is_dir():
            return Path(cand)
    return None


def log_send(repo: Path, session: str, runtime: str, verb: str, keys, reason: str,
             held: str | None) -> None:
    p = repo / LOG_REL
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(
            "# Worker prompt log\n\n"
            "Every prompt the orchestrator injected into a worker's tmux session, one row each.\n\n"
            "Keystroke injection into a session running as another user is invisible unless\n"
            "recorded, so it is recorded. Only the closed verb set in `tools/manage-workers.py`\n"
            "can appear in the verb column; nothing here is ever composed from worker output.\n\n"
            "| UTC | session | runtime | verb | held order | reason | keys sent |\n"
            "| --- | --- | --- | --- | --- | --- | --- |\n")
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sent = " THEN ".join(k if isinstance(k, str) else f"wait {k}s" for k in keys)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(f"| {stamp} | {session} | {runtime} | {verb} | {held or 'none'} | "
                 f"{reason} | `{sent[:160]}` |\n")


def do_list(root: Path | None) -> int:
    held = held_orders(root)
    sessions = tmux_sessions()
    if not sessions:
        print("manage-workers: no tmux sessions visible; nothing to report.")
        return 0
    print(f"{'session':10s} {'runtime':8s} {'pane':6s} {'held order':34s} tail")
    for s in sessions:
        rt = "ORCH" if s in ORCHESTRATOR_SESSIONS else RUNTIME_MAP.get(s, "unmapped")
        # a session name is not a worker id, so match on prefix (worker ids are minted per run)
        h = next((v for k, v in held.items() if k.startswith(s) or s in k), None)
        cap = pane_tail(s, 6)
        # "esc to interrupt" is Claude's busy tell; the prompt marker shows in BOTH states, so
        # it is useless as a discriminator (observed 2026-07-25). Advisory only: no verb gates
        # on it, because Claude queues injected messages safely.
        busy = "busy" if "esc to interrupt" in cap else "idle?"
        tail = pane_tail(s, 1).replace("\n", " ")[:46]
        print(f"{s:10s} {rt:8s} {busy:6s} {(h or '-'):34s} {tail}")
    if root is None:
        print("\n  note: no file-drop root resolved, so held-order state is UNKNOWN, not none.")
    return 0


def do_send(repo: Path, root: Path | None, session: str, verb: str, reason: str,
            force: bool, dry_run: bool) -> int:
    if session in ORCHESTRATOR_SESSIONS:
        print(f"REFUSED: '{session}' is the orchestrator's own session. Sending here would be "
              "the orchestrator prompting itself.")
        return 1
    if session not in tmux_sessions():
        print(f"REFUSED: no tmux session named '{session}'.")
        return 1
    runtime = RUNTIME_MAP.get(session)
    if runtime is None:
        print(f"REFUSED: '{session}' has no runtime mapping in RUNTIME_MAP, so the correct "
              "prompt shape is unknown. Add it rather than guessing: Claude and Codex differ "
              "(Codex has no /credit-offload equivalent).")
        return 1
    keys = VERBS.get(verb, {}).get(runtime)
    if keys is None:
        print(f"REFUSED: verb '{verb}' has no defined sequence for runtime '{runtime}'.")
        return 1
    held = held_orders(root)
    h = next((v for k, v in held.items() if k.startswith(session) or session in k), None)
    if verb in DESTRUCTIVE and h and not force:
        print(f"REFUSED {verb} on '{session}': it holds order '{h}', and {verb} destroys "
              "context, so in-flight work would be lost. Wait for delivery, or reclaim the "
              "order first. --force overrides.")
        return 1
    if root is None and verb in DESTRUCTIVE and not force:
        print(f"REFUSED {verb} on '{session}': no file-drop root resolved, so held-order state "
              "is UNKNOWN rather than none. A destructive verb must not proceed on an unknown "
              "gate. --force overrides.")
        return 1
    if not reason:
        print("REFUSED: --reason is required, because the log is the only record that this "
              "happened at all.")
        return 1
    for k in keys:
        if isinstance(k, float):
            print(f"  (wait {k}s)")
            if not dry_run:
                import time
                time.sleep(k)
            continue
        if dry_run:
            print(f"  WOULD SEND to {session}: {k[:110]}")
            continue
        rc, _, err = sh("tmux", "send-keys", "-t", session, k, "Enter")
        if rc != 0:
            print(f"send-keys FAILED on '{session}': {err.strip()}")
            return 1
        print(f"  SENT to {session}: {k[:110]}")
    if not dry_run:
        log_send(repo, session, runtime, verb, keys, reason, h)
        print(f"logged to {LOG_REL}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true", help="show sessions, runtimes, held orders")
    ap.add_argument("--send", choices=sorted(VERBS), help="verb to send (closed set)")
    ap.add_argument("--session", help="target tmux session name")
    ap.add_argument("--reason", default="", help="why (required for --send; goes in the log)")
    ap.add_argument("--root", help="file-drop root (default $GRC_WORKING or the VM path)")
    ap.add_argument("--repo", default="/home/grc/grc_library", help="repo holding the log")
    ap.add_argument("--force", action="store_true", help="override a destructive-verb gate")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    root = working_root(a.root)
    if a.list or not a.send:
        return do_list(root)
    if not a.session:
        print("--session is required with --send")
        return 1
    return do_send(Path(a.repo), root, a.session, a.send, a.reason, a.force, a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
