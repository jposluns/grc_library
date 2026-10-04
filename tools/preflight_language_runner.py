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
teardown, atexit or shutdown code runs after it. There is deliberately NO
exception handling here: any fault ends the child without the marked result
line (a propagating SystemExit(0), a patched ``sys.exit`` and ``os._exit(0)``
in engine code included, since each skips the marked line), and the parent
fails closed on a nonzero exit, a timeout, a missing or extra or malformed
result line, a wrong nonce, or a schema violation. A child that deliberately
forges a well-formed marked line is outside the threat model (faults, not
malice); see the preflight's module docstring.
"""
import importlib.util
import json
import os
import sys


def main() -> None:
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
    findings = []
    for text in texts:
        matches = []
        for kind, word in engine.spelling_matches(text, checks):
            if not (isinstance(kind, str) and isinstance(word, str)):
                raise TypeError("spelling_matches must yield (kind, word) string pairs")
            matches.append([kind, word])
        findings.append(matches)
    payload = (json.dumps({"nonce": nonce, "findings": findings},
                          ensure_ascii=True) + "\n").encode("ascii")
    while payload:
        payload = payload[os.write(result_fd, payload):]
    os._exit(0)  # seal the result: no engine teardown code runs after it


if __name__ == "__main__":
    main()
