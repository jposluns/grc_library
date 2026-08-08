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
import os
import subprocess
import sys
import time
from pathlib import Path

from lint_common import resolve_working_for_write, resolve_working_for_write_private

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
RUNTIME_MAP = {"worker": "claude", "worker1": "claude", "codex": "codex"}
# Host-specific session names are OPERATIONAL data and live in the private sibling
# (grc_library_private/worker-runtime-map.json, a {"session-name": "family"} object),
# merged over the generic defaults above at import time (disclosure fix, PR #1457).
try:
    import json as _json_rm
    from pathlib import Path as _Path_rm
    _rm_p = _Path_rm(__file__).resolve().parents[2] / "grc_library_private" / "worker-runtime-map.json"
    if _rm_p.is_file():
        _rm = _json_rm.loads(_rm_p.read_text(encoding="utf-8"))
        if isinstance(_rm, dict):
            RUNTIME_MAP.update({str(k): str(v) for k, v in _rm.items()})
except Exception:
    pass  # fail open: the generic map stands; an unmapped session is refused loudly at verb time

# runtime -> the file-drop FAMILY directories that runtime can serve. A TUPLE, not one name,
# because the relationship is ONE-TO-MANY and the previous one-to-one map left the fail-open this
# tool fixed still standing for one family (validate-pr-1170 F1, error). Fable IS a Claude model, so
# a `fable`-family worker runs the `claude` runtime; mapping that runtime to `opus` alone made a
# `fable-` prefixed holder invisible to the fail-safe, so a destructive verb against a fable worker
# holding live work was PERMITTED. The old map even had a `fable` key, which shows the family was
# accounted for in the wrong dimension: `RUNTIME_MAP` can never yield `fable` as a RUNTIME.
RUNTIME_FAMILIES = {"claude": ("opus", "fable"), "codex": ("codex",)}

