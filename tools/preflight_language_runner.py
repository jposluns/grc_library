#!/usr/bin/env python3
"""Isolated gate-2 language-engine runner for tools/preflight-changelog.py.

Runs in a CHILD process (``sys.executable -I``) so that no engine code ever
executes in the preflight process (3b201, /validate-pr round 5). Protocol:

  argv[1]  path to gate 2's project entry point (tools/lint-language.py)
  stdin    one JSON object ``{"nonce": str, "texts": [str, ...]}``
  stdout   on success, EXACTLY one JSON line
           ``{"nonce": <the request's nonce>, "findings": [[[kind, word], ...]
           per input text]}``, then ``os._exit(0)``
  stderr   engine noise and tracebacks; the parent discards it unread

Ordering is the boundary: stdin is consumed and the result channel (a duplicate
of the original stdout file descriptor) is saved BEFORE any engine code runs,
and file descriptor 1 is redirected into stderr, so engine prints and a closed
or replaced ``sys.stdout`` cannot reach the result channel. The result is
written to the saved descriptor and sealed with ``os._exit(0)``, so no engine
teardown, atexit or shutdown code runs after it. Before loading the engine,
unraisable and thread exception hooks are installed to record the fault and
exit immediately with status 70, without writing a result. Exceptions delivered
to either hook before sealing deny the result. After the last matcher call and
BEFORE any matcher result is read, the runner refuses with status 72, without a
result line, if any thread other than the main thread is alive
(``threading.enumerate()``): a matcher that handed its work to a still-running
thread has returned a result it has not finished producing (round 8, E1). Only
after that check are the results copied into an immutable snapshot (validated
string pairs in new tuples), so a list an engine thread could still mutate is
never what gets sealed. Immediately before sealing, ``gc.collect()`` runs under
the fault hooks (surfacing pending destructor faults, retained cycles
included), the result is refused with status 71, without a result line, unless
BOTH hooks are still this runner's own handler (an identity check) and no fault
was recorded, and the thread-liveness check runs once more (status 72): an
engine that merely restored the interpreter's default hooks, turning a fault
into discarded stderr noise, cannot seal a result, and neither can one whose
worker thread is still running. A ``spelling_matches`` result is accepted only as
a list or tuple of two-item list/tuple string pairs; any other return (a str,
dict, set, generator or other iterable included) raises, ending the child
without a result line. Propagating exceptions and early exits before the result
is written leave no valid result; exceptions caught by engine code are not
detected. The parent rejects nonzero exits, timeouts and missing, extra,
malformed or invalid results. Residuals, stated: an engine that REPLACES a
fault hook, absorbs a fault under the replacement, and restores this runner's
own handler before sealing defeats the identity check; like a child that
deliberately forges a well-formed marked line, that is outside the threat model
(faults, not malice); see the preflight's module docstring. An engine that
forks a helper WITHOUT exec leaves the saved result descriptor open in the
helper, so the parent never sees end-of-output and refuses at its timeout:
fail closed, availability only, never a wrong verdict.
"""
import gc
import importlib.util
import json
import os
import sys
import threading

_FAULTS: list = []


def _exit_on_fault(_args, _exit=os._exit, _record=_FAULTS.append) -> None:
    _record(True)  # no formatting, buffering or cleanup before rejecting the result
    _exit(70)


def _refuse_live_engine_threads(_exit=os._exit, _enumerate=threading.enumerate,
                                _main_thread=threading.main_thread) -> None:
    """Refuse (status 72, no result line) while any thread other than the main
    thread is alive: a matcher that handed its work to a thread has returned a
    result it has not finished producing, and sealing it would turn unfinished
    work into a verdict (round 8, E1). The callables are bound at definition
    time, before any engine code runs."""
    for thread in _enumerate():
        if thread is not _main_thread():
            _exit(72)


def _snapshot(raw_results):
    """The validated, immutable copy of the matcher results: one tuple of
    (kind, word) string-pair tuples per input text. The declared contract,
    enforced: each result is a list (or tuple) of two-item list/tuple string
    pairs. A str, dict, set or generator would otherwise iterate into zero or
    garbled pairs and become a sealed verdict. Called only AFTER the
    thread-liveness check, so a list an engine thread could still be filling
    is never what this reads (round 8, E1)."""
    findings = []
    for result in raw_results:
        if not isinstance(result, (list, tuple)):
            raise TypeError("spelling_matches must return a list of (kind, word) pairs")
        matches = []
        for pair in result:
            if not (isinstance(pair, (list, tuple)) and len(pair) == 2
                    and isinstance(pair[0], str) and isinstance(pair[1], str)):
                raise TypeError("spelling_matches must yield (kind, word) string pairs")
            matches.append((pair[0], pair[1]))
        findings.append(tuple(matches))
    return tuple(findings)


def main() -> None:
    sys.unraisablehook = _exit_on_fault
    threading.excepthook = _exit_on_fault
    request = json.loads(sys.stdin.read())
    nonce, texts = request["nonce"], request["texts"]
    result_fd = os.dup(1)
    os.dup2(2, 1)  # engine stdout noise joins stderr; the parent discards both

    gate_path = os.path.abspath(sys.argv[1])
    tools_dir = os.path.dirname(gate_path)
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    spec = importlib.util.spec_from_file_location("_changelog_language", gate_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    engine = mod._engine()
    for name in ("spelling_matches", "compile_language", "language_vocabulary"):
        if not callable(getattr(engine, name, None)):
            raise TypeError(f"language engine {name} must be callable")
    checks = engine.compile_language(mod._language_config())
    raw_results = [engine.spelling_matches(text, checks) for text in texts]
    # Round 8, E1: refuse unfinished matcher work BEFORE any result is read,
    # and snapshot only after that: an asynchronous matcher's still-empty
    # (or still-growing) list never becomes a sealed verdict.
    _refuse_live_engine_threads()
    findings = _snapshot(raw_results)
    # Drop the engine's objects before the pre-seal collection: a retained
    # binding would keep an engine-created reference cycle reachable and
    # hide its destructor fault from gc.collect().
    del raw_results
    payload = (json.dumps({"nonce": nonce, "findings": findings},
                          ensure_ascii=True) + "\n").encode("ascii")
    # Immediately before sealing: surface pending destructor faults (retained
    # cycles included) through the fault hooks, then refuse unless both hooks
    # are still this runner's own handler and no fault was recorded. An engine
    # that restored the interpreter's default hooks cannot turn a masked fault
    # into a sealed result. The thread-liveness check runs once more: a thread
    # still alive at sealing cannot seal either (round 8, E1).
    gc.collect()
    if (sys.unraisablehook is not _exit_on_fault
            or threading.excepthook is not _exit_on_fault or _FAULTS):
        os._exit(71)  # distinct from the in-hook status 70: refused at sealing
    _refuse_live_engine_threads()
    while payload:
        payload = payload[os.write(result_fd, payload):]
    os._exit(0)  # seal the result: no engine teardown code runs after it


if __name__ == "__main__":
    main()
