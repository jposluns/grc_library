#!/usr/bin/env python3
"""Isolated-launch import audit (grc gate 109).

``python3 -I`` (isolated mode) leaves the script's own directory off
``sys.path``, so a file planted beside a tool cannot shadow a standard-library
module. It also means a tool that imports a sibling module from ``tools/``
(``lint_common``, ``aiqt_bootstrap`` and the rest) without putting its own
directory on the path fails on that import. Before the runners can launch the
gates with ``-I``, every tool must reach its sibling modules by appending its own
resolved directory to the END of ``sys.path`` (after the standard library and
site-packages, never at index 0). This gate tracks that conversion and keeps it
from regressing.

For every ``tools/*.py`` it starts a child ``python3 -I -B`` that installs an
audit hook and then executes the tool's source as a module named other than
``__main__``, so the tool runs its module-level code (its imports) but not its
``if __name__ == "__main__"`` entry point. The audit hook refuses, by raising
``PermissionError``, every process start (``subprocess.Popen``, ``os.system``,
``os.exec*``, ``os.spawn*``, ``os.posix_spawn*``, ``os.fork``), every file open
for writing and every file-system mutation (remove, rename, mkdir, chmod and the
like), outbound sockets, and ``os.kill``; reads are allowed. A finder appended to
the end of ``sys.meta_path`` records each top-level import of a ``tools/`` sibling
that no other finder resolved, so a sibling ImportError the tool catches and
swallows still counts. The child's own output is written to a duplicated
descriptor with a per-run token, and the child imports no module beyond
``importlib.util`` before the tool runs, so it does not mask a planted
standard-library shadow with a cached copy.

Each tool gets one of three outcomes:

- ``ok``: its module-level code ran under ``-I`` with no sibling miss.
- ``sibling``: at least one sibling import was not resolved (the first is named).
- ``error``: no sibling miss, but the module-level code raised another exception
  (a refused action, a planted module, any failure), so the probe cannot show
  that its imports complete. ``SystemExit`` counts as ``error`` too.

``BASELINE`` below lists the tools not yet converted (outcome ``sibling`` today).
A finding (exit 1) is: a tool off the list whose outcome is not ``ok``; a tool on
the list whose outcome is ``ok`` (remove it, so the list only shrinks); a tool on
the list whose outcome is ``error``; and a list entry that names no ``tools/*.py``.
A probe that times out or returns no result exits 2.

Residue, stated: the probe runs module-level code only, so a sibling imported
inside a function (a lazy import) is not seen until that function runs; the
probe does not run the tool's entry point, its arguments or its subprocesses; a
write or process start refused here is reported only as an ``error`` outcome, not
proved harmless; and the probe imports ``importlib.util`` itself, so a planted
module of that name is not exercised.

Usage:
    python3 tools/lint-isolated-launch.py
    python3 tools/lint-isolated-launch.py --self-test

Exit codes: 0 clean; 1 findings (or a failed self-test); 2 a probe that timed out
or returned no result.

Stdlib-only Python 3.11. It imports no sibling module, so it passes its own check.
"""

from __future__ import annotations

import argparse
import ast
import os
import secrets
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
PROBE_TIMEOUT = 60  # seconds for one tool's child process
WORKERS = min(8, os.cpu_count() or 1)

