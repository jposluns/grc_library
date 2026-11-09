#!/usr/bin/env python3
"""Isolated-launch import audit (grc gate 109).

``python3 -I`` (isolated mode) leaves the script's own directory off
``sys.path``, so a file planted beside a tool cannot shadow a standard-library
module. It also means a tool that imports a sibling module from ``.claude/skills/corpus-management/tools/``
(``lint_common``, ``aiqt_bootstrap`` and the rest) without putting its own
directory on the path fails on that import. Before the runners can launch the
gates with ``-I``, every tool must reach its sibling modules by appending its own
resolved directory to the END of ``sys.path`` (after the standard library and
site-packages, never at index 0). This gate tracks that conversion and keeps it
from regressing.

The probe checks module-level imports, not a full command launch. For every
``.claude/skills/corpus-management/tools/*.py`` it starts a child ``python3 -I -B`` that installs an audit hook and
then executes the tool's source as a module named other than ``__main__``, so the
tool runs its module-level code (its imports) but not its
``if __name__ == "__main__"`` entry point. The audit hook refuses, by raising
``PermissionError``, the audited events listed in ``REFUSED`` and ``REFUSED_PREFIXES``
in the probe below: the process starts ``subprocess.Popen``,
``_posixsubprocess.fork_exec``, ``os.system``, ``os.exec*``, ``os.spawn*``,
``os.posix_spawn*`` and ``os.fork``; an ``open`` for writing and the listed
file-system mutations (remove, rename, mkdir, chmod and the like); outbound
sockets (``socket.connect``, ``socket.bind``, ``socket.sendto`` and
``socket.sendmsg``; a name lookup is not refused, see the residue); ``os.kill``; every ``ctypes.*`` event (``ctypes.dlopen``, raised by
``import ctypes`` itself, ``ctypes.dlsym``, ``ctypes.call_function`` and the rest);
and every ``sqlite3.*`` event (``sqlite3.connect`` and the extension loads). Reads
are allowed. A finder appended to the end of ``sys.meta_path`` records each
top-level import of a ``.claude/skills/corpus-management/tools/`` sibling that no other finder resolved, so a
sibling ImportError the tool catches and swallows still counts. The child's own
output is written to a duplicated descriptor with a per-run token, and the child
imports no module beyond ``importlib.util`` before the tool runs, so it does not
mask a planted standard-library shadow with a cached copy.

Each tool gets one of three outcomes:

- ``ok``: its module-level code ran under ``-I`` with no sibling miss.
- ``sibling``: at least one sibling import was not resolved (the first is named),
  and any exception raised was the ``ImportError`` for a missed sibling.
- ``error``: the module-level code raised any other exception (a refused action, a
  planted module, any failure), so the probe cannot show that its imports complete,
  whether or not a sibling was also missed. ``SystemExit`` counts as ``error`` too.

Separately, each tool's source is read statically for a ``sys.path.insert(...)``
call at any index, a ``sys.path.__setitem__``, ``__iadd__``, ``sort`` or
``reverse`` call, an assignment or augmented assignment (``+=``) to ``sys.path`` or
to an item or slice of it, or a rebinding of ``sys.path`` (``sys`` reached by name,
by an ``import sys as`` alias or by ``from sys import path``), anywhere in the file,
inside functions included.
Each of these can put the tool's own directory, or the corpus-management pack's
``.claude/skills/corpus-management/src/tools``, ahead of the standard library, which the append form
forbids. The check is static because most such inserts run inside a function
(the lazy engine import), which the module-level probe never reaches; it is
conservative, so ``sys.path.insert(len(sys.path), ...)``,
``sys.path = sys.path + [...]`` or ``sys.path += [...]`` is reported too (use
``append``).

Exactly one form of assignment is accepted, an order-preserving filter:
``sys.path[:] = [<name> for <name> in sys.path if <condition>]``. To be accepted,
the statement must be a plain assignment (not annotated, augmented or chained) with
one target, the whole slice ``sys.path[:]`` (no start, stop or step). Its value must
be a list comprehension with exactly one ``for`` clause, which is not ``async``.
That clause's iterable must be ``sys.path`` written the same way as the target (the
same ``sys`` name or alias, or the same ``from sys import path`` name), and its loop
target must be a single name. The yielded element must be that same name,
unchanged. The clause may have any number of ``if`` conditions, none included. Such
a statement only removes entries and keeps the order of the rest, so it cannot put a
directory ahead of the standard library. Every other assignment to ``sys.path`` or to
a slice of it is still reported. That includes a comprehension that yields a changed
element, one over a different list, one with a second ``for`` clause, a generator
expression, ``list(...)`` or ``filter(...)``, a partial slice such as
``sys.path[1:]``, and ``sys.path = [...]``, even with the accepted comprehension
as its value. The ``if`` conditions are walked like the rest of the file, so a
listed method call inside them (``sys.path.insert(...)``) is still reported on its
own line.

``BASELINE`` lists the tools whose sibling import fails today; ``INSERT_BASELINE``
lists the tools that insert into or assign ``sys.path`` today. A tool counts as
converted only when its outcome is ``ok`` and it is on neither list. A finding
(exit 1) is: an ``error`` outcome, on a list or off it; a tool off ``BASELINE``
whose outcome is ``sibling``; a tool on ``BASELINE`` whose outcome is ``ok``; a
tool off ``INSERT_BASELINE`` with an insert or assignment; a tool on
``INSERT_BASELINE`` with none; and a list entry that names no ``.claude/skills/corpus-management/tools/*.py``. So
both lists only shrink. A probe that times out or returns no result exits 2.

Residue, stated: the probe runs module-level code only, so a sibling imported
inside a function (a lazy import) is not seen until that function runs, and a
module-level pass does not show that the command launches (an import made only
under ``__main__`` passes here and can fail as a script; an import that fails here
can be one the script never reaches); the probe does not run the tool's entry
point, its arguments or its subprocesses; a refused event is reported only as an
``error`` outcome, not proved harmless; the hook sees only audited events, so a
native call through a library already loaded in the child without a ``ctypes``
event (a C extension function that raises no audit event, ``os.write`` to an
inherited descriptor) is not refused; ``_posixsubprocess.fork_exec`` raises its
audit event on the Python 3.14 this was checked on and may not on an older
interpreter; the probed tool runs in the child's process, so it can read the token
and forge the result line on the inherited descriptor (the probed tools are
repository-tracked code, reviewed like this gate); a name lookup
(``socket.getaddrinfo``, ``socket.gethostbyname``), which can send a DNS query, is
not refused; the static ``sys.path`` check does not see a mutation through
``getattr`` or ``setattr``, through ``sys`` reached by ``__import__("sys")``,
``importlib.import_module("sys")`` or ``sys.modules["sys"]``, through a list
reached under another name, or through a method or operator it does not list
(``del sys.path[...]``, ``remove`` and ``pop``, which drop entries, are not
reported); the accepted filter ``sys.path[:] = [<name> for <name> in sys.path if
<condition>]`` is recognised by its syntax alone: its conditions are not evaluated,
a function they call is not followed (a ``sys.path`` change inside a function
defined in this file is reported on its own line, one in another module is not
seen), and a ``sys`` alias or ``from sys import path`` name that is later rebound
to another list without an assignment (as a parameter, loop variable or ``with``
target) is still taken for ``sys.path``, as everywhere in the check; a tool counted as converted can still run another tool's insert by
loading that tool's source (``importlib`` ``exec_module``, ``runpy.run_path``):
``check-generated-commit.py`` loads ``build-taxonomy.py`` and
``adopt-bootstrap-ref.py`` loads ``build-reference-manifest.py``, both on
``INSERT_BASELINE``, and the load targets are paths computed at run time, so the
transitive case is not checked; and the probe imports ``importlib.util`` itself, so
a planted module of that name is not exercised.

Usage:
    python3 .claude/skills/corpus-management/tools/lint-isolated-launch.py
    python3 .claude/skills/corpus-management/tools/lint-isolated-launch.py --self-test

Exit codes: 0 clean; 1 findings (or a failed self-test); 2 a probe that timed out
or returned no result, or a tool whose source does not parse.

Stdlib-only Python 3.14. It imports no sibling module, so it passes its own check.
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

REPO_ROOT = Path(__file__).resolve().parents[4]
TOOLS_DIR = Path(__file__).resolve().parent
PROBE_TIMEOUT = 60  # seconds for one tool's child process
WORKERS = min(8, os.cpu_count() or 1)

# Tools whose first sibling import fails under -I today. Remove a name when its tool
# is converted to the append form; the gate fails until the stale entry is removed.
BASELINE = frozenset("""
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
    lint-acronym-consistency.py
    lint-bare-normative-shall.py
    lint-ccm-aicm-citations.py
    lint-ccm-provider-member-in-range.py
    lint-changelog-link-coverage.py
    lint-changelog-mirror-header-parity.py
    lint-citation-verification-freshness.py
    lint-citations.py
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
    lint-filename-title-alignment.py
    lint-gate-citation-inventory.py
    lint-gate-count-consistency.py
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
    lint-pii-in-content.py
    lint-placeholder-leakage.py
    lint-positional-backlog-tokens.py
    lint-ref-absence-claims.py
    lint-required-sections.py
    lint-retention-consistency.py
    lint-roles.py
    lint-scan-scope-parity.py
    lint-secrets-in-content.py
    lint-section-anchors.py
    lint-section-placement.py
    lint-shall-near-uncertainty.py
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
    provision_citations.py
    sweep-preflight-scanner.py
    verify-reference-modules.py