# The closed set. Values are literal keystroke sequences; a tuple sends in order, and a float
# member is a delay in seconds between sends.
VERBS = {
    "wake": {
        "claude": ("/credit-offload",),
        # Maintainer-specified 2026-07-25, REWORDED to the maintainer's own 2026-07-26 wording after
        # codex workers were observed misdescribing their state. Three deliberate properties.
        # SELF-DEFERRING, so it is safe to send mid-turn: the first clause tells a working worker to
        # discard it, which is why this verb needs no idleness gate. ONE-AT-A-TIME is stated
        # explicitly because a codex worker was observed holding two orders at once, which nothing
        # mechanically prevents. And it points at the ONBOARDING CONTRACT rather than restating the
        # serve loop, so this constant cannot drift out of step with the contract it summarizes.
        "codex": ("If you are currently working on an order, ignore this message and carry on. "
                  "If you are not, then at your next opportunity resync your grc_library_scratch "
                  "clone and check in: claim ONE waiting order in your family, work it to delivery, "
                  "and only then claim another. Follow the worker onboarding instructions in the "
                  "exchange repo's AGENTS.md for the full serve loop, rather than working from "
                  "memory of it.",),
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
ENTER_DELAY_S = 1.0  # raised from 0.4 (validate-pr-1170 F3): the threshold is a
# property of third-party TUIs and is neither measured nor observable, the risk is
# one-sided (too short fails, too long costs only latency), and `restart` already
# sleeps 10s between its keys, so a second here is not the cost worth optimizing.


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


RULE_CHARS = set("\u2500\u2501\u2504\u2505\u2508\u2509\u254c\u254d \t")
COMPOSER_TAIL_LINES = 12
# The submit postcondition polls rather than reading once: see the call site in do_send.
SUBMIT_POLL_S = 8.0
SUBMIT_POLL_INTERVAL_S = 0.5


def composer_region(pane_text: str, runtime: str | None = None):
    """The composer (input box) slice of a captured pane, or None when it cannot be located. PURE.

    Both agent TUIs draw the composer inside a horizontal-rule box at the bottom of the pane and
    ECHO a submitted prompt back into the scrollback above it. That echo is why the whole pane
    cannot answer "is the payload still in the input box": after a SUCCESSFUL submit the payload is
    still visible, as history. Scoping the read to the composer is what makes the question
    answerable.

    Claude's composer sits BETWEEN two rules (top border, input line, bottom border, status), so
    the region starts after the second-to-last rule. Codex draws one rule above its composer, so
    the region starts after the last one. Both are then capped to the final COMPOSER_TAIL_LINES,
    because a rule drawn in transcript OUTPUT would otherwise widen the region back toward the
    echo, which is the exact failure this replaces.

    Returns None rather than guessing when no rule is present, so the caller reports INDETERMINATE
    instead of asserting a submit state its input cannot support.
    """
    lines = pane_text.splitlines()
    if not lines:
        return None
    # A THRESHOLD, not a strict subset. `tmux capture-pane` can truncate a wide box-drawing
    # character at the pane's right edge, leaving a replacement char in the rule line; a strict
    # subset test then rejects a real rule and the caller reports INDETERMINATE for a payload that
    # plainly submitted (observed on both codex sessions, 2026-07-25). Requiring MOST of the line to
    # be rule characters keeps a prose line from matching while tolerating a torn edge.
    rules = []
    for n, ln in enumerate(lines):
        stripped = ln.strip()
        if len(stripped) < 8:
            continue
        rule_chars = sum(1 for ch in stripped if ch in RULE_CHARS)
        if rule_chars / len(stripped) >= 0.8:
            rules.append(n)
    if not rules:
        return None
    # WHICH BORDER IS THIS? The rule COUNT cannot answer that, and inferring the runtime from it was
    # a live FALSE-SUBMITTED path (validate-pr-1176 E1). Claude draws TWO rules around its composer
    # and Codex draws ONE above it, so a single rule is ambiguous: it is either a Codex top border,
    # or a Claude BOTTOM border whose top border has scrolled out of the captured tail. In the
    # second case `rules[-1] + 1` selects the status line BELOW the composer, which can never hold
    # the payload, so the probe is absent and the caller is told the prompt SUBMITTED when it did
    # not. That is reachable rather than theoretical: the bottom border is almost always inside a
    # 12-line tail, the top leaves it once the payload wraps to roughly ten lines, and the probe is
    # the payload's FIRST 40 characters, precisely the part that scrolls away first. So the check
    # failed most readily for exactly the long payloads the whitespace fix was written to handle.
    #
    # The caller KNOWS the runtime (VERBS is keyed by it), so it is passed in rather than guessed.
    # Where it is not passed, or where the count contradicts the runtime, this returns None, which
    # the caller renders as INDETERMINATE. Refusing on ignorance is the discipline this module
    # already states: a check that cannot fail is not a check.
    if runtime == "claude":
        if len(rules) < 2:
            return None          # top border gone: cannot locate the composer, do not guess
        start = rules[-2] + 1
    elif runtime == "codex":
        start = rules[-1] + 1    # one rule, above the composer, by this TUI's construction
    elif len(rules) >= 2:
        start = rules[-2] + 1    # unknown runtime but two rules: the Claude shape is unambiguous
    else:
        return None              # unknown runtime and one rule: genuinely indeterminate
    start = max(start, len(lines) - COMPOSER_TAIL_LINES)
    return "\n".join(lines[start:])


def submit_state(probe: str, pane_text: str, runtime: str | None = None) -> tuple:
    """PURE. Did the payload submit, judged from the composer alone? (state, reason) out.

    THREE states, not two, because a two-state answer forced a claim the input could not support:

      ("submitted",     ...)  the probe is NOT in the composer, so Enter took it
      ("not-submitted", ...)  the probe IS in the composer, so the TUI absorbed the Enter
      ("indeterminate", ...)  the composer could not be located, or the probe cannot discriminate

    THIS REPLACES A FALSE-POSITIVE CHECK (found in use, 2026-07-25). Two claude workers that had in
    fact submitted, and were visibly working seconds later, were both reported NOT SUBMITTED. The
    mechanism is a RACE, not a scoping error: the check read the pane once, ENTER_DELAY_S after
    Enter, and a large payload is still sitting in the composer at that instant because the TUI has
    not finished processing it. The single read cannot distinguish "absorbed the Enter" from "has
    not got to it yet", so the caller now POLLS until SUBMIT_POLL_S (see do_send) and only reports
    failure if the payload is STILL there at the end of the window.

    (The first diagnosis written here was that the TUI echoes a submitted prompt into the
    scrollback and the whole-pane read picked up that echo. That was WRONG and is recorded because
    the correction matters: the old call site read only the last four lines, so the echo, tens of
    lines up, could never have been in scope. Scoping to the composer is still worth doing, and
    this function does it, but a fixed line count was not the defect.)

    An empty or too-short probe discriminates nothing and returns indeterminate rather than a
    reassuring "submitted": a check that cannot fail is not a check.
    """
    if not probe or len(probe.strip()) < 8:
        return ("indeterminate",
                "the probe is empty or too short to discriminate, so no submit claim is made")
    region = composer_region(pane_text, runtime)
    if region is None:
        return ("indeterminate",
                "no composer box could be located in the captured pane, so whether the payload is "
                "still in the input box cannot be read; check the pane directly")
    # NORMALIZE WHITESPACE ON BOTH SIDES BEFORE MATCHING. tmux wraps a long line at the pane width,
    # so a payload sitting in the composer is captured as several lines and a literal probe spanning a
    # wrap boundary does NOT appear in the text. The previous form then fell through to "submitted",
    # reporting a prompt that was never sent as delivered, which is the DANGEROUS direction: the
    # caller prints SENT, logs the send, and stops polling, so a worker that received nothing is
    # recorded as nudged. Found by the #1175 post-merge sweep, in the exact failure direction its
    # order asked it to hunt. Collapsing runs of whitespace to single spaces makes the comparison
    # wrap-invariant.
    flat_region = " ".join(region.split())
    flat_probe = " ".join(probe.split())
    if flat_probe in flat_region:
        return ("not-submitted", "the payload is still in the composer after Enter")
    return ("submitted", "the composer no longer holds the payload")


def attribute_held(session: str, held: dict, families: tuple | None = None) -> tuple:
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
    appeared to work only because an earlier id scheme embedded the session name (`codex-session-m-a`
    contains `session-m`); the timestamped scheme does not.

    The live 2026-07-25 fail-open, which is pinned as a self-test case. `codex-...anon` held
    `order-x` while running in session `session-m`, and `codex-...anol` held nothing in session
    `codex`. First-match attribution credited session `codex` with the first worker's order and session `session-m`
    with NOTHING, so a destructive verb against `session-m` was ALLOWED while its worker had an order in
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
        # Ambiguity only MATTERS when a candidate holds something. If more than one worker id matches
        # but every match holds nothing, then whichever one runs here holds nothing either, so there
        # is nothing a destructive verb could destroy. Refusing anyway was a false refusal that fired
        # permanently on any family-named session with two live workers (validate-pr-1170 F2), and the
        # predictable response to a guard that refuses when nothing is at stake is habitual --force,
        # which disarms it for the cases that do matter. The unsound first-match guess is still never
        # made; only the risk-free case is released.
        return ("ambiguous", None) if any(o for _w, o in matches) else ("free", None)
    if matches:
        _worker_id, order = matches[0]
        return ("held", order) if order else ("free", None)
    # No match. That is not evidence of absence, because the id does not encode the session.
    prefixes = tuple(f"{f}-" for f in families) if families else None
    family_holds = any(
        order for wid, order in held.items()
        if prefixes is None or wid.startswith(prefixes)
    )
    if family_holds:
        return "unknown", None
    # A HOLDER THIS TOOL CANNOT CLASSIFY IS ALSO IGNORANCE, NOT ABSENCE (validate-pr-1172 F-1).
    # The check above answers "does a worker in MY families hold an order". A worker id outside every
    # known family prefix cannot be answered by that question, and worker ids are SELF-MINTED by each
    # session, so nothing constrains them to a prefix. The project's own historical ids took exactly
    # that `worker-<date>-<letter>` shape (id anonymized here), so this is a form in use rather than a
    # hypothetical. Encoding it as `none`, the permissive branch, is the same defect this file has now
    # been fixed for twice: two outcomes for three real states, with ignorance landing on the
    # permissive one. So an unclassifiable holder refuses too.
    all_prefixes = tuple(f"{f}-" for fs in RUNTIME_FAMILIES.values() for f in fs)
    if any(order for wid, order in held.items() if not wid.startswith(all_prefixes)):
        return "unknown", None
    return "none", None


def working_root(explicit: str | None) -> Path | None:
    for cand in (explicit, os.environ.get("GRC_WORKING"), "/home/grc/grc_working"):
        if cand and Path(cand).is_dir():
            return Path(cand)
    return None


def prepare_private_log(repo: Path) -> Path:
    """Resolve, privacy-validate, and initialize the worker-prompt log BEFORE any
    keystroke is sent (codex I-4). Returns the PRIVATE log path, or raises so the
    caller REFUSES the send. A keystroke injected into another user's session is
    invisible unless recorded, so the accountability record must be a validated,
    appendable, PRIVATE destination BEFORE the irreversible tmux send, never a
    recreated public .working/ path resolved after the fact."""
    p = resolve_working_for_write_private(LOG_REL.removeprefix(".working/"), repo_root=repo)
    private_root = (repo.resolve().parent / "grc_library_private").resolve()
    if p is None or not private_root.is_dir():
        raise RuntimeError("private working-state repository is unavailable")
    try:
        p.resolve().relative_to(private_root)
    except ValueError as exc:
        raise RuntimeError(f"resolved prompt log is not under the private sibling: {p}") from exc
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
    # Validate appendability before any tmux keystroke is sent.
    with p.open("a", encoding="utf-8"):
        pass
    return p


def log_send(p: Path, session: str, runtime: str, verb: str, keys, reason: str,
             held: str | None) -> None:
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
            state, h = attribute_held(s, held, RUNTIME_FAMILIES.get(RUNTIME_MAP.get(s)))
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
    state, h = attribute_held(session, held_orders(root), RUNTIME_FAMILIES.get(runtime))
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
              f"worker in the {RUNTIME_FAMILIES.get(runtime)} family/families holds an order. A worker id "
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
    # Resolve, privacy-validate, and initialize the accountability log BEFORE any keystroke
    # (codex I-4): refuse rather than send without a validated PRIVATE record. Dry runs
    # neither send nor log, so they need no log destination.
    log_path: Path | None = None
    if not dry_run:
        try:
            log_path = prepare_private_log(repo)
        except (OSError, RuntimeError) as exc:
            print("REFUSED: no writable private worker-prompt log is available, and a keystroke "
                  f"send must be recorded; nothing was sent: {exc}")
            return 1
    # RE-READ THE GATE IMMEDIATELY BEFORE ACTING (validate-pr-1172 F-2, a check-then-act race).
    # The held-order state above was read once, and claiming is a single rename by an independent
    # process, so a worker matched `free` can be holding live work by the time the keystrokes land.
    # The verifier SIZED the window from its own measurement rather than asserting it: detect-to-claim
    # for an idle polling worker is 8 to 13 seconds (n=8), which is far wider than the gap between the
    # read and the send. The all-idle release added by this same tool's F-2 fix is what makes the race
    # reachable, so the release keeps its own guard rather than being reverted. This closes most of the
    # window; it cannot close all of it, and saying so is the point (a re-check narrows a race, it does
    # not make the operation atomic).
    if verb in DESTRUCTIVE and not force:
        state2, h2 = attribute_held(session, held_orders(root), RUNTIME_FAMILIES.get(runtime))
        if (state2, h2) != (state, h):
            print(f"REFUSED {verb} on '{session}': the held-order state CHANGED between the check and "
                  f"the send ({state}/{h} then {state2}/{h2}), so a worker claimed or delivered in the "
                  "gap. Re-run to decide against the current state rather than a stale one.")
            return 1
    for k in keys:
        if isinstance(k, float):
            print(f"  (wait {k}s)")
            if not dry_run:
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
        # Enter by hand on the worker pane. Both agent TUIs treat a fast burst of input as a PASTE,
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
        time.sleep(ENTER_DELAY_S)
        rc, _, err = sh("tmux", "send-keys", "-t", session, "Enter")
        if rc != 0:
            print(f"send-keys FAILED on '{session}' (Enter): {err.strip()}")
            return 1
        # VERIFY THE SUBMIT, do not merely trust the delay (validate-pr-1170 F3, warning).
        # Both send-keys calls return 0 whether or not the prompt actually submitted, so a regression
        # in the paste-window timing presented as a worker that was never nudged, which is
        # indistinguishable from a stalled worker: the exact condition this tool exists to fix. The
        # original defect was caught only by the maintainer watching a pane by hand, and the fleet is
        # meant to run HEADLESS, so the postcondition is checked rather than assumed. A distinctive
        # slice of the payload still sitting in the pane means it did not submit.
        probe = k.strip()[:40]
        # POLL, do not read once. A single read ENTER_DELAY_S after Enter reports a false failure on
        # a payload the TUI simply has not finished processing (observed on two claude workers that
        # were demonstrably working seconds later). Break as soon as it reads submitted.
        state, why = ("indeterminate", "not yet read")
        deadline = time.time() + SUBMIT_POLL_S
        while True:
            state, why = submit_state(probe, pane_tail(session, COMPOSER_TAIL_LINES), runtime)
            if state == "submitted" or time.time() >= deadline:
                break
            time.sleep(SUBMIT_POLL_INTERVAL_S)
        if state == "not-submitted":
            print(f"  NOT SUBMITTED on '{session}': {why}, still there after {SUBMIT_POLL_S}s. The "
                  f"agent TUI absorbed the Enter as a newline (a paste-burst window wider than "
                  f"ENTER_DELAY_S={ENTER_DELAY_S}s). Nothing was queued; raise the delay or submit "
                  f"by hand. Reported rather than retried, because a blind retry can double-send.")
            return 1
        if state == "indeterminate":
            print(f"  UNVERIFIED on '{session}': the payload was sent, but {why}. Treat delivery as "
                  f"UNCONFIRMED and check the pane rather than assuming either outcome.")
            return 0
        print(f"  SENT to {session}: {k[:110]}")
    if not dry_run:
        assert log_path is not None  # prepared before the send loop, or we returned above
        log_send(log_path, session, runtime, verb, keys, reason, h)
        print(f"logged to {log_path}")
    return 0


def self_test() -> int:
    """Cover the refusals in `do_send`, which ARE this tool's entire safety surface.

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
    # Synthetic session mapping for the fixtures below: `session-m` stands in for a
    # host-specific codex session name (real names live in the private runtime map).
    RUNTIME_MAP.setdefault("session-m", "codex")
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
    tmux_sessions = lambda: ["grc", "worker", "session-m", "codex", "unmapped-session"]  # noqa: E731
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
                           repo, root, "session-m", "no-such-verb", "r", False, True)
            # destructive verb against a holder: the session name must match the worker id by
            # the same prefix rule do_send uses, so 'worker' matches 'worker-x'
            expect_refusal("refuses a destructive verb against an order holder",
                           "it holds order",
                           repo, root, "worker", "restart", "r", False, True)
            expect_refusal("destructive verb refused when the root is UNKNOWN",
                           "no file-drop root resolved",
                           repo, None, "worker", "restart", "r", False, True)
            # The routing refusal inside do_send: unreachable while the live table is clean, so a
            # bad payload is injected for the duration of this one case (a mutation sweep found the
            # branch otherwise undetectable).
            VERBS.setdefault("__probe", {})["claude"] = ("re-read grc_library_scratch/AGENTS.md",)
            try:
                expect_refusal("refuses a payload naming the other runtime's surface",
                               "belongs to the other runtime",
                               repo, root, "worker", "__probe", "r", False, True)
            finally:
                VERBS.pop("__probe", None)
            expect_refusal("refuses a missing --reason",
                           "--reason is required",
                           repo, root, "worker", "wake", "", False, True)
            expect_allowed("a non-destructive verb on a mapped session is allowed (dry-run)",
                           repo, root, "session-m", "wake", "r", False, True)

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
            # THE ACTUAL 2026-07-25 FAIL-OPEN, pinned (identifiers anonymized): session `session-m` matches NO codex worker id,
            # yet a codex worker holds an order, so `session-m` may be that holder and a restart must
            # refuse. Before the family-scoped unknown state, this case PASSED THE SEND.
            expect_refusal("refuses a destructive verb on an unmatched session whose family holds",
                           "no worker id matches this session name",
                           repo, root, "session-m", "restart", "r", False, True)
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

    # The submit postcondition. THREE states, and the indeterminate one is the point: the two-state
    # form asserted a submit verdict its single pane read could not support and reported two working
    # workers as NOT SUBMITTED.
    _rule = "\u2500" * 40
    _claude_empty = "\n".join(["  transcript line", _rule, "\u276f ", _rule, "  auto mode on"])
    _claude_stuck = "\n".join(["  transcript line", _rule,
                                "\u276f At your next opportunity, resync", _rule, "  auto mode on"])
    _claude_echo = "\n".join(["\u276f At your next opportunity, resync", "  assistant reply", _rule,
                               "\u276f ", _rule, "  auto mode on"])
    _codex_empty = "\n".join(["  transcript", _rule, "", "\u203a Improve documentation in @filename",
                               "  gpt-5.6 medium"])
    check_attr("submit: an empty claude composer reads submitted",
               submit_state("At your next opportunity", _claude_empty)[0], "submitted")
    check_attr("submit: a payload still in the claude composer reads not-submitted",
               submit_state("At your next opportunity", _claude_stuck)[0], "not-submitted")
    check_attr("submit: a SUBMITTED payload echoed in the scrollback still reads submitted",
               submit_state("At your next opportunity", _claude_echo)[0], "submitted")
    check_attr("submit: an empty codex composer reads submitted (runtime passed, as the caller does)",
               submit_state("At your next opportunity", _codex_empty, "codex")[0], "submitted")
    check_attr("submit: a pane with no composer box reads indeterminate, not submitted",
               submit_state("At your next opportunity", "just some text\nno rules here")[0],
               "indeterminate")
    check_attr("submit: a too-short probe reads indeterminate rather than reassuring",
               submit_state("hi", _claude_stuck)[0], "indeterminate")
    check_attr("submit: an empty probe reads indeterminate",
               submit_state("", _claude_empty)[0], "indeterminate")
    _torn = "\n".join(["  transcript", "\u2500" * 39 + "\ufffd", "",
                        "\u203a Improve documentation in @filename", "  gpt-5.6"])
    # THE REALITY FIXTURE for V1175-1 (#1175 post-merge sweep). The composer state below is the
    # verbatim shape the sweep constructed to defeat the literal match: tmux wrapped the payload at
    # the pane width, so the probe spanned a wrap boundary, did not appear as a literal, and the
    # check returned "submitted" for a prompt that was never sent. Kept verbatim rather than tidied,
    # because tidying it is where the defect would hide again.
    _wrapped = "\n".join([
        "\u2500" * 40,
        "\u276f At your next opportunity, resync",
        "  your grc_library scratch clone",
        "\u2500" * 40,
        "auto mode",
    ])
    _long_probe = "At your next opportunity, resync your grc_library scratch clone"[:40]
    check_attr("submit: a WRAPPED payload in the composer is not-submitted, not submitted",
               submit_state(_long_probe, _wrapped)[0], "not-submitted")

    # THE E1 REALITY FIXTURE (validate-pr-1176, 2026-07-26). A FALSE-SUBMITTED path that survived
    # the whitespace fix, because that fix repaired the MATCH and not the REGION. A claude pane
    # whose payload is tall enough that the composer's TOP border has scrolled out of the captured
    # tail leaves exactly ONE rule, the BOTTOM border. The old locator read `rules[-1] + 1`, i.e.
    # the status line BELOW the composer, never found the probe there, and answered "submitted" for
    # a prompt still sitting in the box. These cases pin BOTH halves: the runtime-aware locator must
    # now refuse, and the two-rule case must still resolve.
    _e1_one_rule = "\n".join(["  scrollback line",
                              "\u276f At your next opportunity, resync your grc_library_scratch clone",
                              "  and check in: claim ONE waiting order in your family, work it to",
                              "  delivery, and only then claim another. Follow the worker onboarding",
                              _rule,
                              "  auto mode on"])
    check_attr("E1: a claude pane with only the BOTTOM rule is INDETERMINATE, never submitted",
               submit_state("At your next opportunity", _e1_one_rule, "claude")[0], "indeterminate")
    check_attr("E1: the same pane read WITHOUT a runtime is also indeterminate, not guessed",
               submit_state("At your next opportunity", _e1_one_rule)[0], "indeterminate")
    check_attr("E1: codex legitimately has one rule ABOVE its composer, so it still resolves",
               submit_state("At your next opportunity", _codex_empty, "codex")[0], "submitted")
    check_attr("E1: a claude pane with BOTH rules is unaffected by the runtime argument",
               submit_state("At your next opportunity", _claude_stuck, "claude")[0], "not-submitted")
    check_attr("E1: composer_region refuses a one-rule claude pane",
               composer_region(_e1_one_rule, "claude"), None)
    check_attr("E1: composer_region still locates a one-rule CODEX composer",
               composer_region(_e1_one_rule, "codex") is None, False)
    check_attr("submit: the same probe against an EMPTY composer still reads submitted",
               submit_state(_long_probe,
                            "\n".join(["\u2500" * 40, "\u276f ", "\u2500" * 40, "auto mode"]))[0],
               "submitted")
    check_attr("submit: a rule with a truncated wide char is still a rule (codex capture)",
               submit_state("At your next opportunity", _torn, "codex")[0], "submitted")
    check_attr("composer_region: a prose line of words is NOT mistaken for a rule",
               composer_region("a line of ordinary prose here\nand another one"), None)
    check_attr("composer_region: returns None when no rule is present",
               composer_region("no rules at all\nsecond line"), None)

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
               attribute_held("opus-1", {"opus-1": "o"}, ("opus",)), ("held", "o"))
    check_attr("attribute_held: one match holding nothing",
               attribute_held("opus-1", {"opus-1": None}, ("opus",)), ("free", None))
    check_attr("attribute_held: two matches is ambiguous, never a first-match guess",
               attribute_held("codex", {"codex-a": "o", "codex-b": None}, ("codex",)),
               ("ambiguous", None))
    check_attr("attribute_held: no match and NO family holder is a safe none",
               attribute_held("session-m", {"codex-a": None}, ("codex",)), ("none", None))
    check_attr("attribute_held: no match while the family HOLDS is unknown, not none",
               attribute_held("session-m", {"codex-a": "o"}, ("codex",)), ("unknown", None))
    # F4(1): multi-match where EVERY match is idle. This is where F2 lived, which is why F2 shipped.
    check_attr("attribute_held: multi-match with NO holder is free, not a false refusal",
               attribute_held("codex", {"codex-a": None, "codex-b": None}, ("codex",)), ("free", None))
    check_attr("attribute_held: multi-match with ONE holder stays ambiguous",
               attribute_held("codex", {"codex-a": None, "codex-b": "o"}, ("codex",)), ("ambiguous", None))
    # F4(2): families=None, the default, reachable from do_list for an UNMAPPED session.
    check_attr("attribute_held: families=None widens the fail-safe fleet-wide (conservative)",
               attribute_held("nomatch", {"opus-a": "o"}, None), ("unknown", None))
    check_attr("attribute_held: families=None with no holder anywhere is none",
               attribute_held("nomatch", {"opus-a": None}, None), ("none", None))
    # F1: a fable worker runs the CLAUDE runtime, so its family set must include fable.
    check_attr("attribute_held: a fable holder is visible to a claude-runtime session",
               attribute_held("worker9", {"fable-a": "live-order"}, RUNTIME_FAMILIES["claude"]),
               ("unknown", None))
    check_attr("attribute_held: a codex holder still does NOT freeze a claude session",
               attribute_held("worker9", {"codex-a": "live-order"}, RUNTIME_FAMILIES["claude"]),
               ("none", None))
    # F-1: a holder whose id matches NO known family prefix must refuse, not permit.
    check_attr("attribute_held: an unclassifiable holder is unknown, not none",
               attribute_held("worker9", {"mystery-a": "live-order"}, RUNTIME_FAMILIES["claude"]),
               ("unknown", None))
    check_attr("attribute_held: the project's own historical id shape refuses too",
               attribute_held("worker9", {"worker-20990101-a": "live-order"}, RUNTIME_FAMILIES["claude"]),
               ("unknown", None))
    check_attr("attribute_held: an unclassifiable worker holding NOTHING still permits",
               attribute_held("worker9", {"mystery-a": None}, RUNTIME_FAMILIES["claude"]),
               ("none", None))
    check_attr("the runtime-to-family map is one-to-many and covers every family directory",
               sorted({f for fs in RUNTIME_FAMILIES.values() for f in fs}), ["codex", "fable", "opus"])
    check_attr("attribute_held: THE live 2026-07-25 fail-open (session unmatched, worker holding)",
               attribute_held("session-m", {"codex-20260725T041432Z-anon": "order-x",
                                        "codex-20260725T151831Z-anol": None}, ("codex",)),
               ("unknown", None))
    check_attr("attribute_held: its sibling half (family session matches both ids)",
               attribute_held("codex", {"codex-20260725T041432Z-anon": "order-x",
                                        "codex-20260725T151831Z-anol": None}, ("codex",)),
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