# Tools whose first sibling import fails under -I today. Remove a name when its tool
# is converted to the append form; the gate fails until the stale entry is removed.
BASELINE = frozenset("""
    audit-cross-repo-references.py
    audit-held-branch-expiry.py
    audit-matrix-semantic-fit.py
    audit-provision-siblings.py
    audit-reference-acquisition-gaps.py
    audit-reference-breadth.py
    build-corpus-management.py
    build-provision-index.py
    build-todo-number-allocation.py
    check-alignment-register-on-pr.py
    check-changelog-dash-on-pr.py
    check-changelog-length-on-pr.py
    check-changelog-on-pr.py
    check-date-cobump-on-pr.py
    check-narrative-corpus-mixed-diff-on-pr.py
    check-review-cadence.py
    check-version-bump-on-pr.py
    decisions-search.py
    detect-collection-candidates.py
    lint-acronym-consistency.py
    lint-bare-normative-shall.py
    lint-bookkeeping-parity.py
    lint-ccm-aicm-citations.py
    lint-ccm-provider-member-in-range.py
    lint-changelog-link-coverage.py
    lint-changelog-mirror-header-parity.py
    lint-citation-verification-freshness.py
    lint-citations.py
    lint-claude-rules-sync.py
    lint-cobit-iso31000-citations.py
    lint-cobit-title-text.py
    lint-collection-enumeration-consistency.py
    lint-cross-doc-numbers.py
    lint-cross-file-section-names.py
    lint-cross-file-section-refs.py
    lint-date-format.py
    lint-directional-dependency.py
    lint-document-control-codes.py
    lint-document-date-staleness.py
    lint-document-iso-annex-a.py
    lint-external-link-domains.py
    lint-external-overlay-license.py
    lint-filename-title-alignment.py
    lint-followup-ageing.py
    lint-gate-citation-inventory.py
    lint-gate-count-consistency.py
    lint-guardrail-cadence.py
    lint-internal-references.py
    lint-intra-doc-refs.py
    lint-language.py
    lint-library-version-monotonicity.py
    lint-license-consistency.py
    lint-links.py
    lint-listing-surface-completeness.py
    lint-matrix-control-codes.py
    lint-metadata-line-breaks.py
    lint-metadata.py
    lint-narrative-authority-boundary.py
    lint-narrative-boundary.py
    lint-narrative-disclaimer.py
    lint-narrative-metadata.py
    lint-narrative-vocabulary.py
    lint-nested-markdown-links.py
    lint-orphan-documents.py
    lint-overnight-file.py
    lint-paired-skill-step-parity.py
    lint-pii-in-content.py
    lint-placeholder-leakage.py
    lint-positional-backlog-tokens.py
    lint-ref-absence-claims.py
    lint-required-sections.py
    lint-retention-consistency.py
    lint-roles.py
    lint-rule-scope-table.py
    lint-scan-scope-parity.py
    lint-secrets-in-content.py
    lint-section-anchors.py
    lint-section-placement.py
    lint-session-state.py
    lint-shall-near-uncertainty.py
    lint-skill-derives-from.py
    lint-skill-internal-refs.py
    lint-standards-currency.py
    lint-stub-documents.py
    lint-todo-list-tag.py
    lint-todo-marked-done.py
    lint-todo-number-permanence.py
    lint-todo-staleness.py
    lint-tooling-backlog-refs.py
    lint-tooling-provenance-freshness.py
    lint-unbalanced-fences.py
    lint-ungated-dashes.py
    lint-version-bump-recency.py
    lint-web-corpus-links.py
    lint-worker-id-anonymity.py
    lint-working-prose-hygiene.py
    provision_citations.py
    ref-holds.py
    sweep-preflight-scanner.py
    verify-reference-modules.py
""".split())

# The child program. argv: token, script path, mode ("isolated" or "plain"). It imports
# nothing beyond importlib.util before the tool runs, and reports with repr() rather
# than json so that json stays unimported for the tool (a planted json.py is exercised).
PROBE = r'''
import importlib.util
import os
import sys

token, script, mode = sys.argv[1], sys.argv[2], sys.argv[3]
tools = os.path.dirname(os.path.abspath(script))
siblings = {n[:-3] for n in os.listdir(tools) if n.endswith(".py") and n[:-3].isidentifier()}
if mode == "plain":
    # `python3 tools/X.py` puts the script's directory first, where -c put ''.
    sys.path[:1] = [tools] if sys.path[:1] == [""] else [tools, *sys.path[:1]]
out = os.dup(1)
null = os.open(os.devnull, os.O_WRONLY)
os.dup2(null, 1)
missed, refused = [], []


class SiblingMissRecorder:
    """Last finder on sys.meta_path: reached only when no other finder resolved a name."""

    @staticmethod
    def find_spec(name, path=None, target=None):
        if path is None and name in siblings and name not in missed:
            missed.append(name)
        return None


WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_TRUNC
REFUSED = frozenset((
    "subprocess.Popen", "os.system", "os.fork", "os.forkpty", "pty.spawn", "os.startfile",
    "os.kill", "os.killpg",
    "os.remove", "os.rename", "os.mkdir", "os.rmdir", "os.symlink", "os.link", "os.chmod",
    "os.chown", "os.chflags", "os.lchflags", "os.truncate", "os.utime", "os.mkfifo",
    "os.mknod", "os.setxattr", "os.removexattr",
    "shutil.copyfile", "shutil.copymode", "shutil.copystat", "shutil.copytree",
    "shutil.rmtree", "shutil.move", "shutil.chown", "shutil.make_archive",
    "shutil.unpack_archive", "tempfile.mkstemp", "tempfile.mkdtemp",
    "socket.connect", "socket.bind", "socket.sendto", "socket.sendmsg",
))


def hook(event, args):
    if event == "open":
        mode = args[1] if len(args) > 1 else None
        flags = args[2] if len(args) > 2 else 0
        if not ((isinstance(mode, str) and any(c in mode for c in "wax+"))
                or (isinstance(flags, int) and flags & WRITE_FLAGS)):
            return
    elif not (event in REFUSED or event.startswith(("os.exec", "os.spawn", "os.posix_spawn"))):
        return
    refused.append(event)
    raise PermissionError("isolated-launch probe refused " + event)


sys.meta_path.append(SiblingMissRecorder)
name = "__isolated_launch_probe__"
spec = importlib.util.spec_from_file_location(name, script)
module = importlib.util.module_from_spec(spec)
sys.modules[name] = module
sys.argv = [script]
sys.addaudithook(hook)
error = None
try:
    spec.loader.exec_module(module)
except BaseException as exc:  # every outcome is reported, SystemExit included
    error = type(exc).__name__ + ": " + str(exc)[:300]
os.write(out, (token + repr((missed, error, refused)) + "\n").encode("utf-8", "backslashreplace"))
os._exit(0)
'''