""".split())

# Tools that call sys.path.insert(...) or assign sys.path today (their own directory or
# the corpus-management pack's .claude/skills/corpus-management/tools/, at index 0). Remove a name when its tool is
# converted to sys.path.append; the gate fails until the stale entry is removed.
INSERT_BASELINE = frozenset("""
    build-alignment-citation-registry.py
    build-citation-publishers.py
    build-corpus-management.py
    build-historical-citation-exceptions.py
    build-narrative-registry.py
    build-reference-manifest.py
    build-taxonomy.py
    check-class-completeness.py
    check-retired-section-orphan-on-pr.py
    check-stranded-control-code-on-pr.py
    check-todo-rotation-on-pr.py
    lint-acronym-consistency.py
    lint-aiqt-vendor-digest.py
    lint-alignment-citation-existence.py
    lint-allowlist-spec-parity.py
    lint-audit-gate-parity.py
    lint-bare-normative-shall.py
    lint-ccm-aicm-citations.py
    lint-ccm-provider-member-in-range.py
    lint-citation-currency-cadence.py
    lint-citations.py
    lint-cobit-iso31000-citations.py
    lint-cobit-title-text.py
    lint-collection-enumeration-consistency.py
    lint-cross-doc-numbers.py
    lint-cross-file-section-names.py
    lint-cross-file-section-refs.py
    lint-date-format.py
    lint-directional-dependency.py
    lint-doctype-parity.py
    lint-document-control-codes.py
    lint-document-date-staleness.py
    lint-document-iso-annex-a.py
    lint-external-link-domains.py
    lint-filename-title-alignment.py
    lint-gate-citation-inventory.py
    lint-gate-count-consistency.py
    lint-index-header-parity.py
    lint-internal-references.py
    lint-intra-doc-refs.py
    lint-language.py
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
    lint-pii-in-content.py
    lint-placeholder-leakage.py
    lint-positional-backlog-tokens.py
    lint-required-sections.py
    lint-retention-consistency.py
    lint-roles.py
    lint-secrets-in-content.py
    lint-section-anchors.py
    lint-section-placement.py
    lint-shall-near-uncertainty.py
    lint-sibling-placeholders.py
    lint-skill-verdict-carrier-completeness.py
    lint-ssdf-control-ids.py
    lint-standards-currency.py
    lint-startup-character-ceiling.py
    lint-structure.py
    lint-stub-documents.py
    lint-table-cell-count.py
    lint-todo-index-reference-parity.py
    lint-todo-marked-done.py
    lint-todo-staleness.py
    lint-unbalanced-fences.py
    lint-ungated-dashes.py
    preflight-changelog.py
    preflight-version-date.py
    residual-scan.py
    sweep-preflight-scanner.py
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
    # `python3 .claude/skills/corpus-management/tools/X.py` puts the script's directory first, where -c put ''.
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
    "subprocess.Popen", "_posixsubprocess.fork_exec", "os.system", "os.fork", "os.forkpty",
    "pty.spawn", "os.startfile",
    "os.kill", "os.killpg",
    "os.remove", "os.rename", "os.mkdir", "os.rmdir", "os.symlink", "os.link", "os.chmod",
    "os.chown", "os.chflags", "os.lchflags", "os.truncate", "os.utime", "os.mkfifo",
    "os.mknod", "os.setxattr", "os.removexattr",
    "shutil.copyfile", "shutil.copymode", "shutil.copystat", "shutil.copytree",
    "shutil.rmtree", "shutil.move", "shutil.chown", "shutil.make_archive",
    "shutil.unpack_archive", "tempfile.mkstemp", "tempfile.mkdtemp",
    "socket.connect", "socket.bind", "socket.sendto", "socket.sendmsg",
))
# ctypes.* covers ctypes.dlopen (raised by `import ctypes` itself), ctypes.dlsym and
# ctypes.call_function; sqlite3.* covers sqlite3.connect and the extension loads.
REFUSED_PREFIXES = ("os.exec", "os.spawn", "os.posix_spawn", "ctypes.", "sqlite3.")


