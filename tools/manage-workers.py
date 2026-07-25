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
# `codex` added 2026-07-25 after a second Codex worker was started in a session of that name and
# every verb against it was refused for having no mapping. The refusal was correct (this tool will
# not guess a prompt shape), but an unmapped live worker is un-nudgeable, so the map has to keep up
# with the fleet. Adding a session here stays the deliberate, reviewable act it is meant to be.
RUNTIME_MAP = {"worker": "claude", "worker1": "claude", "mailz": "codex", "codex": "codex"}

# runtime -> file-drop FAMILY directory. Needed because held-order attribution scopes its
# fail-safe by family (see attribute_held): the exchange lays out `opus/`, `codex/`, `fable/`,
# and a Claude worker's orders live under `opus/`, so runtime and family are not the same word.
RUNTIME_FAMILY = {"claude": "opus", "codex": "codex", "fable": "fable"}

# The closed set. Values are literal keystroke sequences; a tuple sends in order, and a float
# member is a delay in seconds between sends.
VERBS = {
    "wake": {
        "claude": ("/credit-offload",),
        # Maintainer-specified 2026-07-25. Self-deferring by design, so it is safe mid-turn.
        "codex": ("At your next opportunity, resync your grc_library_scratch clone and check in: "
                  "claim the next waiting order in your family if you are not already working.",),
    },
    # PER-RUNTIME CONTRACT PATH. `AGENTS.md` and `CLAUDE.md` are a deliberate PARALLEL PAIR in the
    # exchange repo, not one file with two names: AGENTS.md states it is "the Codex-agent equivalent
    # of this repository's CLAUDE.md", and CLAUDE.md is auto-loaded by Claude Code. Both texts
    # previously named AGENTS.md, so a `reload` sent a Claude worker to the Codex contract
    # (maintainer-caught 2026-07-25, after exactly that was sent to two Claude workers). Each runtime
    # is now pointed at ITS OWN file. The pairing also means a contract edit must land in BOTH, which
    # the same catch surfaced: the issue-drop rule went into AGENTS.md alone and reached only half the
    # fleet.
    "reload": {
        "claude": ("When you finish your current task, re-read your worker contract at "
                   "grc_library_scratch/CLAUDE.md and your skills, then continue.",),
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

# Surfaces that belong to ONE runtime, so naming them in the OTHER runtime's prompt is a routing
# defect. This exists because the routing itself was never the bug: `do_send` has always selected
# VERBS[verb][runtime], and the 2026-07-25 failure was that BOTH runtime entries for `reload`
# contained the same text naming `AGENTS.md`, so a correctly-routed prompt still sent a Claude worker
# to the Codex contract. A per-runtime table cannot be trusted merely because it is keyed by runtime;
# its VALUES have to be checked too, which is what the guard below does.
RUNTIME_FOREIGN_TOKENS = {
    # AGENTS.md is the Codex-agent contract; CLAUDE.md is the Claude one, auto-loaded by Claude Code.
    # They are a deliberate parallel pair in the exchange repo, not one file with two names.
    "claude": ("AGENTS.md",),
    # `/credit-offload` is a Claude slash command with no Codex equivalent, which is exactly why the
    # Codex wake text is prose instead. Naming it to Codex would send an instruction it cannot run.
    "codex": ("CLAUDE.md", "/credit-offload"),
}


def verb_routing_violations(verbs: dict, foreign: dict) -> list:
    """PURE. Every (verb, runtime, token) where a prompt names another runtime's surface.

    Pure and table-driven so the self-test can pin it with constructed tables AND so the live VERBS
    table is checked on every send, not only when someone remembers to run the self-test.
    """
    out = []
    for verb, per_runtime in sorted(verbs.items()):
        for runtime, keys in sorted(per_runtime.items()):
            payload = " ".join(k for k in keys if isinstance(k, str))
            for token in foreign.get(runtime, ()):
                if token in payload:
                    out.append((verb, runtime, token))
    return out


# Verbs that destroy context, so they require the worker to hold NO order.
DESTRUCTIVE = {"restart"}

# Seconds between sending a prompt's TEXT and sending its Enter. Two separate send-keys calls with
# a gap between them, because a single combined call is read by both agent TUIs as a paste, and a
# paste swallows the trailing Enter into a newline (maintainer-observed 2026-07-25: the prompt sat
# unsubmitted in the input box until they pressed Enter by hand). Small enough not to matter, large
# enough to fall outside the TUIs' paste-burst window.
ENTER_DELAY_S = 0.4


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
    """worker-id -> held order id, or None for a worker present but holding nothing.

    The AUTHORITATIVE half of the gate. A pane can look idle while an order is held (that is
    exactly the stalled-mid-task case), so held-state must come from the exchange, never from
    the pane and never from the worker's self-report.

    Every worker inbox directory is recorded, INCLUDING empty ones, mapped to None. That makes
    "this worker exists and holds nothing" distinguishable from "no such worker", which
    `attribute_held` needs in order to tell a real free worker from an unmatched session name.
    Recording only holders, as this did before, collapsed those two cases together.
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
            orders = sorted(p.stem for p in wdir.glob("*.md"))
            held[wdir.name] = orders[0] if orders else None
    return held


def attribute_held(session: str, held: dict, family: str | None = None) -> tuple:
    """Map a tmux SESSION name to the order held by the worker running in it.

    PURE: (session, held-map, family) in, (state, order-or-none) out. No filesystem, no tmux, no
    clock, so the self-test can pin every branch with constructed inputs.

    Returns one of:
      ("held",      order_id)  exactly one worker id matches this session, and it holds that order
      ("free",      None)      exactly one matches, and it holds nothing
      ("ambiguous", None)      more than one matches, so WHICH worker runs here is unknown
      ("unknown",   None)      none matches, but a worker in this session's family holds an order,
                               so this session CANNOT BE PROVEN not to be that holder
      ("none",      None)      none matches and no worker in the family holds anything

    THIS FUNCTION CANNOT SOUNDLY IDENTIFY THE WORKER, AND SAYS SO RATHER THAN GUESSING. A worker id
    is minted per run as `<family>-<timestamp>-<nonce>` and encodes NOTHING about the tmux session
    it runs in, so matching a session NAME against a worker ID is unsound by construction. It ever
    appeared to work only because an earlier id scheme embedded the session name (`codex-mailz-a`
    contains `mailz`); the timestamped scheme does not.

    The live 2026-07-25 fail-open, which is pinned as a self-test case. `codex-...f8b8` held
    `fnaudit-sweep121` while running in session `mailz`, and `codex-...b6ba` held nothing in session
    `codex`. First-match attribution credited session `codex` with f8b8's order and session `mailz`
    with NOTHING, so a destructive verb against `mailz` was ALLOWED while its worker had an order in
    flight, destroying exactly the work the holder gate exists to protect, while `codex` was refused
    for an order it did not hold. Both verdicts were wrong, and the dangerous one was the silent
    permit rather than the visible refusal.

    So ignorance is reported as ignorance, and it is scoped by FAMILY so the conservatism stays
    proportionate: an unmatched `codex`-family session while a codex worker holds an order is
    `unknown` (refuse a destructive verb), whereas the same session while no codex worker holds
    anything is `none` (nothing to lose, so proceed). Without the family scope, any single holder
    anywhere would freeze destructive verbs against every session, which is the kind of over-broad
    guard that gets switched off. `--force` remains the deliberate override.
    """
    matches = [(k, v) for k, v in held.items() if k.startswith(session) or session in k]
    if len(matches) > 1:
        return "ambiguous", None
    if matches:
        _worker_id, order = matches[0]
        return ("held", order) if order else ("free", None)
    # No match. That is not evidence of absence, because the id does not encode the session.
    prefix = f"{family}-" if family else None
    family_holds = any(
        order for wid, order in held.items()
        if prefix is None or wid.startswith(prefix)
    )
    return ("unknown", None) if family_holds else ("none", None)


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
        # A session name is not a worker id (ids are minted per run), so attribution goes through
        # attribute_held, which reports ambiguity instead of guessing the first match.
        if s in ORCHESTRATOR_SESSIONS:
            # The orchestrator holds no order by construction, and no verb may target it, so
            # attributing held-state to it would be noise rather than information.
            h = None
        else:
            state, h = attribute_held(s, held, RUNTIME_FAMILY.get(RUNTIME_MAP.get(s)))
            if state == "ambiguous":
                h = "AMBIGUOUS (matches >1 worker)"
            elif state == "unknown":
                h = "UNKNOWN (family has a holder)"
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
    bad = [v for v in verb_routing_violations({verb: {runtime: keys}}, RUNTIME_FOREIGN_TOKENS)]
    if bad:
        names = ", ".join(f"'{tok}'" for _v, _r, tok in bad)
        print(f"REFUSED: the '{verb}' prompt for runtime '{runtime}' names {names}, which belongs to "
              f"the other runtime. Sending it would hand this worker an instruction for a surface it "
              f"does not have. Fix the VERBS entry rather than the target.")
        return 1
    state, h = attribute_held(session, held_orders(root), RUNTIME_FAMILY.get(runtime))
    if verb in DESTRUCTIVE and h and not force:
        print(f"REFUSED {verb} on '{session}': it holds order '{h}', and {verb} destroys "
              "context, so in-flight work would be lost. Wait for delivery, or reclaim the "
              "order first. --force overrides.")
        return 1
    if state == "ambiguous" and verb in DESTRUCTIVE and not force:
        print(f"REFUSED {verb} on '{session}': the session name matches MORE THAN ONE worker id, "
              "so which worker runs here, and therefore whether it holds an order, is UNKNOWN. "
              "This happens when a session is named after its family, because every worker id in "
              "that family shares that prefix. Reclaim first, or override. --force overrides.")
        return 1
    if state == "unknown" and verb in DESTRUCTIVE and not force:
        print(f"REFUSED {verb} on '{session}': no worker id matches this session name, AND a "
              f"worker in the '{RUNTIME_FAMILY.get(runtime)}' family holds an order. A worker id "
              "encodes nothing about its tmux session, so a non-match is NOT evidence that this "
              "session is idle: it may be the holder. Confirm which session the holder runs in, "
              "or wait for delivery. --force overrides.")
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
        # TEXT AND ENTER ARE TWO SEPARATE send-keys CALLS, WITH A PAUSE BETWEEN THEM.
        #
        # Maintainer-observed 2026-07-25, and the single most important line in this loop: sending
        # `send-keys -t <session> "<text>" Enter` in ONE call delivered the text but NOT the submit,
        # so the prompt sat in the worker's input box as a line break and the maintainer had to press
        # Enter by hand on the `mailz` pane. Both agent TUIs treat a fast burst of input as a PASTE,
        # and a paste absorbs the trailing Enter as a newline instead of submitting.
        #
        # The failure is LENGTH-DEPENDENT, which is why it was not caught earlier: the Claude `wake`
        # is the single short token `/credit-offload`, which submits fine and did revive a worker in
        # the same run, while the Codex `wake` is a long prose sentence, which did not. So a
        # one-call send appears to work for exactly the verbs whose payload is shortest.
        #
        # `-l` sends the payload LITERALLY, so prose containing anything tmux would otherwise read
        # as a key name (a bare `Enter`, `Space`, `C-c`) cannot be reinterpreted as a keystroke.
        rc, _, err = sh("tmux", "send-keys", "-t", session, "-l", k)
        if rc != 0:
            print(f"send-keys FAILED on '{session}' (text): {err.strip()}")
            return 1
        import time
        time.sleep(ENTER_DELAY_S)
        rc, _, err = sh("tmux", "send-keys", "-t", session, "Enter")
        if rc != 0:
            print(f"send-keys FAILED on '{session}' (Enter): {err.strip()}")
            return 1
        print(f"  SENT to {session}: {k[:110]}")
    if not dry_run:
        log_send(repo, session, runtime, verb, keys, reason, h)
        print(f"logged to {LOG_REL}")
    return 0


def self_test() -> int:
    """Cover all SEVEN refusals in `do_send`, which ARE this tool's entire safety surface.

    Added after the #1167 sweep observed that the CHANGELOG asserted these refusals were tested
    while nothing tested them: they had been exercised by hand and never recorded, so nobody
    could re-check them. A tool that injects keystrokes into a session running under a different
    account should not have its guards resting on an unrepeatable manual run.

    EACH CASE ASSERTS THE SPECIFIC REFUSAL MESSAGE, not merely the return code. Every refusal
    returns 1, so a return-code-only assertion is satisfied by ANY guard firing rather than by the
    one the case names. Sweep 121 mutation-proved the consequence: with the own-session, the
    nonexistent-session, the runtime-mapping, or the verb-sequence guard neutralized one at a time,
    the old self-test still printed PASS *under that case's own label*. That is the
    passes-for-an-unrelated-reason shape, and it made this self-test unable to detect the removal
    of four of the seven guards it claimed to cover. Matching on the message text is what turns
    each case into a real discriminator, so the fix is the assertion, not more cases.

    Each refusal is a pure early return, so it is reachable without touching tmux: the session
    list is stubbed and no send is ever attempted.
    """
    import contextlib
    import io
    import tempfile
    failures, total = [], [0]

    def expect_refusal(name, want_text, *args):
        """Assert do_send REFUSED, that the refusal is the one `want_text` identifies, and that
        it is the ONLY one that fired.

        The exactly-one check is not redundant with the text match. A guard whose `return` is lost
        while its `print` survives still emits its own message and then falls through to a later
        guard, which supplies the 1; text-plus-return-code alone reads that as a pass. Counting the
        refusals catches it, because two messages appear where one should.
        """
        total[0] += 1
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            got = do_send(*args)
        out = buf.getvalue()
        n_refusals = out.count("REFUSED")
        ok = got == 1 and want_text in out and n_refusals == 1
        if ok:
            print(f"  PASS: {name}")
        else:
            if got != 1:
                why = f"returned {got}, expected 1"
            elif want_text not in out:
                why = f"wrong refusal fired; expected text {want_text!r}, got: {out.strip()[:120]!r}"
            else:
                why = (f"{n_refusals} refusals fired, expected exactly 1 (a guard printed and then "
                       f"fell through): {out.strip()[:160]!r}")
            print(f"  FAIL: {name} ({why})")
            failures.append(name)

    def expect_allowed(name, *args):
        """Assert do_send proceeded (rc 0) and printed no refusal at all."""
        total[0] += 1
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            got = do_send(*args)
        out = buf.getvalue()
        ok = got == 0 and "REFUSED" not in out
        print(f"  {'PASS' if ok else 'FAIL'}: {name}"
              + ("" if ok else f" (returned {got}; output: {out.strip()[:120]!r})"))
        if not ok:
            failures.append(name)

    global tmux_sessions
    real = tmux_sessions
    tmux_sessions = lambda: ["grc", "worker", "mailz", "codex", "unmapped-session"]  # noqa: E731
    try:
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            (repo / ".working").mkdir()
            root = Path(td) / "work"
            (root / "opus" / "inbox" / "worker-x").mkdir(parents=True)
            # a worker holding an order, for the destructive gate
            (root / "opus" / "inbox" / "worker-x" / "held-order.md").write_text("x")

            # One case per REFUSED early return in do_send, in source order, each keyed to a
            # distinctive fragment of ITS OWN message so no other guard can satisfy it.
            expect_refusal("refuses the orchestrator's own session",
                           "is the orchestrator's own session",
                           repo, root, "grc", "wake", "r", False, True)
            expect_refusal("refuses a nonexistent session",
                           "no tmux session named",
                           repo, root, "no-such-session", "wake", "r", False, True)
            expect_refusal("refuses a session with no runtime mapping",
                           "has no runtime mapping in RUNTIME_MAP",
                           repo, root, "unmapped-session", "wake", "r", False, True)
            # The seventh guard, previously uncovered: a mapped session but a verb with no
            # sequence defined for that session's runtime.
            expect_refusal("refuses a verb with no sequence for the session's runtime",
                           "has no defined sequence for runtime",
                           repo, root, "mailz", "no-such-verb", "r", False, True)
            # destructive verb against a holder: the session name must match the worker id by
            # the same prefix rule do_send uses, so 'worker' matches 'worker-x'
            expect_refusal("refuses a destructive verb against an order holder",
                           "it holds order",
                           repo, root, "worker", "restart", "r", False, True)
            expect_refusal("destructive verb refused when the root is UNKNOWN",
                           "no file-drop root resolved",
                           repo, None, "worker", "restart", "r", False, True)
            expect_refusal("refuses a missing --reason",
                           "--reason is required",
                           repo, root, "worker", "wake", "", False, True)
            expect_allowed("a non-destructive verb on a mapped session is allowed (dry-run)",
                           repo, root, "mailz", "wake", "r", False, True)

            # The ambiguity gate, end to end: two same-family worker ids both prefix-match the
            # family-named session, so held-state is UNKNOWN and a destructive verb must refuse.
            # This is the 2026-07-25 fail-open, pinned as a case: before the fix, attribution took
            # the first match and a restart against the NON-matching session was allowed while its
            # worker held an order.
            (root / "codex" / "inbox" / "codex-aaa").mkdir(parents=True)
            (root / "codex" / "inbox" / "codex-bbb").mkdir(parents=True)
            (root / "codex" / "inbox" / "codex-aaa" / "live-order.md").write_text("x")
            expect_refusal("refuses a destructive verb when the session matches >1 worker id",
                           "matches MORE THAN ONE worker id",
                           repo, root, "codex", "restart", "r", False, True)
            expect_allowed("a non-destructive verb is allowed despite ambiguous attribution",
                           repo, root, "codex", "wake", "r", False, True)
            # THE ACTUAL 2026-07-25 FAIL-OPEN, pinned: session `mailz` matches NO codex worker id,
            # yet a codex worker holds an order, so `mailz` may be that holder and a restart must
            # refuse. Before the family-scoped unknown state, this case PASSED THE SEND.
            expect_refusal("refuses a destructive verb on an unmatched session whose family holds",
                           "no worker id matches this session name",
                           repo, root, "mailz", "restart", "r", False, True)
    finally:
        tmux_sessions = real

    # attribute_held is pure, so its four states are pinned directly with constructed maps
    # rather than through the filesystem. Purity is what makes these cases discriminating:
    # each asserts a distinct return, not a shared sentinel.
    def check_attr(name, got, want):
        total[0] += 1
        ok = got == want
        print(f"  {'PASS' if ok else 'FAIL'}: {name}" + ("" if ok else f" -> {got}, expected {want}"))
        if not ok:
            failures.append(name)

    # THE LIVE VERBS TABLE must never name another runtime's surface. This is the case that would
    # have caught the 2026-07-25 defect, where both `reload` payloads named the Codex contract.
    check_attr("the shipped VERBS table has no cross-runtime prompt",
               verb_routing_violations(VERBS, RUNTIME_FOREIGN_TOKENS), [])
    # and the guard itself discriminates, pinned on constructed tables
    check_attr("a Claude prompt naming the Codex contract is caught",
               verb_routing_violations({"reload": {"claude": ("re-read grc_library_scratch/AGENTS.md",)}},
                                       RUNTIME_FOREIGN_TOKENS),
               [("reload", "claude", "AGENTS.md")])
    check_attr("a Codex prompt naming the Claude contract is caught",
               verb_routing_violations({"reload": {"codex": ("re-read grc_library_scratch/CLAUDE.md",)}},
                                       RUNTIME_FOREIGN_TOKENS),
               [("reload", "codex", "CLAUDE.md")])
    check_attr("a Codex prompt naming the Claude-only slash command is caught",
               verb_routing_violations({"wake": {"codex": ("/credit-offload",)}},
                                       RUNTIME_FOREIGN_TOKENS),
               [("wake", "codex", "/credit-offload")])
    check_attr("each runtime naming its OWN contract is clean",
               verb_routing_violations({"reload": {"claude": ("grc_library_scratch/CLAUDE.md",),
                                                   "codex": ("grc_library_scratch/AGENTS.md",)}},
                                       RUNTIME_FOREIGN_TOKENS), [])
    check_attr("a float delay in the sequence does not break the scan",
               verb_routing_violations({"restart": {"claude": ("/clear", 10.0, "/credit-offload")}},
                                       RUNTIME_FOREIGN_TOKENS), [])
    check_attr("attribute_held: one match holding an order",
               attribute_held("opus-1", {"opus-1": "o"}, "opus"), ("held", "o"))
    check_attr("attribute_held: one match holding nothing",
               attribute_held("opus-1", {"opus-1": None}, "opus"), ("free", None))
    check_attr("attribute_held: two matches is ambiguous, never a first-match guess",
               attribute_held("codex", {"codex-a": "o", "codex-b": None}, "codex"),
               ("ambiguous", None))
    check_attr("attribute_held: no match and NO family holder is a safe none",
               attribute_held("mailz", {"codex-a": None}, "codex"), ("none", None))
    check_attr("attribute_held: no match while the family HOLDS is unknown, not none",
               attribute_held("mailz", {"codex-a": "o"}, "codex"), ("unknown", None))
    check_attr("attribute_held: the family scope keeps it proportionate (claude session, codex holder)",
               attribute_held("worker9", {"codex-a": "o"}, "opus"), ("none", None))
    check_attr("attribute_held: THE live 2026-07-25 fail-open (mailz unmatched, f8b8 holding)",
               attribute_held("mailz", {"codex-20260725T041432Z-f8b8": "fnaudit-sweep121",
                                        "codex-20260725T151831Z-b6ba": None}, "codex"),
               ("unknown", None))
    check_attr("attribute_held: its sibling half (family session matches both ids)",
               attribute_held("codex", {"codex-20260725T041432Z-f8b8": "fnaudit-sweep121",
                                        "codex-20260725T151831Z-b6ba": None}, "codex"),
               ("ambiguous", None))

    if failures:
        print(f"\nself-test: FAILED ({len(failures)} of {total[0]})")
        return 1
    print(f"\nself-test: {total[0]}/{total[0]} passed")
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
    ap.add_argument("--self-test", action="store_true", help="exercise the refusal paths")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    root = working_root(a.root)
    if a.list or not a.send:
        return do_list(root)
    if not a.session:
        print("--session is required with --send")
        return 1
    return do_send(Path(a.repo), root, a.session, a.send, a.reason, a.force, a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