class ProbeError(Exception):
    """A probe timed out or returned no result (exit 2)."""


def probe(script: Path, *, isolated: bool = True) -> dict:
    """Run one tool's module-level code in a child under the audit hook and return
    ``{"status", "missed", "error", "refused"}``. ``isolated=False`` runs the child
    without ``-I`` and with the tool's directory first on ``sys.path``, as a plain
    ``python3 tools/X.py`` launch has it (used to compare the two launches)."""
    token = "isolated-launch-result " + secrets.token_hex(16) + " "
    flags = ["-I", "-B"] if isolated else ["-B"]
    try:
        proc = subprocess.run(
            [sys.executable, *flags, "-c", PROBE, token, str(script),
             "isolated" if isolated else "plain"],
            cwd=REPO_ROOT, stdin=subprocess.DEVNULL, capture_output=True,
            timeout=PROBE_TIMEOUT)
    except subprocess.TimeoutExpired as exc:
        raise ProbeError(f"{script.name}: probe timed out after {PROBE_TIMEOUT}s") from exc
    lines = [ln for ln in proc.stdout.decode("utf-8", "replace").splitlines()
             if ln.startswith(token)]
    if len(lines) != 1:
        tail = proc.stderr.decode("utf-8", "replace").strip().splitlines()[-3:]
        raise ProbeError(f"{script.name}: probe returned no result (exit {proc.returncode}): "
                         + " | ".join(tail))
    missed, error, refused = ast.literal_eval(lines[0][len(token):])
    status = "sibling" if missed else "error" if error else "ok"
    return {"status": status, "missed": missed, "error": error, "refused": refused}


def probe_all(tools_dir: Path, *, isolated: bool = True) -> dict[str, dict]:
    """Probe every regular ``*.py`` file directly in ``tools_dir``, by file name."""
    scripts = sorted(p for p in tools_dir.glob("*.py") if p.is_file())
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        results = list(pool.map(lambda p: probe(p, isolated=isolated), scripts))
    return {p.name: r for p, r in zip(scripts, results)}


def findings_for(results: dict[str, dict], baseline: frozenset[str]) -> list[str]:
    """The ratchet: off-list failures, on-list passes and errors, and dangling entries."""
    out = []
    for name in sorted(set(results) | baseline):
        result = results.get(name)
        if result is None:
            out.append(f"tools/{name}: on BASELINE but there is no such tools/*.py; remove it")
            continue
        status = result["status"]
        if name in baseline and status == "ok":
            out.append(f"tools/{name}: on BASELINE but now launches under -I; remove it from BASELINE")
        elif name in baseline and status == "error":
            out.append(f"tools/{name}: on BASELINE, but its module-level code raised "
                       f"{result['error']} (refused: {result['refused']})")
        elif name not in baseline and status == "sibling":
            out.append(f"tools/{name}: sibling import {result['missed'][0]!r} fails under "
                       f"python3 -I; append the tool's own directory to the end of sys.path")
        elif name not in baseline and status == "error":
            out.append(f"tools/{name}: module-level code raised {result['error']} under "
                       f"python3 -I (refused: {result['refused']})")
    return out