def hook(event, args):
    if event == "open":
        mode = args[1] if len(args) > 1 else None
        flags = args[2] if len(args) > 2 else 0
        if not ((isinstance(mode, str) and any(c in mode for c in "wax+"))
                or (isinstance(flags, int) and flags & WRITE_FLAGS)):
            return
    elif not (event in REFUSED or event.startswith(REFUSED_PREFIXES)):
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
error, error_is_miss = None, False
try:
    spec.loader.exec_module(module)
except BaseException as exc:  # every outcome is reported, SystemExit included
    error = type(exc).__name__ + ": " + str(exc)[:300]
    # Only the ImportError for a sibling the finder recorded is the sibling outcome.
    error_is_miss = isinstance(exc, ImportError) and exc.name in missed
os.write(out, (token + repr((missed, error, error_is_miss, refused)) + "\n")
         .encode("utf-8", "backslashreplace"))
os._exit(0)
'''


class ProbeError(Exception):
    """A probe timed out or returned no result (exit 2)."""


def probe(script: Path, *, isolated: bool = True) -> dict:
    """Run one tool's module-level code in a child under the audit hook and return
    ``{"status", "missed", "error", "refused"}``. ``isolated=False`` runs the child
    without ``-I`` and with the tool's directory first on ``sys.path``, as a plain
    ``python3 .claude/skills/corpus-management/tools/X.py`` launch has it (used to compare the two launches)."""
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
    missed, error, error_is_miss, refused = ast.literal_eval(lines[0][len(token):])
    # An exception other than the missed sibling's own ImportError is an error even when
    # a sibling was also missed, so a baselined tool that raises is not accepted.
    status = "error" if error and not error_is_miss else "sibling" if missed else "ok"
    return {"status": status, "missed": missed, "error": error, "refused": refused}


# sys.path methods that can put an entry ahead of the standard library: insert at any
# index, the item-assignment and in-place-add dunders, and the two reorderings.
REORDERING_METHODS = frozenset({"insert", "__setitem__", "__iadd__", "sort", "reverse"})


def path_inserts(script: Path) -> list[int]:
    """Line numbers in ``script`` of each call of a ``REORDERING_METHODS`` method on
    ``sys.path`` (``sys.path.insert(...)`` at any index among them), assignment or
    augmented assignment to ``sys.path`` or to an item or slice of it, or rebinding
    of ``sys.path``, anywhere in the file. ``sys`` is recognised by name, by an
    ``import sys as`` alias, and ``path`` by ``from sys import path [as ...]``.
    The one exception is an assignment ``is_order_preserving_filter`` accepts,
    ``sys.path[:] = [<name> for <name> in sys.path if <condition>]``.
    Raises ``SyntaxError`` for a file that does not parse."""
    tree = ast.parse(script.read_bytes(), filename=str(script))
    sys_names, path_names = {"sys"}, set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            sys_names |= {a.asname for a in node.names if a.name == "sys" and a.asname}
        elif isinstance(node, ast.ImportFrom) and node.module == "sys" and not node.level:
            path_names |= {a.asname or a.name for a in node.names if a.name == "path"}

    def is_path(node: ast.expr) -> bool:
        return ((isinstance(node, ast.Attribute) and node.attr == "path"
                 and isinstance(node.value, ast.Name) and node.value.id in sys_names)
                or (isinstance(node, ast.Name) and node.id in path_names))

    lines = set()
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr in REORDERING_METHODS and is_path(node.func.value)):
            lines.add(node.lineno)
        elif is_order_preserving_filter(node, is_path):
            continue
        elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                for t in ast.walk(target):
                    if (isinstance(t, ast.Subscript) and is_path(t.value)) or (
                            is_path(t) and isinstance(t.ctx, ast.Store)):
                        lines.add(node.lineno)
    return sorted(lines)


def is_order_preserving_filter(node: ast.AST, is_path) -> bool:
    """True only for ``sys.path[:] = [<name> for <name> in sys.path if <condition>]``:
    a plain ``ast.Assign`` with one target, the whole slice of a ``sys.path``
    reference (no start, stop or step), whose value is a list comprehension with one
    non-``async`` ``for`` clause over that same reference (equal by ``ast.dump``),
    a single-name loop target, the element yielded as that name unchanged, and any
    number of ``if`` conditions. ``is_path`` is ``path_inserts``' recogniser."""
    if not (isinstance(node, ast.Assign) and len(node.targets) == 1):
        return False
    target, value = node.targets[0], node.value
    if not (isinstance(target, ast.Subscript) and is_path(target.value)
            and isinstance(target.slice, ast.Slice) and target.slice.lower is None
            and target.slice.upper is None and target.slice.step is None):
        return False
    if not (isinstance(value, ast.ListComp) and len(value.generators) == 1):
        return False
    gen = value.generators[0]
    return (not gen.is_async
            and ast.dump(gen.iter) == ast.dump(target.value)
            and isinstance(gen.target, ast.Name) and isinstance(value.elt, ast.Name)
            and value.elt.id == gen.target.id)


def inserts_all(tools_dir: Path) -> dict[str, list[int]]:
    """``path_inserts`` for every regular ``*.py`` file directly in ``tools_dir``."""
    out = {}
    for p in sorted(p for p in tools_dir.glob("*.py") if p.is_file()):
        try:
            out[p.name] = path_inserts(p)
        except SyntaxError as exc:
            raise ProbeError(f"{p.name}: source does not parse: {exc}") from exc
    return out


def probe_all(tools_dir: Path, *, isolated: bool = True) -> dict[str, dict]:
    """Probe every regular ``*.py`` file directly in ``tools_dir``, by file name."""
    scripts = sorted(p for p in tools_dir.glob("*.py") if p.is_file())
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        results = list(pool.map(lambda p: probe(p, isolated=isolated), scripts))
    return {p.name: r for p, r in zip(scripts, results)}


def findings_for(results: dict[str, dict], baseline: frozenset[str],
                 inserts: dict[str, list[int]] | None = None,
                 insert_baseline: frozenset[str] = frozenset()) -> list[str]:
    """The two ratchets: off-list failures, on-list passes, errors on or off a list,
    and dangling entries. ``inserts`` (``inserts_all`` output) is checked against
    ``insert_baseline`` when given."""
    out = []
    for name in sorted(set(results) | baseline):
        result = results.get(name)
        if result is None:
            out.append(f".claude/skills/corpus-management/tools/{name}: on BASELINE but there is no such .claude/skills/corpus-management/tools/*.py; remove it")
            continue
        status = result["status"]
        if status == "error":
            listed = "on BASELINE, but its" if name in baseline else "its"
            missed = f", sibling miss {result['missed']}" if result["missed"] else ""
            out.append(f".claude/skills/corpus-management/tools/{name}: {listed} module-level code raised {result['error']} "
                       f"under python3 -I (refused: {result['refused']}{missed})")
        elif name in baseline and status == "ok":
            out.append(f".claude/skills/corpus-management/tools/{name}: on BASELINE but now imports under -I; remove it from BASELINE")
        elif name not in baseline and status == "sibling":
            out.append(f".claude/skills/corpus-management/tools/{name}: sibling import {result['missed'][0]!r} fails under "
                       f"python3 -I; append the tool's own directory to the end of sys.path")
    if inserts is not None:
        for name in sorted(set(inserts) | insert_baseline):
            lines = inserts.get(name)
            if lines is None:
                out.append(f".claude/skills/corpus-management/tools/{name}: on INSERT_BASELINE but there is no such .claude/skills/corpus-management/tools/*.py; "
                           f"remove it")
            elif lines and name not in insert_baseline:
                out.append(f".claude/skills/corpus-management/tools/{name}:{lines[0]}: inserts into or assigns sys.path (lines "
                           f"{lines}), which can put a directory ahead of the standard library; "
                           f"append to the end of sys.path instead")
            elif not lines and name in insert_baseline:
                out.append(f".claude/skills/corpus-management/tools/{name}: on INSERT_BASELINE but no longer inserts into or "
                           f"assigns sys.path; remove it from INSERT_BASELINE")
    return out


def converted_count(results: dict[str, dict], inserts: dict[str, list[int]]) -> int:
    """Tools whose module-level imports complete under -I and whose own source has no
    ``sys.path`` insert or assignment (a tool it loads by path is not read)."""
    return sum(1 for n, r in results.items() if r["status"] == "ok" and not inserts.get(n))


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
        native, database = Path(tmp) / "native", Path(tmp) / "database"
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
            # A sibling miss that the tool swallows, followed by another failure.
            "miss_then_raises.py": "try:\n    import helper_mod\nexcept ImportError:\n    pass\n"
                                   "raise RuntimeError('module-level failure')\n",
            # `import ctypes` raises ctypes.dlopen before a native call can run.
            "native_caller.py": "import ctypes\nctypes.CDLL(None).system("
                                f"{'touch ' + str(native)!r}.encode())\n",
            "sqlite_user.py": f"import sqlite3\nsqlite3.connect({str(database)!r})\n",
            # The event name only: a real fork_exec reaches it from subprocess internals.
            "fork_execer.py": "import sys\nsys.audit('_posixsubprocess.fork_exec')\n",
            # A lazy insert of the tool's own directory, aliased sys, and a slice assignment.
            "lazy_insert.py": "import sys as _sys\ndef _engine():\n"
                              "    _sys.path.insert(0, 'x')\n",
            "slice_assign.py": "from sys import path\npath[:0] = ['x']\n",
            # An augmented slice assignment and a reordering method.
            "aug_assign.py": "import sys\nsys.path[:0] += ['x']\n",
            "reorders.py": "import sys\nsys.path.reverse()\nsys.path.reverse()\n",
            # The one accepted form, an order-preserving filter of sys.path (any number
            # of if clauses, by name or alias). It runs only when called, not in the probe.
            "path_filter_ok.py": "import sys\nimport sys as _s\nfrom sys import path as p\n"
                                 "def _scrub(bad):\n"
                                 "    sys.path[:] = [entry for entry in sys.path\n"
                                 "                   if not (entry in bad\n"
                                 "                           or entry.endswith('x'))]\n"
                                 "    _s.path[:] = [e for e in _s.path]\n"
                                 "    p[:] = [e for e in p if e if e != 'y']\n",
            # Near variants of that form: each one is still reported.
            "path_filter_transformed.py": "import sys\ndef _scrub():\n"
                                          "    sys.path[:] = [e.strip() for e in sys.path if e]\n"
                                          "    sys.path[:] = ['x' + e for e in sys.path]\n",
            "path_filter_other_list.py": "import sys\ndef _scrub(extra):\n"
                                         "    sys.path[:] = [e for e in extra if e]\n"
                                         "    sys.path[:] = [e for e in sys.path[1:] if e]\n",
            "path_filter_two_for.py": "import sys\ndef _scrub(extra):\n"
                                      "    sys.path[:] = [e for e in sys.path for _ in (1, 2)]\n"
                                      "    sys.path[:] = [e for e in sys.path if e "
                                      "for e in extra]\n",
            "path_slice_other.py": "import sys\ndef _scrub():\n"
                                   "    sys.path[:] = list(filter(None, sys.path))\n"
                                   "    sys.path[:] = (e for e in sys.path if e)\n"
                                   "    sys.path[:] = ['x', *sys.path]\n"
                                   "    sys.path[1:] = [e for e in sys.path if e]\n"
                                   "    sys.path[::1] = [e for e in sys.path if e]\n"
                                   "    sys.path[:] = {e for e in sys.path if e}\n",
            "path_insert.py": "import sys\ndef _engine():\n    sys.path.insert(0, 'x')\n",
            "path_rebind.py": "import sys\ndef _scrub():\n"
                              "    sys.path = [e for e in sys.path if e]\n"
                              "    sys.path = ['x']\n",
            # The accepted value in a statement that is not a plain one-target assignment,
            # an async comprehension, and an insert called inside an accepted condition.
            "path_filter_not_plain.py": "import sys\ndef _scrub():\n"
                                        "    sys.path[:]: list = [e for e in sys.path if e]\n"
                                        "    kept = sys.path[:] = [e for e in sys.path if e]\n"
                                        "async def _a():\n"
                                        "    sys.path[:] = [e async for e in sys.path]\n"
                                        "    sys.path[:] = [e for e in sys.path\n"
                                        "                   if sys.path.insert(0, 'x') or e]\n",
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
            "miss_then_raises.py": "error", "native_caller.py": "error", "sqlite_user.py": "error",
            "fork_execer.py": "error", "lazy_insert.py": "ok", "slice_assign.py": "ok",
            "aug_assign.py": "ok", "reorders.py": "ok", "path_filter_ok.py": "ok",
            "path_filter_transformed.py": "ok", "path_filter_other_list.py": "ok",
            "path_filter_two_for.py": "ok", "path_slice_other.py": "ok", "path_insert.py": "ok",
            "path_rebind.py": "ok", "path_filter_not_plain.py": "ok",
        })
        check("needs_sibling missed", results["needs_sibling.py"]["missed"], ["helper_mod"])
        check("swallowed missed", results["swallowed.py"]["missed"], ["helper_mod"])
        check("miss_then_raises missed", results["miss_then_raises.py"]["missed"], ["helper_mod"])
        check("writer refused", results["writer.py"]["refused"], ["open"])
        check("spawner refused", results["spawner.py"]["refused"], ["subprocess.Popen"])
        check("execer refused", results["execer.py"]["refused"], ["os.exec"])
        check("remover refused", results["remover.py"]["refused"], ["os.remove"])
        check("native_caller refused", results["native_caller.py"]["refused"], ["ctypes.dlopen"])
        check("sqlite_user refused", results["sqlite_user.py"]["refused"], ["sqlite3.connect"])
        check("fork_execer refused", results["fork_execer.py"]["refused"],
              ["_posixsubprocess.fork_exec"])
        check("planted json error", results["uses_json_insert.py"]["error"],
              "RuntimeError: planted json.py imported")
        check("nothing written", written.exists(), False)
        check("nothing spawned", spawned.exists(), False)
        check("no native call", native.exists(), False)
        check("no database created", database.exists(), False)
        check("remover kept", (tools / "remover.py").is_file(), True)
        plain = probe(tools / "needs_sibling.py", isolated=False)
        check("plain launch resolves the sibling", (plain["status"], plain["missed"]), ("ok", []))

        inserts = inserts_all(tools)
        check("inserts", {n: v for n, v in inserts.items() if v}, {
            "uses_json_insert.py": [3], "lazy_insert.py": [3], "slice_assign.py": [2],
            "aug_assign.py": [2], "reorders.py": [2, 3],
            "path_filter_transformed.py": [3, 4], "path_filter_other_list.py": [3, 4],
            "path_filter_two_for.py": [3, 4], "path_slice_other.py": [3, 4, 5, 6, 7, 8],
            "path_insert.py": [3], "path_rebind.py": [3, 4],
            "path_filter_not_plain.py": [3, 4, 6, 8]})
        check("accepted filter", inserts["path_filter_ok.py"], [])
        check("converted", converted_count(results, inserts), 9)

        expected_unlisted = ["fork_execer.py", "json.py", "miss_then_raises.py",
                             "native_caller.py", "needs_sibling.py", "remover.py",
                             "sqlite_user.py", "swallowed.py", "uses_json_insert.py"]
        unlisted = findings_for(results, frozenset())
        check("empty baseline flags", [f.split(":")[0][len(".claude/skills/corpus-management/tools/"):] for f in unlisted],
              expected_unlisted)
        listed = frozenset({"needs_sibling.py", "swallowed.py"})
        check("baselined failures pass", [f for f in findings_for(results, listed)
                                          if "needs_sibling" in f or "swallowed" in f], [])
        stale = findings_for(results, listed | {"plain_ok.py", "ghost.py", "remover.py",
                                                "miss_then_raises.py"})
        check("stale baseline entries", [f for f in stale if "BASELINE" in f], [
            ".claude/skills/corpus-management/tools/ghost.py: on BASELINE but there is no such .claude/skills/corpus-management/tools/*.py; remove it",
            ".claude/skills/corpus-management/tools/miss_then_raises.py: on BASELINE, but its module-level code raised "
            "RuntimeError: module-level failure under python3 -I (refused: [], "
            "sibling miss ['helper_mod'])",
            ".claude/skills/corpus-management/tools/plain_ok.py: on BASELINE but now imports under -I; remove it from BASELINE",
            ".claude/skills/corpus-management/tools/remover.py: on BASELINE, but its module-level code raised PermissionError: "
            "isolated-launch probe refused os.remove under python3 -I (refused: ['os.remove'])",
        ])
        only_ok = {n: results[n] for n in ("plain_ok.py", "lazy_insert.py", "slice_assign.py")}
        # The path_* filter fixtures are checked through "inserts" above.
        older = {n: v for n, v in inserts.items() if not n.startswith("path_")}
        check("unlisted inserts flagged", findings_for(only_ok, frozenset(), older, frozenset({
            "uses_json_insert.py", "plain_ok.py", "ghost.py"})), [
            ".claude/skills/corpus-management/tools/aug_assign.py:2: inserts into or assigns sys.path (lines [2]), which can put "
            "a directory ahead of the standard library; append to the end of sys.path instead",
            ".claude/skills/corpus-management/tools/ghost.py: on INSERT_BASELINE but there is no such .claude/skills/corpus-management/tools/*.py; remove it",
            ".claude/skills/corpus-management/tools/lazy_insert.py:3: inserts into or assigns sys.path (lines [3]), which can put "
            "a directory ahead of the standard library; append to the end of sys.path instead",
            ".claude/skills/corpus-management/tools/plain_ok.py: on INSERT_BASELINE but no longer inserts into or assigns "
            "sys.path; remove it from INSERT_BASELINE",
            ".claude/skills/corpus-management/tools/reorders.py:2: inserts into or assigns sys.path (lines [2, 3]), which can put "
            "a directory ahead of the standard library; append to the end of sys.path instead",
            ".claude/skills/corpus-management/tools/slice_assign.py:2: inserts into or assigns sys.path (lines [2]), which can put "
            "a directory ahead of the standard library; append to the end of sys.path instead",
        ])
    for failure in failures:
        print(f"SELF-TEST FAIL: {failure}")
    if failures:
        return 1
    print("SELF-TEST OK: outcomes, refusals, planted-shadow, sys.path inserts and both baseline "
          "ratchets behave as documented")
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
        inserts = inserts_all(TOOLS_DIR)
        results = probe_all(TOOLS_DIR)
    except ProbeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    scope = ("(this checks module-level imports under python3 -I, not a full command launch)")
    findings = findings_for(results, BASELINE, inserts, INSERT_BASELINE)
    if findings:
        for finding in findings:
            print(finding)
        print(f"\nFAIL: {len(findings)} isolated-launch finding(s) {scope}.")
        return 1
    print(f"OK: {converted_count(results, inserts)} of {len(results)} .claude/skills/corpus-management/tools/*.py complete their "
          f"module-level imports under python3 -I and have no sys.path insert in their own "
          f"source (a tool loaded by path is not read); "
          f"{len(BASELINE)} on BASELINE (sibling import fails), {len(INSERT_BASELINE)} on "
          f"INSERT_BASELINE (sys.path insert or assignment) {scope}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