def _self_test() -> int:
    """Fixture tools in a temporary directory, one per outcome and per refusal."""
    failures = []

    def check(label, actual, expected):
        if actual != expected:
            failures.append(f"{label}: expected {expected!r}, got {actual!r}")

    append = ("import sys\nfrom pathlib import Path\n"
              "sys.path.append(str(Path(__file__).resolve().parent))\n")
    with tempfile.TemporaryDirectory() as tmp:
        tools = Path(tmp) / "tools"
        tools.mkdir()
        written, spawned = Path(tmp) / "written", Path(tmp) / "spawned"
        fixtures = {
            "helper_mod.py": "VALUE = 1\n",
            "plain_ok.py": "import string\n",
            "needs_sibling.py": "import string\nimport helper_mod\n",
            "swallowed.py": "try:\n    import helper_mod\nexcept ImportError:\n    helper_mod = None\n",
            "anchored.py": append + "import helper_mod\n",
            "guarded_main.py": "def main():\n    import helper_mod\n"
                               "if __name__ == '__main__':\n    main()\n",
            "writer.py": f"try:\n    open({str(written)!r}, 'w')\nexcept PermissionError:\n    pass\n",
            "spawner.py": "import subprocess, sys\ntry:\n    subprocess.run([sys.executable, '-c', "
                          f"{'open(%r, chr(119))' % str(spawned)!r}])\n"
                          "except PermissionError:\n    pass\n",
            "execer.py": "import os, sys\ntry:\n    os.execv(sys.executable, [sys.executable, '-V'])\n"
                         "except PermissionError:\n    pass\n",
            "remover.py": "import os\nos.remove(__file__)\n",
            # A planted json.py beside the tools raises if it is ever imported.
            "json.py": "raise RuntimeError('planted json.py imported')\n",
            "uses_json_append.py": append + "import json\njson.dumps(1)\n",
            "uses_json_insert.py": append.replace("sys.path.append(", "sys.path.insert(0, ")
                                   + "import json\n",
        }
        for name, text in fixtures.items():
            (tools / name).write_text(text, encoding="utf-8")
        results = probe_all(tools)
        statuses = {n: r["status"] for n, r in results.items()}
        check("statuses", statuses, {
            "helper_mod.py": "ok", "plain_ok.py": "ok", "needs_sibling.py": "sibling",
            "swallowed.py": "sibling", "anchored.py": "ok", "guarded_main.py": "ok",
            "writer.py": "ok", "spawner.py": "ok", "execer.py": "ok", "remover.py": "error",
            "json.py": "error", "uses_json_append.py": "ok", "uses_json_insert.py": "error",
        })
        check("needs_sibling missed", results["needs_sibling.py"]["missed"], ["helper_mod"])
        check("swallowed missed", results["swallowed.py"]["missed"], ["helper_mod"])
        check("writer refused", results["writer.py"]["refused"], ["open"])
        check("spawner refused", results["spawner.py"]["refused"], ["subprocess.Popen"])
        check("execer refused", results["execer.py"]["refused"], ["os.exec"])
        check("remover refused", results["remover.py"]["refused"], ["os.remove"])
        check("planted json error", results["uses_json_insert.py"]["error"],
              "RuntimeError: planted json.py imported")
        check("nothing written", written.exists(), False)
        check("nothing spawned", spawned.exists(), False)
        check("remover kept", (tools / "remover.py").is_file(), True)
        plain = probe(tools / "needs_sibling.py", isolated=False)
        check("plain launch resolves the sibling", (plain["status"], plain["missed"]), ("ok", []))

        expected_unlisted = ["json.py", "needs_sibling.py", "remover.py", "swallowed.py",
                             "uses_json_insert.py"]
        unlisted = findings_for(results, frozenset())
        check("empty baseline flags", [f.split(":")[0][len("tools/"):] for f in unlisted],
              expected_unlisted)
        listed = frozenset({"needs_sibling.py", "swallowed.py"})
        check("baselined failures pass", [f for f in findings_for(results, listed)
                                          if "needs_sibling" in f or "swallowed" in f], [])
        stale = findings_for(results, listed | {"plain_ok.py", "ghost.py", "remover.py"})
        check("stale baseline entries", [f for f in stale if "BASELINE" in f], [
            "tools/ghost.py: on BASELINE but there is no such tools/*.py; remove it",
            "tools/plain_ok.py: on BASELINE but now launches under -I; remove it from BASELINE",
            "tools/remover.py: on BASELINE, but its module-level code raised PermissionError: "
            "isolated-launch probe refused os.remove (refused: ['os.remove'])",
        ])
    for failure in failures:
        print(f"SELF-TEST FAIL: {failure}")
    if failures:
        return 1
    print("SELF-TEST OK: outcomes, refusals, planted-shadow and baseline ratchet behave as documented")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Isolated-launch import audit (gate 109).")
    parser.add_argument("--self-test", action="store_true",
                        help="run the built-in fixture checks and exit")
    args = parser.parse_args(argv)
    if args.self_test:
        try:
            return _self_test()
        except ProbeError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
    try:
        results = probe_all(TOOLS_DIR)
    except ProbeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    findings = findings_for(results, BASELINE)
    if findings:
        for finding in findings:
            print(finding)
        print(f"\nFAIL: {len(findings)} isolated-launch finding(s).")
        return 1
    converted = sum(1 for r in results.values() if r["status"] == "ok")
    print(f"OK: {converted} of {len(results)} tools/*.py launch under python3 -I up to their "
          f"imports; {len(BASELINE)} not yet converted are on BASELINE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
